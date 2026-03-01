# src/routes/ingestion.py
"""
Document ingestion endpoint for the Stripe RAG Agent.

This module handles triggering the document ingestion pipeline
that parses raw documentation files and populates the vector store.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks

from src.ingestion import ingest_documents

router = APIRouter()


@router.post("/ingest", status_code=202)
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
