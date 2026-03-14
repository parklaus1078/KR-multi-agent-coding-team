# 범용 코딩 원칙

> 모든 프로젝트 타입에 공통으로 적용되는 기본 원칙

---

## 1. 코드 품질 원칙

### DRY (Don't Repeat Yourself)
- 중복 코드를 함수/클래스로 추출
- 같은 로직이 3번 이상 반복되면 리팩토링 필요
- 설정 값은 상수/환경 변수로 분리

### KISS (Keep It Simple, Stupid)
- 간단한 해결책을 먼저 시도
- 불필요한 추상화 지양
- 명확한 변수명 사용 (약어 최소화)

### YAGNI (You Aren't Gonna Need It)
- 현재 필요한 기능만 구현
- 미래를 위한 추측성 코드 작성 금지
- 필요해질 때 추가

### SOLID 원칙

#### S - Single Responsibility Principle (단일 책임 원칙)
- 함수/클래스는 한 가지 일만 수행
- 변경 이유가 하나여야 함

#### O - Open/Closed Principle (개방-폐쇄 원칙)
- 확장에는 열려 있고, 수정에는 닫혀 있어야 함
- 인터페이스/추상 클래스 활용

#### L - Liskov Substitution Principle (리스코프 치환 원칙)
- 하위 타입은 상위 타입을 대체 가능해야 함

#### I - Interface Segregation Principle (인터페이스 분리 원칙)
- 사용하지 않는 메서드에 의존하지 않아야 함
- 작고 구체적인 인터페이스 선호

#### D - Dependency Inversion Principle (의존성 역전 원칙)
- 구체적인 것이 아닌 추상적인 것에 의존
- 의존성 주입(DI) 활용

---

## 2. 네이밍 컨벤션

### 일반 원칙
- **의미 있는 이름**: `data` ❌ → `userData` ✅
- **발음 가능한 이름**: `yyyymmdd` ❌ → `currentDate` ✅
- **검색 가능한 이름**: `7` ❌ → `MAX_RETRY_COUNT` ✅
- **불필요한 맥락 제거**: `UserClass` ❌ → `User` ✅

### 언어별 컨벤션

#### Python
- 변수/함수: `snake_case`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

#### JavaScript/TypeScript
- 변수/함수: `camelCase`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`
- Private (TypeScript): `#field` 또는 `private field`

#### Go
- 변수/함수: `camelCase` (export: `PascalCase`)
- 인터페이스: `PascalCase`
- 상수: `PascalCase` 또는 `camelCase`

#### Rust
- 변수/함수: `snake_case`
- 타입/트레이트: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`

#### Java
- 변수/함수: `camelCase`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`
- 패키지: `lowercase`

---

## 3. 보안 기본 원칙

### 입력 검증
- **모든 사용자 입력은 신뢰하지 않음**
- 타입 검증, 길이 제한, 허용 문자 검증
- 화이트리스트 방식 선호 (블랙리스트 지양)

### 시크릿 관리
- **절대 코드에 하드코딩 금지**
  - API 키, 비밀번호, 토큰 등
- 환경 변수 사용 (`.env` 파일, 절대 Git에 커밋 금지)
- `.env.example` 템플릿 제공
- 프로덕션: 시크릿 관리 도구 사용 (AWS Secrets Manager, HashiCorp Vault 등)

### SQL Injection 방지
- ORM 사용 또는 파라미터화된 쿼리
- 문자열 연결로 SQL 작성 금지

### XSS (Cross-Site Scripting) 방지
- 사용자 입력을 HTML에 삽입 시 이스케이프
- 프레임워크 내장 보호 기능 활용 (React의 자동 이스케이프 등)

### CSRF (Cross-Site Request Forgery) 방지
- CSRF 토큰 사용
- SameSite 쿠키 속성 설정

### 인증/인가
- 비밀번호: bcrypt, argon2 등 강력한 해싱 알고리즘 사용
- JWT: 민감 정보 포함 금지, 짧은 만료 시간 설정
- HTTPS 사용 (프로덕션 필수)

### 에러 메시지
- 프로덕션에서 스택 트레이스 노출 금지
- 사용자에게는 일반적인 에러 메시지
- 상세 에러는 로그에만 기록

---

## 4. 에러 핸들링

### 일반 원칙
- **에러를 무시하지 않음**
- 예상 가능한 에러는 명시적으로 처리
- 복구 불가능한 에러는 빠르게 실패 (Fail Fast)

### 로깅
- 적절한 로그 레벨 사용:
  - `DEBUG`: 개발 중 디버깅 정보
  - `INFO`: 일반 정보 (요청 처리, 시작/종료)
  - `WARNING`: 잠재적 문제
  - `ERROR`: 복구 가능한 에러
  - `CRITICAL`: 시스템 중단 수준 에러

- 민감 정보 로그 금지 (비밀번호, 토큰 등)
- 구조화된 로깅 선호 (JSON 형식)

### 언어별 패턴

