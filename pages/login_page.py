from logging import addLevelName

from playwright.sync_api import Page

class LoginPage:

    def __init__(self, page: Page):
        self.page = page


    def open(self):
        self.page.goto('https://dotesthere.com/')
        return self.page.url

    def login(self):
        self.page.locator('#username').fill('ankur')
        self.page.locator('#password').fill('automation')
        self.page.get_by_role("button", name='Login').click()
        alert_message = self.page.locator('#flash-message')
        return alert_message.inner_text()


