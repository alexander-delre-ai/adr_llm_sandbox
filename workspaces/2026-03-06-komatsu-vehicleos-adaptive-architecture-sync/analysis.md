# Meeting Analysis: Komatsu <> VehicleOS Adaptive Architecture sync (Mar 6, 2026)

## 1. Meeting context

| Field | Value |
|-------|-------|
| Meeting title | Komatsu <> VehicleOS Adaptive Architecture sync |
| Date & time | March 6, 2026 |
| Participants | Srishti Dhamija (VehicleOS), Nuthan Sabbani (Komatsu), Coulomb's Law/Alex (SVL) |
| Stated objective | Technical sync on VehicleOS Adaptive Architecture implementation questions and use cases |

## 2. Key decisions

Decision 1: PyArch does not model internal application threading - this is left to application developers to implement.

Decision 2: Inter-process communication will be handled by PyArch using SomeIP protocol with three communication patterns (events, publish/subscribe, and methods/RPC).

Decision 3: For local communication, PyArch will automatically use Unix domain sockets for performance optimization.

Decision 4: System model can be shared between Linux and QNX platforms, but executables must be built separately for each target platform.

Decision 5: Third-party libraries like SQLite can be integrated through Bazel build configuration for both platforms.

## 3. Discussion themes

**Threading Architecture**: Discussion about how PyArch handles internal application threading vs inter-process communication, with focus on payload application's multi-threaded design.

**Communication Patterns**: Deep dive into SomeIP protocol, Unix domain sockets, and the three communication patterns (events, methods, fields) available in PyArch.

**Service Management**: How PyArch integrates with systemd/SLM for process orchestration, startup dependencies, and service lifecycle management.

**Cross-Platform Support**: Building applications for both Linux and QNX platforms using the same system model with platform-specific compilation.

**Configuration Management**: Real-time configuration updates from UI to applications, including payload meter settings and scoreboard display modes.

**Data Persistence**: Schema migration handling for persistent data structures across software updates and version changes.

**Development Workflow**: Getting started with PyArch development, tutorials, and creating reference applications for Komatsu's use cases.

## 4. Unresolved questions

- OS selection configuration examples and documentation location [Srishti to investigate]
- Schema migration support in PyArch persistency module for handling data structure version changes [Srishti to research with team]
- Specific design patterns and best practices documentation for onboard applications [VehicleOS team to provide based on Komatsu use cases]
- Dependency updates needed in Komatsu repo to support PyArch development [Alex to check with team]
- CLI tools for querying system logs and process status [Srishti to verify upcoming features]
- Detailed payload application feature requirements for reference app development [Nuthan to provide]

## 5. Action items

**Task 1: Provide OS selection configuration examples**
- **What**: Share examples of OS selection configuration in PyArch documentation
- **Who**: Srishti Dhamija
- **When**: After meeting
- **Priority**: Medium
- **Theme**: Cross-Platform Support

**Task 2: Research schema migration support**
- **What**: Investigate PyArch persistency module capabilities for handling data structure version changes and schema migration
- **Who**: Srishti Dhamija (with persistency team)
- **When**: Next week
- **Priority**: High
- **Theme**: Data Persistence

**Task 3: Create payload application reference documentation**
- **What**: Develop step-by-step documentation and examples for payload application use cases based on Komatsu requirements
- **Who**: VehicleOS team (Srishti)
- **When**: TBD (after requirements gathering)
- **Priority**: High
- **Theme**: Development Workflow

**Task 4: Provide detailed payload feature requirements**
- **What**: Document specific payload application features and use cases for reference app development
- **Who**: Nuthan Sabbani
- **When**: ASAP
- **Priority**: High
- **Theme**: Development Workflow

**Task 5: Check Komatsu repo dependencies**
- **What**: Verify if all PyArch dependencies are available in Komatsu repo and update if needed
- **Who**: Alex (SVL team)
- **When**: After meeting
- **Priority**: Medium
- **Theme**: Development Workflow

