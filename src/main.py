# src/main.py
"""
Stripe RAG Agent - FastAPI Application Entry Point

This module initializes the FastAPI application and includes all route handlers.
The actual route implementations are in the routes/ directory.

Run with: uvicorn src.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import router
from src.config import config
from src.memory import get_conversation_memory

# ---------------------------------------------------------------------------
# Initialize Conversation Memory
# ---------------------------------------------------------------------------
# This is initialized here so it can be used by the routes module.
# Due to Python's module caching, routes will get the same instance.
memory_config = config.get("services", {}).get("memory", {})
memory_provider = memory_config.get("provider", "in-memory")
conversation_memory = get_conversation_memory(
    provider=memory_provider,
    db_path=memory_config.get("sqlite_db_path", "data/conversation_memory.db")
)

# ---------------------------------------------------------------------------
# FastAPI Application Setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Stripe RAG Agent API",
    description="An intelligent agent that queries multi-version Stripe API documentation with conversation memory.",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------------------------
@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Stripe RAG Agent"}


# ---------------------------------------------------------------------------
# Include Route Handlers
# ---------------------------------------------------------------------------
# All routes are defined in src/routes/ and aggregated into a single router
app.include_router(router)
