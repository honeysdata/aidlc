# Tech Stack Decisions - Backend API

## 1. 핵심 기술 스택

| 영역 | 기술 | 버전 | 선택 이유 |
|------|------|------|----------|
| 언어 | Python | 3.11+ | 타입 힌트, 성능 개선 |
| 웹 프레임워크 | FastAPI | 0.109+ | 비동기, 자동 문서화, 타입 검증 |
| ORM | SQLAlchemy | 2.0+ | 비동기 지원, 성숙한 생태계 |
| 데이터베이스 | PostgreSQL | 15+ | 안정성, JSON 지원, 성능 |
| 마이그레이션 | Alembic | 1.13+ | SQLAlchemy 통합 |

---

## 2. 의존성 패키지

### 2.1 Core Dependencies

```
# requirements.txt

# Web Framework
fastapi>=0.109.0
uvicorn[standard]>=0.27.0

# Database
sqlalchemy>=2.0.0
asyncpg>=0.29.0
alembic>=1.13.0

# Authentication
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4

# Validation
pydantic>=2.5.0
pydantic-settings>=2.1.0
email-validator>=2.1.0

# SSE
sse-starlette>=1.8.0

# Utilities
python-multipart>=0.0.6
python-dotenv>=1.0.0
```

### 2.2 Development Dependencies

```
# requirements-dev.txt

# Testing
pytest>=7.4.0
pytest-asyncio>=0.23.0
pytest-cov>=4.1.0
httpx>=0.26.0

# Code Quality
black>=24.1.0
isort>=5.13.0
flake8>=7.0.0
mypy>=1.8.0
```

---

## 3. 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 설정 (Pydantic Settings)
│   ├── database.py          # DB 연결 및 세션
│   │
│   ├── models/              # SQLAlchemy 모델
│   │   ├── __init__.py
│   │   ├── base.py          # Base 클래스
│   │   ├── store.py
│   │   ├── user.py
│   │   ├── table.py
│   │   ├── category.py
│   │   ├── menu.py
│   │   └── order.py
│   │
│   ├── schemas/             # Pydantic 스키마
│   │   ├── __init__.py
│   │   ├── common.py        # 공통 응답 스키마
│   │   ├── auth.py
│   │   ├── table.py
│   │   ├── category.py
│   │   ├── menu.py
│   │   └── order.py
│   │
│   ├── routers/             # API 라우터
│   │   ├── __init__.py
│   │   ├── customer/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── menu.py
│   │   │   └── order.py
│   │   └── admin/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── order.py
│   │       ├── table.py
│   │       ├── menu.py
│   │       └── category.py
│   │
│   ├── services/            # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── table.py
│   │   ├── category.py
│   │   ├── menu.py
│   │   ├── order.py
│   │   └── sse.py
│   │
│   ├── repositories/        # 데이터 접근
│   │   ├── __init__.py
│   │   ├── base.py          # 기본 Repository
│   │   ├── store.py
│   │   ├── user.py
│   │   ├── table.py
│   │   ├── category.py
│   │   ├── menu.py
│   │   └── order.py
│   │
│   └── utils/               # 유틸리티
│       ├── __init__.py
│       ├── jwt.py           # JWT 처리
│       ├── password.py      # 비밀번호 해싱
│       ├── errors.py        # 에러 핸들링
│       └── logging.py       # 로깅 설정
│
├── migrations/              # Alembic 마이그레이션
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
│
├── tests/                   # 테스트
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures
│   ├── test_auth.py
│   ├── test_menu.py
│   └── test_order.py
│
├── logs/                    # 로그 파일
│   └── .gitkeep
│
├── .env.example             # 환경 변수 예시
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## 4. 환경 변수

```bash
# .env.example

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/tableorder

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ADMIN_EXPIRE_HOURS=16
JWT_TABLE_EXPIRE_HOURS=24

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

---

## 5. 데이터베이스 설정

### 5.1 연결 풀 설정

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,           # 기본 연결 수
    max_overflow=10,        # 추가 연결 수 (총 20)
    pool_timeout=30,        # 연결 대기 타임아웃
    pool_recycle=3600,      # 연결 재활용 주기 (1시간)
    echo=False              # SQL 로깅 비활성화
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

### 5.2 PostgreSQL 설정

```sql
-- 데이터베이스 생성
CREATE DATABASE tableorder;

-- 사용자 생성
CREATE USER tableorder_user WITH PASSWORD 'your_password';

-- 권한 부여
GRANT ALL PRIVILEGES ON DATABASE tableorder TO tableorder_user;
```

---

## 6. 로깅 설정

```python
# utils/logging.py
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    
    # 파일 핸들러 (일별 로테이션)
    file_handler = TimedRotatingFileHandler(
        "logs/app.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    
    # 포맷터
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger
```

---

## 7. API 문서화

| 항목 | 설정 |
|------|------|
| Swagger UI | `/docs` |
| ReDoc | `/redoc` |
| OpenAPI JSON | `/openapi.json` |
| 자동 생성 | FastAPI 내장 |
