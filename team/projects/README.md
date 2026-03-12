# Projects Directory

이 디렉토리는 모든 프로젝트를 포함합니다.

**중요:** 각 프로젝트는 **독립적인 Git 리포지토리**로 관리되며, 프로젝트 타입에 따라 다른 구조를 가집니다.

---

## 📂 구조

```
projects/
├── {project-name-1}/
│   ├── .git/                       # ← 프로젝트 A의 Git 리포지토리
│   ├── .project-meta.json          # 프로젝트 메타데이터
│   ├── planning/                   # 기획 문서
│   │   ├── tickets/
│   │   ├── specs/
│   │   └── test-cases/
│   ├── src/                        # 실제 코드
│   ├── logs/                       # 에이전트 로그
│   └── README.md
├── {project-name-2}/
│   ├── .git/                       # ← 프로젝트 B의 Git 리포지토리
│   └── ...
└── README.md                       # 이 파일
```

---

## 🚀 새 프로젝트 생성

```bash
cd team
bash scripts/init-project.sh --interactive
```

또는 플래그 방식:

```bash
bash scripts/init-project.sh \
  --type cli-tool \
  --language go \
  --framework cobra \
  --name my-cli-tool
```

---

## 🔄 프로젝트 전환

```bash
# 프로젝트 목록 확인
ls projects/

# 특정 프로젝트로 전환
bash scripts/switch-project.sh my-cli-tool
```

---

## 📋 프로젝트별 메타데이터

각 프로젝트는 `.project-meta.json` 파일을 포함합니다:

```json
{
  "project_name": "my-cli-tool",
  "project_type": "cli-tool",
  "stack": {
    "language": "go",
    "framework": "cobra",
    "version": "latest"
  },
  "created_at": "2026-03-12T10:00:00Z",
  "directory_structure": "cli-tool",
  "active": true
}
```

---

## 🗂️ 프로젝트 타입별 구조

### Web Fullstack

```
planning/specs/
├── backend/
└── frontend/
```

### Web MVC

```
planning/specs/
├── endpoints/
└── templates/
```

### CLI Tool

```
planning/specs/
└── (플랫 구조)
```

### Desktop App

```
planning/specs/
├── screens/
├── state/
└── ipc/
```

### Library

```
planning/specs/
├── api/
└── examples/
```

### Data Pipeline

```
planning/specs/
├── dags/
├── transforms/
└── schedules/
```

---

## 📝 작업 예시

### 1. 프로젝트 생성

```bash
bash scripts/init-project.sh --type cli-tool --language go --framework cobra --name file-search
```

### 2. Git 리포지토리 초기화

```bash
cd projects/file-search
git init
git add .
git commit -m "chore: initial project structure"
git remote add origin https://github.com/your-username/file-search.git
git push -u origin main
cd ../..
```

### 3. 티켓 생성

```bash
bash scripts/run-agent.sh project-planner --project "파일 검색 CLI"
```

### 4. 명세서 생성 (Git 브랜치 자동 생성)

```bash
bash scripts/run-agent.sh pm --ticket-file projects/file-search/planning/tickets/PLAN-001-search.md
# → projects/file-search/.git에서 docs/PLAN-001-search 브랜치 자동 생성
```

### 5. 코딩 (Git 브랜치 자동 생성)

```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
# → projects/file-search/.git에서 feature/PLAN-001-search 브랜치 자동 생성
```

### 6. 테스트 (Git 브랜치 자동 생성)

```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
# → projects/file-search/.git에서 test/PLAN-001-search 브랜치 자동 생성
```

### 7. 커밋 및 푸시

```bash
cd projects/file-search
git add .
git commit -m "feat(PLAN-001): 파일 검색 기능 구현 및 테스트 완료"
git push origin feature/PLAN-001-search
cd ../..
```

---

## 🔍 프로젝트 상태 확인

```bash
# 현재 활성 프로젝트
cat ../.project-config.json

# 특정 프로젝트 메타데이터
cat projects/my-cli-tool/.project-meta.json

# 프로젝트별 로그
bash scripts/show-logs.sh
```

---

**업데이트 일시**: 2026-03-12
