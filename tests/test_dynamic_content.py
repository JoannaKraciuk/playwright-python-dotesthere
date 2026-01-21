import pytest
import allure
from pages.login_page import LoginPage
from pages.dynamic_content_page import DynamicContentPage

@pytest.mark.smoke
@allure.epic("Dynamiczny tekst")
@allure.feature("Dynamiczna zmiana tekstu")
@allure.severity(allure.severity_level.NORMAL)

class TestDynamicContent:
    @allure.story("Użytkownik może dynamicznie zmieniać i pobierać tekst")
    def test_check_dynamic_content(self, login_page: LoginPage, dynamic_content_page: DynamicContentPage):
        with allure.step("Przejście do strony DoTestHere"):
            login_page.open()

        with allure.step("Kliknięcie przycisku 'Refresh Content' i pobranie dynamicznego tekstu"):
            before = dynamic_content_page.dynamic_text.inner_text()
            after = dynamic_content_page.click_change_and_get_text()
            assert before != after

    @allure.story("Użytkownik klika dwukrotnie w przycisk 'Refresh Content'")
    def test_double_click(self, login_page: LoginPage, dynamic_content_page: DynamicContentPage):
        with allure.step("Przejście do strony DoTestHere"):
            login_page.open()

        with allure.step("Dwukrotne kliknięcie w przycisk 'Refresh Content' i porównanie dynamicznego tekstu"):
            before = dynamic_content_page.dynamic_text.inner_text()
            after = dynamic_content_page.double_click_refresh()
            assert before != after

