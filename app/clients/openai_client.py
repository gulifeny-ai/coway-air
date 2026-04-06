import httpx
import json
from typing import Optional
from app.config import settings


def _get_config():
    api_key = settings.get("OPENAI_API_KEY", "")
    if not api_key or api_key == "your-openai-api-key-here":
        return None, None, None
    model = settings.get("OPENAI_MODEL", "gpt-4.1") or "gpt-4.1"
    base_url = settings.get("OPENAI_BASE_URL", "https://api.openai.com/v1") or "https://api.openai.com/v1"
    return api_key, model, base_url


async def chat_completion(system_prompt: str, user_prompt: str) -> dict:
    """OpenAI Chat Completion API 호출"""
    api_key, model, base_url = _get_config()
    if not api_key:
        return {"error": "OPENAI_API_KEY가 설정되지 않았습니다.", "content": ""}

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
    }

    print(f"[OpenAI] URL: {url}")
    print(f"[OpenAI] Model: {model}")
    print(f"[OpenAI] System prompt: {system_prompt[:100]}...")
    print(f"[OpenAI] User prompt: {user_prompt[:200]}...")
    print(f"[OpenAI] Request body size: {len(json.dumps(body, ensure_ascii=False))} chars")

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, headers=headers, json=body)
            data = resp.json()

        if "error" in data:
            print(f"[OpenAI] ERROR: {data['error']}")
            return {"error": data["error"].get("message", str(data["error"])), "content": ""}

        choice = data.get("choices", [{}])[0]
        content = choice.get("message", {}).get("content", "")
        usage = data.get("usage", {})

        print(f"[OpenAI] Response: {len(content)} chars")
        print(f"[OpenAI] Usage: prompt_tokens={usage.get('prompt_tokens')}, completion_tokens={usage.get('completion_tokens')}, total={usage.get('total_tokens')}")

        return {"content": content, "usage": usage}

    except Exception as e:
        print(f"[OpenAI] Exception: {e}")
        return {"error": str(e), "content": ""}
