# 시스템 개선 가이드

> 멀티 에이전트 시스템 개발자를 위한 기여 가이드

**버전**: v0.0.2
**최종 업데이트**: 2026-03-12
**대상**: 시스템 개발자

---

## 🎯 이 문서의 목적

이 문서는 멀티 에이전트 **시스템 자체**를 개선하는 개발자를 위한 가이드입니다.

시스템 사용자가 에이전트를 이용하여 프로젝트를 구현하는 방법은 [루트 README.md](../README.md)를 참고하세요.

---

## 📂 시스템 구조 이해

### 핵심 디렉토리

```
team/
├── .agents/              # 에이전트 지시 파일 (CLAUDE.md)
├── .rules/               # 코딩 룰
│   ├── _verified/        # 검증된 룰
│   └── _cache/           # 자동 생성 룰
├── .config/              # 시스템 설정
├── scripts/              # 시스템 스크립트
├── projects/             # 사용자 프로젝트 (독립 Git)
└── docs/                 # 시스템 문서 (이 디렉토리)
```

### 문서 및 로그 구분

| 디렉토리 | 목적 | 대상 | 예시 |
|---------|------|------|-----|
| `docs/` | 시스템 참고 문서 | 시스템 개발자 | architecture.md, git-branch-strategy.md |
| `logs-agent_dev/` | 시스템 개발 로그 | 시스템 개발자 | 20260312-v0.0.2-cleanup.md |
| `team/projects/{name}/logs/` | 프로젝트 구현 로그 | 시스템 사용자 | coding/20260312-PLAN-001.md |
| 루트 `README.md` | 사용자 가이드 | 시스템 사용자 | 워크플로우, 사용법 |

---

## 🛠️ 시스템 개선 작업 유형

### 1. 에이전트 추가/수정

**위치**: `team/.agents/{agent-name}/CLAUDE.md`

**절차**:
1. 새 에이전트 디렉토리 생성
2. CLAUDE.md 작성 (프롬프트)
3. 필요 시 templates/ 디렉토리 추가
4. `scripts/run-agent.sh`에 case 추가
5. 테스트 실행
6. 문서 업데이트 (README.md, architecture.md)

**예시**:
```bash
# 새 에이전트 추가
mkdir -p team/.agents/devops
vim team/.agents/devops/CLAUDE.md

# run-agent.sh 수정
vim team/scripts/run-agent.sh
# case에 devops 추가

# 테스트
cd team
bash scripts/run-agent.sh devops --help
```

### 2. 프로젝트 타입 추가

**영향 범위**:
- `.agents/pm/templates/{new-type}.md`
- `.agents/coding/templates/{new-type}.md`
- `.agents/qa/templates/{new-type}.md`
- `docs/supported-tech-stacks.md`
- `scripts/init-project.sh`

**절차**:
1. 프로젝트 타입 정의 (예: `iot-firmware`)
2. 각 에이전트 템플릿 작성
3. init-project.sh에 타입 추가
4. 테스트 프로젝트 생성/검증
5. 문서 업데이트

### 3. 스크립트 개선

**위치**: `team/scripts/`

**주요 스크립트**:
- `init-project.sh`: 프로젝트 초기화
- `run-agent.sh`: 에이전트 실행 래퍼
- `git-branch-helper.sh`: Git 브랜치 관리
- `rate-limit-check.sh`: Rate Limit 관리
- `show-logs.sh`: 로그 조회

**절차**:
1. 스크립트 수정
2. 테스트 (다양한 케이스)
3. 에러 처리 추가
4. 문서화 (주석, README)
5. 버전 커밋

### 4. 코딩 룰 추가/개선

**위치**: `team/.rules/`

**구조**:
```
.rules/
├── general-coding-rules.md    # 범용 원칙
├── _verified/                  # 검증된 룰
│   └── {project-type}/
│       └── {framework}-{language}.md
└── _cache/                     # 자동 생성 (24시간)
```

