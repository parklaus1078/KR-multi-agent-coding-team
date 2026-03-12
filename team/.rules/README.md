# 코딩 룰 디렉토리

이 디렉토리는 프로젝트 타입별 코딩 규칙을 관리합니다.

---

## 📂 디렉토리 구조

```
.rules/
├── README.md                        # 이 파일
├── general-coding-rules.md          # 범용 코딩 원칙 (DRY, SOLID 등)
├── _verified/                       # ⭐ 사람이 검증한 룰 (우선순위 최상)
│   └── web-fullstack/
│       ├── be-coding-rules.md       # FastAPI (Python) - 검증 완료
│       └── fe-coding-rules.md       # Next.js (TypeScript) - 검증 완료
└── _cache/                          # 🤖 Stack Initializer Agent가 자동 생성한 룰
    └── (프로젝트 시작 시 자동 생성됨)
```

---

## 🔍 우선순위

코딩 에이전트가 코딩 룰을 찾을 때 아래 순서로 확인합니다:

1. **`_verified/{project_type}/{framework}-{language}.md`** - 사람이 검증한 룰
   - **존재**: 이 룰 사용 (가장 신뢰도 높음)
   - **없음**: 2번 확인

2. **`_cache/{project_type}/{framework}-{language}.md`** - 자동 생성된 룰
   - **존재 + 24시간 이내**: 이 룰 사용
   - **존재 + 24시간 경과**: 재생성 여부 사용자 확인
   - **없음**: 3번 진행

3. **실시간 생성** - Stack Initializer Agent 호출
   - 공식 문서 및 베스트 프랙티스 분석
   - `.rules/_cache/`에 새로운 룰 생성
   - 24시간 캐시

---

## ⭐ Verified 룰 승격 방법

자동 생성된 룰을 검증 완료 상태로 승격:

```bash
# 1. 자동 생성된 룰 확인
cat .rules/_cache/cli-tool/cobra-go.md

# 2. 필요한 부분 수정

# 3. _verified로 이동
mkdir -p .rules/_verified/cli-tool
mv .rules/_cache/cli-tool/cobra-go.md .rules/_verified/cli-tool/

# 4. .project-config.json 업데이트
# "coding_rules_status": "verified"
```

---

## 🤖 자동 생성 룰 특징

Stack Initializer Agent가 생성하는 룰은 다음을 포함합니다:

- **프로젝트 구조**: 디렉토리 레이아웃, 파일 조직
- **아키텍처 패턴**: MVC, Layered, Clean Architecture 등
- **네이밍 컨벤션**: 파일명, 변수명, 함수명, 클래스명
- **보안 가이드**: 입력 검증, 시크릿 관리, OWASP 대응
- **테스팅 전략**: 프레임워크, 디렉토리 구조, 커버리지 목표
- **의존성 관리**: 패키지 매니저, 버전 관리
- **에러 핸들링**: 예외 처리 전략, 로깅
- **성능 최적화**: 프레임워크별 최적화 포인트
- **참고 자료**: 공식 문서 링크, 인기 프로젝트 예시

---

## 📝 general-coding-rules.md

모든 프로젝트 타입에 공통으로 적용되는 범용 원칙:

- **DRY (Don't Repeat Yourself)**
- **SOLID 원칙**
- **KISS (Keep It Simple, Stupid)**
- **YAGNI (You Aren't Gonna Need It)**
- **보안 기본 원칙** (입력 검증, 최소 권한 등)
- **Git 커밋 메시지 규칙**

프레임워크 특화 룰과 함께 참조됩니다.

---

## 🔄 캐시 갱신

`.rules/_cache/` 아래 파일은 24시간 캐시됩니다.

### 수동 갱신

```bash
# 특정 룰 재생성
rm .rules/_cache/cli-tool/cobra-go.md
bash scripts/run-agent.sh stack-initializer --config .project-config.json
```

### 자동 갱신

Stack Initializer Agent가 캐시 파일의 생성 시간을 확인하고:
- 24시간 이내: 기존 파일 사용
- 24시간 경과: 재생성 여부 물어봄

---

## 🌍 커뮤니티 기여

검증된 코딩 룰을 커뮤니티에 기여할 수 있습니다:

1. `.rules/_verified/` 하위 파일을 GitHub에 PR
2. 다른 사용자가 검증된 룰 활용 가능
3. 프로젝트 시작 시 verified 룰이 있으면 자동 생성 생략

---

## 🛠️ 예시: CLI Tool (Go Cobra)

### 초기 상태 (verified 룰 없음)

```bash
bash scripts/init-project.sh --type cli-tool --language go --framework cobra --name my-cli
```

Stack Initializer Agent가:
1. `.rules/_verified/cli-tool/cobra-go.md` 확인 → 없음
2. `.rules/_cache/cli-tool/cobra-go.md` 확인 → 없음
3. 공식 문서 분석 → `cobra-go.md` 생성
4. `.rules/_cache/cli-tool/cobra-go.md`에 저장

### 검증 후 승격

```bash
# 수정 및 검증
vi .rules/_cache/cli-tool/cobra-go.md

# 승격
mkdir -p .rules/_verified/cli-tool
mv .rules/_cache/cli-tool/cobra-go.md .rules/_verified/cli-tool/
```

### 다음 프로젝트 (동일 스택)

```bash
bash scripts/init-project.sh --type cli-tool --language go --framework cobra --name another-cli
```

Stack Initializer Agent가:
1. `.rules/_verified/cli-tool/cobra-go.md` 확인 → **존재!**
2. 자동 생성 생략, 검증된 룰 사용

---

## 📊 상태 표시

코딩 룰 파일 상단에 상태 표시:

### Auto-Generated

```markdown
> 자동 생성 일시: 2026-03-12 10:30:00
> 프레임워크 버전: latest
> 상태: 🤖 Auto-Generated
```

### Verified

```markdown
> 최초 생성: 2026-01-15
> 검증 일시: 2026-02-20
> 프레임워크 버전: 1.8.0
> 상태: ⭐ Verified
```

### Community

```markdown
> 기여자: @username
> 검증 일시: 2026-03-01
> 프레임워크 버전: 2.3.0
> 상태: 🌍 Community
```

---

**다음 단계**: `general-coding-rules.md` 작성 필요
