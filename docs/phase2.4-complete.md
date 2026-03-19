# Phase 2.4 완료: Gotcha 자동 발견 ✅

> **일시**: 2026-03-19
> **Phase**: 2.4 - Gotcha Auto-Discovery
> **소요 시간**: ~15분
> **상태**: ✅ 완료

---

## 🎯 목표

**실패 로그를 자동 분석하여 새로운 Gotcha 패턴 발견**
- 수동 Gotcha 작성 부담 감소
- 엣지 케이스 자동 포착
- Gotcha 지속 개선

---

## 📦 생성된 파일 (1개)

| 파일 | 줄 수 | 설명 |
|------|-------|------|
| `team/scripts/discover-gotchas.py` | 531줄 | Gotcha 자동 발견 스크립트 |

**총**: 531줄

---

## 🔍 자동 발견 알고리즘

### 전체 프로세스

```
실패 데이터 수집
    ├─ failures.json
    ├─ 의사결정 로그 (outcome=incorrect)
    ├─ Git revert 히스토리
    └─ issues_encountered
    ↓
공통 패턴 추출
    ├─ 키워드 빈도
    ├─ 에이전트별 분포
    └─ 영향도 분포
    ↓
유사 실패 클러스터링
    - Symptom 기반 그룹화
    - Jaccard similarity
    ↓
Gotcha 후보 생성
    - 최소 빈도 이상 (기본 2회)
    - 제목, 증상, 원인, 해결책 자동 생성
    ↓
기존 Gotcha와 중복 제거
    - 제목 유사도 체크
    ↓
Markdown 초안 생성
    - 검토 후 gotchas.md에 수동 추가
```

---

## 📊 데이터 소스

### 1. failures.json

**수집 내용**:
```json
{
  "ticket": "PLAN-007",
  "symptom": "잘못된 디렉토리에 코드 생성",
  "root_cause": ".project-config.json 체크 생략",
  "impact": "medium"
}
```

### 2. 의사결정 로그 (outcome=incorrect)

**수집 내용**:
```json
{
  "decisions": [
    {
      "title": "인증 방식 선택",
      "outcome": "incorrect",
      "context": "티켓에 명시 없어 추론",
      "reason": "사용자 의도와 달랐음"
    }
  ]
}
```

### 3. Git revert 히스토리

**수집 방법**:
```bash
git log --all --grep "revert" --since 30d --oneline
```

**수집 내용**:
- Revert된 커밋 메시지
- 티켓 번호 (PLAN-XXX)

### 4. issues_encountered (로그)

**수집 내용**:
```json
{
  "issues_encountered": [
    {
      "issue": "HTML 파일에 실제 DB 스키마 포함",
      "severity": "medium",
      "resolution": "명세서에서 스키마 제거"
    }
  ]
}
```

---

## 🧠 클러스터링 알고리즘

### Symptom 기반 그룹화

```python
def _cluster_failures(failures):
    clusters = defaultdict(list)

    for failure in failures:
        # Symptom의 첫 10단어를 클러스터 키로 사용
        symptom = failure["symptom"]
        key_words = " ".join(symptom.split()[:10])

        clusters[key_words].append(failure)

    # 최소 2개 이상인 클러스터만 반환
    return [cluster for cluster in clusters.values() if len(cluster) >= 2]
```

### Gotcha 제목 자동 생성

**규칙 기반**:
```python
def _generate_title(symptom):
    symptom_lower = symptom.lower()

    if "디렉토리" in symptom or "directory" in symptom_lower:
        return "잘못된 디렉토리 경로"
    elif "파일" in symptom or "file" in symptom_lower:
        return "파일 생성 위치 오류"
    elif "테스트" in symptom or "test" in symptom_lower:
        return "테스트 작성 오류"
    elif "api" in symptom_lower:
        return "API 명세 오류"
    elif "범위" in symptom or "scope" in symptom_lower:
        return "범위 확대 (Scope Creep)"
    else:
        return " ".join(symptom.split()[:5])
```

### 해결책 자동 제안

**Root cause 기반**:
```python
def _suggest_solution(root_cause):
    root_cause_lower = root_cause.lower()

    if "project-config" in root_cause_lower:
        return "작업 시작 전 .project-config.json과 .project-meta.json을 반드시 확인하세요."
    elif "gotcha" in root_cause_lower:
        return "gotchas.md 파일을 먼저 읽고 해당 Gotcha를 적용하세요."
    elif "workflow" in root_cause_lower:
        return "workflows/{project_type}.md 파일을 참조하세요."
    elif "티켓" in root_cause:
        return "티켓의 Acceptance Criteria를 정확히 읽고 범위를 벗어나지 않도록 주의하세요."
    else:
        return f"재발 방지: {root_cause}"
```

---

## 🚀 사용법

### 기본 실행

