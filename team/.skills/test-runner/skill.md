# Test Runner Skill

> **목적**: 테스트 자동 실행 및 결과 분석
>
> **타입**: Testing Skill
>
> **Thariq 교훈**: "Automate testing to catch bugs early"

---

## 🎯 트리거

### 자동 트리거
- Auto-pipeline: QA Agent 완료 후
- Git hook: pre-commit (선택)
- CI/CD: GitHub Actions

### 수동 트리거
```bash
# 전체 테스트 실행
bash scripts/run-skill.sh test-runner --all

# 특정 파일 테스트
bash scripts/run-skill.sh test-runner --file tests/auth/test_login.py

# 특정 디렉토리 테스트
bash scripts/run-skill.sh test-runner --dir tests/auth/

# 커버리지 포함
bash scripts/run-skill.sh test-runner --all --coverage

# 빠른 테스트만 (유닛)
bash scripts/run-skill.sh test-runner --unit
```

---

## 🔍 기능

### 1. 테스트 프레임워크 자동 감지

**지원 프레임워크**:
- **JavaScript/TypeScript**: Jest, Mocha, Vitest
- **Python**: pytest, unittest
- **Go**: go test
- **Rust**: cargo test

**감지 로직**:
```python
def detect_test_framework(project_root):
    # package.json 확인
    if exists("package.json"):
        package = load_json("package.json")
        if "jest" in package["devDependencies"]:
            return "jest"
        elif "mocha" in package["devDependencies"]:
            return "mocha"

    # Python 확인
    if exists("pytest.ini") or exists("setup.py"):
        return "pytest"

    # Go 확인
    if exists("go.mod"):
        return "go test"

    return None
```

### 2. 테스트 자동 실행

**실행 흐름**:
```python
1. 테스트 프레임워크 감지
2. 테스트 파일 찾기
3. 테스트 실행
4. 결과 파싱
5. 리포트 생성
```

**병렬 실행**:
```bash
# Jest
npm test -- --maxWorkers=4

# pytest
pytest -n 4

# Go
go test -parallel 4 ./...
```

### 3. 커버리지 측정

**커버리지 도구**:
- **JavaScript**: Istanbul/NYC
- **Python**: coverage.py
- **Go**: go test -cover
- **Rust**: cargo-tarpaulin

**임계값 검사**:
```python
coverage_thresholds = {
    "statements": 80,
    "branches": 75,
    "functions": 80,
    "lines": 80
}

if coverage < thresholds:
    return {
        "status": "failed",
        "message": f"커버리지 부족: {coverage}% < {threshold}%"
    }
```

### 4. 테스트 결과 분석

**메트릭**:
- 총 테스트 수
- 성공/실패/스킵
- 실행 시간
- 느린 테스트 (> 1초)
- 불안정한 테스트 (Flaky)

**분석 예시**:
```python
{
    "total": 150,
    "passed": 145,
    "failed": 3,
    "skipped": 2,
    "duration": "12.5s",
    "slow_tests": [
        {"name": "test_large_dataset", "duration": "3.2s"},
        {"name": "test_api_integration", "duration": "2.1s"}
    ],
    "flaky_tests": [
        {"name": "test_async_timeout", "failure_rate": 0.15}
    ]
}
```

---

## 📤 출력 형식

### 테스트 리포트

```markdown
# Test Report

## Summary
- **Total Tests**: 150
- **Passed**: ✅ 145 (96.7%)
- **Failed**: ❌ 3 (2.0%)
- **Skipped**: ⏭️ 2 (1.3%)
- **Duration**: 12.5s
- **Coverage**: 85% ✅

---

## Failed Tests

### 1. test_login_with_invalid_credentials
**File**: `tests/auth/test_login.py:45`
**Error**: AssertionError: Expected 401, got 500
**Duration**: 0.3s

```python
def test_login_with_invalid_credentials():
    response = client.post("/login", json={"email": "wrong@example.com"})
    assert response.status_code == 401  # ❌ Got 500
