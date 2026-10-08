# Independent audit invocation correction

2026-09-29. The first invocation of the new, unfrozen `native_thermal_packet_saved_audit_v001.py` stopped at Python parsing, before any audit arithmetic: an extra closing parenthesis in the summary-only connected-probe off-diagonal maximum (line 154) caused `SyntaxError: invalid syntax`. Removed that one parenthesis and retried the saved-data audit. No producer, original artifact, physical input, scientific tolerance or source was changed; no propagation or eigenproblem was run by the auditor.

The second invocation reached JSON publication but refused a NumPy `int64` in the descriptive inverted-line count. Added an explicit `int(...)` conversion to that count and repeated only the saved-array arithmetic. These are auditor implementation corrections, not changes to the frozen scientific packet or its controls.
