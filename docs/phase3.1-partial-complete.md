# Phase 3.1 부분 완료: Skill 기반 아키텍처 (commit skill) ✅

> **일시**: 2026-03-19
> **Phase**: 3.1 - Skill 기반 아키텍처 (점진적 마이그레이션)
> **소요 시간**: ~20분
> **상태**: ⚠️ 부분 완료 (commit skill만)

---

## 🎯 목표

**하이브리드 Agent-Skill 아키텍처 구축**
- 에이전트 유지 (기존 시스템 보존)
- Skills 점진 추가 (독립적인 작업부터)
- 재사용 가능한 워크플로우

---

## 📦 Phase 3.1 - commit skill 생성

### 생성된 파일 (3개)

| 파일 | 줄 수 | 설명 |
|------|-------|------|
| `team/.skills/commit/skill.md` | 387줄 | Commit Skill 문서 |
| `team/.skills/commit/commit-message-generator.py` | 389줄 | 커밋 메시지 자동 생성 스크립트 |
| `team/.memory/commit-history.json` | 43줄 | 커밋 히스토리 학습 데이터 |

**총**: 819줄

**수정된 파일**:
- `team/scripts/run-skill.sh`: commit 스킬 추가 (+3줄)

---

## 🔧 commit skill 기능

### 1. Git Diff 자동 분석

```bash
# 변경된 파일 확인
git diff --cached --name-status
```

**추출 정보**:
- 변경된 파일 목록
- 파일 상태 (A=추가, M=수정, D=삭제)
- 파일 타입

### 2. 커밋 타입 자동 결정

**규칙 기반 판단**:
- `feat`: 새 파일 추가 많음 (A > M)
- `fix`: 기존 파일 수정 많음 (M > A)
- `test`: test/ 또는 spec/ 파일
- `docs`: .md 파일만
- `chore`: package.json, .gitignore 등 설정 파일
- `refactor`: 기능 변경 없이 수정

**자동 판단 로직**:
```python
def determine_type(changed_files):
    if any("test" in f or "spec" in f for f in files):
        return "test"
    elif all(f.endswith(".md") for f in files):
        return "docs"
    elif added_count > modified_count:
        return "feat"
    else:
        return "fix"  # 기본값
```

### 3. Subject 자동 생성

**입력**:
- 커밋 타입
- 변경 파일 경로
- 티켓 설명 (선택)

**출력**:
- 명령형 동사 (implement, fix, add)
- 70자 이하
- 소문자 시작

**예시**:
```
feat(PLAN-001): implement user authentication
fix(PLAN-002): resolve login validation error
test(PLAN-003): add integration tests for API
```

### 4. Body 자동 생성 (조건부)

**생성 조건**:
- 파일 3개 이상 변경
- 또는 타입이 refactor/feat

**내용**:
- 변경 이유 (선택)
- 파일 목록 (최대 5개)

### 5. Footer 자동 추가

**필수 포함**:
```
Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## 📤 출력 예시

### 예시 1: Feature

```
feat(PLAN-001): implement JWT authentication

Added new functionality:
- src/auth/login.js
- src/auth/token.js
- src/auth/middleware.js

Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 예시 2: Bug Fix

```
fix(PLAN-003): resolve null pointer in user profile

Closes #PLAN-003
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 예시 3: Test

```
test(PLAN-005): add unit tests for payment module

Closes #PLAN-005
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## 🚀 사용법

### 수동 실행

```bash
# 기본 - 메시지 생성 및 커밋
bash scripts/run-skill.sh commit --ticket PLAN-001

# Dry-run - 메시지만 확인
bash scripts/run-skill.sh commit --ticket PLAN-001 --dry-run

# 메시지만 생성 (승인 후 커밋)
bash scripts/run-skill.sh commit --ticket PLAN-001 --generate-only
```

### Auto-pipeline 통합 (향후)

```python
# auto_pipeline.py

# QA Agent 완료 후
result_qa = self.run_agent("qa", qa_prompt, ticket_num)

if result_qa["all_tests_passed"]:
    # Commit Skill 실행
    commit_result = self.run_skill("commit", ticket_num)

    if commit_result["success"]:
        print(f"✅ 커밋 완료: {commit_result['commit_hash']}")
```

