"""REQ-03 to REQ-08: data-driven order ticket validation through the browser.

Each row of tests/data/orders.csv tagged with the "ui" layer becomes one test.
Add a row to the CSV and you get a new test, with no code changes.
"""
import pytest

from tests.data_loader import case_ids, order_cases
from tests.pages.blotter_page import BlotterPage
from tests.pages.order_ticket_page import OrderTicketPage

CASES = order_cases("ui")
pytestmark = pytest.mark.ui


@pytest.mark.parametrize("case", CASES, ids=case_ids(CASES))
def test_order_ticket_validation(logged_in_trader, base_url, case):
    ticket = OrderTicketPage(logged_in_trader, base_url).open()
    ticket.submit(case["symbol"], case["side"], case["qty"], case["order_type"], case["price"])

    if case["expected"] == "accepted":
        blotter = BlotterPage(logged_in_trader, base_url)
        assert blotter.success_visible()
        assert blotter.status_of(blotter.created_order_id()) == "NEW"  # REQ-08
    else:
        assert case["expected"] in ticket.error_text()
