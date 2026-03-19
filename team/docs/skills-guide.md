# Skills 사용 가이드

> **목적**: 에이전트가 Skills를 효과적으로 사용하는 방법
>
> **대상**: PM, Coding, QA Agents
>
> **Phase**: 3.3 - Agent-Skill 통합

---

## 📚 Skills 개요

Skills는 재사용 가능한 독립적 워크플로우입니다. 에이전트는 특정 작업을 Skills에 위임하여 일관성과 품질을 보장합니다.

### Skills vs Agents

| 항목 | Skills | Agents |
|------|--------|--------|
| **목적** | 단일 작업 자동화 | 복잡한 의사결정 |
| **재사용성** | 100% (프로젝트 독립) | 프로젝트 의존적 |
| **상태** | 무상태 (Stateless) | 상태 유지 (Stateful) |
| **실행** | 스크립트 실행 | AI 대화 |
| **예시** | 커밋 메시지 생성 | 명세서 작성 |

---

## 🛠️ 전체 Skills 라이브러리

### Code Quality (3개)

#### 1. validate-spec
- **목적**: PM Agent가 생성한 명세서 검증
- **입력**: 티켓 번호
- **출력**: 검증 리포트 (에러, 경고, Auto-fix)
- **사용**: PM Agent 작업 완료 후 자동

```bash
bash scripts/run-skill.sh validate-spec PLAN-001
bash scripts/run-skill.sh validate-spec PLAN-001 --auto-fix
```

**검증 항목**:
- ✅ 완전성: Acceptance Criteria 충족
- ✅ 범위: Out-of-Scope 준수
- ✅ 품질: API 명세, UI 요구사항 완성도

#### 2. review-pr
- **목적**: Pull Request 자동 리뷰
- **입력**: PR 번호 또는 현재 브랜치
- **출력**: 리뷰 리포트 (이슈, Auto-fix 제안)
- **사용**: PR 생성 후

```bash
bash scripts/run-skill.sh review-pr 123
bash scripts/run-skill.sh review-pr --current-branch
bash scripts/run-skill.sh review-pr 123 --auto-fix
```

**리뷰 카테고리**:
- 완전성 (테스트 존재, TODO 없음)
- 품질 (함수 길이, 복잡도)
- 보안 (하드코딩 비밀번호, SQL Injection, XSS)
- 스타일 (Linter 통과)
- 성능 (N+1 쿼리)

#### 3. refactor-code
- **목적**: 코드 리팩토링 제안
- **입력**: 파일 또는 디렉토리
- **출력**: 리팩토링 리포트 (코드 스멜, 제안)
- **사용**: Coding Agent 작업 완료 후 (선택)

```bash
bash scripts/run-skill.sh refactor-code --file src/auth/login.js
bash scripts/run-skill.sh refactor-code --dir src/auth/
bash scripts/run-skill.sh refactor-code --file src/auth/login.js --auto-fix
```

**감지 패턴**:
- Long Method (> 50줄)
- Duplicate Code (6줄 이상)
- Magic Numbers
- God Object (> 300줄)
- N+1 쿼리

---

### Development (3개)

#### 4. commit
- **목적**: 커밋 메시지 자동 생성
- **입력**: 티켓 번호
- **출력**: 커밋 메시지 + 실행
- **사용**: QA Agent 작업 완료 후 자동

```bash
bash scripts/run-skill.sh commit --ticket PLAN-001
bash scripts/run-skill.sh commit --ticket PLAN-001 --dry-run
```

