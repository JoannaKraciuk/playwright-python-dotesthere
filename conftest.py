
# conftest.py
import os
import re
import pytest
import allure
from pathlib import Path
from typing import Union
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# --- Katalogi na artefakty (lokalnie/CI) ---
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

# --- Playwright root (session) ---
@pytest.fixture(scope="session")
def _pw():
    with sync_playwright() as p:
        yield p

# --- Przeglądarka (session) ---
@pytest.fixture(scope="session")
def browser(_pw) -> Browser:
    # Headless w CI i lokalnie (spójność)
    browser = _pw.chromium.launch(
        headless=True,
        args=["--disable-dev-shm-usage", "--disable-gpu"]
    )
    yield browser
    browser.close()

# --- Context (per test) ---
@pytest.fixture
def context(browser: Browser, request) -> BrowserContext:
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 800},
        record_video_dir="videos",
        record_video_size={"width": 1280, "height": 720},
    )
    # Start trace na początku testu
    ctx.tracing.start(
        title=request.node.nodeid,
        screenshots=True,
        snapshots=True,
        sources=True,
    )
    yield ctx

    # Jeśli do tego momentu trace nie był zapisany (fail w hooku) – zatrzymaj (bez zapisu)
    try:
        ctx.tracing.stop()
    except Exception:
        pass

    ctx.close()

# --- Strona (per test) ---
@pytest.fixture
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    # Opcjonalnie: sensowny timeout dla stabilności
    p.set_default_timeout(10_000)
    yield p
    # Zamknięcie strony przed próbą pobrania video w hooku (gdybyś chciała dołączyć)
    try:
        p.close()
    except Exception:
        pass

# --- Page Object Model fixtures ---
from pages.dropdown_page import DropdownPage
from pages.dynamic_controls_page import DynamicPage
from pages.elements_page import ElementsPage
from pages.login_page import LoginPage
from pages.sorting_page import SortingPage
from pages.upload_page import UploadPage
from pages.dynamic_content_page import DynamicContentPage

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

@pytest.fixture
def dynamic_page(page: Page) -> DynamicPage:
    return DynamicPage(page)

@pytest.fixture
def dropdown_page(page: Page) -> DropdownPage:
    return DropdownPage(page)

@pytest.fixture
def upload_page(page: Page) -> UploadPage:
    return UploadPage(page)

@pytest.fixture
def elements_page(page: Page) -> ElementsPage:
    return ElementsPage(page)

@pytest.fixture
def sorting_page(page: Page) -> SortingPage:
    return SortingPage(page)

@pytest.fixture
def dynamic_content_page(page: Page) -> DynamicContentPage:
    return DynamicContentPage(page)

# --- Hook: artefakty Allure przy failu ---
def _safe_name(nodeid: str) -> str:
    # bezpieczna nazwa pliku (Windows/CI)
    name = nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
    name = re.sub(r"[^\w\-.]+", "_", name)
    return name

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Dodaje screenshot + trace do Allure na FAIL.
    Gdy PASS – zatrzymuje trace bez zapisu.
    """
    outcome = yield
    rep = outcome.get_result()

    # Interesuje nas tylko faza call (test body)
    if rep.when != "call":
        return

    page = item.funcargs.get("page", None)
    context = item.funcargs.get("context", None)
    safe = _safe_name(item.nodeid)

    if rep.failed:
        # 1) TRACE
        if context:
            trace_path = Path("traces") / f"{safe}.zip"
            try:
                context.tracing.stop(path=str(trace_path))
            except Exception:
                # jeśli już zatrzymany – ignorujemy
                trace_path = None

            if trace_path and trace_path.exists():
                try:
                    allure.attach.file(
                        str(trace_path),
                        name=f"trace-{safe}",
                        attachment_type=allure.attachment_type.ZIP
                    )
                except Exception:
                    pass

        # 2) SCREENSHOT
        if page:
            screenshot_path = Path("screenshots") / f"{safe}.png"
            try:
                # full_page=True często pomaga w headless przy krótkich viewportach
                page.screenshot(path=str(screenshot_path), full_page=True)
                allure.attach.file(
                    str(screenshot_path),
                    name=f"screenshot-{safe}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass
    else:
        # PASS – zatrzymujemy trace bez zapisu (gdy jeszcze aktywny)
        if context:
            try:
                context.tracing.stop()
            except Exception:
                pass

        # (opcjonalnie) czyścimy video dla PASS
        if page and page.video:
            try:
                video_path = page.video.path()  # wymaga close() strony
                if video_path and os.path.exists(video_path):
                    os.remove(video_path)
            except Exception:
                pass
