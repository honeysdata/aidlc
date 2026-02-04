# Business Rules - Backend API

## 1. 인증 규칙

### BR-AUTH-01: 테이블 로그인
- 매장 ID, 테이블 번호, 비밀번호 모두 필수
- 비밀번호는 bcrypt로 해싱하여 검증
- 로그인 성공 시 JWT 토큰 발급

### BR-AUTH-02: 관리자 로그인
- 매장 ID, 사용자명, 비밀번호 모두 필수
- 비밀번호는 bcrypt로 해싱하여 검증
- JWT 토큰 유효 기간: 16시간
- 토큰 만료 시 재로그인 필요

### BR-AUTH-03: 토큰 검증
- 모든 인증 필요 API는 JWT 토큰 검증 필수
- 토큰 만료 시 401 Unauthorized 응답
- 잘못된 토큰 시 401 Unauthorized 응답

---

## 2. 테이블 세션 규칙

### BR-SESSION-01: 세션 시작
- 테이블 로그인 시 자동으로 세션 시작
- 이미 활성 세션이 있으면 기존 세션 사용
- 세션 시작 시 `started_at` 기록

### BR-SESSION-02: 세션 종료
- 관리자만 세션 종료(이용 완료) 가능
- 세션 종료 시 모든 주문을 OrderHistory로 이동
- 세션 종료 시 `completed_at` 기록, `is_active = false`

### BR-SESSION-03: 세션 격리
- 고객은 현재 활성 세션의 주문만 조회 가능
- 이전 세션의 주문은 조회 불가

---

## 3. 주문 규칙

### BR-ORDER-01: 주문 생성
- 활성 세션이 있어야 주문 생성 가능
- 최소 1개 이상의 주문 항목 필수
- 각 항목의 수량은 1 이상

### BR-ORDER-02: 주문 번호
- 형식: `YYYYMMDD-NNN` (예: 20260204-001)
- 매장별, 일별 순차 번호
- 동일 매장 내 동일 날짜에 중복 불가

### BR-ORDER-03: 주문 상태 전이
- 허용된 전이:
  - `PENDING` → `PREPARING`
  - `PREPARING` → `COMPLETED`
- 금지된 전이:
  - `PREPARING` → `PENDING` (역방향)
  - `COMPLETED` → `PREPARING` (역방향)
  - `COMPLETED` → `PENDING` (역방향)

### BR-ORDER-04: 주문 삭제
- 관리자만 주문 삭제 가능
- 삭제 시 확인 필요 (프론트엔드에서 처리)
- 삭제된 주문은 복구 불가

### BR-ORDER-05: 주문 금액 계산
- 총 금액 = Σ(단가 × 수량)
- 주문 시점의 메뉴 가격으로 계산 (스냅샷)

---

## 4. 주문 항목 규칙

### BR-ITEM-01: 스냅샷 저장
- 주문 생성 시 메뉴명, 단가를 스냅샷으로 저장
- 메뉴 삭제/가격 변경 시에도 주문 내역 유지

### BR-ITEM-02: 수량 제한
- 최소 수량: 1
- 최대 수량: 제한 없음 (정수 범위 내)

### BR-ITEM-03: 소계 계산
- 소계 = 단가 × 수량
- 소계는 주문 생성 시 계산하여 저장

---

## 5. 메뉴 규칙

### BR-MENU-01: 필수 필드
- 메뉴명: 필수, 1~100자
- 가격: 필수, 0 이상의 정수
- 카테고리: 필수

### BR-MENU-02: 가격 제한
- 최소 가격: 0원
- 최대 가격: 제한 없음 (정수 범위 내)

### BR-MENU-03: 메뉴 삭제
- 메뉴 삭제 시 기존 주문의 OrderItem은 유지
- OrderItem의 menu_id는 null이 될 수 있음

### BR-MENU-04: 표시 순서
- display_order 값이 작을수록 먼저 표시
- 기본값: 0
- 동일 순서 시 생성일 순

---

## 6. 카테고리 규칙

### BR-CAT-01: 필수 필드
- 카테고리명: 필수, 1~50자

### BR-CAT-02: 중복 방지
- 동일 매장 내 카테고리명 중복 불가

### BR-CAT-03: 삭제 제한
- 메뉴가 있는 카테고리는 삭제 불가
- 삭제 전 모든 메뉴를 다른 카테고리로 이동하거나 삭제 필요

### BR-CAT-04: 표시 순서
- display_order 값이 작을수록 먼저 표시
- 기본값: 0

---

## 7. 테이블 규칙

### BR-TABLE-01: 필수 필드
- 테이블 번호: 필수, 1 이상의 정수
- 비밀번호: 필수

### BR-TABLE-02: 중복 방지
- 동일 매장 내 테이블 번호 중복 불가

### BR-TABLE-03: 삭제 제한
- 활성 세션이 있는 테이블은 삭제 불가
- 삭제 전 세션 종료 필요

---

## 8. 검증 규칙 요약

| 엔티티 | 필드 | 규칙 |
|--------|------|------|
| Store | store_id | 필수, 고유, 1~50자 |
| User | username | 필수, 매장 내 고유, 1~50자 |
| User | password | 필수, bcrypt 해싱 |
| Table | table_number | 필수, 매장 내 고유, >= 1 |
| Category | name | 필수, 매장 내 고유, 1~50자 |
| Menu | name | 필수, 1~100자 |
| Menu | price | 필수, >= 0 |
| Menu | category_id | 필수, 유효한 카테고리 |
| Order | items | 필수, >= 1개 |
| OrderItem | quantity | 필수, >= 1 |

---

## 9. 에러 코드 정의

| 코드 | HTTP | 설명 |
|------|------|------|
| `STORE_NOT_FOUND` | 404 | 매장을 찾을 수 없음 |
| `TABLE_NOT_FOUND` | 404 | 테이블을 찾을 수 없음 |
| `USER_NOT_FOUND` | 404 | 사용자를 찾을 수 없음 |
| `AUTH_FAILED` | 401 | 인증 실패 |
| `TOKEN_EXPIRED` | 401 | 토큰 만료 |
| `SESSION_INVALID` | 400 | 유효하지 않은 세션 |
| `SESSION_NOT_FOUND` | 404 | 세션을 찾을 수 없음 |
| `ORDER_NOT_FOUND` | 404 | 주문을 찾을 수 없음 |
| `MENU_NOT_FOUND` | 404 | 메뉴를 찾을 수 없음 |
| `CATEGORY_NOT_FOUND` | 404 | 카테고리를 찾을 수 없음 |
| `CATEGORY_HAS_MENUS` | 400 | 메뉴가 있는 카테고리 삭제 불가 |
| `INVALID_STATUS_TRANSITION` | 400 | 유효하지 않은 상태 전이 |
| `VALIDATION_ERROR` | 400 | 입력값 검증 실패 |
| `DUPLICATE_ERROR` | 409 | 중복 데이터 |
