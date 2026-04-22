# App Dev K1 HW Ticket Creation Examples

## Enhanced Features Overview

This skill now includes:
- **Smart Validation**: Pre-flight checks with historical learning
- **Story Points Customization**: Interactive modification during plan review
- **Error Recovery**: Checkpoint-based recovery with multiple options
- **Batch Processing**: Multi-manager support with failure isolation

## Single Manager Example (Enhanced)

### Input Template
```markdown
## Manager: AutoLube

1. List out input/output mappings for AutoLube
2. List out hardware dependencies for application functionality
3. Establish zonal allocation for manager software 
4. Draw subsystem diagrams on shared miro board
5. State machine development for AutoLube 
6. Allocate physical HW for placement on truck bench
7. HW bringup for AutoLube on K1 bench

## Jira ticket link types:
7 is blocked by 6.
6 is blocked by 3
3 is blocked by 2 
2 is blocked by 1
1 and 2 are related
5 is blocked by 4
4 is blocked by 1
```

### Skill Invocation
```
User: "Create JIRA tickets using the K1 HW template for AutoLube epic KATA-2800"

Parameters:
- manager_name: "AutoLube"
- manager_epic_id: "KATA-2800"
- release: "Release 26.1" (default)
- priority: "P2" (default)
- assignee: "Unassigned" (default)

Auto-configured:
- project: "KATA"
- initiative_id: "KATA-1760"
- labels: "k1-hardware,app-dev,AutoLube"
```

### Step 1: Plan Generation
The skill first creates a `plan.md` file for review:

```markdown
# K1 Hardware Development Plan: AutoLube

Generated: 2026-03-11 15:30:00

## Overview
- **Manager**: AutoLube
- **Epic**: KATA-2800 - AutoLube Development
- **Initiative**: KATA-1760 - K1 Hardware Manager Development
- **Release**: Release 26.1
- **Priority**: P2
- **Assignee**: Unassigned
- **Labels**: k1-hardware,app-dev,AutoLube

## Planned Tickets

### 1. [AutoLube] List out input/output mappings for AutoLube
**Description**: K1 Hardware Development Task

Manager: AutoLube
Initiative: KATA-1760
Epic: KATA-2800

Task: List out input/output mappings for AutoLube

Created via App Dev K1 HW template

### 2. [AutoLube] List out hardware dependencies for application functionality
**Description**: K1 Hardware Development Task

Manager: AutoLube
Initiative: KATA-1760
Epic: KATA-2800

Task: List out hardware dependencies for application functionality

Created via App Dev K1 HW template

[... continues for tasks 3-7]

## Dependency Relationships

The following links will be created:
- Task 7 (HW bringup for AutoLube on K1 bench) **is blocked by** Task 6 (Allocate physical HW for placement on truck bench)
- Task 6 (Allocate physical HW for placement on truck bench) **is blocked by** Task 3 (Establish zonal allocation for manager software)
- Task 3 (Establish zonal allocation for manager software) **is blocked by** Task 2 (List out hardware dependencies for application functionality)
- Task 2 (List out hardware dependencies for application functionality) **is blocked by** Task 1 (List out input/output mappings for AutoLube)
- Task 1 (List out input/output mappings for AutoLube) **relates to** Task 2 (List out hardware dependencies for application functionality)
- Task 5 (State machine development for AutoLube) **is blocked by** Task 4 (Draw subsystem diagrams on shared miro board)
- Task 4 (Draw subsystem diagrams on shared miro board) **is blocked by** Task 1 (List out input/output mappings for AutoLube)

## Epic Structure
```
KATA-1760: K1 Hardware Manager Development (Initiative)
└── KATA-2800: AutoLube Development (Epic)
    ├── [AutoLube] List out input/output mappings for AutoLube
    ├── [AutoLube] List out hardware dependencies for application functionality
    ├── [AutoLube] Establish zonal allocation for manager software
    ├── [AutoLube] Draw subsystem diagrams on shared miro board
    ├── [AutoLube] State machine development for AutoLube
    ├── [AutoLube] Allocate physical HW for placement on truck bench
    └── [AutoLube] HW bringup for AutoLube on K1 bench
```

## Next Steps
Review this plan and confirm to proceed with JIRA ticket creation.
```

