# src/routes/query.py
"""
Query endpoint for the Stripe RAG Agent.

This module handles the main /query endpoint that processes natural language
queries through the LangGraph agent workflow.
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
import uuid

from langchain_core.messages import HumanMessage

from src.agent import app_graph, MAX_TOOL_CALLS
from src.config import config
from src.trace import TraceCollector, set_trace
from src.dependencies import get_llm, set_llm
from src.graph.nodes import _extract_content_str
from src.routes.models import (
    QueryRequest,
    QueryResponse,
    SourceChunk,
    ToolCallSource,
    ExecutionTrace,
    TraceNodeExecution,
    TraceRoutingDecision,
)

# Import conversation memory - initialized in main.py but we need to import the getter
from src.memory import get_conversation_memory

router = APIRouter()

# Initialize conversation memory based on config
# This will be the same instance as in main.py due to module caching
memory_config = config.get("services", {}).get("memory", {})
memory_provider = memory_config.get("provider", "in-memory")
conversation_memory = get_conversation_memory(
    provider=memory_provider,
    db_path=memory_config.get("sqlite_db_path", "data/conversation_memory.db")
)


@router.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Takes a natural language query, passes it to the LangGraph agent with conversation context,
    and returns the synthesized response with source documents and execution trace.
    
    Requires provider, model, and api_key to be provided in the request body.
    """
    try:
        # --- Set up per-request LLM with user's credentials ---
        try:
            llm = get_llm(
                provider=request.provider,
                model=request.model,
                api_key=request.api_key,
                temperature=0.0
            )
            set_llm(llm)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # --- Set up per-request trace collector ---
        trace_collector = TraceCollector()
        set_trace(trace_collector)

        # Generate or use provided session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get conversation history for agent context.
        # Only use messages from the current RAG "segment" (after context_start)
        # so that a session with multiple intent switches doesn't confuse the agent.
        context_window = config.get("services", {}).get("memory", {}).get("context_window", 5)
        context_start = conversation_memory.get_context_start(session_id)
        all_stored_messages = conversation_memory.get_messages(session_id)
        relevant_messages = all_stored_messages[context_start:]  # Only current segment
        previous_messages = relevant_messages[-(context_window * 2):]  # Apply window
        
        # Load structured operation log from prior turns
        conversation_context = conversation_memory.get_context(session_id)
        
        # Load active scope (api_classes + versions being discussed)
        active_scope = conversation_memory.get_scope(session_id)
        
        # Add new user message
        new_user_message = HumanMessage(content=request.query)
        
        # Combine history + new message for agent
        all_messages = previous_messages + [new_user_message]
        
        initial_state = {
            "messages": all_messages,
            "tool_call_budget": 0,
            "needs_clarification": False,
            "tool_plan": None,
            "rephrase_count": 0,
            "intent_type": None,
            "conversation_context": conversation_context or None,
            "active_scope": active_scope,
            "query_tracker": None,
            "restructurer_analysis": None,
            "frontier_result": None,
            "is_rejected": False,
        }
        
        print(f"\n[API] Session: {session_id} | Query: {request.query}")
        if previous_messages:
            print(f"[API] Using {len(previous_messages)} previous messages for context")
        
        result = app_graph.invoke(initial_state)
        
        # Extract final answer and intent classification
        final_message = result["messages"][-1]
        final_answer = _extract_content_str(final_message.content)
        intent_type = result.get("intent_type", "new_intent")
        updated_context = result.get("conversation_context") or []
        updated_scope = result.get("active_scope")
        
        # Determine message type (rejected, clarification, or answer)
        is_rejected = result.get("is_rejected", False)
        needs_clarification = result.get("needs_clarification", False)
        if is_rejected:
            message_type = "rejected"
            frontier_result = result.get("frontier_result")
            rejection_type = frontier_result.get("rejection_type") if frontier_result else None
            print(f"[API] Request REJECTED: {rejection_type}")
        elif needs_clarification:
            message_type = "clarification"
        else:
            message_type = "answer"
        
        print(f"[API] Intent detected: {intent_type} | Message type: {message_type}")
        
        # Handle session management based on intent.
        # The session_id is NEVER changed — the frontend always sees the same
        # session with all messages. When a new intent is detected, we only
        # reset the internal RAG context (operation log, scope) and advance
        # the context_start so the agent only reads messages from the current
        # topic on subsequent turns.
        if intent_type == "new_intent" and previous_messages:
            # Advance context_start to skip old-topic messages for future agent calls
            current_msg_count = len(conversation_memory.get_messages(session_id))
            conversation_memory.set_context_start(session_id, current_msg_count)
            print(f"[API] New intent detected. Context boundary advanced to index {current_msg_count} (session stays: {session_id})")
            conversation_memory.add_messages(session_id, [new_user_message, final_message])
            # Fresh operation log — only current turn's record
            new_session_context = updated_context[-1:] if updated_context else []
            conversation_memory.set_context(session_id, new_session_context)
            conversation_memory.set_scope(session_id, updated_scope)
        else:
            # Follow-up or first query — append normally
            conversation_memory.add_messages(session_id, [new_user_message, final_message])
            conversation_memory.set_context(session_id, updated_context)
            conversation_memory.set_scope(session_id, updated_scope)
        
        # --- Build enriched source documents ---
        sources = []
        for src in trace_collector.sources:
            source_chunks = [
                SourceChunk(
                    section=c.get("section", ""),
                    similarity_score=c.get("similarity_score", 0.0),
                    content_preview=c.get("content_preview", ""),
                    source_file=c.get("source_file")
                )
                for c in src.get("chunks", [])
            ]
            sources.append(ToolCallSource(
                api_class=src["api_class"],
                version=src["version"],
                query=src["query"],
                source_file=src["source_file"],
                status=src["status"],
                chunks=source_chunks
            ))

        # --- Build execution trace ---
        query_tracker = result.get("query_tracker") or []
        # Extract plan from the trace events (planner's output)
        plan = []
        for ev in trace_collector.events:
            if ev["type"] == "node_end" and ev["node"] == "planner":
                plan = ev.get("details", {}).get("plan", [])
                break

        raw_trace = trace_collector.to_dict(
            tool_call_budget_used=result.get("tool_call_budget", 0),
            tool_call_budget_max=MAX_TOOL_CALLS,
            query_tracker=query_tracker,
            plan=plan
        )

        execution_trace = ExecutionTrace(
            total_duration_ms=raw_trace["total_duration_ms"],
            nodes_executed=[
                TraceNodeExecution(**n) for n in raw_trace["nodes_executed"]
            ],
            routing_decisions=[
                TraceRoutingDecision(**r) for r in raw_trace["routing_decisions"]
            ],
            query_tracker=raw_trace["query_tracker"],
            plan=raw_trace["plan"],
            tool_call_budget_used=raw_trace["tool_call_budget_used"],
            tool_call_budget_max=raw_trace["tool_call_budget_max"]
        )

        return QueryResponse(
            message_type=message_type,
            answer=final_answer,
            session_id=session_id,
            sources=sources,
            execution_trace=execution_trace
        )
        
    except HTTPException:
        # Re-raise HTTPExceptions (like 400 for missing API key)
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[API Error] {error_msg}")
        import traceback
        traceback.print_exc()
        
        # Detect specific error types for better frontend messages
        error_lower = error_msg.lower()
        if "rate_limit" in error_lower or "rate limit" in error_lower or "429" in error_lower:
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded on Groq API. Please wait a moment and try again. Details: {error_msg}"
            )
        elif "invalid_api_key" in error_lower or "invalid api key" in error_lower or "401" in error_lower:
            raise HTTPException(
                status_code=401, 
                detail=f"Invalid API key. Please check your Groq API key and try again."
            )
        elif "authentication" in error_lower:
            raise HTTPException(
                status_code=401, 
                detail=f"Authentication failed. Please check your API key. Details: {error_msg}"
            )
        else:
            raise HTTPException(status_code=500, detail=error_msg)
