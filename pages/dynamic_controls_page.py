from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect

class DynamicPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page
        self.enable_btn: Locator = page.get_by_role("button", name="Enable")
        self.dynamic_input: Locator = page.locator('#dynamic-input')
        self.disable_btn: Locator = page.get_by_role("button", name="Disable")
        self.toast: Locator = page.locator("div.toast")

    def enable_input(self) -> bool:
        self.click(self.enable_btn)
        return self.wait_enabled(self.dynamic_input)

    def disable_input(self) -> bool:
        self.click(self.disable_btn)
        return self.wait_disabled(self.dynamic_input)

    def fill_input(self, text: str = "Playwright dynamic controls") -> str:
        self.fill(self.dynamic_input, text)
        self.expect_value(self.dynamic_input, text)
        return text

    def get_toast_message(self) -> str:
        self.wait_visible(self.toast)
        return self.toast.inner_text().strip()
