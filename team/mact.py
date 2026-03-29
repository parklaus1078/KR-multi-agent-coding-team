#!/usr/bin/env python3
"""
MACT - Multi-Agent Coding Team CLI

Tech Stack Agnostic 멀티 에이전트 개발 플랫폼
"""

import sys
import argparse
from pathlib import Path

# 버전 정보
VERSION = "0.0.3"

def main():
    parser = argparse.ArgumentParser(
        prog="mact",
        description="Multi-Agent Coding Team - Tech Stack Agnostic 멀티 에이전트 개발 플랫폼",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # 프로젝트 초기화
  mact init --name "my-blog" --type web-fullstack

  # 프로젝트 목록
  mact projects

  # 프로젝트 선택
  mact use my-blog

  # 티켓 생성
  mact plan --project "블로그 시스템"

  # 개발 파이프라인
  mact run pm --ticket PLAN-001
  mact run coding --ticket PLAN-001
  mact run qa --ticket PLAN-001
  mact run evaluator --ticket PLAN-001

  # 자동 개선 루프
  mact improve PLAN-001 --target 90

  # 전체 자동화 (0 to 1)
  mact auto --project "블로그 시스템" --auto-improve

자세한 도움말: mact <command> --help
        """
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )

    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 명령어")

    # ==================== init ====================
    init_parser = subparsers.add_parser(
        "init",
        help="새 프로젝트 초기화",
        description="새 프로젝트를 생성하고 초기 구조를 설정합니다."
    )
    init_parser.add_argument("--name", required=True, help="프로젝트 이름")
    init_parser.add_argument(
        "--type",
        choices=["web-fullstack", "web-mvc", "cli-tool", "desktop-app"],
        default="web-fullstack",
        help="프로젝트 타입 (기본: web-fullstack)"
    )
    init_parser.add_argument("--interactive", action="store_true", help="대화형 모드")

    # ==================== projects ====================
    projects_parser = subparsers.add_parser(
        "projects",
        aliases=["ls", "list"],
        help="프로젝트 목록 조회",
        description="사용 가능한 프로젝트 목록을 표시합니다."
    )

    # ==================== use ====================
    use_parser = subparsers.add_parser(
        "use",
        aliases=["switch"],
        help="프로젝트 선택",
        description="작업할 프로젝트를 선택합니다."
    )
    use_parser.add_argument("project_name", help="프로젝트 이름")

    # ==================== plan ====================
    plan_parser = subparsers.add_parser(
        "plan",
        help="티켓 생성 (Project Planner)",
        description="프로젝트 설명을 받아 티켓으로 분해합니다."
    )
    plan_group = plan_parser.add_mutually_exclusive_group(required=True)
    plan_group.add_argument("--project", help="프로젝트 설명 (터미널 입력)")
    plan_group.add_argument("--req", help="요구사항 파일 경로")
    plan_parser.add_argument("--resume", action="store_true", help="이전 세션 재개")

    # ==================== run ====================
    run_parser = subparsers.add_parser(
        "run",
        help="Agent 실행",
        description="특정 Agent를 실행합니다."
    )
    run_parser.add_argument(
        "agent",
        choices=["pm", "coding", "qa", "evaluator", "stack-initializer"],
        help="실행할 Agent"
    )
    run_parser.add_argument("--ticket", help="티켓 번호 (예: PLAN-001)")
    run_parser.add_argument("--resume", action="store_true", help="이전 세션 재개")

    # ==================== improve ====================
    improve_parser = subparsers.add_parser(
        "improve",
        help="자동 품질 개선 루프",
        description="Coding ↔ Evaluator 반복으로 목표 점수까지 개선합니다."
    )
    improve_parser.add_argument("ticket", help="티켓 번호 (예: PLAN-001)")
    improve_parser.add_argument("--target", type=int, default=90, help="목표 점수 (기본: 90)")
    improve_parser.add_argument("--max-iterations", type=int, default=10, help="최대 반복 횟수 (기본: 10)")

    # ==================== auto ====================
    auto_parser = subparsers.add_parser(
        "auto",
        help="전체 파이프라인 자동 실행 (0 to 1)",
        description="Project Planner → PM → Coding → QA → Evaluator 전체 자동화"
    )
    auto_group = auto_parser.add_mutually_exclusive_group(required=True)
    auto_group.add_argument("--project", help="프로젝트 설명")
    auto_group.add_argument("--req", help="요구사항 파일 경로")
    auto_parser.add_argument("--new-project", action="store_true", help="새 프로젝트 생성")
    auto_parser.add_argument("--project-name", help="프로젝트명 (새 프로젝트 생성 시)")
    auto_parser.add_argument("--auto-improve", action="store_true", help="자동 품질 개선 활성화")
    auto_parser.add_argument("--target-score", type=int, default=90, help="목표 점수 (기본: 90)")
    auto_parser.add_argument("--max-iterations", type=int, default=10, help="최대 반복 횟수 (기본: 10)")
    auto_parser.add_argument("--discord-webhook", help="Discord Webhook URL (실시간 알림)")

    # ==================== status ====================
    status_parser = subparsers.add_parser(
        "status",
        help="현재 프로젝트 상태",
        description="현재 활성 프로젝트와 티켓 상태를 표시합니다."
    )

    # ==================== logs ====================
    logs_parser = subparsers.add_parser(
        "logs",
        help="로그 조회",
        description="Agent 실행 로그를 조회합니다."
    )
    logs_parser.add_argument("--agent", help="특정 Agent 로그만 조회")
    logs_parser.add_argument("--ticket", help="특정 티켓 로그만 조회")
    logs_parser.add_argument("--tail", type=int, help="최근 N개 로그만 표시")

    # ==================== config ====================
    config_parser = subparsers.add_parser(
        "config",
        help="설정 관리",
        description="시스템 설정을 조회하거나 변경합니다."
    )
    config_parser.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"), help="설정 변경")
    config_parser.add_argument("--get", metavar="KEY", help="설정 조회")
    config_parser.add_argument("--list", action="store_true", help="전체 설정 조회")

    # ==================== memory ====================
    memory_parser = subparsers.add_parser(
        "memory",
        help="학습 시스템 관리",
        description=".memory/ 학습 시스템을 관리합니다."
    )
    memory_subparsers = memory_parser.add_subparsers(dest="memory_command", help="memory 하위 명령어")

    # memory learn
    memory_learn_parser = memory_subparsers.add_parser(
        "learn",
        help="로그에서 패턴 학습",
        description="프로젝트 로그를 분석하여 의사결정 패턴을 학습합니다."
    )
    memory_learn_parser.add_argument("--project", help="프로젝트 이름 (없으면 현재 프로젝트)")
    memory_learn_parser.add_argument("--agents", nargs="+", choices=["pm", "coding", "qa"], help="특정 Agent만 학습")

    # memory show
    memory_show_parser = memory_subparsers.add_parser(
        "show",
        help="학습된 패턴 조회",
        description="현재 학습된 의사결정 패턴을 표시합니다."
    )
    memory_show_parser.add_argument("--agent", choices=["pm", "coding", "qa"], help="특정 Agent만 조회")

    # memory clear
    memory_clear_parser = memory_subparsers.add_parser(
        "clear",
        help="학습 데이터 초기화",
        description="⚠️  모든 학습된 패턴을 삭제합니다 (백업 생성)"
    )
    memory_clear_parser.add_argument("--confirm", action="store_true", help="확인 (필수)")

    # 인자가 없으면 help 출력
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # 명령어 실행
    if args.command in ["projects", "ls", "list"]:
        from commands.projects import list_projects
        list_projects()
    elif args.command in ["use", "switch"]:
        from commands.projects import switch_project
        switch_project(args.project_name)
    elif args.command == "init":
        from commands.init import init_project
        init_project(args.name, args.type, args.interactive)
    elif args.command == "plan":
        from commands.plan import run_planner
        run_planner(args.project, args.req, args.resume)
    elif args.command == "run":
        from commands.run import run_agent
        run_agent(args.agent, args.ticket, args.resume)
    elif args.command == "improve":
        from commands.improve import run_improve_loop
        run_improve_loop(args.ticket, args.target, args.max_iterations)
    elif args.command == "auto":
        from commands.auto import run_auto_pipeline
        run_auto_pipeline(
            args.project,
            args.req,
            args.new_project,
            args.project_name,
            args.auto_improve,
            args.target_score,
            args.max_iterations,
            args.discord_webhook
        )
    elif args.command == "status":
        from commands.status import show_status
        show_status()
    elif args.command == "logs":
        from commands.logs import show_logs
        show_logs(args.agent, args.ticket, args.tail)
    elif args.command == "config":
        from commands.config import manage_config
        manage_config(args.set, args.get, args.list)
    elif args.command == "memory":
        from commands.memory import memory_learn, memory_show, memory_clear
        if args.memory_command == "learn":
            memory_learn(args.project, args.agents)
        elif args.memory_command == "show":
            memory_show(args.agent)
        elif args.memory_command == "clear":
            memory_clear(args.confirm)
        else:
            memory_parser.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
