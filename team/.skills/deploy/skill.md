# Deploy Skill

> **목적**: 배포 자동화 및 안전 검증
>
> **타입**: Deployment Skill
>
> **Thariq 교훈**: "Automate deployment with safety checks"

---

## 🎯 트리거

### 자동 트리거
- Auto-pipeline: PR 머지 후 (선택)
- GitHub Actions: main 브랜치 푸시
- Cron: 정기 배포 (예: 매주 금요일)

### 수동 트리거
```bash
# 개발 환경 배포
bash scripts/run-skill.sh deploy --env dev

# 스테이징 배포
bash scripts/run-skill.sh deploy --env staging

# 프로덕션 배포 (안전 검사 포함)
bash scripts/run-skill.sh deploy --env production

# Dry-run (미리보기)
bash scripts/run-skill.sh deploy --env production --dry-run

# 롤백
bash scripts/run-skill.sh deploy --rollback --env production
```

---

## 🔍 기능

### 1. 환경별 배포 전략

**환경 구분**:
```json
{
  "dev": {
    "auto_deploy": true,
    "tests_required": false,
    "approval_required": false,
    "url": "https://dev.example.com"
  },
  "staging": {
    "auto_deploy": true,
    "tests_required": true,
    "approval_required": false,
    "url": "https://staging.example.com"
  },
  "production": {
    "auto_deploy": false,
    "tests_required": true,
    "approval_required": true,
    "smoke_tests": true,
    "canary": true,
    "rollback_enabled": true,
    "url": "https://example.com"
  }
}
```

### 2. 배포 전 검증

**체크리스트**:
```python
def pre_deploy_checks(env):
    checks = []

    # 1. 테스트 통과
    if env.tests_required:
        test_result = run_tests()
        if not test_result.all_passed:
            return {"status": "blocked", "reason": "테스트 실패"}

    # 2. 브랜치 확인
    if env == "production":
        current_branch = get_current_branch()
        if current_branch != "main":
            return {"status": "blocked", "reason": "main 브랜치만 프로덕션 배포"}

    # 3. 미머지 변경사항 확인
    if has_uncommitted_changes():
        return {"status": "blocked", "reason": "커밋되지 않은 변경사항"}

    # 4. 환경 변수 확인
    required_vars = get_required_env_vars(env)
    missing_vars = [v for v in required_vars if not os.getenv(v)]
    if missing_vars:
        return {"status": "blocked", "reason": f"환경 변수 누락: {missing_vars}"}

    # 5. 의존성 확인
    if has_dependency_conflicts():
        return {"status": "warning", "reason": "의존성 충돌 가능"}

    return {"status": "ready"}
```

### 3. 배포 전략

#### Blue-Green Deployment
```python
def blue_green_deploy(env):
    # 1. Green 환경에 새 버전 배포
    deploy_to_green(env)

    # 2. Smoke test
    if not run_smoke_tests(green_url):
        rollback_to_blue()
        return {"status": "failed", "reason": "Smoke test 실패"}

    # 3. 트래픽 전환
    switch_traffic_to_green()

    # 4. Blue 환경 유지 (롤백용)
    keep_blue_for_rollback(hours=24)
```

#### Canary Deployment
```python
def canary_deploy(env):
    # 1. 10% 트래픽만 새 버전으로
    deploy_canary(traffic_percent=10)

    # 2. 모니터링 (10분)
    metrics = monitor_canary(duration_minutes=10)

    # 3. 에러율 확인
    if metrics.error_rate > 1%:
        rollback_canary()
        return {"status": "failed", "reason": "에러율 초과"}

    # 4. 점진적 증가 (50% → 100%)
    increase_canary_traffic(50)
    monitor_canary(duration_minutes=10)

    increase_canary_traffic(100)
```

#### Rolling Deployment
```python
def rolling_deploy(env):
    instances = get_instances(env)

    for instance in instances:
        # 1. 인스턴스 제거
        remove_from_load_balancer(instance)

        # 2. 새 버전 배포
        deploy_to_instance(instance)

        # 3. Health check
        if not health_check(instance):
            rollback_instance(instance)
            return {"status": "failed", "reason": f"{instance} 배포 실패"}

        # 4. 로드 밸런서에 추가
        add_to_load_balancer(instance)

        # 5. 다음 인스턴스 (대기)
        wait(seconds=30)
```

