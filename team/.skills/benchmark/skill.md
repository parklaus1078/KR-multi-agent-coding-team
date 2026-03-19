# Benchmark Skill

> **목적**: 성능 벤치마크 및 회귀 감지
>
> **타입**: Performance Skill
>
> **Thariq 교훈**: "Measure performance to prevent regression"

---

## 🎯 트리거

### 자동 트리거
- Auto-pipeline: 배포 전 (선택)
- Git hook: pre-push (성능 중요 프로젝트)
- CI/CD: PR에서 성능 비교
- Cron: 주간 성능 리포트

### 수동 트리거
```bash
# 전체 벤치마크
bash scripts/run-skill.sh benchmark --all

# 특정 모듈
bash scripts/run-skill.sh benchmark --module auth

# 기준과 비교
bash scripts/run-skill.sh benchmark --compare-to main

# 부하 테스트
bash scripts/run-skill.sh benchmark --load-test --users 1000
```

---

## 🔍 기능

### 1. 성능 메트릭 측정

**측정 항목**:
```python
metrics = {
    # 응답 시간
    "response_time": {
        "p50": 120,  # ms
        "p95": 250,
        "p99": 500,
        "max": 1200
    },

    # 처리량
    "throughput": {
        "requests_per_second": 1000,
        "bytes_per_second": 5000000
    },

    # 리소스 사용량
    "resources": {
        "cpu_percent": 45,
        "memory_mb": 512,
        "disk_io_mb": 100
    },

    # 에러율
    "errors": {
        "rate": 0.001,  # 0.1%
        "total": 10,
        "by_type": {
            "timeout": 5,
            "500": 3,
            "connection": 2
        }
    },

    # 동시성
    "concurrency": {
        "active_connections": 500,
        "max_connections": 1000
    }
}
```

### 2. 벤치마크 시나리오

**API 벤치마크**:
```python
scenarios = {
    "user_login": {
        "endpoint": "/api/login",
        "method": "POST",
        "payload": {"email": "test@example.com", "password": "test123"},
        "expected_time_ms": 200,
        "concurrent_users": 100
    },

    "user_profile": {
        "endpoint": "/api/user/me",
        "method": "GET",
        "auth_required": True,
        "expected_time_ms": 100,
        "concurrent_users": 500
    },

    "search": {
        "endpoint": "/api/search",
        "method": "GET",
        "params": {"q": "test"},
        "expected_time_ms": 300,
        "concurrent_users": 200
    }
}
```

**데이터베이스 벤치마크**:
```python
db_benchmarks = {
    "simple_query": {
        "query": "SELECT * FROM users WHERE id = ?",
        "expected_time_ms": 5
    },

    "complex_join": {
        "query": """
            SELECT u.*, p.*, o.*
            FROM users u
            JOIN profiles p ON u.id = p.user_id
            JOIN orders o ON u.id = o.user_id
            WHERE u.created_at > ?
        """,
        "expected_time_ms": 50
    },

    "bulk_insert": {
        "operation": "INSERT 1000 rows",
        "expected_time_ms": 500
    }
}
```

### 3. 성능 회귀 감지

**비교 분석**:
```python
def detect_regression(current, baseline):
    regressions = []

    # 응답 시간 증가 > 20%
    if current.p95 > baseline.p95 * 1.2:
        regressions.append({
            "metric": "response_time_p95",
            "current": current.p95,
            "baseline": baseline.p95,
            "change_percent": ((current.p95 / baseline.p95) - 1) * 100,
            "severity": "high"
        })

    # 처리량 감소 > 15%
    if current.throughput < baseline.throughput * 0.85:
        regressions.append({
            "metric": "throughput",
            "current": current.throughput,
            "baseline": baseline.throughput,
            "change_percent": ((current.throughput / baseline.throughput) - 1) * 100,
            "severity": "high"
        })

    # 메모리 증가 > 30%
    if current.memory > baseline.memory * 1.3:
        regressions.append({
            "metric": "memory",
            "current": current.memory,
            "baseline": baseline.memory,
            "change_percent": ((current.memory / baseline.memory) - 1) * 100,
            "severity": "medium"
        })

    return regressions
```

### 4. 부하 테스트

**점진적 부하**:
```python
def ramp_up_load_test(endpoint, max_users=1000):
    results = []

    # 단계별 증가: 10 → 100 → 500 → 1000
    for users in [10, 100, 500, 1000]:
        print(f"Testing with {users} concurrent users...")

        result = run_load_test(
            endpoint=endpoint,
            concurrent_users=users,
            duration_seconds=60
        )

        results.append({
            "users": users,
            "avg_response_time": result.avg_response_time,
            "throughput": result.throughput,
            "error_rate": result.error_rate
        })

        # 에러율 > 5%면 중단
        if result.error_rate > 0.05:
            print(f"⚠️ 에러율 초과 at {users} users: {result.error_rate}")
            break

    return results
```

