from typing import Dict, List

from app.utils.env_utils import load_env_items, save_env


def get_settings() -> List[Dict[str, str]]:
    return load_env_items()


def update_settings(items: Dict[str, str]) -> None:
    save_env(items)
