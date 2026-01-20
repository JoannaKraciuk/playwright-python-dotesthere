import pytest
import allure
from pages.login_page import LoginPage
from pages.dynamic_controls_page import DynamicPage

@allure.epic("Dynamic Controls")
@allure.feature("Enalbe/Disable input")
@allure.story("Użytkownik może włączać/wyłączać pole i widzi komunikat")
@allure.severity(allure.severity_level.CRITICAL)

def test_dynamic_controls(page, login_page: LoginPage, dynamic_page: DynamicPage):

    with allure.step("Przejście do strony DoTestHere"):
        login_page.open()

    with allure.step("Zmiana inputu na dostępny"):
        assert dynamic_page.enable_input() is True

    with allure.step("Pobranie komunikatu 'Element jest dostępny'"):
        assert dynamic_page.get_toast_message() == "Input enabled!"

    with allure.step("Wypełnienie pola input"):
        assert dynamic_page.fill_input("Playwright dynamic controls") == "Playwright dynamic controls"

    with allure.step("Zmiana inputu na niedostępny"):
        assert dynamic_page.disable_input() is True

    with allure.step("Pobranie komunikatu 'Element jest niedostępny'"):
        assert dynamic_page.get_toast_message() == "Input disabled!"