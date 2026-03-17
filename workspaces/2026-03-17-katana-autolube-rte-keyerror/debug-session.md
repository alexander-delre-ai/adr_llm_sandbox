# Debug Session: RTE Generator KeyError for auto_lube_pressure_axle_switch_signal

## 1. Chat / Session Summary

- **Title**: RTE Generator KeyError — auto_lube_pressure_axle_switch_signal missing from system_signal_map
- **Context**: Repo `vehicle-os-katana`, branch `jonas/autolube`. Build target: `bazel build //firmware/targets/cab_zonal:cab_zonal_s32k_ecu_rte_gen_cc`.
- **What was tried**: Traced the full data flow from the pyarch Python model through ARXML generation into the RTE code generator. Identified that the signal graph's `system_signal_map` is built exclusively from CAN frame triggerings on the communication cluster, and the auto-lube frames were never placed on the bus.
- **Resolution**: The auto-lube frames (defined in `frames.py`) and PDUs (defined in `pdus.py`) were never wired into the CAN bus as frame triggerings, and the auto-lube SWCs were never registered in the Bazel build. Four files were updated to complete the wiring: ECU frame lists, CAN bus frame triggerings, SWC Bazel targets, and the ECU's software_components list.

## 2. Issue Analysis

### Symptom

```
KeyError:
<MetaElement>[SystemSignal] - auto_lube_pressure_axle_switch_signal
```

Stack trace terminates at `runnables.py:394` in `_generate_implicit_reads`:

```python
) in signal_graph.system_signal_map[bus_signal]
```

Exit code 1 from `generate_rte`.

### Root Cause

The `SignalGraph._build_system_signal_map()` method (in `vehicle_os/tools/autosar/codegen/rte/parse/signals.py`) populates `system_signal_map` by iterating over **CAN frame triggerings** on communication clusters connected to the ECU. Only `SystemSignal`s that appear inside I-Signals inside PDUs inside frames that are triggered on the bus get added to the map.

The auto-lube data flow was partially defined:

| Layer | Defined? | File |
|-------|----------|------|
| SystemSignal (`auto_lube_pressure_axle_switch_signal`) | Yes | `system_signals.py` |
| ISignal (`auto_lube_pressure_axle_switch_isignal`) | Yes | `i_signals.py` |
| PDU (`auto_lube_rear_status`) | Yes | `pdus.py` |
| Frame (`auto_lube_rear_status_frame`) | Yes | `frames.py` |
| **CanFrameTriggering on bus** | **No** | `communication.py` — only had headlight frames |
| **ECU send/receive frame lists** | **No** | `ecus.py` — only had headlight frames |
| **VariableToSignalMapping** | Yes | `system.py` — mapped the variable to the signal |

The variable-to-signal mapping in `system.py` told the RTE generator "this SWC variable maps to this SystemSignal", but when the generator tried to look up that SystemSignal in the signal map (to find which PDU/I-Signal carries it), the signal wasn't there because no frame triggering existed on the bus.

Additionally, the auto-lube SWC Bazel build targets (`software_component` rules) and their inclusion in the `electronic_control_unit` target were missing.

### Code Path

1. `system.py` → `VariableToSignalMapping(variable_path=..., system_signal=SystemSignals.auto_lube_pressure_axle_switch_signal)`
2. ARXML generated with the mapping embedded
3. `generate_rte` invoked by Bazel → `parse_swcs_on_ecu()` → `_generate_runnables()` → `generate_runnables()` → `_generate_concrete_runnable()` → `_generate_implicit_reads()`
4. `_generate_implicit_reads` resolves the variable's provider chain and finds a `SystemSignal`
5. Looks up `signal_graph.system_signal_map[bus_signal]` → **KeyError** because `_build_system_signal_map()` never saw this signal (no frame triggering carried it)

### Contributing Factors

- The pyarch model allows defining signals, I-signals, PDUs, and frames independently without enforcing that they are wired end-to-end through the communication cluster.
- There is no validation step that checks "every SystemSignal referenced in a VariableToSignalMapping is reachable via at least one frame triggering on a bus connected to the ECU."
- The error message (`KeyError: <MetaElement>[SystemSignal] - auto_lube_pressure_axle_switch_signal`) doesn't explain *why* the signal is missing from the map or suggest checking the frame triggerings.

## 3. Steps to Fix (Checklist)

These are the steps that were applied in the `jonas/autolube` branch of `vehicle-os-katana`:

1. **Add frames to ECU instance** (`katana/firmware/katana/model/katana_architecture/hardware/cab_zonal/ecus.py`):
   - Add `Frames.auto_lube_rear_status_frame` to `send_frames` of `cab_zonal_s32k`
   - Add `Frames.central_auto_lube_requests_frame`, `Frames.powertrain_status_frame`, `Frames.drive_system_status_frame`, `Frames.low_voltage_power_status_frame` to `receive_frames` of `cab_zonal_s32k`

2. **Add frame triggerings to CAN bus** (`katana/firmware/katana/model/katana_architecture/communication/cab_zonal/communication.py`):
   - Add `CanFrameTriggering.create(...)` entries for each of the 5 new frames on the `red_bus` cluster
   - Set senders/receivers to the appropriate ECU connectors (only `cab_zonal_s32k` for these)
   - Assign CAN IDs (placeholder IDs `0x0CFED975`–`0x0CFED979` were used; real IDs should be assigned per bus layout)

