# KR-multi-agent-coding-team 프로젝트 전체 구조

## 📁 루트 디렉토리

```
KR-multi-agent-coding-team/
├── CLAUDE.md                    # 이 프로젝트 개발용 Agent 지시사항
├── CODING-RULES.md              # 이 프로젝트 코딩 규칙
├── LICENSE                      # 라이센스
├── README.md                    # 메인 README
├── .gitignore                   # Git 무시 파일
├── .github/                     # GitHub 설정
│   ├── CODEOWNERS
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── docs/                        # 📚 아키텍처 문서
├── logs-agent_dev/              # 📝 KR-multi-agent-coding-team 프로젝트 개발 로그 (35개)
└── team/                        # ⭐ 핵심 작업 디렉토리
```

---

## ⭐ team/ (핵심 디렉토리)

```
team/
├── .agents/                     # 5개 에이전트 정의
│   ├── coding/
│   │   └── CLAUDE.md
│   ├── pm/
│   │   ├── CLAUDE.md
│   │   ├── gotchas.md
│   │   └── workflows/
│   │       ├── cli-tool.md
│   │       ├── desktop-app.md
│   │       ├── lib-package.md
│   │       ├── ml-project.md
│   │       └── web-fullstack.md
│   ├── project-planner/
│   │   └── CLAUDE.md
│   ├── qa/
│   │   └── CLAUDE.md
│   └── stack-initializer/
│       └── CLAUDE.md
│
├── .skills/                     # 8개 재사용 가능 스킬
│   ├── benchmark/
│   │   └── skill.md
│   ├── commit/
│   │   ├── skill.md
│   │   └── commit-message-generator.py
│   ├── deploy/
│   │   └── skill.md
│   ├── docs-generator/
│   │   └── skill.md
│   ├── refactor-code/
│   │   ├── skill.md
│   │   └── refactor-code.py
│   ├── review-pr/
│   │   ├── skill.md
│   │   ├── review-pr.py
│   │   └── review-checklist.json
│   ├── test-runner/
│   │   └── skill.md
│   └── validate-spec/
│       ├── skill.md
│       ├── validate.py
│       └── rules.json
│
├── .rules/                      # 코딩 룰 저장소
│   ├── general-coding-rules.md
│   ├── _verified/               # 검증된 코딩 룰
│   │   ├── cli-tool/
│   │   ├── desktop-app/
│   │   ├── lib-package/
│   │   ├── ml-project/
│   │   └── web-fullstack/
│   └── _cache/                  # 자동 생성된 코딩 룰
│       ├── cli-tool/
│       ├── desktop-app/
│       ├── lib-package/
│       ├── ml-project/
│       └── web-fullstack/
│
├── .config/                     # 시스템 설정
│   ├── auto-responses.json
│   └── log-schema.json
│
├── .memory/                     # 학습 시스템
│   ├── patterns.json
│   ├── commit-history.json
│   └── review-history.json
│
├── scripts/                     # CLI 도구
│   ├── run-agent.sh             # 에이전트 실행
│   ├── resume-session.sh        # 세션 재개
│   ├── run-skill.sh             # 스킬 실행
│   ├── init-project.sh          # 프로젝트 초기화
│   ├── switch-project.sh        # 프로젝트 전환
│   ├── auto_pipeline_v2.py      # 자동 파이프라인
│   ├── README.md
│   └── .legacy/                 # 레거시 스크립트
│
├── docs/                        # 시스템 문서
│   ├── auto-pipeline-v2-guide.md
│   ├── session-management.md
│   └── skills-guide.md
│
├── projects/                    # 🎯 사용자 프로젝트 작업 공간
│   ├── korean-legal-case-evaluator/
│   │   ├── .project-meta.json
│   │   ├── .sessions/           # 세션 저장
│   │   │   ├── KLCE-001/
│   │   │   ├── KLCE-002/
│   │   │   └── session-map.json
│   │   ├── planning/
│   │   │   ├── tickets/
│   │   │   ├── specs/
│   │   │   └── test-cases/
│   │   ├── logs/
│   │   │   ├── pm/
│   │   │   ├── coding/
│   │   │   └── qa/
│   │   ├── src/                 # 실제 코드
│   │   └── README.md
│   └── README.md
│
├── .project-config.json         # 현재 활성 프로젝트 설정
├── .project-meta.schema.json   # 프로젝트 메타데이터 스키마
├── .env.example                 # 환경 변수 예시
├── .gitignore                   # Git 무시 파일
└── README.md                    # team/ README
```

---

## 📚 docs/ (아키텍처 문서)

