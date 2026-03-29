# Multi-Agent Coding Team - Development Agent

> **역할**: Multi-Agent Coding Team 시스템 자체를 개발하고 개선하는 에이전트
>
> **범위**: 시스템 아키텍처, 에이전트 개선, API 개발, 웹 대시보드, 문서화
>
> **버전**: v0.0.3

---

## 🎯 미션

이 시스템은 **Tech Stack Agnostic 멀티 에이전트 개발 플랫폼**입니다.
사용자가 어떤 프로젝트든 자동화된 파이프라인으로 개발할 수 있도록 지원합니다.

---

## 📂 프로젝트 구조 이해

### 핵심 디렉토리

```
KR-multi-agent-coding-team/
├── CLAUDE.md                    # ← 이 파일 (시스템 개발 가이드)
├── README.md                    # 사용자 문서
├── docs/                        # 아키텍처 문서
├── logs-agent_dev/              # 수정사항 로그 문서
└── team/                        # ← 핵심 작업 디렉토리
    ├── .agents/                 # 5개 에이전트 정의
    │   ├── pm/CLAUDE.md
    │   ├── coding/CLAUDE.md
    │   ├── qa/CLAUDE.md
    │   ├── project-planner/CLAUDE.md
    │   └── stack-initializer/CLAUDE.md
    ├── .skills/                 # 8개 재사용 가능 스킬
    │   ├── validate-spec/
    │   ├── commit/
    │   ├── review-pr/
    │   ├── refactor-code/
    │   ├── test-runner/
    │   ├── deploy/
    │   ├── benchmark/
    │   └── docs-generator/
    ├── .config/                 # 시스템 설정
    │   ├── git-workflow.json
    │   ├── auto-responses.json
    │   └── log-schema.json
    ├── .memory/                 # 학습 시스템
    │   ├── patterns.json
    │   ├── commit-history.json
    │   └── review-history.json
    ├── api/                     # FastAPI REST API (Phase 4)
    │   ├── main.py
    │   ├── routers/
    │   ├── services/
    │   └── models/
    ├── web/                     # 웹 대시보드 (Phase 4)
    │   ├── index.html
    │   └── static/
    ├── scripts/                 # CLI 도구
    │   ├── run-agent.sh
    │   ├── run-skill.sh
    │   └── auto_pipeline.py
    └── projects/                # 사용자 프로젝트 작업 공간
        └── {project-name}/
```

---

## 🏗️ 아키텍처 원칙

### 1. Agent vs Skill 분리

**Agent (복잡한 의사결정)**
- PM, Coding, QA, Project Planner, Stack Initializer
- 컨텍스트 이해 필요
- CLAUDE.md로 정의
- 상태 유지 (세션)

**Skill (반복 작업 자동화)**
- validate-spec, commit, review-pr, refactor-code 등
- Stateless (상태 없음)
- 재사용 가능
- skill.md로 정의

### 2. Tech Stack Agnostic

**절대 하드코딩 금지:**
```python
# ❌ 나쁜 예
if language == "python":
    run_pytest()
elif language == "go":
    run_go_test()

# ✅ 좋은 예
framework = meta.get("framework")
test_command = get_test_command(framework)  # 동적 감지
```

**프로젝트 메타데이터 활용:**
```json
{
  "project_type": "web-fullstack",
  "language": "python",
  "framework": "fastapi"
}
```

### 3. 프로젝트 격리

- 시스템 코드: `KR-multi-agent-coding-team/`
- 사용자 프로젝트: `team/projects/{name}/` (독립 Git 리포)
- **절대 섞이면 안 됨**

---

## 🔧 개발 시 필수 확인사항

### 작업 전 체크리스트

1. **현재 버전 확인**
   ```bash
   grep "version" README.md
   # 현재: v0.0.3
   ```

2. **변경 범위 파악**
   - Agent 수정? → `.agents/{agent}/CLAUDE.md`
   - Skill 추가? → `.skills/{skill}/skill.md`
   - API 엔드포인트? → `api/routers/`
   - 웹 UI? → `web/`

3. **테스트 환경**
   ```bash
   cd team
   # API 테스트
   uvicorn api.main:app --reload --port 8000

   # CLI 테스트
   bash scripts/run-agent.sh pm --ticket PLAN-001
   ```

