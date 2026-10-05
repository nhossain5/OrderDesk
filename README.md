# OrderDesk QA

A pytest + Selenium test automation framework, and the small trade-order web app it tests.

**OrderDesk** is a mock trading-desk app: traders log in, submit Market or Limit orders through an order ticket, and manage them in a blotter. It has a REST API and business rules written up front in [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md). Those rules are what the tests verify.

## Stack

- **App:** Python, FastAPI, Jinja2, SQLAlchemy, SQLite by default (PostgreSQL via `DATABASE_URL`)
- **Tests:** pytest, Selenium 4, requests, pytest-html

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload      # http://localhost:8000  (trader / trader123)
```

## Running the tests

UI tests need Google Chrome installed. Selenium Manager downloads the matching driver automatically.

```bash
pytest                              # everything; starts its own app with a throwaway database
pytest -m api                       # API tests only
pytest -m ui                        # browser tests only
pytest -m smoke                     # critical path only
HEADLESS=0 pytest -m ui             # watch the browser
pytest --html=reports/report.html --self-contained-html
```

To test an app that's already running, set `BASE_URL=http://localhost:8000`.

## Framework design

- **Page objects** (`tests/pages/`). Tests call methods like `ticket.submit(...)` and never touch Selenium directly, so a UI change means editing one page object, not every test.
- **Data-driven tests.** One file, `tests/data/orders.csv`, holds boundary-value and equivalence-partition cases. Its `layers` column sends each row to the UI tests, the API tests, or both. Adding a row adds a test.
- **Explicit waits only.** `WebDriverWait` with expected conditions; no `time.sleep`.
- **Stable locators.** Every element the tests use has a `data-testid` attribute.
- **Independent tests.** Each test creates its own data, often through the API, which is faster and less flaky than clicking through the UI.
- **Failure evidence.** Failed UI tests save a screenshot to `reports/screenshots/`.

## Requirements coverage

| Requirement | Tests |
| --- | --- |
| REQ-01 Login | `ui/test_login.py`, `api/test_auth_api.py` |
| REQ-02 Roles | `api/test_your_turn_api.py` (in progress) |
| REQ-03 to REQ-07 Order validation | `ui/test_order_ticket.py`, `api/test_orders_api.py` (via `orders.csv`) |
| REQ-08 Blotter | `ui/test_order_ticket.py`, `ui/test_blotter.py` |
| REQ-09 Cancel | `api/test_your_turn_api.py`, `ui/test_your_turn_ui.py` (in progress) |
| REQ-10 API validation | `api/test_orders_api.py` |
| REQ-11 API auth | `api/test_auth_api.py` |

## Roadmap

Not built yet:

- Docker Compose for the app, PostgreSQL, and Selenium Grid
- GitHub Actions CI running the full suite on every push, with the HTML report as an artifact
- SQL integrity checks against PostgreSQL
- Test plan with exit criteria, traceability matrix, and GitHub Issues bug triage
- A Java + JUnit 5 Selenium module that reuses `orders.csv`