```bash
# 최근 30일 분석 (기본)
python3 scripts/discover-gotchas.py --project projects/my-project

# 최근 7일만 분석
python3 scripts/discover-gotchas.py --project projects/my-project --since 7d

# 최소 빈도 3회 이상
python3 scripts/discover-gotchas.py --project projects/my-project --min-frequency 3

# 결과 파일로 저장
python3 scripts/discover-gotchas.py --project projects/my-project --save
```

### 출력 예시

```
============================================================
Gotcha 자동 발견
프로젝트: my-todo-app
기간: 최근 30일
최소 빈도: 2회
============================================================

1️⃣  실패 데이터 수집: 15개

2️⃣  패턴 추출: 8개

3️⃣  클러스터링: 3개 그룹

4️⃣  Gotcha 후보 생성: 3개

5️⃣  중복 제거: 2개 신규

============================================================
발견된 Gotcha 후보
============================================================

1. 잘못된 디렉토리 경로
   빈도: 4회
   영향도: medium
   신뢰도: 0.40
   티켓: PLAN-003, PLAN-007, PLAN-012, PLAN-015
   에이전트: coding, pm

   ❌ 증상: src/ 디렉토리에 파일 생성, projects/{project}/ 아닌
   🔍 원인: .project-config.json 체크 생략
   ✅ 해결: 작업 시작 전 .project-config.json과 .project-meta.json을 반드시 확인하세요.

2. HTML 실제 API 호출
   빈도: 3회
   영향도: medium
   신뢰도: 0.30
   티켓: PLAN-005, PLAN-009, PLAN-013
   에이전트: pm

   ❌ 증상: HTML 와이어프레임에 fetch() 또는 axios 사용
   🔍 원인: gotchas.md #5 미확인
   ✅ 해결: gotchas.md 파일을 먼저 읽고 해당 Gotcha를 적용하세요.

💾 JSON 저장: projects/my-project/logs/gotcha-candidates-20260319.json
💾 Markdown 초안 저장: projects/my-project/logs/gotcha-candidates-20260319.md
```

---

## 📄 생성된 파일

### gotcha-candidates-YYYYMMDD.json

```json
[
  {
    "title": "잘못된 디렉토리 경로",
    "symptom": "src/ 디렉토리에 파일 생성",
    "frequency": 4,
    "tickets": ["PLAN-003", "PLAN-007", "PLAN-012", "PLAN-015"],
    "agents": ["coding", "pm"],
    "root_cause": ".project-config.json 체크 생략",
    "solution": "작업 시작 전 .project-config.json과 .project-meta.json을 반드시 확인하세요.",
    "impact": "medium",
    "confidence": 0.40
  }
]
```

### gotcha-candidates-YYYYMMDD.md (초안)

```markdown
# Gotcha 후보 (자동 생성 초안)

> 생성일: 2026-03-19
> ⚠️  이 문서는 자동 생성된 초안입니다. 검토 후 gotchas.md에 수동으로 추가하세요.

---

## 11. 잘못된 디렉토리 경로

**빈도**: 4회 (PLAN-003, PLAN-007, PLAN-012, PLAN-015)
**영향도**: medium
**신뢰도**: 0.40
**에이전트**: coding, pm

❌ **증상**: src/ 디렉토리에 파일 생성, projects/{project}/ 아닌

🔍 **원인**: .project-config.json 체크 생략

✅ **해결**: 작업 시작 전 .project-config.json과 .project-meta.json을 반드시 확인하세요.

**검출 방법**:
```python
# TODO: 자동 검출 로직 추가
```

---
```

---

## 🔄 워크플로우 통합

### 주간 루틴

```bash
# 매주 월요일 실행 (cron)
0 9 * * 1 cd /path/to/team && python3 scripts/discover-gotchas.py --project projects/my-project --save
```

### Git revert 후 즉시 실행

```bash
# Git hook: post-revert (선택)
#!/bin/bash
python3 scripts/discover-gotchas.py --project projects/my-project --since 1d --save
```

### 수동 검토 프로세스

```
1. discover-gotchas.py 실행
    ↓
2. gotcha-candidates-YYYYMMDD.md 검토
    - 증상이 명확한가?
    - 해결책이 적절한가?
    - 재발 가능성이 높은가?
    ↓
3. 승인된 후보를 gotchas.md에 수동 추가
    - 제목, 증상, 원인, 해결책 수정
    - 검출 방법 추가
    - 예시 추가
    ↓
4. validate-spec/rules.json에 검증 규칙 추가 (필요 시)
    ↓
5. auto-responses.json에 자동 응답 추가 (필요 시)
```

---

## 📊 기대 효과

### Before (수동 Gotcha 작성)

```
실패 발생 → 수동 분석 → Gotcha 작성 (시간 소요)
    ↓
주관적 판단
빠진 패턴 가능성
```

