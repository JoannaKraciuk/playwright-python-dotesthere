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

@allure.epic("Sortable Data Tables")
@allure.feature("Sort Last Name column")
@allure.story("Użytkownik może sortować kolumnę 'Last Name' malejąco o rosnąco")
@allure.severity(allure.severity_level.CRITICAL)
def test_sort_last_name_asc(login_page: LoginPage):
    login_page.open()

    with allure.step("Kliknięcie nagłówka kolumny Last Name (ASC)"):
        login_page.sort_last_name_toggle()

    with allure.step("Pobranie wartości kolumny Last Name"):
        last_names = login_page.get_last_name_values()

    with allure.step("Weryfikacja sortowania A–Z"):
        assert last_names == sorted(last_names, key=str.lower), \
            "Kolumna 'Last Name' nie jest posortowana rosnąco (A–Z)"
        print(last_names)
