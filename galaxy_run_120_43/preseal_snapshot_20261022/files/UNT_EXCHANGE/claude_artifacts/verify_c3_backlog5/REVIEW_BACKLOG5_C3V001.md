# Review of backlog #5 (cw8 v003-N2 and v003-N3, Codex1 0284): **PASS, 0 blocking.** Six NOTEs

**Reviewer:** Claude3, distinct from the builder, Codex1 (D034). **Date:** 2026-10-22T14:09:10Z (`date -u`). **Contract:** D034 (0371).

## Objects (sha256 from bytes; all equal 0284 and the packet)
- Packet `cw8_hardening_cx1/REVIEW_PACKET_CX1V001.json` — `66efb4304c13f378ee7ec67d81c59ea632a7e5ae38603357b24e6862b78373f5`
- Entry `select_workers_diagnostic_cx1v001.py` — `5a93c37122e416e0d2230ec25be256ec10d913536479f3f1d4de7e6c44ed6eaa` (read in full, 91 lines)
- N3 test `test_lock_diagnostic_cx1v003.py` — `b55c4550…487a`. Its report is `inert_n3_v003/REPORT.json` `33a89bf9…1e94`.
- N2 test `test_comparator_form_cx1v001.py` — `c6cdb19d…8d84`. Its report is `inert_n2_v001/REPORT.json` `5fcd27ee…90f1`.
- Underlying tool: `cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py` `4d5b47e7…919d`, the newest cw8 launcher in its folder, unchanged.

## Reproduction
Both author suites were re-run in fresh folders with `$PY` 3.12.14 `-I -B` at background QoS. **Both reports are equal to the authors' reports:**
- N3: 11 checks.
- N2: 6 controls, plus 6 mutants that are all detected.

## D034 contract: all items hold
- **Record:** `CW8_LOCK_REFUSAL_RECORD_V001` with exactly the nine D034 fields. It is written with O_EXCL, O_NOFOLLOW and mode 0444, fsynced, and its parent is fsynced too.
- **Destination:** the path must be absolute and normalized; its parent must exist and resolve without symlinks; it must have no `worker_choices` component; and it must not already exist. The choice folder is exactly `<p112_launch_root>/worker_choices` (tool L3186), so the component check covers it.
  - The missing-root guard can be reached only when the destination is the missing launch root itself. My probe P3b shows that this refuses `CW8_REFUSAL_RECORD_MISSING_ROOT` and creates no root.
- **Evidence only:**
  - only the three lock codes (L3340–3355), each raised before the `select_workers` body, produce a record;
  - the original refusal is re-raised with a bare `raise`;
  - every other refusal passes through unchanged;
  - an invalid destination refuses before the selector runs.
- **No cohort is published after a lock failure:** the body never runs, so `worker_choices` is never created.
- **The launcher is byte-unchanged.** It is loaded by full sha. Its CLI dispatch calls `select_workers` by its global name (L2548), so the guard is on the real path.
- **Tests:** every D034 test item is present, including the choice-writing mutant, which the no-choice oracle detects.

## Independent probes through the REAL Context and the unchanged CLI (`probe_n3_cli_c3.py`, `probe_n3_missing_root_c3.py`)
The author's tests run the lock refusals only through `select_with_refusal` with a stub ctx. These probes run them end to end:

| Probe | Result |
|---|---|
| P1: FILE refusal (the lock is a directory) | The entry's stdout and rc are **byte-identical** to the unchanged CLI's (rc 2, `CW8_CHOICE_LOCK_FILE`). The record holds the nine fields, the **real Context `config_pin`**, the correct lock path and mode 0444. No `worker_choices` folder exists. |
| P2: IDENTITY refusal (simulated inode substitution) | rc 2, the code is preserved, the record is written, and there are no choices. |
| P3: root given as a symlink | The Context refuses `CONFIG_SYMLINK` first. That is not a lock code, so no record is written, and stdout is identical to the unchanged CLI's. |
| P3b: missing launch root | The unchanged CLI and the entry both refuse `CW8_CHOICE_LOCK_ROOT`. The record is written outside the root. A destination at the root path refuses `MISSING_ROOT`, and the root is never created. |
| P4: an existing destination, and one under the real `worker_choices`, on a fixture that would otherwise succeed | Both refuse before selection (`EXISTS`, `CHOICE_DIRECTORY`). No CHOICE file is written. |
| P5: success without `--refusal-record` | Same keys, status, workers and reason as the unchanged CLI. |
| P6: arguments with `select-workers` not first | argparse exits 2 (invalid choice) before anything is read. See NOTE B5-1. |
| P7: a one-byte-altered tool copy | `load_tool` refuses `CW8_DIAGNOSTIC_TOOL_PIN`. |

## NOTEs (none blocking; A115: no honest-path refusal or physics change)
- **B5-1. Argument order.** `select-workers` must be the first argument. Otherwise the entry's `parse_known_args` takes a value such as the config path as the command and exits 2 (P6). It fails closed and loudly. The README should give the exact command form.
- **B5-2. Refusal format.** A tool-pin failure, or any other non-`Refusal` error raised before `M.cli` runs, exits with a traceback (rc 1) rather than the CLI's JSON refusal. It fails closed; the difference is cosmetic.
- **B5-3. The publication-time recheck.** If `destination_check` fails just before the write, which can happen only in a race, its `CW8_REFUSAL_RECORD_*` code replaces the lock code. It is still a refusal and still writes no choice. A successor could report both codes.
- **B5-4. Module patch.** `cli` patches `M.select_workers` and never restores it. That is harmless in the one-shot process. My probes restore it between calls.
- **B5-5. Coverage.** The P1/P2/P3b end-to-end cases could join the suite in a later version.
- **B5-6. Cosmetic.** Line 8 of `test_comparator_form_cx1v001.py` is dead code (`… if False else None`).

**Verdict:** backlog #5 is **PASS** and ready for root adoption, separately from #4. Adoption, and the exact command form under B5-1, are root's decisions.
