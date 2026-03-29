# Web Fullstack 평가 기준

> **프로젝트 타입**: web-fullstack
>
> **평가 대상**: Backend API + Frontend UI
>
> **총점**: 100점

---

## 📊 평가 기준 (4가지)

### 1. 기능 완성도 (40점)

#### Backend API (20점)

**필수 검증 항목:**

- [ ] **모든 API 엔드포인트 동작** (10점)
  - Acceptance Criteria의 모든 엔드포인트 호출 성공
  - 정상 응답 (200, 201, 204 등)
  - JSON 스키마 일치

- [ ] **에러 케이스 처리** (5점)
  - 400: Bad Request (잘못된 입력)
  - 401: Unauthorized (인증 실패)
  - 403: Forbidden (권한 없음)
  - 404: Not Found (리소스 없음)
  - 500: Internal Server Error (서버 에러)

- [ ] **입력 검증** (5점)
  - 필수 필드 누락 시 400 에러
  - 타입 불일치 시 400 에러
  - SQL Injection, XSS 방어

**검증 스크립트 예시:**

```bash
# 정상 케이스
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}' \
  -w "\nStatus: %{http_code}\n"
# 예상: Status: 201

# 에러 케이스 (필수 필드 누락)
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}' \
  -w "\nStatus: %{http_code}\n"
# 예상: Status: 400

# 에러 케이스 (타입 불일치)
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email": 123, "password": "password123"}' \
  -w "\nStatus: %{http_code}\n"
# 예상: Status: 400
```

#### Frontend UI (20점)

**필수 검증 항목:**

- [ ] **모든 화면 렌더링** (10점)
  - Acceptance Criteria의 모든 화면 접근 가능
  - 404 에러 없음
  - 콘솔 에러 없음

- [ ] **사용자 인터랙션 동작** (5점)
  - 버튼 클릭 동작
  - 폼 제출 동작
  - 네비게이션 동작

- [ ] **데이터 표시 정확성** (5점)
  - Backend API 응답 데이터가 올바르게 표시됨
  - 로딩 상태 표시
  - 에러 메시지 표시

**검증 방법:**

```bash
# 브라우저에서 수동 확인 또는 Playwright 스크립트 사용
# (현재 버전에서는 수동 확인)

# 1. 브라우저 열기
open http://localhost:3000

# 2. 콘솔 에러 확인
# - F12 → Console 탭
# - 에러 메시지 없는지 확인

# 3. 네트워크 요청 확인
# - F12 → Network 탭
# - API 호출 성공하는지 확인
```

---

### 2. 코드 품질 (30점)

#### Backend 코드 (15점)

**필수 검증 항목:**

- [ ] **코딩 룰 준수** (7점)
  - `.rules/_verified/web-fullstack/backend-*.md` 또는
  - `.rules/_cache/{project}/backend-*.md` 준수
  - DRY, SOLID 원칙 적용

  **체크 포인트:**
  - 중복 코드 없음 (동일 로직이 3곳 이상 반복되지 않음)
  - 함수/클래스 크기 적절 (함수 50줄 이하)
  - 책임 분리 (라우팅, 비즈니스 로직, DB 접근 분리)

- [ ] **타입 힌팅 (Python) / TypeScript** (4점)
  - 모든 함수에 타입 힌트 추가 (Python)
  - 또는 TypeScript 사용 (Node.js)

  **예시 (Python):**
  ```python
  # ✅ 좋은 예
  def get_user(user_id: int) -> Optional[User]:
      return db.query(User).filter(User.id == user_id).first()

  # ❌ 나쁜 예
  def get_user(user_id):
      return db.query(User).filter(User.id == user_id).first()
  ```

- [ ] **에러 핸들링** (4점)
  - try-except 사용
  - 로깅 적절 (logger.error)
  - 사용자 친화적 에러 메시지

  **예시:**
  ```python
  # ✅ 좋은 예
  try:
      user = get_user(user_id)
      if not user:
          raise HTTPException(status_code=404, detail="User not found")
      return user
  except DatabaseError as e:
      logger.error(f"Database error: {e}")
      raise HTTPException(status_code=500, detail="Internal server error")

  # ❌ 나쁜 예
  user = get_user(user_id)
  return user
  ```

