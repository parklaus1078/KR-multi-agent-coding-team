#!/bin/bash
# 에이전트 실행 래퍼 스크립트
# 사용법: bash scripts/run-agent.sh <agent_name>
#
# <agent_name> 목록:
#   be-coding   — BE Coding Agent (백엔드 코드 생성)
#   qa-be       — QA-BE Agent (백엔드 테스트 생성)
#   fe-coding   — FE Coding Agent (프론트엔드 코드 생성)
#   qa-fe       — QA-FE Agent (프론트엔드 테스트 생성)

set -e

AGENT_NAME="${1:-}"   # 에이전트 디렉토리 이름 
TICKET_FILE="${2:-}"  # 티켓 파일 경로
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"

# ── 유효성 체크 ─────────────────────────────────────────────
VALID_AGENTS=("pm" "be-coding" "qa-be" "fe-coding" "qa-fe")
if [[ -z "$AGENT_NAME" ]]; then
    echo ""
    echo "사용법: bash scripts/run-agent.sh <agent_name>"
    echo ""
    echo "사용 가능한 에이전트:"
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
    echo "❌ 알 수 없는 에이전트: '$AGENT_NAME'"
    echo "   사용 가능: ${VALID_AGENTS[*]}"
    exit 1
fi

AGENT_DIR="$WORKSPACE_ROOT/.agents/$AGENT_NAME"
CLAUDE_MD="$AGENT_DIR/CLAUDE.md"

if [[ ! -f "$CLAUDE_MD" ]]; then
    echo "❌ CLAUDE.md를 찾을 수 없습니다: $CLAUDE_MD"
    exit 1
fi

# ── claude CLI 확인 ─────────────────────────────────────────
if ! command -v claude &>/dev/null; then
    echo "❌ claude CLI를 찾을 수 없습니다."
    echo "   Claude Code가 설치되어 있는지 확인하세요."
    echo "   설치: https://docs.claude.ai/claude-code"
    exit 1
fi

# -- PM Agent 특별 처리 ──────────────────────────────────────
if [[ "$AGENT_NAME" == "pm" ]]; then
    if [[ -z "$TICKET_FILE" ]]; then
        echo "❌ PM Agent 실행 시 티켓 파일이 필요합니다."
        echo "   사용법: bash scripts/run-agent.sh pm ./tickets/PROJ-123.md"
        exit 1
    fi
    if [[ ! -f "$TICKET_FILE" ]]; then
        echo "❌ 티켓 파일을 찾을 수 없습니다: $TICKET_FILE"
        exit 1
    fi
fi

# ── Rate Limit 사전 기록 ──────────────────────────────────────
# 실행 전 로그에 기록 (--log 플래그)
python3 "$SCRIPT_DIR/parse_usage.py" "$AGENT_NAME" --log 2>/dev/null || true

# ── 에이전트 시작 ────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  에이전트 시작: $AGENT_NAME"
echo "║  워크스페이스: $WORKSPACE_ROOT"
echo "║  지시 파일: .agents/$AGENT_NAME/CLAUDE.md"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "💡 에이전트가 Rate Limit 체크를 자동으로 수행합니다."
echo "   종료: Ctrl+C"
echo ""

# claude 실행
# --system-prompt: 에이전트 전용 CLAUDE.md를 시스템 프롬프트로 지정
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