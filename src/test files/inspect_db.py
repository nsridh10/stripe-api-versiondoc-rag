# src/test files/inspect_db.py
"""
ChromaDB inspection utility.

Fetches all chunks from the ChromaDB vector store and exports them to a
readable Markdown file for debugging and visualization.

Usage:
    cd /Users/navein/stripe-rag-agent
    source venv/bin/activate
    python -m "src.test files.inspect_db"

Output:
    Creates chunk_visualization.md in the project root with all chunks formatted.
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import chromadb
import json
from src.config import config


def inspect_chroma():
    """Fetches all chunks from ChromaDB and exports them to a readable Markdown file."""
    persist_dir = project_root / config["services"]["vector_db"]["persist_directory"]
    
    print(f"Connecting to ChromaDB at: {persist_dir}")
    client = chromadb.PersistentClient(path=str(persist_dir))
    
    # LangChain defaults to naming the collection 'langchain'
    collection_name = "langchain"
    
    try:
        collection = client.get_collection(name=collection_name)
    except Exception as e:
        print(f"Error accessing collection '{collection_name}': {e}")
        print("Available collections:", [c.name for c in client.list_collections()])
        return

    # Fetch everything in the database
    data = collection.get(include=["metadatas", "documents"])
    total_chunks = len(data['ids'])
    
    if total_chunks == 0:
        print("The database is empty. Did ingestion run successfully?")
        return
        
    print(f"Successfully retrieved {total_chunks} chunks.")
    
    # Export to a Markdown file for easy visualization
    output_file = project_root / "chunk_visualization.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# ChromaDB Chunk Dump\n**Total Chunks:** {total_chunks}\n\n---\n\n")
        
        for i in range(total_chunks):
            f.write(f"### Chunk {i+1} | ID: `{data['ids'][i]}`\n\n")
            
            # Format metadata nicely
            meta = data['metadatas'][i]
            f.write("**Metadata:**\n```json\n")
            f.write(json.dumps(meta, indent=2))
            f.write("\n```\n\n")
            
            # Write the actual chunk content
            f.write("**Content:**\n")
            f.write(f"> {data['documents'][i].replace(chr(10), chr(10) + '> ')}\n\n")
            f.write("---\n\n")

    print(f"\n✅ Done! Open '{output_file}' in your IDE to visualize the chunks.")


if __name__ == "__main__":
    inspect_chroma()
