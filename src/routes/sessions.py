# src/routes/sessions.py
"""
Session management endpoints for the Stripe RAG Agent.

This module handles all session-related endpoints including:
- Get session info
- Get session messages
- List all sessions
- Clear session
- Clear all sessions
"""
from fastapi import APIRouter, HTTPException
from typing import List

from langchain_core.messages import HumanMessage, AIMessage

from src.config import config
from src.memory import get_conversation_memory
from src.routes.models import (
    SessionMetadataResponse,
    SessionListItem,
    MessageItem,
)

router = APIRouter()

# Initialize conversation memory based on config
memory_config = config.get("services", {}).get("memory", {})
memory_provider = memory_config.get("provider", "in-memory")
conversation_memory = get_conversation_memory(
    provider=memory_provider,
    db_path=memory_config.get("sqlite_db_path", "data/conversation_memory.db")
)


@router.get("/session/{session_id}", response_model=SessionMetadataResponse)
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


@router.delete("/session/{session_id}")
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


@router.get("/sessions", response_model=List[SessionListItem])
async def list_sessions():
    """List all conversation sessions for the chat history panel."""
    try:
        sessions = conversation_memory.list_sessions()
        return [SessionListItem(**s) for s in sessions]
    except Exception as e:
        print(f"[API Error] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions")
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


@router.get("/session/{session_id}/messages", response_model=List[MessageItem])
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
