from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from agent import nodes
from agent.routing import route_after_investigator
from agent.state import State


def build_graph():
    builder = StateGraph(State)

    builder.add_node("router", nodes.router)
    builder.add_node("investigator", nodes.investigator)
    builder.add_node("check_policy", nodes.check_policy)
    builder.add_node("ask_order_number", nodes.ask_order_number)
    builder.add_node("wait_for_customer", nodes.wait_for_customer)
    builder.add_node("fallback", nodes.fallback)
    builder.add_node("respond", nodes.respond)

    builder.add_edge(START, "router")
    builder.add_edge("router", "investigator")
    builder.add_conditional_edges(
        "investigator",
        route_after_investigator,
        {
            "check_policy": "check_policy",
            "ask_order_number": "ask_order_number",
            "fallback": "fallback",
        },
    )
    builder.add_edge("check_policy", "respond")
    builder.add_edge("respond", END)
    builder.add_edge("ask_order_number", "wait_for_customer")
    builder.add_edge("wait_for_customer", "router")
    builder.add_edge("fallback", END)

    return builder.compile(checkpointer=MemorySaver())
