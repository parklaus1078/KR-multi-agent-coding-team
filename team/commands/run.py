"""
Agent 실행 명령어
"""

import subprocess
import sys
from pathlib import Path

def get_workspace_root():
    """작업 디렉토리 루트 경로"""
    return Path(__file__).parent.parent

def run_agent(agent: str, ticket: str = None, resume: bool = False):
    """Agent 실행"""
    workspace = get_workspace_root()
    run_agent_script = workspace / "scripts" / "run-agent.sh"

    if not run_agent_script.exists():
        print(f"❌ run-agent.sh를 찾을 수 없습니다: {run_agent_script}")
        sys.exit(1)

    # 명령어 구성
    cmd = ["bash", str(run_agent_script), agent]

    if ticket:
        cmd.extend(["--ticket", ticket])

    if resume:
        cmd.append("--resume")

    # Agent 실행
    print(f"🚀 {agent.upper()} Agent 실행 중...\n")

    try:
        result = subprocess.run(cmd, cwd=workspace)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자가 중단했습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Agent 실행 실패: {e}")
        sys.exit(1)
