from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect

class ElementsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page
        self.add_btn: Locator = page.get_by_role("button", name="Add Element")
        self.delete_btn: Locator = page.locator('button.delete-btn')

    def add_element(self):
        self.click(self.add_btn)
        self.wait_visible(self.toast)
        return self.get_text(self.toast)

    def delete_element(self):
        self.click(self.add_btn)
        self.wait_toast_disappear()
        self.click(self.delete_btn)
        self.wait_visible(self.toast)
        return self.get_text(self.toast)

    def get_toast_message(self) -> str:
        return self.read_toast()