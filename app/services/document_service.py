from typing import List, Optional

from app.config import REPORTS_DIR
from app.utils.file_store import list_markdown_files, read_markdown


def get_recent_reports(limit: int = 10) -> List[dict]:
    return list_markdown_files(REPORTS_DIR)[:limit]


def get_report_content(filename: str) -> Optional[str]:
    return read_markdown(REPORTS_DIR, filename)
