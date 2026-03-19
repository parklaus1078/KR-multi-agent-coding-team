# Phase 2.1 완료: 구조화된 의사결정 로그 ✅

> **일시**: 2026-03-19
> **Phase**: 2.1 - 구조화된 의사결정 로그
> **소요 시간**: ~25분
> **상태**: ✅ 완료

---

## 🎯 목표

**에이전트의 의사결정 과정을 구조화하여 기록 → 실수에서 학습 가능**
- 단순 작업 로그 → 의사결정 + 근거 + 신뢰도 기록
- 향후 패턴 분석 및 새 Gotcha 발견의 기반

---

## 📦 생성된 파일 (3개)

| 파일 | 줄 수 | 설명 |
|------|-------|------|
| `team/.config/log-schema.json` | 246줄 | 로그 스키마 정의 (필수 필드, 가이드) |
| `team/scripts/analyze-logs.py` | 477줄 | 로그 분석 스크립트 (패턴 추출) |
| `team/scripts/log-helper.py` | 250줄 | JSON ↔ Markdown 변환 헬퍼 |

**총**: 973줄

**수정된 파일**:
- `team/.agents/pm/CLAUDE.md`: 구조화된 로그 작성 지침 추가 (+100줄)

---

## 📋 로그 스키마 구조

### 필수 필드

```json
{
  "metadata": {
    "agent": "pm",                    // 에이전트 이름
    "ticket": "PLAN-001",             // 티켓 번호
    "timestamp": "2026-03-19T10:30:00Z",
    "decision_count": 2,              // 의사결정 개수
    "completion_status": "success"    // 완료 상태
  },
  "decisions": [                      // 의사결정 목록
    {
      "id": "D-001",                  // 결정 ID
      "title": "OAuth 제외",          // 결정 제목
      "context": "...",               // 결정이 필요했던 상황
      "options": ["A", "B", "C"],     // 고려한 옵션들
      "selected": "A",                // 선택한 옵션
      "reason": "...",                // 선택 이유
      "risk_level": "low",            // 위험도 (low/medium/high)
      "confidence": 0.95,             // 신뢰도 (0.0-1.0)
      "gotcha_applied": "gotchas.md#1", // 적용한 Gotcha
      "outcome": "unknown"            // 사후 평가 (나중에 업데이트)
    }
  ],
  "gotchas_applied": [...],           // 적용한 Gotcha 목록
  "patterns_observed": [...],         // 관찰된 패턴
  "auto_responses_triggered": [...],  // 발동된 자동 응답
  "issues_encountered": [...]         // 발견된 이슈 (Gotcha 후보)
}
```

---

## 📝 로그 작성 가이드

### 언제 의사결정을 기록해야 하나?

**기록 필수**:
- ✅ 티켓에 명시되지 않은 사항을 해석할 때
- ✅ 여러 옵션 중 하나를 선택할 때
- ✅ Gotcha 규칙을 적용할 때
- ✅ 위험도 Medium 이상의 가정을 할 때
- ✅ 범위 내/외 판단을 할 때

**기록 불필요**:
- ❌ 명백한 결정 (티켓에 명시된 그대로)
- ❌ 단순 반복 작업 (파일 생성 등)
- ❌ 자동화된 처리 (템플릿 적용)

### 신뢰도 점수 가이드

| 점수 범위 | 의미 | 예시 |
|----------|------|------|
| **0.9-1.0** | 티켓에 명시, 또는 Gotcha 규칙 명확 적용 | "티켓에 'email/password로 로그인'이라고 명시" |
| **0.7-0.9** | 합리적 추론, 업계 표준 패턴 | "REST API이므로 POST는 생성, GET은 조회" |
| **0.5-0.7** | 가정 포함, 사용자 확인 권장 | "일반적으로 사용되는 패턴이므로 추론" |
| **0.0-0.5** | 불확실, 사용자에게 질문 필요 | "요구사항이 모호하여 정확히 알 수 없음" |

### 위험도 점수 가이드

