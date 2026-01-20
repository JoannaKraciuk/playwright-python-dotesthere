from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect

class DropdownPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page
        self.dropdown: Locator = page.locator("#dropdown")

    def select_option(self, label: str = 'Option 2') -> str:
        self.select_option_in_dropdown(self.dropdown, label)
        return self.read_toast()

