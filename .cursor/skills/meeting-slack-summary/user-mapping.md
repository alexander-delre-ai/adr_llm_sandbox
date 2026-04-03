# User Organization Mapping

This file contains the mapping of users between Komatsu and Applied organizations for accurate Slack summary formatting.

## Komatsu Organization Users

### Active Development Team
- **Mike Lemm** (also: Michael Lamb, Michael Lemm, Marcus)
  - Slack name: `@Mike Lemm`
  - Role: Software developer, Jira lead/admin for Komatsu
  - Started: January 2026
  - Notes: Becoming primary Jira administrator for Komatsu side. Transcript alias "Marcus" in SIL overview meeting.

- **Joseph Boyer**
  - Slack name: `@joseph.boyer`
  - Email: joseph.boyer@global.komatsu
  - Role: Technical lead

- **Jonas Hageman**
  - Slack name: `@jonas.hageman`
  - Role: Developer working on auto loop development

- **Nuthan Sabbani** (also: Nathan, Nuthan)
  - Slack name: `@nuthan.sabbani`
  - Email: nuthan.sabbani@global.komatsu
  - Role: VehicleOS/payload specialist
  - Notes: Transcript alias "Nathan" in SIL overview meeting. Slack handle shorthand `@Nuthan`.

- **Eric Peters**
  - Slack name: `@eric.peters`
  - Role: Developer, discussed test organization and directory structure

- **Joshua Rohman**
  - Email: joshua.rohman@global.komatsu

### System Engineers (DRIs)
- **Jason Shepler** - DRI (Directly Responsible Individual)
- **Nick Sturm** - DRI, system engineering
- **Joel Hatterman** - DRI

### Leadership Team
- **Jeff** - Leadership/strategic decisions
- **Lee** - Leadership/strategic decisions
- **John** - Leadership/strategic decisions

## Applied Organization Users

### Core Team Members
- **Alex Del Re**
  - Slack ID: `U063Y6FQA5V`
  - Role: Meeting facilitator, main Applied contact
  - Notes: Frequently assigned coordination tasks

- **Lauren Joyce**
  - Slack ID: `U07CNBCK53P`
  - Role: Jira admin/manager with permissions
  - Notes: Handles Jira configuration, consults with Greg for admin decisions

- **Timothy Kyung**
  - Slack ID: `U0AHT1Y21EV`
  - Email: timothy.kyung@applied.co
  - Role: New Applied team member (joined recently)
  - Background: Former MathWorks application engineer (6 years)
  - Focus: Komatsu account support and documentation

- **Ashley Forbes** (correct name: **Ashli Forbes**)
  - Slack ID: `U09AUE77ZU5`
  - Email: ashli.forbes@applied.co
  - Role: Software Integration Engineer
  - Expertise: Testing and development infrastructure

- **Jesus Lira**
  - Slack ID: `U07U079V6BT`
  - Email: jesus.lira@applied.co
  - Role: Manager - Electrical Systems Integration

- **Andrew McGovern**
  - Slack ID: `U07AY0G968H`
  - Email: andrew@applied.co
  - Role: Application Engineer

- **Ashwin Raghavachari** (also: AshwinR)
  - Slack ID: `U9178B6DC`
  - Email: ashwin@applied.co
  - Role: Application Engineering

- **Gurinder Dhillon** (also: Grinder)
  - Slack ID: `U09M6QCM4EA`
  - Email: gurinder.dhillon@applied.co
  - Role: Product Manager
  - Notes: Owns data logging strategy (KATA-2575). Primary PM contact for OTAA and data logging workstreams.

### Applied Leadership
- **Greg** - Manager (Lauren's supervisor for admin permissions)
- **Applied TPM** - Technical Program Manager (release coordination)

### Hardware/System Architecture
- **Nick Tokarz** (also: Nicholas Tokarz, NickT)
  - Slack ID: `U0871MMMEAK`
  - Email: nicholas.tokarz@applied.co
  - Role: System Architect
  - Notes: Leads HW <> SW sync, device bring-up planning for Juniper/Walnut

### VehicleOS/SVL Team
- **Srishti Dhamija**
  - Role: VehicleOS team member
  - Expertise: Adaptive architecture

### Resolved Slack IDs
- **U080A6CFRAQ** - Srishti Dhamija (srishti.dhamija@applied.co, Software Engineer)

## Email Patterns

### Komatsu
- Format: `firstname.lastname@global.komatsu`
- Examples:
  - joseph.boyer@global.komatsu
  - nuthan.sabbani@global.komatsu
  - joshua.rohman@global.komatsu

### Applied
- Email addresses not consistently documented in meeting transcripts
- Use Slack IDs for mentions in summaries

## Meeting Room Filtering

### Exclude from Attendee Lists
- **Coulomb's Law (SVL-WCAL-HQ, FL3)** - Meeting room, not a person
- Any name with location codes in parentheses (e.g., "SVL-WCAL-HQ, FL3")

### Special Cases
- **Coulomb's Law/Alex (SVL)** - This refers to Alex Del Re in VehicleOS context
- **Alex (SVL)** - Same as above, Alex Del Re

## Usage Guidelines for Slack Summaries

### Attendee Formatting
1. **Komatsu attendees**: Use plain names (no Slack mentions)
2. **Applied attendees**: Use Slack mentions format `<@USER_ID>`
3. **Name corrections**: Always use "Ashli Forbes" not "Ashley Forbes"
4. **Filter meeting rooms**: Remove any entries with location codes

### Organization Assignment Rules
- If email contains `@global.komatsu` → Komatsu
- If Slack ID is known → Applied (unless explicitly Komatsu)
- If uncertain, default to context from meeting role/discussions

### Slack ID Lookup
When encountering new Applied team members:
1. Use `slack_search_users` to find Slack user ID
2. Update this mapping file with new discoveries
3. Always verify organization assignment through context

## Maintenance Notes

This mapping should be updated when:
- New team members join either organization
- Slack IDs are discovered for existing users
- Organizational changes occur
- Name corrections are identified

Last updated: April 3, 2026