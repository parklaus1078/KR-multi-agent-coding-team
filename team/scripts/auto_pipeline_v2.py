#!/usr/bin/env python3
"""
Auto Pipeline v2 - Claude Code 대화형 세션 기반

Claude Code의 대화형 특성을 활용한 새로운 파이프라인:
1. 각 에이전트마다 새 터미널 탭에서 세션 시작
2. 세션을 유지하여 사용자가 나중에 복귀 가능
3. 세션 ID 기록 및 관리
4. 에이전트 간 순차 실행

⚠️ 중요:
- macOS 전용 (Terminal.app + AppleScript 사용)
- Claude Code CLI 필수
- 사용자가 각 단계를 확인하며 진행
"""

import os
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AutoPipelineV2:
    """
    Claude Code 대화형 세션 기반 Auto Pipeline

    아키텍처:
    1. 각 에이전트 = 별도 Terminal 탭
    2. 세션 유지 (종료하지 않음)
    3. .sessions/session-map.json에 탭 ID 기록
    4. 사용자가 나중에 탭으로 복귀 가능
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.workspace_root = self.project_path.parent.parent
        self.sessions_dir = self.project_path / ".sessions"
        self.sessions_dir.mkdir(exist_ok=True)

        # 세션 맵 파일
        self.session_map_file = self.sessions_dir / "session-map.json"
        self.session_map = self._load_session_map()

        # Terminal.app 지원 확인 (macOS 전용)
        self._check_macos()

    def _check_macos(self):
        """macOS 및 Terminal.app 확인"""
        if os.uname().sysname != "Darwin":
            raise RuntimeError("이 스크립트는 macOS 전용입니다.")

        print("✅ macOS 확인")
        print("✅ Terminal.app 세션 관리 활성화")

    def _load_session_map(self) -> dict:
        """세션 맵 로드"""
        if self.session_map_file.exists():
            with open(self.session_map_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_session_map(self):
        """세션 맵 저장"""
        with open(self.session_map_file, 'w') as f:
            json.dump(self.session_map, f, indent=2)
        print(f"✅ 세션 맵 저장: {self.session_map_file}")

    def open_agent_in_new_tab(
        self,
        agent_name: str,
        ticket_num: str,
        initial_prompt: str
    ) -> str:
        """
        새 Terminal 탭에서 에이전트 세션 시작

        Args:
            agent_name: pm, coding, qa 등
            ticket_num: 티켓 번호 (예: BILL-001)
            initial_prompt: 초기 프롬프트

        Returns:
            세션 ID (Terminal 탭 식별자)
        """
        agent_dir = self.workspace_root / ".agents" / agent_name

        if not agent_dir.exists():
            raise FileNotFoundError(f"에이전트 디렉토리 없음: {agent_dir}")

        # 세션 ID 생성 (타임스탬프 기반)
        session_id = f"{agent_name}-{ticket_num}-{int(time.time())}"

        # 이전 세션 컨텍스트 로드
        context_text = self._load_previous_sessions_text(ticket_num, agent_name)

        # 최종 프롬프트 조합
        if context_text:
            full_prompt = f"""## 이전 에이전트 세션 정보

{context_text}

---

## 현재 작업

{initial_prompt}
"""
        else:
            full_prompt = initial_prompt

        # 프롬프트 파일 생성
        prompt_file = self.sessions_dir / f".prompt-{session_id}.txt"
        prompt_file.write_text(full_prompt, encoding='utf-8')

        # AppleScript로 새 Terminal 탭 열기
        applescript = f'''
tell application "Terminal"
    activate

    -- 새 탭 생성
    tell application "System Events"
        keystroke "t" using command down
    end tell

    delay 0.5

    -- 에이전트 디렉토리로 이동
    do script "cd {agent_dir}" in front window

    delay 0.3

    -- Claude Code 실행 (프롬프트 파일로 초기화)
    do script "echo '🤖 {agent_name.upper()} Agent 세션 시작'" in front window
    do script "echo '📋 Ticket: {ticket_num}'" in front window
    do script "echo '🔑 Session ID: {session_id}'" in front window
    do script "echo ''" in front window
    do script "cat {prompt_file}" in front window
    do script "echo ''" in front window
    do script "echo '⬆️ 위 프롬프트를 복사하여 Claude Code에 붙여넣으세요.'" in front window
    do script "echo ''" in front window
    do script "claude" in front window

    -- 탭 타이틀 설정
    set custom title of front window to "{agent_name.upper()} - {ticket_num}"
end tell
'''

        # AppleScript 실행
        subprocess.run(
            ["osascript", "-e", applescript],
            check=True
        )

        print(f"\n{'='*60}")
        print(f"✅ 새 Terminal 탭에서 {agent_name.upper()} Agent 시작")
        print(f"📋 Ticket: {ticket_num}")
        print(f"🔑 Session ID: {session_id}")
        print(f"📁 Agent Dir: {agent_dir}")
        print('='*60)

        # 세션 맵에 기록
        if ticket_num not in self.session_map:
            self.session_map[ticket_num] = {}

        self.session_map[ticket_num][agent_name] = {
            "session_id": session_id,
            "started_at": datetime.now().isoformat(),
            "status": "active",
            "agent_dir": str(agent_dir),
            "prompt_file": str(prompt_file)
        }

        self._save_session_map()

        return session_id

    def _load_previous_sessions_text(self, ticket_num: str, current_agent: str) -> str:
        """이전 에이전트 세션 요약 텍스트 생성"""
        agent_order = ["project-planner", "pm", "coding", "qa"]

        try:
            current_index = agent_order.index(current_agent)
        except ValueError:
            return ""

        previous_agents = agent_order[:current_index]

        if ticket_num not in self.session_map:
            return ""

        context_parts = []

        for prev_agent in previous_agents:
            if prev_agent in self.session_map[ticket_num]:
                session_info = self.session_map[ticket_num][prev_agent]
                context_parts.append(f"""### {prev_agent.upper()} Agent
