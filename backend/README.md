# Table Order Backend API

테이블 오더 서비스 백엔드 API

## 기술 스택

- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- pytest

## 설치 및 실행

### 1. 가상환경 설정

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 데이터베이스 연결 정보 설정
```

### 3. 데이터베이스 설정

PostgreSQL 데이터베이스를 생성하고 .env 파일에 연결 정보를 설정합니다.

```bash
# PostgreSQL에서 데이터베이스 생성
createdb table_order
```

### 4. 초기 데이터 생성

```bash
python -m scripts.seed
```

### 5. 서버 실행

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API 문서

서버 실행 후 아래 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 엔드포인트

### Customer API (`/api/v1/customer`)

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /auth/login | 테이블 로그인 |
| GET | /menu/categories | 카테고리 목록 |
| GET | /menu | 메뉴 목록 |
| GET | /menu/{id} | 메뉴 상세 |
| POST | /orders | 주문 생성 |
| GET | /orders | 주문 목록 |
| GET | /orders/stream | 주문 상태 SSE |

### Admin API (`/api/v1/admin`)

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /auth/login | 관리자 로그인 |
| GET | /orders/stream | 주문 실시간 SSE |
| PATCH | /orders/{id}/status | 주문 상태 변경 |
| DELETE | /orders/{id} | 주문 삭제 |
| GET | /tables | 테이블 목록 |
| GET | /tables/dashboard | 테이블 현황 |
| POST | /tables | 테이블 생성 |
| PATCH | /tables/{id} | 테이블 수정 |
| DELETE | /tables/{id} | 테이블 삭제 |
| POST | /tables/{id}/complete | 이용 완료 |
| GET | /tables/{id}/history | 과거 주문 내역 |
| GET | /menus | 메뉴 목록 |
| POST | /menus | 메뉴 생성 |
| PATCH | /menus/{id} | 메뉴 수정 |
| DELETE | /menus/{id} | 메뉴 삭제 |
| GET | /categories | 카테고리 목록 |
| POST | /categories | 카테고리 생성 |
| PATCH | /categories/{id} | 카테고리 수정 |
| DELETE | /categories/{id} | 카테고리 삭제 |

## 테스트

```bash
pytest -v
```

## 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI 앱 진입점
│   ├── config.py         # 환경 설정
│   ├── database.py       # DB 연결
│   ├── models/           # SQLAlchemy 모델
│   ├── schemas/          # Pydantic 스키마
│   ├── repositories/     # 데이터 접근 계층
│   ├── services/         # 비즈니스 로직
│   ├── routers/          # API 라우터
│   │   ├── customer/     # 고객 API
│   │   └── admin/        # 관리자 API
│   └── utils/            # 유틸리티
├── scripts/
│   └── seed.py           # 초기 데이터 스크립트
├── tests/                # 테스트
├── .env.example
├── requirements.txt
└── README.md
```