#### Frontend 코드 (15점)

**필수 검증 항목:**

- [ ] **컴포넌트 구조** (7점)
  - 재사용 가능한 컴포넌트 분리
  - Props 타입 정의 (TypeScript 또는 PropTypes)
  - 적절한 파일 분할

  **체크 포인트:**
  - 컴포넌트당 200줄 이하
  - 공통 UI (Button, Input 등) 재사용
  - pages/ 와 components/ 분리

- [ ] **상태 관리** (4점)
  - useState, useReducer, Context API 등 적절히 사용
  - 불필요한 전역 상태 지양
  - Props drilling 최소화

- [ ] **스타일링** (4점)
  - 일관된 스타일링 방법 (CSS Modules, Tailwind, styled-components 등)
  - 반응형 디자인 (모바일, 태블릿, 데스크톱)
  - 접근성 (a11y) 기본 준수

---

### 3. 테스트 커버리지 (20점)

#### Backend 테스트 (12점)

**필수 검증 항목:**

- [ ] **유닛 테스트 커버리지 80% 이상** (6점)
  - pytest, unittest 등 사용
  - 비즈니스 로직 함수 테스트
  - 에러 케이스 포함

  **커버리지 확인:**
  ```bash
  # Python
  pytest --cov=src --cov-report=term
  # 목표: 80% 이상

  # Node.js
  npm test -- --coverage
  # 목표: 80% 이상
  ```

- [ ] **통합 테스트 주요 플로우** (4점)
  - API 엔드포인트 통합 테스트
  - DB 연동 테스트 (실제 DB 또는 Test DB)
  - 인증 플로우 테스트

- [ ] **테스트 통과율 100%** (2점)
  - 모든 테스트 통과
  - Flaky 테스트 없음

  ```bash
  pytest -v
  # 또는
  npm test
  # 예상: All tests passed
  ```

#### Frontend 테스트 (8점)

**필수 검증 항목:**

- [ ] **컴포넌트 테스트** (4점)
  - Vitest, Jest, React Testing Library 사용
  - 주요 컴포넌트 렌더링 테스트
  - 사용자 인터랙션 테스트

  **예시:**
  ```javascript
  // ✅ 좋은 예
  test('renders login form and submits', async () => {
    render(<LoginForm />);

    const emailInput = screen.getByLabelText('Email');
    const passwordInput = screen.getByLabelText('Password');
    const submitButton = screen.getByRole('button', { name: 'Login' });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'password123');
    await userEvent.click(submitButton);

    expect(await screen.findByText('Welcome!')).toBeInTheDocument();
  });
  ```

- [ ] **E2E 테스트 주요 플로우** (4점)
  - Playwright, Cypress 사용 (선택)
  - 사용자 시나리오 테스트 (로그인 → 데이터 조회 → 로그아웃)

---

### 4. 문서화 (10점)

**필수 검증 항목:**

- [ ] **Docstring / JSDoc** (5점)
  - 모든 public 함수/클래스에 문서 주석
  - 파라미터, 리턴 값 설명

  **예시 (Python):**
  ```python
  def create_user(email: str, password: str) -> User:
      """
      새로운 사용자를 생성합니다.

      Args:
          email (str): 사용자 이메일 (유효한 형식)
          password (str): 사용자 비밀번호 (최소 8자)

      Returns:
          User: 생성된 사용자 객체

      Raises:
          ValueError: 이메일 형식이 잘못된 경우
          DatabaseError: DB 저장 실패 시
      """
      ...
  ```

- [ ] **README 업데이트** (3점)
  - 설치 방법
  - 실행 방법
  - API 엔드포인트 목록

- [ ] **API 문서** (2점)
  - Swagger / OpenAPI (FastAPI 자동 생성 등)
  - 또는 수동 작성 (`docs/api.md`)

---

## 🎯 점수 계산 예시

### 예시 1: 우수한 구현 (92점)

