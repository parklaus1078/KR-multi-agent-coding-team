# Auto Pipeline v2 사용 가이드

> Claude Code 대화형 세션 기반 자동 파이프라인

---

## 🎯 개요

### 기존 문제 (v1)

```python
# auto_pipeline.py (v1) - 동작하지 않음
subprocess.run(["claude"], stdin=prompt_file)
# ❌ 문제: Claude Code는 대화형 CLI → subprocess로는 한 턴만 실행
# ❌ 문제: 여러 턴 대화 불가능
# ❌ 문제: 세션 유지 불가
```

### 새로운 접근 (v2)

**Auto Pipeline v2**는 Claude Code의 대화형 특성을 활용:

1. ✅ **각 에이전트 = 별도 Terminal 탭**
2. ✅ **세션 유지** (종료하지 않음)
3. ✅ **사용자가 대화하며 작업 진행**
4. ✅ **세션 ID 기록** → 나중에 복귀 가능

---

## 🚀 Quick Start

### 1. 전체 파이프라인 실행

```bash
cd team

# 티켓 번호로 파이프라인 실행
python scripts/auto_pipeline_v2.py --ticket BILL-001
```

**실행 흐름:**

```
1. PM Agent 탭 열림 (자동)
   ↓
   사용자: Terminal 탭으로 이동 → Claude와 대화 → 명세서 생성 완료
   ↓
   원래 창으로 돌아와 Enter 입력
   ↓
2. Coding Agent 탭 열림 (자동)
   ↓
   사용자: Terminal 탭으로 이동 → Claude와 대화 → 코드 구현 완료
   ↓
   원래 창으로 돌아와 Enter 입력
   ↓
3. QA Agent 탭 열림 (자동)
   ↓
   사용자: Terminal 탭으로 이동 → Claude와 대화 → 테스트 작성 완료
   ↓
   원래 창으로 돌아와 Enter 입력
   ↓
✅ 전체 파이프라인 완료!
```

### 2. 기존 세션 복귀 (수정 작업)

```bash
# PM Agent 세션으로 복귀
python scripts/auto_pipeline_v2.py --ticket BILL-001 --resume pm

# Coding Agent 세션으로 복귀
python scripts/auto_pipeline_v2.py --ticket BILL-001 --resume coding

# QA Agent 세션으로 복귀
python scripts/auto_pipeline_v2.py --ticket BILL-001 --resume qa
```

**복귀 후:**
- Terminal에서 해당 탭 찾기 (탭 타이틀: `PM - BILL-001`)
- Claude Code 세션이 유지되어 있음
- 대화를 이어가며 수정 작업

---

## 📂 세션 관리

### 세션 맵 파일

**위치**: `projects/{project}/.sessions/session-map.json`

**구조:**
```json
{
  "BILL-001": {
    "pm": {
      "session_id": "pm-BILL-001-1711234567",
      "started_at": "2026-03-20T10:00:00",
      "completed_at": "2026-03-20T10:15:00",
      "status": "completed",
      "agent_dir": "/path/to/.agents/pm",
      "prompt_file": "/path/to/.sessions/.prompt-pm-BILL-001-xxx.txt"
    },
    "coding": {
      "session_id": "coding-BILL-001-1711234600",
      "started_at": "2026-03-20T10:20:00",
      "completed_at": "2026-03-20T10:45:00",
      "status": "completed",
      "agent_dir": "/path/to/.agents/coding",
      "prompt_file": "/path/to/.sessions/.prompt-coding-BILL-001-xxx.txt"
    },
    "qa": {
      "session_id": "qa-BILL-001-1711234800",
      "started_at": "2026-03-20T11:00:00",
      "completed_at": "2026-03-20T11:30:00",
      "status": "completed",
      "agent_dir": "/path/to/.agents/qa",
      "prompt_file": "/path/to/.sessions/.prompt-qa-BILL-001-xxx.txt"
    }
  },
  "BILL-002": {
    "pm": {
      ...
    }
  }
}
```

### Terminal 탭 구조

파이프라인 실행 중:

```
Terminal.app
├── 원래 탭 (auto_pipeline_v2.py 실행 중)
├── PM - BILL-001 (Claude Code 세션)
├── Coding - BILL-001 (Claude Code 세션)
└── QA - BILL-001 (Claude Code 세션)
```

**각 탭의 상태:**
- ✅ Claude Code 세션 유지
- ✅ 에이전트 디렉토리 (CLAUDE.md 자동 로드)
- ✅ 이전 세션 컨텍스트 포함된 초기 프롬프트 표시

---

## 🔄 작업 흐름 상세

### Step 1: PM Agent

#### 1-1. 스크립트가 하는 일

```python
# 1. 새 Terminal 탭 열기 (AppleScript)
# 2. 에이전트 디렉토리로 이동
cd .agents/pm

# 3. 초기 프롬프트 표시
cat .sessions/.prompt-pm-BILL-001-xxx.txt

# 4. Claude Code 실행
claude
```

