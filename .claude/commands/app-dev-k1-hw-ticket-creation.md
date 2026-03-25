---
description: Enhanced JIRA ticket creation for K1 hardware application development with smart validation, customizable story points, error recovery, and batch processing. Features historical learning, checkpoint-based recovery, and interactive plan customization. Use for K1 hardware development workflows, batch manager processing, or when you need robust ticket creation with failure recovery.
---

# App Dev K1 Hardware Ticket Creation

Creates JIRA tickets for K1 hardware application development using standardized templates that define tasks and their dependencies.

## Template Structure

The skill expects a markdown template with:
- Manager name placeholder: `{manager_name}`
- Numbered task list (1-11 tasks)
- JIRA ticket link types section defining dependencies

## Template Example

```markdown
## Manager: {manager_name}

1. List out input/output mappings for {manager_name}
2. List out hardware dependencies for application functionality
3. Establish zonal allocation for manager software
4. Draft functional requirements for {manager_name} manager
5. Draft performance requirements for {manager_name} manager
6. Review and sign-off on requirements for {manager_name} manager
7. Draw subsystem diagrams on shared Miro board
8. Define test cases for {manager_name} manager
9. State machine development for {manager_name}
10. Allocate physical HW for placement on truck bench
11. HW bringup for {manager_name} on K1 bench

## Jira ticket link types:
1 and 2 are related
2 blocks 3
1 blocks 4
1 blocks 5
4 and 5 are related
4 blocks 6
5 blocks 6
6 blocks 7
6 blocks 8
4 blocks 9
5 blocks 9
3 blocks 10
10 blocks 11
```

## Required Parameters

When using this skill, you must provide:
- `manager_name`: The specific manager/component name (e.g., "PowerManager", "ThermalManager")
- `manager_epic_id`: The manager-specific epic ID (must use KATA- prefix, e.g., "KATA-2800")

## Auto-configured Parameters

- `project`: Always "KATA" (manager workflows are KATA-specific)
- `initiative_id`: Always "KATA-1760" (top-level initiative for all manager epics)
- `release`: Defaults to "Release 26.1" (ID: 10002) unless specified

## Optional Parameters

- `assignee`: Team member name (default: "Unassigned")
- `priority`: P0-P3 priority level (default: "P2")
- `labels`: Not used (labels are not added to JIRA items)
- `release`: Target release (default: "Release 26.1")
- `story_points`: Custom story points array (11 values) or "default" to use 0 for all tasks (must be estimated)
- `batch_mode`: Set to true for multi-manager batch processing
- `managers_list`: Array of manager configurations for batch mode

## Workflow

1. **Pre-validation** (Smart Validation):
   - Load validation history and check for known issues
   - Verify JIRA connectivity and user permissions
   - Validate epic existence and linkage to KATA-1760
   - Check for duplicate ticket names in target epic
   - Validate release version against available options
   - Generate validation warnings and recommendations

2. **Template Processing**:
   - Replace `{manager_name}` placeholder with actual manager name
   - Parse numbered task list (1-11)
   - Extract dependency relationships from link types section
   - Handle batch mode if multiple managers specified

3. **Plan Generation**:
   - Create enhanced `plan.md` file with validation results
   - Include story points customization section with guidelines
   - Show ticket titles, descriptions, and dependency relationships
   - Display epic structure and initiative linkage
   - Add batch configuration if applicable

4. **Interactive Plan Review**:
   - Present plan.md to user for review
   - Allow story points modification with Fibonacci validation
   - Warn if any tasks remain at 0 points (estimation required)
   - Enable parameter adjustments (priority, assignee, release)
   - Show validation warnings and recommendations
   - Wait for explicit confirmation to proceed

5. **Checkpoint Creation**:
   - Create checkpoint file before starting JIRA operations
   - Initialize progress tracking for error recovery
   - Set up transaction logging for audit trail

6. **Progressive Ticket Creation**:
   - Create 11 JIRA tasks per manager with pause-on-error capability
   - Use format: `[Task Description]` (no manager brackets)
   - Link all tasks to the manager-specific epic
   - Include release and story points for each task (default 0, must be estimated)
   - Set all tasks as unassigned initially
   - Update checkpoint after each successful operation

7. **Dependency Linking** (immediately after ticket creation, no separate confirmation):
   - Create JIRA issue links with CORRECT directions using validated logic
   - For "Task A blocks Task B": inwardIssue = A (gets "blocks"), outwardIssue = B (gets "is blocked by")
   - Support "blocks/blocked by" and "relates" relationships
   - Continue with remaining links if individual links fail
   - Log all operations for potential rollback
   - Dependency directions have been validated across all 20 managers (P0-P3) and are confirmed correct

8. **Error Recovery** (if failures occur):
   - Pause on first failure and generate recovery plan
   - Offer options: retry, skip, rollback, or manual intervention
   - Maintain transaction log for audit and troubleshooting
   - Support resuming from last successful checkpoint

9. **Final Reporting**:
    - Update validation history with results
    - Generate comprehensive success/failure report
    - Update statistics for future smart validation
    - Include dependency verification in final report

## Implementation Details

### MCP Server Configuration

