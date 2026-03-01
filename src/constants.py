# src/constants.py
"""
Constants and configuration helpers for the Stripe RAG Agent.
"""

from src.config import config


def get_config_value(path: str, default):
    """
    Dot-path config reader for accessing nested config values.
    
    Args:
        path: Dot-separated path to config value (e.g., 'agent.max_tool_calls')
        default: Default value if path not found
    
    Returns:
        The config value at the specified path, or default if not found.
    
    Examples:
        >>> get_config_value('agent.max_tool_calls', 6)
        6
        >>> get_config_value('services.vector_db.persist_directory', './data/chroma_db')
        './data/chroma_db'
    """
    parts = path.split(".")
    node = config
    for p in parts:
        if not isinstance(node, dict):
            return default
        node = node.get(p, {})
    return node if node != {} else default


# ---------------------------------------------------------------------------
# Agent Configuration Constants
# ---------------------------------------------------------------------------

# Hard limit on total individual tool invocations per request
MAX_TOOL_CALLS = get_config_value("agent.max_tool_calls", 6)

# Maximum retry attempts for rephrasing failed queries
MAX_REPHRASE = get_config_value("agent.max_rephrase_attempts", 1)

# Maximum operation-log turns injected into planner for context
MAX_CONTEXT_TURNS = get_config_value("agent.max_context_turns", 10)

# Known API classes available in the documentation system
KNOWN_API_CLASSES = get_config_value(
    "agent.known_api_classes",
    ["ACCOUNTS", "CUSTOMERS", "PAYMENT_INTENTS", "TRANSFERS",
     "SUBSCRIPTIONS", "PRODUCTS", "REFUNDS", "PRICES"]
)


# ---------------------------------------------------------------------------
# Status Constants
# ---------------------------------------------------------------------------

# Query tracker status values
STATUS_PENDING = "pending"
STATUS_COVERED = "covered"
STATUS_NOT_FOUND = "not_found"
STATUS_UNAVAILABLE = "unavailable"
STATUS_BUDGET_EXCEEDED = "budget_exceeded"

# Status display icons for console output
STATUS_ICONS = {
    STATUS_COVERED: "✓",
    STATUS_NOT_FOUND: "✗",
    STATUS_UNAVAILABLE: "⊘",
    STATUS_BUDGET_EXCEEDED: "⏸",
}


# ---------------------------------------------------------------------------
# Intent Types
# ---------------------------------------------------------------------------

INTENT_NEW = "new_intent"
INTENT_FOLLOW_UP = "follow_up"
