
import os
import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright

from pages.dynamic_controls_page import DynamicPage
from pages.login_page import LoginPage

os.makedirs("screenshots", exist_ok=True)
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
    # Nagrywanie wideo do katalogu "videos"
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

    # Wideo materializuje się dopiero po close()
    context.close()


@pytest.fixture
def page(context):
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def dynamic_page(page):
    return DynamicPage(page)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Po każdym teście zatrzymuje tracing i:
      - na FAIL: dołącza trace (.zip) i wideo (.webm) do Allure,
      - na PASS: zamyka trace bez pliku, usuwa wideo.
    Zabezpieczone try/except, aby uniknąć INTERNALERROR.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    page = item.funcargs.get("page")
    context = item.funcargs.get("context")

    # Unikalna i bezpieczna nazwa artefaktów
    safe_name = (
        item.nodeid
        .replace("::", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    # Katalogi na pliki
    os.makedirs("traces", exist_ok=True)

    # --- FAIL ---
    if rep.failed:
        os.makedirs("traces", exist_ok=True)

        if context:
            trace_path = f"traces/{safe_name}.zip"

            context.tracing.stop(path=trace_path)

            allure.attach.file(
                trace_path,
                name="Playwright Trace",
                extension=".zip",
            )
    # -------- PASS --------
    else:
        if context:
            context.tracing.stop()

        if page and page.video:
            try:
                os.remove(page.video.path())
            except Exception:
                pass