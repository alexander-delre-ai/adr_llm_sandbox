# Meeting Analysis: SDV SIL Testing Overview (Mar 17, 2026)

## 1. Meeting Context

- **Title**: SDV SIL Testing Overview
- **Date**: March 17, 2026, 4:14 PM
- **Duration**: 2h 50m 5s
- **Location**: In-person (conference room, with lunch break mid-session)
- **Transcription**: Joseph Boyer started/stopped transcription

**Participants**:

| Name | Organization | Role/Context |
|------|-------------|--------------|
| Joseph Boyer | Komatsu | Technical lead, transcription owner |
| Jonas Hageman | Komatsu | Auto lube developer |
| Nuthan Sabbani | Komatsu | Asked about VECU config and executable deployment |
| Mike Lemm | Komatsu | Raised pyArch interface uniqueness concerns |
| Eric Peters | Komatsu | Discussed test organization and directory structure |
| Tess | Komatsu | Departed early |
| Tony | Komatsu | Mentioned re: operator display work (instrument cluster) |
| Alex Del Re | Applied | Joined later for office hours portion |
| Presenter (PMO-CCLL-B-Iron) | Applied | VehicleOS/core platform engineer leading SIL training |

**Stated Objective**: Provide the Komatsu development team with a comprehensive overview of the SIL (Software-in-the-Loop) testing infrastructure, including virtual ECUs, system composition, signal probes, signal injection, and the integration test framework. The session aimed to prepare the team for writing and running integration-level tests against virtualized representations of the Komatsu zonal architecture.

## 2. Key Decisions

Decision 1: SIL testing will focus on integration-level testing (zone-to-zone communication), complementing the unit tests written per-app in each codebase. Unit tests are a narrower form of SIL; Workbench-based SIL is integration-scoped.

Decision 2: Komatsu is primarily a consumer of the VECU/syscomp infrastructure. Applied builds the syscomps and virtualization definitions; Komatsu defines start scripts and writes test cases.

Decision 3: Start scripts are the primary customization point for different truck configurations (930, 830, shovel, LHD). Each configuration variant gets its own start script within the syscomp.

Decision 4: Signal probes require separate definitions per interface being monitored. You cannot reuse a single probe across multiple instances of the same interface.

Decision 5: Test organization will use pytest markers for grouping tests by subsystem (engine, battery, electric, etc.), allowing selective test execution without directory-based filtering.

Decision 6: Early development will use stubbed/mocked signals for subsystems not yet built, with progressive integration as systems mature. The team favored building skeleton frameworks for undeveloped subsystems over pure stubs, so signal paths are architecturally realistic from the start.

## 3. Discussion Themes

### Theme 1: SIL Architecture & Virtual ECUs
Overview of the virtual ECU framework built into VehicleOS. Virtual ECUs are Docker containers representing target compute nodes (zones, central compute). They can run either full firmware (via QEMU with QNX/Yocto) or lighter Docker-based applications. The `maz` command orchestrates bringing up VECU instances from syscomp definitions.

### Theme 2: System Composition (Syscomps)
Syscomps define the vehicle's electronic architecture -- what compute elements exist, how they communicate, and what software runs on each. Compute elements specify build targets (e.g., Qualcomm QNX for central), network interfaces (EMAC, IP addresses), SSH access, and environment configuration. The syscomp is the foundational definition that drives everything downstream.

### Theme 3: Signal Probes & Interface Concerns
Signal probes instrument applications to monitor specific signals (e.g., door state, engine speed). Mike Lemm raised significant concerns about pyArch interface uniqueness constraints: if multiple controllers share the same interface definition (e.g., engine powertrain running vs battery powertrain running), it is unclear how signal probes differentiate between them. This is compounded by runtime configuration (vs build-time configuration), where interfaces may be used in multiple locations simultaneously. The presenter acknowledged these as open questions to take back to the team.

### Theme 4: Integration Test Framework
The pytest-based integration test framework wraps adaptive signal probes, local rig injectors, and instrument cluster readers into a cohesive test harness. Tests follow a directory structure with build files, runners, conftest fixtures, and pytest configuration. The framework supports markers for test categorization and CLI flags for scoping probe targets.

### Theme 5: Signal Injection & Monitoring
The local rig injector provides a CLI for sending CAN/Ethernet traffic into virtualized applications. An interactive CLI establishes connection to a specific rig/board/port, then `injectcan` commands send messages by bus, ID, and data. The `collect_stream` method monitors interfaces for events over a defined period or entry count. Both injection and monitoring can be scripted for automated test cases.

### Theme 6: Test Strategy & Maturity
Discussion on isolation vs full-system testing. Early development (e.g., auto lube) will stub signals from undeveloped subsystems. As the system matures, more realistic signal inputs replace stubs. Trade-off: full virtualization of all zones requires significant compute resources and may not be feasible on a single machine. The team agreed to use both approaches -- isolation tests for rapid development, full-system tests for high-risk subsystems like hoist.

### Theme 7: Propagation Timing
Questions about whether SIL accounts for real-time signal propagation delays. The presenter confirmed SIL is primarily for logical A-to-B data movement validation, not timing verification. However, real-time aspects exist (debounce timers use VM sim time), and timing measurement can be added via manual timer instrumentation in test scripts. The framework does not have built-in propagation timing measurement.

