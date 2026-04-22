# Applied Meeting Room Reference

Applied uses well-known scientists and their associated work to identify conference rooms.

## Known Meeting Room Patterns

### Physics/Science Names
- **Coulomb's Law** - Electrostatics law
- **Newton's Law** - Laws of motion, gravity

### Recognition Pattern
```
<Scientist Name> (<Location Code>, <Building/Floor>)
```

**Examples:**
- "Coulomb's Law (SVL-WCAL-HQ, FL3)"
- "Newton (NYC-MAIN, 5F)"
- "Einstein (AUS-TECH, B2)"

### Location Code Patterns
- **SVL** - Sunnyvale

### Building Codes
- **WCAL-HQ** - West Coast Applied Labs Headquarters

## Usage in Meeting Analysis

When parsing meeting transcripts:

1. **Identify pattern**: Look for scientist names with location codes in parentheses
2. **Exclude from attendees**: Don't include meeting rooms in participant lists
3. **Record location**: Note meeting room in context if relevant
4. **Ask if uncertain**: If a name could be either, ask the user for clarification

## Adding New Rooms

When encountering unknown scientist names in meeting contexts:
1. Check if they follow the location code pattern
2. Research if it's a known scientific figure
3. Add to this reference list
4. Update the meeting analysis skill accordingly