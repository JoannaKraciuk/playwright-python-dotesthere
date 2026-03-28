import re
import requests
import pytest
import allure
import json

@pytest.mark.api
@allure.feature("API")
@allure.story("GET request")
def test_get_api_users(api_base_url):
    url = f"{api_base_url}/users"

    with allure.step("Send GET request"):
        resp = requests.get(url, timeout=10)

    with allure.step("Verify status code"):
        assert resp.status_code in (200,201), f"HTTP {resp.status_code}: {resp.text}"

    resp = requests.get(url, timeout=10)
    assert resp.status_code == 200

    body = resp.json()
    data_list = body["data"]

    assert isinstance(data_list, list) and len(data_list) >= 1

    for user in data_list:
        for key in ("id", "email", "first_name", "last_name", "avatar"):
            assert key in user, f"Brak klucza '{key}' w elemencie {user}"

        assert isinstance(user["id"], int) and user["id"] >= 1
        assert isinstance(user["first_name"], str) and user["first_name"]
        assert isinstance(user["last_name"], str) and user["last_name"]
        assert re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", user["email"])
        assert re.match(r"^https?://[^\s]+$", user["avatar"])

    print(json.dumps(data_list, indent=2))


