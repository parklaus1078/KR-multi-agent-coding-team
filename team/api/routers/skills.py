"""Skills Router"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.models.request import SkillRunRequest
from api.models.response import SkillRunResponse
from api.services.skill_service import SkillService
from api.services.discord_service import DiscordService
import time

router = APIRouter()
skill_service = SkillService()
discord = DiscordService()


@router.post("/validate-spec", response_model=SkillRunResponse)
async def run_validate_spec(request: SkillRunRequest, background_tasks: BackgroundTasks):
    """validate-spec skill 실행"""
    return await _run_skill("validate-spec", request, background_tasks)


@router.post("/commit", response_model=SkillRunResponse)
async def run_commit(request: SkillRunRequest, background_tasks: BackgroundTasks):
    """commit skill 실행"""
    return await _run_skill("commit", request, background_tasks)


@router.post("/review-pr", response_model=SkillRunResponse)
async def run_review_pr(request: SkillRunRequest, background_tasks: BackgroundTasks):
    """review-pr skill 실행"""
    return await _run_skill("review-pr", request, background_tasks)


@router.post("/refactor-code", response_model=SkillRunResponse)
async def run_refactor_code(request: SkillRunRequest, background_tasks: BackgroundTasks):
    """refactor-code skill 실행"""
    return await _run_skill("refactor-code", request, background_tasks)


@router.post("/test-runner", response_model=SkillRunResponse)
async def run_test_runner(request: SkillRunRequest, background_tasks: BackgroundTasks):
    """test-runner skill 실행"""
    return await _run_skill("test-runner", request, background_tasks)


@router.post("/deploy", response_model=SkillRunResponse)
async def run_deploy(request: SkillRunRequest, background_tasks: BackgroundTasks):
    """deploy skill 실행"""
    return await _run_skill("deploy", request, background_tasks)


@router.post("/benchmark", response_model=SkillRunResponse)
async def run_benchmark(request: SkillRunRequest, background_tasks: BackgroundTasks):
    """benchmark skill 실행"""
    return await _run_skill("benchmark", request, background_tasks)


@router.post("/docs-generator", response_model=SkillRunResponse)
async def run_docs_generator(request: SkillRunRequest, background_tasks: BackgroundTasks):
    """docs-generator skill 실행"""
    return await _run_skill("docs-generator", request, background_tasks)


async def _run_skill(skill_name: str, request: SkillRunRequest, background_tasks: BackgroundTasks) -> SkillRunResponse:
    """Skill 실행 (공통 로직)"""

    start_time = time.time()

    try:
        # Skill 실행
        result = skill_service.run_skill(
            skill_name=skill_name,
            ticket=request.ticket,
            project=request.project,
            args=request.args or {},
            auto_fix=request.auto_fix
        )

        duration = time.time() - start_time

        # 에러가 있으면 Discord 알림
        if not result.get("success", True):
            background_tasks.add_task(
                discord.send_notification,
                title=f"⚠️ {skill_name} Skill Issue",
                description=f"Ticket: {request.ticket}\n{result.get('message', 'Unknown issue')}",
                color=16776960  # Yellow
            )

        return SkillRunResponse(
            success=result.get("success", True),
            skill=skill_name,
            duration_seconds=duration,
            result=result,
            error=None
        )

    except Exception as e:
        duration = time.time() - start_time

        # Discord 알림 (실패)
        background_tasks.add_task(
            discord.send_notification,
            title=f"❌ {skill_name} Skill Failed",
            description=f"Ticket: {request.ticket}\nError: {str(e)}",
            color=15158332  # Red
        )

        return SkillRunResponse(
            success=False,
            skill=skill_name,
            duration_seconds=duration,
            result={},
            error=str(e)
        )


@router.get("/list")
async def list_skills():
    """사용 가능한 Skills 목록"""
    return {
        "skills": [
            {
                "name": "validate-spec",
                "category": "Code Quality",
                "description": "명세서 검증",
                "endpoint": "/api/skills/validate-spec"
            },
            {
                "name": "review-pr",
                "category": "Code Quality",
                "description": "PR 자동 리뷰",
                "endpoint": "/api/skills/review-pr"
            },
            {
                "name": "refactor-code",
                "category": "Code Quality",
                "description": "코드 리팩토링 제안",
                "endpoint": "/api/skills/refactor-code"
            },
            {
                "name": "commit",
                "category": "Development",
                "description": "커밋 메시지 자동 생성",
                "endpoint": "/api/skills/commit"
            },
            {
                "name": "test-runner",
                "category": "Development",
                "description": "테스트 자동 실행",
                "endpoint": "/api/skills/test-runner"
            },
            {
                "name": "docs-generator",
                "category": "Development",
                "description": "문서 자동 생성",
                "endpoint": "/api/skills/docs-generator"
            },
            {
                "name": "deploy",
                "category": "Operations",
                "description": "배포 자동화",
                "endpoint": "/api/skills/deploy"
            },
            {
                "name": "benchmark",
                "category": "Operations",
                "description": "성능 벤치마크",
                "endpoint": "/api/skills/benchmark"
            }
        ]
    }
