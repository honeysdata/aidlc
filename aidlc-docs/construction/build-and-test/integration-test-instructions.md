# Integration Test Instructions - 테이블 오더 서비스

## 개요

전체 시스템의 통합 테스트 가이드입니다. API 엔드포인트와 프론트엔드 연동을 검증합니다.

---

## 1. 사전 준비

### 1.1 전체 시스템 실행
```bash
# 터미널 1: Backend
cd backend && source venv/bin/activate
uvicorn app.main:app --reload

# 터미널 2: Customer Frontend
cd customer-frontend && npm run dev

# 터미널 3: Admin Frontend
cd admin-frontend && npm run dev
```

### 1.2 초기 데이터 확인
```bash
cd backend && python -m scripts.seed
```

---

## 2. API 통합 테스트 (curl)

### 2.1 Health Check
```bash
curl http://localhost:8000/health
# 예상: {"status":"healthy"}
```

### 2.2 관리자 로그인
```bash
curl -X POST http://localhost:8000/api/v1/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{"store_id":"demo-store","username":"admin","password":"admin1234"}'
# 예상: {"token":"...","store_id":"demo-store","username":"admin","expires_at":"..."}
```

### 2.3 테이블 로그인
```bash
curl -X POST http://localhost:8000/api/v1/customer/auth/login \
  -H "Content-Type: application/json" \
  -d '{"store_id":"demo-store","table_number":1,"password":"1234"}'
# 예상: {"token":"...","store_id":"demo-store","table_number":1,"session_id":...}
```

### 2.4 메뉴 조회 (인증 필요)
```bash
# TOKEN을 테이블 로그인에서 받은 토큰으로 대체
curl http://localhost:8000/api/v1/customer/menu \
  -H "Authorization: Bearer TOKEN"
# 예상: {"menus":[...]}
```

### 2.5 주문 생성
```bash
curl -X POST http://localhost:8000/api/v1/customer/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"items":[{"menu_id":1,"quantity":2}]}'
# 예상: {"id":...,"order_number":"YYYYMMDD-001",...}
```

---

## 3. E2E 테스트 시나리오

### 시나리오 1: 고객 주문 플로우

1. **Customer Frontend 접속** (http://localhost:3000)
2. **초기 설정**
   - 매장 ID: `demo-store`
   - 테이블 번호: `1`
   - 비밀번호: `1234`
3. **메뉴 조회**
   - 카테고리 탭 전환 확인
   - 메뉴 목록 표시 확인
4. **장바구니 추가**
   - 메뉴 + 버튼 클릭
   - 하단 네비게이션 장바구니 뱃지 확인
5. **장바구니 확인**
   - 수량 증가/감소 확인
   - 총 금액 계산 확인
6. **주문 생성**
   - 주문하기 → 주문 확인 → 주문 확정
   - 주문 성공 화면 확인
   - 5초 후 메뉴 화면 리다이렉트 확인
7. **주문 내역 확인**
   - 주문내역 탭에서 주문 표시 확인
   - 주문 상태 "대기중" 확인

### 시나리오 2: 관리자 주문 처리 플로우

1. **Admin Frontend 접속** (http://localhost:3001)
2. **관리자 로그인**
   - 매장 ID: `demo-store`
   - 사용자명: `admin`
   - 비밀번호: `admin1234`
3. **대시보드 확인**
   - 테이블 카드 표시 확인
   - 주문 있는 테이블 "이용중" 상태 확인
4. **주문 상태 변경**
   - 테이블 카드 클릭 → 주문 상세 모달
   - "준비 시작" 클릭 → 상태 "준비중" 변경 확인
   - "완료" 클릭 → 상태 "완료" 변경 확인
5. **실시간 업데이트 확인**
   - Customer Frontend에서 주문 상태 실시간 변경 확인
6. **이용 완료 처리**
   - 테이블 카드 "이용 완료" 버튼 클릭
   - 확인 팝업 → 확인
   - 테이블 상태 "비어있음" 변경 확인

### 시나리오 3: 메뉴/카테고리 관리

1. **카테고리 관리**
   - 카테고리 추가: "디저트"
   - 카테고리 수정: 이름 변경
   - 카테고리 삭제 (메뉴 없는 경우)
2. **메뉴 관리**
   - 메뉴 추가: 이름, 가격, 카테고리 입력
   - 메뉴 수정: 가격 변경, 품절 설정
   - 메뉴 삭제
3. **Customer Frontend 반영 확인**
   - 새 메뉴/카테고리 표시 확인
   - 품절 메뉴 미표시 확인

### 시나리오 4: 테이블 관리

1. **테이블 추가**
   - 테이블 번호: 6
   - 비밀번호: 1234
2. **테이블 비밀번호 변경**
   - 테이블 선택 → 비밀번호 변경
3. **과거 내역 조회**
   - 테이블 선택 → 과거 내역
   - 날짜 필터 적용
4. **테이블 삭제**
   - 활성 세션 없는 테이블 삭제

---

## 4. SSE 실시간 테스트

### 4.1 테스트 방법
1. Admin Frontend 대시보드 열기
2. Customer Frontend에서 새 주문 생성
3. Admin Frontend에서 2초 이내 새 주문 표시 확인

### 4.2 확인 사항
- 새 주문 알림 (new_order 이벤트)
- 주문 상태 변경 알림 (order_updated 이벤트)
- 주문 삭제 알림 (order_deleted 이벤트)

---

## 5. 에러 케이스 테스트

### 5.1 인증 에러
- 잘못된 비밀번호로 로그인 시도
- 만료된 토큰으로 API 호출
- 토큰 없이 보호된 API 호출

### 5.2 비즈니스 규칙 에러
- 품절 메뉴 주문 시도
- 잘못된 주문 상태 전이 (COMPLETED → PENDING)
- 메뉴 있는 카테고리 삭제 시도
- 활성 세션 있는 테이블 삭제 시도

---

## 6. 체크리스트

| 테스트 항목 | 상태 |
|------------|------|
| Backend Health Check | ☐ |
| 관리자 로그인 | ☐ |
| 테이블 로그인 | ☐ |
| 메뉴 조회 | ☐ |
| 주문 생성 | ☐ |
| 주문 상태 변경 | ☐ |
| SSE 실시간 업데이트 | ☐ |
| 이용 완료 처리 | ☐ |
| 메뉴 CRUD | ☐ |
| 카테고리 CRUD | ☐ |
| 테이블 CRUD | ☐ |
| 과거 내역 조회 | ☐ |