**절차**:
1. Stack Initializer가 생성한 룰 검토 (`_cache/`)
2. 실제 사용 후 품질 확인
3. 검증 완료 시 `_verified/`로 이동
4. 파일명 규칙: `{framework}-{language}.md`

**예시**:
```bash
# 자동 생성된 룰 확인
cat team/.rules/_cache/cli-tool/cobra-go.md

# 검증 후 이동
mkdir -p team/.rules/_verified/cli-tool
mv team/.rules/_cache/cli-tool/cobra-go.md \
   team/.rules/_verified/cli-tool/

# 커밋
git add team/.rules/_verified/cli-tool/cobra-go.md
git commit -m "rules: verify cobra-go coding rules"
```

---

## 📝 개발 로그 작성

### 시스템 개발 로그 위치

`logs-agent_dev/`

### 파일명 규칙

```
YYYYMMDD-{topic}.md
```

**예시**:
- `20260312-v0.0.2-cleanup.md`
- `20260313-git-branch-improvement.md`
- `20260314-new-agent-design.md`

### 로그 내용 구조

```markdown
# {작업 제목}

**날짜**: YYYY-MM-DD
**목적**: 왜 이 작업을 했는가

## 변경 사항

### 추가
- 무엇을 추가했는가

### 수정
- 무엇을 수정했는가

### 삭제
- 무엇을 삭제했는가

## 의사결정

### 선택한 방안
설명

### 대안
- 대안 A: 왜 선택하지 않았는가
- 대안 B: 왜 선택하지 않았는가

## 테스트

수행한 테스트 및 결과

## 다음 작업

향후 개선 사항
```

---

## 🔄 Git 워크플로우

### 브랜치 전략 (시스템 개발)

**베이스**: `dev` (시스템 개발 브랜치)

**브랜치 패턴**:
```
dev
├── feature/system-{feature-name}
├── fix/system-{bug-name}
└── docs/system-{doc-name}
```

**예시**:
```bash
git checkout dev
git pull origin dev

# 새 기능 개발
git checkout -b feature/system-iot-firmware-support
# 작업...
git add .
git commit -m "feat: add IoT firmware project type support"
git push origin feature/system-iot-firmware-support
# PR: feature/system-iot-firmware-support → dev
```

### 커밋 메시지 규칙

**포맷**:
```
{type}({scope}): {description}

{body}
```

**타입**:
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서만 변경
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드, 설정 변경

**스코프** (선택):
- `agent`: 에이전트 관련
- `script`: 스크립트 관련
- `rules`: 코딩 룰 관련
- `docs`: 문서 관련

**예시**:
```bash
git commit -m "feat(agent): add DevOps agent for CI/CD automation"
git commit -m "fix(script): resolve branch detection in git-branch-helper.sh"
git commit -m "docs: update architecture for v0.0.3"
git commit -m "refactor(rules): restructure _verified directory by project type"
```

---

## 🧪 테스트

### 수동 테스트 체크리스트

새 기능 추가 시 확인 사항:

- [ ] 프로젝트 초기화가 정상 동작하는가
- [ ] 에이전트가 올바른 템플릿을 로드하는가
- [ ] Git 브랜치가 올바르게 생성되는가
- [ ] 로그가 올바른 위치에 생성되는가
- [ ] Rate Limit 체크가 동작하는가
- [ ] 다중 프로젝트 전환이 동작하는가
- [ ] 모든 프로젝트 타입에서 동작하는가

### 테스트 프로젝트 생성

```bash
cd team

# 각 타입별 테스트 프로젝트 생성
bash scripts/init-project.sh \
  --type web-fullstack \
  --name test-web-app \
  --language python,typescript \
  --framework fastapi,nextjs

bash scripts/init-project.sh \
  --type cli-tool \
  --name test-cli \
  --language go \
  --framework cobra

# 에이전트 실행 테스트
bash scripts/run-agent.sh project-planner \
  --project "Test TODO app"

bash scripts/run-agent.sh pm \
  --ticket-file projects/test-web-app/planning/tickets/PLAN-001*.md

bash scripts/run-agent.sh coding --ticket PLAN-001

bash scripts/run-agent.sh qa --ticket PLAN-001
```

