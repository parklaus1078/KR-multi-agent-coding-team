#!/bin/bash
# 프로젝트 초기화 스크립트
#
# 사용법:
#   bash scripts/init-project.sh --interactive
#   bash scripts/init-project.sh --type cli-tool --language go --framework cobra --name my-cli

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECTS_DIR="$WORKSPACE_ROOT/projects"
CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"

# ── 기본값 ──────────────────────────────────────────────────────
PROJECT_TYPE=""
LANGUAGE=""
FRAMEWORK=""
VERSION="latest"
PROJECT_NAME=""
PROJECT_DESC=""
INTERACTIVE=false

# ── 플래그 파싱 ──────────────────────────────────────────────────
if [[ $# -eq 0 ]]; then
    INTERACTIVE=true
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --interactive)
            INTERACTIVE=true
            shift
            ;;
        --type)
            PROJECT_TYPE="$2"
            shift 2
            ;;
        --language)
            LANGUAGE="$2"
            shift 2
            ;;
        --framework)
            FRAMEWORK="$2"
            shift 2
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        --name)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --description)
            PROJECT_DESC="$2"
            shift 2
            ;;
        *)
            echo "❌ 알 수 없는 옵션: '$1'"
            echo ""
            echo "사용법:"
            echo "  bash scripts/init-project.sh --interactive"
            echo "  bash scripts/init-project.sh --type cli-tool --language go --framework cobra --name my-cli"
            echo ""
            echo "옵션:"
            echo "  --interactive       대화형 모드"
            echo "  --type             프로젝트 타입 (web-fullstack, web-mvc, cli-tool, desktop-app, mobile-app, library, data-pipeline)"
            echo "  --language         언어 (python, javascript, typescript, go, rust, java, etc.)"
            echo "  --framework        프레임워크 (fastapi, django, nextjs, cobra, etc.)"
            echo "  --version          프레임워크 버전 (기본: latest)"
            echo "  --name             프로젝트 이름"
            echo "  --description      프로젝트 설명"
            exit 1
            ;;
    esac
done

# ── 인터랙티브 모드 ─────────────────────────────────────────────
if [[ "$INTERACTIVE" == true ]]; then
    echo "╔══════════════════════════════════════════════╗"
    echo "║  멀티 에이전트 프로젝트 초기화              ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""

    # 프로젝트 타입 선택
    echo "1. 프로젝트 타입을 선택하세요:"
    echo "   1) web-fullstack     (FE + BE 분리)"
    echo "   2) web-mvc           (Django, Rails, Spring Boot MVC 등)"
    echo "   3) cli-tool          (CLI 도구)"
    echo "   4) desktop-app       (Electron, Tauri, Qt 등)"
    echo "   5) mobile-app        (React Native, Flutter 등)"
    echo "   6) library           (npm, pip 패키지 등)"
    echo "   7) data-pipeline     (Airflow, Prefect 등)"
    echo ""
    read -p "선택 (1-7): " TYPE_CHOICE

    case $TYPE_CHOICE in
        1) PROJECT_TYPE="web-fullstack" ;;
        2) PROJECT_TYPE="web-mvc" ;;
        3) PROJECT_TYPE="cli-tool" ;;
        4) PROJECT_TYPE="desktop-app" ;;
        5) PROJECT_TYPE="mobile-app" ;;
        6) PROJECT_TYPE="library" ;;
        7) PROJECT_TYPE="data-pipeline" ;;
        *) echo "❌ 잘못된 선택"; exit 1 ;;
    esac

    echo ""
    read -p "2. 프로젝트 이름: " PROJECT_NAME
    read -p "3. 언어를 입력하세요 (예: python, go, javascript): " LANGUAGE
    read -p "4. 프레임워크를 입력하세요 (예: fastapi, cobra, nextjs): " FRAMEWORK
    read -p "5. 프레임워크 버전 (기본: latest): " INPUT_VERSION
    if [[ -n "$INPUT_VERSION" ]]; then
        VERSION="$INPUT_VERSION"
    fi
    read -p "6. 프로젝트 설명 (선택): " PROJECT_DESC
fi

# ── 필수 값 검증 ────────────────────────────────────────────────
if [[ -z "$PROJECT_TYPE" ]] || [[ -z "$LANGUAGE" ]] || [[ -z "$FRAMEWORK" ]] || [[ -z "$PROJECT_NAME" ]]; then
    echo "❌ 필수 값이 누락되었습니다."
    echo "   --type, --language, --framework, --name 은 필수입니다."
    exit 1
fi

# 프로젝트 이름 유효성 검사 (영문, 숫자, 하이픈만 허용)
if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9-]+$ ]]; then
    echo "❌ 프로젝트 이름은 영문, 숫자, 하이픈(-)만 사용 가능합니다."
    exit 1
