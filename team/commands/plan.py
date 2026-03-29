"""
Project Planner 실행 명령어
"""

import subprocess
import sys
from pathlib import Path

def get_workspace_root():
    """작업 디렉토리 루트 경로"""
    return Path(__file__).parent.parent

def run_planner(project_desc: str = None, req_file: str = None, resume: bool = False):
    """Project Planner 실행"""
    workspace = get_workspace_root()
    run_agent_script = workspace / "scripts" / "run-agent.sh"

    if not run_agent_script.exists():
        print(f"❌ run-agent.sh를 찾을 수 없습니다: {run_agent_script}")
        sys.exit(1)

    # 명령어 구성
    cmd = ["bash", str(run_agent_script), "project-planner"]

    if resume:
        cmd.append("--resume")
    elif project_desc:
        cmd.extend(["--project", project_desc])
    elif req_file:
        cmd.extend(["--req", req_file])
    else:
        print("❌ --project 또는 --req 중 하나는 필수입니다.")
        sys.exit(1)

    # Project Planner 실행
    print("🚀 Project Planner 실행 중...\n")

    try:
        result = subprocess.run(cmd, cwd=workspace)
        if result.returncode == 0:
            print(f"\n✅ 티켓 생성 완료!")
            print(f"\n다음 단계:")
            print(f"  mact run pm --ticket PLAN-001")
            print(f"  mact auto --project \"추가 기능\" --auto-improve")
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자가 중단했습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Project Planner 실패: {e}")
        sys.exit(1)