### Step 2: Enhanced Plan Review with Validation
```
Assistant: "📋 I've generated an enhanced plan for the AutoLube K1 hardware development tickets.

🔍 Validation Results:
- ✅ Epic KATA-2800 exists and is linked to KATA-1760
- ✅ Release 26.1 is valid
- ✅ No duplicate ticket names detected
- ⚠️ Manager 'AutoLube' is new (no historical data)

📊 Story Points Summary: 0 total points (⚠️ Estimation required)
You must estimate story points for each task before proceeding.

Please review plan.md and let me know if you'd like to:
1. Proceed with ticket creation
2. Modify story points 
3. Adjust any other parameters"

User: "I need to estimate story points. Let me set: I/O Mapping=3, Hardware Dependencies=5, Zonal Allocation=8, Diagrams=5, Functional Req=5, Performance Req=3, State Machine=21, Physical Allocation=3, HW Bringup=8"

### Step 3: Generated Tickets (After Confirmation)
```
KATA-1234: [AutoLube] List out input/output mappings for AutoLube
KATA-1235: [AutoLube] List out hardware dependencies for application functionality
KATA-1236: [AutoLube] Establish zonal allocation for manager software
KATA-1237: [AutoLube] Draw subsystem diagrams on shared miro board
KATA-1238: [AutoLube] State machine development for AutoLube
KATA-1239: [AutoLube] Allocate physical HW for placement on truck bench
KATA-1240: [AutoLube] HW bringup for AutoLube on K1 bench
```

### Generated Links
```
KATA-1240 is blocked by KATA-1239  (HW bringup ← Physical allocation)
KATA-1239 is blocked by KATA-1236  (Physical allocation ← Zonal allocation)
KATA-1236 is blocked by KATA-1235  (Zonal allocation ← Hardware dependencies)
KATA-1235 is blocked by KATA-1234  (Hardware dependencies ← I/O mappings)
KATA-1234 relates to KATA-1235     (I/O mappings ↔ Hardware dependencies)
KATA-1238 is blocked by KATA-1237  (State machine ← Subsystem diagrams)
KATA-1237 is blocked by KATA-1234  (Subsystem diagrams ← I/O mappings)
```

## Different Manager Examples

### ThermalManager
```markdown
## Manager: ThermalManager

1. List out input/output mappings for ThermalManager
2. List out hardware dependencies for application functionality
3. Establish zonal allocation for manager software 
4. Draw subsystem diagrams on shared miro board
5. State machine development for ThermalManager 
6. Allocate physical HW for placement on truck bench
7. HW bringup for ThermalManager on K1 bench
```

Generated tickets would use "ThermalManager" in titles and descriptions.

### BatteryManager
```markdown
## Manager: BatteryManager

1. List out input/output mappings for BatteryManager
2. List out hardware dependencies for application functionality
3. Establish zonal allocation for manager software 
4. Draw subsystem diagrams on shared miro board
5. State machine development for BatteryManager 
6. Allocate physical HW for placement on truck bench
7. HW bringup for BatteryManager on K1 bench
```

## Link Type Variations

### Alternative Dependency Pattern
```markdown
## Jira ticket link types:
7 is blocked by 6.
6 is blocked by 5.
5 is blocked by 4.
4 is blocked by 3.
3 is blocked by 2.
2 is blocked by 1.
1 and 7 are related
```

This creates a linear dependency chain: 1→2→3→4→5→6→7 with 1 and 7 related.

### Parallel Development Pattern
```markdown
## Jira ticket link types:
3 is blocked by 1
3 is blocked by 2
6 is blocked by 4
6 is blocked by 5
7 is blocked by 3
7 is blocked by 6
1 and 4 are related
2 and 5 are related
```

This creates two parallel tracks that converge:
- Track A: 1→3→7
- Track B: 4→6→7
- Track C: 2→3→7
- Track D: 5→6→7

## Plan Review and Modifications

### Plan Approval
```
User: "The plan looks perfect, proceed with creation."
→ Skill proceeds to create JIRA tickets
```

### Plan Modifications
```
User: "Change the assignee to Alex Del Re and priority to P1"
→ Skill updates plan.md with new parameters
→ Regenerates plan for review
→ Waits for confirmation again
```

### Plan Rejection
```
User: "Actually, let's not create these tickets right now."
→ Skill stops execution
→ plan.md remains for future reference
```

## Error Recovery Examples

### Permission Error with Smart Recovery
```
🔄 Creating tickets for AutoLube...
✅ Tickets 1-4 created successfully
❌ Ticket 5 failed: Permission denied for epic KATA-2800

