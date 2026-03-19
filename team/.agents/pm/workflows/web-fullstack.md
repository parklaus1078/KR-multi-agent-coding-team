# Web-Fullstack 워크플로우

> **프로젝트 타입**: web-fullstack (예: FastAPI + Next.js, Express + React, Django + Vue)
>
> **적용 조건**: `.project-meta.json`의 `project_type`이 `"web-fullstack"`인 경우

---

## 📂 산출물 구조

```
projects/{current_project}/planning/specs/
├── backend/
│   └── PLAN-{번호}-{slug}.md          # API 명세서
├── frontend/
│   ├── PLAN-{번호}-{slug}.md          # UI 요구사항
│   └── PLAN-{번호}-{slug}.html        # 와이어프레임
└── test-cases/
    ├── PLAN-{번호}-backend.md         # 백엔드 테스트 케이스
    └── PLAN-{번호}-frontend.md        # 프론트엔드 테스트 케이스
```

---

## 🔨 작업 순서

### Step 1: 티켓 분석

티켓에서 다음 항목을 추출:
- [ ] 기능명
- [ ] Acceptance Criteria
- [ ] API 엔드포인트 (명시 또는 추론)
- [ ] UI 화면 (명시 또는 추론)

**⚠️ Gotcha 체크**:
- Acceptance Criteria에 **없는** 기능은 Out-of-Scope로 분류
- 추론한 내용은 로그에 근거 기록

---

### Step 2: 산출물 목록 제시

사용자에게 생성할 파일 목록을 보여주고 승인받습니다.

**템플릿**:
```
프로젝트: {current_project} (web-fullstack)
티켓: PLAN-{번호}-{slug}

생성 예정 파일:
- projects/{current_project}/planning/specs/backend/PLAN-{번호}-{slug}.md
- projects/{current_project}/planning/specs/frontend/PLAN-{번호}-{slug}.md
- projects/{current_project}/planning/specs/frontend/PLAN-{번호}-{slug}.html
- projects/{current_project}/planning/specs/test-cases/PLAN-{번호}-backend.md
- projects/{current_project}/planning/specs/test-cases/PLAN-{번호}-frontend.md

주요 API: POST /auth/login, POST /auth/logout
주요 화면: 로그인 폼, 메인 페이지 (로그인 성공 후)
유저 플로우: 로그인 성공 → 메인 진입 / 실패 → 에러 메시지 표시

계속 진행하시겠습니까? (yes/no)
```

---

### Step 3-1: API 명세서 생성

**파일**: `specs/backend/PLAN-{번호}-{slug}.md`

**템플릿 구조**:
```markdown
# {기능명} API 명세서

## 엔드포인트 목록

### POST /auth/login
- **설명**: 이메일/비밀번호로 로그인
- **인증 필요**: No

**Request Body**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| email | string | Y | 이메일 |
| password | string | Y | 비밀번호 (8자 이상) |

**Response 200**
| 필드 | 타입 | 설명 |
|------|------|------|
| success | boolean | 성공 여부 |
| data.accessToken | string | JWT 액세스 토큰 |
| data.user.id | number | 유저 ID |
| data.user.email | string | 유저 이메일 |

**Response 401**
| 필드 | 타입 | 설명 |
|------|------|------|
| success | boolean | false |
| error.code | string | INVALID_CREDENTIALS |
| error.message | string | 이메일 또는 비밀번호가 올바르지 않습니다. |

**Response 400**
| 필드 | 타입 | 설명 |
|------|------|------|
| success | boolean | false |
| error.code | string | VALIDATION_ERROR |
| error.message | string | 이메일 형식이 올바르지 않습니다. |
```

**⚠️ Gotcha 체크**:
- [ ] **Gotcha #8**: 모든 엔드포인트에 에러 응답 (400, 401, 403, 404, 500) 포함
- [ ] **Gotcha #10**: 구현 세부사항 (라이브러리, 파일 위치) 제외
- [ ] **Gotcha #1**: Out-of-Scope 섹션에 제외 기능 명시

---

### Step 3-2: UI 요구사항 생성

**파일**: `specs/frontend/PLAN-{번호}-{slug}.md`

