# Spec Validation Skill

> **목적**: PM Agent가 생성한 명세서를 Coding Agent로 전달하기 전에 자동 검증
>
> **효과**: 잘못된 명세서로 인한 코딩 실패를 사전 차단 → API 호출 절약
>
> **Thariq 교훈**: "Validation skills can catch 80%+ spec errors before coding"

---

## 🎯 트리거

### 자동 트리거
- Auto-pipeline: PM Agent 완료 직후
- Manual: `bash scripts/run-skill.sh validate-spec PLAN-001`

### 입력
- 티켓 번호 (예: `PLAN-001`)
- 프로젝트 경로 (`.project-config.json`에서 자동 감지)

---

## ✅ 검증 항목

### 1. 완전성 검사 (Completeness)

#### 필수 파일 존재 여부
프로젝트 타입별로 필요한 파일이 모두 생성되었는지 확인:

**Web-Fullstack**:
- [ ] `specs/backend/PLAN-{번호}-{slug}.md`
- [ ] `specs/frontend/PLAN-{번호}-{slug}.md`
- [ ] `specs/frontend/PLAN-{번호}-{slug}.html`
- [ ] `specs/test-cases/PLAN-{번호}-backend.md`
- [ ] `specs/test-cases/PLAN-{번호}-frontend.md`

**CLI Tool**:
- [ ] `specs/PLAN-{번호}-command-spec.md`
- [ ] `specs/test-cases/PLAN-{번호}-command.md`

**Desktop App**:
- [ ] `specs/screens/PLAN-{번호}-{slug}.md`
- [ ] `specs/screens/PLAN-{번호}-{slug}.html`
- [ ] `specs/state/PLAN-{번호}-{slug}.md`
- [ ] `specs/test-cases/PLAN-{번호}-unit.md`
- [ ] `specs/test-cases/PLAN-{번호}-integration.md`
- [ ] `specs/test-cases/PLAN-{번호}-e2e.md`

**Library**:
- [ ] `specs/api/PLAN-{번호}-{slug}.md`
- [ ] `specs/examples/PLAN-{번호}-{slug}.md`
- [ ] `specs/test-cases/PLAN-{번호}-api.md`
- [ ] `specs/test-cases/PLAN-{번호}-examples.md`

#### API 명세서 필수 섹션
- [ ] "엔드포인트 목록" 섹션 존재
- [ ] 각 엔드포인트에 Request Body 정의
- [ ] 각 엔드포인트에 Response 200 정의
- [ ] 각 엔드포인트에 에러 응답 (4xx/5xx) 정의

#### 테스트 케이스 필수 섹션
- [ ] "정상 케이스" 섹션 존재
- [ ] "예외 케이스" 섹션 존재
- [ ] 각 케이스에 ID 부여 (TC-XXX-001 형식)

---

### 2. 범위 준수 검사 (Scope Compliance)

**Gotcha #1: 범위 확대 방지**

티켓의 Acceptance Criteria와 명세서 내용을 비교:

1. **티켓 읽기**: `planning/tickets/PLAN-{번호}-*.md`
2. **Acceptance Criteria 추출**
3. **명세서의 기능 목록 추출**
4. **Out-of-Scope 섹션 확인**

**검증 로직**:
```python
# 티켓에 없는 기능이 명세서에 있는지 체크
spec_features = extract_features_from_spec(spec_file)
ticket_features = extract_acceptance_criteria(ticket_file)

extra_features = spec_features - ticket_features

if extra_features:
    if not has_out_of_scope_section(spec_file):
        ERROR: "티켓에 없는 기능이 명세서에 있습니다: {extra_features}"
        ERROR: "Out-of-Scope 섹션이 누락되었습니다."
    else:
        # Out-of-Scope 섹션에 명시되어 있는지 확인
        out_of_scope = extract_out_of_scope(spec_file)
        if extra_features not in out_of_scope:
            WARNING: "추가 기능이 Out-of-Scope에 명시되지 않았습니다: {extra_features}"
```

**키워드 기반 검사**:
```python
# 범위 확대 의심 키워드
scope_creep_keywords = [
    "OAuth", "소셜 로그인", "이메일 인증",
    "비밀번호 재설정", "2단계 인증",
    "관리자", "admin", "dashboard",
    "통계", "analytics", "리포트"
]

# 명세서에 있지만 티켓에 없는 키워드 발견 시 경고
for keyword in scope_creep_keywords:
    if keyword in spec_content and keyword not in ticket_content:
        WARNING: f"범위 확대 의심: '{keyword}'가 티켓에 없지만 명세서에 있습니다."
```

---

### 3. 품질 게이트 (Quality Gates)

#### API 명세서 품질
- [ ] **REST 규약 준수**:
  - POST = 생성
  - GET = 조회
  - PUT/PATCH = 수정
  - DELETE = 삭제
