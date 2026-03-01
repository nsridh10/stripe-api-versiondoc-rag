# src/graph/__init__.py
"""
Stripe RAG Agent Graph Module.

This module contains the LangGraph-based agent workflow, segmented into:
- state.py: State type definitions
- nodes.py: Graph node functions (including frontier_node)
- routing.py: Conditional routing functions
- builder.py: Graph assembly and compilation

Usage:
    from src.graph import app_graph, AgentState
"""

from src.graph.state import AgentState, ToolPlan, QueryTracker, FrontierResult
from src.graph.builder import app_graph

__all__ = [
    "app_graph",
    "AgentState",
    "ToolPlan",
    "QueryTracker",
    "FrontierResult",
]
