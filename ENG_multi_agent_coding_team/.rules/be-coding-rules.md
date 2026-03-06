# Backend Coding Rules (FastAPI / Python / PostgreSQL)

> This file defines the coding rules that BE Coding Agent and QA-BE Agent must strictly follow.

---

## 1. Project Structure

```
be-project/
├── src/
│   ├── main.py                   # FastAPI app entrypoint: router/middleware/exception handler registration
│   ├── core/
│   │   ├── config.py             # Environment variable loading via pydantic-settings
│   │   ├── database.py           # Engine, session factory, get_async_db() — infra only
│   │   └── exceptions.py         # BaseCustomException + custom_exception_handler only
│   ├── api/
│   │   └── v1/
│   │       ├── router.py         # Aggregate all routers (include_router)
│   │       ├── swaggers/         # Swagger responses objects per endpoint
│   │       │                     # (reference Pydantic models from schemas/)
│   │       └── endpoints/        # One file per domain (e.g. users.py, items.py)
│   ├── models/                   # SQLAlchemy ORM models (inherit DeclarativeBase)
│   ├── schemas/                  # Pydantic schemas (Request / Response / Base)
│   ├── services/                 # Business logic
│   │   └── exceptions/           # Domain-specific exceptions (e.g. user_exceptions.py)
│   ├── repositories/             # DB query layer (direct AsyncSession usage)
│   │   └── protocols/            # Repository interfaces (Protocol definitions)
│   ├── dependencies/             # DI factory functions (one file per domain)
│   │   └── user.py               # get_user_repository(), get_user_service()
│   ├── constants/                # Domain constants / Enums / env-specific values
│   ├── middleware/               # Cross-cutting concerns (Request ID, logging, etc.)
│   └── utils/                    # Reusable utilities (HTTP client wrapper, logger, etc.)
│       └── logger.py
│
├── tests/
│   ├── conftest.py               # pytest fixtures (TestClient, DB override, etc.)
│   ├── api/v1/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── dependencies/
│
├── alembic/                      # DB migrations
│   └── versions/
├── ruff.toml                     # Linter config (see section below)
└── .envrc.example                # direnv-based environment variable template
```

---

## 2. Layer Responsibilities (Required)

| Layer | Responsibility | Prohibited |
|-------|---------------|------------|
| `endpoints/` | HTTP request/response handling, routing | Writing business logic directly |
| `services/` | Business logic | Writing DB queries directly |
| `repositories/` | DB queries (direct `AsyncSession` usage) | Business logic |
| `schemas/` | Input/output data validation | Exposing ORM models directly |
| `dependencies/` | DI factory functions | Business/query logic |
| `core/` | Infrastructure config (DB, env vars, base exceptions) | Domain logic |

---

## 3. DB Setup (PostgreSQL + Async SQLAlchemy)

### 3-1. Drivers

| Purpose | Library |
|---------|---------|
| Async driver | `asyncpg` |
| ORM | `sqlalchemy[asyncio]` (`AsyncSession`, `async_sessionmaker`) |
| Migrations | `alembic` (runs separately with a sync connection) |

### 3-2. Engine and Session Factory (`src/core/database.py`)

All DB infrastructure config must be defined **exclusively in `src/core/database.py`**.
`dependencies/` imports `get_async_db` from this file.

```python
# src/core/database.py
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,           # postgresql+asyncpg://...
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,              # Automatically detect broken connections
    echo=settings.DEBUG,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,          # Prevent lazy-load errors after await
    autoflush=False,
    autocommit=False,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a per-request AsyncSession.
    Commits on normal exit, rolls back and re-raises on exception.
    Do not import directly — always inject through dependencies/.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 3-3. ORM Model Base

```python
# src/models/base.py
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    """Auto-managed created/updated timestamps. Recommended for all tables."""
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

### 3-4. ORM Model Rules

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

- Always use `Mapped[T]` + `mapped_column()` (SQLAlchemy 2.x style)
- `Column()` syntax is prohibited (legacy)
- Always specify `nullable` on every column
- Add `index=True` to frequently queried fields

### 3-5. Repository Protocol (Interface Definition)

Always **define the Protocol first** before writing the implementation.
Services depend only on the Protocol type, never on the concrete class directly.
This enforces OCP (closed to implementation changes) and LSP (substitutable implementations) at the type level.

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

