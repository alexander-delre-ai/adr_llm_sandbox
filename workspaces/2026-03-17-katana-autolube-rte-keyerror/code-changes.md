# Code Changes: Error Reporting and Debugging Improvements

Suggested code changes for `~/applied/core-stack/vehicle_os` to improve error messages and speed up future debugging of signal wiring issues.

---

## 1. Replace bare `KeyError` with actionable error in `runnables.py`

**File:** `tools/autosar/codegen/rte/parse/runnables.py`

**Problem:** There are 4 identical `signal_graph.system_signal_map[bus_signal]` lookups (lines ~278, ~394, ~528, ~689) across `_generate_implicit_writes`, `_generate_implicit_reads`, `_generate_explicit_writes`, and `_generate_explicit_reads`. When a `SystemSignal` is missing from the map, Python raises a bare `KeyError` with only the `MetaElement` repr, giving no indication of *why* the signal is missing or what to fix.

**Current code** (repeated in 4 locations):

```python
for (
    i_signal,
    pdus,
) in signal_graph.system_signal_map[  # ty: ignore[invalid-argument-type]
    bus_signal
].items():
```

**Suggested change:** Extract a helper method on `SignalGraph` and call it from all 4 sites.

Add to `tools/autosar/codegen/rte/parse/signals.py` in the `SignalGraph` class:

```python
def get_signal_mapping(
    self,
    bus_signal: MetaElement[arxml.SystemSignal],
) -> dict[MetaElement[arxml.ISignal], list[MetaElement]]:
    """Look up a SystemSignal in the signal map, raising a clear error if missing."""
    if bus_signal not in self.system_signal_map:
        available = sorted(
            s.short_name.value for s in self.system_signal_map.keys()
        )
        ecu_name = (
            self.ecu_instance.short_name.value
            if self.ecu_instance is not None
            else "<unknown>"
        )
        raise KeyError(
            f"SystemSignal '{bus_signal.short_name.value}' is referenced in a "
            f"VariableToSignalMapping but is not present in any FrameTriggering "
            f"on a communication cluster connected to ECU '{ecu_name}'.\n"
            f"\n"
            f"This means the signal chain is incomplete. Ensure ALL of these exist:\n"
            f"  1. SystemSignal (defined)\n"
            f"  2. ISignal referencing the SystemSignal\n"
            f"  3. ISignalIPdu (PDU) containing the ISignal\n"
            f"  4. CanFrame containing the PDU\n"
            f"  5. CanFrameTriggering on the bus referencing the frame\n"
            f"  6. ECU send_frames/receive_frames including the frame\n"
            f"\n"
            f"Available SystemSignals in the map ({len(available)}): "
            f"{available}"
        )
    return self.system_signal_map[bus_signal]  # ty: ignore[invalid-argument-type]
```

Then replace all 4 lookup sites in `runnables.py`:

```python
# Before (4 locations):
) in signal_graph.system_signal_map[  # ty: ignore[invalid-argument-type]
    bus_signal
].items():

# After (4 locations):
) in signal_graph.get_signal_mapping(
    bus_signal
).items():
```

**Impact:** Turns a cryptic `KeyError: <MetaElement>[SystemSignal] - name` into a multi-line error that tells the developer exactly which signal is missing, which ECU it's for, the full 6-step wiring chain to check, and which signals *are* available for comparison.

**Priority:** High

---

## 2. Add DEBUG logging after `system_signal_map` construction

**File:** `tools/autosar/codegen/rte/parse/signals.py`

**Problem:** When debugging signal wiring issues, there's no way to see which signals were successfully loaded into the map without adding temporary print statements.

**Where:** At the end of `SignalGraph._build_system_signal_map()`, after the existing loop.

**Suggested change:**

```python
def _build_system_signal_map(self) -> None:
    """Extracts SystemSignal mappings from a System element."""

    # ... existing code ...

    # Add at the end of the method:
    logger.debug(
        f"system_signal_map built with {len(self.system_signal_map)} signals: "
        f"{sorted(s.short_name.value for s in self.system_signal_map.keys())}"
    )
```

The `logger` import already exists in `signals.py` (`from tools.logging.config import logger`).

**Impact:** When running with `--verbosity 2` or equivalent debug logging, developers immediately see which signals were loaded. If a signal is missing, they know before the `KeyError` even fires.

**Priority:** Medium

---

## 3. Improve `frame_triggering.py` assertion messages

**File:** `pyarch/classic/system/frame_triggering.py`

**Problem:** The assertion messages for missing frame ports tell you *which* port is missing and *which* connector, but don't explain *why* or how to fix it.

**Current code** (lines ~56-58 and ~70-72):

```python
assert (
    frame_port_name in sender.target.frame_ports_by_name
), f"Frame port {frame_port_name} not found in {sender.element.name}{sender.local_context}"
```

```python
assert (
    frame_port_name in receiver.target.frame_ports_by_name
), f"Frame port {frame_port_name} not found in {receiver.element.name}{receiver.local_context}"
```

**Suggested change:**

