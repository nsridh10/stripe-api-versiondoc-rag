# src/ingestion.py
import chromadb
from src.config import get_file_mappings
from src.dependencies import get_vector_store
from src.parsers import ParserFactory
from src.config import config

def ingest_documents():
    """Reads configuration, dynamically parses files, and loads them into ChromaDB."""
    print("🧹 Cleaning up old vector data...")
    persist_dir = config["services"]["vector_db"]["persist_directory"]
    
    # Use the native chromadb client to wipe the collection
    client = chromadb.PersistentClient(path=persist_dir)
    try:
        # LangChain's Chroma wrapper defaults to the name 'langchain'
        client.delete_collection(name="langchain")
        print("✅ Collection cleared.")
    except Exception:
        print("ℹ️ No existing collection found to clear. Starting fresh.")

    print("Starting ingestion process...")
    vector_store = get_vector_store()
    file_mappings = get_file_mappings()
    
    # Read the mode from config
    chunking_mode = config.get("ingestion", {}).get("chunking_mode", "large")
    print(f"Running in '{chunking_mode}' chunking mode.")
    
    all_chunks = []

    for file_info in file_mappings:
        file_path = file_info["path"]
        fmt = file_info.get("format", "md")
        
        print(f"Processing: {file_path} via {fmt.upper()} Parser")
        
        # 1. Get the dynamic parser
        parser = ParserFactory.get_parser(fmt, mode=chunking_mode)
        
        # 2. Define the strict metadata for this file
        base_metadata = {
            "api_class": file_info["api_class"],
            "version": file_info["version"],
            "source_file": file_info["path"]
        }
        
        # 3. Parse and chunk
        chunks = parser.parse(file_path, base_metadata)
        all_chunks.extend(chunks)
        
    if all_chunks:
        print(f"Adding {len(all_chunks)} structure-aware chunks to the vector database...")
        vector_store.add_documents(all_chunks)
        print("Ingestion complete!")
    else:
        print("No documents were processed.")

if __name__ == "__main__":
    ingest_documents()