from agent.orders import get_order


def test_known_order_is_found():
    assert get_order("1009").product_name == "Fridge"


def test_order_number_with_spaces_is_found():
    assert get_order(" 1010 ").product_name == "Headphones"


def test_unknown_order_returns_none():
    assert get_order("9999") is None


def test_missing_order_returns_none():
    assert get_order(None) is None
    assert get_order("") is None
