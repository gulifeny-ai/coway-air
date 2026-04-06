from typing import Dict


async def get_credit_rating(corp_code: str) -> Dict[str, str]:
    """신용평가 조회 (현재 mock)"""
    return {
        "corp_code": corp_code,
        "rating": "AA-",
        "agency": "한국신용평가",
        "date": "2024-06-15",
    }