**자동 결정**:
- 커밋 타입 (feat/fix/test/docs/refactor/chore/style)
- Subject (70자 이하, 명령형)
- Body (변경 파일 목록, 3개 이상 시)
- Footer (Closes #PLAN-001, Co-Authored-By)

#### 5. test-runner
- **목적**: 테스트 자동 실행
- **입력**: 테스트 범위 (all/file/dir)
- **출력**: 테스트 리포트 (통과/실패, 커버리지)
- **사용**: QA Agent 작업 완료 후 필수

```bash
bash scripts/run-skill.sh test-runner --all --coverage
bash scripts/run-skill.sh test-runner --file tests/auth/test_login.py
bash scripts/run-skill.sh test-runner --unit
```

**검증**:
- 모든 테스트 통과 (실패 0개)
- 커버리지 80% 이상
- Flaky 테스트 감지
- 느린 테스트 감지 (> 1초)

#### 6. docs-generator
- **목적**: 문서 자동 생성
- **입력**: 생성 범위 (api/readme/changelog)
- **출력**: 문서 파일
- **사용**: API 변경 시 자동

```bash
bash scripts/run-skill.sh docs-generator --all
bash scripts/run-skill.sh docs-generator --api
bash scripts/run-skill.sh docs-generator --readme
```

**생성 항목**:
- API 문서 (OpenAPI, GraphQL)
- README (Features, API, 환경 변수)
- Changelog (Git 커밋에서)
- 예제 코드 (Python, JavaScript, curl)

---

### Operations (2개)

#### 7. deploy
- **목적**: 배포 자동화
- **입력**: 환경 (dev/staging/production)
- **출력**: 배포 리포트
- **사용**: PR 머지 후 (선택)

```bash
bash scripts/run-skill.sh deploy --env staging
bash scripts/run-skill.sh deploy --env production --dry-run
bash scripts/run-skill.sh deploy --rollback --env production
```

**배포 전략**:
- Blue-Green (무중단)
- Canary (10% → 50% → 100%)
- Rolling (순차적)

#### 8. benchmark
- **목적**: 성능 벤치마크
- **입력**: 비교 대상 (main 브랜치 등)
- **출력**: 벤치마크 리포트 (회귀 여부)
- **사용**: 배포 전 (선택)

```bash
bash scripts/run-skill.sh benchmark --all
bash scripts/run-skill.sh benchmark --compare-to main
bash scripts/run-skill.sh benchmark --load-test --users 1000
```

**감지**:
- 응답 시간 증가 > 20% (차단)
- 처리량 감소 > 15% (차단)
- 메모리 증가 > 30% (경고)

---

## 🔄 에이전트별 Skills 사용

### PM Agent

**작업 흐름**:
```
티켓 읽기 → 명세서 생성 → validate-spec skill
```

**Skills 호출**:
1. **validate-spec** (필수)
   - 시점: 명세서 생성 완료 후
   - 목적: 완전성, 범위, 품질 검증
   - 실패 시: Auto-fix 시도 → 재실행

**CLAUDE.md 추가 내용**:
```markdown
## 🛠️ Skills 통합

### 명세서 검증 (자동)

명세서 파일 생성이 완료되면:

```bash
bash scripts/run-skill.sh validate-spec {티켓번호}
```

검증 실패 시:
- Auto-fix 시도
- Auto-fix 불가능한 이슈: 수동 수정 후 재검증

검증 통과 조건:
- 에러 0개
- 경고 3개 이하
```

---

### Coding Agent

**작업 흐름**:
```
명세서 읽기 → 코드 작성 → refactor-code skill (선택)
```

**Skills 호출**:
1. **refactor-code** (선택)
   - 시점: 코드 작성 완료 후
   - 목적: 코드 스멜 감지, 리팩토링 제안
   - 적용: Auto-fix 또는 수동

2. **commit** (자동, auto-pipeline에서)
   - 시점: QA Agent 완료 후
   - 목적: 일관된 커밋 메시지

**CLAUDE.md 추가 내용**:
```markdown
## 🛠️ Skills 통합

### 1. refactor-code skill (선택)

코드 작성 완료 후:

```bash
bash scripts/run-skill.sh refactor-code --dir src/
```

제안 적용:
- Auto-fix: --auto-fix 플래그
- 수동: 리포트 참고하여 개선

### 2. commit skill (자동)

커밋 메시지 자동 생성 (auto-pipeline):
- 타입 자동 결정
- Subject 생성 (70자 이하)
- Body/Footer 추가
```

---

### QA Agent

**작업 흐름**:
```
테스트 케이스 읽기 → 테스트 작성 → test-runner skill
```

**Skills 호출**:
1. **test-runner** (필수)
   - 시점: 테스트 작성 완료 후
   - 목적: 테스트 실행, 커버리지 측정
   - 실패 시: 재실행 필요

2. **review-pr** (PR 생성 후, auto-pipeline에서)
   - 시점: PR 생성 시
   - 목적: 자동 리뷰
   - 적용: Auto-fix

**CLAUDE.md 추가 내용**:
```markdown
## 🛠️ Skills 통합

### 1. test-runner skill (필수)

테스트 작성 완료 후:

```bash
bash scripts/run-skill.sh test-runner --all --coverage
```

검증:
- 모든 테스트 통과
- 커버리지 80% 이상
- Flaky 테스트 감지

실패 시:
- 원인 분석
- 수정 후 재실행

### 2. review-pr skill (PR 생성 후)

자동 리뷰 (auto-pipeline):
- 완전성, 품질, 보안 검사
- Auto-fix 제안
```

---

## 📊 auto-pipeline 통합

### 전체 파이프라인

```python
# Step 1: PM Agent
result_pm = run_agent("pm", ticket_content, ticket_num)

# Step 1.5: validate-spec skill
validation = run_skill("validate-spec", ticket_num, auto_fix=True)
if not validation["passed"]:
    # PM Agent 재실행
    result_pm = run_agent("pm", retry_prompt, ticket_num)

# Step 2: Coding Agent
result_coding = run_agent("coding", coding_prompt, ticket_num)

# Step 2.5: refactor-code skill (선택)
refactor = run_skill("refactor-code", changed_files)

# Step 3: QA Agent
result_qa = run_agent("qa", qa_prompt, ticket_num)

# Step 3.5: test-runner skill (필수)
test = run_skill("test-runner", "--all --coverage")
if not test["all_passed"]:
    raise Exception("테스트 실패")

# Step 4: commit skill
commit = run_skill("commit", ticket_num)

# Step 5: docs-generator skill (API 변경 시)
if has_api_changes():
    docs = run_skill("docs-generator", "--api --readme")

# Step 6: PR 생성 및 review-pr skill
pr_num = create_pr(ticket_num)
review = run_skill("review-pr", pr_num, auto_fix=True)
```

---

## ⚠️ Skills 사용 시 주의사항

### 1. 에러 처리

```python
# ✅ 올바름: 에러 체크
result = run_skill("validate-spec", ticket_num)
if not result["success"]:
    print(f"❌ 스킬 실패: {result['error']}")
    # 대응 로직

# ❌ 잘못: 에러 무시
run_skill("validate-spec", ticket_num)
# 계속 진행...
```

### 2. 필수 vs 선택

**필수 Skills** (파이프라인 차단):
- validate-spec (PM Agent 후)
- test-runner (QA Agent 후)
- commit (모든 변경사항)

**선택 Skills** (권장):
- refactor-code (코드 품질)
- docs-generator (API 변경 시)
- benchmark (성능 중요 시)

### 3. Auto-fix 사용

```python
# 간단한 이슈: Auto-fix 시도
result = run_skill("review-pr", pr_num, auto_fix=True)

# 복잡한 이슈: 수동 수정
if result["manual_fixes_needed"]:
    print("수동 수정 필요:")
    for issue in result["manual_fixes"]:
        print(f"  - {issue}")
```

---

## 📈 기대 효과

### Before (Skills 없이)

```
PM Agent → 수동 검증 (10분)
Coding Agent → 수동 리뷰 (30분)
QA Agent → 수동 테스트 실행 (5분)
수동 커밋 (5분)
수동 PR 리뷰 (수 시간)
```

**문제점**:
- ❌ 시간 소요 (1시간+)
- ❌ 일관성 없음
- ❌ 실수 가능

### After (Skills 통합)

```
PM Agent → validate-spec (1분)
Coding Agent → refactor-code (1분)
QA Agent → test-runner (2분)
commit skill (5초)
review-pr skill (2분)
```

**개선점**:
- ✅ 빠름 (~6분)
- ✅ 100% 일관성
- ✅ 자동 검증

### 수치

| 항목 | Before | After | 개선율 |
|------|--------|-------|--------|
| 검증 시간 | 10분 | 1분 | -90% |
| 테스트 실행 | 5분 | 2분 | -60% |
| 커밋 작성 | 5분 | 5초 | -98% |
| PR 리뷰 | 수 시간 | 2분 | -95%+ |

---

## 🔗 관련 문서

- [Skills 개별 문서](../.skills/)
  - [validate-spec](../.skills/validate-spec/skill.md)
  - [commit](../.skills/commit/skill.md)
  - [review-pr](../.skills/review-pr/skill.md)
  - [refactor-code](../.skills/refactor-code/skill.md)
  - [test-runner](../.skills/test-runner/skill.md)
  - [deploy](../.skills/deploy/skill.md)
  - [benchmark](../.skills/benchmark/skill.md)
  - [docs-generator](../.skills/docs-generator/skill.md)

- [auto_pipeline.py](../scripts/auto_pipeline.py) - Skills 통합 코드
- [run-skill.sh](../scripts/run-skill.sh) - Skills 실행 스크립트