- [ ] **엔드포인트 명명**: `/api/{resource}` 형식
- [ ] **에러 코드 일관성**: INVALID_CREDENTIALS, VALIDATION_ERROR 등
- [ ] **필수 에러 응답**:
  - [ ] 400 (잘못된 요청)
  - [ ] 401 (인증 실패, 인증 필요 시)
  - [ ] 404 (리소스 없음, 필요 시)
  - [ ] 500 (서버 에러)

#### HTML 와이어프레임 품질
**Gotcha #4, #5 적용**

- [ ] **외부 라이브러리 사용 금지**:
  ```bash
  grep -E "tailwind|react|vue|bootstrap|cdn|jsdelivr|unpkg" wireframe.html
  # → 발견 시 ERROR
  ```
- [ ] **실제 API 호출 금지**:
  ```bash
  grep -E "fetch\(|axios\.|XMLHttpRequest|\.get\(|\.post\(" wireframe.html
  # → 발견 시 ERROR
  ```
- [ ] **바닐라 JS 확인**:
  ```bash
  grep -E "import.*from|require\(" wireframe.html
  # → 발견 시 ERROR
  ```

#### 테스트 케이스 품질
**Web-Fullstack/Desktop App**:
- [ ] **접근성 테스트 포함** (Gotcha #9):
  ```bash
  grep -i "접근성\|accessibility\|키보드\|스크린 리더" test-cases/PLAN-*-frontend.md
  # → 없으면 WARNING
  ```

**CLI Tool**:
- [ ] **Exit Code 정의**:
  ```bash
  grep -i "exit code\|종료 코드" specs/PLAN-*-command-spec.md
  # → 없으면 ERROR
  ```

---

### 4. 구현 세부사항 침범 검사

**Gotcha #10: Coding Agent 역할 침범 방지**

명세서에 구현 세부사항이 포함되어 있는지 검사:

**금지된 키워드**:
```python
implementation_keywords = [
    # 라이브러리/패키지
    "bcrypt", "jwt", "jose", "passport",
    "axios", "fetch", "request",
    "mongoose", "sequelize", "typeorm",

    # 파일/디렉토리 구조
    "src/", "lib/", "utils/", "helpers/",
    "controllers/", "services/", "models/",

    # 데이터베이스 세부사항
    "VARCHAR", "INTEGER", "TIMESTAMP",
    "PRIMARY KEY", "FOREIGN KEY", "INDEX",

    # 디자인 패턴
    "Singleton", "Factory", "Observer",
    "Repository Pattern", "MVC",
]

for keyword in implementation_keywords:
    if keyword in spec_content:
        WARNING: f"구현 세부사항 포함 의심: '{keyword}'"
        WARNING: f"PM Agent는 '무엇을'만 정의, '어떻게'는 Coding Agent가 결정"
```

---

### 5. 자동 수정 (Auto-fix)

경미한 이슈는 자동으로 수정:

#### 수정 가능한 이슈

**1. 하드코딩된 비밀번호 → 환경 변수 참조**
```python
# Before
"password": "admin123"

# After
"password": "${ADMIN_PASSWORD}"
```

**2. HTTP → HTTPS**
```python
# Before
"url": "http://api.example.com"

# After
"url": "https://api.example.com"
```

**3. 누락된 Out-of-Scope 섹션 추가**
```markdown
## Out of Scope
(자동 생성: 명세서 검토 후 수동 작성 필요)
```

---

## 📤 출력

### 성공 시
```
✅ Spec Validation 통과: PLAN-001

검증 결과:
- 완전성: ✅ 5/5 파일 생성
- 범위 준수: ✅ 범위 확대 없음
- 품질 게이트: ✅ 모든 규칙 통과
- 구현 세부사항: ✅ 침범 없음

다음 단계: Coding Agent 실행 가능
```

### 실패 시
```
❌ Spec Validation 실패: PLAN-001

에러 (2개):
1. [완전성] specs/test-cases/PLAN-001-backend.md 파일 누락
2. [품질] API 명세서에 401 에러 응답 누락 (POST /auth/login)

경고 (3개):
1. [범위] 'OAuth'가 티켓에 없지만 명세서에 있습니다 → 범위 확대 의심
2. [품질] 접근성 테스트 케이스 누락
3. [구현] 'bcrypt' 키워드 발견 → 구현 세부사항 제거 필요

자동 수정 (1개):
✓ Out-of-Scope 섹션 추가

권장 조치:
1. PM Agent 재실행하여 누락된 파일 생성
2. API 명세서에 401 응답 추가
3. 범위 확대된 기능을 Out-of-Scope로 이동

다음 단계: 수정 후 재검증 필요
```

---

## 🔧 사용법

### Auto-pipeline 통합

```python
# auto_pipeline.py의 PM Agent 실행 후
result_pm = self.run_agent("pm", ticket_content, ticket_num)

# 검증 Skill 실행
validation = self.run_skill("validate-spec", ticket_num)

if not validation["passed"]:
    print(f"\n⚠️  명세서 검증 실패:")
    print(f"  에러: {validation['errors']}")
    print(f"  경고: {validation['warnings']}")

    # 자동 수정 적용
    if validation.get("auto_fixes"):
        print(f"\n✓ 자동 수정 적용: {len(validation['auto_fixes'])}개")

    # PM Agent 재실행 (이슈와 함께)
    retry_prompt = f"""
이전 명세서에 다음 이슈가 발견되었습니다:

{format_issues(validation['errors'], validation['warnings'])}

위 이슈를 수정하여 명세서를 재생성해주세요.
"""
    result_pm_retry = self.run_agent("pm", retry_prompt, ticket_num)

    # 재검증
    validation_retry = self.run_skill("validate-spec", ticket_num)

    if not validation_retry["passed"]:
        print("❌ 재검증 실패 - 수동 개입 필요")
        return False

print("✅ 명세서 검증 통과 - Coding Agent 진행")
```

### 수동 실행

```bash
# 특정 티켓 검증
bash scripts/run-skill.sh validate-spec PLAN-001

# 모든 티켓 검증
bash scripts/run-skill.sh validate-spec --all

# 검증 + 자동 수정
bash scripts/run-skill.sh validate-spec PLAN-001 --auto-fix
```

---

## 📊 검증 규칙 설정

`rules.json` 파일로 검증 규칙을 커스터마이징:

```json
{
  "version": "0.0.1",
  "rules": {
    "completeness": {
      "enabled": true,
      "severity": "error",
      "check_files": true,
      "check_sections": true
    },
    "scope_compliance": {
      "enabled": true,
      "severity": "error",
      "strict_mode": false,
      "allow_out_of_scope": true
    },
    "quality_gates": {
      "rest_conventions": {
        "enabled": true,
        "severity": "warning"
      },
      "error_responses": {
        "enabled": true,
        "severity": "error",
        "required": ["400", "401", "500"]
      },
      "html_libraries": {
        "enabled": true,
        "severity": "error",
        "forbidden": ["tailwind", "react", "vue", "bootstrap"]
      },
      "accessibility": {
        "enabled": true,
        "severity": "warning"
      }
    },
    "implementation_details": {
      "enabled": true,
      "severity": "warning",
      "forbidden_keywords": ["bcrypt", "jwt", "src/", "VARCHAR"]
    }
  },
  "auto_fix": {
    "enabled": true,
    "rules": [
      "add_out_of_scope_section",
      "replace_hardcoded_secrets",
      "http_to_https"
    ]
  }
}
```

---

## 🎯 기대 효과

### Before (검증 없음)
```
PM Agent → Coding Agent
         ↓ (잘못된 명세서)
       실패 → 재작업 → PM Agent 재실행

API 호출: 5-10회 (실패 + 재작업)
```

### After (검증 적용)
```
PM Agent → Validate-Spec → 통과 → Coding Agent
           ↓ (실패)
         재실행 (이슈 포함)
           ↓
         통과 → Coding Agent

API 호출: 2-3회 (초기 + 수정)
절감: 60-70%
```

### 수치 목표
- **에러 사전 포착률**: 80%+
- **API 호출 절감**: 60%+
- **범위 확대 방지**: 90%+
- **품질 게이트 통과율**: 95%+

---

## 📝 로그

검증 결과를 로그로 저장:

**파일**: `projects/{project}/logs/validate-spec/{YYYYMMDD-HHmmss}-PLAN-{번호}.md`

```markdown
# Spec Validation Log: PLAN-001

- **Skill**: validate-spec
- **프로젝트**: my-todo-app
- **티켓**: PLAN-001
- **일시**: 2026-03-19 15:30:00
- **결과**: ✅ 통과 / ❌ 실패

---

## 검증 결과

### 완전성
- ✅ 5/5 파일 생성 완료

### 범위 준수
- ⚠️  'OAuth' 발견 (티켓에 없음)
- ✅ Out-of-Scope에 명시됨

### 품질 게이트
- ✅ REST 규약 준수
- ✅ 에러 응답 완비
- ✅ HTML 외부 라이브러리 없음

### 구현 세부사항
- ✅ 침범 없음

---

## 이슈 상세

없음

---

## 다음 조치

Coding Agent 실행 가능
```

---

**관련 문서**:
- [../gotchas.md](../../.agents/pm/gotchas.md) - PM Agent 실패 패턴
- [rules.json](rules.json) - 검증 규칙 설정
