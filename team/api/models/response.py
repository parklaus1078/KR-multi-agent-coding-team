"""Response Models"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    """파이프라인 상태"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentRunResponse(BaseModel):
    """에이전트 실행 응답"""
    success: bool = Field(..., description="성공 여부")
    agent: str = Field(..., description="에이전트 이름")
    ticket: str = Field(..., description="티켓 번호")
    session_id: str = Field(..., description="세션 ID")
    message_count: int = Field(..., description="메시지 수")
    duration_seconds: float = Field(..., description="실행 시간 (초)")
    output: Optional[str] = Field(None, description="출력 메시지")
    error: Optional[str] = Field(None, description="에러 메시지")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "agent": "pm",
                "ticket": "PLAN-001",
                "session_id": "abc123",
                "message_count": 5,
                "duration_seconds": 45.2,
                "output": "명세서 생성 완료",
                "error": None
            }
        }


class SkillRunResponse(BaseModel):
    """Skill 실행 응답"""
    success: bool = Field(..., description="성공 여부")
    skill: str = Field(..., description="Skill 이름")
    duration_seconds: float = Field(..., description="실행 시간 (초)")
    result: Dict[str, Any] = Field(..., description="실행 결과")
    error: Optional[str] = Field(None, description="에러 메시지")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "skill": "validate-spec",
                "duration_seconds": 2.1,
                "result": {
                    "passed": True,
                    "errors": 0,
                    "warnings": 1
                },
                "error": None
            }
        }


class PipelineStatusResponse(BaseModel):
    """파이프라인 상태 응답"""
    ticket: str = Field(..., description="티켓 번호")
    status: StatusEnum = Field(..., description="상태")
    current_step: Optional[str] = Field(None, description="현재 단계")
    progress: int = Field(..., description="진행률 (0-100)")
    started_at: Optional[datetime] = Field(None, description="시작 시간")
    completed_at: Optional[datetime] = Field(None, description="완료 시간")
    duration_seconds: Optional[float] = Field(None, description="소요 시간")
    steps: List[Dict[str, Any]] = Field(..., description="단계 목록")
    error: Optional[str] = Field(None, description="에러 메시지")

    class Config:
        schema_extra = {
            "example": {
                "ticket": "PLAN-001",
                "status": "running",
                "current_step": "coding",
                "progress": 60,
                "started_at": "2026-03-19T10:00:00Z",
                "completed_at": None,
                "duration_seconds": None,
                "steps": [
                    {"name": "pm", "status": "success", "duration": 45.2},
                    {"name": "validate-spec", "status": "success", "duration": 2.1},
                    {"name": "coding", "status": "running", "duration": None}
                ],
                "error": None
            }
        }


class PipelineListResponse(BaseModel):
    """파이프라인 목록 응답"""
    total: int = Field(..., description="총 개수")
    pipelines: List[PipelineStatusResponse] = Field(..., description="파이프라인 목록")


class HealthCheckResponse(BaseModel):
    """헬스 체크 응답"""
    status: str = Field(..., description="상태")
    service: str = Field(..., description="서비스 이름")
    version: str = Field(..., description="버전")


class WebhookResponse(BaseModel):
    """Webhook 응답"""
    received: bool = Field(True, description="수신 완료")
    event: str = Field(..., description="이벤트 타입")
    action: str = Field(..., description="액션")
    queued: bool = Field(..., description="큐에 추가됨")
    message: str = Field(..., description="응답 메시지")
