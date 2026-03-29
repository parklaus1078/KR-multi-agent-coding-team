# 스프린트 계약 템플릿

> **Phase 5.3**: Anthropic Harness - 스프린트 계약 협상
>
> **목적**: PM, Coding, Evaluator 간 "완료"의 정의 명확화

---

## 📋 스프린트 계약서

**티켓**: PLAN-{번호}
**기능**: {한 줄 설명}
**계약 일시**: {timestamp}

---

## 🤝 계약 당사자

| 역할 | 책임 | 상태 |
|------|------|------|
| **PM Agent** | Acceptance Criteria 작성 | ✅ 완료 |
| **Coding Agent** | Acceptance Criteria 구현 | ⏳ 대기 |
| **Evaluator Agent** | Acceptance Criteria 검증 | ⏳ 대기 |

---

## ✅ Acceptance Criteria (스프린트 계약)

### 기능 요구사항

1. **{기능명 1}**
   - [ ] 구체적 요구사항 1-1 (예: POST /api/auth/login 엔드포인트 생성)
   - [ ] 구체적 요구사항 1-2 (예: 입력: `{ "email": string, "password": string }`)
   - [ ] 구체적 요구사항 1-3 (예: 성공 시: 200 OK + JWT 토큰)

2. **{기능명 2}**
   - [ ] 구체적 요구사항 2-1
   - [ ] 구체적 요구사항 2-2

### 비기능 요구사항

3. **성능**
   - [ ] 응답 시간: {수치}ms 이하 (예: 200ms)
   - [ ] 동시 접속: {수치} req/s 처리 가능 (예: 100)

4. **보안**
   - [ ] 보안 요구사항 1 (예: bcrypt 해싱, salt rounds: 12)
   - [ ] 보안 요구사항 2 (예: SQL Injection 방어)

5. **에러 처리**
   - [ ] 에러 케이스 1 (예: 400 Bad Request: 필수 필드 누락)
   - [ ] 에러 케이스 2 (예: 401 Unauthorized: 잘못된 자격 증명)
   - [ ] 에러 케이스 3 (예: 500 Internal Server Error: 서버 에러)

### 테스트 요구사항

6. **유닛 테스트**
   - [ ] 테스트할 함수 1 (예: `authenticate_user()`)
   - [ ] 테스트할 함수 2 (예: `generate_token()`)
   - [ ] 커버리지: {수치}% 이상 (예: 80%)

7. **통합 테스트**
   - [ ] 시나리오 1 (예: 성공 케이스: 올바른 email/password)
   - [ ] 시나리오 2 (예: 실패 케이스: 잘못된 password)

### 문서화 요구사항

8. **API 문서**
   - [ ] Swagger/OpenAPI 스키마 업데이트
   - [ ] 예시 요청/응답 포함

9. **코드 문서**
   - [ ] 모든 public 함수에 Docstring
   - [ ] 파라미터, 리턴 값, 예외 설명

---

## 📊 계약 요약

**총 Acceptance Criteria 개수**: {체크박스 개수}개

**카테고리별 분포:**
- 기능 요구사항: {개수}개
- 비기능 요구사항: {개수}개
- 테스트 요구사항: {개수}개
- 문서화 요구사항: {개수}개

---

## 🚫 Out-of-Scope (명시적 제외)

**이번 스프린트에서 하지 않을 것:**
- {제외 항목 1} (예: OAuth 로그인 - PLAN-XXX에서 처리)
- {제외 항목 2} (예: 비밀번호 찾기 - PLAN-XXX에서 처리)
- {제외 항목 3} (예: 소셜 로그인 - 향후 고려)

**이유**: 티켓 Acceptance Criteria에 명시되지 않음

---

## 🎯 "완료"의 정의

이 스프린트는 다음 조건을 **모두 만족**할 때 "완료"로 간주합니다:

1. ✅ **모든 Acceptance Criteria 체크박스 완료** (100% 이행)
2. ✅ **Evaluator Agent 평가 90점 이상**
3. ✅ **모든 테스트 통과** (유닛 + 통합)
4. ✅ **코딩 룰 준수** (`.rules/` 기준)
5. ✅ **문서화 완료** (API 문서, Docstring)

**부분 완료 기준** (70-89점):
- 80% 이상의 Acceptance Criteria 만족
- 주요 기능 동작
- 일부 개선 필요

