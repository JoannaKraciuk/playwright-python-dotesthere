import pytest

from pages.login_page import LoginPage

def test_open_login(login_page: LoginPage):
    actual_url = login_page.open()
    assert actual_url == 'https://dotesthere.com/'

def test_login(login_page: LoginPage):
    login_page.open()
    alert_message = login_page.login()
    assert alert_message == 'You logged into a secure area!'

def test_select_option(login_page: LoginPage):
    login_page.open()
    toast_message = login_page.select_option()
    assert toast_message == 'Selected: Option 2'
