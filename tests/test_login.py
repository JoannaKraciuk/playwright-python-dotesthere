import pytest
import allure
from pages.login_page import LoginPage

@allure.epic("Strona główna")
@allure.feature("Weryfikacja adresu url")
@allure.story("Użytkownik po przejściu do strony https://dotesthere.com/ weryfikuje jej aktualny adres url")
@allure.severity(allure.severity_level.CRITICAL)
def test_open_login(login_page: LoginPage):
    with allure.step("Przejście do strony https://dotesthere.com/"):
        actual_url = login_page.open()
    with allure.step("Weryfikacja prawidłowego adresu url strony."):
        assert actual_url == 'https://dotesthere.com/', "Adres strony jest nieprawidłowy"

@allure.epic("Strona logowania")
@allure.feature("Logowanie")
@allure.story("Użytkownik może zalogować się poprawnymi danymi")
@allure.severity(allure.severity_level.CRITICAL)
def test_login(login_page: LoginPage):
    with allure.step("Wejście na stronę logowania"):
        login_page.open()
    with allure.step("Wprowadzenie poprawnych danych"):
        alert_message = login_page.login('ankur', 'automation')
    with allure.step("Weryfikacja komunikatu i widoku po zalogowaniu"):
        assert alert_message == 'You logged into a secure area!', "Brak komunikatu powitalnego"

@allure.epic("Dropdown")
@allure.feature("Wybór opcji z listy rozwijalnej")
@allure.story("Użytkownik może wybrać jedną z opcji na liście rozwijalnej")
@allure.severity(allure.severity_level.NORMAL)
def test_select_option(login_page: LoginPage):
    login_page.open()
    toast_message = login_page.select_option()
    assert toast_message == 'Selected: Option 2'

@allure.epic("Okno dodawania pliku")
@allure.feature("Upload pliku")
@allure.story("Użytkownik może dodać plik w systemie")
@allure.severity(allure.severity_level.CRITICAL)
def test_upload_file(page, login_page: LoginPage):
    login_page.open()
    message = login_page.upload_file("tests/files/Plik 8.pdf")
    assert "uploaded successfully!" in message

@pytest.mark.smoke
@allure.epic("Okno dodawania elementu")
@allure.feature("Dodanie elementu")
@allure.story("Użytkownik może dodać element w systemie")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_element(page, login_page: LoginPage):
    login_page.open()
    confirmation_message = login_page.add_element()
    assert confirmation_message == "Element added! ➕"

@pytest.mark.smoke
@allure.epic("Okno usuwania elementu")
@allure.feature("Usunięcie elementu")
@allure.story("Użytkownik może usunąć element z systemu")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_element(page, login_page: LoginPage):
    login_page.open()
    confirmation_message = login_page.delete_element()
    assert confirmation_message == "Element removed! 🗑️"

