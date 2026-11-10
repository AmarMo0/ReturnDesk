from datetime import date

from agent.orders import Order
from agent.policy import check_replacement_eligibility, check_return_eligibility

ORDER = Order("T1", "Lamp", date(2026, 11, 1))


def test_replacement_day_14_is_eligible():
    assert check_replacement_eligibility(ORDER, date(2026, 11, 15)) == "eligible"


def test_replacement_day_15_is_outside():
    assert check_replacement_eligibility(ORDER, date(2026, 11, 16)) == "outside_window"


def test_replacement_before_delivery_is_invalid():
    assert check_replacement_eligibility(ORDER, date(2026, 10, 30)) == "invalid_dates"


def test_return_day_30_is_eligible():
    assert check_return_eligibility(ORDER, date(2026, 12, 1), item_used=False) == "eligible"


def test_return_day_31_is_outside():
    assert check_return_eligibility(ORDER, date(2026, 12, 2), item_used=False) == "outside_window"


def test_return_asks_when_usage_unknown():
    assert check_return_eligibility(ORDER, date(2026, 11, 10), item_used=None) == "usage_unknown"


def test_return_rejects_used_item():
    assert check_return_eligibility(ORDER, date(2026, 11, 10), item_used=True) == "item_used"
