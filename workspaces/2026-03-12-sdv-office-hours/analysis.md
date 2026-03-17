# Meeting Analysis: Katana <> Applied: SDV SW Office Hours (Mar 12, 2026)

## 1. Meeting Context

**Meeting Title:** Katana <> Applied: SDV SW Office Hours  
**Date:** March 12, 2026  
**Duration:** ~61 minutes (00:00:00 - 01:01:39)  
**Participants:**
- Alex Del Re (Meeting facilitator)
- Jonas Hageman
- Mike (Developer working on workbench code)
- Ashley Forbes (Applied team member)
- Timothy Kyung (Applied team member)

**Meeting Location:** Office room/pod with screen sharing capabilities  
**Stated Objective:** Weekly office hours for SDV software development support and technical discussion

**Content Type:** Full transcript with detailed conversation, speaker identification, and timestamps

## 2. Key Decisions

1. **Decision 1:** Testing strategy will incorporate higher-level SILL (Software-in-the-Loop) testing to catch runtime issues that unit tests miss
2. **Decision 2:** Workbench training session scheduled for Monday to address integration testing workflows  
3. **Decision 3:** System architecture review scheduled for Wednesday to finalize controller placement and zonal assignments
4. **Decision 4:** Documentation will be updated to clarify build dependencies and test target requirements
5. **Decision 5:** Slack channel will be the primary communication method for technical questions rather than office hours notes page

## 3. Discussion Themes

**Testing Validation Gap** - Critical issue where unit tests pass but production code fails due to empty runtime functions while mocks are populated, creating false confidence in code quality

**Build System Complexity** - Confusion around Bazel dependencies, test targets, and what components are actually required versus auto-generated

**System Architecture Planning** - Ongoing work to define controller placement across vehicle zones and whether to aggregate sensors by function or location

**Documentation Clarity** - Need for clearer guidance on build processes, testing setup, and component dependencies

**Communication Workflow** - Establishing proper channels for technical questions and meeting coordination

**Hardware Testing Strategy** - Discussion of when and how to validate code on actual hardware versus simulation/emulation

## 4. Unresolved Questions

- How to systematically detect missing runtime function implementations before hardware deployment? [Ashley to research]
- What is the exact purpose and necessity of "test_only" targets in Bazel builds? [Ashley to clarify with testing team]
- Should sensors be aggregated by function or grouped into zone-based "miscellaneous IO" controllers? [Team discussion needed]
- What are the computational resource limits for stacking multiple software components on a single zonal controller? [Ashley to investigate]
- How will the CI/CD pipeline integrate workbench testing to catch these runtime issues? [TBD - workflow definition needed]

## 5. Action Items

**Action Item 1: Research Testing Validation Solutions**
- **What:** Investigate methods to detect missing runtime function implementations in automated testing
- **Who:** Ashley Forbes
- **When:** Before next office hours
- **Priority:** High
- **Theme:** Testing Validation Gap

**Action Item 2: Clarify Test Target Documentation**  
- **What:** Document the purpose and usage of "test_only" targets and mock kernel interfaces in build system
- **Who:** Ashley Forbes (with testing team consultation)
- **When:** This week
- **Priority:** Medium
- **Theme:** Documentation Clarity

**Action Item 3: Schedule Workbench Training Session**
- **What:** Set up Monday training on workbench integration testing workflows
- **Who:** Alex Del Re
- **When:** Monday (next week)
- **Priority:** High
- **Theme:** Hardware Testing Strategy

**Action Item 4: Define System Architecture Guidelines**
- **What:** Establish recommendations for sensor controller aggregation (function vs. location based)
- **Who:** Ashley Forbes (with team input)
- **When:** Before Wednesday architecture review
- **Priority:** Medium
- **Theme:** System Architecture Planning

**Action Item 5: Update Build Dependencies Documentation**
- **What:** Enhance embedded unit testing documentation with clearer dependency explanations
- **Who:** Ashley Forbes (with documentation team)
- **When:** This week
- **Priority:** Medium
- **Theme:** Documentation Clarity

**Action Item 6: Implement SILL Testing Integration**
- **What:** Design CI/CD pipeline integration for workbench-based testing to catch runtime issues
- **Who:** Unassigned (requires team discussion)
- **When:** TBD
- **Priority:** High
- **Theme:** Testing Validation Gap

## 6. Prioritized Action Plan

| # | Proposed Action Item | Assignee | Priority | Due | Type | Notes |
|---|---------------------|----------|----------|-----|------|-------|
| 1 | Research testing validation solutions for runtime function detection | Ashley Forbes | High | Next office hours | Technical | → JIRA ticket |
| 2 | Schedule workbench training session for integration testing | Alex Del Re | High | Monday | Coordination | → Slack tracking |
| 3 | Implement SILL testing integration in CI/CD pipeline | Unassigned | High | TBD | Technical | → JIRA ticket |
| 4 | Define system architecture guidelines for controller aggregation | Ashley Forbes | Medium | Wednesday review | Technical | → JIRA ticket |
| 5 | Clarify test target documentation and mock interfaces | Ashley Forbes | Medium | This week | Technical | → JIRA ticket |
| 6 | Update build dependencies documentation | Ashley Forbes | Medium | This week | Technical | → JIRA ticket |

**Next Steps:**
- **Immediate:** Ashley to research testing validation approaches and consult with testing team on "test_only" targets
- **This Week:** Schedule Monday workbench training and prepare for Wednesday architecture review
- **Follow-up:** Define CI/CD integration strategy for comprehensive testing validation
- **Documentation:** Update embedded testing guides with clearer dependency and build target explanations
- **Architecture:** Finalize controller placement strategy and zonal assignment guidelines