🔧 Smart Analysis:
- Historical data shows KATA-2800 had permission issues 2 times before
- User permissions may have changed recently
- 4 tickets already created successfully

📋 Recovery Plan Generated: recovery_AutoLube_20260311.md

Recovery Options:
1. **Retry (Recommended)**: Permission may be temporary
2. **Skip Task 5**: Continue with remaining tasks 6-9
3. **Rollback**: Delete tickets 1-4 and start fresh
4. **Manual Fix**: Pause for manual permission resolution

💾 Current state saved in: checkpoint_AutoLube_20260311.json

User: "Let me fix permissions manually, then retry"
Assistant: "✅ Manual intervention mode activated. Resume when ready with checkpoint file."
```

### Link Creation Failure with Continuation
```
✅ All 9 tickets created successfully for AutoLube
🔄 Creating issue links...
✅ Links 1-8 created successfully
❌ Link 9 failed: Link type 'Relates' not available
✅ Links 10-11 created successfully

📊 Final Result:
- Tickets: 9/9 created ✅
- Links: 10/11 created ⚠️
- Failed: Task 5 relates to Task 6 (link type unavailable)

💡 Recommendation: Links can be created manually in JIRA if needed
📈 Validation history updated: Link type issue logged for future prevention
```

### Smart Validation Prevention
```
User: "Create tickets for PowerManager epic KATA-9999"

🔍 Smart Validation Results:
❌ Epic KATA-9999 does not exist
⚠️ Similar epic ID KATA-2999 failed 3 times in history
💡 Did you mean KATA-2900 (PowerManager Development)?

🛡️ Preventing common issues:
- Epic existence verified before proceeding
- Historical failure patterns checked
- Suggested alternatives provided

Please verify the correct epic ID before proceeding.
```

## Advanced Usage Scenarios

### Story Points Estimation Example
```
📊 Story Points Estimation for AutoLube:

Initial state (0 total points - estimation required):
| Task | Description | Current | Suggested Range |
|------|-------------|---------|-----------------|
| 1 | I/O Mapping | 0 ⚠️ | 1-8 |
| 2 | Hardware Dependencies | 0 ⚠️ | 2-13 |
| 7 | State Machine Development | 0 ⚠️ | 8-21 |

User estimations:
- Task 1: 0 → 3 (standard I/O mapping complexity)
- Task 2: 0 → 8 (complex hardware integration expected)
- Task 7: 0 → 21 (very complex state machine)
- [... all other tasks estimated]

Final total: 61 points (all tasks estimated)

✅ All values are valid Fibonacci numbers
✅ No tasks left at 0 points
📊 Updated plan with estimated story points
```

### Historical Learning Example
```
🔍 Smart Validation for ThermalManager:

📈 Historical Analysis:
- ThermalManager created successfully 3 times before
- Average story points: 48 (current plan: 45)
- Common issues: None detected
- Success rate: 100%

💡 Recommendations based on history:
- Consider 5 points for Hardware Dependencies (was 8 in previous runs)
- State Machine typically needs 13 points for ThermalManager
- No permission issues expected for this manager type

✅ High confidence prediction: Success likely
```

## Error Scenarios (Enhanced)

### Smart Error Detection
```
Template: "## Manager: {manager_name}"
🔍 Smart Analysis: Manager name placeholder not replaced
💡 Auto-suggestion: Did you mean to use "AutoLube" based on recent usage?
Error: "Manager name placeholder not replaced. Please provide manager_name parameter."
```

### Enhanced Epic Validation
```
Input: manager_epic_id = "KATA-9999"
🔍 Validation Results:
❌ Epic KATA-9999 does not exist in KATA project
🔍 Historical check: Similar pattern "KATA-999X" failed 5 times
💡 Suggestions: 
  - KATA-2800 (AutoLube Development) - 90% match
  - KATA-2810 (ThermalManager Development) - 75% match
