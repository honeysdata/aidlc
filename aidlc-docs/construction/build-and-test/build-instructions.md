# Build Instructions - 테이블 오더 서비스

## 개요

테이블 오더 서비스는 3개의 독립적인 애플리케이션으로 구성됩니다:
- Backend API (FastAPI + PostgreSQL)
- Customer Frontend (React + Vite)
- Admin Frontend (React + Vite)

---

## 1. 사전 요구사항

### 필수 소프트웨어
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### 버전 확인
```bash
python3 --version   # 3.11 이상
node --version      # 18 이상
npm --version       # 9 이상
psql --version      # 14 이상
```

---

## 2. Backend API 빌드

### 2.1 가상환경 설정
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2.2 의존성 설치
```bash
pip install -r requirements.txt
```

### 2.3 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일 편집:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/table_order
JWT_SECRET_KEY=your-secret-key-change-in-production
```

### 2.4 데이터베이스 설정
```bash
# PostgreSQL에서 데이터베이스 생성
createdb table_order

# 또는 psql 사용
psql -c "CREATE DATABASE table_order;"
```

### 2.5 초기 데이터 생성
```bash
python -m scripts.seed
```

### 2.6 서버 실행
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2.7 API 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 3. Customer Frontend 빌드

### 3.1 의존성 설치
```bash
cd customer-frontend
npm install
```

### 3.2 환경 변수 설정
```bash
cp .env.example .env
```

### 3.3 개발 서버 실행
```bash
npm run dev
```
- 접속: http://localhost:3000

### 3.4 프로덕션 빌드
```bash
npm run build
npm run preview
```

---

## 4. Admin Frontend 빌드

### 4.1 의존성 설치
```bash
cd admin-frontend
npm install
```

### 4.2 환경 변수 설정
```bash
cp .env.example .env
```

### 4.3 개발 서버 실행
```bash
npm run dev
```
- 접속: http://localhost:3001

### 4.4 프로덕션 빌드
```bash
npm run build
npm run preview
```

---

## 5. 전체 시스템 실행 순서

1. PostgreSQL 서버 실행 확인
2. Backend API 실행 (포트 8000)
3. Customer Frontend 실행 (포트 3000)
4. Admin Frontend 실행 (포트 3001)

### 빠른 시작 스크립트 (개발용)

터미널 1 - Backend:
```bash
cd backend && source venv/bin/activate && uvicorn app.main:app --reload
```

터미널 2 - Customer Frontend:
```bash
cd customer-frontend && npm run dev
```

터미널 3 - Admin Frontend:
```bash
cd admin-frontend && npm run dev
```

---

## 6. 테스트 계정

Backend seed 데이터 실행 후:

| 용도 | 매장 ID | 사용자/테이블 | 비밀번호 |
|------|---------|---------------|----------|
| 관리자 | demo-store | admin | admin1234 |
| 고객 (테이블 1~5) | demo-store | 1~5 | 1234 |

---

## 7. 포트 구성

| 서비스 | 포트 | 설명 |
|--------|------|------|
| Backend API | 8000 | FastAPI 서버 |
| Customer Frontend | 3000 | 고객용 React 앱 |
| Admin Frontend | 3001 | 관리자용 React 앱 |
| PostgreSQL | 5432 | 데이터베이스 |
