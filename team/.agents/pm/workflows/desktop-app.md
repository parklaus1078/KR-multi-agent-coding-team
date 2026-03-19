# Desktop App 워크플로우

> **프로젝트 타입**: desktop-app (예: Tauri + React, Electron, Qt)
>
> **적용 조건**: `.project-meta.json`의 `project_type`이 `"desktop-app"`인 경우

---

## 📂 산출물 구조

```
projects/{current_project}/planning/specs/
├── screens/
│   ├── PLAN-{번호}-{slug}.md          # 화면 요구사항
│   └── PLAN-{번호}-{slug}.html        # 와이어프레임
├── state/
│   └── PLAN-{번호}-{slug}.md          # 상태 관리 명세
├── ipc/
│   └── PLAN-{번호}-{slug}.md          # IPC 통신 명세 (필요 시)
└── test-cases/
    ├── PLAN-{번호}-unit.md            # 단위 테스트
    ├── PLAN-{번호}-integration.md     # 통합 테스트
    └── PLAN-{번호}-e2e.md             # E2E 테스트
```

---

## 🔨 작업 순서

### Step 1: 티켓 분석

티켓에서 다음 항목을 추출:
- [ ] 화면/윈도우 (메인 윈도우, 설정 다이얼로그 등)
- [ ] 사용자 인터랙션 (버튼 클릭, 드래그 앤 드롭 등)
- [ ] 상태 관리 (전역 상태, 로컬 상태)
- [ ] 백엔드 통신 (IPC, File I/O, 네트워크)

---

### Step 2: 산출물 목록 제시

```
프로젝트: {current_project} (desktop-app)
티켓: PLAN-{번호}-{slug}

생성 예정 파일:
- specs/screens/PLAN-{번호}-{slug}.md
- specs/screens/PLAN-{번호}-{slug}.html
- specs/state/PLAN-{번호}-{slug}.md
- specs/ipc/PLAN-{번호}-{slug}.md (필요 시)
- specs/test-cases/PLAN-{번호}-unit.md
- specs/test-cases/PLAN-{번호}-integration.md
- specs/test-cases/PLAN-{번호}-e2e.md

주요 화면: 메인 윈도우, 설정 다이얼로그
주요 상태: 파일 목록, 현재 선택 항목
IPC 통신: 파일 열기, 파일 저장

계속 진행하시겠습니까? (yes/no)
```

---

### Step 3-1: 화면 요구사항

**파일**: `specs/screens/PLAN-{번호}-{slug}.md`

```markdown
# {화면명} 요구사항

## 화면 정보
- **타입**: 메인 윈도우 / 다이얼로그 / 모달
- **크기**: 800x600 (최소), 리사이즈 가능 / 고정
- **위치**: 중앙 / 이전 위치 복원

## 레이아웃 구성
- 헤더: 타이틀, 최소화/최대화/닫기 버튼
- 사이드바: 파일 목록
- 메인 영역: 에디터
- 푸터: 상태 표시줄

## 컴포넌트 목록

### 파일 목록 (사이드바)
- 파일 트리 뷰
- 컨텍스트 메뉴 (우클릭)
- 드래그 앤 드롭 지원

### 에디터 (메인 영역)
- 텍스트 입력
- 구문 강조
- 자동 저장 표시

## 키보드 단축키
| 단축키 | 동작 |
|--------|------|
| Ctrl+O | 파일 열기 |
| Ctrl+S | 파일 저장 |
| Ctrl+W | 윈도우 닫기 |

## 윈도우 이벤트
| 이벤트 | 동작 |
|--------|------|
| 윈도우 닫기 | 저장 안 된 변경 확인 → 저장 여부 묻기 |
| 리사이즈 | 레이아웃 재조정, 크기 저장 |
| 포커스 상실 | 자동 저장 (설정 시) |
```

---

### Step 3-2: 와이어프레임

**파일**: `specs/screens/PLAN-{번호}-{slug}.html`

Desktop App도 Web-Fullstack과 동일하게 바닐라 HTML로 작성:
- 외부 라이브러리 금지
- 구조만 표현
- 상태 전환 시뮬레이션

---

### Step 3-3: 상태 관리 명세

**파일**: `specs/state/PLAN-{번호}-{slug}.md`

```markdown
# {기능명} 상태 관리

## 상태 구조

\`\`\`typescript
interface AppState {
  files: FileItem[];
  selectedFile: FileItem | null;
  editorContent: string;
  isDirty: boolean;  // 저장 안 된 변경 여부
}
\`\`\`

## 상태 변경 시나리오

### 파일 열기
1. 초기 상태: `selectedFile = null`
2. 사용자 액션: 파일 목록에서 클릭
3. IPC 호출: `readFile(filePath)`
4. 상태 업데이트: `selectedFile = file, editorContent = content, isDirty = false`

### 내용 수정
1. 사용자 액션: 에디터에 입력
2. 상태 업데이트: `editorContent = newContent, isDirty = true`
3. UI 반영: 타이틀에 "*" 표시

## 상태 지속성
| 상태 | 저장 위치 | 시점 |
|------|----------|------|
| 윈도우 크기/위치 | 로컬 설정 파일 | 윈도우 닫기 시 |
| 최근 열린 파일 | 로컬 설정 파일 | 파일 열기 시 |
| 에디터 설정 | 로컬 설정 파일 | 변경 시 |
```

---

### Step 3-4: IPC 통신 명세 (필요 시)

**파일**: `specs/ipc/PLAN-{번호}-{slug}.md`

```markdown
# {기능명} IPC 통신

## IPC 메서드 목록

### readFile
- **방향**: Frontend → Backend
- **입력**: `{ filePath: string }`
- **출력**: `{ content: string, encoding: string }`
- **에러**: `FileNotFoundError`, `PermissionError`

### writeFile
- **방향**: Frontend → Backend
- **입력**: `{ filePath: string, content: string }`
- **출력**: `{ success: boolean }`
- **에러**: `WriteError`, `DiskFullError`

### watchFile
- **방향**: Frontend ← Backend (이벤트)
- **트리거**: 파일 시스템 변경 감지
- **데이터**: `{ filePath: string, changeType: 'modified' | 'deleted' }`
```

---

### Step 3-5: 테스트 케이스

**3개 파일 생성**:
- `test-cases/PLAN-{번호}-unit.md` - 컴포넌트 단위 테스트
- `test-cases/PLAN-{번호}-integration.md` - IPC 통신, 상태 관리 통합 테스트
- `test-cases/PLAN-{번호}-e2e.md` - 사용자 시나리오 E2E 테스트

---

## ✅ 완료 체크리스트

- [ ] 화면 요구사항 생성 (레이아웃, 컴포넌트)
- [ ] 와이어프레임 생성 (HTML)
- [ ] 상태 관리 명세 생성
- [ ] IPC 명세 생성 (백엔드 통신 있을 시)
- [ ] 3종 테스트 케이스 생성
- [ ] 키보드 단축키 정의
- [ ] 윈도우 이벤트 처리 정의
- [ ] 로그 파일 생성

---

**관련 문서**:
- [gotchas.md](../gotchas.md)
- [CLAUDE.md](../CLAUDE.md)
