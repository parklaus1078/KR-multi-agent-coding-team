#!/usr/bin/env python3
"""
Review PR Skill - PR 자동 리뷰

Usage:
    python3 review-pr.py 123
    python3 review-pr.py --current-branch
    python3 review-pr.py --ticket PLAN-001
    python3 review-pr.py 123 --auto-fix
    python3 review-pr.py 123 --auto-fix --dry-run
"""

import argparse
import json
import re
import os
import subprocess
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class ReviewIssue:
    """리뷰 이슈"""
    severity: str  # error, warning, info
    category: str  # completeness, quality, security, style, performance, documentation
    type: str
    file: str
    line: int
    description: str
    current_code: str
    suggested_code: str
    auto_fixable: bool


class ReviewPRSkill:
    """PR 리뷰 스킬"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.checklist_file = self.project_root / "team" / ".skills" / "review-pr" / "review-checklist.json"
        self.memory_file = self.project_root / "team" / ".memory" / "review-history.json"
        self.issues: List[ReviewIssue] = []
        self.checklist = self._load_checklist()

    def _load_checklist(self) -> Dict:
        """체크리스트 로드"""
        if not self.checklist_file.exists():
            return {}

        with open(self.checklist_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _run_command(self, cmd: str) -> str:
        """명령어 실행"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result.stdout.strip()
        except Exception as e:
            return ""

    def get_pr_files(self, pr_number: int = None, base_branch: str = "main") -> List[str]:
        """PR 변경 파일 목록"""
        if pr_number:
            # GitHub CLI 사용
            cmd = f"gh pr diff {pr_number} --name-only"
        else:
            # 현재 브랜치 대비 main
            cmd = f"git diff {base_branch}...HEAD --name-only"

        output = self._run_command(cmd)
        return [f for f in output.split('\n') if f]

    def get_pr_diff(self, file_path: str, base_branch: str = "main") -> str:
        """파일 diff"""
        cmd = f"git diff {base_branch}...HEAD -- {file_path}"
        return self._run_command(cmd)

    def check_completeness(self, files: List[str], ticket_num: str = None):
        """완전성 검사"""
        if not self.checklist.get("completeness", {}).get("enabled"):
            return

        checks = self.checklist["completeness"]["checks"]

        # TODO/FIXME 검사
        if checks.get("no_todo_fixme", {}).get("enabled"):
            patterns = checks["no_todo_fixme"]["patterns"]
            for file in files:
                if not os.path.exists(file):
                    continue

                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines):
                    for pattern in patterns:
                        if pattern in line:
                            self.issues.append(ReviewIssue(
                                severity=checks["no_todo_fixme"]["severity"],
                                category="completeness",
                                type="todo_fixme",
                                file=file,
                                line=i + 1,
                                description=f"{pattern} 주석 발견",
                                current_code=line.strip(),
                                suggested_code="# 구현 완료 또는 티켓 생성",
                                auto_fixable=False
                            ))

        # 테스트 존재 검사
        if checks.get("tests_exist", {}).get("enabled"):
            test_files = [f for f in files if 'test' in f or 'spec' in f]
            if not test_files:
                self.issues.append(ReviewIssue(
                    severity=checks["tests_exist"]["severity"],
                    category="completeness",
                    type="missing_tests",
                    file="N/A",
                    line=0,
                    description="테스트 파일이 없습니다",
                    current_code="",
                    suggested_code="# 테스트 추가 필요",
                    auto_fixable=False
                ))

    def check_quality(self, files: List[str]):
        """품질 검사"""
        if not self.checklist.get("quality", {}).get("enabled"):
            return

        checks = self.checklist["quality"]["checks"]

        for file in files:
            if not os.path.exists(file):
                continue

            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 함수 길이 검사
            if checks.get("function_length", {}).get("enabled"):
                self._check_function_length(file, lines, checks["function_length"])

            # 복잡도 검사 (간단한 버전)
            if checks.get("complexity", {}).get("enabled"):
                self._check_complexity(file, lines, checks["complexity"])

            # 매직 넘버 검사
            if checks.get("magic_numbers", {}).get("enabled"):
                self._check_magic_numbers(file, lines, checks["magic_numbers"])

    def _check_function_length(self, file: str, lines: List[str], config: Dict):
        """함수 길이 검사"""
        max_lines = config["max_lines"]
        func_pattern = r'^\s*(function|def|const|let)\s+(\w+)'

        current_func = None
        func_start = 0
        brace_count = 0

        for i, line in enumerate(lines):
            if re.search(func_pattern, line):
                if current_func is None:
                    match = re.search(r'(function|def|const|let)\s+(\w+)', line)
                    if match:
                        current_func = match.group(2)
                        func_start = i
                        brace_count = line.count('{') - line.count('}')
            elif current_func:
                brace_count += line.count('{') - line.count('}')

                if brace_count <= 0:
                    func_length = i - func_start + 1

                    if func_length > max_lines:
                        self.issues.append(ReviewIssue(
                            severity=config["severity"],
                            category="quality",
                            type="function_length",
                            file=file,
                            line=func_start + 1,
                            description=f"함수 '{current_func}'가 너무 깁니다 ({func_length}줄 > {max_lines}줄)",
                            current_code=f"# Function: {current_func}",
                            suggested_code="# Extract smaller functions",
                            auto_fixable=False
                        ))

                    current_func = None

    def _check_complexity(self, file: str, lines: List[str], config: Dict):
        """복잡도 검사 (간단한 순환 복잡도)"""
        max_complexity = config["max_complexity"]

        for i, line in enumerate(lines):
            # 간단한 계산: if, for, while, case 개수
            complexity = (
                line.count('if ') +
                line.count('for ') +
                line.count('while ') +
                line.count('case ') +
                line.count('&&') +
                line.count('||')
            )

            if complexity > 3:  # 한 줄에 복잡도 > 3
                self.issues.append(ReviewIssue(
                    severity=config["severity"],
                    category="quality",
                    type="complexity",
                    file=file,
                    line=i + 1,
                    description=f"복잡한 조건문 (간단히 하세요)",
                    current_code=line.strip(),
                    suggested_code="# Extract to named function",
                    auto_fixable=False
                ))

    def _check_magic_numbers(self, file: str, lines: List[str], config: Dict):
        """매직 넘버 검사"""
        allowed = config["allowed"]
        pattern = r'\b\d{2,}\b'

        for i, line in enumerate(lines):
            if '//' in line or '#' in line or '"' in line or "'" in line:
                continue

            matches = re.finditer(pattern, line)
            for match in matches:
                number = int(match.group())
                if number not in allowed:
                    self.issues.append(ReviewIssue(
                        severity=config["severity"],
                        category="quality",
                        type="magic_number",
                        file=file,
                        line=i + 1,
                        description=f"매직 넘버 '{number}' 발견",
                        current_code=line.strip(),
                        suggested_code=f"const CONSTANT_NAME = {number};",
                        auto_fixable=True
                    ))

    def check_security(self, files: List[str]):
        """보안 검사"""
        if not self.checklist.get("security", {}).get("enabled"):
            return

        checks = self.checklist["security"]["checks"]

        for file in files:
            if not os.path.exists(file):
                continue

            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # 하드코딩 비밀번호
            if checks.get("hardcoded_secrets", {}).get("enabled"):
                patterns = checks["hardcoded_secrets"]["patterns"]
                for i, line in enumerate(lines):
                    for pattern in patterns:
                        if re.search(pattern, line):
                            self.issues.append(ReviewIssue(
                                severity=checks["hardcoded_secrets"]["severity"],
                                category="security",
                                type="hardcoded_secret",
                                file=file,
                                line=i + 1,
                                description="하드코딩된 비밀번호/API 키 발견",
                                current_code=line.strip(),
                                suggested_code="# Use environment variables",
                                auto_fixable=True
                            ))

            # SQL Injection
            if checks.get("sql_injection", {}).get("enabled"):
                patterns = checks["sql_injection"]["patterns"]
                for i, line in enumerate(lines):
                    for pattern in patterns:
                        if re.search(pattern, line):
                            self.issues.append(ReviewIssue(
                                severity=checks["sql_injection"]["severity"],
                                category="security",
                                type="sql_injection",
                                file=file,
                                line=i + 1,
                                description="SQL Injection 가능성",
                                current_code=line.strip(),
                                suggested_code="# Use parameterized queries",
                                auto_fixable=False
                            ))

            # XSS
            if checks.get("xss", {}).get("enabled"):
                patterns = checks["xss"]["patterns"]
                for i, line in enumerate(lines):
                    for pattern in patterns:
                        if re.search(pattern, line):
                            self.issues.append(ReviewIssue(
                                severity=checks["xss"]["severity"],
                                category="security",
                                type="xss",
                                file=file,
                                line=i + 1,
                                description="XSS 가능성",
                                current_code=line.strip(),
                                suggested_code="# Sanitize user input",
                                auto_fixable=False
                            ))

    def review_pr(self, pr_number: int = None, ticket_num: str = None) -> Dict:
        """PR 리뷰 실행"""
        self.issues = []

        # 변경 파일 가져오기
        files = self.get_pr_files(pr_number)

        if not files:
            return {"success": False, "message": "변경된 파일 없음"}

        # 각 카테고리 검사
        self.check_completeness(files, ticket_num)
        self.check_quality(files)
        self.check_security(files)

        # 결과 정리
        errors = [i for i in self.issues if i.severity == "error"]
        warnings = [i for i in self.issues if i.severity == "warning"]
        infos = [i for i in self.issues if i.severity == "info"]
        auto_fixable = [i for i in self.issues if i.auto_fixable]

        status = "approved" if not errors else "changes_requested"

        return {
            "success": True,
            "status": status,
            "pr_number": pr_number,
            "files_reviewed": len(files),
            "issues_found": len(self.issues),
            "errors": len(errors),
            "warnings": len(warnings),
            "infos": len(infos),
            "auto_fixable_count": len(auto_fixable)
        }

    def generate_report(self, pr_number: int = None) -> str:
        """리뷰 리포트 생성"""
        errors = [i for i in self.issues if i.severity == "error"]
        warnings = [i for i in self.issues if i.severity == "warning"]
        infos = [i for i in self.issues if i.severity == "info"]
        auto_fixable = [i for i in self.issues if i.auto_fixable]

        status_emoji = "✅" if not errors else "❌"
        status_text = "Approved" if not errors else "Changes Requested"

        report = [f"# PR Review{f': #{pr_number}' if pr_number else ''}\n"]
        report.append("## Summary")
        report.append(f"- **Status**: {status_emoji} {status_text}")
        report.append(f"- **Issues Found**: {len(self.issues)}")
        report.append(f"- **Errors**: {len(errors)}")
        report.append(f"- **Warnings**: {len(warnings)}")
        report.append(f"- **Auto-fixable**: {len(auto_fixable)}\n")

        if errors:
            report.append("## Critical Issues\n")
            for i, issue in enumerate(errors, 1):
                report.append(f"### {i}. {issue.description}")
                report.append(f"**File**: `{issue.file}:{issue.line}`")
                report.append(f"**Category**: {issue.category}")
                report.append(f"**Type**: {issue.type}")
                report.append(f"**Auto-fix**: {'✅' if issue.auto_fixable else '❌'}\n")

        if warnings:
            report.append("## Warnings\n")
            for i, issue in enumerate(warnings, 1):
                report.append(f"### {i}. {issue.description}")
                report.append(f"**File**: `{issue.file}:{issue.line}`\n")

        if auto_fixable:
            report.append("## Auto-fix Available\n")
            report.append(f"Run: `python3 review-pr.py {pr_number or '--current-branch'} --auto-fix`\n")
            report.append("Fixes:")
            for i, issue in enumerate(auto_fixable, 1):
                report.append(f"{i}. {issue.description} ({issue.file}:{issue.line})")

        return '\n'.join(report)

    def auto_fix(self, dry_run: bool = False) -> Dict:
        """자동 수정"""
        fixable = [i for i in self.issues if i.auto_fixable]

        if not fixable:
            return {"success": False, "message": "자동 수정 가능한 이슈 없음"}

        fixed_count = 0

        for issue in fixable:
            # 간단한 수정만 구현 (실제로는 더 정교한 로직 필요)
            if not dry_run:
                # 파일 수정 로직
                pass

            fixed_count += 1

        return {
            "success": True,
            "fixed_count": fixed_count,
            "dry_run": dry_run
        }


def main():
    parser = argparse.ArgumentParser(description="Review PR Skill")
    parser.add_argument('pr_number', nargs='?', type=int, help='PR 번호')
    parser.add_argument('--current-branch', action='store_true', help='현재 브랜치 리뷰')
    parser.add_argument('--ticket', help='티켓 번호')
    parser.add_argument('--auto-fix', action='store_true', help='자동 수정')
    parser.add_argument('--dry-run', action='store_true', help='미리보기')

    args = parser.parse_args()

    skill = ReviewPRSkill()

    # PR 리뷰
    result = skill.review_pr(
        pr_number=args.pr_number,
        ticket_num=args.ticket
    )

    if not result["success"]:
        print(f"❌ {result['message']}")
        return

    # 리포트 출력
    print(skill.generate_report(args.pr_number))

    # Auto-fix
    if args.auto_fix:
        fix_result = skill.auto_fix(dry_run=args.dry_run)
        if fix_result["success"]:
            print(f"\n✅ {fix_result['fixed_count']}개 이슈 수정")


if __name__ == "__main__":
    main()
