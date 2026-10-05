"""Loads the shared test-case table. One CSV drives both the UI and API layers."""
import csv
from pathlib import Path

CSV_PATH = Path(__file__).parent / "data" / "orders.csv"


def order_cases(layer: str) -> list[dict]:
    """Rows whose `layers` column includes `layer` ("ui" or "api")."""
    with open(CSV_PATH, newline="") as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows if layer in r["layers"].split("+")]


def case_ids(cases: list[dict]) -> list[str]:
    return [c["case_id"] for c in cases]
