import re
from typing import List


def extract_title(markdown: str) -> str:
    match = re.search(r"^#\s+(.+)", markdown, re.MULTILINE)
    return match.group(1).strip() if match else "제목 없음"


def markdown_to_html_simple(markdown: str) -> str:
    """최소한의 markdown → HTML 변환 (향후 라이브러리 교체 가능)"""
    lines = markdown.split("\n")
    html_lines: List[str] = []
    for line in lines:
        if line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("- "):
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.strip() == "":
            html_lines.append("<br>")
        else:
            html_lines.append(f"<p>{line}</p>")
    return "\n".join(html_lines)
