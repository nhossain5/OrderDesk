from tests.pages.base_page import BasePage


class BlotterPage(BasePage):
    path = "/orders"

    def title(self) -> str:
        return self.text_of("blotter-title")

    def success_visible(self) -> bool:
        return self.el("order-success").is_displayed()

    def created_order_id(self) -> int:
        return int(self.el("order-success").get_attribute("data-order-id"))

    def has_order(self, order_id: int) -> bool:
        return self.is_present(f"order-row-{order_id}")

    def status_of(self, order_id: int) -> str:
        return self.text_of(f"order-status-{order_id}")

    def cancel(self, order_id: int):
        self.click(f"cancel-{order_id}")
