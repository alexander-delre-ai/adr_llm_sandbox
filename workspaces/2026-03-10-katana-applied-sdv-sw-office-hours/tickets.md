# Action Items: Katana <> Applied: SDV SW Office Hours (Mar 10, 2026)

## Instructions

Edit the fields below as needed. When ready, confirm with the agent to create the action items.

**Field Guide:**

- **tracking**: "jira" (create JIRA ticket + include in Slack), "slack" (Slack summary only, no JIRA ticket), "both" (same as jira)
  - Auto-assigned: Items involving scheduling/meetings default to "slack", others to "jira"
- **priority**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- **assignee**: Single person responsible for the action item (one assignee per item) - defaults to "Unassigned"
- **parent_id**: Epic ID (KATA-XXXX or AVP-XXXX format) - defaults to "KATA-127" if not specified
- **release**: Target release - defaults to "Release 2026.1" if not specified. Can use short format (e.g., "2025.3" will become "Release 2025.3")
- **story_points**: 0.2 (1 day), 0.5 (2.5 days), 1 (1 week), 2 (2 weeks), 3 (3 weeks), 5 (5 weeks), 8 (8 weeks) - defaults to 0 if not specified
- **description**: Brief summary of the work

---

## Action Item 1: Meet with UI team about interface design

```yaml
tracking: slack
priority: P1
assignee: AlexD
parent_id: KATA-127
release: Release 2025.3
story_points: 0.1
description: Schedule and conduct meeting with UI team to discuss what the UI interface is going to look like. This addresses the gap in UI communications that prevents managers from being completed start to finish.
```

---

## Action Item 2: Conduct Auto Lube subsystem walkthrough for timeline estimation

```yaml
tracking: jira
priority: P1
assignee: Joseph Boyer
parent_id: KATA-2560
release: 2025.3
story_points: 0.05
description: Walk through Auto Loop implementation to get an accurate idea of how long a subsystem takes to complete. This will inform SteerCo commitment decisions and scope management for Q2.
```

---

## Action Item 3: Schedule manager planning meetings with system engineering

```yaml
tracking: slack
priority: P1
assignee: AlexD
parent_id: KATA-127
release: 2025.3
story_points: 0.05
description: Schedule 1-hour meetings for each manager with Komatsu and Applied system engineering personnel to discuss zone allocation and I/Os. Critical for August 2027 truck build timeline planning.
```

---

## Action Item 4: Gather dependency information for vehicle managers

```yaml
tracking: jira
priority: P1
assignee: Joseph Boyer
parent_id: KATA-127
release: 2025.3
story_points: 0.1
description: Document clear dependency information including pin-outs, sensors, and motors for various managers. Required for vehicle hardware team planning toward August 2027 first truck build.
```

---

## Action Item 5: Share hardware connector and crimping requirements for Palm zonal

```yaml
tracking: jira
priority: P1
assignee: AlexD
parent_id: KATA-127
release: 2025.3
story_points: 0.05
description: Share list of connectors, terminals, and crimpers needed to expand the harness once application hardware needs on zonal and central compute. This is needed for Koamtsu to modify harness and expect hardware testing.
```

---

## Action Item 6: Define mandatory hardware diagnostics requirements for each manager

```yaml
tracking: jira
priority: P1
assignee: Joseph Boyer
parent_id: KATA-127
release: 2025.3
story_points: 0.1
description: Work with Chad and Lee to determine mandatory requirements for hardware diagnostics, including circuit diagnostics (open, closed, short circuit) for outputs and current/voltage diagnostics for inputs.
```

