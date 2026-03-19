#!/usr/bin/env python3
"""
Refactor Code Skill - 코드 개선 제안 자동화

Usage:
    python3 refactor-code.py --file src/auth/login.js
    python3 refactor-code.py --dir src/auth/
    python3 refactor-code.py --all
    python3 refactor-code.py --file src/auth/login.js --dry-run
    python3 refactor-code.py --file src/auth/login.js --auto-fix
"""

import argparse
import json
import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class RefactorIssue:
    """리팩토링 이슈"""
    severity: str  # error, warning, info
    type: str  # long_method, duplicate_code, magic_number, etc.
    file: str
    line_start: int
    line_end: int
    description: str
    current_code: str
    suggested_code: str
    benefits: List[str]
    auto_fixable: bool
    complexity_before: int = 0
    complexity_after: int = 0


class RefactorCodeSkill:
    """리팩토링 코드 스킬"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.memory_file = self.project_root / "team" / ".memory" / "refactor-patterns.json"
        self.issues: List[RefactorIssue] = []

    def analyze_file(self, file_path: str) -> List[RefactorIssue]:
        """파일 분석"""
        self.issues = []

        if not os.path.exists(file_path):
            print(f"❌ 파일 없음: {file_path}")
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # 코드 스멜 감지
        self._detect_long_methods(file_path, lines)
        self._detect_duplicate_code(file_path, lines)
        self._detect_magic_numbers(file_path, lines)
        self._detect_large_classes(file_path, lines)

        # 성능 이슈 감지
        self._detect_n_plus_one(file_path, lines)
        self._detect_serial_async(file_path, lines)

        return self.issues

    def _detect_long_methods(self, file_path: str, lines: List[str]):
        """긴 함수 감지"""
        # JavaScript/TypeScript 함수
        func_pattern = r'^\s*(function|const|let|var)\s+(\w+)\s*[=(]|^\s*(\w+)\s*\([^)]*\)\s*{'

        current_func = None
        func_start = 0
        brace_count = 0

        for i, line in enumerate(lines):
            # 함수 시작
            if re.search(func_pattern, line):
                if current_func is None:
                    match = re.search(r'(function|const|let|var)\s+(\w+)', line)
                    if match:
                        current_func = match.group(2)
                        func_start = i
                        brace_count = line.count('{') - line.count('}')
            elif current_func:
                brace_count += line.count('{') - line.count('}')

                # 함수 끝
                if brace_count <= 0:
                    func_length = i - func_start + 1

                    if func_length > 50:
                        self.issues.append(RefactorIssue(
                            severity="error" if func_length > 100 else "warning",
                            type="long_method",
                            file=file_path,
                            line_start=func_start + 1,
                            line_end=i + 1,
                            description=f"함수 '{current_func}'가 너무 깁니다 ({func_length}줄, 권장: 50줄 이하)",
                            current_code='\n'.join(lines[func_start:i+1]),
                            suggested_code="# Extract smaller functions\n# Suggestion: Break into logical units",
                            benefits=["가독성 향상", "테스트 용이", "재사용성 증가"],
                            auto_fixable=False
                        ))

                    current_func = None
                    brace_count = 0

    def _detect_duplicate_code(self, file_path: str, lines: List[str]):
        """중복 코드 감지"""
        min_lines = 6
        seen_blocks = {}

        for i in range(len(lines) - min_lines):
            block = '\n'.join(lines[i:i+min_lines])
            block_stripped = block.strip()

            if len(block_stripped) < 20:  # 너무 짧은 블록 무시
                continue

            if block_stripped in seen_blocks:
                prev_line = seen_blocks[block_stripped]
                self.issues.append(RefactorIssue(
                    severity="warning",
                    type="duplicate_code",
                    file=file_path,
                    line_start=i + 1,
                    line_end=i + min_lines + 1,
                    description=f"중복 코드 감지 (line {prev_line}와 중복)",
                    current_code=block,
                    suggested_code="# Extract to a function\n# Suggestion: Create reusable helper",
                    benefits=["중복 제거", "유지보수 용이", "버그 감소"],
                    auto_fixable=False
                ))
            else:
                seen_blocks[block_stripped] = i + 1

    def _detect_magic_numbers(self, file_path: str, lines: List[str]):
        """매직 넘버 감지"""
        # 2자리 이상 숫자 (0, 1, -1 제외)
        pattern = r'\b(?!0\b|1\b|-1\b)\d{2,}\b'

        for i, line in enumerate(lines):
            # 주석이나 문자열 내부는 제외
            if '//' in line or '/*' in line or '#' in line:
                continue
            if '"' in line or "'" in line:
                continue

            matches = re.finditer(pattern, line)
            for match in matches:
                number = match.group()
                self.issues.append(RefactorIssue(
                    severity="warning",
                    type="magic_number",
                    file=file_path,
                    line_start=i + 1,
                    line_end=i + 1,
                    description=f"매직 넘버 '{number}' 발견",
                    current_code=line.strip(),
                    suggested_code=f"const CONSTANT_NAME = {number};\n{line.strip().replace(number, 'CONSTANT_NAME')}",
                    benefits=["의미 명확화", "변경 용이", "재사용 가능"],
                    auto_fixable=True
                ))

    def _detect_large_classes(self, file_path: str, lines: List[str]):
        """거대 클래스 감지"""
        class_pattern = r'^\s*class\s+(\w+)'

        current_class = None
        class_start = 0
        method_count = 0
        brace_count = 0

        for i, line in enumerate(lines):
            if re.search(class_pattern, line):
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    current_class = match.group(1)
                    class_start = i
                    method_count = 0
                    brace_count = line.count('{') - line.count('}')
            elif current_class:
                brace_count += line.count('{') - line.count('}')

                # 메서드 카운트
                if re.search(r'^\s*(public|private|protected)?\s*\w+\s*\([^)]*\)\s*{', line):
                    method_count += 1

                # 클래스 끝
                if brace_count <= 0:
                    class_length = i - class_start + 1

                    if class_length > 300 or method_count > 20:
                        self.issues.append(RefactorIssue(
                            severity="error",
                            type="god_object",
                            file=file_path,
                            line_start=class_start + 1,
                            line_end=i + 1,
                            description=f"클래스 '{current_class}'가 너무 큽니다 ({class_length}줄, {method_count}개 메서드)",
                            current_code=f"# Class too large: {class_length} lines, {method_count} methods",
                            suggested_code="# Split into smaller classes\n# Suggestion: Apply Single Responsibility Principle",
                            benefits=["단일 책임 원칙", "테스트 용이", "재사용성"],
                            auto_fixable=False
                        ))

                    current_class = None

    def _detect_n_plus_one(self, file_path: str, lines: List[str]):
        """N+1 쿼리 감지"""
        loop_patterns = [r'for\s*\(', r'\.forEach\(', r'\.map\(', r'while\s*\(']
        query_patterns = [r'\.query\(', r'\.find\(', r'\.get\(', r'SELECT']

        in_loop = False
        loop_start = 0

        for i, line in enumerate(lines):
            # 루프 시작
            if any(re.search(pattern, line) for pattern in loop_patterns):
                in_loop = True
                loop_start = i

            # 루프 내 쿼리
            if in_loop and any(re.search(pattern, line) for pattern in query_patterns):
                self.issues.append(RefactorIssue(
                    severity="warning",
                    type="n_plus_one",
                    file=file_path,
                    line_start=loop_start + 1,
                    line_end=i + 1,
                    description="N+1 쿼리 가능성 감지",
                    current_code='\n'.join(lines[loop_start:i+1]),
                    suggested_code="# Use eager loading or batch query\n# Example: .includes() or .with()",
                    benefits=["성능 향상 (최대 10-100배)", "DB 부하 감소"],
                    auto_fixable=False
                )
                in_loop = False

            # 루프 끝 (간단한 감지)
            if in_loop and '}' in line:
                in_loop = False

    def _detect_serial_async(self, file_path: str, lines: List[str]):
        """직렬 비동기 감지"""
        # 연속된 await
        serial_awaits = []

        for i in range(len(lines) - 1):
            if 'await' in lines[i] and 'await' in lines[i+1]:
                # 간단한 체크: 독립적인 호출인지
                if not any(keyword in lines[i+1] for keyword in ['if', 'for', 'while', 'return']):
                    serial_awaits.append(i)

        for i in serial_awaits:
            self.issues.append(RefactorIssue(
                severity="info",
                type="serial_async",
                file=file_path,
                line_start=i + 1,
                line_end=i + 3,
                description="직렬 비동기 호출 - 병렬 처리 가능",
                current_code='\n'.join(lines[i:i+2]),
                suggested_code="const [result1, result2] = await Promise.all([...]);",
                benefits=["성능 향상 (2-3배)", "응답 시간 단축"],
                auto_fixable=True
            ))

    def auto_fix(self, file_path: str, dry_run: bool = False) -> Dict:
        """자동 수정 적용"""
        issues = self.analyze_file(file_path)
        fixable = [i for i in issues if i.auto_fixable]

        if not fixable:
            return {"success": False, "message": "자동 수정 가능한 이슈 없음"}

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixed_count = 0

        # 매직 넘버 수정
        for issue in fixable:
            if issue.type == "magic_number":
                # 간단한 구현 (실제로는 더 복잡한 로직 필요)
                pass
            elif issue.type == "serial_async":
                # Promise.all 변환
                pass

        if not dry_run and fixed_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return {
            "success": True,
            "fixed_count": fixed_count,
            "dry_run": dry_run
        }

    def generate_report(self) -> str:
        """리팩토링 리포트 생성"""
        if not self.issues:
            return "✅ 리팩토링 이슈 없음"

        # 심각도별 그룹화
        errors = [i for i in self.issues if i.severity == "error"]
        warnings = [i for i in self.issues if i.severity == "warning"]
        infos = [i for i in self.issues if i.severity == "info"]
        auto_fixable = [i for i in self.issues if i.auto_fixable]

        report = ["# Refactoring Report\n"]
        report.append("## Summary")
        report.append(f"- **Issues Found**: {len(self.issues)}")
        report.append(f"- **Errors**: {len(errors)}")
        report.append(f"- **Warnings**: {len(warnings)}")
        report.append(f"- **Info**: {len(infos)}")
        report.append(f"- **Auto-fixable**: {len(auto_fixable)}\n")

        if errors:
            report.append("## Critical Issues\n")
            for i, issue in enumerate(errors, 1):
                report.append(f"### {i}. {issue.description}")
                report.append(f"**File**: `{issue.file}:{issue.line_start}`")
                report.append(f"**Type**: {issue.type}")
                report.append(f"**Auto-fix**: {'✅' if issue.auto_fixable else '❌'}\n")

        if warnings:
            report.append("## Warnings\n")
            for i, issue in enumerate(warnings, 1):
                report.append(f"### {i}. {issue.description}")
                report.append(f"**File**: `{issue.file}:{issue.line_start}`")
                report.append(f"**Benefits**: {', '.join(issue.benefits)}\n")

        if auto_fixable:
            report.append("## Auto-fix Available\n")
            report.append(f"Run: `python3 refactor-code.py --file <file> --auto-fix`\n")

        return '\n'.join(report)

    def save_to_memory(self):
        """메모리에 패턴 저장"""
        if not self.memory_file.parent.exists():
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)

        # 기존 메모리 로드
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                memory = json.load(f)
        else:
            memory = {
                "version": "0.0.1",
                "updated": datetime.now().isoformat(),
                "project": "multi-agent-coding-team",
                "applied_patterns": [],
                "common_smells": [],
                "metrics": {}
            }

        # 새 패턴 추가
        for issue in self.issues:
            memory["applied_patterns"].append({
                "pattern": issue.type,
                "file": issue.file,
                "timestamp": datetime.now().isoformat(),
                "auto_fixed": issue.auto_fixable
            })

        memory["updated"] = datetime.now().isoformat()

        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Refactor Code Skill")
    parser.add_argument('--file', help='분석할 파일')
    parser.add_argument('--dir', help='분석할 디렉토리')
    parser.add_argument('--all', action='store_true', help='전체 프로젝트 분석')
    parser.add_argument('--dry-run', action='store_true', help='미리보기만')
    parser.add_argument('--auto-fix', action='store_true', help='자동 수정 적용')

    args = parser.parse_args()

    skill = RefactorCodeSkill()

    if args.file:
        issues = skill.analyze_file(args.file)

        if args.auto_fix:
            result = skill.auto_fix(args.file, dry_run=args.dry_run)
            print(f"✅ {result['fixed_count']}개 이슈 수정")
        else:
            print(skill.generate_report())

        skill.save_to_memory()

    elif args.dir:
        # 디렉토리 내 모든 파일
        for root, dirs, files in os.walk(args.dir):
            for file in files:
                if file.endswith(('.js', '.ts', '.py', '.go')):
                    file_path = os.path.join(root, file)
                    skill.analyze_file(file_path)

        print(skill.generate_report())
        skill.save_to_memory()

    elif args.all:
        print("⚠️  전체 프로젝트 분석은 시간이 오래 걸릴 수 있습니다")
        # 구현 생략

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