### Git Hook 통합 (선택)

```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash

TICKET_NUM=$(git branch --show-current | grep -oP 'PLAN-\d+')

if [ -n "$TICKET_NUM" ]; then
    python3 .skills/commit/commit-message-generator.py --ticket $TICKET_NUM --generate-only > $1
fi
```

---

## 🧠 메모리 시스템 연계

### commit-history.json 구조

```json
{
  "project": "my-project",
  "vocabulary": {
    "auth": ["authentication", "login", "logout", "token"],
    "user": ["profile", "settings", "account"]
  },
  "frequent_verbs": {
    "feat": ["implement", "add", "create"],
    "fix": ["fix", "resolve", "correct"]
  },
  "recent_commits": [
    {
      "hash": "abc123",
      "message": "feat(PLAN-001): implement user authentication",
      "files": ["src/auth/login.js"],
      "timestamp": "2026-03-19T10:00:00Z"
    }
  ]
}
```

**학습 방법** (향후 구현):
```python
def learn_from_git_history():
    # Git log에서 최근 50개 커밋 분석
    commits = git_log(limit=50)

    # 자주 사용되는 어휘 추출
    vocabulary = extract_vocabulary(commits)

    # 일관성 점수 계산
    consistency = check_consistency(commits)

    # commit-history.json 업데이트
```

---

## ⚠️ Gotchas (skill 내장)

### 1. Subject에 파일 경로 포함 금지

❌ 잘못:
```
feat(PLAN-001): implement src/auth/login.js
```

✅ 올바름:
```
feat(PLAN-001): implement user authentication
```

### 2. 테스트 실패 시 커밋 금지

**검증**:
```bash
# QA Agent 완료 확인
if qa_result["all_tests_passed"]:
    run_skill("commit")
```

### 3. 여러 티켓 혼합 금지

**검출**:
```python
# 변경 파일에서 티켓 번호 추출
if len(set(tickets)) > 1:
    print("⚠️  여러 티켓의 변경 감지. 티켓별로 커밋하세요.")
```

### 4. 빈 커밋 방지

**검증**:
```bash
git diff --cached --quiet
if [ $? -eq 0 ]; then
    echo "변경 사항 없음"
    exit 0
fi
```

---

## 📊 기대 효과

### Before (수동 커밋)

```
개발자 작성:
- "fix bug"
- "update code"
- "wip"
- "test"
```

**문제점**:
- ❌ 일관성 없음
- ❌ 정보 부족
- ❌ Git history 가독성 낮음

### After (commit skill)

```
자동 생성:
- "feat(PLAN-001): implement user authentication"
- "fix(PLAN-002): resolve login validation error"
- "test(PLAN-003): add integration tests for API"
```

**개선점**:
- ✅ 100% 일관된 형식
- ✅ 명확한 정보 (타입, 스코프, 내용)
- ✅ Git history 가독성 향상

### 수치 목표

| 항목 | 목표 |
|------|------|
| **커밋 메시지 품질** | **+60%** |
| **작성 시간** | **-90%** |
| **Git history 가독성** | **+80%** |
| **프로젝트 간 재사용** | **100%** |

---

## 🔗 다른 Skills와의 연계

### validate-spec → commit

```
명세서 검증 → Coding Agent → QA Agent → commit skill
```

### 향후 Skills (Phase 3.1 완성 시)

**review-pr skill**:
```
커밋 → PR 생성 → review-pr skill (자동 리뷰)
```

**refactor-code skill**:
```
리팩토링 제안 → 적용 → commit skill (type=refactor)
```

---

## 🎯 Phase 3.1 전체 계획

### 완료된 Skills (1/4)

- ✅ **commit skill** - 커밋 메시지 자동 생성
- ⬜ **review-pr skill** - PR 자동 리뷰
- ⬜ **refactor-code skill** - 코드 개선 제안
- ⬜ 에이전트 Skills 사용 리팩토링

### 마이그레이션 경로

