import httpx
from datetime import datetime
from typing import Dict, List, Optional
from app.config import settings
from app.models.schemas import CompanyDetail

DART_API_URL = settings.get("DART_API_URL", "https://opendart.fss.or.kr/api") or "https://opendart.fss.or.kr/api"

REPRT_CODES = {
    "11011": "사업보고서",
    "11014": "3분기보고서",
    "11012": "반기보고서",
    "11013": "1분기보고서",
}


def _get_api_key() -> Optional[str]:
    key = settings.get("DART_API_KEY", "")
    if key and key != "your-dart-api-key-here":
        return key
    return None


async def get_company_detail_by_code(corp_code: str) -> Optional[CompanyDetail]:
    """DART API로 기업 상세 조회 (corp_code 기반)"""
    api_key = _get_api_key()
    if not api_key:
        return None

    url = f"{DART_API_URL}/company.json"
    params = {"crtfc_key": api_key, "corp_code": corp_code}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            data = resp.json()

        if data.get("status") != "000":
            return None

        return CompanyDetail(
            corp_code=data.get("corp_code", ""),
            corp_name=data.get("corp_name", ""),
            corp_name_eng=data.get("corp_name_eng", ""),
            stock_name=data.get("stock_name", ""),
            stock_code=data.get("stock_code", ""),
            ceo_nm=data.get("ceo_nm", ""),
            corp_cls=data.get("corp_cls", ""),
            jurir_no=data.get("jurir_no", ""),
            bizr_no=data.get("bizr_no", ""),
            adres=data.get("adres", ""),
            hm_url=data.get("hm_url", ""),
            ir_url=data.get("ir_url", ""),
            phn_no=data.get("phn_no", ""),
            fax_no=data.get("fax_no", ""),
            induty_code=data.get("induty_code", ""),
            est_dt=data.get("est_dt", ""),
            acc_mt=data.get("acc_mt", ""),
            source="DART OpenAPI",
        )
    except Exception:
        return None


async def get_financial_statements(corp_code: str) -> Dict[str, List[Dict]]:
    """전체 재무제표 조회 — 올해/작년 × 4개 보고서(사업/반기/1분기/3분기), OFS만"""
    api_key = _get_api_key()
    if not api_key:
        return {}

    now = datetime.now()
    years = [str(now.year), str(now.year - 1)]
    url = f"{DART_API_URL}/fnlttSinglAcntAll.json"

    all_data: Dict[str, List[Dict]] = {}

    async with httpx.AsyncClient(timeout=15.0) as client:
        for year in years:
            for reprt_code, reprt_name in REPRT_CODES.items():
                params = {
                    "crtfc_key": api_key,
                    "corp_code": corp_code,
                    "bsns_year": year,
                    "reprt_code": reprt_code,
                    "fs_div": "OFS",
                }
                try:
                    resp = await client.get(url, params=params)
                    data = resp.json()
                    if data.get("status") == "000" and data.get("list"):
                        key = f"{year} {reprt_name}"
                        all_data[key] = data["list"]
                except Exception:
                    continue

    return all_data
