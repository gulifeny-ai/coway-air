# Coway-AIR (Coway AI Research)

AI 기반 자동 조사 보고서 시스템.
키워드만 입력하면 기업 정보 수집, 시장 분석, 보고서 초안 생성까지 자동으로 수행하는 것을 목표로 합니다.

## 현재 범위 (1차 MVP Scaffold)

- FastAPI + Jinja2 + HTMX 기반 프로젝트 뼈대
- 5개 화면 구성 (대시보드, 기업검색, 보고서생성, 우수보고서, 관리자설정)
- Mock 데이터 기반 동작
- 로컬 파일 기반 저장 (DB 미사용)
- 외부 API 연동 인터페이스 준비 (DART, Google, LLM, 신용평가, 그냥평가)

## 설치

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 실행

```bash
uvicorn app.main:app --reload
```

http://localhost:8000 접속

## 디렉터리 구조

```
app/
├── main.py              # FastAPI 앱 진입점
├── config.py            # 설정 관리
├── dependencies.py      # 공통 의존성 (templates 등)
├── routes/              # 라우트 핸들러
├── services/            # 비즈니스 로직
├── clients/             # 외부 API 클라이언트 (mock)
├── models/              # Pydantic 스키마
├── utils/               # 유틸리티
├── templates/           # Jinja2 템플릿
└── static/              # CSS, JS
data/
├── reports/             # 생성된 보고서
├── best_reports/        # 우수 보고서
├── uploads/             # 업로드 파일
├── embeddings/          # 임베딩 캐시 (향후)
└── cache/               # 일반 캐시
```

## .env 설정

`.env.example`을 `.env`로 복사 후 값을 채워 넣으세요.

| 키 | 설명 |
|----|------|
| LLM_API_KEY | LLM API 키 |
| LLM_MODEL | 사용할 모델명 (기본: gpt-4o) |
| DART_API_KEY | DART 전자공시 API 키 |
| GOOGLE_API_KEY | Google Custom Search API 키 |
| GOOGLE_CX | Google CSE ID |
| CREDIT_API_KEY | 신용평가 API 키 |

## 이후 확장 포인트

- **2차**: DART API 실연동, LLM 실연동, 보고서 품질 개선
- **3차**: 우수 보고서 임베딩 + RAG 기반 참조, 자동 조사 파이프라인
- **4차**: 사용자 인증, 보고서 버전 관리, PDF 내보내기
