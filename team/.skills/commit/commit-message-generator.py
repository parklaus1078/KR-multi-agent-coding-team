#!/usr/bin/env python3
"""
Commit Message Generator - 시맨틱 커밋 메시지 자동 생성

Usage:
    python3 commit-message-generator.py --ticket PLAN-001
    python3 commit-message-generator.py --ticket PLAN-001 --dry-run
    python3 commit-message-generator.py --ticket PLAN-001 --generate-only
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class CommitMessageGenerator:
    """커밋 메시지 자동 생성기"""

    def __init__(self, project_path: Path, workspace_root: Path):
        self.project_path = project_path
        self.workspace_root = workspace_root
        self.memory_dir = workspace_root / ".memory"

        # 커밋 히스토리 로드
        self.commit_history = self._load_commit_history()

    def _load_commit_history(self) -> dict:
        """커밋 히스토리 로드"""
        history_file = self.memory_dir / "commit-history.json"

        if not history_file.exists():
            return {
                "project": self.project_path.name,
                "vocabulary": {},
                "frequent_verbs": {
                    "feat": ["implement", "add", "create"],
                    "fix": ["fix", "resolve", "correct"],
                    "test": ["add tests for", "test"],
                    "refactor": ["refactor", "improve", "optimize"],
                    "docs": ["update", "add", "improve"],
                    "chore": ["update", "configure"]
                },
                "recent_commits": []
            }

        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate(self, ticket_num: str) -> Dict:
        """커밋 메시지 생성"""
        print(f"\n{'='*60}")
        print(f"커밋 메시지 생성: {ticket_num}")
        print(f"{'='*60}\n")

        # 1. Git diff 분석
        changed_files = self._get_changed_files()

        if not changed_files:
            print("❌ 변경 사항이 없습니다.")
            return {"success": False, "error": "no_changes"}

        print(f"1️⃣  변경 파일: {len(changed_files)}개")
        for file, status in changed_files:
            print(f"   {status} {file}")
        print()

        # 2. 커밋 타입 결정
        commit_type = self._determine_type(changed_files)
        print(f"2️⃣  커밋 타입: {commit_type}\n")

        # 3. Scope 추출
        scope = ticket_num

        # 4. Subject 생성
        subject = self._generate_subject(commit_type, changed_files, ticket_num)
        print(f"3️⃣  Subject: {subject}\n")

        # 5. Body 생성 (선택)
        body = self._generate_body(commit_type, changed_files)

        # 6. Footer 생성
        footer = self._generate_footer(ticket_num)

        # 7. 최종 메시지 조립
        message = self._assemble_message(commit_type, scope, subject, body, footer)

        print(f"4️⃣  최종 커밋 메시지:")
        print(f"{'─'*60}")
        print(message)
        print(f"{'─'*60}\n")

        return {
            "success": True,
            "message": message,
            "commit_type": commit_type,
            "scope": scope,
            "subject": subject,
            "changed_files": [f for f, _ in changed_files]
        }

    def _get_changed_files(self) -> List[Tuple[str, str]]:
        """변경된 파일 목록 가져오기"""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-status"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return []

            files = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    status, filename = parts
                    files.append((filename, status))

            return files

        except:
            return []

    def _determine_type(self, changed_files: List[Tuple[str, str]]) -> str:
        """커밋 타입 결정"""
        files = [f for f, _ in changed_files]

        # Test 파일
        if any("test" in f.lower() or "spec" in f.lower() for f in files):
            return "test"

        # 문서만
        if all(f.endswith(".md") for f in files):
            return "docs"

        # 설정 파일
        config_files = ["package.json", ".gitignore", "tsconfig.json", "webpack.config.js",
                       "requirements.txt", "setup.py", ".eslintrc", "pyproject.toml"]
        if any(f in config_files or f.startswith(".") for f in files):
            return "chore"

        # 추가/수정 비율로 판단
        added_count = sum(1 for _, status in changed_files if status == "A")
        modified_count = sum(1 for _, status in changed_files if status == "M")

        if added_count > modified_count:
            return "feat"
        else:
            # 기본값: fix
            return "fix"

    def _generate_subject(self, commit_type: str, changed_files: List[Tuple[str, str]], ticket_num: str) -> str:
        """Subject 생성"""
        # 티켓 설명 읽기 (선택)
        ticket_description = self._read_ticket_description(ticket_num)

        # 동사 선택
        verbs = self.commit_history["frequent_verbs"].get(commit_type, ["update"])
        verb = verbs[0]

        # 파일 경로에서 키워드 추출
        files = [f for f, _ in changed_files]
        keywords = self._extract_keywords_from_files(files)

        # 티켓 설명에서 키워드 보완
        if ticket_description:
            ticket_keywords = self._extract_keywords_from_text(ticket_description)
            keywords = ticket_keywords if ticket_keywords else keywords

        # Subject 조립
        if keywords:
            subject = f"{verb} {keywords}"
        else:
            subject = f"{verb} changes for {ticket_num}"

        # 70자 제한
        if len(subject) > 70:
            subject = subject[:67] + "..."

        return subject

    def _read_ticket_description(self, ticket_num: str) -> str:
        """티켓 설명 읽기"""
        try:
            # 티켓 파일 찾기
            tickets_dir = self.project_path / "planning" / "tickets"
            ticket_files = list(tickets_dir.glob(f"{ticket_num}*.md"))

            if not ticket_files:
                return ""

            content = ticket_files[0].read_text(encoding='utf-8')

            # 제목 추출 (첫 번째 # 헤더)
            match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if match:
                return match.group(1)

            return ""

        except:
            return ""

    def _extract_keywords_from_files(self, files: List[str]) -> str:
        """파일 경로에서 키워드 추출"""
        # 디렉토리 이름 추출
        dirs = set()
        for file in files:
            parts = Path(file).parts
            if len(parts) > 1:
                # src/auth/login.js → auth
                dirs.add(parts[1])

        if dirs:
            return ", ".join(sorted(dirs))

        # 파일명에서 추출
        filenames = [Path(f).stem for f in files]
        return ", ".join(filenames[:3])

    def _extract_keywords_from_text(self, text: str) -> str:
        """텍스트에서 키워드 추출 (간단한 규칙)"""
        # 소문자 변환
        text_lower = text.lower()

        # 불용어 제거
        stopwords = ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"]
        words = text_lower.split()
        keywords = [w for w in words if w not in stopwords and len(w) > 3]

        # 처음 3개 단어
        return " ".join(keywords[:3]) if keywords else ""

    def _generate_body(self, commit_type: str, changed_files: List[Tuple[str, str]]) -> str:
        """Body 생성 (선택)"""
        # 조건: 파일 3개 이상 또는 타입이 refactor/feat
        if len(changed_files) < 3 and commit_type not in ["refactor", "feat"]:
            return ""

        body_lines = []

        if commit_type == "feat":
            body_lines.append("Added new functionality:")
        elif commit_type == "fix":
            body_lines.append("Fixed issue:")
        elif commit_type == "refactor":
            body_lines.append("Refactored code:")
        elif commit_type == "test":
            body_lines.append("Added tests:")

        # 파일 목록 (최대 5개)
        files = [f for f, _ in changed_files[:5]]
        for file in files:
            body_lines.append(f"- {file}")

        if len(changed_files) > 5:
            body_lines.append(f"... and {len(changed_files) - 5} more files")

        return "\n".join(body_lines)

    def _generate_footer(self, ticket_num: str) -> str:
        """Footer 생성"""
        footer_lines = []

        # Closes
        footer_lines.append(f"Closes #{ticket_num}")

        # Co-Authored-By
        footer_lines.append("Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>")

        return "\n".join(footer_lines)

    def _assemble_message(self, commit_type: str, scope: str, subject: str, body: str, footer: str) -> str:
        """최종 메시지 조립"""
        parts = []

        # Header
        header = f"{commit_type}({scope}): {subject}"
        parts.append(header)

        # Body
        if body:
            parts.append("")
            parts.append(body)

        # Footer
        if footer:
            parts.append("")
            parts.append(footer)

        return "\n".join(parts)

    def commit(self, message: str) -> Dict:
        """실제 커밋 실행"""
        try:
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": result.stderr
                }

            # 커밋 해시 추출
            commit_hash = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            ).stdout.strip()

            return {
                "success": True,
                "commit_hash": commit_hash
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def save_log(self, ticket_num: str, result: Dict, commit_hash: str = None):
        """커밋 로그 저장"""
        log_dir = self.project_path / "logs" / "commit"
        log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file = log_dir / f"{timestamp}-{ticket_num}.json"

        log_data = {
            "ticket": ticket_num,
            "timestamp": datetime.now().isoformat() + "Z",
            "commit_hash": commit_hash,
            "commit_type": result.get("commit_type"),
            "scope": result.get("scope"),
            "subject": result.get("subject"),
            "changed_files": result.get("changed_files", []),
            "auto_generated": True,
            "message": result.get("message")
        }

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        print(f"💾 로그 저장: {log_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="커밋 메시지 자동 생성")
    parser.add_argument("--ticket", required=True, help="티켓 번호 (예: PLAN-001)")
    parser.add_argument("--project", help="프로젝트 경로 (선택)")
    parser.add_argument("--dry-run", action="store_true", help="메시지만 생성 (커밋 안 함)")
    parser.add_argument("--generate-only", action="store_true", help="메시지만 출력")

    args = parser.parse_args()

    # 프로젝트 경로
    if args.project:
        project_path = Path(args.project)
    else:
        # 현재 디렉토리에서 프로젝트 루트 찾기
        current = Path.cwd()
        while current != current.parent:
            if (current / ".git").exists():
                project_path = current
                break
            current = current.parent
        else:
            print("❌ Git 저장소를 찾을 수 없습니다.")
            sys.exit(1)

    workspace_root = project_path.parent.parent  # team/

    generator = CommitMessageGenerator(project_path, workspace_root)

    # 메시지 생성
    result = generator.generate(args.ticket)

    if not result["success"]:
        print(f"❌ 메시지 생성 실패: {result.get('error')}")
        sys.exit(1)

    # Generate-only 모드
    if args.generate_only:
        print(result["message"])
        sys.exit(0)

    # Dry-run 모드
    if args.dry_run:
        print("✅ Dry-run 모드 - 실제 커밋 생략")
        sys.exit(0)

    # 실제 커밋
    print("5️⃣  커밋 실행 중...\n")
    commit_result = generator.commit(result["message"])

    if commit_result["success"]:
        print(f"✅ 커밋 완료: {commit_result['commit_hash']}")

        # 로그 저장
        generator.save_log(args.ticket, result, commit_result["commit_hash"])

    else:
        print(f"❌ 커밋 실패: {commit_result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
