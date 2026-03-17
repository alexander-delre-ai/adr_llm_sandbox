# Meeting Analysis: Katana <> Applied SDV SW Office Hours (Mar 13, 2026)

## 1. Meeting Context

- **Title**: Katana <> Applied SDV SW Office Hours
- **Date**: March 13, 2026
- **Participants**: Alex Del Re (Applied), Timothy Kyung (Applied), Mike (Komatsu), Joe/Joseph (Komatsu)
- **Stated Objective**: Answer open questions from the Komatsu team and discuss the plan for next week; review upcoming topics including fault injection testing, GPIO, interzonal modeling, diagnostics, and signal validation

---

## 2. Key Decisions

1. **Decision 1**: Embedded unit testing for Monday will focus on workbench tests (fault injection); no additional engineering time needed beyond current resources.
2. **Decision 2**: GPIO input/output will be discussed today; expected to follow the same pattern as HSD/efuse outputs.
3. **Decision 3**: Interzonal communication will move toward plain Ethernet packets rather than CAN-over-Ethernet as the preferred approach going forward.
4. **Decision 4**: The Irene diagnostics implementation PR is targeting a merge today.
5. **Decision 5**: Hardware current-draw readback from EFuse/HSD outputs is a capability to be confirmed on the roadmap -- Alex will follow up with the responsible engineer.
6. **Decision 6**: It is too early to include Applied hardware representatives in the upcoming Komatsu leadership architecture meeting on Wednesday.
7. **Decision 7**: Alex will find time with the tech writer (Gyra) to demo Docusaurus to the Komatsu team for documentation tooling comparison.

---

## 3. Discussion Themes

1. **Embedded Testing & Workbench Tests** - Discussed the plan for Monday's fault injection / workbench testing session and confirmed no blocking gaps on current topics.
2. **HSD vs EFuse Output Clarification** - Deep-dive into the difference between High Side Drive (HSD) and EFuse (EU) outputs, motivated by ambiguities found in the Komatsu headlights controller SWC implementation.
3. **Interzonal Communication Strategy** - Discussed moving away from CAN-over-Ethernet to plain Ethernet packets; desire for a more automated PDU build process to reduce manual signal definition burden.
4. **Diagnostics & DEM Events** - Explored how to set DTC-equivalent events when CAN signal integrity checks fail, including the DEM event (L1-L4) mechanism and masking based on system state / truck configuration.
5. **App Dev Roadmap & Prototype Planning** - Reviewed the Gantt-style R/D/T/H app development schedule; discussed controller IO allocation requirements and upcoming Komatsu leadership architecture meeting.
6. **Documentation Tooling** - Brief discussion comparing Docusaurus (Applied) with Gitbook (Komatsu evaluation); Alex to arrange a short Docusaurus walkthrough.

---

## 4. Unresolved Questions

