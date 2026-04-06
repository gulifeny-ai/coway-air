from typing import Dict, List

MOCK_SEARCH_RESULTS: List[Dict[str, str]] = [
    {"title": "코웨이 2024년 실적 분석 - 렌탈 사업 호조", "url": "https://example.com/1", "snippet": "코웨이의 2024년 매출은 전년 대비 8.3% 성장하며 역대 최대 실적을 기록..."},
    {"title": "환경가전 시장 동향 보고서 2025", "url": "https://example.com/2", "snippet": "국내 환경가전 시장 규모는 약 4조원으로, 정수기·공기청정기 중심 성장세 지속..."},
    {"title": "코웨이 ESG 경영 현황 및 전망", "url": "https://example.com/3", "snippet": "코웨이는 ESG 경영을 통해 지속가능한 성장 기반을 마련하고 있으며..."},
    {"title": "코웨이 동남아 시장 진출 확대 전략", "url": "https://example.com/4", "snippet": "말레이시아, 태국 중심 해외 매출 비중이 전체의 20%를 돌파하며..."},
    {"title": "정수기 렌탈 시장 경쟁 심화 분석", "url": "https://example.com/5", "snippet": "SK매직, 청호나이스 등 후발주자의 공격적 마케팅으로 경쟁 구도 변화..."},
]


async def search_web(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """Google Custom Search (현재 mock)"""
    return MOCK_SEARCH_RESULTS[:num_results]
