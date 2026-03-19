# Library 워크플로우

> **프로젝트 타입**: library (예: npm 패키지, Python 패키지, Rust crate)
>
> **적용 조건**: `.project-meta.json`의 `project_type`이 `"library"`인 경우

---

## 📂 산출물 구조

```
projects/{current_project}/planning/specs/
├── api/
│   └── PLAN-{번호}-{slug}.md          # 공개 API 명세서
├── examples/
│   └── PLAN-{번호}-{slug}.md          # 사용 예시
└── test-cases/
    ├── PLAN-{번호}-api.md             # API 테스트 케이스
    └── PLAN-{번호}-examples.md        # 예시 코드 검증 테스트
```

---

## 🔨 작업 순서

### Step 1: 티켓 분석

티켓에서 다음 항목을 추출:
- [ ] 함수/클래스/메서드명
- [ ] 파라미터와 타입
- [ ] 반환값
- [ ] 예외/에러
- [ ] 사용 시나리오

---

### Step 2: 산출물 목록 제시

```
프로젝트: {current_project} (library)
티켓: PLAN-{번호}-{slug}

생성 예정 파일:
- specs/api/PLAN-{번호}-{slug}.md
- specs/examples/PLAN-{번호}-{slug}.md
- specs/test-cases/PLAN-{번호}-api.md
- specs/test-cases/PLAN-{번호}-examples.md

주요 API: parse(), validate(), transform()
예시: 기본 사용, 옵션 사용, 에러 처리

계속 진행하시겠습니까? (yes/no)
```

---

### Step 3-1: 공개 API 명세서

**파일**: `specs/api/PLAN-{번호}-{slug}.md`

```markdown
# {함수/클래스명} API 명세서

## 함수 시그니처

\`\`\`typescript
function parse(input: string, options?: ParseOptions): ParseResult
\`\`\`

## 파라미터

| 이름 | 타입 | 필수 | 설명 | 기본값 |
|------|------|------|------|--------|
| input | string | Y | 파싱할 입력 문자열 | - |
| options | ParseOptions | N | 파싱 옵션 | {} |
| options.strict | boolean | N | 엄격 모드 | false |
| options.encoding | string | N | 인코딩 | 'utf-8' |

## 반환값

| 타입 | 설명 |
|------|------|
| ParseResult | 파싱 결과 객체 |

**ParseResult 구조**:
\`\`\`typescript
interface ParseResult {
  success: boolean;
  data: any;
  errors: ParseError[];
}
\`\`\`

## 예외

| 예외 타입 | 발생 조건 | 예시 |
|----------|----------|------|
| ParseError | 입력 형식이 잘못된 경우 | `throw new ParseError("Invalid format at line 5")` |
| TypeError | 잘못된 타입 전달 | `parse(123)` → TypeError |

## 동작 설명

1. 입력 문자열 유효성 검사
2. 옵션 병합 (기본값 + 사용자 제공)
3. 파싱 수행
4. 결과 반환 또는 예외 발생

## 성능 특성

- **시간 복잡도**: O(n), n = 입력 문자열 길이
- **공간 복잡도**: O(n)
- **처리량**: ~10MB/s (평균)

## 부작용

- 없음 (순수 함수)

## 스레드 안전성

- 안전 (상태를 변경하지 않음)
```

---

### Step 3-2: 사용 예시

**파일**: `specs/examples/PLAN-{번호}-{slug}.md`

```markdown
# {함수명} 사용 예시

## 기본 사용

\`\`\`typescript
import { parse } from 'my-library';

const input = "name: John\\nage: 30";
const result = parse(input);

console.log(result.data);
// { name: "John", age: 30 }
\`\`\`

## 옵션 사용

### 엄격 모드

\`\`\`typescript
const result = parse(input, { strict: true });

// 엄격 모드에서는 미정의 필드 시 에러
\`\`\`

### 커스텀 인코딩

\`\`\`typescript
const result = parse(input, { encoding: 'latin1' });
\`\`\`

## 에러 처리

\`\`\`typescript
try {
  const result = parse("invalid input");
  if (!result.success) {
    console.error(result.errors);
  }
} catch (error) {
  if (error instanceof ParseError) {
    console.error('Parse failed:', error.message);
  }
}
\`\`\`

## 고급 사용

### 파이프라인 체이닝

\`\`\`typescript
const result = parse(input)
  .transform(data => data.filter(x => x.age > 18))
  .validate(schema);
\`\`\`

### 스트림 처리

\`\`\`typescript
const stream = fs.createReadStream('large-file.txt');
const results = await parseStream(stream);
\`\`\`

## 실제 사용 사례

### 설정 파일 파싱

\`\`\`typescript
const configFile = fs.readFileSync('config.txt', 'utf-8');
const config = parse(configFile);
app.configure(config.data);
\`\`\`

### API 응답 처리

\`\`\`typescript
const response = await fetch('/api/data');
const text = await response.text();
const parsed = parse(text);
\`\`\`
```

