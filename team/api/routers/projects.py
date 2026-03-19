"""Projects Router - 프로젝트 및 티켓 관리"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import List, Dict, Any
import json
from api.config import settings

router = APIRouter()


@router.get("/list")
async def list_projects():
    """프로젝트 목록 조회"""

    projects_dir = settings.TEAM_ROOT / "projects"

    if not projects_dir.exists():
        return {"projects": []}

    projects = []
    for project_dir in projects_dir.iterdir():
        if project_dir.is_dir() and not project_dir.name.startswith('.'):
            # .project-meta.json 읽기
            meta_file = project_dir / ".project-meta.json"
            if meta_file.exists():
                try:
                    with open(meta_file, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                        projects.append({
                            "name": project_dir.name,
                            "path": str(project_dir.relative_to(settings.TEAM_ROOT)),
                            "type": meta.get("project_type", "unknown"),
                            "language": meta.get("language", "unknown"),
                            "framework": meta.get("framework", "unknown"),
                            "description": meta.get("description", "")
                        })
                except Exception as e:
                    # meta 파일 없으면 기본 정보만
                    projects.append({
                        "name": project_dir.name,
                        "path": str(project_dir.relative_to(settings.TEAM_ROOT)),
                        "type": "unknown",
                        "language": "unknown",
                        "framework": "unknown",
                        "description": ""
                    })

    return {
        "total": len(projects),
        "projects": projects
    }


@router.get("/current")
async def get_current_project():
    """현재 활성 프로젝트 조회"""

    config_file = settings.TEAM_ROOT / ".project-config.json"

    if not config_file.exists():
        raise HTTPException(status_code=404, detail="No active project")

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return {
                "current_project": config.get("current_project"),
                "current_project_path": config.get("current_project_path"),
                "recent_projects": config.get("recent_projects", [])
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/switch/{project_name}")
async def switch_project(project_name: str):
    """프로젝트 전환"""

    projects_dir = settings.TEAM_ROOT / "projects"
    project_dir = projects_dir / project_name

    if not project_dir.exists():
        raise HTTPException(status_code=404, detail=f"Project not found: {project_name}")

    config_file = settings.TEAM_ROOT / ".project-config.json"

    # 기존 설정 읽기
    config = {}
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            pass

    # 설정 업데이트
    recent = config.get("recent_projects", [])
    if project_name in recent:
        recent.remove(project_name)
    recent.insert(0, project_name)
    recent = recent[:5]  # 최근 5개만 유지

    config.update({
        "current_project": project_name,
        "current_project_path": f"projects/{project_name}",
        "recent_projects": recent
    })

    # 저장
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    return {
        "message": f"Switched to project: {project_name}",
        "current_project": project_name
    }


@router.get("/{project_name}/tickets")
async def list_tickets(project_name: str):
    """프로젝트의 티켓 목록 조회"""

    projects_dir = settings.TEAM_ROOT / "projects"
    tickets_dir = projects_dir / project_name / "planning" / "tickets"

    if not tickets_dir.exists():
        return {
            "project": project_name,
            "total": 0,
            "tickets": []
        }

    tickets = []
    for ticket_file in sorted(tickets_dir.glob("PLAN-*.md")):
        # 파일 읽어서 제목 추출
        try:
            with open(ticket_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                title = ""
                for line in lines:
                    if line.startswith("# "):
                        title = line.strip("# \n")
                        break

                tickets.append({
                    "ticket": ticket_file.stem,  # PLAN-001-feature-name
                    "filename": ticket_file.name,
                    "title": title,
                    "path": str(ticket_file.relative_to(settings.TEAM_ROOT))
                })
        except Exception as e:
            # 읽기 실패해도 파일명만 추가
            tickets.append({
                "ticket": ticket_file.stem,
                "filename": ticket_file.name,
                "title": "",
                "path": str(ticket_file.relative_to(settings.TEAM_ROOT))
            })

    return {
        "project": project_name,
        "total": len(tickets),
        "tickets": tickets
    }


@router.get("/{project_name}/tickets/{ticket_id}")
async def get_ticket(project_name: str, ticket_id: str):
    """티켓 상세 조회"""

    projects_dir = settings.TEAM_ROOT / "projects"
    tickets_dir = projects_dir / project_name / "planning" / "tickets"

    # ticket_id가 PLAN-001 형태면 파일 찾기
    ticket_files = list(tickets_dir.glob(f"{ticket_id}*.md"))

    if not ticket_files:
        raise HTTPException(status_code=404, detail=f"Ticket not found: {ticket_id}")

    ticket_file = ticket_files[0]

    try:
        with open(ticket_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "ticket": ticket_id,
            "filename": ticket_file.name,
            "project": project_name,
            "content": content,
            "path": str(ticket_file.relative_to(settings.TEAM_ROOT))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_name}/status")
async def get_project_status(project_name: str):
    """프로젝트 상태 조회 (티켓 수, 완료율 등)"""

    projects_dir = settings.TEAM_ROOT / "projects"
    project_dir = projects_dir / project_name

    if not project_dir.exists():
        raise HTTPException(status_code=404, detail=f"Project not found: {project_name}")

    # 티켓 수 계산
    tickets_dir = project_dir / "planning" / "tickets"
    total_tickets = len(list(tickets_dir.glob("PLAN-*.md"))) if tickets_dir.exists() else 0

    # 명세서 수 계산
    specs_dir = project_dir / "planning" / "specs"
    total_specs = len(list(specs_dir.glob("*.md"))) if specs_dir.exists() else 0

    # 테스트 케이스 수 계산
    test_cases_dir = project_dir / "planning" / "test-cases"
    total_test_cases = len(list(test_cases_dir.glob("*.md"))) if test_cases_dir.exists() else 0

    return {
        "project": project_name,
        "tickets": {
            "total": total_tickets
        },
        "specs": {
            "total": total_specs,
            "completion_rate": round(total_specs / total_tickets * 100, 1) if total_tickets > 0 else 0
        },
        "test_cases": {
            "total": total_test_cases,
            "completion_rate": round(total_test_cases / total_tickets * 100, 1) if total_tickets > 0 else 0
        }
    }