| 위험도 | 의미 | 예시 |
|--------|------|------|
| **low** | 틀려도 쉽게 수정 가능, 영향 범위 작음 | "필드 이름 변경" |
| **medium** | 재작업 필요, 다른 부분에 영향 | "API 엔드포인트 구조 변경" |
| **high** | 큰 재작업, 아키텍처 변경, 비용 큼 | "인증 방식 변경 (JWT → OAuth)" |

---

## 🔍 로그 분석 기능

### `analyze-logs.py` 주요 기능

#### 1. 전체 로그 분석

```bash
python3 scripts/analyze-logs.py --project projects/my-project
```

**분석 항목**:
- 총 로그 및 의사결정 개수
- 에이전트별 의사결정 분포
- 위험도 분포 (low/medium/high)
- 평균 신뢰도
- 가장 많이 사용된 Gotcha Top 5
- 고위험+저신뢰도 결정 (주의 필요)
- 관찰된 패턴 Top 5
- 발동된 자동 응답 Top 5

**출력 예시**:
```
============================================================
의사결정 로그 분석
프로젝트: my-todo-app
============================================================

📊 총 15개 로그 분석 중...

📈 분석 결과

1️⃣  전체 통계:
   총 로그: 15개
   총 의사결정: 32개

2️⃣  에이전트별 의사결정:
   pm: 18개
   coding: 10개
   qa: 4개

3️⃣  위험도 분포:
   low: 22개
   medium: 8개
   high: 2개

4️⃣  신뢰도:
   평균: 0.82
   최저: 0.50
   최고: 0.99

5️⃣  가장 많이 사용된 Gotcha (Top 5):
   gotchas.md#1: 12회
   gotchas.md#2: 8회
   gotchas.md#5: 6회
   gotchas.md#10: 4회
   gotchas.md#8: 3회

⚠️  고위험 + 저신뢰도 결정 (2개):
   [PLAN-003] 인증 방식 선택
      위험: high, 신뢰도: 0.60
      이유: 티켓에 명시되지 않아 JWT 가정...

7️⃣  관찰된 패턴 (Top 5):
   [8회] 사용자가 "auth"라고 하면 로그인/로그아웃만 의미
   [5회] "관리"는 CRUD를 의미, 관리자 기능 아님
   [4회] 테스트 케이스 개수는 기능 복잡도에 비례
```

#### 2. 주간 리포트

```bash
python3 scripts/analyze-logs.py --project projects/my-project --weekly-report
```

**기능**:
- 최근 7일 로그만 분석
- 주간 인사이트 제공
- 가장 자주 발동된 Gotcha
- 평균 신뢰도 추이
- 새 Gotcha 후보 발견

**출력 예시**:
```
============================================================
주간 의사결정 리포트
기간: 2026-03-12 ~ 2026-03-19
============================================================

📊 최근 7일 로그: 8개

💡 주간 인사이트:
   - 가장 많이 적용된 Gotcha: gotchas.md#1 (6회)
   ✅ 평균 신뢰도 양호 (0.85)
   🔍 새 Gotcha 후보 1개 발견
```

#### 3. Gotcha 후보 제안

```bash
python3 scripts/analyze-logs.py --project projects/my-project --suggest-gotchas
```

**기능**:
- 로그의 `issues_encountered` 필드 분석
- 유사한 이슈 그룹화
- 빈도순 정렬
- Top 5를 새 Gotcha 후보로 제안

**출력 예시**:
```
============================================================
새 Gotcha 후보 제안
============================================================

📋 총 12개 이슈, 5개 그룹

1. [4회 발생] HTML 파일에 실제 데이터베이스 스키마 포함
   심각도: medium
   해결: 명세서에서 스키마 제거, Out-of-Scope 이동
   발생 티켓: PLAN-002, PLAN-005, PLAN-008, PLAN-011

2. [3회 발생] 테스트 케이스에 구현 세부사항 명시
   심각도: low
   해결: "무엇을 테스트"만 명시, "어떻게"는 제거
   발생 티켓: PLAN-003, PLAN-007, PLAN-009

💾 Gotcha 후보 저장: projects/my-project/logs/gotcha-candidates.json
```

---

## 🛠️ 로그 헬퍼 도구

