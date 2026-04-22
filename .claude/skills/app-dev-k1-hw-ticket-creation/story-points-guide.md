# Story Points Guide for K1 Hardware Development Tasks

## Overview
Story points represent the relative effort and complexity of tasks. Use Fibonacci sequence: 1, 2, 3, 5, 8, 13, 21.

## Task Type Guidelines

### 1. I/O Mapping (Default: 0 points - must be estimated)
**Low Complexity (1-2 points)**: Simple manager with few interfaces
**Medium Complexity (3-5 points)**: Standard manager with typical I/O
**High Complexity (8+ points)**: Complex manager with many interfaces, custom protocols

**Factors to consider**:
- Number of input/output signals
- Complexity of signal types (digital, analog, CAN, custom protocols)
- Documentation requirements (Miro, spreadsheet, flowchart)

### 2. Hardware Dependencies (Default: 0 points - must be estimated)
**Low Complexity (2-3 points)**: Well-known components, minimal dependencies
**Medium Complexity (5-8 points)**: Standard hardware with detailed specs needed
**High Complexity (13+ points)**: Custom hardware, complex integration requirements

**Factors to consider**:
- Number of hardware components
- Availability of specifications and documentation
- Integration complexity with existing systems

### 3. Zonal Allocation (Default: 0 points - must be estimated)
**Low Complexity (3-5 points)**: Clear allocation choice, minimal constraints
**Medium Complexity (8 points)**: Standard analysis of zonal vs central compute
**High Complexity (13+ points)**: Complex trade-offs, multiple viable options

**Factors to consider**:
- Number of allocation options to evaluate
- Complexity of proximity and repairability analysis
- Impact on system architecture

### 4. Functional Requirements (Default: 0 points - must be estimated)
**Low Complexity (3 points)**: Well-understood functionality, existing patterns
**Medium Complexity (5-8 points)**: Standard requirements definition
**High Complexity (13+ points)**: Novel functionality, complex operational states

**Factors to consider**:
- Complexity of operational states
- Number of functional requirements
- Novelty of the functionality

### 5. Performance Requirements (Default: 0 points - must be estimated)
**Low Complexity (1-2 points)**: Standard performance criteria
**Medium Complexity (3-5 points)**: Detailed timing and throughput specs
**High Complexity (8+ points)**: Complex performance modeling needed

**Factors to consider**:
- Number of performance criteria
- Complexity of timing constraints
- Need for performance modeling or simulation

### 6. Requirements Sign-off (Default: 0 points - must be estimated)
**Low Complexity (1 point)**: Simple review and approval process
**Medium Complexity (2-3 points)**: Multiple stakeholder review required
**High Complexity (5+ points)**: Complex approval process, multiple iterations

**Factors to consider**:
- Number of stakeholders involved in sign-off
- Complexity of requirements being reviewed
- Expected number of review iterations
- Documentation requirements for approval

### 7. Subsystem Diagrams (Default: 0 points - must be estimated)
**Low Complexity (3 points)**: Simple diagrams, existing templates
**Medium Complexity (5-8 points)**: Standard architecture and connectivity diagrams
**High Complexity (13+ points)**: Complex system interactions, multiple diagram types

**Factors to consider**:
- Number and complexity of diagrams needed
- Level of detail required
- Integration with other vehicle systems

### 8. Test Cases Definition (Default: 0 points - must be estimated)
**Low Complexity (2-3 points)**: Standard test cases, existing patterns
**Medium Complexity (5-8 points)**: Custom test cases, moderate complexity
**High Complexity (13+ points)**: Complex test scenarios, automation required

**Factors to consider**:
- Number of test cases to define
- Complexity of test scenarios
- Need for test automation
- Integration with existing test frameworks

### 9. State Machine Development (Default: 0 points - must be estimated)
**Low Complexity (8 points)**: Simple state machine, few states
**Medium Complexity (13 points)**: Standard complexity state machine
**High Complexity (21+ points)**: Complex state machine with many transitions

**Factors to consider**:
- Number of states and transitions
- Complexity of state logic
- Integration with other system components
- Testing and validation requirements

### 10. Physical Hardware Allocation (Default: 0 points - must be estimated)
**Low Complexity (1-2 points)**: Clear hardware list from dependencies
**Medium Complexity (3-5 points)**: Standard bench allocation
**High Complexity (8+ points)**: Complex setup requirements, custom configurations

**Factors to consider**:
- Complexity of hardware setup
- Custom mounting or configuration needs
- Integration with test equipment

### 11. Hardware Bringup (Default: 0 points - must be estimated)
**Low Complexity (5 points)**: Standard hardware, known procedures
**Medium Complexity (8 points)**: Standard bringup with validation
**High Complexity (13+ points)**: Complex hardware, extensive validation needed

**Factors to consider**:
- Complexity of hardware components
- Extent of validation required
- Integration testing complexity
- Debugging and troubleshooting expected

## Estimation Tips

1. **Consider team experience**: Reduce points if team has done similar work recently
2. **Account for unknowns**: Increase points if requirements are unclear
3. **Factor in dependencies**: Higher points if waiting on other teams/components
4. **Include testing effort**: Points should include validation and testing time
5. **Consider rework risk**: Increase points if high probability of changes

## Validation Rules

- Must use Fibonacci numbers: 1, 2, 3, 5, 8, 13, 21
- Total points per manager should typically be 30-80 points
- No task should exceed 21 points (break down if larger)
- Minimum 1 point per task (even simple tasks have some effort)