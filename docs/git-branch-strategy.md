# Git 브랜치 전략

멀티 에이전트 시스템의 Git 브랜치 전략 상세 가이드

---

## 📌 핵심 원칙

### 브랜치 흐름

```
main/dev (베이스 브랜치)
  │
  ├─ docs/PLAN-001-xxx        (PM Agent)
  │
  └─ feature/PLAN-001-xxx     (Coding Agent)
       │
       └─ test/PLAN-001-xxx   (QA Agent)
```

**중요:**
- **PM, Coding Agent**: `base_branch` (main/dev)에서 분기
- **QA Agent**: 동일한 티켓의 **feature 브랜치**에서 분기

---

## 🌿 에이전트별 브랜치 전략

### 1. PM Agent

**브랜치 패턴**: `docs/{티켓번호}-{slug}`

**베이스**: base_branch (main/dev)

**예시**:
```bash
bash scripts/run-agent.sh pm --ticket-file projects/my-app/planning/tickets/PLAN-001-user-auth.md
# → main에서 docs/PLAN-001-user-auth 브랜치 생성
```

**용도**: 명세서 및 테스트 케이스 작성

---

### 2. Coding Agent

**브랜치 패턴**: `feature/{티켓번호}-{slug}`

**베이스**: base_branch (main/dev)

**예시**:
```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
# → main에서 feature/PLAN-001-user-auth 브랜치 생성
```

**용도**: 실제 코드 구현

---

### 3. QA Agent

**브랜치 패턴**: `test/{티켓번호}-{slug}`

**베이스**: **feature 브랜치** (동일 티켓)

**예시**:
```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
# → feature/PLAN-001-user-auth에서 test/PLAN-001-user-auth 브랜치 생성
```

**용도**: 테스트 코드 작성

**중요 사항**:
- QA Agent를 실행하기 전에 반드시 Coding Agent를 먼저 실행해야 합니다
- feature 브랜치가 없으면 경고 메시지를 표시하고 base_branch를 사용합니다

---

## 🔄 전체 워크플로우 예시

### 시나리오: PLAN-001 유저 인증 기능 개발

```bash
cd team

# 1. PM Agent: 명세서 작성
bash scripts/run-agent.sh pm --ticket-file projects/my-app/planning/tickets/PLAN-001-user-auth.md
# → docs/PLAN-001-user-auth 브랜치 생성 (from main)

cd projects/my-app
git add .
git commit -m "docs(PLAN-001): 유저 인증 명세서 작성"
git push origin docs/PLAN-001-user-auth
cd ../..

# 2. Coding Agent: 코드 구현
bash scripts/run-agent.sh coding --ticket PLAN-001
# → feature/PLAN-001-user-auth 브랜치 생성 (from main)

cd projects/my-app
git add .
git commit -m "feat(PLAN-001): 유저 인증 구현"
git push origin feature/PLAN-001-user-auth
cd ../..

# 3. QA Agent: 테스트 작성
bash scripts/run-agent.sh qa --ticket PLAN-001
# → test/PLAN-001-user-auth 브랜치 생성 (from feature/PLAN-001-user-auth)

cd projects/my-app
git add .
git commit -m "test(PLAN-001): 유저 인증 테스트 작성"
git push origin test/PLAN-001-user-auth
cd ../..
```

### 브랜치 구조 (최종)

```
my-app/.git/
├── main
├── docs/PLAN-001-user-auth           (from main)
├── feature/PLAN-001-user-auth        (from main)
└── test/PLAN-001-user-auth           (from feature/PLAN-001-user-auth)
```

---

## ⚙️ 설정 파일

### `.config/git-workflow.json`

```json
{
  "branch_strategy": {
    "enabled": true,
    "base_branch": "main",
    "auto_create": true,
    "auto_checkout": true
  },
  "branch_naming": {
    "base_branch_by_agent": {
      "pm": "base_branch",
      "coding": "base_branch",
      "qa": "feature_branch"
    }
  }
}
```

**주요 설정**:
- `base_branch`: PM/Coding이 사용할 베이스 브랜치 (main, dev 등)
- `qa`: feature_branch 사용 (동일 티켓)

