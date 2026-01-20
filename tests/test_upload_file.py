import pytest
import allure
from pages.login_page import LoginPage
from pages.upload_page import UploadPage
from utils.test_data import UPLOAD_FILES


@allure.epic("Okno dodawania pliku")
@allure.feature("Upload pliku")
@allure.story("Użytkownik może dodać plik w systemie")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("file_key", ["valid"])
def test_upload_file(page, login_page: LoginPage, upload_page: UploadPage, file_key):
    with allure.step("Przejście do strony DoTestHere"):
        login_page.open()
    with allure.step("Dołączenie pliku do systemu"):
        message = upload_page.upload_file(UPLOAD_FILES[file_key])
        assert "uploaded successfully!" in message.lower()