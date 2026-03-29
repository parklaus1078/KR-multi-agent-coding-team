"""
프로젝트 상태 조회 명령어
"""

import json
from pathlib import Path

def get_workspace_root():
    """작업 디렉토리 루트 경로"""
    return Path(__file__).parent.parent

def show_status():
    """현재 프로젝트 상태 표시"""
    workspace = get_workspace_root()
    config_file = workspace / ".project-config.json"

    if not config_file.exists():
        print("❌ 활성 프로젝트가 없습니다.")
        print("   프로젝트 초기화: mact init --name my-project")
        return

    with open(config_file, 'r') as f:
        config = json.load(f)

    current_project = config.get('current_project')
    project_path = workspace / "projects" / current_project

    if not project_path.exists():
        print(f"❌ 프로젝트 디렉토리를 찾을 수 없습니다: {current_project}")
        return

    print("\n" + "=" * 60)
    print(f"📊 프로젝트 상태: {current_project}")
    print("=" * 60 + "\n")

    # 티켓 개수
    tickets_dir = project_path / "planning" / "tickets"
    if tickets_dir.exists():
        tickets = [f for f in tickets_dir.iterdir() if f.is_file() and f.name.startswith("PLAN-")]
        print(f"📋 티켓: {len(tickets)}개")
        if tickets:
            print(f"   최신: {sorted([f.name for f in tickets])[-1]}")
    else:
        print(f"📋 티켓: 없음")

    # 명세서 개수
    specs_dir = project_path / "planning" / "specs"
    if specs_dir.exists():
        specs = list(specs_dir.rglob("*.md"))
        print(f"📝 명세서: {len(specs)}개")
    else:
        print(f"📝 명세서: 없음")

    # 소스 코드
    src_dir = project_path / "src"
    if src_dir.exists():
        src_files = list(src_dir.rglob("*"))
        src_files = [f for f in src_files if f.is_file() and not f.name.startswith('.')]
        print(f"💻 소스 파일: {len(src_files)}개")
    else:
        print(f"💻 소스 파일: 없음")

    # 테스트 코드
    tests_dir = project_path / "tests"
    if tests_dir.exists():
        test_files = list(tests_dir.rglob("*test*.py")) + list(tests_dir.rglob("*test*.js"))
        print(f"🧪 테스트 파일: {len(test_files)}개")
    else:
        print(f"🧪 테스트 파일: 없음")

    # 평가 결과
    eval_dir = project_path / "evaluation"
    if eval_dir.exists():
        evaluated_tickets = [d for d in eval_dir.iterdir() if d.is_dir()]
        print(f"📊 평가 완료: {len(evaluated_tickets)}개 티켓")

        # 점수 표시
        for ticket_dir in evaluated_tickets:
            score_file = ticket_dir / "score.txt"
            if score_file.exists():
                score = score_file.read_text().strip()
                print(f"   • {ticket_dir.name}: {score}/100")
    else:
        print(f"📊 평가 결과: 없음")

    print()
    print("📂 프로젝트 경로:")
    print(f"   {project_path}")
    print()

    print("다음 단계:")
    if not tickets:
        print("  mact plan --project \"프로젝트 기능 설명\"")
    elif not specs:
        print("  mact run pm --ticket PLAN-001")
    elif not src_files:
        print("  mact run coding --ticket PLAN-001")
    else:
        print("  mact run evaluator --ticket PLAN-001")
        print("  mact improve PLAN-001 --target 90")
    print()
