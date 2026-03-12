# Backend Coding Rules (FastAPI / Python / PostgreSQL)

> 이 파일은 Coding Agent와 QA Agent가 web-fullstack 프로젝트의 백엔드를 작업할 때 반드시 준수해야 하는 코딩 룰입니다.

---

## 1. 프로젝트 구조

```
be-project/
├── src/
│   ├── main.py                   # FastAPI 앱 엔트리포인트, 라우터/미들웨어/예외 핸들러 등록
│   ├── core/
│   │   ├── config.py             # pydantic-settings 기반 환경변수 로드
│   │   ├── database.py           # 엔진, 세션팩토리, get_async_db() — 인프라 설정만
│   │   └── exceptions.py         # BaseCustomException + custom_exception_handler만 정의
│   ├── api/
│   │   └── v1/
│   │       ├── router.py         # 전체 라우터 통합 (include_router)
│   │       ├── swaggers/         # Swagger 문서용 responses 객체 정의
│   │       │                     # (schemas/ 의 Pydantic 모델을 참조하여 구성)
│   │       └── endpoints/        # 엔드포인트별 파일 (예: users.py, items.py)
│   ├── models/                   # SQLAlchemy ORM 모델 (DeclarativeBase 상속)
│   ├── schemas/                  # Pydantic 스키마 (Request / Response / Base)
│   ├── services/                 # 비즈니스 로직
│   │   └── exceptions/           # 도메인별 예외 클래스 (예: user_exceptions.py)
│   ├── repositories/             # DB 쿼리 레이어 (AsyncSession 직접 사용)
│   │   └── protocols/            # Repository 인터페이스 (Protocol 정의)
│   ├── dependencies/             # DI용 종속성 주입 함수 (도메인별 파일 분리)
│   │   └── user.py               # get_user_repository(), get_user_service()
│   ├── constants/                # 도메인별 상수 / Enum / 환경별 값 파일로 분리
│   ├── middleware/               # 횡단 관심사 미들웨어 (Request ID, 로깅 등)
│   └── utils/                    # 재사용 유틸 (HTTP 클라이언트 래퍼, logger 등)
│       └── logger.py
│
├── tests/
│   ├── conftest.py               # pytest fixtures (TestClient, DB override 등)
│   ├── api/v1/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── dependencies/
│
├── alembic/                      # DB 마이그레이션
│   └── versions/
├── ruff.toml                     # 린터 설정 (아래 섹션 참조)
└── .envrc.example                # direnv 기반 환경변수 예시
```

---

## 2. 레이어 책임 분리 (필수)

| 레이어 | 역할 | 금지 사항 |
|--------|------|-----------|
| `endpoints/` | HTTP 요청/응답 처리, 라우팅 | 비즈니스 로직 직접 작성 금지 |
| `services/` | 비즈니스 로직 | DB 쿼리 직접 작성 금지 |
| `repositories/` | DB 쿼리 (`AsyncSession` 직접 사용) | 비즈니스 로직 금지 |
| `schemas/` | 입출력 데이터 검증 | ORM 모델 직접 노출 금지 |
| `dependencies/` | DI 팩토리 함수 | 비즈니스/쿼리 로직 금지 |
| `core/` | 인프라 설정 (DB, 환경변수, 기반 예외) | 도메인 로직 금지 |

---

## 3. DB 설정 (PostgreSQL + Async SQLAlchemy)

### 3-1. 드라이버

| 목적 | 라이브러리 |
|------|-----------|
| 비동기 드라이버 | `asyncpg` |
| ORM | `sqlalchemy[asyncio]` (`AsyncSession`, `async_sessionmaker`) |
| 마이그레이션 | `alembic` (동기 커넥션으로 별도 실행) |

### 3-2. 엔진 및 세션 팩토리 (`src/core/database.py`)

DB 인프라 설정은 **반드시 `src/core/database.py`에만** 정의한다.
`dependencies/`는 이 파일에서 `get_async_db`를 import해서 사용한다.

