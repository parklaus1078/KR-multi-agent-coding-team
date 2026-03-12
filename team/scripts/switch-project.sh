#!/bin/bash
# 프로젝트 전환 스크립트
#
# 사용법:
#   bash scripts/switch-project.sh my-cli-tool
#   bash scripts/switch-project.sh --list

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"
PROJECTS_DIR="$WORKSPACE_ROOT/projects"

# ── 프로젝트 목록 표시 ─────────────────────────────────────────
show_projects() {
    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║  프로젝트 목록                               ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""

    if [[ ! -d "$PROJECTS_DIR" ]] || [[ -z "$(ls -A "$PROJECTS_DIR" 2>/dev/null)" ]]; then
        echo "프로젝트가 없습니다."
        echo ""
        echo "새 프로젝트 생성:"
        echo "  bash scripts/init-project.sh --interactive"
        exit 0
    fi

    # 현재 활성 프로젝트 확인
    CURRENT_PROJECT=""
    if [[ -f "$CONFIG_FILE" ]]; then
        CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4 2>/dev/null || echo "")
    fi

    for project_dir in "$PROJECTS_DIR"/*; do
        if [[ -d "$project_dir" ]]; then
            project_name=$(basename "$project_dir")
            meta_file="$project_dir/.project-meta.json"

            # 현재 프로젝트 표시
            if [[ "$project_name" == "$CURRENT_PROJECT" ]]; then
                echo "  → $project_name (현재 활성)"
            else
                echo "    $project_name"
            fi

            # 메타데이터 표시
            if [[ -f "$meta_file" ]]; then
                project_type=$(grep -o '"project_type": *"[^"]*"' "$meta_file" | cut -d'"' -f4 2>/dev/null || echo "unknown")
                echo "      타입: $project_type"
            fi
            echo ""
        fi
    done
}

# ── 인자 확인 ────────────────────────────────────────────────────
if [[ $# -eq 0 ]] || [[ "$1" == "--list" ]] || [[ "$1" == "-l" ]]; then
    show_projects
    exit 0
fi

PROJECT_NAME="$1"
PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"

# ── 프로젝트 존재 확인 ────────────────────────────────────────────
if [[ ! -d "$PROJECT_PATH" ]]; then
    echo "❌ 프로젝트를 찾을 수 없습니다: $PROJECT_NAME"
    echo ""
    echo "사용 가능한 프로젝트:"
    show_projects
    exit 1
fi

# ── 프로젝트 메타데이터 읽기 ──────────────────────────────────────
META_FILE="$PROJECT_PATH/.project-meta.json"
if [[ ! -f "$META_FILE" ]]; then
    echo "❌ 프로젝트 메타데이터를 찾을 수 없습니다: $META_FILE"
    exit 1
fi

PROJECT_TYPE=$(grep -o '"project_type": *"[^"]*"' "$META_FILE" | cut -d'"' -f4 2>/dev/null || echo "unknown")
CREATED_AT=$(grep -o '"created_at": *"[^"]*"' "$META_FILE" | cut -d'"' -f4 2>/dev/null || echo "unknown")

# ── .project-config.json 업데이트 ─────────────────────────────────
echo ""
echo "프로젝트 전환: $PROJECT_NAME"
echo "  타입: $PROJECT_TYPE"
echo "  생성일: $CREATED_AT"
echo ""

# 기존 recent_projects 배열 읽기 (JSON 파싱은 jq 없이 간단히 처리)
RECENT_PROJECTS=()
if [[ -f "$CONFIG_FILE" ]]; then
    # 기존 프로젝트 목록 추출 (간단한 grep)
    while IFS= read -r line; do
        RECENT_PROJECTS+=("$line")
    done < <(grep -o '"[^"]*"' "$CONFIG_FILE" | grep -v "current_project\|current_project_path\|recent_projects" | tr -d '"' | head -5)
fi

# 현재 프로젝트를 맨 앞에 추가 (중복 제거)
NEW_RECENT=("$PROJECT_NAME")
for proj in "${RECENT_PROJECTS[@]}"; do
    if [[ "$proj" != "$PROJECT_NAME" ]] && [[ ${#NEW_RECENT[@]} -lt 5 ]]; then
        NEW_RECENT+=("$proj")
    fi
done

# JSON 생성 (recent_projects 배열)
RECENT_JSON=""
for i in "${!NEW_RECENT[@]}"; do
    if [[ $i -eq 0 ]]; then
        RECENT_JSON="\"${NEW_RECENT[$i]}\""
    else
        RECENT_JSON="$RECENT_JSON, \"${NEW_RECENT[$i]}\""
    fi
done

cat > "$CONFIG_FILE" <<EOF
{
  "current_project": "$PROJECT_NAME",
  "current_project_path": "projects/$PROJECT_NAME",
  "recent_projects": [$RECENT_JSON]
}
EOF

echo "✅ 프로젝트 전환 완료"
echo ""
echo "다음 단계:"
echo "  1. 티켓 생성: bash scripts/run-agent.sh project-planner --project \"프로젝트 설명\""
echo "  2. 명세서 생성: bash scripts/run-agent.sh pm --ticket-file projects/$PROJECT_NAME/planning/tickets/PLAN-001-*.md"
echo "  3. 코딩: bash scripts/run-agent.sh coding --ticket PLAN-001"
echo "  4. 테스트: bash scripts/run-agent.sh qa --ticket PLAN-001"
echo ""
