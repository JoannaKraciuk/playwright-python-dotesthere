import re
import requests
import pytest
import allure
from datetime import datetime

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ISO_Z_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")

@pytest.mark.smoke
@pytest.mark.api
@allure.feature("API")
@allure.story("POST request")
def test_post_users_full_payload(api_base_url):
    url = f"{api_base_url}/users"

    payload = {
        "first_name": "John",
        "name": "Nowak",
        "job": "Tester",
        "email": "test@test.com",
    }

    with allure.step("Send POST request"):
        resp = requests.post(url, json=payload, timeout=10)

    with allure.step("Verify status code"):
        assert resp.status_code in (200,201), f"HTTP {resp.status_code}: {resp.text}"

    body = resp.json()
    # Obsługa dwóch możliwych kształtów odpowiedzi
    user = body.get("data", body)

    with allure.step("Verify required fields in response"):
        for key in ("id", "first_name", "name", "job", "email"):
            assert key in user, f"Brak klucza '{key}' w odpowiedzi"

    with allure.step("Verify echo of payload"):
        assert user["first_name"] == payload["first_name"]
        assert user["name"] == payload["name"]
        assert user["job"] == payload["job"]
        assert user["email"] == payload["email"]