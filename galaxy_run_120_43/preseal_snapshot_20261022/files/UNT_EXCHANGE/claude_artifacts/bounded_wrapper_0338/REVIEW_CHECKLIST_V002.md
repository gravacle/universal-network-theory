# V002 wrapper: custody-accounting repair (task 0338). Review-read checklist

- **Candidate:** `readiness_fixed_probe_cij_root_launch_wrapper_v002.py`. V001 is preserved unchanged (sha 227dd2f5…).
- **Exact diff:** `V001_to_V002.diff` (unified).
- **Scope:** custody only. No change to the producer pin, inputs, cases, scientific predicates, output paths or caps. The receipt hierarchy is documented in the module docstring.

## What changed
1. **Streaming `pin()`:** 1 MiB chunks, so memory stays bounded while hashing outputs of up to 32 MiB.
2. **Reordered finalization:**
   - **Phase A:** output hashes and stderr check.
   - **Phase B:** measure wall and peak RSS, then a provisional verdict. The primary receipt is serialized in memory, checked against its reserved budget, then written exclusively (`xb`, fsync).
   - **Phase C:** wall and peak RSS measured again *after* the primary write. A small exclusive **TERMINAL receipt** carries the authoritative status.
3. **Receipt hierarchy.** The primary receipt's status is `PROVISIONAL_<verdict>` and it is never the acceptance record. The terminal status is authoritative. Each of these means FAILED_OR_INCOMPLETE:
   - no terminal receipt;
   - no primary receipt;
   - an accounting exception;
   - postwrite wall > 10 s;
   - postwrite peak RSS > 256 MiB;
   - total created bytes over the cap.
4. **Output accounting.**
   - `RECEIPT_RESERVE` = 1 MiB inside the unchanged 32 MiB cap, so the producer files' live cap is 31 MiB.
   - The primary receipt must fit within the reserve minus `TERMINAL_MAX` (64 KiB). The terminal receipt is capped at `TERMINAL_MAX`; if oversized, a minimal FAILED record is written instead.
   - Terminal check: producer bytes + primary bytes + `TERMINAL_MAX` ≤ 32 MiB.
5. **Bounded unmeasured interval.** Only the terminal receipt write itself (≤ 64 KiB) is unmeasured. This is documented, with no recursive self-measurement.
6. **Inherited from V001 unchanged:**
   - fail-closed preflight;
   - the new terminal path is added to the no-overwrite list;
   - one child, `-B`, optimization prohibited, process-group SIGKILL;
   - per-owner stdout/stderr files;
   - no retry, and no cap change.

## Points for the reviewer to confirm
- [ ] **WALL semantics.** The authoritative check now requires the whole envelope, including the custody tail, to finish within 10 s (postwrite). That is stricter than V001, and intended.
- [ ] **Reserve size.** 1 MiB comfortably covers the primary receipt: about 500 RSS samples at roughly 70 B each, plus pins. Should the producer's live cap move to 31 MiB, or should the reserve shrink?
- [ ] **Two acceptable outcome splits.**
  - Provisional pass with terminal fail: a tail overrun. Reported as FAILED_OR_INCOMPLETE.
  - Primary missing with terminal present: reported as FAILED.
- [ ] **Separate preflight.** Input pin hashing remains documentary preflight outside the timed child envelope, as V001's review allowed.
- [ ] **Output names.** Kept at the V001 `_V001` suffixes, since the task fixes paths. Rename to `_V002` if root wants output names tied to the wrapper version.

## Validation done (scratch only; no scientific producer)
- **Checks:** AST parse OK.
- **Control-flow test:** a scratch copy with paths and pins substituted to a dummy producer was run under three scenarios:

| Scenario | Terminal | Primary | Notes |
|---|---|---|---|
| ok | COMPLETED_WITHIN_ENVELOPE | PROVISIONAL_COMPLETED… | |
| slow (12 s) | FAILED_OR_INCOMPLETE | — | WALL_CAP; postwrite wall false |
| exit 3 | FAILED_OR_INCOMPLETE | — | |

- **Not done:** the real producer was not imported, compiled or executed. No launch.
