from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    def login(self, username: str, password: str):
        self.type("username", username)
        self.type("password", password)
        self.click("login-submit")
        return self

    def error_text(self) -> str:
        return self.text_of("login-error")
