# 테이블오더 서비스 컴포넌트 설계

## 아키텍처 개요

```
+------------------+     +------------------+
|  Customer App    |     |   Admin App      |
|  (React SPA)     |     |  (React SPA)     |
+--------+---------+     +--------+---------+
         |                        |
         +------------+-----------+
                      |
                      v
         +------------+-----------+
         |     FastAPI Backend    |
         |  (Layered Architecture)|
         +------------+-----------+
                      |
                      v
         +------------+-----------+
         |     PostgreSQL DB      |
         +------------------------+
```

---

## 1. Backend Components

### 1.1 API Layer (Controllers/Routers)

| Component | 책임 | 엔드포인트 |
|-----------|------|-----------|
| `CustomerAuthRouter` | 고객 테이블 인증 | `/api/v1/customer/auth/*` |
| `CustomerMenuRouter` | 고객 메뉴 조회 | `/api/v1/customer/menus/*` |
| `CustomerOrderRouter` | 고객 주문 관리 | `/api/v1/customer/orders/*` |
| `AdminAuthRouter` | 관리자 인증 | `/api/v1/admin/auth/*` |
| `AdminOrderRouter` | 관리자 주문 관리 | `/api/v1/admin/orders/*` |
| `AdminTableRouter` | 테이블 관리 | `/api/v1/admin/tables/*` |
| `AdminMenuRouter` | 메뉴 관리 | `/api/v1/admin/menus/*` |
| `AdminCategoryRouter` | 카테고리 관리 | `/api/v1/admin/categories/*` |

### 1.2 Service Layer

| Component | 책임 |
|-----------|------|
| `AuthService` | 인증/인가 로직 (JWT 발급, 검증) |
| `StoreService` | 매장 정보 관리 |
| `TableService` | 테이블 및 세션 관리 |
| `MenuService` | 메뉴 CRUD 로직 |
| `CategoryService` | 카테고리 CRUD 로직 |
| `OrderService` | 주문 생성, 상태 변경, 삭제 |
| `SSEService` | Server-Sent Events 관리 |

### 1.3 Repository Layer

| Component | 책임 |
|-----------|------|
| `StoreRepository` | Store 테이블 CRUD |
| `UserRepository` | User 테이블 CRUD |
| `TableRepository` | Table 테이블 CRUD |
| `TableSessionRepository` | TableSession 테이블 CRUD |
| `CategoryRepository` | Category 테이블 CRUD |
| `MenuRepository` | Menu 테이블 CRUD |
| `OrderRepository` | Order 테이블 CRUD |
| `OrderItemRepository` | OrderItem 테이블 CRUD |
| `OrderHistoryRepository` | OrderHistory 테이블 CRUD |

### 1.4 Domain Models (Entities)

| Entity | 설명 |
|--------|------|
| `Store` | 매장 정보 |
| `User` | 관리자 계정 |
| `Table` | 테이블 정보 |
| `TableSession` | 테이블 세션 (고객 이용 단위) |
| `Category` | 메뉴 카테고리 |
| `Menu` | 메뉴 항목 |
| `Order` | 주문 |
| `OrderItem` | 주문 항목 |
| `OrderHistory` | 과거 주문 이력 |

### 1.5 Cross-Cutting Components

| Component | 책임 |
|-----------|------|
| `JWTHandler` | JWT 토큰 생성/검증 |
| `PasswordHasher` | 비밀번호 해싱 (bcrypt) |
| `ErrorHandler` | 표준화된 에러 응답 처리 |
| `DatabaseSession` | DB 세션 관리 |

---

## 2. Frontend Components (Customer App)

### 2.1 Pages

| Component | 책임 |
|-----------|------|
| `SetupPage` | 초기 설정 (매장ID, 테이블번호, 비밀번호) |
| `MenuPage` | 메뉴 조회 및 탐색 (기본 화면) |
| `CartPage` | 장바구니 관리 |
| `OrderConfirmPage` | 주문 확인 |
| `OrderSuccessPage` | 주문 성공 (5초 후 리다이렉트) |
| `OrderHistoryPage` | 주문 내역 조회 |

### 2.2 UI Components

| Component | 책임 |
|-----------|------|
| `CategoryTabs` | 카테고리 탭 네비게이션 |
| `MenuCard` | 메뉴 카드 (이름, 가격, 설명) |
| `MenuList` | 메뉴 목록 그리드 |
| `CartItem` | 장바구니 항목 |
| `CartSummary` | 장바구니 요약 (총액) |
| `OrderItem` | 주문 내역 항목 |
| `OrderStatusBadge` | 주문 상태 배지 |
| `LoadingSpinner` | 로딩 인디케이터 |
| `ErrorMessage` | 에러 메시지 표시 |

### 2.3 Hooks & Utilities

| Component | 책임 |
|-----------|------|
| `useLocalStorage` | 로컬 스토리지 관리 |
| `useCart` | 장바구니 상태 관리 |
| `useAuth` | 인증 상태 관리 |
| `useSSE` | SSE 연결 관리 |
| `api` | API 호출 유틸리티 (Axios) |

---

## 3. Frontend Components (Admin App)

### 3.1 Pages

| Component | 책임 |
|-----------|------|
| `LoginPage` | 관리자 로그인 |
| `DashboardPage` | 실시간 주문 모니터링 대시보드 |
| `TableDetailPage` | 테이블 상세 (주문 목록) |
| `TableHistoryPage` | 테이블 과거 주문 내역 |
| `MenuManagementPage` | 메뉴 관리 |
| `CategoryManagementPage` | 카테고리 관리 |
| `TableManagementPage` | 테이블 설정 관리 |

### 3.2 UI Components

| Component | 책임 |
|-----------|------|
| `TableCard` | 테이블 카드 (총액, 최신 주문) |
| `TableGrid` | 테이블 그리드 레이아웃 |
| `OrderCard` | 주문 카드 |
| `OrderDetailModal` | 주문 상세 모달 |
| `StatusChangeButton` | 상태 변경 버튼 |
| `ConfirmDialog` | 확인 팝업 |
| `MenuForm` | 메뉴 등록/수정 폼 |
| `CategoryForm` | 카테고리 등록/수정 폼 |
| `DateFilter` | 날짜 필터 |
| `NewOrderHighlight` | 신규 주문 강조 애니메이션 |

### 3.3 Hooks & Utilities

| Component | 책임 |
|-----------|------|
| `useAuth` | 인증 상태 관리 (JWT) |
| `useSSE` | SSE 연결 관리 (실시간 주문) |
| `useOrders` | 주문 상태 관리 |
| `api` | API 호출 유틸리티 (Axios) |
