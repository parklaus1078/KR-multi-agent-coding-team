# Refactor Code Skill

> **목적**: 코드 개선 제안 - 리팩토링 패턴 자동 감지 및 적용
>
> **타입**: Code Quality Skill
>
> **Thariq 교훈**: "Scripts for repetitive refactoring"

---

## 🎯 트리거

### 자동 트리거
- Auto-pipeline: Coding Agent 완료 후 (선택)
- Git hook: pre-commit (선택)
- 주간 cron: 코드베이스 전체 분석

### 수동 트리거
```bash
# 특정 파일 리팩토링
bash scripts/run-skill.sh refactor-code --file src/auth/login.js

# 특정 디렉토리 리팩토링
bash scripts/run-skill.sh refactor-code --dir src/auth/

# 전체 프로젝트 리팩토링
bash scripts/run-skill.sh refactor-code --all

# Dry-run (제안만)
bash scripts/run-skill.sh refactor-code --file src/auth/login.js --dry-run
```

---

## 🔍 감지 패턴

### 1. 코드 스멜 (Code Smells)

#### Long Method
**감지**:
- 함수 길이 > 50줄
- 중첩 깊이 > 3

**제안**:
```javascript
// Before
function processUser(user) {
  // 80 lines of code...
}

// After
function processUser(user) {
  validateUser(user);
  enrichUserData(user);
  saveUser(user);
}

function validateUser(user) { ... }
function enrichUserData(user) { ... }
function saveUser(user) { ... }
```

#### Duplicate Code
**감지**:
- 6줄 이상 중복

**제안**:
```javascript
// Before
function loginUser(credentials) {
  const token = jwt.sign(credentials, SECRET);
  const expiry = Date.now() + 3600000;
  return { token, expiry };
}

function refreshToken(oldToken) {
  const token = jwt.sign(payload, SECRET);
  const expiry = Date.now() + 3600000;
  return { token, expiry };
}

// After
function createTokenResponse(data) {
  const token = jwt.sign(data, SECRET);
  const expiry = Date.now() + 3600000;
  return { token, expiry };
}

function loginUser(credentials) {
  return createTokenResponse(credentials);
}

function refreshToken(oldToken) {
  return createTokenResponse(payload);
}
```

#### Magic Numbers
**감지**:
- 2자리 이상 숫자 리터럴

**제안**:
```javascript
// Before
if (user.age > 18) { ... }
setTimeout(callback, 3600000);

// After
const ADULT_AGE = 18;
const ONE_HOUR_MS = 3600000;

if (user.age > ADULT_AGE) { ... }
setTimeout(callback, ONE_HOUR_MS);
```

#### Large Class / God Object
**감지**:
- 클래스 > 300줄
- 메서드 > 20개

**제안**:
```javascript
// Before
class UserManager {
  // 500 lines
  // 30 methods
}

// After
class UserManager {
  constructor() {
    this.validator = new UserValidator();
    this.repository = new UserRepository();
    this.notifier = new UserNotifier();
  }
}

class UserValidator { ... }
class UserRepository { ... }
class UserNotifier { ... }
```

### 2. 리팩토링 패턴

#### Extract Function
**시나리오**: 긴 함수, 중복 로직

```python
# Before
def process_order(order):
    # Validation
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

    # Processing
    for item in order.items:
        item.calculate_tax()
        item.apply_discount()

    # Saving
    db.save(order)
    send_confirmation(order)

# After
def process_order(order):
    validate_order(order)
    process_items(order.items)
    finalize_order(order)

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

def process_items(items):
    for item in items:
        item.calculate_tax()
        item.apply_discount()

def finalize_order(order):
    db.save(order)
    send_confirmation(order)
```

#### Replace Conditional with Polymorphism
**시나리오**: 타입 체크 반복