- **HSD vs EFuse in same SWC**: Why does the Komatsu headlights `system.py` define both `HSD` outputs and `EFuse` (EU) outputs for similar light controls? Alex believes it may be due to running out of HSD pins on the PCB but needs to confirm. [Alex Del Re]
- **CAN signal integrity -> DTC path**: Is setting a DEM event (and subsequently a DTC) based on a failed CRC check something that must be done explicitly in a runnable, or is it handled by the PiArch diagnostic layer automatically? [Alex Del Re / Applied Platform Team]
- **Current draw readback from EFuse outputs**: Can the application layer read back current draw from EFuse/HSD outputs? This is expected by Komatsu hardware team but not confirmed on the roadmap. [Alex Del Re to confirm with HSD platform engineer]
- **Interzonal PDU automation**: What would an automated PDU build process look like so that teams do not need to manually define start bit / signal length for interzonal signals where both sender and receiver are defined? [TBD - future discussion]
- **Hardware delivery timeline**: Tracking numbers for hardware exist but shipment had not left as of this morning. [Joe / Mike]
- **Prototype controller allocation**: Full controller and zonal IO allocations are still being compiled (Joe's exercise); initial schematic meeting with Komatsu leadership is Wednesday. [Joe / Alex Del Re]

---

## 5. Action Items

| # | Action Item | Assignee | Priority | Theme |
|---|-------------|----------|----------|-------|
| 1 | Confirm HSD vs EFuse distinction and why both are defined in `system.py` headlights SWC | Alex Del Re | High | HSD vs EFuse Output Clarification |
| 2 | Confirm current-draw readback capability from EFuse/HSD outputs is on the platform roadmap (before 2027) | Alex Del Re | High | HSD vs EFuse Output Clarification |
| 3 | Clarify the mechanism to set a DEM event / DTC based on a failed CAN signal CRC check | Alex Del Re | High | Diagnostics & DEM Events |
| 4 | Schedule and attend Komatsu leadership architecture meeting (Wednesday) to finalize controller/zonal allocations | Alex Del Re | High | App Dev Roadmap & Prototype Planning |
| 5 | Arrange a short Docusaurus walkthrough with tech writer Gyra for the Komatsu team | Alex Del Re | Medium | Documentation Tooling |
| 6 | Provide examples for interzonal communication (inner-zonal communication examples for Newton/Komatsu) | Alex Del Re | Medium | Interzonal Communication Strategy |
| 7 | Merge Irene diagnostics PR into Komatsu codebase | Alex Del Re | High | Diagnostics & DEM Events |
| 8 | Discuss signal validation custom approach with Evan (follow up from last week) | Alex Del Re | Medium | Diagnostics & DEM Events |
| 9 | Monitor hardware shipment tracking and confirm delivery timeline | Joe / Mike | Low | App Dev Roadmap & Prototype Planning |

---

## 6. Prioritized Action Plan

| # | Proposed Action Item | Assignee | Priority | Due | Type | Notes |
|---|---------------------|----------|----------|-----|------|-------|
| 1 | Merge Irene diagnostics PR into Komatsu codebase | Alex Del Re | High | Today (Mar 13) | Technical | PR targeting merge today |
| 2 | Confirm HSD vs EFuse distinction in `system.py` headlights SWC | Alex Del Re | High | Next OH / ASAP | Technical | Likely due to pin exhaustion on PCB |
| 3 | Confirm current-draw readback from EFuse/HSD is on platform roadmap | Alex Del Re | High | ASAP | Technical | Komatsu hardware team is assuming this exists |
| 4 | Clarify DEM event / DTC mechanism for failed CAN signal CRC | Alex Del Re | High | Next OH | Technical | May need input from Applied platform/diagnostics team |
| 5 | Attend Komatsu leadership architecture meeting (Wednesday) | Alex Del Re | High | Wed Mar 18 | Coordination | Finalize controller/zonal allocations; too early for Applied HW to join |
| 6 | Discuss signal validation custom approach with Evan | Alex Del Re | Medium | Next week | Technical | Custom hand signal validation for Komatsu |
| 7 | Provide interzonal communication examples to Newton/Komatsu | Alex Del Re | Medium | This week | Technical | Supporting Newton's autosact dev work |
| 8 | Schedule Docusaurus walkthrough with Gyra for Komatsu team | Alex Del Re | Medium | This week | Coordination | Gitbook vs Docusaurus comparison |
| 9 | Monitor hardware shipment and confirm delivery | Joe / Mike | Low | TBD | Coordination | Has tracking number, had not shipped as of Mar 13 morning |

**Next Steps:**
- Alex to follow up on HSD/EFuse question internally before next office hours
- Alex to confirm current-draw readback with HSD platform engineer and get it on the roadmap if missing
- Alex to clarify DTC-setting mechanism via runnable vs platform-handled
- Architecture meeting Wednesday is the key near-term milestone -- confirm attendee list
- Arrange Docusaurus demo with Gyra this week
