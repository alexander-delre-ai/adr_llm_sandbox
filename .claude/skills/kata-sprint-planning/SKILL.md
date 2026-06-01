---
name: kata-sprint-planning
description: Plan a single upcoming KATA sprint for one Top-Level Initiative. Takes a sprint code (e.g., 2026.21) and a TLI key (e.g., KATA-1760), reviews what was completed in the prior sprint and how well it advanced the TLI's stated goals, proposes Eng Sprint v2 assignments for the next sprint, and applies changes to Jira after user review.
---

# KATA Sprint Planning (single sprint, single TLI)

Plans the next two-week sprint for one KATA Top-Level Initiative. Uses last sprint's completed work as a retro lens to check TLI alignment, then proposes what should land in the upcoming sprint by setting Eng Sprint v2 (`customfield_10103`) on candidate tasks.

## When to invoke

Trigger when the user says any of:
- "plan sprint 2026.XX for KATA-NNNN"
- "what should KATA-NNNN do next sprint"
- "sprint planning for <TLI summary>"

Do NOT invoke for:
- Multi-sprint / full-release planning (no longer supported by this skill).
- Bulk reassigning a hand-picked set of tickets (call `editJiraIssue` directly).
- AVP project planning.

## Required Inputs

The skill needs exactly two arguments. Ask for missing ones before doing anything else.

1. **Next sprint code** (e.g., `2026.21`). Must be one of the values listed in `release-sprint-map.json`. The "last sprint" is implicitly the prior odd-week code (e.g., `2026.21` → last `2026.19`).
2. **TLI key** (e.g., `KATA-1760`). Must be an issue of type `Top-level Initiative` in the KATA project. Listed in `../meeting-plan/kata-initiatives.json`.

Optional:
- **Inline goal additions**: free-text notes the user provides on TLI-level priorities for the upcoming sprint (e.g., "Komatsu wants Autolube validated by 2026.21"). Used during alignment scoring and gap proposals.

## Field IDs & Capacity Source

- **Eng Sprint v2**: `customfield_10103` (single-select). Option IDs in `release-sprint-map.json`.
- **Story Points v2**: `customfield_10137` (float; 1 pt = 1 week of one engineer).
- **Per-assignee capacity**: `capacity.json` in this skill directory. Default 1.6 pts/sprint. Supports `unavailable_sprints` for PTO.
- **Dependencies**: Jira `Blocks` / `is blocked by` issue links within KATA. Cross-project links ignored.

## Workflow

### Phase 1: Load context

1. Validate inputs:
   - Resolve next sprint code → option ID via `release-sprint-map.json`. Compute `last_sprint_code` = the immediately prior entry in that file.
   - Look up the TLI in `../meeting-plan/kata-initiatives.json` to get its summary, owner, and child epic list.
2. Fetch the TLI live via `mcp__kata-atlassian__getJiraIssue` (request `summary, description, status, assignee`). The description is the source of truth for stated TLI goals/outcomes. If empty, fall back to the TLI summary plus any inline goal additions the user provided.
3. Read `capacity.json`. Build the per-assignee capacity map for the upcoming sprint, subtracting any `unavailable_sprints` entries.

### Phase 2: Retro (what got done last sprint)

For every epic listed under the TLI:

```
parent = <epic_key> AND "Eng Sprint v2" = "<last_sprint_code>"
```

Request: `summary, status, assignee, customfield_10137, priority, resolutiondate`.

Categorize results:
- **Completed**: `statusCategory == Done` (Complete / Resolved). These are the retro signal.
- **Carried over**: still In Progress / Blocked / Todo. Will be candidates for the upcoming sprint.
- **Rejected / Won't Do**: note but do not score for alignment.

For each completed task:
- **Alignment score**: a one-line judgement of how well the task's summary matches the TLI description/goals. Three buckets:
  - `aligned` — task summary clearly advances a stated TLI outcome.
  - `partial` — task is within the TLI's scope but not in the stated near-term goals.
  - `drift` — task does not obviously advance the TLI; flag for the user to review.
- Use the TLI description + inline goal additions as the rubric. Do not be overly strict; this is a discussion prompt, not a grade.

Aggregate retro numbers:
- Total points completed last sprint vs. capacity used.
- % aligned / partial / drift by points.
- Per-assignee delivery: planned points vs. completed points last sprint.

### Phase 3: Propose next-sprint plan

Build the candidate pool:
- All Carried-over tasks from Phase 2.
- Tasks under the TLI's epics with no Eng Sprint v2 set (`customfield_10103 is EMPTY`) and `statusCategory != Done`. Run one JQL per epic or batch with `parent in (...)`.

