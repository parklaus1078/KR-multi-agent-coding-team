# 스프린트 계약 가이드 (PM Agent)

> **Phase 5.3**: Anthropic Harness - 스프린트 계약 협상
>
> **목적**: Coding Agent와 Evaluator Agent가 "완료"의 정의에 합의하도록 명확한 계약 작성

---

## 🎯 핵심 원칙

### Anthropic 연구 결과

> "Evaluator가 구현 전 Generator와 스프린트 계약을 협상한다."
> "이번 스프린트에서 '완료'의 정의는 무엇인가요?"

**효과:**
- 모호한 요구사항 제거
- 평가 기준 사전 합의
- 불필요한 반복 감소

---

## 📋 Acceptance Criteria 작성 기준

### SMART 원칙

모든 Acceptance Criteria는 **SMART**해야 합니다:

- **S**pecific (구체적): "로그인 기능"이 아닌 "POST /api/auth/login 엔드포인트"
- **M**easurable (측정 가능): "빠르게"가 아닌 "200ms 이하"
- **A**chievable (달성 가능): 현실적인 범위
- **R**elevant (관련성): 티켓 목표와 직접 연관
- **T**ime-bound (기한): 1개 티켓 = 1개 스프린트

### ❌ 나쁜 예

```markdown
## Acceptance Criteria

1. 로그인 기능 구현
2. 에러 처리
3. 테스트 작성
```

**문제점:**
- 너무 모호함
- 측정 불가능
- 범위 불명확

### ✅ 좋은 예

```markdown
## Acceptance Criteria

### 기능 요구사항 (Functional)

1. **로그인 API**
   - [ ] POST /api/auth/login 엔드포인트 생성
   - [ ] 입력: `{ "email": string, "password": string }`
   - [ ] 성공 시: 200 OK + `{ "token": string, "user": {...} }`
   - [ ] 실패 시: 401 Unauthorized + `{ "error": "Invalid credentials" }`

2. **JWT 토큰 발급**
   - [ ] HS256 알고리즘 사용
   - [ ] 토큰 유효 기간: 24시간
   - [ ] Payload: `{ "user_id": int, "email": string, "exp": timestamp }`

3. **비밀번호 검증**
   - [ ] bcrypt 해싱 사용 (salt rounds: 12)
   - [ ] 평문 비밀번호 저장 금지

### 비기능 요구사항 (Non-Functional)

4. **성능**
   - [ ] 응답 시간: 200ms 이하 (p95)
   - [ ] 동시 접속: 100 req/s 처리 가능

5. **보안**
   - [ ] SQL Injection 방어 (Parameterized Query)
   - [ ] Rate Limiting: 5회/분 (IP 기준)

6. **에러 처리**
   - [ ] 400 Bad Request: 필수 필드 누락 시
   - [ ] 401 Unauthorized: 잘못된 자격 증명 시
   - [ ] 500 Internal Server Error: 서버 에러 시
   - [ ] 모든 에러는 JSON 형식: `{ "error": "message" }`

### 테스트 요구사항

7. **유닛 테스트**
   - [ ] `authenticate_user()` 함수 테스트
   - [ ] `generate_token()` 함수 테스트
   - [ ] `verify_password()` 함수 테스트
   - [ ] 커버리지: 80% 이상

8. **통합 테스트**
   - [ ] 성공 케이스: 올바른 email/password
   - [ ] 실패 케이스: 잘못된 email
   - [ ] 실패 케이스: 잘못된 password
   - [ ] 실패 케이스: 필수 필드 누락

### 문서화 요구사항

9. **API 문서**
   - [ ] Swagger/OpenAPI 스키마 업데이트
   - [ ] 예시 요청/응답 포함

10. **코드 문서**
    - [ ] 모든 public 함수에 Docstring
    - [ ] 파라미터, 리턴 값, 예외 설명
```

---

## 🔍 체크리스트: Acceptance Criteria 작성 후

작성한 Acceptance Criteria가 다음 질문에 **모두 Yes**인지 확인:

- [ ] **Coding Agent가 이것만 보고 구현 가능한가?**
  - 엔드포인트 경로, HTTP 메서드, 입출력 형식 명시
  - 사용할 라이브러리/알고리즘 명시

- [ ] **Evaluator Agent가 이것만 보고 평가 가능한가?**
  - 각 항목이 체크박스로 검증 가능
  - 성능/보안 기준 수치화

- [ ] **QA Agent가 이것만 보고 테스트 케이스 작성 가능한가?**
  - 성공/실패 케이스 명시
  - 입력/출력 예시 제공