4. **마이그레이션 체크**
   - KR 버전 수정 → ENG 버전도 수정 필요
   - A_coding-team도 동기화 필요한지 확인

---

## 📝 코딩 규칙

**중요**: 상세한 코딩 규칙은 별도 문서 참조

- **전체 코딩 규칙**: `CODING-RULES.md` (이 파일과 같은 위치)
  - Python (FastAPI, Services)
  - Shell Scripts
  - JavaScript (Web Dashboard)
  - DRY, SRP, KISS, YAGNI 등 원칙
  - 선언적 코딩 우선
  - 에러 핸들링 패턴

- **범용 원칙**: `team/.rules/general-coding-rules.md`
- **Backend 상세**: `team/.rules/_verified/web-fullstack/backend-fastapi-python.md`
- **Frontend 상세**: `team/.rules/_verified/web-fullstack/frontend-nextjs-typescript.md`

### 핵심 원칙만 요약

1. **DRY**: 중복 코드를 함수로 추출
2. **SRP**: 함수/클래스는 한 가지 책임만
3. **명시적 타입 힌팅** (Python)
4. **선언적 코딩 우선** (SQLAlchemy, JavaScript)
5. **함수 크기 제한**: 50줄 초과 시 분리
6. **에러 핸들링**: 모든 예외 명시적 처리
7. **로깅**: `print()` 금지, `logger` 사용

---

## 🎨 Phase별 개발 전략

### Phase 1-2: 기본 멀티 에이전트 시스템 ✅ 완료
- 5개 에이전트
- Git 브랜치 자동 관리
- Rate limit 추적

### Phase 3: Skills 아키텍처 ✅ 완료
- 8개 재사용 가능 스킬
- Agent-Skill 분리
- Memory 시스템

### Phase 4: 웹 플랫폼 ✅ 완료 - 삭제
- FastAPI REST API (25+ 엔드포인트)
- 웹 대시보드
- Discord 연동
- GitHub Webhook

### Phase 5: 향후 계획 (참고용)
- Database 연동 (PostgreSQL)
- Authentication (JWT)
- WebSocket (실시간 업데이트)
- Docker/Kubernetes 배포

---

## 🚨 중요 제약사항

### 절대 하면 안 되는 것

1. **하드코딩된 언어/프레임워크 가정**
   ```python
   # ❌ 절대 금지
   if framework == "fastapi":
       # FastAPI 전용 코드
   ```

2. **프로젝트 디렉토리 오염**
   ```bash
   # ❌ 절대 금지
   cp system-file.md projects/user-project/
   ```

3. **에이전트 CLAUDE.md 무단 수정**
   - PM, Coding, QA 등의 CLAUDE.md는 신중하게 수정
   - 테스트 필수

4. **하위 호환성 깨기**
   - 기존 티켓/명세서 형식 유지
   - API 엔드포인트 변경 시 버전 관리

### 반드시 해야 하는 것

1. **에러 핸들링**
   ```python
   try:
       result = execute_agent()
   except FileNotFoundError:
       logger.error("Ticket file not found")
       return {"error": "Ticket not found"}
   except Exception as e:
       logger.error(f"Unexpected error: {e}")
       return {"error": str(e)}
   ```

2. **로깅**
   ```python
   import logging
   logger = logging.getLogger(__name__)

   logger.info(f"Starting agent: {agent_name}")
   logger.error(f"Failed to execute: {error}")
   ```

3. **타입 힌트 (Python)**
   ```python
   def run_pipeline(
       ticket: str,
       project: str,
       resume: bool = False
   ) -> PipelineStatusResponse:
   ```

