from langchain_core.messages import SystemMessage
from langgraph.types import interrupt

from agent import prompts
from agent.config import get_router_llm, get_writer_llm
from agent.orders import get_order
from agent.policy import check_replacement_eligibility, check_return_eligibility
from agent.schemas import Extracted
from agent.state import State


def _reply(system_prompt: str, state: State) -> dict:
    reply = get_writer_llm().invoke([SystemMessage(content=system_prompt), *state["messages"]])
    return {"messages": [reply]}


def router(state: State) -> dict:
    result = get_router_llm().with_structured_output(Extracted).invoke(
        [SystemMessage(content=prompts.ROUTER), *state["messages"]]
    )
    return {
        "request_type": result.request_type,
        "order_id": result.order_id or state.get("order_id"),
        "item_used": result.item_used if result.item_used is not None else state.get("item_used"),
    }


def investigator(state: State) -> dict:
    order_id = state.get("order_id") 
    found_order = get_order(order_id)
    return {"found_order": found_order}

def check_policy(state: State) -> dict:
    order, reported_on = state["found_order"], state["reported_on"]
    request_type = state["request_type"]

    if request_type == "standard_return":
        result = check_return_eligibility(order, reported_on, state.get("item_used"))
    elif request_type == "damaged_replacement":
        result = check_replacement_eligibility(order, reported_on)
    else:
        raise ValueError(f"check_policy got unexpected request type: {request_type}")

    return {"eligibility_result": result}


def ask_order_number(state: State) -> dict:
    return _reply(prompts.ASK_ORDER_NUMBER, state)


def fallback(state: State) -> dict:
    return _reply(prompts.FALLBACK, state)


def respond(state: State) -> dict:
    product = state["found_order"].product_name
    decision = prompts.DECISION_MEANING[state["eligibility_result"]]
    return _reply(f"{prompts.RESPOND}\n\nProduct: {product}\nDecision: {decision}", state)


def wait_for_customer(state: State) -> dict:
    answer = interrupt(state["messages"][-1].content)
    return {"messages": [("user", answer)]}
