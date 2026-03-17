# Action Items: Katana <> Applied: SDV SW Office Hours (Mar 12, 2026)

## Instructions

Edit the fields below as needed. When ready, confirm with the agent to create the action items.

**Field Guide:**

- **tracking**: "jira" (create JIRA ticket + include in Slack), "slack" (Slack summary only, no JIRA ticket), "both" (same as jira)
  - Auto-assigned: Items involving scheduling/meetings default to "slack", others to "jira"
- **priority**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- **assignee**: Single person responsible for the action item (one assignee per item) - defaults to "Unassigned"
- **parent_id**: Epic ID (KATA-XXXX or AVP-XXXX format) - leave as "TBD" to use default "KATA-127"
- **release**: Target release - leave as "TBD" to use default "Release 2026.1". Can use short format (e.g., "2025.3" will become "Release 2025.3")
- **story_points**: 0.2 (1 day), 0.5 (2.5 days), 1 (1 week), 2 (2 weeks), 3 (3 weeks), 5 (5 weeks), 8 (8 weeks) - defaults to 0 if not specified
- **description**: Brief summary of the work

---

## Action Item 1: Research Testing Validation Solutions

```yaml
tracking: slack
priority: P1
assignee: AlexD
parent_id: TBD
release: TBD
story_points: 0
description: Investigate methods to detect missing runtime function implementations in automated testing. Focus on identifying gaps where unit tests pass but production code fails due to empty runtime functions while mocks are populated.
```

## Action Item 3: Scope SIL Testing CI Integration

```yaml
tracking: jira
priority: P2
assignee: Unassigned
parent_id: KATA-378
release: 2025.3
story_points: 0
description: Design and implement CI/CD pipeline integration for workbench-based SILL testing to catch runtime issues that unit tests miss.
```

## Action Item 5: Clarify Test Target Documentation

```yaml
tracking: slack
priority: P2
assignee: AlexD
parent_id: KATA-2226
release: 2025.3
story_points: 0
description: Document the purpose and usage of test_only targets and mock kernel interfaces in the build system. Consult with testing team for accurate explanations.
```

## Action Item 6: Update Build Dependencies Documentation

```yaml
tracking: jira
priority: P2
assignee: Unassigned
parent_id: KATA-2226
release: 2025.3
story_points: 0
description: Enhance embedded unit testing documentation with clearer explanations of Bazel dependencies, build targets, and component requirements.
```

