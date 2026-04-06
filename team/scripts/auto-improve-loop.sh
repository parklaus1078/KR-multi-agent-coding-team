#!/bin/bash
#
# Auto-Improve Loop: Coding ↔ Evaluator 반복
#
# 사용법:
#   bash scripts/auto-improve-loop.sh PLAN-001 --target-score 90 --max-iterations 10
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT_CONFIG="$WORKSPACE_ROOT/.project-config.json"

# ── 인자 파싱 ──────────────────────────────────────────────
TICKET_NUM="$1"
TARGET_SCORE=90
MAX_ITERATIONS=10

if [[ -z "$TICKET_NUM" ]]; then
    echo "사용법: bash scripts/auto-improve-loop.sh <TICKET> [OPTIONS]"
    echo ""
    echo "옵션:"
    echo "  --target-score N    목표 점수 (기본: 90)"
    echo "  --max-iterations N  최대 반복 (기본: 10)"
    echo ""
    echo "예시:"
    echo "  bash scripts/auto-improve-loop.sh PLAN-001 --target-score 95 --max-iterations 15"
    exit 1
fi

shift

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target-score)
            TARGET_SCORE="$2"
            shift 2
            ;;
        --max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        *)
            echo "❌ 알 수 없는 옵션: $1"
            exit 1
            ;;
    esac
done

# ── 현재 프로젝트 확인 ──────────────────────────────────────
if [[ ! -f "$PROJECT_CONFIG" ]]; then
    echo "❌ .project-config.json을 찾을 수 없습니다."
    exit 1
fi

CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$PROJECT_CONFIG" | cut -d'"' -f4 2>/dev/null)
if [[ -z "$CURRENT_PROJECT" ]]; then
    echo "❌ 현재 활성 프로젝트가 없습니다."
    exit 1
fi

PROJECT_PATH="$WORKSPACE_ROOT/projects/$CURRENT_PROJECT"
EVAL_DIR="$PROJECT_PATH/evaluation"
mkdir -p "$EVAL_DIR"

# ── 자동 승인 모드 ──────────────────────────────────────────
export AUTO_APPROVE=1

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  🔄 Auto-Improve Loop"
echo "║  티켓: $TICKET_NUM"
echo "║  목표 점수: $TARGET_SCORE/100"
echo "║  최대 반복: $MAX_ITERATIONS회"
echo "║  프로젝트: $CURRENT_PROJECT"
echo "╚══════════════════════════════════════════════╝"
echo ""

# ── 초기 평가 (있으면) ──────────────────────────────────────
SCORE_FILE="$EVAL_DIR/${TICKET_NUM}-score.json"
CURRENT_SCORE=0
ITERATION=0

if [[ -f "$SCORE_FILE" ]]; then
    CURRENT_SCORE=$(jq -r '.total_score' "$SCORE_FILE" 2>/dev/null || echo "0")
    echo "📊 기존 평가 점수: $CURRENT_SCORE/100"
else
    echo "📊 초기 평가 실행 중..."
    bash "$SCRIPT_DIR/run-agent.sh" evaluator --ticket "$TICKET_NUM" || {
        echo "❌ 초기 평가 실패"
        exit 1
    }

    if [[ -f "$SCORE_FILE" ]]; then
        CURRENT_SCORE=$(jq -r '.total_score' "$SCORE_FILE" 2>/dev/null || echo "0")
        echo "✅ 초기 점수: $CURRENT_SCORE/100"
    else
        echo "⚠️  평가 점수를 찾을 수 없습니다. 0점으로 시작합니다."
        CURRENT_SCORE=0
    fi
fi

# ── 개선 루프 ──────────────────────────────────────────────
while [[ $CURRENT_SCORE -lt $TARGET_SCORE ]] && [[ $ITERATION -lt $MAX_ITERATIONS ]]; do
    ITERATION=$((ITERATION + 1))

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔄 반복 #$ITERATION / $MAX_ITERATIONS"
    echo "   현재 점수: $CURRENT_SCORE/100"
    echo "   목표 점수: $TARGET_SCORE/100"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # ── Step 1: 이전 평가 리포트 읽기 ──────────────────────
    LATEST_REPORT=$(ls -t "$EVAL_DIR/${TICKET_NUM}"-report-v*.md 2>/dev/null | head -1)

    if [[ -z "$LATEST_REPORT" ]]; then
        echo "⚠️  이전 평가 리포트를 찾을 수 없습니다."
        echo "   Evaluator를 먼저 실행하세요."
        exit 1
    fi

    echo "📋 피드백 로드: $(basename "$LATEST_REPORT")"
    echo ""

    # ── Step 2: Coding Agent 재실행 (피드백 포함) ──────────
    echo "💻 Coding Agent 재실행 중 (피드백 반영)..."

    # 피드백을 프롬프트에 추가
    FEEDBACK_PROMPT="이전 Evaluator 평가 결과를 반영하여 코드를 개선하세요.

