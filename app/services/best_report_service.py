from typing import List, Optional
from pathlib import Path
from app.config import BEST_REPORTS_DIR
from app.utils.file_store import list_markdown_files, read_markdown, save_markdown, delete_file


def get_best_reports() -> List[dict]:
    return list_markdown_files(BEST_REPORTS_DIR)


def get_best_report_content(filename: str) -> Optional[str]:
    return read_markdown(BEST_REPORTS_DIR, filename)


def upload_best_report(filename: str, content: str) -> Path:
    return save_markdown(BEST_REPORTS_DIR, filename, content)


def remove_best_report(filename: str) -> bool:
    return delete_file(BEST_REPORTS_DIR, filename)
