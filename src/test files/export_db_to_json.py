# src/test files/export_db_to_json.py
"""
Export ChromaDB contents to JSON for enrichment.

This script exports all chunks from the ChromaDB vector store to a JSON file
that can be processed by an LLM to add enrichment data (summaries, keywords,
hypothetical questions).

Usage:
    cd /Users/navein/stripe-rag-agent
    source venv/bin/activate
    python -m src.test\ files.export_db_to_json

Output:
    Creates data/db_dump.json with all chunks and placeholder enrichment fields.
"""
import json
import sys
import os
from pathlib import Path

# Add project root to Python path
# Note: This file is in src/test files/, so we need to go up 3 levels to project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import chromadb
import chromadb.errors
from src.config import config


def export_db():
    """
    Exports ChromaDB collection contents to a JSON file.
    
    Creates a JSON file with all document chunks and placeholder fields
    for enrichment data that can be filled in using an LLM.
    """
    persist_dir = project_root / config["services"]["vector_db"]["persist_directory"]
    client = chromadb.PersistentClient(path=str(persist_dir))
    
    try:
        collection = client.get_collection(name="langchain")
    except chromadb.errors.NotFoundError:
        print("❌ ChromaDB collection 'langchain' does not exist!")
        print("\nYou need to run the ingestion script first to populate the database:")
        print("  cd /Users/navein/stripe-rag-agent")
        print("  source venv/bin/activate")
        print("  python3 -m src.ingestion")
        print("\nOr make an API call to trigger ingestion:")
        print("  curl -X POST http://localhost:8000/ingest")
        return
    
    data = collection.get(include=["metadatas", "documents"])
    total_chunks = len(data['ids'])
    
    if total_chunks == 0:
        print("Database is empty!")
        return
        
    export_data = []
    for i in range(total_chunks):
        export_data.append({
            "chunk_id": data['ids'][i],
            "metadata": data['metadatas'][i],
            "content": data['documents'][i],
            # Placeholders for you to fill in using the LLM UI
            "enriched_summary": "",
            "enriched_keywords": [],
            "enriched_questions": []
        })
    
    output_path = project_root / "data" / "db_dump.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)
        
    print(f"✅ Exported {total_chunks} chunks to '{output_path}'.")
    print("Take this file to your LLM UI, ask it to fill in the 'enriched_' fields, and save the result as 'data/enriched_db.json'.")


if __name__ == "__main__":
    export_db()
