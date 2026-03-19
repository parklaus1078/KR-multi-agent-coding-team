"""Webhooks Router"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request, Header
from api.models.request import GitHubWebhookRequest, DiscordCommandRequest
from api.models.response import WebhookResponse
from api.services.webhook_service import WebhookService
from api.services.discord_service import DiscordService
import hmac
import hashlib
import os

router = APIRouter()
webhook_service = WebhookService()
discord = DiscordService()


@router.post("/github", response_model=WebhookResponse)
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):
    """GitHub Webhook 수신"""

    # Signature 검증
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    if secret:
        body = await request.body()
        signature = hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(f"sha256={signature}", x_hub_signature_256 or ""):
            raise HTTPException(status_code=401, detail="Invalid signature")

    # Payload 파싱
    payload = await request.json()

    # 이벤트 처리
    event_type = x_github_event
    action = payload.get("action", "")

    # PR 이벤트
    if event_type == "pull_request":
        pr = payload.get("pull_request", {})
        pr_number = pr.get("number")
        pr_title = pr.get("title")

        if action in ["opened", "synchronize"]:
            # review-pr skill 실행
            background_tasks.add_task(
                webhook_service.handle_pr_event,
                pr_number=pr_number,
                action=action,
                repository=payload.get("repository", {})
            )

            # Discord 알림
            await discord.send_notification(
                title=f"🔔 GitHub PR {action.capitalize()}",
                description=f"**PR #{pr_number}**: {pr_title}",
                color=5814783,  # Purple
                url=pr.get("html_url")
            )

            return WebhookResponse(
                received=True,
                event=event_type,
                action=action,
                queued=True,
                message=f"PR #{pr_number} review queued"
            )

    # Issue 이벤트
    elif event_type == "issues":
        issue = payload.get("issue", {})
        issue_number = issue.get("number")
        issue_title = issue.get("title")

        if action == "opened":
            # 티켓 자동 생성
            background_tasks.add_task(
                webhook_service.handle_issue_event,
                issue_number=issue_number,
                issue=issue,
                repository=payload.get("repository", {})
            )

            # Discord 알림
            await discord.send_notification(
                title=f"🔔 GitHub Issue Opened",
                description=f"**Issue #{issue_number}**: {issue_title}",
                color=5814783,  # Purple
                url=issue.get("html_url")
            )

            return WebhookResponse(
                received=True,
                event=event_type,
                action=action,
                queued=True,
                message=f"Issue #{issue_number} ticket creation queued"
            )

    # 기본 응답
    return WebhookResponse(
        received=True,
        event=event_type,
        action=action,
        queued=False,
        message="Event received but not processed"
    )


@router.post("/discord", response_model=WebhookResponse)
async def discord_webhook(request: DiscordCommandRequest, background_tasks: BackgroundTasks):
    """Discord 커맨드 수신"""

    command = request.command
    args = request.args or []

    # 커맨드 처리
    if command == "run":
        # 파이프라인 실행
        if not args:
            return WebhookResponse(
                received=True,
                event="discord",
                action=command,
                queued=False,
                message="Usage: /run <ticket>"
            )

        ticket = args[0]

        background_tasks.add_task(
            webhook_service.handle_discord_command,
            command=command,
            args=args,
            user_id=request.user_id,
            channel_id=request.channel_id
        )

        return WebhookResponse(
            received=True,
            event="discord",
            action=command,
            queued=True,
            message=f"Pipeline {ticket} started"
        )

    elif command == "status":
        # 상태 조회
        if not args:
            return WebhookResponse(
                received=True,
                event="discord",
                action=command,
                queued=False,
                message="Usage: /status <ticket>"
            )

        ticket = args[0]

        background_tasks.add_task(
            webhook_service.handle_discord_command,
            command=command,
            args=args,
            user_id=request.user_id,
            channel_id=request.channel_id
        )

        return WebhookResponse(
            received=True,
            event="discord",
            action=command,
            queued=True,
            message=f"Checking status for {ticket}"
        )

    elif command == "help":
        # 도움말
        help_text = """
**Available Commands**:
- `/run <ticket>` - Run pipeline
- `/status <ticket>` - Check status
- `/cancel <ticket>` - Cancel pipeline
- `/list` - List active pipelines
- `/help` - Show this help
"""
        background_tasks.add_task(
            discord.send_message,
            channel_id=request.channel_id,
            content=help_text
        )

        return WebhookResponse(
            received=True,
            event="discord",
            action=command,
            queued=False,
            message="Help sent"
        )

    else:
        return WebhookResponse(
            received=True,
            event="discord",
            action=command,
            queued=False,
            message=f"Unknown command: {command}"
        )
