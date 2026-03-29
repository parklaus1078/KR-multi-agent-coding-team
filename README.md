# Multi-Agent Coding Team

> Tech Stack Agnostic 멀티 에이전트 개발 시스템

[![Version](https://img.shields.io/badge/version-v0.0.3-blue.svg)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable-green.svg)]()

Claude Code 기반의 멀티 에이전트 시스템으로, 프로젝트 아이디어에서 구현 및 테스트 완료까지의 개발 사이클을 자동화합니다.

**✨ 핵심 기능**: CLI 기반 멀티 에이전트 시스템 + 세션 관리 + Tech Stack Agnostic 코딩 룰

---

## 🚀 Quick Start

### 1. 설치 및 초기화

```bash
# 1. 리포지토리 클론
git clone https://github.com/your-username/KR-multi-agent-coding-team.git
cd KR-multi-agent-coding-team

# 2. team 디렉토리로 이동
cd team

# 3. 프로젝트 초기화
bash scripts/init-project.sh --interactive
```

### 2. 에이전트 워크플로우

```bash
# Stack 초기화 (코딩 룰 자동 생성)
bash scripts/run-agent.sh stack-initializer

# 티켓 생성 (Project Planner)
bash scripts/run-agent.sh project-planner --project "할일 관리 앱"
# 또는 파일 입력
bash scripts/run-agent.sh project-planner --req requirements.md

# 명세서 작성 (PM Agent)
bash scripts/run-agent.sh pm --ticket PLAN-001

# 코드 구현 (Coding Agent)
bash scripts/run-agent.sh coding --ticket PLAN-001

# 테스트 작성 (QA Agent)
bash scripts/run-agent.sh qa --ticket PLAN-001
```

### 3. 세션 재개 (수정 및 개선)

```bash
# 세션 목록 확인
bash scripts/resume-session.sh --list

# 세션 재개 (이어서 작업)
bash scripts/resume-session.sh PLAN-001 coding

# 세션 포크 (새 세션으로 실험)
bash scripts/resume-session.sh PLAN-001 coding --fork
```

---

## ⚠️ 중요 사항

현재 **v0.0.3** 버전입니다:

- ✅ **안정적**: CLI 기반 멀티 에이전트 시스템
- ✅ **세션 관리**: 작업 재개 및 포크 기능
- ✅ **Tech Stack Agnostic**: 모든 언어/프레임워크 지원
- ⚠️ **수동 Git 관리**: 브랜치 생성, 커밋, 푸시는 사용자가 직접 수행
- ⚠️ **Claude Code Desktop App**: Claude API가 아닌 Desktop App 기반

---

## 🎯 핵심 개념

### 1. 멀티 에이전트 아키텍처

**5개 에이전트** (각각 독립된 전문 역할)

```
에이전트 (Agents)
├─ stack-initializer    프로젝트 타입별 코딩 룰 자동 생성
├─ project-planner      프로젝트를 티켓 단위로 분해
├─ pm                   티켓별 명세서 및 테스트 케이스 작성
├─ coding               명세서 기반 코드 구현
└─ qa                   테스트 케이스 기반 테스트 코드 작성
```

**8개 스킬** (재사용 가능한 도구 - 현재 참고용)
```
스킬 (Skills)
├─ validate-spec     (명세서 검증)
├─ commit            (커밋 메시지 자동 생성)
├─ review-pr         (PR 자동 리뷰)
├─ refactor-code     (리팩토링 제안)
├─ test-runner       (테스트 실행)
├─ deploy            (배포 자동화)
├─ benchmark         (성능 테스트)
└─ docs-generator    (문서 자동 생성)
```

### 2. 세션 관리 시스템

작업한 에이전트 세션을 저장하고 재개할 수 있습니다:

```bash
# 세션 목록 확인
bash scripts/resume-session.sh --list

# 세션 재개 (이어서 작업)
bash scripts/resume-session.sh PLAN-001 coding

# 세션 포크 (새 세션으로 실험)
bash scripts/resume-session.sh PLAN-001 coding --fork
```

### 3. Tech Stack Agnostic 코딩 룰

Stack Initializer가 프로젝트 타입별 코딩 룰을 자동 생성:

```
team/.rules/
├── general-coding-rules.md          # 범용 원칙 (DRY, SOLID 등)
├── _verified/                       # 사람이 검증한 룰 (최고 우선순위)
│   └── web-fullstack/
│       ├── backend-fastapi-python.md
│       └── frontend-nextjs-typescript.md
└── _cache/                          # AI 자동 생성 룰 (24시간 캐시)
    └── (프로젝트 시작 시 자동 생성)
```

**지원하는 프로젝트 타입:**
- **Web Fullstack**: Express+React, Django+Vue, FastAPI+Next.js
- **Web MVC**: Django, Rails, Spring Boot
- **CLI Tool**: Click, Cobra, Clap
- **Desktop App**: Tauri, Electron, Qt
- **Mobile App**: React Native, Flutter
- **Library**: npm, pip, cargo 패키지

### 4. 프로젝트 격리

```
KR-multi-agent-coding-team/          # ← 멀티 에이전트 시스템 (이 리포지토리)
├── CLAUDE.md                        # 시스템 개발 Agent 지시사항
├── README.md                        # 이 파일
├── docs/                            # 아키텍처 문서
├── logs-agent_dev/                  # 시스템 개발 로그 (35개)
└── team/                            # ← 작업 디렉토리
    ├── .agents/                     # 5개 에이전트 정의
    ├── .skills/                     # 8개 스킬 (참고용)
    ├── .rules/                      # 코딩 룰 저장소
    ├── .config/                     # 시스템 설정
    ├── scripts/                     # CLI 도구 (6개)
    ├── docs/                        # 시스템 문서
    └── projects/                    # 사용자 프로젝트
        ├── my-todo-app/             # ← 프로젝트 A (독립 Git 리포)
        │   ├── .git/
        │   ├── .project-meta.json
        │   ├── .sessions/           # 세션 저장
        │   ├── planning/
        │   ├── logs/
        │   └── src/
        └── my-blog/                 # ← 프로젝트 B (독립 Git 리포)
            ├── .git/
            ├── planning/
            └── src/
```

---

## 📦 사전 준비

### 필수
- [Claude Code Desktop App](https://docs.claude.ai/claude-code) 설치 및 로그인
- Git
- Bash Shell (macOS/Linux 기본 제공, Windows는 Git Bash 사용)

### 프로젝트별 의존성
프로젝트 타입에 따라 필요:
- **Python 프로젝트**: Python 3.10+
- **Node.js 프로젝트**: Node.js 18+
- **Go 프로젝트**: Go 1.20+
- 등등...

---

## 📂 주요 디렉토리 구조

### team/ (작업 디렉토리)

모든 명령어는 `team/` 디렉토리에서 실행합니다:

```
team/
├── .agents/                         # 5개 에이전트 정의
│   ├── stack-initializer/
│   │   └── CLAUDE.md
│   ├── project-planner/
│   │   └── CLAUDE.md
│   ├── pm/
│   │   ├── CLAUDE.md
│   │   ├── gotchas.md
│   │   └── workflows/               # 프로젝트 타입별 워크플로우
│   ├── coding/
│   │   └── CLAUDE.md
│   └── qa/
│       └── CLAUDE.md
│
├── .skills/                         # 8개 재사용 가능 스킬 (참고용)
│   ├── validate-spec/
│   ├── commit/
│   ├── review-pr/
│   ├── refactor-code/
│   ├── test-runner/
│   ├── deploy/
│   ├── benchmark/
│   └── docs-generator/
│
├── .rules/                          # 코딩 룰 저장소
│   ├── general-coding-rules.md
│   ├── _verified/                   # 검증된 코딩 룰
│   └── _cache/                      # 자동 생성된 코딩 룰 (24h)
│
├── .config/                         # 시스템 설정
│   ├── auto-responses.json
│   └── log-schema.json
│
├── scripts/                         # CLI 도구
│   ├── init-project.sh              # 프로젝트 초기화
│   ├── switch-project.sh            # 프로젝트 전환
│   ├── run-agent.sh                 # 에이전트 실행
│   ├── resume-session.sh            # 세션 재개 ⭐
│   ├── run-skill.sh                 # 스킬 실행
│   └── auto_pipeline_v2.py          # 자동 파이프라인
│
├── docs/                            # 시스템 문서
│   ├── auto-pipeline-v2-guide.md
│   ├── session-management.md
│   └── skills-guide.md
│
├── projects/                        # 🎯 사용자 프로젝트 작업 공간
│   └── {project-name}/
│       ├── .project-meta.json
│       ├── .sessions/               # 세션 저장
│       ├── planning/
│       │   ├── tickets/
│       │   ├── specs/
│       │   └── test-cases/
│       ├── logs/
│       └── src/                     # 실제 코드
│
├── .project-config.json             # 현재 활성 프로젝트 설정
├── .project-meta.schema.json        # 프로젝트 메타데이터 스키마
└── README.md
```

### logs-agent_dev/ (시스템 개발 로그)

멀티 에이전트 시스템 자체의 개발 히스토리를 기록합니다:

```
logs-agent_dev/
├── README.md                        # 로그 작성 가이드
├── 20260309-*.md                    # 날짜별 개발 로그 (35개)
├── 20260312-*.md
├── 20260316-*.md
├── 20260319-*.md
├── 20260320-*.md
├── 20260323-*.md
└── 20260324-*.md
```

**로그 작성 시기:**
- 에이전트 워크플로우 변경
- 새로운 스크립트 추가
- 설정 파일 구조 변경
- 시스템 개선 및 버그 수정

### docs/ (아키텍처 문서)

시스템 전체 아키텍처 및 가이드 문서:

```
docs/
├── architecture.md                  # 전체 아키텍처
├── supported-tech-stacks.md         # 지원하는 기술 스택
├── CHANGELOG.md                     # 변경 로그
├── contributing.md                  # 기여 가이드
├── git-branch-strategy.md           # Git 브랜치 전략 (참고용)
├── improvement-plan.md              # 개선 계획
└── phase*.md                        # Phase별 완료 보고서 (13개)
```

---

## 🔄 워크플로우

### 전체 워크플로우

```bash
cd team

# 1. 프로젝트 초기화
bash scripts/init-project.sh --interactive

# 2. 프로젝트 디렉토리에서 Git 초기화
cd projects/{project-name}
git init
git remote add origin https://github.com/your-username/{project-name}.git
cd ../..

# 3. Stack Initializer (코딩 룰 자동 생성)
bash scripts/run-agent.sh stack-initializer

# 4. Project Planner (티켓 생성)
bash scripts/run-agent.sh project-planner --project "할일 관리 앱"
# 또는 파일 입력
bash scripts/run-agent.sh project-planner --req requirements.md

# 5. 각 티켓별로 순차 실행
bash scripts/run-agent.sh pm --ticket PLAN-001
bash scripts/run-agent.sh coding --ticket PLAN-001
bash scripts/run-agent.sh qa --ticket PLAN-001

# 6. Git 커밋 (프로젝트 디렉토리에서 수동)
cd projects/{project-name}
git checkout -b feature/PLAN-001-user-auth
git add .
git commit -m "feat(PLAN-001): 사용자 인증 구현"
git push origin feature/PLAN-001-user-auth
cd ../..

# 7. 다음 티켓 진행
bash scripts/run-agent.sh pm --ticket PLAN-002
bash scripts/run-agent.sh coding --ticket PLAN-002
bash scripts/run-agent.sh qa --ticket PLAN-002
```

### 세션 재개 워크플로우

작업 중 수정이 필요하거나 개선하고 싶을 때:

```bash
# 1. 세션 목록 확인
bash scripts/resume-session.sh --list

# 출력 예시:
# 📋 저장된 에이전트 세션 목록
# PLAN-001
#   pm: 2A703096-70FB-4B8D-BE46-C1484AEDE0E0
#   coding: D2BDFDBD-C90C-4C56-A0BF-14F9815F533B
#   qa: 3F8E19AA-8E2D-4F9A-9C76-E5B6F7A8D9E1

# 2. 코드 수정이 필요하면 coding 세션 재개
bash scripts/resume-session.sh PLAN-001 coding

# Claude Code 세션에서:
> src/auth/login.py 파일의 authenticate 함수를
> 더 명확한 에러 메시지를 반환하도록 리팩토링해줘.

# 3. 실험적 변경은 --fork로
bash scripts/resume-session.sh PLAN-001 coding --fork

# 원본 세션 유지하면서 새 세션으로 분기
> JWT 대신 Session 기반 인증으로 완전히 다시 구현해봐
```

### 자동 파이프라인 (Python 스크립트)

```bash
cd team

# 자동 파이프라인 실행 (v2)
python scripts/auto_pipeline_v2.py --project "할일 관리 앱"

# 자동 실행 단계:
# 1. Project Planner → 티켓 생성
# 2. 각 티켓별로:
#    - PM Agent → 명세서 생성
#    - Coding Agent → 코드 구현
#    - QA Agent → 테스트 작성
```

---

## 🤖 에이전트 (5개)

| 에이전트 | 역할 | 입력 | 출력 | 실행 명령 |
|---------|------|------|------|----------|
| `stack-initializer` | 스택 초기화 | `.project-meta.json` | 코딩 룰, 프로젝트 구조 | `bash scripts/run-agent.sh stack-initializer` |
| `project-planner` | 프로젝트 분해 | 자연어 설명 또는 requirements.md | `planning/tickets/PLAN-XXX-*.md` | `bash scripts/run-agent.sh project-planner --project "..."`<br/>`bash scripts/run-agent.sh project-planner --req requirements.md` |
| `pm` | 요구사항 문서화 | 티켓 `.md` | 명세서, 테스트 케이스 | `bash scripts/run-agent.sh pm --ticket PLAN-001` |
| `coding` | 코드 구현 | 명세서 | `src/` 코드 | `bash scripts/run-agent.sh coding --ticket PLAN-001` |
| `qa` | 테스트 작성 | 테스트 케이스 | 테스트 코드 | `bash scripts/run-agent.sh qa --ticket PLAN-001` |

**모든 스택 지원** - 프로젝트 타입에 따라 자동 분기

**세션 자동 저장** - 각 에이전트 실행 시 `.sessions/{TICKET}/{AGENT}.session`에 세션 ID 저장

---

## 🛠️ 스킬 (8개 - 참고용)

| 스킬 | 설명 | 상태 |
|-----|------|------|
| `validate-spec` | 명세서 검증 | 참고용 (수동 실행 가능) |
| `commit` | 커밋 메시지 생성 | 참고용 (수동 실행 가능) |
| `review-pr` | PR 리뷰 | 참고용 (수동 실행 가능) |
| `refactor-code` | 리팩토링 제안 | 참고용 (수동 실행 가능) |
| `test-runner` | 테스트 실행 | 참고용 (수동 실행 가능) |
| `deploy` | 배포 자동화 | 참고용 (수동 실행 가능) |
| `benchmark` | 성능 테스트 | 참고용 (수동 실행 가능) |
| `docs-generator` | 문서 생성 | 참고용 (수동 실행 가능) |

**스킬 실행:**
```bash
bash scripts/run-skill.sh <skill-name> <ticket>
# 예시:
bash scripts/run-skill.sh commit PLAN-001
bash scripts/run-skill.sh review-pr PLAN-001
```

**주의:** v0.0.3에서는 스킬이 에이전트에서 자동 실행되지 않습니다. 필요 시 수동으로 실행하세요.

---

## ✨ 주요 기능

### 1. 🎨 Tech Stack Agnostic 코딩 룰 자동 생성

**모든 언어, 모든 프레임워크 지원**

Stack Initializer Agent가 프로젝트 타입별로 코딩 룰을 자동 생성합니다:

```bash
bash scripts/run-agent.sh stack-initializer
```

**생성 위치:**
- `team/.rules/_cache/{project_type}/{framework}-{language}.md` (24시간 캐시)
- 사람이 검증한 룰은 `team/.rules/_verified/`에 저장

**지원 프로젝트 타입:**
- Web Fullstack (Express+React, Django+Vue, FastAPI+Next.js 등)
- Web MVC (Django, Rails, Spring Boot 등)
- CLI Tool (Click, Cobra, Clap 등)
- Desktop App (Tauri, Electron, Qt 등)
- Mobile App (React Native, Flutter 등)
- Library (npm, pip, cargo 패키지 등)

### 2. 🔄 세션 관리 시스템

**작업한 에이전트 세션을 저장하고 재개**

```bash
# 세션 목록 확인
bash scripts/resume-session.sh --list

# 세션 재개 (이어서 작업)
bash scripts/resume-session.sh PLAN-001 coding

# 세션 포크 (새 세션으로 실험)
bash scripts/resume-session.sh PLAN-001 coding --fork
```

**특징:**
- 에이전트 실행 시 자동으로 세션 ID 저장
- CLAUDE.md 자동 로드
- 프로젝트 디렉토리로 자동 이동
- Fork 모드로 원본 유지하면서 실험 가능

### 3. 🤖 멀티 에이전트 자동화

**5개 전문 에이전트가 역할 분담**

```bash
# 티켓 생성
bash scripts/run-agent.sh project-planner --project "할일 관리 앱"

# 각 티켓별 자동화
bash scripts/run-agent.sh pm --ticket PLAN-001        # 명세서 작성
bash scripts/run-agent.sh coding --ticket PLAN-001    # 코드 구현
bash scripts/run-agent.sh qa --ticket PLAN-001        # 테스트 작성
```

### 4. 📂 프로젝트 격리

**여러 프로젝트를 독립적으로 관리**

```bash
# 프로젝트 목록
bash scripts/switch-project.sh --list

# 프로젝트 전환
bash scripts/switch-project.sh another-project

# 이제 모든 명령어는 another-project 컨텍스트에서 실행됨
bash scripts/run-agent.sh coding --ticket PLAN-005
```

각 프로젝트는 `team/projects/{name}/` 디렉토리에 격리되고, 독립적인 Git 리포지토리를 가집니다.

### 5. 🧠 학습 시스템

**에이전트 실행 히스토리를 학습**

```
team/.memory/
├── patterns.json           # 반복 패턴 학습
├── commit-history.json     # 커밋 메시지 패턴
└── review-history.json     # 리뷰 피드백
```

### 6. 📝 자동 파이프라인

**Python 스크립트로 전체 워크플로우 자동화**

```bash
python scripts/auto_pipeline_v2.py --project "할일 관리 앱"
```

- Project Planner → PM → Coding → QA 순차 실행
- 진행 상황 저장
- 에러 발생 시 재개 기능

---

## 📁 프로젝트 구조 (간략)

전체 구조는 [project-structure.md](project-structure.md) 참조

```
KR-multi-agent-coding-team/          # 멀티 에이전트 시스템 (이 리포지토리)
├── .git/                            # 시스템 Git
├── CLAUDE.md                        # 시스템 개발 Agent 지시사항
├── CODING-RULES.md                  # 이 프로젝트 코딩 규칙
├── README.md                        # 이 파일
├── LICENSE
├── docs/                            # 아키텍처 문서 (14개)
├── logs-agent_dev/                  # 시스템 개발 로그 (35개)
└── team/                            # ← 작업 디렉토리
    ├── .agents/                     # 5개 에이전트
    │   ├── stack-initializer/
    │   ├── project-planner/
    │   ├── pm/
    │   ├── coding/
    │   └── qa/
    │
    ├── .skills/                     # 8개 스킬 (참고용)
    │   ├── validate-spec/
    │   ├── commit/
    │   ├── review-pr/
    │   ├── refactor-code/
    │   ├── test-runner/
    │   ├── deploy/
    │   ├── benchmark/
    │   └── docs-generator/
    │
    ├── .rules/                      # 코딩 룰 저장소
    │   ├── general-coding-rules.md
    │   ├── _verified/               # 검증된 코딩 룰
    │   └── _cache/                  # 자동 생성 (24h)
    │
    ├── .config/                     # 시스템 설정
    │   ├── auto-responses.json
    │   └── log-schema.json
    │
    ├── .memory/                     # 학습 시스템
    │   ├── patterns.json
    │   ├── commit-history.json
    │   └── review-history.json
    │
    ├── scripts/                     # CLI 도구 (6개)
    │   ├── init-project.sh
    │   ├── switch-project.sh
    │   ├── run-agent.sh
    │   ├── resume-session.sh        # ⭐ 세션 재개
    │   ├── run-skill.sh
    │   └── auto_pipeline_v2.py
    │
    ├── docs/                        # 시스템 문서
    │   ├── session-management.md
    │   ├── skills-guide.md
    │   └── auto-pipeline-v2-guide.md
    │
    ├── projects/                    # 프로젝트 작업 공간
    │   └── {project-name}/          # 프로젝트 (독립 Git 리포)
    │       ├── .git/
    │       ├── .project-meta.json
    │       ├── .sessions/           # ⭐ 세션 저장
    │       ├── planning/
    │       ├── logs/
    │       └── src/
    │
    ├── .project-config.json         # 현재 활성 프로젝트
    ├── .project-meta.schema.json
    └── .gitignore
```

---

## 📚 스크립트 가이드

### 프로젝트 관리

| 스크립트 | 설명 | 사용법 |
|---------|------|--------|
| `init-project.sh` | 프로젝트 초기화 | `bash scripts/init-project.sh --interactive` |
| `switch-project.sh` | 프로젝트 전환 | `bash scripts/switch-project.sh --list`<br/>`bash scripts/switch-project.sh {name}` |

### 에이전트 실행

| 스크립트 | 설명 | 사용법 |
|---------|------|--------|
| `run-agent.sh` | 에이전트 실행 | `bash scripts/run-agent.sh {agent} --ticket {TICKET}` |
| `resume-session.sh` | 세션 재개 | `bash scripts/resume-session.sh --list`<br/>`bash scripts/resume-session.sh {TICKET} {agent}`<br/>`bash scripts/resume-session.sh {TICKET} {agent} --fork` |

### 스킬 실행

| 스크립트 | 설명 | 사용법 |
|---------|------|--------|
| `run-skill.sh` | 스킬 실행 | `bash scripts/run-skill.sh {skill} {TICKET}` |

### 자동화

| 스크립트 | 설명 | 사용법 |
|---------|------|--------|
| `auto_pipeline_v2.py` | 자동 파이프라인 | `python scripts/auto_pipeline_v2.py --project "..."` |

상세 가이드: [team/scripts/README.md](team/scripts/README.md)

---

## 📚 문서

### 시스템 가이드
- **프로젝트 구조**: [project-structure.md](project-structure.md) - 전체 디렉토리 구조 및 파일 목록
- **스크립트 가이드**: [team/scripts/README.md](team/scripts/README.md) - CLI 도구 사용법
- **세션 관리**: [team/docs/session-management.md](team/docs/session-management.md) - 세션 재개 및 포크
- **Skills 가이드**: [team/docs/skills-guide.md](team/docs/skills-guide.md) - 8개 스킬 설명
- **자동 파이프라인**: [team/docs/auto-pipeline-v2-guide.md](team/docs/auto-pipeline-v2-guide.md)

### 코딩 룰
- **범용 코딩 규칙**: [team/.rules/general-coding-rules.md](team/.rules/general-coding-rules.md)
- **코딩 룰 시스템**: [team/.rules/README.md](team/.rules/README.md) - Verified vs Cache
- **검증된 룰 예시**: [team/.rules/_verified/web-fullstack/](team/.rules/_verified/web-fullstack/)

### 아키텍처
- **전체 아키텍처**: [docs/architecture.md](docs/architecture.md)
- **지원 기술 스택**: [docs/supported-tech-stacks.md](docs/supported-tech-stacks.md)
- **Git 브랜치 전략**: [docs/git-branch-strategy.md](docs/git-branch-strategy.md) (참고용)
- **CHANGELOG**: [docs/CHANGELOG.md](docs/CHANGELOG.md)

### 개발 로그
- **시스템 개발 로그**: [logs-agent_dev/README.md](logs-agent_dev/README.md) - 35개 개발 히스토리

---

## 🎯 사용 시나리오

### 시나리오 1: 신규 프로젝트 (전체 워크플로우)

```bash
cd team

# 1. 프로젝트 초기화
bash scripts/init-project.sh --interactive

# 2. Git 리포지토리 초기화
cd projects/my-todo-app
git init
git remote add origin https://github.com/username/my-todo-app.git
cd ../..

# 3. 스택 초기화 (코딩 룰 생성)
bash scripts/run-agent.sh stack-initializer

# 4. 프로젝트 분해 (티켓 생성)
bash scripts/run-agent.sh project-planner --project "할일 관리 앱"

# 5. 각 티켓별 개발
bash scripts/run-agent.sh pm --ticket PLAN-001
bash scripts/run-agent.sh coding --ticket PLAN-001
bash scripts/run-agent.sh qa --ticket PLAN-001

# 6. Git 커밋 및 푸시
cd projects/my-todo-app
git checkout -b feature/PLAN-001-user-auth
git add .
git commit -m "feat(PLAN-001): 사용자 인증 구현"
git push origin feature/PLAN-001-user-auth
cd ../..
```

### 시나리오 2: 코드 수정 (세션 재개)

PR 리뷰 중 수정사항이 생겼을 때:

```bash
cd team

# 1. 세션 목록 확인
bash scripts/resume-session.sh --list

# 2. Coding Agent 세션 재개
bash scripts/resume-session.sh PLAN-001 coding

# Claude Code 세션에서:
# > src/auth/login.py 파일의 authenticate 함수를
# > 더 명확한 에러 메시지를 반환하도록 리팩토링해줘.

# 3. 변경사항 커밋
cd projects/my-todo-app
git add .
git commit -m "refactor(PLAN-001): 인증 에러 메시지 개선"
git push
cd ../..
```

### 시나리오 3: 대안 구현 시도 (세션 포크)

원본 코드 유지하면서 다른 방식 시도:

```bash
cd team

# 1. 세션 포크
bash scripts/resume-session.sh PLAN-001 coding --fork

# Claude Code 세션에서:
# > JWT 대신 Session 기반 인증으로 완전히 다시 구현해봐.
# > src/auth/session_login.py로 새 파일 생성.

# 2. 대안 구현 완료 (원본 파일 유지됨)
# 3. 비교 후 선택
```

### 시나리오 4: 자동 파이프라인 (Python 스크립트)

```bash
cd team

# 자동 파이프라인 실행
python scripts/auto_pipeline_v2.py --project "할일 관리 앱"

# 자동 실행 단계:
# 1. Project Planner → 티켓 생성
# 2. 각 티켓별로 PM → Coding → QA 순차 실행
# 3. 진행 상황 자동 저장
```

### 시나리오 5: 여러 프로젝트 관리

```bash
cd team

# 프로젝트 A 작업
bash scripts/switch-project.sh todo-app
bash scripts/run-agent.sh coding --ticket PLAN-001

# 프로젝트 B로 전환
bash scripts/switch-project.sh blog
bash scripts/run-agent.sh coding --ticket PLAN-003

# 다시 프로젝트 A로
bash scripts/switch-project.sh todo-app
```

---

## 🔄 버전 히스토리

### v0.0.1: 초기 버전
- 5개 에이전트 (stack-initializer, project-planner, pm, coding, qa)
- Tech Stack Agnostic 설계
- 프로젝트 격리

### v0.0.2: Git 워크플로우 자동화
- Git 브랜치 자동 생성/전환
- Rate limit 추적
- Skills 아키텍처 추가 (8개 스킬)

### v0.0.3: 세션 관리 및 안정화 (현재)
- ✅ **세션 관리 시스템** (resume-session.sh)
  - 작업 재개 기능
  - 세션 포크 기능
  - CLAUDE.md 자동 로드
- ✅ **Git 수동 관리로 전환** (사용자가 브랜치 생성/커밋)
- ✅ **Skills 자동 실행 제거** (수동 실행만 가능)
- ✅ **Rate limit 체크 제거** (Claude Code Desktop App 특성)
- ✅ **안정성 개선** (35개 개발 로그)

**총 라인 수**: 약 50,000+ 줄 (코드 + 문서 + 스크립트)

---

## 🚧 향후 계획

### v0.0.4: 개선 예정
- [ ] 자동 파이프라인 v2 고도화
- [ ] 코딩 룰 검증 시스템 개선
- [ ] 메모리 시스템 활용도 증대
- [ ] 에이전트 간 컨텍스트 공유 개선

### v1.0.0: 장기 계획
- [ ] REST API 복원 (선택사항)
- [ ] 웹 대시보드 복원 (선택사항)
- [ ] Database 연동
- [ ] Multi-user 지원

---

## 🤝 기여 가이드

### 검증된 코딩 룰 기여

새로운 기술 스택의 코딩 룰을 기여할 수 있습니다:

1. Stack Initializer로 코딩 룰 자동 생성
2. 실제 프로젝트에서 사용하며 검증
3. `team/.rules/_verified/{project_type}/`로 이동
4. Pull Request 생성

**예시:**
```bash
# 1. 자동 생성
bash scripts/run-agent.sh stack-initializer

# 2. 검증 완료 후 승격
mkdir -p team/.rules/_verified/cli-tool
mv team/.rules/_cache/cli-tool/cobra-go.md team/.rules/_verified/cli-tool/

# 3. PR 생성
git add team/.rules/_verified/
git commit -m "feat: add verified coding rules for Cobra (Go)"
git push origin add-cobra-rules
```

### 새로운 스킬 기여

재사용 가능한 스킬을 추가할 수 있습니다:

1. `team/.skills/{skill-name}/` 디렉토리 생성
2. `skill.md` 작성 (스킬 정의)
3. 필요한 Python 스크립트 작성
4. Pull Request 생성

### 에이전트 개선

에이전트 CLAUDE.md 개선 제안:

1. `team/.agents/{agent}/CLAUDE.md` 수정
2. 실제 프로젝트에서 테스트
3. `logs-agent_dev/` 에 개선 로그 작성
4. Pull Request 생성

### 문서 기여

- 아키텍처 문서: `docs/`
- 시스템 문서: `team/docs/`
- 개발 로그: `logs-agent_dev/`

**기여 시 주의사항:**
- 모든 변경사항은 `logs-agent_dev/`에 로그 작성
- CODING-RULES.md 준수
- 테스트 필수

---

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

---

## 🔗 관련 링크

- **Claude Code 문서**: [https://docs.claude.ai/claude-code](https://docs.claude.ai/claude-code)
- **GitHub Repository**: [https://github.com/your-username/KR-multi-agent-coding-team](https://github.com/your-username/KR-multi-agent-coding-team)

---

**버전**: v0.0.3
**최종 업데이트**: 2026-03-24

## 🆕 최근 업데이트 (2026-03-23~24)

### v0.0.3: 세션 관리 및 안정화 ✨

**세션 관리 시스템:**
- ✅ `resume-session.sh` 구현 (173줄)
- ✅ 세션 목록 보기 (`--list`)
- ✅ 세션 재개 (이어서 작업)
- ✅ 세션 포크 (`--fork`, 새 세션으로 실험)
- ✅ CLAUDE.md 자동 로드
- ✅ 프로젝트 디렉토리 자동 이동

**시스템 안정화:**
- ✅ Git 브랜치 자동화 제거 (사용자가 수동으로)
- ✅ Skills 자동 실행 제거 (수동 실행만)
- ✅ Rate limit 체크 제거 (Claude Code 특성상 불필요)
- ✅ 세션 저장 버그 수정 (exec 제거)
- ✅ PM Agent `--ticket` 옵션 추가

**개발 로그:**
- ✅ 35개 개발 로그 작성
- ✅ logs-agent_dev/ 디렉토리 구조화

자세한 내용:
- [logs-agent_dev/20260324-implement-resume-session.md](logs-agent_dev/20260324-implement-resume-session.md)
- [logs-agent_dev/20260323-remove-git-branch-automation.md](logs-agent_dev/20260323-remove-git-branch-automation.md)
- [logs-agent_dev/20260323-remove-skills-from-agents.md](logs-agent_dev/20260323-remove-skills-from-agents.md)

---

**🌟 Multi-Agent Coding Team v0.0.3: 안정적인 CLI 기반 멀티 에이전트 시스템**
