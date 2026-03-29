#!/usr/bin/env python3
"""
Spec Validation Skill - PM Agent 출력물 자동 검증

Usage:
    python validate.py PLAN-001
    python validate.py PLAN-001 --auto-fix
    python validate.py --all
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ValidationResult:
    """검증 결과"""
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    auto_fixes: List[str] = field(default_factory=list)
    details: Dict = field(default_factory=dict)


class SpecValidator:
    """명세서 검증기"""

    def __init__(self, project_root: Path, ticket_num: str):
        self.project_root = project_root
        self.ticket_num = ticket_num
        self.rules = self._load_rules()
        self.project_meta = self._load_project_meta()
        self.project_type = self.project_meta.get("project_type", "web-fullstack")

    def _load_rules(self) -> dict:
        """rules.json 로드"""
        rules_path = Path(__file__).parent / "rules.json"
        with open(rules_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_project_meta(self) -> dict:
        """프로젝트 메타 정보 로드"""
        meta_path = self.project_root / ".project-meta.json"
        if not meta_path.exists():
            return {"project_type": "web-fullstack"}
        with open(meta_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def validate(self, auto_fix: bool = False) -> ValidationResult:
        """전체 검증 실행"""
        result = ValidationResult(passed=True)

        print(f"\n{'='*60}")
        print(f"Spec Validation: {self.ticket_num}")
        print(f"프로젝트 타입: {self.project_type}")
        print(f"{'='*60}\n")

        # 1. 완전성 검사
        if self.rules["rules"]["completeness"]["enabled"]:
            self._check_completeness(result)

        # 2. 범위 준수 검사
        if self.rules["rules"]["scope_compliance"]["enabled"]:
            self._check_scope_compliance(result)

        # 3. 품질 게이트
        self._check_quality_gates(result)

        # 4. 구현 세부사항 침범
        if self.rules["rules"]["implementation_details"]["enabled"]:
            self._check_implementation_details(result)

        # 5. 자동 수정
        if auto_fix and self.rules["auto_fix"]["enabled"]:
            self._apply_auto_fixes(result)

        # 최종 판정
        result.passed = len(result.errors) == 0

        return result

    def _check_completeness(self, result: ValidationResult):
        """완전성 검사 - 필수 파일 및 섹션"""
        print("1️⃣  완전성 검사...")

        type_reqs = self.rules["project_type_requirements"].get(self.project_type, {})
        required_files = type_reqs.get("required_files", [])

        # 티켓 파일에서 slug 추출
        ticket_slug = self._extract_ticket_slug()

        missing_files = []
        found_files = []

        for file_pattern in required_files:
            # {number}, {slug} 치환
            file_path = file_pattern.replace("{number}", self.ticket_num.replace("PLAN-", ""))
            file_path = file_path.replace("{slug}", ticket_slug)

            full_path = self.project_root / "planning" / file_path

            if full_path.exists():
                found_files.append(file_path)
                # 섹션 검사
                self._check_file_sections(full_path, file_path, result)
            else:
                missing_files.append(file_path)

        result.details["completeness"] = {
            "found": found_files,
            "missing": missing_files
        }

        if missing_files:
            for file in missing_files:
                result.errors.append(f"[완전성] 필수 파일 누락: {file}")
            print(f"   ❌ {len(missing_files)}개 파일 누락")
        else:
            print(f"   ✅ {len(found_files)}/{len(required_files)} 파일 생성 완료")

    def _check_file_sections(self, file_path: Path, file_name: str, result: ValidationResult):
        """파일 내 필수 섹션 확인"""
        type_reqs = self.rules["project_type_requirements"].get(self.project_type, {})
        required_sections = type_reqs.get("required_sections", {})

        # 파일 타입 추출 (backend, frontend, command-spec 등)
        file_type = None
        if "backend" in file_name:
            file_type = "backend"
        elif "frontend" in file_name:
            file_type = "frontend"
        elif "command-spec" in file_name:
            file_type = "command-spec"
        elif "screens" in file_name:
            file_type = "screens"
        elif "state" in file_name:
            file_type = "state"
        elif "api" in file_name:
            file_type = "api"
        elif "examples" in file_name:
            file_type = "examples"

        if not file_type or file_type not in required_sections:
            return

        content = file_path.read_text(encoding='utf-8')
        missing_sections = []

        for section in required_sections[file_type]:
            # 섹션 헤더 찾기 (## 또는 ###)
            pattern = rf"#+\s*{re.escape(section)}"
            if not re.search(pattern, content, re.IGNORECASE):
                missing_sections.append(section)

        if missing_sections:
            for section in missing_sections:
                result.errors.append(f"[완전성] {file_name}에 '{section}' 섹션 누락")

    def _check_scope_compliance(self, result: ValidationResult):
        """범위 준수 검사 - Gotcha #1"""
        print("2️⃣  범위 준수 검사...")

        # 티켓 파일 읽기
        ticket_content = self._read_ticket_file()
        if not ticket_content:
            result.warnings.append("[범위] 티켓 파일을 읽을 수 없어 범위 검사 생략")
            return

        # Acceptance Criteria 추출
        ticket_features = self._extract_acceptance_criteria(ticket_content)

        # 명세서 파일들 읽기
        spec_files = self._find_spec_files()
        scope_creep_detected = []

        scope_keywords = self.rules["rules"]["scope_compliance"]["scope_creep_keywords"]

        for spec_file in spec_files:
            content = spec_file.read_text(encoding='utf-8')

            # 범위 확대 키워드 탐지
            for keyword in scope_keywords:
                if keyword in content and keyword not in ticket_content:
                    scope_creep_detected.append((keyword, spec_file.name))

        result.details["scope_compliance"] = {
            "ticket_features": ticket_features,
            "scope_creep": scope_creep_detected
        }

        if scope_creep_detected:
            # Out-of-Scope 섹션 확인
            has_out_of_scope = any(
                "Out of Scope" in f.read_text(encoding='utf-8') or
                "Out-of-Scope" in f.read_text(encoding='utf-8')
                for f in spec_files
            )

            for keyword, file_name in scope_creep_detected:
                if has_out_of_scope:
                    result.warnings.append(
                        f"[범위] '{keyword}' 발견 (티켓에 없음) - {file_name}"
                    )
                else:
                    result.errors.append(
                        f"[범위] '{keyword}' 발견 (티켓에 없음) + Out-of-Scope 섹션 누락 - {file_name}"
                    )

            print(f"   ⚠️  {len(scope_creep_detected)}개 범위 확대 의심 키워드 발견")
        else:
            print("   ✅ 범위 확대 없음")

    def _check_quality_gates(self, result: ValidationResult):
        """품질 게이트 검사"""
        print("3️⃣  품질 게이트...")

        quality_rules = self.rules["rules"]["quality_gates"]

        # API 에러 응답 검사
        if quality_rules["error_responses"]["enabled"]:
            self._check_error_responses(result)

        # HTML 외부 라이브러리 검사
        if quality_rules["html_libraries"]["enabled"]:
            self._check_html_libraries(result)

        # HTML API 호출 검사
        if quality_rules["html_api_calls"]["enabled"]:
            self._check_html_api_calls(result)

        # 접근성 테스트 검사
        if quality_rules["accessibility"]["enabled"]:
            if self.project_type in quality_rules["accessibility"]["applies_to"]:
                self._check_accessibility(result)

        # CLI Exit Code 검사
        if quality_rules["cli_exit_codes"]["enabled"]:
            if self.project_type in quality_rules["cli_exit_codes"]["applies_to"]:
                self._check_cli_exit_codes(result)

    def _check_error_responses(self, result: ValidationResult):
        """API 에러 응답 검사 - Gotcha #8"""
        required_codes = self.rules["rules"]["quality_gates"]["error_responses"]["required_codes"]

        # backend 명세서 찾기
        backend_files = list(self.project_root.glob(f"planning/specs/backend/{self.ticket_num}*.md"))

        if not backend_files:
            return

        missing_errors = []

        for backend_file in backend_files:
            content = backend_file.read_text(encoding='utf-8')

            for code in required_codes:
                # "Response 400", "401:", "에러 500" 등 패턴
                pattern = rf"(Response|응답|에러|Error)\s*{code}"
                if not re.search(pattern, content, re.IGNORECASE):
                    missing_errors.append(f"{code} (in {backend_file.name})")

        if missing_errors:
            for err in missing_errors:
                result.errors.append(f"[품질] API 에러 응답 누락: {err}")
            print(f"   ❌ {len(missing_errors)}개 에러 응답 누락")
        else:
            print("   ✅ API 에러 응답 완비")

    def _check_html_libraries(self, result: ValidationResult):
        """HTML 외부 라이브러리 검사 - Gotcha #4"""
        forbidden = self.rules["rules"]["quality_gates"]["html_libraries"]["forbidden_patterns"]

        html_files = list(self.project_root.glob(f"planning/specs/**/{self.ticket_num}*.html"))

        violations = []

        for html_file in html_files:
            content = html_file.read_text(encoding='utf-8')

            for pattern in forbidden:
                if re.search(pattern, content, re.IGNORECASE):
                    violations.append((pattern, html_file.name))

        if violations:
            for pattern, file_name in violations:
                result.errors.append(f"[품질] HTML 외부 라이브러리 사용: '{pattern}' in {file_name}")
            print(f"   ❌ {len(violations)}개 금지 패턴 발견")
        elif html_files:
            print("   ✅ HTML 외부 라이브러리 없음")

    def _check_html_api_calls(self, result: ValidationResult):
        """HTML 실제 API 호출 검사 - Gotcha #5"""
        forbidden = self.rules["rules"]["quality_gates"]["html_api_calls"]["forbidden_patterns"]

        html_files = list(self.project_root.glob(f"planning/specs/**/{self.ticket_num}*.html"))

        violations = []

        for html_file in html_files:
            content = html_file.read_text(encoding='utf-8')

            for pattern in forbidden:
                if re.search(pattern, content):
                    violations.append((pattern, html_file.name))

        if violations:
            for pattern, file_name in violations:
                result.errors.append(f"[품질] HTML 실제 API 호출 금지: '{pattern}' in {file_name}")
            print(f"   ❌ {len(violations)}개 금지 API 호출 발견")
        elif html_files:
            print("   ✅ HTML API 호출 없음 (목업만 사용)")

    def _check_accessibility(self, result: ValidationResult):
        """접근성 테스트 검사 - Gotcha #9"""
        keywords = self.rules["rules"]["quality_gates"]["accessibility"]["keywords"]

        test_files = list(self.project_root.glob(f"planning/test-cases/{self.ticket_num}*frontend.md"))

        if not test_files:
            return

        found = False

        for test_file in test_files:
            content = test_file.read_text(encoding='utf-8')

            for keyword in keywords:
                if keyword in content:
                    found = True
                    break

            if found:
                break

        if not found:
            result.warnings.append("[품질] 접근성 테스트 케이스 누락")
            print("   ⚠️  접근성 테스트 케이스 누락")
        else:
            print("   ✅ 접근성 테스트 포함")

    def _check_cli_exit_codes(self, result: ValidationResult):
        """CLI Exit Code 검사"""
        keywords = self.rules["rules"]["quality_gates"]["cli_exit_codes"]["keywords"]

        spec_files = list(self.project_root.glob(f"planning/specs/{self.ticket_num}*command-spec.md"))

        if not spec_files:
            return

        found = False

        for spec_file in spec_files:
            content = spec_file.read_text(encoding='utf-8')

            for keyword in keywords:
                if keyword in content:
                    found = True
                    break

            if found:
                break

        if not found:
            result.errors.append("[품질] CLI Exit Code 정의 누락")
            print("   ❌ CLI Exit Code 정의 누락")
        else:
            print("   ✅ CLI Exit Code 정의됨")

    def _check_implementation_details(self, result: ValidationResult):
        """구현 세부사항 침범 검사 - Gotcha #10"""
        print("4️⃣  구현 세부사항 침범 검사...")

        forbidden = self.rules["rules"]["implementation_details"]["forbidden_keywords"]

        spec_files = self._find_spec_files()
        violations = []

        for spec_file in spec_files:
            content = spec_file.read_text(encoding='utf-8')

            for keyword in forbidden:
                if keyword in content:
                    violations.append((keyword, spec_file.name))

        result.details["implementation_details"] = violations

        if violations:
            for keyword, file_name in violations:
                result.warnings.append(
                    f"[구현] 구현 세부사항 포함 의심: '{keyword}' in {file_name}"
                )
            print(f"   ⚠️  {len(violations)}개 구현 세부사항 키워드 발견")
        else:
            print("   ✅ 구현 세부사항 침범 없음")

    def _apply_auto_fixes(self, result: ValidationResult):
        """자동 수정 적용"""
        print("\n5️⃣  자동 수정 적용...")

        auto_fix_rules = self.rules["auto_fix"]["rules"]

        for rule in auto_fix_rules:
            if not rule["enabled"]:
                continue

            if rule["id"] == "add_out_of_scope_section":
                self._add_out_of_scope_section(result)
            elif rule["id"] == "replace_hardcoded_secrets":
                self._replace_hardcoded_secrets(result)
            elif rule["id"] == "http_to_https":
                self._http_to_https(result)

    def _add_out_of_scope_section(self, result: ValidationResult):
        """Out-of-Scope 섹션 자동 추가"""
        spec_files = self._find_spec_files()

        for spec_file in spec_files:
            content = spec_file.read_text(encoding='utf-8')

            if "Out of Scope" not in content and "Out-of-Scope" not in content:
                # 파일 끝에 섹션 추가
                new_content = content.rstrip() + "\n\n## Out of Scope\n\n(명세서 검증 중 자동 생성됨 - 검토 후 수동 작성 필요)\n\n"
                spec_file.write_text(new_content, encoding='utf-8')
                result.auto_fixes.append(f"Out-of-Scope 섹션 추가: {spec_file.name}")

    def _replace_hardcoded_secrets(self, result: ValidationResult):
        """하드코딩된 비밀번호 → 환경 변수"""
        patterns = self.rules["auto_fix"]["rules"][1]["patterns"]

        spec_files = self._find_spec_files()

        for spec_file in spec_files:
            content = spec_file.read_text(encoding='utf-8')
            modified = False

            for pattern_rule in patterns:
                old_pattern = pattern_rule["find"]
                new_pattern = pattern_rule["replace"]

                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    modified = True

            if modified:
                spec_file.write_text(content, encoding='utf-8')
                result.auto_fixes.append(f"하드코딩 비밀번호 제거: {spec_file.name}")

    def _http_to_https(self, result: ValidationResult):
        """HTTP → HTTPS 변환"""
        spec_files = self._find_spec_files()

        for spec_file in spec_files:
            content = spec_file.read_text(encoding='utf-8')

            if "http://" in content:
                content = content.replace("http://", "https://")
                spec_file.write_text(content, encoding='utf-8')
                result.auto_fixes.append(f"HTTP → HTTPS 변환: {spec_file.name}")

    # Helper methods

    def _extract_ticket_slug(self) -> str:
        """티켓 파일에서 slug 추출"""
        ticket_files = list(self.project_root.glob(f"planning/tickets/{self.ticket_num}*.md"))

        if not ticket_files:
            return "unknown"

        # PLAN-001-user-auth.md → user-auth
        filename = ticket_files[0].stem
        parts = filename.split("-", 2)
        if len(parts) >= 3:
            return parts[2]
        return "unknown"

    def _read_ticket_file(self) -> str:
        """티켓 파일 읽기"""
        ticket_files = list(self.project_root.glob(f"planning/tickets/{self.ticket_num}*.md"))

        if not ticket_files:
            return ""

        return ticket_files[0].read_text(encoding='utf-8')

    def _extract_acceptance_criteria(self, ticket_content: str) -> List[str]:
        """티켓에서 Acceptance Criteria 추출"""
        # "## Acceptance Criteria" 섹션 찾기
        pattern = r"##\s*Acceptance Criteria\s*\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, ticket_content, re.DOTALL | re.IGNORECASE)

        if not match:
            return []

        criteria_text = match.group(1)

        # 각 항목 추출 (- 또는 * 로 시작)
        items = re.findall(r"^[*-]\s*(.+)$", criteria_text, re.MULTILINE)

        return items

    def _find_spec_files(self) -> List[Path]:
        """명세서 파일들 찾기"""
        return list(self.project_root.glob(f"planning/specs/**/{self.ticket_num}*.md"))

    def print_result(self, result: ValidationResult):
        """결과 출력"""
        print(f"\n{'='*60}")

        if result.passed:
            print(f"✅ Spec Validation 통과: {self.ticket_num}")
        else:
            print(f"❌ Spec Validation 실패: {self.ticket_num}")

        print(f"{'='*60}\n")

        # 에러
        if result.errors:
            print(f"에러 ({len(result.errors)}개):")
            for i, err in enumerate(result.errors, 1):
                print(f"{i}. {err}")
            print()

        # 경고
        if result.warnings:
            print(f"경고 ({len(result.warnings)}개):")
            for i, warn in enumerate(result.warnings, 1):
                print(f"{i}. {warn}")
            print()

        # 자동 수정
        if result.auto_fixes:
            print(f"자동 수정 ({len(result.auto_fixes)}개):")
            for i, fix in enumerate(result.auto_fixes, 1):
                print(f"✓ {fix}")
            print()

        # 다음 조치
        print("다음 조치:")
        if result.passed:
            print("Coding Agent 실행 가능")
        else:
            print("1. PM Agent 재실행하여 누락된 파일/섹션 생성")
            print("2. 에러 수정 후 재검증 필요")

        print()

    def save_log(self, result: ValidationResult):
        """검증 로그 저장"""
        log_dir = self.project_root / "logs" / "validate-spec"
        log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file = log_dir / f"{timestamp}-{self.ticket_num}.md"

        status = "✅ 통과" if result.passed else "❌ 실패"

        log_content = f"""# Spec Validation Log: {self.ticket_num}

- **Skill**: validate-spec
- **프로젝트**: {self.project_root.name}
- **티켓**: {self.ticket_num}
- **일시**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **결과**: {status}

---

## 검증 결과

### 완전성
"""

        if "completeness" in result.details:
            found = result.details["completeness"]["found"]
            missing = result.details["completeness"]["missing"]
            log_content += f"- ✅ {len(found)}/{len(found) + len(missing)} 파일 생성 완료\n"
            if missing:
                log_content += f"- ❌ 누락: {', '.join(missing)}\n"

        log_content += "\n### 범위 준수\n"
        if "scope_compliance" in result.details:
            scope_creep = result.details["scope_compliance"]["scope_creep"]
            if scope_creep:
                log_content += f"- ⚠️  {len(scope_creep)}개 범위 확대 의심 키워드 발견\n"
                for keyword, file_name in scope_creep:
                    log_content += f"  - '{keyword}' in {file_name}\n"
            else:
                log_content += "- ✅ 범위 확대 없음\n"

        log_content += "\n### 품질 게이트\n"
        log_content += "- API 에러 응답, HTML 규칙 등 검증 완료\n"

        log_content += "\n### 구현 세부사항\n"
        if "implementation_details" in result.details:
            violations = result.details["implementation_details"]
            if violations:
                log_content += f"- ⚠️  {len(violations)}개 구현 세부사항 키워드 발견\n"
            else:
                log_content += "- ✅ 침범 없음\n"

        log_content += "\n---\n\n## 이슈 상세\n\n"

        if result.errors:
            log_content += "### 에러\n\n"
            for err in result.errors:
                log_content += f"- {err}\n"
            log_content += "\n"

        if result.warnings:
            log_content += "### 경고\n\n"
            for warn in result.warnings:
                log_content += f"- {warn}\n"
            log_content += "\n"

        if result.auto_fixes:
            log_content += "### 자동 수정\n\n"
            for fix in result.auto_fixes:
                log_content += f"- ✓ {fix}\n"
            log_content += "\n"

        log_content += "---\n\n## 다음 조치\n\n"
        if result.passed:
            log_content += "Coding Agent 실행 가능\n"
        else:
            log_content += "PM Agent 재실행 또는 수동 수정 필요\n"

        log_file.write_text(log_content, encoding='utf-8')
        print(f"📝 로그 저장: {log_file}")


def main():
    """메인 실행"""
    if len(sys.argv) < 2:
        print("Usage: python validate.py PLAN-001 [--auto-fix]")
        sys.exit(1)

    ticket_num = sys.argv[1]
    auto_fix = "--auto-fix" in sys.argv

    # 프로젝트 루트 찾기 (현재 위치에서 상위로 탐색)
    current = Path.cwd()
    project_root = None

    # team/scripts에서 실행 시 → 프로젝트 루트 찾기
    while current != current.parent:
        if (current / ".project-meta.json").exists() or (current / "planning").exists():
            project_root = current
            break
        current = current.parent

    if not project_root:
        print("❌ 프로젝트 루트를 찾을 수 없습니다 (.project-meta.json 또는 planning/ 디렉토리)")
        sys.exit(1)

    # 검증 실행
    validator = SpecValidator(project_root, ticket_num)
    result = validator.validate(auto_fix=auto_fix)

    # 결과 출력
    validator.print_result(result)
    validator.save_log(result)

    # Exit code
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
