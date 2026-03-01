# src/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from langchain_core.messages import HumanMessage

# Import the compiled LangGraph workflow
from src.agent import app_graph
# Import the ingestion function
from src.ingestion import ingest_documents
# Import conversation memory
from src.memory import get_conversation_memory
from src.config import config

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

class QueryResponse(BaseModel):
    answer: str
    session_id: str

class SessionMetadataResponse(BaseModel):
    session_id: str
    created_at: str
    last_accessed: str
    message_count: int

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
async def query_agent(request: QueryRequest):
    """
    Takes a natural language query, passes it to the LangGraph agent with conversation context,
    and returns the synthesized response.
    
    Supports multi-turn conversations via session_id.
    """
    try:
        # Generate or use provided session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get conversation history for context
        context_window = config.get("services", {}).get("memory", {}).get("context_window", 5)
        previous_messages = conversation_memory.get_messages(session_id, limit=context_window * 2)
        
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
        
        print(f"[API] Intent detected: {intent_type}")
        
        # Handle session management based on intent
        if intent_type == "new_intent" and previous_messages:
            # User started a completely new topic/intent
            # Clear old session and create new one for clean context
            print(f"[API] New intent detected. Creating fresh session...")
            old_session_id = session_id
            session_id = str(uuid.uuid4())  # Generate new session ID
            print(f"[API] Session switched: {old_session_id} → {session_id}")
            # Save to the new session (fresh context — only this turn's record)
            conversation_memory.add_messages(session_id, [new_user_message, final_message])
            # Start fresh operation log with only the current turn
            new_session_context = updated_context[-1:] if updated_context else []
            conversation_memory.set_context(session_id, new_session_context)
            # Carry the scope derived from the current turn
            conversation_memory.set_scope(session_id, updated_scope)
        else:
            # Follow-up or first query - save to existing/current session
            conversation_memory.add_messages(session_id, [new_user_message, final_message])
            conversation_memory.set_context(session_id, updated_context)
            conversation_memory.set_scope(session_id, updated_scope)
        
        return QueryResponse(answer=final_answer, session_id=session_id)
        
    except Exception as e:
        print(f"[API Error] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


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