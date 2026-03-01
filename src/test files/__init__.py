# src/test files/__init__.py
"""
Test and utility scripts for the Stripe RAG Agent.

This directory contains scripts used for testing, data management, and
database maintenance. These are not part of the main application flow.

Available scripts:
- export_db_to_json.py: Export ChromaDB contents for enrichment
- reingest_enriched.py: Re-ingest enriched data back into ChromaDB
- inspect_db.py: Visualize ChromaDB chunks as Markdown
- test_session.py: End-to-end session continuity tests
- demo_memory.py: Demo script for conversation memory features

Usage:
    cd /Users/navein/stripe-rag-agent
    source venv/bin/activate
    python -m "src.test files.export_db_to_json"
    python -m "src.test files.reingest_enriched"
    python -m "src.test files.inspect_db"
    python -m "src.test files.test_session"
    python -m "src.test files.demo_memory"
"""
