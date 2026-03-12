---
name: app-dev-k1-hw-ticket-creation
description: Enhanced JIRA ticket creation for K1 hardware application development with smart validation, customizable story points, error recovery, and batch processing. Features historical learning, checkpoint-based recovery, and interactive plan customization. Use for K1 hardware development workflows, batch manager processing, or when you need robust ticket creation with failure recovery.
---

# App Dev K1 Hardware Ticket Creation

Creates JIRA tickets for K1 hardware application development using standardized templates that define tasks and their dependencies.

## Template Structure

The skill expects a markdown template with:
- Manager name placeholder: `{manager_name}`
- Numbered task list (1-7 tasks)
- JIRA ticket link types section defining dependencies

## Template Example

```markdown
## Manager: {manager_name}

1. List out input/output mappings for {manager_name}
2. List out hardware dependencies for application functionality
3. Establish zonal allocation for manager software 
4. Draw subsystem diagrams on shared miro board
5. Draft functional requirements for {manager_name} manager
6. Draft performance requirements for {manager_name} manager
7. State machine development for {manager_name} 
8. Allocate physical HW for placement on truck bench
9. HW bringup for {manager_name} on K1 bench

## Jira ticket link types:
9 is blocked by 8.
8 is blocked by 3
3 is blocked by 2 
2 is blocked by 1
1 and 2 are related
7 is blocked by 5
7 is blocked by 6
5 and 6 are related
5 is blocked by 4
6 is blocked by 4
4 is blocked by 1
```

## Required Parameters

When using this skill, you must provide:
- `manager_name`: The specific manager/component name (e.g., "PowerManager", "ThermalManager")
- `manager_epic_id`: The manager-specific epic ID (must use KATA- prefix, e.g., "KATA-2800")

## Auto-configured Parameters

- `project`: Always "KATA" (manager workflows are KATA-specific)
- `initiative_id`: Always "KATA-1760" (top-level initiative for all manager epics)
- `release`: Defaults to "Release 26.1" unless specified

## Optional Parameters

- `assignee`: Team member name (default: "Unassigned")
- `priority`: P0-P3 priority level (default: "P2")
- `labels`: Not used (labels are not added to JIRA items)
- `release`: Target release (default: "Release 26.1")
- `story_points`: Custom story points array (9 values) or "default" to use 0 for all tasks (must be estimated)
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
   - Parse numbered task list (1-9)
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

6. **Progressive Ticket Creation** (after confirmation):
   - Create 9 JIRA tasks per manager with pause-on-error capability
   - Use format: `[Task Description]` (no manager brackets)
   - Link all tasks to the manager-specific epic
   - Include release and story points for each task (default 0, must be estimated)
   - Set all tasks as unassigned initially
   - Update checkpoint after each successful operation

7. **Dependency Linking**:
   - Create JIRA issue links with error recovery
   - Support "blocks/blocked by" and "relates" relationships
   - Continue with remaining links if individual links fail
   - Log all operations for potential rollback

8. **Error Recovery** (if failures occur):
   - Pause on first failure and generate recovery plan
   - Offer options: retry, skip, rollback, or manual intervention
   - Maintain transaction log for audit and troubleshooting
   - Support resuming from last successful checkpoint

9. **Final Reporting**:
   - Update validation history with results
   - Generate comprehensive success/failure report
   - Update statistics for future smart validation

## Implementation Details

### MCP Server Configuration