**템플릿 구조**:
```markdown
# {기능명} UI 요구사항

## 화면 목록
- 로그인 폼 (기본 상태)
- 로그인 폼 (에러 상태)
- 메인 페이지 (로그인 성공 후)

## 유저 플로우
1. 로그인 폼 진입
2. 이메일/비밀번호 입력 후 로그인 버튼 클릭
   - 성공: 메인 페이지로 이동
   - 실패: 에러 메시지 표시, 폼 유지

## 컴포넌트 구성

### 로그인 폼
- 이메일 Input
- 비밀번호 Input
- 로그인 Button (로딩 상태 포함)
- 에러 메시지 영역 (실패 시 표시)
- 회원가입 링크
- 비밀번호 찾기 링크

## 연결 API
- 로그인 버튼 클릭 → POST /auth/login

## 엣지 케이스
- 이메일 형식 오류 → 클라이언트 유효성 검사
- 비밀번호 8자 미만 → 클라이언트 유효성 검사
- API 호출 중 → 버튼 비활성화 + 로딩 표시
```

---

### Step 3-3: 와이어프레임 생성

**파일**: `specs/frontend/PLAN-{번호}-{slug}.html`

**HTML 유형 결정**:

| 상황 | HTML 유형 |
|------|----------|
| 단순 정보 표시, 레이아웃 확인만 필요 | 정적 HTML |
| 폼 제출 후 화면 전환 | 인터랙션 포함 |
| 성공/실패에 따라 다른 상태 표시 | 인터랙션 포함 |
| 모달, 토스트, 드로어 등 오버레이 | 인터랙션 포함 |
| 탭, 스텝, 위저드 등 단계 전환 | 인터랙션 포함 |

**HTML 작성 규칙**:
- ✅ 스타일 없이 구조만 표현 (인라인 style 최소화)
- ✅ 바닐라 JS만 사용 (외부 라이브러리 금지)
- ✅ 각 상태를 `id="state-{name}"` div로 구분
- ✅ 숨겨진 상태는 `style="display:none"`
- ✅ API 호출은 시뮬레이션 (실제 fetch 금지)
- ✅ 컴포넌트 역할을 주석으로 명시

**⚠️ Gotcha 체크**:
- [ ] **Gotcha #4**: Tailwind, React, Vue, Bootstrap 사용 금지
- [ ] **Gotcha #5**: fetch(), axios 등 실제 API 호출 금지

**인터랙션 포함 HTML 템플릿**:
```html
<!DOCTYPE html>
<html lang="ko">
<body>

  <!-- 상태 1: 로그인 폼 -->
  <div id="state-login">
    <h1>로그인</h1>
    <input id="email" type="email" placeholder="이메일" />
    <input id="password" type="password" placeholder="비밀번호" />
    <!-- 실패 시 표시되는 에러 메시지 -->
    <div id="error-message" style="display:none">
      이메일 또는 비밀번호가 올바르지 않습니다.
    </div>
    <button onclick="handleLogin()">로그인</button>
    <a href="/signup">회원가입</a>
  </div>

  <!-- 상태 2: 로그인 성공 후 메인 페이지 -->
  <div id="state-main" style="display:none">
    <h1>메인 페이지</h1>
    <p>환영합니다!</p>
  </div>

  <script>
    function handleLogin() {
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      // 성공 시나리오 (이메일/비밀번호 입력된 경우)
      if (email && password) {
        document.getElementById('state-login').style.display = 'none';
        document.getElementById('state-main').style.display = 'block';
        return;
      }

      // 실패 시나리오
      document.getElementById('error-message').style.display = 'block';
    }
  </script>

</body>
</html>
```

---

### Step 3-4: 테스트 케이스 생성

#### 백엔드 테스트 케이스

**파일**: `specs/test-cases/PLAN-{번호}-backend.md`

```markdown
# {기능명} BE 테스트 케이스

## POST /auth/login

### 정상 케이스
| ID | 시나리오 | 입력 | 기대 결과 |
|----|---------|------|---------|
| TC-BE-001 | 유효한 이메일/비밀번호로 로그인 | email: test@example.com, password: password123 | 200, accessToken 반환 |

### 예외 케이스
| ID | 시나리오 | 입력 | 기대 결과 |
|----|---------|------|---------|
| TC-BE-002 | 존재하지 않는 이메일 | email: wrong@example.com | 401, INVALID_CREDENTIALS |
| TC-BE-003 | 비밀번호 불일치 | password: wrongpass | 401, INVALID_CREDENTIALS |
| TC-BE-004 | 이메일 형식 오류 | email: notanemail | 400, VALIDATION_ERROR |
| TC-BE-005 | 비밀번호 8자 미만 | password: short | 400, VALIDATION_ERROR |
```

