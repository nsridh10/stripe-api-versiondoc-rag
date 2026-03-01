# src/routes/models.py
"""
Pydantic models for API request and response schemas.
"""
from pydantic import BaseModel
from typing import Optional, List


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------

class QueryRequest(BaseModel):
    """Request body for the query endpoint."""
    query: str
    session_id: Optional[str] = None  # Optional: if not provided, creates new session


# ---------------------------------------------------------------------------
# Source Document Models
# ---------------------------------------------------------------------------

class SourceChunk(BaseModel):
    """A single retrieved documentation chunk."""
    section: str              # Header hierarchy, e.g. "Create a Customer > Parameters"
    similarity_score: float   # 0-1, higher = more relevant
    content_preview: str      # First ~300 chars of chunk content
    source_file: Optional[str] = None  # Raw file path this chunk came from


class ToolCallSource(BaseModel):
    """Source documents retrieved by a single tool call."""
    api_class: str            # e.g. "CUSTOMERS"
    version: str              # e.g. "v2", "latest"
    query: str                # The semantic search query used
    source_file: str          # Raw file path, e.g. "data/raw/CUSTOMERS.md"
    status: str               # "found" | "not_found" | "error"
    chunks: List[SourceChunk] # Retrieved chunks (empty if not_found)


# ---------------------------------------------------------------------------
# Execution Trace Models
# ---------------------------------------------------------------------------

class TraceNodeExecution(BaseModel):
    """A single graph node execution record."""
    node: str
    start_time: str
    end_time: str
    duration_ms: float
    input_details: dict       # What the node received / decided at entry
    output_details: dict      # What the node produced / decided at exit


class TraceRoutingDecision(BaseModel):
    """A conditional edge routing decision."""
    from_node: str
    to_node: str
    reason: str
    timestamp: str


class ExecutionTrace(BaseModel):
    """Full LangGraph execution trace for a single query."""
    total_duration_ms: float
    nodes_executed: List[TraceNodeExecution]
    routing_decisions: List[TraceRoutingDecision]
    query_tracker: List[dict]     # Final state of all sub-queries
    plan: List[dict]              # The planner's original retrieval plan
    tool_call_budget_used: int
    tool_call_budget_max: int


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------

class QueryResponse(BaseModel):
    """Enriched response with answer, sources, and execution trace."""
    message_type: str             # "answer" | "clarification" | "error"
    answer: str                   # The synthesized markdown answer
    session_id: str
    sources: List[ToolCallSource] # Documents used to generate the answer
    execution_trace: ExecutionTrace  # Full graph execution details


class MessageItem(BaseModel):
    """A single message in the conversation."""
    role: str                     # "user" | "assistant"
    content: str


class SessionMetadataResponse(BaseModel):
    """Session metadata response."""
    session_id: str
    created_at: str
    last_accessed: str
    message_count: int
    context_start: int = 0


class SessionListItem(BaseModel):
    """Session list item for chat history panel."""
    session_id: str
    created_at: str
    last_accessed: str
    message_count: int
    preview: str                  # First user message (truncated)
