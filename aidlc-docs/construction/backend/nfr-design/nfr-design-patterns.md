# NFR Design Patterns - Backend API

## 1. 아키텍처 패턴

### 1.1 Layered Architecture

```
+------------------+
|   API Routers    |  ← 요청 검증, 응답 포맷팅
+------------------+
         |
         v
+------------------+
|    Services      |  ← 비즈니스 로직, 트랜잭션
+------------------+
         |
         v
+------------------+
|  Repositories    |  ← 데이터 접근 추상화
+------------------+
         |
         v
+------------------+
|   SQLAlchemy     |  ← ORM, 쿼리 빌더
+------------------+
         |
         v
+------------------+
|   PostgreSQL     |  ← 데이터 저장
+------------------+
```

**적용 이유**: 관심사 분리, 테스트 용이성, 유지보수성

---

## 2. 인증 패턴

### 2.1 JWT Bearer Token Pattern

```
[클라이언트]                    [서버]
     |                            |
     |-- POST /login ------------>|
     |                            |-- 자격 증명 검증
     |                            |-- JWT 토큰 생성
     |<-- JWT Token --------------|
     |                            |
     |-- GET /api (Bearer Token)->|
     |                            |-- 토큰 검증
     |                            |-- 요청 처리
     |<-- Response ---------------|
```

**구현**:
```python
# Dependency Injection 패턴
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = verify_token(token)
    user = await user_repo.get(db, payload.user_id)
    if not user:
        raise HTTPException(status_code=401)
    return user
```

### 2.2 Role-Based Access Control (RBAC)

| 역할 | 접근 가능 API |
|------|--------------|
| Table (고객) | `/api/v1/customer/*` |
| Admin (관리자) | `/api/v1/admin/*` |

**구현**:
```python
# 테이블 전용 의존성
async def get_current_table(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token, token_type="table")
    return payload

# 관리자 전용 의존성
async def get_current_admin(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token, token_type="admin")
    return payload
```

---

## 3. 에러 처리 패턴

### 3.1 Global Exception Handler

```python
# 커스텀 예외 클래스
class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

# 전역 예외 핸들러
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.code,
            "message": exc.message
        }
    )
```

### 3.2 표준 에러 응답

```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "입력값이 올바르지 않습니다.",
  "details": {
    "field": "price",
    "reason": "가격은 0 이상이어야 합니다."
  }
}
```

---

## 4. 데이터베이스 패턴

### 4.1 Repository Pattern

```python
# 기본 Repository
class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    
    async def get(self, db: AsyncSession, id: int) -> T | None:
        return await db.get(self.model, id)
    
    async def get_all(self, db: AsyncSession) -> List[T]:
        result = await db.execute(select(self.model))
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, obj: T) -> T:
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    
    async def update(self, db: AsyncSession, obj: T) -> T:
        await db.commit()
        await db.refresh(obj)
        return obj
    
    async def delete(self, db: AsyncSession, obj: T) -> bool:
        await db.delete(obj)
        await db.commit()
        return True
```

### 4.2 Unit of Work Pattern (트랜잭션)

```python
# 트랜잭션 관리
async def create_order_with_items(
    db: AsyncSession,
    order_data: OrderCreate
) -> Order:
    async with db.begin():  # 트랜잭션 시작
        order = Order(**order_data.dict())
        db.add(order)
        
        for item in order_data.items:
            order_item = OrderItem(order=order, **item.dict())
            db.add(order_item)
        
        # 트랜잭션 커밋 (자동)
    return order
```

### 4.3 Connection Pool Pattern

```python
# 연결 풀 설정
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,        # 기본 연결
    max_overflow=10,     # 추가 연결
    pool_timeout=30,     # 대기 타임아웃
    pool_recycle=3600    # 연결 재활용
)
```

---

## 5. 실시간 통신 패턴

### 5.1 Server-Sent Events (SSE) Pattern

```python
# SSE 매니저
class SSEManager:
    def __init__(self):
        self.connections: Dict[str, List[Queue]] = {}
    
    async def subscribe(self, channel: str) -> AsyncGenerator:
        queue = asyncio.Queue()
        if channel not in self.connections:
            self.connections[channel] = []
        self.connections[channel].append(queue)
        
        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        finally:
            self.connections[channel].remove(queue)
    
    async def broadcast(self, channel: str, data: dict):
        if channel in self.connections:
            for queue in self.connections[channel]:
                await queue.put(data)

sse_manager = SSEManager()
```

### 5.2 채널 구조

| 채널 | 구독자 | 이벤트 |
|------|--------|--------|
| `admin:{store_id}` | 관리자 | new_order, order_updated, order_deleted |
| `customer:{session_id}` | 고객 | order_updated |

---

## 6. 로깅 패턴

### 6.1 Structured Logging

```python
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    
    # 파일 핸들러
    handler = TimedRotatingFileHandler(
        "logs/app.log",
        when="midnight",
        backupCount=7
    )
    
    # 포맷
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

### 6.2 Request Logging Middleware

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"- {response.status_code} - {duration:.3f}s"
    )
    
    return response
```

---

## 7. 검증 패턴

### 7.1 Pydantic Validation

```python
from pydantic import BaseModel, Field, validator

class MenuCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: int = Field(..., ge=0)
    category_id: int
    description: str | None = None
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('메뉴명은 비어있을 수 없습니다')
        return v.strip()
```

### 7.2 Business Rule Validation

```python
# 서비스 레이어에서 비즈니스 규칙 검증
class OrderService:
    async def update_status(
        self, db: AsyncSession, order_id: int, new_status: OrderStatus
    ) -> Order:
        order = await self.order_repo.get(db, order_id)
        if not order:
            raise AppException("NOT_FOUND", "주문을 찾을 수 없습니다", 404)
        
        # 상태 전이 규칙 검증
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.PREPARING],
            OrderStatus.PREPARING: [OrderStatus.COMPLETED],
            OrderStatus.COMPLETED: []
        }
        
        if new_status not in valid_transitions[order.status]:
            raise AppException(
                "INVALID_STATUS_TRANSITION",
                f"{order.status}에서 {new_status}로 변경할 수 없습니다"
            )
        
        order.status = new_status
        return await self.order_repo.update(db, order)
```

---

## 8. 의존성 주입 패턴

### 8.1 FastAPI Dependency Injection

```python
# 데이터베이스 세션 의존성
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# 서비스 의존성
def get_order_service() -> OrderService:
    return OrderService(OrderRepository())

# 라우터에서 사용
@router.post("/orders")
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    service: OrderService = Depends(get_order_service),
    current_table: TablePayload = Depends(get_current_table)
):
    return await service.create_order(db, order_data, current_table)
```
