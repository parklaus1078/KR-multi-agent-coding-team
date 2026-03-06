#!/usr/bin/env python3
"""
Rate Limit 추적 및 체크 스크립트
Claude Max 5x: 5시간 롤링 윈도우 기준

사용법: python3 scripts/parse_usage.py <agent_name> [--log]
  --log: 현재 실행을 로그에 기록 (run-agent.sh에서 호출 시)
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

# ── 설정 ──────────────────────────────────────────────────
USAGE_LOG_DIR = Path.home() / ".claude-agents"
USAGE_LOG_FILE = USAGE_LOG_DIR / "usage.log"
WINDOW_HOURS = 5
WINDOW_SECONDS = WINDOW_HOURS * 3600

# 임계값: 5시간 윈도우 내 에이전트 실행 횟수 기준
# Claude Max 실제 한도를 정확히 알 수 없으므로 보수적으로 설정
# 실제 사용 패턴을 보며 WARN_THRESHOLD, STOP_THRESHOLD를 조정할 것
WARN_THRESHOLD = 35   # 이 횟수 이상이면 경고
STOP_THRESHOLD = 45   # 이 횟수 이상이면 중단 권고
# ───────────────────────────────────────────────────────────


def ensure_log_dir():
    USAGE_LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not USAGE_LOG_FILE.exists():
        USAGE_LOG_FILE.write_text("[]")


def load_log():
    try:
        return json.loads(USAGE_LOG_FILE.read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_log(entries):
    USAGE_LOG_FILE.write_text(json.dumps(entries, indent=2))


def get_recent_entries(entries):
    now = time.time()
    cutoff = now - WINDOW_SECONDS
    return [e for e in entries if e["timestamp"] > cutoff]


def log_invocation(agent_name):
    """현재 에이전트 실행을 로그에 기록"""
    ensure_log_dir()
    entries = load_log()
    entries.append({
        "timestamp": time.time(),
        "agent": agent_name,
        "datetime": datetime.now().isoformat()
    })
    # 오래된 항목 정리 (24시간 이상)
    entries = [e for e in entries if e["timestamp"] > time.time() - 86400]
    save_log(entries)


def check_rate_limit(agent_name):
    """
    Returns: (status, count, message)
      status: "ok" | "warn" | "stop"
    """
    ensure_log_dir()
    entries = load_log()
    recent = get_recent_entries(entries)
    count = len(recent)

    reset_in_minutes = 0
    if recent:
        oldest = min(e["timestamp"] for e in recent)
        reset_in_seconds = int(WINDOW_SECONDS - (time.time() - oldest))
        reset_in_minutes = max(0, reset_in_seconds // 60)

    if count >= STOP_THRESHOLD:
        msg = (
            f"[STOP] Rate Limit 임박으로 작업을 중단합니다.\n"
            f"  현재 {WINDOW_HOURS}시간 윈도우 내 실행 횟수: {count}회 (한도 권고: {STOP_THRESHOLD}회)\n"
            f"  약 {reset_in_minutes}분 후 윈도우가 초기화됩니다.\n"
            f"  초기화 후 다시 실행해주세요."
        )
        return "stop", count, msg
    elif count >= WARN_THRESHOLD:
        msg = (
            f"[WARN] Rate Limit 경고: 현재 {WINDOW_HOURS}시간 내 {count}회 실행됨 (경고 기준: {WARN_THRESHOLD}회)\n"
            f"  약 {reset_in_minutes}분 후 윈도우 초기화 예정.\n"
            f"  계속 진행하시겠습니까? (사용자 확인 후 진행)"
        )
        return "warn", count, msg
    else:
        remaining = STOP_THRESHOLD - count
        msg = f"[OK] Rate Limit 여유 있음: {WINDOW_HOURS}시간 내 {count}회 실행됨 (여유: {remaining}회)"
        return "ok", count, msg


if __name__ == "__main__":
    agent_name = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    should_log = "--log" in sys.argv

    if should_log:
        log_invocation(agent_name)

    status, count, message = check_rate_limit(agent_name)
    print(message)

    if status == "stop":
        sys.exit(2)
    elif status == "warn":
        sys.exit(1)
    else:
        sys.exit(0)
