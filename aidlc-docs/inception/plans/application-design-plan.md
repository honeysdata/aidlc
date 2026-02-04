# Application Design Plan

## Overview
테이블오더 서비스의 애플리케이션 설계 계획

## Execution Checklist

### Phase 1: Component Identification
- [x] 백엔드 컴포넌트 식별 및 정의
- [x] 프론트엔드 컴포넌트 식별 및 정의
- [x] 컴포넌트 문서 생성 (components.md)

### Phase 2: Component Methods Design
- [x] 각 컴포넌트의 메서드 시그니처 정의
- [x] 입출력 타입 정의
- [x] 컴포넌트 메서드 문서 생성 (component-methods.md)

### Phase 3: Service Layer Design
- [x] 서비스 레이어 정의
- [x] 서비스 오케스트레이션 패턴 정의
- [x] 서비스 문서 생성 (services.md)

### Phase 4: Dependency Mapping
- [x] 컴포넌트 간 의존성 매핑
- [x] 통신 패턴 정의
- [x] 의존성 문서 생성 (component-dependency.md)

---

## Questions for Application Design

아래 질문에 답변해주세요. [Answer]: 태그 뒤에 선택한 옵션을 입력해주세요.

---

### Question 1: 백엔드 아키텍처 패턴
백엔드 코드 구조를 어떤 패턴으로 설계하시겠습니까?

A) Layered Architecture (Controller → Service → Repository)
B) Clean Architecture (Use Cases, Entities, Interfaces)
C) Simple Structure (라우터에서 직접 DB 접근, 소규모 MVP용)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 2: 프론트엔드 상태 관리
React 앱의 상태 관리 방식을 어떻게 하시겠습니까?

A) React Context API (간단한 전역 상태)
B) Redux / Redux Toolkit (복잡한 상태 관리)
C) Zustand (경량 상태 관리)
D) 로컬 상태만 사용 (useState, props drilling)
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

### Question 3: 고객/관리자 앱 분리
고객용 앱과 관리자용 앱을 어떻게 구성하시겠습니까?

A) 하나의 React 앱에서 라우팅으로 분리 (/customer/*, /admin/*)
B) 두 개의 별도 React 앱으로 분리
C) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 4: API 버전 관리
API 버전 관리를 어떻게 하시겠습니까?

A) URL 경로에 버전 포함 (/api/v1/...)
B) 버전 관리 없음 (MVP 단계)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 5: 에러 처리 패턴
API 에러 응답 형식을 어떻게 하시겠습니까?

A) 표준화된 에러 응답 (status, code, message, details)
B) HTTP 상태 코드와 간단한 메시지만
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Instructions

1. 위 5개 질문에 대해 [Answer]: 태그 뒤에 선택한 옵션(A, B, C 등)을 입력해주세요.
2. 모든 질문에 답변 후 "완료" 또는 "done"이라고 알려주세요.
3. 답변을 바탕으로 애플리케이션 설계 문서를 생성합니다.
