# 멀티 에이전트 개발 워크플로우 (베타)

Claude Code 기반의 멀티 에이전트 시스템으로, 프로젝트 아이디어에서 구현 및 테스트 완료까지의 개발 사이클을 자동화합니다.

## 주의 사항

현재 이 프로젝트는 베타 테스팅 단계입니다. 아래 사항에 대해서는 책임지지 않습니다.

- 사용 방식에 따라 Claude Code 토큰을 과도하게 소비할 수 있습니다.
- 작업을 작은 단위로 세분화하지 않고 맡길 시 Context Window가 넘어가 작업이 중단될 수 있습니다.
- 현재 FE는 TypeScript + Next.js, BE는 Python + FastAPI, DB는 PostgreSQL 스택에 최적화되어 있습니다.

---

## 개요

프로젝트 아이디어를 던지면, 에이전트들이 나머지를 처리합니다.

```
프로젝트 설명 (자연어)
    ↓
Project Planner Agent — 기능 목록 + 우선순위 + tickets/ 생성
    ↓
사람 검수              — 기능 범위 조정
    ↓
PM Agent              — 티켓 → API 명세서, UI 와이어프레임, 테스트 케이스 생성
    ↓
사람 검수              — 모든 산출물 확인 및 수정
    ↓
BE Coding Agent       — FastAPI 구현
FE Coding Agent       — Next.js / React 구현
    ↓
QA-BE Agent           — pytest 테스트 스위트 작성
QA-FE Agent           — Vitest / Jest 테스트 스위트 작성
    ↓
사람 검수
```

각 에이전트는 모든 결정 사항을 설명하는 구현 로그를 남깁니다. 블랙박스는 없습니다.

---

## 에이전트 목록

| 에이전트 | 역할 | 입력 | 출력 |
|---------|------|------|------|
| `project-planner` | 프로젝트 분해 | 자연어 설명 | `planning-materials/tickets/PLAN-XXX-*.md` |
| `pm` | 요구사항 문서화 | 티켓 `.md` | API 명세서, UI 명세서, 와이어프레임 HTML, 테스트 케이스 |
| `be-coding` | 백엔드 초벌 구현 | API 명세서 | `applications/be-project/` 코드 |
| `fe-coding` | 프론트엔드 초벌 구현 | UI 명세서 + 와이어프레임 + API 명세서 | `applications/fe-project/` 코드 |
| `qa-be` | 백엔드 테스트 작성 | BE 테스트 케이스 + 구현 코드 | pytest 테스트 스위트 |
| `qa-fe` | 프론트엔드 테스트 작성 | FE 테스트 케이스 + 구현 코드 | Vitest / Jest 테스트 스위트 |

---

## 프로젝트 구조

```
프로젝트 루트/
├── team/                           # 메인 작업 디렉토리
│   ├── .agents/                    # 에이전트 지시 파일
│   │   ├── project-planner/CLAUDE.md
│   │   ├── pm/CLAUDE.md
│   │   ├── be-coding/CLAUDE.md
│   │   ├── fe-coding/CLAUDE.md
│   │   ├── qa-be/CLAUDE.md
│   │   └── qa-fe/CLAUDE.md
│   │
│   ├── .rules/                     # 코딩 규칙 (에이전트가 참조)
│   │   ├── be-coding-rules.md
│   │   └── fe-coding-rules.md
│   │
│   ├── .config/                    # 설정 파일
│   │   └── git-workflow.json
│   │
│   ├── scripts/                    # 유틸리티 스크립트
│   │   ├── run-agent.sh            # 에이전트 실행 래퍼
│   │   ├── rate-limit-check.sh     # Claude Max Rate Limit 체크
│   │   ├── parse_usage.py          # 사용량 추적
│   │   ├── show-logs.sh            # 구현 로그 조회
│   │   ├── git-branch-helper.sh    # Git 브랜치 관리
│   │   └── create-dev-log.sh       # 개발 로그 생성
│   │
│   ├── planning-materials/         # PM 산출물
│   │   ├── tickets/                # 티켓 파일 (Project Planner 산출물)
│   │   │   └── PLAN-001-user-auth.md
│   │   ├── be-api-requirements/    # API 명세서 (PM Agent 산출물)
│   │   │   └── PLAN-001-user-auth.md
│   │   ├── fe-ui-requirements/     # UI 명세서 및 와이어프레임
│   │   │   ├── PLAN-001-login-ui-spec.md
│   │   │   └── PLAN-001-login-wireframe.html
│   │   ├── be-test-cases/          # BE 테스트 케이스
│   │   │   └── PLAN-001-user-auth.md
│   │   └── fe-test-cases/          # FE 테스트 케이스
│   │       └── PLAN-001-user-auth.md
│   │
│   └── applications/               # 실제 애플리케이션 코드
│       ├── be-project/             # FastAPI 백엔드
│       ├── fe-project/             # Next.js 프론트엔드
│       └── logs/                   # 구현 로그 (코딩 에이전트 산출물)
│           ├── be-coding/
│           ├── fe-coding/
│           ├── qa-be/
│           └── qa-fe/
│
└── logs-agent_dev/                 # 개발 로그 (루트 레벨)
```

