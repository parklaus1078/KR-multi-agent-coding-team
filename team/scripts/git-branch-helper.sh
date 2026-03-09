#!/bin/bash
# Git 브랜치 관리 헬퍼 스크립트
# 코딩 에이전트가 작업 전후로 호출하는 유틸리티

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$WORKSPACE_ROOT/.config/git-workflow.json"

# ── 설정 파일 읽기 ──────────────────────────────────────────
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "⚠️  설정 파일이 없습니다: $CONFIG_FILE"
    echo "   기본 설정으로 진행합니다."
    BASE_BRANCH="dev"
    ENABLED=true
else
    BASE_BRANCH=$(jq -r '.branch_strategy.base_branch // "dev"' "$CONFIG_FILE")
    ENABLED=$(jq -r '.branch_strategy.enabled // true' "$CONFIG_FILE")
    AUTO_CREATE=$(jq -r '.branch_strategy.auto_create // true' "$CONFIG_FILE")
    AUTO_CHECKOUT=$(jq -r '.branch_strategy.auto_checkout // true' "$CONFIG_FILE")
    CHECK_UNCOMMITTED=$(jq -r '.safety.check_uncommitted_changes // true' "$CONFIG_FILE")
    STASH_BEFORE=$(jq -r '.safety.stash_before_checkout // true' "$CONFIG_FILE")
fi

# ── 서브커맨드 처리 ──────────────────────────────────────────

