# README c3v004: the SELECTED seal pre-stage tuple after FROM_CODEX/0643 (A106) (Claude3)

Written 2026-10-18T23:23:42Z (`date -u`). This supersedes `README_SEAL_ASSEMBLY_C3_c3v003.md` (`e369a27e`) for everything 0643 changes. The selection of record is `SELECTED_SEAL_PRESTAGE_C3SA_c3v004.json`. Codex1 runs the final delta, focused on C-02 to C-06 and the r6/v003 wiring.

## The selected tuple

| role | file | sha256 |
|---|---|---|
| script (root runs it) | `ROOT_SEAL_STEPS_c3v011.sh` | af74e9bde45a5ec0d082ed61f61261757986f1796ebf448746355bf1871111dc |
| per-step helper | `tools/seal_steps_c3sa_c3v012.py` | b13483966fcb8755608d73e05c0e70dc94e39a2b07635f54efc0c86849748bac |
| pinned-source runner (unchanged) | `tools/run_pinned_c3sa_c3v003.py` | 2b040e94a2b74eae981485288471376b86be0784a0a50b59093312c4fd87bf73 |
| in-process fence (unchanged) | `tools/fence_c3sa_c3v003.py` | 9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863 |
| slot draft (unchanged) | `SLOT_VALUES_DRAFT.json` | c93691f5d1931beef8abb656ced3446c99d0adf286d4b5de0c709ecb570284ba |
| step-8 manifest draft (unchanged) | `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` | e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da |

The convenience watchdog `step2_disk_watch.sh` (`bd0d9bab…`) is unchanged, and it stays outside the seal tuple and its hash chain.

**Step 0 refuses** until prereg r6 and seal tools v003 are wired in (P1, P11). Neither is published yet: at 23:21Z `v007_final_prereg_c4/r6/out/` and `seal_tools_v003/out/` were empty, and neither SELECTED file exists. Claude4 0110 (`a2c90720`) names them as `SELECTED_R6_C4V001.json` and `SELECTED_SEAL_TOOLS_V003_C4V001.json`.

## What 0643 (A106) adds

### A. The FINAL V005 addendum
- `V005_FINAL_SHA` (`c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1`) and `V005_FINAL_BYTES` (143081) are constants. The root input `UNT_SEAL_FREEZE_V005_SHA256` is gone.
- Step 1 checks the open file's sha **and** length **before** copying. It then creates the copy exclusively, re-reads it no-follow and re-hashes it.
- The same sha fills the `frozen_addendum` slot. It is also the frozen sha that the dispositions JSON's `frozen_addendum_sha256` must equal.

### C-02 (steps 0, 4a, 10): the text of record
- `PREREG_TOR` must be exactly what `R6_SELECTED` stores (path and sha, from bytes), and it must be an **unsealed** text: every seal slot except `cache_directory_r6_only` is still a PENDING marker.
- At steps 4a and 10, the sealed prereg must be a different file, byte-equal to the text of record with only `seal_slots.<k>.value` filled from the final slots.
- An edited sealed prereg named as its own text of record refuses: MUST_FAIL C02-1, C02-2, C02-3 and C02-7.

### C-04 (step 3b): the slot records against the registry
- The reviewed compare r13 is read once, compiled from that buffer and run inside the fence. Its own `load_producer_registry` loads V009 (`32ddadcb`).
- Each slot is then checked with r13's `gate_record_sha_codes`, `file_pin_codes` and `identity_comparator_codes`:
  - every certificate;
  - every identity record (gate, record sha, producer, comparator and tokens);
  - the identity comparator;
  - any other slotted gate record (B2/B3 where slotted; none are slotted in C4V001).
- **Every slot must PASS. Finding: the current draft fails here (P12).**
  - **EPS_NGC** `1d5eef1b`: its gate is `EPS`, its record sha is not in V009's `gate_records.EPS`, and its producer `eps_ngc91_assemble_c2v001.py` (`04bba30b`) is not in `producers.EPS`.
  - **I1T_NGC** `3ae7981a`: `I1T_NGC` is not a registry gate.
  - Every other slot passes.
- Step 0 also requires the reviewed compare's sha to be r13's `f5adfd11`.

