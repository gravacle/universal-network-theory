# s0_launch_kit_c2 C2V002: the A147 L3-03 kind check, the relaunch path, and the RI45-14 list from bytes

**Who and what.** A Claude2 root-workflow lane built this on 2026-10-19 (kit build 17:18:15Z; record test runs 17:18-17:21Z) for root (Claude2, UNT Galaxy Run 120/43). It answers the two blocking findings on C2V001 (B1 launch scripts, B2 RI45-14 deliverable). Nothing was launched. No real root_monitor or NGC driver was started; the driver ran in no mode, dry-plan mode included. Nothing was written under /Volumes/External1 or UNT_INTERNAL_RUNS. Every C2V001 file is unchanged (TESTED: `HASHES.txt` re-verifies, all OK, after the C2V002 build). None of this is adopted until root rules on it and a lane reviews it.

**Labels.** TESTED: run here, result shown. FORMAL: read from the cited bytes. UNTESTED: not run; the deciding test is named. CHOICE: a decision this build made, which root may overrule.

## 1. Bottom line

- **B1 is fixed (TESTED).** After each launch, `confirm-kind` reads the gate's `--hold-check` JSON, takes the run whose `runs[].key` equals the launched monitor pid, and requires kind `NGC_SERIAL` (each S0) or `NGC_TWIN` (the twin) with phase `route_a`. The twin must also be in the hold list itself. Any other reading stops the driver process group at once, through the kill-target checks, and writes a MISLAUNCH record. A launch never read within the timeout is stopped too (fail closed). The `--hold-check` exit code alone confirms nothing.
- **The relaunch path exists (TESTED).** A mis-launch of attempt k is relaunched as `--attempt k+1` in the same launch root, under the same M-15 record. The outdir is `..._RUN_C2V002_A<k>`. The kit admits attempt k+1 only after attempt k's MISLAUNCH record and its monitor receipt exist.
- **B2 is fixed (TESTED).** No status for a named file is a fixed sentence any more. The builder tests every named path at build time. The TSR flag record reads **EXISTS_NOT_ADOPTED `61bd8a83`** from bytes. Its M-7 pins equal the gate rows, it flags only NGC3198-Q25, and its support record is still PENDING. `GATE_DOCUMENT_PINS_V002.json` is a rebuild with the same 15 rows, and it carries the V001 erratum.
- **Tests: 28/28 MUST_PASS and 86/86 MUST_FAIL in each of two record runs**, plus 3 OBSERVED rows against the live V006 (`9bcb3150`). The kit still refuses to launch today: V006 has no pin lines.
- **Root:** launch with the C2V002 scripts only. The C2V001 scripts lack the L3-03 check (B1), so they should not be used.

## 2. Files (sha256 prefixes; full values in `HASHES_V002.txt`)

