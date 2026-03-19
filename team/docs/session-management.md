# 에이전트 세션 관리 가이드

## 개요

모든 에이전트 실행은 자동으로 세션을 저장합니다. 나중에 코드가 마음에 들지 않으면, 해당 에이전트 세션을 재개하여 수정을 요청할 수 있습니다.

---

## 세션 자동 저장

### 저장 위치

```
projects/my-todo-app/
└── .sessions/
    ├── PLAN-001/
    │   ├── pm.session           # PM Agent 세션 ID
    │   ├── coding.session       # Coding Agent 세션 ID
    │   └── qa.session           # QA Agent 세션 ID
    ├── PLAN-002/
    │   ├── pm.session
    │   ├── coding.session
    │   └── qa.session
    └── session-map.json         # 모든 세션 메타데이터
```

### session-map.json 구조

```json
{
  "PLAN-001": {
    "pm": {
      "session_id": "a1b2c3d4-e5f6-4789-a0b1-c2d3e4f5g6h7",
      "timestamp": "2026-03-16T23:01:00Z",
      "status": "completed",
      "command": "claude --resume a1b2c3d4-e5f6-4789-a0b1-c2d3e4f5g6h7"
    },
    "coding": {
      "session_id": "b2c3d4e5-f6g7-4890-b1c2-d3e4f5g6h7i8",
      "timestamp": "2026-03-16T23:03:00Z",
      "status": "completed",
      "command": "claude --resume b2c3d4e5-f6g7-4890-b1c2-d3e4f5g6h7i8"
    },
    "qa": {
      "session_id": "c3d4e5f6-g7h8-4901-c2d3-e4f5g6h7i8j9",
      "timestamp": "2026-03-16T23:08:00Z",
      "status": "completed",
      "command": "claude --resume c3d4e5f6-g7h8-4901-c2d3-e4f5g6h7i8j9"
    }
  }
}
```

---

## 세션 목록 보기

### 모든 세션 확인

```bash
bash scripts/resume-session.sh --list
```

출력 예시:
```
📋 저장된 에이전트 세션 목록
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLAN-001
  pm: a1b2c3d4-e5f6-4789-a0b1-c2d3e4f5g6h7
    재개: claude --resume a1b2c3d4-e5f6-4789-a0b1-c2d3e4f5g6h7
    시간: 2026-03-16T23:01:00Z

  coding: b2c3d4e5-f6g7-4890-b1c2-d3e4f5g6h7i8
    재개: claude --resume b2c3d4e5-f6g7-4890-b1c2-d3e4f5g6h7i8
    시간: 2026-03-16T23:03:00Z

  qa: c3d4e5f6-g7h8-4901-c2d3-e4f5g6h7i8j9
    재개: claude --resume c3d4e5f6-g7h8-4901-c2d3-e4f5g6h7i8j9
    시간: 2026-03-16T23:08:00Z

PLAN-002
  ...
```

---

## 세션 재개

### 방법 1: resume-session.sh 사용 (권장)

```bash
# 기본 사용법
bash scripts/resume-session.sh <티켓번호> <에이전트명>

# 예시
bash scripts/resume-session.sh PLAN-001 coding
```

**장점:**
- 자동으로 CLAUDE.md 로드
- 프로젝트 디렉토리로 자동 이동
- 세션 찾기 자동화

### 방법 2: Claude CLI 직접 사용

```bash
# session-map.json에서 세션 ID 확인
cat projects/my-todo-app/.sessions/session-map.json

# 수동으로 재개
cd projects/my-todo-app
claude --resume a1b2c3d4-e5f6-4789-a0b1-c2d3e4f5g6h7
```

---

## 사용 시나리오

### 시나리오 1: 코드 리팩토링 요청

```bash
# 1. auto-pipeline으로 전체 개발 완료
bash scripts/auto-pipeline.sh --project "..." --auto-push

# 2. 코드 리뷰 중 PLAN-001 코드가 마음에 안 듦
# 3. Coding Agent 세션 재개
bash scripts/resume-session.sh PLAN-001 coding

# 4. 대화 시작
```

Claude Code 세션:
```
> src/auth/login.py 파일의 authenticate 함수를
> 더 명확한 에러 메시지를 반환하도록 리팩토링해줘.
>
> 또한 비밀번호 검증 로직을 별도 함수로 분리해.

✅ 변경 완료
- authenticate() 함수 리팩토링
- validate_password() 함수 분리
- 에러 메시지 개선
```

### 시나리오 2: 테스트 케이스 추가