**Task 6: Share process startup configuration examples**
- **What**: Provide examples of state-dependent startup configuration and process dependencies in PyArch
- **Who**: Srishti Dhamija
- **When**: After meeting
- **Priority**: Medium
- **Theme**: Service Management

**Task 7: Share logging configuration examples**
- **What**: Provide examples of AR log module usage and syslog integration
- **Who**: Srishti Dhamija
- **When**: After meeting
- **Priority**: Low
- **Theme**: Service Management

## 6. JIRA tickets

**Successfully created 7 JIRA tickets using the KATA MCP server:**

1. **KATA-2563** - Research schema migration support in PyArch persistency module (P1)
   - URL: https://appliedint-katana.atlassian.net/browse/KATA-2563

2. **KATA-2564** - Create payload application reference documentation (P1)
   - URL: https://appliedint-katana.atlassian.net/browse/KATA-2564

3. **KATA-2565** - Provide detailed payload feature requirements (P1)
   - URL: https://appliedint-katana.atlassian.net/browse/KATA-2565

4. **KATA-2566** - Provide OS selection configuration examples (P2)
   - URL: https://appliedint-katana.atlassian.net/browse/KATA-2566

5. **KATA-2567** - Check Komatsu repo dependencies for PyArch development (P2)
   - URL: https://appliedint-katana.atlassian.net/browse/KATA-2567

6. **KATA-2568** - Share process startup configuration examples (P2)
   - URL: https://appliedint-katana.atlassian.net/browse/KATA-2568

7. **KATA-2569** - Share logging configuration examples (P3)
   - URL: https://appliedint-katana.atlassian.net/browse/KATA-2569

All tickets are:
- Linked to Epic KATA-2561
- Assigned to Release 26.1
- Include MCP creation tracking in descriptions

## 7. Prioritized action plan

| # | Ticket | Assignee | Priority | Due | Epic | Release |
|---|--------|----------|----------|-----|------|---------|
| 1 | [KATA-2563](https://appliedint-katana.atlassian.net/browse/KATA-2563) Research schema migration support | Srishti Dhamija | P1 | Next week | KATA-2561 | Release 26.1 |
| 2 | [KATA-2564](https://appliedint-katana.atlassian.net/browse/KATA-2564) Create payload application reference documentation | Srishti Dhamija | P1 | TBD | KATA-2561 | Release 26.1 |
| 3 | [KATA-2565](https://appliedint-katana.atlassian.net/browse/KATA-2565) Provide detailed payload feature requirements | Nuthan Sabbani | P1 | ASAP | KATA-2561 | Release 26.1 |
| 4 | [KATA-2566](https://appliedint-katana.atlassian.net/browse/KATA-2566) Provide OS selection configuration examples | Srishti Dhamija | P2 | After meeting | KATA-2561 | Release 26.1 |
| 5 | [KATA-2567](https://appliedint-katana.atlassian.net/browse/KATA-2567) Check Komatsu repo dependencies | Alex | P2 | After meeting | KATA-2561 | Release 26.1 |
| 6 | [KATA-2568](https://appliedint-katana.atlassian.net/browse/KATA-2568) Share process startup configuration examples | Srishti Dhamija | P2 | After meeting | KATA-2561 | Release 26.1 |
| 7 | [KATA-2569](https://appliedint-katana.atlassian.net/browse/KATA-2569) Share logging configuration examples | Srishti Dhamija | P3 | After meeting | KATA-2561 | Release 26.1 |

### Next steps

- **Nuthan should immediately document detailed payload application requirements** (KATA-2565) to unblock reference documentation creation
- **Srishti should prioritize schema migration research** (KATA-2563) as this is a critical blocker for Komatsu's use case
- **Alex should verify Komatsu repo dependencies** (KATA-2567) to ensure development can begin without delays
- **Schedule follow-up meeting** once requirements are documented and initial examples are shared
- **Continue technical discussions in office hours** as Komatsu team works through PyArch tutorials