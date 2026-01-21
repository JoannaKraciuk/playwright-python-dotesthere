from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect

class SortingPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page
        self.table: Locator = page.locator('#table1')
        self.c_headers: Locator = page.locator("#table1 >  thead > tr > th")
        self.last_name_cells: Locator = page.locator('#table1 tbody tr')

    def sort_last_name_toggle(self):
        self.click(self.c_headers.nth(0))

    def get_last_name_values(self) -> list[str]:
        return self.get_visible_texts(self.last_name_cells)