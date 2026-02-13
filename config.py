from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DB_PATH = PROJECT_ROOT / "data/weather.db" # a local SQLITE3 database used for early testing.
DESC_PATH = PROJECT_ROOT / "descriptions.json" # path to weather code descriptions JSON file. Very important.
TIME_PATH = PROJECT_ROOT / "update_time.txt" # no longer used, but kept for reference. May be deleted in future updates.