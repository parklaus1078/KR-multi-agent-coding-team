#!/usr/bin/env python3
"""
Track and check Rate Limit
Claude Max 5x: 5-hour rolling window

Usage: python3 scripts/parse_usage.py <agent_name> [--log]
  --log: Record the current execution in the log (when called by run-agent.sh)
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

# Threshold: Based on the number of agent executions within a 5-hour window
# Since the actual limit of Claude Max is not exactly known, set conservatively
# Adjust WARN_THRESHOLD and STOP_THRESHOLD based on actual usage patterns
WARN_THRESHOLD = 35   # Warn when this number is exceeded
STOP_THRESHOLD = 45   # Stop recommended when this number is exceeded
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
    """Record the current agent execution in the log"""
    ensure_log_dir()
    entries = load_log()
    entries.append({
        "timestamp": time.time(),
        "agent": agent_name,
        "datetime": datetime.now().isoformat()
    })
    # Clean up old entries (older than 24 hours)
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
            f"[STOP] Rate Limit is approaching. Stopping work.\n"
            f"  Current execution count within {WINDOW_HOURS} hour window: {count} (recommended limit: {STOP_THRESHOLD})\n"
            f"  Approximately {reset_in_minutes} minutes until window reset.\n"
            f"  Please run again after the reset."
        )
        return "stop", count, msg
    elif count >= WARN_THRESHOLD:
        msg = (
            f"[WARN] Rate Limit Warning: Currently {count} executions within {WINDOW_HOURS} hour window (warning threshold: {WARN_THRESHOLD})\n"
            f"  Approximately {reset_in_minutes} minutes until window reset.\n"
            f"  Continue? (Please confirm with the user)"
        )
        return "warn", count, msg
    else:
        remaining = STOP_THRESHOLD - count
        msg = f"[OK] Rate Limit is available: {count} executions within {WINDOW_HOURS} hour window (remaining: {remaining})"
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
