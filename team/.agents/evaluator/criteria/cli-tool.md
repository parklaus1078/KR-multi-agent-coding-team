# CLI Tool 평가 기준

> **프로젝트 타입**: cli-tool
>
> **평가 대상**: 커맨드라인 인터페이스 도구
>
> **총점**: 100점

---

## 📊 평가 기준 (4가지)

### 1. 기능 완성도 (40점)

#### 명령어 동작 (25점)

**필수 검증 항목:**

- [ ] **모든 명령어 실행 가능** (15점)
  - Acceptance Criteria의 모든 명령어 성공
  - Exit code 0 반환
  - 예상 출력 생성

  **검증 예시:**
  ```bash
  # 1. help 명령어
  mycli --help
  # 예상: 사용법 표시, Exit code 0

  # 2. 메인 명령어
  mycli create todo "Buy milk"
  # 예상: "Todo created: Buy milk", Exit code 0

  # 3. 서브 명령어
  mycli list todos
  # 예상: 할일 목록 표시, Exit code 0

  # 4. Exit code 확인
  echo $?
  # 예상: 0
  ```

- [ ] **옵션/플래그 동작** (5점)
  - `--help`, `--version` 필수
  - 선택 옵션 정상 동작
  - 플래그 조합 지원

  **검증 예시:**
  ```bash
  # 버전 확인
  mycli --version
  # 예상: "mycli version 1.0.0"

  # 플래그 조합
  mycli list --format json --limit 10
  # 예상: JSON 형식으로 10개 표시
  ```

- [ ] **에러 케이스 처리** (5점)
  - 잘못된 명령어 시 에러 메시지 + Exit code 1
  - 필수 인자 누락 시 에러 메시지
  - 권한 문제 시 명확한 에러

  **검증 예시:**
  ```bash
  # 잘못된 명령어
  mycli invalid-command
  # 예상: "Error: Unknown command 'invalid-command'", Exit code 1

  # 필수 인자 누락
  mycli create todo
  # 예상: "Error: Missing required argument 'description'", Exit code 1

  # Exit code 확인
  echo $?
  # 예상: 1
  ```

#### 입출력 (15점)

**필수 검증 항목:**

- [ ] **출력 형식** (5점)
  - 읽기 쉬운 텍스트 출력
  - 색상 지원 (선택)
  - 프로그레스바 지원 (장시간 작업 시)

- [ ] **파일 입출력** (5점)
  - 설정 파일 읽기/쓰기
  - 데이터 파일 읽기/쓰기
  - 파일 없을 시 적절한 기본값 또는 에러

- [ ] **표준 스트림 활용** (5점)
  - stdin 입력 지원
  - stdout 출력 (정상 메시지)
  - stderr 출력 (에러 메시지)

  **검증 예시:**
  ```bash
  # stdin 파이프
  echo "Buy milk" | mycli create todo
  # 예상: "Todo created: Buy milk"

  # stdout 리다이렉트
  mycli list todos > output.txt
  cat output.txt
  # 예상: 할일 목록

  # stderr 확인
  mycli invalid-command 2> error.txt
  cat error.txt
  # 예상: "Error: Unknown command..."
  ```

---

### 2. 코드 품질 (30점)

#### 코딩 룰 준수 (15점)

**필수 검증 항목:**

- [ ] **코딩 룰 준수** (8점)
  - `.rules/_verified/cli-tool/` 또는 `.rules/_cache/` 준수
  - DRY, SOLID 원칙 적용
  - 명령어별 함수 분리

  **체크 포인트:**
  - 각 명령어가 독립 함수로 분리됨
  - 중복 코드 없음
  - 공통 유틸리티 함수 재사용

- [ ] **타입 힌팅** (4점)
  - 모든 함수에 타입 힌트 (Python)
  - 또는 정적 타입 언어 사용 (Go, Rust)

  **예시 (Python):**
  ```python
  # ✅ 좋은 예
  def create_todo(description: str, priority: int = 0) -> Todo:
      """할일을 생성합니다."""
      return Todo(description=description, priority=priority)

  # ❌ 나쁜 예
  def create_todo(description, priority=0):
      return Todo(description=description, priority=priority)
  ```

- [ ] **에러 핸들링** (3점)
  - try-except 사용
  - 사용자 친화적 에러 메시지
  - 적절한 Exit code (0: 성공, 1: 에러)

#### 아키텍처 (15점)

**필수 검증 항목:**

- [ ] **명령어 구조** (7점)
  - Click, Typer, Cobra 등 CLI 프레임워크 사용
  - 명령어/서브명령어 계층 구조
  - 옵션/인자 명확히 정의

  **예시 (Python Click):**
  ```python
  import click

  @click.group()
  def cli():
      """My CLI tool"""
      pass

  @cli.command()
  @click.argument('description')
  @click.option('--priority', default=0, help='Task priority')
  def create(description: str, priority: int):
      """Create a new todo"""
      ...

  @cli.command()
  @click.option('--format', default='text', type=click.Choice(['text', 'json']))
  def list(format: str):
      """List all todos"""
      ...
  ```

