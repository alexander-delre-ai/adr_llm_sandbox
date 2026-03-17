# Auto Lube (P0) - Corrections Needed

**Generated:** March 11, 2026

## Issues Identified
1. ❌ **All dependency directions are flipped** - I created "blocks" relationships backwards
2. ❌ **Task 11 (Power validation) should not exist** for future managers
3. ❌ **Used Release 26.2** instead of the requested Release 2026.1 (not available in system)

## Manual Corrections Required in JIRA

### Auto Lube Epic: KATA-2611
The following dependency links need to be **manually corrected** in JIRA (all are currently backwards):

#### Current (WRONG) → Should Be (CORRECT)
1. **KATA-2613 blocks KATA-2612** → **KATA-2612 blocks KATA-2613**
2. **KATA-2614 blocks KATA-2613** → **KATA-2613 blocks KATA-2614** 
3. **KATA-2615 blocks KATA-2612** → **KATA-2612 blocks KATA-2615**
4. **KATA-2616 blocks KATA-2612** → **KATA-2612 blocks KATA-2616**
5. **KATA-2617 blocks KATA-2615** → **KATA-2615 blocks KATA-2617**
6. **KATA-2617 blocks KATA-2616** → **KATA-2616 blocks KATA-2617**
7. **KATA-2618 blocks KATA-2617** → **KATA-2617 blocks KATA-2618**
8. **KATA-2619 blocks KATA-2617** → **KATA-2617 blocks KATA-2619**
9. **KATA-2620 blocks KATA-2615** → **KATA-2615 blocks KATA-2620**
10. **KATA-2620 blocks KATA-2616** → **KATA-2616 blocks KATA-2620**
11. **KATA-2621 blocks KATA-2614** → **KATA-2614 blocks KATA-2621**
12. **KATA-2622 blocks KATA-2621** → **KATA-2621 blocks KATA-2622**
13. **KATA-2623 blocks KATA-2622** → **KATA-2622 blocks KATA-2623**

#### Correct Links (should remain as-is)
- **KATA-2612 relates to KATA-2613** ✅ (bidirectional, correct)
- **KATA-2615 relates to KATA-2616** ✅ (bidirectional, correct)

## Skill Updates Completed ✅

I have updated the skill for future managers:

### Template Changes:
- ✅ **Removed Task 11** (Power and signal validation)
- ✅ **Updated to 11 tasks** instead of 12
- ✅ **Fixed all dependency directions** in template
- ✅ **Updated story points guide** to reflect 11 tasks
- ✅ **Corrected link count** to 14 total dependencies

### New Corrected Template (11 tasks):
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
1 blocks 2
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

## Next Steps

1. **Manual Fix Required**: Please manually correct the 13 flipped dependency links in JIRA for Auto Lube (KATA-2611)
2. **Confirmation**: Once dependencies are fixed, confirm if Auto Lube looks correct
3. **Proceed with P1**: I'm ready to create P1 managers with the corrected 11-task template

## P1 Managers Ready for Creation (11 tasks each):
- Engine Interface (CAN)
- Low Voltage Power  
- Chassis Brakes
- Shutdown Processes
- Drive System Interface
- Cab Components
- Operator Displays

All future managers will use the corrected template with proper dependency directions and no Task 11.