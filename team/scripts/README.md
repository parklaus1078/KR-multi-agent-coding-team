# Scripts Directory

멀티 에이전트 시스템 유틸리티 스크립트 모음

**실행 위치**: `team/` 디렉토리에서 실행

```bash
cd team
bash scripts/run-agent.sh coding --ticket PLAN-001
```

---

## 📋 스크립트 목록

### 프로젝트 관리

#### `init-project.sh`
프로젝트 초기화

```bash
# 대화형 모드
bash scripts/init-project.sh --interactive

# 플래그 모드
bash scripts/init-project.sh \
  --type cli-tool \
  --language go \
  --framework cobra \
  --name my-cli-tool
```

#### `switch-project.sh`
프로젝트 전환

```bash
# 프로젝트 목록
bash scripts/switch-project.sh --list

# 프로젝트 전환
bash scripts/switch-project.sh my-cli-tool
```

---

### 에이전트 실행

#### `run-agent.sh`
에이전트 실행 래퍼 (현재 활성 프로젝트 자동 인식)

```bash
# Stack Initializer
bash scripts/run-agent.sh stack-initializer

# Project Planner
bash scripts/run-agent.sh project-planner --project "프로젝트 설명"

# PM (Git 브랜치 자동 생성)
bash scripts/run-agent.sh pm --ticket-file projects/{name}/planning/tickets/PLAN-001-*.md

# Coding (Git 브랜치 자동 생성)
bash scripts/run-agent.sh coding --ticket PLAN-001

# QA (Git 브랜치 자동 생성)
bash scripts/run-agent.sh qa --ticket PLAN-001
```

**주요 기능:**
- `.project-config.json`의 `current_project` 자동 인식
- PM, Coding, QA 실행 시 티켓 번호 기반 Git 브랜치 자동 생성/전환
- 브랜치 생성 실패 시에도 작업 계속 진행

---

### 로그 및 모니터링

#### `show-logs.sh`
에이전트 로그 조회 (v2.0)

```bash
# 현재 프로젝트 전체 로그
bash scripts/show-logs.sh

# 특정 에이전트만
bash scripts/show-logs.sh coding

# 모든 프로젝트 로그
bash scripts/show-logs.sh --all
```

#### `rate-limit-check.sh`
Claude API Rate Limit 확인

```bash
bash scripts/rate-limit-check.sh [agent_name]
```

#### `parse_usage.py`
API 사용량 파싱 (내부 사용)

---

### Git 관리

#### `git-branch-helper.sh`
Git 브랜치 자동 관리

```bash
# 브랜치 준비
bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth

# 현재 상태 확인
bash scripts/git-branch-helper.sh status

# 설정 확인
bash scripts/git-branch-helper.sh config
```

---

### 시스템 개발

#### `create-dev-log.sh`
시스템 개발 로그 생성 (에이전트 시스템 자체 개선용)

```bash
bash scripts/create-dev-log.sh git-workflow-automation
```

---


## 📊 v1.0 vs v2.0 차이점

| 스크립트 | v1.0 | v2.0 | 변경사항 |
|---------|------|------|---------|
| `init-project.sh` | `applications/`, `planning-materials/` 생성 | `projects/{name}/` 생성 | 프로젝트 격리, 타입별 동적 구조 |

---

## 🚀 시작하기

새 프로젝트 시작:

```bash
cd team
bash scripts/init-project.sh --interactive
```

---

## 🛠️ 스크립트 개발 가이드

### 공통 패턴

```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"

# 현재 프로젝트 읽기
CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
PROJECT_PATH="$WORKSPACE_ROOT/projects/$CURRENT_PROJECT"
```

### 프로젝트 경로 규칙

모든 프로젝트는 `projects/{current_project}/` 디렉토리에 격리됩니다.

---

---

## 🔑 핵심 개념

### 프로젝트 Git 리포지토리

각 프로젝트는 **독립적인 Git 리포지토리**로 관리됩니다:

```
team/projects/
├── my-todo-app/
│   ├── .git/                    # ← 프로젝트 A의 Git 리포지토리
│   └── src/
└── my-blog/
    ├── .git/                    # ← 프로젝트 B의 Git 리포지토리
    └── src/
```

### Git 브랜치 작업

`git-branch-helper.sh`와 `run-agent.sh`는 **프로젝트 리포지토리** 내에서 Git 작업을 수행합니다.

```bash
cd team
bash scripts/run-agent.sh coding --ticket PLAN-001

# 내부 동작:
# 1. projects/{current_project}/.git에서 feature/PLAN-001-xxx 브랜치 생성
# 2. 해당 브랜치로 전환
# 3. 코드 작성
```

---

**업데이트 일시**: 2026-03-12
**버전**: v0.0.2
