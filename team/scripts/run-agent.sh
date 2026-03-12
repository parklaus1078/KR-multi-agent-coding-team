#!/bin/bash
# 에이전트 실행 래퍼 스크립트
#
# 사용법:
#   bash scripts/run-agent.sh project-planner --project "할일 관리 앱"
#   bash scripts/run-agent.sh pm              --ticket-file ./tickets/PLAN-001-user-auth.md

set -e

AGENT_NAME="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT_CONFIG="$WORKSPACE_ROOT/.project-config.json"

# ── 현재 프로젝트 확인 ──────────────────────────────────────
if [[ ! -f "$PROJECT_CONFIG" ]]; then
    echo "❌ 프로젝트 설정 파일이 없습니다: .project-config.json"
    echo "   먼저 프로젝트를 초기화하세요:"
    echo "   bash scripts/init-project.sh --interactive"
    exit 1
fi

CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$PROJECT_CONFIG" | cut -d'"' -f4 2>/dev/null)
if [[ -z "$CURRENT_PROJECT" ]]; then
    echo "❌ 현재 활성 프로젝트가 없습니다."
    echo "   프로젝트를 초기화하거나 전환하세요:"
    echo "   bash scripts/init-project.sh --interactive"
    echo "   bash scripts/switch-project.sh <project-name>"
    exit 1
fi

PROJECT_PATH="$WORKSPACE_ROOT/projects/$CURRENT_PROJECT"
if [[ ! -d "$PROJECT_PATH" ]]; then
    echo "❌ 프로젝트 디렉토리를 찾을 수 없습니다: $PROJECT_PATH"
    exit 1
fi

echo ""
echo "📍 현재 프로젝트: $CURRENT_PROJECT"
echo "📂 경로: $PROJECT_PATH"
echo ""

# ── 유효성 체크 ─────────────────────────────────────────────
VALID_AGENTS=("stack-initializer" "project-planner" "pm" "coding" "qa")

if [[ -z "$AGENT_NAME" ]]; then
    echo ""
    echo "사용법: bash scripts/run-agent.sh <agent_name> [options]"
    echo ""
    echo "에이전트 목록:"
    echo "  stack-initializer --config <경로>           스택 초기화"
    echo "  project-planner   --project <설명>          프로젝트 분해 → tickets/ 생성"
    echo "  pm                --ticket-file <경로>      티켓 → 명세서 생성"
    echo "  coding            --ticket <티켓번호>        코드 구현 (모든 타입)"
    echo "  qa                --ticket <티켓번호>        테스트 작성 (모든 타입)"
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

# ── 플래그 파싱 ──────────────────────────────────────────────
shift  # agent_name 제거 후 나머지 플래그 파싱
TICKET_FILE=""
TICKET_NUM=""
PROJECT_DESC=""
CONFIG_FILE=""
RESUME_MODE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --ticket-file)
            TICKET_FILE="$2"
            shift 2
            ;;
        --ticket)
            TICKET_NUM="$2"
            shift 2
            ;;
        --project)
            PROJECT_DESC="$2"
            shift 2
            ;;
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --resume)
            RESUME_MODE=true
            shift
            ;;
        *)
            echo "❌ 알 수 없는 옵션: '$1'"
            exit 1
            ;;
    esac
done

