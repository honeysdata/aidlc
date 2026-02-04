# Code Generation Plan - Unit 3: Admin Frontend

## Overview
Admin Frontend 코드 생성 계획 (React.js)

## Unit Context
- **Unit Name**: Admin Frontend
- **Tech Stack**: React.js, Vite, Axios
- **Stories**: US-A01~A09 (관리자 로그인, 주문 모니터링, 테이블/메뉴/카테고리 관리)
- **Location**: `admin-frontend/` (모노레포 구조)
- **Port**: 3001

## Code Generation Steps

### Phase 1: Project Setup
- [x] Step 1: Vite + React 프로젝트 생성
- [x] Step 2: 프로젝트 구조 설정

### Phase 2: Core Utilities
- [x] Step 3: API 클라이언트 설정
- [x] Step 4: 인증 컨텍스트 (AuthContext)
- [x] Step 5: useSSE 훅

### Phase 3: Common Components
- [x] Step 6: 레이아웃 컴포넌트
- [x] Step 7: 공통 UI 컴포넌트

### Phase 4: Dashboard & Order
- [x] Step 8: LoginPage
- [x] Step 9: DashboardPage (테이블 그리드 + 실시간 주문)
- [x] Step 10: 주문 상태 변경/삭제 기능

### Phase 5: Table Management
- [x] Step 11: TableManagementPage
- [x] Step 12: TableHistoryPage

### Phase 6: Menu & Category Management
- [x] Step 13: MenuManagementPage
- [x] Step 14: CategoryManagementPage

### Phase 7: App Entry & Routing
- [x] Step 15: 라우터 및 App.jsx 완성
- [x] Step 16: 스타일링

### Phase 8: Documentation
- [x] Step 17: README.md 작성

## Story Traceability

| Story | 구현 Step |
|-------|----------|
| US-A01 (관리자 로그인) | Step 4, 8 |
| US-A02 (실시간 모니터링) | Step 5, 9 |
| US-A03 (주문 상태 변경) | Step 10 |
| US-A04 (주문 삭제) | Step 10 |
| US-A05 (이용 완료) | Step 9 |
| US-A06 (과거 내역) | Step 12 |
| US-A07 (테이블 설정) | Step 11 |
| US-A08 (메뉴 관리) | Step 13 |
| US-A09 (카테고리 관리) | Step 14 |

## File Structure

```
admin-frontend/
├── public/
│   └── index.html
├── src/
│   ├── api/
│   │   └── client.js
│   ├── components/
│   │   ├── common/
│   │   ├── layout/
│   │   ├── dashboard/
│   │   ├── table/
│   │   ├── menu/
│   │   └── category/
│   ├── contexts/
│   │   └── AuthContext.jsx
│   ├── hooks/
│   │   └── useSSE.js
│   ├── pages/
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── TableManagementPage.jsx
│   │   ├── TableHistoryPage.jsx
│   │   ├── MenuManagementPage.jsx
│   │   └── CategoryManagementPage.jsx
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