## 4. Unresolved Questions

- Who ultimately owns the virtualization definitions (syscomps, compute elements) long-term? [Applied/Komatsu -- open question with the team]
- How does the VECU config tie back to the repository target/build system? Nuthan asked how a named VECU (e.g., "cabsnormal") gets linked to actual build targets and application definitions. [Presenter noted the question]
- Can pyArch support multiple instances of the same software component with identical port names on different ECUs? [Mike Lemm -- needs follow-up with Ian/pyArch team]
- How does a signal probe differentiate between identical interfaces on different zones (e.g., front brake controller vs rear brake controller)? [Mike Lemm/Jonas -- presenter suggested CLI flags may help but needs verification]
- Does the local rig injector support physical signals (current sensing, analog voltages) in addition to CAN/Ethernet? [Presenter said "I believe so" -- needs confirmation]
- What is the field name mapping between pyArch port names and signal probe event names? [Multiple people asked -- presenter traced it to service interface defined events but could not fully confirm]
- NDA status for Qualcomm QNX binary [Josh Rohman is working on it]
- Runtime configuration solution for the Komatsu team [Still being worked on with core platform team]
- Can multiple pytest markers be applied to a single test? [Presenter confirmed yes via Stack Overflow reference, but noted it should be verified]

## 5. Action Items

### Action Item 1: Follow up on PyArch interface constraints for interface creation
- **What**: Joseph raised that multiple controllers sharing the same interface definition will cause issues with signal probes when using runtime (not build-time) configuration. Confirm with Ian/pyArch team whether this is a blocker and what workarounds exist.
- **Who**: Alex Del Re
- **When**: Before next SIL working session
- **Priority**: High
- **Theme**: Signal Probes & Interface Concerns

### Action Item 2: Clarify vECU-to-repository target binding mechanism
- **What**: Nuthan asked how a named VECU (e.g., "cabsnormal") gets linked to the actual build targets and application definitions in the repo. The presenter noted the question but did not have the answer.
- **Who**: Alex Del Re
- **When**: TBD
- **Priority**: Medium
- **Theme**: System Composition (Syscomps)

### Action Item 3: Confirm physical signal support in local rig injector
- **What**: Team needs to know if SIL testing supports current sensing, analog voltages, and other physical signals beyond CAN/Ethernet digital buses.
- **Who**: Alex Del Re
- **When**: TBD
- **Priority**: Medium
- **Theme**: Signal Injection & Monitoring

### Action Item 4: Clarify signal probe field name mapping from pyArch
- **What**: Multiple team members were unclear on how pyArch port names/interface variables map to signal probe event names in the test framework. The presenter traced it to service interface defined events but the full mapping was not confirmed.
- **Who**: Alex Del Re
- **When**: TBD
- **Priority**: Medium
- **Theme**: Signal Probes & Interface Concerns

### Action Item 5: Identify how SIL start script configuration patterns for Komatsu truck variants
- **What**: Start scripts are the key customization point for different truck configurations. Define patterns for 930, 830, shovel, LHD and document how environment variables and build variations are managed within the syscomp framework.
- **Who**: Unassigned
- **When**: TBD
- **Priority**: Medium
- **Theme**: SIL Architecture & Virtual ECUs

### Action Item 6: Investigate multiple software component instance support with signal probes
- **What**: Joseph raised concern about running identical software components (e.g., brake controller) on front and rear zones with same port names. Signal probes and pyArch interfaces cannot differentiate between instances with the same defined event names. Determine if CLI flags, zone-scoped probes, or other mechanisms can differentiate instances.
- **Who**: Unassigned
- **When**: TBD
- **Priority**: High
- **Theme**: Signal Probes & Interface Concerns

## 6. Prioritized Action Plan

| # | Proposed Action Item | Assignee | Priority | Due | Type | Notes |
|---|---------------------|----------|----------|-----|------|-------|
| 1 | Follow up on PyArch interface constraints for interface creation | Alex Del Re | High | Before next SIL session | Coordination | -> Slack tracking |
| 2 | Investigate multiple software component instance support with signal probes | Unassigned | High | TBD | Coordination | -> Slack tracking |
| 3 | Clarify vECU-to-repository target binding mechanism | Alex Del Re | Medium | TBD | Coordination | -> Slack tracking |
| 4 | Confirm physical signal support in local rig injector | Alex Del Re | Medium | TBD | Coordination | -> Slack tracking |
| 5 | Clarify signal probe field name mapping from pyArch | Alex Del Re | Medium | TBD | Coordination | -> Slack tracking |
| 6 | Identify how SIL start script configuration patterns for Komatsu truck variants | Unassigned | Medium | TBD | Coordination | -> Slack tracking |

### Next Steps

- Alex Del Re to consolidate the Slack-tracked follow-up questions and raise them with the Applied core platform / VehicleOS team (Ian for pyArch, presenter for VECU/injector questions)
- Komatsu team to review the SIL documentation in the VehicleOS repo (`vehicle_os/test/integration_tests/`) and begin familiarizing with the example tests (Marco/Polo signal probe test)
- Schedule a follow-up hands-on SIL working session once the pyArch interface questions are resolved, so the team can begin writing their first auto lube integration test