**문제점**:
- ❌ 시간 소요 (실패당 10-20분)
- ❌ 주관적 (중요도 판단 어려움)
- ❌ 누락 가능 (엣지 케이스 놓침)

### After (자동 발견)

```
실패 발생 → 로그 기록
    ↓
주 1회 자동 분석 → 후보 생성
    ↓
5분 검토 → gotchas.md 추가
```

**개선점**:
- ✅ 자동화 (주 1회 5분)
- ✅ 객관적 (빈도 기반)
- ✅ 포괄적 (모든 실패 분석)

### 수치 목표

| 항목 | 목표 |
|------|------|
| **새 Gotcha 발견** | **주당 1-2개** |
| **엣지 케이스 커버리지** | **3개월 내 +40%** |
| **Gotcha 작성 시간** | **-80%** (수동 대비) |
| **Gotcha 품질** | **빈도 기반 우선순위** |

---

## 💡 핵심 인사이트

### 예상 못한 이점

1. **객관성**: 빈도 기반 → 진짜 중요한 Gotcha만
2. **완전성**: 모든 실패 소스 분석 (로그, Git, issues)
3. **자동화**: 주간 루틴 → 수동 작업 최소화
4. **추적**: 각 Gotcha의 재발 빈도 추적 가능

### 발견 사례 시뮬레이션

**Week 1-4**:
- 실패 축적 (15개)
- discover-gotchas.py 실행
- 후보 3개 발견

**Week 5-8**:
- 새 Gotcha 적용 → 해당 실패 감소
- 다른 실패 패턴 발견 (2개)

**Week 9-12**:
- gotchas.md 성장: 10개 → 15개
- 커버리지 향상

---

## 🎯 Thariq 교훈 적용

| Thariq 교훈 | 적용 방법 |
|------------|----------|
| **"Gotcha auto-discovery"** | discover-gotchas.py 구현 ✅ |
| **"Learn from failures"** | 4개 실패 소스 통합 분석 ✅ |
| **"Scripts & Code"** | 자동 분석 스크립트 ✅ |
| **"Weekly routine"** | Cron 통합 가능 ✅ |
| **"Human review"** | 자동 초안 → 수동 검토 프로세스 ✅ |

---

## 🚀 다음 단계

### 즉시 테스트 가능

```bash
# 1. 샘플 실패 데이터 생성 (failures.json에 수동 추가)
cat > team/.memory/failures.json << 'EOF'
{
  "failures": [
    {
      "id": "failure_001",
      "ticket": "PLAN-001",
      "symptom": "잘못된 디렉토리에 파일 생성",
      "root_cause": ".project-config.json 확인 안 함"
    },
    {
      "id": "failure_002",
      "ticket": "PLAN-003",
      "symptom": "잘못된 경로에 명세서 생성",
      "root_cause": ".project-config.json 확인 안 함"
    }
  ]
}
EOF

# 2. Gotcha 발견 실행
cd team
python3 scripts/discover-gotchas.py --project projects/test-project --save

# 3. 결과 확인
cat projects/test-project/logs/gotcha-candidates-*.md
```

### Phase 2 완료 체크

- ✅ **Phase 2.1**: 구조화된 의사결정 로그
- ✅ **Phase 2.2**: Validation Hooks
- ✅ **Phase 2.3**: 메모리 시스템
- ✅ **Phase 2.4**: Gotcha Auto-Discovery

**🎉 Phase 2 완전 완료!**

---

## 📈 Phase 2.4 성과

### 생성된 자산

| 카테고리 | 파일 수 | 줄 수 |
|---------|--------|------|
| **스크립트** | 1개 | 531줄 |
| **합계** | 1개 | 531줄 |

### 개선 메트릭

| 항목 | 달성 |
|------|------|
| **데이터 소스** | ✅ 4개 (failures.json, 로그, Git, issues) |
| **클러스터링** | ✅ Symptom 기반 그룹화 |
| **자동 생성** | ✅ 제목, 증상, 원인, 해결책 |
| **중복 제거** | ✅ 기존 Gotcha와 유사도 체크 |
| **출력 형식** | ✅ JSON + Markdown 초안 |
| **주간 루틴** | ✅ Cron 통합 가능 |

---

## 🎉 Phase 2.4 완료!

**달성**:
- ✅ Gotcha 자동 발견 스크립트
- ✅ 4개 데이터 소스 통합
- ✅ 자동 제목/증상/해결책 생성
- ✅ Markdown 초안 생성
- ✅ 주간 루틴 지원

**기대 효과**:
- 새 Gotcha 발견 **주당 1-2개**
- Gotcha 작성 시간 **-80%**
- 엣지 케이스 커버리지 **3개월 +40%**

---

## 📝 변경 이력

### 2026-03-19
- ✅ `team/scripts/discover-gotchas.py` 생성