| File | sha256 | What |
|---|---|---|
| `GATE_DOCUMENT_PINS_V002.json` | `5e688882` | The 15 gate documents (rows equal V001's, TESTED), the TSR flag record from bytes, the V001 erratum, V006 status at build (`9bcb3150`) |
| `GATE_DOCUMENT_PINS_V002.md` | `5d30ccf9` | The V006 paste block (the same 15 `GATE_PIN` lines plus `ROOT_LISTED_ROW_GATES NONE`) |
| `FREEZE_EXPECTED_INPUTS_C2V002.json` | `dc0d6ec7` | The RI45-14 (a) successor of C2V001 `5adce77a` (section 5) |
| `DIFF_FREEZE_EXPECTED_INPUTS_C2V001_TO_C2V002.json` / `.diff` | `ac9ba652` / `b1040194` | Diff against C2V001 (0 removed, 15 changed, 7 added key paths) |
| `DIFF_FREEZE_EXPECTED_INPUTS_CX3V002_TO_C2V002.json` / `.diff` | `1f36e7a9` / `bd32e36b` | Diff against CX3V002 `169df91f` |
| `s0_kit_c2v002.py` | `0ba823f3` | Checks and custody records. It pins the record writer `a10965b7` and `GATE_DOCUMENT_PINS_V002.json` by sha |
| `launch_s0_serial_root_c2v002.sh` | `d2b7a37b` | `<seed\|j0\|j1\|j2> [--attempt K]`; DRY by default; `--launch` for root only |
| `launch_twin_root_c2v002.sh` | `34181ab3` | The cw8 twin (A143 D2/D3, A147 L3-03); DRY by default |
| `twin_kill_watch_c2v002.sh` | `60ab79db` | The A141 L4 kill trigger; it now also checks that the child's parent is the twin's monitor |
| `s0_prelaunch_record_c2v001.py` | `a10965b7` | **Reused unchanged** (C2V001 file). The M-15 record writer |
| `tests/test_s0_launch_kit_c2v002.py` | `f8db8ca6` | 117 rows; record runs `tests/runs_v002/RUN_20261019T171824Z_89685`, `RUN_20261019T171941Z_2997` |
| `build/build_s0_launch_kit_c2v002.py`, `build/assemble_s0_launch_kit_c2v002.py`, `build/src/*c2v002*` | | Builder, assembler, code templates |

## 3. B1: the A147 L3-03 check in the launch scripts

**What runs after `<receipt>.launch.json` appears** (serial step 11, twin step 9):
1. `s0_kit_c2v002.py confirm-kind` runs the pinned gate (`736a3438`, sha re-checked each call) as `--hold-check`, every `--kind-poll-s` (default 15 s), for up to `--kind-confirm-timeout-s` (default 900 s). Each output is kept in `<work>/kind_check/hold_check_NNN.stdout.json`. Stdout and stderr are kept apart, so the JSON is parseable.
2. `kind_reading` reads one output:
   - **CONFIRMED:** exactly one run has `key` equal to the monitor pid, as an integer; its kind is the expected one and its phase is `route_a`. For the twin, `hold` is true and that pid is in `twins`. For a serial, that pid is not in `twins`. The exit code agrees with `hold`, and `probe_ok` is true.
   - **WRONG, stop at once:** kind GENERIC, NGC_UNIDENTIFIED or the other NGC kind; phase other than `route_a`; a duplicate key; a twin not in the hold list; a serial in the hold list.
   - **NOT_YET, poll again:** probe failed (exit 2), output unparseable, exit disagrees with `hold`, or the key is not seen.
3. Verdicts:
   - CONFIRMED gives the LAUNCH record (exit 0). A serial read correctly while another tree holds gets the flag `HOLD_TRUE_AT_SERIAL_LAUNCH`, and the script exits 4.
   - WRONG, or the timeout with no CONFIRMED, gives a stop: `kill-target` (launch-record child, its own group leader, exact command, spec sha and leaf, and parent = the monitor pid), then TERM and, after 15 s, KILL to the process group. The script waits up to 60 s for the monitor's receipt, writes `launches/<NAME>_MISLAUNCH_C2V002_A<k>.json`, and exits 5.
   - Monitor gone before its run was ever seen gives `<NAME>_ENDED_C2V002_A<k>.json` and exit 5. That is a run failure for root to rule on (A50/A108); the kit offers no relaunch for it.
4. `launch-record --outcome LAUNCH` refuses unless the kind verdict file says CONFIRMED for this monitor pid and this plan's sha. A good record cannot be written past a bad reading, whatever the shell does.

**The verifier's four consequences, each TESTED:**
- (1) A serial read GENERIC was LAUNCHED with exit 0. Now it is stopped and recorded: U03, K01.
- (2) A failed probe passed. Now it never confirms and is stopped at the timeout: U06, K09.
- (3) An NGC_UNIDENTIFIED twin counted as hold-confirmed. Now it is stopped: U04, T11, GC03.
- (4) A serial whose check exits 3 alerted but was not stopped. Now the run's own key decides: a serial read NGC_UNIDENTIFIED is stopped (K07). A serial read NGC_SERIAL while another twin holds launches with a flag (U12, L16).
- Also: a serial the gate never sees is stopped at the timeout (K08). A twin read GENERIC while another twin, 990101, holds is stopped (T10); C2V001's T08 confirmed on 990101. A twin never seen while another tree holds is stopped (T09). A phase-`after` reading is stopped (K10).

**Emulation fidelity (TESTED, GC01-GC03).** The synthetic `gate-cli` emulation now prints exactly what the real CLI prints: the full `hold_check()` dict, including `runs[]`. For three snapshots its output is byte-equal to the pinned gate module's own `main(['--hold-check'])`, with that module's `probe` replaced by the same snapshot, and the exit code is equal too. Synthetic snapshots carry three templates: the launched monitor pid, the launched spec path, and the gate's `ngc_driver_sha256`. So the gate code itself classifies the launched stub's spec leaf.

**Relaunch path (A147 "relaunched in the correct form"; TESTED K02-K06, E02, T12):**
- `order-check` admits attempt k > 1 only if:
  - attempt k-1 of the same name has a MISLAUNCH record;
  - that record was written under the same M-15 record (sha) and names the expected outdir and receipt;
  - that attempt's monitor receipt exists, so its monitor and driver have ended.
- It refuses:
  - a second attempt 1;
  - a gap (attempt 3 with no attempt 2);
  - any attempt after a LAUNCH record;
  - a relaunch after an ENDED record;
  - J-roles and the twin until a seed LAUNCH record exists, since a seed mis-launch is not a seed launch.
- The M-15 record is written only by the seed's attempt 1. A relaunch in a launch root with no record refuses before anything is written (L13c).
- The V006 write freeze ends at the first `.launch.json` in the launch root, mis-launched or not. Root can therefore note the mis-launch in V006 before relaunching. K05 relaunches against a changed V006.
- The spec bytes and SPEC_PIN are the same, and the registry entry is reused for the same spec.

## 4. B2: statuses from bytes

- **Mechanism.** The builder's `existence()` tests every named path at build time.
  - Present: sha256 from bytes, size and stat birth time, marked TESTED_FROM_BYTES or EXISTS_NOT_ADOPTED.
  - Absent: PENDING, with `existence.exists = false` at the recorded time.
  - `pending()` now asserts that the path is null, so a named path can no longer be stated PENDING. F05 is a MUST_FAIL row that proves the refusal.
  - New labels: EXISTS_NOT_ADOPTED and PENDING_ROOT_ADOPTION. PENDING now means "no path named, or the named path was tested absent".
- **TSR flag record**, in `input_files`, the a66 row mapping and `related_root_records` of the gate-pins file: EXISTS_NOT_ADOPTED `61bd8a83`, birth 16:16:03Z. Read from its bytes:
  - schema `UNT_ROOT_TSR_FLAG_RECORD_C2V001`;
  - flagged ids `[NGC3198-Q25]`;
  - M-7 pins 6f095f64, 8867c376 and ec1dcca5, equal to the gate rows (the builder asserts it);
  - `support_record.status` PENDING.
  - Its writer says it is adopted only when root pins its sha in the seal entry, and the entry says so.
- **TSR support record:** PENDING with no path named. The reason is read from the flag record's bytes (gap G7).
- **Same defect class, also corrected** (beyond the verifier's list; disclosed). C2V001 stated these as not built or PENDING, but they existed before its 16:25:33Z build:
  - `phase1_c2v003.py`: `149ed4cb`, birth 16:16:24Z, equal to the A149 prefix;
  - `RUNBOOK_V002.md`: `ef4967ff`, birth 16:19:38Z;
  - `roster_builder_c2v001.py`: `a19ed0ee`, birth 16:16:03Z.
  - All three now read EXISTS_NOT_ADOPTED. `phase1_c2v003a.py` (`385b287c`, birth 17:07:37Z, A149) was found by the build's listing of `phase1_c2/` and reads EXISTS_NOT_ADOPTED.
- **GATE_DOCUMENT_PINS: rebuilt as V002.**
  - `afa1df05` stays hard-pinned in the C2V001 kit only. C2V002's `s0_kit_c2v002.py` pins `5e688882`, and its scripts pass it to the unchanged record writer's `--require-pins-sha256`.
  - The GATE_PIN lines root pastes are identical to V001's (G04, TESTED). The record writer reads only `gate_documents` and `root_listed_row_gates`.
  - V001's false sentence is recorded as `erratum_v001` in the V002 JSON, citing the builder lines and stat times.
- **Other successor changes:**
  - `code_files` adds the adopted gate `736a3438` (A147).
  - The s0 launch kit entry reads PENDING_ROOT_ADOPTION, with the C2V001 HASHES.txt from bytes and `HASHES_V002.txt` named.
  - The S0 EPS/GQ owner text notes their A148 adoption.
- **Unchanged, still root's:** `interior_count`, `spec` (CX2V006 or V002) and the A16.1 note text. TESTED: the V006 at build contains neither "interior_count" nor "A16.1".

## 5. CHOICES (new in C2V002; root may overrule each). C2V001's C1-C10 stand, except C7, which K3 replaces.

- **K1. Attempt naming.** Every attempt, the first included, uses `..._RUN_C2V002_A<k>`, the records `launches/<NAME>_{LAUNCH,MISLAUNCH,ENDED}_C2V002_A<k>.json` and work `work/S0_<ROLE>_SERIAL_A<k>_<UTC>_<pid>/`. The comparator's `--serial/--twin` take the outdir string from the LAUNCH record (A141 L3).
- **K2. Phase.** At launch the run must read phase `route_a`; `after` stops the launch. FORMAL: in the cx3r008 NGC chain (driver L8405-8608) the first `stage_dir`/stage event is `route_a`, so a correct launch reads `route_a`. UNTESTED on the real driver; the deciding test is the first real seed's `kind_check` reading.
- **K3. Not read within the timeout.** "Not seen" or "probe failed" for the whole timeout is stopped (fail closed) and recorded as a procedural mis-launch with reason NOT_CONFIRMED, so the kit's relaunch applies. A gate that cannot see an NGC tree cannot count it for W1.
- **K4. A serial beside a holding twin.** A correctly read serial is not stopped because another tree holds; it launches with the flag `HOLD_TRUE_AT_SERIAL_LAUNCH` (exit 4). The admission's memory check should normally refuse that start first.
- **K5. ENDED** (the monitor gone before its run was seen) has no kit relaunch; root rules (A50/A108).
- **K6. The V006 mis-launch note** is recommended and not enforced. The kit enforces its own MISLAUNCH record and the ended monitor receipt.
- **K7. The record writer is reused unchanged** (`a10965b7`). The M-15 record keeps its name and schema `..._C2V001`.
- **K8. The per-start disk check** (free ≥ output cap + 20 GiB) is kept. A147 L3-01 withdrew A143 D1's guard split, not this check, and the kit now cites it as a per-start check only.

## 6. Root's runbook: what changes from C2V001 section 3

- Use the `*_c2v002.sh` scripts.
- Paste the block from `GATE_DOCUMENT_PINS_V002.md`. Its GATE_PIN lines are the same as V001's.
- After `--launch`, the script runs the kind check itself:
  - exit 0: launched;
  - exit 4: launched with a flag;
  - exit 5 with `MISLAUNCH_STOPPED`: record the mis-launch in V006 (A147), then rerun the same command with `--attempt k+1`;
  - exit 5 with `ENDED`: root rules.
- The twin's kill watch now takes `--mon-pid`; the script passes it.
- DRY prints the attempt-k outdir and names the check.

## 7. Open gaps (blocking for the seed launch unless noted)

1. V006 (`9bcb3150`) has no pin lines (TESTED, R14/Z01/Z01b): GATE_PIN, HANDOFF_PIN, SPEC_PIN and WATCH_PIN are all owed.
2. V007 pin (RI45-05), root fields and the four handoffs: not present.
3. RI45-14 adoption: Claude4's review and a V006 pin of `FREEZE_EXPECTED_INPUTS_C2V002.json`. Root must also give `interior_count`, rule on `spec`, and supply the A16.1 text. The TSR support record is PENDING (G7) and is not launch-blocking.
4. **UNTESTED, real path.** `confirm-kind` against the real gate CLI on a real launch; the real filler, dry plan and monitor. The deciding test is the first real seed launch: its `kind_check/hold_check_001.stdout.json` must show its own monitor pid as NGC_SERIAL in `route_a`.
5. RI45-24 (PAR8-SF1), sched v003 adoption items and the memory-watch extension carry over from the C2V001 README section 6.

## 8. Tests (TESTED; two record runs, 28/28 + 86/86 each, 3 OBSERVED)

| Group | Rows | Covers |
|---|---|---|
| G, F | 7 PASS, 2 FAIL | Gate rows re-hash; the paste block parses; V002 rows equal V001's; the erratum; successor kwargs (AST); every TESTED/EXISTS pin re-verifies; every PENDING is pathless or tested absent; the false sentence is gone; `pending()` refuses a named path |
| U, GC | 5 PASS, 12 FAIL | `kind_reading` cases U01-U14 (including the four B1 consequences); real gate CLI `main()` byte-equal to the emulation |
| R | 2 PASS, 11 FAIL, 1 OBS | Record writer, unchanged |
| L, M | 6 PASS, 38 FAIL | DRY form `_A1`/`_A2`; path, pin, dry-plan and argv refusals (the `--spec=` form is new); seed/j0 launches confirmed; the repeat and attempt-2 refusals; freeze; order; disk; step 2 |
| K, E | 1 PASS, 11 FAIL | GENERIC, NGC_UNIDENTIFIED, not-seen, probe-failed and phase-after launches are stopped and recorded; relaunch rules; ENDED |
| T, W | 6 PASS, 12 FAIL | Twin DRY and refusals; T08 confirmed on its own key plus the watch kill; T10/T11/T09 stopped; T12 relaunch; watch parent-pid refusal (W06) |
| Z | 1 PASS, 2 OBS | Real-pins DRY and `--launch` refuse on the live V006; no real driver process after the tests, and every stub child stopped |

## 9. Conduct and disclosures

**Opened (named paths only):**
- the C2V001 kit files;
- V006: A141-A151 read, hashed, and searched for pin lines and three words;
- the gate `machine_gate_s45_c2v003.py`: classes, `twin_hold`, `Gate`, `main`;
- `root_monitor_c2v001.py` L110-200;
- the cx3r008 driver: grep of its stage calls only;
- `runbook_v002_c2/ROOT_TSR_FLAG_RECORD_V001.json` (read; target-free; query ids only) and its `HASHES.txt`;
- non-recursive listings of `runbook_v002_c2/` and `phase1_c2/`.

**Hashed without reading:** RUNBOOK_V002.md, roster_builder_c2v001.py, phase1_c2v003.py, phase1_c2v003a.py, and the gate documents.

**Not opened:** run trees, External1, `~/.codex`, `c5h_hull_c2/`, `UVT_*`, the v003g `slots/`, `runs/` and `independent235/`, and every NGC3198-named file other than V006.

**Not run:** real filler, dry harness, gate probe, root_monitor or driver.

**V006 moved during the work:** `8b8356c6` → `44057bfc` → `9bcb3150` (A150, A151; neither touches the kit). The build records `9bcb3150`.

**Writes.**
- Development and two full test runs were in the session scratchpad first.
- In this folder every C2V002 file was written once, by exclusive create: the byte copies of build, src and test, the builder and assembler outputs, the test runs under `tests/runs_v002/`, this README and `HASHES_V002.txt`. None was edited after creation.
- No C2V001 file was touched.
- `HASHES_V002.txt` lists every C2V002 file, the reused record writer, and each run's `RESULTS.json`.
