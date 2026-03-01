# src/tools/__init__.py
"""
Tools for the Stripe RAG Agent.

This module contains LangChain-compatible tools that the agent can use
during execution to retrieve information from the documentation.

Available tools:
- search_stripe_api_docs: Search Stripe API documentation by semantic query

Usage:
    from src.tools import tools
    # tools is a list of all available tools for the agent
"""

from src.tools.search import search_stripe_api_docs, StripeAPISearchInput

# Exported tool list consumed by the agent
tools = [search_stripe_api_docs]

__all__ = [
    "tools",
    "search_stripe_api_docs",
    "StripeAPISearchInput",
]
