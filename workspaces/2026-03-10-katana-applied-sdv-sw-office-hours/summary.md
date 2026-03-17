# Meeting Transcript: Katana <> Applied: SDV SW Office Hours (Mar 10, 2026)

## Original Gemini Summary

Mar 10, 2026
Katana <> Applied: SDV SW Office Hours
Invited Alex Del Re  joseph.boyer@global.komatsu nuthan.sabbani@global.komatsu michael.lemm@global.komatsu joshua.rohman@global.komatsu
Attachments Katana <> Applied: SDV SW Office Hours 

Summary
Autosar call types clarified, with sync server call points designated for hardware interaction, while planning manager development for the 2027 truck build was emphasized.

Autosar Call Point Clarification
The discussion clarified the difference between I-read/I-write calls and sync server call points within the Autosar standard. Sync server call points will be used for all IO abstraction involving hardware interaction, such as PWM and ADC, as they function like a callback.

Manager Development Planning
A clear need for dependency information (pin-outs, sensors, motors) was raised for various managers to support the August 2027 first truck build timeline. 1-hour meetings for each manager should be scheduled with Kamasu and applied system engineering personnel to discuss zone allocation and I/Os.

Subsystem Scope Management
The risk of over-committing to 4 subsystems for Steering Committee goals was discussed, advocating for limited scope to ensure correct completion. The team may prioritize Auto Loop and potentially Engine, treating the other planned subsystems as a stretch goal for the next quarter.

Details
Meeting and Technical Setup::  Ashli Forbes apologized for the background noise in their location, noting that the office had become very active. Joseph Boyer was working to address connection issues and mentioned they were looking to establish a reusable Teams meeting or similar resource with the Kamasu team.
Clarification on Autosar Call Types (I/O, Read/Write, and Call Points)::  The discussion focused on the difference between I-read/I-write calls and "sync server call points" (simply referred to as calls) within the Autosar standard. Ashli Forbes explained that this is largely an Autosar design standard and not an applied decision. I-read and I-write function like reading and writing to a buffer, while sync server call points function more like a callback, which is used for hardware interaction, such as with high-side drives (HSD).
Hardware Abstraction and Call Point Usage::  Ashli Forbes confirmed that anything involving IO abstraction, such as Pulse-Width Modulation (PWM), Analog-to-Digital Converter (ADC), and edge counters, will use sync server call points. This structure is part of the hardware abstraction efforts by applied, and this choice is made because the call points function more like a callback, which is appropriate for hardware behavior.
Planning for Manager Development and Hardware Bring-up::  Joseph Boyer introduced the need for clear dependency information (pin-outs, sensors, motors) for various managers, which is necessary for the vehicle hardware team's planning toward the August 2027 timeline for a first truck build. Ashli Forbes suggested scheduling one-hour meetings for each manager with Joseph Boyer and appropriate Kamasu and applied system engineering personnel to discuss zone allocation and I/Os. Joseph Boyer's current documentation on the engine manager interface was deemed a good start for providing context to the systems engineers.
Hardware Flashing and Setup::  Joseph Boyer reported that they had brought in a Linux laptop with necessary dependencies to help the team flash one of the Programmable Automotive Modules (PAMs) for the first time. Ashli Forbes clarified that this laptop is intended for flashing single boards or smaller rigs, separate from the cloud-based workbench instance, to allow for local testing before pushing changes to the cloud. Joseph Boyer stated that they would look into getting a list of connectors, terminals, and crimpers needed to expand the harness once the application hardware needs are better understood.
Cyclical Development and Feature Gaps::  Joseph Boyer noted that certain features, such as circuit diagnostics for high-side drivers (HSDs) and communications with the UI, are not yet fully implemented on the vehicle OS side, meaning the managers cannot be completed start to finish. Ashli Forbes recommended managing this by using placeholders or "to-do" links in the code pointing to specific tickets for future implementation, which helps Project Managers track dependencies and back-trace completion timelines.
SteerCo Goals and Scope Management::  Joseph Boyer discussed the consequences of committing to Steering Committee (SteerCo) goals, particularly the risk of over-committing to complete four subsystems in a quarter. They advocated for limiting the scope to prioritize completing subsystems correctly, suggesting that they may focus on Auto Loop in isolation for the next quarter, possibly adding a simpler system like Engine, and treating the other planned subsystems as a stretch goal.
Requirement Discussion for Hardware Diagnostics::  Joseph Boyer initiated a discussion with Chad and Lee (who was joining late) to determine the mandatory requirements for hardware diagnostics, particularly given the removal of large portions of the "oxbox" functionality. The initial thought was to require circuit diagnostics (open, closed, or short circuit) for every output, along with current and voltage diagnostics for inputs, and to move toward resistive switches to enable diagnostics on those as well.

Suggested next steps
Joseph Boyer will meet with the UI team later today to talk about what the UI interface is going to look like.
Joseph Boyer and Alex Del Re will try to run through auto loop to get an idea of how long a subsystem takes.

You should review Gemini's notes to make sure they're accurate. Get tips and learn how Gemini takes notes
Please provide feedback about using Gemini to take notes in a short survey.