"""
프로젝트 관리 명령어
"""

import json
from pathlib import Path

def get_workspace_root():
    """작업 디렉토리 루트 경로"""
    return Path(__file__).parent.parent

def list_projects():
    """프로젝트 목록 조회"""
    workspace = get_workspace_root()
    projects_dir = workspace / "projects"
    config_file = workspace / ".project-config.json"

    if not projects_dir.exists():
        print("❌ projects/ 디렉토리가 없습니다.")
        return

    projects = [p.name for p in projects_dir.iterdir() if p.is_dir() and not p.name.startswith('.')]

    if not projects:
        print("❌ 프로젝트가 없습니다.")
        print("   새 프로젝트 생성: mact init --name my-project")
        return

    # 현재 활성 프로젝트 확인
    current_project = None
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            current_project = config.get('current_project')

    print("\n📂 사용 가능한 프로젝트:\n")
    for p in sorted(projects):
        marker = " ← 현재 활성" if p == current_project else ""
        print(f"  • {p}{marker}")

    print(f"\n총 {len(projects)}개 프로젝트")
    print("\n사용법:")
    print(f"  mact use {projects[0]}")
    print()

def switch_project(project_name: str):
    """프로젝트 선택"""
    workspace = get_workspace_root()
    project_path = workspace / "projects" / project_name
    config_file = workspace / ".project-config.json"

    if not project_path.exists():
        print(f"❌ 프로젝트를 찾을 수 없습니다: {project_name}")
        print("\n사용 가능한 프로젝트:")
        list_projects()
        return

    # .project-config.json 업데이트
    config = {
        "current_project": project_name,
        "current_project_path": f"projects/{project_name}",
        "recent_projects": [project_name]
    }

    if config_file.exists():
        with open(config_file, 'r') as f:
            old_config = json.load(f)
            recent = old_config.get('recent_projects', [])
            if project_name in recent:
                recent.remove(project_name)
            recent.insert(0, project_name)
            config['recent_projects'] = recent[:10]

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✅ 프로젝트 선택: {project_name}")
    print(f"📂 경로: {project_path}")
    print()
    print("다음 단계:")
    print(f"  mact plan --project \"프로젝트 기능 설명\"")
    print(f"  mact run pm --ticket PLAN-001")
