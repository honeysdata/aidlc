# Unit Test Instructions - 테이블 오더 서비스

## 개요

Backend API의 단위 테스트 실행 가이드입니다.

---

## 1. 테스트 환경 설정

### 1.1 가상환경 활성화
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 1.2 테스트 의존성 확인
`requirements.txt`에 포함된 테스트 패키지:
- pytest
- pytest-asyncio
- httpx (API 테스트용)

---

## 2. 테스트 실행

### 2.1 전체 테스트 실행
```bash
cd backend
pytest -v
```

### 2.2 특정 테스트 파일 실행
```bash
# 모델 테스트
pytest tests/test_models.py -v

# 유틸리티 테스트
pytest tests/test_utils.py -v

# 리포지토리 테스트
pytest tests/test_repositories.py -v

# 서비스 테스트
pytest tests/test_services/ -v
```

### 2.3 특정 테스트 함수 실행
```bash
pytest tests/test_services/test_auth_service.py::test_login_table_success -v
```

### 2.4 커버리지 리포트
```bash
pytest --cov=app --cov-report=html
# htmlcov/index.html 에서 결과 확인
```

---

## 3. 테스트 구조

```
backend/tests/
├── __init__.py
├── conftest.py              # pytest 설정 및 fixtures
├── test_models.py           # 도메인 모델 테스트
├── test_utils.py            # 유틸리티 테스트 (JWT, Password)
├── test_repositories.py     # 리포지토리 레이어 테스트
└── test_services/
    ├── __init__.py
    ├── test_auth_service.py     # 인증 서비스 테스트
    ├── test_menu_service.py     # 메뉴 서비스 테스트
    ├── test_category_service.py # 카테고리 서비스 테스트
    ├── test_order_service.py    # 주문 서비스 테스트
    └── test_table_service.py    # 테이블 서비스 테스트
```

---

## 4. 테스트 케이스 목록

### 4.1 모델 테스트 (test_models.py)
- Store 모델 생성
- User 모델 생성
- Table 모델 생성
- Category 모델 생성
- Menu 모델 생성
- Order/OrderItem 모델 생성
- TableSession 모델 생성

### 4.2 유틸리티 테스트 (test_utils.py)
- JWT 토큰 생성 (테이블용)
- JWT 토큰 생성 (관리자용)
- JWT 토큰 검증
- 비밀번호 해싱
- 비밀번호 검증

### 4.3 리포지토리 테스트 (test_repositories.py)
- CRUD 기본 동작
- 매장별 조회
- 카테고리별 메뉴 조회
- 세션별 주문 조회

### 4.4 서비스 테스트 (test_services/)

**AuthService:**
- 테이블 로그인 성공
- 테이블 로그인 실패 (잘못된 비밀번호)
- 테이블 로그인 실패 (매장 없음)
- 관리자 로그인 성공
- 관리자 로그인 실패

**MenuService:**
- 매장별 메뉴 조회
- 메뉴 생성
- 메뉴 수정
- 메뉴 삭제
- 잘못된 카테고리로 메뉴 생성 실패

**CategoryService:**
- 카테고리 목록 조회
- 카테고리 생성
- 중복 카테고리명 생성 실패
- 카테고리 삭제
- 메뉴 있는 카테고리 삭제 실패

**OrderService:**
- 주문 생성 성공
- 주문 생성 실패 (잘못된 세션)
- 주문 생성 실패 (메뉴 없음)
- 주문 상태 변경 (유효한 전이)
- 주문 상태 변경 실패 (잘못된 전이)
- 주문 삭제

**TableService:**
- 테이블 목록 조회
- 테이블 생성
- 중복 테이블 번호 생성 실패
- 테이블 비밀번호 변경
- 테이블 삭제
- 활성 세션 있는 테이블 삭제 실패
- 이용 완료 처리
- 대시보드 데이터 조회

---

## 5. 테스트 데이터베이스

테스트는 SQLite 인메모리 데이터베이스를 사용합니다 (`conftest.py` 설정).

```python
# conftest.py
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
```

각 테스트는 독립적인 데이터베이스 세션을 사용하여 격리됩니다.

---

## 6. 예상 결과

모든 테스트 통과 시:
```
========================= test session starts ==========================
collected XX items

tests/test_models.py::test_create_store PASSED
tests/test_models.py::test_create_user PASSED
...
tests/test_services/test_auth_service.py::test_login_table_success PASSED
...

========================= XX passed in X.XXs ===========================
```
