from typing import List, Optional
from pydantic import BaseModel


class CompanySearchRequest(BaseModel):
    query: str


class CompanyInfo(BaseModel):
    name: str
    corp_code: str
    industry: str
    ceo: str
    address: str


class CompanyDetail(BaseModel):
    corp_code: str
    corp_name: str
    corp_name_eng: str = ""
    stock_name: str = ""
    stock_code: str = ""
    ceo_nm: str = ""
    corp_cls: str = ""  # Y:유가증권, K:코스닥, N:코넥스, E:기타
    jurir_no: str = ""
    bizr_no: str = ""
    adres: str = ""
    hm_url: str = ""
    ir_url: str = ""
    phn_no: str = ""
    fax_no: str = ""
    induty_code: str = ""
    est_dt: str = ""
    acc_mt: str = ""
    source: str = "DART"


class WebSearchResult(BaseModel):
    title: str
    url: str
    snippet: str


class Research(BaseModel):
    id: str
    title: str
    topic: str
    company_name: str
    keywords: List[str]
    status: str  # draft, collecting, analyzing, completed
    creator: str
    created_at: str
    updated_at: str
    company_data: Optional[CompanyDetail] = None
    web_results: Optional[List[WebSearchResult]] = None
    notes: str = ""


class ResearchStats(BaseModel):
    total: int
    in_progress: int
    completed: int
    companies_count: int
    this_week: int


class ReportGenerateRequest(BaseModel):
    company_name: str
    keywords: str = ""


class ReportResult(BaseModel):
    title: str
    company_name: str
    markdown: str


class BestReportMeta(BaseModel):
    filename: str
    title: str
    size_kb: float


class SettingsItem(BaseModel):
    key: str
    value: str
    description: str
