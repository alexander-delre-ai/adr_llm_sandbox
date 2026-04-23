---
name: kata-sprint-ticket-factory
description: Creates multiple KATA JIRA tickets for an upcoming sprint. Mandatory fields are release, sprint, and assignee. Infers ticket title and description from context. Suggests epics from active (In Progress or Backlog) Virtual Toolchain and SDV SW initiative epics, then confirms with the user before creating.
---

# KATA Sprint Ticket Factory

Creates a batch of KATA JIRA tasks for an upcoming sprint. Built on top of `jira-task-creation-KATA`.

## Mandatory fields (apply to all tickets in the batch)

- `release` - target release (e.g. `25.3`, `26.1`)
- `sprint` - sprint name as it appears in JIRA (e.g. `SDV Sprint 1`)
- `assignee` - team member name or handle (can be per-ticket)

## Per-ticket fields

- `title` - inferred from the provided description/context if not explicit
- `description` - inferred from context; omit if insufficient information
- `priority` - default `P1`
- `epic` - suggested from the active epic list below; confirmed with user before creation

---

## Active Epic Mapping

Only suggest epics from this list (status: In Progress or Backlog). Never suggest epics with status Complete, Done, or Rejected.

### Virtual Toolchain (KATA-15)

| Epic | Title | Status |
|------|-------|--------|
| KATA-379 | [VT] Development environment setup | In Progress |
| KATA-797 | [VT] Development of vehicle dynamics model for 930E | In Progress |
| KATA-1686 | [VT] Onboard FADC users onto ADP + SDV platforms | In Progress |
| KATA-1687 | [VT] Execute Level 1 stack/developer tooling with Katana users | In Progress |
| KATA-1688 | [VT] Execute Level 2 training for vehicle integration team | In Progress |
| KATA-1689 | [VT] Create vehicle asset import pipeline | In Progress |
| KATA-1692 | [VT] Establish training certification track for Komatsu ADP users | In Progress |
| KATA-2155 | [VT] EMERST Scenario creation | In Progress |
| KATA-2322 | [VT] ADP Feature Support | In Progress |

### SDV SW (KATA-1760)

| Epic | Title | Status |
|------|-------|--------|
| KATA-127 | Application SW Development Planning | In Progress |
| KATA-726 | VehicleOS SW Development | In Progress |
| KATA-1032 | UI/UX R&D | In Progress |
| KATA-1912 | Exterior Lights SW Integration & Development | In Progress |
| KATA-2162 | [SDV][SW] Application development: Exterior Lighting Reference | Backlog |
| KATA-2226 | [SDV][SW] Documentation and reference updates | Backlog |
| KATA-2543 | Data Logging Strategy | Backlog |
| KATA-2544 | OTA (Over-the-Air Update) Strategy | Backlog |
| KATA-2561 | Payload meter application development | Backlog |
| KATA-2608 | Cybersecurity Strategy | Backlog |
| KATA-2611 | Auto Lube Development | Backlog |
| KATA-2624 | Engine Interface (CAN) Development | Backlog |
| KATA-2636 | Low Voltage Power Development | Backlog |
| KATA-2648 | Chassis Brakes Development | Backlog |
| KATA-2660 | Shutdown Processes Development | Backlog |
| KATA-2661 | Drive System Interface Development | Backlog |
| KATA-2662 | Cab Components Development | Backlog |
| KATA-2663 | Operator Displays Development | Backlog |
| KATA-2708 | Hoist Development | Backlog |
| KATA-2709 | HMU Development | Backlog |
| KATA-2710 | Payload Meter Development | Backlog |
| KATA-2744 | Enhanced Brake Development | Backlog |
| KATA-2745 | Enhanced Steering Development | Backlog |
| KATA-2746 | Powered Ladder Development | Backlog |
| KATA-2747 | Lights & Accessories Development | Backlog |
| KATA-2748 | HVAC Development | Backlog |
| KATA-2749 | Wipers Development | Backlog |
| KATA-2750 | Autonomous Interface Development | Backlog |
| KATA-2751 | GPS Interface Development | Backlog |
| KATA-2752 | Authentication Development | Backlog |
| KATA-2753 | Infotainment UI Development | Backlog |
| KATA-2754 | Machine Intervention Controller (MIC) Development | Backlog |

