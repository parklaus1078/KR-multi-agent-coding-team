#!/bin/bash
#
# Skill 실행 wrapper 스크립트
#
# Usage:
#   bash scripts/run-skill.sh validate-spec PLAN-001
#   bash scripts/run-skill.sh validate-spec PLAN-001 --auto-fix
#   bash scripts/run-skill.sh validate-spec --all
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEAM_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILL_NAME="$1"
shift

if [ -z "$SKILL_NAME" ]; then
    echo "Usage: bash scripts/run-skill.sh <skill-name> [args...]"
    echo ""
    echo "Available skills:"
    echo ""
    echo "Code Quality:"
    echo "  validate-spec  - PM Agent 명세서 검증"
    echo "  review-pr      - PR 자동 리뷰"
    echo "  refactor-code  - 코드 리팩토링 제안"
    echo ""
    echo "Development:"
    echo "  commit         - 커밋 메시지 자동 생성"
    echo "  test-runner    - 테스트 자동 실행"
    echo "  docs-generator - 문서 자동 생성"
    echo ""
    echo "Operations:"
    echo "  deploy         - 배포 자동화"
    echo "  benchmark      - 성능 벤치마크"
    exit 1
fi

SKILL_DIR="$TEAM_ROOT/.skills/$SKILL_NAME"

if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ Skill을 찾을 수 없습니다: $SKILL_NAME"
    echo "경로: $SKILL_DIR"
    exit 1
fi

# Skill별 실행
case "$SKILL_NAME" in
    validate-spec)
        python3 "$SKILL_DIR/validate.py" "$@"
        ;;
    commit)
        python3 "$SKILL_DIR/commit-message-generator.py" "$@"
        ;;
    review-pr)
        python3 "$SKILL_DIR/review-pr.py" "$@"
        ;;
    refactor-code)
        python3 "$SKILL_DIR/refactor-code.py" "$@"
        ;;
    test-runner)
        python3 "$SKILL_DIR/test-runner.py" "$@"
        ;;
    deploy)
        python3 "$SKILL_DIR/deploy.py" "$@"
        ;;
    benchmark)
        python3 "$SKILL_DIR/benchmark.py" "$@"
        ;;
    docs-generator)
        python3 "$SKILL_DIR/docs-generator.py" "$@"
        ;;
    *)
        echo "❌ 알 수 없는 Skill: $SKILL_NAME"
        exit 1
        ;;
esac
