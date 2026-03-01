# src/graph/routing.py
"""
Conditional routing functions for the Stripe RAG Agent graph.
"""

from typing import Literal
from langchain_core.messages import ToolMessage

from src.graph.state import AgentState
from src.trace import get_trace
from src.constants import MAX_REPHRASE, STATUS_PENDING


def route_after_planner(state: AgentState) -> Literal["budget_checker", "__end__"]:
    """
    Routes after planner node.
    
    If the planner asked a clarification question, end the turn (the question
    is already in messages). Otherwise proceed to budget check.
    """
    trace = get_trace()
    if state.get("needs_clarification"):
        if trace:
            trace.add_routing("planner", "__end__", "Clarification needed")
        return "__end__"
    if trace:
        trace.add_routing("planner", "budget_checker", "Plan ready, checking budget")
    return "budget_checker"


def route_after_budget_checker(state: AgentState) -> Literal["executor", "restructurer", "__end__"]:
    """
    Routes after budget check.
    
    - Over budget on fresh request → __end__ (clarification)
    - Over budget on retry with nothing left to execute → restructurer (show partial results)
    - Within budget or truncated with items left → executor
    """
    if state.get("needs_clarification"):
        return "__end__"
    plan = state.get("tool_plan", []) or []
    if plan:
        return "executor"
    # No executable plan remaining — budget exhausted on retry path.
    # Go to restructurer so partial results are still presented.
    return "restructurer"


def route_after_executor(state: AgentState) -> Literal["tools", "restructurer", "synthesizer"]:
    """
    Routes after executor node.
    
    Routes to tools if the executor made tool calls, to restructurer if
    returning from query_expander with no new calls, else to synthesizer.
    """
    trace = get_trace()
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        if trace:
            trace.add_routing("executor", "tools", f"Executing {len(last_message.tool_calls)} tool call(s)")
        return "tools"
    
    # If we have a query_tracker, we should always go through restructurer
    if state.get("query_tracker"):
        if trace:
            trace.add_routing("executor", "restructurer", "Has query tracker, analyzing coverage")
        return "restructurer"
    
    # No tracker = budget exhausted fallback or planner failure
    if trace:
        trace.add_routing("executor", "synthesizer", "No tracker, direct synthesis")
    return "synthesizer"


def route_after_tools(state: AgentState) -> Literal["query_expander", "restructurer"]:
    """
    Per-tool retry routing.
    
    If ANY tool call returned 'No documentation found' and retry attempts remain,
    route to query_expander.
    """
    trace = get_trace()
    current_rephrase = state.get("rephrase_count", 0)
    
    # Collect all recent ToolMessages
    tool_messages = []
    for m in reversed(state["messages"]):
        if isinstance(m, ToolMessage):
            tool_messages.append(m)
        elif tool_messages:  # Stop once we pass the ToolMessage block
            break
    
    if not tool_messages:
        if trace:
            trace.add_routing("tools", "restructurer", "No tool messages found")
        return "restructurer"
    
    # Check if ANY tool call failed
    any_failure = any(
        "No documentation found" in tm.content for tm in tool_messages
    )
    
    # Route to query_expander if there are failures and retries remain
    if any_failure and current_rephrase < MAX_REPHRASE:
        if trace:
            trace.add_routing("tools", "query_expander", f"Failures detected, retry {current_rephrase + 1}/{MAX_REPHRASE}")
        return "query_expander"
    
    if trace:
        reason = "All tools succeeded" if not any_failure else f"Retries exhausted ({current_rephrase}/{MAX_REPHRASE})"
        trace.add_routing("tools", "restructurer", reason)
    return "restructurer"
