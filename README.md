# Multi-Agent Coding Team

> Tech Stack Agnostic 멀티 에이전트 개발 시스템 + REST API + Web Dashboard

[![Version](https://img.shields.io/badge/version-v0.0.3-blue.svg)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-green.svg)]()

Claude Code 기반의 멀티 에이전트 시스템으로, 프로젝트 아이디어에서 구현 및 테스트 완료까지의 개발 사이클을 자동화합니다.

**✨ 새로운 기능**: REST API + Discord 연동 + 웹 대시보드로 CLI 없이도 전체 파이프라인을 웹에서 관리할 수 있습니다!

---

## 🚀 Quick Start (3가지 방법)

### 방법 1: 웹 대시보드 (🎨 추천 - 가장 쉬움)

```bash
# 1. 리포지토리 클론
git clone https://github.com/your-username/KR-multi-agent-coding-team.git
cd KR-multi-agent-coding-team/team

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
cp .env.example .env
# .env 파일을 열어서 다음 항목 설정:
# - DISCORD_WEBHOOK_URL (선택)
# - ANTHROPIC_API_KEY (필수)

# 4. API 서버 실행
uvicorn api.main:app --reload --port 8000

# 5. 웹 브라우저에서 접속
# http://localhost:8000
```

웹 대시보드에서:
- 🚀 파이프라인 실행 버튼 클릭
- 📊 실시간 진행 상황 모니터링
- 🤖 개별 에이전트 실행
- 🛠️ 개별 스킬 실행
- 📈 통계 대시보드

### 방법 2: REST API (🔌 프로그래밍)

```bash
# 파이프라인 실행
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-todo-app",
    "resume": false
  }'

# 상태 확인
curl http://localhost:8000/api/pipeline/status/PLAN-001

# API 문서
# http://localhost:8000/api/docs (Swagger UI)
# http://localhost:8000/api/redoc (ReDoc)
```

### 방법 3: CLI (⌨️ 고급 사용자)

```bash
cd team

# 프로젝트 초기화
bash scripts/init-project.sh --interactive

# 에이전트 실행
bash scripts/run-agent.sh pm --ticket PLAN-001
bash scripts/run-agent.sh coding --ticket PLAN-001
bash scripts/run-agent.sh qa --ticket PLAN-001

# 스킬 실행
bash scripts/run-skill.sh commit PLAN-001
bash scripts/run-skill.sh review-pr PLAN-001

# 자동 파이프라인
python scripts/auto_pipeline.py --project "할일 관리 앱"
```

---

## 🔵 Discord 연동 (선택사항)

실시간 알림을 받으려면 Discord Webhook을 설정하세요.

### 1. Discord Webhook 생성

1. Discord 서버 열기
2. **서버 설정** → **연동** → **웹후크**
3. **새 웹후크** 클릭
4. 설정:
   - 이름: Multi-Agent Coding Team
   - 채널: 알림 받을 채널 선택 (예: #dev-notifications)
5. **웹후크 URL 복사**

### 2. 환경 변수 설정

```bash
cd team

# .env 파일 편집
nano .env

# 또는 처음이라면
cp .env.example .env
nano .env
```

`.env` 파일에 Webhook URL 추가:
```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN
ANTHROPIC_API_KEY=sk-ant-your-api-key
```

### 3. 테스트

```bash
# API 서버 실행
uvicorn api.main:app --reload --port 8000

# 시작 알림이 Discord에 표시됨:
# 🚀 API Server Started
# Multi-Agent Coding Team API v0.0.3
```

### 4. 받을 수 있는 알림

- 🚀 **Pipeline Started** - 파이프라인 시작
- 🤖 **Agent Started/Completed** - 에이전트 실행 상황
- ✅ **Tests Passed** / ❌ **Tests Failed** - 테스트 결과
- 🚀 **Deployed to Production** - 배포 완료
- ⚠️ **PR Review Issues** - PR 리뷰 문제 발견
- 🛑 **API Server Stopped** - 서버 종료

**Discord 없이도 시스템은 정상 작동합니다.** (알림만 안 옴)

---

## ⚠️ 주의사항

현재 **v0.0.3** 버전입니다:

- ✅ **Production Ready**: API + 웹 대시보드 완성
- ✅ **Discord 연동**: 실시간 알림 지원
- ✅ **GitHub Webhook**: PR 자동 리뷰
- ⚠️ **In-Memory Storage**: 파이프라인 상태가 메모리에만 저장 (서버 재시작 시 사라짐)
- ⚠️ **No Authentication**: API 엔드포인트에 인증 없음 (VPN 뒤에서 사용 권장)
- 💰 **API 비용**: 작업량에 따라 Claude API 토큰 소비

---

## 🎯 핵심 개념

### 1. 멀티 에이전트 + Skills 아키텍처

**5개 에이전트** (복잡한 의사결정) + **8개 스킬** (반복 작업 자동화)

```
에이전트 (Agents)               스킬 (Skills)
├─ stack-initializer            ├─ validate-spec     (명세서 검증)
├─ project-planner              ├─ commit            (커밋 메시지 자동 생성)
├─ pm                           ├─ review-pr         (PR 자동 리뷰)
├─ coding                       ├─ refactor-code     (리팩토링 제안)
└─ qa                           ├─ test-runner       (테스트 실행)
                                ├─ deploy            (배포 자동화)
                                ├─ benchmark         (성능 테스트)
                                └─ docs-generator    (문서 자동 생성)
```

### 2. 3가지 사용 방법

```
┌─────────────────────────────────────────────────────────────┐
│  웹 대시보드 (Web Dashboard)                                 │
│  http://localhost:8000                                      │
│  - 버튼 클릭만으로 파이프라인 실행                            │
│  - 실시간 모니터링 (5초 자동 갱신)                            │
│  - 모달 다이얼로그, 토스트 알림                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  REST API                                                   │
│  POST /api/pipeline/run                                     │
│  GET  /api/pipeline/status/{ticket}                         │
│  - 프로그래밍 방식으로 통합                                   │
│  - CI/CD 파이프라인 연동                                      │
│  - Discord/GitHub Webhook                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  CLI Scripts                                                │
│  bash scripts/run-agent.sh pm --ticket PLAN-001             │
│  python scripts/auto_pipeline.py                            │
│  - 세밀한 제어                                                │
│  - 디버깅 및 커스터마이징                                      │
└─────────────────────────────────────────────────────────────┘
```

### 3. Tech Stack Agnostic

모든 언어, 모든 프레임워크를 지원:
- **Web Fullstack**: Express+React, Django+Vue, FastAPI+Next.js
- **Web MVC**: Django, Rails, Spring Boot
- **CLI Tool**: Click, Cobra, Clap
- **Desktop App**: Tauri, Electron, Qt
- **Mobile App**: React Native, Flutter
- **Library**: npm, pip, cargo 패키지

### 4. 프로젝트 격리

```
KR-multi-agent-coding-team/          # ← 멀티 에이전트 시스템 (이 리포지토리)
└── team/
    ├── api/                         # REST API (FastAPI)
    ├── web/                         # 웹 대시보드
    ├── .agents/                     # 5개 에이전트
    ├── .skills/                     # 8개 스킬
    ├── scripts/                     # CLI 도구
    └── projects/
        ├── my-todo-app/             # ← 프로젝트 A (독립 Git 리포)
        │   ├── .git/
        │   ├── planning/
        │   └── src/
        └── my-blog/                 # ← 프로젝트 B (독립 Git 리포)
            ├── .git/
            ├── planning/
            └── src/
```

---

## 📦 사전 준비

### 필수
- [Claude Code](https://docs.claude.ai/claude-code) 설치 및 로그인
- Python 3.10+
- Git
- Claude Pro 이상 플랜 권장

### 선택 (고급 기능)
- Discord Webhook URL (알림 받으려면)
- GitHub Personal Access Token (Webhook 설정 시)

---

## 🌐 Phase 4: 웹 플랫폼 기능

### REST API (25+ 엔드포인트)

#### Agents
- `POST /api/agents/pm` - PM Agent 실행
- `POST /api/agents/coding` - Coding Agent 실행
- `POST /api/agents/qa` - QA Agent 실행
- `POST /api/agents/project-planner` - Project Planner 실행
- `POST /api/agents/stack-initializer` - Stack Initializer 실행
- `GET /api/agents/list` - 에이전트 목록

#### Skills
- `POST /api/skills/validate-spec` - 명세서 검증
- `POST /api/skills/commit` - 커밋 메시지 생성
- `POST /api/skills/review-pr` - PR 리뷰
- `POST /api/skills/refactor-code` - 리팩토링 제안
- `POST /api/skills/test-runner` - 테스트 실행
- `POST /api/skills/deploy` - 배포
- `POST /api/skills/benchmark` - 벤치마크
- `POST /api/skills/docs-generator` - 문서 생성
- `GET /api/skills/list` - 스킬 목록

#### Pipeline
- `POST /api/pipeline/run` - 파이프라인 실행
- `GET /api/pipeline/status/{ticket}` - 상태 조회
- `GET /api/pipeline/list` - 파이프라인 목록
- `POST /api/pipeline/cancel/{ticket}` - 파이프라인 취소
- `GET /api/pipeline/logs/{ticket}` - 로그 조회
- `GET /api/pipeline/stats` - 통계 조회

#### Webhooks
- `POST /api/webhooks/github` - GitHub Webhook (PR 자동 리뷰)
- `POST /api/webhooks/discord` - Discord 커맨드

#### Health
- `GET /api/health` - 헬스 체크
- `GET /api/info` - API 정보

### Discord 연동 (6가지 알림 타입)

1. **🚀 Pipeline Started**
   ```
   Ticket: PLAN-001
   Project: my-todo-app
   Status: 🟢 Running
   ```

2. **🤖 Agent Started/Completed**
   ```
   PM Agent Started
   Ticket: PLAN-001
   Duration: 45.2s
   ```

3. **✅ Tests Passed / ❌ Tests Failed**
   ```
   Tests Passed
   Coverage: 85%
   Duration: 12.3s
   ```

4. **🚀 Deployed to Production**
   ```
   Environment: production
   URL: https://my-app.com
   ```

5. **⚠️ PR Review Issues**
   ```
   PR #123: Add new feature
   Issues: 3 security warnings
   ```

6. **🛑 API Server Stopped**

### GitHub Webhook 설정

```bash
# 1. GitHub Repository → Settings → Webhooks
# 2. Add webhook
# 3. Payload URL: https://your-domain.com/api/webhooks/github
# 4. Content type: application/json
# 5. Secret: (환경 변수에 설정한 값)
# 6. Events: Pull requests, Issues
```

**자동 동작:**
- PR 생성/업데이트 → `review-pr` skill 자동 실행
- Issue 생성 → 티켓 자동 생성 (PLAN-XXX)

### 웹 대시보드

**4개 탭:**
1. **Pipelines** - 실시간 파이프라인 모니터링
   - 파이프라인 실행 폼
   - 진행 중인 파이프라인 그리드
   - 진행률 바 (0-100%)
   - 상태별 색상 (Running, Success, Failed)
   - 클릭하면 상세 모달

2. **Agents** - 5개 에이전트 카드
   - PM, Coding, QA, Project Planner, Stack Initializer
   - 티켓/프로젝트 입력 후 실행 버튼

3. **Skills** - 8개 스킬 카드
   - validate-spec, commit, review-pr, refactor-code
   - test-runner, deploy, benchmark, docs-generator
   - 클릭하면 파라미터 입력 후 실행

4. **Statistics** - 통계 대시보드
   - Total Pipelines
   - Success Rate
   - Average Duration
   - Active Now
   - Recent Activity 차트

**실시간 기능:**
- 5초마다 자동 갱신
- 토스트 알림 (성공/실패)
- 모달 다이얼로그 (파이프라인 상세)
- 로그 뷰어
- 파이프라인 취소 버튼

---

## 🔄 워크플로우

### 완전 자동 파이프라인 (웹 또는 API)

```bash
# 웹 대시보드에서:
1. Pipelines 탭 열기
2. Ticket: PLAN-001 입력
3. Project: my-todo-app 입력
4. "🚀 Run Pipeline" 버튼 클릭
5. 실시간 진행 상황 모니터링
6. Discord에서 알림 수신

# 또는 API로:
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"ticket": "PLAN-001", "project": "my-todo-app"}'
```

**자동 실행 단계:**
```
1. PM Agent → 명세서 생성
2. validate-spec skill → 명세서 검증
3. Coding Agent → 코드 구현
4. commit skill → 커밋 메시지 생성
5. QA Agent → 테스트 작성
6. test-runner skill → 테스트 실행
7. Git commit & push
```

### 수동 실행 (CLI - 세밀한 제어)

```bash
cd team

# 1. 프로젝트 초기화
bash scripts/init-project.sh --interactive

# 2. Stack Initializer (코딩 룰 자동 생성)
bash scripts/run-agent.sh stack-initializer

# 3. 티켓 생성
bash scripts/run-agent.sh project-planner --project "할일 관리 앱"

# 4. 티켓별 개발
bash scripts/run-agent.sh pm --ticket PLAN-001
bash scripts/run-skill.sh validate-spec PLAN-001
bash scripts/run-agent.sh coding --ticket PLAN-001
bash scripts/run-agent.sh qa --ticket PLAN-001

# 5. 커밋 (프로젝트 디렉토리에서)
cd projects/my-todo-app
git add .
git commit -m "feat(PLAN-001): 구현 완료"
git push origin feature/PLAN-001-xxx
cd ../..
```

---

## 🤖 에이전트 (5개)

| 에이전트 | 역할 | 입력 | 출력 |
|---------|------|------|------|
| `stack-initializer` | 스택 초기화 | `.project-meta.json` | 코딩 룰, 프로젝트 구조 |
| `project-planner` | 프로젝트 분해 | 자연어 설명 | `planning/tickets/PLAN-XXX-*.md` |
| `pm` | 요구사항 문서화 | 티켓 `.md` | 명세서, 테스트 케이스 |
| `coding` | 코드 구현 | 명세서 | `src/` 코드 |
| `qa` | 테스트 작성 | 테스트 케이스 | 테스트 코드 |

**모든 스택 지원** - 프로젝트 타입에 따라 자동 분기

---

## 🛠️ 스킬 (8개)

| 스킬 | 설명 | 자동 실행 | 수동 실행 |
|-----|------|---------|---------|
| `validate-spec` | 명세서 검증 | PM 후 | `POST /api/skills/validate-spec` |
| `commit` | 커밋 메시지 생성 | Coding 후 | `POST /api/skills/commit` |
| `review-pr` | PR 리뷰 | GitHub Webhook | `POST /api/skills/review-pr` |
| `refactor-code` | 리팩토링 제안 | - | `POST /api/skills/refactor-code` |
| `test-runner` | 테스트 실행 | QA 후 | `POST /api/skills/test-runner` |
| `deploy` | 배포 자동화 | - | `POST /api/skills/deploy` |
| `benchmark` | 성능 테스트 | - | `POST /api/skills/benchmark` |
| `docs-generator` | 문서 생성 | API 변경 시 | `POST /api/skills/docs-generator` |

**Skills는 재사용 가능하고 상태가 없는(stateless) 워크플로우 컴포넌트입니다.**

---

## ✨ 주요 기능

### 1. 🌐 웹 대시보드 (Phase 4 신규)

**CLI 없이 브라우저에서 모든 작업**
- 버튼 클릭으로 파이프라인 실행
- 실시간 진행 상황 모니터링
- 에이전트/스킬 개별 실행
- 로그 뷰어
- 통계 대시보드

### 2. 🔌 REST API (Phase 4 신규)

**프로그래밍 방식 통합**
- 25+ HTTP 엔드포인트
- Swagger UI 자동 생성
- Background task 지원
- CORS 설정

### 3. 🔵 Discord 연동 (Phase 4 신규)

**실시간 알림**
- 파이프라인 시작/완료
- 에이전트 실행 상황
- 테스트 결과
- 배포 상태
- 에러 알림

### 4. 🔗 GitHub Webhook (Phase 4 신규)

**자동화**
- PR 생성 시 자동 리뷰
- Issue 생성 시 티켓 자동 생성
- HMAC-SHA256 서명 검증

### 5. 🤖 자동 파이프라인

**전체 자동화**
```bash
python scripts/auto_pipeline.py --project "할일 관리 앱" --auto-push
```
- 티켓 생성부터 푸시까지 자동
- Rate limit 자동 관리
- 진행상황 저장 (`.pipeline-progress.json`)

### 6. 🌿 Git 브랜치 자동 관리

**에이전트가 자동으로 브랜치 생성/전환**
- PM: `docs/PLAN-001-xxx`
- Coding: `feature/PLAN-001-xxx`
- QA: `test/PLAN-001-xxx` (feature 브랜치 기반)

### 7. 🎨 Tech Stack Agnostic

**모든 언어, 모든 프레임워크**
- Stack Initializer가 공식 문서 기반 코딩 룰 자동 생성
- 6가지 프로젝트 타입
- 동적 디렉토리 구조

### 8. 📊 Rate Limit 추적

```bash
bash scripts/rate-limit-check.sh
```
- 일일/주간 사용량 자동 추적
- 제한 도달 전 경고

---

## 📁 프로젝트 구조

```
KR-multi-agent-coding-team/          # 멀티 에이전트 시스템 (이 리포지토리)
├── .git/                            # 시스템 Git
├── README.md                        # 이 파일
├── LICENSE
└── team/                            # ← 작업 디렉토리
    ├── api/                         # ✨ FastAPI REST API (Phase 4)
    │   ├── main.py                  # FastAPI 앱
    │   ├── config.py                # 설정
    │   ├── models/                  # Pydantic 모델
    │   │   ├── request.py
    │   │   └── response.py
    │   ├── routers/                 # 엔드포인트
    │   │   ├── agents.py
    │   │   ├── skills.py
    │   │   ├── pipeline.py
    │   │   └── webhooks.py
    │   ├── services/                # 비즈니스 로직
    │   │   ├── discord_service.py
    │   │   ├── agent_service.py
    │   │   ├── skill_service.py
    │   │   ├── pipeline_service.py
    │   │   └── webhook_service.py
    │   └── README.md                # API 문서
    │
    ├── web/                         # ✨ 웹 대시보드 (Phase 4)
    │   ├── index.html               # 메인 페이지
    │   └── static/
    │       ├── css/
    │       │   └── styles.css       # 스타일시트
    │       └── js/
    │           └── app.js           # 프론트엔드 로직
    │
    ├── .agents/                     # 5개 에이전트
    │   ├── stack-initializer/
    │   ├── project-planner/
    │   ├── pm/
    │   ├── coding/
    │   └── qa/
    │
    ├── .skills/                     # ✨ 8개 스킬 (Phase 3)
    │   ├── validate-spec/
    │   ├── commit/
    │   ├── review-pr/
    │   ├── refactor-code/
    │   ├── test-runner/
    │   ├── deploy/
    │   ├── benchmark/
    │   └── docs-generator/
    │
    ├── .rules/                      # 코딩 룰
    │   ├── general-coding-rules.md
    │   ├── _cache/                  # AI 자동 생성 (24h)
    │   └── _verified/               # 사람이 검증
    │
    ├── .config/                     # 시스템 설정
    │   └── git-workflow.json
    │
    ├── scripts/                     # CLI 도구
    │   ├── init-project.sh
    │   ├── switch-project.sh
    │   ├── run-agent.sh
    │   ├── run-skill.sh             # ✨ (Phase 3)
    │   ├── auto_pipeline.py         # ✨ Python 버전
    │   ├── git-branch-helper.sh
    │   └── rate-limit-check.sh
    │
    ├── docs/                        # 시스템 문서
    │   ├── session-management.md
    │   ├── skills-guide.md          # ✨ (Phase 3)
    │   └── phase4-complete.md       # ✨ (Phase 4)
    │
    ├── projects/                    # 프로젝트 작업 공간
    │   ├── my-todo-app/             # 프로젝트 A (독립 Git 리포)
    │   │   ├── .git/
    │   │   ├── .project-meta.json
    │   │   ├── planning/
    │   │   │   ├── tickets/
    │   │   │   ├── specs/
    │   │   │   └── test-cases/
    │   │   ├── src/
    │   │   └── logs/
    │   └── my-blog/                 # 프로젝트 B (독립 Git 리포)
    │
    ├── requirements.txt             # Python 의존성
    ├── .env.example                 # 환경 변수 템플릿
    └── .gitignore
```

---

## 🔧 환경 변수

`.env.example` → `.env`로 복사 후 설정:

```bash
# Discord Integration (선택)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN

# GitHub Webhook (선택)
GITHUB_WEBHOOK_SECRET=your-github-webhook-secret

# Anthropic API (필수)
ANTHROPIC_API_KEY=sk-ant-your-api-key

# API Server
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 📚 문서

- **API 문서**: [team/api/README.md](team/api/README.md)
- **Skills 가이드**: [team/docs/skills-guide.md](team/docs/skills-guide.md)
- **Phase 4 완료 보고서**: [team/docs/phase4-complete.md](team/docs/phase4-complete.md)
- **세션 관리**: [team/docs/session-management.md](team/docs/session-management.md)

---

## 🎯 사용 시나리오

### 시나리오 1: 신규 프로젝트 (웹 대시보드)

1. **API 서버 실행**
   ```bash
   cd team
   uvicorn api.main:app --reload --port 8000
   ```

2. **웹 브라우저 접속**: `http://localhost:8000`

3. **Pipelines 탭에서 파이프라인 실행**
   - Ticket: `PLAN-001`
   - Project: `my-todo-app`
   - 버튼 클릭

4. **실시간 모니터링**
   - 진행 상황 그리드에서 확인
   - Discord에서 알림 수신

5. **완료 후 PR 리뷰**
   - GitHub에서 생성된 PR 확인

### 시나리오 2: 기존 프로젝트에 기능 추가 (API)

```bash
# 1. 티켓 생성
curl -X POST http://localhost:8000/api/agents/project-planner \
  -H "Content-Type: application/json" \
  -d '{"project": "새로운 기능 추가"}'

# 2. 파이프라인 실행
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"ticket": "PLAN-002", "project": "my-todo-app"}'

# 3. 상태 확인
curl http://localhost:8000/api/pipeline/status/PLAN-002
```

### 시나리오 3: PR 리뷰 자동화 (GitHub Webhook)

1. **GitHub Webhook 설정** (위 섹션 참조)
2. **PR 생성** → 자동으로 `review-pr` skill 실행
3. **Discord 알림** 수신
4. **리뷰 결과 확인** → PR 코멘트

### 시나리오 4: 세밀한 제어 (CLI)

```bash
cd team

# 개별 에이전트 실행
bash scripts/run-agent.sh pm --ticket PLAN-001
bash scripts/run-agent.sh coding --ticket PLAN-001

# 개별 스킬 실행
bash scripts/run-skill.sh validate-spec PLAN-001
bash scripts/run-skill.sh commit PLAN-001
bash scripts/run-skill.sh review-pr PLAN-001

# 자동 파이프라인 (Python)
python scripts/auto_pipeline.py --project "새 프로젝트" --auto-push
```

---

## 🔄 Phase별 발전 과정(v0.0.3)

### Phase 1-2: CLI 기반 멀티 에이전트 시스템
- 5개 에이전트 (stack-initializer, project-planner, pm, coding, qa)
- Git 브랜치 자동 관리
- Rate limit 추적
- Tech stack agnostic

### Phase 3: Skills 아키텍처 (2026-03-19)
- 8개 재사용 가능 스킬 추가
- Agent와 Skill 분리 (복잡한 결정 vs 반복 작업)
- 스킬 메모리 시스템 (학습 기능)
- 22 files, 6,040 lines 추가

### Phase 4: 웹 플랫폼 (2026-03-19) ✨ 현재
- **FastAPI REST API** (25+ 엔드포인트)
- **웹 대시보드** (4개 탭, 실시간 모니터링)
- **Discord 연동** (6가지 알림 타입)
- **GitHub Webhook** (PR 자동 리뷰)
- 18 files, 4,000+ lines 추가

---

## 🚧 향후 계획

### Phase 4.1: Database Integration (계획 중)
- PostgreSQL 연동
- 파이프라인 히스토리 저장
- 검색/필터 기능

### Phase 4.2: Authentication (계획 중)
- JWT 인증
- API Key 관리
- Role-based access control

### Phase 4.3: WebSocket (계획 중)
- 실시간 푸시 알림 (polling 대체)
- 더 빠른 상태 업데이트

### Phase 4.4: Production Deployment (계획 중)
- Docker 컨테이너화
- Kubernetes 배포 매니페스트
- Monitoring (Prometheus/Grafana)

---

## 🤝 기여 가이드

### 검증된 코딩 룰 기여
`.rules/_verified/`에 새로운 스택의 코딩 룰 기여 가능

### 새로운 스킬 기여
`.skills/` 디렉토리에 새로운 스킬 추가 가능

### API 엔드포인트 기여
`team/api/routers/`에 새로운 라우터 추가 가능

---

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

---

## 🔗 관련 링크

- **Claude Code 문서**: [https://docs.claude.ai/claude-code](https://docs.claude.ai/claude-code)
- **API 문서**: `http://localhost:8000/api/docs` (서버 실행 후)
- **Discord Developer Portal**: [https://discord.com/developers](https://discord.com/developers)
- **GitHub Webhooks**: [https://docs.github.com/en/webhooks](https://docs.github.com/en/webhooks)

---

**버전**: v0.0.3
**최종 업데이트**: 2026-03-19

## 🆕 최근 업데이트 (2026-03-19)

### Phase 4: 웹 플랫폼 완성 ✨

**Backend:**
- ✅ FastAPI REST API (25+ 엔드포인트)
- ✅ Pydantic 모델 (Request/Response)
- ✅ Background Tasks (비동기 실행)
- ✅ CORS 미들웨어
- ✅ Swagger UI 자동 생성

**Integration:**
- ✅ Discord Webhook (6가지 알림 타입)
- ✅ GitHub Webhook (PR 자동 리뷰)
- ✅ HMAC-SHA256 서명 검증

**Frontend:**
- ✅ 웹 대시보드 (4개 탭)
- ✅ 실시간 모니터링 (5초 자동 갱신)
- ✅ 모달 다이얼로그
- ✅ 토스트 알림
- ✅ 반응형 디자인

**Architecture:**
- ✅ Service Layer (Agent, Skill, Pipeline, Discord, Webhook)
- ✅ DTO Pattern (Pydantic)
- ✅ Repository Pattern (PipelineService)
- ✅ Observer Pattern (Discord 알림)

자세한 내용: [team/docs/phase4-complete.md](team/docs/phase4-complete.md)

---

**🌟 이제 Multi-Agent Coding Team은 CLI, REST API, 웹 대시보드 3가지 방법으로 사용할 수 있습니다!**
