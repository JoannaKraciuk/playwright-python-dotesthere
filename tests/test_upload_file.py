import pytest
import allure
from pages.login_page import LoginPage
from pages.upload_page import UploadPage


@allure.epic("Okno dodawania pliku")
@allure.feature("Upload pliku")
@allure.story("Użytkownik może dodać plik w systemie")
@allure.severity(allure.severity_level.CRITICAL)
def test_upload_file(page, login_page: LoginPage, upload_page: UploadPage):
    with allure.step("Przejście do strony DoTestHere"):
        login_page.open()
    with allure.step("Dołączenie pliku do systemu"):
        message = upload_page.upload_file('tests/files/Plik 8.pdf')
        assert "uploaded successfully!" in message