# Action Items: SDV SIL Testing Overview (Mar 17, 2026)

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

## Follow up on PyArch interface constraints for interface creation

```yaml
tracking: slack
priority: P1
assignee: Alex Del Re
parent_id: TBD
release: TBD
story_points: 0
description: Joseph raised that multiple controllers sharing the same interface definition will cause issues with signal probes when using runtime (not build-time) configuration. Confirm with Ian/pyArch team whether this is a blocker and what workarounds exist. Historically, build-time config meant interfaces were only used once in code, but runtime config means they will be used in multiple locations simultaneously.
```

## Clarify vECU-to-repository target binding mechanism

```yaml
tracking: slack
priority: P2
assignee: Alex Del Re
parent_id: TBD
release: TBD
story_points: 0
description: Nuthan asked how a named VECU (e.g., "cabsnormal") gets linked to the actual build targets and application definitions in the repo. The presenter noted the question but did not have the answer. Follow up with Applied core platform team.
```

## Confirm physical signal support in local rig injector

```yaml
tracking: slack
priority: P2
assignee: Alex Del Re
parent_id: TBD
release: TBD
story_points: 0
description: Team needs to know if SIL testing supports current sensing, analog voltages, and other physical signals beyond CAN/Ethernet digital buses. Presenter said "I believe so" but could not confirm. Follow up with VehicleOS team.
```

## Clarify signal probe field name mapping from pyArch

```yaml
tracking: slack
priority: P2
assignee: Alex Del Re
parent_id: TBD
release: TBD
story_points: 0
description: Multiple team members unclear on how pyArch port names/interface variables map to signal probe event names in the test framework. Presenter traced it to service interface defined events but the full mapping was not confirmed. Need definitive documentation or confirmation from the platform team.
```

## Identify how SIL start script configuration patterns for Komatsu truck variants

```yaml
tracking: slack
priority: P2
assignee: Unassigned
parent_id: TBD
release: TBD
story_points: 0
description: Start scripts are the key customization point for different truck configurations. Define patterns for 930, 830, shovel, LHD and document how environment variables and build variations are managed within the syscomp framework.
```

## Investigate multiple software component instance support with signal probes

```yaml
tracking: slack
priority: P1
assignee: Unassigned
parent_id: TBD
release: TBD
story_points: 0
description: Joseph raised concern about running identical software components (e.g., brake controller) on front and rear zones with same port names. Signal probes and pyArch interfaces cannot differentiate between instances with the same defined event names. Determine if CLI flags, zone-scoped probes, or other mechanisms can differentiate instances. Related to the pyArch interface uniqueness constraint issue.
```