```

**Suggestion**: 서버가 500 에러를 반환 - 에러 핸들링 확인 필요

---

### 2. test_user_profile_update
**File**: `tests/user/test_profile.py:78`
**Error**: Timeout after 5s
**Duration**: 5.0s

**Suggestion**: API 응답 시간 개선 또는 타임아웃 증가

---

## Slow Tests (> 1s)

| Test | Duration | File |
|------|----------|------|
| test_large_dataset | 3.2s | tests/data/test_processing.py:120 |
| test_api_integration | 2.1s | tests/integration/test_api.py:55 |
| test_db_migration | 1.8s | tests/db/test_migrations.py:30 |

**Suggestion**: 병렬화 또는 테스트 데이터 축소 고려

---

## Coverage Report

| File | Coverage | Missing Lines |
|------|----------|---------------|
| src/auth/login.js | 95% | 45-47, 89 |
| src/auth/token.js | 88% | 23-25 |
| src/user/profile.js | 72% ⚠️ | 34-50, 78-90 |

**Overall**: 85% ✅ (threshold: 80%)

---

## Recommendations

1. 🔴 **Fix failing tests** (3개)
2. 🟡 **Improve coverage** for user/profile.js (72% → 80%+)
3. 🟡 **Optimize slow tests** (3개 > 1s)
4. 🟢 **Consider mocking** for API integration tests
```

---

## 🧠 메모리 활용

### test-history.json

```json
{
  "version": "0.0.1",
  "project": "multi-agent-coding-team",

  "test_runs": [
    {
      "timestamp": "2026-03-19T11:00:00Z",
      "total": 150,
      "passed": 145,
      "failed": 3,
      "duration": 12.5,
      "coverage": 0.85
    }
  ],

  "flaky_tests": [
    {
      "name": "test_async_timeout",
      "file": "tests/async/test_timeout.py",
      "failure_rate": 0.15,
      "last_failures": [
        "2026-03-18T10:00:00Z",
        "2026-03-17T14:00:00Z"
      ]
    }
  ],

  "slow_tests": [
    {
      "name": "test_large_dataset",
      "avg_duration": 3.2,
      "trend": "increasing"
    }
  ],

  "coverage_trend": [
    {"date": "2026-03-15", "coverage": 0.82},
    {"date": "2026-03-18", "coverage": 0.84},
    {"date": "2026-03-19", "coverage": 0.85}
  ],

  "common_failures": [
    {
      "error": "Timeout",
      "frequency": 8,
      "tests": ["test_api_integration", "test_async_timeout"]
    },
    {
      "error": "AssertionError",
      "frequency": 5,
      "tests": ["test_login_with_invalid_credentials"]
    }
  ]
}
```

---

## ⚠️ Gotchas

### 1. 테스트 순서 의존성 금지

**검증**:
```python
# 테스트를 랜덤 순서로 실행
pytest --random-order

# 실패하면 순서 의존성 있음
if random_run_failed and sequential_run_passed:
    raise Error("테스트가 순서에 의존합니다")
```

### 2. 테스트 환경 격리

**원칙**:
- 각 테스트는 독립적
- DB는 트랜잭션 롤백 또는 임시 DB
- 파일 시스템은 임시 디렉토리

**예시**:
```python
# ✅ 올바름
@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()  # 롤백으로 격리

# ❌ 잘못
def test_create_user():
    # DB 영구 변경 - 다른 테스트 영향
    db.users.insert({"name": "test"})
```

### 3. Flaky 테스트 추적

**감지**:
```python
# 같은 테스트를 10번 실행
for i in range(10):
    result = run_test("test_async_timeout")
    if result != "passed":
        flaky_count += 1

if flaky_count > 0:
    mark_as_flaky("test_async_timeout", flaky_count / 10)
```

### 4. 커버리지 감소 방지

**검증**:
```python
old_coverage = get_coverage_from_history()
new_coverage = run_tests_with_coverage()

if new_coverage < old_coverage - 5:  # 5% 이상 감소
    raise Error(f"커버리지 감소: {old_coverage}% → {new_coverage}%")
```

---

## 🔧 고급 기능

### 1. 테스트 자동 재시도

**Flaky 테스트 재시도**:
```python
# pytest
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_async_timeout():
    # 3번까지 재시도, 1초 대기
    pass
```

