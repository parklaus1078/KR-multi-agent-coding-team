# Phase 2.2 완료: Validation Hooks (validate-spec Skill) ✅

> **일시**: 2026-03-19
> **Phase**: 2.2 - 검증 Hooks
> **소요 시간**: ~30분
> **상태**: ✅ 완료

---

## 🎯 목표

**PM Agent 출력물을 Coding Agent로 전달하기 전에 자동 검증**
- 잘못된 명세서로 인한 코딩 실패 사전 차단
- API 호출 60%+ 절약

---

## 📦 생성된 파일 (4개)

| 파일 | 줄 수 | 설명 |
|------|-------|------|
| `team/.skills/validate-spec/skill.md` | 473줄 | 스킬 문서 (검증 항목, 사용법) |
| `team/.skills/validate-spec/rules.json` | 234줄 | 검증 규칙 설정 (프로젝트 타입별) |
| `team/.skills/validate-spec/validate.py` | 573줄 | 실제 검증 로직 (Python) |
| `team/scripts/run-skill.sh` | 32줄 | Skill 실행 wrapper |

**총**: 1,312줄

---

## 🔍 검증 항목 (5개 카테고리)

### 1. 완전성 검사 (Completeness)

**프로젝트 타입별 필수 파일 존재 여부**:
- Web-Fullstack: 5개 파일 (backend, frontend, html, 2 test-cases)
- CLI Tool: 2개 파일 (command-spec, test-cases)
- Desktop App: 6개 파일 (screens, state, 3 test-cases)
- Library: 4개 파일 (api, examples, 2 test-cases)

**필수 섹션 존재 여부**:
- Backend: "엔드포인트 목록", "Request Body", "Response 200"
- Frontend: "화면 목록", "유저 플로우", "컴포넌트 구성"
- CLI: "커맨드", "플래그", "종료 코드"

### 2. 범위 준수 검사 (Scope Compliance)

**Gotcha #1 적용 - 범위 확대 방지**:
- 티켓의 Acceptance Criteria 추출
- 명세서의 기능 목록 추출
- 범위 확대 의심 키워드 탐지:
  - OAuth, 소셜 로그인, 이메일 인증
  - 비밀번호 재설정, 2FA
  - 관리자, dashboard, analytics
- Out-of-Scope 섹션 확인

### 3. 품질 게이트 (Quality Gates)

**API 명세서**:
- [x] REST 규약 준수 (POST=생성, GET=조회, etc.)
- [x] 에러 응답 완비 (400, 401, 500 필수) - **Gotcha #8**

**HTML 와이어프레임**:
- [x] 외부 라이브러리 금지 (tailwind, react, vue 등) - **Gotcha #4**
- [x] 실제 API 호출 금지 (fetch, axios 등) - **Gotcha #5**

**접근성**:
- [x] 접근성 테스트 케이스 포함 - **Gotcha #9**

**CLI Tool**:
- [x] Exit Code 정의 필수

### 4. 구현 세부사항 침범 검사

**Gotcha #10 적용 - Coding Agent 역할 침범 방지**:

금지된 키워드 탐지:
- 라이브러리: bcrypt, jwt, axios, mongoose, prisma
- 파일 구조: src/, lib/, controllers/, services/
- DB 스키마: VARCHAR, INTEGER, PRIMARY KEY
- 디자인 패턴: Singleton, Factory, MVC

### 5. 자동 수정 (Auto-fix)

경미한 이슈 자동 수정:
- [x] Out-of-Scope 섹션 누락 시 자동 추가
- [x] 하드코딩 비밀번호 → 환경 변수 참조
- [x] HTTP → HTTPS 변환

---

## 🚀 사용법

### 수동 실행

```bash
# 특정 티켓 검증
bash team/scripts/run-skill.sh validate-spec PLAN-001

# 검증 + 자동 수정
bash team/scripts/run-skill.sh validate-spec PLAN-001 --auto-fix

# Python 직접 실행
cd projects/my-project
python3 ../../.skills/validate-spec/validate.py PLAN-001 --auto-fix
```

### Auto-pipeline 통합 (자동)

