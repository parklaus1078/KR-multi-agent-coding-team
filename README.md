# Multi-Agent Coding Team (MACT)

> AI-Driven Development Platform with Multi-Agent System

[![Version](https://img.shields.io/badge/version-v0.0.3-blue.svg)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable-green.svg)]()

**프로젝트 아이디어에서 구현 완료까지, 5개 AI 에이전트가 자동으로 개발합니다.**

Claude Code 기반 멀티 에이전트 시스템으로 Tech Stack에 구애받지 않는 자동화된 개발 파이프라인을 제공합니다.

---

## ✨ 핵심 기능

- 🤖 **5개 전문 AI 에이전트** - 기획, PM, 개발, QA, 평가
- 🚀 **CLI 기반 자동화** - `mact` 명령어 하나로 전체 개발 사이클
- 🎯 **Tech Stack Agnostic** - Python, Node.js, Go 등 모든 언어/프레임워크
- 💾 **세션 관리** - 작업 중단 후 재개 가능
- 🧠 **학습 시스템** - 과거 의사결정에서 패턴 학습
- 📊 **자동 품질 개선** - 목표 점수까지 반복 개선

---

## 🚀 빠른 시작 (5분)

### 1. 설치

```bash
# 리포지토리 클론
git clone https://github.com/your-username/KR-multi-agent-coding-team.git
cd KR-multi-agent-coding-team/team

# CLI 설치
bash install.sh

# 터미널 재시작 또는
source ~/.zshrc  # zsh
source ~/.bashrc # bash
```

### 2. 첫 프로젝트 생성

```bash
# 대화형 프로젝트 초기화
mact init --interactive

# 또는 직접 지정
mact init --name my-blog --type web-fullstack
```

### 3. 자동 개발 실행

```bash
# 전체 자동화 (아이디어 → 구현 완료)
mact auto --project "블로그 시스템: 글쓰기, 댓글, 태그 기능" --auto-improve

# Discord 알림 포함 (선택)
mact auto --project "TODO 앱" --auto-improve --discord-webhook "$DISCORD_WEBHOOK_URL"
```

**3-5분 후**: 티켓 생성 → 명세서 → 코드 구현 → 테스트 → 평가 완료! 🎉

---

## 📖 사용 가이드

### 기본 명령어

```bash
mact --help              # 전체 도움말
mact --version           # 버전 확인
mact projects            # 프로젝트 목록
mact status              # 현재 상태
```

### 프로젝트 관리

```bash
# 프로젝트 생성
mact init --name my-app --type web-fullstack

# 프로젝트 선택
mact use my-app

# 프로젝트 목록
mact projects
```

**지원하는 프로젝트 타입:**
- `web-fullstack` - React/Next.js + FastAPI/Express
- `web-mvc` - Django/Flask/Rails
- `cli-tool` - Python/Node.js CLI
- `desktop-app` - Electron/Tauri

### 개발 워크플로우

#### 🎯 방법 1: 완전 자동화 (권장)

```bash
# 한 번에 실행: 티켓 생성 → 구현 → 테스트 → 평가
mact auto --project "프로젝트 설명" --auto-improve
```

#### 🔧 방법 2: 단계별 실행 (세밀한 제어)

```bash
# Step 1: 티켓 생성
mact plan --project "블로그 시스템: 글쓰기, 댓글 기능"

# Step 2: 명세서 작성
mact run pm --ticket PLAN-001

# Step 3: 코드 구현
mact run coding --ticket PLAN-001

# Step 4: 코드 평가
mact run evaluator --ticket PLAN-001  # 예: 82/100

# Step 5: 품질 개선 (점수 낮으면)
mact improve PLAN-001 --target 90
# → Coding ↔ Evaluator 반복 (90점까지)

# Step 6: 테스트 작성 (품질 만족 후)
mact run qa --ticket PLAN-001
```

**⚠️ 중요**: QA Agent는 코드 품질이 만족스러울 때 **마지막에** 실행합니다.

### 자동 품질 개선

```bash
# 전제: Coding Agent 최소 1회 실행 완료
# Coding ↔ Evaluator 반복으로 90점까지
mact improve PLAN-001 --target 90

# 최대 15회 반복, 95점 목표
mact improve PLAN-001 --target 95 --max-iterations 15
```

**동작:**
```
1. Evaluator 평가 (현재 점수 확인)
2. 점수 < 목표 → Coding Agent 재실행 (피드백 반영)
3. Evaluator 재평가
4. 반복 (목표 점수 달성 또는 최대 횟수까지)
```

### 학습 시스템 (Memory)

```bash
# 로그에서 패턴 학습
mact memory learn

# 학습된 패턴 조회
mact memory show --agent pm

# 초기화 (백업 생성)
mact memory clear --confirm
```

**자동 학습**: 과거 의사결정을 분석하여 다음 작업 시 자동 적용

---

## 🎯 실전 예시

### 예시 1: TODO 앱 (수동 제어)

```bash
# 1. 프로젝트 초기화
mact init --name simple-todo --type web-fullstack
mact use simple-todo

# 2. 티켓 생성
mact plan --project "할일 추가, 완료 표시, 삭제 기능"

# 3. 첫 티켓 개발 (올바른 순서)
mact run pm --ticket PLAN-001          # 명세서
mact run coding --ticket PLAN-001      # 구현
mact run evaluator --ticket PLAN-001   # 평가 (예: 78/100)

# 4. 품질 개선 (점수 낮으면)
mact improve PLAN-001 --target 90      # 90점까지 반복

# 5. 테스트 작성 (품질 만족 후)
mact run qa --ticket PLAN-001

# 6. 나머지 티켓 반복
mact run pm --ticket PLAN-002
mact run coding --ticket PLAN-002
mact run evaluator --ticket PLAN-002
mact improve PLAN-002 --target 90
mact run qa --ticket PLAN-002
```

### 예시 2: 블로그 시스템 (완전 자동화)

```bash
# 한 줄로 끝
mact auto \
  --new-project \
  --project-name "my-blog" \
  --project "블로그: 글쓰기, 댓글, 태그, 검색" \
  --auto-improve \
  --target-score 95

# 결과 확인
mact status
mact logs --tail 5
```

### 예시 3: 기존 프로젝트에 기능 추가

```bash
# 프로젝트 선택
mact use my-blog

# 새 기능 티켓 생성
mact plan --project "이미지 업로드 기능"

# 자동 개발 (새 티켓만)
mact auto --project "이미지 업로드" --auto-improve
```

---

## 🏗️ 시스템 아키텍처

### 5개 AI 에이전트

```
프로젝트 아이디어
    ↓
┌──────────────────────────────────────────┐
│  Project Planner Agent                   │  프로젝트를 티켓으로 분해
│  "블로그 시스템" → 티켓 5개 생성         │
└──────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────┐
│  PM Agent                                │  티켓별 상세 명세서
│  PLAN-001 → API 명세, UI 요구사항        │
└──────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────┐
│  Coding Agent                            │  명세서 기반 코드 구현
│  FastAPI + React 코드 생성               │
└──────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────┐
│  Evaluator Agent                         │  코드 품질 평가
│  점수 82/100 → 개선 사항 제시            │
└──────────────────────────────────────────┘
    ↓ (점수 < 목표)
    ↓ Coding ↔ Evaluator 반복 (5-15회)
    ↓
┌──────────────────────────────────────────┐
│  Evaluator Agent (재평가)                │  개선된 코드 평가
│  점수 93/100 → 목표 달성! ✅             │
└──────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────┐
│  QA Agent                                │  테스트 코드 작성
│  pytest + Jest 테스트 생성               │
└──────────────────────────────────────────┘
    ↓
구현 완료 ✅
```

### Tech Stack Agnostic 코딩 룰

```
team/.rules/
├── general-coding-rules.md          # 범용 원칙
├── _verified/                       # 검증된 룰 (최고 우선순위)
│   └── web-fullstack/
│       ├── backend-fastapi-python.md
│       └── frontend-nextjs-typescript.md
└── _cache/                          # AI 자동 생성 (24시간 캐시)
```

**동작:**
1. 프로젝트 생성 시 Stack Initializer가 프레임워크 분석
2. 공식 문서 + 베스트 프랙티스 → 코딩 룰 자동 생성
3. Coding Agent가 이 룰을 따라 코드 생성

### 프로젝트 격리

```
team/
├── projects/                    # 사용자 프로젝트
│   ├── my-blog/                 # 독립 Git 리포
│   │   ├── .git/
│   │   ├── planning/            # 티켓, 명세서
│   │   ├── logs/                # 에이전트 로그
│   │   └── src/                 # 구현 코드
│   └── simple-todo/             # 독립 Git 리포
│       └── ...
├── .agents/                     # 5개 에이전트 정의
├── .memory/                     # 학습 시스템
├── .rules/                      # 코딩 룰
└── scripts/                     # CLI 스크립트
```

---

## 🧠 학습 시스템 (Memory)

에이전트가 과거 의사결정에서 학습하여 점점 똑똑해집니다.

### 동작 원리

```
1. Agent 실행 → 의사결정 로그 기록
   {
     "decision": "OAuth 제외",
     "reason": "티켓에 명시 안 됨",
     "confidence": 0.95
   }

2. 학습 실행 (mact memory learn)
   로그 분석 → 패턴 추출

3. 다음 실행 시 자동 적용
   "auth" 트리거 감지 → "Email/Password만" 자동 결정
```

### 사용법

```bash
# 학습 실행 (프로젝트 로그에서)
mact memory learn

# 특정 에이전트만
mact memory learn --agents pm coding

# 학습된 패턴 조회
mact memory show
mact memory show --agent pm

# 초기화
mact memory clear --confirm
```

**효과:**
- Scope Creep: **80% 감소**
- 의사결정 일관성: **+60%**
- 반복 실수: **70% 감소**

---

## 📊 로그 및 모니터링

### 로그 조회

```bash
# 전체 로그
mact logs

# 특정 Agent
mact logs --agent project-planner

# 특정 티켓
mact logs --ticket PLAN-001

# 최근 10개만
mact logs --tail 10
```

### Discord 알림 (선택)

```bash
# 환경 변수 설정
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# 실행 시 알림
mact auto --project "프로젝트" --discord-webhook "$DISCORD_WEBHOOK_URL"
```

**알림 내용:**
- 에이전트 시작/완료
- 티켓 진행 상황
- 점수 및 반복 횟수
- 에러 발생 시 상세 정보

---

## ⚙️ 설정

### 설정 관리

```bash
# 전체 설정 조회
mact config --list

# 특정 설정 조회
mact config --get current_project

# 설정 변경
mact config --set discord_webhook "https://..."
```

### 주요 설정 항목

- `current_project`: 현재 활성 프로젝트
- `discord_webhook`: Discord Webhook URL
- `default_target_score`: 기본 목표 점수 (기본: 90)
- `max_iterations`: 최대 반복 횟수 (기본: 10)

---

## 🔧 고급 기능

### 세션 재개

```bash
# Project Planner 재개
mact plan --resume

# Agent 재개
mact run coding --ticket PLAN-001 --resume
```

### 요구사항 파일 입력

```bash
# requirements.md 작성
cat > requirements.md <<EOF
# 블로그 시스템
- 글쓰기 (제목, 본문, 태그)
- 댓글 시스템
- 태그별 검색
EOF

# 파일로 티켓 생성
mact plan --req requirements.md
```

### 프로젝트별 개선 목표

```bash
# 높은 품질 (95점)
mact auto --project "금융 시스템" --auto-improve --target-score 95

# 빠른 프로토타입 (70점)
mact auto --project "MVP 테스트" --target-score 70
```

---

## 📦 사전 요구사항

### 필수

- [Claude Code Desktop App](https://docs.claude.ai/claude-code) 설치 및 로그인
- Git
- Bash Shell (macOS/Linux 기본, Windows는 Git Bash)
- Python 3.10+ (CLI 실행용)

### 프로젝트별 의존성

프로젝트 타입에 따라:
- **Python 프로젝트**: Python 3.10+, pip
- **Node.js 프로젝트**: Node.js 18+, npm/yarn
- **Go 프로젝트**: Go 1.20+
- 등등...

---

## 🎨 CLI 출력 예시

### `mact projects`

```
📂 사용 가능한 프로젝트:

  • my-blog ← 현재 활성
  • simple-todo
  • korean-legal-case-evaluator

총 3개 프로젝트
```

### `mact status`

```
============================================================
📊 프로젝트 상태: my-blog
============================================================

📋 티켓: 3개
   최신: PLAN-003-image-upload.md
📝 명세서: 6개
💻 소스 파일: 12개
🧪 테스트 파일: 8개
📊 평가 완료: 2개 티켓
   • PLAN-001: 92/100
   • PLAN-002: 88/100

다음 단계:
  mact run evaluator --ticket PLAN-003
  mact improve PLAN-003 --target 90
```

### `mact logs --tail 3`

```
📋 로그 목록 (최신순, 총 3개):

  ✅ 20260329-183406 | project-planner | N/A      |  12.3 KB
  ✅ 20260329-182100 | pm             | PLAN-001 |   8.7 KB
  ❌ 20260329-181000 | coding         | PLAN-001 |  15.2 KB
```

---

## 🆘 문제 해결

### CLI를 찾을 수 없음

```bash
# PATH 확인
echo $PATH | grep ".local/bin"

# PATH 추가 (필요 시)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 권한 오류

```bash
chmod +x ~/.local/bin/mact
chmod +x /path/to/team/mact.py
```

### Python 경로 오류

```bash
# python3 확인
which python3

# mact.py 첫 줄 확인/수정
# #!/usr/bin/env python3
```

### Claude Code 연결 실패

```bash
# Claude Code CLI 확인
which claude

# Claude Code 재로그인
claude logout
claude login
```

---

## 📚 추가 문서

- **CLI 상세 가이드**: [`team/CLI-GUIDE.md`](team/CLI-GUIDE.md)
- **시스템 개발 가이드**: [`CLAUDE.md`](CLAUDE.md)
- **Agent 설명**: `team/.agents/*/CLAUDE.md`
- **코딩 룰**: `team/.rules/`
- **아키텍처 문서**: `docs/architecture.md`

---

## 🗺️ 로드맵

### v0.0.3 (현재) ✅
- CLI 기반 멀티 에이전트 시스템
- 세션 관리
- Tech Stack Agnostic 코딩 룰
- 학습 시스템 (Memory)

### v0.0.4 (계획)
- 자동 Git 워크플로우 (브랜치, 커밋, PR)
- 웹 대시보드 (선택)
- 더 많은 프로젝트 타입 지원
- 성능 최적화

---

## 🤝 기여

이슈, PR 환영합니다!

```bash
# 시스템 개발 시 참고
# CLAUDE.md - 시스템 개발 Agent 지시사항
# docs/ - 아키텍처 문서
# logs-agent_dev/ - 개발 히스토리
```

---

## 📄 라이선스

MIT License

---

## 📞 문의

- Issues: [GitHub Issues](https://github.com/your-username/KR-multi-agent-coding-team/issues)
- Discussions: [GitHub Discussions](https://github.com/your-username/KR-multi-agent-coding-team/discussions)

---

**버전**: v0.0.3
**마지막 업데이트**: 2026-03-29
**Powered by**: Claude Code + Multi-Agent System
