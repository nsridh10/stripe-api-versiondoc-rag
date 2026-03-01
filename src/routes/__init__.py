# src/routes/__init__.py
"""
FastAPI Routes for the Stripe RAG Agent.

This module aggregates all route handlers into a single router
that can be included in the main FastAPI application.

Modules:
- query.py: Main query endpoint for RAG agent
- sessions.py: Session management endpoints
- ingestion.py: Document ingestion endpoint
- models.py: Pydantic request/response models
"""

from fastapi import APIRouter

from src.routes.query import router as query_router
from src.routes.sessions import router as sessions_router
from src.routes.ingestion import router as ingestion_router

# Create main router that includes all sub-routers
router = APIRouter()

router.include_router(query_router, tags=["Query"])
router.include_router(sessions_router, tags=["Sessions"])
router.include_router(ingestion_router, tags=["Ingestion"])

__all__ = ["router"]
