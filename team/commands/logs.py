"""
로그 조회 명령어
"""

import json
from pathlib import Path
from datetime import datetime

def get_workspace_root():
    """작업 디렉토리 루트 경로"""
    return Path(__file__).parent.parent

def show_logs(agent: str = None, ticket: str = None, tail: int = None):
    """로그 조회"""
    workspace = get_workspace_root()
    config_file = workspace / ".project-config.json"

    if not config_file.exists():
        print("❌ 활성 프로젝트가 없습니다.")
        return

    with open(config_file, 'r') as f:
        config = json.load(f)

    current_project = config.get('current_project')
    logs_dir = workspace / "projects" / current_project / "logs" / "orchestrator"

    if not logs_dir.exists():
        print("❌ 로그 디렉토리가 없습니다.")
        print("   아직 Agent를 실행하지 않았거나 Orchestrator를 사용하지 않았습니다.")
        return

    # 로그 파일 필터링
    log_files = sorted(logs_dir.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)

    if agent:
        log_files = [f for f in log_files if agent in f.name]

    if ticket:
        log_files = [f for f in log_files if ticket in f.name]

    if not log_files:
        print("❌ 조건에 맞는 로그가 없습니다.")
        return

    # tail 옵션 적용
    if tail:
        log_files = log_files[:tail]

    print(f"\n📋 로그 목록 (최신순, 총 {len(log_files)}개):\n")

    for log_file in log_files:
        # 파일명에서 정보 추출
        # 형식: YYYYMMDD-HHMMSS-agent_name-ticket.log
        parts = log_file.stem.split('-')
        if len(parts) >= 4:
            date = parts[0]
            time = parts[1]
            agent_name = parts[2]
            ticket_name = '-'.join(parts[3:]) if len(parts) > 3 else "N/A"
        else:
            date = "Unknown"
            time = "Unknown"
            agent_name = "Unknown"
            ticket_name = "N/A"

        # 파일 크기
        size_kb = log_file.stat().st_size / 1024

        # 성공/실패 확인 (파일 읽기)
        status = "❓"
        try:
            content = log_file.read_text()
            if "Status: ✅ SUCCESS" in content:
                status = "✅"
            elif "Status: ❌ FAILED" in content:
                status = "❌"
        except:
            pass

        print(f"  {status} {date}-{time} | {agent_name:15s} | {ticket_name:10s} | {size_kb:6.1f} KB")
        print(f"     {log_file.name}")

    print(f"\n로그 파일 경로:")
    print(f"  {logs_dir}")
    print(f"\n로그 보기:")
    print(f"  cat {log_files[0]}")
    print()
