# Logical Components - Backend API

## 1. 시스템 컴포넌트 다이어그램

```
+------------------------------------------------------------------+
|                        FastAPI Application                        |
+------------------------------------------------------------------+
|                                                                    |
|  +------------------+  +------------------+  +------------------+  |
|  |   API Routers    |  |   Middleware     |  |   SSE Manager    |  |
|  |  - Customer      |  |  - CORS          |  |  - Connections   |  |
|  |  - Admin         |  |  - Logging       |  |  - Broadcast     |  |
|  +--------+---------+  |  - Auth          |  +--------+---------+  |
|           |            +------------------+           |            |
|           v                                           |            |
|  +------------------+                                 |            |
|  |    Services      |<--------------------------------+            |
|  |  - AuthService   |                                              |
|  |  - OrderService  |                                              |
|  |  - MenuService   |                                              |
|  |  - TableService  |                                              |
|  +--------+---------+                                              |
|           |                                                        |
|           v                                                        |
|  +------------------+                                              |
|  |  Repositories    |                                              |
|  |  - OrderRepo     |                                              |
|  |  - MenuRepo      |                                              |
|  |  - TableRepo     |                                              |
|  +--------+---------+                                              |
|           |                                                        |
+-----------|--------------------------------------------------------+
            |
            v
+------------------+
|   PostgreSQL     |
|  - Connection    |
|    Pool (10-20)  |
+------------------+
```

---

## 2. 핵심 컴포넌트

### 2.1 FastAPI Application

| 컴포넌트 | 책임 | 설정 |
|----------|------|------|
| `main.py` | 앱 초기화, 라우터 등록 | - |
| `config.py` | 환경 변수 관리 | Pydantic Settings |
| `database.py` | DB 연결 관리 | AsyncSession |

### 2.2 Middleware Stack

```python
# 미들웨어 적용 순서 (위에서 아래로)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def logging_middleware(request, call_next):
    # 요청/응답 로깅
    ...

@app.middleware("http")
async def error_handling_middleware(request, call_next):
    # 전역 에러 처리
    ...
```

---

## 3. API 라우터 구조

### 3.1 Customer API (`/api/v1/customer`)

| 라우터 | 엔드포인트 | 인증 |
|--------|-----------|------|
| `auth.py` | `POST /auth/login` | 없음 |
| `menu.py` | `GET /categories` | Table Token |
| `menu.py` | `GET /menus` | Table Token |
| `order.py` | `POST /orders` | Table Token |
| `order.py` | `GET /orders` | Table Token |
| `order.py` | `GET /orders/stream` | Table Token |

### 3.2 Admin API (`/api/v1/admin`)

| 라우터 | 엔드포인트 | 인증 |
|--------|-----------|------|
| `auth.py` | `POST /auth/login` | 없음 |
| `order.py` | `GET /orders/stream` | Admin Token |
| `order.py` | `PATCH /orders/{id}/status` | Admin Token |
| `order.py` | `DELETE /orders/{id}` | Admin Token |
| `table.py` | `GET /tables` | Admin Token |
| `table.py` | `POST /tables` | Admin Token |
| `table.py` | `POST /tables/{id}/complete` | Admin Token |
| `table.py` | `GET /tables/{id}/history` | Admin Token |
| `menu.py` | CRUD `/menus/*` | Admin Token |
| `category.py` | CRUD `/categories/*` | Admin Token |

---

## 4. 서비스 컴포넌트

### 4.1 AuthService

```python
class AuthService:
    """인증 서비스"""
    
    def __init__(self):
        self.jwt_handler = JWTHandler()
        self.password_hasher = PasswordHasher()
    
    # 테이블 로그인
    async def login_table(self, db, store_id, table_number, password) -> dict
    
    # 관리자 로그인
    async def login_admin(self, db, store_id, username, password) -> dict
    
    # 토큰 검증
    def verify_token(self, token, token_type) -> dict
```

### 4.2 OrderService

