# =============================================================================
# LANGGRAPH - StateGraph definition
# =============================================================================
#
#          ┌──────────────────┐
#          │  classify_intent  │
#          └────────┬─────────┘
#                   │
#          ┌────────▼─────────┐
#          │  route_by_intent  │
#          └──┬────────────┬──┘
#             │            │
#    "product_search"   "chitchat"
#             │            │
#    ┌────────▼──────┐  ┌──▼───────────┐
#    │   call_tool   │  │handle_chitchat│
#    └────────┬──────┘  └──────┬────────┘
#             │                │
#    ┌────────▼──────────┐    │
#    │ route_after_tool   │    │
#    └──┬─────────────┬──┘    │
#       │             │       │
#   has_args      no_args     │
#       │             │       │
#  ┌────▼──────┐  ┌───▼──────▼┐
#  │exec_search│  │  chitchat  │
#  └────┬──────┘  └────────────┘
#       │
#  ┌────▼──────────┐
#  │generate_answer │
#  └────┬──────────┘
#       │
#      END

from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    classify_intent,
    call_tool,
    execute_search,
    generate_answer,
    handle_chitchat,
)


def route_by_intent(state: AgentState) -> str:
    """Conditional edge: route theo intent."""
    if state["intent"] == "chitchat":
        return "chitchat"
    return "product_search"


def route_after_tool(state: AgentState) -> str:
    """Conditional edge: kiểm tra call_tool có trả về tool_args không."""
    if state["tool_args"]:
        return "has_args"
    return "no_args"


def create_graph():
    """Tạo và compile LangGraph StateGraph."""

    graph = StateGraph(AgentState)

    # Thêm nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("call_tool", call_tool)
    graph.add_node("execute_search", execute_search)
    graph.add_node("generate_answer", generate_answer)
    graph.add_node("handle_chitchat", handle_chitchat)

    # Entry point
    graph.set_entry_point("classify_intent")

    # Conditional edge sau classify_intent
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "product_search": "call_tool",
            "chitchat": "handle_chitchat",
        }
    )

    # Conditional edge sau call_tool: có tool_args → search, không → chitchat
    graph.add_conditional_edges(
        "call_tool",
        route_after_tool,
        {
            "has_args": "execute_search",
            "no_args": "handle_chitchat",
        }
    )

    # Product search path: execute_search → generate_answer → END
    graph.add_edge("execute_search", "generate_answer")
    graph.add_edge("generate_answer", END)

    # Chitchat path: handle_chitchat → END
    graph.add_edge("handle_chitchat", END)

    return graph.compile()
