from typing import Dict
from datetime import datetime
from app.clients.llm_client import generate_text
from app.utils.file_store import save_markdown
from app.config import REPORTS_DIR


async def generate_report(company_name: str, keywords: str = "") -> Dict[str, str]:
    prompt = f"{company_name} {keywords}".strip()
    markdown = await generate_text(prompt)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{company_name}_{timestamp}.md"
    save_markdown(REPORTS_DIR, filename, markdown)
    return {"title": f"{company_name} 조사 보고서", "markdown": markdown, "filename": filename}
