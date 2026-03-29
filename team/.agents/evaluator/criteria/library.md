# Library 평가 기준

> **프로젝트 타입**: library
>
> **평가 대상**: 재사용 가능한 라이브러리 (Python, JavaScript, Go, Rust 등)
>
> **총점**: 100점

---

## 📊 평가 기준 (4가지)

### 1. 기능 완성도 (40점)

#### API 동작 (25점)

**필수 검증 항목:**

- [ ] **모든 Public API 동작** (15점)
  - Acceptance Criteria의 모든 함수/클래스 정상 동작
  - 예상 입력에 대한 올바른 출력
  - 타입 일치

  **검증 예시 (Python):**
  ```python
  # 라이브러리 import
  from mylib import calculate, DataProcessor

  # 함수 테스트
  result = calculate(10, 20)
  assert result == 30, "✅ calculate() 정상 동작"

  # 클래스 테스트
  processor = DataProcessor()
  output = processor.transform([1, 2, 3])
  assert output == [2, 4, 6], "✅ DataProcessor 정상 동작"
  ```

- [ ] **에러 처리** (5점)
  - 잘못된 입력 시 명확한 예외 발생
  - 예외 타입 명확 (ValueError, TypeError 등)
  - 예외 메시지 명확

  **검증 예시:**
  ```python
  import pytest
  from mylib import calculate

  def test_calculate_invalid_input():
      with pytest.raises(TypeError) as exc_info:
          calculate("10", "20")
      assert "Expected int" in str(exc_info.value)
  ```

- [ ] **엣지 케이스 처리** (5점)
  - None, 빈 리스트, 0, 음수 등 처리
  - 대용량 데이터 처리 (메모리 에러 없음)

#### API 일관성 (15점)

**필수 검증 항목:**

- [ ] **명명 규칙 일관성** (5점)
  - 함수명: `snake_case` (Python), `camelCase` (JavaScript)
  - 클래스명: `PascalCase`
  - 상수: `UPPER_SNAKE_CASE`

- [ ] **파라미터 순서 일관성** (5점)
  - 유사한 함수의 파라미터 순서 동일
  - 필수 파라미터 → 선택 파라미터 순서

  **예시:**
  ```python
  # ✅ 좋은 예 (일관성 있음)
  def process_data(data, mode="fast", verbose=False):
      ...

  def process_batch(data, mode="fast", verbose=False):
      ...

  # ❌ 나쁜 예 (일관성 없음)
  def process_data(data, mode="fast", verbose=False):
      ...

  def process_batch(mode="fast", data, verbose=False):
      ...
  ```

- [ ] **반환 타입 일관성** (5점)
  - 유사한 함수의 반환 타입 동일
  - None 반환 시 명시적 이유
  - 성공/실패를 Result/Option 타입으로 표현 (Rust 스타일)

---

### 2. 코드 품질 (30점)

#### 코딩 룰 준수 (15점)

**필수 검증 항목:**

- [ ] **코딩 룰 준수** (8점)
  - `.rules/_verified/library/` 또는 `.rules/_cache/` 준수
  - DRY, SOLID 원칙 적용
  - 각 함수/클래스의 책임 명확

  **체크 포인트:**
  - 중복 코드 없음
  - 함수 크기 적절 (50줄 이하)
  - 단일 책임 원칙 (SRP)

- [ ] **타입 정의** (4점)
  - 타입 힌트 (Python)
  - TypeScript 사용 (JavaScript)
  - 정적 타입 언어 (Go, Rust)

  **예시 (Python):**
  ```python
  from typing import List, Optional

  # ✅ 좋은 예
  def find_user(user_id: int) -> Optional[User]:
      """사용자를 찾습니다."""
      ...

  # ❌ 나쁜 예
  def find_user(user_id):
      ...
  ```

- [ ] **Public API 최소화** (3점)
  - 내부 함수는 `_` 접두사 (Python) 또는 private 키워드
  - `__all__` 명시 (Python)
  - Public API만 문서화

