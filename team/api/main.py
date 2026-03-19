#!/usr/bin/env python3
"""
Multi-Agent Coding Team API
FastAPI 기반 REST API

Usage:
    uvicorn api.main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
import uvicorn

from api.routers import agents, skills, pipeline, webhooks, projects
from api.services.discord_service import DiscordService

# FastAPI 앱 생성
app = FastAPI(
    title="Multi-Agent Coding Team API",
    description="AI 에이전트 기반 자동화 개발 플랫폼",
    version="0.0.4",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(pipeline.router, prefix="/api/pipeline", tags=["Pipeline"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])

# 정적 파일 (웹 대시보드)
web_dir = Path(__file__).parent.parent / "web"
if web_dir.exists():
    app.mount("/static", StaticFiles(directory=str(web_dir / "static")), name="static")

# Discord 서비스 초기화
discord = DiscordService()


@app.on_event("startup")
async def startup_event():
    """앱 시작 시"""
    print("🚀 Multi-Agent Coding Team API 시작")

    # Discord 알림
    await discord.send_notification(
        title="🚀 API Server Started",
        description="Multi-Agent Coding Team API가 시작되었습니다.",
        color=3066993  # Green
    )


@app.on_event("shutdown")
async def shutdown_event():
    """앱 종료 시"""
    print("👋 Multi-Agent Coding Team API 종료")

    # Discord 알림
    await discord.send_notification(
        title="👋 API Server Stopped",
        description="Multi-Agent Coding Team API가 종료되었습니다.",
        color=15158332  # Red
    )


@app.get("/", response_class=HTMLResponse)
async def root():
    """웹 대시보드 메인 페이지"""
    html_file = web_dir / "index.html"

    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()

    # 대시보드 HTML이 없으면 간단한 안내 페이지
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi-Agent Coding Team</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 { color: #333; }
            .status { color: #22c55e; font-weight: bold; }
            .link {
                display: inline-block;
                margin: 10px 10px 10px 0;
                padding: 10px 20px;
                background: #3b82f6;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }
            .link:hover { background: #2563eb; }
            code {
                background: #f3f4f6;
                padding: 2px 6px;
                border-radius: 3px;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Multi-Agent Coding Team</h1>
            <p class="status">✅ API Server Running</p>

            <h2>📚 API Documentation</h2>
            <a href="/api/docs" class="link">Swagger UI</a>
            <a href="/api/redoc" class="link">ReDoc</a>

            <h2>🔗 Quick Start</h2>
            <h3>1. Run Pipeline</h3>
            <pre><code>curl -X POST http://localhost:8000/api/pipeline/run \\
  -H "Content-Type: application/json" \\
  -d '{"ticket": "PLAN-001", "project": "my-project"}'</code></pre>

            <h3>2. Check Status</h3>
            <pre><code>curl http://localhost:8000/api/pipeline/status/PLAN-001</code></pre>

            <h3>3. Run Agent</h3>
            <pre><code>curl -X POST http://localhost:8000/api/agents/pm \\
  -H "Content-Type: application/json" \\
  -d '{"ticket": "PLAN-001", "project": "my-project"}'</code></pre>

            <h2>🎯 Available Endpoints</h2>
            <ul>
                <li><code>POST /api/agents/{agent_name}</code> - Run agent</li>
                <li><code>POST /api/skills/{skill_name}</code> - Run skill</li>
                <li><code>POST /api/pipeline/run</code> - Run full pipeline</li>
                <li><code>GET /api/pipeline/status/{ticket}</code> - Get status</li>
                <li><code>POST /api/webhooks/github</code> - GitHub webhook</li>
                <li><code>POST /api/webhooks/discord</code> - Discord webhook</li>
            </ul>

            <h2>🔧 Configuration</h2>
            <p>Set environment variables:</p>
            <pre><code>DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
GITHUB_WEBHOOK_SECRET=your-secret
API_PORT=8000</code></pre>
        </div>
    </body>
    </html>
    """


@app.get("/api/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "service": "multi-agent-coding-team",
        "version": "0.0.4"
    }


@app.get("/api/info")
async def info():
    """API 정보"""
    return {
        "name": "Multi-Agent Coding Team API",
        "version": "0.0.4",
        "agents": ["pm", "coding", "qa", "project-planner", "stack-initializer"],
        "skills": [
            "validate-spec",
            "commit",
            "review-pr",
            "refactor-code",
            "test-runner",
            "deploy",
            "benchmark",
            "docs-generator"
        ],
        "integrations": ["discord", "github"],
        "docs": {
            "swagger": "/api/docs",
            "redoc": "/api/redoc"
        }
    }


if __name__ == "__main__":
    # 개발 모드 실행
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
