# Unit of Work 의존성

## 의존성 매트릭스

| Unit | 의존 대상 | 의존 유형 |
|------|----------|----------|
| Unit 1: Backend API | PostgreSQL | 런타임 (데이터베이스) |
| Unit 2: Customer Frontend | Unit 1: Backend API | 런타임 (API 호출) |
| Unit 3: Admin Frontend | Unit 1: Backend API | 런타임 (API 호출) |

---

## 의존성 다이어그램

```
+-------------------------+
|   Unit 1: Backend API   |
|   (FastAPI + PostgreSQL)|
+------------+------------+
             |
             | REST API + SSE
             |
     +-------+-------+
     |               |
     v               v
+----+----+    +----+----+
| Unit 2  |    | Unit 3  |
| Customer|    | Admin   |
| Frontend|    | Frontend|
+---------+    +---------+
```

---

## 개발 순서 및 근거

### 1단계: Unit 1 - Backend API
**근거**:
- Frontend가 의존하는 API를 먼저 완성
- 데이터 모델 및 비즈니스 로직 확정
- API 스펙이 명확해야 Frontend 개발 가능

**완료 기준**:
- 모든 API 엔드포인트 구현
- 데이터베이스 스키마 완성
- 단위 테스트 통과
- API 문서화 (Swagger/OpenAPI)

### 2단계: Unit 2 - Customer Frontend
**근거**:
- 고객 주문이 서비스의 핵심 기능
- Backend API 완성 후 실제 API 연동 가능
- Admin보다 사용자 수가 많음

**완료 기준**:
- 모든 고객용 페이지 구현
- Backend API 연동 완료
- SSE 실시간 업데이트 동작
- 반응형 UI 완성

### 3단계: Unit 3 - Admin Frontend
**근거**:
- 고객 주문 기능 완성 후 관리 기능 개발
- Backend API 완성 후 실제 API 연동 가능
- 실시간 모니터링 기능 테스트 가능

**완료 기준**:
- 모든 관리자용 페이지 구현
- Backend API 연동 완료
- SSE 실시간 주문 모니터링 동작
- 관리 기능 (CRUD) 동작

---

## 통합 포인트

### Backend API ↔ Customer Frontend
| API 엔드포인트 | Frontend 사용처 |
|---------------|----------------|
| `POST /api/v1/customer/auth/login` | SetupPage |
| `GET /api/v1/customer/categories` | MenuPage |
| `GET /api/v1/customer/menus` | MenuPage |
| `POST /api/v1/customer/orders` | OrderConfirmPage |
| `GET /api/v1/customer/orders` | OrderHistoryPage |
| `GET /api/v1/customer/orders/stream` | OrderHistoryPage (SSE) |

### Backend API ↔ Admin Frontend
| API 엔드포인트 | Frontend 사용처 |
|---------------|----------------|
| `POST /api/v1/admin/auth/login` | LoginPage |
| `GET /api/v1/admin/orders/stream` | DashboardPage (SSE) |
| `PATCH /api/v1/admin/orders/{id}/status` | DashboardPage |
| `DELETE /api/v1/admin/orders/{id}` | TableDetailPage |
| `POST /api/v1/admin/tables/{id}/complete` | TableDetailPage |
| `GET /api/v1/admin/tables/{id}/history` | TableHistoryPage |
| CRUD `/api/v1/admin/menus/*` | MenuManagementPage |
| CRUD `/api/v1/admin/categories/*` | CategoryManagementPage |
| CRUD `/api/v1/admin/tables/*` | TableManagementPage |

---

## 개발 환경 설정

### Unit 1 실행
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Unit 2 실행
```bash
cd customer-frontend
npm install
npm start  # localhost:3000
```

### Unit 3 실행
```bash
cd admin-frontend
npm install
npm start  # localhost:3001
```

### 환경 변수
```
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/tableorder
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256

# Frontend (공통)
REACT_APP_API_URL=http://localhost:8000/api/v1
```