```python
# auto_pipeline.py에 통합됨

# PM Agent 실행 후
result = self.run_agent("pm", ticket_content, ticket_num)

# 자동으로 검증 실행
validation_result = self._run_validate_spec(ticket_num, auto_fix=True)

if not validation_result["passed"]:
    # PM Agent 재실행 (이슈 포함)
    retry_prompt = self._build_retry_prompt(ticket_content, validation_result)
    result = self.run_agent("pm", retry_prompt, ticket_num)

    # 재검증
    validation_retry = self._run_validate_spec(ticket_num, auto_fix=True)

    if not validation_retry["passed"]:
        raise Exception("수동 개입 필요")
```

---

## 📤 출력 예시

### 성공 시

```
============================================================
Spec Validation: PLAN-001
프로젝트 타입: web-fullstack
============================================================

1️⃣  완전성 검사...
   ✅ 5/5 파일 생성 완료

2️⃣  범위 준수 검사...
   ✅ 범위 확대 없음

3️⃣  품질 게이트...
   ✅ API 에러 응답 완비
   ✅ HTML 외부 라이브러리 없음
   ✅ HTML API 호출 없음 (목업만 사용)

4️⃣  구현 세부사항 침범 검사...
   ✅ 구현 세부사항 침범 없음

5️⃣  자동 수정 적용...
   (없음)

============================================================
✅ Spec Validation 통과: PLAN-001
============================================================

다음 조치:
Coding Agent 실행 가능

📝 로그 저장: projects/my-project/logs/validate-spec/20260319-153000-PLAN-001.md
```

### 실패 시

```
============================================================
❌ Spec Validation 실패: PLAN-001
============================================================

에러 (2개):
1. [완전성] 필수 파일 누락: specs/test-cases/PLAN-001-backend.md
2. [품질] API 에러 응답 누락: 401 (in PLAN-001-backend.md)

경고 (3개):
1. [범위] 'OAuth' 발견 (티켓에 없음) - PLAN-001-backend.md
2. [품질] 접근성 테스트 케이스 누락
3. [구현] 구현 세부사항 포함 의심: 'bcrypt' in PLAN-001-backend.md

자동 수정 (1개):
✓ Out-of-Scope 섹션 추가: PLAN-001-backend.md

다음 조치:
1. PM Agent 재실행하여 누락된 파일/섹션 생성
2. 에러 수정 후 재검증 필요
```

---

## 🧪 검증 로직 구현

### 핵심 클래스

```python
class SpecValidator:
    def __init__(self, project_root: Path, ticket_num: str):
        self.rules = self._load_rules()  # rules.json
        self.project_meta = self._load_project_meta()  # .project-meta.json
        self.project_type = self.project_meta.get("project_type")

    def validate(self, auto_fix: bool = False) -> ValidationResult:
        # 1. 완전성 검사
        self._check_completeness(result)

        # 2. 범위 준수 검사
        self._check_scope_compliance(result)

        # 3. 품질 게이트
        self._check_quality_gates(result)

        # 4. 구현 세부사항
        self._check_implementation_details(result)

        # 5. 자동 수정
        if auto_fix:
            self._apply_auto_fixes(result)

        return result
```

### 주요 메서드

**완전성 검사**:
```python
def _check_completeness(self, result):
    # 프로젝트 타입별 필수 파일 확인
    required_files = self.rules["project_type_requirements"][self.project_type]["required_files"]

    for file_pattern in required_files:
        # {number}, {slug} 치환
        file_path = file_pattern.replace("{number}", ticket_num)
        if not file_path.exists():
            result.errors.append(f"필수 파일 누락: {file_path}")

        # 섹션 검사
        self._check_file_sections(file_path, result)
```

**범위 준수 검사**:
```python
def _check_scope_compliance(self, result):
    # 티켓 Acceptance Criteria 추출
    ticket_features = self._extract_acceptance_criteria(ticket_content)

    # 범위 확대 키워드 탐지
    scope_keywords = self.rules["scope_creep_keywords"]
    for keyword in scope_keywords:
        if keyword in spec_content and keyword not in ticket_content:
            # Out-of-Scope 섹션 확인
            if not has_out_of_scope_section(spec_file):
                result.errors.append(f"범위 확대 + Out-of-Scope 누락: {keyword}")
            else:
                result.warnings.append(f"범위 확대 의심: {keyword}")
```

