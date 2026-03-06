# API 명세서 디렉토리

Notion에서 작성한 API 명세서를 `.md` 형식으로 export하여 이 폴더에 배치하세요.

## 파일 네이밍 규칙
`{티켓번호}-{도메인명(feature-slug)}-api-spec.md`
예시: `PROJ-123-user-api-spec.md`, `PROJ-123-product-api-spec.md`

## 권장 명세서 구조
각 파일은 아래 구조를 포함하면 BE Coding Agent가 더 정확하게 파싱합니다:

```markdown
# {도메인} API 명세서

## 엔드포인트 목록

### GET /api/v1/{resource}/{id}
- **설명**: ...
- **인증 필요**: Yes/No
- **권한(RBAC Role)**: ...
- **Path Params**: ...
- **Query Params**: ...
- **Request Body**: ...
- **Response (200)**: ...
- **Response (4xx)**: ...
```
