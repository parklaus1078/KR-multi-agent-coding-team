#!/usr/bin/env python3
"""
Memory Loader - .memory/ 시스템 로더

에이전트가 작업 시작 시 과거 학습 패턴을 로드하여
더 나은 의사결정을 할 수 있도록 지원합니다.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class MemoryLoader:
    """메모리 시스템 로더"""

    def __init__(self, workspace_root: Path):
        """
        Args:
            workspace_root: team/ 디렉토리 경로
        """
        self.workspace_root = Path(workspace_root)
        self.memory_dir = self.workspace_root / ".memory"

    def load_patterns(self, agent_name: str) -> Dict:
        """
        특정 에이전트의 학습된 패턴 로드

        Args:
            agent_name: pm, coding, qa, project-planner

        Returns:
            해당 에이전트의 패턴 딕셔너리
        """
        patterns_file = self.memory_dir / "patterns.json"

        if not patterns_file.exists():
            print(f"⚠️  patterns.json을 찾을 수 없습니다: {patterns_file}")
            return {}

        try:
            with open(patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            agent_patterns = data.get(agent_name, {})

            if agent_patterns:
                print(f"✅ {agent_name} 패턴 로드: {len(agent_patterns)}개")
            else:
                print(f"ℹ️  {agent_name} 학습된 패턴 없음")

            return agent_patterns

        except json.JSONDecodeError as e:
            print(f"❌ patterns.json 파싱 실패: {e}")
            return {}
        except Exception as e:
            print(f"❌ 패턴 로드 실패: {e}")
            return {}

    def load_failures(self) -> List[Dict]:
        """실패 사례 로드"""
        failures_file = self.memory_dir / "failures.json"

        if not failures_file.exists():
            return []

        try:
            with open(failures_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            failures = data.get("failures", [])

            if failures:
                print(f"✅ 실패 사례 로드: {len(failures)}개")

            return failures

        except Exception as e:
            print(f"⚠️  실패 사례 로드 실패: {e}")
            return []

    def format_patterns_for_agent(self, agent_name: str) -> str:
        """
        에이전트에게 전달할 패턴 텍스트 생성

        Args:
            agent_name: pm, coding, qa, project-planner

        Returns:
            마크다운 형식의 패턴 가이드
        """
        patterns = self.load_patterns(agent_name)

        if not patterns:
            return ""

        lines = [
            "## 📚 학습된 의사결정 패턴 (과거 성공 사례)",
            "",
            "아래는 과거 작업에서 성공한 의사결정 패턴입니다.",
            "유사한 상황에서 참고하세요:",
            ""
        ]

        for pattern_id, pattern in patterns.items():
            confidence = pattern.get("confidence", 0)
            confidence_emoji = "🟢" if confidence >= 0.9 else "🟡" if confidence >= 0.7 else "🔴"

            lines.append(f"### {confidence_emoji} {pattern.get('id', pattern_id)}")
            lines.append(f"**트리거**: {pattern.get('trigger', 'N/A')}")
            lines.append(f"**결정**: {pattern.get('learned_decision', 'N/A')}")
            lines.append(f"**신뢰도**: {confidence:.0%}")

            if 'notes' in pattern:
                lines.append(f"**참고**: {pattern['notes']}")

            lines.append("")

        return "\n".join(lines)

    def format_failures_summary(self) -> str:
        """실패 사례 요약"""
        failures = self.load_failures()

        if not failures:
            return ""

        lines = [
            "## ⚠️ 과거 실패 사례 요약",
            "",
            "같은 실수를 반복하지 마세요:",
            ""
        ]

        for failure in failures[:5]:  # 최근 5개만
            symptom = failure.get("symptom", "N/A")
            fix = failure.get("fix_applied", "N/A")

            lines.append(f"- **{symptom}** → {fix}")

        lines.append("")
        lines.append(f"*전체 {len(failures)}개 실패 사례 기록됨*")
        lines.append("")

        return "\n".join(lines)

    def get_initial_context(self, agent_name: str) -> str:
        """
        에이전트 시작 시 전달할 전체 컨텍스트

        Args:
            agent_name: pm, coding, qa, project-planner

        Returns:
            학습 패턴 + 실패 요약
        """
        context_parts = []

        # 1. 학습된 패턴
        patterns_text = self.format_patterns_for_agent(agent_name)
        if patterns_text:
            context_parts.append(patterns_text)

        # 2. 실패 사례 요약
        failures_text = self.format_failures_summary()
        if failures_text:
            context_parts.append(failures_text)

        if context_parts:
            return "\n".join(context_parts)
        else:
            return ""


# 테스트 코드
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python memory_loader.py <agent_name>")
        print("Example: python memory_loader.py pm")
        sys.exit(1)

    agent_name = sys.argv[1]

    # 현재 디렉토리 기준으로 team/ 찾기
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent

    loader = MemoryLoader(workspace_root)

    print(f"\n{'='*60}")
    print(f"Memory Loader - {agent_name.upper()} Agent")
    print(f"{'='*60}\n")

    context = loader.get_initial_context(agent_name)

    if context:
        print(context)
    else:
        print("ℹ️  학습된 데이터가 없습니다.")

    print(f"\n{'='*60}\n")
