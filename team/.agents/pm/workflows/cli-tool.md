# CLI Tool 워크플로우

> **프로젝트 타입**: cli-tool (예: Go Cobra, Python Click, Rust Clap)
>
> **적용 조건**: `.project-meta.json`의 `project_type`이 `"cli-tool"`인 경우

---

## 📂 산출물 구조

```
projects/{current_project}/planning/specs/
├── PLAN-{번호}-command-spec.md        # 커맨드 명세서
└── test-cases/
    └── PLAN-{번호}-command.md          # 커맨드 테스트 케이스
```

---

## 🔨 작업 순서

### Step 1: 티켓 분석

티켓에서 다음 항목을 추출:
- [ ] 커맨드명 (예: `mycli init`, `mycli search`)
- [ ] 플래그/옵션 (예: `--name`, `--verbose`)
- [ ] 인자 (예: `<파일명>`, `<경로>`)
- [ ] 출력 형식 (stdout, stderr, exit code)
- [ ] 에러 케이스

**⚠️ Gotcha 체크**:
- CLI Tool은 UI 없음 → 와이어프레임 불필요
- 출력은 텍스트/JSON만 → HTML 생성 금지

---

### Step 2: 산출물 목록 제시

사용자에게 생성할 파일 목록을 보여주고 승인받습니다.

**템플릿**:
```
프로젝트: {current_project} (cli-tool)
티켓: PLAN-{번호}-{slug}

생성 예정 파일:
- projects/{current_project}/planning/specs/PLAN-{번호}-command-spec.md
- projects/{current_project}/planning/test-cases/PLAN-{번호}-command.md

주요 커맨드: mycli init
플래그: --name, --template
출력: 프로젝트 초기화 완료 메시지

계속 진행하시겠습니까? (yes/no)
```

---

### Step 3-1: 커맨드 명세서 생성

**파일**: `specs/PLAN-{번호}-command-spec.md`

**템플릿 구조**:
```markdown
# {커맨드명} 명세서

## 커맨드
`mycli {command} [subcommand]`

## 설명
{커맨드가 하는 일을 2-3줄로}

## 플래그
| 플래그 | 단축 | 타입 | 필수 | 기본값 | 설명 |
|-------|------|------|------|--------|------|
| --name | -n | string | Y | - | 프로젝트 이름 |
| --template | -t | string | N | default | 템플릿 종류 (default, minimal, full) |
| --verbose | -v | boolean | N | false | 상세 로그 출력 |

## 인자
| 인자 | 타입 | 필수 | 설명 |
|------|------|------|------|
| path | string | N | 초기화할 경로 (기본값: 현재 디렉토리) |

## 출력 예시

### 성공 시
\`\`\`
✅ 프로젝트 'my-app'이 초기화되었습니다.
생성된 파일:
- my-app/config.yaml
- my-app/README.md
- my-app/src/main.go
\`\`\`

### 실패 시
\`\`\`
❌ 에러: 디렉토리 'my-app'이 이미 존재합니다.
   --force 플래그를 사용하여 덮어쓸 수 있습니다.
\`\`\`

## 에러 케이스
| 상황 | 에러 코드 | 메시지 | 표준 스트림 |
|------|----------|--------|-----------|
| 이미 존재하는 디렉토리 | 1 | 디렉토리가 이미 존재합니다. | stderr |
| 잘못된 템플릿 | 2 | 유효하지 않은 템플릿입니다. | stderr |
| 권한 없음 | 3 | 디렉토리 생성 권한이 없습니다. | stderr |
| 네트워크 오류 (템플릿 다운로드) | 4 | 템플릿을 다운로드할 수 없습니다. | stderr |

## 종료 코드
| 코드 | 의미 |
|------|------|
| 0 | 성공 |
| 1 | 파일/디렉토리 오류 |
| 2 | 유효성 검사 실패 |
| 3 | 권한 오류 |
| 4 | 네트워크 오류 |

## 환경 변수 (선택)
| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| MYCLI_TEMPLATE_REPO | 템플릿 저장소 URL | https://github.com/... |
| MYCLI_CONFIG_HOME | 설정 파일 경로 | ~/.mycli |

## 예시

### 기본 사용
\`\`\`bash
mycli init --name my-project
\`\`\`

### 템플릿 지정
\`\`\`bash
mycli init --name my-project --template minimal
\`\`\`

### 특정 경로에 생성
\`\`\`bash
mycli init --name my-project /path/to/workspace
\`\`\`

### 상세 로그
\`\`\`bash
mycli init --name my-project --verbose
\`\`\`
```

**⚠️ Gotcha 체크**:
- [ ] **Gotcha #10**: 구현 세부사항 (어떤 라이브러리 사용) 제외
- [ ] 모든 에러 케이스에 exit code 명시
- [ ] stdout vs stderr 구분 명확히

---

### Step 3-2: 테스트 케이스 생성

**파일**: `specs/test-cases/PLAN-{번호}-command.md`

