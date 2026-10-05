from selenium.webdriver.support.ui import Select

from tests.pages.base_page import BasePage


class OrderTicketPage(BasePage):
    path = "/orders/new"

    def submit(self, symbol: str, side: str, qty: str, order_type: str, price: str = ""):
        Select(self.el("symbol")).select_by_value(symbol)
        self.click(f"side-{side.lower()}")
        self.type("qty", qty)
        Select(self.el("order-type")).select_by_value(order_type)
        if price:
            self.type("price", price)
        self.click("submit")

    def error_text(self) -> str:
        return self.text_of("form-error")
