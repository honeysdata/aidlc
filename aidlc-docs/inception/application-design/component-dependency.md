# 컴포넌트 의존성 설계

## 1. 시스템 아키텍처 다이어그램

```
+-------------------+          +-------------------+
|   Customer App    |          |    Admin App      |
|   (React SPA)     |          |   (React SPA)     |
+--------+----------+          +--------+----------+
         |                              |
         |  HTTP/SSE                    |  HTTP/SSE
         |                              |
         +-------------+----------------+
                       |
                       v
         +-------------+----------------+
         |        FastAPI Backend       |
         |   +----------------------+   |
         |   |    API Routers       |   |
         |   +----------+-----------+   |
         |              |               |
         |   +----------v-----------+   |
         |   |      Services        |   |
         |   +----------+-----------+   |
         |              |               |
         |   +----------v-----------+   |
         |   |    Repositories      |   |
         |   +----------+-----------+   |
         +-------------+----------------+
                       |
                       v
         +-------------+----------------+
         |        PostgreSQL            |
         +------------------------------+
```

---

## 2. Backend 의존성 매트릭스

### 2.1 Router → Service 의존성

| Router | 의존 Service |
|--------|-------------|
| `CustomerAuthRouter` | `AuthService` |
| `CustomerMenuRouter` | `MenuService`, `CategoryService` |
| `CustomerOrderRouter` | `OrderService`, `SSEService` |
| `AdminAuthRouter` | `AuthService` |
| `AdminOrderRouter` | `OrderService`, `SSEService` |
| `AdminTableRouter` | `TableService`, `OrderService` |
| `AdminMenuRouter` | `MenuService` |
| `AdminCategoryRouter` | `CategoryService` |

### 2.2 Service → Repository 의존성

| Service | 의존 Repository |
|---------|----------------|
| `AuthService` | `UserRepository`, `TableRepository`, `TableSessionRepository` |
| `TableService` | `TableRepository`, `TableSessionRepository` |
| `MenuService` | `MenuRepository`, `CategoryRepository` |
| `CategoryService` | `CategoryRepository`, `MenuRepository` |
| `OrderService` | `OrderRepository`, `OrderItemRepository`, `OrderHistoryRepository`, `MenuRepository`, `TableSessionRepository` |
| `SSEService` | (없음 - 독립적) |

### 2.3 Service → Service 의존성

| Service | 의존 Service |
|---------|-------------|
| `TableService` | `OrderService` (세션 종료 시 주문 아카이브) |
| `OrderService` | `SSEService` (주문 변경 시 브로드캐스트) |

---

## 3. Frontend 의존성

### 3.1 Customer App 컴포넌트 트리

```
App
├── SetupPage
│   └── SetupForm
├── MenuPage (기본 화면)
│   ├── CategoryTabs
│   ├── MenuList
│   │   └── MenuCard (multiple)
│   └── CartButton (floating)
├── CartPage
│   ├── CartItem (multiple)
│   ├── CartSummary
│   └── OrderButton
├── OrderConfirmPage
│   ├── OrderSummary
│   └── ConfirmButton
├── OrderSuccessPage
│   └── OrderNumber
└── OrderHistoryPage
    └── OrderItem (multiple)
        └── OrderStatusBadge
```

### 3.2 Admin App 컴포넌트 트리

```
App
├── LoginPage
│   └── LoginForm
├── DashboardPage
│   ├── TableGrid
│   │   └── TableCard (multiple)
│   │       └── NewOrderHighlight
│   └── OrderDetailModal
│       ├── OrderCard
│       └── StatusChangeButton
├── TableDetailPage
│   ├── OrderList
│   │   └── OrderCard (multiple)
│   └── ActionButtons (삭제, 이용완료)
├── TableHistoryPage
│   ├── DateFilter
│   └── HistoryList
├── MenuManagementPage
│   ├── MenuList
│   └── MenuForm
├── CategoryManagementPage
│   ├── CategoryList
│   └── CategoryForm
└── TableManagementPage
    ├── TableList
    └── TableForm
```

---

## 4. 데이터 흐름

### 4.1 고객 주문 플로우

```
Customer App                    Backend                         Database
     |                            |                                |
     |-- GET /menus ------------->|                                |
     |                            |-- MenuService.get_menus() ---->|
     |                            |<-- List[Menu] -----------------|
     |<-- MenuResponse -----------|                                |
     |                            |                                |
     |-- POST /orders ----------->|                                |
     |                            |-- OrderService.create_order()->|
     |                            |<-- Order ----------------------|
     |                            |-- SSEService.broadcast() ----->| (Admin)
     |<-- OrderResponse ----------|                                |
```

### 4.2 관리자 실시간 모니터링 플로우

```
Admin App                       Backend                         Database
     |                            |                                |
     |-- GET /orders/stream ----->|                                |
     |                            |-- SSEService.subscribe() ----->|
     |<-- SSE Connection ---------|                                |
     |                            |                                |
     |                            |<-- (New Order Event) ----------|
     |<-- SSE: new_order ---------|                                |
     |                            |                                |
     |-- PATCH /orders/{id} ----->|                                |
     |                            |-- OrderService.update_status()->|
     |                            |<-- Order ----------------------|
     |                            |-- SSEService.broadcast() ----->| (Customer)
     |<-- OrderResponse ----------|                                |
```

---

## 5. 통신 패턴

### 5.1 동기 통신 (HTTP REST)
- 모든 CRUD 작업
- 인증/인가
- 데이터 조회

### 5.2 비동기 통신 (SSE)
- 고객: 주문 상태 업데이트 수신
- 관리자: 신규 주문 및 상태 변경 수신

### 5.3 SSE 이벤트 타입

| 이벤트 | 대상 | 페이로드 |
|--------|------|----------|
| `new_order` | Admin | Order 전체 정보 |
| `order_updated` | Admin, Customer | Order ID, 새 상태 |
| `order_deleted` | Admin, Customer | Order ID |

---

## 6. 보안 의존성

### 6.1 인증 흐름

```
Request → JWTMiddleware → Router → Service → Repository
              |
              v
         Token 검증
         (JWTHandler)
```

### 6.2 인증 적용 범위

| 엔드포인트 | 인증 필요 | 토큰 타입 |
|-----------|----------|----------|
| `/api/v1/customer/auth/login` | No | - |
| `/api/v1/customer/*` | Yes | Table Token |
| `/api/v1/admin/auth/login` | No | - |
| `/api/v1/admin/*` | Yes | Admin Token |