**품질 게이트**:
```python
def _check_error_responses(self, result):
    # API 에러 응답 (Gotcha #8)
    required_codes = ["400", "401", "500"]
    for code in required_codes:
        pattern = rf"(Response|응답|에러|Error)\s*{code}"
        if not re.search(pattern, content, re.IGNORECASE):
            result.errors.append(f"API 에러 응답 누락: {code}")

def _check_html_libraries(self, result):
    # HTML 외부 라이브러리 (Gotcha #4)
    forbidden = ["tailwind", "react", "vue", "bootstrap", "cdn"]
    for pattern in forbidden:
        if re.search(pattern, html_content, re.IGNORECASE):
            result.errors.append(f"HTML 외부 라이브러리 사용: {pattern}")
```

---

## 📊 기대 효과

### Before (검증 없음)

```
PM Agent → Coding Agent
         ↓ (잘못된 명세서)
       실패 → 재작업 → PM Agent 재실행 → Coding Agent 재실행

API 호출: 5-10회
```

### After (검증 적용)

```
PM Agent → Validate-Spec → 통과 → Coding Agent
           ↓ (실패)
         재실행 (이슈 포함)
           ↓
         통과 → Coding Agent

API 호출: 2-3회
절감: 60-70%
```

### 수치 목표

| 항목 | 목표 |
|------|------|
| **에러 사전 포착률** | **80%+** |
| **API 호출 절감** | **60%+** |
| **범위 확대 방지** | **90%+** |
| **품질 게이트 통과율** | **95%+** |

---

## 🔗 Gotchas 연결

| Gotcha | 검증 항목 | 탐지 방법 |
|--------|---------|---------|
| #1 범위 확대 | 범위 준수 검사 | 키워드 매칭 + Out-of-Scope 확인 |
| #4 HTML 라이브러리 | 품질 게이트 | Regex 패턴 매칭 |
| #5 API 호출 | 품질 게이트 | fetch/axios 탐지 |
| #8 에러 응답 누락 | 품질 게이트 | 필수 HTTP 코드 확인 |
| #9 접근성 누락 | 품질 게이트 | 키워드 매칭 |
| #10 역할 침범 | 구현 세부사항 | 구현 키워드 탐지 |

---

## 📝 로그 시스템

**로그 경로**: `projects/{project}/logs/validate-spec/{timestamp}-{ticket_num}.md`

**로그 내용**:
- 검증 결과 요약 (통과/실패)
- 각 카테고리별 상세 결과
- 발견된 에러/경고 목록
- 적용된 자동 수정 목록
- 다음 조치 권장사항

**활용**:
- 실패 패턴 분석
- 주간 리포트 (가장 많이 발견된 이슈)
- Phase 2.4 (Gotcha Auto-Discovery)의 데이터 소스

---

## 🔧 설정 커스터마이징

`rules.json`에서 검증 규칙 조정 가능:

