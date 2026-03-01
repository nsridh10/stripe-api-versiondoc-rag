# src/dependencies.py
import os
import threading
from pathlib import Path
from src.config import config
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores import VectorStore

# Get project root directory
project_root = Path(__file__).parent.parent

# Singleton cache for embeddings to avoid reloading model on every call
_embeddings_cache = None
_embeddings_lock = threading.Lock()

def get_embeddings() -> Embeddings:
    """Returns the configured embedding provider. Cached as singleton to avoid reloading."""
    global _embeddings_cache
    
    # Double-checked locking pattern for thread-safe singleton
    if _embeddings_cache is not None:
        return _embeddings_cache
    
    with _embeddings_lock:
        # Check again inside lock in case another thread initialized it
        if _embeddings_cache is not None:
            return _embeddings_cache
        
        provider = config["services"]["embedding"]["provider"].lower()
        model_name = config["services"]["embedding"]["model_name"]
        
        print(f"[Embeddings] Loading {provider} model: {model_name}")
        
        if provider == "huggingface":
            # Uses the huggingface_hub backend
            from langchain_huggingface import HuggingFaceEmbeddings
            _embeddings_cache = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={'device': 'cpu'},  # Explicitly use CPU to avoid GPU issues
                encode_kwargs={'normalize_embeddings': True}
            )
            
        elif provider == "sentence-transformers":
            # Direct local sentence-transformers implementation
            from langchain_community.embeddings import SentenceTransformerEmbeddings
            _embeddings_cache = SentenceTransformerEmbeddings(model_name=model_name)
            
        elif provider == "openai":
            from langchain_openai import OpenAIEmbeddings
            if "OPENAI_API_KEY" not in os.environ:
                raise ValueError("OPENAI_API_KEY environment variable is missing. Please set it before running.")
            _embeddings_cache = OpenAIEmbeddings(model=model_name)
            
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")
        
        print(f"[Embeddings] Model loaded successfully")
        return _embeddings_cache

def get_llm() -> BaseChatModel:
    provider = config["services"]["llm"]["provider"].lower()
    model_name = config["services"]["llm"]["model_name"]
    temperature = config["services"]["llm"].get("temperature", 0.0)
    
    if provider == "groq":
        from langchain_groq import ChatGroq
        api_key = config["services"]["api_keys"].get("groq")
        return ChatGroq(model=model_name, temperature=temperature, groq_api_key=api_key)
    
    elif provider == "grok":
        from langchain_xai import ChatXAI
        api_key = config["services"]["api_keys"].get("grok")
        return ChatXAI(model=model_name, temperature=temperature, xai_api_key=api_key)
        
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        api_key = config["services"]["api_keys"].get("gemini")
        return ChatGoogleGenerativeAI(model=model_name, temperature=temperature, google_api_key=api_key)
        
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        api_key = config["services"]["api_keys"].get("openai")
        return ChatOpenAI(model=model_name, temperature=temperature, openai_api_key=api_key)
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

# Singleton cache for vector store to reuse connection
_vector_store_cache = None
_vector_store_lock = threading.Lock()

def get_vector_store() -> VectorStore:
    """Returns the configured vector database. Cached as singleton."""
    global _vector_store_cache
    
    # Double-checked locking pattern for thread-safe singleton
    if _vector_store_cache is not None:
        return _vector_store_cache
    
    with _vector_store_lock:
        # Check again inside lock in case another thread initialized it
        if _vector_store_cache is not None:
            return _vector_store_cache
        
        provider = config["services"]["vector_db"]["provider"].lower()
        persist_dir = config["services"]["vector_db"]["persist_directory"]
        
        # Ensure we use absolute path
        if not Path(persist_dir).is_absolute():
            persist_dir = str(project_root / persist_dir)
        
        print(f"[VectorStore] Initializing database at: {persist_dir}")
        
        if provider == "chroma":
            from langchain_chroma import Chroma
            _vector_store_cache = Chroma(
                collection_name="langchain",
                persist_directory=persist_dir,
                embedding_function=get_embeddings()  # This now returns cached embeddings
            )
            print(f"[VectorStore] Connected successfully")
            
        else:
            raise ValueError(f"Unsupported vector DB provider: {provider}")
        
        return _vector_store_cache