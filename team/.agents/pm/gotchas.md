# PM Agent Gotchas

> **목적**: PM Agent가 반복적으로 실패했던 패턴들을 기록하여 같은 실수를 방지합니다.
>
> **업데이트**: 새로운 실패 패턴 발견 시 즉시 추가합니다.
>
> **Thariq의 조언**: "The highest-signal content in any skill is the Gotchas section"

---

## 1. 범위 확대 (Scope Creep)

### 증상
티켓에 명시되지 않은 기능을 명세서에 포함

### 실제 실패 사례
- **티켓**: "유저 로그인/로그아웃 구현"
- **PM이 생성한 명세**: 로그인, 로그아웃 + **OAuth 연동** + **비밀번호 재설정** + **이메일 인증**
- **문제**: 티켓 범위의 3배로 확대 → Coding Agent가 불필요한 코드 작성 → API 호출 낭비

### 근본 원인
1. "auth"라는 단어를 보고 "완전한 인증 시스템"으로 해석
2. Acceptance Criteria를 체크하지 않고 업계 베스트 프랙티스 적용
3. "사용자가 원할 것 같다"는 추측으로 기능 추가

### 탐지 방법
```
1. 명세서 생성 후 자가 점검:
   - 명세서의 각 기능을 티켓 Acceptance Criteria와 대조
   - 티켓에 명시되지 않은 항목이 있는가?

2. 키워드 체크:
   - "또한", "추가로", "더 나아가" → 범위 확대 징후
   - "일반적으로", "보통" → 추측 기반 결정 징후
```

### 올바른 접근
1. ✅ **티켓 Acceptance Criteria가 진리**
2. ✅ 명시된 항목만 In Scope
3. ✅ 고려했지만 제외한 기능은 **Out of Scope 섹션에 명시적 기록**
   ```markdown
   ## Out of Scope
   - OAuth 연동 (티켓에 명시 안 됨)
   - 비밀번호 재설정 (티켓에 명시 안 됨)
   - 이메일 인증 (티켓에 명시 안 됨)
   ```
4. ✅ 정말 필요하다고 판단되면 로그에 근거 작성, 명세서에는 **절대 포함하지 않음**

### 관련 자동화 모드 규칙
```
"A-1, A-2 기능도 추가할까요?" → NO (티켓 범위 확대 방지)
```

---

## 2. 잘못된 프로젝트 디렉토리

### 증상
`team/.agents/pm/` 또는 `team/.rules/`에 명세서 파일 생성

### 실제 실패 사례
- **의도**: `projects/my-todo-app/planning/specs/backend/PLAN-001-auth.md` 생성
- **실제**: `team/.agents/pm/specs/backend/PLAN-001-auth.md` 생성
- **문제**: 프로젝트 코드와 분리됨, Git 커밋 누락, 다른 에이전트가 파일 못 찾음

### 근본 원인
1. `.project-config.json` 읽기 생략
2. 상대 경로 혼동 (현재 위치가 `team/` 디렉토리라고 착각)
3. 템플릿 경로를 참고하다가 실수로 같은 위치에 생성

### 탐지 방법
```bash
# 생성 전 자가 점검
echo $FILE_PATH | grep -E "team/\.agents|team/\.rules"

# 정상 경로 패턴:
✅ projects/{current_project}/planning/specs/...
✅ projects/my-todo-app/planning/specs/backend/PLAN-001-auth.md

# 비정상 경로 패턴:
❌ team/.agents/pm/specs/...
❌ team/.rules/...
❌ .agents/...
```

### 올바른 접근
```markdown
## Step 0 (절대 생략 불가)
1. .project-config.json 읽기
2. current_project 추출
3. 모든 경로 앞에 projects/{current_project}/ 붙이기

예시:
current_project = "my-todo-app"
→ projects/my-todo-app/planning/specs/backend/PLAN-001-auth.md
```

### 자가 점검 질문
```
Q: 지금 만들려는 파일 경로가 projects/로 시작하는가?
   → NO면 즉시 중단, .project-config.json 다시 읽기

Q: 경로에 .agents/ 또는 .rules/가 포함되어 있는가?
   → YES면 100% 잘못된 경로
```

---

## 3. 프로젝트 타입 무시

### 증상
Web-Fullstack 프로젝트인데 CLI Tool 명세서 생성

### 실제 실패 사례
- **프로젝트 타입**: `web-fullstack` (FastAPI + Next.js)
- **PM이 생성한 파일**: `PLAN-001-command-spec.md` (CLI 명세서)
- **문제**: Coding Agent가 웹 서버 대신 CLI 커맨드 구현 시도

### 근본 원인
1. `.project-meta.json` 읽지 않음
2. 티켓 내용만 보고 프로젝트 타입 추측
3. 이전 프로젝트의 템플릿 재사용

### 탐지 방법
```bash
# Step 0에서 필수 체크
cat projects/{current_project}/.project-meta.json
# → project_type 확인

# 타입별 생성 파일 매핑:
web-fullstack → specs/backend/, specs/frontend/
cli-tool      → specs/PLAN-XXX-command-spec.md
desktop-app   → specs/screens/, specs/state/, specs/ipc/
```

