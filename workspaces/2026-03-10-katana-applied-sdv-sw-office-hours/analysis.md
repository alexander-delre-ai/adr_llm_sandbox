# Meeting Analysis: Katana <> Applied: SDV SW Office Hours (Mar 10, 2026)

## 1. Meeting Context

**Content Type**: Gemini Summary

**Meeting Details**:
- **Title**: Katana <> Applied: SDV SW Office Hours
- **Date**: March 10, 2026
- **Participants**: Alex Del Re, Joseph Boyer, Nuthan Sabbani, Michael Lemm, Joshua Rohman
- **Meeting Location**: Not specified (Teams/virtual meeting)
- **Stated Objective**: Technical coordination between Katana and Applied teams for SDV software development, focusing on Autosar implementation and manager development planning

## 2. Key Decisions

1. **Decision 1**: Sync server call points will be used for all IO abstraction involving hardware interaction (PWM, ADC, edge counters) as they function like callbacks, which is appropriate for hardware behavior.

2. **Decision 2**: One-hour meetings for each manager should be scheduled with Komatsu and Applied system engineering personnel to discuss zone allocation and I/Os for the August 2027 truck build timeline.

3. **Decision 3**: Use placeholders or "to-do" links in code pointing to specific tickets for incomplete features (circuit diagnostics, UI communications) to help Project Managers track dependencies.

4. **Decision 4**: Focus scope on Auto Loop subsystem for next quarter, potentially adding Engine as a simpler system, treating other planned subsystems as stretch goals to avoid over-commitment.

## 3. Discussion Themes

**Autosar Implementation**: Technical clarification of I-read/I-write calls vs sync server call points, with decisions on hardware abstraction patterns for PWM, ADC, and other IO operations.

**Hardware Bring-up Planning**: Discussion of dependency information needs (pin-outs, sensors, motors) and coordination requirements for the August 2027 first truck build timeline.

**Development Infrastructure**: Setup of hardware flashing capabilities, Linux laptop configuration, and local testing environment separate from cloud workbench.

**Feature Gap Management**: Addressing incomplete features like circuit diagnostics and UI communications through placeholder/ticket-based tracking for project management visibility.

**Scope and Timeline Management**: Strategic discussion about SteerCo commitments, risk of over-commitment to four subsystems, and prioritization of Auto Loop with Engine as potential additions.

**Hardware Diagnostics Requirements**: Technical requirements discussion for circuit diagnostics (open/closed/short), current/voltage diagnostics, and resistive switch implementations.

## 4. Unresolved Questions

- **Hardware connector specifications**: List of connectors, terminals, and crimpers needed to expand the harness once application hardware needs are better understood [Joseph Boyer]

- **Mandatory hardware diagnostics requirements**: Specific requirements for circuit diagnostics (open, closed, short circuit) for every output, and current/voltage diagnostics for inputs [Chad and Lee discussion needed]

- **Reusable Teams meeting setup**: Establishing a permanent meeting resource with the Komatsu team [Joseph Boyer]

- **Manager completion timeline**: How long each subsystem/manager actually takes to complete, pending Auto Loop walkthrough [Joseph Boyer, Alex Del Re]

- **SteerCo commitment scope**: Final decision on which 4 subsystems to commit to for Steering Committee goals vs. focusing on fewer with higher quality

## 5. Action Items

**From Suggested Next Steps:**

1. **Meet with UI team about interface design**
   - **What**: Meet with UI team to discuss what the UI interface is going to look like
   - **Who**: Joseph Boyer
   - **When**: Today (Mar 10, 2026)
   - **Priority**: High
   - **Theme**: Feature Gap Management

2. **Run through Auto Loop subsystem walkthrough**
   - **What**: Walk through Auto Loop implementation to estimate subsystem completion timeline
   - **Who**: Joseph Boyer, Alex Del Re
   - **When**: Not specified
   - **Priority**: High
   - **Theme**: Scope and Timeline Management

**From Details Section:**

3. **Schedule manager planning meetings**
   - **What**: Schedule 1-hour meetings for each manager with Komatsu and Applied system engineering personnel to discuss zone allocation and I/Os
   - **Who**: Joseph Boyer (coordinator)
   - **When**: Before August 2027 truck build
   - **Priority**: High
   - **Theme**: Hardware Bring-up Planning

4. **Provide dependency information for managers**
   - **What**: Gather and document clear dependency information (pin-outs, sensors, motors) for various managers
   - **Who**: Unassigned (vehicle hardware team)
   - **When**: Before August 2027 truck build
   - **Priority**: High
   - **Theme**: Hardware Bring-up Planning

5. **Determine hardware connector requirements**
   - **What**: Get list of connectors, terminals, and crimpers needed to expand harness
   - **Who**: Joseph Boyer
   - **When**: After application hardware needs are understood
   - **Priority**: Medium
   - **Theme**: Development Infrastructure

6. **Define hardware diagnostics requirements**
   - **What**: Determine mandatory requirements for hardware diagnostics with Chad and Lee
   - **Who**: Joseph Boyer, Chad, Lee
   - **When**: Not specified
   - **Priority**: Medium
   - **Theme**: Hardware Diagnostics Requirements

## 6. Prioritized Action Plan

| # | Proposed Ticket | Assignee | Priority | Due | Type | Notes |
|---|-----------------|----------|----------|-----|------|-------|
| 1 | Meet with UI team about interface design | Joseph Boyer | P0 | Today | General | → User Epic |
| 2 | Conduct Auto Loop subsystem walkthrough for timeline estimation | Joseph Boyer, Alex Del Re | P0 | ASAP | General | → User Epic |
| 3 | Schedule manager planning meetings with system engineering | Joseph Boyer | P0 | Before Aug 2027 | General | → User Epic |
| 4 | Gather dependency information for vehicle managers | Unassigned | P0 | Before Aug 2027 | General | → User Epic |
| 5 | Define hardware connector and crimping requirements | Joseph Boyer | P1 | TBD | General | → User Epic |
| 6 | Define mandatory hardware diagnostics requirements | Joseph Boyer | P1 | TBD | General | → User Epic |

## Next Steps

- Joseph Boyer should prioritize the UI team meeting today to unblock manager completion
- Schedule the Auto Loop walkthrough with Alex Del Re immediately to inform Q2 scope decisions
- Begin coordinating manager planning meetings with Komatsu and Applied system engineering teams
- Identify and assign ownership for gathering vehicle manager dependency information
- Consider establishing a regular cadence for Katana <> Applied coordination beyond office hours