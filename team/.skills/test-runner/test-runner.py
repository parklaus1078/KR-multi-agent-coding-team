#!/usr/bin/env python3
"""
Test Runner Skill - 프로젝트 타입별 테스트 자동 실행
"""

import sys
import json
import subprocess
from pathlib import Path


def detect_test_framework(project_path: Path) -> str:
    """테스트 프레임워크 감지"""
    # Python
    if (project_path / "pytest.ini").exists() or (project_path / "pyproject.toml").exists():
        return "pytest"

    # Node.js
    package_json = project_path / "package.json"
    if package_json.exists():
        with open(package_json, 'r') as f:
            data = json.load(f)
            scripts = data.get("scripts", {})
            if "test" in scripts:
                test_cmd = scripts["test"]
                if "jest" in test_cmd:
                    return "jest"
                elif "vitest" in test_cmd:
                    return "vitest"
                elif "mocha" in test_cmd:
                    return "mocha"
                else:
                    return "npm"

    # Go
    if list(project_path.glob("*_test.go")):
        return "go"

    # Rust
    if (project_path / "Cargo.toml").exists():
        return "cargo"

    return "unknown"


def run_tests(project_path: Path, framework: str, verbose: bool = False):
    """테스트 실행"""
    print(f"🧪 테스트 프레임워크: {framework}")
    print(f"📂 프로젝트: {project_path}")
    print()

    commands = {
        "pytest": ["pytest", "-v" if verbose else "", "--cov=."],
        "jest": ["npm", "test", "--", "--coverage"],
        "vitest": ["npm", "run", "test"],
        "mocha": ["npm", "test"],
        "npm": ["npm", "test"],
        "go": ["go", "test", "./..."],
        "cargo": ["cargo", "test"]
    }

    cmd = commands.get(framework)
    if not cmd:
        print(f"❌ 지원하지 않는 프레임워크: {framework}")
        sys.exit(1)

    # 빈 문자열 제거
    cmd = [c for c in cmd if c]

    print(f"🚀 실행: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, cwd=project_path)
        if result.returncode == 0:
            print("\n✅ 모든 테스트 통과!")
            sys.exit(0)
        else:
            print("\n❌ 테스트 실패!")
            sys.exit(1)

    except FileNotFoundError:
        print(f"❌ {cmd[0]} 명령을 찾을 수 없습니다.")
        print(f"   설치 필요: {framework}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python test-runner.py <project_path> [--verbose]")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    verbose = "--verbose" in sys.argv

    if not project_path.exists():
        print(f"❌ 프로젝트를 찾을 수 없습니다: {project_path}")
        sys.exit(1)

    framework = detect_test_framework(project_path)

    if framework == "unknown":
        print("⚠️  테스트 프레임워크를 감지할 수 없습니다.")
        print("   지원: pytest, jest, vitest, mocha, go test, cargo test")
        sys.exit(1)

    run_tests(project_path, framework, verbose)


if __name__ == "__main__":
    main()