**스파이크 테스트**:
```python
def spike_test(endpoint):
    # 정상 부하
    normal = run_load_test(endpoint, users=100, duration=60)

    # 갑작스런 스파이크 (10배)
    spike = run_load_test(endpoint, users=1000, duration=10)

    # 복구
    recovery = run_load_test(endpoint, users=100, duration=60)

    return {
        "normal": normal,
        "spike": spike,
        "recovery": recovery,
        "recovery_time": calculate_recovery_time(spike, recovery)
    }
```

### 5. 프로파일링

**코드 핫스팟 감지**:
```python
import cProfile
import pstats

def profile_function(func):
    profiler = cProfile.Profile()
    profiler.enable()

    # 함수 실행
    result = func()

    profiler.disable()

    # 결과 분석
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')

    # 상위 10개 느린 함수
    hotspots = stats.print_stats(10)

    return {
        "result": result,
        "hotspots": hotspots
    }
```

---

## 📤 출력 형식

### 벤치마크 리포트

```markdown
# Benchmark Report

## Summary
- **Date**: 2026-03-19T13:00:00Z
- **Branch**: feature/optimize-auth
- **Comparison**: main branch
- **Status**: ⚠️ Performance Regression Detected

---

## Performance Metrics

### Response Time

| Metric | Current | Baseline | Change |
|--------|---------|----------|--------|
| p50 | 125ms | 120ms | +4.2% 🟡 |
| p95 | 310ms | 250ms | +24% 🔴 |
| p99 | 650ms | 500ms | +30% 🔴 |
| max | 1500ms | 1200ms | +25% 🔴 |

### Throughput

| Metric | Current | Baseline | Change |
|--------|---------|----------|--------|
| Requests/sec | 850 | 1000 | -15% 🔴 |
| Bytes/sec | 4.2MB | 5.0MB | -16% 🔴 |

### Resources

| Metric | Current | Baseline | Change |
|--------|---------|----------|--------|
| CPU | 52% | 45% | +15.6% 🟡 |
| Memory | 680MB | 512MB | +32.8% 🔴 |
| Disk I/O | 95MB | 100MB | -5% ✅ |

---

## Regressions Detected (4)

### 🔴 Critical: Response Time p95 (+24%)
**Impact**: High
**Affected**: /api/login, /api/user/me
**Baseline**: 250ms
**Current**: 310ms

**Root Cause Analysis**:
- Profiling shows new database query in auth middleware
- N+1 query detected

**Recommendation**:
```python
# Before
for user in users:
    user.permissions  # N+1 query

# After
users = User.includes('permissions').all()  # Eager load
```

---

### 🔴 Critical: Memory Usage (+33%)
**Impact**: High
**Baseline**: 512MB
**Current**: 680MB

**Root Cause**:
- Memory leak in session storage
- Cache not being cleared

**Recommendation**:
```python
# Add cache cleanup
def cleanup_old_sessions():
    sessions.delete_where(age > 24_hours)
```

---

### 🔴 High: Throughput (-15%)
**Impact**: High
**Baseline**: 1000 req/s
**Current**: 850 req/s

**Related to**: Response time regression

---

## Load Test Results

### Concurrent Users Test

| Users | Avg Response | Throughput | Error Rate |
|-------|--------------|------------|------------|
| 10 | 95ms | 105 req/s | 0% ✅ |
| 100 | 125ms | 850 req/s | 0.1% ✅ |
| 500 | 310ms | 1200 req/s | 1.2% 🟡 |
| 1000 | 650ms | 1100 req/s | 5.5% 🔴 |

**Max Capacity**: ~500 users (error rate < 2%)

---

## Hotspots (Top 5 Slow Functions)

| Function | Cumulative Time | Calls | Time/Call |
|----------|-----------------|-------|-----------|
| auth.check_permissions | 2.5s | 1000 | 2.5ms |
| db.query_users | 1.8s | 1500 | 1.2ms |
| cache.get | 1.2s | 5000 | 0.24ms |
| json.serialize | 0.9s | 2000 | 0.45ms |
| logging.write | 0.5s | 10000 | 0.05ms |

---

## Recommendations

1. 🔴 **Fix N+1 query** in auth middleware (High priority)
2. 🔴 **Fix memory leak** in session storage (High priority)
3. 🟡 **Optimize cache** strategy (Medium priority)
4. 🟢 **Consider CDN** for static assets (Low priority)

---

## Approval Status

❌ **Performance regression detected - Changes not recommended for merge**

Fix critical issues before merging.
```

---

## 🧠 메모리 활용

