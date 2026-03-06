# UI Specification Directory

Write UI specifications in `.md` format and place them in this folder along with `.fig` files.

## File Naming Convention
- Text specification: `{screen-name}-ui-spec.md`
- Wireframe: `{screen-name}-wireframe.fig`

## Recommended UI Specification Structure
Since `.fig` files cannot be parsed directly, write the `.md` file as detailed as possible.

```markdown
# {Screen Name} UI Specification

## Screen Overview
- **Purpose**: ...
- **Connected API**: GET /api/v1/users/{id}

## Component Structure
### UserCard
- Display items: Name, Email, Join date
- On click: Navigate to /users/{id} page

## State Definitions
- Loading: Display skeleton UI
- Error: "Failed to load data" message + retry button
- Empty data: "No users" message
```
