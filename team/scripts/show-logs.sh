#!/bin/bash
# 에이전트 구현 로그 조회 스크립트 v2.0
# 사용법:
#   bash scripts/show-logs.sh              # 현재 프로젝트 전체 로그
#   bash scripts/show-logs.sh coding       # 특정 에이전트만
#   bash scripts/show-logs.sh --all        # 모든 프로젝트

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"
FILTER="${1:-}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " 에이전트 구현 로그 (v2.0)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 모든 프로젝트 모드 ──────────────────────────────────────────
if [[ "$FILTER" == "--all" ]]; then
    PROJECTS_DIR="$WORKSPACE_ROOT/projects"

    if [[ ! -d "$PROJECTS_DIR" ]] || [[ -z "$(ls -A "$PROJECTS_DIR" 2>/dev/null)" ]]; then
        echo ""
        echo "프로젝트가 없습니다."
        echo ""
        exit 0
    fi

    for project_dir in "$PROJECTS_DIR"/*; do
        if [[ -d "$project_dir" ]]; then
            project_name=$(basename "$project_dir")
            echo ""
            echo "📦 프로젝트: $project_name"
            echo "   경로: $project_dir"

            LOGS_DIR="$project_dir/logs"
            if [[ ! -d "$LOGS_DIR" ]]; then
                echo "   (로그 디렉토리 없음)"
                continue
            fi

            AGENTS=("stack-initializer" "project-planner" "pm" "coding" "qa")
            for agent in "${AGENTS[@]}"; do
                LOG_DIR="$LOGS_DIR/$agent"
                COUNT=$(find "$LOG_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

                if [[ "$COUNT" -gt 0 ]]; then
                    echo ""
                    echo "   📁 [$agent] — $COUNT 개의 로그"
                    find "$LOG_DIR" -name "*.md" | sort -r | head -3 | while read -r f; do
                        BASENAME=$(basename "$f")
                        echo "      - $BASENAME"
                    done
                    if [[ "$COUNT" -gt 3 ]]; then
                        echo "      ... (외 $((COUNT - 3))개)"
                    fi
                fi
            done
        fi
    done

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
fi

# ── 현재 프로젝트 모드 ──────────────────────────────────────────

# 현재 프로젝트 확인
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo ""
    echo "❌ .project-config.json을 찾을 수 없습니다."
    echo "   프로젝트를 먼저 초기화하세요:"
    echo "   bash scripts/init-project-v2.sh --interactive"
    echo ""
    exit 1
fi

CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4 2>/dev/null)

if [[ -z "$CURRENT_PROJECT" ]]; then
    echo ""
    echo "❌ 현재 활성 프로젝트가 없습니다."
    echo ""
    exit 1
fi

PROJECT_PATH="$WORKSPACE_ROOT/projects/$CURRENT_PROJECT"
LOGS_DIR="$PROJECT_PATH/logs"

echo ""
echo "📦 현재 프로젝트: $CURRENT_PROJECT"
echo "   경로: $PROJECT_PATH"

if [[ ! -d "$LOGS_DIR" ]]; then
    echo ""
    echo "   (로그 디렉토리 없음)"
    echo ""
    exit 0
fi

# v2.0 에이전트 목록
AGENTS=("stack-initializer" "project-planner" "pm" "coding" "qa")

for agent in "${AGENTS[@]}"; do
    # 필터링
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
            # 파일 크기 표시
            SIZE=$(du -h "$f" | cut -f1)
            echo "   - $BASENAME ($SIZE)"
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
echo "💡 팁:"
echo "   전체 프로젝트 로그: bash scripts/show-logs.sh --all"
echo "   특정 에이전트만:   bash scripts/show-logs.sh coding"
echo "   프로젝트 전환:     bash scripts/switch-project.sh <project-name>"
echo ""
