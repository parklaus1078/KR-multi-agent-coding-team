#!/usr/bin/env python3
"""
Status Command - 프로젝트 상태 조회

현재 프로젝트의 전체 진행 상황을 보여줍니다.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class StatusCommand:
    """프로젝트 상태 조회"""

    def __init__(self, workspace_root: Path):
        """
        Args:
            workspace_root: team/ 디렉토리 경로
        """
        self.workspace_root = Path(workspace_root)
        self.project_config = self.workspace_root / ".project-config.json"
        self.current_project: Optional[str] = None
        self.project_path: Optional[Path] = None

    def load_current_project(self) -> bool:
        """현재 활성 프로젝트 로드"""
        if not self.project_config.exists():
            print("❌ 프로젝트 설정 파일이 없습니다: .project-config.json")
            print("   먼저 프로젝트를 초기화하세요: mact init")
            return False

        try:
            with open(self.project_config, 'r') as f:
                config = json.load(f)

            self.current_project = config.get("current_project")
            if not self.current_project:
                print("❌ 활성 프로젝트가 없습니다.")
                return False

            self.project_path = self.workspace_root / "projects" / self.current_project

            if not self.project_path.exists():
                print(f"❌ 프로젝트 디렉토리를 찾을 수 없습니다: {self.project_path}")
                return False

            return True

        except Exception as e:
            print(f"❌ 프로젝트 설정 로드 실패: {e}")
            return False

    def load_project_meta(self) -> Optional[Dict]:
        """프로젝트 메타데이터 로드"""
        meta_file = self.project_path / ".project-meta.json"

        if not meta_file.exists():
            return None

        try:
            with open(meta_file, 'r') as f:
                return json.load(f)
        except Exception:
            return None

    def get_tickets(self) -> List[str]:
        """티켓 목록 가져오기"""
        tickets_dir = self.project_path / "planning" / "tickets"

        if not tickets_dir.exists():
            return []

        ticket_files = sorted(tickets_dir.glob("PLAN-*.md"))
        tickets = []

        for ticket_file in ticket_files:
            # PLAN-001-user-auth.md → PLAN-001
            parts = ticket_file.stem.split('-', 2)
            if len(parts) >= 2:
                ticket_id = f"{parts[0]}-{parts[1]}"
                if ticket_id not in tickets:
                    tickets.append(ticket_id)

        return sorted(tickets, key=lambda x: int(x.split('-')[1]))

    def get_ticket_status(self, ticket: str) -> str:
        """
        티켓 상태 확인

        Returns:
            not_started, pm_done, coding_done, qa_done, completed
        """
        # PM 명세서 확인
        specs_dir = self.project_path / "planning" / "specs"
        has_spec = False
        if specs_dir.exists():
            spec_files = list(specs_dir.glob(f"{ticket}-*.md"))
            has_spec = len(spec_files) > 0

        if not has_spec:
            return "not_started"

        # Coding 구현 확인 (src/ 디렉토리에 변경사항 있는지)
        # 간단히 evaluation 폴더로 판단
        eval_dir = self.project_path / "evaluation"
        has_eval = False
        if eval_dir.exists():
            eval_files = list(eval_dir.glob(f"{ticket}-*.md"))
            has_eval = len(eval_files) > 0

        if not has_eval:
            return "pm_done"

        # QA 테스트 확인
        tests_dir = self.project_path / "tests"
        has_tests = False
        if tests_dir.exists():
            # 티켓 관련 테스트 파일 있는지 (대략적)
            test_files = list(tests_dir.rglob("*.py")) + list(tests_dir.rglob("*.test.js")) + list(tests_dir.rglob("*.test.ts"))
            has_tests = len(test_files) > 0

        if has_tests:
            return "completed"
        elif has_eval:
            return "coding_done"
        else:
            return "pm_done"

    def get_evaluation_score(self, ticket: str) -> Optional[int]:
        """평가 점수 가져오기"""
        score_file = self.project_path / "evaluation" / f"{ticket}-score.json"

        if not score_file.exists():
            return None

        try:
            with open(score_file, 'r') as f:
                data = json.load(f)
                return data.get("total_score", 0)
        except Exception:
            return None

    def show_status(self):
        """전체 상태 출력"""
        if not self.load_current_project():
            return

        print(f"\n{'='*70}")
        print(f"📊 프로젝트 상태: {self.current_project}")
        print(f"{'='*70}\n")

        # 프로젝트 메타 정보
        meta = self.load_project_meta()
        if meta:
            print("📋 프로젝트 정보:")
            print(f"   타입: {meta.get('project_type', 'N/A')}")
            print(f"   언어: {meta.get('language', 'N/A')}")
            print(f"   프레임워크: {meta.get('framework', 'N/A')}")
            print()

        # 티켓 상태
        tickets = self.get_tickets()

        if not tickets:
            print("⚠️  생성된 티켓이 없습니다.")
            print("   프로젝트 계획: mact plan \"프로젝트 설명\"")
            return

        print(f"📋 티켓 진행 상황: 총 {len(tickets)}개\n")

        status_emoji = {
            "not_started": "⚪",
            "pm_done": "🟡",
            "coding_done": "🟠",
            "qa_done": "🟢",
            "completed": "✅"
        }

        status_text = {
            "not_started": "시작 안 됨",
            "pm_done": "PM 완료",
            "coding_done": "코딩 완료",
            "qa_done": "QA 완료",
            "completed": "완료"
        }

        completed_count = 0
        in_progress_count = 0

        for ticket in tickets:
            status = self.get_ticket_status(ticket)
            emoji = status_emoji.get(status, "❓")
            text = status_text.get(status, "알 수 없음")

            # 평가 점수
            score = self.get_evaluation_score(ticket)
            score_text = f" ({score}/100)" if score is not None else ""

            print(f"   {emoji} {ticket}: {text}{score_text}")

            if status == "completed":
                completed_count += 1
            elif status != "not_started":
                in_progress_count += 1

        print()
        print(f"✅ 완료: {completed_count}/{len(tickets)}")
        print(f"🚧 진행 중: {in_progress_count}/{len(tickets)}")
        print(f"⚪ 대기: {len(tickets) - completed_count - in_progress_count}/{len(tickets)}")
        print()

        # 세션 정보
        sessions_dir = self.project_path / ".sessions"
        if sessions_dir.exists():
            session_map = sessions_dir / "session-map.json"
            if session_map.exists():
                try:
                    with open(session_map, 'r') as f:
                        sessions = json.load(f)

                    session_count = sum(len(v) for v in sessions.values())
                    print(f"💾 저장된 세션: {session_count}개")
                    print()
                except Exception:
                    pass

        # 다음 액션 제안
        print("💡 다음 액션:")
        if in_progress_count == 0 and completed_count == 0:
            print("   mact run pm --ticket PLAN-001        # PM Agent로 첫 티켓 시작")
        elif in_progress_count > 0:
            # 진행 중인 첫 티켓 찾기
            for ticket in tickets:
                status = self.get_ticket_status(ticket)
                if status in ["pm_done", "coding_done"]:
                    if status == "pm_done":
                        print(f"   mact run coding --ticket {ticket}   # 코딩 진행")
                    elif status == "coding_done":
                        print(f"   mact run qa --ticket {ticket}       # QA 테스트 작성")
                    break
        else:
            print("   🎉 모든 티켓 완료!")

        print(f"\n{'='*70}\n")


def main():
    """CLI 엔트리포인트"""
    import sys

    # workspace root 찾기
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent

    cmd = StatusCommand(workspace_root)
    cmd.show_status()


if __name__ == "__main__":
    main()
