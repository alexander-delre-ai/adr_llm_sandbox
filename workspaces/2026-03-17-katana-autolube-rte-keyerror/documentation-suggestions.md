# Documentation Suggestions for vehicle_os

Suggested changes to documentation in `~/applied/core-stack/vehicle_os/doc` based on the debug session for the RTE generator `KeyError: auto_lube_pressure_axle_switch_signal`.

---

## 1. Add "Signal Wiring Checklist" to `define_communication.mdx`

**File:** `doc/docusaurus/docs/onboard_sdk/embedded_firmware/tutorials/pyarch/define_communication.mdx`

**What to add:** A summary checklist at the end of the tutorial (or as a callout box) listing every layer a new signal must pass through. The tutorial already covers each step individually, but users miss steps because there is no single-glance checklist.

**Suggested content:**

```mdx
:::info Signal Wiring Checklist

Every signal that participates in inter-ECU communication must be defined at **all** of these layers. Missing any layer will cause a build failure in RTE generation.

| # | Layer | File location | Example |
|---|-------|---------------|---------|
| 1 | `SystemSignal` | `signals/system_signals.py` | `my_signal = pyar.SystemSignal()` |
| 2 | `ISignal` | `signals/i_signals.py` | `my_isignal = pyar.ISignal(bit_length=2, system_signal=SystemSignals.my_signal)` |
| 3 | `ISignalIPdu` (PDU) | `pdus/pdus.py` | `my_pdu = pyar.ISignalIPdu(...)` with `signal_mapping` referencing the ISignal |
| 4 | `CanFrame` | `frames/frames.py` | `my_frame = pyar.CanFrame.create(byte_length=8, pdus=(PDUs.my_pdu,))` |
| 5 | `CanFrameTriggering` on bus | `communication.py` | `pyar.CanFrameTriggering.create(frame_ref=Frames.my_frame, can_id=0x123, ...)` |
| 6 | ECU `send_frames` / `receive_frames` | `ecus.py` | Add the frame to the appropriate ECU instance |
| 7 | `VariableToSignalMapping` | `system.py` | `pyar.VariableToSignalMapping(variable_path=..., system_signal=...)` |
| 8 | `software_component` BUILD target | `autosar_swc/BUILD` | Bazel target for the SWC that uses the signal |
| 9 | `electronic_control_unit` `software_components` | `targets/<target>/BUILD` | Add the SWC target to the ECU's component list |

If you see `KeyError: <MetaElement>[SystemSignal] - <name>` during RTE generation, the signal at layer 5 or 6 is missing.
:::
```

---

## 2. Add "Troubleshooting" section to `generate_rte.mdx`

**File:** `doc/docusaurus/docs/onboard_sdk/embedded_firmware/tutorials/pyarch/generate_rte.mdx`

**What to add:** A new section at the end titled "Troubleshooting" covering the most common RTE generation errors and how to resolve them.

**Suggested content:**

```mdx
## Troubleshooting

### `KeyError: <MetaElement>[SystemSignal] - <signal_name>`

**Cause:** The RTE generator builds a `system_signal_map` by scanning `CanFrameTriggering` entries on communication clusters connected to the ECU. If a `SystemSignal` is referenced in a `VariableToSignalMapping` but does not appear in any frame triggering, this error occurs.

**Fix:**
1. Verify the signal has an `ISignal` referencing it
2. Verify the `ISignal` is mapped into a PDU (`ISignalIPdu`)
3. Verify the PDU is placed in a `CanFrame`
4. Verify the frame has a `CanFrameTriggering` on the communication cluster
5. Verify the ECU lists the frame in `send_frames` or `receive_frames`

See the [Signal Wiring Checklist](/docs/onboard_sdk/embedded_firmware/tutorials/pyarch/define_communication#signal-wiring-checklist) for the full chain.

### `AssertionError: Frame port <name>_frame_port_rx not found in <ECU>/<connector>`

**Cause:** A `CanFrameTriggering` lists an ECU connector as a receiver, but that ECU does not have the frame in its `receive_frames`. Frame ports are auto-generated from the ECU's frame lists.

**Fix:** Either:
- Add the frame to the ECU's `receive_frames` (if it should receive it), or
- Remove the ECU from the frame triggering's `receivers` tuple

### `AssertionError: Frame port <name>_frame_port_tx not found in <ECU>/<connector>`

**Cause:** Same as above but for senders. The ECU is listed as a sender but doesn't have the frame in `send_frames`.

**Fix:** Add the frame to the ECU's `send_frames`, or remove the ECU from `senders`.
```

---

## 3. Expand `signals.mdx` with `system_signal_map` population details

**File:** `doc/docusaurus/docs/developer_tooling_internal/autosar/rte/signals.mdx`

**What to add:** The existing doc explains `SignalGraph` at a high level but doesn't describe how `system_signal_map` is populated or what causes lookup failures. Add a subsection explaining the map's construction.

**Suggested content:**

