# Review PR Skill

> **목적**: Pull Request 자동 리뷰 - 코드 품질 검사 및 개선 제안
>
> **타입**: Code Quality Skill
>
> **Thariq 교훈**: "Validation skills catch errors early"

---

## 🎯 트리거

### 자동 트리거
- Auto-pipeline: PR 생성 직후
- GitHub Actions: PR 이벤트 발생 시
- Git hook: pre-push

### 수동 트리거
```bash
# PR 번호로 리뷰
bash scripts/run-skill.sh review-pr 123

# 현재 브랜치 리뷰
bash scripts/run-skill.sh review-pr --current-branch

# 특정 티켓 리뷰
bash scripts/run-skill.sh review-pr --ticket PLAN-001
```

---

## 📋 리뷰 체크리스트

### 1. 완전성 검사 (Completeness)

**티켓 요구사항 충족**:
- [ ] 티켓의 Acceptance Criteria 모두 구현
- [ ] Out-of-Scope 항목 구현 안 됨
- [ ] 명세서와 구현 일치

**코드 완전성**:
- [ ] 모든 함수에 구현 존재 (TODO, FIXME 없음)
- [ ] 에러 핸들링 존재
- [ ] 엣지 케이스 처리

**테스트 완전성**:
- [ ] 유닛 테스트 존재
- [ ] 통합 테스트 존재 (필요 시)
- [ ] 테스트 커버리지 80% 이상

### 2. 품질 검사 (Quality)

**코드 품질**:
- [ ] 함수 길이 < 50줄
- [ ] 순환 복잡도 < 10
- [ ] 중복 코드 없음
- [ ] 네이밍 명확 (변수, 함수, 클래스)
- [ ] 매직 넘버 없음 (상수 사용)

