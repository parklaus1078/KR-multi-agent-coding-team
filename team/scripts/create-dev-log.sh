#!/bin/bash
# 에이전트 시스템 개발 로그 생성 스크립트

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
LOGS_DIR="$WORKSPACE_ROOT/../logs-agent_dev"

TOPIC="$1"

if [[ -z "$TOPIC" ]]; then
    echo ""
    echo "사용법: bash scripts/create-dev-log.sh <주제>"
    echo ""
    echo "예시:"
    echo "  bash scripts/create-dev-log.sh git-branch-automation"
    echo "  bash scripts/create-dev-log.sh rate-limit-optimization"
    echo "  bash scripts/create-dev-log.sh new-agent-implementation"
    echo ""
    exit 1
fi

DATE=$(date +%Y%m%d)
FILENAME="$LOGS_DIR/${DATE}-${TOPIC}.md"

# 로그 디렉토리가 없으면 생성
if [[ ! -d "$LOGS_DIR" ]]; then
    mkdir -p "$LOGS_DIR"
    echo "📁 logs-agent_dev/ 디렉토리 생성됨"
fi

# 파일이 이미 존재하면 경고
if [[ -f "$FILENAME" ]]; then
    echo "⚠️  파일이 이미 존재합니다: $FILENAME"
    echo "   덮어쓰시겠습니까? (y/N)"
    read -r CONFIRM
    if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
        echo "❌ 취소되었습니다."
        exit 0
    fi
fi

# 템플릿 생성
cat > "$FILENAME" <<EOF
# [${DATE}] ${TOPIC}

## 개요

{무엇을 개선했는지 2-3줄 요약}

## 문제점

{기존에 어떤 문제가 있었는지}

## 해결 방법

### 1. {방법 1}

{설명}

### 2. {방법 2}

{설명}

## 변경된 파일

### KR 버전
- \`path/to/file1.md\` - {변경 내용}
- \`path/to/file2.sh\` - {변경 내용}

### ENG 버전
- \`path/to/file1.md\` - {변경 내용}

## 새로 생성된 파일

### KR 버전
- \`path/to/new-file.json\` - {목적}

### ENG 버전
- \`path/to/new-file.json\` - {목적}

## 사용 예시

\`\`\`bash
# 예시 명령어
\`\`\`

## 동작 흐름

\`\`\`
1. {단계 1}
   ↓
2. {단계 2}
   ↓
3. {단계 3}
\`\`\`

## 영향 범위

- [ ] KR 버전 (\`KR-multi-agent-coding-team/\`)
- [ ] ENG 버전 (\`ENG-multi-agent-coding-team/\`)
- [ ] 호환성: {기존 사용자에게 영향 여부}

## 테스트 체크리스트

- [ ] {테스트 항목 1}
- [ ] {테스트 항목 2}
- [ ] {테스트 항목 3}
- [ ] 실제 프로젝트에서 에이전트 실행 테스트 (사용자)

## 관련 이슈/요청

**사용자 요청:**
> {요청 내용}

**GitHub Issue:**
- #{이슈 번호}

## 참고 문서

- \`path/to/doc.md\` - {설명}

## 주요 설정 (있는 경우)

\`\`\`json
{
  "key": "value"
}
\`\`\`

## 향후 개선 계획

- [ ] {개선 항목 1}
- [ ] {개선 항목 2}

## 알려진 제한사항

1. **{제한사항 1}**: {설명}
2. **{제한사항 2}**: {설명}

## 노트

- {추가 메모 1}
- {추가 메모 2}
EOF

echo ""
echo "✅ 개발 로그 템플릿 생성 완료!"
echo ""
echo "📄 파일: $FILENAME"
echo ""
echo "다음 단계:"
echo "  1. 에디터에서 파일을 열어 내용을 작성하세요."
echo "  2. 작성 완료 후 Git에 커밋하세요."
echo ""
echo "  code \"$FILENAME\""
echo ""
