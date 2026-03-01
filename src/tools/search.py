# src/tools/search.py
"""
Stripe API Documentation Search Tool.

This tool provides semantic search capabilities over the Stripe API
documentation vector store, with support for filtering by API class
and version (basil, clover, etc.).
"""
from typing import Optional, List
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from src.dependencies import get_vector_store
from src.config import config, get_latest_version
from src.trace import get_trace


class StripeAPISearchInput(BaseModel):
    """Input schema for the Stripe API documentation search tool."""
    query: str = Field(
        description=(
            "The semantic search query. Be specific and use Stripe API terminology. "
            "Example: 'required fields to create a customer', 'retrieve payment intent by id'."
        )
    )
    api_class: Optional[str] = Field(
        default=None,
        description=(
            "The specific Stripe API class to filter by. MUST be uppercase. "
            "Example: 'CUSTOMERS', 'ACCOUNTS', 'PAYMENT_INTENTS'. "
            "Leave null only if the query clearly spans multiple classes."
        )
    )
    version: Optional[str] = Field(
        default=None,
        description=(
            "The specific API version to filter by: 'basil' or 'clover'. "
            "Stripe uses codename-based versioning (acacia, basil, clover). "
            "Leave null to automatically use the latest version for this api_class."
        )
    )


@tool("search_stripe_api_docs", args_schema=StripeAPISearchInput)
def search_stripe_api_docs(
    query: str,
    api_class: Optional[str] = None,
    version: Optional[str] = None
) -> str:
    """
    Searches the Stripe API documentation vector database for a single, specific endpoint
    or API concept. Use one call per distinct (api_class, version) combination.

    Parallel calls are ONLY appropriate when comparing different versions of the SAME
    endpoint (e.g., CUSTOMERS basil vs CUSTOMERS clover) or querying two entirely different
    API classes in one turn. Never call this tool twice for the same endpoint with
    different phrasings — use the most precise query on the first attempt.
    """
    print(f"\n[Tool Execution] Searching: '{query}' | class={api_class} | version={version}")

    # Handle unknown API classes
    if api_class and api_class.upper() == "UNKNOWN":
        print(f"[Tool Execution] API class 'UNKNOWN' detected - this API class is not supported.")
        available_classes = config.get("agent", {}).get("known_api_classes", [])
        return (
            f"Unable to search for '{query}' because the API class is not recognized or supported.\n\n"
            f"Available API classes in this system:\n" +
            "\n".join(f"  - {cls}" for cls in available_classes) +
            f"\n\nPlease specify one of the available API classes above."
        )

    # Read config values
    vector_db_config = config.get("services", {}).get("vector_db", {})
    k_value = vector_db_config.get("retrieval_k", 3)
    similarity_threshold = vector_db_config.get("similarity_threshold", 0.0)
    
    print(f"[Tool Execution] Config values - retrieval_k: {k_value}, similarity_threshold: {similarity_threshold}")
    
    vector_store = get_vector_store()

    # --- Build metadata filters ---
    filter_dict = {}

    if api_class:
        filter_dict["api_class"] = api_class.upper()
        # Treat "latest" string the same as None/null
        if not version or version.lower() == "latest":
            latest_v = get_latest_version(api_class)
            if latest_v:
                print(f"[Tool Execution] Defaulting to latest version ({latest_v}) for {api_class}.")
                filter_dict["version"] = latest_v
            else:
                print(f"[Tool Execution] WARNING: No latest version configured for {api_class}, searching without version filter.")
        else:
            filter_dict["version"] = version.lower()

    search_kwargs: dict = {"k": k_value}
    if filter_dict:
        if len(filter_dict) == 1:
            search_kwargs["filter"] = filter_dict
        else:
            search_kwargs["filter"] = {"$and": [{k: v} for k, v in filter_dict.items()]}
    
    print(f"[Tool Execution DEBUG] search_kwargs: {search_kwargs}")
    print(f"[Tool Execution DEBUG] filter_dict: {filter_dict}")

    # --- Execute search with scores ---
    try:
        results_with_scores = vector_store.similarity_search_with_score(query, **search_kwargs)
        print(f"[Tool Execution] Raw search returned {len(results_with_scores)} chunks")
    except Exception as e:
        return f"Error executing search: {str(e)}"

    if not results_with_scores:
        # Trace: record not-found
        trace = get_trace()
        if trace:
            trace.add_tool_source(
                api_class=(api_class or "").upper(),
                version=filter_dict.get("version", "latest"),
                query=query,
                source_file="unknown",
                status="not_found",
                chunks=[],
            )
        return (
            f"No documentation found for query: '{query}' with filters: {filter_dict}. "
            "The vector store returned 0 results. Try a different query or check if the database is populated."
        )

    # Filter by similarity threshold
    # Note: For different embedding models, distance metrics vary
    # Chroma with cosine similarity: lower distance = more similar (typically 0-2)
    # We'll filter to keep chunks with distance <= (2 - 2*threshold) for cosine
    # This converts our 0-1 threshold to distance scale: threshold=0.5 -> distance<=1
    filtered_results = []
    print(f"\n[Tool Execution] Analyzing {len(results_with_scores)} chunks with threshold {similarity_threshold}:")
    for idx, (doc, distance) in enumerate(results_with_scores):
        # Convert distance to similarity score (0-1 scale, higher is better)
        # For cosine distance in Chroma: similarity = 1 - (distance / 2)
        similarity_score = max(0, 1 - (distance / 2))
        
        print(f"  Chunk {idx+1}: distance={distance:.4f}, similarity_score={similarity_score:.3f}", end="")
        
        if similarity_score >= similarity_threshold:
            filtered_results.append((doc, similarity_score))
            print(" ✓ KEPT")
        else:
            print(f" ✗ FILTERED (below {similarity_threshold})")

    if not filtered_results:
        # Trace: record not-found (all below threshold)
        trace = get_trace()
        if trace:
            trace.add_tool_source(
                api_class=(api_class or "").upper(),
                version=filter_dict.get("version", "latest"),
                query=query,
                source_file="unknown",
                status="not_found",
                chunks=[],
            )
        return (
            f"No documentation found for query: '{query}' with filters: {filter_dict}. "
            f"Note: {len(results_with_scores)} chunks were retrieved but all had similarity scores below the threshold ({similarity_threshold}). "
            "Try a different query or adjust the similarity threshold."
        )

    # --- Format results ---
    formatted_results = []
    print(f"\n=== [DEBUG] Retrieved {len(filtered_results)} chunks (after threshold filter) for '{query}' ===")

    for i, (doc, similarity_score) in enumerate(filtered_results):
        meta = doc.metadata
        header_context = " > ".join(
            v for k, v in meta.items() if "Header" in k and v
        )
        chunk_str = (
            f"API Class: {meta.get('api_class', 'Unknown')} "
            f"(Version: {meta.get('version', 'Unknown')})\n"
            f"Section: {header_context}\n"
            f"Similarity Score: {similarity_score:.3f}\n"
            f"Content:\n{doc.page_content}"
        )
        print(f"\n[Chunk {i+1}] (Similarity: {similarity_score:.3f}):\n{chunk_str}")
        formatted_results.append(chunk_str)

    print("=" * 62 + "\n")

    # --- Capture source documents in trace ---
    trace = get_trace()
    if trace:
        resolved_version = filter_dict.get("version", "latest")
        # Derive source_file from chunk metadata (set during ingestion)
        # All chunks in a single tool call share the same (api_class, version),
        # so we take source_file from the first chunk's metadata.
        source_file = filtered_results[0][0].metadata.get("source_file", "unknown") if filtered_results else "unknown"
        trace_chunks = []
        for doc, sim_score in filtered_results:
            meta = doc.metadata
            header_ctx = " > ".join(
                v for k, v in sorted(meta.items()) if "Header" in k and v
            )
            trace_chunks.append({
                "section": header_ctx,
                "similarity_score": round(sim_score, 3),
                "content_preview": (
                    doc.page_content[:300] + "..."
                    if len(doc.page_content) > 300
                    else doc.page_content
                ),
                "source_file": meta.get("source_file", "unknown"),
            })
        trace.add_tool_source(
            api_class=(api_class or "").upper(),
            version=resolved_version,
            query=query,
            source_file=source_file,
            status="found",
            chunks=trace_chunks,
        )

    return "\n\n---\n\n".join(formatted_results)