**미완료 기준** (70점 미만):
- 70% 미만의 Acceptance Criteria 만족
- 주요 기능 미동작
- 전면 재작업 필요

---

## 📝 계약 확약

### PM Agent (명세서 작성자)

```
✅ 확인했습니다.

이 Acceptance Criteria는 SMART 원칙을 준수하며,
Coding Agent가 구현 가능하고 Evaluator Agent가 검증 가능합니다.

작성 일시: {timestamp}
```

### Coding Agent (구현자)

```
✅ 확인했습니다.

이 명세서의 모든 Acceptance Criteria를 구현하겠습니다.
Out-of-Scope 항목은 구현하지 않겠습니다.

확약 일시: {timestamp}
예상 소요 시간: {추정}분
```

### Evaluator Agent (평가자)

```
✅ 확인했습니다.

이 Acceptance Criteria를 기준으로 평가하겠습니다.
계약 이행률을 계산하여 점수를 산출하겠습니다.

평가 기준:
- 기능 완성도 (40점): 계약 이행률 × 0.4
- 코드 품질 (30점): 코딩 룰 준수도
- 테스트 커버리지 (20점): 유닛 + 통합 테스트
- 문서화 (10점): API 문서 + Docstring

평가 일시: {timestamp}
```

---

## 🔄 계약 변경 프로세스

### 계약 변경이 필요한 경우

1. **PM Agent가 Acceptance Criteria 수정**
   - 명세서 파일 업데이트
   - Coding Agent에게 통지 (새 파일 생성)

2. **Coding Agent가 불명확한 부분 발견**
   - 로그에 기록
   - 합리적 해석으로 진행
   - 평가 후 개선

3. **Evaluator Agent가 평가 기준 조정 필요**
   - 피드백에 명시
   - 다음 반복에 반영

### 계약 변경 시 원칙

- ✅ 범위 축소: 가능 (현실적 조정)
- ⚠️ 범위 확대: 신중 (새 티켓 생성 권장)
- ❌ 평가 기준 완화: 불가 (품질 유지)

---

## 📈 성공 지표

**계약 이행률**:
```
계약 이행률 = (만족한 AC 개수 / 전체 AC 개수) × 100
```

**목표:**
- 1차 반복: 70% 이상
- 2차 반복: 85% 이상
- 3차 반복: 95% 이상

**실제 예시:**

| 반복 | 만족 AC | 전체 AC | 이행률 | 점수 |
|------|---------|---------|--------|------|
| 1차 | 9개 | 13개 | 69% | 65점 |
| 2차 | 11개 | 13개 | 85% | 82점 |
| 3차 | 13개 | 13개 | 100% | 92점 |

---

## 💡 Tip: 명확한 계약의 이점

### Before (모호한 계약)

```markdown
## Acceptance Criteria

1. 로그인 기능 구현
2. 에러 처리
3. 테스트 작성
```

**결과:**
- Coding Agent: "OAuth도 구현?"
- Evaluator: "OAuth는 티켓에 없음" (-10점)
- 5-10회 반복 필요 ⚠️

### After (명확한 계약)

```markdown
## Acceptance Criteria

1. **로그인 API**
   - [ ] POST /api/auth/login
   - [ ] 입력: `{ "email": string, "password": string }`
   - [ ] 성공: 200 OK + JWT 토큰

2. **에러 처리**
   - [ ] 400: 필수 필드 누락
   - [ ] 401: 잘못된 자격 증명

3. **테스트**
   - [ ] 유닛 테스트 80% 이상
   - [ ] 통합 테스트: 성공/실패 케이스

## Out-of-Scope
- OAuth 로그인 (명시되지 않음)
```

**결과:**
- Coding Agent: "명확함, 바로 구현"
- Evaluator: "계약 100% 이행" (92점)
- 1-2회 반복으로 완료 ✅

---

## 📚 참고 자료

- **PM Agent 가이드**: `.agents/pm/sprint-contract-guide.md`
- **Coding Agent 확약**: `.agents/coding/CLAUDE.md` (Step 2)
- **Evaluator Agent 검증**: `.agents/evaluator/CLAUDE.md` (Step 2-4)
- **Anthropic Harness 논문**: https://www.anthropic.com/engineering/harness-design-long-running-apps

---

**이 템플릿을 사용하여 PM, Coding, Evaluator 간 명확한 스프린트 계약을 체결하고, 불필요한 반복을 줄이며 품질을 향상시킵니다.**
