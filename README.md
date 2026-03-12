# Multi-Agent Coding Team

> Tech Stack Agnostic 멀티 에이전트 개발 시스템

[![Version](https://img.shields.io/badge/version-v0.0.2-blue.svg)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)]()

Claude Code 기반의 멀티 에이전트 시스템으로, 프로젝트 아이디어에서 구현 및 테스트 완료까지의 개발 사이클을 자동화합니다.

---

## ⚠️ 베타 버전 주의사항

현재 **v0.0.2 베타** 버전입니다. 다음 사항에 유의하세요:

- 사용 방식에 따라 Claude API 토큰을 과도하게 소비할 수 있습니다
- 작업을 작은 단위로 세분화하지 않으면 Context Window 초과로 중단될 수 있습니다
- 프로덕션 환경에서 사용하기 전 충분한 테스트를 권장합니다

---

## 🎯 핵심 개념

### 1. 멀티 에이전트 시스템 = 도구 (Tool)

이 리포지토리는 **개발 도구**입니다. 사용자의 실제 프로젝트 코드는 별도 리포지토리로 관리됩니다.

```
KR-multi-agent-coding-team/          # ← 멀티 에이전트 시스템 (이 리포지토리)
└── team/                            # 작업 디렉토리
    ├── scripts/                     # 에이전트 실행 스크립트
    ├── .agents/                     # 5개 통합 에이전트
    └── projects/                    # 프로젝트 작업 공간
        ├── my-todo-app/             # ← 프로젝트 A (독립 Git 리포지토리)
        │   ├── .git/
        │   ├── planning/
        │   └── src/
        └── my-blog/                 # ← 프로젝트 B (독립 Git 리포지토리)
            ├── .git/
            ├── planning/
            └── src/
```

### 2. Tech Stack Agnostic

모든 언어, 모든 프레임워크를 지원합니다:
- **Web Fullstack**: Express+React, Django+Vue, FastAPI+Next.js 등
- **Web MVC**: Django, Rails, Spring Boot 등
- **CLI Tool**: Click, Cobra, Clap 등
- **Desktop App**: Tauri, Electron, Qt 등
- **Mobile App**: React Native, Flutter 등
- **Library**: npm, pip, cargo 패키지 등
- **Data Pipeline**: Airflow, Prefect 등

### 3. 프로젝트 격리

각 프로젝트는 `team/projects/{name}/` 디렉토리에 독립적으로 생성되며, **각각 별도의 Git 리포지토리**로 관리됩니다.

---

## 📦 사전 준비

- [Claude Code](https://docs.claude.ai/claude-code) 설치 및 로그인
- Python 3 (Rate Limit 추적용)
- Git
- Claude Pro 이상 플랜 권장

---

## 🚀 빠른 시작

### 1. 시스템 클론

```bash
git clone https://github.com/your-username/KR-multi-agent-coding-team.git
cd KR-multi-agent-coding-team/team
```

### 2. 첫 프로젝트 생성

```bash
# 대화형 모드로 프로젝트 초기화
bash scripts/init-project.sh --interactive
```

대화형 모드에서 선택:
- 프로젝트 타입: web-fullstack, cli-tool, desktop-app 등
- 언어: Python, Go, TypeScript 등
- 프레임워크: FastAPI, Cobra, Tauri 등
- 프로젝트 이름: my-todo-app

### 3. 프로젝트 Git 리포지토리 초기화

```bash
# 생성된 프로젝트 디렉토리로 이동
cd projects/my-todo-app

# Git 리포지토리 초기화
git init
git add .
git commit -m "chore: initial project structure"

# 원격 리포지토리 연결 (옵션)
git remote add origin https://github.com/your-username/my-todo-app.git
git branch -M main
git push -u origin main

# 작업 디렉토리로 복귀
cd ../..
```

### 4. Stack Initializer 실행 (코딩 룰 자동 생성)

```bash
bash scripts/run-agent.sh stack-initializer
```

Stack Initializer는:
- 선택한 프레임워크의 공식 문서를 분석
- 베스트 프랙티스 기반 코딩 룰 자동 생성
- `.rules/_cache/`에 저장 (24시간 캐시)

### 5. 티켓 생성

```bash
bash scripts/run-agent.sh project-planner --project "할일 관리 앱: 유저 인증, 할일 CRUD, 카테고리 기능"
```

생성 결과:
```
projects/my-todo-app/planning/tickets/
├── PLAN-001-user-auth.md
├── PLAN-002-todo-crud.md
└── PLAN-003-category.md
```

### 6. 명세서 생성 (자동 브랜치 생성)

```bash
bash scripts/run-agent.sh pm --ticket-file projects/my-todo-app/planning/tickets/PLAN-001-user-auth.md
```

자동 동작:
1. `docs/PLAN-001-user-auth` 브랜치 자동 생성/전환
2. 명세서 작성:
   - `planning/specs/` (프로젝트 타입에 따라 동적 구조)
   - `planning/test-cases/`

### 7. 코딩 (자동 브랜치 생성)

```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
```

자동 동작:
1. `feature/PLAN-001-user-auth` 브랜치 자동 생성/전환
2. 코드 구현
3. 구현 로그 작성

### 8. 테스트 작성 (자동 브랜치 생성)

```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
```

자동 동작:
1. `test/PLAN-001-user-auth` 브랜치 자동 생성/전환
2. 테스트 코드 작성
3. 테스트 로그 작성

### 9. 커밋 및 푸시

```bash
# 프로젝트 디렉토리로 이동
cd projects/my-todo-app

# 코드 리뷰 후 커밋
git add .
git commit -m "feat(PLAN-001): 유저 인증 구현 및 테스트 완료

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 푸시
git push origin feature/PLAN-001-user-auth

# 작업 디렉토리로 복귀
cd ../..
```

---

## 🔄 워크플로우 상세

### 프로젝트 아이디어 → 구현 완료까지

```
1. 프로젝트 초기화
   bash scripts/init-project.sh --interactive
   → projects/{name}/ 생성

2. Git 리포지토리 초기화 (사용자)
   cd projects/{name}
   git init
   cd ../..

3. Stack Initializer (코딩 룰 자동 생성)
   bash scripts/run-agent.sh stack-initializer

4. Project Planner (티켓 생성)
   bash scripts/run-agent.sh project-planner --project "프로젝트 설명"
   → planning/tickets/PLAN-XXX-*.md

5. PM Agent (명세서 생성)
   bash scripts/run-agent.sh pm --ticket-file projects/{name}/planning/tickets/PLAN-001-*.md
   → Git 브랜치 자동 생성: docs/PLAN-001-xxx
   → planning/specs/ 및 planning/test-cases/ 생성

6. Coding Agent (코드 구현)
   bash scripts/run-agent.sh coding --ticket PLAN-001
   → Git 브랜치 자동 생성: feature/PLAN-001-xxx
   → src/ 코드 작성

7. QA Agent (테스트 작성)
   bash scripts/run-agent.sh qa --ticket PLAN-001
   → Git 브랜치 자동 생성: test/PLAN-001-xxx
   → 테스트 코드 작성

8. 커밋 및 푸시 (사용자)
   cd projects/{name}
   git add .
   git commit -m "feat(PLAN-001): 구현 완료"
   git push origin feature/PLAN-001-xxx
```

---

## 🤖 에이전트 목록

| 에이전트 | 역할 | 입력 | 출력 |
|---------|------|------|------|
| `stack-initializer` | 스택 초기화 | `.project-config.json` | 코딩 룰, 프로젝트 구조 |
| `project-planner` | 프로젝트 분해 | 자연어 설명 | `planning/tickets/PLAN-XXX-*.md` |
| `pm` | 요구사항 문서화 | 티켓 `.md` | 명세서, 테스트 케이스 |
| `coding` | 코드 구현 (모든 스택) | 명세서 | `src/` 코드 |
| `qa` | 테스트 작성 (모든 스택) | 테스트 케이스 | 테스트 코드 |

**총 5개 통합 에이전트** - 프로젝트 타입에 따라 자동 분기

---

## 📁 프로젝트 구조 (타입별 동적 생성)

### Web Fullstack (예: FastAPI + Next.js)

```
projects/my-todo-app/
├── .git/                           # 프로젝트 Git 리포지토리
├── .project-meta.json              # 프로젝트 메타데이터
├── planning/
│   ├── tickets/                    # 티켓 파일
│   ├── specs/
│   │   ├── backend/                # API 명세서
│   │   └── frontend/               # UI 명세서
│   └── test-cases/
│       ├── backend/
│       └── frontend/
├── src/
│   ├── backend/                    # FastAPI 코드
│   └── frontend/                   # Next.js 코드
└── logs/                           # 에이전트 구현 로그
    ├── coding/
    └── qa/
```

### CLI Tool (예: Go + Cobra)

```
projects/file-search-cli/
├── .git/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/                      # 커맨드 명세서
│   └── test-cases/
├── src/
│   ├── cmd/                        # 커맨드 구현
│   └── internal/                   # 내부 로직
└── logs/
```

### Desktop App (예: Tauri + React)

```
projects/notes-app/
├── .git/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── screens/                # 화면 명세서
│   │   ├── state/                  # 상태 관리
│   │   └── ipc/                    # IPC 통신
│   └── test-cases/
│       ├── unit/
│       ├── integration/
│       └── e2e/
├── src/
│   ├── src-tauri/                  # Rust 백엔드
│   └── src/                        # React 프론트엔드
└── logs/
```

---

## 🔀 다중 프로젝트 관리

### 프로젝트 전환

```bash
# 프로젝트 목록 확인
bash scripts/switch-project.sh --list

# 프로젝트 전환
bash scripts/switch-project.sh my-blog

# 이제 모든 명령어는 my-blog 컨텍스트에서 실행됨
bash scripts/run-agent.sh coding --ticket PLAN-005
```

### 프로젝트 컨텍스트 자동 인식

`.project-config.json`의 `current_project` 값을 읽어 자동으로 프로젝트를 인식합니다.

```json
{
  "current_project": "my-todo-app",
  "current_project_path": "projects/my-todo-app",
  "recent_projects": ["my-todo-app", "my-blog"]
}
```

---

## 🌿 Git 브랜치 전략

### 자동 브랜치 생성

PM, Coding, QA Agent 실행 시 **티켓 번호 기반으로 자동 브랜치 생성/전환**:

| 에이전트 | 브랜치 패턴 | 베이스 브랜치 | 예시 |
|---------|-----------|-------------|------|
| `pm` | `docs/{티켓번호}-{slug}` | base_branch (main/dev) | `docs/PLAN-001-user-auth` |
| `coding` | `feature/{티켓번호}-{slug}` | base_branch (main/dev) | `feature/PLAN-001-user-auth` |
| `qa` | `test/{티켓번호}-{slug}` | **feature 브랜치** | `test/PLAN-001-user-auth` |

**중요:** QA Agent는 동일한 티켓의 feature 브랜치를 베이스로 test 브랜치를 생성합니다.

### Git 작업 위치

**중요:** Git 작업은 **프로젝트 리포지토리** 내에서 수행됩니다.

```bash
# 시스템은 team/에 있지만, Git 브랜치는 projects/{name}/.git에 생성됨
cd team
bash scripts/run-agent.sh coding --ticket PLAN-001

# 내부 동작:
# 1. projects/my-todo-app/.git에서 feature/PLAN-001-xxx 브랜치 생성
# 2. 해당 브랜치로 전환
# 3. 코드 작성
```

### 브랜치 설정

`.config/git-workflow.json`:

```json
{
  "branch_strategy": {
    "enabled": true,
    "base_branch": "main",
    "auto_create": true,
    "auto_checkout": true
  },
  "safety": {
    "check_uncommitted_changes": true,
    "stash_before_checkout": true
  }
}
```

---

## ⚡ Rate Limit 관리

모든 에이전트는 작업 시작 전 자동으로 Rate Limit을 체크합니다.

### 임계값

| 상태 | 사용량 | 동작 |
|------|--------|------|
| ✅ 여유 있음 | 0-34회 | 작업 진행 |
| ⚠️ 경고 | 35-44회 | 사용자에게 알리고, 동의 시 진행 |
| 🛑 중단 | 45회 이상 | 즉시 중단, 재개 가능 시간 안내 |

### 수동 확인

```bash
bash scripts/rate-limit-check.sh
```

임계값 조정: `scripts/parse_usage.py`

---

## 📚 코딩 룰 시스템

### 자동 생성 vs 검증된 룰

```
.rules/
├── general-coding-rules.md         # 범용 원칙 (DRY, SOLID 등)
├── _cache/                          # AI 자동 생성 (24시간 캐시)
│   └── cli-tool-cobra-go.md
└── _verified/                       # 사람이 검증한 룰
    └── web-fullstack/
        ├── backend-fastapi-python.md
        └── frontend-nextjs-typescript.md
```

### Stack Initializer 워크플로우

1. 프레임워크 공식 문서 분석 (WebFetch/WebSearch)
2. 베스트 프랙티스 추출
3. 코딩 룰 자동 생성 → `.rules/_cache/`
4. 사용자 검증 후 → `.rules/_verified/`로 승격

---

## 📖 로그 시스템

모든 에이전트는 작업 완료 후 구현 로그를 작성합니다.

### 로그 위치

```
projects/{name}/logs/{agent}/
└── 20260312-143022-PLAN-001-user-auth.md
```

### 로그 내용

- 생성/수정한 파일 목록
- 주요 결정 사항 및 Trade-off
- 고려한 대안
- 검수자를 위한 주의사항

### 로그 조회

```bash
# 현재 프로젝트 전체 로그
bash scripts/show-logs.sh

# 특정 에이전트만
bash scripts/show-logs.sh coding

# 모든 프로젝트 로그
bash scripts/show-logs.sh --all
```

---

## 🛠️ 고급 사용법

### 플래그 모드로 프로젝트 초기화

```bash
bash scripts/init-project.sh \
  --type cli-tool \
  --language go \
  --framework cobra \
  --name file-search-cli \
  --description "빠른 파일 검색 도구"
```

### Project Planner 재개 모드

Context Window 초과로 중단된 경우:

```bash
bash scripts/run-agent.sh project-planner --resume
```

### 수동 브랜치 관리

```bash
# 브랜치 준비
bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth

# 현재 상태 확인
bash scripts/git-branch-helper.sh status

# 설정 확인
bash scripts/git-branch-helper.sh config
```

---

## 📂 전체 디렉토리 구조

```
KR-multi-agent-coding-team/          # 멀티 에이전트 시스템 (이 리포지토리)
├── .git/                            # 시스템 Git
├── README.md                        # 이 파일
├── LICENSE
├── docs/                            # 아키텍처 문서
│   ├── architecture-final.md
│   └── supported-tech-stacks.md
├── logs-agent_dev/                  # 시스템 개발 로그
└── team/                            # ← 작업 디렉토리 (여기서 명령어 실행)
    ├── .agents/                     # 에이전트 정의 (CLAUDE.md)
    │   ├── stack-initializer/
    │   ├── project-planner/
    │   ├── pm/
    │   ├── coding/
    │   └── qa/
    ├── .rules/                      # 코딩 룰
    │   ├── general-coding-rules.md
    │   ├── _cache/                  # AI 자동 생성
    │   └── _verified/               # 사람이 검증
    ├── .config/                     # 시스템 설정
    │   └── git-workflow.json
    ├── scripts/                     # 유틸리티 스크립트
    │   ├── init-project.sh
    │   ├── switch-project.sh
    │   ├── run-agent.sh
    │   ├── show-logs.sh
    │   ├── git-branch-helper.sh
    │   └── rate-limit-check.sh
    ├── projects/                    # 프로젝트 작업 공간
    │   ├── my-todo-app/             # 프로젝트 A (독립 Git 리포지토리)
    │   │   ├── .git/                # ← 프로젝트 자체의 Git
    │   │   ├── .project-meta.json
    │   │   ├── planning/
    │   │   ├── src/
    │   │   └── logs/
    │   └── my-blog/                 # 프로젝트 B (독립 Git 리포지토리)
    │       ├── .git/
    │       └── ...
    ├── .project-config.json         # 현재 활성 프로젝트
    └── .gitignore
```

---

## 🤝 기여 가이드

### 검증된 코딩 룰 기여

`.rules/_verified/`에 새로운 스택의 코딩 룰을 기여할 수 있습니다:

1. Stack Initializer로 룰 자동 생성
2. 실제 프로젝트에서 검증
3. PR 제출: `.rules/_verified/{project-type}/{framework}.md`

### 템플릿 기여

`.agents/*/templates/`에 새로운 프로젝트 타입 템플릿을 기여할 수 있습니다.

---

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

---

## 🔗 관련 링크

- [Claude Code 문서](https://docs.claude.ai/claude-code)
- [지원 스택 목록](docs/supported-tech-stacks.md)
- [아키텍처 상세](docs/architecture-final.md)

---

**버전**: v0.0.2 (베타)
**최종 업데이트**: 2026-03-12
