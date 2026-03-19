# Docs Generator Skill

> **목적**: 코드에서 문서 자동 생성
>
> **타입**: Documentation Skill
>
> **Thariq 교훈**: "Keep documentation in sync with code"

---

## 🎯 트리거

### 자동 트리거
- Auto-pipeline: Coding Agent 완료 후 (선택)
- Git hook: pre-commit (API 변경 시)
- CI/CD: PR에서 문서 업데이트

### 수동 트리거
```bash
# 전체 문서 생성
bash scripts/run-skill.sh docs-generator --all

# API 문서만
bash scripts/run-skill.sh docs-generator --api

# README 업데이트
bash scripts/run-skill.sh docs-generator --readme

# 특정 모듈
bash scripts/run-skill.sh docs-generator --module auth
```

---

## 🔍 기능

### 1. API 문서 자동 생성

**지원 포맷**:
- **OpenAPI/Swagger**: REST API
- **GraphQL Schema**: GraphQL API
- **JSDoc/TSDoc**: JavaScript/TypeScript
- **Sphinx/reStructuredText**: Python
- **GoDoc**: Go
- **RustDoc**: Rust

**예시 (OpenAPI)**:
```python
def generate_openapi_spec(routes):
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "My API",
            "version": "1.0.0"
        },
        "paths": {}
    }

    for route in routes:
        spec["paths"][route.path] = {
            route.method.lower(): {
                "summary": route.summary,
                "parameters": route.parameters,
                "responses": route.responses
            }
        }

    return spec
```

**코드에서 추출**:
```python
# 소스 코드
@app.post("/api/login")
async def login(email: str, password: str):
    """
    사용자 로그인

    Args:
        email: 사용자 이메일
        password: 비밀번호

    Returns:
        {"token": "jwt_token", "user": {...}}

    Raises:
        401: 잘못된 인증 정보
    """
    pass

# 자동 생성된 문서
"""
POST /api/login

사용자 로그인

Parameters:
  - email (string, required): 사용자 이메일
  - password (string, required): 비밀번호

Responses:
  - 200: {"token": "jwt_token", "user": {...}}
  - 401: 잘못된 인증 정보
"""
```

### 2. README 자동 업데이트

**섹션 자동 생성**:
```markdown
# My Project

> Auto-generated from code and git history

## Features

- ✅ User authentication (JWT)
- ✅ Profile management
- ✅ Search functionality
- 🚧 Payment integration (in progress)

## Installation

```bash
npm install
```

## API Endpoints

### Authentication

- `POST /api/login` - 사용자 로그인
- `POST /api/logout` - 로그아웃
- `POST /api/register` - 회원가입

### User

- `GET /api/user/me` - 현재 사용자 정보
- `PUT /api/user/me` - 프로필 업데이트

## Environment Variables

- `DATABASE_URL` - 데이터베이스 연결 URL (required)
- `JWT_SECRET` - JWT 서명 비밀키 (required)
- `API_KEY` - 외부 API 키 (optional)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

**자동 감지**:
```python
def update_readme():
    # 1. Features 추출
    features = extract_features_from_code()

    # 2. API 엔드포인트 추출
    endpoints = extract_endpoints()

    # 3. 환경 변수 추출
    env_vars = extract_env_vars_from_code()

    # 4. README 업데이트
    update_readme_sections({
        "Features": features,
        "API Endpoints": endpoints,
        "Environment Variables": env_vars
    })
```

### 3. Changelog 자동 생성

**Git 커밋에서 생성**:
```markdown
# Changelog

## [1.3.0] - 2026-03-19

### Added
- feat(PLAN-001): implement JWT authentication
- feat(PLAN-003): add user profile API

### Fixed
- fix(PLAN-002): resolve login validation error
- fix(PLAN-005): fix memory leak in session storage

### Changed
- refactor(PLAN-004): optimize database queries

## [1.2.0] - 2026-03-12

### Added
- feat: add search functionality
```

**생성 로직**:
```python
def generate_changelog(from_version, to_version):
    # 1. 커밋 로그 가져오기
    commits = git_log(f"{from_version}..{to_version}")

    # 2. 커밋 타입별 그룹화
    changelog = {
        "Added": [],
        "Fixed": [],
        "Changed": [],
        "Removed": []
    }

    for commit in commits:
        if commit.message.startswith("feat"):
            changelog["Added"].append(commit.message)
        elif commit.message.startswith("fix"):
            changelog["Fixed"].append(commit.message)
        elif commit.message.startswith("refactor"):
            changelog["Changed"].append(commit.message)

    return format_changelog(changelog, to_version)
