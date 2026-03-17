# Action Items: Katana <> Applied SDV SW Office Hours (Mar 13, 2026)

## Instructions

Edit the fields below as needed. When ready, confirm with the agent to create the action items.

**Field Guide:**

- **tracking**: "jira" (create JIRA ticket + include in Slack), "slack" (Slack summary only, no JIRA ticket), "both" (same as jira)
  - Auto-assigned: Items involving scheduling/meetings default to "slack", others to "jira"
- **priority**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- **assignee**: Single person responsible for the action item (one assignee per item) - defaults to "Unassigned"
- **parent_id**: Epic ID (KATA-XXXX or AVP-XXXX format) - leave as "TBD" to use default "KATA-127"
- **release**: Target release - leave as "TBD" to use default "Release 2026.1". Can use short format (e.g., "2025.3" will become "Release 2025.3")
- **story_points**: 0.2 (1 day), 0.5 (2.5 days), 1 (1 week), 2 (2 weeks), 3 (3 weeks), 5 (5 weeks), 8 (8 weeks) - always defaults to 0
- **description**: Brief summary of the work

---

## Action Item 1: Merge Irene Diagnostics PR into Komatsu Codebase

```yaml
tracking: slack
priority: P0
assignee: AlexD
parent_id: TBD
release: TBD
story_points: 0
description: Merge the Irene diagnostics implementation PR that brings the Irene diagnostics layer into the Komatsu codebase. Targeting merge today (Mar 13).
```

---

## Action Item 2: Add clarification to documentation over HSD vs EFuse Output Definition in system.py

```yaml
tracking: jira
priority: P1
assignee: Unassigned
parent_id: KATA-2226
release: 25.3
story_points: 0
description: Investigate and document why the Komatsu headlights controller SWC (system.py) defines both HSD and EFuse (EU) outputs for similar light controls. Suspected cause is running out of HSD pins on the PCB. Confirm and provide clear guidance to the Komatsu team.
```

---

## Action Item 3: Confirm Current-Draw Readback Capability is on Platform Roadmap

```yaml
tracking: slack
priority: P1
assignee: AlexD
parent_id: TBD
release: TBD
story_points: 0
description: Confirm with the HSD platform engineer that current-draw readback from EFuse/HSD outputs is a planned capability available before the 2027 Arizona prototype delivery. If not on the roadmap, escalate to get it added. Komatsu hardware team is assuming this functionality will exist.
```

---

## Action Item 6: Schedule Docusaurus overview with Komatsu Team

```yaml
tracking: slack
priority: P2
assignee: Alex Del Re
parent_id: TBD
release: TBD
story_points: 0
description: Arrange a short Docusaurus demo session with Katana tech writer Gyra for the Komatsu team. Komatsu is evaluating Gitbook vs Docusaurus before making a purchase decision.
```

---

## Action Item 7: Follow Up on Signal Validation Custom Approach

```yaml
tracking: slack
priority: P2
assignee: Unassigned
parent_id: TBD
release: TBD
story_points: 0
description: Follow up with Evan (who attended last week's office hours) on building a more custom signal validation process for Komatsu, as the current approach relies heavily on AutoSAR schemas. Schedule a focused discussion for next week.
```