- Session ID: {session_info['session_id']}
- Started: {session_info['started_at']}
- Status: {session_info['status']}

작업 내용은 Terminal 탭에서 확인 가능합니다.
""")

        if not context_parts:
            return ""

        return "\n".join(context_parts)

    def wait_for_user_confirmation(self, agent_name: str, ticket_num: str):
        """
        사용자가 에이전트 작업 완료를 확인할 때까지 대기

        사용자는 Terminal 탭에서 에이전트와 대화하며 작업 완료.
        완료 후 이 스크립트로 돌아와서 Enter 입력.
        """
        print(f"\n{'='*60}")
        print(f"⏳ {agent_name.upper()} Agent 작업 대기 중...")
        print(f"📋 Ticket: {ticket_num}")
        print(f"\n지침:")
        print(f"1. Terminal 탭 '{agent_name.upper()} - {ticket_num}'으로 이동")
        print(f"2. Claude Code와 대화하며 작업 완료")
        print(f"3. 작업 완료 후 이 창으로 돌아와서 Enter 입력")
        print('='*60)

        input("\n✅ 작업 완료 후 Enter를 누르세요... ")

        # 세션 상태 업데이트
        if ticket_num in self.session_map and agent_name in self.session_map[ticket_num]:
            self.session_map[ticket_num][agent_name]["status"] = "completed"
            self.session_map[ticket_num][agent_name]["completed_at"] = datetime.now().isoformat()
            self._save_session_map()

        print(f"✅ {agent_name.upper()} Agent 작업 완료 확인")

    def run_full_pipeline(self, ticket_num: str):
        """
        전체 파이프라인 실행

        Args:
            ticket_num: 티켓 번호 (예: BILL-001)

        흐름:
        1. PM Agent → 새 탭 열기 → 사용자 작업 → 확인 대기
        2. Coding Agent → 새 탭 열기 → 사용자 작업 → 확인 대기
        3. QA Agent → 새 탭 열기 → 사용자 작업 → 확인 대기
        """
        print(f"\n{'='*60}")
        print(f"🚀 Auto Pipeline 시작")
        print(f"📂 프로젝트: {self.project_path.name}")
        print(f"📋 티켓: {ticket_num}")
        print('='*60)

        # 티켓 파일 확인
        ticket_file = self._find_ticket_file(ticket_num)

        if not ticket_file:
            raise FileNotFoundError(f"티켓 파일을 찾을 수 없습니다: {ticket_num}")

        # 티켓 내용 읽기
        ticket_content = ticket_file.read_text(encoding='utf-8')

        # Step 1: PM Agent
        print(f"\n{'='*60}")
        print("1️⃣ PM Agent 실행")
        print('='*60)

        pm_prompt = f"""다음 티켓의 명세서를 생성해주세요:

{ticket_content}

작업:
1. API 명세서 생성 (planning/specs/backend/)
2. UI 요구사항 생성 (planning/specs/frontend/)
3. 테스트 케이스 생성 (planning/test-cases/)
"""

        self.open_agent_in_new_tab("pm", ticket_num, pm_prompt)
        self.wait_for_user_confirmation("pm", ticket_num)

        # Step 2: Coding Agent
        print(f"\n{'='*60}")
        print("2️⃣ Coding Agent 실행")
        print('='*60)

        coding_prompt = f"""티켓 {ticket_num}을 구현해주세요.