```python
assert (
    frame_port_name in sender.target.frame_ports_by_name
), (
    f"Frame port '{frame_port_name}' not found in "
    f"{sender.element.name}{sender.local_context}. "
    f"Add '{frame_ref.name}' to the 'send_frames' of ECU "
    f"'{sender.element.name}' in your ecus.py. "
    f"Available frame ports: "
    f"{sorted(sender.target.frame_ports_by_name.keys())}"
)
```

```python
assert (
    frame_port_name in receiver.target.frame_ports_by_name
), (
    f"Frame port '{frame_port_name}' not found in "
    f"{receiver.element.name}{receiver.local_context}. "
    f"Add '{frame_ref.name}' to the 'receive_frames' of ECU "
    f"'{receiver.element.name}' in your ecus.py. "
    f"Available frame ports: "
    f"{sorted(receiver.target.frame_ports_by_name.keys())}"
)
```

**Impact:** The error now tells the developer exactly what to do ("add frame X to send_frames/receive_frames of ECU Y") and lists available frame ports so they can verify their ECU configuration.

**Priority:** High

---

## 4. Add model-level validation for signal wiring completeness

**File:** New method in `pyarch/classic/system/` or `tools/autosar/codegen/rte/parse/signals.py`

**Problem:** The pyarch model allows defining signals, I-signals, PDUs, frames, and VariableToSignalMappings independently. Nothing validates that the full chain is connected until the RTE generator crashes at build time. A validation step at ARXML generation time would catch these issues earlier with a clear error.

**Suggested change:** Add a `validate_signal_wiring()` method to `SignalGraph` that can be called after construction:

```python
def validate_signal_wiring(self) -> list[str]:
    """
    Check that every SystemSignal referenced in VariableToSignalMappings
    is present in system_signal_map (i.e., reachable via frame triggerings).

    Returns a list of error messages for missing signals. Empty list means valid.
    """
    errors: list[str] = []

    referenced_signals: set[str] = set()
    for signal_name in self.inbound_signals:
        referenced_signals.add(signal_name)
    for signal_name in self.outbound_signals:
        referenced_signals.add(signal_name)

    available_signals = {
        s.short_name.value for s in self.system_signal_map.keys()
    }

    for signal_name in sorted(referenced_signals - available_signals):
        ecu_name = (
            self.ecu_instance.short_name.value
            if self.ecu_instance is not None
            else "<unknown>"
        )
        errors.append(
            f"SystemSignal '{signal_name}' is referenced in a "
            f"VariableToSignalMapping but has no FrameTriggering on any "
            f"communication cluster connected to ECU '{ecu_name}'. "
            f"Check that the signal has an ISignal, PDU, Frame, and "
            f"CanFrameTriggering on the bus, and that the ECU lists "
            f"the frame in send_frames/receive_frames."
        )

    return errors
```

Call it after `SignalGraph` construction in `parse_arxml.py` or `runtime_interface.py`:

```python
wiring_errors = signal_graph.validate_signal_wiring()
if wiring_errors:
    for error in wiring_errors:
        logger.error(error)
    raise ValueError(
        f"Signal wiring validation failed with {len(wiring_errors)} error(s). "
        f"See errors above."
    )
```

**Impact:** Catches incomplete signal wiring at the start of RTE generation, before the generator reaches the point where it tries to look up the signal. All missing signals are reported at once rather than failing on the first one.

**Priority:** Medium (higher value but larger change)

---

## 5. Add `--dry-run` or `--validate-only` flag to `generate_rte`

**File:** `tools/autosar/build/generate_rte.py`

**Problem:** The RTE generator runs inside a Bazel sandbox, making iterative debugging slow (~9s per attempt). A validation-only mode would let developers check their signal wiring without running the full code generation.

**Suggested change:** Add a `--validate-only` flag to the CLI:

```python
@click.option(
    "--validate-only",
    is_flag=True,
    default=False,
    help="Only validate signal wiring and ARXML structure; skip code generation.",
)
def main(arxml, ..., validate_only):
    # ... existing ARXML parsing ...

    if validate_only:
        wiring_errors = signal_graph.validate_signal_wiring()
        if wiring_errors:
            for error in wiring_errors:
                logger.error(error)
            sys.exit(1)
        else:
            logger.info("Signal wiring validation passed.")
            sys.exit(0)

    # ... existing code generation ...
```

**Impact:** Developers can run `generate_rte --validate-only` to quickly check their model without waiting for full code generation. Pairs well with change #4.

**Priority:** Low (nice-to-have)

---

## Summary

| # | File | Change | Priority | Effort |
|---|------|--------|----------|--------|
| 1 | `runnables.py` + `signals.py` | Replace bare `KeyError` with actionable error via helper method | High | Small |
| 2 | `signals.py` | Add DEBUG logging of `system_signal_map` contents | Medium | Trivial |
| 3 | `frame_triggering.py` | Improve assertion messages with fix instructions | High | Small |
| 4 | `signals.py` | Add `validate_signal_wiring()` method | Medium | Medium |
| 5 | `generate_rte.py` | Add `--validate-only` flag | Low | Medium |
