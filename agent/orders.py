from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Order:
    order_id: str
    product_name: str
    delivery_date: date

_SAMPLE_ORDERS = (
    Order("1009", "Fridge", date.today() - timedelta(days=30)),
    Order("1010", "Headphones", date.today() - timedelta(days=4)),
)

_ORDERS_BY_ID = {order.order_id: order for order in _SAMPLE_ORDERS}


def get_order(order_id: str | None) -> Order | None:
    if not order_id:
        return None
    return _ORDERS_BY_ID.get(order_id.strip())
