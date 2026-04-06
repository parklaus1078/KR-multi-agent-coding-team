#!/usr/bin/env python3
"""
Logs Command - 에이전트 로그 조회

에이전트 실행 로그를 필터링하고 조회합니다.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class LogsCommand:
    """로그 조회 명령"""

    def __init__(self, workspace_root: Path):
        """
        Args:
            workspace_root: team/ 디렉토리 경로
        """
        self.workspace_root = Path(workspace_root)
        self.project_config = self.workspace_root / ".project-config.json"

    def show_logs(self, agent: Optional[str] = None, ticket: Optional[str] = None, tail: Optional[int] = 20):
        """
        로그 조회 및 출력

        Args:
            agent: 에이전트 이름 필터 (pm, coding, qa 등)
            ticket: 티켓 번호 필터 (PLAN-001 등)
            tail: 최신 N개만 표시 (기본: 20)
        """
        if not self.project_config.exists():
            print("❌ 활성 프로젝트가 없습니다.")
            print("   프로젝트를 초기화하세요: mact init")
            return

        try:
            with open(self.project_config, 'r') as f:
                config = json.load(f)

            current_project = config.get('current_project')
            if not current_project:
                print("❌ 활성 프로젝트가 없습니다.")
                return

            project_path = self.workspace_root / "projects" / current_project

            # 여러 로그 디렉토리 확인
            log_locations = [
                project_path / "logs",
                project_path / "logs" / "orchestrator",
                project_path / "logs" / "pm",
                project_path / "logs" / "coding",
                project_path / "logs" / "qa",
                project_path / "decisions"  # decision logs
            ]

            all_log_files = []

            for logs_dir in log_locations:
                if logs_dir.exists():
                    # .log, .md 파일 모두 수집
                    all_log_files.extend(logs_dir.glob("*.log"))
                    all_log_files.extend(logs_dir.glob("*.md"))

            if not all_log_files:
                print(f"⚠️  로그 파일이 없습니다.")
                print(f"   프로젝트: {current_project}")
                print(f"   아직 Agent를 실행하지 않았습니다.")
                return

            # 시간순 정렬 (최신순)
            all_log_files = sorted(all_log_files, key=lambda f: f.stat().st_mtime, reverse=True)

            # 필터링
            if agent:
                all_log_files = [f for f in all_log_files if agent.lower() in f.name.lower()]

            if ticket:
                all_log_files = [f for f in all_log_files if ticket.upper() in f.name.upper()]

            if not all_log_files:
                print(f"❌ 조건에 맞는 로그가 없습니다.")
                if agent:
                    print(f"   Agent: {agent}")
                if ticket:
                    print(f"   Ticket: {ticket}")
                return

            # tail 적용
            if tail:
                all_log_files = all_log_files[:tail]

            print(f"\n{'='*80}")
            print(f"📋 로그 목록: {current_project} (최신순, 총 {len(all_log_files)}개)")
            print(f"{'='*80}\n")

            for log_file in all_log_files:
                # 파일 정보
                size_kb = log_file.stat().st_size / 1024
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                mtime_str = mtime.strftime("%Y-%m-%d %H:%M:%S")

                # 파일명 파싱 (다양한 형식 지원)
                filename = log_file.name
                parent = log_file.parent.name

                # 성공/실패 확인
                status = "❓"
                try:
                    content = log_file.read_text(encoding='utf-8', errors='ignore')
                    if "✅" in content or "SUCCESS" in content.upper() or "완료" in content:
                        status = "✅"
                    elif "❌" in content or "FAILED" in content.upper() or "실패" in content:
                        status = "❌"
                    elif "⚠️" in content or "WARNING" in content.upper() or "경고" in content:
                        status = "⚠️"
                except:
                    pass

                print(f"  {status} {mtime_str} | {parent:15s} | {filename:40s} | {size_kb:6.1f} KB")

            print(f"\n{'='*80}")
            print(f"💡 로그 보기:")
            print(f"   cat {all_log_files[0]}")
            print(f"\n💡 필터링:")
            print(f"   mact logs --agent pm              # PM Agent 로그만")
            print(f"   mact logs --ticket PLAN-001       # PLAN-001 티켓 로그만")
            print(f"   mact logs --tail 10               # 최신 10개만")
            print(f"{'='*80}\n")

        except Exception as e:
            print(f"❌ 로그 조회 실패: {e}")


def main():
    """CLI 엔트리포인트"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="프로젝트 로그 조회")
    parser.add_argument("--agent", help="에이전트 필터 (pm, coding, qa)")
    parser.add_argument("--ticket", help="티켓 번호 필터 (PLAN-001)")
    parser.add_argument("--tail", type=int, default=20, help="최신 N개만 표시 (기본: 20)")

    args = parser.parse_args()

    # workspace root
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent

    cmd = LogsCommand(workspace_root)
    cmd.show_logs(agent=args.agent, ticket=args.ticket, tail=args.tail)


if __name__ == "__main__":
    main()
