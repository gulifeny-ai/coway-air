import httpx
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from app.config import settings

NEWS_API_URL = settings.get("NEWS_API_URL", "https://newsapi.org/v2") or "https://newsapi.org/v2"


def _get_api_key() -> Optional[str]:
    key = settings.get("NEWS_API_KEY", "")
    if key and key != "your-news-api-key-here":
        return key
    return None


async def search_news_direct(query: str, days: int = 20, page_size: int = 20) -> Dict:
    """News API로 검색어 직접 전달 (직전 N일, 인기도순)"""
    api_key = _get_api_key()
    if not api_key:
        return {"error": "NEWS_API_KEY가 설정되지 않았습니다.", "articles": []}
    return await _call_news_api(query, api_key, days, page_size)


async def search_news(keywords: List[str], days: int = 7, page_size: int = 20) -> Dict:
    """News API로 키워드 리스트 기반 뉴스 검색"""
    api_key = _get_api_key()
    if not api_key:
        return {"error": "NEWS_API_KEY가 설정되지 않았습니다.", "articles": []}

    query = " ".join(keywords)
    return await _call_news_api(query, api_key, days, page_size)


async def _call_news_api(query: str, api_key: str, days: int, page_size: int) -> Dict:
    today = datetime.now()
    from_date = (today - timedelta(days=days)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    url = f"{NEWS_API_URL}/everything" if NEWS_API_URL else "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "sortBy": "popularity",
        "apiKey": api_key,
        "pageSize": page_size,
    }

    print(f"[NewsAPI] URL={url}")
    print(f"[NewsAPI] params: q='{query}', from={from_date}, to={to_date}, pageSize={page_size}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            data = resp.json()

        print(f"[NewsAPI] status={data.get('status')}, totalResults={data.get('totalResults', 0)}, articles={len(data.get('articles', []))}")

        if data.get("status") != "ok":
            print(f"[NewsAPI] ERROR: {data.get('message')}")
            return {"error": data.get("message", "API 오류"), "articles": []}

        return {
            "total": data.get("totalResults", 0),
            "from_date": from_date,
            "to_date": to_date,
            "query": query,
            "articles": data.get("articles", []),
        }
    except Exception as e:
        return {"error": str(e), "articles": []}