#### 1-2. 사용자가 하는 일

1. **Terminal 탭 'PM - BILL-001'로 이동**
2. **표시된 프롬프트 복사** (이전 세션 컨텍스트 + 현재 작업)
3. **Claude Code에 붙여넣기**
4. **Claude와 대화하며 작업 진행:**
   - API 명세서 생성
   - UI 요구사항 생성
   - 테스트 케이스 생성
5. **작업 완료 후 원래 창으로 돌아와 Enter**

#### 1-3. 세션 유지

- ❌ **탭을 닫지 않음** (나중에 복귀 가능)
- ✅ Claude Code 세션 유지
- ✅ 대화 히스토리 보존

### Step 2: Coding Agent

#### 2-1. 스크립트가 하는 일

```python
# 1. 새 Terminal 탭 열기
# 2. 에이전트 디렉토리로 이동
cd .agents/coding

# 3. 초기 프롬프트 표시 (PM 세션 컨텍스트 포함)
cat .sessions/.prompt-coding-BILL-001-xxx.txt

# 4. Claude Code 실행
claude
```

#### 2-2. 사용자가 하는 일

1. **Terminal 탭 'Coding - BILL-001'로 이동**
2. **프롬프트 복사 & 붙여넣기**
3. **Claude와 대화하며 작업:**
   - PM이 생성한 명세서 확인
   - 코드 구현
   - Git 브랜치 생성 & 커밋
4. **완료 후 원래 창으로 Enter**

#### 2-3. PM 세션 컨텍스트

Coding Agent가 받는 초기 프롬프트:

```markdown
## 이전 에이전트 세션 정보

### PM Agent
- Session ID: pm-BILL-001-1711234567
- Started: 2026-03-20T10:00:00
- Status: completed

작업 내용은 Terminal 탭에서 확인 가능합니다.

---

## 현재 작업

티켓 BILL-001을 구현해주세요.

작업:
1. PM Agent가 생성한 명세서 확인
2. 코드 구현 (src/ 디렉토리)
3. Git 브랜치 생성 및 커밋
```

**중요**: Coding Agent는 PM 탭으로 이동하여 명세서 내용 확인 가능

### Step 3: QA Agent

#### 3-1. 스크립트가 하는 일

```python
# 1. 새 Terminal 탭 열기
cd .agents/qa

# 2. 초기 프롬프트 표시 (PM + Coding 세션 컨텍스트 포함)
cat .sessions/.prompt-qa-BILL-001-xxx.txt

# 3. Claude Code 실행
claude
```

#### 3-2. 사용자가 하는 일

1. **Terminal 탭 'QA - BILL-001'로 이동**
2. **프롬프트 복사 & 붙여넣기**
3. **Claude와 대화하며 작업:**
   - PM의 테스트 케이스 확인
   - Coding의 구현 코드 확인
   - 테스트 코드 작성 및 실행
4. **완료 후 원래 창으로 Enter**

#### 3-3. PM + Coding 세션 컨텍스트

QA Agent가 받는 초기 프롬프트:

```markdown
## 이전 에이전트 세션 정보

### PM Agent
- Session ID: pm-BILL-001-1711234567
- Started: 2026-03-20T10:00:00
- Status: completed

### CODING Agent
- Session ID: coding-BILL-001-1711234600
- Started: 2026-03-20T10:20:00
- Status: completed

작업 내용은 Terminal 탭에서 확인 가능합니다.

---

## 현재 작업

티켓 BILL-001의 테스트를 작성해주세요.

작업:
1. PM Agent의 테스트 케이스 확인
2. Coding Agent가 구현한 코드 확인
3. 테스트 코드 작성 및 실행
```

---

## 🔧 수정 작업 (세션 복귀)

### 시나리오: PM 명세서 수정

```bash
# 1. PM 세션 복귀
python scripts/auto_pipeline_v2.py --ticket BILL-001 --resume pm

# 출력:
# 📍 세션 정보
#   - Agent: PM
#   - Ticket: BILL-001
#   - Session ID: pm-BILL-001-1711234567
#   - Started: 2026-03-20T10:00:00
#   - Status: completed
#
# 💡 Terminal에서 해당 탭을 찾으세요:
#    탭 타이틀: 'PM - BILL-001'
```

**작업:**
1. Terminal.app으로 이동
2. 탭 'PM - BILL-001' 찾기
3. Claude Code 세션이 유지되어 있음
4. 대화 이어가며 명세서 수정:
   ```
   사용자: "API 명세서에 pagination 추가해줘"
   Claude: "알겠습니다. 다음과 같이 수정하겠습니다..."
   ```
5. 수정 완료

### 시나리오: Coding 버그 수정

```bash
# Coding 세션 복귀
python scripts/auto_pipeline_v2.py --ticket BILL-001 --resume coding
```

**작업:**
1. 탭 'Coding - BILL-001'로 이동
2. 대화 이어가기:
   ```
   사용자: "user_service.py에 버그가 있어. 이메일 중복 체크가 안 됨"
   Claude: "확인했습니다. user_service.py를 수정하겠습니다..."
   ```
