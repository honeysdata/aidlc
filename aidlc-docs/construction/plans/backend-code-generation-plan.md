# Code Generation Plan - Unit 1: Backend API (TDD)

## Overview
Backend API 코드 생성 계획 (Test-Driven Development 방식)

## Unit Context
- **Unit Name**: Backend API
- **Tech Stack**: FastAPI, SQLAlchemy, PostgreSQL, pytest
- **Stories**: US-C01~C05 (고객), US-A01~A09 (관리자) API 제공
- **Location**: `backend/` (모노레포 구조)

## Code Generation Steps

### Phase 1: Project Setup
- [x] Step 1: 프로젝트 디렉토리 구조 생성
- [x] Step 2: requirements.txt 생성
- [x] Step 3: 환경 설정 파일 생성 (config.py, .env.example)
- [x] Step 4: 데이터베이스 연결 설정 (database.py)
- [x] Step 5: pytest 설정 (conftest.py)

### Phase 2: Domain Models (TDD)
- [x] Step 6: 모델 테스트 작성 (test_models.py)
- [x] Step 7: SQLAlchemy 모델 구현 (models/)
- [x] Step 8: Pydantic 스키마 구현 (schemas/)

### Phase 3: Utilities (TDD)
- [x] Step 9: JWT 유틸리티 테스트 작성
- [x] Step 10: JWT 유틸리티 구현 (utils/jwt.py)
- [x] Step 11: 비밀번호 유틸리티 테스트 작성
- [x] Step 12: 비밀번호 유틸리티 구현 (utils/password.py)
- [x] Step 13: 에러 핸들링 구현 (utils/errors.py)

### Phase 4: Repository Layer (TDD)
- [x] Step 14: Repository 테스트 작성 (test_repositories.py)
- [x] Step 15: Base Repository 구현
- [x] Step 16: 도메인별 Repository 구현

### Phase 5: Service Layer (TDD)
- [x] Step 17: AuthService 테스트 작성
- [x] Step 18: AuthService 구현
- [x] Step 19: MenuService 테스트 작성
- [x] Step 20: MenuService 구현
- [x] Step 21: CategoryService 테스트 작성
- [x] Step 22: CategoryService 구현
- [x] Step 23: OrderService 테스트 작성
- [x] Step 24: OrderService 구현
- [x] Step 25: TableService 테스트 작성
- [x] Step 26: TableService 구현
- [x] Step 27: SSE Manager 구현

### Phase 6: API Layer (TDD)
- [x] Step 28: Customer Auth API 테스트 및 구현
- [x] Step 29: Customer Menu API 테스트 및 구현
- [x] Step 30: Customer Order API 테스트 및 구현
- [x] Step 31: Admin Auth API 테스트 및 구현
- [x] Step 32: Admin Order API 테스트 및 구현
- [x] Step 33: Admin Table API 테스트 및 구현
- [x] Step 34: Admin Menu API 테스트 및 구현
- [x] Step 35: Admin Category API 테스트 및 구현

### Phase 7: Application Entry Point
- [x] Step 36: FastAPI 앱 설정 (main.py)
- [x] Step 37: 초기 데이터 시드 스크립트

### Phase 8: Documentation
- [x] Step 38: README.md 작성
- [x] Step 39: 코드 생성 요약 문서

## Story Traceability

| Story | 구현 Step |
|-------|----------|
| US-C01 (테이블 로그인) | Step 17-18, 28 |
| US-C02 (메뉴 조회) | Step 19-22, 29 |
| US-C03 (장바구니) | Frontend only |
| US-C04 (주문 생성) | Step 23-24, 30 |
| US-C05 (주문 내역) | Step 23-24, 30 |
| US-A01 (관리자 로그인) | Step 17-18, 31 |
| US-A02 (실시간 모니터링) | Step 27, 32 |
| US-A03 (주문 상태 변경) | Step 23-24, 32 |
| US-A04 (주문 삭제) | Step 23-24, 32 |
| US-A05 (이용 완료) | Step 25-26, 33 |
| US-A06 (과거 내역) | Step 25-26, 33 |
| US-A07 (테이블 설정) | Step 25-26, 33 |
| US-A08 (메뉴 관리) | Step 19-20, 34 |
| US-A09 (카테고리 관리) | Step 21-22, 35 |

## File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   ├── repositories/
│   └── utils/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_repositories.py
│   ├── test_services/
│   └── test_routers/
├── .env.example
├── requirements.txt
└── README.md
```
