from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DB_PATH = PROJECT_ROOT / "weather.db"
DESC_PATH = PROJECT_ROOT / "descriptions.json"
TIME_PATH = PROJECT_ROOT / "update_time.txt"