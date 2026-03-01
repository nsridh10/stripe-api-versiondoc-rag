# src/graph/state.py
"""
State type definitions for the Stripe RAG Agent graph.
"""

import operator
from typing import Annotated, Sequence, TypedDict, Optional, List
from langchain_core.messages import BaseMessage


class ToolPlan(TypedDict):
    """
    Structured output of the planner node.
    Represents a single planned tool call.
    """
    api_class: str          # e.g., "CUSTOMERS"
    version: Optional[str]  # e.g., "basil", "clover", or None for latest
    query: str              # The semantic search query to use


class QueryTracker(TypedDict):
    """
    Tracks each sub-query through the pipeline with its status and result.
    Used for coverage analysis and reporting.
    """
    api_class: str          # e.g., "CUSTOMERS", "INVOICES"
    version: Optional[str]  # e.g., "basil", "clover", or None
    query: str              # The semantic search query
    status: str             # "pending" | "covered" | "not_found" | "unavailable" | "budget_exceeded"
    reason: Optional[str]   # Why unavailable/not_found/budget_exceeded


class FrontierResult(TypedDict):
    """
    Structured output of the frontier node validation.
    """
    is_valid: bool                      # Whether the request passed validation
    rejection_reason: Optional[str]     # Why the request was rejected (if invalid)
    rejection_type: Optional[str]       # "out_of_scope" | "unsupported_version" | "junk"
    detected_versions: List[str]        # API versions detected in the request
    detected_api_classes: List[str]     # API classes detected in the request


class AgentState(TypedDict):
    """
    Main state container for the agent graph.
    
    Attributes:
        messages: Conversation message history (append-only)
        tool_call_budget: Tracks individual tool calls across ALL turns
        tool_plan: Structured plan produced by the planner, consumed by the executor
        needs_clarification: Whether the agent needs clarification from the user
        rephrase_count: Number of query rephrase attempts made
        intent_type: "new_intent" or "follow_up" for session management
        query_tracker: Structured tracking of each sub-query through the pipeline
        restructurer_analysis: Analysis text injected only into synthesizer
        conversation_context: Operation log for context-aware multi-turn planning
        active_scope: Current API class(es) and version(s) being discussed
        frontier_result: Validation result from the frontier node
        is_rejected: Whether the request was rejected by frontier
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    tool_call_budget: int
    tool_plan: Optional[List[ToolPlan]]
    needs_clarification: bool
    rephrase_count: int
    intent_type: Optional[str]
    query_tracker: Optional[List[QueryTracker]]
    restructurer_analysis: Optional[str]
    conversation_context: Optional[List[dict]]
    active_scope: Optional[dict]
    frontier_result: Optional[FrontierResult]
    is_rejected: bool
