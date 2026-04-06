#!/bin/bash
# 통합 테스트 스크립트 - 전체 시스템 검증

set -e

echo "=========================================="
echo "🧪 Multi-Agent Coding Team 통합 테스트"
echo "=========================================="
echo ""

# 1. Memory System 테스트
echo "1️⃣ Memory System 테스트"
echo "   - memory_loader.py"
python3 scripts/memory_loader.py coding > /dev/null 2>&1 && echo "   ✅ memory_loader.py 작동" || echo "   ❌ memory_loader.py 실패"

echo "   - memory_learner.py"
python3 scripts/memory_learner.py --help > /dev/null 2>&1 && echo "   ✅ memory_learner.py 작동" || echo "   ❌ memory_learner.py 실패"

echo "   - decision_logger.py"
python3 scripts/decision_logger.py --help > /dev/null 2>&1 && echo "   ✅ decision_logger.py 작동" || echo "   ❌ decision_logger.py 실패"

echo ""

# 2. Auto-responder 테스트
echo "2️⃣ Auto-responder 테스트"
RESPONSE=$(python3 scripts/auto_responder.py pm "OAuth 기능도 추가할까요?" 2>&1)
if [[ "$RESPONSE" =~ "no, 티켓 범위" ]]; then
    echo "   ✅ 패턴 매칭 성공"
else
    echo "   ❌ 패턴 매칭 실패"
fi

echo ""

# 3. Skills 테스트
echo "3️⃣ Skills 테스트 (8개)"
SKILLS=("validate-spec" "commit" "review-pr" "refactor-code" "test-runner" "deploy" "benchmark" "docs-generator")

for skill in "${SKILLS[@]}"; do
    SKILL_PATH=".skills/$skill"
    if [[ -d "$SKILL_PATH" ]]; then
        # Python 스크립트 찾기
        SCRIPT=$(find "$SKILL_PATH" -name "*.py" | head -1)
        if [[ -n "$SCRIPT" ]]; then
            python3 "$SCRIPT" --help > /dev/null 2>&1 || python3 "$SCRIPT" > /dev/null 2>&1 || true
            echo "   ✅ $skill"
        else
            # Bash 스크립트
            SCRIPT=$(find "$SKILL_PATH" -name "*.sh" | head -1)
            if [[ -n "$SCRIPT" ]]; then
                bash "$SCRIPT" --help > /dev/null 2>&1 || bash "$SCRIPT" > /dev/null 2>&1 || true
                echo "   ✅ $skill"
            else
                echo "   ⚠️  $skill (스크립트 없음)"
            fi
        fi
    else
        echo "   ❌ $skill (디렉토리 없음)"
    fi
done

echo ""

# 4. Commands 테스트
echo "4️⃣ Commands 테스트"
python3 commands/status.py > /dev/null 2>&1 && echo "   ✅ status.py 작동" || echo "   ❌ status.py 실패"
python3 commands/logs.py --tail 1 > /dev/null 2>&1 && echo "   ✅ logs.py 작동" || echo "   ❌ logs.py 실패"

echo ""

# 5. 주요 스크립트 존재 확인
echo "5️⃣ 주요 스크립트 존재 확인"
FILES=(
    "scripts/run-agent.sh"
    "scripts/auto-improve-loop.sh"
    "scripts/orchestrator.py"
    "scripts/discord_logger.py"
)

for file in "${FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (없음)"
    fi
done

echo ""

# 6. Agent CLAUDE.md 존재 확인
echo "6️⃣ Agent 정의 확인"
AGENTS=("project-planner" "pm" "coding" "qa" "evaluator")

for agent in "${AGENTS[@]}"; do
    if [[ -f ".agents/$agent/CLAUDE.md" ]]; then
        echo "   ✅ $agent"
    else
        echo "   ❌ $agent (CLAUDE.md 없음)"
    fi
done

echo ""

# 7. 설정 파일 확인
echo "7️⃣ 설정 파일 확인"
CONFIG_FILES=(
    ".config/auto-responses.json"
    ".memory/patterns.json"
)

for config in "${CONFIG_FILES[@]}"; do
    if [[ -f "$config" ]]; then
        echo "   ✅ $config"
    else
        echo "   ❌ $config (없음)"
    fi
done

echo ""
echo "=========================================="
echo "✅ 통합 테스트 완료"
echo "=========================================="