**템플릿 구조**:
```markdown
# {커맨드명} 테스트 케이스

## 정상 케이스

| ID | 시나리오 | 커맨드 | 기대 출력 | Exit Code |
|----|---------|--------|----------|-----------|
| TC-CLI-001 | 기본 초기화 | `mycli init --name my-app` | "프로젝트 'my-app'이 초기화" | 0 |
| TC-CLI-002 | 템플릿 지정 | `mycli init --name my-app --template minimal` | minimal 템플릿 사용 메시지 | 0 |
| TC-CLI-003 | 상세 로그 | `mycli init --name my-app --verbose` | 각 단계별 로그 출력 | 0 |
| TC-CLI-004 | 특정 경로 | `mycli init --name my-app /tmp/test` | /tmp/test/my-app 생성 | 0 |

## 예외 케이스

| ID | 시나리오 | 커맨드 | 기대 출력 | Exit Code |
|----|---------|--------|----------|-----------|
| TC-CLI-101 | 이미 존재하는 디렉토리 | `mycli init --name existing` | "디렉토리가 이미 존재" | 1 |
| TC-CLI-102 | 잘못된 템플릿 | `mycli init --name my-app --template invalid` | "유효하지 않은 템플릿" | 2 |
| TC-CLI-103 | 필수 플래그 누락 | `mycli init` | "--name 플래그가 필요합니다" | 2 |
| TC-CLI-104 | 권한 없는 경로 | `mycli init --name my-app /root/forbidden` | "권한이 없습니다" | 3 |

## 플래그 조합 테스트

| ID | 시나리오 | 커맨드 | 기대 결과 |
|----|---------|--------|----------|
| TC-CLI-201 | 단축 플래그 | `mycli init -n my-app -t minimal` | 정상 동작 |
| TC-CLI-202 | 플래그 순서 무관 | `mycli init --template minimal --name my-app` | 정상 동작 |

## 출력 형식 테스트

| ID | 시나리오 | 체크 항목 |
|----|---------|----------|
| TC-CLI-301 | 성공 메시지 stdout | stdout에 "✅"로 시작하는 메시지 |
| TC-CLI-302 | 에러 메시지 stderr | stderr에 "❌"로 시작하는 메시지 |
| TC-CLI-303 | 파일 목록 출력 | 생성된 파일 목록이 stdout에 표시됨 |

## 상호작용 테스트 (해당 시)

| ID | 시나리오 | 입력 | 기대 동작 |
|----|---------|------|----------|
| TC-CLI-401 | 대화형 프롬프트 | `mycli init` (플래그 없이) | 프로젝트 이름 입력 요청 |
| TC-CLI-402 | Ctrl+C 중단 | 실행 중 Ctrl+C | 즉시 종료, 부분 생성 파일 정리 |

## 성능 테스트 (선택)

| ID | 시나리오 | 조건 | 기대 결과 |
|----|---------|------|----------|
| TC-CLI-501 | 대용량 템플릿 | 1000개 파일 템플릿 | 30초 이내 완료 |
| TC-CLI-502 | 네트워크 지연 | 느린 네트워크 | 타임아웃 메시지 표시 |
```

---

## 📝 로그 작성

**파일**: `projects/{current_project}/logs/pm/{YYYYMMDD-HHmmss}-PLAN-{번호}-{커맨드명}.md`

**필수 포함 내용**:
```markdown
# PM 로그: {커맨드명}

- **에이전트**: PM Agent
- **프로젝트**: {current_project}
- **프로젝트 타입**: cli-tool
- **티켓 번호**: PLAN-{번호}
- **일시**: {YYYY-MM-DD HH:mm:ss}
- **생성 파일**:
  - specs/PLAN-{번호}-command-spec.md
  - specs/test-cases/PLAN-{번호}-command.md

---

## 요청 해석
{티켓을 어떻게 해석했는지}

## 적용한 Gotchas
- ✅ Gotcha #1: 범위 확대 방지 - [구체적 내용]
- ✅ Gotcha #2: 올바른 디렉토리 - projects/{current_project}/planning/specs/
- ✅ Gotcha #10: 구현 세부사항 제외 - 커맨드 동작만 정의

## CLI 특수 고려사항
- stdout/stderr 구분 명확히
- Exit code 정의
- 환경 변수 (필요 시)
- 대화형 모드 (필요 시)

## 검수자 주의사항
{모호하여 임의로 결정한 내용}
```

---

## ✅ 완료 체크리스트

- [ ] 커맨드 명세서 생성 완료
- [ ] 모든 플래그/인자 문서화
- [ ] 출력 예시 (성공/실패) 포함
- [ ] 에러 케이스별 exit code 정의
- [ ] stdout/stderr 구분 명확
- [ ] 테스트 케이스 생성 완료
- [ ] 로그 파일 생성 완료
- [ ] "✅ PM Agent 작업 완료" 메시지 출력

---

## 🔍 CLI Tool 특수 체크 사항

### 플래그 네이밍 규칙
- 긴 플래그: `--kebab-case` (예: `--project-name`)
- 단축 플래그: `-x` 한 글자 (예: `-n`)
- Boolean 플래그: `--verbose` (값 없음)
- 값 받는 플래그: `--name <값>` 또는 `--name=<값>`

### 출력 포맷
- 성공: `✅`로 시작, stdout 출력
- 에러: `❌`로 시작, stderr 출력
- 경고: `⚠️`로 시작, stderr 출력
- 정보: `ℹ️`로 시작, stdout 출력

### Exit Code 컨벤션
- `0`: 성공
- `1`: 일반 에러
- `2`: 유효성 검사 실패
- `3-9`: 프로젝트별 정의
- `126`: 실행 권한 없음
- `127`: 커맨드 없음
- `130`: Ctrl+C로 중단

---

**관련 문서**:
- [gotchas.md](../gotchas.md) - 실패 패턴
- [CLAUDE.md](../CLAUDE.md) - 메인 에이전트 정의
