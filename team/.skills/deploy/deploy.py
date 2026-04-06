#!/usr/bin/env python3
"""
Deploy Skill - 배포 자동화 (간단한 스크립트)
"""

import sys
import subprocess
from pathlib import Path


def deploy(project_path: Path, env: str = "production"):
    """배포 실행"""
    print(f"🚀 배포 시작")
    print(f"   프로젝트: {project_path}")
    print(f"   환경: {env}")
    print()

    # deploy.sh 확인
    deploy_script = project_path / "deploy.sh"

    if deploy_script.exists():
        print("📜 deploy.sh 발견, 실행 중...")
        result = subprocess.run(["bash", str(deploy_script), env], cwd=project_path)
        if result.returncode == 0:
            print("\n✅ 배포 성공!")
            return True
        else:
            print("\n❌ 배포 실패!")
            return False

    # Docker Compose
    docker_compose = project_path / "docker-compose.yml"
    if docker_compose.exists():
        print("🐳 Docker Compose 발견, 실행 중...")
        result = subprocess.run(
            ["docker-compose", "up", "-d", "--build"],
            cwd=project_path
        )
        if result.returncode == 0:
            print("\n✅ Docker 배포 성공!")
            return True

    # Vercel
    vercel_json = project_path / "vercel.json"
    if vercel_json.exists():
        print("▲ Vercel 프로젝트 발견")
        print("   수동 배포: vercel --prod")
        return True

    # Heroku
    if (project_path / "Procfile").exists():
        print("🟣 Heroku 프로젝트 발견")
        print("   수동 배포: git push heroku main")
        return True

    print("⚠️  배포 스크립트를 찾을 수 없습니다.")
    print("   지원: deploy.sh, docker-compose.yml, vercel.json, Procfile")
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python deploy.py <project_path> [env]")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    env = sys.argv[2] if len(sys.argv) > 2 else "production"

    if not project_path.exists():
        print(f"❌ 프로젝트를 찾을 수 없습니다: {project_path}")
        sys.exit(1)

    if deploy(project_path, env):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
