
from pathlib import Path
from playwright.sync_api import Page, Locator, expect

class LoginPage:
    BASE_URL = "https://dotesthere.com/"

    def __init__(self, page: Page):
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

    def open(self) -> str:
        self.page.goto(self.BASE_URL)
        return self.page.url

    def login(self, username: str, password: str) -> str:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        expect(self.flash_message).to_be_visible()
        return self.flash_message.inner_text()

    def select_option(self, label: str = "Option 2") -> str:
        self.dropdown.select_option(label=label)
        expect(self.toast).to_be_visible()
        return self.toast.inner_text()

    def upload_file(self, relative_path: str) -> str:
        file_path = str((Path.cwd() / relative_path).resolve())
        self.file_input.set_input_files(file_path)
        self.upload_button.click()
        expect(self.upload_result).to_be_visible()
        return self.upload_result.inner_text()

    def get_flash_message_text(self) -> str:
        expect(self.flash_message).to_be_visible()
        return self.flash_message.inner_text()

    def add_element(self):
        self.add_btn.click()
        confirmation_message = self.toast.inner_text()
        return confirmation_message

    def delete_element(self):
        self.add_btn.click()
        self.delete_btn.click()
        confirmation_message = self.toast.inner_text()
        return confirmation_message