Error: "Epic not found. Smart suggestions provided based on historical data."
```

### Proactive Link Type Validation
```
Template dependency: "5 and 6 are related"
🔍 Pre-validation: Checking available link types...
⚠️ Warning: "Relates" link type success rate only 60% in this JIRA instance
💡 Alternative: "Dependency" link type has 95% success rate
Recommendation: "Consider using 'Dependency' instead of 'Relates' for better reliability"
```

## Initiative Structure Example

### KATA-1760 Initiative Hierarchy
```
KATA-1760: K1 Hardware Manager Development (Initiative)
├── KATA-2800: AutoLube Development (Epic)
│   ├── KATA-2801: [AutoLube] List out input/output mappings for AutoLube
│   ├── KATA-2802: [AutoLube] List out hardware dependencies for application functionality
│   ├── KATA-2803: [AutoLube] Establish zonal allocation for manager software
│   ├── KATA-2804: [AutoLube] Draw subsystem diagrams on shared miro board
│   ├── KATA-2805: [AutoLube] State machine development for AutoLube
│   ├── KATA-2806: [AutoLube] Allocate physical HW for placement on truck bench
│   └── KATA-2807: [AutoLube] HW bringup for AutoLube on K1 bench
├── KATA-2810: ThermalManager Development (Epic)
│   ├── KATA-2811: [ThermalManager] List out input/output mappings for ThermalManager
│   └── ... (6 more tasks)
└── KATA-2820: BatteryManager Development (Epic)
    ├── KATA-2821: [BatteryManager] List out input/output mappings for BatteryManager
    └── ... (6 more tasks)
```

## Batch Processing Example

## Batch Processing Example

### Multiple Managers with Enhanced Features
```
User: "Create tickets for AutoLube, ThermalManager, and BatteryManager using the K1 template in batch mode"

Parameters:
- batch_mode: true
- managers_list: [
    {
      manager_name: "AutoLube",
      manager_epic_id: "KATA-2800",
      priority: "P1"
    },
    {
      manager_name: "ThermalManager", 
      manager_epic_id: "KATA-2810",
      story_points: [2,3,5,3,5,2,8,2,5], // custom points
      priority: "P2"
    },
    {
      manager_name: "BatteryManager",
      manager_epic_id: "KATA-2820",
      priority: "P2"
    }
  ]
```

### Batch Plan Generation
```
📋 Generated batch plan: batch_plan_20260311.md

🔍 Batch Validation Results:
- ✅ All 3 epics exist and linked to KATA-1760
- ✅ Release 26.1 valid for all managers
- ⚠️ ThermalManager had 1 permission issue in previous runs
- ✅ No duplicate ticket names across all managers

📊 Batch Summary:
- Total managers: 3
- Total tasks: 27 (9 per manager)
- Total links: 33 (11 per manager)
- Estimated points: 0 total (⚠️ Estimation required for all managers)
  - AutoLube: 0 points (needs estimation)
  - ThermalManager: 0 points (needs estimation) 
  - BatteryManager: 0 points (needs estimation)

## Story Points Customization (Per Manager)
[Interactive table allowing modification of points for each manager]

## Batch Execution Plan
1. Pre-validate all 3 managers
2. Create AutoLube tickets and links
3. Create ThermalManager tickets and links  
4. Create BatteryManager tickets and links
5. Generate combined report

Note: Each manager processed independently - failure in one won't affect others.
```

### Batch Execution with Partial Failure
```
Assistant: "🔄 Starting batch creation for 3 managers..."

✅ AutoLube: 9 tickets, 11 links created successfully (45 pts)
❌ ThermalManager: Failed at ticket 6/9 (Permission denied)
⏸️ BatteryManager: Paused due to ThermalManager failure

🔧 Recovery options for ThermalManager:
1. Retry failed operations (recommended)
2. Skip ThermalManager, continue with BatteryManager
3. Manual intervention for ThermalManager permissions

Current state saved: checkpoint_batch_20260311.json
Recovery plan: recovery_ThermalManager_20260311.md

What would you like to do?
```

## Custom Task Descriptions

### Modified Template
```markdown
## Manager: CustomManager

1. Define interface specifications for CustomManager
2. Analyze hardware compatibility requirements
3. Design software architecture and zonal mapping
4. Create detailed system diagrams
5. Implement state machine logic for CustomManager
6. Configure hardware test environment
7. Execute full integration testing on K1 platform
```

The skill adapts to any task descriptions while maintaining the 7-task structure and dependency parsing.