### 올바른 접근
```markdown
1. .project-meta.json 읽기 → project_type 추출
2. project_type에 맞는 산출물 템플릿 선택
3. 해당 타입의 디렉토리 구조 준수
```

---

## 4. HTML 와이어프레임에 외부 라이브러리

### 증상
와이어프레임 HTML에 Tailwind, React, Vue 사용

### 실제 실패 사례
```html
<!-- ❌ 잘못된 예시 -->
<script src="https://cdn.tailwindcss.com"></script>
<div class="flex justify-center items-center bg-blue-500">
  ...
</div>
```

### 근본 원인
1. 프로덕션 코드를 작성하는 것으로 착각
2. "깔끔한 디자인"을 보여주려는 과잉 친절
3. Coding Agent의 역할 침범

### 탐지 방법
```bash
# 생성 후 자가 점검
grep -E "tailwind|react|vue|bootstrap|cdn|import.*from" wireframe.html

# 발견되면 즉시 제거
```

### 올바른 접근
```html
<!-- ✅ 올바른 예시 -->
<!DOCTYPE html>
<html lang="ko">
<body>
  <!-- 상태 1: 로그인 폼 -->
  <div id="state-login">
    <h1>로그인</h1>
    <input id="email" type="email" placeholder="이메일" />
    <input id="password" type="password" placeholder="비밀번호" />
    <div id="error-message" style="display:none">
      이메일 또는 비밀번호가 올바르지 않습니다.
    </div>
    <button onclick="handleLogin()">로그인</button>
  </div>

  <!-- 상태 2: 로그인 성공 -->
  <div id="state-main" style="display:none">
    <h1>메인 페이지</h1>
  </div>

  <script>
    // 바닐라 JS만 사용
    function handleLogin() {
      const email = document.getElementById('email').value;
      if (email && document.getElementById('password').value) {
        document.getElementById('state-login').style.display = 'none';
        document.getElementById('state-main').style.display = 'block';
      } else {
        document.getElementById('error-message').style.display = 'block';
      }
    }
  </script>
</body>
</html>
```

### 핵심 원칙
- **스타일 없이 구조만** (인라인 style 최소화)
- **바닐라 JS만** (외부 라이브러리 금지)
- **각 상태를 div로 구분** (`id="state-{name}"`)
- **API 호출은 시뮬레이션** (실제 fetch 금지)

---

## 5. 실제 API 호출 시뮬레이션 누락

### 증상
와이어프레임에 `fetch()`, `axios` 등 실제 API 호출 코드

### 실제 실패 사례
```javascript
// ❌ 잘못된 예시
async function handleLogin() {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  // ...
}
```

### 근본 원인
1. 와이어프레임을 "프로토타입"으로 착각
2. Coding Agent가 구현할 코드를 미리 작성

### 올바른 접근
```javascript
// ✅ 올바른 예시
function handleLogin() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  // 성공 시나리오 시뮬레이션 (실제 API 호출 없음)
  if (email && password) {
    // 성공 → 다음 상태로 전환
    document.getElementById('state-login').style.display = 'none';
    document.getElementById('state-main').style.display = 'block';
    return;
  }

  // 실패 시나리오
  document.getElementById('error-message').style.display = 'block';
}
```

---

## 6. 사용자 승인 없이 파일 생성

### 증상
산출물 목록을 보여주지 않고 바로 파일 생성 시작

### 근본 원인
1. "자동화 모드"를 "승인 생략 모드"로 착각
2. 빠른 처리를 위해 프로세스 단계 생략

### 올바른 접근
```markdown
## Step 2: 산출물 목록 제시 및 승인 (절대 생략 불가)

생성 예정 파일:
- projects/my-todo-app/planning/specs/backend/PLAN-001-user-auth.md
- projects/my-todo-app/planning/specs/frontend/PLAN-001-user-auth.md
- projects/my-todo-app/planning/specs/frontend/PLAN-001-user-auth.html
- projects/my-todo-app/planning/test-cases/PLAN-001-backend.md
- projects/my-todo-app/planning/test-cases/PLAN-001-frontend.md

주요 API: POST /auth/login, POST /auth/logout
주요 화면: 로그인 폼, 메인 페이지

계속 진행하시겠습니까? (yes/no)
```

### 자동화 모드에서도 예외 없음
자동화 모드(`auto-pipeline.py`)에서도 이 단계는 **반드시** 수행해야 합니다.
단, 자동 응답 규칙에 의해 "yes"로 자동 처리될 뿐입니다.

---

## 7. 로그 작성 생략

### 증상
작업 완료 후 로그 파일 미작성

### 문제점
- 의사결정 근거 사라짐
- 다음 프로젝트에서 학습 불가
- 검수자가 "왜 이렇게 만들었는지" 파악 못 함

