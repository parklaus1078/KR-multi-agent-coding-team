#!/usr/bin/env python3
"""
Orchestrator - 전체 파이프라인 자동 실행

Project Planner → (for each ticket) PM → Coding → Evaluator → (improve loop) → QA

Discord 알림, 로깅, 에러 처리 포함
"""

import os
import sys
import json
import time
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Discord Logger import
sys.path.insert(0, str(Path(__file__).parent))
from discord_logger import DiscordLogger


class Orchestrator:
    """전체 파이프라인 오케스트레이터"""

    def __init__(
        self,
        workspace_root: Path,
        auto_improve: bool = False,
        target_score: int = 90,
        max_iterations: int = 10,
        discord_webhook: Optional[str] = None
    ):
        self.workspace_root = Path(workspace_root)
        self.auto_improve = auto_improve
        self.target_score = target_score
        self.max_iterations = max_iterations

        # Discord Logger
        self.discord = DiscordLogger(discord_webhook)

        # 스크립트 경로
        self.scripts_dir = self.workspace_root / "scripts"
        self.run_agent_sh = self.scripts_dir / "run-agent.sh"
        self.auto_improve_sh = self.scripts_dir / "auto-improve-loop.sh"

        # 프로젝트 설정
        self.project_config = self.workspace_root / ".project-config.json"
        self.current_project = None
        self.project_path = None

        # 통계
        self.stats = {
            "total_tickets": 0,
            "completed": 0,
            "failed": 0,
            "ticket_scores": {},
            "start_time": time.time()
        }

    def load_current_project(self):
        """현재 활성 프로젝트 로드"""
        if not self.project_config.exists():
            raise FileNotFoundError(f".project-config.json 없음: {self.project_config}")

        with open(self.project_config, 'r') as f:
            config = json.load(f)

        self.current_project = config.get("current_project")
        if not self.current_project:
            raise ValueError("활성 프로젝트 없음")

        self.project_path = self.workspace_root / "projects" / self.current_project

        if not self.project_path.exists():
            raise FileNotFoundError(f"프로젝트 없음: {self.project_path}")

        print(f"📍 프로젝트: {self.current_project}")
        print(f"📂 경로: {self.project_path}")

    def run_agent(self, agent_name: str, ticket: Optional[str] = None, extra_args: List[str] = None) -> bool:
        """Agent 실행"""
        print(f"\n{'='*60}")
        print(f"🤖 {agent_name.upper()} Agent 실행 중...")
        print(f"{'='*60}\n")

        self.discord.agent_started(agent_name, ticket)

        cmd = ["bash", str(self.run_agent_sh), agent_name]

        if ticket:
            cmd.extend(["--ticket", ticket])

        if extra_args:
            cmd.extend(extra_args)

        # 자동 승인 모드
        env = os.environ.copy()
        env["AUTO_APPROVE"] = "1"

        start = time.time()

        try:
            result = subprocess.run(cmd, cwd=self.workspace_root, env=env)

            duration = time.time() - start

            if result.returncode == 0:
                print(f"\n✅ {agent_name.upper()} Agent 완료 ({duration:.1f}s)\n")
                self.discord.agent_completed(agent_name, ticket, duration)
                return True
            else:
                print(f"\n❌ {agent_name.upper()} Agent 실패 (exit code: {result.returncode})\n")
                self.discord.agent_failed(agent_name, ticket, error=f"Exit code: {result.returncode}")
                return False

        except Exception as e:
            duration = time.time() - start
            print(f"\n❌ {agent_name.upper()} Agent 예외 발생: {e}\n")
            self.discord.agent_failed(agent_name, ticket, error=str(e))
            return False

    def run_improve_loop(self, ticket: str) -> int:
        """Auto-improve loop 실행"""
        print(f"\n{'='*60}")
        print(f"🔄 Auto-Improve Loop")
        print(f"   티켓: {ticket}")
        print(f"   목표: {self.target_score}/100")
        print(f"{'='*60}\n")

        cmd = [
            "bash",
            str(self.auto_improve_sh),
            ticket,
            "--target-score", str(self.target_score),
            "--max-iterations", str(self.max_iterations)
        ]

        # 자동 승인 모드
        env = os.environ.copy()
        env["AUTO_APPROVE"] = "1"

        try:
            result = subprocess.run(cmd, cwd=self.workspace_root, env=env)

            # 점수 확인
            score_file = self.project_path / "evaluation" / f"{ticket}-score.json"
            if score_file.exists():
                with open(score_file, 'r') as f:
                    score_data = json.load(f)
                    final_score = score_data.get("total_score", 0)
                    return final_score
            else:
                return 0

        except Exception as e:
            print(f"❌ Improve loop 실패: {e}")
            return 0

    def get_ticket_list(self) -> List[str]:
        """티켓 목록 가져오기"""
        tickets_dir = self.project_path / "planning" / "tickets"

        if not tickets_dir.exists():
            return []

        ticket_files = sorted(tickets_dir.glob("PLAN-*.md"))
        tickets = [f.stem.split('-')[1] for f in ticket_files]  # PLAN-001 → 001

        # 중복 제거 및 정렬
        tickets = sorted(set(tickets), key=lambda x: int(x))

        return [f"PLAN-{t}" for t in tickets]

    def process_ticket(self, ticket: str) -> bool:
        """티켓 하나 처리"""
        print(f"\n{'🎫'*30}")
        print(f"🎫 티켓 처리: {ticket}")
        print(f"{'🎫'*30}\n")

        # Phase 1: PM Agent
        if not self.run_agent("pm", ticket):
            self.discord.ticket_failed(ticket, "PM Agent 실패")
            return False

        # Phase 2: Coding Agent
        if not self.run_agent("coding", ticket):
            self.discord.ticket_failed(ticket, "Coding Agent 실패")
            return False

        # Phase 3: Evaluator + Improve (선택)
        if self.auto_improve:
            final_score = self.run_improve_loop(ticket)

            if final_score >= self.target_score:
                print(f"✅ 목표 달성: {final_score}/100")
            else:
                print(f"⚠️  목표 미달성: {final_score}/{self.target_score}")

            self.stats["ticket_scores"][ticket] = final_score
        else:
            # Evaluator만 실행
            if not self.run_agent("evaluator", ticket):
                self.discord.ticket_failed(ticket, "Evaluator 실패")
                return False

            # 점수 확인
            score_file = self.project_path / "evaluation" / f"{ticket}-score.json"
            if score_file.exists():
                with open(score_file, 'r') as f:
                    score_data = json.load(f)
                    self.stats["ticket_scores"][ticket] = score_data.get("total_score", 0)

        # Phase 4: QA Agent
        if not self.run_agent("qa", ticket):
            print("⚠️  QA Agent 실패 (계속 진행)")
            # QA 실패는 치명적이지 않음

        self.discord.ticket_completed(
            ticket,
            self.stats["ticket_scores"].get(ticket, 0),
            iterations=1  # TODO: 실제 반복 횟수
        )

        return True

    def run_pipeline(self, project_desc: str = None, req_file: str = None):
        """전체 파이프라인 실행"""
        print("\n" + "="*60)
        print("🚀 Multi-Agent Coding Team - Auto Pipeline")
        print("="*60 + "\n")

        self.discord.pipeline_started(self.current_project, self.auto_improve)

        try:
            # Phase 0: Project Planner
            if project_desc:
                if not self.run_agent("project-planner", extra_args=["--project", project_desc]):
                    raise RuntimeError("Project Planner 실패")
            elif req_file:
                if not self.run_agent("project-planner", extra_args=["--req", req_file]):
                    raise RuntimeError("Project Planner 실패")

            # 티켓 목록 가져오기
            tickets = self.get_ticket_list()

            if not tickets:
                raise RuntimeError("생성된 티켓이 없습니다.")

            self.stats["total_tickets"] = len(tickets)

            print(f"\n📋 생성된 티켓: {len(tickets)}개")
            for ticket in tickets:
                print(f"   - {ticket}")
            print()

            # 각 티켓 처리
            for ticket in tickets:
                if self.process_ticket(ticket):
                    self.stats["completed"] += 1
                else:
                    self.stats["failed"] += 1
                    print(f"⚠️  {ticket} 실패, 다음 티켓 계속...")

            # 완료
            duration = time.time() - self.stats["start_time"]

            print("\n" + "="*60)
            print("🎉 파이프라인 완료!")
            print("="*60 + "\n")

            print(f"📊 통계:")
            print(f"   총 티켓: {self.stats['total_tickets']}개")
            print(f"   완료: {self.stats['completed']}개")
            print(f"   실패: {self.stats['failed']}개")
            print(f"   소요 시간: {int(duration//60)}분 {int(duration%60)}초")
            print()

            print(f"📊 티켓별 점수:")
            for ticket, score in self.stats["ticket_scores"].items():
                emoji = "✅" if score >= 90 else "⚠️" if score >= 70 else "❌"
                print(f"   {emoji} {ticket}: {score}/100")

            self.discord.pipeline_completed(
                self.current_project,
                self.stats["total_tickets"],
                self.stats["completed"],
                self.stats["failed"],
                duration,
                self.stats["ticket_scores"]
            )

        except Exception as e:
            print(f"\n❌ 파이프라인 오류: {e}")
            self.discord.pipeline_failed(self.current_project, "오류 발생", str(e))
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Coding Team Orchestrator"
    )

    parser.add_argument("--new-project", action="store_true", help="새 프로젝트 생성")
    parser.add_argument("--project-name", help="프로젝트 이름")
    parser.add_argument("--project", help="프로젝트 설명")
    parser.add_argument("--req", help="요구사항 파일")
    parser.add_argument("--auto-improve", action="store_true", help="자동 품질 개선")
    parser.add_argument("--target-score", type=int, default=90, help="목표 점수")
    parser.add_argument("--max-iterations", type=int, default=10, help="최대 반복")
    parser.add_argument("--discord-webhook", help="Discord Webhook URL")

    args = parser.parse_args()

    # workspace root
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent

    # 새 프로젝트 생성
    if args.new_project:
        print("🆕 새 프로젝트 생성...")
        if not args.project_name:
            args.project_name = f"project-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        # init 명령 실행
        subprocess.run([
            sys.executable,
            str(workspace_root / "mact.py"),
            "init",
            "--name", args.project_name,
            "--type", "web-fullstack"  # TODO: 타입 선택
        ], cwd=workspace_root)

    # Orchestrator 실행
    orchestrator = Orchestrator(
        workspace_root,
        auto_improve=args.auto_improve,
        target_score=args.target_score,
        max_iterations=args.max_iterations,
        discord_webhook=args.discord_webhook
    )

    orchestrator.load_current_project()
    orchestrator.run_pipeline(args.project, args.req)


if __name__ == "__main__":
    main()