case "${1:-}" in
    # ── prepare: 작업 전 브랜치 준비 ──────────────────────────
    prepare)
        AGENT_NAME="${2:-}"
        TICKET_NUM="${3:-}"
        SLUG="${4:-}"

        if [[ "$ENABLED" != "true" ]]; then
            echo "ℹ️  Git 브랜치 자동 관리가 비활성화되어 있습니다."
            exit 0
        fi

        if [[ -z "$AGENT_NAME" || -z "$TICKET_NUM" ]]; then
            echo "❌ 사용법: bash scripts/git-branch-helper.sh prepare <agent-name> <ticket-number> [slug]"
            exit 1
        fi

        # 에이전트별 prefix 결정
        case "$AGENT_NAME" in
            be-coding) PREFIX="feature/be" ;;
            fe-coding) PREFIX="feature/fe" ;;
            qa-be)     PREFIX="test/be" ;;
            qa-fe)     PREFIX="test/fe" ;;
            *)
                echo "⚠️  알 수 없는 에이전트: $AGENT_NAME"
                PREFIX="feature"
                ;;
        esac

        # 브랜치명 생성
        if [[ -n "$SLUG" ]]; then
            BRANCH_NAME="$PREFIX/$TICKET_NUM-$SLUG"
        else
            BRANCH_NAME="$PREFIX/$TICKET_NUM"
        fi

        echo ""
        echo "╔══════════════════════════════════════════════╗"
        echo "║  Git 브랜치 준비"
        echo "║  베이스: $BASE_BRANCH"
        echo "║  타겟: $BRANCH_NAME"
        echo "╚══════════════════════════════════════════════╝"
        echo ""

        # 현재 브랜치 확인
        CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

        if [[ "$CURRENT_BRANCH" == "$BRANCH_NAME" ]]; then
            echo "✅ 이미 타겟 브랜치에 있습니다: $BRANCH_NAME"
            exit 0
        fi

        # Uncommitted changes 확인
        if [[ "$CHECK_UNCOMMITTED" == "true" ]]; then
            if ! git diff-index --quiet HEAD -- 2>/dev/null; then
                if [[ "$STASH_BEFORE" == "true" ]]; then
                    echo "⚠️  커밋되지 않은 변경사항이 있습니다. Stash에 저장합니다."
                    git stash push -m "Auto-stash before switching to $BRANCH_NAME"
                    echo "💾 Stash 저장 완료. 나중에 'git stash pop'으로 복원할 수 있습니다."
                else
                    echo "❌ 커밋되지 않은 변경사항이 있습니다."
                    echo "   먼저 커밋하거나 stash하세요."
                    echo "   또는 .config/git-workflow.json에서 stash_before_checkout을 true로 설정하세요."
                    exit 1
                fi
            fi
        fi

        # 베이스 브랜치 최신화
        echo "📥 베이스 브랜치 최신화: $BASE_BRANCH"
        git fetch origin "$BASE_BRANCH" 2>/dev/null || true

        # 브랜치 존재 여부 확인
        if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
            # 브랜치 존재 → checkout
            echo "🔀 기존 브랜치로 전환: $BRANCH_NAME"
            git checkout "$BRANCH_NAME"
        else
            # 브랜치 없음
            if [[ "$AUTO_CREATE" == "true" ]]; then
                echo "🌿 새 브랜치 생성: $BRANCH_NAME (from $BASE_BRANCH)"
                git checkout -b "$BRANCH_NAME" "origin/$BASE_BRANCH" 2>/dev/null || \
                git checkout -b "$BRANCH_NAME" "$BASE_BRANCH"
                echo "✅ 브랜치 생성 완료"
            else
                echo "❌ 브랜치가 존재하지 않으며, auto_create가 비활성화되어 있습니다."
                echo "   .config/git-workflow.json에서 auto_create를 true로 설정하거나"
                echo "   수동으로 브랜치를 생성하세요: git checkout -b $BRANCH_NAME $BASE_BRANCH"
                exit 1
            fi
        fi

        echo ""
        echo "✅ 브랜치 준비 완료: $BRANCH_NAME"
        echo ""
        ;;

    # ── status: 현재 Git 상태 확인 ──────────────────────────
    status)
        CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
        echo ""
        echo "📍 현재 브랜치: $CURRENT_BRANCH"
        echo "📌 베이스 브랜치 (설정): $BASE_BRANCH"
        echo ""

        if ! git diff-index --quiet HEAD -- 2>/dev/null; then
            echo "📝 커밋되지 않은 변경사항:"
            git status --short
        else
            echo "✅ 작업 디렉토리 깨끗함 (커밋되지 않은 변경사항 없음)"
        fi
        echo ""
        ;;

    # ── cleanup: 작업 완료 후 정리 ──────────────────────────
    cleanup)
        echo "🧹 브랜치 정리 작업은 수동으로 수행하세요."
        echo "   - 불필요한 브랜치 삭제: git branch -d <branch-name>"
        echo "   - 원격 브랜치 삭제: git push origin --delete <branch-name>"
        ;;

    # ── config: 설정 확인 ────────────────────────────────────
    config)
        if [[ -f "$CONFIG_FILE" ]]; then
            echo ""
            echo "📋 현재 Git Workflow 설정:"
            echo ""
            cat "$CONFIG_FILE" | jq '.'
            echo ""
        else
            echo "⚠️  설정 파일이 없습니다: $CONFIG_FILE"
        fi
        ;;

    # ── help ────────────────────────────────────────────────
    *)
        echo ""
        echo "Git 브랜치 관리 헬퍼 스크립트"
        echo ""
        echo "사용법:"
        echo "  bash scripts/git-branch-helper.sh prepare <agent-name> <ticket-number> [slug]"
        echo "    → 작업 전 브랜치 준비 (생성 또는 전환)"
        echo ""
        echo "  bash scripts/git-branch-helper.sh status"
        echo "    → 현재 Git 상태 확인"
        echo ""
        echo "  bash scripts/git-branch-helper.sh config"
        echo "    → 현재 설정 확인"
        echo ""
        echo "예시:"
        echo "  bash scripts/git-branch-helper.sh prepare be-coding PLAN-001 user-auth"
        echo "  → feature/be/PLAN-001-user-auth 브랜치 생성/전환"
        echo ""
        echo "  bash scripts/git-branch-helper.sh prepare fe-coding PLAN-001"
        echo "  → feature/fe/PLAN-001 브랜치 생성/전환"
        echo ""
        exit 1
        ;;
esac
