"""
자동 품질 개선 루프 명령어
"""

import subprocess
import sys
from pathlib import Path

def get_workspace_root():
    """작업 디렉토리 루트 경로"""
    return Path(__file__).parent.parent

def run_improve_loop(ticket: str, target_score: int, max_iterations: int):
    """자동 품질 개선 루프 실행"""
    workspace = get_workspace_root()
    improve_script = workspace / "scripts" / "auto-improve-loop.sh"

    if not improve_script.exists():
        print(f"❌ auto-improve-loop.sh를 찾을 수 없습니다: {improve_script}")
        sys.exit(1)

    # 명령어 구성
    cmd = [
        "bash",
        str(improve_script),
        ticket,
        "--target-score", str(target_score),
        "--max-iterations", str(max_iterations)
    ]

    # 개선 루프 실행
    print(f"🔄 자동 품질 개선 루프 시작")
    print(f"   티켓: {ticket}")
    print(f"   목표 점수: {target_score}/100")
    print(f"   최대 반복: {max_iterations}회\n")

    try:
        result = subprocess.run(cmd, cwd=workspace)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자가 중단했습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 개선 루프 실패: {e}")
        sys.exit(1)
