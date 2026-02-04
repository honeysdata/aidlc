# Code Generation Plan - Unit 2: Customer Frontend

## Overview
Customer Frontend 코드 생성 계획 (React.js)

## Unit Context
- **Unit Name**: Customer Frontend
- **Tech Stack**: React.js, Vite, Axios
- **Stories**: US-C01~C05 (테이블 로그인, 메뉴 조회, 장바구니, 주문, 주문 내역)
- **Location**: `customer-frontend/` (모노레포 구조)
- **Port**: 3000

## Code Generation Steps

### Phase 1: Project Setup
- [x] Step 1: Vite + React 프로젝트 생성
- [x] Step 2: 의존성 설치 (axios, react-router-dom)
- [x] Step 3: 프로젝트 구조 설정
- [x] Step 4: 환경 설정 (.env)

### Phase 2: Core Utilities
- [x] Step 5: API 클라이언트 설정 (axios instance)
- [x] Step 6: 로컬 스토리지 유틸리티
- [x] Step 7: 인증 컨텍스트 (AuthContext)
- [x] Step 8: 장바구니 컨텍스트 (CartContext)

### Phase 3: Common Components
- [x] Step 9: 레이아웃 컴포넌트 (Layout, Header, Navigation)
- [x] Step 10: 공통 UI 컴포넌트 (Button, Loading, ErrorMessage)

### Phase 4: Pages - Authentication
- [x] Step 11: SetupPage (초기 설정 페이지)

### Phase 5: Pages - Menu & Cart
- [x] Step 12: MenuPage (메뉴 조회 페이지)
- [x] Step 13: CartPage (장바구니 페이지)

### Phase 6: Pages - Order
- [x] Step 14: OrderConfirmPage (주문 확인 페이지)
- [x] Step 15: OrderSuccessPage (주문 성공 페이지)
- [x] Step 16: OrderHistoryPage (주문 내역 페이지)

### Phase 7: SSE Integration
- [x] Step 17: useSSE 훅 구현
- [x] Step 18: 실시간 주문 상태 업데이트 연동

### Phase 8: Routing & App Entry
- [x] Step 19: 라우터 설정
- [x] Step 20: App.jsx 완성
- [x] Step 21: 스타일링 (CSS)

### Phase 9: Documentation
- [x] Step 22: README.md 작성

## Story Traceability

| Story | 구현 Step |
|-------|----------|
| US-C01 (테이블 로그인) | Step 7, 11 |
| US-C02 (메뉴 조회) | Step 12 |
| US-C03 (장바구니) | Step 8, 13 |
| US-C04 (주문 생성) | Step 14, 15 |
| US-C05 (주문 내역) | Step 16, 17, 18 |

## File Structure

```
customer-frontend/
├── public/
│   └── index.html
├── src/
│   ├── api/
│   │   └── client.js
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.jsx
│   │   │   ├── Loading.jsx
│   │   │   └── ErrorMessage.jsx
│   │   ├── layout/
│   │   │   ├── Layout.jsx
│   │   │   ├── Header.jsx
│   │   │   └── Navigation.jsx
│   │   ├── menu/
│   │   │   ├── CategoryTabs.jsx
│   │   │   ├── MenuCard.jsx
│   │   │   └── MenuList.jsx
│   │   ├── cart/
│   │   │   ├── CartItem.jsx
│   │   │   └── CartSummary.jsx
│   │   └── order/
│   │       ├── OrderItem.jsx
│   │       └── OrderStatusBadge.jsx
│   ├── contexts/
│   │   ├── AuthContext.jsx
│   │   └── CartContext.jsx
│   ├── hooks/
│   │   ├── useLocalStorage.js
│   │   └── useSSE.js
│   ├── pages/
│   │   ├── SetupPage.jsx
│   │   ├── MenuPage.jsx
│   │   ├── CartPage.jsx
│   │   ├── OrderConfirmPage.jsx
│   │   ├── OrderSuccessPage.jsx
│   │   └── OrderHistoryPage.jsx
│   ├── utils/
│   │   └── format.js
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── .env.example
├── package.json
├── vite.config.js
└── README.md
```
