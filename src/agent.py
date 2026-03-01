# src/agent.py
"""
Stripe RAG Agent - Backward Compatibility Module

This module re-exports from the refactored graph module to maintain
backward compatibility with existing imports.

The actual implementation has been modularized into:
- src/graph/state.py     - State type definitions
- src/graph/nodes.py     - Graph node functions
- src/graph/routing.py   - Conditional routing functions
- src/graph/builder.py   - Graph assembly and compilation
- src/prompts/           - Static prompt templates
- src/constants.py       - Configuration constants
"""

# Re-export the compiled graph and state types
from src.graph import app_graph, AgentState, ToolPlan, QueryTracker

# Re-export constants for backward compatibility
from src.constants import (
    MAX_TOOL_CALLS,
    MAX_REPHRASE,
    MAX_CONTEXT_TURNS,
    KNOWN_API_CLASSES,
)

__all__ = [
    "app_graph",
    "AgentState",
    "ToolPlan",
    "QueryTracker",
    "MAX_TOOL_CALLS",
    "MAX_REPHRASE",
    "MAX_CONTEXT_TURNS",
    "KNOWN_API_CLASSES",
]
