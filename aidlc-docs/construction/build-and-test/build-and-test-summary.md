# Build and Test Summary - 테이블 오더 서비스

## 프로젝트 개요

테이블 오더 서비스는 식당에서 고객이 테이블에서 직접 주문하고, 관리자가 실시간으로 주문을 모니터링할 수 있는 시스템입니다.

---

## 시스템 구성

| 컴포넌트 | 기술 스택 | 포트 | 위치 |
|----------|-----------|------|------|
| Backend API | FastAPI, SQLAlchemy, PostgreSQL | 8000 | `backend/` |
| Customer Frontend | React, Vite | 3000 | `customer-frontend/` |
| Admin Frontend | React, Vite | 3001 | `admin-frontend/` |

---

## 빌드 요약

### Backend
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # DB 설정 편집
python -m scripts.seed
uvicorn app.main:app --reload
```

### Frontend (Customer & Admin)
```bash
cd customer-frontend  # 또는 admin-frontend
npm install
cp .env.example .env
npm run dev
```

---

## 테스트 요약

### 단위 테스트
```bash
cd backend
pytest -v
```

테스트 범위:
- 모델 테스트
- 유틸리티 테스트 (JWT, Password)
- 리포지토리 테스트
- 서비스 테스트 (Auth, Menu, Category, Order, Table)

### 통합 테스트
- API 엔드포인트 테스트 (curl)
- E2E 시나리오 테스트 (브라우저)
- SSE 실시간 테스트

---

## 테스트 계정

| 용도 | 매장 ID | 사용자/테이블 | 비밀번호 |
|------|---------|---------------|----------|
| 관리자 | demo-store | admin | admin1234 |
| 고객 | demo-store | 1~5 | 1234 |

---

## 주요 기능 검증 항목

### 고객 기능 (Customer Frontend)
- [x] 테이블 로그인 (자동 로그인)
- [x] 메뉴 조회 (카테고리별)
- [x] 장바구니 관리
- [x] 주문 생성
- [x] 주문 내역 조회
- [x] 실시간 주문 상태 업데이트 (SSE)

### 관리자 기능 (Admin Frontend)
- [x] 관리자 로그인 (16시간 세션)
- [x] 실시간 주문 모니터링 (SSE)
- [x] 주문 상태 변경
- [x] 주문 삭제
- [x] 테이블 이용 완료 처리
- [x] 과거 주문 내역 조회
- [x] 테이블 관리 (CRUD)
- [x] 메뉴 관리 (CRUD)
- [x] 카테고리 관리 (CRUD)

---

## 문서 목록

| 문서 | 설명 |
|------|------|
| `build-instructions.md` | 빌드 및 실행 가이드 |
| `unit-test-instructions.md` | 단위 테스트 가이드 |
| `integration-test-instructions.md` | 통합 테스트 가이드 |

---

## 다음 단계

1. 프로덕션 배포 준비
   - 환경 변수 보안 설정
   - HTTPS 설정
   - 프로덕션 빌드

2. 추가 개선 사항 (선택)
   - 메뉴 이미지 업로드
   - 푸시 알림
   - 매출 리포트
