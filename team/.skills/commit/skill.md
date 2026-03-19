# Commit Skill

> **목적**: 프로젝트 규약에 따라 시맨틱 커밋 메시지 자동 생성
>
> **타입**: Code Quality Skill
>
> **Thariq 교훈**: "Skills for repetitive workflows"

---

## 🎯 트리거

### 자동 트리거
- Auto-pipeline: Coding Agent + QA Agent 완료 후
- Git pre-commit hook: 커밋 전 자동 실행

### 수동 트리거
```bash
# 명령어
bash scripts/run-skill.sh commit PLAN-001

# 또는 직접
python3 .skills/commit/commit-message-generator.py --ticket PLAN-001
```

---

## 📋 프로세스

### 1. Git Diff 분석

```bash
# 변경 사항 확인
git diff --cached --stat
git diff --cached --name-status
```

**추출 정보**:
- 변경된 파일 목록
- 파일 타입 (추가/수정/삭제)
- 변경 줄 수

### 2. 커밋 타입 결정

**규칙**:
- **feat**: 새 기능 추가 (A 파일, 새 함수/클래스)
- **fix**: 버그 수정 (M 파일, 에러 핸들링 추가)
- **test**: 테스트 추가/수정 (test/, spec/ 파일)
- **docs**: 문서만 변경 (README, *.md)
- **refactor**: 리팩토링 (M 파일, 기능 변경 없음)
- **style**: 포맷팅 (공백, 세미콜론 등)
- **chore**: 빌드/설정 변경 (package.json, .gitignore)

**자동 판단 로직**:
```python
def determine_type(changed_files):
    if any("test" in f or "spec" in f for f in changed_files):
        return "test"
    elif all(f.endswith(".md") for f in changed_files):
        return "docs"
    elif any(f in ["package.json", ".gitignore", "tsconfig.json"] for f in changed_files):
        return "chore"
    else:
        # Git diff 내용 분석
        added_lines = count_added_lines()
        modified_lines = count_modified_lines()

        if added_lines > modified_lines * 2:
            return "feat"
        else:
            return "fix"  # 기본값
```

### 3. Scope 추출

**티켓 번호 기반**:
```python
scope = ticket_num  # PLAN-001
```

**또는 파일 경로 기반**:
```python
# src/auth/login.js 변경 → scope: auth
# src/user/profile.js 변경 → scope: user
```

### 4. Subject 생성

**규칙**:
- 명령형 (implement, fix, add, update)
- 70자 이하
- 첫 글자 소문자
- 마침표 없음

**생성 로직**:
```python
def generate_subject(commit_type, changed_files, ticket_description):
    if commit_type == "feat":
        verb = "implement" or "add"
    elif commit_type == "fix":
        verb = "fix"
    elif commit_type == "test":
        verb = "add tests for"

    # 티켓 설명에서 핵심 키워드 추출
    keywords = extract_keywords(ticket_description)

    subject = f"{verb} {keywords}"

    # 70자 제한
    if len(subject) > 70:
        subject = subject[:67] + "..."

    return subject
```

### 5. Body 생성 (선택)

**포함 내용**:
- 변경 이유 (why)
- 주요 변경 사항 (what)
- 파일 경로 (if needed)

**생성 조건**:
- 파일 3개 이상 변경
- 또는 100줄 이상 변경
- 또는 복잡한 변경 (리팩토링, 마이그레이션)

### 6. Footer 추가

**필수 포함**:
```
Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**선택 포함**:
```
Breaking-Change: API 엔드포인트 변경
Refs: #PLAN-002, #PLAN-003
```

---

## 📤 출력 형식

### 기본 템플릿

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 예시 1: Feature

```
feat(PLAN-001): implement JWT authentication

Added login/logout endpoints with token generation.
Password hashing uses bcrypt with salt rounds=12.

Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 예시 2: Bug Fix

```
fix(PLAN-003): resolve null pointer in user profile

Fixed crash when user has no avatar image.
Added null check before accessing avatar.url property.

Closes #PLAN-003
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 예시 3: Test

```
test(PLAN-005): add unit tests for payment module

Covers success cases, edge cases, and error handling.

Closes #PLAN-005
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## 🧠 메모리 활용

### commit-history.json

**목적**: 프로젝트별 일관된 어휘 학습

```json
{
  "project": "my-todo-app",
  "vocabulary": {
    "auth": ["authentication", "login", "logout", "token"],
    "user": ["profile", "settings", "preferences"],
    "task": ["todo", "item", "completion"]
  },
  "frequent_verbs": {
    "feat": ["implement", "add", "create"],
    "fix": ["fix", "resolve", "correct"],
    "refactor": ["refactor", "improve", "optimize"]
  },
  "recent_commits": [
    {
      "hash": "abc123",
      "message": "feat(PLAN-001): implement user authentication",
      "files": ["src/auth/login.js", "src/auth/token.js"],
      "timestamp": "2026-03-19T10:00:00Z"
    }
  ]
}
```