- [ ] **설정 관리** (4점)
  - 설정 파일 지원 (YAML, JSON, TOML)
  - 환경 변수 지원
  - 우선순위: CLI 옵션 > 환경 변수 > 설정 파일 > 기본값

- [ ] **데이터 저장** (4점)
  - SQLite, JSON 파일 등 로컬 저장
  - 데이터 무결성 보장
  - 마이그레이션 지원 (버전 업그레이드 시)

---

### 3. 테스트 커버리지 (20점)

#### 유닛 테스트 (12점)

**필수 검증 항목:**

- [ ] **커버리지 80% 이상** (6점)
  - pytest, go test, cargo test 사용
  - 각 명령어 함수 테스트
  - 에러 케이스 포함

  **커버리지 확인:**
  ```bash
  # Python
  pytest --cov=src --cov-report=term
  # 목표: 80% 이상

  # Go
  go test -cover ./...
  # 목표: 80% 이상

  # Rust
  cargo tarpaulin
  # 목표: 80% 이상
  ```

- [ ] **명령어별 테스트** (4점)
  - 각 명령어의 정상 케이스 테스트
  - 에러 케이스 테스트
  - Exit code 확인

  **예시 (Python):**
  ```python
  from click.testing import CliRunner
  from mycli import cli

  def test_create_todo():
      runner = CliRunner()
      result = runner.invoke(cli, ['create', 'Buy milk'])
      assert result.exit_code == 0
      assert 'Todo created' in result.output

  def test_create_todo_missing_arg():
      runner = CliRunner()
      result = runner.invoke(cli, ['create'])
      assert result.exit_code == 2  # Click의 기본 에러 코드
      assert 'Missing argument' in result.output
  ```

- [ ] **테스트 통과율 100%** (2점)
  - 모든 테스트 통과
  - Flaky 테스트 없음

#### 통합 테스트 (8점)

**필수 검증 항목:**

- [ ] **실제 명령어 실행 테스트** (4점)
  - 서브프로세스로 CLI 실행
  - 실제 파일 시스템 사용 (또는 tmpdir)

  **예시 (Python):**
  ```python
  import subprocess

  def test_cli_integration(tmp_path):
      # 임시 디렉토리에서 실행
      result = subprocess.run(
          ['mycli', 'create', 'Buy milk'],
          cwd=tmp_path,
          capture_output=True,
          text=True
      )
      assert result.returncode == 0
      assert 'Todo created' in result.stdout
  ```

