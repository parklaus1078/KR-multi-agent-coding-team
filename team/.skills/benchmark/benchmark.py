#!/usr/bin/env python3
"""
Benchmark Skill - 성능 벤치마크
"""

import sys
import time
import statistics
import subprocess
import requests
from pathlib import Path
from typing import List


def benchmark_api(url: str, requests_count: int = 100) -> dict:
    """API 벤치마크"""
    print(f"🚀 API 벤치마크")
    print(f"   URL: {url}")
    print(f"   요청 수: {requests_count}")
    print()

    response_times: List[float] = []
    success_count = 0
    error_count = 0

    print("진행 중", end="", flush=True)

    for i in range(requests_count):
        if i % 10 == 0:
            print(".", end="", flush=True)

        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            duration = (time.time() - start) * 1000  # ms

            if response.status_code == 200:
                success_count += 1
                response_times.append(duration)
            else:
                error_count += 1

        except Exception:
            error_count += 1

    print("\n")

    if not response_times:
        print("❌ 모든 요청 실패")
        return {}

    # 통계 계산
    avg = statistics.mean(response_times)
    median = statistics.median(response_times)
    p95 = sorted(response_times)[int(len(response_times) * 0.95)]
    p99 = sorted(response_times)[int(len(response_times) * 0.99)]

    results = {
        "success_count": success_count,
        "error_count": error_count,
        "success_rate": success_count / requests_count * 100,
        "avg_ms": avg,
        "median_ms": median,
        "p95_ms": p95,
        "p99_ms": p99,
        "min_ms": min(response_times),
        "max_ms": max(response_times)
    }

    # 결과 출력
    print("📊 결과:")
    print(f"   성공률: {results['success_rate']:.1f}% ({success_count}/{requests_count})")
    print(f"   평균: {avg:.1f}ms")
    print(f"   중앙값: {median:.1f}ms")
    print(f"   P95: {p95:.1f}ms")
    print(f"   P99: {p99:.1f}ms")
    print(f"   최소: {results['min_ms']:.1f}ms")
    print(f"   최대: {results['max_ms']:.1f}ms")

    # 판정
    if results['success_rate'] < 95:
        print("\n❌ 성공률이 95% 미만입니다.")
    elif p95 > 200:
        print("\n⚠️  P95 응답 시간이 200ms를 초과합니다.")
    else:
        print("\n✅ 성능 기준 통과!")

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python benchmark.py <url> [requests_count]")
        print("Example: python benchmark.py http://localhost:8000/api/health 100")
        sys.exit(1)

    url = sys.argv[1]
    requests_count = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    results = benchmark_api(url, requests_count)

    # 성공 기준
    if results.get("success_rate", 0) >= 95 and results.get("p95_ms", 999) <= 200:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