### 올바른 접근
```markdown
## Step 4: 로그 작성 (필수, 완료 직후)

파일 위치: projects/{current_project}/logs/pm/{YYYYMMDD-HHmmss}-{티켓번호}-{기능명}.md

반드시 포함:
- 생성한 모든 파일 목록
- 요청 해석 (모호한 부분을 어떻게 판단했는지)
- 프로젝트 타입별 결정 (어떤 산출물을 생성/생략했는지, 이유)
- HTML 유형 결정 (정적/인터랙션 선택 이유)
- 검수자 주의사항 (모호하여 임의 결정한 내용)
```

---

## 8. API 명세서에서 에러 응답 누락

### 증상
200 OK만 문서화, 4xx/5xx 에러 응답 미기록

### 실제 실패 사례
```markdown
### POST /auth/login
**Response 200**
| 필드 | 타입 | 설명 |
|------|------|------|
| accessToken | string | JWT 토큰 |

<!-- ❌ 401, 400 응답이 없음 -->
```

### 근본 원인
1. "성공 케이스"만 집중
2. 에러 처리는 Coding Agent의 몫이라고 착각

### 올바른 접근
```markdown
### POST /auth/login

**Response 200**
| 필드 | 타입 | 설명 |
|------|------|------|
| success | boolean | true |
| data.accessToken | string | JWT 액세스 토큰 |
| data.user.id | number | 유저 ID |

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

### 필수 에러 응답
- **400**: 요청 파라미터 오류 (형식, 타입, 필수 필드 누락)
- **401**: 인증 실패
- **403**: 권한 없음
- **404**: 리소스 없음
- **409**: 중복 (이메일 중복 등)
- **500**: 서버 에러

---

## 9. 테스트 케이스 접근성 누락

### 증상
프론트엔드 테스트 케이스에 접근성(Accessibility) 항목 없음

### 근본 원인
1. 테스트 = 기능 동작만 확인하는 것으로 착각
2. 접근성은 "선택 사항"이라고 생각

### 올바른 접근
```markdown
### 접근성
| ID | 시나리오 | 기대 결과 |
|----|---------|----------|
| TC-FE-005 | 키보드 네비게이션 | Tab으로 모든 입력 요소 접근 가능 |
| TC-FE-006 | 에러 메시지 스크린 리더 | role=alert로 에러 메시지 읽힘 |
| TC-FE-007 | 포커스 표시 | 모든 인터랙티브 요소에 포커스 아웃라인 |
```

### 언제 추가하는가?
- **Web Fullstack/MVC**: 항상 포함
- **Desktop App**: 항상 포함
- **CLI Tool**: 불필요
- **Library**: API별 판단

---

## 10. Coding Agent 역할 침범

### 증상
명세서에 구현 세부사항 포함 (어떤 라이브러리 사용할지, 파일 구조 등)

### 실제 실패 사례
```markdown
<!-- ❌ 잘못된 예시 -->
## 구현 방법
- bcrypt 라이브러리 사용 (salt rounds=12)
- JWT 토큰은 jose 패키지로 생성
- 파일 위치: src/backend/api/auth.py

## 데이터베이스
- users 테이블에 password_hash 컬럼 추가
- password_hash는 VARCHAR(255)
```

### 근본 원인
1. "자세할수록 좋다"는 착각
2. Coding Agent가 무엇을 결정해야 하는지 모름

### PM Agent vs Coding Agent 역할 구분
```
PM Agent (무엇을):
- 어떤 API 엔드포인트가 필요한가?
- 어떤 입력/출력 필드가 필요한가?
- 어떤 에러 응답이 필요한가?
- 어떤 화면이 필요한가?

Coding Agent (어떻게):
- 어떤 라이브러리 사용할까?
- 파일을 어떻게 구조화할까?
- 어떤 디자인 패턴 적용할까?
- 데이터베이스 스키마 어떻게 설계할까?
```

### 올바른 접근
```markdown
<!-- ✅ 올바른 예시 -->
### POST /auth/login
- **설명**: 이메일/비밀번호로 로그인
- **입력**: email, password
- **출력**: accessToken, user 정보
- **보안**: 비밀번호는 해싱하여 저장 (구체적 알고리즘은 코딩 룰 참조)
- **에러**: 이메일 형식 오류, 비밀번호 불일치, 계정 없음

<!-- "bcrypt 사용", "파일 위치", "VARCHAR(255)" 같은 구현 세부사항은 절대 포함하지 않음 -->
```

---

## 📊 Gotcha 효과 측정

각 Gotcha가 얼마나 자주 발동되는지 추적하여 효과를 측정합니다.

```json
{
  "gotcha_001_scope_creep": {
    "prevented_count": 12,
    "last_triggered": "2026-03-15",
    "effectiveness": "high"
  },
  "gotcha_002_wrong_directory": {
    "prevented_count": 8,
    "last_triggered": "2026-03-14",
    "effectiveness": "high"
  }
}
```

---

## 🔄 업데이트 히스토리

- **2026-03-19**: 초기 버전 생성 (10개 Gotchas)
- 새로운 실패 패턴 발견 시 즉시 추가 예정

---

**다음 읽기**: [workflows/web-fullstack.md](workflows/web-fullstack.md)
