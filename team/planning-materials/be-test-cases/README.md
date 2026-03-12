# 백엔드 테스트 케이스 디렉토리

API 테스트 케이스를 `.md` 형식으로 작성하여 이 폴더에 배치하세요.

## 파일 네이밍 규칙
`{티켓번호}-{{도메인명}-test-cases.md`
예시: `PROJ-123-user-test-cases.md`

## 권장 테스트 케이스 구조
```markdown
# {도메인} API 테스트 케이스

## TC-001: 정상적인 유저 조회
- **대상 API**: GET /api/v1/users/{id}
- **전제 조건**: id=1인 유저가 DB에 존재
- **입력**: user_id = 1
- **기댓값**: status 200, data.id == 1
- **케이스 유형**: Happy Path

## TC-002: 존재하지 않는 유저 조회
- **대상 API**: GET /api/v1/users/{id}
- **입력**: user_id = 99999
- **기댓값**: status 404, error.code == "USER_NOT_FOUND"
- **케이스 유형**: Error
```