#### 프론트엔드 테스트 케이스

**파일**: `specs/test-cases/PLAN-{번호}-frontend.md`

```markdown
# {기능명} FE 테스트 케이스

## 로그인 폼

### 정상 케이스
| ID | 시나리오 | 액션 | 기대 결과 |
|----|---------|------|---------|
| TC-FE-001 | 로그인 성공 | 유효한 이메일/비밀번호 입력 후 로그인 클릭 | 메인 페이지로 이동 |

### 예외 케이스
| ID | 시나리오 | 액션 | 기대 결과 |
|----|---------|------|---------|
| TC-FE-002 | 로그인 실패 | 잘못된 비밀번호 입력 후 로그인 클릭 | 에러 메시지 표시, 폼 유지 |
| TC-FE-003 | 이메일 형식 오류 | 잘못된 형식 입력 후 클릭 | 클라이언트 유효성 오류 표시 |
| TC-FE-004 | 로딩 상태 | 로그인 버튼 클릭 직후 | 버튼 비활성화, 로딩 표시 |

### 접근성
| ID | 시나리오 | 기대 결과 |
|----|---------|----------|
| TC-FE-005 | 키보드 네비게이션 | Tab으로 모든 입력 요소 접근 가능 |
| TC-FE-006 | 에러 메시지 스크린 리더 | role=alert로 에러 메시지 읽힘 |
```

**⚠️ Gotcha 체크**:
- [ ] **Gotcha #9**: 접근성 테스트 케이스 포함

---

## 📝 로그 작성

**파일**: `projects/{current_project}/logs/pm/{YYYYMMDD-HHmmss}-PLAN-{번호}-{기능명}.md`

**필수 포함 내용**:
```markdown
# PM 로그: {기능명}

- **에이전트**: PM Agent
- **프로젝트**: {current_project}
- **프로젝트 타입**: web-fullstack
- **티켓 번호**: PLAN-{번호}
- **일시**: {YYYY-MM-DD HH:mm:ss}
- **생성 파일**:
  - specs/backend/PLAN-{번호}-{slug}.md
  - specs/frontend/PLAN-{번호}-{slug}.md
  - specs/frontend/PLAN-{번호}-{slug}.html
  - specs/test-cases/PLAN-{번호}-backend.md
  - specs/test-cases/PLAN-{번호}-frontend.md

---

## 요청 해석
{티켓 내용을 어떻게 해석했는지, 모호한 부분은 어떻게 판단했는지}

## 적용한 Gotchas
- ✅ Gotcha #1: 범위 확대 방지 - [구체적 내용]
- ✅ Gotcha #2: 올바른 디렉토리 - projects/{current_project}/planning/specs/
- ✅ Gotcha #4: HTML 외부 라이브러리 금지 - 바닐라 JS만 사용
- ✅ Gotcha #8: 에러 응답 문서화 - 모든 엔드포인트에 4xx/5xx 포함
- ✅ Gotcha #9: 접근성 테스트 - 키보드 네비게이션, 스크린 리더 포함

## HTML 유형 결정
{정적 HTML / 인터랙션 포함 HTML 선택 이유, 구현한 상태 목록}

## 프로젝트 타입별 결정
- 생성: backend API 명세, frontend UI 명세, 와이어프레임, 테스트 케이스
- 생략: 없음 (web-fullstack은 모든 산출물 필요)

## 검수자 주의사항
{모호하여 임의로 결정한 내용, 추가 확인 필요 항목}
```

---

## ✅ 완료 체크리스트

- [ ] 티켓 Acceptance Criteria와 대조 완료
- [ ] 5개 파일 모두 생성 (backend, frontend, html, test-cases x2)
- [ ] 모든 API 엔드포인트에 에러 응답 포함
- [ ] HTML에 외부 라이브러리 사용 안 함
- [ ] 접근성 테스트 케이스 포함
- [ ] Out-of-Scope 섹션 작성 완료
- [ ] 로그 파일 생성 완료
- [ ] "✅ PM Agent 작업 완료" 메시지 출력

---

**관련 문서**:
- [gotchas.md](../gotchas.md) - 실패 패턴
- [CLAUDE.md](../CLAUDE.md) - 메인 에이전트 정의