4. **문서화**
   - 파일에 대한 변동(생성/수정/삭제) 사항이 있을 때, 해당 파일이 속한 디렉토리 내에 `README.md` 파일이 있는 디렉토리라면 해당 README.md 파일을 꼭 수정해주어야 함.
   - 기능 변동(생성/수정/삭제) 사항 생길 시, 무조건 `README.md` 수정
   - 새 API 엔드포인트 → `api/README.md`에 추가
   - 새 스킬 → `docs/skills-guide.md`에 추가
   - 주요 변경사항 → `logs-agent_dev/`에 기록
     - 언제나 파일을 생성/수정/삭제한 내역이 있다면 `logs-agent_dev/{today's date}-{task name}.md` 패턴을 따르는 마크다운 파일에 관련 내용 작성
     - 로그를 작성할 때는 육하원칙에 따라 누가 언제 무엇을 어떻게 왜 수정했는지를 꼭 기록할 것
       - 누가: 누가 생성/수정/삭제하였는지
       - 언제: 언제 생성/수정/삭제하였는지
       - 어디서: 제외
       - 무엇: 어떤 파일들을 생성/수정/삭제하였는지
       - 왜: 왜 생성/수정/삭제하였는지
     - 해당 디렉토리에 작성되는 로그들은 
       1. 이 multi agent coding team 프로젝트의 개발자가 개발 히스토리를 추적하기 용이하게 하기 위함.
       2. 이 multi agent coding team 프로젝트 개발 Agent 가 개발 히스토리를 추적하기 용이하게 하고, 컨텍스트 파악을 용이하게 하기 위함.

---

## 🔍 디버깅 가이드

### API 디버깅

```bash
# 1. 로그 확인
tail -f logs/api.log

# 2. Swagger UI로 테스트
# http://localhost:8000/api/docs

# 3. curl로 직접 테스트
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"ticket": "PLAN-001", "project": "test"}'
```

### Agent 디버깅

```bash
# 1. 직접 실행
cd team/.agents/pm
claude

# 2. 스크립트로 실행 (verbose)
# 모든 에이전트 동일한 방식
bash -x scripts/run-agent.sh pm --ticket PLAN-001
bash -x scripts/run-agent.sh coding --ticket PLAN-001
bash -x scripts/run-agent.sh qa --ticket PLAN-001

# Project Planner는 2가지 방식
bash -x scripts/run-agent.sh project-planner --project "프로젝트 설명"
bash -x scripts/run-agent.sh project-planner --req requirements.md

# 3. 로그 확인
cat projects/{project}/logs/pm/*.md
```

### Skill 디버깅

```bash
# 1. 직접 실행
bash scripts/run-skill.sh commit PLAN-001

# 2. Python으로 직접 호출
python .skills/commit/commit-message-generator.py
```

---

## 📊 테스트 전략

### 1. API 테스트

```bash
# 헬스 체크
curl http://localhost:8000/api/health

# 프로젝트 목록
curl http://localhost:8000/api/projects/list

# 티켓 목록
curl http://localhost:8000/api/projects/bill-organizer/tickets
```

### 2. Agent 테스트

```bash
# Project Planner (파일 입력)
bash scripts/run-agent.sh project-planner --req test-requirements.md

# PM Agent
bash scripts/run-agent.sh pm --ticket PLAN-001

# 결과 확인
ls projects/{project}/planning/specs/
ls projects/{project}/planning/test-cases/
```

### 3. Skill 테스트

```bash
# validate-spec
bash scripts/run-skill.sh validate-spec PLAN-001

# commit
bash scripts/run-skill.sh commit PLAN-001
```

### 4. 웹 대시보드 테스트

```
1. 브라우저: http://localhost:8000
2. 프로젝트 선택
3. 티켓 목록 확인
4. 파이프라인 실행
5. Discord 알림 확인
```

---

## 🔄 마이그레이션 체크리스트

새 기능 추가 시:

- [ ] KR 버전에 구현
- [ ] ENG 버전에 마이그레이션 (번역)
- [ ] A_coding-team에 필요하면 적용
- [ ] README.md 업데이트 (KR + ENG)
- [ ] API 문서 업데이트 (`api/README.md`)
- [ ] 변경 로그 작성 (`logs-agent_dev/`)

---

## 📚 주요 파일 참조
**핵심 원칙**: 사용자의 요청 사항에 따라 수정의 여지가 있음. 별도의 관련 지시가 없을 시에는 참조하고, 별도의 지사가 있을 때에는 수정 가능

### 설계 문서
- `docs/architecture-final.md` - 최종 아키텍처
- `docs/supported-tech-stacks.md` - 지원 스택
- `docs/phase4-complete.md` - Phase 4 완료 보고서