fi

PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"

# ── 기존 프로젝트 확인 ──────────────────────────────────────────
if [[ -d "$PROJECT_PATH" ]]; then
    echo ""
    echo "⚠️  이미 존재하는 프로젝트입니다: $PROJECT_NAME"
    read -p "덮어쓰시겠습니까? (yes/no): " OVERWRITE

    if [[ "$OVERWRITE" != "yes" ]]; then
        echo "❌ 초기화 취소"
        exit 0
    fi

    rm -rf "$PROJECT_PATH"
fi

# ── 프로젝트 디렉토리 생성 ─────────────────────────────────────
echo ""
echo "📝 프로젝트 디렉토리 생성 중: $PROJECT_PATH"
mkdir -p "$PROJECT_PATH"

# ── 프로젝트 메타데이터 생성 ──────────────────────────────────
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "📝 프로젝트 메타데이터 생성: .project-meta.json"

# web-fullstack의 경우 frontend/backend 추가 입력 받기
if [[ "$PROJECT_TYPE" == "web-fullstack" ]]; then
    if [[ "$INTERACTIVE" == true ]]; then
        echo ""
        echo "Frontend 설정:"
        read -p "  언어 (javascript/typescript): " FE_LANGUAGE
        read -p "  프레임워크 (nextjs, vite-react, nuxt 등): " FE_FRAMEWORK
        echo ""
        echo "Backend 설정:"
        echo "  언어: $LANGUAGE"
        echo "  프레임워크: $FRAMEWORK"
        read -p "  데이터베이스 (postgresql, mysql, mongodb 등): " DATABASE
    fi

    cat > "$PROJECT_PATH/.project-meta.json" <<EOF
{
  "project_name": "$PROJECT_NAME",
  "project_type": "$PROJECT_TYPE",
  "stack": {
    "type": "$PROJECT_TYPE",
    "backend": {
      "language": "$LANGUAGE",
      "framework": "$FRAMEWORK",
      "version": "$VERSION",
      "database": "${DATABASE:-postgresql}"
    },
    "frontend": {
      "language": "${FE_LANGUAGE:-typescript}",
      "framework": "${FE_FRAMEWORK:-nextjs}",
      "version": "latest"
    }
  },
  "project_description": "$PROJECT_DESC",
  "created_at": "$TIMESTAMP",
  "directory_structure": "$PROJECT_TYPE",
  "active": true
}
EOF
else
    # 다른 프로젝트 타입
    cat > "$PROJECT_PATH/.project-meta.json" <<EOF
{
  "project_name": "$PROJECT_NAME",
  "project_type": "$PROJECT_TYPE",
  "stack": {
    "type": "$PROJECT_TYPE",
    "language": "$LANGUAGE",
    "framework": "$FRAMEWORK",
    "version": "$VERSION"
  },
  "project_description": "$PROJECT_DESC",
  "created_at": "$TIMESTAMP",
  "directory_structure": "$PROJECT_TYPE",
  "active": true
}
EOF
fi

# ── planning/ 디렉토리 생성 (타입별 구조) ───────────────────────
echo "📁 planning/ 디렉토리 생성 중..."

mkdir -p "$PROJECT_PATH/planning/tickets"

case "$PROJECT_TYPE" in
    web-fullstack)
        mkdir -p "$PROJECT_PATH/planning/specs/backend"
        mkdir -p "$PROJECT_PATH/planning/specs/frontend"
        mkdir -p "$PROJECT_PATH/planning/test-cases/backend"
        mkdir -p "$PROJECT_PATH/planning/test-cases/frontend"
        ;;
    web-mvc)
        mkdir -p "$PROJECT_PATH/planning/specs/endpoints"
        mkdir -p "$PROJECT_PATH/planning/specs/templates"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
    cli-tool)
        mkdir -p "$PROJECT_PATH/planning/specs"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
    desktop-app)
        mkdir -p "$PROJECT_PATH/planning/specs/screens"
        mkdir -p "$PROJECT_PATH/planning/specs/state"
        mkdir -p "$PROJECT_PATH/planning/specs/ipc"
        mkdir -p "$PROJECT_PATH/planning/test-cases/unit"
        mkdir -p "$PROJECT_PATH/planning/test-cases/integration"
        mkdir -p "$PROJECT_PATH/planning/test-cases/e2e"
        ;;
    mobile-app)
        mkdir -p "$PROJECT_PATH/planning/specs/screens"
        mkdir -p "$PROJECT_PATH/planning/specs/navigation"
        mkdir -p "$PROJECT_PATH/planning/specs/state"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
    library)
        mkdir -p "$PROJECT_PATH/planning/specs/api"
        mkdir -p "$PROJECT_PATH/planning/specs/examples"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
    data-pipeline)
        mkdir -p "$PROJECT_PATH/planning/specs/dags"
        mkdir -p "$PROJECT_PATH/planning/specs/transforms"
        mkdir -p "$PROJECT_PATH/planning/specs/schedules"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