## 📊 현재 점수
$CURRENT_SCORE/100 (목표: $TARGET_SCORE/100)

## 📋 평가 리포트
$(cat "$LATEST_REPORT")

## 🎯 작업 지시
1. 위 평가 리포트의 '❌ 실패한 항목'을 모두 수정하세요
2. '🔧 개선 제안'의 우선순위 1 (필수) 항목을 반영하세요
3. 코드 품질을 높이세요
4. 완료 후 '✅ Coding Agent 작업 완료' 메시지를 출력하세요

---

티켓 번호: $TICKET_NUM"

    # Coding Agent 실행
    echo "$FEEDBACK_PROMPT" | bash "$SCRIPT_DIR/run-agent.sh" coding --ticket "$TICKET_NUM" || {
        echo "❌ Coding Agent 실행 실패"
        exit 1
    }

    echo "✅ Coding Agent 완료"
    echo ""

    # ── Step 3: Evaluator 재평가 ──────────────────────────
    echo "📊 Evaluator 재평가 중..."

    bash "$SCRIPT_DIR/run-agent.sh" evaluator --ticket "$TICKET_NUM" || {
        echo "❌ Evaluator 실행 실패"
        exit 1
    }

    # 새 점수 확인
    if [[ -f "$SCORE_FILE" ]]; then
        NEW_SCORE=$(jq -r '.total_score' "$SCORE_FILE" 2>/dev/null || echo "0")
        IMPROVEMENT=$((NEW_SCORE - CURRENT_SCORE))

        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📊 반복 #$ITERATION 결과"
        echo "   이전 점수: $CURRENT_SCORE/100"
        echo "   새 점수: $NEW_SCORE/100"
        echo "   개선: ${IMPROVEMENT:+"+"}$IMPROVEMENT점"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""

        # 점수 업데이트
        CURRENT_SCORE=$NEW_SCORE

        # 점수가 오히려 떨어진 경우
        if [[ $IMPROVEMENT -lt 0 ]]; then
            echo "⚠️  점수가 하락했습니다. 이전 코드로 롤백을 권장합니다."
        fi

        # 점수가 개선되지 않은 경우
        if [[ $IMPROVEMENT -eq 0 ]]; then
            echo "⚠️  점수가 개선되지 않았습니다."
        fi
    else
        echo "❌ 평가 점수 파일을 찾을 수 없습니다."
        exit 1
    fi

    # 목표 달성 확인
    if [[ $CURRENT_SCORE -ge $TARGET_SCORE ]]; then
        echo ""
        echo "🎉 목표 점수 달성!"
        break
    fi

    # 사용자 확인 (선택)
    if [[ -z "$AUTO_APPROVE" ]]; then
        echo ""
        echo "계속 진행하시겠습니까? (y/n)"
        read -r response
        if [[ "$response" != "y" ]]; then
            echo "사용자가 중단했습니다."
            break
        fi
    fi
done

# ── 최종 결과 ──────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  🏁 Auto-Improve Loop 완료"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "📊 최종 결과:"
echo "   티켓: $TICKET_NUM"
echo "   최종 점수: $CURRENT_SCORE/100"
echo "   목표 점수: $TARGET_SCORE/100"
echo "   반복 횟수: $ITERATION회"
echo ""

if [[ $CURRENT_SCORE -ge $TARGET_SCORE ]]; then
    echo "✅ 목표 달성!"
    echo ""
    echo "다음 단계:"
    echo "  mact run qa --ticket $TICKET_NUM  # 테스트 작성"
    exit 0
else
    if [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
        echo "⚠️  최대 반복 횟수 도달 (목표 미달성)"
    else
        echo "⚠️  목표 미달성 (사용자 중단)"
    fi
    echo ""
    echo "권장 조치:"
    echo "  1. 평가 리포트 확인: cat $EVAL_DIR/${TICKET_NUM}-report-v*.md"
    echo "  2. 수동 개선 또는 목표 점수 조정"
    echo "  3. 다시 실행: mact improve $TICKET_NUM --target $TARGET_SCORE"
    exit 1
fi
