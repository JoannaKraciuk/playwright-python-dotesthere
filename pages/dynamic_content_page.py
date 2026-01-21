from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect

class DynamicContentPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page

        self.refresh_btn: Locator   = self.page.get_by_role('button', name='Refresh Content')
        self.dynamic_content: Locator = self.page.locator('div.content-row > p')

    @property
    def refresh_button(self):
        return self.refresh_btn

    @property
    def dynamic_text(self):
        return self.dynamic_content

    @property
    def toast_message(self):
        return self.read_toast

    def click_change_and_get_text(self):
        self.click(self.refresh_button)
        self.wait_visible(self.dynamic_text)
        return self.dynamic_text.inner_text()

    def double_click_refresh(self):
        self.refresh_button.dblclick()
        self.wait_visible(self.dynamic_text)
        return self.dynamic_text.inner_text()

    def multi_click_refresh(self, times: int = 5, delay: float = 0.1):
        import time
        for i in range(times):
            self.click(self.refresh_button)
            if delay > 0:
                time.sleep(delay)
        self.wait_visible(self.dynamic_text)
        return self.dynamic_text.inner_text()