### `log-helper.py` 기능

#### 1. JSON → Markdown 변환

```bash
python3 scripts/log-helper.py --json logs/pm/20260319-103000-PLAN-001.json
```

**결과**: 동일 이름의 `.md` 파일 생성 (사람 읽기 편한 형식)

#### 2. 대화형 로그 작성

```bash
python3 scripts/log-helper.py --interactive --agent pm --ticket PLAN-001
```

**기능**:
- 터미널에서 대화형으로 로그 작성
- JSON과 Markdown 자동 생성
- 필드 검증

**예시**:
```
============================================================
대화형 로그 작성: PM - PLAN-001
============================================================

의사결정을 추가합니다. (빈 제목 입력 시 종료)

Decision 1 제목 (또는 엔터로 종료): OAuth 제외
컨텍스트: 티켓에 'login' 명시, 방법 미지정
옵션 (쉼표 구분): Email/Password만, OAuth, 둘 다
선택한 옵션: Email/Password만
이유: Acceptance Criteria에 email/password만 명시
위험도 (low/medium/high): low
신뢰도 (0.0-1.0): 0.95
적용한 Gotcha (선택, 예: gotchas.md#1): gotchas.md#1

...

✅ JSON 저장: logs/pm/20260319-153000-PLAN-001.json
✅ Markdown 저장: logs/pm/20260319-153000-PLAN-001.md
```

---

## 📊 기대 효과

### Before (비구조화 로그)

```markdown
# PM 로그

- 티켓 PLAN-001 작업 완료
- 파일 5개 생성
- OAuth는 제외했음
```

**문제점**:
- ❌ "왜 제외했는지" 없음
- ❌ 다른 옵션 고려했는지 불명
- ❌ 신뢰도/위험도 없음
- ❌ 기계 분석 불가

### After (구조화 로그)

```json
{
  "decisions": [
    {
      "title": "OAuth 제외",
      "context": "티켓에 'login' 명시, 방법 미지정",
      "options": ["Email/Password만", "OAuth", "둘 다"],
      "selected": "Email/Password만",
      "reason": "Acceptance Criteria에 email/password만 명시",
      "risk_level": "low",
      "confidence": 0.95,
      "gotcha_applied": "gotchas.md#1"
    }
  ]
}
```

**개선점**:
- ✅ 결정 과정 투명
- ✅ 다른 옵션도 기록
- ✅ 신뢰도/위험도 명시
- ✅ 기계 분석 가능
- ✅ Gotcha 연결

### 수치 목표

| 항목 | 목표 |
|------|------|
| **회고적 학습** | **+80%** |
| **새 Gotcha 발견률** | **주당 2-3개** (초기) |
| **고위험 결정 추적** | **100%** |
| **의사결정 품질 개선** | **신뢰도 vs 실제 결과 추적** |

---

## 🔄 워크플로우 통합

### PM Agent 작업 순서

```
1. 티켓 읽기
2. Gotchas 확인
3. 워크플로우 로드
4. 산출물 생성
   ↓ (의사결정 발생 시)
   → 결정 과정 기록 (context, options, selected, reason, risk, confidence)
5. 작업 완료
6. 구조화된 로그 작성 (JSON + Markdown)
   - metadata
   - decisions
   - gotchas_applied
   - patterns_observed
   - auto_responses_triggered
   - issues_encountered
```

### 주간 루틴 (자동화 권장)

```bash
# 매주 월요일 실행 (cron)
python3 scripts/analyze-logs.py --project projects/my-project --weekly-report

# 매월 초 실행
python3 scripts/analyze-logs.py --project projects/my-project --suggest-gotchas
```

---

## 💡 핵심 인사이트

### 예상 못한 이점

1. **투명성**: 에이전트가 "왜" 그렇게 결정했는지 명확
2. **디버깅**: 실패 시 어떤 결정이 잘못되었는지 즉시 파악
3. **신뢰**: 신뢰도 점수로 불확실한 결정 사전 파악
4. **학습**: 패턴 분석 → 새 Gotcha 발견 → 룰 추가

### 활용 사례

