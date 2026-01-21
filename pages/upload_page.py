from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect

class UploadPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page
        self.file_input: Locator = page.locator("#file-upload")
        self.upload_button: Locator = page.get_by_role("button", name="Upload")
        self.upload_result: Locator = page.locator("#upload-result")

    def upload_file(self, relative_path: str) -> str:
        self.set_file(self.file_input, relative_path)
        self.click_and_wait_for_element(self.upload_button, self.upload_result)
        return self.upload_result.inner_text()