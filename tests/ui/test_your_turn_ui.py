"""YOUR TURN: see MORNING.md, exercise 4. Delete the pytest.skip line when you start."""
import pytest

from tests.pages.blotter_page import BlotterPage

pytestmark = pytest.mark.ui


def test_trader_can_cancel_order_from_blotter(trader_api, base_url, logged_in_trader):
    pytest.skip("YOUR TURN: exercise 4 in MORNING.md")
    # 1. Create an order with trader_api (copy the pattern from test_blotter.py).
    # 2. Open the BlotterPage and call .cancel(order_id).
    # 3. Assert .status_of(order_id) == "CANCELLED".
