# Admin Frontend

테이블 오더 서비스 - 관리자용 프론트엔드

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

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 http://localhost:3001 접속

### 4. 프로덕션 빌드

```bash
npm run build
npm run preview
```

## 주요 기능

- **관리자 로그인**: 매장ID, 사용자명, 비밀번호로 로그인 (16시간 세션)
- **실시간 대시보드**: 테이블별 주문 현황 실시간 모니터링 (SSE)
- **주문 관리**: 주문 상태 변경 (대기중→준비중→완료), 주문 삭제
- **테이블 관리**: 테이블 추가/삭제, 비밀번호 변경, 이용 완료 처리
- **과거 내역**: 테이블별 과거 주문 내역 조회 (날짜 필터)
- **메뉴 관리**: 메뉴 CRUD, 품절 설정
- **카테고리 관리**: 카테고리 CRUD

## 페이지 구조

| 경로 | 페이지 | 설명 |
|------|--------|------|
| `/login` | LoginPage | 관리자 로그인 |
| `/` | DashboardPage | 실시간 주문 대시보드 |
| `/tables` | TableManagementPage | 테이블 관리 |
| `/tables/:id/history` | TableHistoryPage | 과거 주문 내역 |
| `/menus` | MenuManagementPage | 메뉴 관리 |
| `/categories` | CategoryManagementPage | 카테고리 관리 |

## 프로젝트 구조

```
src/
├── api/           # API 클라이언트
├── components/    # 재사용 컴포넌트
│   ├── common/    # 공통 UI (Button, Modal, Loading)
│   ├── layout/    # 레이아웃 (사이드바)
│   └── dashboard/ # 대시보드 컴포넌트
├── contexts/      # React Context (Auth)
├── hooks/         # Custom Hooks (SSE)
├── pages/         # 페이지 컴포넌트
├── utils/         # 유틸리티 함수
├── App.jsx        # 앱 진입점
└── main.jsx       # React 렌더링
```

## 테스트 계정

Backend seed 데이터 사용 시:
- 매장 ID: `demo-store`
- 사용자명: `admin`
- 비밀번호: `admin1234`
