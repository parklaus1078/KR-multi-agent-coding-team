# Multi-Agent Coding Tool - API 마이그레이션 기획안

**작성일**: 2026-03-16
**목표**: Claude Code CLI → Anthropic API 기반 전환으로 완전 자동화된 agentic coding tool 구축

---

## 📋 목차

1. [현황 분석](#1-현황-분석)
2. [목표 및 요구사항](#2-목표-및-요구사항)
3. [기술 스택 비교](#3-기술-스택-비교)
4. [아키텍처 설계](#4-아키텍처-설계)
5. [구현 계획](#5-구현-계획)
6. [비용 분석](#6-비용-분석)
7. [리스크 관리](#7-리스크-관리)
8. [마일스톤](#8-마일스톤)

---

## 1. 현황 분석

### 1.1 현재 시스템 (v0.0.2)

**구조:**
```
Shell Script (auto-pipeline.sh)
  ↓
Claude Code CLI (대화형)
  ↓
수동 Ctrl+C 종료
```

**장점:**
- ✅ 빠른 프로토타입
- ✅ Claude Code Max 구독 활용
- ✅ 티켓별 실행 잘 작동

**단점:**
- ❌ 자동화 불완전 (수동 개입 필요)
- ❌ Follow-up 질문 시 대기
- ❌ 프로그래밍 방식 제어 불가
- ❌ 에러 핸들링 제한적
- ❌ 로깅/모니터링 어려움

### 1.2 사용 패턴 분석

**티켓별 실행 (Manual Mode):**
- 빈도: 80%
- 사용 케이스: 복잡한 기능, 실험적 개발
- 요구사항: 대화형, 사람 개입 가능

**전체 자동 실행 (Auto-Pipeline):**
- 빈도: 20%
- 사용 케이스: 명확한 요구사항, 반복 작업
- 요구사항: 완전 자동화, 무인 실행

---

## 2. 목표 및 요구사항

### 2.1 핵심 목표

1. **완전 자동화**: Follow-up 질문 자동 응답, 무인 실행
2. **비용 효율**: 장기적으로 Claude Code Max보다 저렴
3. **유지보수성**: 확장 가능하고 관리 쉬운 코드베이스
4. **양립 가능**: Manual/Auto 모드 모두 지원

### 2.2 기능 요구사항

**Must Have:**
- [ ] 티켓별 실행 (Manual Mode)
- [ ] 전체 티켓 자동 실행 (Auto-Pipeline)
- [ ] 자동 응답 시스템
- [ ] 세션 저장 및 재개
- [ ] Rate limit 자동 관리
- [ ] Git 자동 커밋/푸시
- [ ] 진행상황 저장/복원

**Should Have:**
- [ ] 에러 자동 복구 (재시도)
- [ ] 상세 로깅/모니터링
- [ ] 비용 추적
- [ ] 대화 히스토리 분석

**Nice to Have:**
- [ ] Multi-agent 병렬 실행
- [ ] 학습 기반 자동 응답 개선
- [ ] Web UI
- [ ] Slack/Discord 알림

---

## 3. 기술 스택 비교

### 3.1 Claude Code CLI vs Anthropic API

| 항목 | Claude Code CLI | Anthropic API |
|------|----------------|---------------|
| **비용 모델** | 월 구독 ($110) | 사용량 기반 (~$50/월 예상) |
| **제어 수준** | 제한적 (CLI 인터페이스) | 완전 제어 (Python API) |
| **자동화** | 부분적 (--print 모드) | 완벽 (프로그래밍) |
| **대화 관리** | 자동 (내장) | 수동 (코드 작성) |
| **에러 핸들링** | 제한적 | 완전 제어 |
| **로깅** | 제한적 | 완전 제어 |
| **확장성** | 낮음 | 높음 |
| **러닝 커브** | 낮음 | 중간 |

### 3.2 선택 근거

**Anthropic API 선택 이유:**

1. **비용**: 월 $50 예상 vs $110 (45% 절감)
2. **자동화**: 100% 무인 실행 가능
3. **확장성**: 미래 기능 추가 용이
4. **제어**: 모든 단계 세밀 제어

**리스크:**
- 초기 개발 시간 (2-4주)
- 코드 복잡도 증가
- API 변경 대응 필요

---

## 4. 아키텍처 설계

### 4.1 시스템 구조

```
┌─────────────────────────────────────────┐
│         CLI Interface                    │
│  python auto_pipeline.py [options]       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Pipeline Controller                 │
│  - Mode selection (manual/auto)         │
│  - Ticket orchestration                 │
│  - Progress management                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Agent System                     │
│  ┌─────────┬─────────┬─────────┐       │
│  │   PM    │ Coding  │   QA    │       │
│  └─────────┴─────────┴─────────┘       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Anthropic API Client                │
│  - Message management                   │
│  - Auto-response engine                 │
│  - Session persistence                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│    Infrastructure Services               │
│  - Git operations                       │
│  - File I/O                             │
│  - Logging                              │
│  - Cost tracking                        │
└─────────────────────────────────────────┘
```

### 4.2 핵심 컴포넌트

#### 4.2.1 Pipeline Controller

```python
class PipelineController:
    """
    파이프라인 전체 오케스트레이션

    책임:
    - Ticket 로딩 및 순서 관리
    - Agent 실행 조율
    - 진행상황 관리
    - 에러 처리 및 복구
    """

    def run_manual_mode(self, ticket_num: str)
    def run_auto_mode(self, resume: bool = False)
    def save_progress(self, ticket_num: str, step: str)
    def load_progress(self) -> dict
```

#### 4.2.2 Agent System

```python
class BaseAgent:
    """
    모든 에이전트의 베이스 클래스

    책임:
    - System prompt 로딩
    - 대화 관리
    - 자동 응답 규칙 적용
    - 완료 감지
    """

    def run(self, prompt: str, auto_respond: bool) -> ConversationResult
    def is_complete(self, message: str) -> bool
    def auto_reply(self, message: str) -> Optional[str]

class PMAgent(BaseAgent):
    """PM 특화 로직"""

class CodingAgent(BaseAgent):
    """Coding 특화 로직"""

class QAAgent(BaseAgent):
    """QA 특화 로직"""
```

#### 4.2.3 Auto-Response Engine

```python
class AutoResponseEngine:
    """
    자동 응답 규칙 관리

    책임:
    - 패턴 매칭
    - 컨텍스트 기반 응답 선택
    - 학습 데이터 수집 (미래)
    """

    rules: Dict[str, ResponseRule]

    def match_pattern(self, message: str) -> Optional[str]
    def add_rule(self, pattern: str, response: str)
    def learn_from_history(self, conversations: List[Conversation])
```

#### 4.2.4 Session Manager

```python
class SessionManager:
    """
    세션 저장 및 재개

    책임:
    - 대화 히스토리 저장
    - 세션 복원
    - 메타데이터 관리
    """

    def save_session(self, ticket_num: str, agent: str, messages: List)
    def load_session(self, ticket_num: str, agent: str) -> List
    def list_sessions(self) -> List[SessionInfo]
```

### 4.3 데이터 모델

```python
@dataclass
class Ticket:
    number: str          # "PLAN-001"
    title: str
    content: str
    status: TicketStatus  # pending, pm_done, coding_done, qa_done, completed

@dataclass
class ConversationResult:
    messages: List[Message]
    completed: bool
    session_id: str
    cost: float

@dataclass
class Message:
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime

@dataclass
class PipelineProgress:
    last_ticket: str
    last_step: str  # "pm" | "coding" | "qa"
    timestamp: datetime
    total_cost: float
```

---

## 5. 구현 계획

### 5.1 Phase 1: 기본 인프라 (Week 1-2)

**목표**: API 기반 단일 티켓 실행

**작업:**
- [ ] `anthropic` 라이브러리 설치 및 설정
- [ ] `BaseAgent` 클래스 구현
- [ ] `PMAgent`, `CodingAgent`, `QAAgent` 구현
- [ ] 단일 티켓 manual 모드 작동
- [ ] 기본 로깅 시스템

**산출물:**
```python
# 실행 예시
python auto_pipeline.py --ticket PLAN-001 --mode manual
```

**테스트:**
- PLAN-001 티켓으로 PM → Coding → QA 전체 플로우 성공

---

### 5.2 Phase 2: 자동 응답 시스템 (Week 3)

**목표**: Follow-up 질문 자동 처리

**작업:**
- [ ] `AutoResponseEngine` 구현
- [ ] 기본 응답 규칙 정의
- [ ] 패턴 매칭 로직
- [ ] Auto 모드 구현

**응답 규칙 예시:**
```python
AUTO_RESPONSE_RULES = {
    r".*추가.*할까요.*\?": "no, 티켓 범위 내에서만 진행",
    r".*변경.*할까요.*\?": "no, 현재 명세대로",
    r".*확인.*필요.*\?": "yes, 계속 진행",
    r".*리팩토링.*\?": "no, 현재 티켓만 집중",
}
```

**산출물:**
```python
# 실행 예시
python auto_pipeline.py --ticket PLAN-001 --mode auto
```

**테스트:**
- Follow-up 질문 5개 시나리오에서 자동 응답 성공

---

### 5.3 Phase 3: 전체 파이프라인 (Week 4)

**목표**: 전체 티켓 자동 실행

**작업:**
- [ ] `PipelineController` 구현
- [ ] 티켓 순회 로직
- [ ] 진행상황 저장/복원
- [ ] Git 자동 커밋/푸시
- [ ] Rate limit 체크 통합

**산출물:**
```python
# 실행 예시
python auto_pipeline.py --mode auto --all-tickets
python auto_pipeline.py --mode auto --resume
```

**테스트:**
- 5개 티켓 프로젝트 무인 실행 성공
- 중단 후 resume 성공

---

### 5.4 Phase 4: 고급 기능 (Week 5-6)

**목표**: Production-ready 기능

**작업:**
- [ ] 에러 자동 복구 (재시도 로직)
- [ ] 상세 로깅 (파일별, 타임스탬프)
- [ ] 비용 추적 및 리포트
- [ ] 세션 관리 개선
- [ ] 성능 최적화

**산출물:**
```python
# 비용 리포트
python auto_pipeline.py --cost-report

# 세션 목록
python auto_pipeline.py --list-sessions

# 재시도
python auto_pipeline.py --retry-failed
```

---

### 5.5 Phase 5: 병행 운영 및 전환 (Week 7-8)

**목표**: Shell script → Python 완전 전환

**작업:**
- [ ] 기존 shell script와 병행 운영
- [ ] 비용/성능 비교 측정
- [ ] 사용자 가이드 작성
- [ ] Migration 스크립트 작성
- [ ] 기존 시스템 deprecated 마킹

**의사결정 기준:**
```
비용 비교:
- Shell script (Claude Code Max): $110/month
- Python (Anthropic API): $XX/month

성능 비교:
- 자동화율: Shell XX% vs Python XX%
- 에러율: Shell XX% vs Python XX%
- 평균 실행 시간: Shell XXm vs Python XXm

→ Python이 더 저렴하고 자동화율 높으면 전환
```

---

## 6. 비용 분석

### 6.1 예상 사용량

**가정:**
- 월 5개 프로젝트 개발
- 프로젝트당 평균 20개 티켓
- 티켓당 3단계 (PM, Coding, QA)

**총 요청:**
- 5 프로젝트 × 20 티켓 × 3 에이전트 = **300 요청/월**

### 6.2 토큰 사용량 추정

**PM Agent (티켓당):**
```
Input:
  - 티켓 내용: 1,000 tokens
  - System prompt: 2,000 tokens
  - 총: 3,000 tokens

Output:
  - 명세서: 5,000 tokens

비용: 3K × $3/1M + 5K × $15/1M = $0.084
```

**Coding Agent (티켓당):**
```
Input:
  - 명세서: 5,000 tokens
  - System prompt: 2,000 tokens
  - 코드 참조: 3,000 tokens
  - 총: 10,000 tokens

Output:
  - 코드: 10,000 tokens

비용: 10K × $3/1M + 10K × $15/1M = $0.18
```

**QA Agent (티켓당):**
```
Input:
  - 테스트케이스: 3,000 tokens
  - System prompt: 2,000 tokens
  - 총: 5,000 tokens

Output:
  - 테스트 코드: 8,000 tokens

비용: 5K × $3/1M + 8K × $15/1M = $0.135
```

**티켓당 총 비용:**
```
$0.084 + $0.18 + $0.135 = $0.40/티켓
```

### 6.3 월간 비용 추정

**기본 시나리오:**
```
100 티켓/월 × $0.40 = $40/월
```

**여유분 (재시도, 실험, 수정):**
```
+30% = $12/월
```

**총 예상 비용:**
```
$52/월
```

**Claude Code Max 대비:**
```
절감액: $110 - $52 = $58/월 (53% 절감)
연간: $696 절감
```

### 6.4 비용 최적화 전략

**단기:**
- Prompt 최적화 (불필요한 토큰 제거)
- Caching 활용 (system prompt 캐싱)

**중기:**
- Batch API 활용 (50% 할인)
- 모델 선택 최적화 (Haiku for simple tasks)

**장기:**
- Fine-tuning으로 prompt 축소
- Self-hosting 고려

---

## 7. 리스크 관리

### 7.1 기술 리스크

| 리스크 | 영향도 | 가능성 | 완화 방안 |
|--------|--------|--------|-----------|
| API 변경 | 높음 | 낮음 | 버전 핀닝, 정기 업데이트 체크 |
| Rate limit 초과 | 중간 | 중간 | 자동 재시도, 백오프 전략 |
| 비용 초과 | 중간 | 낮음 | 비용 모니터링, 예산 알림 |
| 자동 응답 실패 | 중간 | 중간 | Fallback 전략, 수동 개입 |

### 7.2 운영 리스크

| 리스크 | 영향도 | 가능성 | 완화 방안 |
|--------|--------|--------|-----------|
| 마이그레이션 실패 | 높음 | 낮음 | 병행 운영, 롤백 계획 |
| 학습 곡선 | 낮음 | 중간 | 상세 문서, 예제 제공 |
| 유지보수 부담 | 중간 | 중간 | 모듈화, 테스트 코드 |

### 7.3 비용 리스크

**시나리오 분석:**

**Best Case (월 $30):**
- 효율적인 prompt
- 재시도 최소화
- Batch API 활용

**Base Case (월 $52):**
- 현재 추정치

**Worst Case (월 $80):**
- 비효율적 사용
- 많은 재시도
- 실험 많음

**대응:**
- 월 $100 초과 시 알림
- 비용 분석 리포트 주간 생성
- 필요 시 Claude Code로 롤백

---

## 8. 마일스톤

### 8.1 개발 일정

```
Week 1-2: Phase 1 - 기본 인프라
  ├─ Day 1-3: API 연동 및 BaseAgent
  ├─ Day 4-7: PM/Coding/QA Agent 구현
  └─ Day 8-10: 통합 테스트

Week 3: Phase 2 - 자동 응답
  ├─ Day 11-13: AutoResponseEngine
  └─ Day 14-15: Auto 모드 테스트

Week 4: Phase 3 - 전체 파이프라인
  ├─ Day 16-18: PipelineController
  ├─ Day 19-20: Git 통합
  └─ Day 21-22: 전체 테스트

Week 5-6: Phase 4 - 고급 기능
  ├─ Week 5: 에러 처리, 로깅
  └─ Week 6: 비용 추적, 최적화

Week 7-8: Phase 5 - 병행 운영
  ├─ Week 7: 병행 운영, 비용 측정
  └─ Week 8: 의사결정, 전환 or 롤백
```

### 8.2 성공 기준

**MVP (Week 4 완료 시):**
- [ ] 단일 티켓 manual 모드 100% 성공
- [ ] 단일 티켓 auto 모드 80% 성공 (자동 응답)
- [ ] 전체 티켓 auto 모드 70% 성공 (5개 티켓)

**Production (Week 8 완료 시):**
- [ ] 전체 티켓 auto 모드 90% 성공
- [ ] 월 비용 $60 이하
- [ ] 에러 복구율 95% 이상
- [ ] 문서화 완료

---

## 9. 다음 단계

### 9.1 즉시 실행 (이번 주)

1. **의사결정**: API 마이그레이션 진행 여부 최종 확인
2. **환경 설정**: Anthropic API 키 발급, 개발 환경 구축
3. **킥오프**: Phase 1 시작

### 9.2 체크포인트

**Week 2 종료 시:**
- Phase 1 완료 확인
- 단일 티켓 manual 모드 작동 검증
- Go/No-go 결정

**Week 4 종료 시:**
- MVP 완성 확인
- 초기 비용 측정
- 전환 여부 예비 결정

**Week 8 종료 시:**
- 최종 비용/성능 비교
- 전환 or 롤백 최종 결정

---

## 10. 부록

### 10.1 참고 자료

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude Sonnet 4.5 Pricing](https://www.anthropic.com/pricing)
- [Best Practices for Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)

### 10.2 FAQ

**Q: 기존 shell script는 어떻게 되나요?**
A: Week 8까지 병행 운영 후, Python이 더 나으면 deprecated 처리합니다.

**Q: 비용이 예상보다 높으면?**
A: 월 $100 초과 시 Claude Code Max로 롤백 가능합니다.

**Q: 개발 기간 중 프로젝트는 어떻게 진행하나요?**
A: 기존 shell script 계속 사용하면서 병행 개발합니다.

**Q: API 키 관리는?**
A: 환경변수 `.env` 파일로 관리, git에 커밋 안 함.

---

## 11. 승인

이 기획안에 대한 승인 및 피드백:

- [ ] **승인**: API 마이그레이션 진행
- [ ] **보류**: 추가 검토 필요
- [ ] **거부**: 현재 시스템 유지

**피드백:**
```
(여기에 의견 작성)
```

---

**문서 버전**: v1.0
**최종 수정**: 2026-03-16
**작성자**: Claude Sonnet 4.5