```bash
# QA Agent 세션 재개
bash scripts/resume-session.sh PLAN-001 qa
```

Claude Code 세션:
```
> tests/test_auth.py에 다음 테스트 케이스 추가해줘:
> - 비밀번호에 특수문자가 없을 때 실패하는 케이스
> - 이메일 형식이 잘못되었을 때 실패하는 케이스
> - 동일한 이메일로 중복 가입 시도하는 케이스

✅ 테스트 케이스 추가 완료
```

### 시나리오 3: 명세서 수정

```bash
# PM Agent 세션 재개
bash scripts/resume-session.sh PLAN-001 pm
```

Claude Code 세션:
```
> planning/specs/backend/PLAN-001-user-auth.md 명세서에
> OAuth 2.0 로그인 엔드포인트 추가해줘.

✅ 명세서 업데이트 완료
```

### 시나리오 4: Fork 모드 (실험적 수정)

원본 세션을 유지하면서 새로운 방향 시도:

```bash
# 새 세션으로 포크
bash scripts/resume-session.sh PLAN-001 coding --fork
```

Claude Code 세션:
```
> 원본 코드를 보존하면서,
> JWT 대신 Session 기반 인증으로 완전히 다시 구현해줘.
> src/auth/session_login.py로 새 파일 생성.

✅ 대안 구현 완료 (원본 유지)
```

---

## 고급 사용법

### 여러 세션 순차 재개

```bash
# 1. 명세서 수정
bash scripts/resume-session.sh PLAN-001 pm
# → OAuth 엔드포인트 추가

# 2. 코드 재구현
bash scripts/resume-session.sh PLAN-001 coding
# → 수정된 명세서 기반으로 OAuth 구현

# 3. 테스트 추가
bash scripts/resume-session.sh PLAN-001 qa
# → OAuth 테스트 케이스 작성
```

### 직접 Claude CLI 사용

세션 ID를 알고 있다면:

```bash
cd projects/my-todo-app

# 재개
claude --resume b2c3d4e5-f6g7-4890-b1c2-d3e4f5g6h7i8

# 포크
claude --resume b2c3d4e5-f6g7-4890-b1c2-d3e4f5g6h7i8 --fork-session
```

---

## 주의사항

### 1. 세션 유효 기간

Claude Code 세션은 일정 기간 후 만료될 수 있습니다.
- 만료된 세션은 재개 불가
- `.sessions/` 디렉토리는 Git에 커밋하지 않음 (`.gitignore` 권장)

### 2. 컨텍스트 윈도우

재개된 세션도 컨텍스트 윈도우 제한이 있습니다.
- 장시간 대화 후 재개 시 초기 컨텍스트가 손실될 수 있음
- 필요 시 `--fork-session`으로 새로 시작

### 3. 파일 변경사항

세션 재개 시:
- 이전 세션의 모든 대화 기록 유지
- 파일 변경사항은 현재 작업 디렉토리 기준
- Git 상태 확인 권장

---

## .gitignore 설정

```gitignore
# 프로젝트 .gitignore에 추가
.sessions/
```

세션 ID는 로컬에서만 유지하고, 원격에는 푸시하지 않습니다.

---

## 트러블슈팅

### 세션을 찾을 수 없습니다

```bash
# 세션 목록 확인
bash scripts/resume-session.sh --list

# session-map.json 직접 확인
cat projects/my-todo-app/.sessions/session-map.json | jq .
```

### 세션 재개가 실패합니다

```bash
# Claude CLI로 직접 시도
claude --resume <session-id>

# 에러 메시지 확인 후:
# - 세션 만료: 새로 실행
# - 세션 ID 오류: --list로 확인
```

### 잘못된 세션 삭제

```bash
# 특정 티켓 세션 삭제
rm -rf projects/my-todo-app/.sessions/PLAN-001

# session-map.json 수정
# (수동으로 jq 사용 또는 텍스트 에디터)
```

---

## 요약

| 명령 | 설명 |
|------|------|
| `bash scripts/resume-session.sh --list` | 모든 세션 목록 보기 |
| `bash scripts/resume-session.sh PLAN-001 coding` | 세션 재개 (이어서 작업) |
| `bash scripts/resume-session.sh PLAN-001 coding --fork` | 세션 포크 (새 세션으로 실험) |
| `claude --resume <session-id>` | Claude CLI로 직접 재개 |

---

**💡 Tip**: auto-pipeline 완료 후 PR 리뷰 과정에서 수정사항이 생기면, 해당 에이전트 세션을 재개하여 빠르게 수정할 수 있습니다!
