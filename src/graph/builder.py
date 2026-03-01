# src/graph/builder.py
"""
Graph assembly and compilation for the Stripe RAG Agent.
"""

from langgraph.graph import StateGraph, END

from src.graph.state import AgentState
from src.graph.nodes import (
    planner_node,
    budget_checker_node,
    executor_node,
    tool_node,
    query_expander_node,
    restructurer_node,
    synthesizer_node,
)
from src.graph.routing import (
    route_after_planner,
    route_after_budget_checker,
    route_after_executor,
    route_after_tools,
)


def build_graph() -> StateGraph:
    """
    Constructs the LangGraph workflow for the Stripe RAG Agent.
    
    Graph Structure:
    
    planner → budget_checker → executor → tools → restructurer → synthesizer → END
                    │              │          │
                    └──────────────┼──────────┼─→ END (clarification/budget exceeded)
                                   │          │
                                   │          └─→ query_expander → budget_checker (retry loop)
                                   │
                                   └─→ restructurer (budget exhausted during retry)
    
    Returns:
        Compiled StateGraph ready for execution.
    """
    workflow = StateGraph(AgentState)

    # Add all nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("budget_checker", budget_checker_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("query_expander", query_expander_node)
    workflow.add_node("restructurer", restructurer_node)
    workflow.add_node("synthesizer", synthesizer_node)

    # Set entry point
    workflow.set_entry_point("planner")

    # Add conditional edges
    workflow.add_conditional_edges("planner", route_after_planner)
    workflow.add_conditional_edges(
        "budget_checker", 
        route_after_budget_checker,
        {"executor": "executor", "restructurer": "restructurer", "__end__": END}
    )
    workflow.add_conditional_edges(
        "executor",
        route_after_executor,
        {"tools": "tools", "restructurer": "restructurer", "synthesizer": "synthesizer"}
    )
    workflow.add_conditional_edges("tools", route_after_tools)
    
    # Add fixed edges
    workflow.add_edge("query_expander", "budget_checker")  # Retries also go through budget check
    workflow.add_edge("restructurer", "synthesizer")       # Restructurer always leads to synthesis
    workflow.add_edge("synthesizer", END)

    return workflow


# Compile the graph for use
app_graph = build_graph().compile()
