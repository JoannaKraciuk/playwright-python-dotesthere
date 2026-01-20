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

        self.dropdown: Locator      = page.locator("#dropdown")
        self.toast: Locator         = page.locator("div.toast")

        self.file_input: Locator    = page.locator("#file-upload")
        self.upload_button: Locator = page.get_by_role("button", name="Upload")
        self.upload_result: Locator = page.locator("#upload-result")
        self.add_btn: Locator = page.get_by_role("button", name="Add Element")
        self.delete_btn: Locator = page.locator('button.delete-btn')

        self.enable_btn: Locator = page.get_by_role("button", name="Enable")
        self.dynamic_input: Locator = page.locator('#dynamic-input')
        self.disable_btn: Locator = page.get_by_role("button", name="Disable")

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

    def select_option(self, label: str = 'Option 2') -> str:
        self.select_option_in_dropdown(self.dropdown, label)
        expect(self.toast).to_be_visible()
        return self.toast.inner_text()

    def upload_file(self, relative_path: str = 'tests/files/Plik 8.pdf') -> str:
        self.set_file(self.file_input, relative_path)
        self.click_and_wait_for(self.upload_button, self.upload_result)
        return self.upload_result.inner_text()

    def get_flash_message_text(self) -> str:
        expect(self.flash_message).to_be_visible()
        return self.flash_message.inner_text()

    def add_element(self) -> str:
        self.click(self.add_btn)
        self.wait_visible(self.toast)
        return self.get_text(self.toast)

    def delete_element(self):
        self.click(self.add_btn)
        self.click(self.delete_btn)
        self.wait_visible(self.toast)
        return self.get_text(self.toast)



    def get_toast_message(self) -> str:
        self.wait_visible(self.toast)
        return self.toast.inner_text().strip()

    def sort_last_name_toggle(self):
        self.click(self.c_headers.nth(0))

    def get_last_name_values(self) -> list[str]:
        return self.get_visible_texts(self.last_name_cells)




