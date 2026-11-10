from agent.routing import route_after_investigator


def test_unsupported_request_goes_to_fallback():
    assert route_after_investigator({"request_type": "unknown", "found_order": None}) == "fallback"


def test_unsupported_request_ignores_missing_order():
    assert route_after_investigator({"request_type": "banana"}) == "fallback"


def test_valid_request_without_order_asks_for_it():
    state = {"request_type": "damaged_replacement", "found_order": None}
    assert route_after_investigator(state) == "ask_order_number"


def test_valid_request_with_order_checks_policy():
    state = {"request_type": "standard_return", "found_order": object()}
    assert route_after_investigator(state) == "check_policy"
