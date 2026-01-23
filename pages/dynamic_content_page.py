from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect

class DynamicContentPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page

        self.refresh_btn: Locator   = self.page.get_by_role('button', name='Refresh Content')
        self.dynamic_content: Locator = self.page.locator('div.content-row > p').first

    @property
    def refresh_button(self) -> Locator:
        return self.refresh_btn

    @property
    def dynamic_text(self) -> Locator:
        return self.dynamic_content

    @property
    def toast_message(self):
        return self.read_toast

    def click_change_and_get_text(self):
        before = self.click(self.refresh_button)
        expect(self.dynamic_text).not_to_have_text(before, timeout=10000)
        return self.dynamic_text.inner_text()

    def double_click_refresh(self):
        before = self.refresh_button.inner_text()
        self.refresh_button.dblclick()
        expect(self.dynamic_text).not_to_have_text(before, timeout=10000)
        return self.dynamic_text.inner_text()

    def multi_click_refresh(self, times: int = 5, delay: float = 0.1) -> str:
        before = self.dynamic_text.inner_text()
        for _ in range(times):
            self.refresh_button.click()
            self.page.wait_for_timeout(int(delay * 1000))
        expect(self.dynamic_text).not_to_have_text(before, timeout=10000)
        return self.dynamic_text.inner_text()