**Note**: This mapping may go stale. Before each use, refresh with:
- `parent = KATA-15 AND statusCategory not in (Done) AND status != Rejected ORDER BY key ASC`
- `parent = KATA-1760 AND statusCategory not in (Done) AND status != Rejected ORDER BY key ASC`

If the live data differs from the table, use the live data.

---

## Workflow

### Step 1 - Parse tickets from input

Extract each ticket from the user's prompt. For each item:
- Infer a short imperative title (10-255 characters) if not explicitly provided
- Infer a brief description from the context if available; otherwise omit
- Record the assignee (@mention or name); use the batch-level assignee if not per-ticket
- Record priority if specified; default to P1

### Step 2 - Resolve sprint ID

1. Run JQL: `project = KATA AND sprint = "<sprint_name>" ORDER BY created DESC` with `maxResults: 1` and `fields: ["customfield_10020"]`
2. Extract `customfield_10020[0].id` (integer) from the result
3. If not found, try `sprint in openSprints()` and match by name
4. If still not found: warn the user, list available open/future sprints, and ask them to confirm the exact sprint name. Do NOT create any tickets until the sprint ID is resolved.

### Step 3 - MANDATORY REVIEW: Present proposed tickets for user confirmation

**Do not create any tickets until this step is explicitly approved by the user.**

Present a complete review table covering every proposed ticket:

| # | Title | Description | Epic | Assignee | Priority | Release | Sprint |
|---|-------|-------------|------|----------|----------|---------|--------|

Below the table, explicitly ask:
> "Please review and confirm or correct these ticket and epic assignments before I proceed with creation."

Wait for an explicit approval or correction response. If the user corrects any field (title, epic, assignee, description), update the table and re-present for final confirmation before creating anything.

Do not proceed to Step 4 until the user has given clear approval.

### Step 4 - Create tickets

Only execute this step after user approval in Step 3.

Look up account IDs for all unique assignees in parallel via `mcp__kata-atlassian__lookupJiraAccountId` (cloudId: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`).

Then create each ticket via `mcp__kata-atlassian__createJiraIssue`:

```
cloudId:             "eadd00c6-0d3f-4c89-99e3-ad95a0daaa51"
projectKey:          "KATA"
issueTypeName:       "Task"
summary:             <title>
description:         <plain prose - see formatting rules below>
contentFormat:       "markdown"
assignee_account_id: <from lookup>
additional_fields:
  priority:           {"name": "P1"}
  parent:             {"key": "<epic_key>"}
  customfield_10104:  {"id": "<release_id>"}
  customfield_10020:  {"id": <sprint_id>}    <- integer, not string
  customfield_10137:  0
```

Create all tickets in parallel where possible (after account ID lookups complete).

### Step 5 - Summary

Output a results table:

| Ticket | Title | Epic | Assignee |
|--------|-------|------|----------|

Note any failures or fields that could not be set.

---

## Release Mapping

| Release | customfield_10104 id |
|---------|----------------------|
| 25.1 | 10000 |
| 25.2 | 10001 |
| 25.3 | 10036 |
| 26.1 | 10002 |
| 26.2 | 10003 |

---

## Description Formatting Rules

**CRITICAL - prevents garbled output in JIRA:**

- Write descriptions as plain readable prose
- Do NOT use `\n` escape sequences - they render as literal characters in JIRA
- Write as a single sentence or short paragraph; use real paragraph breaks if multi-line
- Append "Created via JIRA MCP" as the final sentence
- Always set `contentFormat: "markdown"` on every `createJiraIssue` call