### benchmark-history.json

```json
{
  "version": "0.0.1",
  "project": "multi-agent-coding-team",

  "baseline": {
    "branch": "main",
    "commit": "abc123",
    "timestamp": "2026-03-15T10:00:00Z",
    "metrics": {
      "response_time_p95": 250,
      "throughput": 1000,
      "memory_mb": 512
    }
  },

  "benchmark_runs": [
    {
      "branch": "feature/optimize-auth",
      "commit": "def456",
      "timestamp": "2026-03-19T13:00:00Z",
      "metrics": {
        "response_time_p95": 310,
        "throughput": 850,
        "memory_mb": 680
      },
      "regressions": [
        {
          "metric": "response_time_p95",
          "change_percent": 24,
          "severity": "critical"
        }
      ]
    }
  ],

  "performance_trend": [
    {"date": "2026-03-01", "p95": 280},
    {"date": "2026-03-08", "p95": 265},
    {"date": "2026-03-15", "p95": 250},
    {"date": "2026-03-19", "p95": 310}
  ],

  "known_bottlenecks": [
    {
      "name": "auth.check_permissions",
      "avg_time_ms": 2.5,
      "frequency": "high",
      "optimization_attempted": false
    }
  ]
}
```

---

## ⚠️ Gotchas

### 1. 회귀 임계값 설정

**원칙**:
- 응답 시간: +20% → 🔴 차단
- 처리량: -15% → 🔴 차단
- 메모리: +30% → 🟡 경고
- CPU: +20% → 🟡 경고

### 2. 실제 환경과 유사하게

**검증**:
```python
# ❌ 잘못: 로컬에서만 테스트
run_benchmark(env="local")

# ✅ 올바름: 실제 환경과 유사한 데이터
run_benchmark(
    env="staging",
    data_volume=production_data_volume,
    concurrent_users=production_avg_users
)
```

### 3. 캐시 워밍업

**원칙**:
```python
# 벤치마크 전 캐시 워밍업
def warmup_cache():
    # 주요 쿼리 미리 실행
    for query in common_queries:
        execute(query)

    # 충분한 대기
    time.sleep(5)

# 워밍업 후 측정
warmup_cache()
run_benchmark()
```

### 4. 외부 의존성 제어

**원칙**:
- 외부 API는 Mock
- 데이터베이스는 전용 인스턴스
- 네트워크 지연 시뮬레이션

---

## 📊 기대 효과

### Before (수동 벤치마크)

```
배포 → 프로덕션에서 느림 감지 (수 시간~수 일 후)
   → 롤백
   → 원인 분석
   → 수정
```

**문제점**:
- ❌ 늦은 감지 (이미 배포 후)
- ❌ 사용자 영향
- ❌ 원인 분석 어려움

### After (자동 벤치마크)

```
PR 생성 → benchmark skill (자동)
       → 회귀 감지 (2분)
       → PR 차단
       → 수정 후 재테스트
```

**개선점**:
- ✅ 즉시 감지 (배포 전)
- ✅ 사용자 영향 없음
- ✅ 자동 원인 분석

### 수치 목표

| 항목 | 목표 |
|------|------|
| **성능 회귀 감지** | **100%** (배포 전) |
| **사용자 영향** | **0%** |
| **분석 시간** | **-80%** (자동) |
| **프로덕션 롤백** | **-90%** |

---

## 🔗 통합

### Auto-pipeline 통합

```python
# auto_pipeline.py

# 배포 전 벤치마크 (선택)
if env == "production":
    print("🔬 성능 벤치마크 실행 중...")

    benchmark_result = self.run_skill("benchmark", {
        "compare_to": "main"
    })

    if benchmark_result["regressions"]:
        critical = [r for r in benchmark_result["regressions"] if r["severity"] == "critical"]

        if critical:
            print(f"❌ 성능 회귀 감지: {len(critical)}개")
            print("   배포 차단")
            raise Exception("성능 회귀 - 수정 필요")

        print(f"⚠️  경고: {len(benchmark_result['regressions'])}개 회귀")
    else:
        print("✅ 성능 회귀 없음")
```

### GitHub Actions 통합

```yaml
# .github/workflows/benchmark.yml
name: Performance Benchmark

on: [pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Checkout base branch
        run: git fetch origin ${{ github.base_ref }}

      - name: Run benchmark
        run: |
          bash scripts/run-skill.sh benchmark --compare-to origin/${{ github.base_ref }}

      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('benchmark-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

---

**관련 문서**:
- [benchmark.py](benchmark.py) - 실제 구현
- [benchmark-history.json](../../.memory/benchmark-history.json) - 벤치마크 히스토리
- [benchmark-config.json](benchmark-config.json) - 벤치마크 설정
