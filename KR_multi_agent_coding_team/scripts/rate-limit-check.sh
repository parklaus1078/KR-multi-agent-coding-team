#!/bin/bash
# Rate Limit 사전 체크 스크립트
# 사용법: bash scripts/rate-limit-check.sh <agent_name>
#
# Exit codes:
#   0 = OK (여유 있음)
#   1 = WARN (경고, 사용자 판단 필요)
#   2 = STOP (중단 권고)

AGENT_NAME="${1:-unknown}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Rate Limit 체크 | 에이전트: $AGENT_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Python 확인
if ! command -v python3 &>/dev/null; then
    echo "❌ python3를 찾을 수 없습니다."
    exit 0  # 체크 불가 시 진행 허용 (보수적 실패 방지)
fi

# parse_usage.py 실행
python3 "$SCRIPT_DIR/parse_usage.py" "$AGENT_NAME"
EXIT_CODE=$?

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

exit $EXIT_CODE