**Case 1: 고위험+저신뢰도 결정 발견**
```
⚠️  [PLAN-005] 인증 방식 선택
   위험: high, 신뢰도: 0.55
   → 사용자에게 확인 요청 권장
```

**Case 2: 반복 패턴 발견**
```
[8회 발생] 사용자가 "관리"라고 하면 CRUD를 의미
→ Auto-response 규칙 추가 제안
```

**Case 3: 새 Gotcha 발견**
```
[4회 발생] HTML에 실제 DB 스키마 포함
→ Gotcha #11로 추가
→ validate-spec 스킬에 규칙 추가
```

---

## 🎯 Thariq 교훈 적용

| Thariq 교훈 | 적용 방법 |
|------------|----------|
| **"Memory & Data"** | JSON 스키마로 의사결정 구조화 ✅ |
| **"Scripts & Code"** | analyze-logs.py로 자동 분석 ✅ |
| **"Gotchas are highest-signal"** | 의사결정과 Gotcha 연결 ✅ |
| **"Learn from failures"** | issues_encountered → Gotcha 후보 ✅ |
| **"Retrospective learning"** | 주간 리포트, 패턴 분석 ✅ |

---

## 🚀 다음 단계

### 즉시 테스트 가능

```bash
# 1. 대화형 로그 작성 테스트
cd team
python3 scripts/log-helper.py --interactive --agent pm --ticket PLAN-001

# 2. JSON → Markdown 변환 테스트
python3 scripts/log-helper.py --json logs/pm/20260319-103000-PLAN-001.json

# 3. 로그 분석 (샘플 로그 생성 후)
python3 scripts/analyze-logs.py --project projects/test-project
```

### Phase 2 나머지 항목

- ✅ **Phase 2.1**: 구조화된 의사결정 로그 (완료)
- ✅ **Phase 2.2**: Validation Hooks (완료)
- ⬜ **Phase 2.3**: 메모리 시스템
- ⬜ **Phase 2.4**: Gotcha Auto-Discovery

---

## 📈 Phase 2.1 성과

### 생성된 자산

| 카테고리 | 파일 수 | 줄 수 |
|---------|--------|------|
| **스키마** | 1개 | 246줄 |
| **스크립트** | 2개 | 727줄 |
| **문서 업데이트** | 1개 | +100줄 |
| **합계** | 4개 | 1,073줄 |

### 개선 메트릭

| 항목 | 달성 |
|------|------|
| **로그 구조화** | ✅ JSON 스키마 정의 |
| **의사결정 추적** | ✅ context, options, reason, risk, confidence |
| **Gotcha 연결** | ✅ gotcha_applied 필드 |
| **패턴 수집** | ✅ patterns_observed 필드 |
| **자동 분석** | ✅ analyze-logs.py (9개 분석 항목) |
| **주간 리포트** | ✅ --weekly-report 옵션 |
| **Gotcha 발견** | ✅ --suggest-gotchas 옵션 |
| **헬퍼 도구** | ✅ log-helper.py (JSON ↔ MD) |

---

## 🎉 Phase 2.1 완료!

**달성**:
- ✅ 로그 스키마 **JSON 정의**
- ✅ 의사결정 필드 **8개** (id, title, context, options, selected, reason, risk, confidence)
- ✅ 로그 분석 **9개 항목**
- ✅ 주간 리포트 자동화
- ✅ Gotcha 후보 자동 발견
- ✅ JSON ↔ Markdown 변환

**기대 효과**:
- 회고적 학습 **+80%**
- 새 Gotcha 발견 **주당 2-3개**
- 고위험 결정 **100% 추적**

**다음**: Phase 2.3 (메모리 시스템) 또는 Phase 2.4 (Gotcha Auto-Discovery)?

---

## 📝 변경 이력

### 2026-03-19
- ✅ `team/.config/log-schema.json` 생성
- ✅ `team/scripts/analyze-logs.py` 생성
- ✅ `team/scripts/log-helper.py` 생성
- ✅ `team/.agents/pm/CLAUDE.md` 업데이트 (구조화된 로그 작성 지침)
