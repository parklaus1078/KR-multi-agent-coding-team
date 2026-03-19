"""Pipeline Router"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.models.request import PipelineRunRequest
from api.models.response import PipelineStatusResponse, PipelineListResponse, StatusEnum
from api.services.pipeline_service import PipelineService
from api.services.discord_service import DiscordService
from typing import List

router = APIRouter()
pipeline_service = PipelineService()
discord = DiscordService()


@router.post("/run")
async def run_pipeline(request: PipelineRunRequest, background_tasks: BackgroundTasks):
    """파이프라인 실행"""

    # Discord 알림 (시작)
    await discord.send_notification(
        title="🚀 Pipeline Started",
        description=f"**Ticket**: {request.ticket}\n**Project**: {request.project}",
        color=3447003,  # Blue
        fields=[
            {"name": "Mode", "value": "Resume" if request.resume else "New", "inline": True},
            {"name": "Status", "value": "🟢 Running", "inline": True}
        ]
    )

    # 백그라운드에서 파이프라인 실행
    background_tasks.add_task(
        pipeline_service.run_pipeline,
        ticket=request.ticket,
        project=request.project,
        resume=request.resume,
        skip_steps=request.skip_steps
    )

    return {
        "message": "Pipeline started",
        "ticket": request.ticket,
        "status": "running",
        "check_status": f"/api/pipeline/status/{request.ticket}"
    }


@router.get("/status/{ticket}", response_model=PipelineStatusResponse)
async def get_pipeline_status(ticket: str):
    """파이프라인 상태 조회"""

    status = pipeline_service.get_status(ticket)

    if not status:
        raise HTTPException(status_code=404, detail=f"Pipeline not found: {ticket}")

    return status


@router.get("/list", response_model=PipelineListResponse)
async def list_pipelines(status: str = None, limit: int = 50):
    """파이프라인 목록 조회"""

    pipelines = pipeline_service.list_pipelines(status=status, limit=limit)

    return PipelineListResponse(
        total=len(pipelines),
        pipelines=pipelines
    )


@router.post("/cancel/{ticket}")
async def cancel_pipeline(ticket: str, background_tasks: BackgroundTasks):
    """파이프라인 취소"""

    try:
        pipeline_service.cancel_pipeline(ticket)

        # Discord 알림
        background_tasks.add_task(
            discord.send_notification,
            title="⏹️ Pipeline Cancelled",
            description=f"**Ticket**: {ticket}",
            color=16776960  # Yellow
        )

        return {
            "message": "Pipeline cancelled",
            "ticket": ticket
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{ticket}")
async def delete_pipeline(ticket: str):
    """파이프라인 삭제 (히스토리 제거)"""

    try:
        pipeline_service.delete_pipeline(ticket)

        return {
            "message": "Pipeline deleted",
            "ticket": ticket
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/logs/{ticket}")
async def get_pipeline_logs(ticket: str, step: str = None):
    """파이프라인 로그 조회"""

    try:
        logs = pipeline_service.get_logs(ticket, step=step)

        return {
            "ticket": ticket,
            "step": step,
            "logs": logs
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/stats")
async def get_pipeline_stats():
    """파이프라인 통계"""

    stats = pipeline_service.get_stats()

    return stats
