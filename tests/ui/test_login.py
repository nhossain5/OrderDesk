"""REQ-01: users log in with username and password; wrong credentials show an error."""
import pytest

from tests.conftest import TRADER
from tests.pages.blotter_page import BlotterPage
from tests.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_trader_login_lands_on_blotter(driver, base_url):
    LoginPage(driver, base_url).open().login(*TRADER)
    assert BlotterPage(driver, base_url).title() == "Order blotter"


@pytest.mark.parametrize(
    "username, password",
    [("trader", "wrong-password"), ("nobody", "trader123"), ("", "")],
    ids=["wrong-password", "unknown-user", "empty-fields"],
)
def test_bad_credentials_show_error(driver, base_url, username, password):
    page = LoginPage(driver, base_url).open().login(username, password)
    assert page.error_text() == "Invalid username or password"
