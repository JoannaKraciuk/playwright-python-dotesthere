
import subprocess
import sys
import platform
import os

def run_command(command):
    print(f"\n>> Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        sys.exit(result.returncode)

def open_report(path):
    system = platform.system()
    if system == "Windows":
        os.startfile(os.path.abspath(path))
    elif system == "Darwin":
        run_command(f'open "{os.path.abspath(path)}"')
    else:
        run_command(f'xdg-open "{os.path.abspath(path)}"')

def main():
    allure_results = "allure-results"
    allure_report = "allure-report"

    # 1. Uruchom testy
    run_command(f"pytest -vv -s --alluredir {allure_results}")

    # 2. Generuj statyczny raport
    run_command(f"allure generate {allure_results} -o {allure_report} --clean")

    # 3. Otwórz statyczny raport
    index_html = os.path.join(allure_report, "index.html")
    if os.path.exists(index_html):
        open_report(index_html)
    else:
        print(f"❌ Could not find {index_html} to open")

if __name__ == "__main__":
    main()