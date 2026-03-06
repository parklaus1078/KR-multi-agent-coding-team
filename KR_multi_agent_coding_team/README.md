# 멀티 에이전트 개발 워크플로우

Claude Code 기반의 멀티 에이전트 시스템으로, Jira 티켓에서 구현 및 테스트 완료까지의 개발 사이클을 자동화합니다.

---

## 개요

Jira 티켓을 작성하면, 에이전트들이 나머지를 처리합니다.

```
Jira 티켓
    ↓
PM Agent          — API 명세서, UI 와이어프레임, 테스트 케이스 초안 생성
    ↓
사람 검수          — 모든 산출물 확인 및 수정
    ↓
BE Coding Agent   — FastAPI 구현
FE Coding Agent   — Next.js / React 구현
    ↓
QA-BE Agent       — pytest 테스트 스위트 작성
QA-FE Agent       — Vitest / Jest 테스트 스위트 작성
    ↓
사람 검수
```

각 에이전트는 모든 결정 사항을 설명하는 구현 로그를 남깁니다. 블랙박스는 없습니다.

---

## 에이전트 목록

| 에이전트 | 역할 | 입력 | 출력 |
|---------|------|------|------|
| `pm` | 요구사항 문서화 | Jira 티켓 `.md` | API 명세서, UI 명세서, 와이어프레임 HTML, 테스트 케이스 |
| `be-coding` | 백엔드 초벌 구현 | API 명세서 | FastAPI 라우터, 서비스, 레포지토리 |
| `fe-coding` | 프론트엔드 초벌 구현 | UI 명세서 + 와이어프레임 + API 명세서 | Next.js 페이지, 컴포넌트, 훅 |
| `qa-be` | 백엔드 테스트 작성 | BE 테스트 케이스 + 구현 코드 | pytest 테스트 스위트 |
| `qa-fe` | 프론트엔드 테스트 작성 | FE 테스트 케이스 + 구현 코드 | Vitest / Jest 테스트 스위트 |

---

## 프로젝트 구조

```
Workspace/
├── .agents/                        # 에이전트 지시 파일
│   ├── pm/CLAUDE.md
│   ├── be-coding/CLAUDE.md
│   ├── fe-coding/CLAUDE.md
│   ├── qa-be/CLAUDE.md
│   └── qa-fe/CLAUDE.md
│
├── .rules/                         # 코딩 규칙 (에이전트가 참조)
│   ├── be-coding-rules.md
│   └── fe-coding-rules.md
│
├── scripts/                        # 유틸리티 스크립트
│   ├── run-agent.sh                # 에이전트 실행 래퍼
│   ├── rate-limit-check.sh         # Claude Max Rate Limit 체크
│   ├── parse_usage.py              # 사용량 추적
│   └── show-logs.sh                # 구현 로그 조회
│
├── tickets/                        # Jira 티켓 export 파일
│   └── PROJ-123.md
│
├── be-api-requirements/            # API 명세서 (PM Agent 산출물)
│   └── PROJ-123-user-login.md
│
├── fe-ui-requirements/             # UI 명세서 및 와이어프레임 (PM Agent 산출물)
│   ├── PROJ-123-login-ui-spec.md
│   └── PROJ-123-login-wireframe.html
│
├── be-test-cases/                  # BE 테스트 케이스 (PM Agent 산출물)
│   └── PROJ-123-user-login.md
│
├── fe-test-cases/                  # FE 테스트 케이스 (PM Agent 산출물)
│   └── PROJ-123-user-login.md
│
├── logs/                           # 구현 로그 (에이전트 산출물)
│   ├── pm/
│   ├── be-coding/
│   ├── fe-coding/
│   ├── qa-be/
│   └── qa-fe/
│
├── be-project/                     # FastAPI 백엔드
└── fe-project/                     # Next.js 프론트엔드
```

---

## 사전 준비

- [Claude Code](https://docs.claude.ai/claude-code) 설치 및 로그인
- Python 3 (Rate Limit 추적용)
- Claude Max 플랜 (5x 사용량 티어)

---

## 사용법

### 1. Jira 티켓을 Markdown으로 export

Jira 티켓 (Title, Description, Comments)을 `.md` 파일로 export하여 `tickets/`에 배치합니다.

```
tickets/PROJ-123.md
```

### 2. PM Agent 실행

```bash
bash scripts/run-agent.sh pm --ticket-file ./tickets/PROJ-123.md
```

PM Agent는 파일을 생성하기 전에 산출물 목록과 주요 내용을 제시하고 승인을 요청합니다.

**산출물 확인 및 검수:**
- `be-api-requirements/PROJ-123-*.md` — API 명세서
- `fe-ui-requirements/PROJ-123-*.md` — UI 명세서
- `fe-ui-requirements/PROJ-123-*.html` — 와이어프레임 (브라우저에서 열어 인터랙션 확인)
- `be-test-cases/PROJ-123-*.md` — BE 테스트 케이스
- `fe-test-cases/PROJ-123-*.md` — FE 테스트 케이스

다음 단계로 넘어가기 전에 필요한 부분을 수정합니다.

### 3. 코딩 에이전트 실행

```bash
bash scripts/run-agent.sh be-coding --ticket PROJ-123
bash scripts/run-agent.sh fe-coding --ticket PROJ-123
```

각 에이전트는 코드를 작성하기 전에 구현 계획을 제시하고 승인을 요청합니다.

### 4. QA 에이전트 실행

```bash
bash scripts/run-agent.sh qa-be --ticket PROJ-123
bash scripts/run-agent.sh qa-fe --ticket PROJ-123
```

### 5. 로그 조회

```bash
bash scripts/show-logs.sh            # 전체 에이전트
bash scripts/show-logs.sh be-coding  # 특정 에이전트만
```

---

## 와이어프레임 HTML 규칙

PM Agent는 유저 플로우가 있는 화면에 대해 인터랙션이 포함된 와이어프레임을 생성합니다.

**정적 HTML** — 단순 정보 표시, 상태 전환이 없는 화면.

**인터랙션 포함 HTML** — 아래 상황에 해당하는 화면:
- 폼 제출 후 화면 전환
- 성공/실패에 따라 다른 상태 표시
- 모달, 토스트, 드로어 등 오버레이
- 탭, 스텝, 위저드 등 단계 전환

인터랙션 포함 와이어프레임은 바닐라 JS만 사용합니다 (프레임워크, 외부 라이브러리 금지). 각 상태는 `id="state-{name}"`을 가진 `div`로 표현되며 `display:none/block`으로 전환됩니다. API 호출은 시뮬레이션으로 대체합니다.

FE Coding Agent는 이 와이어프레임을 참조하여 상태를 React `useState`와 라우터 전환으로 매핑합니다.

---

## 파일 네이밍 규칙

모든 산출물 파일명은 Jira 티켓 번호를 prefix로 사용합니다. 여러 티켓이 동시에 쌓여도 혼선이 없습니다.

```
{티켓번호}-{기능명-슬러그}.{확장자}

예시:
  PROJ-123-user-login.md
  PROJ-123-user-login.html
  PROJ-124-product-list.md
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
logs/fe-coding/20250306-143022-PROJ-123-user-login.md
```