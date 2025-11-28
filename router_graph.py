# router_graph.py
from langgraph.graph import StateGraph, END
from router_logic import decide_route
from rag_agent import run_rag
from code_agent import code_executor

class RouterState(dict):
    """Custom state dict for LangGraph workflow."""
    pass


def router_node(state: RouterState) -> RouterState:
    """Decide route based on the query."""
    query = state.get("query", "")
    route = decide_route(query)
    state["route"] = route
    return state


def rag_node(state: RouterState) -> RouterState:
    """Run the RAG agent for knowledge retrieval."""
    query = state.get("query", "")
    response = run_rag(query)
    state["response"] = response
    return state


def code_node(state: RouterState) -> RouterState:
    """Run the code executor agent."""
    query = state.get("query", "")
    response = code_executor(query)
    state["response"] = response
    return state


# Initialize workflow
workflow = StateGraph(RouterState)

# Add nodes
workflow.add_node("router", router_node)
workflow.add_node("rag", rag_node)
workflow.add_node("code", code_node)

# Entry point
workflow.set_entry_point("router")

# Conditional edges based on route
workflow.add_conditional_edges(
    "router",
    lambda s: s.get("route", None),  # safe access
    {
        "rag": "rag",
        "code": "code"
    }
)

# Terminal nodes
workflow.add_edge("rag", END)
workflow.add_edge("code", END)

# Compile workflow
graph = workflow.compile()