3. 버그 수정 및 재커밋

---

## 💡 Best Practices

### 1. 세션 관리

**DO:**
- ✅ 각 에이전트 탭을 유지 (닫지 않기)
- ✅ 탭 타이틀로 쉽게 찾기 (`PM - BILL-001`)
- ✅ session-map.json 백업 (중요!)

**DON'T:**
- ❌ 작업 중 탭 닫기 (세션 손실)
- ❌ Terminal.app 강제 종료 (모든 세션 손실)

### 2. 작업 순서

**권장:**
```
1. PM → 완료 → Enter
2. Coding → 완료 → Enter
3. QA → 완료 → Enter
```

**비권장:**
```
1. PM 시작
2. 완료 전에 Coding 시작 (컨텍스트 불완전)
```

### 3. 컨텍스트 공유

**PM → Coding:**
- Coding Agent가 PM 탭의 명세서 파일 읽기
- 또는 PM 탭 대화 내용 참고

**Coding → QA:**
- QA Agent가 Coding 탭의 구현 내용 확인
- Git 커밋 로그 확인

### 4. 세션 백업

```bash
# 세션 맵 백업 (정기적으로)
cp projects/{project}/.sessions/session-map.json \
   projects/{project}/.sessions/session-map.backup.json
```

---

## 🐛 트러블슈팅

### 문제 1: Terminal 탭이 안 열림

**원인**: macOS 보안 설정

**해결:**
```bash
# System Preferences → Security & Privacy → Automation
# Terminal.app에 접근 권한 부여
```

### 문제 2: Claude Code가 설치되지 않음

**해결:**
```bash
# Claude Code 설치
# https://docs.claude.ai/claude-code

# 설치 확인
which claude
```

### 문제 3: 세션을 찾을 수 없음

**원인**: session-map.json 손상 또는 삭제

**해결:**
```bash
# 백업에서 복구
cp projects/{project}/.sessions/session-map.backup.json \
   projects/{project}/.sessions/session-map.json
```

### 문제 4: 탭을 실수로 닫음

**해결:**
1. **세션 ID는 보존됨** (session-map.json)
2. **프롬프트 파일 확인:**
   ```bash
   cat projects/{project}/.sessions/.prompt-pm-BILL-001-xxx.txt
   ```
3. **수동으로 탭 재생성:**
   ```bash
   cd .agents/pm
   claude
   # 프롬프트 파일 내용 붙여넣기
   ```

---

## 🔄 기존 v1과 비교

### Auto Pipeline v1 (auto_pipeline.py)

```python
# subprocess로 실행
result = subprocess.run(
    ["claude"],
    stdin=open(prompt_file),
    cwd=agent_dir
)

# ❌ 문제:
# - 한 턴만 실행 (대화 불가)
# - 세션 유지 불가
# - 사용자 개입 불가
```

### Auto Pipeline v2 (auto_pipeline_v2.py)

```python
# Terminal 탭에서 대화형 실행
applescript = '''
tell application "Terminal"
    do script "cd {agent_dir}" in front window
    do script "claude" in front window
end tell
'''

# ✅ 개선:
# - 대화형 세션 (여러 턴 가능)
# - 세션 유지 (나중에 복귀)
# - 사용자가 Claude와 직접 대화
```

---

## 📊 세션 상태 조회

### 수동 조회

```bash
# 세션 맵 확인
cat projects/{project}/.sessions/session-map.json | jq

# 특정 티켓 세션 확인
cat projects/{project}/.sessions/session-map.json | \
    jq '.["BILL-001"]'
```

### Python 스크립트로 조회 (향후 추가 예정)

```bash
# 모든 세션 조회
python scripts/auto_pipeline_v2.py --list-sessions

# 특정 티켓 조회
python scripts/auto_pipeline_v2.py --ticket BILL-001 --status
```

---

## 🚀 향후 개선 계획

### v2.1 (단기)
- [ ] 세션 상태 조회 명령어 (`--list-sessions`, `--status`)
- [ ] 세션 자동 백업 (매 작업 완료 시)
- [ ] 탭 닫힘 감지 및 경고

### v2.2 (중기)
- [ ] iTerm2 지원
- [ ] 리눅스 지원 (tmux 기반)
- [ ] Windows 지원 (Windows Terminal)

### v2.3 (장기)
- [ ] 웹 대시보드 통합
- [ ] 세션 시각화
- [ ] 자동 복구 (탭 닫힘 시)

---

## 📚 참고 자료

- **Claude Code 문서**: https://docs.claude.ai/claude-code
- **AppleScript 가이드**: https://developer.apple.com/library/archive/documentation/AppleScript/
- **Terminal.app Automation**: https://ss64.com/osx/osascript.html

---

**버전**: v2.0
**최종 업데이트**: 2026-03-20
**플랫폼**: macOS 전용
