# Morning plan: 8:00 to 10:45

Goal for the 11:30 call: the app runs, the tests are green, you understand the code well enough to explain it, and it's pushed to GitHub. Hard stop on coding at 10:45.

## 8:00 Setup and run the app (15 min)

```bash
cd orderdesk
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000 and log in as `trader` / `trader123`. Submit a good order, then some bad ones (quantity 0, Limit with no price). Log out and in as `viewer` / `viewer123` and see what changes. Also open http://localhost:8000/docs; FastAPI generates it automatically. Stop the server with Ctrl+C when done.

## 8:15 Run the tests (15 min)

```bash
pytest -m api                 # should pass right away
pytest -m ui                  # needs Google Chrome installed
HEADLESS=0 pytest -m ui -k login      # watch the browser do it (Windows: set HEADLESS=0 first)
```

The API tests were verified before handoff. The UI tests couldn't be run there because that environment had no Chrome, so this is their first real run. If one fails, paste the error into the chat and we'll fix it together.

## 8:30 Read the code, in this order (45 min)

1. `docs/REQUIREMENTS.md`: the rules everything is built on.
2. `app/schemas.py`: one validation model enforces the rules for both the form and the API.
3. `app/main.py`: skim the routes. Notice `require_user` and `require_trader`.
4. `tests/pages/base_page.py`, then the other page objects.
5. `tests/data/orders.csv` and `tests/data_loader.py`.
6. `tests/ui/test_order_ticket.py` and `tests/api/test_orders_api.py`: the same CSV drives both.
7. `tests/conftest.py`: fixtures, the self-starting app, screenshots on failure.

Make sure you can answer these out loud:

- Why use page objects instead of calling Selenium in the tests?
- Why `WebDriverWait` instead of `time.sleep`?
- What is boundary-value analysis, and which CSV rows use it?
- Why do some tests create data through the API before checking the UI?
- Why does a request with no session get 401 instead of 422?

## 9:15 Your turn: exercises (60 min)

Do them in order. Each one should end with a passing test.

**Exercise 1: add three CSV rows.** Add these to `tests/data/orders.csv`, choosing the right `layers` value for each. Hint: the UI's symbol and side controls only allow valid choices, so rows with invalid values can only be tested through the API.

- Quantity `abc` → expected `Quantity must be a whole number`
- A Market order that includes a price → expected `Market orders must not include a price`
- Side `Hold` → expected `Side must be Buy or Sell`

Run `pytest -k TC-` and confirm the new cases appear and pass.

**Exercise 2: `test_viewer_cannot_create_order`** in `tests/api/test_your_turn_api.py` (REQ-02). Delete the `pytest.skip` line, post a valid order with `viewer_api`, and assert 403.

**Exercise 3: `test_order_cannot_be_cancelled_twice`** in the same file (REQ-09). Create an order, cancel it through `POST /api/orders/{id}/cancel` (expect 200 and status `CANCELLED`), then cancel again and assert 409.

**Exercise 4: `test_trader_can_cancel_order_from_blotter`** in `tests/ui/test_your_turn_ui.py` (REQ-09). Follow the steps in the comments. `BlotterPage` already has the methods you need.

Once exercises 2 to 4 pass, update the "(in progress)" notes in the README's coverage table.

If you get stuck on one for more than 10 minutes, ask in the chat and move on.

## 10:15 Report and push (30 min)

```bash
pytest --html=reports/report.html --self-contained-html
```

Open `reports/report.html` and note the numbers: how many tests, how many passed. You'll quote them on the call.

Create an empty public repo on GitHub named `orderdesk-qa` (no README, since you already have one). Then:

```bash
git init
git add .
git commit -m "OrderDesk MVP: FastAPI app + pytest/Selenium framework"
git branch -M main
git remote add origin https://github.com/<your-username>/orderdesk-qa.git
git push -u origin main
```

## 10:45 Stop coding

Eat, then rehearse the 30-second pitch and the "3+ years" answer from the SOP doc. Say the pitch with your real test count.
