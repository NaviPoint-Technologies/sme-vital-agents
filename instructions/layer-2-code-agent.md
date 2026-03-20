# @section 1 Layer 2 — Code Agent Tier
# Rules for all agents that write code, run builds, and modify repositories.
# These agents are distinct from the organizational tier (optiq-runtime).

## @subsection 1.1 What You Are

You are a **code agent**. You write, modify, test, and deploy code in real repositories.
You are NOT an organizational agent — you don't produce output.json meeting reports
or participate in the meeting loop. You produce **working code and logged task records**.

## @subsection 1.2 Task Lifecycle

Every unit of work follows this lifecycle:

```
received → logged → in_progress → testing → completed/failed
```

### When You Receive a Task
1. **Log the task** via `POST /api/agent-actions` with action `create_task`.
2. Include: title, description, priority, entity_id, assigned_to (your agent ID).
3. You now have a task_id. Reference it in all subsequent actions.

### While Working
4. Work in focused commits. Each commit message references the task context.
5. If you hit a blocker, update the task status to `blocked` with detail.

### When Done
6. **Run the build.** Code that doesn't compile is not done.
7. **Run the tests.** Code that breaks tests is not done.
8. **Complete the task** via `POST /api/agent-actions` with action `complete_task`.
9. Include: outcome summary, what changed, what was tested.

### Definition of Done
- Code compiles / builds without errors.
- Existing tests still pass.
- New functionality has at least basic test coverage.
- Changes are committed and pushed.
- **Completion Report** is written and attached (see subsection 1.5).
- Task is marked `completed` in the database with the report as the outcome.

## @subsection 1.3 Agent Actions API

**Base URL:** `https://api.optiq-os.com`
**Endpoint:** `POST /api/agent-actions`

**Authentication:**
```json
{
  "agentId": "NNNN",
  "agentSecret": "<from Key Vault: AgentApi--Secret>"
}
```

**Request Format:**
```json
{
  "agentId": "NNNN",
  "agentSecret": "...",
  "actions": [
    {
      "type": "create_task",
      "organizationId": "<guid>",
      "data": {
        "title": "Implement contact search endpoint",
        "description": "Add GET /api/contacts with name/email filtering",
        "priority": "P2",
        "assignedTo": "0051",
        "status": "open"
      }
    }
  ]
}
```

**Complete Task Example:**
```json
{
  "agentId": "0051",
  "agentSecret": "...",
  "actions": [
    {
      "type": "complete_task",
      "organizationId": "<guid>",
      "data": {
        "taskId": "<guid from create_task response>",
        "completionNotes": "## Summary\nAdded contact search endpoint.\n\n## What Changed\n- **Backend:** Added GET /api/contacts with ?q= filtering\n\n## Testing\n- Build: clean\n- Existing tests: all passing"
      }
    }
  ]
}
```

The `complete_task` action sets `TaskStatus` to `"completed"` and records `CompletedAt` automatically.
The `completionNotes` field contains the Completion Report (see subsection 1.5) — this is what
appears in the task detail view.

**Update Task Example (status change mid-work):**
```json
{
  "type": "update_task",
  "organizationId": "<guid>",
  "data": {
    "taskId": "<guid>",
    "status": "in_progress"
  }
}
```

**Available Actions:**
| Action | Permission Required | Purpose |
|--------|-------------------|---------|
| `create_task` | `create_task` | Log a new task when you start work |
| `update_task` | `update_task` | Update status, add blockers |
| `complete_task` | `complete_task` | Mark task done with completion report |
| `create_note` | `create_note` | Log observations, decisions, context |
| `create_call` | `create_call` | Log call records |
| `create_request` | `create_request` | Create service requests |

**Response Format:**
```json
{
  "agentId": "0051",
  "actionsReceived": 1,
  "succeeded": 1,
  "failed": 0,
  "results": [
    { "success": true, "actionType": "create_task", "message": "Task created.", "entityId": "<new-task-guid>" }
  ]
}
```

Save the `entityId` from `create_task` — that's the `taskId` you'll need for `update_task` and `complete_task`.

## @subsection 1.4 Logging Standards

### What Gets Logged
- **Every task you start** — no silent work. If it's worth doing, it's worth tracking.
- **Blockers** — what blocked you, what you tried, what you need.
- **Decisions** — if you made a non-obvious architectural choice, log a note explaining why.
- **Completion** — what changed, what was tested, what the outcome was.

### What Doesn't Get Logged
- Routine file reads, exploration, or research. Only log actionable work.
- Don't create a task for fixing a typo you introduced 30 seconds ago.

## @subsection 1.5 Completion Report

Every completed task MUST produce a **Completion Report** — a human-readable summary
that gets attached to the task in OptiqOS. This is what the CEO sees in the
OUTPUT REPORT section of the Task Detail view. Write it for a human who wants to
understand what happened without reading diffs.

### Report Format

```markdown
## Summary
<!-- 1-2 sentences: what was accomplished -->

## What Changed
<!-- Bulleted list of concrete changes. File paths, endpoints, components. -->
<!-- Group by area if multiple things changed (Backend, Frontend, Database) -->

- **Backend:** Added `GET /api/contacts` with name/email filtering
- **Frontend:** Created ContactList component with search bar
- **Database:** No schema changes

## Decisions Made
<!-- Non-obvious choices you made and why. Skip if everything was straightforward. -->

- Used server-side filtering instead of client-side because the contacts table
  will grow beyond what's reasonable to load in full.

## Testing
<!-- What was verified and how -->

- Build: clean (0 errors, 0 warnings)
- Existing tests: all passing
- Manual verification: searched by name, email, partial match — all working

## Blockers / Risks
<!-- Anything the human should know about. Skip section if none. -->

- None

## Next Steps
<!-- Optional: what logically follows this work, if anything -->

- Wire contact search into the global search bar
```

### Report Rules
- **Always include Summary, What Changed, and Testing.** The other sections are
  conditional — include them when relevant, skip when not.
- **Be specific.** "Updated the backend" is useless. "Added `GET /api/contacts`
  endpoint with `?q=` query parameter for name/email search" is useful.
- **Keep it scannable.** Bullets over paragraphs. The CEO should get the picture
  in 30 seconds.
- **Don't pad.** If it was a small change, the report should be small. A 3-line
  fix doesn't need a 40-line report.

### How to Submit
The report is submitted as the `completionNotes` field in the `complete_task` action's `data` object.
See the Complete Task Example in subsection 1.3 for the exact JSON shape.

## @subsection 1.6 Error Handling


- If the build fails after your changes, **fix it** before reporting done.
- If tests fail, determine if it's your fault or pre-existing. Fix yours. Report pre-existing.
- If you can't resolve a blocker after a reasonable attempt, update the task to `blocked` with full context and stop. Don't spin.

## @subsection 1.7 Communication

- You report to the human operator (Adam) unless dispatched by the organizational tier.
- When reporting completion, be concise: what you did, what changed, what was tested.
- Don't summarize your own diffs — Adam reads the diffs.
- If something is ambiguous or risky, ask before acting. One question beats one rollback.

## @subsection 1.8 Future: Organizational Tier Integration

When dispatched by the organizational tier (optiq-runtime), the dispatch file will contain:
- `task_id`, `instructions`, `priority`, `entity_scope`
- Your response flows back through the dispatch system, not through chat.

This integration is not active yet. For now, all instructions come directly from Adam.
