# =============================================================================
# LANGGRAPH - StateGraph definition
# =============================================================================
#
#       ┌─────────────────┐
#       │ classify_intent  │  ← entry point (gpt-4.1-nano)
#       └────────┬────────┘
#                │ intent
#       ┌────────┼────────────┐
#       │        │            │
#       ▼        ▼            ▼
#   call_tool  chitchat     END (answer cố định)
#       │        │
#       ▼       END
#   execute_search
#       │
#      END
#

from langgraph.graph import StateGraph, END
from .nodes import classify_intent, chitchat, call_tool, execute_search
from .state import AgentState


def create_graph():
    graph = StateGraph(AgentState)

    graph.add_node("classify_intent", classify_intent)
    graph.add_node("chitchat", chitchat)
    graph.add_node("call_tool", call_tool)
    graph.add_node("execute_search", execute_search)

    graph.set_entry_point("classify_intent")

    graph.add_conditional_edges(
        "classify_intent",
        lambda state: state["intent"],
        {
            "product_search": "call_tool",
            "chit_chat": "chitchat",
            "handle_other_types": END,
        }
    )

    graph.add_edge("chitchat", END)
    graph.add_edge("call_tool", "execute_search")
    graph.add_edge("execute_search", END)

    return graph.compile()
