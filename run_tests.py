import subprocess
import sys
import platform
import os

def run_command(command):
    """Uruchamia komendę i przerywa przy błędzie"""
    print(f"\n>> Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        sys.exit(result.returncode)

def open_report(path):
    """Otwiera statyczny raport w przeglądarce w zależności od OS"""
    system = platform.system()
    if system == "Windows":
        run_command(f'start "" "{os.path.abspath(path)}"')
    elif system == "Darwin":  # Mac
        run_command(f'open "{os.path.abspath(path)}"')
    else:  # Linux
        run_command(f'xdg-open "{os.path.abspath(path)}"')

def main():
    allure_results = "allure-results"
    allure_report = "allure-report"

    # 1. Uruchom testy
    run_command(f"pytest -vv -s --alluredir {allure_results}")

    # 2. Otwórz raport tymczasowy w przeglądarce (serve)
    print("\n🔹 Opening temporary Allure report (serve)...")
    run_command(f"allure serve {allure_results}")

    # 3. Wygeneruj statyczny raport
    print("\n🔹 Generating static Allure report...")
    run_command(f"allure generate {allure_results} -o {allure_report} --clean")

    # 4. Otwórz statyczny raport w przeglądarce
    print("\n🔹 Opening static Allure report...")
    index_html = os.path.join(allure_report, "index.html")
    if os.path.exists(index_html):
        open_report(index_html)
    else:
        print(f"❌ Could not find {index_html} to open")

if __name__ == "__main__":
    main()