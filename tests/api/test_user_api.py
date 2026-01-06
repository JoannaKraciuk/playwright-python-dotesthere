import re
import requests
import pytest

from datetime import datetime


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
URL_RE = re.compile(r"^https?://[^\s]+$")


@pytest.mark.smoke
def test_get_users_ok(api_base_url):
    url = f"{api_base_url}/users?page=1&limit=10"

    resp = requests.get(url, timeout=10)
    assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text}"

    data = resp.json()

    # 2) Sprawdzenie paginacji i typów
    assert isinstance(data, dict)
    for key in ("page", "per_page", "total", "total_pages", "data"):
        assert key in data, f"Brak klucza '{key}' w odpowiedzi"

    assert isinstance(data["page"], int) and data["page"] == 1
    assert isinstance(data["per_page"], int) and data["per_page"] == 10
    assert isinstance(data["total"], int) and data["total"] >= 2
    assert isinstance(data["total_pages"], int) and data["total_pages"] >= 1

    # 3) Struktura listy data
    assert isinstance(data["data"], list), "Pole 'data' powinno być listą"
    assert len(data["data"]) >= 1, "Oczekiwano co najmniej 1 elementu w 'data'"

    first = data["data"][0]
    for key in ("id", "email", "first_name", "last_name", "avatar"):
        assert key in first, f"Brak klucza '{key}' w elemencie danych"

    # 4) Typy i podstawowe wartości
    assert isinstance(first["id"], int) and first["id"] >= 1
    assert isinstance(first["first_name"], str) and first["first_name"]
    assert isinstance(first["last_name"], str) and first["last_name"]
    assert isinstance(first["email"], str) and EMAIL_RE.match(first["email"]), "Niepoprawny format email"
    assert isinstance(first["avatar"], str) and URL_RE.match(first["avatar"]), "Niepoprawny URL avatara"

@pytest.mark.smoke
def test_user_by_first_id(api_base_url):
    url = f"{api_base_url}/users/1"

    resp = requests.get(url, timeout=10)
    assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text}"

    body = resp.json()

    # Sprawdź, że top-level zawiera 'data'
    assert "data" in body and isinstance(body["data"], dict), "Brak klucza 'data' lub nie jest dictem"

    user = body["data"]

    # Wymagane klucze wewnątrz 'data'
    for key in ("id", "email", "first_name", "last_name", "avatar"):
        assert key in user, f"Brak klucza '{key}' w elemencie danych"

    # Typy i wartości
    assert isinstance(user["id"], int) and user["id"] == 1
    assert isinstance(user["email"], str) and user["email"] == "ankur.automation@dotesthere.com"
    assert isinstance(user["first_name"], str) and user["first_name"] == "Ankur"
    assert isinstance(user["last_name"], str) and user["last_name"] == "Autoamtion"
    assert isinstance(user["avatar"], str) and user["avatar"] == "https://dotesthere.com/img/faces/1-image.jpg"


@pytest.mark.smoke
def test_user_by_second_id(api_base_url):
    url = f"{api_base_url}/users/2"

    resp = requests.get(url, timeout=10)
    assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text}"

    body = resp.json()

    # Sprawdź, że top-level zawiera 'data'
    assert "data" in body and isinstance(body["data"], dict), "Brak klucza 'data' lub nie jest dictem"

    user = body["data"]

    # Wymagane klucze wewnątrz 'data'
    for key in ("id", "email", "first_name", "last_name", "avatar"):
        assert key in user, f"Brak klucza '{key}' w elemencie danych"

    # Typy i wartości
    assert isinstance(user["id"], int) and user["id"] == 2
    assert isinstance(user["email"], str) and user["email"] == "janet.weaver@dotesthere.com"
    assert isinstance(user["first_name"], str) and user["first_name"] == "Janet"
    assert isinstance(user["last_name"], str) and user["last_name"] == "Weaver"
    assert isinstance(user["avatar"], str) and user["avatar"] == "https://dotesthere.com/img/faces/2-image.jpg"


# ISO-8601 z sufiksem Z, np. 2023-01-01T12:00:00.000Z
ISO_Z_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")


@pytest.mark.smoke
def test_post_users_returns_echo_and_metadata(api_base_url):
    url = f"{api_base_url}/users"
    payload = {
        "first_name": "John",
        "name": "Nowak",
        "job": "Tester",
        "email": "test@test.com",
    }

    resp = requests.post(url, json=payload, timeout=10)
    assert resp.status_code in (200, 201), f"HTTP {resp.status_code}: {resp.text}"

    body = resp.json()
    assert "data" in body and isinstance(body["data"], dict), "Brak 'data' na top-level"

    user = body["data"]  # ✅ właściwy poziom

    # Klucze wymagane w odpowiedzi
    for key in ("id", "email", "first_name", "name", "job", "createdAt"):
        assert key in user, f"Brak klucza '{key}' w odpowiedzi"

    # Echo payloadu (jeśli API zwraca wysłane pola)
    assert user["name"] == payload["name"]
    assert user["job"] == payload["job"]
    assert user["email"] == payload["email"]
    assert user["first_name"] == payload["first_name"]

    assert isinstance(user["id"], int) and str(user["id"]).strip(), "Pole 'id' powinno być niepuste"
    # 'createdAt' – ISO-8601 z 'Z'
    assert isinstance(user["createdAt"], str) and ISO_Z_RE.match(user["createdAt"]), "createdAt nie jest ISO-8601 z 'Z'"

    dt = datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00"))
    assert dt.year >= 1970, "Parsowanie createdAt zakończone nieprawidłową datą"

@pytest.mark.smoke
def test_post_users_minimal_metadata(api_base_url):
    url = f"{api_base_url}/users"
    payload = {
        "first_name": "John",
        "name": "Nowak",
        "job": "Tester",
        "email": "test@test.com",
    }

    resp = requests.post(url, json=payload, timeout=10)
    assert resp.status_code in (200, 201), f"HTTP {resp.status_code}: {resp.text}"

    body = resp.json()
    obj = body.get("data", body)  # obsługa 2 kształtów: z wrapperem i bez

    for key in ("id", "createdAt"):
        assert key in obj, f"Brak '{key}' w odpowiedzi"

    assert isinstance(obj["id"], (str, int)) and str(obj["id"]).strip()
    assert isinstance(obj["createdAt"], str) and ISO_Z_RE.match(obj["createdAt"])

    # Parsowanie daty:
    dt = datetime.fromisoformat(obj["createdAt"].replace("Z", "+00:00"))
    assert dt.year >= 1970