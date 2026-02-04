# Customer Frontend

테이블 오더 서비스 - 고객용 프론트엔드

## 기술 스택

- React 18
- Vite
- React Router v6
- Axios

## 설치 및 실행

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 설정

```bash
cp .env.example .env
```

`.env` 파일에서 API URL을 설정합니다 (기본값: `http://localhost:8000/api/v1`)

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 http://localhost:3000 접속

### 4. 프로덕션 빌드

```bash
npm run build
npm run preview
```

## 주요 기능

- **테이블 로그인**: 매장ID, 테이블번호, 비밀번호로 로그인
- **메뉴 조회**: 카테고리별 메뉴 탐색
- **장바구니**: 메뉴 추가/수량 조절/삭제
- **주문**: 주문 생성 및 확인
- **주문 내역**: 현재 세션 주문 목록 및 실시간 상태 업데이트

## 페이지 구조

| 경로 | 페이지 | 설명 |
|------|--------|------|
| `/setup` | SetupPage | 초기 설정 (로그인) |
| `/menu` | MenuPage | 메뉴 조회 (기본 화면) |
| `/cart` | CartPage | 장바구니 |
| `/order/confirm` | OrderConfirmPage | 주문 확인 |
| `/order/success` | OrderSuccessPage | 주문 완료 |
| `/orders` | OrderHistoryPage | 주문 내역 |

## 프로젝트 구조

```
src/
├── api/           # API 클라이언트
├── components/    # 재사용 컴포넌트
│   ├── common/    # 공통 UI
│   ├── layout/    # 레이아웃
│   ├── menu/      # 메뉴 관련
│   ├── cart/      # 장바구니 관련
│   └── order/     # 주문 관련
├── contexts/      # React Context
├── hooks/         # Custom Hooks
├── pages/         # 페이지 컴포넌트
├── utils/         # 유틸리티 함수
├── App.jsx        # 앱 진입점
└── main.jsx       # React 렌더링
```

## 테스트 계정

Backend seed 데이터 사용 시:
- 매장 ID: `demo-store`
- 테이블 번호: `1` ~ `5`
- 비밀번호: `1234`