Manager workflows always use:
- **MCP Server**: `user-atlassian-mcp-kata` 
- **Cloud ID**: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`
- **Project**: KATA
- **Initiative**: KATA-1760 (top-level initiative for all manager epics)

### Enhanced Plan Generation Process

1. **Smart Pre-validation**:
   ```javascript
   // Load validation history
   const history = JSON.parse(readFile("validation-history.json"));
   
   // Check epic existence and linkage
   CallMcpTool({
     server: "user-atlassian-mcp-kata",
     toolName: "getJiraIssue",
     arguments: { cloudId: "...", issueIdOrKey: manager_epic_id }
   });
   
   // Validate release version
   CallMcpTool({
     server: "user-atlassian-mcp-kata", 
     toolName: "getVisibleJiraProjects",
     arguments: { cloudId: "..." }
   });
   ```

2. **Create Enhanced Plan Document**:
   Generate `plan.md` with enhanced structure:
   ```markdown
   # K1 Hardware Development Plan: [Manager Name]
   
   ## Overview
   - Manager: [Manager Name]
   - Epic: [Epic ID] - [Manager Name] Development
   - Initiative: KATA-1760 - K1 Hardware Manager Development
   - Release: [Release Name]
   - Total Tasks: 9
   - Estimated Points: [Total Points]
   
   ## Validation Results
   ### Pre-flight Checks
   - [x] JIRA connectivity verified
   - [x] Epic exists and is linked to KATA-1760
   - [x] Release version is valid
   - [x] No duplicate ticket names detected
   - [x] User permissions verified
   
   ### Warnings
   [Any validation warnings or recommendations]
   
   ## Story Points Customization
   **Current Total**: [Total Points] points
   
   You can modify story points below. Use Fibonacci numbers (1,2,3,5,8,13,21).
   See [story-points-guide.md](story-points-guide.md) for guidelines.
   
   | Task | Current Points | Suggested Range | Modify |
   |------|----------------|-----------------|---------|
   | 1. I/O Mapping | 3 | 1-8 | [ ] |
   | 2. Hardware Dependencies | 5 | 2-13 | [ ] |
   | ... (all 9 tasks)
   
   ## Planned Tickets
   [List of 9 tickets with enhanced descriptions]
   
   ## Dependency Relationships
   [Visual representation of links]
   
   ## Epic Structure
   [Hierarchy showing initiative → epic → tasks]
   
   ## Next Steps
   1. Review story points and modify if needed
   2. Verify all configurations are correct
   3. Confirm to proceed with ticket creation
   ```

3. **Batch Mode Plan Generation**:
   For multiple managers, use batch template with combined overview and individual manager sections.

### Enhanced Ticket Creation Process (After Confirmation)

1. **Create Checkpoint**:
   ```javascript
   const checkpoint = {
     timestamp: new Date().toISOString(),
     manager_name: manager_name,
     epic_id: manager_epic_id,
     total_tasks: 9,
     completed_tickets: [],
     completed_links: [],
     failed_operations: [],
     current_step: "initialization"
   };
   writeFile(`checkpoint_${manager_name}_${timestamp}.json`, JSON.stringify(checkpoint));
   ```

2. **Progressive Task Creation with Error Recovery**:
   ```javascript
   for (let i = 0; i < tasks.length; i++) {
     try {
       const result = await CallMcpTool({
         server: "user-atlassian-mcp-kata",
         toolName: "createJiraIssue",
         arguments: {
           cloudId: "eadd00c6-0d3f-4c89-99e3-ad95a0daaa51",
           projectKey: "KATA",
           issueTypeName: "Task",
           summary: `${tasks[i].description}`,
           description: `K1 Hardware Development Task\n\nManager: ${manager_name}\nInitiative: KATA-1760\nEpic: ${manager_epic_id}\n\nTask: ${tasks[i].detailed_description}\n\nCreated via JIRA MCP`,
           additional_fields: {
             priority: {"name": priority},
             parent: {"key": manager_epic_id},
             customfield_10104: {"id": release_id},
             customfield_10137: tasks[i].story_points
           }
         }
       });
       
       // Update checkpoint on success
       checkpoint.completed_tickets.push({
         task_number: i + 1,
         ticket_id: result.key,
         summary: tasks[i].description
       });
       updateCheckpoint(checkpoint);
       
     } catch (error) {
       // Pause on error and generate recovery plan
       checkpoint.failed_operations.push({
         operation: "create_ticket",
         task_number: i + 1,
         error: error.message,
         timestamp: new Date().toISOString()
       });
       
       const recoveryPlan = generateRecoveryPlan(checkpoint, error);
       writeFile(`recovery_${manager_name}_${timestamp}.md`, recoveryPlan);
       
       throw new Error(`Ticket creation failed at task ${i + 1}. Recovery plan generated.`);
     }
   }
   ```

3. **Progressive Link Creation with Error Recovery**:
   ```javascript
   for (const linkDef of linkDefinitions) {
     try {
       const result = await CallMcpTool({
         server: "user-atlassian-mcp-kata",
         toolName: "createIssueLink",
         arguments: {
           cloudId: "eadd00c6-0d3f-4c89-99e3-ad95a0daaa51",
           inwardIssue: linkDef.inward_ticket_id,
           outwardIssue: linkDef.outward_ticket_id,
           type: linkDef.link_type,
           comment: "Dependency created via K1 HW template"
         }
       });
       
       checkpoint.completed_links.push({
         inward: linkDef.inward_ticket_id,
         outward: linkDef.outward_ticket_id,
         type: linkDef.link_type
       });
       updateCheckpoint(checkpoint);
       
     } catch (error) {
       // Log link failure but continue with others
       checkpoint.failed_operations.push({
         operation: "create_link",
         link: `${linkDef.inward_ticket_id} ${linkDef.link_type} ${linkDef.outward_ticket_id}`,
         error: error.message,
         timestamp: new Date().toISOString()
       });
       
       // Continue with remaining links rather than stopping
       console.warn(`Link creation failed: ${error.message}`);
     }
   }
   ```

4. **Validation History Update**:
   ```javascript
   // Update validation history with results
   const history = JSON.parse(readFile("validation-history.json"));
   history.history.push({
     timestamp: new Date().toISOString(),
     manager_name: manager_name,
     epic_id: manager_epic_id,
     success: checkpoint.failed_operations.length === 0,
     tickets_created: checkpoint.completed_tickets.length,
     links_created: checkpoint.completed_links.length,
     failures: checkpoint.failed_operations,
     story_points_total: tasks.reduce((sum, task) => sum + task.story_points, 0)
   });
   
   // Update statistics
   history.statistics.total_runs++;
   if (checkpoint.failed_operations.length === 0) {
     history.statistics.successful_runs++;
   } else {
     history.statistics.failed_runs++;
   }
   
   writeFile("validation-history.json", JSON.stringify(history, null, 2));
   ```

## Task Template Mapping

Standard K1 hardware development tasks:
1. **I/O Mapping**: List input/output mappings for {manager_name}
2. **Hardware Dependencies**: List hardware dependencies for application functionality
3. **Zonal Allocation**: Establish zonal allocation for manager software
4. **Subsystem Diagrams**: Draw subsystem diagrams on shared miro board
5. **Functional Requirements**: Draft functional requirements for {manager_name} manager
6. **Performance Requirements**: Draft performance requirements for {manager_name} manager
7. **State Machine**: State machine development for {manager_name}
8. **Physical Allocation**: Allocate physical HW for placement on truck bench
9. **HW Bringup**: HW bringup for {manager_name} on K1 bench

## Dependency Patterns

Common dependency relationships:
- **Sequential**: Tasks 1→2→3 (each blocks the next)
- **Parallel branches**: Tasks can have independent parallel tracks
- **Convergence**: Multiple tasks feeding into final integration
- **Related**: Tasks that share context but don't block each other

## Release Mapping (KATA)

| Release Name | Field ID | Usage |
|--------------|----------|-------|
| Release 25.1 | 10000 | Legacy |
| Release 25.2 | 10001 | Legacy |
| Release 25.3 | 10036 | Current |
| Release 26.1 | 10002 | Default |
| Release 26.2 | 10003 | Future |

## Epic Structure

```
KATA-1760 (Initiative: K1 Hardware Manager Development)
├── KATA-XXXX (Epic: PowerManager Development)
│   ├── KATA-YYYY (Task 1: List out input/output mappings for PowerManager)
│   ├── KATA-YYYY (Task 2: List out HW dependencies for application functionality)
│   └── ... (Tasks 3-7)
├── KATA-XXXX (Epic: ThermalManager Development)
│   ├── KATA-YYYY (Task 1: List out input/output mappings for ThermalManager)
│   └── ... (Tasks 2-7)
└── ... (Other Manager Epics)
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
      story_points: [3,5,8,5,5,3,13,3,8], // optional custom points
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
- Maintains `validation-history.json` with past successes/failures
- Learns from common failure patterns
- Provides proactive warnings based on historical data

