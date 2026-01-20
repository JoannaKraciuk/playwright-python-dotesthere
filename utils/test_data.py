import configparser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

config = configparser.ConfigParser()
config.read(ROOT_DIR / "config" / "test_data.ini")

UPLOAD_FILES = config["upload_files"]