- [ ] **모호한 표현이 없는가?**
  - "적절히", "빠르게", "효율적으로" 제거
  - 구체적 수치나 조건으로 대체

- [ ] **Out-of-Scope가 명확한가?**
  - 이번 티켓에서 하지 않을 것 명시
  - 범위 확대 방지

---

## 📝 명세서 템플릿 (강화)

### Backend API 명세서

```markdown
# Backend API 명세서: PLAN-{번호}

## 개요

**티켓**: PLAN-{번호}
**기능**: {한 줄 설명}
**스프린트 계약**: 이 명세서의 모든 Acceptance Criteria 만족 시 "완료"로 간주

---

## Acceptance Criteria (스프린트 계약)

### 기능 요구사항

1. **{기능명 1}**
   - [ ] 구체적 요구사항 1
   - [ ] 구체적 요구사항 2

2. **{기능명 2}**
   - [ ] 구체적 요구사항 1
   - [ ] 구체적 요구사항 2

### 비기능 요구사항

3. **성능**
   - [ ] 측정 가능한 기준 1
   - [ ] 측정 가능한 기준 2

4. **보안**
   - [ ] 보안 요구사항 1
   - [ ] 보안 요구사항 2

5. **에러 처리**
   - [ ] 에러 케이스 1
   - [ ] 에러 케이스 2

### 테스트 요구사항

6. **유닛 테스트**
   - [ ] 테스트할 함수 1
   - [ ] 테스트할 함수 2
   - [ ] 커버리지: 80% 이상

7. **통합 테스트**
   - [ ] 시나리오 1
   - [ ] 시나리오 2

### 문서화 요구사항

8. **API 문서**
   - [ ] Swagger/OpenAPI 업데이트
   - [ ] 예시 포함

9. **코드 문서**
   - [ ] Docstring 작성
   - [ ] 파라미터/리턴/예외 설명

---

## Out-of-Scope (이번 티켓에서 제외)

**명시적으로 하지 않을 것:**
- OAuth 로그인 (PLAN-XXX에서 처리)
- 비밀번호 찾기 (PLAN-XXX에서 처리)
- 소셜 로그인 (향후 고려)

**이유**: 티켓 Acceptance Criteria에 명시되지 않음

---

## API 엔드포인트

### POST /api/auth/login

**설명**: 사용자 로그인

**요청**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**응답 (성공 200)**:
```json
{
  "token": "eyJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**응답 (실패 401)**:
```json
{
  "error": "Invalid credentials"
}
```

**응답 (실패 400)**:
```json
{
  "error": "Missing required field: email"
}
```

**성능 기준**:
- 응답 시간: 200ms 이하 (p95)
- Rate Limit: 5회/분 (IP 기준)

**보안**:
- bcrypt 해싱 (salt rounds: 12)
- SQL Injection 방어 (Parameterized Query)

**테스트 케이스**:
1. 성공: 올바른 email/password
2. 실패: 잘못된 email
3. 실패: 잘못된 password
4. 실패: 필수 필드 누락 (email)
5. 실패: 필수 필드 누락 (password)
6. 실패: Rate Limit 초과

---

## 데이터 모델

### User

```python
class User:
    id: int              # Primary Key
    email: str           # Unique, Not Null
    password_hash: str   # bcrypt hash, Not Null
    name: str            # Not Null
    created_at: datetime # Auto-generated
```

---

## 아키텍처

### Layered Architecture

```
Controller (routes/auth.py)
  ↓ 입력 검증, 요청 파싱
Service (services/auth_service.py)
  ↓ 비즈니스 로직 (인증, 토큰 발급)
Repository (models/user.py)
  ↓ 데이터베이스 접근
Database (PostgreSQL)
```

---

## 코딩 룰 준수

**적용 룰**: `.rules/_verified/web-fullstack/backend-fastapi-python.md`

**핵심 원칙**:
- DRY, SOLID 원칙
- 타입 힌팅 필수
- Docstring 작성
- 에러 핸들링 (try-except)

---

## 평가 기준 (Evaluator Agent용)

**Coding Agent 구현 완료 후, Evaluator Agent는 다음을 확인:**

| 항목 | 배점 | 확인 방법 |
|------|-----|----------|
| **기능 완성도** | 40 | 모든 Acceptance Criteria 체크박스 ✓ |
| - POST /api/auth/login | 10 | curl 테스트 성공 |
| - JWT 토큰 발급 | 10 | 토큰 검증 성공 |
| - 비밀번호 검증 | 10 | bcrypt 사용 확인 |
| - 에러 처리 | 10 | 모든 에러 케이스 테스트 |
| **코드 품질** | 30 | 코딩 룰 준수 확인 |
| **테스트 커버리지** | 20 | pytest --cov (80% 이상) |
| **문서화** | 10 | Docstring, API 문서 확인 |

**목표 점수**: 90점 이상

---

## 스프린트 계약 확약

**PM Agent (나)**: 이 명세서를 작성했습니다.

**Coding Agent**: 이 명세서의 모든 Acceptance Criteria를 구현하겠습니다.

**Evaluator Agent**: 이 명세서를 기준으로 평가하겠습니다.

**계약 일시**: {timestamp}
```

---

## 🎯 작성 후 체크리스트

명세서 작성 완료 후 다음을 확인:

- [ ] 모든 Acceptance Criteria가 체크박스 형식
- [ ] 모든 Acceptance Criteria가 SMART 원칙 준수
- [ ] Out-of-Scope 명시
- [ ] API 엔드포인트 상세 (경로, 메서드, 입출력)
- [ ] 성능 기준 수치화 (200ms, 80% 등)
- [ ] 보안 요구사항 명시
- [ ] 에러 케이스 나열
- [ ] 테스트 케이스 나열
- [ ] 평가 기준 명시
- [ ] 스프린트 계약 확약 섹션 포함

---

## 📚 참고 예시

### CLI Tool 명세서

```markdown
## Acceptance Criteria

### 기능 요구사항

1. **create 명령어**
   - [ ] `mycli create <description>` 형식
   - [ ] description은 필수 인자
   - [ ] 성공 시: "Todo created: {description}" 출력 + Exit code 0
   - [ ] 실패 시: "Error: Missing argument 'description'" 출력 + Exit code 1

2. **list 명령어**
   - [ ] `mycli list` 형식
   - [ ] 저장된 모든 할일 목록 출력
   - [ ] 형식: "1. Buy milk\n2. Read book"
   - [ ] 빈 목록 시: "No todos found" 출력

3. **데이터 저장**
   - [ ] SQLite 데이터베이스 사용
   - [ ] 파일 위치: `~/.mycli/data.db`
   - [ ] 테이블: todos (id, description, created_at)

### 비기능 요구사항

4. **성능**
   - [ ] 실행 시간: 100ms 이하
   - [ ] 메모리 사용: 50MB 이하

5. **에러 처리**
   - [ ] 잘못된 명령어: "Error: Unknown command '{cmd}'" + Exit code 1
   - [ ] DB 접근 실패: "Error: Database connection failed" + Exit code 1
   - [ ] 모든 에러는 stderr로 출력

### 테스트 요구사항

6. **유닛 테스트**
   - [ ] `test_create_todo()`: 정상 생성
   - [ ] `test_create_todo_missing_arg()`: 인자 누락
   - [ ] `test_list_todos()`: 목록 조회
   - [ ] `test_list_todos_empty()`: 빈 목록
   - [ ] 커버리지: 80% 이상

7. **통합 테스트**
   - [ ] 실제 명령어 실행 (subprocess)
   - [ ] 임시 DB 사용 (tmpdir)
   - [ ] Exit code 확인

### 문서화 요구사항

8. **--help 문서**
   - [ ] `mycli --help`: 전체 명령어 목록
   - [ ] `mycli create --help`: create 명령어 상세
   - [ ] 각 명령어 설명 + 사용 예시 포함

9. **README**
   - [ ] 설치 방법 (pip install)
   - [ ] 사용 예시 (3-5개 명령어)
```

---

## 💡 Tip: 명확한 계약 = 적은 반복

**명확한 계약:**
```
Acceptance Criteria: 10개 항목, 모두 체크박스
→ Coding Agent: 10개 모두 구현
→ Evaluator: 10개 모두 확인
→ 1-2회 반복으로 완료 ✅
```

**모호한 계약:**
```
Acceptance Criteria: "로그인 기능 구현"
→ Coding Agent: OAuth도 구현 (범위 확대)
→ Evaluator: "OAuth는 티켓에 없음" (-10점)
→ 5-10회 반복 필요 ⚠️
```

---

**이 가이드는 PM Agent가 명세서 작성 시 참조하여, Coding Agent와 Evaluator Agent가 합의할 수 있는 명확한 스프린트 계약을 작성하도록 돕습니다.**