#### 아키텍처 (15점)

**필수 검증 항목:**

- [ ] **모듈 구조** (7점)
  - 기능별 모듈 분리
  - `__init__.py`에서 Public API 노출
  - 순환 의존성 없음

  **예시 (Python):**
  ```
  mylib/
  ├── __init__.py        # Public API 노출
  ├── core.py            # 핵심 기능
  ├── utils.py           # 유틸리티
  └── _internal.py       # 내부 구현 (Private)
  ```

  ```python
  # mylib/__init__.py
  from .core import calculate, DataProcessor
  from .utils import parse_config

  __all__ = ['calculate', 'DataProcessor', 'parse_config']
  ```

- [ ] **의존성 최소화** (4점)
  - 불필요한 외부 라이브러리 의존성 없음
  - 가능하면 표준 라이브러리만 사용
  - 선택적 의존성은 extras로 분리

  **예시 (Python):**
  ```toml
  # pyproject.toml
  [project]
  dependencies = []  # 필수 의존성 없음

  [project.optional-dependencies]
  viz = ["matplotlib>=3.0"]  # 시각화 기능 (선택)
  ```

- [ ] **버전 관리** (4점)
  - Semantic Versioning (SemVer) 준수
  - `__version__` 변수 제공
  - CHANGELOG 업데이트

---

### 3. 테스트 커버리지 (20점)

#### 유닛 테스트 (15점)

**필수 검증 항목:**

- [ ] **커버리지 90% 이상** (10점)
  - pytest, jest, go test, cargo test 사용
  - 모든 Public API 테스트
  - 에러 케이스 포함
  - 엣지 케이스 포함

  **커버리지 확인:**
  ```bash
  # Python
  pytest --cov=mylib --cov-report=term
  # 목표: 90% 이상

  # JavaScript
  npm test -- --coverage
  # 목표: 90% 이상

  # Go
  go test -cover ./...
  # 목표: 90% 이상

  # Rust
  cargo tarpaulin
  # 목표: 90% 이상
  ```

- [ ] **테스트 통과율 100%** (3점)
  - 모든 테스트 통과
  - Flaky 테스트 없음

- [ ] **프로퍼티 기반 테스트** (2점) (선택)
  - Hypothesis (Python), fast-check (JavaScript) 사용
  - 무작위 입력에 대한 속성 검증

  **예시 (Python):**
  ```python
  from hypothesis import given
  import hypothesis.strategies as st

  @given(st.integers(), st.integers())
  def test_add_commutative(a, b):
      """덧셈의 교환 법칙 검증"""
      assert add(a, b) == add(b, a)
  ```

#### 예제 코드 테스트 (5점)

**필수 검증 항목:**

- [ ] **README 예제 동작** (3점)
  - README의 모든 코드 예시가 실제로 실행됨
  - doctest 또는 별도 테스트로 검증

  **예시 (Python doctest):**
  ```python
  def add(a: int, b: int) -> int:
      """
      두 수를 더합니다.

      >>> add(1, 2)
      3
      >>> add(-1, 1)
      0
      """
      return a + b
  ```

  ```bash
  python -m doctest mylib/core.py
  # 예상: All tests passed
  ```

- [ ] **examples/ 디렉토리 예제 동작** (2점)
  - 모든 예제 파일 실행 가능
  - 에러 없이 완료

---

### 4. 문서화 (10점)

**필수 검증 항목:**

- [ ] **README** (4점)
  - 설치 방법
  - 빠른 시작 (Quick Start)
  - 주요 기능 예시
  - API 문서 링크

  **예시:**
  ```markdown
  # My Library

  ## Installation

  ```bash
  pip install mylib
  ```

  ## Quick Start

  ```python
  from mylib import calculate

  result = calculate(10, 20)
  print(result)  # 30
  ```

  ## Features

  - Feature 1: Description
  - Feature 2: Description

  ## API Documentation

  See [API Docs](docs/api.md) for detailed documentation.
  ```