```
docs/
├── architecture.md              # 전체 아키텍처
├── supported-tech-stacks.md     # 지원하는 기술 스택
├── CHANGELOG.md                 # 변경 로그
├── contributing.md              # 기여 가이드
├── git-branch-strategy.md       # Git 브랜치 전략
├── improvement-plan.md          # 개선 계획
├── api-migration-plan.md        # API 마이그레이션 계획
└── phase*.md                    # Phase별 완료 보고서 (13개)
```

---

## 📝 logs-agent_dev/ (개발 로그)

```
logs-agent_dev/
├── README.md
├── 20260309-*.md                # 3월 9일 작업 (3개)
├── 20260312-*.md                # 3월 12일 작업 (1개)
├── 20260316-*.md                # 3월 16일 작업 (1개)
├── 20260319-*.md                # 3월 19일 작업 (2개)
├── 20260320-*.md                # 3월 20일 작업 (12개)
├── 20260323-*.md                # 3월 23일 작업 (7개)
├── 20260324-*.md                # 3월 24일 작업 (1개)
└── 2026-03-20-*.md              # 3월 20일 작업 (8개)

총 35개 로그 파일
```

---

## 🎯 프로젝트별 구조 (예시)

```
team/projects/korean-legal-case-evaluator/
├── .project-meta.json           # 프로젝트 메타데이터
│   {
│     "project_type": "web-fullstack",
│     "language": "typescript",
│     "framework": "nestjs",
│     "ticket_acronym": "KLCE"
│   }
│
├── .sessions/                   # 세션 관리
│   ├── KLCE-001/
│   │   ├── pm.session
│   │   ├── coding.session
│   │   └── qa.session
│   ├── KLCE-002/
│   │   └── pm.session
│   └── session-map.json
│
├── planning/                    # 기획 산출물
│   ├── tickets/
│   │   ├── KLCE-001-user-auth.md
│   │   └── KLCE-002-case-upload.md
│   ├── specs/
│   │   ├── backend/
│   │   │   ├── KLCE-001-user-auth.md
│   │   │   └── KLCE-002-case-upload.md
│   │   └── frontend/
│   └── test-cases/
│       ├── KLCE-001-backend.md
│       └── KLCE-001-frontend.md
│
├── logs/                        # 에이전트 작업 로그
│   ├── pm/
│   ├── coding/
│   └── qa/
│
├── src/                         # 실제 코드
│   ├── backend/
│   └── frontend/
│
└── README.md
```

---

## 📊 통계

### 파일 수
- **에이전트**: 5개 (pm, coding, qa, project-planner, stack-initializer)
- **스킬**: 8개 (commit, review-pr, refactor-code, test-runner, deploy, benchmark, docs-generator, validate-spec)
- **코딩 룰**: 2개 디렉토리 (verified, cache)
- **스크립트**: 6개 (.sh, .py)
- **문서**: 14개 (docs/) + 35개 (logs-agent_dev/)
- **프로젝트**: 1개 (korean-legal-case-evaluator)

### 주요 디렉토리 크기
- `team/`: 핵심 시스템 (가장 중요)
- `docs/`: 아키텍처 문서
- `logs-agent_dev/`: 개발 히스토리
- `team/projects/`: 사용자 프로젝트 (Git 리포별로 독립)

---

## 🔑 핵심 파일

1. **CLAUDE.md** - 시스템 개발 Agent 지시사항
2. **team/.agents/*/CLAUDE.md** - 각 Agent 지시사항
3. **team/scripts/run-agent.sh** - Agent 실행 래퍼
4. **team/scripts/resume-session.sh** - 세션 재개 ⭐
5. **team/.project-meta.schema.json** - 프로젝트 스키마 정의
6. **team/.project-config.json** - 현재 활성 프로젝트

---

## 🚀 주요 워크플로우

1. **프로젝트 초기화**
   ```bash
   bash team/scripts/init-project.sh --interactive
   ```

2. **에이전트 실행**
   ```bash
   bash team/scripts/run-agent.sh project-planner --project "..."
   bash team/scripts/run-agent.sh pm --ticket PLAN-001
   bash team/scripts/run-agent.sh coding --ticket PLAN-001
   bash team/scripts/run-agent.sh qa --ticket PLAN-001
   ```

3. **세션 재개** ⭐
   ```bash
   bash team/scripts/resume-session.sh --list
   bash team/scripts/resume-session.sh PLAN-001 coding
   ```

---

**총 라인 수**: 약 50,000+ 줄 (코드 + 문서 + 스크립트)
