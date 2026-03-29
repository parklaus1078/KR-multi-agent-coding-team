"""
설정 관리 명령어
"""

import json
from pathlib import Path

def get_workspace_root():
    """작업 디렉토리 루트 경로"""
    return Path(__file__).parent.parent

def manage_config(set_kv: list = None, get_key: str = None, list_all: bool = False):
    """설정 관리"""
    workspace = get_workspace_root()
    config_file = workspace / ".project-config.json"

    # 설정 조회
    if list_all or get_key:
        if not config_file.exists():
            print("❌ 설정 파일이 없습니다.")
            return

        with open(config_file, 'r') as f:
            config = json.load(f)

        if list_all:
            print("\n⚙️  현재 설정:\n")
            print(json.dumps(config, indent=2, ensure_ascii=False))
            print()
        elif get_key:
            value = config.get(get_key)
            if value is not None:
                print(f"{get_key} = {value}")
            else:
                print(f"❌ 설정을 찾을 수 없습니다: {get_key}")
        return

    # 설정 변경
    if set_kv:
        key, value = set_kv

        if not config_file.exists():
            config = {}
        else:
            with open(config_file, 'r') as f:
                config = json.load(f)

        # 타입 추론
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.isdigit():
            value = int(value)
        elif value.replace(".", "", 1).isdigit():
            value = float(value)

        config[key] = value

        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"✅ 설정 변경: {key} = {value}")
        return

    # 인자가 없으면 도움말
    print("사용법:")
    print("  mact config --list              # 전체 설정 조회")
    print("  mact config --get KEY           # 특정 설정 조회")
    print("  mact config --set KEY VALUE     # 설정 변경")
    print()
    print("예시:")
    print("  mact config --list")
    print("  mact config --get current_project")
    print("  mact config --set discord_webhook https://discord.com/...")
