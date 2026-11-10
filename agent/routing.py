from typing import Literal

from agent.config import REQUEST_TYPES
from agent.state import State


def route_after_investigator(
    state: State,
) -> Literal["check_policy", "ask_order_number", "fallback"]:
    if state.get("request_type") not in REQUEST_TYPES:
        return "fallback"
    if state.get("found_order") is None:
        return "ask_order_number"
    return "check_policy"