```javascript
// Before
function getArea(shape) {
  if (shape.type === 'circle') {
    return Math.PI * shape.radius ** 2;
  } else if (shape.type === 'rectangle') {
    return shape.width * shape.height;
  } else if (shape.type === 'triangle') {
    return 0.5 * shape.base * shape.height;
  }
}

// After
class Shape {
  getArea() { throw new Error('Not implemented'); }
}

class Circle extends Shape {
  getArea() { return Math.PI * this.radius ** 2; }
}

class Rectangle extends Shape {
  getArea() { return this.width * this.height; }
}

class Triangle extends Shape {
  getArea() { return 0.5 * this.base * this.height; }
}
```

#### Simplify Conditional
**시나리오**: 복잡한 조건문

```python
# Before
if user.age >= 18 and user.country == 'US' and user.verified == True:
    allow_access()

# After
def is_eligible_user(user):
    return (
        user.age >= 18 and
        user.country == 'US' and
        user.verified
    )

if is_eligible_user(user):
    allow_access()
```

#### Replace Loop with Pipeline
**시나리오**: 명령형 루프 → 선언형

```javascript
// Before
const adults = [];
for (let i = 0; i < users.length; i++) {
  if (users[i].age >= 18) {
    adults.push(users[i].name);
  }
}

// After
const adults = users
  .filter(user => user.age >= 18)
  .map(user => user.name);
```

### 3. 성능 개선

#### Avoid N+1 Queries
```python
# Before
users = User.all()
for user in users:
    user.posts  # N+1 query

# After
users = User.includes(:posts).all()
```

#### Use Caching
```javascript
// Before
function getExpensiveData(id) {
  return database.query(`SELECT * FROM large_table WHERE id = ${id}`);
}

// After
const cache = new Map();

function getExpensiveData(id) {
  if (cache.has(id)) {
    return cache.get(id);
  }

  const data = database.query(`SELECT * FROM large_table WHERE id = ${id}`);
  cache.set(id, data);
  return data;
}
```

#### Parallel Processing
```javascript
// Before
const result1 = await fetchData1();
const result2 = await fetchData2();
const result3 = await fetchData3();

// After
const [result1, result2, result3] = await Promise.all([
  fetchData1(),
  fetchData2(),
  fetchData3()
]);
```

---

## 📤 출력 형식

### 리팩토링 리포트

```markdown
# Refactoring Report: src/auth/login.js

## Summary
- **Issues Found**: 5
- **Auto-fixable**: 2
- **Complexity Reduction**: 15 → 8
- **Estimated Time**: 30 minutes

---

## Suggestions

### 1. Extract Function: Separate Validation Logic
**Severity**: 🟡 Medium
**Lines**: 45-65
**Complexity**: 12 → 6

**Current Code**:
```javascript
function handleLogin(credentials) {
  // 20 lines of validation
  if (!credentials.email) throw new Error('Email required');
  if (!credentials.password) throw new Error('Password required');
  if (credentials.password.length < 8) throw new Error('Password too short');
  // ... more validation

  // 15 lines of login logic
  const user = await findUser(credentials.email);
  // ...
}
```

**Suggested**:
```javascript
function handleLogin(credentials) {
  validateCredentials(credentials);
  return performLogin(credentials);
}

function validateCredentials(credentials) {
  if (!credentials.email) throw new Error('Email required');
  if (!credentials.password) throw new Error('Password required');
  if (credentials.password.length < 8) throw new Error('Password too short');
}

function performLogin(credentials) {
  const user = await findUser(credentials.email);
  // ...
}
```

**Benefits**:
- Complexity: 12 → 6
- Readability: +++
- Testability: +++

**Auto-fix**: ❌ Manual refactoring needed

---

### 2. Replace Magic Number
**Severity**: 🟢 Low
**Line**: 23

**Current**:
```javascript
if (user.loginAttempts > 5) {
  lockAccount(user);
}
```

**Suggested**:
```javascript
const MAX_LOGIN_ATTEMPTS = 5;

