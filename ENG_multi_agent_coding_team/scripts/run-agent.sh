#!/bin/bash
# Wrapper script to run an agent
# 사용법: bash scripts/run-agent.sh <agent_name>
#
# <agent_name> list:
#   be-coding   — BE Coding Agent (backend code generation)
#   qa-be       — QA-BE Agent (backend test generation)
#   fe-coding   — FE Coding Agent (frontend code generation)
#   qa-fe       — QA-FE Agent (frontend test generation)

set -e

AGENT_NAME="${1:-}"   # Agent directory name
TICKET_FILE="${2:-}"  # Ticket file path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"

# ── Validation check ─────────────────────────────────────────────
VALID_AGENTS=("pm" "be-coding" "qa-be" "fe-coding" "qa-fe")
if [[ -z "$AGENT_NAME" ]]; then
    echo ""
    echo "Usage: bash scripts/run-agent.sh <agent_name>"
    echo ""
    echo "Available agents:"
    for a in "${VALID_AGENTS[@]}"; do
        echo "  - $a"
    done
    echo ""
    exit 1
fi

VALID=false
for a in "${VALID_AGENTS[@]}"; do
    [[ "$AGENT_NAME" == "$a" ]] && VALID=true && break
done

if [[ "$VALID" == false ]]; then
    echo "❌ Unknown agent: '$AGENT_NAME'"
    echo "   Available: ${VALID_AGENTS[*]}"
    exit 1
fi

AGENT_DIR="$WORKSPACE_ROOT/.agents/$AGENT_NAME"
CLAUDE_MD="$AGENT_DIR/CLAUDE.md"

if [[ ! -f "$CLAUDE_MD" ]]; then
    echo "❌ CLAUDE.md not found: $CLAUDE_MD"
    exit 1
fi

# ── claude CLI check ─────────────────────────────────────────
if ! command -v claude &>/dev/null; then
    echo "❌ claude CLI not found."
    echo "   Check if Claude Code is installed."
    echo "   Installation: https://docs.claude.ai/claude-code"
    exit 1
fi

# -- PM Agent special handling ──────────────────────────────────────
if [[ "$AGENT_NAME" == "pm" ]]; then
    if [[ -z "$TICKET_FILE" ]]; then
        echo "❌ PM Agent execution requires a ticket file."
        echo "   Usage: bash scripts/run-agent.sh pm ./tickets/PROJ-123.md"
        exit 1
    fi
    if [[ ! -f "$TICKET_FILE" ]]; then
        echo "❌ Ticket file not found: $TICKET_FILE"
        exit 1
    fi
fi

# ── Rate Limit pre-record ──────────────────────────────────────
# Record before execution (--log flag)
python3 "$SCRIPT_DIR/parse_usage.py" "$AGENT_NAME" --log 2>/dev/null || true

# ── Agent start ────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  Agent start: $AGENT_NAME"
echo "║  Workspace: $WORKSPACE_ROOT"
echo "║  Instruction file: .agents/$AGENT_NAME/CLAUDE.md"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "💡 The agent will automatically perform the Rate Limit check."
echo "   Exit: Ctrl+C"
echo ""

# Run claude
# --system-prompt: Specify the agent-specific CLAUDE.md as the system prompt
if [[ "$AGENT_NAME" == "pm" && -n "$TICKET_FILE" ]]; then
    exec claude \
        --model claude-sonnet-4-5 \
        --append-system-prompt "$(cat "$CLAUDE_MD")" \
        "${cat "$TICKET_FILE"}" \
        --allowedTools "Bash" "Read" "Edit" "Write" \
else
    exec claude \
        --model claude-sonnet-4-5 \
        --append-system-prompt "$(cat "$CLAUDE_MD")" \
        --allowedTools "Bash" "Read" "Edit" "Write" \
fi