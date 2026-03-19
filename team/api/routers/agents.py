"""Agent Router"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.models.request import AgentRunRequest
from api.models.response import AgentRunResponse
from api.services.agent_service import AgentService
from api.services.discord_service import DiscordService
import time

router = APIRouter()
agent_service = AgentService()
discord = DiscordService()


@router.post("/pm", response_model=AgentRunResponse)
async def run_pm_agent(request: AgentRunRequest, background_tasks: BackgroundTasks):
    """PM Agent 실행"""
    return await _run_agent("pm", request, background_tasks)


@router.post("/coding", response_model=AgentRunResponse)
async def run_coding_agent(request: AgentRunRequest, background_tasks: BackgroundTasks):
    """Coding Agent 실행"""
    return await _run_agent("coding", request, background_tasks)


@router.post("/qa", response_model=AgentRunResponse)
async def run_qa_agent(request: AgentRunRequest, background_tasks: BackgroundTasks):
    """QA Agent 실행"""
    return await _run_agent("qa", request, background_tasks)


@router.post("/project-planner", response_model=AgentRunResponse)
async def run_project_planner(request: AgentRunRequest, background_tasks: BackgroundTasks):
    """Project Planner Agent 실행"""
    return await _run_agent("project-planner", request, background_tasks)


@router.post("/stack-initializer", response_model=AgentRunResponse)
async def run_stack_initializer(request: AgentRunRequest, background_tasks: BackgroundTasks):
    """Stack Initializer Agent 실행"""
    return await _run_agent("stack-initializer", request, background_tasks)


async def _run_agent(agent_name: str, request: AgentRunRequest, background_tasks: BackgroundTasks) -> AgentRunResponse:
    """에이전트 실행 (공통 로직)"""

    # Discord 알림 (시작)
    await discord.send_notification(
        title=f"🤖 {agent_name.upper()} Agent Started",
        description=f"Ticket: {request.ticket}\nProject: {request.project}",
        color=3447003  # Blue
    )

    start_time = time.time()

    try:
        # 에이전트 실행
        result = agent_service.run_agent(
            agent_name=agent_name,
            ticket=request.ticket,
            project=request.project,
            prompt=request.prompt,
            auto_mode=request.auto_mode
        )

        duration = time.time() - start_time

        # Discord 알림 (성공)
        background_tasks.add_task(
            discord.send_notification,
            title=f"✅ {agent_name.upper()} Agent Completed",
            description=f"Ticket: {request.ticket}\nDuration: {duration:.1f}s",
            color=3066993  # Green
        )

        return AgentRunResponse(
            success=True,
            agent=agent_name,
            ticket=request.ticket,
            session_id=result.get("session_id", ""),
            message_count=result.get("message_count", 0),
            duration_seconds=duration,
            output=result.get("output", ""),
            error=None
        )

    except Exception as e:
        duration = time.time() - start_time

        # Discord 알림 (실패)
        background_tasks.add_task(
            discord.send_notification,
            title=f"❌ {agent_name.upper()} Agent Failed",
            description=f"Ticket: {request.ticket}\nError: {str(e)}",
            color=15158332  # Red
        )

        return AgentRunResponse(
            success=False,
            agent=agent_name,
            ticket=request.ticket,
            session_id="",
            message_count=0,
            duration_seconds=duration,
            output=None,
            error=str(e)
        )


@router.get("/list")
async def list_agents():
    """사용 가능한 에이전트 목록"""
    return {
        "agents": [
            {
                "name": "pm",
                "description": "제품 기획을 구조화된 산출물로 변환",
                "endpoint": "/api/agents/pm"
            },
            {
                "name": "coding",
                "description": "프로젝트 타입에 맞춰 코드 구현",
                "endpoint": "/api/agents/coding"
            },
            {
                "name": "qa",
                "description": "프로젝트 타입에 맞춰 테스트 작성",
                "endpoint": "/api/agents/qa"
            },
            {
                "name": "project-planner",
                "description": "프로젝트 전체 티켓 생성 및 분해",
                "endpoint": "/api/agents/project-planner"
            },
            {
                "name": "stack-initializer",
                "description": "프로젝트 타입별 초기 스택 구성",
                "endpoint": "/api/agents/stack-initializer"
            }
        ]
    }
