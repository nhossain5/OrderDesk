"""Shared pytest fixtures.

If BASE_URL is set, tests run against that running app.
Otherwise this file starts the app itself on a free port with a fresh,
throwaway SQLite database, so `pytest` works with one command.
"""
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests
from selenium import webdriver

from tests.pages.blotter_page import BlotterPage
from tests.pages.login_page import LoginPage

ROOT = Path(__file__).resolve().parents[1]
TRADER = ("trader", "trader123")
VIEWER = ("viewer", "viewer123")


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_until_up(url: str, timeout: float = 20) -> None:
    """Poll until the app answers. A condition-based wait, not a blind sleep."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if requests.get(f"{url}/login", timeout=1).ok:
                return
        except requests.ConnectionError:
            pass
        time.sleep(0.25)  # polling interval between checks
    raise RuntimeError(f"App did not start at {url} within {timeout}s")


@pytest.fixture(scope="session")
def base_url(tmp_path_factory):
    external = os.getenv("BASE_URL")
    if external:
        external = external.rstrip("/")
        _wait_until_up(external)
        yield external
        return

    port = _free_port()
    db_file = tmp_path_factory.mktemp("db") / "test.db"
    env = {**os.environ, "DATABASE_URL": f"sqlite:///{db_file}"}
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", str(port), "--log-level", "warning"],
        cwd=ROOT,
        env=env,
    )
    url = f"http://127.0.0.1:{port}"
    try:
        _wait_until_up(url)
        yield url
    finally:
        proc.terminate()
        proc.wait(timeout=10)


# ---------- browser (UI tests) ----------

@pytest.fixture
def driver(request):
    opts = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "1") == "1":  # HEADLESS=0 to watch the browser
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,900")
    # Turn off Chrome's password manager and breach-check popup, which can block the page.
    opts.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    grid = os.getenv("SELENIUM_URL")  # used later with Docker / Selenium Grid
    drv = webdriver.Remote(command_executor=grid, options=opts) if grid else webdriver.Chrome(options=opts)
    yield drv
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        out = ROOT / "reports" / "screenshots"
        out.mkdir(parents=True, exist_ok=True)
        drv.save_screenshot(str(out / f"{request.node.name}.png"))
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Stash each phase's result on the test so the driver fixture knows if it failed."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _log_in(driver, base_url, creds):
    LoginPage(driver, base_url).open().login(*creds)
    # Wait for the blotter so the session cookie is set before the test navigates.
    BlotterPage(driver, base_url).el("blotter-title")
    return driver


@pytest.fixture
def logged_in_trader(driver, base_url):
    return _log_in(driver, base_url, TRADER)


@pytest.fixture
def logged_in_viewer(driver, base_url):
    return _log_in(driver, base_url, VIEWER)


# ---------- HTTP sessions (API tests) ----------

def _api_session(base_url, creds=None) -> requests.Session:
    s = requests.Session()
    if creds:
        r = s.post(f"{base_url}/api/login", json={"username": creds[0], "password": creds[1]})
        assert r.ok, r.text
    return s


@pytest.fixture
def trader_api(base_url):
    return _api_session(base_url, TRADER)


@pytest.fixture
def viewer_api(base_url):
    return _api_session(base_url, VIEWER)


@pytest.fixture
def anon_api(base_url):
    return _api_session(base_url)
