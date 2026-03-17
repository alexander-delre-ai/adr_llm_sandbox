# Action Items: SDV SW Office Hours (Mar 16, 2026)

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

## Deliver a timeline for native Ethernet frame packing support

```yaml
tracking: jira
priority: P1
assignee: Alex Del Re
parent_id: KATA-726
release: 25.3
story_points: 0.1
description: Raise with the engineering team to determine when native Ethernet frame packing (instead of CAN-over-ETH) will be available. Jonas flagged that current docs note limitations in modeling/code generation for Ethernet frames. Engine interface and payload meter are high-priority apps that will need this.
```

## Investigate some-IP cross-zone latency for central-to-zone communication

```yaml
tracking: slack
priority: P1
assignee: Alex Del Re
parent_id: TBD
release: TBD
story_points: 0
description: Check with Rushi on what the some-IP cross-zone latency is for data passing between central and zones. Same-zone uses shared memory (very fast), but cross-zone latency is unknown. Joe needs this to evaluate IP middleware as a transport option for payload meter.
```

## Provide struct sizes for PIP and HIP payload meter data

```yaml
tracking: slack
priority: P2
assignee: Joseph Boyer
parent_id: TBD
release: TBD
story_points: 0
description: Get struct sizes for PIP and HIP from Jason to quantify how limiting the CAN FD 64-byte payload is for payload meter data. This helps determine urgency of Ethernet frame or IP transport support.
```

## Review other subsystem signal sizes that may exceed CAN frame limits

```yaml
tracking: slack
priority: P2
assignee: Joseph Boyer
parent_id: TBD
release: TBD
story_points: 0
description: Assess offline which subsystem outputs may not fit within CAN frame limitations. Engine interface will be a concern in phase 2 due to large diagnostic data volumes. Drive systems may also be impacted if integrated.
```

## Follow up on automated PDU start-bit calculation feature request

```yaml
tracking: slack
priority: P2
assignee: Alex Del Re
parent_id: TBD
release: TBD
story_points: 0
description: Follow up internally on Joe Boyer's formal request to have PDU start-bit offsets automatically calculated at build time. Currently developers must manually define offsets when adding/removing/reordering signals, which is tedious and error-prone. Determine if this becomes a feature request or engineering task.x
```

