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
