from pathlib import Path
from typing import Dict, List, Optional, Union


def list_markdown_files(directory: Path) -> List[Dict[str, Union[str, float]]]:
    if not directory.exists():
        return []
    files = sorted(directory.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    return [
        {
            "filename": f.name,
            "title": f.stem.replace("_", " ").title(),
            "size_kb": round(f.stat().st_size / 1024, 1),
        }
        for f in files
    ]


def read_markdown(directory: Path, filename: str) -> Optional[str]:
    path = directory / filename
    if not path.exists() or not path.suffix == ".md":
        return None
    return path.read_text(encoding="utf-8")


def save_markdown(directory: Path, filename: str, content: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    path.write_text(content, encoding="utf-8")
    return path


def delete_file(directory: Path, filename: str) -> bool:
    path = directory / filename
    if path.exists():
        path.unlink()
        return True
    return False
