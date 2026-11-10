from datetime import date
from typing import Annotated, Optional

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from agent.orders import Order


class State(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    order_id: Optional[str]
    found_order: Optional[Order]
    request_type: Optional[str]
    reported_on: date
    item_used: Optional[bool]
    eligibility_result: Optional[str]
