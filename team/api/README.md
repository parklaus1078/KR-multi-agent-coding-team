# Multi-Agent Coding Team API

FastAPI 기반 REST API + Discord 연동 + 웹 대시보드

---

## 🚀 Quick Start

### 1. 설치

```bash
# Requirements 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 수정하여 DISCORD_WEBHOOK_URL 등을 설정
```

### 2. API 서버 실행

```bash
# 개발 모드 (자동 재시작)
uvicorn api.main:app --reload --port 8000

# 또는 직접 실행
python -m api.main
```

### 3. 웹 대시보드 접속

```
http://localhost:8000
```

### 4. API 문서 확인

```
Swagger UI: http://localhost:8000/api/docs
ReDoc: http://localhost:8000/api/redoc
```

---

## 📡 API Endpoints

### Agents

```bash
# PM Agent 실행
curl -X POST http://localhost:8000/api/agents/pm \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-cli-tool",
    "auto_mode": true
  }'

# Coding Agent 실행
curl -X POST http://localhost:8000/api/agents/coding \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-cli-tool"
  }'

# QA Agent 실행
curl -X POST http://localhost:8000/api/agents/qa \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-cli-tool"
  }'

# 에이전트 목록 조회
curl http://localhost:8000/api/agents/list
```

### Skills

```bash
# validate-spec skill 실행
curl -X POST http://localhost:8000/api/skills/validate-spec \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-cli-tool",
    "auto_fix": true
  }'

# commit skill 실행
curl -X POST http://localhost:8000/api/skills/commit \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-cli-tool"
  }'

# test-runner skill 실행
curl -X POST http://localhost:8000/api/skills/test-runner \
  -H "Content-Type: application/json" \
  -d '{
    "project": "my-cli-tool",
    "args": {"coverage": true}
  }'

# Skills 목록 조회
curl http://localhost:8000/api/skills/list
```

### Pipeline

```bash
# 전체 파이프라인 실행
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "PLAN-001",
    "project": "my-cli-tool",
    "resume": false
  }'

# 파이프라인 상태 조회
curl http://localhost:8000/api/pipeline/status/PLAN-001

# 파이프라인 목록 조회
curl http://localhost:8000/api/pipeline/list

# 파이프라인 취소
curl -X POST http://localhost:8000/api/pipeline/cancel/PLAN-001

# 로그 조회
curl http://localhost:8000/api/pipeline/logs/PLAN-001

# 통계 조회
curl http://localhost:8000/api/pipeline/stats
```

### Webhooks

```bash
# GitHub Webhook (GitHub에서 자동 호출)
POST /api/webhooks/github
Headers:
  X-GitHub-Event: pull_request
  X-Hub-Signature-256: sha256=...

# Discord Command (Discord Bot에서 호출)
POST /api/webhooks/discord
{
  "command": "run",
  "args": ["PLAN-001"],
  "user_id": "123456789",
  "channel_id": "987654321"
}
```

---

## 🔵 Discord 연동

### 1. Webhook URL 생성

1. Discord 서버 설정 → 연동 → 웹후크
2. 새 웹후크 생성
3. 웹후크 URL 복사

### 2. 환경 변수 설정

```bash
export DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
```

### 3. 알림 수신

파이프라인 실행 시 자동으로 Discord 알림:

- 🚀 Pipeline Started
- 🤖 Agent Started/Completed
- ✅ Tests Passed / ❌ Tests Failed
- 🚀 Deployed to Production
- ⚠️ PR Review Issues

### Discord 알림 예시

```
🚀 Pipeline Started
━━━━━━━━━━━━━━━━━━━━
Ticket: PLAN-001
Project: my-cli-tool
━━━━━━━━━━━━━━━━━━━━
Mode: New | Status: 🟢 Running
```

---

## 🔗 GitHub Webhook 설정

### 1. Repository 설정

1. GitHub Repository → Settings → Webhooks
2. Add webhook
3. Payload URL: `https://your-domain.com/api/webhooks/github`
4. Content type: `application/json`
5. Secret: (설정한 SECRET)
6. Events: Pull requests, Issues

### 2. 환경 변수 설정

```bash
export GITHUB_WEBHOOK_SECRET=your-secret
```

### 3. 자동 동작

- **PR 생성/업데이트** → review-pr skill 자동 실행
- **Issue 생성** → 티켓 자동 생성 (추후 구현)

---

## 🏗️ Architecture

```
api/
├── main.py                 # FastAPI 앱
├── config.py               # 설정
├── models/
│   ├── request.py          # Request 모델
│   └── response.py         # Response 모델
├── routers/
│   ├── agents.py           # /api/agents/*
│   ├── skills.py           # /api/skills/*
│   ├── pipeline.py         # /api/pipeline/*
│   └── webhooks.py         # /api/webhooks/*
└── services/
    ├── agent_service.py    # 에이전트 실행
    ├── skill_service.py    # Skill 실행
    ├── pipeline_service.py # 파이프라인 관리
    ├── discord_service.py  # Discord 연동
    └── webhook_service.py  # Webhook 처리
```

---

## 📊 Response Examples

### Agent Run Response

```json
{
  "success": true,
  "agent": "pm",
  "ticket": "PLAN-001",
  "session_id": "abc123",
  "message_count": 5,
  "duration_seconds": 45.2,
  "output": "명세서 생성 완료",
  "error": null
}
```

### Pipeline Status Response

```json
{
  "ticket": "PLAN-001",
  "status": "running",
  "current_step": "coding",
  "progress": 60,
  "started_at": "2026-03-19T10:00:00Z",
  "completed_at": null,
  "steps": [
    {"name": "pm", "status": "success", "duration": 45.2},
    {"name": "validate-spec", "status": "success", "duration": 2.1},
    {"name": "coding", "status": "running", "duration": null}
  ],
  "error": null
}
```

---

## 🔧 Development

### Running Tests

```bash
pytest api/tests/
```

### Code Style

```bash
# Format
black api/

# Lint
pylint api/
```

---

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_WEBHOOK_URL` | Yes | Discord webhook URL |
| `GITHUB_WEBHOOK_SECRET` | No | GitHub webhook secret |
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key |
| `API_HOST` | No | API host (default: 0.0.0.0) |
| `API_PORT` | No | API port (default: 8000) |

---

## 🚨 Error Handling

모든 엔드포인트는 다음 형식의 에러를 반환합니다:

```json
{
  "detail": "Error message"
}
```

HTTP Status Codes:
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Discord Webhooks Guide](https://discord.com/developers/docs/resources/webhook)
- [GitHub Webhooks Guide](https://docs.github.com/en/webhooks)
