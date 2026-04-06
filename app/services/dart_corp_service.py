import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
from app.config import DART_XML_PATH, DART_INDEX_PATH

# 메모리 캐시
_corps: Optional[List[Dict[str, str]]] = None
_corps_by_code: Optional[Dict[str, Dict[str, str]]] = None


def _build_index() -> None:
    """XML을 파싱해서 JSON 인덱스를 생성한다. 최초 1회만 실행."""
    if DART_INDEX_PATH.exists():
        return
    if not DART_XML_PATH.exists():
        return

    tree = ET.parse(str(DART_XML_PATH))
    root = tree.getroot()

    corps = []
    for item in root.findall("list"):
        corp_code = (item.findtext("corp_code") or "").strip()
        corp_name = (item.findtext("corp_name") or "").strip()
        corp_eng_name = (item.findtext("corp_eng_name") or "").strip()
        stock_code = (item.findtext("stock_code") or "").strip()
        modify_date = (item.findtext("modify_date") or "").strip()
        if corp_code and corp_name:
            corps.append({
                "corp_code": corp_code,
                "corp_name": corp_name,
                "corp_eng_name": corp_eng_name,
                "stock_code": stock_code,
                "modify_date": modify_date,
            })

    DART_INDEX_PATH.write_text(
        json.dumps(corps, ensure_ascii=False),
        encoding="utf-8",
    )


def _load() -> List[Dict[str, str]]:
    global _corps, _corps_by_code
    if _corps is not None:
        return _corps

    _build_index()

    if not DART_INDEX_PATH.exists():
        _corps = []
        _corps_by_code = {}
        return _corps

    _corps = json.loads(DART_INDEX_PATH.read_text(encoding="utf-8"))
    _corps_by_code = {c["corp_code"]: c for c in _corps}
    return _corps


def get_total_count() -> int:
    return len(_load())


def get_listed_count() -> int:
    """상장사(stock_code가 있는) ��"""
    return sum(1 for c in _load() if c.get("stock_code"))


def search_corps(query: str, limit: int = 30) -> List[Dict[str, str]]:
    """기업명 또는 기업코드로 검색"""
    if not query or not query.strip():
        return []
    q = query.strip().lower()
    corps = _load()
    results = []
    for c in corps:
        if (q in c["corp_name"].lower()
                or q in c.get("corp_eng_name", "").lower()
                or q in c["corp_code"]):
            results.append(c)
            if len(results) >= limit:
                break
    return results


def get_corp_by_code(corp_code: str) -> Optional[Dict[str, str]]:
    _load()
    if _corps_by_code is None:
        return None
    return _corps_by_code.get(corp_code)