---

## 사전 준비

- [Claude Code](https://docs.claude.ai/claude-code) 설치 및 로그인
- Python 3 (Rate Limit 추적용)
- Claude Max 플랜 (5x 사용량 티어 이상)

---

## 사용법

### 방법 A — 프로젝트 주제로 시작 (추천)

#### 1. Project Planner 실행

```bash
cd team
bash scripts/run-agent.sh project-planner --project "할일 관리 앱, 유저 인증/할일 CRUD/카테고리 기능 필요"
```

**⚠️ 컨텍스트 윈도우 관리:**
Project Planner는 작업을 **3개 Phase로 분할**하여 실행합니다:

- **Phase 1**: 프로젝트 분석 → 기능 분해 → 계획 승인 → `planning-materials/tickets/.plan-{timestamp}.json` 저장
- **Phase 2**: 계획 파일을 읽어 티켓 파일 생성 (5개씩 배치로 분할)
- **Phase 3**: 로그 작성

에이전트가 기능 목록과 우선순위를 제시하고 승인을 요청합니다. 승인 후 `planning-materials/tickets/`에 티켓 파일이 생성됩니다.

```
planning-materials/tickets/
├── PLAN-001-user-auth.md
├── PLAN-002-todo-crud.md
├── PLAN-003-category.md
└── .plan-20260309-103000.json  # 임시 계획 파일 (완료 후 자동 삭제)
```

**중단/재개:**
작업 중 컨텍스트 윈도우 초과로 중단된 경우:

```bash
cd team
bash scripts/run-agent.sh project-planner --resume
```

생성된 파일을 검토하고 필요한 부분을 수정합니다.

#### 2. 이후 방법 B와 동일

---

### 방법 B — 티켓 파일로 시작

#### 1. 티켓 파일 준비

Jira 티켓 또는 직접 작성한 `.md` 파일을 `team/planning-materials/tickets/`에 배치합니다.

#### 2. PM Agent 실행

```bash
cd team
bash scripts/run-agent.sh pm --ticket-file ./planning-materials/tickets/PLAN-001-user-auth.md
```

PM Agent는 파일을 생성하기 전에 산출물 목록과 주요 내용을 제시하고 승인을 요청합니다.

**산출물 확인 및 검수:**
- `planning-materials/be-api-requirements/PLAN-001-*.md` — API 명세서
- `planning-materials/fe-ui-requirements/PLAN-001-*.md` — UI 명세서
- `planning-materials/fe-ui-requirements/PLAN-001-*.html` — 와이어프레임 (브라우저에서 열어 인터랙션 확인)
- `planning-materials/be-test-cases/PLAN-001-*.md` — BE 테스트 케이스
- `planning-materials/fe-test-cases/PLAN-001-*.md` — FE 테스트 케이스

다음 단계로 넘어가기 전에 필요한 부분을 수정합니다.

#### 3. 코딩 에이전트 실행

```bash
cd team
bash scripts/run-agent.sh be-coding --ticket PLAN-001
bash scripts/run-agent.sh fe-coding --ticket PLAN-001
```

각 에이전트는 코드를 작성하기 전에 구현 계획을 제시하고 승인을 요청합니다.

#### 4. QA 에이전트 실행

```bash
cd team
bash scripts/run-agent.sh qa-be --ticket PLAN-001
bash scripts/run-agent.sh qa-fe --ticket PLAN-001
```

#### 5. 로그 조회

```bash
cd team
bash scripts/show-logs.sh              # 전체 에이전트
bash scripts/show-logs.sh be-coding    # 특정 에이전트만
```

---

## 와이어프레임 HTML 규칙

PM Agent는 유저 플로우가 있는 화면에 대해 인터랙션 와이어프레임을 생성합니다.

**정적 HTML** — 단순 정보 표시, 상태 전환이 없는 화면.

**인터랙션 포함 HTML** — 아래 상황에 해당하는 화면:
- 폼 제출 후 화면 전환
- 성공/실패에 따라 다른 상태 표시
- 모달, 토스트, 드로어 등 오버레이
- 탭, 스텝, 위저드 등 단계 전환

인터랙션 포함 와이어프레임은 바닐라 JS만 사용합니다 (프레임워크, 외부 라이브러리 금지). 각 상태는 `id="state-{name}"`을 가진 `div`로 표현되며 `display:none/block`으로 전환됩니다. API 호출은 시뮬레이션으로 대체합니다.

FE Coding Agent는 이 와이어프레임을 참조하여 상태를 React `useState`와 라우터 전환으로 매핑합니다.

---

## Git 브랜치 워크플로우

코딩 에이전트는 작업 시작 전 자동으로 티켓 전용 브랜치를 생성하고 전환합니다.

### 설정 파일

`.config/git-workflow.json`에서 브랜치 전략을 설정할 수 있습니다:

```json
{
  "branch_strategy": {
    "enabled": true,
    "base_branch": "dev",
    "auto_create": true,
    "auto_checkout": true
  }
}
```

### 브랜치 네이밍 규칙

| 에이전트 | 브랜치 패턴 | 예시 |
|---------|-----------|------|
| `be-coding` | `feature/be/{티켓번호}-{slug}` | `feature/be/PLAN-001-user-auth` |
| `fe-coding` | `feature/fe/{티켓번호}-{slug}` | `feature/fe/PLAN-001-user-auth` |
| `qa-be` | `test/be/{티켓번호}-{slug}` | `test/be/PLAN-001-user-auth` |
| `qa-fe` | `test/fe/{티켓번호}-{slug}` | `test/fe/PLAN-001-user-auth` |

### 자동 동작

#### 작업 시작 시
1. 설정된 베이스 브랜치(기본: `dev`)를 fetch
2. 티켓 전용 브랜치가 없으면 생성
3. 해당 브랜치로 자동 전환
4. 커밋되지 않은 변경사항이 있으면 자동 stash

#### 작업 완료 시
- 에이전트가 커밋은 **하지 않음** (사람이 코드 리뷰 후 커밋)
- 다음 단계 안내 (커밋 명령어 예시 제공)

### 수동 브랜치 관리

```bash
cd team

# 브랜치 준비 (에이전트가 자동으로 실행)
bash scripts/git-branch-helper.sh prepare be-coding PLAN-001 user-auth

# 현재 Git 상태 확인
bash scripts/git-branch-helper.sh status

# 설정 확인
bash scripts/git-branch-helper.sh config
```

### 일반적인 워크플로우

```bash
cd team

# 1. BE 코딩 에이전트 실행
bash scripts/run-agent.sh be-coding --ticket PLAN-001
# → 자동으로 feature/be/PLAN-001-user-auth 브랜치 생성/전환
# → 코드 구현

# 2. 코드 리뷰 후 커밋
git add .
git commit -m "feat(PLAN-001): 유저 인증 API 구현"

# 3. FE 코딩 에이전트 실행
bash scripts/run-agent.sh fe-coding --ticket PLAN-001
# → 자동으로 feature/fe/PLAN-001-user-auth 브랜치 생성/전환
# → 코드 구현

# 4. 코드 리뷰 후 커밋
git add .
git commit -m "feat(PLAN-001): 유저 인증 UI 구현"

# 5. 푸시 및 PR 생성
git push origin feature/be/PLAN-001-user-auth
git push origin feature/fe/PLAN-001-user-auth
# GitHub에서 PR 생성
```

### 브랜치 전략 비활성화

자동 브랜치 관리를 원하지 않는 경우:

```json
{
  "branch_strategy": {
    "enabled": false
  }
}
```

---

## 파일 네이밍 규칙

모든 산출물 파일명은 티켓 번호를 prefix로 사용합니다.

```
{티켓번호}-{기능명-슬러그}.{확장자}

예시:
  PLAN-001-user-auth.md
  PLAN-001-user-auth.html
  PLAN-002-todo-crud.md
```

---

## Rate Limit 관리

이 시스템은 **Claude Max 5x** (5시간 롤링 윈도우) 기준으로 설계되었습니다.

모든 에이전트는 작업 시작 전 `rate-limit-check.sh`를 실행합니다:

| 결과 | 동작 |
|------|------|
| ✅ 여유 있음 | 작업 진행 |
| ⚠️ 경고 (35회 이상) | 사용자에게 알리고, 동의 시 진행 |
| 🛑 중단 (45회 이상) | 즉시 중단, 재개 가능 시간 안내 |

수동으로 현재 사용량을 확인하려면:

```bash
bash scripts/rate-limit-check.sh
```

임계값은 `scripts/parse_usage.py`에서 조정할 수 있습니다:

```python
WARN_THRESHOLD = 35
STOP_THRESHOLD = 45
```

---

## 코딩 규칙

에이전트의 `CLAUDE.md` 파일에는 코딩 규칙이 직접 포함되어 있지 않습니다. 모든 규칙은 아래 파일에 위임됩니다:

- `.rules/be-coding-rules.md` — FastAPI / Python / PostgreSQL 규칙
- `.rules/fe-coding-rules.md` — Next.js / React / TypeScript 규칙

이 구조 덕분에 에이전트 워크플로우 지시를 건드리지 않고 코딩 규칙만 독립적으로 수정할 수 있습니다.

---

## 구현 로그

모든 에이전트는 작업 완료 직후 로그를 작성합니다. 로그에는 다음 내용이 포함됩니다:

- 생성하거나 수정한 파일 목록
- 주요 결정 사항 (예: Server vs Client Component, 데이터 페칭 전략)
- 고려한 대안과 Trade-off
- 검수자를 위한 주의사항

로그는 `logs/{에이전트명}/`에 저장되며, 타임스탬프와 티켓 번호로 파일명이 지정됩니다:

```
logs/fe-coding/20250306-143022-PLAN-001-user-auth.md
```
