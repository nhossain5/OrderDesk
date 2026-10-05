"""One validation model shared by the HTML form and the REST API (REQ-10).

Every rule here maps to a requirement in docs/REQUIREMENTS.md, and every
error message is what the tests assert on.
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

SYMBOLS = ["ABC1", "DEF2", "GHI3", "JKL4", "MNO5"]  # made-up contract codes (REQ-03)
SIDES = ["Buy", "Sell"]
ORDER_TYPES = ["Market", "Limit"]
MIN_QTY, MAX_QTY = 1, 10_000


class OrderIn(BaseModel):
    symbol: str
    side: str
    qty: int
    order_type: str
    price: Decimal | None = None

    @field_validator("symbol")
    @classmethod
    def check_symbol(cls, v: str) -> str:  # REQ-03
        if v not in SYMBOLS:
            raise ValueError("Unknown symbol")
        return v

    @field_validator("side")
    @classmethod
    def check_side(cls, v: str) -> str:  # REQ-04
        if v not in SIDES:
            raise ValueError("Side must be Buy or Sell")
        return v

    @field_validator("qty", mode="before")
    @classmethod
    def check_qty(cls, v) -> int:  # REQ-05
        if isinstance(v, bool):
            raise ValueError("Quantity must be a whole number")
        try:
            qty = int(str(v).strip())
        except ValueError:
            raise ValueError("Quantity must be a whole number")
        if not MIN_QTY <= qty <= MAX_QTY:
            raise ValueError(f"Quantity must be between {MIN_QTY} and {MAX_QTY}")
        return qty

    @field_validator("order_type")
    @classmethod
    def check_order_type(cls, v: str) -> str:  # REQ-06
        if v not in ORDER_TYPES:
            raise ValueError("Order type must be Market or Limit")
        return v

    @field_validator("price", mode="before")
    @classmethod
    def check_price(cls, v):  # REQ-07
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return None
        try:
            price = Decimal(str(v).strip())
        except InvalidOperation:
            raise ValueError("Price must be a number")
        if not price.is_finite():
            raise ValueError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        if price.as_tuple().exponent < -2:
            raise ValueError("Price allows at most 2 decimals")
        return price

    @model_validator(mode="after")
    def check_price_matches_type(self):  # REQ-06, REQ-07
        if self.order_type == "Limit" and self.price is None:
            raise ValueError("Limit orders require a price")
        if self.order_type == "Market" and self.price is not None:
            raise ValueError("Market orders must not include a price")
        return self


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    side: str
    qty: int
    order_type: str
    price: Decimal | None
    status: str
    created_at: datetime


class LoginIn(BaseModel):
    username: str
    password: str
