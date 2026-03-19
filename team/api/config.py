"""API Configuration"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)


class Settings:
    """API 설정"""

    # API
    API_TITLE = "Multi-Agent Coding Team API"
    API_VERSION = "0.0.4"
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    # Discord
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

    # GitHub
    GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

    # Anthropic
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # Paths
    TEAM_ROOT = Path(__file__).parent.parent
    PROJECTS_DIR = TEAM_ROOT / "projects"
    LOGS_DIR = TEAM_ROOT / "logs"


settings = Settings()
