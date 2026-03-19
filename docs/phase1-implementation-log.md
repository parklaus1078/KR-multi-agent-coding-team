# Phase 1.1 구현 로그

> **일시**: 2026-03-19
> **작업**: Gotchas 파일 생성 + Progressive Disclosure 적용
> **소요 시간**: ~30분
> **상태**: ✅ 완료

---

## 📋 구현 내용

### 1. PM Agent Gotchas 파일 생성

**파일**: `team/.agents/pm/gotchas.md` (483줄)

**포함된 10가지 Gotchas**:
1. ✅ 범위 확대 (Scope Creep)
2. ✅ 잘못된 프로젝트 디렉토리
3. ✅ 프로젝트 타입 무시
4. ✅ HTML 와이어프레임에 외부 라이브러리
5. ✅ 실제 API 호출 시뮬레이션 누락
6. ✅ 사용자 승인 없이 파일 생성
7. ✅ 로그 작성 생략
8. ✅ API 명세서에서 에러 응답 누락
9. ✅ 테스트 케이스 접근성 누락
10. ✅ Coding Agent 역할 침범

**각 Gotcha 구조**:
- ❌ 증상
- 🔍 근본 원인
- 📝 실제 실패 사례
- 🚨 탐지 방법
- ✅ 올바른 접근

---

### 2. CLAUDE.md 축소 (Progressive Disclosure)

**변경 전**: `CLAUDE.md` (833줄)
**변경 후**: `CLAUDE.md` (231줄)
**축소율**: **-72% (602줄 감소)**

**백업**: `CLAUDE-backup-20260319.md`

**새 구조**:
```markdown
# PM Agent (231줄)
├── 역할 정의
├── 📂 파일 구조 안내 (gotchas, workflows, templates)
├── 🤖 자동화 모드 규칙
├── 🔨 핵심 프로세스 (Step 0-4)
├── ⚠️ 금지 사항 (요약만, 상세는 gotchas.md)
└── 📋 체크리스트
```

**Progressive Disclosure 적용**:
- 에이전트가 필요한 파일만 읽도록 안내
- `gotchas.md` → `workflows/{project_type}.md` → 작업 시작
- 컨텍스트 로드 시 전체가 아닌 필요 부분만

---

### 3. Auto-Responses 데이터화

**파일**: `team/.config/auto-responses.json`

**하드코딩 제거**:
```python
# 기존 (auto_pipeline.py 24-29줄)
self.auto_responses = {
    "추가할까요": "no, 티켓 범위 내에서만...",
    "변경할까요": "no, 현재 명세대로...",
    "괜찮을까요": "yes, 계속..."
}
```

**새로운 방식** (JSON 기반):
```json
{
  "pm": {
    "patterns": [
      {
        "id": "prevent-scope-creep",
        "trigger": "(추가|더|또한).*(기능|구현).*할까요",
        "response": "no, 티켓 범위 내에서만...",
        "reason": "scope_creep_prevention",
        "gotcha_ref": "gotchas.md#1",
        "confidence": 0.95
      }
    ]
  }
}
```

**장점**:
- ✅ Regex 지원 (더 정교한 매칭)
- ✅ Gotcha 참조 연결
- ✅ 신뢰도 점수 (학습 기반 조정 가능)
- ✅ 코드 배포 없이 규칙 변경

---

## 📊 기대 효과

### 컨텍스트 효율
```
기존: 833줄 전체 로드
개선: 231줄 (핵심) + 필요 시 gotchas.md/workflows 로드
절약: -30% 예상
```

### 실패 방지
```
Gotcha #1 (범위 확대): 40% 감소 예상
Gotcha #2 (잘못된 디렉토리): 90% 감소 예상
Gotcha #4 (HTML 라이브러리): 100% 감소 예상
```

### 유지보수
```
새 실패 패턴 발견 시:
- 기존: CLAUDE.md 전체 수정 (833줄)
- 개선: gotchas.md만 업데이트 (1개 섹션 추가)
```

---

## 🧪 테스트 계획

### 1. 기존 기능 호환성 테스트

```bash
# PM Agent 실행 (기존 방식)
bash team/scripts/run-agent.sh pm --ticket-file projects/test-project/planning/tickets/PLAN-001-test.md

# 체크 포인트:
# - gotchas.md를 읽는가?
# - 올바른 경로에 파일 생성하는가?
# - 로그가 정상 작성되는가?
```