```mdx
### How `system_signal_map` is built

The `system_signal_map` is a dictionary mapping `SystemSignal` → `{ISignal → [PDU, ...]}`. It is populated in `_build_system_signal_map()` by:

1. Iterating over `fibex_elements` (communication clusters) in the ARXML `System`
2. For each cluster, iterating over physical channels where the ECU has a connector
3. For each frame triggering on the channel that the ECU sends or receives
4. For each PDU triggering within the frame
5. For each I-Signal triggering within the PDU, resolving the `SystemSignal` via `i_signal.system_signal_ref()`

**Key implication:** A `SystemSignal` only appears in `system_signal_map` if it is reachable through the full chain: `SystemSignal` ← `ISignal` ← `PDU` ← `Frame` ← `FrameTriggering` on a bus connected to the ECU.

If a `VariableToSignalMapping` references a `SystemSignal` that is not in this map, the RTE generator will raise a `KeyError` when processing implicit reads/writes for the associated SWC runnable.
```

---

## 4. Add `variable_path` format documentation to `connections.mdx`

**File:** `doc/docusaurus/docs/onboard_sdk/embedded_firmware/classic/rte/connections.mdx`

**What to add:** The doc mentions `VariableToSignalMapping` and `variable_path` but doesn't clearly document the expected format or common mistakes.

**Suggested addition after the existing `VariableToSignalMapping` example:**

```mdx
:::caution variable_path format

`variable_path` must be a **variable reference** (3-element tuple: SWC instance, port, data element), not a **port reference** (2-element tuple). Use the generated variable refs from your `gen` module:

```python
# Correct: variable ref (instance, port, data element)
variable_path=I_auto_lube_controller_ports.RP_auto_lube_pressure_axle_switch_state

# Wrong: port ref (instance, port only) — will cause IndexError in _traverse_swc_path
variable_path=I_auto_lube_controller_ports.RP_auto_lube_pressure_axle_switch
```

The variable ref names follow the pattern `<PortName>_<dataElementName>` where `dataElementName` comes from the `VariableDataPrototype.name` in the `SenderReceiverInterface`.
:::
```

---

## 5. Add cross-references between communication docs

**Files affected:**
- `doc/docusaurus/docs/onboard_sdk/embedded_firmware/classic/modeling/communication.mdx`
- `doc/docusaurus/docs/onboard_sdk/embedded_firmware/tutorials/pyarch/define_communication.mdx`
- `doc/docusaurus/docs/onboard_sdk/embedded_firmware/classic/rte/connections.mdx`

**What to add:** These three docs cover overlapping topics (signal definitions, PDUs, frames, frame triggerings, variable-to-signal mappings) but don't link to each other. Add "See also" blocks:

In `communication.mdx`:
```mdx
:::tip See also
- [PyArch Tutorial: Define Communication](/docs/onboard_sdk/embedded_firmware/tutorials/pyarch/define_communication) — step-by-step guide including frame triggerings and BUILD setup
- [Classic RTE: Connections](/docs/onboard_sdk/embedded_firmware/classic/rte/connections) — how signals connect to SWC variables via `VariableToSignalMapping`
:::
```

In `connections.mdx`:
```mdx
:::tip See also
- [Classic Modeling: Communication](/docs/onboard_sdk/embedded_firmware/classic/modeling/communication) — naming conventions for signals, PDUs, and frames
- [PyArch Tutorial: Define Communication](/docs/onboard_sdk/embedded_firmware/tutorials/pyarch/define_communication) — end-to-end signal wiring with code examples
:::
```

---

## 6. Enhance error messages in RTE generator code

**File:** `vehicle_os/tools/autosar/codegen/rte/parse/signals.py` (code, not docs — but included here as a documentation-adjacent improvement)

**What to change:** In `_build_system_signal_map` or at the call site in `runnables.py:394`, replace the bare `dict[key]` lookup with a guarded access that raises a descriptive error:

```python
if bus_signal not in signal_graph.system_signal_map:
    raise KeyError(
        f"SystemSignal '{bus_signal.short_name.value}' is referenced in a "
        f"VariableToSignalMapping but is not present in any FrameTriggering "
        f"on a communication cluster connected to this ECU. "
        f"Ensure the signal chain is complete: SystemSignal → ISignal → PDU → "
        f"Frame → CanFrameTriggering on the bus. "
        f"Available signals: {[s.short_name.value for s in signal_graph.system_signal_map.keys()]}"
    )
```

This change turns a cryptic `KeyError: <MetaElement>[SystemSignal] - name` into an actionable error message that tells the developer exactly what's wrong and what to check.

---

## Summary of suggested changes

| # | Doc file | Change type | Priority |
|---|----------|-------------|----------|
| 1 | `define_communication.mdx` | Add Signal Wiring Checklist | High |
| 2 | `generate_rte.mdx` | Add Troubleshooting section | High |
| 3 | `signals.mdx` | Explain `system_signal_map` construction | Medium |
| 4 | `connections.mdx` | Document `variable_path` format | Medium |
| 5 | Multiple | Add cross-references | Low |
| 6 | `signals.py` (code) | Improve error message | High |
