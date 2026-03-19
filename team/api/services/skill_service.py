"""Skill Service - Skill 실행을 담당"""

import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class SkillService:
    """Skill 실행 서비스"""

    def __init__(self):
        self.team_root = Path(__file__).parent.parent.parent
        self.run_skill_script = self.team_root / "scripts" / "run-skill.sh"

    def run_skill(
        self,
        skill_name: str,
        ticket: Optional[str],
        project: str,
        args: Dict[str, Any],
        auto_fix: bool = False
    ) -> Dict[str, Any]:
        """
        Skill 실행

        Returns:
            실행 결과 딕셔너리
        """

        # run-skill.sh 호출
        cmd = [
            "bash",
            str(self.run_skill_script),
            skill_name
        ]

        # 티켓 번호
        if ticket:
            cmd.extend(["--ticket", ticket])

        # Auto-fix
        if auto_fix:
            cmd.append("--auto-fix")

        # 추가 인자
        for key, value in args.items():
            cmd.extend([f"--{key}", str(value)])

        # 프로젝트 디렉토리에서 실행
        project_dir = self.team_root / "projects" / project

        if not project_dir.exists():
            raise Exception(f"Project not found: {project}")

        result = subprocess.run(
            cmd,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=600  # 10분 타임아웃
        )

        # 결과 파싱 (간단한 버전)
        success = result.returncode == 0
        output = result.stdout

        return {
            "success": success,
            "output": output,
            "error": result.stderr if not success else None
        }
