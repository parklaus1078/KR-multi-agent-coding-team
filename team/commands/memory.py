"""
Memory 시스템 관리 명령어
"""

import subprocess
import sys
from pathlib import Path


def get_workspace_root():
    """작업 디렉토리 루트"""
    return Path(__file__).parent.parent


def get_current_project():
    """현재 활성 프로젝트 가져오기"""
    workspace = get_workspace_root()
    config_file = workspace / ".project-config.json"

    if not config_file.exists():
        return None

    import json
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get("current_project")
    except:
        return None


def memory_learn(project: str = None, agents: list = None):
    """프로젝트 로그에서 패턴 학습"""
    workspace = get_workspace_root()
    learner_script = workspace / "scripts" / "memory_learner.py"

    if not learner_script.exists():
        print(f"❌ memory_learner.py를 찾을 수 없습니다.")
        sys.exit(1)

    # 프로젝트 결정
    if not project:
        project = get_current_project()
        if not project:
            print("❌ 현재 활성 프로젝트가 없습니다.")
            print("   mact use <project-name> 또는 --project 옵션 사용")
            sys.exit(1)

    project_path = workspace / "projects" / project

    if not project_path.exists():
        print(f"❌ 프로젝트를 찾을 수 없습니다: {project}")
        sys.exit(1)

    # 명령어 구성
    cmd = ["python3", str(learner_script), str(project_path)]

    if agents:
        cmd.extend(agents)

    # 학습 실행
    print(f"🧠 Memory Learning: {project}\n")

    try:
        result = subprocess.run(cmd, cwd=workspace)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자가 중단했습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 학습 실패: {e}")
        sys.exit(1)


def memory_show(agent: str = None):
    """현재 학습된 패턴 조회"""
    workspace = get_workspace_root()
    loader_script = workspace / "scripts" / "memory_loader.py"

    if not loader_script.exists():
        print(f"❌ memory_loader.py를 찾을 수 없습니다.")
        sys.exit(1)

    if not agent:
        print("📚 학습된 패턴 요약\n")
        agents = ["pm", "coding", "qa"]
    else:
        agents = [agent]

    for ag in agents:
        cmd = ["python3", str(loader_script), ag]

        try:
            subprocess.run(cmd, cwd=workspace)
        except:
            pass


def memory_clear(confirm: bool = False):
    """학습된 패턴 초기화 (위험!)"""
    if not confirm:
        print("⚠️  학습된 모든 패턴이 삭제됩니다!")
        print("   계속하려면 --confirm 플래그를 추가하세요:")
        print("   mact memory clear --confirm")
        sys.exit(1)

    workspace = get_workspace_root()
    memory_dir = workspace / ".memory"

    files_to_clear = [
        "patterns.json",
        "failures.json",
        "successes.json",
        "commit-history.json",
        "review-history.json"
    ]

    print("🗑️  메모리 시스템 초기화 중...\n")

    for filename in files_to_clear:
        file_path = memory_dir / filename
        if file_path.exists():
            try:
                # 백업
                backup_path = file_path.with_suffix('.json.bak')
                import shutil
                shutil.copy(file_path, backup_path)
                print(f"   💾 백업: {filename}.bak")

                # 빈 구조로 초기화
                if filename == "patterns.json":
                    import json
                    from datetime import datetime

                    empty = {
                        "version": "0.0.1",
                        "updated": datetime.now().strftime("%Y-%m-%d"),
                        "description": "학습된 의사결정 패턴",
                        "pm": {},
                        "coding": {},
                        "qa": {},
                        "global": {},
                        "learning_metadata": {
                            "total_patterns": 0,
                            "last_learning_run": None
                        }
                    }

                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(empty, f, indent=2, ensure_ascii=False)

                print(f"   ✅ 초기화: {filename}")

            except Exception as e:
                print(f"   ❌ 실패: {filename} - {e}")

    print("\n✅ 메모리 시스템이 초기화되었습니다.")
    print("   백업 파일: .memory/*.bak")
