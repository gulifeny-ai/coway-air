from app.config import DART_DIR, RESEARCH_DIR, REPORTS_DIR, BEST_REPORTS_DIR, UPLOADS_DIR, EMBEDDINGS_DIR, CACHE_DIR


def ensure_directories() -> None:
    for d in [DART_DIR, RESEARCH_DIR, REPORTS_DIR, BEST_REPORTS_DIR, UPLOADS_DIR, EMBEDDINGS_DIR, CACHE_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def build_dart_index() -> None:
    from app.services.dart_corp_service import _build_index, get_total_count
    _build_index()
    count = get_total_count()
    if count:
        print(f"[Coway-AIR] DART 기업 인덱스 로드 완료: {count:,}개 기업")
