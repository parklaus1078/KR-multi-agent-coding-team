"""Agent Service - 에이전트 실행을 담당"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any


class AgentService:
    """에이전트 실행 서비스"""

    def __init__(self):
        self.team_root = Path(__file__).parent.parent.parent
        self.run_agent_script = self.team_root / "scripts" / "run-agent.sh"

    def run_agent(
        self,
        agent_name: str,
        ticket: str,
        project: str,
        prompt: Optional[str] = None,
        auto_mode: bool = True
    ) -> Dict[str, Any]:
        """
        에이전트 실행

        Returns:
            {"session_id": str, "message_count": int, "output": str}
        """

        # run-agent.sh 호출
        cmd = [
            "bash",
            str(self.run_agent_script),
            agent_name,
            "--ticket", ticket
        ]

        if auto_mode:
            cmd.append("--auto")

        # 프로젝트 디렉토리에서 실행
        project_dir = self.team_root / "projects" / project

        if not project_dir.exists():
            raise Exception(f"Project not found: {project}")

        result = subprocess.run(
            cmd,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=3600  # 1시간 타임아웃
        )

        if result.returncode != 0:
            raise Exception(f"Agent execution failed: {result.stderr}")

        # 출력 파싱
        output = result.stdout

        # 세션 ID 추출 (간단한 버전)
        session_id = "unknown"
        message_count = 0

        return {
            "session_id": session_id,
            "message_count": message_count,
            "output": output
        }