### Pre-flight Validation Checks
- **Epic Validation**: Verify epic exists and is linked to KATA-1760
- **Permission Check**: Confirm user can create tickets in target epic
- **Release Validation**: Ensure release version exists in JIRA project
- **Duplicate Detection**: Check for existing tickets with similar names
- **Connectivity Test**: Verify JIRA and MCP server accessibility

### Smart Warnings
Based on validation history, the system warns about:
- Epic IDs that have failed before
- Release versions that are commonly invalid
- Manager names that typically cause issues
- Permission problems for specific users

## Error Recovery System

### Checkpoint-Based Recovery
- Creates checkpoint files before starting JIRA operations
- Tracks progress of ticket and link creation
- Enables resuming from last successful operation

### Recovery Options
When failures occur, users can choose:

1. **Retry Failed Operations**: Attempt failed items again
2. **Skip and Continue**: Mark failed items as completed, continue with rest
3. **Rollback**: Delete all created tickets/links and start fresh
4. **Manual Intervention**: Pause for manual JIRA operations, then resume

### Recovery Plan Generation
Automatic generation of detailed recovery plans including:
- Current state (completed vs failed operations)
- Error analysis and recommended actions
- Specific commands for each recovery option
- Prevention tips for future runs

### Transaction Logging
- Complete audit trail of all operations
- Detailed error messages and context
- Timestamps for all operations
- Rollback information for created items

