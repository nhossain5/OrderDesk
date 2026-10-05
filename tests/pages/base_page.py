"""Base page object. Tests never touch Selenium directly; they call page methods."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    path = "/"

    def __init__(self, driver, base_url, timeout: float = 10):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.base_url + self.path)
        return self

    @staticmethod
    def by_testid(testid: str):
        return (By.CSS_SELECTOR, f'[data-testid="{testid}"]')

    def el(self, testid: str):
        """Wait until the element is visible, then return it. No time.sleep anywhere."""
        return self.wait.until(
            EC.visibility_of_element_located(self.by_testid(testid)),
            message=f"'{testid}' not visible on {self.driver.current_url}",
        )

    def click(self, testid: str):
        self.wait.until(EC.element_to_be_clickable(self.by_testid(testid))).click()

    def type(self, testid: str, text: str):
        field = self.el(testid)
        field.clear()
        field.send_keys(text)

    def text_of(self, testid: str) -> str:
        return self.el(testid).text

    def is_present(self, testid: str) -> bool:
        return len(self.driver.find_elements(*self.by_testid(testid))) > 0