작업:
1. PM Agent가 생성한 명세서 확인
2. 코드 구현 (src/ 디렉토리)
3. Git 브랜치 생성 및 커밋
"""

        self.open_agent_in_new_tab("coding", ticket_num, coding_prompt)
        self.wait_for_user_confirmation("coding", ticket_num)

        # Step 3: QA Agent
        print(f"\n{'='*60}")
        print("3️⃣ QA Agent 실행")
        print('='*60)

        qa_prompt = f"""티켓 {ticket_num}의 테스트를 작성해주세요.

작업:
1. PM Agent의 테스트 케이스 확인
2. Coding Agent가 구현한 코드 확인
3. 테스트 코드 작성 및 실행
"""

        self.open_agent_in_new_tab("qa", ticket_num, qa_prompt)
        self.wait_for_user_confirmation("qa", ticket_num)

        # 완료
        print(f"\n{'='*60}")
        print("🎉 전체 파이프라인 완료!")
        print(f"📋 티켓: {ticket_num}")
        print(f"\n세션 정보:")
        if ticket_num in self.session_map:
            for agent_name, session_info in self.session_map[ticket_num].items():
                print(f"  - {agent_name.upper()}: {session_info['session_id']}")
        print('='*60)

        print(f"\n💡 팁:")
        print(f"  - 각 에이전트 탭은 계속 열려있습니다.")
        print(f"  - 나중에 수정이 필요하면 해당 탭으로 돌아가서 대화 이어가기")
        print(f"  - 세션 맵: {self.session_map_file}")

    def _find_ticket_file(self, ticket_num: str) -> Optional[Path]:
        """티켓 파일 찾기"""
        tickets_dir = self.project_path / "planning" / "tickets"

        if not tickets_dir.exists():
            return None

        # {ACRONYM}-XXX-*.md 패턴 찾기
        for ticket_file in tickets_dir.glob(f"{ticket_num}-*.md"):
            return ticket_file

        return None

    def resume_agent_session(self, ticket_num: str, agent_name: str):
        """
        기존 에이전트 세션으로 복귀 (수정 작업)

        Args:
            ticket_num: 티켓 번호
            agent_name: 에이전트 이름
        """
        if ticket_num not in self.session_map:
            print(f"❌ 티켓 {ticket_num}의 세션을 찾을 수 없습니다.")
            return

        if agent_name not in self.session_map[ticket_num]:
            print(f"❌ {agent_name.upper()} Agent 세션을 찾을 수 없습니다.")
            return

        session_info = self.session_map[ticket_num][agent_name]

        print(f"\n{'='*60}")
        print(f"📍 세션 정보")
        print(f"  - Agent: {agent_name.upper()}")
        print(f"  - Ticket: {ticket_num}")
        print(f"  - Session ID: {session_info['session_id']}")
        print(f"  - Started: {session_info['started_at']}")
        print(f"  - Status: {session_info['status']}")
        print('='*60)

        print(f"\n💡 Terminal에서 해당 탭을 찾으세요:")
        print(f"   탭 타이틀: '{agent_name.upper()} - {ticket_num}'")
        print(f"\n   해당 탭으로 이동하면 Claude Code 세션이 유지되어 있습니다.")
        print(f"   대화를 이어가며 수정 작업을 진행하세요.")


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Auto Pipeline v2 - Claude Code 대화형 세션 기반"
    )

    parser.add_argument(
        "--project",
        help="프로젝트 경로 (생략 시 .project-config.json에서 읽기)"
    )

    parser.add_argument(
        "--ticket",
        required=True,
        help="티켓 번호 (예: BILL-001, TODO-002)"
    )

    parser.add_argument(
        "--resume",
        metavar="AGENT",
        help="기존 세션 복귀 (pm, coding, qa)"
    )

    args = parser.parse_args()

    # 프로젝트 경로 결정
    if args.project:
        project_path = Path(args.project)
    else:
        # .project-config.json에서 읽기
        config_file = Path(__file__).parent.parent / ".project-config.json"
        if not config_file.exists():
            print("❌ .project-config.json을 찾을 수 없습니다.")
            print("   --project 옵션으로 경로 지정 필요")
            return

        with open(config_file) as f:
            config = json.load(f)

        current_project = config["current_project"]
        project_path = Path(__file__).parent.parent / "projects" / current_project

    # Auto Pipeline 실행
    pipeline = AutoPipelineV2(str(project_path))

    if args.resume:
        # 기존 세션 복귀
        pipeline.resume_agent_session(args.ticket, args.resume)
    else:
        # 전체 파이프라인 실행
        pipeline.run_full_pipeline(args.ticket)


if __name__ == "__main__":
    main()