```

### 4. 코드 주석 검증

**누락된 주석 감지**:
```python
def validate_docstrings(files):
    issues = []

    for file in files:
        functions = extract_functions(file)

        for func in functions:
            # 공개 함수는 docstring 필수
            if func.is_public and not func.has_docstring:
                issues.append({
                    "file": file,
                    "function": func.name,
                    "line": func.line,
                    "severity": "warning",
                    "message": "공개 함수에 docstring 없음"
                })

            # 복잡한 함수는 docstring 권장
            if func.complexity > 10 and not func.has_docstring:
                issues.append({
                    "file": file,
                    "function": func.name,
                    "line": func.line,
                    "severity": "info",
                    "message": "복잡한 함수에 docstring 권장"
                })

    return issues
```

### 5. 예제 코드 자동 생성

**API 사용 예제**:
```python
# API 정의
@app.post("/api/login")
async def login(email: str, password: str):
    pass

# 자동 생성된 예제
"""
### Example: User Login

```python
import requests

response = requests.post(
    "https://api.example.com/api/login",
    json={
        "email": "user@example.com",
        "password": "password123"
    }
)

if response.status_code == 200:
    token = response.json()["token"]
    print(f"Login successful: {token}")
else:
    print(f"Login failed: {response.text}")
```

```javascript
fetch('https://api.example.com/api/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
})
  .then(res => res.json())
  .then(data => console.log('Token:', data.token))
  .catch(err => console.error('Error:', err));
```

```bash
curl -X POST https://api.example.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```
"""
```

---

## 📤 출력 형식

### 문서 생성 리포트

```markdown
# Documentation Report

## Summary
- **Files Processed**: 45
- **API Endpoints**: 28
- **Docstrings Added**: 12
- **README Updated**: Yes
- **Changelog Generated**: Yes

---

## Generated Files

✅ `docs/api/openapi.yaml` - OpenAPI 3.0 spec (28 endpoints)
✅ `docs/api/README.md` - API 문서
✅ `README.md` - Updated Features, API, Environment Variables
✅ `CHANGELOG.md` - v1.2.0 → v1.3.0
✅ `docs/examples/` - 14 code examples

---

## API Documentation

### Endpoints by Module

| Module | Endpoints | Documented |
|--------|-----------|------------|
| auth | 5 | ✅ 5/5 |
| user | 8 | ✅ 8/8 |
| search | 3 | ✅ 3/3 |
| admin | 12 | ⚠️ 10/12 |

---

## Missing Documentation

### 1. admin.delete_user (admin/user.py:45)
**Severity**: Warning
**Reason**: 공개 함수에 docstring 없음

**Suggestion**:
```python
def delete_user(user_id: int):
    """
    사용자 삭제

    Args:
        user_id: 삭제할 사용자 ID

    Returns:
        True if successful

    Raises:
        ValueError: 사용자를 찾을 수 없음
    """
    pass
```

---

### 2. search.advanced_search (search/engine.py:120)
**Severity**: Info
**Reason**: 복잡한 함수 (complexity: 15)

---

## README Changes

### Features Section
+ ✅ User authentication (JWT)
+ ✅ Profile management
+ ✅ Search functionality

### API Endpoints Section
+ POST /api/login - 사용자 로그인
+ GET /api/user/me - 현재 사용자 정보
+ ... (28 endpoints total)

### Environment Variables Section
+ DATABASE_URL (required)
+ JWT_SECRET (required)
+ API_KEY (optional)

---

## Changelog (v1.3.0)

### Added (3)
- feat(PLAN-001): implement JWT authentication
- feat(PLAN-003): add user profile API
- feat(PLAN-007): add search functionality

### Fixed (2)
- fix(PLAN-002): resolve login validation error
- fix(PLAN-005): fix memory leak

---

## Next Steps

