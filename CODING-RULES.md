# 코딩 규칙 - Multi-Agent Coding Team

> 이 문서는 Multi-Agent Coding Team 시스템 자체를 개발할 때 에이전트(Coding Agent, QA Agent)가 반드시 따라야 하는 모든 코딩 규칙을 통합한 문서입니다.
>
> 프로젝트별 상세 규칙은 `team/.rules/` 디렉토리를 참조하세요.

---

## 목차

1. [범용 코딩 원칙](#1-범용-코딩-원칙)
2. [백엔드 (FastAPI / Python / PostgreSQL)](#2-백엔드-fastapi--python--postgresql)
3. [프론트엔드 (Next.js / React / TypeScript)](#3-프론트엔드-nextjs--react--typescript)

---

## 1. 범용 코딩 원칙

### 1.1. DRY (Don't Repeat Yourself)

**원칙**: 코드 중복을 피하고, 반복되는 로직은 함수, 클래스, 또는 모듈로 추출합니다.

```python
# ❌ 나쁜 예
def calculate_user_total(user):
    return user.amount * 1.1

def calculate_admin_total(admin):
    return admin.amount * 1.1

# ✅ 좋은 예
def calculate_total_with_tax(entity):
    return entity.amount * 1.1
```

### 1.2. KISS (Keep It Simple, Stupid)

**원칙**: 복잡한 해결책보다 간단한 해결책을 선호합니다. 과도한 엔지니어링을 피합니다.

```python
# ❌ 지나치게 복잡
def is_valid(user):
    return all([
        hasattr(user, 'email') and bool(user.email),
        hasattr(user, 'name') and bool(user.name),
        hasattr(user, 'age') and isinstance(user.age, int) and user.age > 0
    ])

# ✅ 간단하고 읽기 쉬움
def is_valid(user):
    return user.email and user.name and user.age > 0
```

### 1.3. YAGNI (You Aren't Gonna Need It)

**원칙**: 실제로 필요할 때까지 기능을 추가하지 않습니다.

```python
# ❌ 미래를 위한 과도한 준비
class User:
    def __init__(self):
        self.cache = {}
        self.backup_cache = {}
        self.tertiary_cache = {}  # 과연 캐시 3개가 필요할까?

# ✅ 현재 필요한 것만 구현
class User:
    def __init__(self):
        self.cache = {}
```

### 1.4. SOLID 원칙

#### 단일 책임 원칙 (SRP)
클래스/함수는 하나의, 단 하나의 변경 이유만 가져야 합니다.

```python
# ❌ 여러 책임
class UserManager:
    def create_user(self, data): ...
    def send_welcome_email(self, user): ...
    def log_to_file(self, message): ...

# ✅ 단일 책임
class UserService:
    def create_user(self, data): ...

class EmailService:
    def send_welcome_email(self, user): ...

class Logger:
    def log(self, message): ...
```

#### 개방-폐쇄 원칙 (OCP)
확장에는 열려 있고, 수정에는 닫혀 있어야 합니다.

```python
# ✅ Protocol을 사용한 확장 가능성
from typing import Protocol

class PaymentProcessor(Protocol):
    def process(self, amount: float) -> bool: ...

class CreditCardProcessor:
    def process(self, amount: float) -> bool:
        # 신용카드 로직
        return True

class PayPalProcessor:
    def process(self, amount: float) -> bool:
        # PayPal 로직
        return True
```

### 1.5. 함수 크기 제한

**규칙**: 50줄을 초과하는 함수는 더 작은 함수로 분리해야 합니다.

```python
# ❌ 너무 김
def process_order(order):
    # 100줄의 코드...
    pass

# ✅ 작은 함수로 분리
def validate_order(order): ...
def calculate_total(order): ...
def apply_discount(order): ...
def process_payment(order): ...

def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    total = apply_discount(order)
    process_payment(order)
```

### 1.6. 에러 핸들링

**규칙**: 모든 예외는 명시적으로 처리해야 합니다. 조용한 실패는 금지입니다.

```python
# ❌ 조용한 실패
try:
    result = risky_operation()
except:
    pass

# ✅ 명시적 처리
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"잘못된 값: {e}")
    raise
except Exception as e:
    logger.error(f"예상치 못한 에러: {e}")
    raise
```

### 1.7. 로깅

**규칙**: logger를 사용하고, 절대 `print()`를 사용하지 않습니다.

```python
# ❌ 절대 사용 금지
print("사용자 생성됨")

# ✅ logger 사용
import logging
logger = logging.getLogger(__name__)
logger.info("사용자 생성됨: user_id=%s", user.id)
```

**로깅 레벨**:
- `DEBUG`: 상세한 진단 정보
- `INFO`: 일반 정보성 메시지
- `WARNING`: 경고 메시지
- `ERROR`: 에러 메시지
- `CRITICAL`: 치명적인 에러

**민감 정보 로깅 금지** (비밀번호, 토큰, API 키).

### 1.8. 보안 기본 원칙

#### 시크릿 하드코딩 금지
```python
# ❌ 절대 금지
API_KEY = "sk-1234567890abcdef"

# ✅ 환경 변수 사용
import os
API_KEY = os.getenv("API_KEY")
```

#### 모든 입력 검증
```python
# ✅ 항상 검증
def create_user(email: str, age: int):
    if not email or "@" not in email:
        raise ValueError("잘못된 이메일")
    if age < 0 or age > 150:
        raise ValueError("잘못된 나이")
    # 진행...
```

### 1.9. 테스팅 전략

#### 유닛 테스트
개별 함수/메서드를 독립적으로 테스트합니다.

```python
# tests/test_user_service.py
async def test_create_user():
    mock_repo = AsyncMock()
    service = UserService(mock_repo)

    user = await service.create_user({"email": "test@example.com"})

    assert user.email == "test@example.com"
    mock_repo.create.assert_called_once()
```

#### 통합 테스트
컴포넌트 간 상호작용을 테스트합니다.

```python
# tests/api/test_users.py
async def test_create_user_endpoint(client):
    response = await client.post("/api/users", json={"email": "test@example.com"})

    assert response.status_code == 201
    assert response.json()["data"]["email"] == "test@example.com"
```

### 1.10. Git 커밋 컨벤션

**형식**: `<type>: <설명>`

**타입**:
- `feat`: 새 기능
- `fix`: 버그 수정
- `refactor`: 코드 리팩토링
- `docs`: 문서 변경
- `test`: 테스트 추가/변경
- `chore`: 빌드/도구 변경

**예시**:
```bash
feat: 사용자 프로필 엔드포인트 추가
fix: 결제 처리에서 null pointer 해결
refactor: 이메일 검증을 유틸리티로 추출
docs: /users 엔드포인트 API 문서 업데이트
test: 인증 통합 테스트 추가
chore: 의존성 업데이트
```

### 1.11. 코드 리뷰 체크리스트

코드 제출 전:

- [ ] 모든 테스트 통과
- [ ] `print()` 문 없음
- [ ] 하드코딩된 시크릿 없음
- [ ] 에러 핸들링 추가됨
- [ ] 로깅 추가됨
- [ ] 타입 힌트 추가됨 (Python)
- [ ] Docstring 추가됨
- [ ] 코드 중복 없음
- [ ] 함수 크기 < 50줄
- [ ] 보안 고려사항 처리됨

---

## 2. 백엔드 (FastAPI / Python / PostgreSQL)

### 2.1. 프로젝트 구조

```
be-project/
├── src/
│   ├── main.py                   # FastAPI 앱 엔트리포인트
│   ├── core/
│   │   ├── config.py             # pydantic-settings 기반 환경변수 로드
│   │   ├── database.py           # 엔진, 세션팩토리, get_async_db()
│   │   └── exceptions.py         # BaseCustomException + 핸들러
│   ├── api/
│   │   └── v1/
│   │       ├── router.py         # 라우터 통합
│   │       ├── swaggers/         # Swagger 응답 정의
│   │       └── endpoints/        # 엔드포인트 파일 (users.py, items.py)
│   ├── models/                   # SQLAlchemy ORM 모델
│   ├── schemas/                  # Pydantic 스키마 (Request/Response)
│   ├── services/                 # 비즈니스 로직
│   │   └── exceptions/           # 도메인별 예외
│   ├── repositories/             # DB 쿼리 레이어
│   │   └── protocols/            # Repository 인터페이스 (Protocol)
│   ├── dependencies/             # DI 팩토리 함수
│   ├── constants/                # 도메인 상수/Enum
│   ├── middleware/               # 횡단 관심사 미들웨어
│   └── utils/                    # 재사용 유틸리티
│       └── logger.py
├── tests/
│   ├── conftest.py               # pytest fixtures
│   ├── api/v1/
│   ├── services/
│   └── repositories/
├── alembic/                      # DB 마이그레이션
├── ruff.toml                     # 린터 설정
└── .envrc.example                # direnv 환경변수
```

### 2.2. 레이어 책임

| 레이어 | 역할 | 금지 사항 |
|-------|------|-----------|
| `endpoints/` | HTTP 요청/응답 처리 | 비즈니스 로직 직접 작성 금지 |
| `services/` | 비즈니스 로직 | DB 쿼리 직접 작성 금지 |
| `repositories/` | DB 쿼리 (AsyncSession) | 비즈니스 로직 금지 |
| `schemas/` | 입출력 데이터 검증 | ORM 모델 직접 노출 금지 |
| `dependencies/` | DI 팩토리 함수 | 비즈니스/쿼리 로직 금지 |
| `core/` | 인프라 설정 | 도메인 로직 금지 |

### 2.3. 데이터베이스 설정

#### 드라이버 스택
| 목적 | 라이브러리 |
|------|-----------|
| 비동기 드라이버 | `asyncpg` |
| ORM | `sqlalchemy[asyncio]` (`AsyncSession`, `async_sessionmaker`) |
| 마이그레이션 | `alembic` (동기 커넥션으로 실행) |

#### 엔진 및 세션 팩토리 (`src/core/database.py`)

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

#### ORM 모델 Base

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

#### ORM 모델 작성 규칙

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

**규칙**:
- `Mapped[T]` + `mapped_column()` 사용 필수 (SQLAlchemy 2.x 스타일)
- **절대** `Column()` 구문 사용 금지 (레거시)
- 모든 컬럼에 `nullable` 명시
- 자주 조회되는 필드에 `index=True`

### 2.4. Repository 패턴 with Protocol

#### Protocol 정의 (인터페이스)

**구현체 작성 전에 반드시 Protocol을 먼저 정의**합니다.
Service는 Protocol 타입에만 의존하고, 구체 클래스를 직접 참조하지 않습니다.
이를 통해 OCP(구현 변경에 닫힘)와 LSP(구현체 교체 가능)를 타입 수준에서 보장합니다.

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

#### Repository 구현체

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
        await self._db.flush()     # ID 확보 (commit은 get_async_db에서 처리)
        await self._db.refresh(user)
        return user
```

**규칙**:
- **절대** `self._db.commit()` 직접 호출 금지 — commit은 `get_async_db()`에서 일괄 처리
- `flush()`는 ID 선확보 등 필요 시 허용
- N+1 문제가 예상되는 관계는 `selectinload` / `joinedload` 명시

### 2.5. 멀티 Repository 트랜잭션 (Unit of Work)

**하나의 비즈니스 로직에서 여러 Repository를 사용할 때는 반드시 같은 `AsyncSession`을 공유해야 합니다.**
DI 팩토리에서 동일한 `db` 인스턴스를 각 Repository에 주입하는 방식으로 처리합니다.

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
# src/services/order_service.py — 트랜잭션 원자성 자동 보장
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

**규칙**:
- Service 생성자는 Protocol 타입으로 선언 (구현체 직접 참조 금지)
- 트랜잭션 경계는 항상 `get_async_db()`가 관리 — Service에서 commit/rollback 금지

### 2.6. FastAPI 작성 규칙

#### 라우터

```python
# ✅ APIRouter 사용, prefix와 tags 명시
router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/{user_id}",
    response_model=BaseResponse[UserResponse],
    status_code=200,
    responses=GET_USER_RESPONSES,   # swaggers/ 에서 가져온 명세
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> BaseResponse[UserResponse]:
    return await service.get_user(user_id)
```

#### 의존성 주입 규칙

- 서비스는 반드시 `Depends(get_{domain}_service)`로 주입
- DB 세션(`get_async_db`)은 `core/database.py`에 정의, `dependencies/`에서 import하여 사용
- 엔드포인트에서 `AsyncSession`을 직접 주입받는 것 금지
- 엔드포인트에서 Repository를 직접 주입받는 것 금지

```
엔드포인트 → get_{domain}_service → get_{domain}_repository → get_async_db
(엔드포인트는 서비스만 알고, 그 아래 체인은 DI가 해결)
```

#### 응답 형식 통일

모든 API 응답은 `BaseResponse[T]`를 사용합니다:

```python
# 성공
{"success": true, "data": {...}, "error": null}

# 실패
{"success": false, "data": null, "error": {"code": "USER_NOT_FOUND", "message": "..."}}
```

#### 예외 구조

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
# src/main.py — 핸들러 등록 필수
from src.core.exceptions import BaseCustomException, custom_exception_handler

app = FastAPI()
app.add_exception_handler(BaseCustomException, custom_exception_handler)
```

**규칙**:
- `HTTPException` 직접 사용 금지
- 새 도메인 추가 시 `services/exceptions/{domain}_exceptions.py` 파일 신규 생성

### 2.7. Pydantic 스키마 규칙

#### BaseResponse (모든 응답에 필수 적용)

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

#### 도메인 스키마 패턴

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

**규칙**:
- `orm_mode` 사용 금지 → `ConfigDict(from_attributes=True)` 사용 (Pydantic v2)
- Response 스키마에서 `password` 등 민감 정보 노출 금지
- Update 스키마의 모든 필드는 `Optional`

### 2.8. 환경변수 관리 (direnv + pydantic-settings)

#### 동작 원리

direnv는 `.envrc`를 읽어 변수를 **셸 환경(`os.environ`)에 올립니다.**
pydantic-settings는 인스턴스 생성 시 `os.environ`을 자동으로 읽으므로,
**`env_file` 설정 없이도 모든 환경변수를 정상적으로 가져옵니다.**

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

#### config.py

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

#### .envrc.example

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

**규칙**:
- 하드코딩된 시크릿/URL 절대 금지
- `.envrc`는 `.gitignore`에 추가, `.envrc.example`만 커밋
- `.env` 파일 생성 및 `env_file` 설정 금지 (direnv와 혼용 금지)
- 새 환경변수 추가 시 `Settings` 클래스와 `.envrc.example` 동시 업데이트

### 2.9. 선언적 코딩 우선

SQLAlchemy 쿼리, 리스트 처리 등에서 선언적 스타일을 우선 사용합니다.

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

### 2.10. 백엔드 네이밍 컨벤션

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

### 2.11. 백엔드 금지 사항

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

---

## 3. 프론트엔드 (Next.js / React / TypeScript)

### 3.1. 프로젝트 구조

```
fe-project/
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── layout.tsx              # 루트 레이아웃 (폰트, 전역 프로바이더)
│   │   ├── page.tsx
│   │   ├── loading.tsx             # 루트 Suspense 폴백
│   │   ├── not-found.tsx           # 404 페이지
│   │   ├── error.tsx               # 루트 에러 바운더리 (Client Component)
│   │   ├── global-error.tsx        # 크래시 수준 에러 바운더리
│   │   ├── providers.tsx           # 전역 Client Provider 모음 ('use client')
│   │   └── (routes)/               # 라우트 그룹 — 도메인별 폴더
│   │       └── {domain}/
│   │           ├── page.tsx
│   │           ├── loading.tsx
│   │           ├── error.tsx
│   │           └── _components/    # 라우트 로컬 컴포넌트 (공유 불가)
│   ├── components/
│   │   ├── ui/                     # 재사용 원자 컴포넌트 (Button, Input 등)
│   │   └── features/               # 도메인별 복합 컴포넌트
│   ├── hooks/                      # 커스텀 훅
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts           # 기본 fetch 래퍼
│   │   │   └── {domain}.ts         # 도메인별 API 함수
│   │   └── utils/                  # 순수 유틸 함수
│   ├── stores/                     # Zustand 스토어 (클라이언트 전역 상태 전용)
│   ├── types/
│   │   └── api/                    # API 응답 타입 (BE 스키마 미러링)
│   ├── constants/                  # 앱 전역 상수 및 Enum
│   ├── styles/                     # 전역 스타일
│   └── middleware.ts               # Edge 미들웨어 (인증, 리다이렉트 등)
├── public/
├── tests/
│   ├── components/
│   └── hooks/
├── next.config.ts
├── tsconfig.json
└── .env.example                    # 필요한 환경변수 키만 나열 (값 없음)
```

### 3.2. TanStack Query 설정

#### QueryClient Provider (필수 초기 설정)

`layout.tsx`는 Server Component이므로 `QueryClientProvider`를 직접 넣을 수 없습니다.
반드시 별도 `providers.tsx`를 만들어 분리합니다.

```tsx
// src/app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function AppProviders({ children }: { children: React.ReactNode }) {
  // useState로 감싸야 컴포넌트당 한 번만 생성됨
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 1000 * 60,       // 전역 기본 staleTime: 1분
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

```tsx
// src/app/layout.tsx — Server Component 유지
import { AppProviders } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
```

#### 데이터 페칭 전략 선택 기준

| 데이터 유형 | 패턴 | 위치 |
|------------|------|------|
| 거의 변하지 않음, SEO 중요 | `fetch` + `cache: 'force-cache'` (SSG) | Server Component |
| 주기적으로 변함 (분~시간 단위) | `fetch` + `next: { revalidate: N }` (ISR) | Server Component |
| 매 요청마다 변함, 인증 의존 | `fetch` + `cache: 'no-store'` (SSR) | Server Component |
| 실시간, 사용자 트리거, 네비게이션 후 갱신 | TanStack Query | Client Component |

### 3.3. 컴포넌트 작성 규칙

#### 기본 형식

```tsx
// ✅ named export + Props 인터페이스 분리
'use client';

interface UserCardProps {
  userId: number;
  variant?: 'compact' | 'full';
}

export function UserCard({ userId, variant = 'full' }: UserCardProps) {
  const { data: user, isLoading } = useUser(userId);

  if (isLoading) return <UserCardSkeleton />;
  if (!user) return null;

  return <div className={cn(userCardVariants({ variant }))}>{user.name}</div>;
}
```

#### Server Component vs Client Component

- 기본은 **Server Component** — 꼭 필요한 경우에만 `'use client'` 선언
- `'use client'`가 필요한 경우: 이벤트 핸들러, `useState`, `useEffect`, 브라우저 API, TanStack Query 훅
- `'use client'`는 트리의 최하단으로 밀어낼 것

### 3.4. 선언적 코딩 우선

#### 조건부 렌더링

```tsx
// ❌ 명령형
function UserStatus({ user }: { user: User }) {
  let badge;
  if (user.role === 'admin') {
    badge = <AdminBadge />;
  } else if (user.isActive) {
    badge = <ActiveBadge />;
  } else {
    badge = <InactiveBadge />;
  }
  return <div>{badge}</div>;
}

// ✅ 선언적
const statusBadgeMap: Record<string, React.ComponentType> = {
  admin: AdminBadge,
  active: ActiveBadge,
  inactive: InactiveBadge,
};

function UserStatus({ user }: { user: User }) {
  const key = user.role === 'admin' ? 'admin' : user.isActive ? 'active' : 'inactive';
  const Badge = statusBadgeMap[key];
  return <div><Badge /></div>;
}
```

### 3.5. TypeScript 규칙

- `tsconfig.json`에 `strict: true` 필수
- `any` 타입 사용 금지
- `// @ts-ignore` 사용 금지 — `// @ts-expect-error` + 이유 주석 허용
- 모든 컴포넌트 Props에 타입 명시 필수

### 3.6. 프론트엔드 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 컴포넌트 파일 | PascalCase | `UserCard.tsx` |
| 훅 파일 | camelCase, `use` 접두사 | `useUserProfile.ts` |
| 유틸 파일 | camelCase | `formatDate.ts` |
| 스토어 파일 | camelCase, `Store` 접미사 | `authStore.ts` |
| 타입/인터페이스 | PascalCase | `UserProfile` |
| 상수 | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |

### 3.7. 프론트엔드 금지 사항

| 금지 항목 | 대안 |
|-----------|------|
| 커밋된 코드에 `console.log()` | 커밋 전 제거 또는 logger 유틸 사용 |
| `// @ts-ignore` | `// @ts-expect-error` + 이유 주석 |
| `any` 타입 | 명시적 타입 |
| `default export` | named export (Next.js 페이지/레이아웃 제외) |
| `useEffect` 내 API 호출 | TanStack Query (`useQuery` / `useMutation`) |
| 하드코딩된 API URL | `env` 상수를 통한 환경변수 |
| `<img>` 태그 | `next/image` |
| `<link>` / `@import` 폰트 로드 | `next/font` |
| `style={{ ... }}` | Tailwind 클래스 |
| Zustand에 서버 상태 저장 | TanStack Query |

---

## 요약

이 문서는 다음을 통합합니다:
1. **범용 코딩 원칙** — DRY, KISS, YAGNI, SOLID, 에러 핸들링, 로깅, 보안, 테스팅
2. **백엔드 규칙** — FastAPI, Python, PostgreSQL, SQLAlchemy, Repository 패턴, DI, Pydantic
3. **프론트엔드 규칙** — Next.js, React, TypeScript, TanStack Query, Server/Client 컴포넌트, 폼

**프로젝트별 상세 규칙은 다음을 참조하세요:**
- `team/.rules/general-coding-rules.md`
- `team/.rules/_verified/web-fullstack/backend-fastapi-python.md`
- `team/.rules/_verified/web-fullstack/frontend-nextjs-typescript.md`

**코드 품질, 일관성, 시스템 안정성을 유지하기 위해 이 규칙들을 엄격히 따르세요.**
