# Unit of Work 정의

## 개요

테이블오더 서비스는 3개의 작업 단위로 분해되어 순차적으로 개발됩니다.

| Unit | 이름 | 기술 스택 | 개발 순서 |
|------|------|----------|----------|
| Unit 1 | Backend API | FastAPI, PostgreSQL, SQLAlchemy | 1st |
| Unit 2 | Customer Frontend | React.js | 2nd |
| Unit 3 | Admin Frontend | React.js | 3rd |

---

## 프로젝트 디렉토리 구조 (모노레포)

```
table-order/
├── backend/                    # Unit 1: Backend API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI 앱 진입점
│   │   ├── config.py          # 설정
│   │   ├── database.py        # DB 연결
│   │   ├── models/            # SQLAlchemy 모델
│   │   │   ├── __init__.py
│   │   │   ├── store.py
│   │   │   ├── user.py
│   │   │   ├── table.py
│   │   │   ├── category.py
│   │   │   ├── menu.py
│   │   │   └── order.py
│   │   ├── schemas/           # Pydantic 스키마
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── table.py
│   │   │   ├── category.py
│   │   │   ├── menu.py
│   │   │   └── order.py
│   │   ├── routers/           # API 라우터
│   │   │   ├── __init__.py
│   │   │   ├── customer/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── menu.py
│   │   │   │   └── order.py
│   │   │   └── admin/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── order.py
│   │   │       ├── table.py
│   │   │       ├── menu.py
│   │   │       └── category.py
│   │   ├── services/          # 비즈니스 로직
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── table.py
│   │   │   ├── category.py
│   │   │   ├── menu.py
│   │   │   ├── order.py
│   │   │   └── sse.py
│   │   ├── repositories/      # 데이터 접근
│   │   │   ├── __init__.py
│   │   │   ├── store.py
│   │   │   ├── user.py
│   │   │   ├── table.py
│   │   │   ├── category.py
│   │   │   ├── menu.py
│   │   │   └── order.py
│   │   └── utils/             # 유틸리티
│   │       ├── __init__.py
│   │       ├── jwt.py
│   │       ├── password.py
│   │       └── errors.py
│   ├── tests/                 # 단위 테스트
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_menu.py
│   │   └── test_order.py
│   ├── requirements.txt
│   └── README.md
│
├── customer-frontend/          # Unit 2: Customer Frontend
│   ├── public/
│   ├── src/
│   │   ├── index.js
│   │   ├── App.js
│   │   ├── pages/
│   │   │   ├── SetupPage.js
│   │   │   ├── MenuPage.js
│   │   │   ├── CartPage.js
│   │   │   ├── OrderConfirmPage.js
│   │   │   ├── OrderSuccessPage.js
│   │   │   └── OrderHistoryPage.js
│   │   ├── components/
│   │   │   ├── CategoryTabs.js
│   │   │   ├── MenuCard.js
│   │   │   ├── MenuList.js
│   │   │   ├── CartItem.js
│   │   │   ├── CartSummary.js
│   │   │   └── OrderStatusBadge.js
│   │   ├── hooks/
│   │   │   ├── useLocalStorage.js
│   │   │   ├── useCart.js
│   │   │   ├── useAuth.js
│   │   │   └── useSSE.js
│   │   ├── api/
│   │   │   └── index.js
│   │   └── styles/
│   ├── package.json
│   └── README.md
│
├── admin-frontend/             # Unit 3: Admin Frontend
│   ├── public/
│   ├── src/
│   │   ├── index.js
│   │   ├── App.js
│   │   ├── pages/
│   │   │   ├── LoginPage.js
│   │   │   ├── DashboardPage.js
│   │   │   ├── TableDetailPage.js
│   │   │   ├── TableHistoryPage.js
│   │   │   ├── MenuManagementPage.js
│   │   │   ├── CategoryManagementPage.js
│   │   │   └── TableManagementPage.js
│   │   ├── components/
│   │   │   ├── TableCard.js
│   │   │   ├── TableGrid.js
│   │   │   ├── OrderCard.js
│   │   │   ├── OrderDetailModal.js
│   │   │   ├── StatusChangeButton.js
│   │   │   ├── ConfirmDialog.js
│   │   │   ├── MenuForm.js
│   │   │   ├── CategoryForm.js
│   │   │   └── DateFilter.js
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useSSE.js
│   │   │   └── useOrders.js
│   │   ├── api/
│   │   │   └── index.js
│   │   └── styles/
│   ├── package.json
│   └── README.md
│
└── README.md                   # 프로젝트 전체 설명
```

---

## Unit 1: Backend API

### 책임 범위
- REST API 제공 (고객용 + 관리자용)
- 데이터베이스 관리 (PostgreSQL)
- 인증/인가 (JWT)
- 실시간 이벤트 (SSE)
- 비즈니스 로직 처리

### 주요 기능
- 고객 API: 테이블 로그인, 메뉴 조회, 주문 생성/조회, SSE 구독
- 관리자 API: 로그인, 주문 모니터링/관리, 테이블 관리, 메뉴/카테고리 관리

### 기술 스택
- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Pydantic (데이터 검증)
- python-jose (JWT)
- bcrypt (비밀번호 해싱)
- pytest (테스트)

---

## Unit 2: Customer Frontend

### 책임 범위
- 고객용 웹 인터페이스
- 테이블 태블릿에서 실행
- 메뉴 탐색 및 주문 기능

### 주요 기능
- 초기 설정 (테이블 로그인)
- 메뉴 조회 및 탐색
- 장바구니 관리
- 주문 생성 및 확인
- 주문 내역 조회 (실시간 상태 업데이트)

### 기술 스택
- React.js 18+
- React Router
- Axios (HTTP 클라이언트)
- CSS (스타일링)

---

## Unit 3: Admin Frontend

### 책임 범위
- 관리자용 웹 인터페이스
- 매장 운영 관리 기능

### 주요 기능
- 관리자 로그인
- 실시간 주문 모니터링 (대시보드)
- 주문 상태 변경 및 삭제
- 테이블 세션 관리
- 메뉴/카테고리 관리

### 기술 스택
- React.js 18+
- React Router
- Axios (HTTP 클라이언트)
- CSS (스타일링)