1. ⚠️ Add docstrings to 2 functions
2. ✅ Review generated API docs
3. ✅ Publish to documentation site
```

---

## 🧠 메모리 활용

### docs-history.json

```json
{
  "version": "0.0.1",
  "project": "multi-agent-coding-team",

  "documentation_coverage": {
    "api_endpoints": {
      "total": 28,
      "documented": 28,
      "coverage": 1.0
    },
    "public_functions": {
      "total": 150,
      "documented": 138,
      "coverage": 0.92
    }
  },

  "generated_files": [
    {
      "file": "docs/api/openapi.yaml",
      "timestamp": "2026-03-19T14:00:00Z",
      "endpoints": 28
    },
    {
      "file": "CHANGELOG.md",
      "timestamp": "2026-03-19T14:00:00Z",
      "version": "1.3.0"
    }
  ],

  "missing_docs_trend": [
    {"date": "2026-03-01", "count": 25},
    {"date": "2026-03-15", "count": 8},
    {"date": "2026-03-19", "count": 2}
  ],

  "common_patterns": [
    {
      "pattern": "API endpoint without examples",
      "frequency": 5
    }
  ]
}
```

---

## ⚠️ Gotchas

### 1. 코드와 문서 동기화

**원칙**: 문서는 코드에서 생성 (Single Source of Truth)

```python
# ❌ 잘못: 수동 문서
# docs/api.md에 수동으로 API 설명

# ✅ 올바름: 코드에서 생성
@app.post("/api/login")
async def login(email: str, password: str):
    """
    사용자 로그인

    이 docstring이 문서로 자동 생성됨
    """
    pass
```

### 2. 예제 코드 테스트

**검증**:
```python
# 생성된 예제 코드가 실제로 작동하는지 테스트
def test_generated_examples():
    examples = load_generated_examples()

    for example in examples:
        # 예제 코드 실행
        result = execute_code(example.code)

        if not result.success:
            raise Error(f"예제 코드 실패: {example.name}")
```

### 3. Changelog 중복 방지

**검증**:
```python
# 이미 Changelog에 있는 버전인지 확인
if version_exists_in_changelog(new_version):
    print(f"⚠️ Changelog에 {new_version} 이미 존재")
    return
```

### 4. 민감 정보 제외

**검증**:
```python
# 예제 코드에서 민감 정보 제거
sensitive_patterns = [
    r'api_key\s*=\s*["\'][^"\']+["\']',
    r'password\s*=\s*["\'][^"\']+["\']',
    r'sk-[a-zA-Z0-9]+'
]

for pattern in sensitive_patterns:
    if re.search(pattern, example_code):
        # 플레이스홀더로 대체
        example_code = re.sub(pattern, 'api_key = "YOUR_API_KEY"', example_code)
```

---

## 📊 기대 효과

### Before (수동 문서)

```
코드 작성 → 수동 문서 작성 (30분)
       → 코드 수정
       → 문서 업데이트 누락
       → 문서와 코드 불일치
```

**문제점**:
- ❌ 시간 소요
- ❌ 동기화 문제
- ❌ 문서 누락
- ❌ 예제 코드 오래됨

### After (자동 문서)

```
코드 작성 → docs-generator skill (자동)
       → 문서 자동 생성 (1분)
       → 예제 코드 자동 생성
       → 100% 동기화
```

**개선점**:
- ✅ 즉시 생성
- ✅ 항상 동기화
- ✅ 누락 없음
- ✅ 예제 코드 최신

### 수치 목표

| 항목 | 목표 |
|------|------|
| **문서 작성 시간** | **-90%** |
| **동기화 문제** | **0%** |
| **API 문서 커버리지** | **100%** |
| **예제 코드 정확성** | **100%** |

---

## 🔗 통합

### Auto-pipeline 통합

```python
# auto_pipeline.py

# Coding Agent 완료 후 (API 변경 감지)
if api_changed(changed_files):
    print("📝 API 문서 업데이트 중...")

    docs_result = self.run_skill("docs-generator", {
        "api": True,
        "readme": True,
        "changelog": True
    })

    if docs_result["success"]:
        print(f"✅ 문서 생성 완료:")
        print(f"   - API 문서: {docs_result['api_endpoints']}개 엔드포인트")
        print(f"   - README 업데이트: {docs_result['readme_updated']}")
        print(f"   - Changelog: {docs_result['changelog_version']}")

        # 문서 커밋
        self.run_skill("commit", {
            "ticket": ticket_num,
            "type": "docs"
        })
```

### GitHub Actions 통합

```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate docs
        run: |
          bash scripts/run-skill.sh docs-generator --all

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

---

**관련 문서**:
- [docs-generator.py](docs-generator.py) - 실제 구현
- [docs-history.json](../../.memory/docs-history.json) - 문서 히스토리
- [docs-config.json](docs-config.json) - 문서 설정