# ── 에이전트별 필수 옵션 검증 및 초기 프롬프트 설정 ────────────
case "$AGENT_NAME" in
    stack-initializer)
        if [[ -z "$CONFIG_FILE" ]]; then
            # .project-config.json이 있으면 사용
            if [[ -f "$WORKSPACE_ROOT/.project-config.json" ]]; then
                CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"
            else
                echo "❌ stack-initializer는 --config 옵션이 필요합니다."
                echo "   또는 .project-config.json 파일이 존재해야 합니다."
                echo "   예: bash scripts/init-project.sh"
                exit 1
            fi
        fi
        if [[ ! -f "$CONFIG_FILE" ]]; then
            echo "❌ 설정 파일을 찾을 수 없습니다: $CONFIG_FILE"
            exit 1
        fi
        INITIAL_PROMPT="프로젝트 설정 파일을 읽고 스택을 초기화합니다: $CONFIG_FILE"
        ;;
    project-planner)
        if [[ "$RESUME_MODE" == true ]]; then
            # 재개 모드: 계획 파일 존재 여부 확인
            LATEST_PLAN=$(ls -t "$PROJECT_PATH/planning/tickets/.plan-"*.json 2>/dev/null | head -1)
            if [[ -z "$LATEST_PLAN" ]]; then
                echo "❌ 재개할 계획 파일을 찾을 수 없습니다."
                echo "   $PROJECT_PATH/planning/tickets/.plan-*.json 파일이 필요합니다."
                exit 1
            fi
            INITIAL_PROMPT="재개: Phase 2부터 티켓 파일을 생성합니다. 계획 파일: $LATEST_PLAN"
        else
            if [[ -z "$PROJECT_DESC" ]]; then
                echo "❌ project-planner는 --project 옵션이 필요합니다."
                echo "   예: bash scripts/run-agent.sh project-planner --project \"할일 관리 앱\""
                echo "   재개: bash scripts/run-agent.sh project-planner --resume"
                exit 1
            fi
            INITIAL_PROMPT="$PROJECT_DESC"
        fi
        ;;
    pm)
        if [[ -z "$TICKET_FILE" ]]; then
            echo "❌ pm은 --ticket-file 옵션이 필요합니다."
            echo "   예: bash scripts/run-agent.sh pm --ticket-file $PROJECT_PATH/planning/tickets/PLAN-001-user-auth.md"
            exit 1
        fi
        # 상대 경로를 절대 경로로 변환
        if [[ ! "$TICKET_FILE" =~ ^/ ]]; then
            TICKET_FILE="$WORKSPACE_ROOT/$TICKET_FILE"
        fi
        if [[ ! -f "$TICKET_FILE" ]]; then
            echo "❌ 티켓 파일을 찾을 수 없습니다: $TICKET_FILE"
            exit 1
        fi

        # Git 브랜치 자동 생성 (티켓 파일에서 티켓 번호와 slug 추출)
        FILENAME=$(basename "$TICKET_FILE")
        # PLAN-001-user-auth.md에서 PLAN-001 추출
        TICKET_NUM=$(echo "$FILENAME" | grep -o '^PLAN-[0-9]*')
        # user-auth 추출
        SLUG=$(echo "$FILENAME" | sed "s/${TICKET_NUM}-//" | sed 's/\.md$//')

        if [[ -n "$TICKET_NUM" ]] && [[ -n "$SLUG" ]]; then
            echo "🌿 Git 브랜치 자동 생성 중..."
            if bash "$SCRIPT_DIR/git-branch-helper.sh" prepare "pm" "$TICKET_NUM" "$SLUG" 2>/dev/null; then
                echo "✅ 브랜치 준비 완료"
            else
                echo "⚠️  브랜치 생성 실패 (Git 설정 확인 필요, 작업은 계속됩니다)"
            fi
            echo ""
        fi

        INITIAL_PROMPT="$(cat "$TICKET_FILE")"
        ;;
    coding|qa)
        if [[ -z "$TICKET_NUM" ]]; then
            echo "❌ $AGENT_NAME 은 --ticket 옵션이 필요합니다."
            echo "   예: bash scripts/run-agent.sh $AGENT_NAME --ticket PLAN-001"
            exit 1
        fi

        # Git 브랜치 자동 생성 (티켓 파일에서 slug 추출)
        TICKET_FILE_PATTERN="$PROJECT_PATH/planning/tickets/${TICKET_NUM}-*.md"
        TICKET_FILE_FOUND=$(ls $TICKET_FILE_PATTERN 2>/dev/null | head -1)

        if [[ -n "$TICKET_FILE_FOUND" ]]; then
            # 파일명에서 slug 추출 (PLAN-001-user-auth.md → user-auth)
            FILENAME=$(basename "$TICKET_FILE_FOUND")
            SLUG=$(echo "$FILENAME" | sed "s/${TICKET_NUM}-//" | sed 's/\.md$//')

            echo "🌿 Git 브랜치 자동 생성 중..."
            if bash "$SCRIPT_DIR/git-branch-helper.sh" prepare "$AGENT_NAME" "$TICKET_NUM" "$SLUG" 2>/dev/null; then
                echo "✅ 브랜치 준비 완료"
            else
                echo "⚠️  브랜치 생성 실패 (Git 설정 확인 필요, 작업은 계속됩니다)"
            fi
            echo ""
        fi

        INITIAL_PROMPT="$TICKET_NUM 티켓을 작업합니다."
        ;;
esac

# ── CLAUDE.md 존재 확인 ──────────────────────────────────────
AGENT_DIR="$WORKSPACE_ROOT/.agents/$AGENT_NAME"
CLAUDE_MD="$AGENT_DIR/CLAUDE.md"

if [[ ! -f "$CLAUDE_MD" ]]; then
    echo "❌ CLAUDE.md를 찾을 수 없습니다: $CLAUDE_MD"
    exit 1
fi

# ── claude CLI 확인 ──────────────────────────────────────────
if ! command -v claude &>/dev/null; then
    echo "❌ claude CLI를 찾을 수 없습니다."
    echo "   Claude Code가 설치되어 있는지 확인하세요."
    echo "   설치: https://docs.claude.ai/claude-code"
    exit 1
fi

# ── Rate Limit 사전 기록 ─────────────────────────────────────
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

# ── claude 실행 ──────────────────────────────────────────────
# --append-system-prompt: Claude Code 기본값을 유지하면서 CLAUDE.md를 추가
# (--system-prompt 사용 시 Claude Code 내장 도구 설명이 제거되므로 사용 금지)

# 대화형 모드로 시작 (--print 제거)
echo "📝 초기 프롬프트를 전달합니다..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$INITIAL_PROMPT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

exec claude \
    --model claude-sonnet-4-5 \
    --append-system-prompt "$(cat "$CLAUDE_MD")" \
    --allowedTools "Bash" "Read" "Edit" "Write" \
    <<EOF
$INITIAL_PROMPT
EOF
