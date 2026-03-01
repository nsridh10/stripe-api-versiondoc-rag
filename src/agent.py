# src/agent.py
"""
Stripe RAG Agent - Backward Compatibility Module

This module re-exports from the refactored graph module to maintain
backward compatibility with existing imports.

The actual implementation has been modularized into:
- src/graph/state.py     - State type definitions
- src/graph/nodes.py     - Graph node functions (including frontier_node)
- src/graph/routing.py   - Conditional routing functions
- src/graph/builder.py   - Graph assembly and compilation
- src/prompts/           - Static prompt templates
- src/constants.py       - Configuration constants
"""

# Re-export the compiled graph and state types
from src.graph import app_graph, AgentState, ToolPlan, QueryTracker, FrontierResult

# Re-export constants for backward compatibility
from src.constants import (
    MAX_TOOL_CALLS,
    MAX_REPHRASE,
    MAX_CONTEXT_TURNS,
    KNOWN_API_CLASSES,
    SUPPORTED_API_VERSIONS,
    ALL_STRIPE_VERSIONS,
    UNSUPPORTED_VERSIONS,
    DEFAULT_API_VERSION,
)

__all__ = [
    "app_graph",
    "AgentState",
    "ToolPlan",
    "QueryTracker",
    "FrontierResult",
    "MAX_TOOL_CALLS",
    "MAX_REPHRASE",
    "MAX_CONTEXT_TURNS",
    "KNOWN_API_CLASSES",
    "SUPPORTED_API_VERSIONS",
    "ALL_STRIPE_VERSIONS",
    "UNSUPPORTED_VERSIONS",
    "DEFAULT_API_VERSION",
]