---

### Step 3-3: 테스트 케이스

#### API 테스트

**파일**: `specs/test-cases/PLAN-{번호}-api.md`

```markdown
# {함수명} API 테스트 케이스

## 정상 케이스

| ID | 시나리오 | 입력 | 기대 반환값 |
|----|---------|------|-----------|
| TC-API-001 | 기본 사용 | `parse("name: John")` | `{ success: true, data: { name: "John" } }` |
| TC-API-002 | 옵션 사용 | `parse(input, { strict: true })` | strict 모드 적용 |

## 예외 케이스

| ID | 시나리오 | 입력 | 기대 예외 |
|----|---------|------|----------|
| TC-API-101 | 빈 문자열 | `parse("")` | `ParseError: "Empty input"` |
| TC-API-102 | null 입력 | `parse(null)` | `TypeError` |
| TC-API-103 | 잘못된 형식 | `parse("invalid:::")` | `ParseError: "Invalid format"` |

## 엣지 케이스

| ID | 시나리오 | 입력 | 기대 결과 |
|----|---------|------|----------|
| TC-API-201 | 매우 긴 문자열 | 10MB 문자열 | 성능 저하 없이 처리 |
| TC-API-202 | 특수 문자 | `parse("emoji 😀")` | 올바르게 파싱 |
| TC-API-203 | 유니코드 | `parse("한글 테스트")` | 올바르게 파싱 |
```

#### 예시 검증 테스트

**파일**: `specs/test-cases/PLAN-{번호}-examples.md`

```markdown
# {함수명} 예시 코드 검증 테스트

## README 예시 실행 테스트

| ID | 예시 | 기대 결과 |
|----|------|----------|
| TC-EX-001 | README의 기본 사용 예시 | 에러 없이 실행 |
| TC-EX-002 | README의 고급 사용 예시 | 문서화된 결과와 일치 |

## 문서 예시 검증

| ID | 예시 위치 | 테스트 방법 |
|----|----------|----------|
| TC-EX-101 | API 문서의 모든 코드 스니펫 | 복사-붙여넣기로 실행 가능 |
| TC-EX-102 | 블로그 포스트 예시 | 실제 동작과 일치 |
```

---

## ✅ 완료 체크리스트

- [ ] 공개 API 명세서 생성 (함수 시그니처, 파라미터, 반환값)
- [ ] 사용 예시 생성 (기본, 옵션, 에러 처리, 고급)
- [ ] API 테스트 케이스 (정상, 예외, 엣지)
- [ ] 예시 검증 테스트 케이스
- [ ] 성능 특성 문서화
- [ ] 예외 타입 명확히 정의
- [ ] 로그 파일 생성

---

## 🔍 Library 특수 체크 사항

### API 설계 원칙
- **간결성**: 필수 파라미터만, 옵션은 선택
- **일관성**: 네이밍 규칙 통일
- **예측 가능성**: 동작이 직관적
- **확장성**: 옵션으로 기능 확장

### 문서화 필수 항목
- [ ] 함수 시그니처 (타입 포함)
- [ ] 파라미터 설명 (필수/선택, 기본값)
- [ ] 반환값 구조
- [ ] 예외 목록
- [ ] 사용 예시 (최소 3개)

### 버전 호환성
- Breaking change 여부 명시
- Deprecated API 표시
- 마이그레이션 가이드 (필요 시)

---

**관련 문서**:
- [gotchas.md](../gotchas.md)
- [CLAUDE.md](../CLAUDE.md)