#### Python
```python
# ✅ 좋은 예
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

#### JavaScript/TypeScript
```typescript
// ✅ 좋은 예
try {
  const result = await riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error });
  throw error;
}
```

#### Go
```go
// ✅ 좋은 예
result, err := riskyOperation()
if err != nil {
    log.Printf("operation failed: %v", err)
    return err
}
```

---

## 5. 테스팅

### 테스트 피라미드
1. **유닛 테스트 (70%)**: 개별 함수/메서드
2. **통합 테스트 (20%)**: 여러 모듈 협업
3. **E2E 테스트 (10%)**: 전체 시스템 플로우

### 테스트 작성 원칙
- **F.I.R.S.T 원칙**:
  - **Fast**: 빠르게 실행
  - **Independent**: 독립적 실행 가능
  - **Repeatable**: 반복 가능
  - **Self-Validating**: 자동 검증
  - **Timely**: 적시에 작성 (구현과 함께)

### AAA 패턴
```python
def test_user_creation():
    # Arrange (준비)
    user_data = {"email": "test@example.com", "password": "secret"}

    # Act (실행)
    user = create_user(user_data)

    # Assert (검증)
    assert user.email == "test@example.com"
    assert user.id is not None
```

### 커버리지 목표
- 유닛 테스트: 80% 이상
- 통합 테스트: 주요 플로우 커버
- E2E 테스트: 크리티컬 유저 플로우

---

## 6. Git 커밋 메시지

### Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅 (기능 변경 없음)
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드, 패키지 등

### 예시
```
feat(auth): JWT 토큰 기반 인증 구현

- 로그인 시 JWT 토큰 발급
- 토큰 검증 미들웨어 추가
- 만료 시간 1시간으로 설정

Closes #123
```

---

## 7. 코드 리뷰

### 리뷰어 체크리스트
- [ ] 코드가 요구사항을 충족하는가?
- [ ] 테스트가 포함되어 있는가?
- [ ] 보안 취약점이 없는가?
- [ ] 성능 이슈가 없는가?
- [ ] 네이밍이 명확한가?
- [ ] 불필요한 중복이 없는가?
- [ ] 에러 핸들링이 적절한가?

### 작성자 체크리스트
- [ ] 자가 리뷰 완료
- [ ] 테스트 통과
- [ ] 린터/포맷터 실행
- [ ] 커밋 메시지 규칙 준수
- [ ] 변경 사항 문서화

---

## 8. 문서화

### 코드 주석
- **왜(Why)를 설명**, 무엇(What)은 코드로 표현
- 복잡한 알고리즘은 주석 필요
- TODO, FIXME, HACK 태그 활용

### README.md 필수 섹션
1. **프로젝트 설명**
2. **설치 방법**
3. **사용법**
4. **환경 변수 설정**
5. **테스트 실행**
6. **라이선스**

### API 문서 (백엔드)
- OpenAPI/Swagger 자동 생성 활용
- 모든 엔드포인트에 설명 추가
- Request/Response 예시 포함

---

## 9. 의존성 관리

### 버전 고정
- 프로덕션 의존성: 정확한 버전 고정
- 개발 의존성: 범위 허용 가능

### 보안 업데이트
- 정기적으로 의존성 보안 스캔
- Dependabot, Snyk 등 자동화 도구 활용

### 최소 의존성
- 필요한 라이브러리만 추가
- 거대한 라이브러리보다 작은 유틸리티 선호

---

## 10. 성능

### 일반 원칙
- **측정 후 최적화** (추측 금지)
- 병목 지점 프로파일링
- 너무 이른 최적화 지양

### 데이터베이스
- N+1 쿼리 문제 방지
- 적절한 인덱스 사용
- 페이지네이션 구현 (대량 데이터)

### 캐싱
- 변경 빈도 낮은 데이터 캐싱
- 캐시 만료 전략 설정
- 캐시 키 네이밍 규칙 준수

---

## 11. 금지 사항

### 절대 금지
- ❌ 하드코딩된 시크릿
- ❌ SQL 인젝션 가능한 쿼리
- ❌ 사용자 입력 직접 실행 (eval 등)
- ❌ Git에 `.env` 파일 커밋
- ❌ 프로덕션에서 디버그 모드 활성화
- ❌ 민감 정보 로그 출력

### 지양
- ⚠️ 전역 변수 남용
- ⚠️ 깊은 중첩 (3단계 이상)
- ⚠️ 긴 함수 (50줄 이상)
- ⚠️ Magic Number (설명 없는 상수)
- ⚠️ 주석 처리된 코드 (Git 히스토리 활용)

---

## 12. 참고 자료

### 책
- Clean Code (Robert C. Martin)
- The Pragmatic Programmer (David Thomas, Andrew Hunt)
- Refactoring (Martin Fowler)

### 웹 리소스
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- 12 Factor App: https://12factor.net/
- Semantic Versioning: https://semver.org/

---

**버전**: v0.0.1
**최종 업데이트**: 2026-03-12
