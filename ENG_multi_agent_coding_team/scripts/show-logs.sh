#!/bin/bash
# Script to view agent implementation logs
# Usage: bash scripts/show-logs.sh [agent_name]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
LOGS_DIR="$WORKSPACE_ROOT/logs"
FILTER="${1:-}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Agent implementation logs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

AGENTS=("pm" "be-coding" "qa-be" "fe-coding" "qa-fe")
for agent in "${AGENTS[@]}"; do
    if [[ -n "$FILTER" && "$agent" != "$FILTER" ]]; then
        continue
    fi

    LOG_DIR="$LOGS_DIR/$agent"
    COUNT=$(find "$LOG_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

    echo ""
    echo "📁 [$agent] — $COUNT logs"

    if [[ "$COUNT" -gt 0 ]]; then
        find "$LOG_DIR" -name "*.md" | sort -r | while read -r f; do
            BASENAME=$(basename "$f")
            echo "   - $BASENAME"
        done
    else
        echo "   (no logs)"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Rate Limit status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 "$SCRIPT_DIR/parse_usage.py" "status" 2>/dev/null || echo "  (no usage records)"
echo ""