**아키텍처**:
- [ ] 단일 책임 원칙 (SRP)
- [ ] DRY (Don't Repeat Yourself)
- [ ] 코딩 룰 준수 (.rules/ 참조)

**보안**:
- [ ] 하드코딩된 비밀번호/API 키 없음
- [ ] SQL Injection 방어
- [ ] XSS 방어
- [ ] CSRF 방어 (필요 시)
- [ ] 입력 검증 존재

### 3. 스타일 검사 (Style)

**포맷팅**:
- [ ] Linter 통과 (ESLint, Pylint 등)
- [ ] 일관된 들여쓰기
- [ ] 일관된 괄호 스타일
- [ ] 불필요한 공백 없음

**주석**:
- [ ] 복잡한 로직에 주석
- [ ] 주석 오타 없음
- [ ] 주석된 코드 없음 (삭제)

### 4. 성능 검사 (Performance)

**일반**:
- [ ] N+1 쿼리 없음
- [ ] 불필요한 반복문 없음
- [ ] 메모리 누수 없음

**비동기**:
- [ ] Async/await 적절히 사용
- [ ] Promise 체인 최적화
- [ ] 병렬 처리 가능한 작업 병렬화

### 5. 문서화 검사 (Documentation)

**코드 문서**:
- [ ] 공개 API에 docstring/JSDoc
- [ ] 복잡한 알고리즘 설명

**변경 문서**:
- [ ] CHANGELOG 업데이트 (필요 시)
- [ ] README 업데이트 (API 변경 시)

---

## 🔍 자동 검사 항목

### Static Analysis

```python
def run_static_analysis(files):
    issues = []

    # Linter
    lint_result = run_linter(files)
    issues.extend(lint_result)

    # Complexity
    complexity = calculate_complexity(files)
    if complexity > 10:
        issues.append({
            "type": "complexity",
            "severity": "warning",
            "message": f"Cyclomatic complexity too high: {complexity}"
        })

    # Security
    security_issues = run_security_scan(files)
    issues.extend(security_issues)

    return issues
```

**도구 통합**:
- ESLint / Pylint - 스타일 검사
- Bandit / Safety - 보안 검사
- SonarQube - 코드 품질
- Coverage.py / Istanbul - 커버리지

### Pattern Detection

**안티패턴 감지**:
```python
anti_patterns = [
    {
        "name": "God Object",
        "pattern": r"class \w+ {[\s\S]{2000,}}",  # 2000+ 줄 클래스
        "severity": "error"
    },
    {
        "name": "Magic Number",
        "pattern": r"if.*==\s*\d{2,}",  # 2자리 이상 숫자
        "severity": "warning"
    },
    {
        "name": "Hardcoded Secret",
        "pattern": r"(password|api_key|secret)\s*=\s*['\"]",
        "severity": "error"
    }
]
```

---

## 📤 출력 형식

### 리뷰 리포트

```markdown
# PR Review: #123 - Implement User Authentication

## Summary
- **Status**: ⚠️ Changes Requested
- **Reviewed Files**: 5
- **Issues Found**: 3 errors, 2 warnings
- **Test Coverage**: 85% ✅
- **Estimated Review Time**: 15 minutes

---

## Critical Issues (3)

### 1. Security: Hardcoded API Key
**File**: `src/auth/api-client.js:12`
**Severity**: 🔴 Error

```javascript
const API_KEY = "sk-1234567890abcdef";  // ❌
```

**Suggestion**:
```javascript
const API_KEY = process.env.API_KEY;  // ✅
```

**Auto-fix**: Available

---

### 2. Code Quality: Function Too Long
**File**: `src/auth/login.js:45-120`
**Severity**: 🔴 Error

Function `handleLogin` is 75 lines long (limit: 50).

**Suggestion**: Extract validation logic to separate function.

**Auto-fix**: Not available (manual refactoring needed)

---

## Warnings (2)

### 1. Style: Inconsistent Naming
**File**: `src/auth/token.js:23`
**Severity**: 🟡 Warning

```javascript
const JWT_token = generateToken();  // camelCase + PascalCase 혼합
```

**Suggestion**:
```javascript
const jwtToken = generateToken();  // ✅
```

---

## Suggestions

### Performance Optimization
Consider using parallel API calls in `src/auth/verify.js:34`:
```javascript
// Before
const user = await fetchUser(id);
const permissions = await fetchPermissions(id);

// After
const [user, permissions] = await Promise.all([
  fetchUser(id),
  fetchPermissions(id)
]);
```

---

## Test Coverage

| File | Coverage | Status |
|------|----------|--------|
| src/auth/login.js | 90% | ✅ |
| src/auth/token.js | 85% | ✅ |
| src/auth/verify.js | 75% | ⚠️ |

**Overall**: 85% ✅

---

## Approval Status

❌ **Changes Requested**

Please fix 3 critical issues before approval.

**Auto-fixable**: 1 issue
Run: `bash scripts/run-skill.sh review-pr 123 --auto-fix`
```

---

## 🔧 Auto-Fix 기능

### 수정 가능한 이슈

1. **하드코딩 비밀번호**:
   ```python
   "password": "admin123" → "password": process.env.PASSWORD
   ```

2. **Import 정렬**:
   ```python
   # 알파벳 순 정렬
   import z_module
   import a_module
   →
   import a_module
   import z_module
   ```

3. **불필요한 공백**:
   ```python
   # 제거
   function foo()  {  // 2개 공백
   →
   function foo() {  // 1개 공백
   ```

4. **주석된 코드 삭제**:
   ```python
   # const oldCode = ...;
   # console.log(oldCode);
   → (삭제)
   ```

### Auto-fix 실행

```bash
# 자동 수정 적용
bash scripts/run-skill.sh review-pr 123 --auto-fix

# 수정 사항 미리보기
bash scripts/run-skill.sh review-pr 123 --auto-fix --dry-run
```

---

## ⚠️ Gotchas

### 1. 테스트 없는 PR 차단

**검증**:
```python
if not has_tests(changed_files):
    return {
        "status": "blocked",
        "message": "모든 PR은 테스트를 포함해야 합니다."
    }
```

### 2. 커버리지 감소 방지

**검증**:
```python
old_coverage = get_coverage("main")
new_coverage = get_coverage("feature-branch")

if new_coverage < old_coverage - 5:  # 5% 이상 감소
    return {
        "status": "warning",
        "message": f"커버리지 감소: {old_coverage}% → {new_coverage}%"
    }
```

### 3. 대용량 PR 경고

**검증**:
```python
if lines_changed > 500:
    return {
        "status": "warning",
        "message": "PR이 너무 큽니다 (500+ 줄). 분리를 고려하세요."
    }
```

### 4. Breaking Change 감지

**검증**:
```python
if has_breaking_changes(diff):
    return {
        "status": "warning",
        "message": "Breaking Change 감지. CHANGELOG에 명시하세요."
    }
```

---

## 🔗 통합

### GitHub Actions 통합

```yaml
# .github/workflows/review-pr.yml
name: Auto PR Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run review-pr skill
        run: |
          bash scripts/run-skill.sh review-pr ${{ github.event.pull_request.number }}
      - name: Post comment
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

### Auto-pipeline 통합

```python
# auto_pipeline.py

# QA Agent 완료 후 PR 생성
pr_number = create_pull_request(ticket_num, branch_name)

# PR 리뷰 실행
review_result = self.run_skill("review-pr", pr_number)

if review_result["status"] == "approved":
    print("✅ PR 승인 - 머지 가능")
elif review_result["auto_fixable_count"] > 0:
    print(f"⚠️  {review_result['auto_fixable_count']}개 이슈 자동 수정 가능")
    # Auto-fix 실행
    self.run_skill("review-pr", pr_number, auto_fix=True)
else:
    print(f"❌ {review_result['error_count']}개 수동 수정 필요")
```

---

## 🧠 메모리 활용

### review-history.json

```json
{
  "project": "my-project",
  "common_issues": [
    {
      "issue": "Hardcoded API Key",
      "frequency": 12,
      "auto_fixed": 10,
      "last_seen": "2026-03-15"
    },
    {
      "issue": "Missing Error Handling",
      "frequency": 8,
      "auto_fixed": 0,
      "last_seen": "2026-03-18"
    }
  ],
  "approval_criteria": {
    "min_coverage": 80,
    "max_complexity": 10,
    "max_function_length": 50
  }
}
```

---

## 📊 기대 효과

### Before (수동 리뷰)

```
PR 생성 → 사람 리뷰 대기 (수 시간~수 일)
       → 코멘트
       → 수정
       → 재리뷰
```

**문제점**:
- ❌ 느림 (대기 시간)
- ❌ 일관성 없음 (리뷰어 차이)
- ❌ 간단한 이슈도 사람 확인

### After (자동 리뷰)

```
PR 생성 → review-pr skill (즉시)
       → 리포트 생성 (1-2분)
       → Auto-fix 적용 (선택)
       → 사람 리뷰 (복잡한 로직만)
```

**개선점**:
- ✅ 빠름 (즉시 피드백)
- ✅ 일관성 (체크리스트 기반)
- ✅ 간단한 이슈 자동 수정

### 수치 목표

| 항목 | 목표 |
|------|------|
| **리뷰 시간** | **-80%** (수동 대비) |
| **간단한 이슈 포착** | **95%+** |
| **Auto-fix 성공률** | **80%+** |
| **사람 리뷰 부담** | **-60%** |

---

## 📝 로그

**리뷰 로그**: `projects/{project}/logs/review-pr/{timestamp}-PR-{number}.json`

```json
{
  "pr_number": 123,
  "timestamp": "2026-03-19T10:30:00Z",
  "status": "changes_requested",
  "errors": 3,
  "warnings": 2,
  "suggestions": 1,
  "auto_fixable": 1,
  "files_reviewed": 5,
  "test_coverage": 0.85,
  "review_time_seconds": 45
}
```

---

**관련 문서**:
- [review-pr.py](review-pr.py) - 실제 구현
- [review-checklist.json](review-checklist.json) - 체크리스트 설정
- [auto-fix-rules.json](auto-fix-rules.json) - Auto-fix 규칙
