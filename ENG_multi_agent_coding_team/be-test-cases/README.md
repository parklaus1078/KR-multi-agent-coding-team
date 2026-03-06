# Backend Test Cases Directory

Write API test cases in `.md` format and place them in this folder.

## File Naming Convention
`{domain-name}-test-cases.md`
Examples: `user-test-cases.md`

## Recommended Test Case Structure
```markdown
# {Domain} API Test Cases

## TC-001: Normal User Retrieval
- **Target API**: GET /api/v1/users/{id}
- **Precondition**: User with id=1 exists in DB
- **Input**: user_id = 1
- **Expected**: status 200, data.id == 1
- **Case Type**: Happy Path

## TC-002: Non-existent User Retrieval
- **Target API**: GET /api/v1/users/{id}
- **Input**: user_id = 99999
- **Expected**: status 404, error.code == "USER_NOT_FOUND"
- **Case Type**: Error
```
