"""
전체 파이프라인 자동 실행 명령어
"""

import subprocess
import sys
from pathlib import Path

def get_workspace_root():
    """작업 디렉토리 루트 경로"""
    return Path(__file__).parent.parent

def run_auto_pipeline(
    project_desc: str = None,
    req_file: str = None,
    new_project: bool = False,
    project_name: str = None,
    auto_improve: bool = False,
    target_score: int = 90,
    max_iterations: int = 10,
    discord_webhook: str = None
):
    """전체 파이프라인 자동 실행 (Orchestrator)"""
    workspace = get_workspace_root()
    orchestrator_script = workspace / "scripts" / "orchestrator.py"

    if not orchestrator_script.exists():
        print(f"❌ orchestrator.py를 찾을 수 없습니다: {orchestrator_script}")
        sys.exit(1)

    # 명령어 구성
    cmd = ["python3", str(orchestrator_script)]

    if new_project:
        cmd.append("--new-project")
        if project_name:
            cmd.extend(["--project-name", project_name])

    if project_desc:
        cmd.extend(["--project", project_desc])
    elif req_file:
        cmd.extend(["--req", req_file])
    else:
        print("❌ --project 또는 --req 중 하나는 필수입니다.")
        sys.exit(1)

    if auto_improve:
        cmd.append("--auto-improve")
        cmd.extend(["--target-score", str(target_score)])
        cmd.extend(["--max-iterations", str(max_iterations)])

    if discord_webhook:
        cmd.extend(["--discord-webhook", discord_webhook])

    # Orchestrator 실행
    print("🚀 전체 파이프라인 자동 실행 (0 to 1)")
    if new_project:
        print(f"   새 프로젝트: {project_name or '자동 생성'}")
    print(f"   자동 개선: {'✅ 활성화' if auto_improve else '❌ 비활성화'}")
    if auto_improve:
        print(f"   목표 점수: {target_score}/100")
    if discord_webhook:
        print(f"   Discord 알림: ✅ 활성화")
    print()

    try:
        result = subprocess.run(cmd, cwd=workspace)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자가 중단했습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 파이프라인 실패: {e}")
        sys.exit(1)