Order candidates:
1. **Topological by `Blocks` links**: tasks blocking other in-scope tasks come first.
2. **Priority within ready frontier**: P0 → P3.
3. **Carryover bonus**: carried-over tasks slightly outrank fresh tasks at the same priority (finish what's already started).
4. **Size as final tiebreak**: larger points first for better packing.

Place candidates one at a time:
- For each candidate, check the assignee's remaining capacity for the upcoming sprint.
- Place if blockers are already scheduled (last sprint or this sprint) AND capacity is available.
- Skip if unestimated (`customfield_10137` is null) and add to `NEEDS-ESTIMATE`.
- If capacity exhausted before all high-priority work fits, add the rest to `DEFERRED` with reason.

Gap analysis (light, single-TLI scope):
- If a stated TLI goal has zero candidate work touching it, propose 1–3 stub tickets under the most relevant epic. Use the cross-TLI vocabulary table below.
- Story-point heuristics for stubs: 0.2 (doc/spec), 1.0 (validation plan, small integration), 2.0 (new component).

### Phase 4: Stage output for review

Write under `workspaces/2026.WW/YYYY-MM-DD/kata-{tli_key}-{next_sprint_code}/`:

#### `retro.md`

Sections:
1. **Header**: TLI key + summary, last sprint code, next sprint code, today's date.
2. **TLI goals (as understood)**: quote the TLI description + any inline goal additions the user supplied.
3. **Delivery summary**: total completed points, % aligned/partial/drift, per-assignee planned vs. completed.
4. **Completed tasks table**: `Task | Assignee | Points | Alignment | One-line judgement`.
5. **Carryover**: tasks that were assigned to last sprint but didn't finish, with status.
6. **Discussion prompts**: any `drift` items the user should weigh in on; assignees who under-delivered (completed < 50% of planned points).

#### `next-sprint-plan.md`

Sections:
1. **Header**: TLI, next sprint, total proposed points.
2. **Capacity bar chart** (ASCII) per assignee for the upcoming sprint:

   ```
   2026.21
     alexd     [#####.....]  1.0 / 1.6
     mahmouds  [########..]  1.6 / 1.6  FULL
     nicholas  [###.......]  0.6 / 1.6
   ```

3. **Proposed assignments table**: `Task | Assignee | Status | Points | Current Sprint | Proposed Sprint | Source | Notes`.
   - `Source` is either `Carryover`, `New from backlog`, or `Gap stub (proposed)`.
   - `Notes` flags `[BIG]` (>2 pt), `[BLOCKED]` (waiting on out-of-sprint work), or links to a stated goal.
4. **NEEDS-ESTIMATE**: candidate tasks with no Story Points v2. List separately; the user must estimate them before they can be planned next run.
5. **DEFERRED**: candidate tasks that didn't fit, with reason (capacity / blocked / unestimated).
6. **Mermaid Gantt**: each proposed task as a 1-sprint bar grouped by assignee.
7. **Verification JQL**: a snippet the user can paste into Jira to view exactly the tickets the skill will edit.

Display both files inline in the conversation so the user can scan without opening them.

### Phase 5: Apply (after explicit user review)

1. Print a single dry-run block listing every action:
   ```
   EDIT KATA-XXXX  Eng Sprint v2: <current or empty> -> 2026.21
   CREATE under KATA-EPIC: <title>  sprint=2026.21  points=0.2  priority=P1  assignee=<owner-or-Unassigned>
   ```
2. Wait for the user to type `apply` (or equivalent). Do not partial-apply on ambiguous input.
3. On apply:
   - `mcp__kata-atlassian__editJiraIssue` for each EDIT with `{ "customfield_10103": { "id": "<option_id>" } }`.
   - `mcp__kata-atlassian__createJiraIssue` for each CREATE (resolve assignee via `lookupJiraAccountId` if a real name is given).
   - After each call, append one line to `apply.log`: `<timestamp> <action> <key> <result>`.
   - If any call fails, stop the batch immediately, print the failure, and leave the rest unapplied.
4. After the batch, print summary counts and the path to `apply.log`. Do nothing else (no Slack, no TickTick).

## Cross-TLI Vocabulary (for gap stubs)

When proposing stub tickets in Phase 3, use the right vocabulary for the TLI:

| TLI | Common gap patterns |
|---|---|
| KATA-14 (Smart Machine Cloud) | RBAC, rollback, payload verification, OTA dashboards |
| KATA-11 (SDV-HW) | Mining safety analysis, HIL bench, K2/K4 compute |
| KATA-1760 (SDV-SW) | DTC modeling, fault injection, signal probes |
| KATA-10 (SVS) | DVR export, masking, HMI integration |
| KATA-15 (Virtual Toolchain) | Vehicle dynamics, asset import, CI/CD |
| KATA-1758 (Smart AHT Kit) | HIL bench, Raptor upfit, ODS test scenarios |
| KATA-1759 (Underground Exploration) | Data processing, ADP map creation |

## Conventions

- Sprints are 2-week cadence on odd ISO weeks: `2026.01, 2026.03, ..., 2026.45`. The "last sprint" is always the prior entry in `release-sprint-map.json`.
- Default priority for gap stubs: P1.
- Default assignee for gap stubs: TLI owner from `kata-initiatives.json`; else "Unassigned".
- Never set Eng Sprint v2 to a sprint other than the user-supplied target. Carryover tasks are explicitly re-assigned to the next sprint, not left on the prior one.
- One story point equals one week of work (per project CLAUDE.md).

## Output Conventions

- Speak in points, not days. (0.2 → "1 day", 0.5 → "2-3 days", 1 → "1 week", 2 → "1 sprint".)
- Capacity rendered as `used/total`.
- Tag tasks with `[BIG]` (>2 pt), `[BLOCKED]`, or `[EST]` (needs estimate) inline in tables.
- Always include the verification JQL in `next-sprint-plan.md`.
