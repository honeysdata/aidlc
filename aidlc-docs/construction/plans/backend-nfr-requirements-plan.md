# NFR Requirements Plan - Unit 1: Backend API

## Overview
Backend API의 비기능 요구사항 및 기술 스택 결정

## Execution Checklist

### Phase 1: NFR Assessment
- [x] 성능 요구사항 정의
- [x] 보안 요구사항 정의
- [x] 가용성 요구사항 정의
- [x] nfr-requirements.md 생성

### Phase 2: Tech Stack Decisions
- [x] 기술 스택 상세 결정
- [x] 라이브러리/프레임워크 버전 결정
- [x] tech-stack-decisions.md 생성

---

## Questions for NFR Requirements

이미 결정된 사항:
- 백엔드: FastAPI (Python)
- 데이터베이스: PostgreSQL
- 동시 접속자: 11~50명
- 테이블 수: 10개 이하
- 실시간 업데이트: SSE

아래 추가 질문에 답변해주세요.

---

### Question 1: 응답 시간 목표
API 응답 시간 목표를 어떻게 설정하시겠습니까?

A) 일반 API: 500ms 이내, SSE 연결: 2초 이내
B) 일반 API: 1초 이내, SSE 연결: 3초 이내
C) 특별한 목표 없음 (합리적인 수준)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 2: 데이터베이스 연결 풀
데이터베이스 연결 풀 크기를 어떻게 설정하시겠습니까?

A) 소규모 (5~10 연결)
B) 중규모 (10~20 연결)
C) 자동 관리 (SQLAlchemy 기본값)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 3: 로깅 수준
로깅을 어떻게 설정하시겠습니까?

A) 기본 로깅 (INFO 레벨, 콘솔 출력)
B) 상세 로깅 (DEBUG 레벨, 파일 저장)
C) 구조화된 로깅 (JSON 형식, 파일 저장)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 4: CORS 설정
CORS(Cross-Origin Resource Sharing)를 어떻게 설정하시겠습니까?

A) 모든 출처 허용 (개발 편의)
B) 특정 출처만 허용 (localhost:3000, localhost:3001)
C) 환경 변수로 설정 가능하게
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 5: 비밀번호 정책
비밀번호 정책을 어떻게 설정하시겠습니까?

A) 최소 길이만 (4자 이상)
B) 기본 정책 (8자 이상)
C) 강화 정책 (8자 이상, 대소문자+숫자+특수문자)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Instructions

1. 위 5개 질문에 대해 [Answer]: 태그 뒤에 선택한 옵션(A, B, C 등)을 입력해주세요.
2. 모든 질문에 답변 후 "완료" 또는 "done"이라고 알려주세요.
3. 답변을 바탕으로 NFR Requirements 문서를 생성합니다.
