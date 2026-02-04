# 테이블오더 서비스 요구사항 명세서

## Intent Analysis Summary

### User Request
테이블오더 서비스 개발 - 고객이 테이블에서 직접 주문하고, 관리자가 실시간으로 주문을 모니터링할 수 있는 시스템

### Request Type
New Project (Greenfield)

### Scope Estimate
Multiple Components - 고객용 UI, 관리자용 UI, 백엔드 API, 데이터베이스

### Complexity Estimate
Moderate - 실시간 통신(SSE), 인증, 다중 매장 지원 등 복잡한 요소 포함

---

## 1. 기술 스택 결정사항

| 영역 | 선택 | 비고 |
|------|------|------|
| 백엔드 | FastAPI (Python) | 비동기 지원, SSE 용이 |
| 프론트엔드 | React.js | SPA 구조 |
| 데이터베이스 | PostgreSQL | 관계형, 트랜잭션 지원 |
| 배포 환경 | 로컬/온프레미스 | Docker 미사용 |
| 테스트 | 단위 테스트 | pytest 사용 |

---

## 2. 기능 요구사항 (Functional Requirements)

### 2.1 고객용 기능 (Customer Interface)

#### FR-C01: 테이블 태블릿 자동 로그인
- 초기 설정: 매장 식별자, 테이블 번호, 테이블 비밀번호 입력
- 로그인 정보 로컬 저장 (localStorage)
- 저장된 정보로 자동 로그인

#### FR-C02: 메뉴 조회 및 탐색
- 메뉴 화면이 기본 화면
- 카테고리별 메뉴 분류 및 표시
- 메뉴 상세 정보: 메뉴명, 가격, 설명 (이미지 없음 - MVP)
- 카테고리 간 빠른 이동
- 터치 친화적 UI (최소 44x44px 버튼)

#### FR-C03: 장바구니 관리
- 메뉴 추가/삭제
- 수량 조절 (증가/감소)
- 총 금액 실시간 계산
- 장바구니 비우기
- 로컬 저장 (페이지 새로고침 시 유지)

#### FR-C04: 주문 생성
- 주문 내역 최종 확인
- 주문 확정 버튼
- 주문 성공 시: 주문 번호 표시, 장바구니 비우기, 5초 후 메뉴 화면 리다이렉트
- 주문 실패 시: 에러 메시지 표시, 장바구니 유지

#### FR-C05: 주문 내역 조회
- 현재 테이블 세션 주문만 표시
- 주문 시간 순 정렬
- 주문별 상세 정보: 주문 번호, 시각, 메뉴/수량, 금액, 상태
- 주문 상태 실시간 업데이트 (SSE)

### 2.2 관리자용 기능 (Admin Interface)

#### FR-A01: 매장 인증
- 매장 식별자, 사용자명, 비밀번호 입력
- JWT 토큰 기반 인증
- 16시간 세션 유지
- 비밀번호 bcrypt 해싱

#### FR-A02: 실시간 주문 모니터링
- SSE 기반 실시간 주문 업데이트 (2초 이내)
- 그리드/대시보드 레이아웃 (테이블별 카드)
- 각 테이블 카드: 총 주문액, 최신 주문 미리보기
- 주문 카드 클릭 시 전체 메뉴 목록 상세 보기
- 주문 상태 변경 (대기중/준비중/완료)
- 신규 주문 시각적 강조

#### FR-A03: 테이블 관리
- 테이블 태블릿 초기 설정 (테이블 번호, 비밀번호)
- 주문 삭제 (확인 팝업, 총 주문액 재계산)
- 테이블 세션 종료 (이용 완료 처리)
- 과거 주문 내역 조회 (날짜 필터링)

#### FR-A04: 메뉴 관리
- 메뉴 CRUD (등록, 조회, 수정, 삭제)
- 메뉴 정보: 메뉴명, 가격, 설명, 카테고리
- 메뉴 노출 순서 조정
- 필수 필드 및 가격 범위 검증

#### FR-A05: 카테고리 관리
- 카테고리 CRUD (동적 관리)
- 카테고리 순서 조정

---

## 3. 비기능 요구사항 (Non-Functional Requirements)

### NFR-01: 성능
- 동시 접속자: 11~50명 지원
- 매장당 테이블: 최대 10개
- 주문 실시간 반영: 2초 이내

### NFR-02: 보안
- JWT 토큰 기반 인증
- 비밀번호 bcrypt 해싱
- 로그인 시도 제한

### NFR-03: 사용성
- 한국어 UI만 지원
- 터치 친화적 인터페이스
- 직관적인 네비게이션

### NFR-04: 확장성
- 다중 매장 지원 (멀티테넌트)
- 각 매장별 독립적인 데이터 관리

---

## 4. 제외 기능 (Out of Scope)

`requirements/constraints.md` 참조:
- 결제 처리 (PG사 연동, 영수증, 환불, 포인트/쿠폰)
- 복잡한 인증 (OAuth, SNS 로그인, 2FA)
- 이미지 업로드/리사이징
- 알림 시스템 (푸시, SMS, 이메일)
- 주방 기능 (주방 전달, 재고 관리)
- 고급 기능 (분석, 리포트, 직원 관리, 예약, 리뷰, 다국어)
- 외부 연동 (배달, POS, 소셜미디어)

---

## 5. 데이터 모델 개요

### 핵심 엔티티
- **Store**: 매장 정보
- **User**: 관리자 계정
- **Table**: 테이블 정보
- **TableSession**: 테이블 세션 (고객 이용 단위)
- **Category**: 메뉴 카테고리
- **Menu**: 메뉴 항목
- **Order**: 주문
- **OrderItem**: 주문 항목
- **OrderHistory**: 과거 주문 이력

---

## 6. API 개요

### 고객용 API
- `POST /api/customer/login` - 테이블 로그인
- `GET /api/customer/categories` - 카테고리 목록
- `GET /api/customer/menus` - 메뉴 목록
- `POST /api/customer/orders` - 주문 생성
- `GET /api/customer/orders` - 주문 내역 조회
- `GET /api/customer/orders/stream` - 주문 상태 SSE

### 관리자용 API
- `POST /api/admin/login` - 관리자 로그인
- `GET /api/admin/orders/stream` - 실시간 주문 SSE
- `PATCH /api/admin/orders/{id}/status` - 주문 상태 변경
- `DELETE /api/admin/orders/{id}` - 주문 삭제
- `POST /api/admin/tables/{id}/complete` - 테이블 이용 완료
- `GET /api/admin/tables/{id}/history` - 과거 주문 내역
- CRUD: `/api/admin/categories`, `/api/admin/menus`, `/api/admin/tables`

---

## 7. 요약

테이블오더 서비스는 FastAPI + React.js + PostgreSQL 스택으로 구현되며, 다중 매장을 지원하는 멀티테넌트 구조입니다. 고객은 테이블 태블릿에서 메뉴 조회, 장바구니 관리, 주문을 수행하고, 관리자는 실시간으로 주문을 모니터링하며 테이블과 메뉴를 관리합니다. SSE를 통해 실시간 주문 업데이트를 제공하며, MVP 단계에서는 이미지 없이 텍스트 기반 메뉴를 표시합니다.