### 3-6. Repository Implementation

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
        await self._db.flush()     # Obtain ID early (commit is handled by get_async_db)
        await self._db.refresh(user)
        return user
```

- Never call `self._db.commit()` directly — commit is handled by `get_async_db()`
- `flush()` is allowed when early ID retrieval is necessary
- Use `selectinload` / `joinedload` explicitly when N+1 is anticipated

### 3-7. Multi-Repository Transactions (Unit of Work)

**When multiple repositories are used within a single business operation, they must share the same `AsyncSession`.**
Inject the same `db` instance into each repository from the DI factory.

```python
# dependencies/order.py — inject the same session into both repositories
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_async_db
from src.repositories.order_repository import OrderRepository
from src.repositories.inventory_repository import InventoryRepository
from src.services.order_service import OrderService

def get_order_service(
    db: AsyncSession = Depends(get_async_db),
) -> OrderService:
    # Same db session → both operations belong to a single transaction
    return OrderService(
        order_repo=OrderRepository(db),
        inventory_repo=InventoryRepository(db),
    )
```

```python
# src/services/order_service.py — atomicity is guaranteed automatically
class OrderService:
    def __init__(
        self,
        order_repo: OrderRepositoryProtocol,
        inventory_repo: InventoryRepositoryProtocol,
    ) -> None:
        self._order_repo = order_repo
        self._inventory_repo = inventory_repo

    async def place_order(self, user_id: int, item_id: int, quantity: int) -> Order:
        # Both queries share the same session → if either raises, get_async_db() rolls back all
        await self._inventory_repo.decrease(item_id, quantity)
        return await self._order_repo.create(user_id, item_id, quantity)
```

- Service constructors must declare Protocol types (never reference concrete classes directly)
- Transaction boundaries are always managed by `get_async_db()` — Services must never commit or rollback

### 3-8. Alembic Migrations

- Migrations use a sync connection (`psycopg2` or `pg8000`) — Alembic requirement
- Always review the generated file after `alembic revision --autogenerate`
- When `__tablename__` changes, explicitly use `op.rename_table()` (autogenerate may incorrectly generate drop/create)

---

## 4. FastAPI Rules

### 4-1. Router

```python
# Use APIRouter with explicit prefix and tags
router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/{user_id}",
    response_model=BaseResponse[UserResponse],
    status_code=200,
    responses=GET_USER_RESPONSES,   # Swagger spec imported from swaggers/
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> BaseResponse[UserResponse]:
    return await service.get_user(user_id)
```

### 4-2. Dependency Injection Rules

- Services must always be injected via `Depends(get_{domain}_service)`
- `get_async_db` is defined in `core/database.py` and imported in `dependencies/`
- Endpoints must never receive `AsyncSession` directly
- Endpoints must never receive a Repository directly

```
endpoint → get_{domain}_service → get_{domain}_repository → get_async_db
(endpoints know only the service; the rest of the chain is resolved by DI)
```

### 4-3. Unified Response Format

All API responses must use `BaseResponse[T]` (see section 5):

```python
# Success
{"success": true, "data": {...}, "error": null}

# Failure
{"success": false, "data": null, "error": {"code": "USER_NOT_FOUND", "message": "..."}}
```

### 4-4. Exception Structure

**`core/exceptions.py`**: base class and handler only.
**`services/exceptions/`**: domain exceptions in separate files.

```python
# src/core/exceptions.py — base class + handler only
from fastapi import Request
from fastapi.responses import JSONResponse

class BaseCustomException(Exception):
    status_code: int = 500
    code: str = "INTERNAL_SERVER_ERROR"
    message: str = "An internal server error occurred."

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
# src/services/exceptions/user_exceptions.py — domain exceptions in their own file
from src.core.exceptions import BaseCustomException

class UserNotFoundException(BaseCustomException):
    status_code = 404
    code = "USER_NOT_FOUND"
    message = "The requested user was not found."

class UserAlreadyExistsException(BaseCustomException):
    status_code = 409
    code = "USER_ALREADY_EXISTS"
    message = "A user with that identifier already exists."
```

```python
# src/main.py — handler registration is required (without it, all custom exceptions return 500)
from src.core.exceptions import BaseCustomException, custom_exception_handler

