# Functional Design Plan - Unit 1: Backend API

## Overview
Backend API의 비즈니스 로직 및 도메인 모델 상세 설계

## Execution Checklist

### Phase 1: Domain Entities Design
- [x] 핵심 엔티티 정의 (Store, User, Table, Menu, Order 등)
- [x] 엔티티 관계 정의
- [x] domain-entities.md 생성

### Phase 2: Business Logic Model
- [x] 주요 비즈니스 프로세스 정의
- [x] 데이터 흐름 정의
- [x] business-logic-model.md 생성

### Phase 3: Business Rules
- [x] 검증 규칙 정의
- [x] 비즈니스 제약 조건 정의
- [x] business-rules.md 생성

---

## Questions for Functional Design

아래 질문에 답변해주세요. [Answer]: 태그 뒤에 선택한 옵션을 입력해주세요.

---

### Question 1: 주문 번호 생성 방식
주문 번호를 어떻게 생성하시겠습니까?

A) 순차 번호 (매장별 1, 2, 3...)
B) 날짜 기반 (20260204-001, 20260204-002...)
C) UUID (고유 식별자)
D) Other (please describe after [Answer]: tag below)

[Answer]:   B

---

### Question 2: 테이블 세션 자동 시작
테이블 세션은 언제 자동으로 시작됩니까?

A) 첫 주문 생성 시 자동 시작
B) 테이블 로그인 시 자동 시작
C) 관리자가 수동으로 시작
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 3: 주문 상태 전이 규칙
주문 상태 변경에 제한을 두시겠습니까?

A) 순차적 전이만 허용 (대기중→준비중→완료, 역방향 불가)
B) 자유로운 전이 허용 (어떤 상태에서든 변경 가능)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 4: 메뉴 삭제 시 기존 주문 처리
메뉴가 삭제될 때 해당 메뉴가 포함된 기존 주문은 어떻게 처리합니까?

A) 메뉴 정보를 주문에 스냅샷으로 저장 (삭제되어도 주문 내역 유지)
B) 메뉴 삭제 시 해당 메뉴가 포함된 주문도 함께 삭제
C) 주문이 있는 메뉴는 삭제 불가
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 5: 가격 변경 시 기존 주문 처리
메뉴 가격이 변경될 때 기존 주문의 금액은 어떻게 처리합니까?

A) 주문 시점의 가격을 스냅샷으로 저장 (가격 변경 영향 없음)
B) 메뉴 가격 변경 시 기존 주문 금액도 자동 업데이트
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Instructions

1. 위 5개 질문에 대해 [Answer]: 태그 뒤에 선택한 옵션(A, B, C 등)을 입력해주세요.
2. 모든 질문에 답변 후 "완료" 또는 "done"이라고 알려주세요.
3. 답변을 바탕으로 Functional Design 문서를 생성합니다.