- [ ] **API 문서** (4점)
  - 모든 Public 함수/클래스 문서화
  - Docstring (Python), JSDoc (JavaScript)
  - 파라미터, 리턴 값, 예외 설명

  **예시 (Python):**
  ```python
  def calculate(a: int, b: int, operation: str = "add") -> int:
      """
      두 수를 계산합니다.

      Args:
          a (int): 첫 번째 수
          b (int): 두 번째 수
          operation (str): 연산 종류 ("add", "subtract", "multiply", "divide")

      Returns:
          int: 계산 결과

      Raises:
          ValueError: operation이 지원되지 않는 경우
          ZeroDivisionError: division by zero 시

      Examples:
          >>> calculate(10, 20, "add")
          30
          >>> calculate(10, 20, "multiply")
          200
      """
      ...
  ```

- [ ] **CHANGELOG** (2점)
  - 버전별 변경 사항 기록
  - Keep a Changelog 형식 준수

  **예시:**
  ```markdown
  # Changelog

  ## [1.1.0] - 2026-03-29

  ### Added
  - 새로운 기능: `DataProcessor` 클래스

  ### Changed
  - `calculate()` 함수 성능 개선 (10배 빠름)

  ### Fixed
  - `parse_config()` 버그 수정

  ## [1.0.0] - 2026-03-01

  ### Added
  - 초기 릴리스
  ```

---

## 🎯 점수 계산 예시

### 예시 1: 우수한 라이브러리 (95점)

| 항목 | 만점 | 획득 | 비고 |
|------|-----|-----|------|
| **기능 완성도** | 40 | 39 | 일부 엣지 케이스 미처리 |
| - API 동작 | 25 | 24 | 대용량 데이터 테스트 부족 |
| - API 일관성 | 15 | 15 | 완벽 |
| **코드 품질** | 30 | 29 | 일부 내부 함수 public |
| - 코딩 룰 | 15 | 15 | 완벽 |
| - 아키텍처 | 15 | 14 | Public API 일부 노출 과다 |
| **테스트** | 20 | 19 | 커버리지 88% |
| - 유닛 테스트 | 15 | 14 | 목표 90% |
| - 예제 테스트 | 5 | 5 | 완벽 |
| **문서화** | 10 | 8 | CHANGELOG 부족 |
| **총점** | **100** | **95** | ✅ **우수** |

**판정:** ✅ 우수 (재작업 불필요)

---

## 🔍 특수 검증 항목 (Library)

### 배포 준비

- [ ] **패키지 메타데이터**
  - `setup.py` / `pyproject.toml` (Python)
  - `package.json` (JavaScript)
  - `Cargo.toml` (Rust)
  - `go.mod` (Go)

  **체크 포인트:**
  - name, version, description, author, license 명시
  - keywords, classifiers 추가 (검색 가능성)

- [ ] **LICENSE 파일**
  - MIT, Apache 2.0, BSD 등 명시
  - 저작권 정보

- [ ] **패키지 빌드**
  ```bash
  # Python
  python -m build
  # 예상: dist/mylib-1.0.0.tar.gz, dist/mylib-1.0.0-py3-none-any.whl

  # JavaScript
  npm pack
  # 예상: mylib-1.0.0.tgz

  # Rust
  cargo build --release
  # 예상: target/release/libmylib.rlib

  # Go
  go build
  # 예상: 바이너리 생성
  ```

### 하위 호환성

- [ ] **Semantic Versioning 준수**
  - Major: Breaking changes
  - Minor: New features (backward compatible)
  - Patch: Bug fixes

- [ ] **Deprecation 경고**
  - 제거 예정 API에 `@deprecated` 표시
  - 대안 제시

  **예시 (Python):**
  ```python
  import warnings

  def old_function():
      """
      .. deprecated:: 1.5.0
         Use :func:`new_function` instead.
      """
      warnings.warn(
          "old_function is deprecated, use new_function instead",
          DeprecationWarning,
          stacklevel=2
      )
      ...
  ```

### 성능