app = FastAPI()
app.add_exception_handler(BaseCustomException, custom_exception_handler)
```

- Using `HTTPException` directly is prohibited
- When adding a new domain, create `services/exceptions/{domain}_exceptions.py`

### 4-5. Middleware (`middleware/`)

Handle cross-cutting concerns with middleware. Register via `add_middleware()` in `main.py`.

```python
# src/middleware/request_id.py — assign a unique ID to every request
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
# src/middleware/logging.py — common request/response logging
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

### 4-6. `swaggers/` Directory

Define Swagger `responses=` objects per domain, referencing Pydantic models from `schemas/`.

```python
# src/api/v1/swaggers/user.py
from src.schemas.user import UserResponse
from src.schemas.base import BaseResponse

GET_USER_RESPONSES: dict = {
    200: {"model": BaseResponse[UserResponse], "description": "User retrieved successfully"},
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {"code": "USER_NOT_FOUND", "message": "The requested user was not found."},
                }
            }
        },
    },
}
```

### 4-7. `constants/` Directory

Separate domain constants, Enums, and env-specific values into individual files.

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

## 5. Pydantic Schema Rules

### 5-1. BaseResponse (Required for All Responses)

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

### 5-2. Pagination Schema (Common for All List Endpoints)

All list endpoints that require pagination must use the schemas below.
Default to offset-based pagination; define cursor-based separately only for infinite scroll.

```python
# src/schemas/pagination.py
from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationQuery(BaseModel):
    """Common pagination query parameters."""
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    size: int = Field(default=20, ge=1, le=100, description="Page size")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size

class PaginatedData(BaseModel, Generic[T]):
    """Common pagination response structure."""
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
# Endpoint usage example
@router.get("/", response_model=BaseResponse[PaginatedData[UserResponse]])
async def list_users(
    query: Annotated[PaginationQuery, Query()],
    service: UserService = Depends(get_user_service),
) -> BaseResponse[PaginatedData[UserResponse]]:
    result = await service.list_users(query)
    return BaseResponse.ok(result)
```

### 5-3. Domain Schema Pattern

```python
# src/schemas/user.py — Base → Create/Update → Response pattern
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):           # All fields are Optional for partial updates
    name: str | None = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

- Never use `orm_mode` → use `ConfigDict(from_attributes=True)` (Pydantic v2)
- Never expose sensitive fields like `password` in Response schemas
- All fields in Update schemas must be `Optional`

---

## 6. Inversion of Control & Dependency Injection

Define the full DI chain (DB session → Repository → Service) in `dependencies/{domain}.py`.

```python
# src/dependencies/user.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_async_db          # always import from core
from src.repositories.user_repository import UserRepository
from src.repositories.protocols.user_repository import UserRepositoryProtocol
from src.services.user_service import UserService

def get_user_repository(
    db: AsyncSession = Depends(get_async_db),
) -> UserRepositoryProtocol:                        # return Protocol type, not concrete class
    return UserRepository(db)

def get_user_service(
    user_repository: UserRepositoryProtocol = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)
```

- `get_async_db` must always be imported from `src/core/database.py`
- Return types must be declared as Protocols to guarantee substitutability at the type level
- Services and repositories receive all dependencies only through constructor parameters (no global state)

---

## 7. Async Rules

- DB I/O: `AsyncSession` + `async/await` required (sync `Session` prohibited)
- External HTTP: use `httpx.AsyncClient` (`requests` library prohibited)
- CPU-bound work: use `asyncio.run_in_executor()`
- No blocking sleep — only `asyncio.sleep()` is allowed

---

## 8. Environment Variable Management (direnv + pydantic-settings)

### How It Works

direnv reads `.envrc` and exports variables into the **shell environment (`os.environ`)**.
pydantic-settings automatically reads `os.environ` on instantiation, so
**all environment variables are picked up without any `env_file` configuration.**

Why `env_file=".env"` must not be used alongside direnv:
- `.envrc` uses `export KEY="value"` format; `.env` uses `KEY=value` — mixing formats causes parsing issues
- `.env` can silently overwrite values already loaded by direnv into `os.environ`, causing priority confusion
- Maintaining two files for the same purpose increases maintenance burden

```
Priority (high → low)
1. os.environ   ← direnv loads .envrc here         ✅ use this only
2. env_file     ← direct .env file parsing         ❌ prohibited
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
        # env_file intentionally omitted — direnv already populated os.environ
        case_sensitive=True,
    )

settings = Settings()
```

### .envrc.example

```bash
# .envrc.example — keys only, no real values; this file is the only one committed to git
# Usage: cp .envrc.example .envrc → fill in values → direnv allow

