from langgraph.graph import (
    StateGraph,
    START,
    END
)

from .state import EmailState
from .nodes import (
    analyze_email,
    decide_action,
    generate_reply
)


def route_after_decision(state):

    if state["decision"] == "draft_reply":
        return "generate_reply"

    return END


def build_graph():

    graph = StateGraph(EmailState)

    graph.add_node(
        "analyze",
        analyze_email
    )

    graph.add_node(
        "decide",
        decide_action
    )

    graph.add_node(
        "generate_reply",
        generate_reply
    )

    graph.add_edge(
        START,
        "analyze"
    )

    graph.add_edge(
        "analyze",
        "decide"
    )

    graph.add_conditional_edges(
        "decide",
        route_after_decision,
        {
            "generate_reply": "generate_reply",
            END: END
        }
    )

    graph.add_edge(
        "generate_reply",
        END
    )

    return graph.compile()