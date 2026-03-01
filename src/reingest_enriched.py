# src/reingest_enriched.py
import json
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import chromadb
from langchain_core.documents import Document
from src.dependencies import get_vector_store
from src.config import config, get_file_mappings

def _build_source_file_lookup() -> dict:
    """Build a (api_class, version) -> source_file path lookup from config."""
    lookup = {}
    for file_info in get_file_mappings():
        key = (file_info["api_class"], file_info["version"])
        lookup[key] = file_info["path"]
    return lookup

def reingest_enriched_data():
    enriched_file = project_root / "data" / "enriched_db.json"
    
    if not enriched_file.exists():
        print(f"Error: {enriched_file} not found.")
        return
        
    with open(enriched_file, "r", encoding="utf-8") as f:
        enriched_data = json.load(f)

    # Build source_file lookup from config
    source_lookup = _build_source_file_lookup()
    print(f"Source file lookup: {len(source_lookup)} entries")

    # 1. Clear the old database so we don't have duplicates
    print("Clearing old ChromaDB collection...")
    persist_dir = project_root / config["services"]["vector_db"]["persist_directory"]
    client = chromadb.PersistentClient(path=str(persist_dir))
    try:
        client.delete_collection(name="langchain")
        print("  ✓ Old collection deleted")
    except Exception as e:
        print(f"  ✓ No existing collection to delete ({type(e).__name__})")
    
    # Create fresh collection via get_vector_store()
    print("Creating new ChromaDB collection...")
    vector_store = get_vector_store()
    print("  ✓ Collection ready")
    new_documents = []
    
    # 2. Rebuild the documents, fusing the enrichment data into the content
    for idx, item in enumerate(enriched_data):
        try:
            raw_content = item["content"]
            meta = item["metadata"]
            
            # Inject source_file from config lookup
            key = (meta.get("api_class"), meta.get("version"))
            meta["source_file"] = source_lookup.get(key, "unknown")
            
            summary = item.get("enriched_summary", "")
            keywords = item.get("enriched_keywords", [])
            questions = item.get("enriched_questions", [])
            
            k_str = ", ".join(keywords) if isinstance(keywords, list) else keywords
            q_str = "\n- ".join(questions) if isinstance(questions, list) else questions
            if q_str and not q_str.startswith("-"): q_str = "- " + q_str
            
            # [THE MAGIC HAPPENS HERE]
            # FUSE the data into the page_content for maximum semantic search accuracy
            fused_content = f"""{raw_content}

---
[ENRICHED CONTEXT]
Summary: {summary}
Keywords: {k_str}
Hypothetical Questions Answered:
{q_str}
"""
            meta["summary"] = summary
            
            new_documents.append(Document(page_content=fused_content, metadata=meta))
        except KeyError as e:
            print(f"⚠️  Warning: Item {idx} is missing key {e}. Available keys: {list(item.keys())}")
            print(f"   Chunk ID: {item.get('chunk_id', 'unknown')}")
            continue
        
    # 3. Add to the fresh database
    if new_documents:
        print(f"Loading {len(new_documents)} supercharged chunks into ChromaDB...")
        vector_store.add_documents(new_documents)
        print(f"✅ Enriched re-ingestion complete! Processed {len(new_documents)}/{len(enriched_data)} chunks.")
    else:
        print("❌ No valid documents to ingest!")

if __name__ == "__main__":
    reingest_enriched_data()