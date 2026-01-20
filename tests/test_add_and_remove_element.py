import pytest
import allure
from pages.login_page import LoginPage
from pages.elements_page import ElementsPage

@pytest.mark.smoke
@allure.epic("Okno dodawania elementu")
@allure.feature("Dodanie elementu")
@allure.severity(allure.severity_level.CRITICAL)
class TestElements:
    @allure.story("Użytkownik może dodać element w systemie")
    def test_add_element(page, login_page: LoginPage, elements_page: ElementsPage):

        with allure.step("Przejście do strony https://dotesthere.com/"):
            login_page.open()

        with allure.step("Dodanie elementu w systemie"):
            confirmation_message = elements_page.add_element()
            assert confirmation_message == "Element added! ➕"

    @allure.story("Użytkownik może usunąć element z systemu")
    def test_delete_element(page, login_page: LoginPage, elements_page: ElementsPage):

        with allure.step("Przejście do strony https://dotesthere.com/"):
            login_page.open()

        with allure.step("Usunięcie elementu z systemu"):
            confirmation_message = elements_page.delete_element()
            assert confirmation_message == "Element removed! 🗑️"