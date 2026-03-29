#!/usr/bin/env python3
"""
Decision Logger - 의사결정 로그 기록

에이전트가 작업 중 내린 의사결정을 구조화된 형식으로 기록하여
나중에 학습 시스템이 패턴을 추출할 수 있도록 합니다.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class DecisionLogger:
    """의사결정 로거"""

    def __init__(self, project_path: Path, agent_name: str, ticket: str):
        """
        Args:
            project_path: 프로젝트 경로 (projects/xxx/)
            agent_name: pm, coding, qa
            ticket: 티켓 번호 (PLAN-001)
        """
        self.project_path = Path(project_path)
        self.agent_name = agent_name
        self.ticket = ticket

        # 로그 디렉토리
        self.logs_dir = self.project_path / "logs" / agent_name
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # 로그 파일명
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_file = self.logs_dir / f"{timestamp}-{ticket}.json"

        # 로그 데이터 초기화
        self.log_data = {
            "metadata": {
                "agent": agent_name,
                "ticket": ticket,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "decision_count": 0,
                "completion_status": "unknown"
            },
            "decisions": [],
            "gotchas_applied": [],
            "patterns_observed": [],
            "auto_responses_triggered": [],
            "issues_encountered": []
        }

    def add_decision(
        self,
        decision_id: str,
        title: str,
        context: str,
        options: List[str],
        selected: str,
        reason: str,
        risk_level: str = "low",
        confidence: float = 0.8,
        gotcha_applied: Optional[str] = None
    ):
        """
        의사결정 추가

        Args:
            decision_id: 결정 ID (D-001)
            title: 결정 제목
            context: 결정이 필요했던 상황
            options: 고려한 옵션들
            selected: 선택한 옵션
            reason: 선택 이유
            risk_level: low|medium|high
            confidence: 신뢰도 (0.0-1.0)
            gotcha_applied: 적용한 Gotcha (gotchas.md#1)
        """
        decision = {
            "id": decision_id,
            "title": title,
            "context": context,
            "options": options,
            "selected": selected,
            "reason": reason,
            "risk_level": risk_level,
            "confidence": confidence,
            "outcome": "unknown"
        }

        if gotcha_applied:
            decision["gotcha_applied"] = gotcha_applied

        self.log_data["decisions"].append(decision)
        self.log_data["metadata"]["decision_count"] += 1

    def add_gotcha(self, gotcha_id: str, gotcha_title: str, how_applied: str):
        """Gotcha 적용 기록"""
        self.log_data["gotchas_applied"].append({
            "gotcha_id": gotcha_id,
            "gotcha_title": gotcha_title,
            "how_applied": how_applied
        })

    def add_pattern_observed(self, pattern: str, frequency: str, confidence: float):
        """관찰된 패턴 기록"""
        self.log_data["patterns_observed"].append({
            "pattern": pattern,
            "frequency": frequency,
            "confidence": confidence
        })

    def add_auto_response(self, rule_id: str, trigger: str, response: str):
        """자동 응답 규칙 발동 기록"""
        self.log_data["auto_responses_triggered"].append({
            "rule_id": rule_id,
            "trigger": trigger,
            "response": response
        })

    def add_issue(self, issue: str, severity: str, resolution: str):
        """이슈 발생 기록 (향후 Gotcha 후보)"""
        self.log_data["issues_encountered"].append({
            "issue": issue,
            "severity": severity,
            "resolution": resolution
        })

    def set_completion_status(self, status: str):
        """작업 완료 상태 설정: success|partial|failed"""
        self.log_data["metadata"]["completion_status"] = status

    def save(self):
        """로그 파일 저장"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.log_data, f, indent=2, ensure_ascii=False)

            print(f"✅ 의사결정 로그 저장: {self.log_file}")
            return True

        except Exception as e:
            print(f"❌ 로그 저장 실패: {e}")
            return False

    def save_markdown(self):
        """마크다운 형식으로도 저장 (사람이 읽기 쉽게)"""
        md_file = self.log_file.with_suffix('.md')

        lines = [
            f"# {self.agent_name.upper()} Agent - {self.ticket}",
            "",
            f"- **Timestamp**: {self.log_data['metadata']['timestamp']}",
            f"- **Decision Count**: {self.log_data['metadata']['decision_count']}",
            f"- **Status**: {self.log_data['metadata']['completion_status']}",
            "",
            "---",
            ""
        ]

        # 의사결정
        if self.log_data["decisions"]:
            lines.append("## 📋 의사결정")
            lines.append("")

            for decision in self.log_data["decisions"]:
                risk_emoji = {
                    "low": "🟢",
                    "medium": "🟡",
                    "high": "🔴"
                }.get(decision["risk_level"], "⚪")

                lines.append(f"### {risk_emoji} {decision['id']}: {decision['title']}")
                lines.append(f"**상황**: {decision['context']}")
                lines.append(f"**옵션**: {', '.join(decision['options'])}")
                lines.append(f"**선택**: {decision['selected']}")
                lines.append(f"**이유**: {decision['reason']}")
                lines.append(f"**위험도**: {decision['risk_level']} | **신뢰도**: {decision['confidence']:.0%}")

                if "gotcha_applied" in decision:
                    lines.append(f"**적용된 Gotcha**: {decision['gotcha_applied']}")

                lines.append("")

        # Gotchas
        if self.log_data["gotchas_applied"]:
            lines.append("## ⚠️ 적용된 Gotchas")
            lines.append("")

            for gotcha in self.log_data["gotchas_applied"]:
                lines.append(f"- **#{gotcha['gotcha_id']}** {gotcha['gotcha_title']}")
                lines.append(f"  - {gotcha['how_applied']}")

            lines.append("")

        # 관찰된 패턴
        if self.log_data["patterns_observed"]:
            lines.append("## 🔍 관찰된 패턴")
            lines.append("")

            for pattern in self.log_data["patterns_observed"]:
                lines.append(f"- {pattern['pattern']} (신뢰도: {pattern['confidence']:.0%})")

            lines.append("")

        # 이슈
        if self.log_data["issues_encountered"]:
            lines.append("## 🚨 발생한 이슈")
            lines.append("")

            for issue in self.log_data["issues_encountered"]:
                lines.append(f"- **[{issue['severity'].upper()}]** {issue['issue']}")
                lines.append(f"  - 해결: {issue['resolution']}")

            lines.append("")

        try:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))

            print(f"✅ Markdown 로그 저장: {md_file}")
            return True

        except Exception as e:
            print(f"❌ Markdown 저장 실패: {e}")
            return False


# 테스트 코드
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python decision_logger.py <project_path> <agent_name> <ticket>")
        print("Example: python decision_logger.py projects/test-project pm PLAN-001")
        sys.exit(1)

    project_path = sys.argv[1]
    agent_name = sys.argv[2]
    ticket = sys.argv[3]

    logger = DecisionLogger(Path(project_path), agent_name, ticket)

    # 예시 의사결정 추가
    logger.add_decision(
        decision_id="D-001",
        title="OAuth 제외",
        context="티켓에 'login' 명시, 방법 미지정",
        options=["Email/Password만", "OAuth", "둘 다"],
        selected="Email/Password만",
        reason="Acceptance Criteria에 'email/password'만 명시. OAuth는 Out-of-Scope.",
        risk_level="low",
        confidence=0.95,
        gotcha_applied="gotchas.md#1"
    )

    logger.add_gotcha(
        gotcha_id="1",
        gotcha_title="범위 확대 (Scope Creep)",
        how_applied="티켓 Acceptance Criteria 확인 후 OAuth 제외"
    )

    logger.set_completion_status("success")

    # 저장
    logger.save()
    logger.save_markdown()

    print("\n✅ 테스트 완료!")
