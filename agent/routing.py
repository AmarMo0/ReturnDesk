
from typing import Literal

from agent.state import State


def route_after_router(
    state: State,
) -> Literal["investigator", "fallback"]:

    if not state.get("order_id"):
        return "fallback"

    if state.get("request_type") not in {
        "standard_return",
        "damaged_replacement",
    }:
        return "fallback"

    return "investigator"


def route_after_investigator(
    state: State,
) -> Literal["check_policy", "fallback"]:

    if state.get("found_order") is None:
        return "fallback"

    return "check_policy"


def route_after_respond(
    state: State,
) -> Literal["confirm_case", "end"]:

    if state.get("eligibility_result") == "eligible":
        return "confirm_case"

    return "end"
