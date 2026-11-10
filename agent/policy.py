from datetime import date
from typing import Literal

from agent.orders import Order

REPLACEMENT_WINDOW_DAYS = 14
RETURN_WINDOW_DAYS = 30

ReplacementStatus = Literal["eligible", "outside_window", "invalid_dates"]
ReturnStatus = Literal[
    "eligible", "outside_window", "invalid_dates", "usage_unknown", "item_used"
]


def check_replacement_eligibility(order: Order, reported_on: date) -> ReplacementStatus:
    days_since_delivery = (reported_on - order.delivery_date).days

    if days_since_delivery < 0:
        return "invalid_dates"
    if days_since_delivery <= REPLACEMENT_WINDOW_DAYS:
        return "eligible"
    return "outside_window"


def check_return_eligibility(
    order: Order, reported_on: date, item_used: bool | None
) -> ReturnStatus:
    days_since_delivery = (reported_on - order.delivery_date).days

    if days_since_delivery < 0:
        return "invalid_dates"
    if days_since_delivery > RETURN_WINDOW_DAYS:
        return "outside_window"
    if item_used is None:
        return "usage_unknown"
    if item_used:
        return "item_used"
    return "eligible"
