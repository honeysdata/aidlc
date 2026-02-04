# 컴포넌트 메서드 설계

## 1. Backend Service Layer Methods

### 1.1 AuthService

```python
class AuthService:
    def login_table(store_id: str, table_number: int, password: str) -> TableLoginResponse
    # 테이블 로그인, JWT 토큰 반환
    
    def login_admin(store_id: str, username: str, password: str) -> AdminLoginResponse
    # 관리자 로그인, JWT 토큰 반환 (16시간 유효)
    
    def verify_token(token: str) -> TokenPayload
    # JWT 토큰 검증
    
    def hash_password(password: str) -> str
    # 비밀번호 bcrypt 해싱
    
    def verify_password(plain: str, hashed: str) -> bool
    # 비밀번호 검증
```

### 1.2 StoreService

```python
class StoreService:
    def get_store(store_id: str) -> Store
    # 매장 정보 조회
    
    def validate_store(store_id: str) -> bool
    # 매장 존재 여부 확인
```

### 1.3 TableService

```python
class TableService:
    def get_table(store_id: str, table_number: int) -> Table
    # 테이블 정보 조회
    
    def get_tables(store_id: str) -> List[Table]
    # 매장의 모든 테이블 조회
    
    def create_table(store_id: str, table_number: int, password: str) -> Table
    # 테이블 생성 및 초기 설정
    
    def update_table(store_id: str, table_number: int, data: TableUpdate) -> Table
    # 테이블 정보 수정
    
    def delete_table(store_id: str, table_number: int) -> bool
    # 테이블 삭제
    
    def start_session(store_id: str, table_number: int) -> TableSession
    # 테이블 세션 시작 (첫 주문 시)
    
    def end_session(store_id: str, table_number: int) -> bool
    # 테이블 세션 종료 (이용 완료)
    
    def get_current_session(store_id: str, table_number: int) -> TableSession | None
    # 현재 활성 세션 조회
```

### 1.4 CategoryService

```python
class CategoryService:
    def get_categories(store_id: str) -> List[Category]
    # 매장의 카테고리 목록 조회 (순서대로)
    
    def create_category(store_id: str, name: str, display_order: int) -> Category
    # 카테고리 생성
    
    def update_category(category_id: int, data: CategoryUpdate) -> Category
    # 카테고리 수정
    
    def delete_category(category_id: int) -> bool
    # 카테고리 삭제 (메뉴 있으면 실패)
    
    def reorder_categories(store_id: str, order: List[int]) -> bool
    # 카테고리 순서 변경
```

### 1.5 MenuService

```python
class MenuService:
    def get_menus(store_id: str, category_id: int | None) -> List[Menu]
    # 메뉴 목록 조회 (카테고리별 필터 가능)
    
    def get_menu(menu_id: int) -> Menu
    # 메뉴 상세 조회
    
    def create_menu(store_id: str, data: MenuCreate) -> Menu
    # 메뉴 생성
    
    def update_menu(menu_id: int, data: MenuUpdate) -> Menu
    # 메뉴 수정
    
    def delete_menu(menu_id: int) -> bool
    # 메뉴 삭제
    
    def reorder_menus(category_id: int, order: List[int]) -> bool
    # 메뉴 순서 변경
```

### 1.6 OrderService

```python
class OrderService:
    def create_order(store_id: str, table_number: int, session_id: int, items: List[OrderItemCreate]) -> Order
    # 주문 생성
    
    def get_order(order_id: int) -> Order
    # 주문 상세 조회
    
    def get_orders_by_session(session_id: int) -> List[Order]
    # 세션별 주문 목록 조회
    
    def get_orders_by_table(store_id: str, table_number: int) -> List[Order]
    # 테이블별 현재 주문 목록 조회
    
    def get_all_active_orders(store_id: str) -> List[Order]
    # 매장의 모든 활성 주문 조회
    
    def update_order_status(order_id: int, status: OrderStatus) -> Order
    # 주문 상태 변경 (대기중/준비중/완료)
    
    def delete_order(order_id: int) -> bool
    # 주문 삭제
    
    def get_order_history(store_id: str, table_number: int, date_from: date, date_to: date) -> List[OrderHistory]
    # 과거 주문 내역 조회
    
    def archive_orders(session_id: int) -> bool
    # 세션 종료 시 주문을 히스토리로 이동
    
    def calculate_table_total(store_id: str, table_number: int) -> int
    # 테이블 총 주문액 계산
```

### 1.7 SSEService

```python
class SSEService:
    def subscribe_customer(store_id: str, table_number: int, session_id: int) -> AsyncGenerator
    # 고객용 SSE 구독 (주문 상태 업데이트)
    
    def subscribe_admin(store_id: str) -> AsyncGenerator
    # 관리자용 SSE 구독 (실시간 주문)
    
    def broadcast_order_update(store_id: str, order: Order) -> None
    # 주문 업데이트 브로드캐스트
    
    def broadcast_new_order(store_id: str, order: Order) -> None
    # 신규 주문 브로드캐스트
```

---

## 2. Backend Repository Layer Methods

### 2.1 Common Pattern

```python
class BaseRepository[T]:
    def get(id: int) -> T | None
    def get_all() -> List[T]
    def create(data: dict) -> T
    def update(id: int, data: dict) -> T
    def delete(id: int) -> bool
```

### 2.2 Specialized Methods

```python
class OrderRepository(BaseRepository[Order]):
    def get_by_session(session_id: int) -> List[Order]
    def get_by_table(store_id: str, table_number: int) -> List[Order]
    def get_active_by_store(store_id: str) -> List[Order]

class TableSessionRepository(BaseRepository[TableSession]):
    def get_active_session(store_id: str, table_number: int) -> TableSession | None
    def end_session(session_id: int, completed_at: datetime) -> bool

class OrderHistoryRepository(BaseRepository[OrderHistory]):
    def get_by_table_and_date(store_id: str, table_number: int, date_from: date, date_to: date) -> List[OrderHistory]
```

---

## 3. API Response Types

### 3.1 Success Response

```python
class SuccessResponse[T]:
    status: str = "success"
    data: T
```

### 3.2 Error Response

```python
class ErrorResponse:
    status: str = "error"
    code: str  # e.g., "AUTH_FAILED", "NOT_FOUND"
    message: str
    details: dict | None
```

### 3.3 Domain DTOs

```python
class TableLoginResponse:
    token: str
    store_id: str
    table_number: int
    session_id: int

class AdminLoginResponse:
    token: str
    store_id: str
    username: str
    expires_at: datetime

class OrderResponse:
    order_id: int
    order_number: str
    table_number: int
    items: List[OrderItemResponse]
    total_amount: int
    status: OrderStatus
    created_at: datetime

class OrderItemResponse:
    menu_name: str
    quantity: int
    unit_price: int
    subtotal: int
```
