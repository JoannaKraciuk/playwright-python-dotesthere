
Playwright Python – DoTestHere
Automatyczne testy E2E w Pythonie z użyciem PyTest, Playwright oraz raportowaniem Allure.

✅ Wymagania

Python 3.10+
Przeglądarki Playwright (playwright install)
(Opcjonalnie) Allure CLI do generowania/otwierania raportów

✅ Instalacja
Windows (PowerShell):

python -m venv .venv
.\\.venv\\Scripts\\activate
pip install -r requirements.txt
playwright install



Linux/Mac (Bash):

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install


Minimalny requirements.txt:
pytest
pytest-playwright
playwright
allure-pytest


✅ Struktura projektu

playwright-python-dotesthere/

├─ pytest.ini

├─ conftest.py

├─ tests/

│  └─ test_login.py

├─ allure-results/        # generowane

└─ allure-report/         # generowane



Przykładowy pytest.ini:
[pytest]

markers =
    smoke: podstawowe testy smoke

testpaths = tests
addopts = -vv -s


✅ Uruchamianie testów
Podstawowo:
pytest


Z logami i zapisem wyników Allure:
pytest -vv -s --alluredir allure-results


Uruchom tylko smoke:
pytest -m smoke --alluredir allure-results

Uruchom tylko api:
pytest -m api --alluredir allure-results


Filtrowanie po nazwie:
pytest -k login --alluredir allure-results


✅ Raporty Allure
Szybkie serwowanie:
allure serve allure-results


Statyczny raport + otwarcie:
allure generate allure-results -o allure-report --clean
allure open allure-report


Jedna komenda (Windows PowerShell):

python -m pytest -vv -s --alluredir allure-results; allure generate allure-results -o allure-report --clean; allure open allure-report


✅ Uruchamianie z PyCharm

Interpreter: 

File → Settings → Project → Python Interpreter → wybierz .venv tego projektu.
Run → Edit Configurations… → PyTest:Working directory: katalog projektu
Additional Arguments: -vv -s --alluredir allure-results
Environment variables: puste (chyba że potrzebne dla środowiska)