---

## 🔧 수동 브랜치 관리

### 브랜치 준비 (에이전트가 자동 실행)

```bash
# Coding Agent용
bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth
# → main에서 feature/PLAN-001-user-auth 생성

# QA Agent용
bash scripts/git-branch-helper.sh prepare qa PLAN-001 user-auth
# → feature/PLAN-001-user-auth에서 test/PLAN-001-user-auth 생성
```

### 현재 상태 확인

```bash
bash scripts/git-branch-helper.sh status
```

### 설정 확인

```bash
bash scripts/git-branch-helper.sh config
```

---

## 🚨 주의사항

### 1. QA Agent 실행 순서

❌ **잘못된 순서**:
```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
# feature 브랜치가 없음 → 경고
```

✅ **올바른 순서**:
```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
# feature 브랜치 생성

bash scripts/run-agent.sh qa --ticket PLAN-001
# feature 브랜치에서 test 브랜치 생성
```

### 2. 베이스 브랜치 변경

dev 브랜치를 사용하려면:

```json
{
  "branch_strategy": {
    "base_branch": "dev"
  }
}
```

### 3. 프로젝트별 Git

각 프로젝트는 독립적인 Git 리포지토리입니다:

```
team/projects/
├── my-app/.git/           # 프로젝트 A Git
└── my-blog/.git/          # 프로젝트 B Git
```

브랜치 작업은 **프로젝트 리포지토리 내**에서 수행됩니다.

---

## 📋 브랜치 네이밍 규칙

### 패턴

```
{prefix}/{ticket-number}-{slug}
```

### 예시

| 티켓 | PM | Coding | QA |
|-----|-------|--------|-----|
| PLAN-001-user-auth | `docs/PLAN-001-user-auth` | `feature/PLAN-001-user-auth` | `test/PLAN-001-user-auth` |
| PLAN-002-todo-crud | `docs/PLAN-002-todo-crud` | `feature/PLAN-002-todo-crud` | `test/PLAN-002-todo-crud` |

### Slug 추출

티켓 파일명에서 자동 추출:
- `PLAN-001-user-auth.md` → slug: `user-auth`
- `PLAN-002-todo-crud.md` → slug: `todo-crud`

---

## 🔀 PR (Pull Request) 전략

### 1. Feature → Main

```bash
cd projects/my-app
git checkout feature/PLAN-001-user-auth
git push origin feature/PLAN-001-user-auth
# GitHub에서 PR: feature/PLAN-001-user-auth → main
```

### 2. Test → Feature (옵션)

테스트를 별도 PR로 관리:

```bash
cd projects/my-app
git checkout test/PLAN-001-user-auth
git push origin test/PLAN-001-user-auth
# GitHub에서 PR: test/PLAN-001-user-auth → feature/PLAN-001-user-auth
```

### 3. Feature + Test → Main (권장)

feature 브랜치에 test 브랜치를 머지 후 PR:

```bash
cd projects/my-app
git checkout feature/PLAN-001-user-auth
git merge test/PLAN-001-user-auth
git push origin feature/PLAN-001-user-auth
# GitHub에서 PR: feature/PLAN-001-user-auth → main
```

---

## 🛠️ 트러블슈팅

### Q1. feature 브랜치가 없는데 QA를 실행했어요

**현상**:
```
⚠️  feature 브랜치가 없습니다: feature/PLAN-001-user-auth
   먼저 coding 에이전트를 실행하세요.
   또는 기본 베이스 브랜치를 사용합니다: main
```

**해결**:
1. Coding Agent를 먼저 실행
2. 또는 main에서 test 브랜치 생성 (권장하지 않음)

### Q2. 브랜치가 자동으로 생성되지 않아요

**확인사항**:
```bash
# 설정 확인
cat .config/git-workflow.json

# auto_create가 true인지 확인
```

### Q3. 다른 베이스 브랜치를 사용하고 싶어요

**해결**:
```json
{
  "branch_strategy": {
    "base_branch": "develop"
  }
}
```

---

**버전**: v0.0.2
**최종 업데이트**: 2026-03-12
