"""Pipeline Service - 파이프라인 실행 및 관리"""

import sys
from pathlib import Path

# auto_pipeline.py를 임포트하기 위한 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from auto_pipeline import AutoPipeline
from typing import Optional, List, Dict, Any
import json
from datetime import datetime


class PipelineService:
    """파이프라인 서비스"""

    def __init__(self):
        self.team_root = Path(__file__).parent.parent.parent
        self.pipelines: Dict[str, Dict[str, Any]] = {}  # In-memory storage

    def run_pipeline(
        self,
        ticket: str,
        project: str,
        resume: bool = False,
        skip_steps: Optional[List[str]] = None
    ):
        """파이프라인 실행 (백그라운드)"""

        project_path = self.team_root / "projects" / project

        if not project_path.exists():
            raise Exception(f"Project not found: {project}")

        # AutoPipeline 인스턴스 생성
        pipeline = AutoPipeline(str(project_path))

        # 상태 초기화
        self.pipelines[ticket] = {
            "ticket": ticket,
            "status": "running",
            "current_step": "pm",
            "progress": 0,
            "started_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "duration_seconds": None,
            "steps": [],
            "error": None
        }

        try:
            # 파이프라인 실행
            pipeline.run_full_pipeline(resume=resume)

            # 성공 상태 업데이트
            self.pipelines[ticket].update({
                "status": "success",
                "progress": 100,
                "completed_at": datetime.utcnow().isoformat()
            })

        except Exception as e:
            # 실패 상태 업데이트
            self.pipelines[ticket].update({
                "status": "failed",
                "completed_at": datetime.utcnow().isoformat(),
                "error": str(e)
            })

    def get_status(self, ticket: str) -> Optional[Dict[str, Any]]:
        """파이프라인 상태 조회"""
        return self.pipelines.get(ticket)

    def list_pipelines(
        self,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """파이프라인 목록 조회"""

        pipelines = list(self.pipelines.values())

        if status:
            pipelines = [p for p in pipelines if p["status"] == status]

        # 최신순 정렬
        pipelines.sort(key=lambda x: x["started_at"], reverse=True)

        return pipelines[:limit]

    def cancel_pipeline(self, ticket: str):
        """파이프라인 취소"""

        if ticket not in self.pipelines:
            raise Exception(f"Pipeline not found: {ticket}")

        self.pipelines[ticket].update({
            "status": "cancelled",
            "completed_at": datetime.utcnow().isoformat()
        })

    def delete_pipeline(self, ticket: str):
        """파이프라인 삭제"""

        if ticket not in self.pipelines:
            raise Exception(f"Pipeline not found: {ticket}")

        del self.pipelines[ticket]

    def get_logs(self, ticket: str, step: Optional[str] = None) -> List[str]:
        """파이프라인 로그 조회"""

        # 실제로는 파일 시스템에서 로그 읽기
        log_dir = self.team_root / "projects" / "logs"

        if not log_dir.exists():
            return []

        # 간단한 구현
        return ["Log line 1", "Log line 2"]

    def get_stats(self) -> Dict[str, Any]:
        """파이프라인 통계"""

        total = len(self.pipelines)
        by_status = {}

        for pipeline in self.pipelines.values():
            status = pipeline["status"]
            by_status[status] = by_status.get(status, 0) + 1

        return {
            "total": total,
            "by_status": by_status,
            "success_rate": by_status.get("success", 0) / total if total > 0 else 0
        }
