import os
import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright

from pages.dropdown_page import DropdownPage
from pages.dynamic_controls_page import DynamicPage
from pages.elements_page import ElementsPage
from pages.login_page import LoginPage
from pages.sorting_page import SortingPage
from pages.upload_page import UploadPage
from pages.dynamic_content_page import DynamicContentPage

# Tworzymy foldery na screenshoty i artefakty
os.makedirs("screenshots", exist_ok=True)
os.makedirs("traces", exist_ok=True)
os.makedirs("videos", exist_ok=True)

# --- Konfiguracja bazowych URL ---
@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://dotesthere.com")

@pytest.fixture(scope="session")
def api_base_url() -> str:
    return os.getenv("API_BASE_URL", "https://dotesthere.com/api")

# --- Playwright / Browser ---
@pytest.fixture(scope="session")
def _pw():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(_pw):
    browser = _pw.chromium.launch(headless=False, slow_mo=800)  # zawsze headed
    yield browser
    browser.close()

# --- Context / Page ---
@pytest.fixture
def context(browser, request):
    context = browser.new_context(
        record_video_dir="videos",
        record_video_size={"width": 1280, "height": 720},
    )

    # Start tracingu na początku testu
    context.tracing.start(
        title=request.node.nodeid,
        screenshots=True,
        snapshots=True,
        sources=True,
    )
    yield context
    context.close()

@pytest.fixture
def page(context):
    p = context.new_page()
    yield p
    p.close()

# --- Page Object Model Fixtures ---
@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def dynamic_page(page):
    return DynamicPage(page)

@pytest.fixture
def dropdown_page(page):
    return DropdownPage(page)

@pytest.fixture
def upload_page(page):
    return UploadPage(page)

@pytest.fixture
def elements_page(page):
    return ElementsPage(page)

@pytest.fixture
def sorting_page(page):
    return SortingPage(page)

@pytest.fixture
def dynamic_content_page(page):
    return DynamicContentPage(page)

# --- Hook do raportowania fail / artefaktów ---
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Dodaje screenshoty i trace do raportu Allure przy fail
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    page = item.funcargs.get("page")
    context = item.funcargs.get("context")

    # Bezpieczna nazwa artefaktu
    safe_name = (
        item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
    )

    # --- FAIL ---
    if rep.failed:
        if context:
            trace_path = f"traces/{safe_name}.zip"
            context.tracing.stop(path=trace_path)
            allure.attach.file(trace_path, name="Playwright Trace", extension=".zip")

        if page:
            # screenshot przy fail
            screenshot_path = f"screenshots/{safe_name}.png"
            page.screenshot(path=screenshot_path)
            allure.attach.file(
                screenshot_path,
                name="Screenshot on Fail",
                attachment_type=allure.attachment_type.PNG,
            )
    else:
        # --- PASS ---
        if context:
            context.tracing.stop()
        if page and page.video:
            try:
                os.remove(page.video.path())
            except Exception:
                pass