### 2. 병렬 테스트

**설정**:
```python
# Jest
{
  "jest": {
    "maxWorkers": "50%"
  }
}

# pytest
pytest -n auto  # CPU 코어 수만큼
```

### 3. 테스트 선택 실행

**변경 파일 기반**:
```bash
# Git diff로 변경 파일 찾기
changed_files=$(git diff --name-only HEAD~1)

# 관련 테스트만 실행
jest --findRelatedTests $changed_files
```

### 4. Mutation Testing

**개념**: 코드를 변경(mutate)해서 테스트가 잡아내는지 확인

**도구**:
- JavaScript: Stryker
- Python: mutmut

**예시**:
```python
# 원본 코드
def is_adult(age):
    return age >= 18

# Mutation
def is_adult(age):
    return age > 18  # >= → >

# 테스트가 실패해야 함
def test_is_adult():
    assert is_adult(18) == True  # Mutation 감지!
```

---

## 📊 기대 효과

### Before (수동 테스트)

```
코드 작성 → 수동 테스트 실행 (5분)
       → 실패 확인
       → 수정
       → 재실행
```

**문제점**:
- ❌ 시간 소요
- ❌ 테스트 누락 가능
- ❌ 커버리지 미측정
- ❌ Flaky 테스트 방치

### After (자동 테스트)

```
코드 작성 → test-runner skill (자동)
       → 리포트 생성 (1분)
       → 실패 원인 분석
       → Flaky 테스트 추적
```

**개선점**:
- ✅ 즉시 피드백
- ✅ 100% 테스트 실행
- ✅ 커버리지 자동 측정
- ✅ Flaky 테스트 감지

### 수치 목표

| 항목 | 목표 |
|------|------|
| **테스트 실행 시간** | **-50%** (병렬화) |
| **커버리지 추적** | **100%** |
| **Flaky 테스트 감지** | **90%+** |
| **실패 원인 분석** | **자동** |

---

## 🔗 통합

### Auto-pipeline 통합

```python
# auto_pipeline.py

# QA Agent 완료 후
result_qa = self.run_agent("qa", qa_prompt, ticket_num)

# Test Runner Skill 실행
test_result = self.run_skill("test-runner", {
    "mode": "all",
    "coverage": True
})

if not test_result["all_passed"]:
    print(f"❌ 테스트 실패: {test_result['failed']}개")
    print(f"   상세: {test_result['report_path']}")

    # QA Agent 재실행
    retry_prompt = self._build_test_retry_prompt(test_result)
    result_qa = self.run_agent("qa", retry_prompt, ticket_num)

    # 재테스트
    test_retry = self.run_skill("test-runner", {"mode": "all"})

    if not test_retry["all_passed"]:
        raise Exception("재테스트 실패 - 수동 개입 필요")

if test_result["coverage"] < 80:
    print(f"⚠️  커버리지 부족: {test_result['coverage']}%")
else:
    print(f"✅ 모든 테스트 통과, 커버리지: {test_result['coverage']}%")
```

### GitHub Actions 통합

```yaml
# .github/workflows/test.yml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run test-runner skill
        run: |
          bash scripts/run-skill.sh test-runner --all --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

---

## 📝 로그

**테스트 로그**: `projects/{project}/logs/test-runner/{timestamp}.json`

```json
{
  "timestamp": "2026-03-19T11:00:00Z",
  "framework": "pytest",
  "total_tests": 150,
  "passed": 145,
  "failed": 3,
  "skipped": 2,
  "duration_seconds": 12.5,
  "coverage": 0.85,
  "failed_tests": [
    {
      "name": "test_login_with_invalid_credentials",
      "file": "tests/auth/test_login.py",
      "line": 45,
      "error": "AssertionError: Expected 401, got 500",
      "duration": 0.3
    }
  ],
  "slow_tests": [
    {
      "name": "test_large_dataset",
      "duration": 3.2
    }
  ]
}
```

---

**관련 문서**:
- [test-runner.py](test-runner.py) - 실제 구현
- [test-history.json](../../.memory/test-history.json) - 테스트 히스토리
