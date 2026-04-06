from pathlib import Path
from typing import Dict, Optional
from dotenv import dotenv_values, find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DART_DIR = DATA_DIR / "dart"
DART_XML_PATH = DART_DIR / "dart_corp_code.xml"
DART_INDEX_PATH = DART_DIR / "dart_corp_index.json"
RESEARCH_DIR = DATA_DIR / "researches"
REPORTS_DIR = DATA_DIR / "reports"
BEST_REPORTS_DIR = DATA_DIR / "best_reports"
UPLOADS_DIR = DATA_DIR / "uploads"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
CACHE_DIR = DATA_DIR / "cache"


def load_env() -> Dict[str, Optional[str]]:
    env_path = find_dotenv(usecwd=True)
    if env_path:
        return dict(dotenv_values(env_path))
    return dict(dotenv_values(BASE_DIR / ".env.example"))


settings = load_env()

APP_TITLE: str = settings.get("APP_TITLE", "Coway-AIR") or "Coway-AIR"
DEBUG: bool = (settings.get("DEBUG", "false") or "false").lower() == "true"
