"""
프로젝트 초기화 명령어
"""

import subprocess
import sys
from pathlib import Path

def get_workspace_root():
    """작업 디렉토리 루트 경로"""
    return Path(__file__).parent.parent

def init_project(name: str, project_type: str, interactive: bool):
    """프로젝트 초기화"""
    workspace = get_workspace_root()
    init_script = workspace / "scripts" / "init-project.sh"

    if not init_script.exists():
        print(f"❌ init-project.sh를 찾을 수 없습니다: {init_script}")
        sys.exit(1)

    # 명령어 구성
    cmd = ["bash", str(init_script)]

    if interactive:
        cmd.append("--interactive")
    else:
        cmd.extend(["--name", name, "--type", project_type])

    # 초기화 실행
    print(f"🚀 프로젝트 초기화 중: {name} ({project_type})\n")

    try:
        result = subprocess.run(cmd, cwd=workspace)
        if result.returncode == 0:
            print(f"\n✅ 프로젝트 초기화 완료!")
            print(f"\n다음 단계:")
            print(f"  mact use {name}")
            print(f"  mact plan --project \"프로젝트 기능 설명\"")
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자가 중단했습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 초기화 실패: {e}")
        sys.exit(1)
