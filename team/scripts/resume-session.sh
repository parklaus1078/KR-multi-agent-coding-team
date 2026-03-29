#!/bin/bash
# 세션 재개 스크립트
#
# 사용법:
#   bash scripts/resume-session.sh --list
#   bash scripts/resume-session.sh <티켓번호> <에이전트명>
#   bash scripts/resume-session.sh <티켓번호> <에이전트명> --fork

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT_CONFIG="$WORKSPACE_ROOT/.project-config.json"

# ── 플래그 파싱 ──────────────────────────────────────────────
LIST_MODE=false
FORK_MODE=false
TICKET_NUM=""
AGENT_NAME=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --list)
            LIST_MODE=true
            shift
            ;;
        --fork)
            FORK_MODE=true
            shift
            ;;
        *)
            if [[ -z "$TICKET_NUM" ]]; then
                TICKET_NUM="$1"
            elif [[ -z "$AGENT_NAME" ]]; then
                AGENT_NAME="$1"
            else
                echo "❌ 알 수 없는 인자: '$1'"
                exit 1
            fi
            shift
            ;;
    esac
done

# ── 현재 프로젝트 확인 ──────────────────────────────────────
if [[ ! -f "$PROJECT_CONFIG" ]]; then
    echo "❌ 프로젝트 설정 파일이 없습니다: .project-config.json"
    echo "   먼저 프로젝트를 초기화하세요."
    exit 1
fi

CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$PROJECT_CONFIG" | cut -d'"' -f4 2>/dev/null)
if [[ -z "$CURRENT_PROJECT" ]]; then
    echo "❌ 현재 활성 프로젝트가 없습니다."
    exit 1
fi

PROJECT_PATH="$WORKSPACE_ROOT/projects/$CURRENT_PROJECT"
SESSIONS_DIR="$PROJECT_PATH/.sessions"
SESSION_MAP="$SESSIONS_DIR/session-map.json"

# ── 세션 목록 표시 ────────────────────────────────────────────
if [[ "$LIST_MODE" == true ]]; then
    if [[ ! -f "$SESSION_MAP" ]]; then
        echo "📋 저장된 세션이 없습니다."
        echo "   프로젝트: $CURRENT_PROJECT"
        exit 0
    fi

    echo ""
    echo "📋 저장된 에이전트 세션 목록"
    echo "   프로젝트: $CURRENT_PROJECT"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # jq로 파싱
    if command -v jq &>/dev/null; then
        jq -r 'to_entries[] |
            "\(.key)\n" +
            (.value | to_entries[] |
                "  \(.key): \(.value.session_id)\n    재개: \(.value.command)\n    시간: \(.value.timestamp)\n"
            )' "$SESSION_MAP"
    else
        # jq 없으면 cat으로 표시
        cat "$SESSION_MAP"
    fi

    echo ""
    exit 0
fi

# ── 세션 재개 ────────────────────────────────────────────────
if [[ -z "$TICKET_NUM" ]] || [[ -z "$AGENT_NAME" ]]; then
    echo ""
    echo "사용법:"
    echo "  bash scripts/resume-session.sh --list"
    echo "  bash scripts/resume-session.sh <티켓번호> <에이전트명>"
    echo "  bash scripts/resume-session.sh <티켓번호> <에이전트명> --fork"
    echo ""
    echo "예시:"
    echo "  bash scripts/resume-session.sh --list"
    echo "  bash scripts/resume-session.sh PLAN-001 pm"
    echo "  bash scripts/resume-session.sh PLAN-001 coding"
    echo "  bash scripts/resume-session.sh PLAN-001 qa"
    echo "  bash scripts/resume-session.sh PLAN-001 coding --fork"
    echo ""
    exit 1
fi

# ── 세션 파일 확인 ────────────────────────────────────────────
TICKET_SESSION_DIR="$SESSIONS_DIR/$TICKET_NUM"
SESSION_FILE="$TICKET_SESSION_DIR/${AGENT_NAME}.session"

if [[ ! -f "$SESSION_FILE" ]]; then
    echo "❌ 세션을 찾을 수 없습니다."
    echo "   티켓: $TICKET_NUM"
    echo "   에이전트: $AGENT_NAME"
    echo "   경로: $SESSION_FILE"
    echo ""
    echo "💡 세션 목록 확인: bash scripts/resume-session.sh --list"
    exit 1
fi

SESSION_ID=$(cat "$SESSION_FILE")

# ── CLAUDE.md 로드 ────────────────────────────────────────────
AGENT_DIR="$WORKSPACE_ROOT/.agents/$AGENT_NAME"
CLAUDE_MD="$AGENT_DIR/CLAUDE.md"

if [[ ! -f "$CLAUDE_MD" ]]; then
    echo "⚠️  CLAUDE.md를 찾을 수 없습니다: $CLAUDE_MD"
    echo "   CLAUDE.md 없이 재개합니다."
    CLAUDE_MD=""
fi

# ── Claude CLI 확인 ──────────────────────────────────────────
if ! command -v claude &>/dev/null; then
    echo "❌ claude CLI를 찾을 수 없습니다."
    echo "   Claude Code가 설치되어 있는지 확인하세요."
    exit 1
fi

# ── 세션 재개 ────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  세션 재개"
echo "║  프로젝트: $CURRENT_PROJECT"
echo "║  티켓: $TICKET_NUM"
echo "║  에이전트: $AGENT_NAME"
echo "║  세션 ID: ${SESSION_ID:0:20}..."
if [[ "$FORK_MODE" == true ]]; then
echo "║  모드: Fork (새 세션으로 실험)"
fi
echo "╚══════════════════════════════════════════════╝"
echo ""

# 프로젝트 디렉토리로 이동
cd "$PROJECT_PATH" || exit 1

# Claude 실행
if [[ "$FORK_MODE" == true ]]; then
    if [[ -n "$CLAUDE_MD" ]]; then
        claude --resume "$SESSION_ID" --fork-session --append-system-prompt "$(cat "$CLAUDE_MD")"
    else
        claude --resume "$SESSION_ID" --fork-session
    fi
else
    if [[ -n "$CLAUDE_MD" ]]; then
        claude --resume "$SESSION_ID" --append-system-prompt "$(cat "$CLAUDE_MD")"
    else
        claude --resume "$SESSION_ID"
    fi
fi
