Playwright Python – DoTestHere

Automatyczne testy E2E w Pythonie z użyciem PyTest, Playwright, z raportowaniem w Allure.
Projekt pokazuje dobre praktyki w automatyzacji testów: POM (Page Object Model), parametryzacja testów oraz generowanie raportów.

✅ Wymagania

- Python 3.10+
- Przeglądarki Playwright (playwright install)
- (Opcjonalnie) Allure CLI do generowania raportów

✅ Instalacja

Windows (PowerShell):
```text
python -m venv .venv
.\\.venv\\Scripts\\activate
pip install -r requirements.txt
playwright install
```
```text
Linux / Mac (Bash):
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

Minimalny requirements.txt:
```text
pytest
pytest-playwright
playwright
allure-pytest
```
✅ Struktura projektu
```text
playwright-python-dotesthere/
├─ pytest.ini
├─ conftest.py              # konfiguracja PyTest i fixture
├─ tests/
│   └─ test_login.py        # przykładowe testy logowania
├─ pages/                   # Page Object Model – klasy stron
├─ utils/                   # funkcje pomocnicze, np. logi i screenshoty
├─ allure-results/          # generowane raporty Allure
└─ allure-report/           # generowane raporty statyczne
```
✅ Uruchamianie testów

Podstawowo:
```text
pytest
```
Z logami i zapisaniem wyników do Allure:
```text
pytest -vv -s --alluredir allure-results
```
Uruchom tylko smoke:
```text
pytest -m smoke --alluredir allure-results
```
Uruchom tylko API:
```text
pytest -m api --alluredir allure-results
```
Filtrowanie po nazwie testu:
```text
pytest -k login --alluredir allure-results
```
✅ Raporty Allure

Szybki:
```text
allure serve allure-results
```
Statyczny raport + otwarcie:
```text
allure generate allure-results -o allure-report --clean
allure open allure-report
```
Jedna komenda (Windows PowerShell):
```text
python -m pytest -vv -s --alluredir allure-results; allure generate allure-results -o allure-report --clean; allure open allure-report
```

✅ Uruchamianie z PyCharm

Interpreter: .venv projektu

Run → Edit Configurations → PyTest

Working directory: katalog projektu

Additional Arguments: -vv -s --alluredir allure-results

Environment variables: puste (chyba że potrzebne dla środowiska)

✅ Dobre praktyki w projekcie

POM (Page Object Model): oddzielne klasy dla każdej strony, łatwe do utrzymania i rozbudowy testów.

Parametryzacja testów: testy mogą działać dla różnych danych wejściowych bez powielania kodu.

Logi i screenshoty: przy błędach generowane są screenshoty i logi, widoczne w raportach Allure.

Czytelny kod: sensowne nazwy testów i funkcji, komentarze wyjaśniające krok testowy.

✅ Przykłady raportów

![Raport_Allure](screenshots/2026-01-22_09h40_48.png)
![Raport_Allure](screenshots/2026-01-22_09h42_23.png)
![Raport_Allure](screenshots/2026-01-22_09h42_55.png)
![Raport_Allure](screenshots/2026-01-22_09h43_22.png)
