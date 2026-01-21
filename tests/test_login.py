import pytest
import allure
from pages.login_page import LoginPage
from utils.test_data import USERNAMES, PASSWORDS

@allure.epic("Strona główna")
@allure.feature("Testy url oraz logowania")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    @allure.story("Użytkownik po przejściu na stronę główną, weryfikuje jej aktualny adres url")
    def test_open_login(self, login_page: LoginPage):

        with allure.step("Przejście do strony https://dotesthere.com/"):
            actual_url = login_page.open()

        with allure.step("Weryfikacja prawidłowego adresu url strony."):
            assert actual_url == 'https://dotesthere.com/', "Adres strony jest nieprawidłowy"

    @pytest.mark.parametrize(("username", "password"), [(USERNAMES["valid"], PASSWORDS["valid"])])
    @allure.story("Użytkownik może zalogować się poprawnymi danymi")
    def test_login(self, login_page: LoginPage, username, password):

        with allure.step("Wejście na stronę logowania"):
            login_page.open()

        with allure.step("Wprowadzenie poprawnych danych"):
            alert_message = login_page.login(username, password)

        with allure.step("Weryfikacja komunikatu i widoku po zalogowaniu"):
            assert alert_message == 'You logged into a secure area!', "Brak komunikatu powitalnego"

        with allure.step("Weryfikacja komunikatu sukcesu"):
            toast_message = login_page.read_toast()
            assert toast_message == 'Login successful!'

    @pytest.mark.parametrize(("username", "password"), [(USERNAMES["invalid"], PASSWORDS["valid"])])
    @allure.story("Próba logowania błędnym loginem")
    def test_login_invalid_username(self, login_page: LoginPage, username, password):
        with allure.step("Wejście na stronę logowania"):
            login_page.open()

        with allure.step("Wprowadzenie niepoprawnego loginu i poprawnego hasła"):
            alert_message = login_page.login(username, password)

        with allure.step("Weryfikacja komunikatu i widoku po zalogowaniu"):
            assert alert_message == "Your username is invalid!", "Brak komunikatu o błędzie"

        with allure.step("Weryfikacja komunikatu sukcesu"):
            toast_message = login_page.read_toast()
            assert toast_message == 'Invalid credentials'

    @pytest.mark.parametrize(("username", "password"), [(USERNAMES["valid"], PASSWORDS["invalid"])])
    @allure.story("Próba logowania błędnym hasłem")
    def test_login_invalid_password(self, login_page: LoginPage, username, password):
        with allure.step("Wejście na stronę logowania"):
            login_page.open()

        with allure.step("Wprowadzenie poprawny login i niepoprawne hasło"):
            alert_message = login_page.login(username, password)

        with allure.step("Weryfikacja komunikatu i widoku po zalogowaniu"):
            assert alert_message == "Your username is invalid!", "Brak komunikatu o błędzie"

        with allure.step("Weryfikacja komunikatu sukcesu"):
            toast_message = login_page.read_toast()
            assert toast_message == 'Invalid credentials'
