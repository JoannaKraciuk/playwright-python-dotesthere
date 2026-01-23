
import pytest
import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.dynamic_content_page import DynamicContentPage


@pytest.mark.smoke
@allure.epic("Dynamiczny tekst")
@allure.feature("Dynamiczna zmiana tekstu")
@allure.severity(allure.severity_level.NORMAL)
class TestDynamicContent:

    @allure.story("Użytkownik może dynamicznie zmieniać i pobierać tekst")
    def test_check_dynamic_content(
        self,
        login_page: LoginPage,
        dynamic_content_page: DynamicContentPage
    ):
        with allure.step("Przejście do strony DoTestHere"):
            login_page.open()

        with allure.step("Kliknięcie 'Refresh Content' i oczekiwanie na zmianę tekstu"):
            before = dynamic_content_page.dynamic_text.inner_text()
            dynamic_content_page.refresh_button.click()
            # Czekamy aż treść będzie inna niż 'before'
            expect(dynamic_content_page.dynamic_text).not_to_have_text(before, timeout=10_000)

        with allure.step("Weryfikacja, że tekst się zmienił"):
            after = dynamic_content_page.dynamic_text.inner_text()
            assert before != after

    @allure.story("Użytkownik klika dwukrotnie w przycisk 'Refresh Content'")
    def test_double_click(
        self,
        login_page: LoginPage,
        dynamic_content_page: DynamicContentPage
    ):
        with allure.step("Przejście do strony DoTestHere"):
            login_page.open()

        with allure.step("Dwukrotne kliknięcie i oczekiwanie na zmianę tekstu"):
            before = dynamic_content_page.dynamic_text.inner_text()
            dynamic_content_page.refresh_button.dblclick()
            expect(dynamic_content_page.dynamic_text).not_to_have_text(before, timeout=10_000)

        with allure.step("Weryfikacja, że tekst się zmienił"):
            after = dynamic_content_page.dynamic_text.inner_text()
            assert before != after

    @pytest.mark.parametrize("clicks", [1, 2, 5])
    @allure.story("Użytkownik może dynamicznie zmieniać tekst przyciskiem")
    def test_multi_click_dynamic_content(
        self,
        login_page: LoginPage,
        dynamic_content_page: DynamicContentPage,
        clicks: int
    ):
        with allure.step("Otwórz stronę DoTestHere"):
            login_page.open()

        with allure.step("Pobranie początkowego tekstu"):
            before = dynamic_content_page.dynamic_text.inner_text()

        with allure.step(f"Wykonanie {clicks} kliknięć w 'Refresh Content'"):
            for _ in range(clicks):
                dynamic_content_page.refresh_button.click()
                # krótkie odczekanie pomaga, ale kluczowe jest oczekiwanie na zmianę poniżej
                dynamic_content_page.page.wait_for_timeout(50)

        with allure.step("Oczekiwanie aż tekst będzie inny niż początkowy"):
            expect(dynamic_content_page.dynamic_text).not_to_have_text(before, timeout=10_000)

        with allure.step("Sprawdzenie, że tekst się zmienił po multi-click"):
            after = dynamic_content_page.dynamic_text.inner_text()
            assert before != after