| 항목 | 만점 | 획득 | 비고 |
|------|-----|-----|------|
| **기능 완성도** | 40 | 38 | DELETE 엔드포인트 일부 에러 |
| - Backend API | 20 | 18 | 에러 처리 일부 누락 |
| - Frontend UI | 20 | 20 | 완벽 |
| **코드 품질** | 30 | 28 | 일부 중복 코드 |
| - Backend | 15 | 14 | 타입 힌트 일부 누락 |
| - Frontend | 15 | 14 | Props 타입 일부 누락 |
| **테스트** | 20 | 18 | 커버리지 75% |
| - Backend | 12 | 10 | 유닛 테스트 75% |
| - Frontend | 8 | 8 | 완벽 |
| **문서화** | 10 | 8 | API 문서 부족 |
| **총점** | **100** | **92** | ✅ **우수** |

**판정:** ✅ 우수 (재작업 불필요)

---

### 예시 2: 보통 구현 (75점)

| 항목 | 만점 | 획득 | 비고 |
|------|-----|-----|------|
| **기능 완성도** | 40 | 30 | 일부 기능 동작 안 함 |
| - Backend API | 20 | 15 | PUT 엔드포인트 버그 |
| - Frontend UI | 20 | 15 | 에러 메시지 미표시 |
| **코드 품질** | 30 | 22 | 많은 중복 코드 |
| - Backend | 15 | 11 | 에러 핸들링 부족 |
| - Frontend | 15 | 11 | 컴포넌트 크기 과다 |
| **테스트** | 20 | 15 | 커버리지 60% |
| - Backend | 12 | 9 | 통합 테스트 없음 |
| - Frontend | 8 | 6 | 일부 컴포넌트만 테스트 |
| **문서화** | 10 | 8 | Docstring 일부 누락 |
| **총점** | **100** | **75** | ⚠️ **보통** |

**판정:** ⚠️ 보통 (일부 개선 필요)

---

### 예시 3: 미흡한 구현 (55점)

| 항목 | 만점 | 획득 | 비고 |
|------|-----|-----|------|
| **기능 완성도** | 40 | 20 | 절반만 동작 |
| - Backend API | 20 | 10 | 주요 엔드포인트 에러 |
| - Frontend UI | 20 | 10 | 데이터 표시 안 됨 |
| **코드 품질** | 30 | 15 | 코딩 룰 미준수 |
| - Backend | 15 | 8 | 타입 힌트 없음 |
| - Frontend | 15 | 7 | 컴포넌트 구조 엉망 |
| **테스트** | 20 | 12 | 커버리지 30% |
| - Backend | 12 | 7 | 유닛 테스트 부족 |
| - Frontend | 8 | 5 | 테스트 거의 없음 |
| **문서화** | 10 | 8 | README만 작성 |
| **총점** | **100** | **55** | ❌ **미흡** |

**판정:** ❌ 미흡 (재작업 필요)

---

## 🔍 특수 검증 항목 (Web Fullstack)

### 보안 체크

- [ ] **CORS 설정 적절**
  - 프로덕션에서 `*` 사용 금지
  - 명시적인 origin 허용

- [ ] **인증 토큰 안전**
  - JWT는 httpOnly 쿠키 또는 Authorization 헤더
  - LocalStorage에 민감 정보 저장 금지

- [ ] **SQL Injection 방어**
  - ORM 사용 또는 파라미터화된 쿼리

- [ ] **XSS 방어**
  - React/Vue의 기본 이스케이핑 사용
  - dangerouslySetInnerHTML 사용 최소화

### 성능 체크

- [ ] **API 응답 시간** (목표: 200ms 이하)
  ```bash
  curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/users
  # time_total: 0.150s → ✅ 통과
  # time_total: 0.350s → ⚠️ 최적화 필요
  ```

- [ ] **Frontend 번들 크기** (목표: 500KB 이하)
  ```bash
  npm run build
  # dist/assets/index.js: 320KB → ✅ 통과
  # dist/assets/index.js: 800KB → ⚠️ 최적화 필요
  ```

### 크로스 브라우저 호환성 (선택)

