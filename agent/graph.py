from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from .orders import Order

from agent import nodes
from agent.routing import (
    route_after_router,
    route_after_respond,
    route_after_investigator)
from agent.state import State


def build_graph():
    builder = StateGraph(State)

    builder.add_node("router", nodes.router)
    builder.add_node("investigator", nodes.investigator)
    builder.add_node("check_policy", nodes.check_policy)
    builder.add_node("fallback", nodes.fallback)
    builder.add_node("respond", nodes.respond)
    builder.add_node("confirm_case", nodes.confirm_case)
    builder.add_node("open_case", nodes.open_case)


    builder.add_edge(START, "router")
    builder.add_conditional_edges(
    "router",
    route_after_router,
        {
        "investigator": "investigator",
        "fallback": "fallback",
        },
    )
    builder.add_conditional_edges(
    "investigator",
    route_after_investigator,
    {
        "check_policy": "check_policy",
        "fallback": "fallback",
    },
)

    builder.add_edge("check_policy", "respond")

    builder.add_conditional_edges(
        "respond",
        route_after_respond,
        {
            "confirm_case": "confirm_case",
            "end": END
        }
    )
    builder.add_edge("fallback", END)
    builder.add_edge("open_case", END)


    return builder.compile(checkpointer=MemorySaver(serde=JsonPlusSerializer(allowed_msgpack_modules=[Order])))