## Error Handling

### Smart Error Handling
- **Missing manager name**: Prompt user for specific manager
- **Invalid manager epic ID**: Reject non-KATA prefixed epics, check validation history
- **Epic not linked to KATA-1760**: Error with specific linkage instructions
- **Permission denied**: Check validation history for user permission patterns
- **Link creation failure**: Log failed links, continue with remaining, offer recovery
- **MCP unavailable**: Generate recovery plan, offer retry options
- **Duplicate tickets**: Smart detection and user choice to skip or rename

### Failure Isolation
- In batch mode, manager failures are isolated
- Partial successes are preserved and reported
- Recovery plans are generated per manager
- Cross-manager dependencies are avoided

## Enhanced Plan.md Format

The generated plan file includes validation results and story points customization:

```markdown
# K1 Hardware Development Plan: [Manager Name]

Generated: [timestamp]

## Overview
- **Manager**: [Manager Name]
- **Epic**: [Epic ID] - [Manager Name] Development
- **Initiative**: KATA-1760 - K1 Hardware Manager Development
- **Release**: [Release Name]
- **Priority**: [Priority Level]
- **Assignee**: Unassigned
- **Total Tasks**: 9
- **Estimated Points**: [Total Points]

## Validation Results

### Pre-flight Checks
- [x] JIRA connectivity verified
- [x] Epic exists and is linked to KATA-1760
- [x] Release version is valid
- [x] No duplicate ticket names detected
- [x] User permissions verified

### Warnings
[Any validation warnings based on history]
- ⚠️ Epic KATA-XXXX had permission issues in previous runs
- ⚠️ Release 26.1 validation recommended
- ⚠️ All tasks have 0 story points - estimation required before proceeding
- ✅ Manager name follows consistent pattern

## Story Points Customization

**Current Total**: [Total Points] points (⚠️ All tasks default to 0 - estimation required)

**IMPORTANT**: Story points must be estimated for each task. Use Fibonacci numbers (1,2,3,5,8,13,21).
See [story-points-guide.md](story-points-guide.md) for detailed guidelines.

| Task | Description | Current | Suggested Range | Complexity Factors |
|------|-------------|---------|-----------------|-------------------|
| 1 | I/O Mapping | 0 ⚠️ | 1-8 | Signal count, protocol complexity |
| 2 | Hardware Dependencies | 0 ⚠️ | 2-13 | Component count, spec availability |
| 3 | Zonal Allocation | 0 ⚠️ | 3-13 | Options analysis, constraints |
| 4 | Subsystem Diagrams | 0 ⚠️ | 3-13 | Diagram complexity, detail level |
| 5 | Functional Requirements | 0 ⚠️ | 3-13 | Requirement complexity, novelty |
| 6 | Performance Requirements | 0 ⚠️ | 1-8 | Criteria count, modeling needs |
| 7 | State Machine Development | 0 ⚠️ | 8-21 | States, transitions, complexity |
| 8 | Physical Allocation | 0 ⚠️ | 1-8 | Setup complexity, custom needs |
| 9 | Hardware Bringup | 0 ⚠️ | 5-13 | Hardware complexity, validation |

**To modify story points**: Edit the values above and confirm changes.

## Planned Tickets

### 1. List out input/output mappings for [Manager]
**Description**: K1 Hardware Development Task
Manager: [Manager Name]
Initiative: KATA-1760
Epic: [Epic ID]
Release: [Release Name]
Story Points: [Customizable Points]
Assignee: Unassigned

Task: [Enhanced detailed task description based on user feedback]

Created via JIRA MCP

[... continues for all 9 tasks with enhanced descriptions]

## Dependency Relationships

The following 11 links will be created:
- Task 9 (HW bringup for [Manager] on K1 bench) **is blocked by** Task 8 (Allocate physical HW)
- Task 8 (Allocate physical HW) **is blocked by** Task 3 (Zonal allocation)
- Task 3 (Zonal allocation) **is blocked by** Task 2 (Hardware dependencies)
- Task 2 (Hardware dependencies) **is blocked by** Task 1 (I/O mappings)
- Task 1 (I/O mappings) **relates to** Task 2 (Hardware dependencies)
- Task 7 (State machine development) **is blocked by** Task 5 (Functional requirements)
- Task 7 (State machine development) **is blocked by** Task 6 (Performance requirements)
- Task 5 (Functional requirements) **relates to** Task 6 (Performance requirements)
- Task 5 (Functional requirements) **is blocked by** Task 4 (Subsystem diagrams)
- Task 6 (Performance requirements) **is blocked by** Task 4 (Subsystem diagrams)
- Task 4 (Subsystem diagrams) **is blocked by** Task 1 (I/O mappings)

## Epic Structure
```
KATA-1760: K1 Hardware Manager Development (Initiative)
└── [Epic ID]: [Manager Name] Development (Epic)
    ├── List out input/output mappings for [Manager]
    ├── List out hardware dependencies for application functionality
    ├── Establish zonal allocation for manager software
    ├── Draw subsystem diagrams on shared miro board
    ├── Draft functional requirements for [Manager] manager
    ├── Draft performance requirements for [Manager] manager
    ├── State machine development for [Manager]
    ├── Allocate physical HW for placement on truck bench
    └── HW bringup for [Manager] on K1 bench