if (user.loginAttempts > MAX_LOGIN_ATTEMPTS) {
  lockAccount(user);
}
```

**Auto-fix**: ✅ Available

---

### 3. Use Parallel Processing
**Severity**: 🟡 Medium
**Lines**: 78-80

**Current**:
```javascript
const user = await fetchUser(id);
const permissions = await fetchPermissions(id);
const settings = await fetchSettings(id);
```

**Suggested**:
```javascript
const [user, permissions, settings] = await Promise.all([
  fetchUser(id),
  fetchPermissions(id),
  fetchSettings(id)
]);
```

**Benefits**:
- Performance: 3x faster (serial → parallel)

**Auto-fix**: ✅ Available

---

## Auto-fix Available (2)

Run: `bash scripts/run-skill.sh refactor-code --file src/auth/login.js --auto-fix`

Fixes:
1. Replace magic number (line 23)
2. Use parallel processing (lines 78-80)
```

---

## 🔧 Auto-Fix 기능

### 수정 가능한 패턴

1. **Magic Numbers → Constants**
2. **Serial → Parallel Async**
3. **Import 정렬**
4. **불필요한 else 제거**
5. **var → const/let**

### Auto-fix 실행

```bash
# 자동 수정 적용
bash scripts/run-skill.sh refactor-code --file src/auth/login.js --auto-fix

# Dry-run
bash scripts/run-skill.sh refactor-code --file src/auth/login.js --auto-fix --dry-run
```

---

## 🧠 메모리 활용

### refactor-patterns.json

```json
{
  "project": "my-project",
  "applied_patterns": [
    {
      "pattern": "extract_function",
      "file": "src/auth/login.js",
      "before_complexity": 12,
      "after_complexity": 6,
      "timestamp": "2026-03-19T10:00:00Z",
      "success": true
    }
  ],
  "common_smells": [
    {
      "smell": "long_method",
      "frequency": 15,
      "avg_length": 75
    }
  ],
  "metrics": {
    "avg_complexity_before": 10.5,
    "avg_complexity_after": 7.2,
    "improvement": "31%"
  }
}
```

---

## ⚠️ Gotchas

### 1. 테스트 커버리지 유지

**검증**:
```python
# 리팩토링 전 커버리지
before_coverage = run_tests()

# 리팩토링 적용
apply_refactoring()

# 리팩토링 후 커버리지
after_coverage = run_tests()

if after_coverage < before_coverage:
    rollback_refactoring()
    raise Error("리팩토링으로 커버리지 감소")
```

### 2. Breaking Change 방지

**검증**:
```python
# 공개 API 시그니처 변경 금지
if is_public_api(function) and signature_changed(function):
    raise Error("공개 API 시그니처 변경 불가")
```

### 3. 과도한 추상화 방지

**규칙**:
- 함수/클래스가 1곳에서만 사용되면 추출 안 함
- 중복이 3회 이상일 때만 추출 ("Rule of Three")

---

## 📊 기대 효과

### Before (수동 리팩토링)

```
코드 스멜 발견 → 수동 분석 → 수동 수정
    ↓
- 시간 소요 (수 시간)
- 일관성 없음
- 놓치는 패턴 많음
```

### After (자동 리팩토링)

```
코드 작성 → refactor-code skill
         ↓
       제안 (1-2분)
         ↓
       Auto-fix 또는 수동 적용
```

### 수치 목표

| 항목 | 목표 |
|------|------|
| **복잡도 감소** | **-30%** |
| **리팩토링 시간** | **-70%** |
| **코드 스멜 감지** | **90%+** |
| **유지보수성** | **+50%** |

---

## 🔗 통합

### Coding Agent 통합

```python
# auto_pipeline.py

# Coding Agent 완료 후
result_coding = self.run_agent("coding", coding_prompt, ticket_num)

# Refactor Skill 실행 (선택)
refactor_result = self.run_skill("refactor-code", {
    "files": result_coding["changed_files"]
})

if refactor_result["suggestions"]:
    print(f"💡 {len(refactor_result['suggestions'])}개 리팩토링 제안")

    if refactor_result["auto_fixable"]:
        # Auto-fix 적용
        self.run_skill("refactor-code", auto_fix=True)
```

---

**관련 문서**:
- [refactor-code.py](refactor-code.py) - 실제 구현
- [refactor-patterns.json](../../.memory/refactor-patterns.json) - 패턴 데이터
