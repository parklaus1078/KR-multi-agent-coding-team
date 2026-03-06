# Frontend Test Cases Directory

Write UI test cases in `.md` format and place them in this folder.

## File Naming Convention
`{screen-name}-test-cases.md`

## Recommended Test Case Structure
```markdown
# {Screen Name} UI Test Cases

## TC-FE-001: User List Normal Loading
- **Target Component**: UserListPage
- **Mock API**: GET /api/v1/users → 200 (returns 3 users)
- **Expected**: 3 user names displayed on screen
- **Case Type**: Happy Path

## TC-FE-002: Error Message on API Failure
- **Target Component**: UserListPage
- **Mock API**: GET /api/v1/users → 500
- **Expected**: "Failed to load data" text displayed
- **Case Type**: Error
```
