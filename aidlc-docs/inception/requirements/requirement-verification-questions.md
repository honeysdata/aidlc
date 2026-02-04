# 요구사항 검증 질문

제공된 요구사항 문서를 분석한 결과, 몇 가지 명확화가 필요한 부분이 있습니다.
각 질문에 대해 [Answer]: 태그 뒤에 선택한 옵션의 알파벳을 입력해주세요.

---

## Question 1
기술 스택 선택: 백엔드 서버 프레임워크로 어떤 것을 사용하시겠습니까?

A) Node.js + Express.js (JavaScript/TypeScript)
B) Spring Boot (Java/Kotlin)
C) FastAPI (Python)
D) NestJS (TypeScript)
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 2
기술 스택 선택: 프론트엔드 프레임워크로 어떤 것을 사용하시겠습니까?

A) React.js
B) Vue.js
C) Next.js (React 기반 SSR)
D) Vanilla JavaScript (프레임워크 없음)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 3
데이터베이스 선택: 어떤 데이터베이스를 사용하시겠습니까?

A) PostgreSQL (관계형)
B) MySQL (관계형)
C) MongoDB (NoSQL Document)
D) SQLite (경량 관계형, 개발/테스트용)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 4
배포 환경: 어떤 환경에 배포할 예정입니까?

A) AWS (EC2, ECS, Lambda 등)
B) 로컬/온프레미스 서버
C) Docker 컨테이너 (클라우드 미정)
D) 개발 환경만 (배포 미정)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 5
매장(Store) 관리: 시스템이 단일 매장만 지원합니까, 아니면 다중 매장(멀티테넌트)을 지원해야 합니까?

A) 단일 매장만 지원 (하나의 매장 데이터만 관리)
B) 다중 매장 지원 (여러 매장이 각자의 데이터를 관리)
C) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 6
메뉴 이미지 처리: 메뉴 이미지는 어떻게 관리하시겠습니까?

A) 외부 URL 직접 입력 (이미지 호스팅은 별도 서비스 사용)
B) 서버에 이미지 파일 업로드 기능 구현
C) 이미지 없이 텍스트만 표시 (MVP 단계)
D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 7
테이블 수: 매장당 최대 몇 개의 테이블을 지원해야 합니까?

A) 10개 이하
B) 11~30개
C) 31~50개
D) 50개 초과
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 8
동시 접속자 수: 예상되는 동시 접속자 수는 얼마입니까?

A) 10명 이하 (소규모)
B) 11~50명 (중규모)
C) 51~100명 (대규모)
D) 100명 초과
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 9
주문 상태 실시간 업데이트: 고객 화면에서 주문 상태 실시간 업데이트가 필요합니까?

A) 필요함 (SSE 또는 WebSocket으로 실시간 반영)
B) 필요 없음 (수동 새로고침으로 확인)
C) MVP에서는 제외하고 추후 구현
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 10
언어 설정: UI 언어는 어떻게 지원하시겠습니까?

A) 한국어만 지원
B) 한국어 + 영어 지원
C) 다국어 지원 (추후 확장 가능한 구조)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 11
카테고리 관리: 메뉴 카테고리는 어떻게 관리하시겠습니까?

A) 고정된 카테고리 (코드에 하드코딩)
B) 관리자가 동적으로 카테고리 추가/수정/삭제 가능
C) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 12
테스트 전략: 어떤 수준의 테스트를 원하십니까?

A) 단위 테스트만
B) 단위 테스트 + 통합 테스트
C) 단위 테스트 + 통합 테스트 + E2E 테스트
D) 테스트 없이 MVP 우선 개발
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---