**학습 방법**:
```python
def learn_from_history():
    # Git log에서 최근 50개 커밋 분석
    commits = git_log(limit=50)

    # 자주 사용되는 단어 추출
    vocabulary = extract_vocabulary(commits)

    # 일관성 체크 (같은 scope에 같은 용어 사용)
    consistency_score = check_consistency(commits)

    # commit-history.json 업데이트
```

---

## ⚠️ Gotchas

### 1. Subject에 파일 경로 포함 금지

❌ **잘못된 예시**:
```
feat(PLAN-001): implement src/auth/login.js
```

✅ **올바른 예시**:
```
feat(PLAN-001): implement user authentication

Files modified:
- src/auth/login.js
- src/auth/token.js
```

### 2. 테스트 실패 시 커밋 금지

**검증**:
```bash
# 커밋 전 테스트 실행
npm test || exit 1
pytest || exit 1
```

**Auto-pipeline 통합**:
```python
# QA Agent 완료 확인 후 커밋
if qa_result["all_tests_passed"]:
    run_skill("commit", ticket_num)
else:
    print("테스트 실패 - 커밋 생략")
```

### 3. 여러 티켓의 변경 혼합 금지

**검출**:
```python
# 변경된 파일에서 티켓 번호 추출
files_tickets = extract_tickets_from_files(changed_files)

if len(files_tickets) > 1:
    print("⚠️  여러 티켓의 변경 감지. 티켓별로 커밋하세요.")
    sys.exit(1)
```

### 4. 빈 커밋 방지

**검증**:
```bash
git diff --cached --quiet
if [ $? -eq 0 ]; then
    echo "변경 사항 없음 - 커밋 생략"
    exit 0
fi
```

---

## 🔧 사용법

### 수동 실행

```bash
# 기본
bash scripts/run-skill.sh commit PLAN-001

# Dry-run (실제 커밋 안 함)
bash scripts/run-skill.sh commit PLAN-001 --dry-run

# 메시지만 생성 (승인 후 커밋)
bash scripts/run-skill.sh commit PLAN-001 --generate-only
```

### Auto-pipeline 통합

```python
# auto_pipeline.py

# QA Agent 완료 후
result_qa = self.run_agent("qa", qa_prompt, ticket_num)

# Commit Skill 실행
commit_result = self.run_skill("commit", ticket_num)

if commit_result["success"]:
    print(f"✅ 커밋 완료: {commit_result['commit_hash']}")
else:
    print(f"❌ 커밋 실패: {commit_result['error']}")
```

### Git Hook 통합

```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash

# 커밋 메시지 파일
COMMIT_MSG_FILE=$1

# Commit Skill 실행하여 메시지 생성
python3 .skills/commit/commit-message-generator.py --ticket $TICKET_NUM > $COMMIT_MSG_FILE
```

---

## 📊 기대 효과

### Before (수동 커밋 메시지)

```
수동 작성 → 불일치
    ↓
"fix bug"
"update code"
"wip"
```

**문제점**:
- ❌ 일관성 없음
- ❌ 정보 부족
- ❌ 시간 소요

### After (Commit Skill)

```
자동 생성 → 일관성
    ↓
"feat(PLAN-001): implement user authentication"
"fix(PLAN-002): resolve login validation error"
"test(PLAN-003): add integration tests for API"
```

**개선점**:
- ✅ 일관된 형식
- ✅ 명확한 정보
- ✅ 자동화

### 수치 목표

| 항목 | 목표 |
|------|------|
| **커밋 메시지 품질** | **+60%** |
| **작성 시간** | **-90%** (수동 대비) |
| **프로젝트 간 재사용** | **100%** |
| **Git history 가독성** | **+80%** |

---

## 🔗 통합

### 다른 Skill과의 연계

**validate-spec → commit**:
```
명세서 검증 통과 → Coding Agent → QA Agent → Commit Skill
```

**refactor-code → commit**:
```
리팩토링 제안 → 적용 → Commit Skill (type=refactor)
```

### 메모리 시스템 연계

**patterns.json 참조**:
```python
# 과거 성공한 커밋 메시지 패턴 활용
patterns = load_patterns("commit")

if patterns:
    # 유사한 변경 → 유사한 메시지 구조 사용
    similar_commit = find_similar(current_changes, patterns)
    message_template = similar_commit["message_template"]
```

---

## 📝 로그

**커밋 로그**: `projects/{project}/logs/commit/{timestamp}-{ticket}.json`

```json
{
  "ticket": "PLAN-001",
  "timestamp": "2026-03-19T10:30:00Z",
  "commit_hash": "abc123def456",
  "commit_type": "feat",
  "scope": "PLAN-001",
  "subject": "implement user authentication",
  "changed_files": ["src/auth/login.js", "src/auth/token.js"],
  "added_lines": 150,
  "deleted_lines": 10,
  "confidence": 0.92,
  "auto_generated": true
}
```

---

**관련 문서**:
- [commit-message-generator.py](commit-message-generator.py) - 실제 구현
- [commit-history.json](../../.memory/commit-history.json) - 학습 데이터
- [Phase 3.1 문서](../../../docs/phase3.1-complete.md)