### C-05 and C-06 (step 3, after the binder): the launcher, the guard and the bound command
- **C-05.** The launcher must be the BUILD_V007 row named exactly `route_a_token_launcher_cx1v007.py` (`861bba68…`), and the guard the row named exactly `producer_guard_cx1v008.py` (`294cb776…`). Each name must occur in exactly one row, and the bound plan must name exactly these two pins. "Any allowlisted source" no longer passes.
- **C-06.** The **whole** bound command file must be byte-equal to the binder's output: its fixed comment line plus `shlex.join([PYTHON, -I, -B, launcher, plan, --execute-root-only])`. Both forms are taken from the pinned binder source.

### C-03 (step 8): gates-only provenance (it fit in 10 minutes)
- In the sealed-mode GATES_ONLY body, each of the 8 slotted gate records must have its gate's `record_sha256` equal to the slot's sha and `status` PASS: EPS, LO, GQ, DOUBLING and LO_NGC, plus Z2→B1, Z2_OFF_RO1→B1_OFF and B0prime_RERUN.
- EPS_NGC and I1T_NGC are not gates-only gate records. C-04 covers them.

### C-08: ROOT MANUAL CHECK (it did not fit 10 minutes)
**C-08 is not encoded. Root checks it by hand at assembly, and the seal record must say so (A106.2).**
- **Why it is not encoded:** r13's IMPL `v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md` (`274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3`, 38 lines) contains **no NEW-item id at all**. The root NEW-item list format is also not fixed yet (A81 RI-20).

Exact steps:
1. Verify from bytes the NEW-item list (`UNT_SEAL_NEW_ITEM_LIST_PATH` / `_SHA256`), the IMPL above and the compare `kmax_tail_compare_c2v007_r13_cx3v001.py` (`f5adfd11…`):
   `shasum -a 256 <list> <IMPL> <compare>`
2. List the list's ids. The form is `NEW-<n>`, as r13's own comments use it, e.g. `[NEW-52]`:
   `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B -c 'import re,sys; print(sorted(set(re.findall(r"\bNEW-[0-9]+\b", open(sys.argv[1]).read()))))' <list>`
3. For each id, find it in r13:
   `grep -n -w 'NEW-<n>' <IMPL> <compare>`
   The IMPL will not contain it, so the hit must be in the compare source. Record id, file and line.
4. An id with no hit refuses the seal. Put the (id, file, line) table in the seal record's disclosures, with "C-08 checked by hand by root (A106.2)".

## Wiring r6 and v003 when Claude4 publishes (the successor, from the SELECTED files, from bytes)

### r6
- Set two lines:
  - `PREREG_TOR="<r6 path>"; PREREG_TOR_SHA="<sha>"`
  - `R6_SELECTED=".../SELECTED_R6_C4V001.json"; R6_SELECTED_SHA="<sha>"`
- Step 0's `check-tor` then requires the SELECTED file to name that path and sha, with no other sha for that path. The check is format-agnostic, but it assumes the SELECTED file lists absolute paths. If it lists relative paths, the check refuses and the successor adapts.
- `TABLE_BYTES` derives from r6's own `addendum_read`: `r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md`, `c01b3c51` (0110).
- **Dispositions.** r6's table ends at A106, so the later and changed sets are empty: the dispositions object is `{schema, frozen_addendum_sha256: c01b3c51…, entries: []}`.
  - Whether v003 still takes the flag belongs to the v003 wiring.
  - The helper's empty-entries path is **UNTESTED** until r6 exists.
- **The draft.** If r6 changes its `seal_slots` keys, step 4 refuses (`PREREG_SEAL_SLOTS_KEYS`), and the slot draft needs a successor.

### v003
- Set the five `T_*` paths and shas from `SELECTED_SEAL_TOOLS_V003_C4V001.json`, plus `V003_SELECTED` and its sha. Step 0's `selected-names` checks that the SELECTED file names each tool.
- Set `SEAL_TOOLS_STATUS` to a non-PENDING value.
- Update the RUN forms to v003's module names.
- Add `--addendum-at-text-of-record "$TABLE_BYTES"` to tool 1 (0110).
- Add tool 4 `--check-admission-config` at step 12 (B8), per v003's README.
- Then re-run dry-run passes A and B. With the real v003, pass A needs no shim.