**Week 1** (현재):
- ✅ commit skill 생성
- ⬜ validate-spec skill (Phase 2.2에서 이미 완료)

**Week 2**:
- review-pr skill 추가
- refactor-code skill 추가

**Week 3**:
- PM Agent가 validate-spec skill 호출하도록 수정
- Coding Agent가 commit skill 호출하도록 수정
- QA Agent가 review-pr skill 호출하도록 수정

**2-3개월**:
- 에이전트 기능을 점진적으로 Skills로 마이그레이션
- 하이브리드 구조 유지

---

## 💡 핵심 인사이트

### Skill 아키텍처의 장점

1. **재사용성**: 프로젝트 간 100% 재사용
2. **독립성**: Skill 추가/제거가 에이전트에 영향 없음
3. **테스트 용이**: Skill 단위로 테스트 가능
4. **확장 용이**: 새 워크플로우는 Skill만 추가

### 하이브리드 접근의 이점

1. **기존 시스템 보존**: 에이전트 계속 작동
2. **점진적 마이그레이션**: 한 번에 하나씩
3. **위험 최소화**: 실패 시 롤백 쉬움
4. **학습 곡선**: 천천히 적응 가능

---

## 🚀 다음 단계

### 즉시 테스트 가능

```bash
# 1. 테스트용 변경 만들기
cd projects/test-project
echo "# Test" > test.md
git add test.md

# 2. Commit Skill 실행 (dry-run)
bash ../../scripts/run-skill.sh commit --ticket PLAN-001 --dry-run

# 3. 실제 커밋
bash ../../scripts/run-skill.sh commit --ticket PLAN-001

# 4. Git log 확인
git log -1
```

### Phase 3.1 완성 (권장 순서)

1. **review-pr skill** 추가
   - PR 자동 리뷰 체크리스트
   - 코드 품질 검사
   - Auto-fix 제안

2. **refactor-code skill** 추가
   - 코드 스멜 감지
   - 리팩토링 패턴 제안
   - 복잡도 분석

3. **에이전트 리팩토링**
   - auto_pipeline.py에 Skills 통합
   - 에이전트 CLAUDE.md에 Skill 사용 지침 추가

---

## 📈 Phase 3.1 (commit skill) 성과

### 생성된 자산

| 카테고리 | 파일 수 | 줄 수 |
|---------|--------|------|
| **Skill 문서** | 1개 | 387줄 |
| **Skill 스크립트** | 1개 | 389줄 |
| **메모리 파일** | 1개 | 43줄 |
| **스크립트 수정** | 1개 | +3줄 |
| **합계** | 4개 | 822줄 |

### 개선 메트릭

| 항목 | 달성 |
|------|------|
| **커밋 타입 자동 결정** | ✅ 7개 타입 (feat, fix, test, docs, refactor, chore, style) |
| **Subject 자동 생성** | ✅ 70자 제한, 명령형 |
| **Body 조건부 생성** | ✅ 파일 3개 이상 또는 refactor/feat |
| **Footer 자동 추가** | ✅ Closes, Co-Authored-By |
| **Gotchas 내장** | ✅ 4개 (파일 경로, 테스트, 여러 티켓, 빈 커밋) |
| **메모리 연계** | ✅ commit-history.json |

---

## 🎉 Phase 3.1 (commit skill) 완료!

**달성**:
- ✅ commit skill 생성 (문서 + 스크립트)
- ✅ 커밋 타입 자동 결정
- ✅ Subject/Body/Footer 자동 생성
- ✅ 4개 Gotchas 내장
- ✅ 메모리 시스템 연계

**기대 효과**:
- 커밋 메시지 품질: **+60%**
- 작성 시간: **-90%**
- Git history 가독성: **+80%**

**다음**: Phase 3.1 나머지 (review-pr, refactor-code)? 또는 Phase 3.2/3.3?

---

## 📝 변경 이력

### 2026-03-19
- ✅ `team/.skills/commit/skill.md` 생성
- ✅ `team/.skills/commit/commit-message-generator.py` 생성
- ✅ `team/.memory/commit-history.json` 생성
- ✅ `team/scripts/run-skill.sh` 업데이트 (commit 추가)
