# Meeting Analysis: SDV SW Office Hours (Mar 16, 2026)

## 1. Meeting Context

- **Title**: Katana <> Applied: SDV SW Office Hours
- **Date**: March 16, 2026
- **Participants**: Alex Del Re, Jonas Hageman, Joseph Boyer, Timothy Kyung, Mike Lemm
- **Location**: Virtual (Teams)
- **Objective**: Weekly sync between Katana and Applied (Komatsu) teams on SDV software development topics -- ETH/CAN transport concerns, documentation tooling, and middleware roadmap.

## 2. Key Decisions

1. **Decision 1**: Continue with CAN-over-Ethernet transport for now as the plan of record, with native Ethernet frame packing and IP middleware as future improvements.
2. **Decision 2**: Alex to raise two questions with the engineering team: (a) timeline for native Ethernet frame packing, and (b) some-IP cross-zone latency numbers.
3. **Decision 3**: Joe Boyer formally requested auto-calculated PDU start-bit offsets at build time -- Alex confirmed this has been raised internally but no response yet.
4. **Decision 4**: Documentation co-pilot (RAG-based) is now available on Komatsu accounts; Komatsu docs can be integrated into the knowledge base without requiring Docusaurus adoption.

## 3. Discussion Themes

### Theme 1: ETH-CAN Frame Packing Limitations
Jonas raised that current system packs CAN frames into L2 Ethernet packets rather than native Ethernet frames. Joe Boyer expressed concerns about the 64-byte CAN FD payload limit being too restrictive for larger subsystems like engine interface and payload meter, particularly for interzonal data that needs to traverse the Ethernet ring to central.

### Theme 2: IP Middleware Roadmap (some-IP)
Alex shared that an IP-based pub/sub middleware (some-IP) is on the internal roadmap targeting end of Q2 (~June/July 2026). It uses shared memory for same-zone communication (very fast) but cross-zone latency is still unknown. A basic calculator demo app could be shown to Komatsu in April. Joe confirmed this aligns with what Lee had envisioned.

### Theme 3: PDU Auto-Calculation Feature Request
Joe formally requested that PDU start-bit offsets be automatically calculated at build time, removing the need for developers to manually define offsets when adding, removing, or reordering signals. Alex confirmed this was previously raised but hasn't received a response yet.

### Theme 4: Documentation Co-Pilot and Shared Docs
Alex demoed a new RAG-based co-pilot feature added to Komatsu accounts over the weekend. It searches across all Vehicle OS documentation categories (Vehicle OS, infotainment, SDK, developer tooling) and provides confidence-rated answers with an escalation path to Applied engineers. Mike Lemm asked about Docusaurus requirements -- Alex clarified docs just need to be stored in the codebase on vehicle.komatsu, no specific framework required.

### Theme 5: Drive Controller Scoping
Joe mentioned the electric drive controller is not currently in development planning but hardware is being designed to support it. A Wednesday meeting will reassess scope. If integrated, drive systems would have significant software components requiring interzonal communication, reinforcing the need for better-than-CAN transport.

## 4. Unresolved Questions

- When will native Ethernet frame packing be supported? [Alex Del Re - to raise with engineering team]
- What is the some-IP cross-zone (central-to-zone) latency? [Alex Del Re - to check with Rushi]
- How large are the PIP and HIP struct sizes for payload meter? [Joseph Boyer - to get from Jason]
- Which other subsystems may exceed CAN frame size limits? [Joseph Boyer - to review offline]
- Will the electric drive controller be included as a project milestone? [Joseph Boyer - depends on Wednesday meeting]
- What options exist for automated PDU creation/offset calculation? [Alex Del Re - raised but no response yet]

## 5. Action Items

### Action 1: Deliver a timeline for native Ethernet frame packing support
- **What**: Raise with the engineering team to determine when native Ethernet frame packing (instead of CAN-over-ETH) will be available. Jonas flagged that current docs note limitations in modeling/code generation for Ethernet frames. Engine interface and payload meter are high-priority apps that will need this.
- **Who**: Alex Del Re
- **When**: Release 25.3
- **Priority**: High (P1)
- **Theme**: ETH-CAN Frame Packing Limitations
- **Tracking**: JIRA - [KATA-2894](https://appliedint-katana.atlassian.net/browse/KATA-2894)

### Action 2: Investigate some-IP cross-zone latency for central-to-zone communication
- **What**: Check with Rushi on what the some-IP cross-zone latency is for data passing between central and zones. Same-zone uses shared memory (very fast), but cross-zone latency is unknown. Joe needs this to evaluate IP middleware as a transport option for payload meter.
- **Who**: Alex Del Re
- **Priority**: High (P1)
- **Theme**: IP Middleware Roadmap
- **Tracking**: Slack

### Action 3: Provide struct sizes for PIP and HIP payload meter data
- **What**: Get struct sizes for PIP and HIP from Jason to quantify how limiting the CAN FD 64-byte payload is for payload meter data. This helps determine urgency of Ethernet frame or IP transport support.
- **Who**: Joseph Boyer
- **Priority**: Medium (P2)
- **Theme**: ETH-CAN Frame Packing Limitations
- **Tracking**: Slack

### Action 4: Review other subsystem signal sizes that may exceed CAN frame limits
- **What**: Assess offline which subsystem outputs may not fit within CAN frame limitations. Engine interface will be a concern in phase 2 due to large diagnostic data volumes. Drive systems may also be impacted if integrated.
- **Who**: Joseph Boyer
- **Priority**: Medium (P2)
- **Theme**: ETH-CAN Frame Packing Limitations
- **Tracking**: Slack

### Action 5: Follow up on automated PDU start-bit calculation feature request
- **What**: Follow up internally on Joe Boyer's formal request to have PDU start-bit offsets automatically calculated at build time. Currently developers must manually define offsets when adding/removing/reordering signals, which is tedious and error-prone. Determine if this becomes a feature request or engineering task.
- **Who**: Alex Del Re
- **Priority**: Medium (P2)
- **Theme**: PDU Auto-Calculation Feature Request
- **Tracking**: Slack

## 6. Prioritized Action Plan

| # | Proposed Action Item | Assignee | Priority | Tracking | Notes |
|---|---------------------|----------|----------|----------|-------|
| 1 | Deliver a timeline for native Ethernet frame packing support | Alex Del Re | P1 | JIRA ([KATA-2894](https://appliedint-katana.atlassian.net/browse/KATA-2894)) | Parent: KATA-726, Release 25.3 |
| 2 | Investigate some-IP cross-zone latency for central-to-zone communication | Alex Del Re | P1 | Slack | Check with Rushi on middleware |
| 3 | Provide struct sizes for PIP and HIP payload meter data | Joseph Boyer | P2 | Slack | Get from Jason; quantifies CAN limitation |
| 4 | Review other subsystem signal sizes that may exceed CAN frame limits | Joseph Boyer | P2 | Slack | Offline review of subsystem outputs |
| 5 | Follow up on automated PDU start-bit calculation feature request | Alex Del Re | P2 | Slack | Joe's formal request; raised but no response |

### Next Steps

- Alex to deliver ETH frame packing timeline via KATA-2894 (Release 25.3)
- Alex to check with Rushi on some-IP cross-zone latency numbers
- Joe to get PIP/HIP struct sizes from Jason to quantify CAN frame limitation
- Alex to follow up on PDU auto-calculation feature request status
- Reconvene on subsystem signal size review in ~2 weeks