```python
# src/core/database.py
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,           # postgresql+asyncpg://...
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,              # 끊어진 커넥션 자동 감지
    echo=settings.DEBUG,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,          # await 후 lazy-load 방지
    autoflush=False,
    autocommit=False,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    요청 단위 AsyncSession 제공.
    정상 종료 시 commit, 예외 발생 시 rollback 후 re-raise.
    직접 import 금지 — 반드시 dependencies/ 를 통해 주입받을 것.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 3-3. ORM 모델 Base

```python
# src/models/base.py
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    """생성/수정 시각 자동 관리. 모든 테이블에 적용 권장."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
```

### 3-4. ORM 모델 작성 규칙

```python
# src/models/user.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
```

- `Mapped[T]` + `mapped_column()` 사용 필수 (SQLAlchemy 2.x 스타일)
- `Column()` 구문 사용 금지 (레거시)
- 모든 컬럼에 `nullable` 명시
- 자주 조회되는 필드에 `index=True`

### 3-5. Repository Protocol (인터페이스 정의)

구현체 작성 전에 반드시 **Protocol을 먼저 정의**한다.
Service는 Protocol 타입에만 의존하고, 구현체(concrete class)를 직접 참조하지 않는다.
이를 통해 OCP(구현 변경에 닫힘)와 LSP(구현체 교체 가능)를 타입 수준에서 보장한다.

```python
# src/repositories/protocols/user_repository.py
from typing import Protocol
from src.models.user import User

class UserRepositoryProtocol(Protocol):
    async def find_by_id(self, user_id: int) -> User | None: ...
    async def find_all_active(self, *, offset: int, limit: int) -> list[User]: ...
    async def count_active(self) -> int: ...
    async def create(self, user: User) -> User: ...
    async def update(self, user: User) -> User: ...
    async def delete(self, user_id: int) -> None: ...
```

### 3-6. Repository 구현체

```python
# src/repositories/user_repository.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_by_id(self, user_id: int) -> User | None:
        result = await self._db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def find_all_active(self, *, offset: int, limit: int) -> list[User]:
        result = await self._db.execute(
            select(User)
            .where(User.is_active == True)
            .order_by(User.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_active(self) -> int:
        result = await self._db.execute(
            select(func.count()).where(User.is_active == True)
        )
        return result.scalar_one()

    async def create(self, user: User) -> User:
        self._db.add(user)
        await self._db.flush()     # ID 확보 (commit은 get_async_db에서 일괄 처리)
        await self._db.refresh(user)
        return user
```

- `self._db.commit()` 직접 호출 금지 — commit은 `get_async_db()`에서 일괄 처리
- `flush()`는 ID 선확보 등 필요 시 허용
- N+1 문제가 예상되는 관계는 `selectinload` / `joinedload` 명시

### 3-7. 멀티 Repository 트랜잭션 (Unit of Work)

**하나의 비즈니스 로직에서 여러 Repository를 함께 사용할 때는 반드시 같은 `AsyncSession`을 공유해야 한다.**
DI 팩토리에서 동일한 `db` 인스턴스를 각 Repository에 주입하는 방식으로 처리한다.

```python
# dependencies/order.py — 같은 세션을 두 Repository에 주입
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_async_db
from src.repositories.order_repository import OrderRepository
from src.repositories.inventory_repository import InventoryRepository
from src.services.order_service import OrderService

def get_order_service(
    db: AsyncSession = Depends(get_async_db),
) -> OrderService:
    # 같은 db 세션 → 하나의 트랜잭션으로 묶임
    return OrderService(
        order_repo=OrderRepository(db),
        inventory_repo=InventoryRepository(db),
    )
```

```python
# src/services/order_service.py — 트랜잭션 원자성이 자동 보장
class OrderService:
    def __init__(
        self,
        order_repo: OrderRepositoryProtocol,
        inventory_repo: InventoryRepositoryProtocol,
    ) -> None:
        self._order_repo = order_repo
        self._inventory_repo = inventory_repo

    async def place_order(self, user_id: int, item_id: int, quantity: int) -> Order:
        # 두 쿼리가 같은 세션 → 하나라도 예외 시 get_async_db()가 전체 rollback
        await self._inventory_repo.decrease(item_id, quantity)
        return await self._order_repo.create(user_id, item_id, quantity)
```

- Service 생성자는 Protocol 타입으로 선언 (구현체 직접 참조 금지)
- 트랜잭션 경계는 항상 `get_async_db()`가 관리 — Service에서 commit/rollback 금지

### 3-8. Alembic 마이그레이션

- 마이그레이션은 동기 커넥션(`psycopg2` 또는 `pg8000`) 사용 (Alembic 요구사항)
- `alembic revision --autogenerate` 후 반드시 생성된 파일 검토
- `__tablename__` 변경 시 `op.rename_table()` 명시 (미명시 시 autogenerate가 drop/create로 잘못 생성)

---

## 4. FastAPI 작성 규칙

### 4-1. 라우터

```python
# ✅ APIRouter 사용, prefix와 tags 명시
router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/{user_id}",
    response_model=BaseResponse[UserResponse],
    status_code=200,
    responses=GET_USER_RESPONSES,   # swaggers/ 에서 가져온 Swagger 명세
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> BaseResponse[UserResponse]:
    return await service.get_user(user_id)
```

### 4-2. 의존성 주입 규칙

- 서비스는 반드시 `Depends(get_{domain}_service)`로 주입
- DB 세션(`get_async_db`)은 `core/database.py`에 정의, `dependencies/`에서 import하여 사용
- 엔드포인트에서 `AsyncSession`을 직접 주입받는 것 금지
- 엔드포인트에서 Repository를 직접 주입받는 것 금지

```
엔드포인트 → get_{domain}_service → get_{domain}_repository → get_async_db
(엔드포인트는 서비스만 알고, 그 아래 체인은 DI가 해결)
```

### 4-3. 응답 형식 통일

모든 API 응답은 `BaseResponse[T]`를 사용한다 (섹션 5 참조):

```python
# 성공
{"success": true, "data": {...}, "error": null}

# 실패
{"success": false, "data": null, "error": {"code": "USER_NOT_FOUND", "message": "..."}}
```

### 4-4. 예외 구조

**`core/exceptions.py`**: 기반 클래스와 핸들러만.
**`services/exceptions/`**: 도메인별 예외 파일로 분리.

```python
# src/core/exceptions.py — 기반 클래스 + 핸들러만 정의
from fastapi import Request
from fastapi.responses import JSONResponse

class BaseCustomException(Exception):
    status_code: int = 500
    code: str = "INTERNAL_SERVER_ERROR"
    message: str = "서버 오류가 발생했습니다."

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.__class__.message

async def custom_exception_handler(
    request: Request, exc: BaseCustomException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {"code": exc.code, "message": exc.message},
        },
    )
```

```python
# src/services/exceptions/user_exceptions.py — 도메인 예외는 도메인 파일로 분리
from src.core.exceptions import BaseCustomException

class UserNotFoundException(BaseCustomException):
    status_code = 404
    code = "USER_NOT_FOUND"
    message = "해당 유저를 찾을 수 없습니다."

class UserAlreadyExistsException(BaseCustomException):
    status_code = 409
    code = "USER_ALREADY_EXISTS"
    message = "이미 존재하는 유저입니다."
```

```python
# src/main.py — 핸들러 등록 필수 (없으면 모든 커스텀 예외가 500으로 반환됨)
from src.core.exceptions import BaseCustomException, custom_exception_handler

app = FastAPI()
app.add_exception_handler(BaseCustomException, custom_exception_handler)
```

- `HTTPException` 직접 사용 금지
- 새 도메인 추가 시 `services/exceptions/{domain}_exceptions.py` 파일 신규 생성

### 4-5. 미들웨어 (`middleware/`)

횡단 관심사는 미들웨어로 처리한다. `main.py`에서 `add_middleware()`로 등록.

```python
# src/middleware/request_id.py — 모든 요청에 고유 ID 부여
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

```python
# src/middleware/logging.py — 요청/응답 공통 로깅
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "method=%s path=%s status=%s duration=%.1fms request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            getattr(request.state, "request_id", "-"),
        )
        return response
```

```python
# src/main.py
from src.middleware.request_id import RequestIDMiddleware
from src.middleware.logging import LoggingMiddleware

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
```

### 4-6. `swaggers/` 디렉토리 사용법

엔드포인트의 `responses=` 파라미터에 전달할 Swagger 명세 객체를 도메인별로 분리하여 정의한다.
`schemas/`의 Pydantic 모델을 최대한 재사용한다.

```python
# src/api/v1/swaggers/user.py
from src.schemas.user import UserResponse
from src.schemas.base import BaseResponse

GET_USER_RESPONSES: dict = {
    200: {"model": BaseResponse[UserResponse], "description": "유저 조회 성공"},
    404: {
        "description": "유저 없음",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {"code": "USER_NOT_FOUND", "message": "해당 유저를 찾을 수 없습니다."},
                }
            }
        },
    },
}
```

### 4-7. `constants/` 디렉토리 사용법

도메인별 상수, Enum, 환경별 분기 값을 파일로 분리한다.

```python
# src/constants/user.py
from enum import StrEnum

class UserRole(StrEnum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

MAX_LOGIN_ATTEMPT = 5
DEFAULT_PAGE_SIZE = 20
```

---

## 5. Pydantic 스키마 규칙

### 5-1. BaseResponse (모든 응답에 필수 적용)

```python
# src/schemas/base.py
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    message: str

class BaseResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: ErrorDetail | None = None

    @classmethod
    def ok(cls, data: T) -> "BaseResponse[T]":
        return cls(success=True, data=data, error=None)

    @classmethod
    def fail(cls, code: str, message: str) -> "BaseResponse[None]":
        return cls(success=False, data=None, error=ErrorDetail(code=code, message=message))
```

### 5-2. 페이지네이션 스키마 (조회 API 공통)

페이지네이션이 필요한 모든 조회 API는 아래 스키마를 사용한다.
offset 방식을 기본으로 하되, 무한스크롤이 필요한 경우 cursor 방식으로 별도 정의한다.

```python
# src/schemas/pagination.py
from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationQuery(BaseModel):
    """공통 페이지네이션 쿼리 파라미터"""
    page: int = Field(default=1, ge=1, description="페이지 번호 (1부터 시작)")
    size: int = Field(default=20, ge=1, le=100, description="페이지 크기")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size

class PaginatedData(BaseModel, Generic[T]):
    """페이지네이션 응답 공통 구조"""
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int

    @classmethod
    def of(cls, items: list[T], total: int, query: PaginationQuery) -> "PaginatedData[T]":
        return cls(
            items=items,
            total=total,
            page=query.page,
            size=query.size,
            total_pages=-(-total // query.size),  # ceiling division
        )
```

```python
# 엔드포인트 사용 예시
@router.get("/", response_model=BaseResponse[PaginatedData[UserResponse]])
async def list_users(
    query: Annotated[PaginationQuery, Query()],
    service: UserService = Depends(get_user_service),
) -> BaseResponse[PaginatedData[UserResponse]]:
    result = await service.list_users(query)
    return BaseResponse.ok(result)
```

### 5-3. 도메인 스키마 패턴

```python
# src/schemas/user.py — Base → Create/Update → Response 패턴
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):           # Update는 모든 필드 Optional
    name: str | None = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

- `orm_mode` 사용 금지 → `ConfigDict(from_attributes=True)` 사용 (Pydantic v2)
- Response 스키마에서 `password` 등 민감 정보 노출 금지
- Update 스키마의 모든 필드는 `Optional`

---

## 6. Inversion of Control & Dependency Injection

DB 세션 → Repository → Service 로 이어지는 전체 DI 체인을 `dependencies/{domain}.py`에 정의한다.

```python
# src/dependencies/user.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_async_db          # core에서 import
from src.repositories.user_repository import UserRepository
from src.repositories.protocols.user_repository import UserRepositoryProtocol
from src.services.user_service import UserService

def get_user_repository(
    db: AsyncSession = Depends(get_async_db),
) -> UserRepositoryProtocol:                        # Protocol 타입으로 반환
    return UserRepository(db)

def get_user_service(
    user_repository: UserRepositoryProtocol = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)
```

- `get_async_db`는 항상 `src/core/database.py`에서만 가져온다
- 반환 타입은 Protocol로 선언해 구현체 교체를 타입 수준에서 보장한다
- 서비스/레포지토리 클래스는 생성자 파라미터로만 의존성을 받는다 (전역 상태 금지)

---

## 7. 비동기 처리

- DB I/O: `AsyncSession` + `async/await` 필수 (동기 `Session` 사용 금지)
- 외부 HTTP 호출: `httpx.AsyncClient` 사용 (`requests` 금지)
- CPU-bound 작업: `asyncio.run_in_executor()` 사용
- `asyncio.sleep()` 외의 blocking sleep 금지

---

## 8. 환경변수 관리 (direnv + pydantic-settings)

### 동작 원리

direnv는 `.envrc`를 읽어 변수를 **셸 환경(`os.environ`)에 올린다.**
pydantic-settings는 인스턴스 생성 시 `os.environ`을 자동으로 읽으므로,
**`env_file` 설정 없이도 모든 환경변수를 정상적으로 가져온다.**

`env_file=".env"`를 함께 쓰면 안 되는 이유:
- `.envrc`는 `export KEY="value"` 포맷, `.env`는 `KEY=value` 포맷 — 혼용 시 포맷 불일치
- direnv가 이미 `os.environ`에 올린 값을 `.env`가 덮어쓸 수 있어 우선순위 혼란 발생
- 두 파일을 이중으로 관리하게 되어 유지보수 부담 증가

```
우선순위 (높음 → 낮음)
1. os.environ   ← direnv가 .envrc를 읽어 여기에 올려줌  ✅ 이것만 사용
2. env_file     ← .env 파일 직접 파싱                   ❌ 사용 금지
3. field default
```

### config.py

```python
# src/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # DB
    DATABASE_URL: str                 # postgresql+asyncpg://user:pass@host:5432/dbname
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # App
    SECRET_KEY: str
    DEBUG: bool = False
    ALLOWED_ORIGINS: list[str] = []

    model_config = SettingsConfigDict(
        # env_file 미설정 — direnv가 os.environ에 올린 값을 그대로 읽음
        case_sensitive=True,
    )

settings = Settings()
```

### .envrc.example

```bash
# .envrc.example — 실제 값 없이 키만 나열, 이 파일만 git에 커밋
# 사용법: cp .envrc.example .envrc → 값 채운 후 direnv allow

export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/dbname"
export DATABASE_POOL_SIZE="10"
export DATABASE_MAX_OVERFLOW="20"
export SECRET_KEY=""
export DEBUG="false"
export ALLOWED_ORIGINS=""
```

### 규칙

- 하드코딩된 시크릿/URL 절대 금지
- `.envrc`는 `.gitignore`에 추가, `.envrc.example`만 커밋
- `.env` 파일 생성 및 `env_file` 설정 금지 (direnv와 혼용 금지)
- 새 환경변수 추가 시 `Settings` 클래스와 `.envrc.example` 동시 업데이트
- 환경별 분기 값은 `constants/` 파일에서 `settings`를 참조하여 처리

---

## 9. 선언적 코딩 우선

SQLAlchemy 쿼리, 리스트 처리 등에서 선언적 스타일을 우선 사용한다.
선언적으로 작성했음에도 50줄이 넘는 경우, 분리 가능한 부분을 별도 함수로 추출한다.

```python
# ❌ 명령형
async def get_recent_active_emails(db: AsyncSession) -> list[str]:
    emails = []
    rows = await db.execute(select(User))
    for user in rows.scalars():
        if user.is_active and user.created_at > cutoff:
            emails.append(user.email)
    return emails

# ✅ 선언적
async def get_recent_active_emails(db: AsyncSession) -> list[str]:
    result = await db.execute(
        select(User.email)
        .where(User.is_active == True, User.created_at > cutoff)
        .order_by(User.created_at.desc())
    )
    return list(result.scalars().all())
```

---

## 10. 가독성

모듈화와 명시적 코딩을 배합하여 엔드포인트 코드가 "영어 문장처럼 읽히도록" 작성한다.
복잡한 조건은 변수명으로 의도를 드러낸다.

```python
# ❌
if user and user.is_active and not user.is_deleted and user.role in ("admin", "member"):
    ...

# ✅
is_valid_user = user and user.is_active and not user.is_deleted
has_required_role = user.role in (UserRole.ADMIN, UserRole.MEMBER)
if is_valid_user and has_required_role:
    ...
```

---

## 11. 유틸 (`utils/`)

### logger

```python
# src/utils/logger.py
import logging
import sys

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

# 사용처
logger = get_logger(__name__)
logger.info("유저 생성 완료: user_id=%s", user.id)
```

- `print()` 사용 금지, 반드시 `logger` 사용
- 민감 정보(비밀번호, 토큰) 로그 출력 금지

### HTTP 클라이언트

```python
# src/utils/http_client.py
import httpx

class AsyncHTTPClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def get(self, path: str, **kwargs) -> httpx.Response:
        response = await self._client.get(path, **kwargs)
        response.raise_for_status()
        return response

    async def aclose(self) -> None:
        await self._client.aclose()
```

---

## 12. 린터 설정 (`ruff.toml`)

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "N",    # pep8-naming
    "ASYNC",# flake8-async (async 함수 내 blocking call 감지)
]
ignore = ["E501"]   # line-length는 formatter에 위임

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

---

## 13. 테스트 DI Override 패턴

QA-BE Agent는 아래 패턴으로 DB 세션을 override한다.

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.main import app
from src.core.database import get_async_db          # core에서 import
from src.models.base import Base

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/test_db"

@pytest.fixture(scope="session")
async def engine():
    _engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield _engine
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await _engine.dispose()

@pytest.fixture
async def db_session(engine):
    SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with SessionFactory() as session:
        yield session
        await session.rollback()   # 테스트 격리: 각 테스트 후 롤백

@pytest.fixture
async def client(db_session: AsyncSession):
    async def override_get_async_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_async_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

**서비스 단위 테스트** — Repository를 `AsyncMock`으로 교체:

```python
# tests/services/test_user_service.py
from unittest.mock import AsyncMock
from src.services.user_service import UserService
from src.services.exceptions.user_exceptions import UserNotFoundException

async def test_get_user_raises_when_not_found():
    # Given
    mock_repo = AsyncMock()
    mock_repo.find_by_id.return_value = None
    service = UserService(mock_repo)

    # When / Then
    with pytest.raises(UserNotFoundException):
        await service.get_user(user_id=999)
```

- `app.dependency_overrides[get_async_db]`로 실제 세션을 테스트 세션으로 교체
- 각 테스트는 트랜잭션 롤백으로 격리 (`scope="function"`)
- 서비스 단위 테스트는 실제 DB 없이 `AsyncMock`만으로 실행 가능해야 함

---

## 14. 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 파일명 | snake_case | `user_service.py` |
| 클래스명 | PascalCase | `UserService` |
| 함수/변수 | snake_case | `get_user_by_id` |
| 상수 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| API 경로 | kebab-case | `/api/v1/user-profiles` |
| DB 테이블명 | snake_case 복수형 | `users`, `user_profiles` |
| DB 컬럼명 | snake_case | `created_at`, `is_active` |
| Protocol 파일 | `{domain}_repository.py` | `user_repository.py` |
| 예외 파일 | `{domain}_exceptions.py` | `user_exceptions.py` |

---

## 15. 금지 사항 (전체 요약)

| 금지 항목 | 대안 |
|-----------|------|
| `print()` | `logger.info()` |
| `from module import *` | 명시적 import |
| `HTTPException` 직접 raise | `BaseCustomException` 상속 예외 |
| `requests` 라이브러리 | `httpx.AsyncClient` |
| 동기 `Session` | `AsyncSession` |
| `Column()` 구문 (SQLAlchemy 레거시) | `Mapped[T]` + `mapped_column()` |
| Repository 내 `commit()` | `get_async_db()`에서 일괄 처리 |
| 엔드포인트에서 `AsyncSession` 직접 주입 | `get_{domain}_service` 통해 주입 |
| `core/exceptions.py`에 도메인 예외 정의 | `services/exceptions/{domain}_exceptions.py` |
| `dependencies/`에서 `get_async_db` 정의 | `core/database.py`에서 정의, `dependencies/`에서 import |
| Service가 Repository 구현체 타입 직접 참조 | Protocol 타입으로 선언 |
| `any` 타입 남용 | 명시적 타입 + 필요 시 주석으로 이유 명시 |
| 50줄 초과 단일 함수 | 분리 후 의미 있는 이름 부여 |
| 하드코딩 시크릿/URL | `settings` 객체 참조 |
| `.env` 파일 + `env_file` 설정 | direnv + `.envrc`로 통일 |