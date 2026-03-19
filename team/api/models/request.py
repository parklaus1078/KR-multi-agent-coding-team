"""Request Models"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class AgentRunRequest(BaseModel):
    """에이전트 실행 요청"""
    ticket: str = Field(..., description="티켓 번호 (예: PLAN-001)")
    project: str = Field(..., description="프로젝트 이름")
    prompt: Optional[str] = Field(None, description="추가 프롬프트")
    auto_mode: bool = Field(True, description="자동 모드 (질문 안 함)")

    class Config:
        schema_extra = {
            "example": {
                "ticket": "PLAN-001",
                "project": "my-cli-tool",
                "prompt": None,
                "auto_mode": True
            }
        }


class SkillRunRequest(BaseModel):
    """Skill 실행 요청"""
    ticket: Optional[str] = Field(None, description="티켓 번호")
    project: str = Field(..., description="프로젝트 이름")
    args: Optional[Dict[str, Any]] = Field(None, description="추가 인자")
    auto_fix: bool = Field(False, description="자동 수정 적용")

    class Config:
        schema_extra = {
            "example": {
                "ticket": "PLAN-001",
                "project": "my-cli-tool",
                "args": {},
                "auto_fix": False
            }
        }


class PipelineRunRequest(BaseModel):
    """파이프라인 실행 요청"""
    ticket: str = Field(..., description="티켓 번호")
    project: str = Field(..., description="프로젝트 이름")
    resume: bool = Field(False, description="중단된 파이프라인 재개")
    skip_steps: Optional[list[str]] = Field(None, description="건너뛸 단계")

    class Config:
        schema_extra = {
            "example": {
                "ticket": "PLAN-001",
                "project": "my-cli-tool",
                "resume": False,
                "skip_steps": None
            }
        }


class GitHubWebhookRequest(BaseModel):
    """GitHub Webhook 요청"""
    action: str = Field(..., description="이벤트 액션")
    pull_request: Optional[Dict[str, Any]] = Field(None, description="PR 정보")
    issue: Optional[Dict[str, Any]] = Field(None, description="이슈 정보")
    repository: Dict[str, Any] = Field(..., description="저장소 정보")
    sender: Dict[str, Any] = Field(..., description="발신자 정보")


class DiscordCommandRequest(BaseModel):
    """Discord 커맨드 요청"""
    command: str = Field(..., description="커맨드 이름")
    args: Optional[list[str]] = Field(None, description="커맨드 인자")
    user_id: str = Field(..., description="Discord 유저 ID")
    channel_id: str = Field(..., description="Discord 채널 ID")

    class Config:
        schema_extra = {
            "example": {
                "command": "run",
                "args": ["PLAN-001"],
                "user_id": "123456789",
                "channel_id": "987654321"
            }
        }
