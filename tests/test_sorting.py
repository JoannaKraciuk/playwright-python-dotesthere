import pytest
import allure
from pages.login_page import LoginPage
from pages.sorting_page import SortingPage

@allure.epic("Sortable Data Tables")
@allure.feature("Sort Last Name column")
@allure.story("Użytkownik może sortować kolumnę 'Last Name' malejąco o rosnąco")
@allure.severity(allure.severity_level.CRITICAL)
def test_sort_last_name_asc(login_page: LoginPage, sorting_page: SortingPage):
    login_page.open()

    with allure.step("Kliknięcie nagłówka kolumny Last Name (ASC)"):
        sorting_page.sort_last_name_toggle()

    with allure.step("Pobranie wartości kolumny Last Name"):
        last_names = sorting_page.get_last_name_values()

    with allure.step("Weryfikacja sortowania A–Z"):
        assert last_names == sorted(last_names, key=str.lower), \
            "Kolumna 'Last Name' nie jest posortowana rosnąco (A–Z)"
        print(last_names)