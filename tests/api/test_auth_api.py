"""REQ-01 and REQ-11: login and authentication on the API."""
import pytest

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_login_returns_role(anon_api, base_url):
    r = anon_api.post(f"{base_url}/api/login", json={"username": "trader", "password": "trader123"})
    assert r.status_code == 200
    assert r.json() == {"username": "trader", "role": "trader"}


def test_login_with_wrong_password_is_rejected(anon_api, base_url):
    r = anon_api.post(f"{base_url}/api/login", json={"username": "trader", "password": "nope"})
    assert r.status_code == 401


@pytest.mark.parametrize("method, path", [("get", "/api/orders"), ("post", "/api/orders")])
def test_requests_without_session_get_401(anon_api, base_url, method, path):
    # Even an invalid body must get 401, not 422: auth is checked before validation.
    r = anon_api.request(method, f"{base_url}{path}", json={})
    assert r.status_code == 401
