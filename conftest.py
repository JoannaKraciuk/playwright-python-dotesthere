import os
import pytest

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://dotesthere.com")

@pytest.fixture(scope="session")
def _pw():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(_pw, pytestconfig):
    headed = pytestconfig.getoption("--headed")
    b = _pw.chromium.launch(headless=True, slow_mo=800)  # headed=True => headless=False
    yield b
    b.close()

@pytest.fixture
def context(browser):
    ctx = browser.new_context()
    yield ctx
    ctx.close()

@pytest.fixture
def page(context):
    p = context.new_page()
    yield p
    p.close()

@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture(scope="session")
def api_base_url() -> str:
    return os.getenv("API_BASE_URL", "https://dotesthere.com/api")
