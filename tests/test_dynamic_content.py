import pytest
import allure
from pages.login_page import LoginPage
from pages.dynamic_content_page import DynamicContentPage

@pytest.mark.smoke
@allure.epic("Dynamiczny tekst")
@allure.feature("Dynamiczna zmiana tekstu")
@allure.story("Użytkownik może dynamicznie zmieniać i pobierać tekst")
@allure.severity(allure.severity_level.NORMAL)
def test_select_option(login_page: LoginPage, dynamic_content_page: DynamicContentPage):
    with allure.step("Przejście do strony DoTestHere"):
        login_page.open()

    with allure.step("Kliknięcie przycisku 'Refresh Content' i pobranie dynamicznego tekstu"):
        before = dynamic_content_page.dynamic_text.inner_text()
        after = dynamic_content_page.click_change_and_get_text()
        assert before != after