- [ ] **시간 복잡도 문서화**
  - O(n), O(log n) 등 명시
  - 대용량 데이터 처리 시간 벤치마크

- [ ] **메모리 효율**
  - 불필요한 복사 최소화
  - Generator/Iterator 사용 (Python)
  - Lazy evaluation

---

## 📝 평가 리포트 예시

```markdown
# 평가 리포트: PLAN-001 (Data Processing Library)

## 📊 종합 점수

**총점: 82/100** ⚠️ **보통**

| 항목 | 만점 | 획득 |
|------|-----|-----|
| 기능 완성도 | 40 | 35 |
| 코드 품질 | 30 | 25 |
| 테스트 커버리지 | 20 | 15 |
| 문서화 | 10 | 7 |

---

## ✅ 통과한 항목

### 기능 완성도
- [x] 모든 Public API 정상 동작
- [x] 명명 규칙 일관성

### 코드 품질
- [x] 타입 힌트 작성
- [x] 모듈 구조 명확

### 문서화
- [x] README 작성됨
- [x] Docstring 작성

---

## ❌ 실패한 항목

### 기능 완성도 (35/40점)

#### 1. 엣지 케이스 미처리 (-5점)
- **문제**: 빈 리스트 입력 시 에러 발생
- **재현 방법**:
  ```python
  from mylib import DataProcessor
  processor = DataProcessor()
  result = processor.transform([])
  # 예상: []
  # 실제: ValueError: list is empty
  ```
- **수정 방법**: `src/core.py:45` - 빈 리스트 체크 추가

### 코드 품질 (25/30점)

#### 1. Public API 과다 노출 (-3점)
- **문제**: 내부 함수가 public으로 노출됨
- **파일**: `mylib/__init__.py`
- **수정 방법**: `_internal_helper()` 함수를 `_`로 시작하도록 변경

#### 2. 불필요한 의존성 (-2점)
- **문제**: `requests` 라이브러리를 사용하지만 선택적 기능
- **수정 방법**: `pyproject.toml`에서 optional-dependencies로 이동

### 테스트 커버리지 (15/20점)

#### 1. 유닛 테스트 커버리지 75% (-5점)
- **목표**: 90% 이상
- **현재**: 75%
- **누락된 테스트**:
  - `DataProcessor.validate()` 메서드
  - 에러 케이스 테스트
- **수정 방법**: `tests/test_core.py`에 테스트 추가

### 문서화 (7/10점)

#### 1. CHANGELOG 없음 (-2점)
- **수정 방법**: `CHANGELOG.md` 파일 생성

#### 2. API 문서 일부 누락 (-1점)
- **문제**: `DataProcessor.validate()` 메서드 Docstring 없음
- **수정 방법**: Docstring 추가

---

## 🔧 개선 제안

### 우선순위 1 (필수)
1. ✅ 엣지 케이스 처리 (빈 리스트)
2. ✅ 테스트 커버리지 90% 달성
3. ✅ Public API 최소화

### 우선순위 2 (권장)
1. CHANGELOG 작성
2. 의존성 정리 (optional-dependencies)

### 우선순위 3 (선택)
1. 프로퍼티 기반 테스트 추가
2. 성능 벤치마크 추가

---

## 📝 다음 단계

**재작업 필요**: 예

**권장 조치:**
1. Coding Agent 재실행으로 버그 수정
2. QA Agent 재실행으로 테스트 추가
3. Evaluator Agent 재평가

**예상 점수 향상**: +13점 → 총 95점 (보통 → 우수)
```

---

## 🎯 작업 완료 체크리스트

- [ ] 모든 Public API 테스트
- [ ] 에러 케이스 및 엣지 케이스 검증
- [ ] 코딩 룰 준수 여부 확인
- [ ] 테스트 커버리지 측정 (목표: 90%)
- [ ] README 예제 동작 확인
- [ ] API 문서 완성도 확인
- [ ] 패키지 빌드 가능 확인
- [ ] 평가 리포트 작성
- [ ] 점수 JSON 저장
- [ ] 피드백 요약 생성