### 에이전트 가이드
- `team/.agents/project-planner/CALUDE.md` - Project Planner Agent(프로젝트 파악 및 전체 티켓 생성)
- `team/.agents/pm/CLAUDE.md` - PM Agent(각 티켓 별 세부 명세서, 요구사항, 테스트 케이스 정의)
- `team/.agents/coding/CLAUDE.md` - Coding Agent(명세서 및 요구사항에 따라 코딩)
- `team/.agents/qa/CLAUDE.md` - QA Agent(테스트 케이스에 따라 Coding Agent가 구현한 내용을 테스트하는 테스트 코드를 작성)

### 스킬 가이드
- `team/docs/skills-guide.md` - Skills 사용 가이드
- `team/.skills/*/skill.md` - 개별 스킬 문서

### API 문서
- `team/api/README.md` - REST API 전체 문서

---

## 🎯 작업 우선순위

### P0 (즉시)
- 에이전트 CLAUDE.md 개선
- 버그 수정
- 보안 이슈

### P1 (중요)
- 새 스킬 추가
- API 엔드포인트 개선
- 웹 대시보드 기능 추가

### P2 (나중에)
- Database 연동
- Authentication
- 성능 최적화

---

## 💡 개발 팁

### 1. 점진적 개발
```
1. KR 버전에서 먼저 구현
2. 테스트
3. ENG 버전 마이그레이션
4. 문서화
```

### 2. 에이전트 수정 시
```
1. .agents/{agent}/CLAUDE.md 백업
2. 수정
3. 테스트 (실제 티켓으로)
4. 문제 없으면 커밋
```

### 3. API 개발 시
```
1. models/ (Pydantic) 먼저 정의
2. services/ 비즈니스 로직
3. routers/ 엔드포인트
4. main.py에 등록
5. Swagger UI 확인
```

### 4. 웹 대시보드 개발 시
```
1. HTML 구조 먼저
2. CSS 스타일
3. JavaScript 로직
4. API 연동
5. 에러 핸들링
```

---

## 🔐 보안 고려사항

### API Keys
- `.env` 파일에만 저장
- Git에 절대 커밋 안 됨 (`.gitignore`)
- `.env.example`은 템플릿만

### GitHub Webhook
- HMAC-SHA256 서명 검증 필수
- `api/routers/webhooks.py` 참조

### Discord Webhook
- URL 노출 주의
- 환경 변수로만 관리

---

## 📖 학습 자료

### FastAPI
- 공식 문서: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/

### Discord Webhooks
- 공식 문서: https://discord.com/developers/docs/resources/webhook

### Claude Code
- 문서: https://docs.claude.ai/claude-code
- CLAUDE.md 가이드: 각 에이전트 폴더 참조

---

## ✅ 작업 완료 기준

1. **코드 품질**
   - [ ] 타입 힌트 추가
   - [ ] Docstring 작성
   - [ ] 에러 핸들링 구현
   - [ ] 로깅 추가

2. **테스트**
   - [ ] 로컬에서 동작 확인
   - [ ] API 엔드포인트 테스트
   - [ ] 웹 대시보드 확인

3. **문서화**
   - [ ] README 업데이트
   - [ ] API 문서 업데이트
   - [ ] 변경 로그 작성

4. **마이그레이션**
   - [ ] ENG 버전 동기화
   - [ ] 필요 시 A_coding-team 동기화

---

## 🚀 시작하기

```bash
# 1. 프로젝트 루트로 이동
cd /Users/geunwoopark/Desktop/multi_agent_coding_team/KR-multi-agent-coding-team

# 2. 현재 상태 확인
git status

# 3. team 디렉토리로 이동
cd team

# 4. 에이전트 실행 테스트
# 방법 1: 터미널 입력
bash scripts/run-agent.sh project-planner --project "테스트 TODO 앱"

# 방법 2: 파일 입력
cat > requirements.md <<EOF
# 테스트 프로젝트
간단한 TODO 앱
EOF
bash scripts/run-agent.sh project-planner --req requirements.md

# PM Agent (티켓 번호만으로 자동 감지)
bash scripts/run-agent.sh pm --ticket PLAN-001

# 5. API 서버 실행 (테스트)
cd team
uvicorn api.main:app --reload --port 8000

# 4. 새 터미널에서 개발 시작
cd team
# 작업 시작...
```

---

**이 파일은 Multi-Agent Coding Team 시스템을 개발하는 에이전트를 위한 가이드입니다.**
**사용자용 가이드는 README.md를 참조하세요.**
