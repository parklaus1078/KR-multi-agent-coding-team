#!/bin/bash
# 에이전트 구현 로그 조회 스크립트
# 사용법: bash scripts/show-logs.sh [agent_name]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
LOGS_DIR="$WORKSPACE_ROOT/logs"
FILTER="${1:-}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " 에이전트 구현 로그"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

AGENTS=("pm" "be-coding" "qa-be" "fe-coding" "qa-fe")
for agent in "${AGENTS[@]}"; do
    if [[ -n "$FILTER" && "$agent" != "$FILTER" ]]; then
        continue
    fi

    LOG_DIR="$LOGS_DIR/$agent"
    COUNT=$(find "$LOG_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

    echo ""
    echo "📁 [$agent] — $COUNT 개의 로그"

    if [[ "$COUNT" -gt 0 ]]; then
        find "$LOG_DIR" -name "*.md" | sort -r | while read -r f; do
            BASENAME=$(basename "$f")
            echo "   - $BASENAME"
        done
    else
        echo "   (로그 없음)"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Rate Limit 현황"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 "$SCRIPT_DIR/parse_usage.py" "status" 2>/dev/null || echo "  (사용 기록 없음)"
echo ""
