# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v0.0.2.html).

---

## [Unreleased]

---

## [0.0.2] - 2026-03-12

### Added
- **Tech Stack Agnostic Architecture**: 모든 개발 타입 지원
  - web-fullstack, web-mvc, cli-tool, desktop-app, mobile-app, library, data-pipeline
- **프로젝트 격리 구조**: `team/projects/{project-name}/`
  - 각 프로젝트는 독립적인 Git 리포지토리
  - 프로젝트별 planning, logs 디렉토리
  - 다중 프로젝트 동시 관리 가능
- **Stack Initializer Agent**: 프로젝트 타입 및 스택에 맞는 환경 자동 초기화
  - 공식 문서 자동 분석 (WebSearch, WebFetch)
  - 코딩 룰 자동 생성 (`.rules/_cache/`)
  - PM/Coding/QA 템플릿 자동 생성
  - 프로젝트 초기 구조 생성
- **init-project.sh**: 프로젝트 초기화 스크립트
  - 대화형 모드 지원
  - 플래그 방식 지원
  - Stack Initializer Agent 자동 호출
- **통합 에이전트 구조**: `coding`, `qa` 에이전트 (모든 타입 지원)
- **동적 템플릿 시스템**: `.agents/{agent}/templates/{project_type}.md`
- **코딩 룰 우선순위 시스템**:
  - `.rules/_verified/`: 사람이 검증한 룰 (최우선)
  - `.rules/_cache/`: 자동 생성 룰 (24시간 캐시)
- **범용 코딩 원칙**: `.rules/general-coding-rules.md` (DRY, SOLID, 보안 등)
- **프로젝트 메타데이터**: `.project-meta.json` (각 프로젝트)
- **전역 프로젝트 설정**: `.project-config.json` (루트)
- **설정 스키마**: `.project-config.schema.json`
- **Git 브랜치 전략 개선**:
  - PM/Coding: base_branch (main/dev)에서 분기
  - QA: feature 브랜치에서 분기
  - 자동 브랜치 생성/전환
  - 브랜치명: `{prefix}/{ticket-number}-{slug}`

### Changed
- **디렉토리 구조 전면 재편**:
  - 고정된 `be-`/`fe-` 구조 제거
  - 프로젝트 타입 기반 동적 구조 생성
  - 각 프로젝트가 독립적인 Git 리포지토리로 관리
- **run-agent.sh 개선**:
  - 자동 프로젝트 컨텍스트 감지 (`.project-config.json`)
  - 자동 Git 브랜치 생성 (coding, qa)
  - 티켓 파일에서 slug 자동 추출
- **git-branch-helper.sh 개선**:
  - QA Agent는 feature 브랜치를 베이스로 사용
  - 에이전트별 prefix 자동 설정 (pm: docs, coding: feature, qa: test)
- **문서 재정리**:
  - docs/: 시스템 개발자용 문서
  - logs-agent_dev/: 시스템 개발 로그
  - team/projects/{name}/logs/: 프로젝트 구현 로그
- **.gitignore 업데이트**:
  - projects/ 하위 디렉토리 제외 (독립 리포지토리)

### Removed
- 고정된 디렉토리 구조 (FastAPI + Next.js 종속)
- Tech Stack 종속적인 구조

---

## [1.0.0] - 2026-03-09

### Added
- **Project Planner Agent**: 프로젝트 분해 및 티켓 생성
  - Phase 분할 실행 (컨텍스트 윈도우 관리)
  - 배치 단위 티켓 생성 (5개씩)
  - 재개 기능 (`--resume`)
- **PM Agent**: API 명세서, UI 명세서, 와이어프레임, 테스트 케이스 생성
  - 인터랙션 와이어프레임 지원 (바닐라 JS)
  - 티켓 기반 자동 파일명 생성
- **BE Coding Agent**: FastAPI 백엔드 구현
  - Layered Architecture
  - Repository Pattern (Protocol + Implementation)
  - 도메인별 예외 처리
- **FE Coding Agent**: Next.js 프론트엔드 구현
  - App Router
  - Server/Client Component 분리
  - 타입 안전성 (TypeScript)
- **QA-BE Agent**: pytest 테스트 스위트 작성
- **QA-FE Agent**: Vitest 테스트 스위트 작성
- **Git 브랜치 워크플로우 자동화**:
  - `git-branch-helper.sh`
  - `.config/git-workflow.json` 설정 파일
  - 티켓별 자동 브랜치 생성/전환 (feature/be/PLAN-XXX, feature/fe/PLAN-XXX 등)
- **Rate Limit 관리 시스템**:
  - `rate-limit-check.sh`
  - `parse_usage.py`
  - Claude Max 5x 티어 기준 (35회 경고, 45회 중단)
- **구현 로그 시스템**: 모든 에이전트가 작업 완료 시 로그 작성
  - `applications/logs/{agent}/` 디렉토리
  - 의사결정 내역, 대안 비교, 검수자 주의사항 포함
- **show-logs.sh**: 로그 조회 스크립트
- **run-agent.sh**: 에이전트 실행 래퍼 스크립트

### Documentation
- README.md: 전체 워크플로우 가이드
- 코딩 룰:
  - `.rules/be-coding-rules.md` (FastAPI)
  - `.rules/fe-coding-rules.md` (Next.js)
- 개발 로그: `logs-agent_dev/`
  - Git 워크플로우 자동화 로그
  - 컨텍스트 윈도우 관리 로그

---

## [0.1.0] - 2026-01-15 (초기 베타)

### Added
- 기본 에이전트 구조
- FastAPI + Next.js 고정 스택
- 수동 티켓 생성 워크플로우

---

[Unreleased]: https://github.com/user/repo/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/user/repo/compare/v0.0.1...v0.0.2
[1.0.0]: https://github.com/user/repo/compare/v0.1.0...v0.0.1
[0.1.0]: https://github.com/user/repo/releases/tag/v0.1.0