```json
{
  "rules": {
    "completeness": {
      "enabled": true,
      "severity": "error"
    },
    "scope_compliance": {
      "enabled": true,
      "severity": "error",
      "strict_mode": false,
      "scope_creep_keywords": [
        "OAuth", "소셜 로그인", "관리자"
      ]
    },
    "quality_gates": {
      "error_responses": {
        "enabled": true,
        "required_codes": ["400", "401", "500"]
      },
      "html_libraries": {
        "enabled": true,
        "forbidden_patterns": ["tailwind", "react"]
      }
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

## 💡 핵심 인사이트

### 예상 못한 이점

1. **조기 피드백**: Coding Agent 실행 전 문제 발견 → 빠른 수정 사이클
2. **학습 데이터**: 검증 로그 → Phase 2.4 자동 Gotcha 발견에 활용
3. **자동 수정**: 간단한 이슈는 자동 해결 → 수동 개입 최소화
4. **일관성**: 모든 명세서가 동일한 품질 기준 통과

### 개선 포인트

1. **다른 에이전트로 확장**:
   - Coding Agent 출력물 검증 (코딩 룰 준수 확인)
   - QA Agent 출력물 검증 (테스트 커버리지 확인)

2. **신뢰도 점수**:
   - 검증 규칙별 성공률 추적
   - 낮은 성공률 규칙 → 튜닝 필요

3. **CI/CD 통합**:
   - PR 생성 전 자동 검증
   - 검증 실패 시 PR block

---

## 🎯 Thariq 교훈 적용

| Thariq 교훈 | 적용 방법 |
|------------|----------|
| **"Validation skills catch 80%+ errors"** | validate-spec 스킬 구현 ✅ |
| **"Hooks before expensive operations"** | PM → Coding 사이에 검증 ✅ |
| **"Scripts & Code over instructions"** | Python 스크립트로 자동화 ✅ |
| **"Memory & Data"** | rules.json으로 설정 관리 ✅ |
| **"Gotchas are highest-signal"** | Gotchas 6개 연결 ✅ |

---

## 🚀 다음 단계

### 즉시 테스트 가능

```bash
# 테스트용 티켓 생성
cd team
bash scripts/run-agent.sh pm --ticket-file projects/test-project/planning/tickets/PLAN-001-test.md

# 검증 실행
bash scripts/run-skill.sh validate-spec PLAN-001 --auto-fix

# Auto-pipeline 통합 테스트
python3 scripts/auto_pipeline.py --project projects/test-project
```

### Phase 2 나머지 항목

**Phase 2.1 - 구조화된 의사결정 로그** (우선순위: 높음)
- 에이전트 로그에 의사결정 + 근거 + 신뢰도 기록
- 향후 학습의 기반

**Phase 2.3 - 메모리 시스템** (우선순위: 중간)
- `patterns.json`: 성공 패턴 저장
- `failures.json`: 실패 패턴 저장
- 반복 실수 학습

**Phase 2.4 - Gotcha Auto-Discovery** (우선순위: 중간)
- 검증 로그 분석
- 새로운 Gotcha 자동 발견
- 주간 리포트

---

## 📈 Phase 2.2 성과

### 생성된 자산

| 카테고리 | 파일 수 | 줄 수 |
|---------|--------|------|
| **문서** | 1개 | 473줄 |
| **설정** | 1개 | 234줄 |
| **스크립트** | 2개 | 605줄 |
| **통합** | auto_pipeline.py 수정 | +70줄 |
| **합계** | 4개 | 1,382줄 |

### 개선 메트릭

| 항목 | 달성 |
|------|------|
| **검증 카테고리** | **5개** (완전성, 범위, 품질, 구현, 자동수정) |
| **Gotcha 연결** | **6개** (#1, #4, #5, #8, #9, #10) |
| **프로젝트 타입 지원** | **4개** (web-fullstack, cli-tool, desktop-app, library) |
| **Auto-fix 규칙** | **3개** (Out-of-Scope, 비밀번호, HTTP) |
| **로그 시스템** | **✅** (검증 결과 저장) |
| **Auto-pipeline 통합** | **✅** (PM Agent 후 자동 검증) |

---

## 🎉 Phase 2.2 완료!

**달성**:
- ✅ 검증 스킬 **5개 카테고리** 구현
- ✅ Gotcha 연결 **6개**
- ✅ Auto-fix **3개 규칙**
- ✅ Auto-pipeline 통합
- ✅ 로그 시스템
- ✅ 프로젝트 타입별 규칙 **4개**

**기대 효과**:
- 에러 사전 포착 **80%+**
- API 호출 절감 **60%+**
- 범위 확대 방지 **90%+**

**다음**: Phase 2.1, 2.3, 또는 2.4?

---

## 📝 변경 이력

### 2026-03-19
- ✅ `team/.skills/validate-spec/skill.md` 생성
- ✅ `team/.skills/validate-spec/rules.json` 생성
- ✅ `team/.skills/validate-spec/validate.py` 생성
- ✅ `team/scripts/run-skill.sh` 생성
- ✅ `team/scripts/auto_pipeline.py` 수정 (검증 통합)