## PENDING (step 0 refuses while P1-P11 are open)

| # | item | now |
|---|---|---|
| P1 | seal tools v003 (A106.2 option (b)) | NOT PUBLISHED. The v001 placeholders stay, and `V003_SELECTED` is PENDING. |
| P2 | compare | r13 `f5adfd11` / SELECTED_R13 `10acd098`, supplied by root at invocation; step 0 now requires r13's sha |
| P3 | driver check record (RI-36) | PENDING_ROOT_RULING: CHECK.md `89a6de88` or R5_REVIEW_FINAL `6758bd24` |
| P4 | EPS_NGC, I1T_NGC (GAP-12) | PENDING_ROOT_RULING (single candidates `1d5eef1b` / `3ae7981a`); see also P12 |
| P5 | dispositions JSON | on r6: `entries: []` (see above); the dry run (r5 stand-in) used A102-A106 |
| P6-P10 | B7 inputs; CASCADE_MAP_R5_ADDENDUM; C5H spelling; ack string; free-space floor | unchanged |
| P11 | **text of record: prereg r6** (C-02) | NOT PUBLISHED. `PREREG_TOR` and `R6_SELECTED` are PENDING; r5 stands in only in the dry run. |
| **P12** | **C-04 scope for EPS_NGC and I1T_NGC** | **PENDING_ROOT_RULING.** Under V009 strict C-04 refuses the draft. Root registers them in a registry successor (which changes the V009 binding A106 keeps) or rules them out of C-04 by name. The script does not guess. |

## Evidence
- **Dry run of record:** `dry_run_20261018T231735Z/INDEX_DRY_RUN_C3SA.md`.
  - Pass A stops at 3b, where C-04 refuses EPS_NGC and I1T_NGC.
  - Pass B passes every step, with S22 logging the C-04 refusal and step 9 STUBBED. C-02, C-03, C-05 and C-06 all PASS. Fence 0; prefix empty.
- **MUST_FAIL, A and C-02 to C-06:** `mustfail_c0x_20261018T232043Z/MUSTFAIL_C0X_RESULTS_C3SA.json`, `b5a15c88…`. 33/33 ALL_OK, each case in its own isolated process.
  - **A refused:** a wrong length; one extra byte; the copy existing.
  - **C-02 refused:** an edited sealed prereg as its own text of record; the same with a forged SELECTED; the genuine sealed prereg as the text of record; a sealed prereg edited outside the slots; a SELECTED file giving another sha; r4 as the text of record; one file given as both.
  - **C-03 refused:** another GQ record; B1 FAIL; LO_NGC missing; a test-mode body.
  - **C-04 refused:** the draft's slots (exactly EPS_NGC and I1T_NGC); GQ V005 `fbceefe6`; the superseded comparator `06ff52d6`; Z2 holding the B1_OFF record; another registry sha.
  - **C-05 refused:** ea_replay as the plan's launcher; shell_filter as the plan's guard; ea_replay given as the launcher; the right name with another sha.
  - **C-06 refused:** an edited non-final (comment) line; an extra line; an edited last line; CRLF.
  - **Controls passed:** A-0, C02-0, C03-0, C04-1 (the slots without the two NGC certificates), C05-0 and C06-0.
- **Regressions on helper c3v012:**
  - W7-S1 and RP-S1: `mustfail_w7rps1_20261018T232131Z/` (`d34db66e…`), 41/41.
  - B1/B3: `mustfail_regress_20261018T232131Z/` (`de9ca480…`), ALL_OK; B3 now covers A102-A106.

## Superseded in this round
- `ROOT_SEAL_STEPS_c3v010.sh` (`2b9d02fa`) and helper `seal_steps_c3sa_c3v011.py` (`7caad125`): the 0642 selection, before 0643.
- `SELECTED_SEAL_PRESTAGE_C3SA_c3v003.json` (`bb95b89b`) and `README_SEAL_ASSEMBLY_C3_c3v003.md` (`e369a27e`).
- `tools/setup_dry_run_c3sa_c3v002.sh` and `tools/make_dry_run_c3sa_c3v004.py`.

Findings F1/F2 are unchanged (README c3v002). The full file list is in `HASHES_C3SA_c3v003.txt`.