```python
class OrderService:
    """주문 서비스"""
    
    def __init__(self):
        self.order_repo = OrderRepository()
        self.sse_manager = sse_manager
    
    # 주문 생성
    async def create_order(self, db, session_id, items) -> Order
    
    # 주문 상태 변경
    async def update_status(self, db, order_id, status) -> Order
    
    # 주문 삭제
    async def delete_order(self, db, order_id) -> bool
    
    # 주문 아카이브
    async def archive_orders(self, db, session_id) -> bool
```

### 4.3 TableService

```python
class TableService:
    """테이블 서비스"""
    
    def __init__(self):
        self.table_repo = TableRepository()
        self.session_repo = TableSessionRepository()
        self.order_service = OrderService()
    
    # 세션 시작
    async def start_session(self, db, table_id) -> TableSession
    
    # 세션 종료 (이용 완료)
    async def end_session(self, db, table_id) -> bool
```

### 4.4 SSEService

```python
class SSEManager:
    """SSE 연결 관리"""
    
    def __init__(self):
        self.connections: Dict[str, List[Queue]] = {}
    
    # 구독
    async def subscribe(self, channel) -> AsyncGenerator
    
    # 브로드캐스트
    async def broadcast(self, channel, event_type, data) -> None
    
    # 연결 해제
    async def disconnect(self, channel, queue) -> None
```

---

## 5. Repository 컴포넌트

### 5.1 Base Repository

```python
class BaseRepository(Generic[T]):
    """기본 Repository"""
    
    model: Type[T]
    
    async def get(self, db, id) -> T | None
    async def get_all(self, db) -> List[T]
    async def create(self, db, obj) -> T
    async def update(self, db, obj) -> T
    async def delete(self, db, obj) -> bool
```

### 5.2 Specialized Repositories

| Repository | 추가 메서드 |
|------------|------------|
| `OrderRepository` | `get_by_session()`, `get_active_by_store()` |
| `TableSessionRepository` | `get_active_session()`, `end_session()` |
| `OrderHistoryRepository` | `get_by_table_and_date()` |
| `MenuRepository` | `get_by_category()`, `reorder()` |
| `CategoryRepository` | `get_by_store()`, `reorder()` |

---

## 6. 유틸리티 컴포넌트

### 6.1 JWTHandler

```python
class JWTHandler:
    """JWT 토큰 처리"""
    
    def create_token(self, payload, token_type, expires_hours) -> str
    def verify_token(self, token) -> dict
    def decode_token(self, token) -> dict
```

### 6.2 PasswordHasher

```python
class PasswordHasher:
    """비밀번호 해싱"""
    
    def hash(self, password) -> str
    def verify(self, password, hashed) -> bool
```

### 6.3 ErrorHandler

```python
class AppException(Exception):
    """애플리케이션 예외"""
    
    code: str
    message: str
    status_code: int
    details: dict | None
```

---

## 7. 데이터베이스 컴포넌트

### 7.1 Connection Pool

| 설정 | 값 | 설명 |
|------|-----|------|
| `pool_size` | 10 | 기본 연결 수 |
| `max_overflow` | 10 | 추가 연결 수 |
| `pool_timeout` | 30 | 연결 대기 (초) |
| `pool_recycle` | 3600 | 연결 재활용 (초) |

### 7.2 Session Management

```python
# 비동기 세션 팩토리
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 의존성 주입
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

---

## 8. 로깅 컴포넌트

### 8.1 Logger Configuration

| 설정 | 값 |
|------|-----|
| 레벨 | DEBUG |
| 출력 | 파일 (`logs/app.log`) |
| 로테이션 | 일별 |
| 보관 | 7일 |

### 8.2 Log Categories

| 카테고리 | 레벨 | 내용 |
|----------|------|------|
| `app.api` | INFO | API 요청/응답 |
| `app.auth` | INFO | 인증 시도 |
| `app.db` | DEBUG | DB 쿼리 |
| `app.sse` | DEBUG | SSE 연결/이벤트 |
| `app.error` | ERROR | 예외/에러 |

---

## 9. 헬스체크 컴포넌트

### 9.1 Health Endpoint

```python
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"}
        )
```