### 4. Smoke Tests

**배포 후 자동 검증**:
```python
def run_smoke_tests(url):
    tests = [
        # 1. Health check
        {"name": "Health", "endpoint": "/health", "expected": 200},

        # 2. 주요 API 동작
        {"name": "Login", "endpoint": "/api/login", "method": "POST"},
        {"name": "User Profile", "endpoint": "/api/user/me", "method": "GET"},

        # 3. 데이터베이스 연결
        {"name": "DB Connection", "check": lambda: db.ping()}
    ]

    for test in tests:
        result = run_test(test, url)
        if not result.passed:
            return {"status": "failed", "test": test.name}

    return {"status": "passed"}
```

### 5. 롤백

**자동 롤백 조건**:
```python
def should_auto_rollback(metrics):
    # 1. 에러율 > 5%
    if metrics.error_rate > 0.05:
        return True

    # 2. 응답 시간 > 2x 이전
    if metrics.response_time > previous_metrics.response_time * 2:
        return True

    # 3. 5xx 에러 > 10개/분
    if metrics.server_errors_per_min > 10:
        return True

    return False
```

**롤백 실행**:
```bash
# 이전 버전으로 즉시 롤백
bash scripts/run-skill.sh deploy --rollback --env production

# 특정 버전으로 롤백
bash scripts/run-skill.sh deploy --rollback --version v1.2.3 --env production
```

---

## 📤 출력 형식

### 배포 리포트

```markdown
# Deployment Report: Production

## Summary
- **Environment**: Production
- **Version**: v1.3.0
- **Strategy**: Canary (10% → 50% → 100%)
- **Status**: ✅ Success
- **Duration**: 15 minutes
- **Deployed At**: 2026-03-19T12:00:00Z

---

## Pre-Deploy Checks

✅ All tests passed (150/150)
✅ Coverage: 85%
✅ Branch: main
✅ No uncommitted changes
✅ Environment variables: OK
✅ Dependencies: OK

---

## Deployment Steps

### 1. Canary Deploy (10%)
- **Started**: 12:00:00
- **Traffic**: 10%
- **Monitoring**: 10 minutes
- **Error Rate**: 0.05% ✅
- **Response Time**: 120ms ✅

### 2. Increase to 50%
- **Started**: 12:10:00
- **Traffic**: 50%
- **Monitoring**: 10 minutes
- **Error Rate**: 0.03% ✅
- **Response Time**: 118ms ✅

### 3. Full Deployment (100%)
- **Started**: 12:20:00
- **Traffic**: 100%
- **Status**: ✅ Complete

---

## Smoke Tests

✅ Health check: /health → 200 OK
✅ Login API: /api/login → 200 OK
✅ User Profile: /api/user/me → 200 OK
✅ Database: Connection OK

---

## Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Response Time | 125ms | 118ms | -5.6% ✅ |
| Error Rate | 0.02% | 0.03% | +0.01% ✅ |
| Throughput | 1000 req/s | 1050 req/s | +5% ✅ |
| Memory | 1.2GB | 1.1GB | -8% ✅ |

---

## Rollback Plan

Previous version: v1.2.9
Rollback command:
```bash
bash scripts/run-skill.sh deploy --rollback --version v1.2.9 --env production
```

Rollback available for: 24 hours

---

## Next Steps

1. ✅ Monitor metrics for 24 hours
2. ✅ Keep v1.2.9 for rollback
3. ⬜ Remove old version after 24h
```

---

## 🧠 메모리 활용

### deploy-history.json