export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/dbname"
export DATABASE_POOL_SIZE="10"
export DATABASE_MAX_OVERFLOW="20"
export SECRET_KEY=""
export DEBUG="false"
export ALLOWED_ORIGINS=""
```

### Rules

- Never hardcode secrets or URLs
- Add `.envrc` to `.gitignore`; commit only `.envrc.example`
- Never create a `.env` file or set `env_file` (prohibited when using direnv)
- When adding a new env var, update both `Settings` class and `.envrc.example` simultaneously
- Environment-specific branching values should be handled in `constants/` by referencing `settings`

---

## 9. Declarative Code First

Prefer declarative style for SQLAlchemy queries and list processing.
If a declarative implementation still exceeds 50 lines, extract separable parts into named functions.

```python
# ❌ Imperative
async def get_recent_active_emails(db: AsyncSession) -> list[str]:
    emails = []
    rows = await db.execute(select(User))
    for user in rows.scalars():
        if user.is_active and user.created_at > cutoff:
            emails.append(user.email)
    return emails

# ✅ Declarative
async def get_recent_active_emails(db: AsyncSession) -> list[str]:
    result = await db.execute(
        select(User.email)
        .where(User.is_active == True, User.created_at > cutoff)
        .order_by(User.created_at.desc())
    )
    return list(result.scalars().all())
```

---

## 10. Readability

Combine modularization and explicit naming so that endpoint code reads like an English sentence.
Express complex conditions through descriptive variable names.

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

## 11. Utils (`utils/`)

### Logger

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

# Usage
logger = get_logger(__name__)
logger.info("User created: user_id=%s", user.id)
```

- `print()` is prohibited — always use `logger`
- Never log sensitive data (passwords, tokens)

### HTTP Client

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

## 12. Linter Config (`ruff.toml`)

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
    "ASYNC",# flake8-async (detects blocking calls inside async functions)
]
ignore = ["E501"]   # line-length delegated to formatter

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

---

## 13. Test DI Override Pattern

QA-BE Agent overrides the DB session using the pattern below.

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.main import app
from src.core.database import get_async_db          # import from core
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
        await session.rollback()   # Isolate each test: rollback after every test

@pytest.fixture
async def client(db_session: AsyncSession):
    async def override_get_async_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_async_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

**Service unit tests** — replace Repository with `AsyncMock`:

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

- Use `app.dependency_overrides[get_async_db]` to swap the real session with a test session
- Each test is isolated via transaction rollback (`scope="function"`)
- Service unit tests must be runnable with `AsyncMock` alone, without a real DB

---

## 14. Naming Conventions

| Target | Rule | Example |
|--------|------|---------|
| File names | snake_case | `user_service.py` |
| Class names | PascalCase | `UserService` |
| Functions / variables | snake_case | `get_user_by_id` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| API paths | kebab-case | `/api/v1/user-profiles` |
| DB table names | snake_case, plural | `users`, `user_profiles` |
| DB column names | snake_case | `created_at`, `is_active` |
| Protocol files | `{domain}_repository.py` | `user_repository.py` |
| Exception files | `{domain}_exceptions.py` | `user_exceptions.py` |

---

## 15. Prohibited Patterns (Full Summary)

| Prohibited | Alternative |
|-----------|-------------|
| `print()` | `logger.info()` |
| `from module import *` | Explicit imports |
| Raising `HTTPException` directly | Raise exceptions that inherit `BaseCustomException` |
| `requests` library | `httpx.AsyncClient` |
| Sync `Session` | `AsyncSession` |
| `Column()` syntax (SQLAlchemy legacy) | `Mapped[T]` + `mapped_column()` |
| `commit()` inside a Repository | Handled exclusively by `get_async_db()` |
| Injecting `AsyncSession` directly into an endpoint | Inject via `get_{domain}_service` |
| Defining domain exceptions in `core/exceptions.py` | Use `services/exceptions/{domain}_exceptions.py` |
| Defining `get_async_db` in `dependencies/` | Define in `core/database.py`, import in `dependencies/` |
| Service referencing a Repository concrete class directly | Declare as Protocol type |
| Overusing `Any` type | Explicit types; add a comment if unavoidable |
| Single function exceeding 50 lines | Extract and give meaningful names |
| Hardcoded secrets or URLs | Reference `settings` object |
| `.env` file + `env_file` config | Use direnv + `.envrc` exclusively |