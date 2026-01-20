from typing import Optional, Union
from pathlib import Path
from playwright.sync_api import Page, Locator, expect


class BasePage:
    BASE_URL = "https://dotesthere.com/"

    def __init__(self, page: Page, default_timeout_ms: int = 5000):
        self.page = page
        self.page.set_default_timeout(default_timeout_ms)


    def open(self, url: str = BASE_URL):
        self.page.goto(url, timeout=50000)
        return url

    def wait_for_url(self, url_or_regex: Union[str, object], timeout_ms: int = 5000):
        expect(self.page).to_have_url(url_or_regex, timeout=timeout_ms)

    def wait_visible(self, locator: Locator, timeout_ms: int = 5000):
        expect(locator).to_be_visible(timeout=timeout_ms)
        return locator

    def wait_hidden(self, locator: Locator, timeout_ms: int = 5000):
        expect(locator).to_be_hidden(timeout=timeout_ms)
        return locator

    def wait_enabled(self, locator: Locator) -> bool:
        expect(locator).to_be_enabled()
        return True

    def wait_disabled(self, locator: Locator) -> bool:
        expect(locator).to_be_disabled()
        return True

    def wait_text(self, locator: Locator, text: str):
        expect(locator).to_have_text(text)

    def get_input_value(self, locator: Locator) -> str:
        return locator.input_value()

    def wait_for_spinner(self, spinner: Locator, timeout_ms: int = 10000):
        try:
            expect(spinner).to_be_visible(timeout=2000)
        except Exception:
            pass
        expect(spinner).to_be_hidden(timeout=timeout_ms)

    def click(self, locator: Locator, timeout_ms: int = 5000):
        self.wait_visible(locator, timeout_ms)
        locator.click()
        return locator

    def fill(self, locator: Locator, text: str, timeout_ms: int = 5000, clear: bool = True):
        self.wait_visible(locator, timeout_ms)
        if clear:
            locator.fill("")
        locator.fill(text)
        return locator

    def select_option_in_dropdown(self, locator: Locator, label: str):
        locator.select_option(label=label)

    def resolve_file_path(self, relative_path: str) -> str:
        return str((Path.cwd() / relative_path).resolve())

    def set_file(self, locator: Locator, relative_path: str):
        file_path = str((Path.cwd() / relative_path).resolve())
        locator.set_input_files(file_path)

    def click_and_wait_for(self, button: Locator, element_to_wait: Locator):
        button.click()
        expect(element_to_wait).to_be_visible()

    def get_text(self, locator: Locator) -> str:
        return locator.inner_text()

    def get_input_value(self, locator: Locator) -> str:
        return locator.input_value()

    def expect_value(self, locator: Locator, expected: str):
        expect(locator).to_have_value(expected)

    def get_visible_texts(self, locator: Locator) -> list[str]:
        values = []
        count = locator.count()

        for i in range(count):
            element = locator.nth(i)
            if element.is_visible():
                text = element.text_content()
                if text:
                    values.append(text.strip())
        return values

    @property
    def toast(self):
        return self.page.locator("div.toast")

    def read_toast(self) -> str:
        expect(self.toast).to_be_visible()
        return self.toast.inner_text().strip()