---

## 📚 문서 업데이트

### 문서 파일 위치

| 파일 | 목적 | 업데이트 시기 |
|------|------|-------------|
| `README.md` (루트) | 사용자 가이드 | 사용자 워크플로우 변경 시 |
| `docs/architecture.md` | 시스템 아키텍처 | 구조 변경 시 |
| `docs/git-branch-strategy.md` | Git 브랜치 전략 | 브랜치 전략 변경 시 |
| `docs/supported-tech-stacks.md` | 지원 스택 목록 | 새 스택 추가 시 |
| `docs/CHANGELOG.md` | 변경 이력 | 모든 릴리스 |
| `docs/contributing.md` | 이 문서 | 개발 프로세스 변경 시 |

### 버전 업데이트

새 버전 릴리스 시:

1. **CHANGELOG.md 업데이트**
   ```markdown
   ## [0.0.3] - 2026-03-15

   ### Added
   - ...

   ### Changed
   - ...
   ```

2. **문서 frontmatter 업데이트**
   ```markdown
   **버전**: v0.0.3
   **최종 업데이트**: 2026-03-15
   ```

3. **README.md 버전 태그 업데이트**

---

## 🚀 릴리스 프로세스

### 버전 관리

**버전 체계**: Semantic Versioning (Major.Minor.Patch)

- **Major (1.0.0)**: 호환성 깨지는 변경
- **Minor (0.1.0)**: 새 기능 추가 (호환 유지)
- **Patch (0.0.1)**: 버그 수정

**현재 버전**: `v0.0.2` (beta)

### 릴리스 절차

```bash
# 1. dev 브랜치에서 릴리스 준비
git checkout dev
git pull origin dev

# 2. 버전 확인 및 문서 업데이트
vim docs/CHANGELOG.md
# [Unreleased] → [0.0.3]

vim README.md
# 버전 태그 업데이트

# 3. 커밋
git add .
git commit -m "chore: prepare release v0.0.3"

# 4. main에 머지
git checkout main
git merge dev
git tag -a v0.0.3 -m "Release v0.0.3"
git push origin main --tags

# 5. dev 브랜치 동기화
git checkout dev
git merge main
git push origin dev
```

---

## 🔧 트러블슈팅

### 자주 발생하는 문제

#### Q1. Rate Limit 초과

```bash
# rate-limit-check.sh 확인
bash scripts/rate-limit-check.sh

# 사용량 파싱
python3 scripts/parse_usage.py
```

#### Q2. Git 브랜치 생성 실패

```bash
# 설정 확인
bash scripts/git-branch-helper.sh config

# 수동 브랜치 준비
bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth
```

#### Q3. 프로젝트 컨텍스트 인식 실패

```bash
# .project-config.json 확인
cat team/.project-config.json

# current_project 설정 확인
jq '.current_project' team/.project-config.json
```

---

## 📞 커뮤니케이션

### 이슈 제기

GitHub Issues 사용

**템플릿**:
```markdown
## 문제 설명
무슨 문제인가?

## 재현 방법
1. ...
2. ...

## 예상 동작
무엇이 일어나야 하는가?

## 실제 동작
무엇이 일어났는가?

## 환경
- OS: macOS/Linux/Windows
- Shell: bash/zsh
- Claude Code 버전: ...
```

### Pull Request

**템플릿**:
```markdown
## 변경 내용
무엇을 변경했는가?

## 목적
왜 변경했는가?

## 테스트
어떻게 테스트했는가?

## 체크리스트
- [ ] 문서 업데이트
- [ ] CHANGELOG.md 업데이트
- [ ] 테스트 완료
```

---

## 📖 참고 자료

- [Architecture](./architecture.md): 시스템 구조
- [Git Branch Strategy](./git-branch-strategy.md): 브랜치 전략
- [Supported Tech Stacks](./supported-tech-stacks.md): 지원 스택
- [CHANGELOG](./CHANGELOG.md): 변경 이력

---

**버전**: v0.0.2
**최종 업데이트**: 2026-03-12
