#!/usr/bin/env python3
"""
Auto Responder - .config/auto-responses.json 기반 자동 응답

에이전트가 질문할 때 패턴 매칭하여 자동 응답합니다.
"""

import re
import json
from pathlib import Path
from typing import Optional, Dict, List


class AutoResponder:
    """자동 응답 시스템"""

    def __init__(self, workspace_root: Path):
        """
        Args:
            workspace_root: team/ 디렉토리 경로
        """
        self.workspace_root = Path(workspace_root)
        self.config_file = self.workspace_root / ".config" / "auto-responses.json"
        self.responses: Dict[str, List[Dict]] = {}
        self._load_config()

    def _load_config(self):
        """auto-responses.json 로드"""
        if not self.config_file.exists():
            print(f"⚠️  auto-responses.json을 찾을 수 없습니다: {self.config_file}")
            return

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 새로운 구조: {"pm": {"patterns": [...]}, "coding": {"patterns": [...]}}
            # 또는 옛날 구조: {"responses": {"pm": [...]}}
            if "responses" in data:
                self.responses = data["responses"]
            else:
                # patterns 배열 추출
                for agent_name, agent_data in data.items():
                    if isinstance(agent_data, dict) and "patterns" in agent_data:
                        self.responses[agent_name] = agent_data["patterns"]

            pattern_count = sum(len(v) if isinstance(v, list) else 0 for v in self.responses.values())
            print(f"✅ 자동 응답 설정 로드: {pattern_count}개 패턴")

        except json.JSONDecodeError as e:
            print(f"❌ auto-responses.json 파싱 실패: {e}")
        except Exception as e:
            print(f"❌ 설정 로드 실패: {e}")

    def find_response(self, question: str, agent_name: str) -> Optional[Dict]:
        """
        질문에 대한 자동 응답 찾기

        Args:
            question: 에이전트의 질문 텍스트
            agent_name: pm, coding, qa, project-planner

        Returns:
            매칭된 응답 딕셔너리 또는 None
        """
        # 공통 응답 먼저 확인 (global)
        global_patterns = self.responses.get("global", [])
        if isinstance(global_patterns, list):
            for pattern_obj in global_patterns:
                if self._match_pattern(question, pattern_obj):
                    return pattern_obj

        # 에이전트별 응답 확인
        agent_patterns = self.responses.get(agent_name, [])
        if isinstance(agent_patterns, list):
            for pattern_obj in agent_patterns:
                if self._match_pattern(question, pattern_obj):
                    return pattern_obj

        return None

    def _match_pattern(self, question: str, pattern_obj: Dict) -> bool:
        """
        질문이 패턴과 매칭되는지 확인

        Args:
            question: 질문 텍스트
            pattern_obj: 패턴 딕셔너리

        Returns:
            매칭 여부
        """
        # "trigger" 필드가 패턴
        pattern = pattern_obj.get("trigger", "")

        if not pattern:
            return False

        try:
            # case-insensitive 정규식 매칭
            return bool(re.search(pattern, question, re.IGNORECASE))
        except re.error:
            print(f"⚠️  잘못된 정규식 패턴: {pattern}")
            return False

    def get_response_text(self, pattern_obj: Dict) -> str:
        """
        응답 텍스트 생성

        Args:
            pattern_obj: 패턴 딕셔너리

        Returns:
            응답 텍스트
        """
        response = pattern_obj.get("response", "")
        reason = pattern_obj.get("reason", "")
        gotcha_ref = pattern_obj.get("gotcha_ref", "")

        parts = [response]

        if reason:
            parts.append(f"\n📝 이유: {reason}")

        if gotcha_ref:
            parts.append(f"\n⚠️  관련 Gotcha: {gotcha_ref}")

        return "".join(parts)

    def handle_question(self, question: str, agent_name: str) -> Optional[str]:
        """
        질문에 대한 자동 응답 처리

        Args:
            question: 에이전트의 질문
            agent_name: pm, coding, qa, project-planner

        Returns:
            응답 텍스트 또는 None (자동 응답 불가)
        """
        pattern_obj = self.find_response(question, agent_name)

        if pattern_obj:
            response_text = self.get_response_text(pattern_obj)

            pattern_id = pattern_obj.get('id', 'N/A')
            print(f"\n{'='*60}")
            print(f"🤖 자동 응답 (패턴: {pattern_id})")
            print(f"{'='*60}")
            print(response_text)
            print(f"{'='*60}\n")

            return response_text
        else:
            return None

    def interactive_mode(self, agent_name: str):
        """
        대화형 모드 (테스트용)

        Args:
            agent_name: pm, coding, qa, project-planner
        """
        print(f"\n{'='*60}")
        print(f"Auto Responder - {agent_name.upper()} Agent")
        print(f"{'='*60}\n")

        print("💬 질문을 입력하세요 (종료: exit)")
        print()

        while True:
            try:
                question = input(f"{agent_name}> ")

                if question.lower() in ["exit", "quit"]:
                    break

                response = self.handle_question(question, agent_name)

                if not response:
                    print("⚠️  매칭되는 자동 응답이 없습니다.\n")

            except KeyboardInterrupt:
                print("\n\n종료합니다.")
                break


# CLI 실행
if __name__ == "__main__":
    import sys

    # 현재 디렉토리 기준으로 team/ 찾기
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent

    responder = AutoResponder(workspace_root)

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python auto_responder.py <agent_name>               # 대화형 모드")
        print("  python auto_responder.py <agent_name> \"<question>\"  # 단일 질문")
        print()
        print("Example:")
        print("  python auto_responder.py pm")
        print('  python auto_responder.py pm "Should I use SQLite or PostgreSQL?"')
        sys.exit(1)

    agent_name = sys.argv[1]

    if len(sys.argv) >= 3:
        # 단일 질문 모드
        question = sys.argv[2]
        response = responder.handle_question(question, agent_name)

        if not response:
            print("⚠️  매칭되는 자동 응답이 없습니다.")
            sys.exit(1)
    else:
        # 대화형 모드
        responder.interactive_mode(agent_name)
