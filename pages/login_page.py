from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect

class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page
        self.username_input: Locator = page.locator("#username")
        self.password_input: Locator = page.locator("#password")
        self.login_button: Locator  = page.get_by_role("button", name="Login")
        self.flash_message: Locator = page.locator("#flash-message")

        self.table: Locator = page.locator('#table1')
        self.c_headers: Locator = page.locator("#table1 >  thead > tr > th")

        self.last_name_cells: Locator = page.locator('#table1 tbody tr')

    def open_login_page(self):
        return self.open(self.BASE_URL)

    def login(self, username: str, password: str) -> str:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        expect(self.flash_message).to_be_visible()
        return self.flash_message.inner_text()

    def get_flash_message_text(self) -> str:
        expect(self.flash_message).to_be_visible()
        return self.flash_message.inner_text()

    def get_toast_message(self) -> str:
        return self.read_toast()




