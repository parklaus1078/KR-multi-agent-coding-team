# API Specification Directory

Export API specifications written in Notion as `.md` files and place them in this folder.

## File Naming Convention
`{domain-name}-api-spec.md`
Examples: `user-api-spec.md`, `product-api-spec.md`

## Recommended Specification Structure
Including the following structure in each file helps the BE Coding Agent parse more accurately:

```markdown
# {Domain} API Specification

## Endpoint List

### GET /api/v1/{resource}/{id}
- **Description**: ...
- **Authentication Required**: Yes/No
- **Path Params**: ...
- **Query Params**: ...
- **Request Body**: ...
- **Response (200)**: ...
- **Response (4xx)**: ...
```
