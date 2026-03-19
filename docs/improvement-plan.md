2.3# Multi-Agent Coding Team 개선 계획
## Thariq의 Skills 가이드 기반

> **작성일**: 2026-03-19
> **참고**: [Lessons from Building Claude Code - How We Use Skills](https://x.com/trq212/status/2033949937936085378)

---

## 📊 현재 상태 진단

### ✅ 강점
- **5개 통합 에이전트**: stack-initializer, project-planner, pm, coding, qa
- **Tech-stack 독립성**: 프로젝트 타입별 동적 디렉토리 구조
- **자동 파이프라인**: 무인 실행 가능한 Python 오케스트레이션
- **세션 관리**: Claude CLI 세션 재개로 반복 수정 가능
- **Rate Limit 추적**: API 사용량 사전 모니터링
- **Git 자동화**: 브랜치 생성, 커밋 템플릿

### ❌ 주요 문제점

#### 1. **워크플로우 정확성 부족**
- **증상**: 에이전트가 티켓 범위를 벗어나 불필요한 기능 추가
- **영향**: API 호출 낭비, 코드 리뷰 부담 증가
- **예시**: "로그인" 티켓에 OAuth, 비밀번호 재설정까지 구현

#### 2. **Self-learning 메커니즘 부재**
- **현재**: 로그는 작성하지만 재사용 안 됨 (`projects/{name}/logs/`)
- **문제**: 같은 실수를 반복함 (프로젝트 경로 오류, 범위 확대 등)
- **Thariq 교훈**: "storing data within them... the next time you run it, Claude reads its own history"

#### 3. **컨텍스트 효율성 저하**
- **현재**: PM Agent CLAUDE.md = 833줄, Coding = 428줄
- **문제**: 매번 전체 로드 → 토큰 낭비
- **Thariq 교훈**: "Progressive Disclosure - tell Claude what files are in your skill"

#### 4. **Gotchas 섹션 부재**
- **현재**: 47개의 "금지 사항" 산재 (부정형 규칙)
- **문제**: "왜 실패하는지" 패턴 미기록
- **Thariq 교훈**: "The highest-signal content in any skill is the Gotchas section"

#### 5. **검증 후크 없음**
- **현재**: Auto-pipeline이 품질 게이트 없이 실행
- **문제**: 잘못된 명세 → 잘못된 코드 → API 호출 낭비
- **Thariq 교훈**: "blocks rm -rf, DROP TABLE, force-push via PreToolUse matcher"

---

## 🎯 개선 로드맵

### **Phase 1: Quick Wins (1-2일)**
> 즉각적인 정확성 개선, 아키텍처 변경 없음

#### 1.1 금지사항 → Gotchas 파일 전환
**난이도**: 🟢 Low
**영향**: 🔴 High - 범위 이탈 40% 감소

**생성할 파일**:
```
team/.agents/pm/gotchas.md
team/.agents/coding/gotchas.md
team/.agents/qa/gotchas.md
team/.agents/project-planner/gotchas.md
```

**구조** (Thariq 패턴):
```markdown
# PM Agent Gotchas

## 1. 범위 확대 패턴 (Scope Creep)
❌ **증상**: 티켓에 없는 기능 추가
🔍 **원인**: "user auth" → OAuth, 이메일 인증까지 해석
✅ **해결**: 티켓 Acceptance Criteria 먼저 확인
📝 **실패 사례**: PLAN-001이 로그인/로그아웃만 요청 → PM이 비밀번호 재설정까지 추가
🎯 **올바른 접근**: 티켓 항목만 구현, 추가는 "Out of Scope"에 기록

## 2. 잘못된 디렉토리 생성
❌ **증상**: team/.agents/ 에 명세서 생성
🔍 **원인**: .project-config.json 체크 생략
🚨 **탐지**: 경로에 "team/.agents" 또는 "team/.rules" 포함
✅ **해결**: mkdir 전에 항상 .project-config.json → current_project 읽기

## 3. HTML 와이어프레임에 외부 라이브러리
❌ **증상**: Tailwind, React 사용
🔍 **원인**: 프로덕션 코드 작성으로 착각
✅ **해결**: 바닐라 JS만, 구조만 표현
📝 **검증**: grep -E "tailwind|react|vue" 으로 체크
```

**작업 순서**:
1. 모든 CLAUDE.md의 "금지 사항" 추출
2. 각 금지사항을 Gotcha로 변환 (실패 패턴 + 근본 원인 + 탐지법 + 해결책)
3. 각 CLAUDE.md를 ~200줄 축소

**기대 효과**:
- 에이전트당 토큰 사용량: **-15%**
- 범위 이탈 에러: **-40%**
- 엣지 케이스 처리 명확성: **+60%**

---

#### 1.2 Progressive Disclosure 리팩토링
**난이도**: 🟡 Medium
**영향**: 🔴 High - 컨텍스트 사용량 30% 감소

**새 구조**:
```
team/.agents/pm/
├── CLAUDE.md (100줄 - 핵심 역할 + 파일 인벤토리)
├── gotchas.md (1.1에서 생성)
├── workflows/
│   ├── web-fullstack.md
│   ├── cli-tool.md
│   └── desktop-app.md
└── templates/ (기존)
```

**새 CLAUDE.md 구조** (~100줄):
```markdown
# PM Agent

티켓을 구조화된 명세서로 변환하는 에이전트.

## 📂 파일 구조
- `gotchas.md` - **먼저 읽기**. 일반적인 실패 패턴과 회피법
- `workflows/{project_type}.md` - .project-meta.json의 project_type 기반으로 읽기
- `templates/{project_type}.md` - 명세서 생성 템플릿

## 🔨 핵심 프로세스
1. gotchas.md 읽기
2. Rate limit 체크: `bash scripts/rate-limit-check.sh pm`
3. .project-config.json 읽기 → current_project
4. .project-meta.json 읽기 → project_type
5. workflows/{project_type}.md에서 프로젝트별 단계 로드
6. templates/{project_type}.md로 명세서 생성

## 📤 산출물
- API 명세, UI 명세, 테스트 케이스: `projects/{project}/planning/specs/`
- 로그: `projects/{project}/logs/pm/`

상세 지침은 workflows/ 참조.
```

**생성할 파일**:
- `team/.agents/pm/workflows/web-fullstack.md` (현재 CLAUDE.md에서 추출)
- `team/.agents/pm/workflows/cli-tool.md`
- `team/.agents/coding/workflows/web-fullstack.md`
- `team/.agents/qa/workflows/web-fullstack.md`

**기대 효과**:
- 초기 컨텍스트 로드: **-30%**
- 필요한 워크플로우만 온디맨드 읽기
- 새 프로젝트 타입 추가 용이 (워크플로우 파일만 추가)

---

#### 1.3 Auto-Response 규칙을 데이터화
**난이도**: 🟢 Low
**영향**: 🟡 Medium - 튜닝 용이, 코드 변경 불필요

**생성할 파일**: `team/.config/auto-responses.json`

```json
{
  "pm": {
    "patterns": [
      {
        "trigger": "추가.*기능.*할까요",
        "response": "no, 티켓 범위 내에서만 진행해주세요",
        "reason": "scope_creep_prevention"
      },
      {
        "trigger": "변경.*할까요",
        "response": "no, 현재 명세대로 진행해주세요",
        "reason": "spec_compliance"
      },
      {
        "trigger": "이 부분.*애매",
        "response": "티켓의 Acceptance Criteria를 기반으로 합리적으로 판단하고 로그에 기록해주세요",
        "reason": "ambiguity_handling"
      }
    ]
  },
  "coding": {
    "patterns": [
      {
        "trigger": "더 나은 패턴",
        "response": "코딩 룰에 명시된 패턴을 우선 사용하세요. 대안이 명백히 우수하면 로그에 근거를 작성하세요",
        "reason": "architecture_consistency"
      }
    ]
  }
}
```

**수정할 파일**:
- `team/scripts/auto_pipeline.py` (24-29줄, 140-145줄)

**기대 효과**:
- 코드 배포 없이 응답 튜닝
- 로그에서 패턴 학습 가능 (Phase 2)
- 응답 전략 버전 관리

---

### **Phase 2: 핵심 개선 (1주)**
> Self-learning 메커니즘 및 검증 후크

#### 2.1 구조화된 의사결정 로그
**난이도**: 🟡 Medium
**영향**: 🔴 High - 실수에서 학습 가능

**현재 문제**: 로그는 작성되지만 분석 안 됨

**새 로그 구조**:
```markdown
# PM Log: User Authentication

## 메타데이터
- Agent: PM
- Ticket: PLAN-001
- Timestamp: 2026-03-19T10:30:00Z
- Decision Count: 3

## 의사결정

### Decision 1: OAuth 제외
- **컨텍스트**: 티켓에 "login" 명시, 방법 미지정
- **옵션**: [Email/Password만, OAuth, 둘 다]
- **선택**: Email/Password만
- **이유**: Acceptance Criteria에 email/password만 명시
- **위험도**: Low (티켓에 명확함)
- **신뢰도**: 95%

### Decision 2: 비밀번호 재설정 엔드포인트 포함 여부
- **컨텍스트**: 티켓에 없지만 일반적인 패턴
- **옵션**: [포함, 제외, 사용자에게 질문]
- **선택**: 제외
- **이유**: Gotcha #1 적용 (범위 확대 방지)
- **위험도**: Medium (사용자가 기대할 수 있음)
- **신뢰도**: 70%

## 적용한 Gotchas
- ✅ Gotcha #1: 범위 확대 - 티켓 확인, 비밀번호 재설정 제외
- ✅ Gotcha #5: 잘못된 디렉토리 - .project-config.json 먼저 읽기

## 관찰된 패턴
- 사용자가 "auth"라고 하면 → 로그인/로그아웃만 의미할 가능성 높음
- "forgot password" 언급 없음 → 비밀번호 재설정 제외
```

**생성할 파일**:
```
team/.config/log-schema.json (필수 의사결정 필드 정의)
team/scripts/analyze-logs.py (로그에서 패턴 추출)
```

**통합**:
- 모든 에이전트 CLAUDE.md를 구조화된 로그 형식으로 업데이트
- 주간으로 `analyze-logs.py` 실행:
  - 가장 흔한 의사결정 패턴 식별
  - 실패한 고위험 결정 발견
  - 새 Gotcha 후보 발견

**기대 효과**:
- 회고적 학습: **+80%**
- 새 Gotcha 발견률: 초기에 주당 **2-3개**
- 의사결정 품질 추적 (신뢰도 vs 실제 결과)

---

#### 2.2 검증 후크 (Skill 기반)
**난이도**: 🟡 Medium
**영향**: 🔴 High - 비용 높은 코딩 단계 전에 에러 포착

**생성할 Skills**:
```
team/.skills/
├── validate-spec/
│   ├── skill.md
│   ├── rules.json
│   └── examples/
└── validate-code/
    ├── skill.md
    └── rules.json
```

**`validate-spec/skill.md`**:
```markdown
# Spec Validation Skill

PM Agent 결과를 Coding Agent로 전달하기 전에 검증.

## 트리거
- Auto-pipeline: PM agent 완료 후
- 수동: `bash scripts/run-skill.sh validate-spec PLAN-001`

## 검사 항목

### 1. 완전성
- [ ] API 명세에 티켓의 모든 CRUD 엔드포인트 포함
- [ ] UI 명세에 Acceptance Criteria의 모든 유저 플로우 포함
- [ ] 모든 엣지 케이스에 대한 테스트 케이스 존재
- [ ] 와이어프레임 HTML 존재 (프로젝트 타입이 필요로 하는 경우)

### 2. 범위 준수
- [ ] 티켓 Acceptance Criteria 외 기능 없음
- [ ] Out-of-Scope 섹션에 제외 항목 나열
- [ ] .project-meta.json의 tech stack 변경 없음

### 3. 품질 게이트
- [ ] API 엔드포인트가 REST 규약 준수
- [ ] 예시에 하드코딩된 비밀번호 없음
- [ ] 에러 응답 문서화됨
- [ ] 입력 검증 규칙 명시됨

## 출력
- Pass/Fail 상태
- 발견된 이슈 목록
- 사소한 이슈에 대한 자동 수정 제안
```

**`validate-spec/rules.json`**:
```json
{
  "rules": [
    {
      "id": "no-scope-creep",
      "check": "명세 기능을 티켓 Acceptance Criteria와 비교",
      "severity": "error",
      "auto_fix": false
    },
    {
      "id": "rest-conventions",
      "check": "POST=생성, GET=읽기, PUT=수정, DELETE=삭제",
      "severity": "warning",
      "auto_fix": false
    },
    {
      "id": "no-hardcoded-secrets",
      "check": "명세에서 API_KEY, PASSWORD, SECRET 패턴 검색",
      "severity": "error",
      "auto_fix": true,
      "fix": "환경 변수 참조로 대체"
    }
  ]
}
```

**Auto-Pipeline 통합**:
```python
# auto_pipeline.py의 PM agent 후
result = self.run_agent("pm", ticket_content, ticket_num)

# 검증 skill 실행
validation = self.run_skill("validate-spec", ticket_num)
if not validation["passed"]:
    print(f"⚠️  명세 검증 실패: {validation['issues']}")
    # 이슈를 컨텍스트로 PM agent 재시도
    self.run_agent("pm", f"다음 이슈 수정: {validation['issues']}", ticket_num)
```

**기대 효과**:
- 명세 품질 에러 포착: **+90%**
- 낭비된 코딩 반복: **-60%**
- 티켓당 절약된 API 호출: **~3-5회** (재작업 없음)

---

#### 2.3 메모리 시스템 (학습된 패턴)
**난이도**: 🟡 Medium
**영향**: 🔴 High - 과거 실수에서 학습

**파일 구조**:
```
team/.memory/
├── patterns.json (학습된 의사결정 패턴)
├── failures.json (카탈로그화된 실패)
└── successes.json (검증된 모범 사례)
```

**`patterns.json`**:
```json
{
  "pm": {
    "pattern_001": {
      "trigger": "티켓에 'auth' 언급, OAuth 없음",
      "learned_decision": "OAuth 제외, Out-of-Scope에 기록",
      "confidence": 0.95,
      "learned_from": ["PLAN-001", "PLAN-023", "PLAN-047"],
      "success_rate": "47/50",
      "last_updated": "2026-03-15"
    },
    "pattern_002": {
      "trigger": "폼 제출 UI 명세",
      "learned_decision": "항상 로딩 상태와 에러 표시 포함",
      "confidence": 0.88,
      "learned_from": ["PLAN-005", "PLAN-012"],
      "success_rate": "28/32"
    }
  }
}
```

**`failures.json`**:
```json
{
  "failure_001": {
    "ticket": "PLAN-007",
    "agent": "coding",
    "symptom": "잘못된 디렉토리에 코드 생성",
    "root_cause": ".project-config.json 체크 생략",
    "detection": "수동 리뷰",
    "fix_applied": "gotchas.md #3에 추가",
    "prevented_count": 12
  }
}
```

**학습 스크립트**: `team/scripts/learn-from-logs.py`

**기능**:
1. 최근 7일 로그 파싱
2. 의사결정 + 결과 추출 (git commit, 테스트 결과에서)
3. >80% 성공률 패턴 → `patterns.json`에 추가
4. 반복 실패 식별 → `failures.json` → 새 Gotcha 생성
5. 성공 패턴 기반으로 auto-responses.json 업데이트

**통합**:
```markdown
## 메모리 파일
- `.memory/patterns.json` - 학습된 모범 사례 적용
- `.memory/failures.json` - 알려진 실패 모드 회피
```

**기대 효과**:
- 반복 실수: **-70%**
- 의사결정 품질 (정확도): **+25%**
- 새 프로젝트 타입 숙련 시간: **-50%**

---

#### 2.4 Gotcha 자동 발견
**난이도**: 🟡 Medium
**영향**: 🟡 Medium - Gotcha 지속 개선

**스크립트**: `team/scripts/discover-gotchas.py`

**알고리즘**:
1. 모든 실패 로그 파싱 (git revert, 실패한 테스트, 수동 수정)
2. 공통 패턴 추출:
   - 에러 메시지
   - 관련 파일 경로
   - 실패 전 에이전트 의사결정
3. 유사 실패 클러스터링
4. Gotcha 초안 생성:
   ```markdown
   ## [초안] 잘못된 테스트 파일 위치
   **증상**: src/에 테스트 생성, tests/가 아닌
   **빈도**: 3회 (PLAN-012, PLAN-019, PLAN-024)
   **원인**: QA agent가 프로젝트 구조 오독
   **해결**: 테스트 디렉토리 규약은 항상 .project-meta.json 확인
   ```
5. `gotchas.md`에 추가 전 사람 검토

**트리거**:
- cron으로 주간 실행
- git revert 후 실행
- 온디맨드: `bash scripts/discover-gotchas.py --since 7d`

**기대 효과**:
- 새 Gotcha 발견: 주당 **1-2개**
- 엣지 케이스 커버리지: 3개월 내 **+40%**
- Gotcha 수동 작성 감소

---

### **Phase 3: 고급 기능 (2주+)**
> 하이브리드 agent-skill 아키텍처, 고급 학습

#### 3.1 Skill 기반 아키텍처 (점진적 마이그레이션)
**난이도**: 🔴 High
**영향**: 🔴 High - Anthropic의 최신 Skills 패턴

**전략**: 하이브리드 - 에이전트 유지, Skills 점진 추가

**새 구조**:
```
team/
├── .agents/ (기존 - 당분간 유지)
├── .skills/ (신규)
│   ├── commit/
│   │   ├── skill.md
│   │   ├── commit-message-generator.py
│   │   └── gotchas.md
│   ├── review-pr/
│   │   ├── skill.md
│   │   ├── review-checklist.json
│   │   └── auto-fix-rules.json
│   ├── validate-spec/ (Phase 2.2에서)
│   └── refactor-code/
│       ├── skill.md
│       └── patterns.json
```

**마이그레이션 경로**:
1. **1주차**: 작고 독립적인 작업을 Skills로 전환
   - `commit` skill (하드코딩 커밋 템플릿 대체)
   - `validate-spec` skill (Phase 2.2에서)
2. **2주차**: 누락된 부분을 위한 새 Skills 추가
   - `review-pr` skill (자동 PR 리뷰)
   - `refactor-code` skill (코드 개선 제안)
3. **3주차**: 에이전트가 Skills 사용하도록 리팩토링
   - PM agent가 생성 후 `validate-spec` skill 호출
   - Coding agent가 커밋 전 `refactor-code` skill 호출
4. **2-3개월**: 에이전트 기능을 Skills로 점진 마이그레이션

**예시 Skill**: `commit/skill.md`
```markdown
# Commit Skill

프로젝트 규약에 따라 시맨틱 커밋 생성.

## 트리거
- 수동: 코드 생성 후 사용자가 "commit" 입력
- Auto-pipeline: coding/qa agents 완료 후

## 프로세스
1. git diff 읽기
2. 변경 파일 분석
3. 커밋 메시지 생성:
   - Prefix: feat/fix/test/docs/refactor
   - Scope: (ticket-number)
   - Subject: 명령형, <70자
   - Body: 변경 이유
   - Footer: Co-Authored-By, Closes #
4. 승인을 위해 메시지 표시
5. 커밋 실행

## 메모리
- `.memory/commit-history.json` - 일관성을 위한 과거 커밋 메시지
- 프로젝트별 어휘 학습

## 예시
```
feat(PLAN-001): implement JWT authentication

Added login/logout endpoints with token generation.
Password hashing uses bcrypt with salt rounds=12.

Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Gotchas
- Subject에 파일 경로 포함 금지 (Body 사용)
- 테스트 실패 시 커밋 금지 (검증 먼저 실행)
```

**기대 효과**:
- 커밋 메시지 품질: **+60%**
- 프로젝트 간 재사용
- 새 워크플로우 추가 용이 (Skill만 추가)

---

#### 3.2 피드백 루프 통합
**난이도**: 🔴 High
**영향**: 🔴 High - 학습 루프 완성

**시스템**:
```
team/.feedback/
├── outcomes.json (티켓 → 결과 매핑)
└── metrics.json (에이전트 성능 메트릭)
```

**`outcomes.json`**:
```json
{
  "PLAN-001": {
    "agents": ["pm", "coding", "qa"],
    "completed": "2026-03-10T15:00:00Z",
    "pr_merged": "2026-03-11T10:00:00Z",
    "review_comments": 3,
    "revisions": 1,
    "test_pass_rate": 0.95,
    "outcome": "success",
    "learnings": [
      {
        "agent": "pm",
        "issue": "에러 응답 문서 누락",
        "pattern": "항상 4xx/5xx 응답 문서화",
        "added_to": "patterns.json#pm_pattern_003"
      }
    ]
  }
}
```

**피드백 수집**:
1. **PR 머지 후**: `bash scripts/record-outcome.sh PLAN-001 success`
2. **PR 코멘트 후**: GitHub API 파싱, 이슈 추출
3. **테스트 실패 후**: 어떤 테스트 케이스가 왜 실패했는지 기록

**피드백 적용**:
1. 검증된 의사결정으로 `patterns.json` 업데이트
2. 반복 이슈에 대한 새 Gotcha 추가
3. auto-response 신뢰도 점수 조정
4. 검증 규칙 튜닝

**대시보드** (선택):
```
team/scripts/dashboard.py
```

표시 항목:
- 에이전트별 성공률 (최근 30 티켓)
- 가장 흔한 실패 유형
- Gotcha 효과성 (방지된 실패 수)
- 패턴 신뢰도 추세

**기대 효과**:
- 에이전트 정확도: 월 **+15%**
- 자기 개선 시스템
- 데이터 기반 Gotcha 우선순위

---

#### 3.3 On-Demand Hooks (안전 가드)
**난이도**: 🟡 Medium
**영향**: 🟡 Medium - 치명적 실수 방지

**Thariq 영감**: "blocks rm -rf, DROP TABLE, force-push via PreToolUse matcher"

**구현**:
```
team/.hooks/
├── pre-tool-use.json
└── validators/
    ├── dangerous-commands.py
    ├── scope-validator.py
    └── file-safety.py
```

**`pre-tool-use.json`**:
```json
{
  "hooks": [
    {
      "name": "block-dangerous-commands",
      "trigger": "Bash tool with rm -rf, DROP, git push --force",
      "action": "block",
      "message": "위험한 명령 차단. 안전한 대안 사용."
    },
    {
      "name": "validate-file-paths",
      "trigger": "Write/Edit tool with path outside projects/{current_project}",
      "action": "warn",
      "message": "경고: 현재 프로젝트 디렉토리 외부에 파일 생성."
    },
    {
      "name": "prevent-spec-bloat",
      "trigger": "PM agent creates >5 spec files for single ticket",
      "action": "warn",
      "message": "범위 확대 가능성 - 티켓당 명세 2-3개 권장."
    }
  ]
}
```

**기대 효과**:
- 치명적 에러: **-100%** (main으로 force push, 데이터 삭제)
- 프로젝트 외부 파일 생성: **-90%**
- 정당한 작업 제한 없이 안전성 확보

---

## 🔄 하위 호환성 전략

**원칙**: 모든 개선은 추가형, 파괴적 변경 없음

### Phase 1
✅ 에이전트는 전체 CLAUDE.md로 여전히 작동
✅ 새 `gotchas.md`와 `workflows/`는 선택적 개선
✅ auto-responses.json 없으면 하드코딩으로 폴백

### Phase 2
✅ 검증 skills는 선택 (auto-pipeline은 없이도 작동)
✅ 메모리 파일은 읽기 전용 추가 (에이전트는 없이도 작동)
✅ 로그는 하위 호환

### Phase 3
✅ Skills는 에이전트 보완 (초기에는 대체 안 함)
✅ Hooks는 프로젝트별 선택
✅ 피드백 시스템은 수동 (워크플로우 차단 안 함)

**프로젝트별 마이그레이션**:
```bash
# 기존 프로젝트는 계속 작동
cd projects/old-project
bash ../../scripts/run-agent.sh pm --ticket PLAN-001

# 새 프로젝트는 개선 사항 적용
cd projects/new-project
# 자동으로 gotchas, memory, validation 로드
bash ../../scripts/run-agent.sh pm --ticket PLAN-001
```

---

## 📈 성공 메트릭

### Phase 1 (1-2주차)
- [ ] 각 에이전트 CLAUDE.md를 <150줄로 축소
- [ ] 에이전트당 10+ Gotchas 문서화
- [ ] 호출당 컨텍스트 사용량: **-30%**
- [ ] 범위 이탈 사고: **-40%**

### Phase 2 (3-5주차)
- [ ] 티켓 100%에 구조화된 로그
- [ ] `patterns.json`에 20+ 패턴 학습
- [ ] 검증이 코딩 전 명세 에러 80%+ 포착
- [ ] 5+ 새 Gotcha 자동 발견

### Phase 3 (6주차+)
- [ ] 3+ Skills 운영
- [ ] 피드백 루프가 50+ 티켓 결과 추적
- [ ] 에이전트 정확도 월별 10% 개선
- [ ] 치명적 에러 제로 (force push, 잘못된 디렉토리)

---

## 🎯 구현 우선순위

### Must-Have (먼저 실행)
1. **Gotchas 파일** (Phase 1.1) - 최고 ROI, 가장 쉬움
2. **Progressive Disclosure** (Phase 1.2) - 큰 컨텍스트 절약
3. **검증 후크** (Phase 2.2) - 비용 높은 실수 방지

### Should-Have (다음 실행)
4. **의사결정 로그** (Phase 2.1) - 학습 가능화
5. **메모리 시스템** (Phase 2.3) - 자기 개선
6. **Auto-responses 데이터화** (Phase 1.3) - 유연성

### Nice-to-Have (나중 실행)
7. **Skills 마이그레이션** (Phase 3.1) - 장기 아키텍처
8. **피드백 루프** (Phase 3.2) - 티켓 볼륨 필요
9. **안전 Hooks** (Phase 3.3) - 완성도

---

## 🔑 핵심 구현 파일

### 즉시 생성/수정 필요
- **team/.agents/pm/gotchas.md** - 현재 CLAUDE.md 769-781줄에서 추출, 금지사항을 근본 원인과 탐지법이 있는 실패 패턴으로 전환

- **team/.agents/pm/CLAUDE.md** - ~150줄로 축소, gotchas.md와 workflows/{project_type}.md를 가리키는 progressive disclosure 구조 추가

- **team/.config/auto-responses.json** - team/scripts/auto_pipeline.py 24-29줄의 하드코딩 패턴을 regex 지원 JSON으로 이동

- **team/scripts/auto_pipeline.py** - _check_auto_response() 메서드 (140-145줄) 수정하여 JSON에서 로드, PM agent 완료 후 검증 skill 통합 추가

- **team/.skills/validate-spec/skill.md** - 완전성, 범위 준수, 품질 게이트에 대한 명세 검증 체크 및 자동 수정 제안 생성

---

## 💡 다음 단계

1. **Phase 1.1부터 시작** (1-2일)
   - PM Agent의 gotchas.md 생성
   - 즉각적인 효과 확인

2. **결과 측정**
   - 범위 이탈 사고 추적
   - 토큰 사용량 비교

3. **점진적 확장**
   - 작동하면 다른 에이전트로 확대
   - Phase 1.2, 1.3 진행

4. **피드백 수집**
   - 어떤 Gotchas가 가장 유용한지
   - 어떤 패턴이 가장 자주 나타나는지

**시작하시겠습니까?** Phase 1.1 (Gotchas 파일)부터 구현해드릴까요?
