"""YOUR TURN: see MORNING.md, exercises 2 and 3. Delete each pytest.skip line when you start."""
import pytest

pytestmark = pytest.mark.api


def test_viewer_cannot_create_order(viewer_api, base_url):
    pytest.skip("YOUR TURN: exercise 2 in MORNING.md")
    # REQ-02: POST a valid order with viewer_api and assert the status code is 403.


def test_order_cannot_be_cancelled_twice(trader_api, base_url):
    pytest.skip("YOUR TURN: exercise 3 in MORNING.md")
    # REQ-09: create an order, cancel it (expect 200 and status "CANCELLED"),
    # then cancel it again and assert 409.