Manager workflows always use:
- **MCP Tools**: `mcp__kata-atlassian__*`
- **Cloud ID**: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`
- **Project**: KATA
- **Initiative**: KATA-1760 (top-level initiative for all manager epics)

### Validated Dependency Pattern

The dependency directions below have been validated across all 20 managers (6 P1, 3 P2, 11 P3) and confirmed correct.
No separate dependency confirmation step is required. Ticket creation and dependency linking
proceed as a single continuous operation after plan review.

**Standard 13-link dependency pattern (validated)**:
```
1 relates 2      (bidirectional)
2 blocks 3       (2 must complete before 3)
1 blocks 4       (1 must complete before 4)
1 blocks 5       (1 must complete before 5)
4 relates 5      (bidirectional)
4 blocks 6       (4 must complete before 6)
5 blocks 6       (5 must complete before 6)
6 blocks 7       (6 must complete before 7)
6 blocks 8       (6 must complete before 8)
4 blocks 9       (4 must complete before 9)
5 blocks 9       (5 must complete before 9)
3 blocks 10      (3 must complete before 10)
10 blocks 11     (10 must complete before 11)
```

## JIRA Link Direction Logic (CRITICAL)

**Understanding JIRA createIssueLink parameters**:

For relationship "Task A blocks Task B":
- `inwardIssue`: Task A (gets "blocks" relationship)
- `outwardIssue`: Task B (gets "is blocked by" relationship)
- `type`: "Blocks"

**Example**: "Task 1 blocks Task 2"
- `mcp__kata-atlassian__createIssueLink` with:
  - `inwardIssue`: "KATA-2625" (Task 1 - shows "blocks KATA-2626")
  - `outwardIssue`: "KATA-2626" (Task 2 - shows "is blocked by KATA-2625")
  - `type`: "Blocks"

**CRITICAL**: Do NOT include a comment field in createIssueLink calls - causes "Invalid ADF content" errors.

## Task Template Mapping

Standard K1 hardware development tasks:
1. **I/O Mapping**: List input/output mappings for {manager_name}
2. **Hardware Dependencies**: List hardware dependencies for application functionality
3. **Zonal Allocation**: Establish zonal allocation for manager software
4. **Functional Requirements**: Draft functional requirements for {manager_name} manager
5. **Performance Requirements**: Draft performance requirements for {manager_name} manager
6. **Requirements Sign-off**: Review and sign-off on requirements for {manager_name} manager
7. **Subsystem Diagrams**: Draw subsystem diagrams on shared Miro board
8. **Test Cases**: Define test cases for {manager_name} manager
9. **State Machine**: State machine development for {manager_name}
10. **Physical Allocation**: Allocate physical HW for placement on truck bench
11. **HW Bringup**: HW bringup for {manager_name} on K1 bench

## Release Mapping (KATA)

| Release Name | Field ID | Usage |
|--------------|----------|-------|
| Release 25.1 | 10000 | Legacy |
| Release 25.2 | 10001 | Legacy |
| Release 25.3 | 10036 | Legacy |
| Release 26.1 | 10002 | **Default** |
| Release 26.2 | 10003 | Available |

## Epic Structure

```
KATA-1760 (Initiative: K1 Hardware Manager Development)
├── KATA-XXXX (Epic: [Manager] Development)
│   ├── KATA-YYYY (Task 1: List out input/output mappings for [Manager])
│   ├── KATA-YYYY (Task 2: List out hardware dependencies for application functionality)
│   └── ... (Tasks 3-11)
└── ... (20 Manager Epics total: 6 P1, 3 P2, 11 P3)
```

## Batch Processing Support

### Single Manager Mode (Default)
Standard workflow for creating tickets for one manager at a time.

### Batch Mode
Process multiple managers independently with combined reporting.

**Usage**:
```
Parameters:
- batch_mode: true
- managers_list: [
    {
      manager_name: "AutoLube",
      manager_epic_id: "KATA-2800",
      story_points: [3,5,8,5,5,3,13,5,8,3,5], // optional custom points (11 values)
      priority: "P2" // optional per-manager priority
    },
    {
      manager_name: "ThermalManager",
      manager_epic_id: "KATA-2810"
    }
  ]
```

**Batch Workflow**:
1. Generate combined batch plan showing all managers
2. Allow story points customization per manager
3. Process each manager independently
4. Generate combined summary report
5. Handle failures in isolation (one manager failure doesn't affect others)

## Smart Validation System

### Validation History Tracking
- Maintains `.cursor/skills/app-dev-k1-hw-ticket-creation/validation-history.json` with past successes/failures
- Learns from common failure patterns
- Provides proactive warnings based on historical data

### Pre-flight Validation Checks
- **Epic Validation**: Verify epic exists and is linked to KATA-1760
- **Permission Check**: Confirm user can create tickets in target epic
- **Release Validation**: Ensure release version exists in JIRA project
- **Duplicate Detection**: Check for existing tickets with similar names
- **Connectivity Test**: Verify JIRA and MCP server accessibility

## Error Recovery System

### Recovery Options
When failures occur, users can choose:

1. **Retry Failed Operations**: Attempt failed items again
2. **Skip and Continue**: Mark failed items as completed, continue with rest
3. **Rollback**: Delete all created tickets/links and start fresh
4. **Manual Intervention**: Pause for manual JIRA operations, then resume
