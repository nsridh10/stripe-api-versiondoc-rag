# src/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any
import uuid
from langchain_core.messages import HumanMessage, AIMessage, messages_to_dict

# Import the compiled LangGraph workflow
from src.agent import app_graph, MAX_TOOL_CALLS
# Import the ingestion function
from src.ingestion import ingest_documents
# Import conversation memory
from src.memory import get_conversation_memory
from src.config import config
# Import trace system
from src.trace import TraceCollector, set_trace, get_trace
# Import LLM setup for per-request API keys
from src.dependencies import get_llm, set_llm

# Initialize conversation memory based on config
memory_config = config.get("services", {}).get("memory", {})
memory_provider = memory_config.get("provider", "in-memory")
conversation_memory = get_conversation_memory(
    provider=memory_provider,
    db_path=memory_config.get("sqlite_db_path", "data/conversation_memory.db")
)

# Initialize FastAPI
app = FastAPI(
    title="Stripe RAG Agent API",
    description="An intelligent agent that queries multi-version Stripe API documentation with conversation memory.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None  # Optional: if not provided, creates new session

# ---------------------------------------------------------------------------
# Enriched Response Models
# ---------------------------------------------------------------------------

class SourceChunk(BaseModel):
    """A single retrieved documentation chunk."""
    section: str              # Header hierarchy, e.g. "Create a Customer > Parameters"
    similarity_score: float   # 0-1, higher = more relevant
    content_preview: str      # First ~300 chars of chunk content
    source_file: Optional[str] = None  # Raw file path this chunk came from (from vector metadata)

class ToolCallSource(BaseModel):
    """Source documents retrieved by a single tool call."""
    api_class: str            # e.g. "CUSTOMERS"
    version: str              # e.g. "v2", "latest"
    query: str                # The semantic search query used
    source_file: str          # Raw file path, e.g. "data/raw/CUSTOMERS.md"
    status: str               # "found" | "not_found" | "error"
    chunks: List[SourceChunk] # Retrieved chunks (empty if not_found)

class TraceNodeExecution(BaseModel):
    """A single graph node execution record."""
    node: str
    start_time: str
    end_time: str
    duration_ms: float
    input_details: dict       # What the node received / decided at entry
    output_details: dict      # What the node produced / decided at exit

class TraceRoutingDecision(BaseModel):
    """A conditional edge routing decision."""
    from_node: str
    to_node: str
    reason: str
    timestamp: str

class ExecutionTrace(BaseModel):
    """Full LangGraph execution trace for a single query."""
    total_duration_ms: float
    nodes_executed: List[TraceNodeExecution]
    routing_decisions: List[TraceRoutingDecision]
    query_tracker: List[dict]     # Final state of all sub-queries
    plan: List[dict]              # The planner's original retrieval plan
    tool_call_budget_used: int
    tool_call_budget_max: int

class MessageItem(BaseModel):
    """A single message in the conversation."""
    role: str                     # "user" | "assistant"
    content: str

class QueryResponse(BaseModel):
    """Enriched response with answer, sources, and execution trace."""
    message_type: str             # "answer" | "clarification" | "error"
    answer: str                   # The synthesized markdown answer
    session_id: str
    sources: List[ToolCallSource] # Documents used to generate the answer
    execution_trace: ExecutionTrace  # Full graph execution details

class SessionMetadataResponse(BaseModel):
    session_id: str
    created_at: str
    last_accessed: str
    message_count: int
    context_start: int = 0

class SessionListItem(BaseModel):
    session_id: str
    created_at: str
    last_accessed: str
    message_count: int
    preview: str                  # First user message (truncated)

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "Stripe RAG Agent"}

@app.post("/ingest", status_code=202)
async def trigger_ingestion(background_tasks: BackgroundTasks):
    """
    Triggers the document ingestion pipeline in the background.
    Returns a 202 Accepted immediately while parsing happens asynchronously.
    """
    try:
        background_tasks.add_task(ingest_documents)
        return {
            "status": "accepted", 
            "message": "Ingestion process has been started in the background. Check server logs for completion."
        }
    except Exception as e:
        print(f"[API Error] Failed to start ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_agent(
    request: QueryRequest,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    Takes a natural language query, passes it to the LangGraph agent with conversation context,
    and returns the synthesized response with source documents and execution trace.
    
    Pass your Groq API key in the X-API-Key header.
    """
    try:
        # --- Set up per-request LLM with user's API key ---
        try:
            llm = get_llm(api_key=x_api_key)
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
            "active_scope": active_scope
        }
        
        print(f"\n[API] Session: {session_id} | Query: {request.query}")
        if previous_messages:
            print(f"[API] Using {len(previous_messages)} previous messages for context")
        
        result = app_graph.invoke(initial_state)
        
        # Extract final answer and intent classification
        final_message = result["messages"][-1]
        final_answer = final_message.content
        intent_type = result.get("intent_type", "new_intent")
        updated_context = result.get("conversation_context") or []
        updated_scope = result.get("active_scope")
        
        # Determine message type
        needs_clarification = result.get("needs_clarification", False)
        message_type = "clarification" if needs_clarification else "answer"
        
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


@app.get("/session/{session_id}", response_model=SessionMetadataResponse)
async def get_session_info(session_id: str):
    """Get metadata about a conversation session."""
    try:
        if not conversation_memory.session_exists(session_id):
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        metadata = conversation_memory.get_session_metadata(session_id)
        return SessionMetadataResponse(**metadata)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API Error] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear all messages from a conversation session."""
    try:
        if not conversation_memory.session_exists(session_id):
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        conversation_memory.clear_session(session_id)
        return {"status": "success", "message": f"Session {session_id} cleared"}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API Error] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions", response_model=List[SessionListItem])
async def list_sessions():
    """List all conversation sessions for the chat history panel."""
    try:
        sessions = conversation_memory.list_sessions()
        return [SessionListItem(**s) for s in sessions]
    except Exception as e:
        print(f"[API Error] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/sessions")
async def clear_all_sessions():
    """Clear ALL sessions. Called on frontend page refresh to start fresh."""
    try:
        sessions = conversation_memory.list_sessions()
        count = 0
        for s in sessions:
            conversation_memory.clear_session(s["session_id"])
            count += 1
        print(f"[API] Cleared all {count} session(s)")
        return {"status": "success", "cleared": count}
    except Exception as e:
        print(f"[API Error] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/session/{session_id}/messages", response_model=List[MessageItem])
async def get_session_messages(session_id: str):
    """
    Get all messages in a session for rendering chat history.
    Returns messages in chronological order with role and content.
    """
    try:
        if not conversation_memory.session_exists(session_id):
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        raw_messages = conversation_memory.get_messages(session_id)
        messages = []
        for msg in raw_messages:
            if isinstance(msg, HumanMessage):
                messages.append(MessageItem(role="user", content=msg.content))
            elif isinstance(msg, AIMessage):
                messages.append(MessageItem(role="assistant", content=msg.content))
            # Skip system/tool messages — not relevant for chat display
        return messages
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API Error] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))