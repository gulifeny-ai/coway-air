from typing import Dict, List
from app.config import BASE_DIR

ENV_DESCRIPTIONS: Dict[str, str] = {
    "OPENAI_API_KEY": "OpenAI API 키",
    "OPENAI_MODEL": "OpenAI 모델명 (gpt-4.1 등)",
    "OPENAI_BASE_URL": "OpenAI API 엔드포인트",
    "DART_API_KEY": "DART 전자공시 API 키",
    "DART_API_URL": "DART API 엔드포인트",
    "NEWS_API_KEY": "News API 키 (newsapi.org)",
    "NEWS_API_URL": "News API 엔드포인트",
    "GOOGLE_API_KEY": "Google Custom Search API 키",
    "GOOGLE_CX": "Google Custom Search Engine ID",
    "CREDIT_API_KEY": "신용평가 API 키",
    "APP_TITLE": "애플리케이션 타이틀",
    "APP_HOST": "서버 호스트",
    "APP_PORT": "서버 포트",
    "DATA_DIR": "데이터 저장 경로",
    "DEBUG": "디버그 모드 (true/false)",
}


def load_env_items() -> List[Dict[str, str]]:
    env_path = BASE_DIR / ".env"
    example_path = BASE_DIR / ".env.example"
    source = env_path if env_path.exists() else example_path
    if not source.exists():
        return []
    items: List[Dict[str, str]] = []
    for line in source.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            items.append({
                "key": key,
                "value": value.strip(),
                "description": ENV_DESCRIPTIONS.get(key, ""),
            })
    return items


def save_env(items: Dict[str, str]) -> None:
    env_path = BASE_DIR / ".env"
    lines: List[str] = []
    for key, value in items.items():
        lines.append(f"{key}={value}")
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
