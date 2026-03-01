# src/trace.py
"""
Execution trace collector for the RAG pipeline.
Uses contextvars for thread-safe, per-request trace accumulation.

Each API request creates a TraceCollector, sets it via set_trace(),
and all graph nodes + tools record events into it. After the graph
completes, the trace is extracted and included in the API response.
"""

import time
import contextvars
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone


# Context variable — each request gets its own TraceCollector instance.
_trace_var: contextvars.ContextVar[Optional['TraceCollector']] = contextvars.ContextVar(
    'trace_collector', default=None
)


def get_trace() -> Optional['TraceCollector']:
    """Get the current request's trace collector, or None if not set."""
    return _trace_var.get(None)


def set_trace(collector: 'TraceCollector') -> contextvars.Token:
    """Set the trace collector for the current request context."""
    return _trace_var.set(collector)


class TraceCollector:
    """
    Accumulates execution trace events and source documents throughout
    a single request's LangGraph execution.

    Node events capture which graph nodes ran, how long they took, and
    what they decided. Source events capture which document chunks were
    retrieved and from which files.
    """

    def __init__(self):
        self.start_time: float = time.time()
        self.events: List[Dict[str, Any]] = []
        self.sources: List[Dict[str, Any]] = []
        self._node_starts: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Node lifecycle
    # ------------------------------------------------------------------

    def start_node(self, node: str, details: Optional[Dict] = None):
        """Record the start of a graph node execution."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details or {}
        }
        self._node_starts[node] = entry
        self.events.append({
            "node": node,
            "type": "node_start",
            "timestamp": entry["timestamp"],
            "details": entry["details"],
        })

    def end_node(self, node: str, details: Optional[Dict] = None):
        """Record the end of a graph node execution with computed duration."""
        start_entry = self._node_starts.pop(node, {})
        start_ts = start_entry.get("timestamp", "")

        # Compute wall-clock duration from stored start timestamp
        duration_ms = 0.0
        if start_ts:
            try:
                t0 = datetime.fromisoformat(start_ts)
                t1 = datetime.now(timezone.utc)
                duration_ms = round((t1 - t0).total_seconds() * 1000, 1)
            except Exception:
                pass

        self.events.append({
            "node": node,
            "type": "node_end",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "duration_ms": duration_ms,
            "details": details or {},
        })

    # ------------------------------------------------------------------
    # Routing decisions
    # ------------------------------------------------------------------

    def add_routing(self, from_node: str, to_node: str, reason: str = ""):
        """Record a conditional edge / routing decision."""
        self.events.append({
            "type": "routing",
            "from_node": from_node,
            "to_node": to_node,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    # ------------------------------------------------------------------
    # Source documents from tool execution
    # ------------------------------------------------------------------

    def add_tool_source(
        self,
        api_class: str,
        version: str,
        query: str,
        source_file: str,
        status: str,
        chunks: List[Dict],
    ):
        """
        Record source documents retrieved by a tool call.
        
        Args:
            api_class:   e.g. "CUSTOMERS"
            version:     e.g. "v2", "latest"
            query:       the semantic search query used
            source_file: the raw doc file this data came from
            status:      "found" | "not_found" | "error"
            chunks:      list of dicts with section, similarity_score, content_preview
        """
        self.sources.append({
            "api_class": api_class,
            "version": version or "latest",
            "query": query,
            "source_file": source_file,
            "status": status,
            "chunks": chunks,
        })

    # ------------------------------------------------------------------
    # Serialize to dict for API response
    # ------------------------------------------------------------------

    def to_dict(
        self,
        tool_call_budget_used: int = 0,
        tool_call_budget_max: int = 6,
        query_tracker: Optional[List[Dict]] = None,
        plan: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """Produce the final execution trace dictionary for the API response."""
        total_ms = round((time.time() - self.start_time) * 1000, 1)

        # Pair up node_start / node_end events into a summary list
        nodes_executed = []
        pending_starts: Dict[str, Dict] = {}
        for ev in self.events:
            if ev["type"] == "node_start":
                pending_starts[ev["node"]] = ev
            elif ev["type"] == "node_end":
                start_ev = pending_starts.pop(ev["node"], {})
                nodes_executed.append({
                    "node": ev["node"],
                    "start_time": start_ev.get("timestamp", ""),
                    "end_time": ev["timestamp"],
                    "duration_ms": ev.get("duration_ms", 0),
                    "input_details": start_ev.get("details", {}),
                    "output_details": ev.get("details", {}),
                })

        routing_decisions = [
            {
                "from_node": ev["from_node"],
                "to_node": ev["to_node"],
                "reason": ev.get("reason", ""),
                "timestamp": ev["timestamp"],
            }
            for ev in self.events
            if ev["type"] == "routing"
        ]

        return {
            "total_duration_ms": total_ms,
            "nodes_executed": nodes_executed,
            "routing_decisions": routing_decisions,
            "query_tracker": query_tracker or [],
            "plan": plan or [],
            "tool_call_budget_used": tool_call_budget_used,
            "tool_call_budget_max": tool_call_budget_max,
        }