```json
{
  "version": "0.0.1",
  "project": "multi-agent-coding-team",

  "deployments": [
    {
      "version": "v1.3.0",
      "env": "production",
      "timestamp": "2026-03-19T12:00:00Z",
      "strategy": "canary",
      "duration_minutes": 15,
      "status": "success",
      "metrics": {
        "error_rate_before": 0.02,
        "error_rate_after": 0.03,
        "response_time_before": 125,
        "response_time_after": 118
      }
    }
  ],

  "rollbacks": [
    {
      "timestamp": "2026-03-10T14:30:00Z",
      "from_version": "v1.2.5",
      "to_version": "v1.2.4",
      "reason": "Error rate spike: 5%",
      "duration_minutes": 2
    }
  ],

  "success_rate": {
    "dev": 1.0,
    "staging": 0.98,
    "production": 0.95
  },

  "avg_deployment_time": {
    "dev": 5,
    "staging": 8,
    "production": 15
  },

  "common_failures": [
    {
      "reason": "Smoke test failure",
      "frequency": 3,
      "last_occurrence": "2026-03-15T10:00:00Z"
    }
  ]
}
```

---

## ⚠️ Gotchas

### 1. 프로덕션 배포는 main 브랜치만

**검증**:
```python
if env == "production":
    current_branch = get_current_branch()
    if current_branch != "main":
        raise Error(f"프로덕션은 main 브랜치만 배포 가능 (현재: {current_branch})")
```

### 2. 배포 전 승인 필수 (프로덕션)

**워크플로우**:
```python
if env == "production" and not has_approval():
    print("배포 승인 필요:")
    print(f"  버전: {version}")
    print(f"  변경사항: {changelog}")

    approval = input("배포하시겠습니까? (yes/no): ")
    if approval != "yes":
        return {"status": "cancelled"}
```

### 3. 롤백 계획 필수

**원칙**:
- 이전 버전 최소 24시간 유지
- 롤백 명령어 리포트에 포함
- 자동 롤백 조건 설정

### 4. 환경 변수 검증

**검증**:
```python
required_env_vars = {
    "production": [
        "DATABASE_URL",
        "API_KEY",
        "SECRET_KEY",
        "REDIS_URL"
    ],
    "staging": [
        "DATABASE_URL",
        "API_KEY"
    ]
}

missing = [v for v in required_env_vars[env] if not os.getenv(v)]
if missing:
    raise Error(f"환경 변수 누락: {missing}")
```

---

## 📊 기대 효과

### Before (수동 배포)

```
코드 머지 → 수동 빌드 (10분)
       → 수동 배포 (15분)
       → 수동 검증 (10분)
       → 에러 발견 (수 시간 후)
       → 수동 롤백 (20분)
```

**문제점**:
- ❌ 시간 소요 (1시간+)
- ❌ 수동 실수 가능
- ❌ 롤백 느림
- ❌ 일관성 없음

### After (자동 배포)

```
PR 머지 → deploy skill (자동)
       → Pre-deploy 검증 (1분)
       → Canary 배포 (15분)
       → Smoke tests (1분)
       → 자동 롤백 (에러 시)
```

**개선점**:
- ✅ 빠름 (20분 이내)
- ✅ 100% 일관성
- ✅ 자동 롤백 (2분)
- ✅ 안전성 검증

### 수치 목표

| 항목 | 목표 |
|------|------|
| **배포 시간** | **-60%** |
| **배포 실패율** | **-80%** |
| **롤백 시간** | **-90%** (2분) |
| **다운타임** | **0** (Blue-Green) |

---

## 🔗 통합

### Auto-pipeline 통합

```python
# auto_pipeline.py

# PR 머지 후
if pr_merged and env == "staging":
    # 자동 배포 (staging)
    deploy_result = self.run_skill("deploy", {
        "env": "staging",
        "auto_deploy": True
    })

    if deploy_result["status"] == "success":
        print(f"✅ Staging 배포 완료: {deploy_result['url']}")
    else:
        print(f"❌ 배포 실패: {deploy_result['reason']}")

# 프로덕션은 수동 승인
if env == "production":
    print("프로덕션 배포 준비 완료")
    print(f"  명령: bash scripts/run-skill.sh deploy --env production")
```

### GitHub Actions 통합

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to staging
        run: |
          bash scripts/run-skill.sh deploy --env staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.event_name == 'workflow_dispatch'
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to production
        run: |
          bash scripts/run-skill.sh deploy --env production
```

---

**관련 문서**:
- [deploy.py](deploy.py) - 실제 구현
- [deploy-history.json](../../.memory/deploy-history.json) - 배포 히스토리
- [deploy-config.json](deploy-config.json) - 환경별 설정
