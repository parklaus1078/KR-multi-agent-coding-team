#!/usr/bin/env python3
"""
Memory Learner - 로그에서 패턴 학습

의사결정 로그를 분석하여 성공/실패 패턴을 추출하고
.memory/ 시스템을 업데이트합니다.
"""

import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
from datetime import datetime


class MemoryLearner:
    """메모리 학습 시스템"""

    def __init__(self, workspace_root: Path):
        """
        Args:
            workspace_root: team/ 디렉토리
        """
        self.workspace_root = Path(workspace_root)
        self.memory_dir = self.workspace_root / ".memory"

        # 메모리 파일들
        self.patterns_file = self.memory_dir / "patterns.json"
        self.failures_file = self.memory_dir / "failures.json"
        self.successes_file = self.memory_dir / "successes.json"

    def load_patterns(self) -> Dict:
        """현재 패턴 로드"""
        if not self.patterns_file.exists():
            return self._create_empty_patterns()

        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  패턴 로드 실패: {e}")
            return self._create_empty_patterns()

    def _create_empty_patterns(self) -> Dict:
        """빈 패턴 구조 생성"""
        return {
            "version": "0.0.1",
            "updated": datetime.now().strftime("%Y-%m-%d"),
            "description": "학습된 의사결정 패턴",
            "pm": {},
            "coding": {},
            "qa": {},
            "global": {},
            "learning_metadata": {
                "total_patterns": 0,
                "last_learning_run": None,
                "next_learning_scheduled": None,
                "learning_algorithm_version": "0.0.1"
            }
        }

    def load_decision_logs(self, project_path: Path, agent_name: str) -> List[Dict]:
        """특정 에이전트의 의사결정 로그 로드"""
        logs_dir = project_path / "logs" / agent_name
        if not logs_dir.exists():
            return []

        logs = []
        for log_file in logs_dir.glob("*.json"):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    logs.append(log_data)
            except Exception as e:
                print(f"⚠️  로그 읽기 실패 ({log_file.name}): {e}")

        return logs

    def extract_patterns_from_logs(self, logs: List[Dict], agent_name: str) -> Dict:
        """로그에서 패턴 추출"""
        patterns = {}

        # 결정별 빈도 추적
        decision_tracker = defaultdict(lambda: {
            "count": 0,
            "successes": 0,
            "triggers": set(),
            "decisions": set(),
            "confidences": []
        })

        for log in logs:
            status = log["metadata"].get("completion_status", "unknown")
            decisions = log.get("decisions", [])

            for decision in decisions:
                key = decision.get("title", "").lower()
                if not key:
                    continue

                tracker = decision_tracker[key]
                tracker["count"] += 1

                if status == "success":
                    tracker["successes"] += 1

                # 트리거 수집 (컨텍스트)
                context = decision.get("context", "")
                if context:
                    tracker["triggers"].add(context)

                # 결정 수집
                selected = decision.get("selected", "")
                if selected:
                    tracker["decisions"].add(selected)

                # 신뢰도 수집
                confidence = decision.get("confidence", 0)
                if confidence > 0:
                    tracker["confidences"].append(confidence)

        # 패턴 생성 (성공률 50% 이상, 2회 이상 발생)
        pattern_id = 1
        for title, tracker in decision_tracker.items():
            if tracker["count"] < 2:
                continue

            success_rate = tracker["successes"] / tracker["count"] if tracker["count"] > 0 else 0

            if success_rate >= 0.5:
                # 평균 신뢰도
                avg_confidence = sum(tracker["confidences"]) / len(tracker["confidences"]) if tracker["confidences"] else 0.5

                pattern = {
                    "id": f"{agent_name}-pattern-{pattern_id:03d}",
                    "trigger": " OR ".join(list(tracker["triggers"])[:3]),  # 상위 3개
                    "learned_decision": " / ".join(list(tracker["decisions"])[:2]),  # 상위 2개
                    "confidence": round(avg_confidence, 2),
                    "learned_from": f"{tracker['count']} logs",
                    "success_rate": f"{tracker['successes']}/{tracker['count']}",
                    "last_updated": datetime.now().strftime("%Y-%m-%d"),
                    "notes": f"자동 학습: 성공률 {success_rate:.0%}"
                }

                patterns[pattern["id"]] = pattern
                pattern_id += 1

        return patterns

    def update_patterns(self, project_path: Path, agent_name: str):
        """특정 에이전트의 패턴 업데이트"""
        print(f"\n🧠 {agent_name.upper()} Agent 학습 시작...")

        # 로그 로드
        logs = self.load_decision_logs(project_path, agent_name)
        if not logs:
            print(f"   ℹ️  분석할 로그 없음")
            return

        print(f"   📊 {len(logs)}개 로그 분석 중...")

        # 패턴 추출
        new_patterns = self.extract_patterns_from_logs(logs, agent_name)
        if not new_patterns:
            print(f"   ℹ️  추출된 패턴 없음")
            return

        print(f"   ✅ {len(new_patterns)}개 패턴 추출")

        # 기존 패턴 로드
        all_patterns = self.load_patterns()

        # 에이전트별 패턴 업데이트 (기존 수동 패턴 유지)
        if agent_name not in all_patterns:
            all_patterns[agent_name] = {}

        # 자동 학습 패턴만 업데이트 (수동 패턴은 보존)
        for pattern_id, pattern in new_patterns.items():
            # 기존 패턴이 있고, 수동으로 작성된 것이면 건너뛰기
            existing = all_patterns[agent_name].get(pattern_id)
            if existing and "자동 학습" not in existing.get("notes", ""):
                print(f"   ⏭️  {pattern_id} - 수동 패턴 보존")
                continue

            all_patterns[agent_name][pattern_id] = pattern
            print(f"   📝 {pattern_id} - 업데이트")

        # 메타데이터 업데이트
        all_patterns["updated"] = datetime.now().strftime("%Y-%m-%d")
        all_patterns["learning_metadata"]["last_learning_run"] = datetime.now().isoformat()
        all_patterns["learning_metadata"]["total_patterns"] = sum(
            len(patterns) for key, patterns in all_patterns.items()
            if key not in ["version", "updated", "description", "learning_metadata"]
        )

        # 저장
        try:
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                json.dump(all_patterns, f, indent=2, ensure_ascii=False)

            print(f"   ✅ patterns.json 업데이트 완료")

        except Exception as e:
            print(f"   ❌ 저장 실패: {e}")

    def learn_from_project(self, project_path: Path, agents: List[str] = None):
        """프로젝트 전체에서 학습"""
        if agents is None:
            agents = ["pm", "coding", "qa"]

        print(f"{'='*60}")
        print(f"Memory Learning - {project_path.name}")
        print(f"{'='*60}")

        for agent_name in agents:
            self.update_patterns(project_path, agent_name)

        print(f"\n{'='*60}")
        print("✅ 학습 완료!")
        print(f"{'='*60}\n")


# 테스트 및 실행
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python memory_learner.py <project_path> [agent1 agent2 ...]")
        print("Example: python memory_learner.py projects/test-project")
        print("Example: python memory_learner.py projects/test-project pm coding")
        sys.exit(1)

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(f"❌ 프로젝트를 찾을 수 없습니다: {project_path}")
        sys.exit(1)

    # workspace root 찾기
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent

    learner = MemoryLearner(workspace_root)

    # 특정 에이전트만 지정했으면 그것만 학습
    agents = sys.argv[2:] if len(sys.argv) > 2 else None

    learner.learn_from_project(project_path, agents)