- [ ] Chrome, Firefox, Safari에서 동작 확인

---

## 📝 평가 리포트 예시

```markdown
# 평가 리포트: PLAN-001 (User Authentication)

## 📊 종합 점수

**총점: 75/100** ⚠️ **보통**

| 항목 | 만점 | 획득 |
|------|-----|-----|
| 기능 완성도 | 40 | 30 |
| 코드 품질 | 30 | 22 |
| 테스트 커버리지 | 20 | 15 |
| 문서화 | 10 | 8 |

---

## ✅ 통과한 항목

### 기능 완성도
- [x] POST /api/auth/login 정상 동작
- [x] POST /api/auth/register 정상 동작
- [x] 로그인 페이지 렌더링 정상

### 코드 품질
- [x] 코딩 룰 대부분 준수
- [x] DRY 원칙 적용

### 문서화
- [x] README 업데이트됨
- [x] Docstring 대부분 작성

---

## ❌ 실패한 항목

### 기능 완성도 (30/40점)

#### 1. PUT /api/auth/password 버그 (-5점)
- **문제**: 비밀번호 변경 시 500 에러 발생
- **원인**: `src/routes/auth.py:67` - bcrypt 해싱 누락
- **재현 방법**:
  ```bash
  curl -X PUT http://localhost:8000/api/auth/password \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"old_password": "old123", "new_password": "new123"}'
  # 응답: 500 Internal Server Error
  ```
- **수정 방법**:
  ```python
  # src/routes/auth.py:67
  # 수정 전
  user.password = new_password

  # 수정 후
  user.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
  ```

#### 2. 에러 메시지 미표시 (-5점)
- **문제**: Frontend에서 로그인 실패 시 에러 메시지 안 보임
- **파일**: `frontend/src/pages/Login.tsx:45`
- **수정 방법**: API 에러 응답을 state에 저장하고 표시

### 코드 품질 (22/30점)

#### 1. 중복 코드 (-5점)
- **문제**: 비밀번호 검증 로직이 3곳에 반복됨
- **파일**:
  - `src/routes/auth.py:23`
  - `src/routes/auth.py:45`
  - `src/routes/auth.py:67`
- **수정 방법**: `src/utils/validation.py`에 `validate_password()` 함수 추출

#### 2. 타입 힌트 누락 (-3점)
- **파일**: `src/utils/token.py:10` - `generate_token()` 함수
- **수정 방법**:
  ```python
  def generate_token(user_id: int) -> str:
  ```

### 테스트 커버리지 (15/20점)

#### 1. 유닛 테스트 커버리지 60% (-5점)
- **목표**: 80% 이상
- **현재**: 60%
- **누락된 테스트**:
  - `update_password()` 함수
  - `refresh_token()` 함수
- **수정 방법**: `tests/test_auth.py`에 테스트 추가

---

## 🔧 개선 제안

### 우선순위 1 (필수)
1. ✅ PUT /api/auth/password 버그 수정
2. ✅ 테스트 커버리지 80% 달성
3. ✅ 중복 코드 제거

### 우선순위 2 (권장)
1. 에러 메시지 표시 (Frontend)
2. 타입 힌트 추가

### 우선순위 3 (선택)
1. API 응답 시간 최적화 (현재 평균 180ms)
2. 보안 감사 (OWASP Top 10 체크)

---

## 📝 다음 단계

**재작업 필요**: 예

**권장 조치:**
1. Coding Agent 재실행으로 버그 수정
2. QA Agent 재실행으로 테스트 추가
3. Evaluator Agent 재평가

**예상 점수 향상**: +15점 → 총 90점 (보통 → 우수)
```

---

## 🎯 작업 완료 체크리스트

- [ ] Backend API 모든 엔드포인트 테스트
- [ ] Frontend 모든 화면 렌더링 확인
- [ ] 코딩 룰 준수 여부 확인
- [ ] 테스트 커버리지 측정
- [ ] 문서화 확인
- [ ] 평가 리포트 작성
- [ ] 점수 JSON 저장
- [ ] 피드백 요약 생성