```

## Next Steps
1. Review validation results and address any warnings
2. Customize story points if needed using the table above
3. Verify all configurations are correct
4. Confirm to proceed with ticket creation

## Recovery Information
Checkpoint file will be created: `checkpoint_[Manager]_[timestamp].json`
Recovery plan will be available if needed: `recovery_[Manager]_[timestamp].md`
```

## Batch Plan Format

For multiple managers, the plan includes:
- Combined overview with total tasks and points across all managers
- Individual validation results per manager
- Story points customization table for each manager
- Batch execution plan with failure isolation
- Combined epic structure showing all managers

## Enhanced Output Format (After Creation)

### Single Manager Success
```
📋 Generated enhanced plan: plan.md
🔍 Validation completed: 5/5 checks passed
📊 Story points customized: 45 total points (3 tasks modified)

✅ Created 9 K1 Hardware Development tickets for AutoLube:
- KATA-1234: List out input/output mappings for AutoLube (3 pts)
- KATA-1235: List out hardware dependencies for application functionality (8 pts)
- KATA-1236: Establish zonal allocation for manager software (5 pts)
- ... (6 more)

✅ Created 11 issue links:
- KATA-1243 blocks KATA-1242 (HW bringup → Physical allocation)
- KATA-1242 blocks KATA-1236 (Physical allocation → Zonal allocation)
- KATA-1241 relates KATA-1240 (Functional ↔ Performance requirements)
- ... (8 more)

📈 Updated validation history: Success rate for AutoLube: 100%
💾 Checkpoint completed successfully: checkpoint_AutoLube_20260311.json
```

### Batch Mode Success
```
📋 Generated batch plan: batch_plan_20260311.md
🔍 Batch validation: 3 managers validated successfully

✅ Batch creation completed:
- AutoLube: 9 tickets, 11 links (45 pts) ✅
- ThermalManager: 9 tickets, 11 links (52 pts) ✅  
- PowerManager: 9 tickets, 11 links (48 pts) ✅

📊 Batch Summary:
- Total tickets: 27
- Total links: 33
- Total story points: 145
- Success rate: 100%
- Duration: 3m 24s

📈 Validation history updated for all managers
```

### Error Recovery Output
```
📋 Generated plan: plan.md
🔍 Validation completed with warnings

⚠️ Ticket creation paused at task 5/9
❌ Error: Permission denied for epic KATA-2800

🔧 Recovery plan generated: recovery_AutoLube_20260311.md
📊 Current state:
- Completed tickets: 4/9
- Completed links: 3/11
- Failed operation: Create ticket #5

🔄 Recovery options:
1. Retry failed operations (recommended)
2. Skip failed items and continue
3. Rollback all created items
4. Manual intervention mode

💾 Checkpoint saved: checkpoint_AutoLube_20260311.json
📈 Failure pattern logged for future prevention
```

### Validation Warning Output
```
📋 Generated plan: plan.md
🔍 Validation completed with warnings

⚠️ Validation warnings:
- Epic KATA-2800 had permission issues in 2 previous runs
- Release "Release 26.1" not found in recent project versions
- Manager name "AutoLube" is new (no historical data)

💡 Recommendations:
- Verify epic permissions before proceeding
- Consider using "Release 26.2" instead
- Proceed with caution for new manager type

✅ Pre-flight checks:
- JIRA connectivity: OK
- User permissions: OK (with warnings)
- Epic existence: OK
- No duplicate tickets: OK

🔄 Proceed with creation? Review warnings and confirm.
```