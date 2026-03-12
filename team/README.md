# Team 작업 디렉토리

이 디렉토리는 멀티 에이전트 시스템의 **작업 디렉토리**입니다. 모든 명령어는 여기서 실행됩니다.

---

## 📍 현재 위치

```
KR-multi-agent-coding-team/          # 시스템 루트
└── team/                            # ← 여기 (작업 디렉토리)
```

---

## 🚀 빠른 시작

### 1. 프로젝트 초기화

```bash
bash scripts/init-project.sh --interactive
```

### 2. 프로젝트 Git 리포지토리 초기화

```bash
cd projects/{your-project-name}
git init
git remote add origin https://github.com/your-username/{your-project-name}.git
cd ../..
```

### 3. 에이전트 워크플로우

```bash
# Stack 초기화
bash scripts/run-agent.sh stack-initializer

# 티켓 생성
bash scripts/run-agent.sh project-planner --project "프로젝트 설명"

# 명세서 작성
bash scripts/run-agent.sh pm --ticket-file projects/{name}/planning/tickets/PLAN-001-*.md

# 코딩
bash scripts/run-agent.sh coding --ticket PLAN-001

# 테스트
bash scripts/run-agent.sh qa --ticket PLAN-001
```

---

## 📁 디렉토리 구조

```
team/
├── .agents/                         # 에이전트 정의 (5개)
│   ├── stack-initializer/
│   ├── project-planner/
│   ├── pm/
│   ├── coding/
│   └── qa/
│
├── .rules/                          # 코딩 룰
│   ├── general-coding-rules.md      # 범용 원칙
│   ├── _cache/                      # AI 자동 생성 (24h)
│   └── _verified/                   # 사람이 검증
│
├── .config/                         # 시스템 설정
│   └── git-workflow.json
│
├── scripts/                         # 유틸리티 스크립트
│   ├── init-project.sh              # 프로젝트 초기화
│   ├── switch-project.sh            # 프로젝트 전환
│   ├── run-agent.sh                 # 에이전트 실행
│   ├── show-logs.sh                 # 로그 조회
│   ├── git-branch-helper.sh         # Git 브랜치 관리
│   └── rate-limit-check.sh          # Rate Limit 체크
│
├── projects/                        # 프로젝트 작업 공간
│   ├── project-a/                   # 각 프로젝트는 독립 Git 리포지토리
│   │   ├── .project-meta.json       # ← 프로젝트 스택 세팅
│   │   ├── .git/                    # ← 프로젝트 자체의 Git
│   │   ├── planning/
│   │   ├── src/
│   │   └── logs/
│   └── project-b/
│       └── ...
│
├── .project-config.json             # 현재 활성 프로젝트
└── README.md                        # 이 파일
```

---

## 🔄 프로젝트 전환

한 시스템에서 여러 프로젝트를 관리할 수 있습니다:

```bash
# 프로젝트 목록
bash scripts/switch-project.sh --list

# 프로젝트 전환
bash scripts/switch-project.sh project-b

# 이제 모든 명령어는 project-b 컨텍스트에서 실행됨
bash scripts/run-agent.sh coding --ticket PLAN-005
```

---

## 📚 자세한 문서

- [루트 README.md](../README.md) - 전체 시스템 개요
- [스크립트 가이드](scripts/README.md) - 각 스크립트 사용법
- [코딩 룰 가이드](.rules/README.md) - 코딩 룰 시스템
- [아키텍처 문서](../docs/architecture-final.md) - 상세 아키텍처

---

**버전**: v0.0.2
**최종 업데이트**: 2026-03-12
