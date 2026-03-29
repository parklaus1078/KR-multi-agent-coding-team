# MACT CLI 사용 가이드

> **MACT** = Multi-Agent Coding Team

Tech Stack Agnostic 멀티 에이전트 개발 플랫폼을 위한 통합 CLI 도구입니다.

---

## 🚀 설치

```bash
cd team
bash install.sh
```

설치 후 터미널을 재시작하거나:

```bash
source ~/.zshrc  # zsh 사용 시
source ~/.bashrc # bash 사용 시
```

---

## 📖 명령어 목록

### 기본 명령어

```bash
mact --help              # 전체 도움말
mact --version           # 버전 확인
mact <command> --help    # 특정 명령어 도움말
```

---

## 🎯 주요 워크플로우

### 1. 프로젝트 초기화

```bash
# 새 프로젝트 생성
mact init --name my-blog --type web-fullstack

# 대화형 모드
mact init --interactive
```

**프로젝트 타입**:
- `web-fullstack` - React/Next.js + FastAPI/Express
- `web-mvc` - Django/Flask/Rails
- `cli-tool` - Python/Node.js CLI
- `desktop-app` - Electron/Tauri

### 2. 프로젝트 관리

```bash
# 프로젝트 목록
mact projects
mact ls          # 별칭

# 프로젝트 선택
mact use my-blog
mact switch my-blog  # 별칭

# 현재 상태 확인
mact status
```

### 3. 티켓 생성 (Project Planner)

```bash
# 프로젝트 설명으로 티켓 생성
mact plan --project "블로그 시스템: 글쓰기, 댓글, 태그 기능"

# 요구사항 파일로 티켓 생성
mact plan --req requirements.md

# 이전 세션 재개
mact plan --resume
```

### 4. 개발 파이프라인

```bash
# PM Agent - 명세서 작성
mact run pm --ticket PLAN-001

# Coding Agent - 코드 구현
mact run coding --ticket PLAN-001

# QA Agent - 테스트 작성
mact run qa --ticket PLAN-001

# Evaluator Agent - 코드 평가
mact run evaluator --ticket PLAN-001
```

### 5. 자동 품질 개선

```bash
# Coding ↔ Evaluator 반복 (90점까지)
mact improve PLAN-001 --target 90

# 최대 15회 반복
mact improve PLAN-001 --target 95 --max-iterations 15
```

### 6. 전체 자동화 (0 to 1)

```bash
# 기본 자동화 (평가만)
mact auto --project "할일 관리 앱"

# 자동 개선 포함 (90점까지)
mact auto --project "블로그 시스템" --auto-improve

# 새 프로젝트 생성 + 자동화
mact auto --new-project --project-name "my-shop" --project "쇼핑몰" --auto-improve

# Discord 알림 포함
mact auto --project "블로그" --auto-improve --discord-webhook "https://discord.com/..."
```

### 7. 로그 조회

```bash
# 전체 로그 (최신순)
mact logs

# 특정 Agent 로그
mact logs --agent project-planner

# 특정 티켓 로그
mact logs --ticket PLAN-001

# 최근 10개만
mact logs --tail 10
```

### 8. 설정 관리

```bash
# 전체 설정 조회
mact config --list

# 특정 설정 조회
mact config --get current_project

# 설정 변경
mact config --set discord_webhook "https://discord.com/..."
```

---

## 📋 실전 예시

### 예시 1: 간단한 TODO 앱 (수동)

```bash
# 1. 프로젝트 초기화
mact init --name simple-todo --type web-fullstack

# 2. 프로젝트 선택
mact use simple-todo

# 3. 티켓 생성
mact plan --project "할일 추가, 완료 표시, 삭제 기능"

# 4. 첫 번째 티켓 개발
mact run pm --ticket PLAN-001
mact run coding --ticket PLAN-001
mact run qa --ticket PLAN-001
mact run evaluator --ticket PLAN-001

# 5. 개선 (필요 시)
mact improve PLAN-001 --target 90

# 6. 나머지 티켓도 반복
mact run pm --ticket PLAN-002
# ...
```

### 예시 2: 블로그 시스템 (완전 자동화)

```bash
# 한 번에 실행
mact auto \
  --new-project \
  --project-name "my-blog" \
  --project "블로그 시스템: 글쓰기, 댓글, 태그, 검색 기능" \
  --auto-improve \
  --target-score 95 \
  --discord-webhook "$DISCORD_WEBHOOK_URL"

# 결과 확인
mact status
mact logs --tail 5
```

### 예시 3: 기존 프로젝트에 기능 추가

```bash
# 1. 프로젝트 선택
mact use my-blog

# 2. 새 기능 티켓 생성
mact plan --project "이미지 업로드 기능 추가"

# 3. 자동화 실행 (기존 티켓은 건너뛰고 새 티켓만 처리)
mact auto --project "이미지 업로드" --auto-improve
```

---

## 🎨 출력 예시

### `mact projects`

```
📂 사용 가능한 프로젝트:

  • my-blog ← 현재 활성
  • simple-todo
  • korean-legal-case-evaluator

총 3개 프로젝트

사용법:
  mact use my-blog
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

📂 프로젝트 경로:
   /path/to/projects/my-blog

다음 단계:
  mact run evaluator --ticket PLAN-003
  mact improve PLAN-003 --target 90
```

### `mact logs --tail 3`

```
📋 로그 목록 (최신순, 총 3개):

  ✅ 20260329-183406 | project-planner | N/A        |   12.3 KB
     20260329-183406-project-planner.log
  ✅ 20260329-182100 | pm             | PLAN-001   |    8.7 KB
     20260329-182100-pm-PLAN-001.log
  ❌ 20260329-181000 | coding         | PLAN-001   |   15.2 KB
     20260329-181000-coding-PLAN-001.log

로그 파일 경로:
  /path/to/projects/my-blog/logs/orchestrator

로그 보기:
  cat /path/to/projects/my-blog/logs/orchestrator/20260329-183406-project-planner.log
```

---

## 🔧 고급 사용법

### Discord Webhook 설정

```bash
# 1. Discord Webhook URL 발급 (서버 설정 → 연동 → 웹후크)

# 2. 환경 변수 설정
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# 3. 실행
mact auto --project "프로젝트" --auto-improve --discord-webhook "$DISCORD_WEBHOOK_URL"

# 또는 설정에 저장
mact config --set discord_webhook "$DISCORD_WEBHOOK_URL"
```

### 세션 재개

```bash
# Project Planner 세션 재개
mact plan --resume

# Agent 세션 재개
mact run coding --ticket PLAN-001 --resume
```

---

## 📚 추가 문서

- **전체 시스템 가이드**: `../README.md`
- **Agent 설명**: `.agents/*/CLAUDE.md`
- **코딩 룰**: `.rules/`
- **API 문서**: `api/README.md`

---

## 🆘 문제 해결

### CLI를 찾을 수 없음

```bash
# PATH 확인
echo $PATH | grep ".local/bin"

# PATH 추가 (zsh)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# PATH 추가 (bash)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Python 경로 오류

```bash
# python3 확인
which python3

# 필요 시 mact.py 첫 줄 수정
# #!/usr/bin/env python3
```

### 권한 오류

```bash
chmod +x ~/.local/bin/mact
chmod +x /path/to/team/mact.py
```

---

**버전**: v0.0.3
**마지막 업데이트**: 2026-03-29