- [ ] **크로스 플랫폼 테스트** (4점)
  - Linux, macOS, Windows에서 동작 확인 (CI/CD)
  - 경로 구분자 (`/` vs `\`) 처리
  - 환경 변수 처리

---

### 4. 문서화 (10점)

**필수 검증 항목:**

- [ ] **README** (5점)
  - 설치 방법 (pip, npm, cargo, go install)
  - 사용 예시 (주요 명령어)
  - 설정 방법

  **예시:**
  ```markdown
  # My CLI Tool

  ## Installation

  ```bash
  pip install mycli
  ```

  ## Usage

  ```bash
  # Create a todo
  mycli create "Buy milk"

  # List todos
  mycli list

  # Complete a todo
  mycli complete 1
  ```

  ## Configuration

  Create `~/.mycli/config.yaml`:
  ```yaml
  format: json
  color: true
  ```
  ```

- [ ] **--help 문서** (3점)
  - 각 명령어에 help 텍스트
  - 옵션 설명 명확
  - 예시 포함

  **검증:**
  ```bash
  mycli --help
  # 예상: 전체 명령어 목록 + 설명

  mycli create --help
  # 예상: create 명령어 상세 설명 + 옵션 + 예시
  ```

- [ ] **Docstring** (2점)
  - 모든 명령어 함수에 문서 주석
  - 파라미터, 리턴 값 설명

---

## 🎯 점수 계산 예시

### 예시 1: 우수한 CLI (90점)

| 항목 | 만점 | 획득 | 비고 |
|------|-----|-----|------|
| **기능 완성도** | 40 | 38 | 일부 에러 메시지 불명확 |
| - 명령어 동작 | 25 | 24 | delete 명령어 일부 버그 |
| - 입출력 | 15 | 14 | stderr 사용 누락 |
| **코드 품질** | 30 | 27 | 일부 중복 코드 |
| - 코딩 룰 | 15 | 14 | 타입 힌트 일부 누락 |
| - 아키텍처 | 15 | 13 | 설정 우선순위 불명확 |
| **테스트** | 20 | 18 | 커버리지 75% |
| - 유닛 테스트 | 12 | 10 | 일부 에러 케이스 미테스트 |
| - 통합 테스트 | 8 | 8 | 완벽 |
| **문서화** | 10 | 7 | help 텍스트 일부 불명확 |
| **총점** | **100** | **90** | ✅ **우수** |

**판정:** ✅ 우수 (재작업 불필요)

---

## 🔍 특수 검증 항목 (CLI Tool)

### 사용자 경험

- [ ] **에러 메시지 품질**
  - 무엇이 잘못되었는지 명확히 설명
  - 해결 방법 제시

  **예시:**
  ```bash
  # ❌ 나쁜 예
  Error: Invalid input

  # ✅ 좋은 예
  Error: Invalid priority value '10'
  Priority must be between 0 and 5.
  Usage: mycli create "description" --priority 0-5
  ```

- [ ] **명령어 자동 완성** (선택)
  - Bash, Zsh 자동 완성 스크립트 제공

- [ ] **색상 지원** (선택)
  - 성공 메시지: 녹색
  - 에러 메시지: 빨간색
  - 경고 메시지: 노란색
  - `--no-color` 옵션 지원

### 성능

- [ ] **실행 속도** (목표: 100ms 이하)
  ```bash
  time mycli list
  # 예상: real 0m0.050s → ✅ 통과
  # 예상: real 0m0.500s → ⚠️ 최적화 필요
  ```

- [ ] **메모리 사용량** (목표: 50MB 이하)
  - 작은 CLI 도구는 가벼워야 함

### 배포

- [ ] **패키지 설치 가능**
  - Python: `pip install`
  - Node.js: `npm install -g`
  - Go: `go install`
  - Rust: `cargo install`

- [ ] **의존성 명확**
  - requirements.txt, package.json, go.mod, Cargo.toml
  - 불필요한 의존성 없음

---

## 📝 평가 리포트 예시

```markdown
# 평가 리포트: PLAN-001 (Todo CLI Tool)

## 📊 종합 점수

**총점: 78/100** ⚠️ **보통**

| 항목 | 만점 | 획득 |
|------|-----|-----|
| 기능 완성도 | 40 | 32 |
| 코드 품질 | 30 | 23 |
| 테스트 커버리지 | 20 | 15 |
| 문서화 | 10 | 8 |

---

## ✅ 통과한 항목

### 기능 완성도
- [x] create, list, complete 명령어 정상 동작
- [x] --help, --version 지원
- [x] 설정 파일 읽기/쓰기

### 코드 품질
- [x] Click 프레임워크 사용
- [x] 명령어별 함수 분리

### 문서화
- [x] README 작성됨
- [x] --help 텍스트 명확

---

## ❌ 실패한 항목

### 기능 완성도 (32/40점)

#### 1. delete 명령어 버그 (-5점)
- **문제**: 존재하지 않는 ID 삭제 시 에러 메시지 없음
- **재현 방법**:
  ```bash
  mycli delete 999
  echo $?
  # 예상: Exit code 1, 에러 메시지
  # 실제: Exit code 0, 메시지 없음
  ```
- **수정 방법**: `src/commands/delete.py:15` - ID 존재 여부 확인 추가

#### 2. stderr 사용 누락 (-3점)
- **문제**: 에러 메시지가 stdout으로 출력됨
- **재현 방법**:
  ```bash
  mycli invalid-command 2> error.txt 1> output.txt
  cat error.txt  # 비어 있음
  cat output.txt  # 에러 메시지 여기에 있음
  ```
- **수정 방법**: Click의 `echo(err=True)` 사용

### 코드 품질 (23/30점)

#### 1. 중복 코드 (-4점)
- **문제**: 데이터 로드 로직이 3개 명령어에 반복됨
- **파일**:
  - `src/commands/list.py:10`
  - `src/commands/complete.py:8`
  - `src/commands/delete.py:7`
- **수정 방법**: `src/utils/data.py`에 `load_todos()` 함수 추출

#### 2. 타입 힌트 누락 (-3점)
- **파일**: `src/utils/storage.py` - 대부분의 함수
- **수정 방법**: 타입 힌트 추가

### 테스트 커버리지 (15/20점)

#### 1. 유닛 테스트 커버리지 65% (-5점)
- **목표**: 80% 이상
- **현재**: 65%
- **누락된 테스트**:
  - `delete` 명령어 에러 케이스
  - `utils/storage.py` 함수들
- **수정 방법**: `tests/test_commands.py`에 테스트 추가

---

## 🔧 개선 제안

### 우선순위 1 (필수)
1. ✅ delete 명령어 버그 수정
2. ✅ 테스트 커버리지 80% 달성
3. ✅ 중복 코드 제거

### 우선순위 2 (권장)
1. stderr 사용 (에러 메시지)
2. 타입 힌트 추가

### 우선순위 3 (선택)
1. 색상 지원 추가
2. 자동 완성 스크립트 제공

---

## 📝 다음 단계

**재작업 필요**: 예

**권장 조치:**
1. Coding Agent 재실행으로 버그 수정
2. QA Agent 재실행으로 테스트 추가
3. Evaluator Agent 재평가

**예상 점수 향상**: +12점 → 총 90점 (보통 → 우수)
```

---

## 🎯 작업 완료 체크리스트

- [ ] 모든 명령어 실행 테스트
- [ ] Exit code 확인
- [ ] 에러 메시지 품질 확인
- [ ] 코딩 룰 준수 여부 확인
- [ ] 테스트 커버리지 측정
- [ ] README 및 help 텍스트 확인
- [ ] 평가 리포트 작성
- [ ] 점수 JSON 저장
- [ ] 피드백 요약 생성
