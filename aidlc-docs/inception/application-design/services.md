# 서비스 레이어 설계

## 아키텍처 패턴: Layered Architecture

```
+------------------+
|   API Routers    |  ← HTTP 요청/응답 처리
+------------------+
         |
         v
+------------------+
|    Services      |  ← 비즈니스 로직, 트랜잭션 관리
+------------------+
         |
         v
+------------------+
|  Repositories    |  ← 데이터 접근, CRUD
+------------------+
         |
         v
+------------------+
|   Database       |  ← PostgreSQL
+------------------+
```

---

## 1. 서비스 정의

### 1.1 AuthService
**책임**: 인증 및 인가 처리

**의존성**:
- `UserRepository`
- `TableRepository`
- `TableSessionRepository`
- `JWTHandler`
- `PasswordHasher`

**오케스트레이션**:
1. 테이블 로그인: 테이블 검증 → 비밀번호 확인 → 세션 확인/생성 → JWT 발급
2. 관리자 로그인: 사용자 검증 → 비밀번호 확인 → JWT 발급 (16시간)

---

### 1.2 TableService
**책임**: 테이블 및 세션 라이프사이클 관리

**의존성**:
- `TableRepository`
- `TableSessionRepository`
- `OrderService`
- `PasswordHasher`

**오케스트레이션**:
1. 세션 시작: 활성 세션 확인 → 없으면 새 세션 생성
2. 세션 종료: 주문 아카이브 → 세션 종료 → 테이블 리셋

---

### 1.3 OrderService
**책임**: 주문 생성, 상태 관리, 히스토리 관리

**의존성**:
- `OrderRepository`
- `OrderItemRepository`
- `OrderHistoryRepository`
- `MenuRepository`
- `TableSessionRepository`
- `SSEService`

**오케스트레이션**:
1. 주문 생성: 메뉴 검증 → 가격 계산 → 주문 저장 → SSE 브로드캐스트
2. 상태 변경: 주문 조회 → 상태 업데이트 → SSE 브로드캐스트
3. 주문 삭제: 주문 조회 → 삭제 → 총액 재계산 → SSE 브로드캐스트
4. 아카이브: 세션 주문 조회 → 히스토리 저장 → 원본 삭제

---

### 1.4 MenuService
**책임**: 메뉴 CRUD 및 순서 관리

**의존성**:
- `MenuRepository`
- `CategoryRepository`

**오케스트레이션**:
1. 메뉴 생성: 카테고리 검증 → 메뉴 저장 → 순서 할당
2. 메뉴 삭제: 메뉴 조회 → 삭제 → 순서 재정렬

---

### 1.5 CategoryService
**책임**: 카테고리 CRUD 및 순서 관리

**의존성**:
- `CategoryRepository`
- `MenuRepository`

**오케스트레이션**:
1. 카테고리 삭제: 메뉴 존재 확인 → 있으면 실패 → 없으면 삭제

---

### 1.6 SSEService
**책임**: 실시간 이벤트 브로드캐스트

**의존성**: 없음 (독립적)

**오케스트레이션**:
1. 구독 관리: 클라이언트 연결 → 채널 등록 → 이벤트 스트림
2. 브로드캐스트: 이벤트 수신 → 해당 채널 구독자에게 전송

---

## 2. 트랜잭션 관리

### 2.1 트랜잭션 경계
- 서비스 레이어에서 트랜잭션 시작/종료
- Repository는 트랜잭션 내에서 동작

### 2.2 트랜잭션이 필요한 작업
- 주문 생성 (Order + OrderItems)
- 세션 종료 (Orders → OrderHistory + Session 종료)
- 주문 삭제 (Order + OrderItems 삭제)

---

## 3. 에러 처리 전략

### 3.1 에러 코드 체계

| 코드 | HTTP | 설명 |
|------|------|------|
| `AUTH_FAILED` | 401 | 인증 실패 |
| `TOKEN_EXPIRED` | 401 | 토큰 만료 |
| `FORBIDDEN` | 403 | 권한 없음 |
| `NOT_FOUND` | 404 | 리소스 없음 |
| `VALIDATION_ERROR` | 400 | 입력값 검증 실패 |
| `DUPLICATE_ERROR` | 409 | 중복 데이터 |
| `BUSINESS_ERROR` | 422 | 비즈니스 규칙 위반 |
| `SERVER_ERROR` | 500 | 서버 내부 오류 |

### 3.2 에러 응답 형식

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "주문을 찾을 수 없습니다.",
  "details": {
    "order_id": 123
  }
}
```

---

## 4. API 버전 관리

### 4.1 URL 구조
```
/api/v1/customer/*  - 고객용 API
/api/v1/admin/*     - 관리자용 API
```

### 4.2 버전 업그레이드 전략
- 새 버전 추가 시 `/api/v2/*` 경로 사용
- 이전 버전은 일정 기간 유지 후 deprecate
