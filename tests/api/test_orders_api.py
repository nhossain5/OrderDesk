"""REQ-03 to REQ-10: the API enforces the same rules as the UI.

Same CSV as the UI tests, filtered to rows tagged with the "api" layer.
"""
import pytest

from tests.data_loader import case_ids, order_cases

CASES = order_cases("api")
pytestmark = pytest.mark.api


def payload(case: dict) -> dict:
    qty = case["qty"]
    return {
        "symbol": case["symbol"],
        "side": case["side"],
        "qty": int(qty) if qty.lstrip("-").isdigit() else qty,
        "order_type": case["order_type"],
        "price": case["price"] or None,
    }


@pytest.mark.parametrize("case", CASES, ids=case_ids(CASES))
def test_create_order_validation(trader_api, base_url, case):
    r = trader_api.post(f"{base_url}/api/orders", json=payload(case))

    if case["expected"] == "accepted":
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["status"] == "NEW"
        assert body["symbol"] == case["symbol"]
        assert body["qty"] == int(case["qty"])
    else:
        assert r.status_code == 422, r.text  # REQ-10
        assert case["expected"] in r.text


def test_created_order_can_be_fetched_by_id(trader_api, base_url):
    created = trader_api.post(
        f"{base_url}/api/orders",
        json={"symbol": "JKL4", "side": "Buy", "qty": 5, "order_type": "Limit", "price": "99.99"},
    ).json()

    r = trader_api.get(f"{base_url}/api/orders/{created['id']}")
    assert r.status_code == 200
    assert r.json()["price"] == "99.99"  # stored exactly, not as a float


def test_unknown_order_returns_404(trader_api, base_url):
    assert trader_api.get(f"{base_url}/api/orders/999999").status_code == 404
