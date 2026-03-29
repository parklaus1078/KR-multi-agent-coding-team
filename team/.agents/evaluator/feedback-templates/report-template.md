# 평가 리포트: {TICKET_NUMBER}

## 📊 종합 점수

**총점: {TOTAL_SCORE}/100** {VERDICT_EMOJI} **{VERDICT}**

| 항목 | 만점 | 획득 |
|------|-----|-----|
| 기능 완성도 | 40 | {FUNCTIONALITY_SCORE} |
| 코드 품질 | 30 | {CODE_QUALITY_SCORE} |
| 테스트 커버리지 | 20 | {TEST_COVERAGE_SCORE} |
| 문서화 | 10 | {DOCUMENTATION_SCORE} |

**판정 기준:**
- 90점 이상: ✅ 우수 (재작업 불필요)
- 70-89점: ⚠️ 보통 (일부 개선 필요)
- 50-69점: ❌ 미흡 (재작업 필요)
- 50점 미만: 🛑 불합격 (전면 재작업)

---

## ✅ 통과한 항목

### 기능 완성도
{PASSED_FUNCTIONALITY_ITEMS}

### 코드 품질
{PASSED_CODE_QUALITY_ITEMS}

### 테스트 커버리지
{PASSED_TEST_COVERAGE_ITEMS}

### 문서화
{PASSED_DOCUMENTATION_ITEMS}

---

## ❌ 실패한 항목

### 기능 완성도 ({FUNCTIONALITY_SCORE}/40점)

{FAILED_FUNCTIONALITY_ITEMS}

### 코드 품질 ({CODE_QUALITY_SCORE}/30점)

{FAILED_CODE_QUALITY_ITEMS}

### 테스트 커버리지 ({TEST_COVERAGE_SCORE}/20점)

{FAILED_TEST_COVERAGE_ITEMS}

### 문서화 ({DOCUMENTATION_SCORE}/10점)

{FAILED_DOCUMENTATION_ITEMS}

---

## 🔧 개선 제안

### 우선순위 1 (필수)
{PRIORITY_1_SUGGESTIONS}

### 우선순위 2 (권장)
{PRIORITY_2_SUGGESTIONS}

### 우선순위 3 (선택)
{PRIORITY_3_SUGGESTIONS}

---

## 📝 다음 단계

**재작업 필요**: {NEEDS_REWORK}

**권장 조치:**
{RECOMMENDED_ACTIONS}

**예상 점수 향상**: +{EXPECTED_IMPROVEMENT}점 → 총 {EXPECTED_NEW_SCORE}점 ({OLD_VERDICT} → {NEW_VERDICT})

---

## 📊 이전 평가 대비 변화 (재평가인 경우)

{ITERATION_HISTORY}

---

**평가 완료 시각**: {TIMESTAMP}
**Evaluator Agent 버전**: v0.0.4
**반복 횟수**: {ITERATION_NUMBER}
