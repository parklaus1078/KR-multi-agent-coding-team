# Multi-Agent Development Workflow

A Claude Code-based multi-agent system that automates the full development cycle — from Jira ticket to implemented and tested code.

---

## Overview

You write a Jira ticket(or any ticket based task). The agents handle the rest.

```
Jira Ticket       - Ticket Number, Title, Domain Name, Description, etc.
    ↓
PM Agent          — API spec, UI wireframe, test cases (draft)
    ↓
Human Review      — inspect and edit all generated artifacts
    ↓
BE Coding Agent   — FastAPI implementation
FE Coding Agent   — Next.js / React implementation
    ↓
QA-BE Agent       — pytest test suite
QA-FE Agent       — Vitest / Jest test suite
    ↓
Human Review
```

Each agent writes an implementation log explaining every decision it made. Nothing is a black box.

---

## Agents

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| `pm` | Requirements authoring | Jira ticket exported in `.md` | API spec, UI spec, wireframe HTML, test cases |
| `be-coding` | Backend scaffolding | API spec | FastAPI routes, services, repositories |
| `fe-coding` | Frontend scaffolding | UI spec + wireframe + API spec | Next.js pages, components, hooks |
| `qa-be` | Backend test authoring | BE test cases + implemented code | pytest test suite |
| `qa-fe` | Frontend test authoring | FE test cases + implemented code | Vitest / Jest test suite |

---

## Project Structure

```
Workspace/
├── .agents/                        # Agent instruction files
│   ├── pm/CLAUDE.md
│   ├── be-coding/CLAUDE.md
│   ├── fe-coding/CLAUDE.md
│   ├── qa-be/CLAUDE.md
│   └── qa-fe/CLAUDE.md
│
├── .rules/                         # Coding standards (referenced by agents)
│   ├── be-coding-rules.md
│   └── fe-coding-rules.md
│
├── scripts/                        # Utility scripts
│   ├── run-agent.sh                # Agent launcher
│   ├── rate-limit-check.sh         # Claude Max rate limit check
│   ├── parse_usage.py              # Usage tracking
│   └── show-logs.sh                # View implementation logs
│
├── tickets/                        # Jira ticket exports
│   └── PROJ-123.md
│
├── be-api-requirements/            # API specs (PM Agent output)
│   └── PROJ-123-user-login.md
│
├── fe-ui-requirements/             # UI specs and wireframes (PM Agent output)
│   ├── PROJ-123-login-ui-spec.md
│   └── PROJ-123-login-wireframe.html
│
├── be-test-cases/                  # BE test cases (PM Agent output)
│   └── PROJ-123-user-login.md
│
├── fe-test-cases/                  # FE test cases (PM Agent output)
│   └── PROJ-123-user-login.md
│
├── logs/                           # Implementation logs (agent output)
│   ├── pm/
│   ├── be-coding/
│   ├── fe-coding/
│   ├── qa-be/
│   └── qa-fe/
│
├── be-project/                     # FastAPI backend
└── fe-project/                     # Next.js frontend
```

---

## Prerequisites

- [Claude Code](https://docs.claude.ai/claude-code) installed and authenticated
- Python 3 (for rate limit tracking)
- Claude Max plan (5x usage tier)

---

## Usage

### 1. Export Jira ticket as Markdown

Export your Jira ticket (Title, Description, Comments) as a `.md` file and place it in `tickets/`.

```
tickets/PROJ-123.md
```

### 2. Run PM Agent

```bash
bash scripts/run-agent.sh pm --ticket-file ./tickets/PROJ-123.md
```

The PM Agent will generate all requirement artifacts and ask for your approval before writing any files.

**Review the outputs:**
- `be-api-requirements/PROJ-123-*.md` — API spec
- `fe-ui-requirements/PROJ-123-*.md` — UI spec
- `fe-ui-requirements/PROJ-123-*.html` — Wireframe (open in browser to inspect interactions)
- `be-test-cases/PROJ-123-*.md` — BE test cases
- `fe-test-cases/PROJ-123-*.md` — FE test cases

Edit any file as needed before proceeding.

### 3. Run Coding Agents

```bash
bash scripts/run-agent.sh be-coding --ticket PROJ-123
bash scripts/run-agent.sh fe-coding --ticket PROJ-123
```

Each agent will present an implementation plan for your approval before writing any code.

### 4. Run QA Agents

```bash
bash scripts/run-agent.sh qa-be --ticket PROJ-123
bash scripts/run-agent.sh qa-fe --ticket PROJ-123
```

### 5. View Logs

```bash
bash scripts/show-logs.sh          # All agents
bash scripts/show-logs.sh be-coding  # Specific agent
```

---

## Wireframe HTML Convention

PM Agent generates interactive wireframes for screens with user flows.

**Static HTML** — for simple display screens with no state transitions.

**Interactive HTML** — for screens with:
- Form submission and page transitions
- Success / failure state display
- Modals, toasts, drawers
- Tabs, steps, or wizards

Interactive wireframes use vanilla JS only (no frameworks, no external libraries). Each state is represented as a `div` with `id="state-{name}"`, toggled via `display:none/block`. API calls are simulated — no real `fetch` calls.

FE Coding Agent reads these wireframes to map states to React `useState` and router transitions.

---

## File Naming Convention

All artifacts are prefixed with the Jira ticket number to prevent cross-ticket confusion.

```
{ticket-number}-{feature-slug}.{ext}

Examples:
  PROJ-123-user-login.md
  PROJ-123-user-login.html
  PROJ-124-product-list.md
```

---

## Rate Limit Handling

This system is designed for **Claude Max 5x** (5-hour rolling window).

Every agent runs `rate-limit-check.sh` before starting work:

| Result | Action |
|--------|--------|
| ✅ Available | Proceed |
| ⚠️ Warning (≥35 calls) | Notify user, proceed with approval |
| 🛑 Stop (≥45 calls) | Halt, show estimated reset time |

To check current usage manually:

```bash
bash scripts/rate-limit-check.sh
```

Thresholds can be adjusted in `scripts/parse_usage.py`:
```python
WARN_THRESHOLD = 35
STOP_THRESHOLD = 45
```

---

## Coding Standards

Agents do not have coding rules embedded in their `CLAUDE.md` files. All standards are delegated to:

- `.rules/be-coding-rules.md` — FastAPI / Python / PostgreSQL standards
- `.rules/fe-coding-rules.md` — Next.js / React / TypeScript standards

This separation means you can update coding rules without touching agent workflow instructions.

---

## Implementation Logs

Every agent writes a log immediately after completing work. Logs include:

- Files created or modified
- Key decisions made (e.g. Server vs Client Component, data fetching strategy)
- Alternative approaches considered and trade-offs
- Notes for the reviewer

Logs are stored in `logs/{agent-name}/` and named with a timestamp and ticket number:

```
logs/fe-coding/20250306-143022-PROJ-123-user-login.md
```