#!/usr/bin/env python3
"""
Discord Webhook Logger
Orchestrator Agent의 실시간 로깅을 Discord로 전송

기능:
- 각 Agent 실행 시작/완료 알림
- 에러 발생 시 상세 정보 전송
- 최종 요약 전송
- 색상별 임베드 (성공=녹색, 경고=노랑, 에러=빨강)
"""

import os
import json
import time
import traceback
from typing import Optional, Dict, List
from datetime import datetime
import urllib.request
import urllib.error


class DiscordLogger:
    """Discord Webhook을 통한 로깅"""

    # Discord 임베드 색상
    COLOR_SUCCESS = 0x2ecc71  # 녹색
    COLOR_INFO = 0x3498db     # 파란색
    COLOR_WARNING = 0xf39c12  # 노란색
    COLOR_ERROR = 0xe74c3c    # 빨간색
    COLOR_PURPLE = 0x9b59b6   # 보라색

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Args:
            webhook_url: Discord Webhook URL (없으면 환경 변수에서 읽기)
        """
        self.webhook_url = webhook_url or os.getenv('DISCORD_WEBHOOK_URL')
        self.enabled = bool(self.webhook_url)

        if not self.enabled:
            print("ℹ️  Discord 로깅 비활성화 (DISCORD_WEBHOOK_URL 없음)")

    def _send(self, payload: Dict) -> bool:
        """
        Discord Webhook으로 메시지 전송

        Args:
            payload: Discord API 페이로드

        Returns:
            성공 여부
        """
        if not self.enabled:
            return False

        try:
            data = json.dumps(payload).encode('utf-8')

            # 디버깅: 페이로드 출력 (환경 변수로 제어)
            if os.getenv('DEBUG_DISCORD') == '1':
                print(f"📤 Discord 페이로드 ({len(data)} bytes):")
                print(json.dumps(payload, indent=2, ensure_ascii=False))

            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Orchestrator-Agent/1.0'
                }
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 204

        except urllib.error.HTTPError as e:
            print(f"⚠️  Discord 전송 실패 (HTTP {e.code}): {e.reason}")
            print(f"   Webhook URL: {self.webhook_url[:50]}...")
            # 403은 보통 권한 문제
            if e.code == 403:
                print("   💡 해결 방법:")
                print("      1. Discord 서버 설정에서 Webhook이 삭제되지 않았는지 확인")
                print("      2. Webhook URL을 다시 복사해서 설정 (공백/줄바꿈 없이)")
                print("      3. 새 Webhook을 만들어서 시도")
            try:
                error_body = e.read().decode('utf-8')
                print(f"   에러 상세: {error_body}")
            except:
                pass
            return False
        except Exception as e:
            print(f"⚠️  Discord 전송 실패: {e}")
            print(f"   Webhook URL: {self.webhook_url[:50]}...")
            return False

    def _create_embed(self, title: str, description: str, color: int,
                     fields: Optional[List[Dict]] = None,
                     footer: Optional[str] = None) -> Dict:
        """
        Discord 임베드 생성

        Args:
            title: 제목
            description: 설명
            color: 색상 (16진수)
            fields: 필드 목록
            footer: 푸터 텍스트

        Returns:
            임베드 딕셔너리
        """
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }

        if fields:
            embed["fields"] = fields

        if footer:
            embed["footer"] = {"text": footer}

        return embed

    def pipeline_started(self, project: str, auto_improve: bool):
        """파이프라인 시작 알림"""
        if not self.enabled:
            return

        embed = self._create_embed(
            title="🚀 파이프라인 시작",
            description=f"프로젝트 **{project}** 의 전체 파이프라인이 시작되었습니다.",
            color=self.COLOR_INFO,
            fields=[
                {
                    "name": "자동 품질 개선",
                    "value": "✅ 활성화" if auto_improve else "❌ 비활성화",
                    "inline": True
                },
                {
                    "name": "예상 소요 시간",
                    "value": "25-40분" if auto_improve else "10-15분",
                    "inline": True
                }
            ],
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def phase_started(self, phase_num: int, phase_name: str, description: str):
        """Phase 시작 알림"""
        if not self.enabled:
            return

        embed = self._create_embed(
            title=f"📋 Phase {phase_num}: {phase_name}",
            description=description,
            color=self.COLOR_PURPLE,
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def agent_started(self, agent_name: str, ticket: Optional[str] = None):
        """Agent 실행 시작 알림"""
        if not self.enabled:
            return

        description = f"**{agent_name}** Agent 실행 중..."
        if ticket:
            description += f"\n티켓: `{ticket}`"

        embed = self._create_embed(
            title=f"🔄 {agent_name} 실행 중",
            description=description,
            color=self.COLOR_INFO,
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def agent_completed(self, agent_name: str, ticket: Optional[str] = None,
                       duration: Optional[float] = None,
                       details: Optional[str] = None):
        """Agent 실행 완료 알림"""
        if not self.enabled:
            return

        description = f"**{agent_name}** Agent 완료!"
        if ticket:
            description += f"\n티켓: `{ticket}`"

        fields = []
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            fields.append({
                "name": "소요 시간",
                "value": f"{minutes}분 {seconds}초",
                "inline": True
            })

        if details:
            fields.append({
                "name": "상세 정보",
                "value": details,
                "inline": False
            })

        embed = self._create_embed(
            title=f"✅ {agent_name} 완료",
            description=description,
            color=self.COLOR_SUCCESS,
            fields=fields if fields else None,
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def agent_failed(self, agent_name: str, ticket: Optional[str] = None,
                    error: Optional[str] = None, stderr: Optional[str] = None):
        """Agent 실행 실패 알림"""
        if not self.enabled:
            return

        description = f"**{agent_name}** Agent 실패!"
        if ticket:
            description += f"\n티켓: `{ticket}`"

        fields = []

        if error:
            # 에러 메시지 길이 제한 (1024자)
            error_text = error[:1000] + "..." if len(error) > 1000 else error
            fields.append({
                "name": "에러 메시지",
                "value": f"```\n{error_text}\n```",
                "inline": False
            })

        if stderr:
            # stderr 길이 제한
            stderr_text = stderr[:1000] + "..." if len(stderr) > 1000 else stderr
            fields.append({
                "name": "Stderr 출력",
                "value": f"```\n{stderr_text}\n```",
                "inline": False
            })

        embed = self._create_embed(
            title=f"❌ {agent_name} 실패",
            description=description,
            color=self.COLOR_ERROR,
            fields=fields if fields else None,
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def ticket_completed(self, ticket: str, score: int, iterations: int):
        """티켓 완료 알림"""
        if not self.enabled:
            return

        # 점수에 따른 이모지
        if score >= 90:
            emoji = "✅"
            color = self.COLOR_SUCCESS
            status = "우수"
        elif score >= 70:
            emoji = "⚠️"
            color = self.COLOR_WARNING
            status = "보통"
        else:
            emoji = "❌"
            color = self.COLOR_ERROR
            status = "미흡"

        embed = self._create_embed(
            title=f"{emoji} {ticket} 완료",
            description=f"티켓 **{ticket}** 처리가 완료되었습니다.",
            color=color,
            fields=[
                {
                    "name": "최종 점수",
                    "value": f"{score}/100 ({status})",
                    "inline": True
                },
                {
                    "name": "반복 횟수",
                    "value": f"{iterations}회",
                    "inline": True
                }
            ],
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def ticket_failed(self, ticket: str, reason: str):
        """티켓 실패 알림"""
        if not self.enabled:
            return

        embed = self._create_embed(
            title=f"❌ {ticket} 실패",
            description=f"티켓 **{ticket}** 처리가 실패했습니다.",
            color=self.COLOR_ERROR,
            fields=[
                {
                    "name": "실패 이유",
                    "value": reason,
                    "inline": False
                }
            ],
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def auto_improve_progress(self, ticket: str, iteration: int,
                              current_score: int, target_score: int):
        """자동 개선 진행 상황"""
        if not self.enabled:
            return

        # 진행률 계산
        progress = min(int((current_score / target_score) * 100), 100)
        bar_length = 10
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        embed = self._create_embed(
            title=f"🔄 {ticket} 자동 개선 중",
            description=f"반복 **{iteration}회** - 점수: **{current_score}/100**",
            color=self.COLOR_INFO,
            fields=[
                {
                    "name": "진행률",
                    "value": f"{bar} {progress}%",
                    "inline": False
                },
                {
                    "name": "현재 점수",
                    "value": f"{current_score}/100",
                    "inline": True
                },
                {
                    "name": "목표 점수",
                    "value": f"{target_score}/100",
                    "inline": True
                }
            ],
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def pipeline_completed(self, project: str, total_tickets: int,
                          completed: int, failed: int,
                          duration: float, ticket_scores: Dict[str, int]):
        """파이프라인 완료 알림"""
        if not self.enabled:
            return

        # 소요 시간 포맷
        minutes = int(duration // 60)
        seconds = int(duration % 60)

        # 티켓별 점수 필드
        score_fields = []
        for ticket, score in ticket_scores.items():
            if score >= 90:
                emoji = "✅"
            elif score >= 70:
                emoji = "⚠️"
            else:
                emoji = "❌"

            score_fields.append({
                "name": ticket,
                "value": f"{emoji} {score}/100",
                "inline": True
            })

        # 성공/실패 판단
        if failed == 0:
            title = "🎉 파이프라인 완료!"
            color = self.COLOR_SUCCESS
        else:
            title = "⚠️ 파이프라인 완료 (일부 실패)"
            color = self.COLOR_WARNING

        embed = self._create_embed(
            title=title,
            description=f"프로젝트 **{project}** 의 전체 파이프라인이 완료되었습니다.",
            color=color,
            fields=[
                {
                    "name": "총 티켓",
                    "value": f"{total_tickets}개",
                    "inline": True
                },
                {
                    "name": "완료",
                    "value": f"✅ {completed}개",
                    "inline": True
                },
                {
                    "name": "실패",
                    "value": f"❌ {failed}개",
                    "inline": True
                },
                {
                    "name": "소요 시간",
                    "value": f"{minutes}분 {seconds}초",
                    "inline": True
                },
                {"name": "\u200b", "value": "\u200b", "inline": False},  # 빈 줄
                *score_fields
            ],
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def pipeline_failed(self, project: str, phase: str, reason: str):
        """파이프라인 실패 알림"""
        if not self.enabled:
            return

        embed = self._create_embed(
            title="🛑 파이프라인 중단",
            description=f"프로젝트 **{project}** 의 파이프라인이 중단되었습니다.",
            color=self.COLOR_ERROR,
            fields=[
                {
                    "name": "중단 단계",
                    "value": phase,
                    "inline": True
                },
                {
                    "name": "이유",
                    "value": reason,
                    "inline": False
                }
            ],
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})

    def send_custom(self, title: str, message: str, color: str = "info"):
        """커스텀 메시지 전송"""
        if not self.enabled:
            return

        color_map = {
            "success": self.COLOR_SUCCESS,
            "info": self.COLOR_INFO,
            "warning": self.COLOR_WARNING,
            "error": self.COLOR_ERROR,
            "purple": self.COLOR_PURPLE
        }

        embed = self._create_embed(
            title=title,
            description=message,
            color=color_map.get(color, self.COLOR_INFO),
            footer="Orchestrator Agent"
        )

        self._send({"embeds": [embed]})


# 테스트 코드
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python discord_logger.py <webhook_url>")
        sys.exit(1)

    webhook_url = sys.argv[1]
    logger = DiscordLogger(webhook_url)

    print("Discord 로거 테스트 중...")

    # 1. 파이프라인 시작
    logger.pipeline_started("test-project", auto_improve=True)
    time.sleep(1)

    # 2. Phase 시작
    logger.phase_started(1, "Project Planner", "티켓 생성 중...")
    time.sleep(1)

    # 3. Agent 시작
    logger.agent_started("Project Planner")
    time.sleep(2)

    # 4. Agent 완료
    logger.agent_completed("Project Planner", duration=120, details="3개 티켓 생성")
    time.sleep(1)

    # 5. 티켓 완료
    logger.ticket_completed("PLAN-001", score=92, iterations=3)
    time.sleep(1)

    # 6. 자동 개선 진행
    logger.auto_improve_progress("PLAN-002", iteration=2, current_score=75, target_score=90)
    time.sleep(1)

    # 7. 파이프라인 완료
    logger.pipeline_completed(
        "test-project",
        total_tickets=3,
        completed=3,
        failed=0,
        duration=1500,
        ticket_scores={"PLAN-001": 92, "PLAN-002": 88, "PLAN-003": 94}
    )

    print("✅ 테스트 완료! Discord 채널을 확인하세요.")
