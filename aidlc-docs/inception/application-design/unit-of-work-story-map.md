# Unit of Work - Story Mapping

## 스토리 매핑 개요

| Unit | 스토리 수 | 스토리 ID |
|------|----------|----------|
| Unit 1: Backend API | 14 | 모든 스토리 (API 제공) |
| Unit 2: Customer Frontend | 5 | US-C01 ~ US-C05 |
| Unit 3: Admin Frontend | 9 | US-A01 ~ US-A09 |

---

## Unit 1: Backend API

모든 사용자 스토리의 백엔드 API를 제공합니다.

### 고객용 API (US-C01 ~ US-C05)

| Story ID | 스토리 | 관련 API |
|----------|--------|----------|
| US-C01 | 테이블 자동 로그인 | `POST /customer/auth/login` |
| US-C02 | 메뉴 조회 및 탐색 | `GET /customer/categories`, `GET /customer/menus` |
| US-C03 | 장바구니 관리 | (Frontend only - localStorage) |
| US-C04 | 주문 생성 | `POST /customer/orders` |
| US-C05 | 주문 내역 조회 | `GET /customer/orders`, `GET /customer/orders/stream` |

### 관리자용 API (US-A01 ~ US-A09)

| Story ID | 스토리 | 관련 API |
|----------|--------|----------|
| US-A01 | 관리자 로그인 | `POST /admin/auth/login` |
| US-A02 | 실시간 주문 모니터링 | `GET /admin/orders/stream`, `GET /admin/tables` |
| US-A03 | 주문 상태 변경 | `PATCH /admin/orders/{id}/status` |
| US-A04 | 주문 삭제 | `DELETE /admin/orders/{id}` |
| US-A05 | 테이블 이용 완료 | `POST /admin/tables/{id}/complete` |
| US-A06 | 과거 주문 내역 조회 | `GET /admin/tables/{id}/history` |
| US-A07 | 테이블 초기 설정 | `POST /admin/tables`, `PUT /admin/tables/{id}` |
| US-A08 | 메뉴 관리 | CRUD `/admin/menus/*` |
| US-A09 | 카테고리 관리 | CRUD `/admin/categories/*` |

---

## Unit 2: Customer Frontend

고객용 사용자 스토리의 UI를 구현합니다.

| Story ID | 스토리 | 구현 페이지/컴포넌트 |
|----------|--------|---------------------|
| US-C01 | 테이블 자동 로그인 | `SetupPage`, `useAuth`, `useLocalStorage` |
| US-C02 | 메뉴 조회 및 탐색 | `MenuPage`, `CategoryTabs`, `MenuList`, `MenuCard` |
| US-C03 | 장바구니 관리 | `CartPage`, `CartItem`, `CartSummary`, `useCart` |
| US-C04 | 주문 생성 | `OrderConfirmPage`, `OrderSuccessPage` |
| US-C05 | 주문 내역 조회 | `OrderHistoryPage`, `OrderStatusBadge`, `useSSE` |

---

## Unit 3: Admin Frontend

관리자용 사용자 스토리의 UI를 구현합니다.

| Story ID | 스토리 | 구현 페이지/컴포넌트 |
|----------|--------|---------------------|
| US-A01 | 관리자 로그인 | `LoginPage`, `useAuth` |
| US-A02 | 실시간 주문 모니터링 | `DashboardPage`, `TableGrid`, `TableCard`, `useSSE` |
| US-A03 | 주문 상태 변경 | `OrderDetailModal`, `StatusChangeButton` |
| US-A04 | 주문 삭제 | `TableDetailPage`, `ConfirmDialog` |
| US-A05 | 테이블 이용 완료 | `TableDetailPage`, `ConfirmDialog` |
| US-A06 | 과거 주문 내역 조회 | `TableHistoryPage`, `DateFilter` |
| US-A07 | 테이블 초기 설정 | `TableManagementPage` |
| US-A08 | 메뉴 관리 | `MenuManagementPage`, `MenuForm` |
| US-A09 | 카테고리 관리 | `CategoryManagementPage`, `CategoryForm` |

---

## 스토리 우선순위별 개발 순서

### Must (필수) - 13개

**Unit 1 (Backend) - 1단계**:
1. US-C01, US-A01: 인증 API
2. US-C02: 메뉴/카테고리 조회 API
3. US-C04, US-C05: 주문 생성/조회 API
4. US-A02, US-A03: 주문 모니터링/상태 변경 API
5. US-A04, US-A05: 주문 삭제/이용 완료 API
6. US-A07, US-A08, US-A09: 테이블/메뉴/카테고리 관리 API

**Unit 2 (Customer Frontend) - 2단계**:
1. US-C01: 테이블 로그인
2. US-C02: 메뉴 조회
3. US-C03: 장바구니
4. US-C04: 주문 생성
5. US-C05: 주문 내역

**Unit 3 (Admin Frontend) - 3단계**:
1. US-A01: 관리자 로그인
2. US-A02: 실시간 모니터링
3. US-A03, US-A04, US-A05: 주문 관리
4. US-A07, US-A08, US-A09: 설정 관리

### Should (권장) - 1개

**Unit 3 (Admin Frontend)**:
- US-A06: 과거 주문 내역 조회 (Must 완료 후)

---

## 검증 체크리스트

### Unit 1 완료 검증
- [ ] 모든 API 엔드포인트 동작 확인
- [ ] Swagger 문서 자동 생성 확인
- [ ] 단위 테스트 통과
- [ ] SSE 연결 테스트

### Unit 2 완료 검증
- [ ] 모든 고객 스토리 (US-C01~C05) 구현 확인
- [ ] Backend API 연동 확인
- [ ] 장바구니 localStorage 동작 확인
- [ ] SSE 실시간 업데이트 확인

### Unit 3 완료 검증
- [ ] 모든 관리자 스토리 (US-A01~A09) 구현 확인
- [ ] Backend API 연동 확인
- [ ] 실시간 주문 모니터링 확인
- [ ] CRUD 기능 동작 확인
