import pytest
import allure
from pages.login_page import LoginPage
from pages.dropdown_page import DropdownPage

@allure.epic("Dropdown")
@allure.feature("Wybór opcji z listy rozwijalnej")
@allure.story("Użytkownik może wybrać jedną z opcji na liście rozwijalnej")
@allure.severity(allure.severity_level.NORMAL)
def test_select_option(login_page: LoginPage, dropdown_page: DropdownPage):
    with allure.step("Przejście do strony DoTestHere"):
        login_page.open()
    with allure.step("Wybranie opcji na dropdownu i pobranie komunikatu"):
        toast_message = dropdown_page.select_option()
        assert toast_message == 'Selected: Option 2'