"""REQ-08: new orders appear in the blotter with status NEW.

Uses the API to create test data, then checks it in the browser.
Setting up through the API is faster and less flaky than clicking through the UI.
"""
import pytest

from tests.pages.blotter_page import BlotterPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_api_created_order_shows_in_blotter(trader_api, base_url, logged_in_trader):
    r = trader_api.post(
        f"{base_url}/api/orders",
        json={"symbol": "GHI3", "side": "Sell", "qty": 250, "order_type": "Limit", "price": "15.50"},
    )
    assert r.status_code == 201, r.text
    order_id = r.json()["id"]

    blotter = BlotterPage(logged_in_trader, base_url).open()
    assert blotter.has_order(order_id)
    assert blotter.status_of(order_id) == "NEW"
