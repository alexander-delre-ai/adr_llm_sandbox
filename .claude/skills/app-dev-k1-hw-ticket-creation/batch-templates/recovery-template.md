# K1 Hardware Development Recovery Plan

Generated: {timestamp}
Recovery from: {original_plan_file}

## Recovery Overview
- **Manager**: {manager_name}
- **Epic**: {epic_id}
- **Failure Point**: {failure_point}
- **Completed Tasks**: {completed_count}/{total_tasks}
- **Failed Operation**: {failed_operation}

## Current State

### Successfully Created Tickets
{completed_tickets}

### Failed Tickets
{failed_tickets}

### Successfully Created Links
{completed_links}

### Failed Links
{failed_links}

## Error Details

**Primary Error**: {primary_error}
**Error Context**: {error_context}
**Timestamp**: {error_timestamp}

## Recovery Options

### Option 1: Retry Failed Operations
- Attempt to create failed tickets/links again
- Preserves all successfully created items
- **Risk**: May fail again if underlying issue not resolved

### Option 2: Skip and Continue
- Skip failed items and mark as completed
- Continue with remaining operations
- **Risk**: Incomplete ticket set, missing dependencies

### Option 3: Rollback and Restart
- Delete all successfully created tickets and links
- Start fresh with original plan
- **Risk**: Loses progress, may hit same error again

### Option 4: Manual Intervention
- Pause automation, allow manual JIRA operations
- Resume automation after manual fixes
- **Risk**: Requires manual JIRA knowledge

## Recommended Action

Based on error analysis: **{recommended_action}**

Reasoning: {recommendation_reasoning}

## Recovery Commands

### To Retry Failed Operations:
```
Resume from checkpoint: {checkpoint_file}
Retry failed items: {failed_items_list}
```

### To Rollback:
```
Delete created tickets: {created_ticket_ids}
Delete created links: {created_link_ids}
Reset to clean state
```

### To Skip and Continue:
```
Mark as completed: {failed_items_list}
Continue with: {remaining_operations}
```

## Prevention for Next Time

Based on this failure:
- {prevention_tip_1}
- {prevention_tip_2}
- {prevention_tip_3}

## Audit Log

{audit_log_entries}

---

**Note**: This recovery plan was generated automatically. Review carefully before proceeding.