# src/dependencies.py
import os
import threading
from contextvars import ContextVar
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

# Context variable for per-request LLM instance
_llm_context: ContextVar[BaseChatModel] = ContextVar("llm_context")

def set_llm(llm: BaseChatModel) -> None:
    """Set the LLM instance for the current request context."""
    _llm_context.set(llm)

def get_current_llm() -> BaseChatModel:
    """Get the LLM instance for the current request context."""
    try:
        return _llm_context.get()
    except LookupError:
        # No LLM set in context - raise clear error
        raise ValueError(
            "No LLM configured. Call set_llm() first or provide credentials via API."
        )

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

def get_llm(provider: str, model: str, api_key: str, temperature: float = 0.0) -> BaseChatModel:
    """Returns the configured LLM with provided credentials.
    
    Args:
        provider: LLM provider name ("groq", "grok", "gemini", or "openai")
        model: Model name for the provider
        api_key: API key for authentication
        temperature: Temperature setting for the model (default: 0.0)
    """
    provider = provider.lower()
    
    if not api_key:
        raise ValueError(f"{provider.title()} API key not provided. Please enter your API key.")
    
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(model=model, temperature=temperature, groq_api_key=api_key)
    
    elif provider == "grok":
        from langchain_xai import ChatXAI
        return ChatXAI(model=model, temperature=temperature, xai_api_key=api_key)
        
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model, temperature=temperature, google_api_key=api_key)
        
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model, temperature=temperature, openai_api_key=api_key)
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Supported providers: groq, grok, gemini, openai")

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