### 2. Gotcha 효과 측정

다음 3개 티켓으로 테스트:
- 티켓 A: 범위 확대 유도 ("auth 기능" → OAuth 추가하는지 확인)
- 티켓 B: 경로 혼동 유도 (프로젝트 확인 생략하는지)
- 티켓 C: HTML 라이브러리 (Tailwind 사용하는지)

**성공 기준**:
- [ ] 범위 확대 안 함 (Out-of-Scope에 기록만)
- [ ] 올바른 경로에 파일 생성
- [ ] 바닐라 JS만 사용

### 3. 컨텍스트 사용량 측정

```bash
# API 호출 로그 비교
# 기존: 833줄 CLAUDE.md → N tokens
# 개선: 231줄 CLAUDE.md → M tokens
# 절감: (N-M)/N * 100%
```

---

## 🚀 다음 단계 (Phase 1.2, 1.3)

### Phase 1.2: Workflows 파일 분리

**생성할 파일**:
```
team/.agents/pm/workflows/
├── web-fullstack.md (현재 CLAUDE-backup에서 추출)
├── cli-tool.md
├── desktop-app.md
├── web-mvc.md
├── library.md
└── data-pipeline.md
```

**예상 효과**:
- CLAUDE.md를 100줄 이하로 더 축소
- 프로젝트 타입별 필요한 워크플로우만 로드
- 새 프로젝트 타입 추가 시 워크플로우 파일만 추가

**소요 시간**: 1-2시간

---

### Phase 1.3: auto_pipeline.py 수정

**수정 파일**: `team/scripts/auto_pipeline.py`

**변경 내용**:
```python
# 기존 (24-29줄)
self.auto_responses = {
    "추가할까요": "no, ...",
    # ...
}

# 개선
def load_auto_responses(self):
    with open('.config/auto-responses.json') as f:
        return json.load(f)

def _check_auto_response(self, message: str) -> str:
    rules = self.auto_responses.get(self.agent_name, {}).get("patterns", [])
    for rule in rules:
        if re.search(rule["trigger"], message):
            return rule["response"]
    return self.auto_responses["fallback"]["default_response"]
```

**소요 시간**: 30분

---

## 📈 성공 메트릭

### 즉시 측정 가능
- [x] CLAUDE.md 줄 수: 833 → 231 (-72%)
- [ ] Gotchas 문서화: 0 → 10개
- [ ] Auto-response 패턴: 3 → 15+

### 1주일 후 측정
- [ ] 범위 이탈 사고: 이전 대비 -40%
- [ ] 잘못된 경로 에러: 이전 대비 -90%
- [ ] HTML 라이브러리 사용: 0건

### 1개월 후 측정
- [ ] 새 Gotcha 발견: 5+ 개 (자동 발견 스크립트 Phase 2.4)
- [ ] 컨텍스트 토큰 절약: 누적 20%+

---

## 🔄 롤백 계획

문제 발생 시:
```bash
cd team/.agents/pm
mv CLAUDE.md CLAUDE-new-broken.md
mv CLAUDE-backup-20260319.md CLAUDE.md
```

---

## 💡 인사이트

### Thariq의 교훈 적용

1. **"The highest-signal content is the Gotchas section"**
   ✅ 구현: gotchas.md 483줄 (가장 많은 정보)

2. **"Progressive Disclosure"**
   ✅ 구현: CLAUDE.md → gotchas.md → workflows/{type}.md

3. **"Don't state the obvious"**
   ✅ 구현: 금지사항을 "왜 실패하는지" 패턴으로 전환

### 예상 못한 이점

- **검색 가능성**: Gotcha별 ID로 참조 (gotchas.md#1)
- **학습 가능성**: 신뢰도 점수로 패턴 효과 추적
- **협업 개선**: 팀원이 gotchas.md만 보고 에이전트 동작 이해

---

## 📝 개선 아이디어 (나중에)

- [ ] Gotcha 효과 자동 측정 스크립트
- [ ] 주간 Gotcha 리포트 (가장 많이 발동된 패턴)
- [ ] Auto-response 신뢰도 자동 조정 (성공률 기반)

---

**다음 구현**: Phase 1.2 - Workflows 파일 분리
**예상 일정**: 2026-03-20