3. **Add SWC build targets** (`katana/firmware/katana/applications/autosar_swc/BUILD`):
   - Add `software_component` rules for `autoLubeController` and `autoLubeManager`, following the same pattern as the existing `headlightController` / `headlightManager` targets

4. **Wire SWCs into ECU target** (`katana/firmware/targets/cab_zonal/BUILD`):
   - Add `"//firmware/katana/applications/autosar_swc:autoLubeController"` and `"//firmware/katana/applications/autosar_swc:autoLubeManager"` to the `software_components` list of the `electronic_control_unit` rule

5. **Re-run** `bazel build //firmware/targets/cab_zonal:cab_zonal_s32k_ecu_rte_gen_cc` and confirm success

### Secondary fix during verification

The first fix attempt listed `cab_zonal_rtu` as a receiver for the `auto_lube_rear_status_frame` triggering. This caused an `AssertionError: Frame port auto_lube_rear_status_frame_frame_port_rx not found in CabZonal_RTU/red_bus_connector` because the RTU ECU didn't have that frame in its `receive_frames`. Fix: set `receivers=()` for the auto-lube rear status triggering since no local ECU on this bus receives it.

## 4. Recommendations

### Error Reporting

- **In `_build_system_signal_map` or `_generate_implicit_reads`**: When a `SystemSignal` is not found in `system_signal_map`, catch the `KeyError` and raise a descriptive error:
  ```
  SystemSignal 'auto_lube_pressure_axle_switch_signal' is referenced in a
  VariableToSignalMapping but is not present in any frame triggering on a
  communication cluster connected to ECU 'CabZonal_S32K'. Ensure the signal
  is carried by an ISignal in a PDU in a frame with a CanFrameTriggering
  on the bus.
  ```
- **In pyarch model validation**: Add a check during ARXML generation or as a separate `validate()` step that verifies every `SystemSignal` referenced in `variable_to_signal_mappings` is reachable from at least one frame triggering on a connected bus. This would catch the issue at model-build time rather than at RTE generation time.

### Logging

- Log the contents of `system_signal_map` at DEBUG level after `_build_system_signal_map()` completes, showing which signals were found on which buses. This makes it immediately obvious which signals are missing.
- In sandboxed Bazel builds, logs may not be easily accessible. Consider writing diagnostics to stderr so they appear in the Bazel error output.

### Instrumentation

- The RTE generator runs inside a Bazel sandbox, making file-based logging difficult. The most practical approach for debugging is:
  1. Use `--sandbox_debug` to retain the sandbox root
  2. Add temporary `print()` / `logger.error()` statements that go to stderr (visible in Bazel output)
  3. Run the generator directly outside Bazel if possible for interactive debugging

### Documentation

- **Document the full signal wiring chain**: A new signal requires entries at every layer: `SystemSignal` → `ISignal` → `PDU` → `Frame` → `CanFrameTriggering` on bus → ECU `send_frames`/`receive_frames`. Missing any layer causes a silent gap until the RTE generator crashes.
- **Add a "Common Mistakes / Troubleshooting" section** to the pyarch or RTE generator docs:
  - `KeyError: <MetaElement>[SystemSignal] - <name>` → The signal is not on any frame triggering on the ECU's bus. Check `communication.py` frame triggerings and `ecus.py` send/receive frames.
  - `AssertionError: Frame port <name>_frame_port_rx not found` → The ECU listed as a receiver in a frame triggering doesn't have that frame in its `receive_frames`.
- **Document the ECU wiring pattern**: When adding a new SWC that communicates over CAN, you must: (a) define the SWC and its ports, (b) create the signal chain, (c) add frame triggerings, (d) update ECU frame lists, (e) add `software_component` BUILD target, (f) add it to `electronic_control_unit` `software_components`.

## 5. Reference: Files Changed

| File | Change |
|------|--------|
| `katana/.../hardware/cab_zonal/ecus.py` | Added auto-lube frames to `cab_zonal_s32k` send/receive lists |
| `katana/.../communication/cab_zonal/communication.py` | Added 5 `CanFrameTriggering` entries for auto-lube frames |
| `katana/.../applications/autosar_swc/BUILD` | Added `software_component` targets for `autoLubeController` and `autoLubeManager` |
| `katana/firmware/targets/cab_zonal/BUILD` | Added auto-lube SWCs to `electronic_control_unit` `software_components` |

---

**Handoff to Cursor (paste this plus the exported document into a new chat in the target repo):**

I'm sharing a debug-session export from another repo. Please act on it as follows.

1. **Ingest**: The content below (or in the attached file) is a post-mortem with: session summary, issue analysis, steps to fix, and recommendations for error reporting, logging, instrumentation, and documentation.

2. **Branch**: Create a new branch off the latest `master` (e.g. `git fetch origin master && git checkout -b fix/rte-keyerror-missing-signal-validation origin/master`) and apply all changes on that branch.

3. **Apply**:
   - Implement the **Error reporting** recommendations: add input validation in `_generate_implicit_reads` (or `_build_system_signal_map`) to catch missing SystemSignals with a clear message explaining the full wiring chain.
   - Add or update **Documentation** as recommended: document the required signal wiring chain, add a troubleshooting section for the `KeyError` and `AssertionError` failure modes.
   - For **Logging**: add DEBUG-level logging of `system_signal_map` contents after construction.

4. **Confirm**: After making changes, list what you did and suggest a quick verification (e.g. run the previously failing command or tests).

Paste the exported document below this line, or attach it and say "the exported document is in `workspaces/2026-03-17-katana-autolube-rte-keyerror/debug-session.md`".
