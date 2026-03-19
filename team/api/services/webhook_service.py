"""Webhook Service - GitHub/Discord 이벤트 처리"""

from typing import Dict, Any
from api.services.skill_service import SkillService
from api.services.pipeline_service import PipelineService


class WebhookService:
    """Webhook 처리 서비스"""

    def __init__(self):
        self.skill_service = SkillService()
        self.pipeline_service = PipelineService()

    async def handle_pr_event(
        self,
        pr_number: int,
        action: str,
        repository: Dict[str, Any]
    ):
        """GitHub PR 이벤트 처리"""

        # PR이 open되거나 업데이트되면 review-pr skill 실행
        if action in ["opened", "synchronize"]:
            # 프로젝트 이름 추출
            project_name = repository.get("name", "unknown")

            try:
                result = self.skill_service.run_skill(
                    skill_name="review-pr",
                    ticket=None,
                    project=project_name,
                    args={"pr_number": pr_number},
                    auto_fix=True
                )

                print(f"✅ PR #{pr_number} 리뷰 완료: {result}")

            except Exception as e:
                print(f"❌ PR #{pr_number} 리뷰 실패: {e}")

    async def handle_issue_event(
        self,
        issue_number: int,
        issue: Dict[str, Any],
        repository: Dict[str, Any]
    ):
        """GitHub Issue 이벤트 처리"""

        # Issue가 생성되면 자동으로 티켓 생성
        issue_title = issue.get("title", "")
        issue_body = issue.get("body", "")

        # 티켓 번호 생성 (간단한 버전)
        ticket_num = f"PLAN-{issue_number:03d}"

        # 티켓 파일 생성 로직 (추후 구현)
        print(f"📋 티켓 생성: {ticket_num} - {issue_title}")

    async def handle_discord_command(
        self,
        command: str,
        args: list,
        user_id: str,
        channel_id: str
    ):
        """Discord 커맨드 처리"""

        if command == "run":
            # 파이프라인 실행
            ticket = args[0]
            project = args[1] if len(args) > 1 else "default"

            self.pipeline_service.run_pipeline(
                ticket=ticket,
                project=project,
                resume=False
            )

        elif command == "status":
            # 상태 조회
            ticket = args[0]
            status = self.pipeline_service.get_status(ticket)

            # Discord로 응답 전송 (추후 구현)
            print(f"📊 Status for {ticket}: {status}")