esac

# ── src/ 디렉토리 생성 (프레임워크별 초기 구조) ──────────────────
echo "📁 src/ 디렉토리 생성 중..."
mkdir -p "$PROJECT_PATH/src"

# 프레임워크별 초기 파일은 Stack Initializer Agent가 생성
# 여기서는 기본 디렉토리만 생성

# ── logs/ 디렉토리 생성 ────────────────────────────────────────
echo "📁 logs/ 디렉토리 생성 중..."
mkdir -p "$PROJECT_PATH/logs/stack-initializer"
mkdir -p "$PROJECT_PATH/logs/project-planner"
mkdir -p "$PROJECT_PATH/logs/pm"
mkdir -p "$PROJECT_PATH/logs/coding"
mkdir -p "$PROJECT_PATH/logs/qa"

# ── README.md 생성 ──────────────────────────────────────────────
echo "📝 README.md 생성 중..."
cat > "$PROJECT_PATH/README.md" <<EOF
# $PROJECT_NAME

$PROJECT_DESC

---

## 프로젝트 정보

- **타입**: $PROJECT_TYPE
- **언어**: $LANGUAGE
- **프레임워크**: $FRAMEWORK
- **생성일**: $TIMESTAMP

---

## 디렉토리 구조

\`\`\`
$PROJECT_NAME/
├── .project-meta.json          # 프로젝트 메타데이터
├── planning/                   # 기획 문서
│   ├── tickets/                # 티켓 파일
│   ├── specs/                  # 명세서
│   └── test-cases/             # 테스트 케이스
├── src/                        # 실제 코드
├── logs/                       # 에이전트 로그
└── README.md                   # 이 파일
\`\`\`

---

## 워크플로우

### 1. 티켓 생성

\`\`\`bash
cd team
bash scripts/run-agent.sh project-planner --project "프로젝트 설명"
\`\`\`

### 2. 명세서 생성

\`\`\`bash
bash scripts/run-agent.sh pm --ticket-file projects/$PROJECT_NAME/planning/tickets/PLAN-001-*.md
\`\`\`

### 3. 코딩

\`\`\`bash
bash scripts/run-agent.sh coding --ticket PLAN-001
\`\`\`

### 4. 테스트

\`\`\`bash
bash scripts/run-agent.sh qa --ticket PLAN-001
\`\`\`

---

## 로그 조회

\`\`\`bash
bash scripts/show-logs.sh
\`\`\`

---

**생성 일시**: $TIMESTAMP
EOF

# ── .project-config.json 업데이트 (현재 프로젝트로 설정) ─────────
echo "📝 .project-config.json 업데이트 중..."

cat > "$CONFIG_FILE" <<EOF
{
  "current_project": "$PROJECT_NAME",
  "current_project_path": "projects/$PROJECT_NAME",
  "recent_projects": ["$PROJECT_NAME"]
}
EOF

# ── 완료 메시지 ─────────────────────────────────────────────────
echo ""
echo "✅ 프로젝트 초기화 완료!"
echo ""
echo "📁 프로젝트 경로: $PROJECT_PATH"
echo "📊 프로젝트 타입: $PROJECT_TYPE"
echo "💻 언어/프레임워크: $LANGUAGE / $FRAMEWORK"
echo ""
echo "📋 생성된 디렉토리:"
echo "  - planning/tickets/       티켓 파일"
echo "  - planning/specs/         명세서"
echo "  - planning/test-cases/    테스트 케이스"
echo "  - src/                    소스 코드 (Stack Initializer가 구조 생성)"
echo "  - logs/                   에이전트 로그"
echo ""
echo "🚀 다음 단계:"
echo ""
echo "1. Stack Initializer 실행 (코딩 룰 생성 + 프로젝트 구조 초기화):"
echo "   bash scripts/run-agent.sh stack-initializer"
echo ""
echo "2. 티켓 생성:"
echo "   bash scripts/run-agent.sh project-planner --project \"프로젝트 설명\""
echo ""
echo "3. 명세서 생성:"
echo "   bash scripts/run-agent.sh pm --ticket-file projects/$PROJECT_NAME/planning/tickets/PLAN-001-*.md"
echo ""
echo "4. 코딩:"
echo "   bash scripts/run-agent.sh coding --ticket PLAN-001"
echo ""
echo "5. 테스트:"
echo "   bash scripts/run-agent.sh qa --ticket PLAN-001"
echo ""
