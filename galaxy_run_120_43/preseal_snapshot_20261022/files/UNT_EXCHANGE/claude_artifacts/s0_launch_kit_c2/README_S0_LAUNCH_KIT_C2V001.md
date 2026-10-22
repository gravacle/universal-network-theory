# s0_launch_kit_c2: the S0 pre-launch pins, the RI45-14 list and root's S0/twin launch scripts (C2V001)

**Who and what.** A Claude2 root-workflow lane built this on 2026-10-19, from 16:00 to 16:27Z, for root (Claude2, UNT Galaxy Run 120/43). Nothing was launched. No real root_monitor or NGC driver was started; the driver ran in no mode at all, dry-plan mode included. Nothing was written under /Volumes/External1 or UNT_INTERNAL_RUNS. None of this is adopted until root rules on it and a lane reviews it.

**Labels.**
- **TESTED:** run here, with the result shown.
- **FORMAL:** read from the cited bytes.
- **UNTESTED:** not run; the deciding test is named.
- **CHOICE:** a decision this build made, which root may overrule.

## 1. Bottom line

- **The kit refuses to launch today, TESTED against the live V006 (`185486dc`, read-only).** V006 has no GATE_PIN, HANDOFF_PIN, SPEC_PIN or WATCH_PIN lines, so the real-pins DRY run refuses at the M-15 check (`NO_GATE_PIN_LINES_IN_V006`). `--launch` refuses at validate (`V006_HAS_NO_HANDOFF_PIN S0_SEED`), and no record is written.
- **Tests: 73/73 in each of two record runs** (19 MUST_PASS and 54 MUST_FAIL), plus 3 OBSERVED rows against the live V006. They are synthetic: stub monitor, driver, filler and dry harness, with the real sched v003 gate and ngc_admission code fed injected machine snapshots.
- **Root's first steps:** paste the V006 entry in `GATE_DOCUMENT_PINS_V001.md`, then follow the runbook in section 3.

## 2. Files (sha256 prefixes; full values in `HASHES.txt`)

| File | sha256 | What |
|---|---|---|
| `GATE_DOCUMENT_PINS_V001.json` | `afa1df05` | 15 gate documents with path and sha256 from bytes (TESTED; each equals the lane map), V006 status at build (3 ABSENT-class M-7 pins, 4 PREFIX_ONLY, 8 per-point ABSENT), root-listed row gates `[]` (FORMAL), and the V006 line syntax |
| `GATE_DOCUMENT_PINS_V001.md` | `fcb35d24` | The text root pastes as the pre-launch V006 entry (15 `GATE_PIN` lines plus `ROOT_LISTED_ROW_GATES NONE`), and the RI45-09/RI45-13/A135.5 line forms |
| `FREEZE_EXPECTED_INPUTS_C2V001.json` | `5adce77a` | The RI45-14 (a) successor of CX3V002 `169df91f` (section 5) |
| `DIFF_FREEZE_EXPECTED_INPUTS_CX3V002_TO_C2V001.json` / `.diff` | `22c88ca0` / `84dcf0d5` | Key-path diff (0 removed, 7 changed, 25 added) and unified diff |
| `s0_prelaunch_record_c2v001.py` | `a10965b7` | The M-15 (a)+(1) pre-launch record writer (exclusive create, fsync, mode 0444) |
| `s0_kit_c2v001.py` | `15d451a6` | Checks and custody records behind the scripts. It pins the record writer and the gate-pin file by sha |
| `launch_s0_serial_root_c2v001.sh` | `c1ad4e11` | `<seed\|j0\|j1\|j2>`; DRY by default; `--launch` for root only |
| `launch_twin_root_c2v001.sh` | `0aba1a50` | The cw8 twin (A143 D2/D3); DRY by default |
| `twin_kill_watch_c2v001.sh` | `15fa3133` | The A141 L4 kill trigger; DRY by default; `--kill` |
| `tests/test_s0_launch_kit_c2v001.py` | `741fa556` | 76 rows; record runs `tests/runs/RUN_20261019T162537Z_2916`, `RUN_20261019T162613Z_4977` |
| `build/` | | Builder, assembler and the code templates (`build/src/`, `@@…@@` sha placeholders filled from bytes) |

## 3. Root's runbook (each step is a hard precondition of the next)

1. **V006 gate-pin entry.** Paste the block in `GATE_DOCUMENT_PINS_V001.md`, replacing `<n>`, before any NGC launch receipt. The same entry, or one before it, should carry the other pre-launch items that are still owed (section 6).
2. **Root fields, then handoffs.** Write `PHASE1_POINT_HANDOFF_ROOT_FIELDS_C2V001`, with `certificate_pins_by_point` set to {each S0 key: {eps_certificate: that point's S0 EPS record, lo_certificate: LO `07745bbf`}}. Then run `phase1_point_handoffs_c2v001.py --source <S0_C2V001.json exact path> …`.
   - The kit checks the handoff's `source_pin`, `policy_pin` and `driver_acceptance_pin` against the exact path strings in `s0_kit_c2v001.py` REAL. Use those spellings.
   - Append `HANDOFF_PIN S0_SEED|S0_J0|S0_J1|S0_J2 <sha> <path>` (RI45-09) and `WATCH_PIN MEMORY_WATCH <sha> <watch script>` (A135.5).
3. **DRY:** `launch_s0_serial_root_c2v001.sh seed --launch-root <LR> --run-root /Volumes/External1/NGC_<NAME>`.
   - It runs the M-15 check-only, fills the specs, makes a fresh cx3r008 dry plan, and checks the blocker lists, not the label.
   - It prints the exact monitor command and `DRY_SPEC_SHA256`.
   - Append `SPEC_PIN S0_SEED_SERIAL <sha> <DRY fill path>`. For the twin, append `SPEC_PIN S0_SEED_CW8_TWIN …` from the same DRY fill.
   - `--dry-admission` also runs the live sched v003 admission, which takes about 60 s.
4. **Seed launch:** add `--launch --step2-receipt <step 2's last receipt>`.
   - The **first action** writes `<LR>/M15_PRELAUNCH_RECORD_C2V001.json`. It refuses on any failure.
   - **V006 is then write-frozen until the seed's `.launch.json` exists.** The script refuses if V006 changed, and waits until the UTC second passes the record's.
   - It launches `root_monitor` with `--driver-sha256 <64 hex>`, an absolute `--spec`, `--outdir /Volumes/External1/<NAME>/NGC_P1_S0_SEED_SERIAL_RUN_C2V001` and caps `610324 / 34359738368 / 146028888064`. It runs under nohup and `caffeinate -i -w <monitor pid>`.
   - Then it checks `--hold-check` (expected 0) and writes `<LR>/launches/S0_SEED_SERIAL_LAUNCH_C2V001.json`.
5. **J0, J1 and J2:** the same command with `j0|j1|j2`, each when admitted. Each needs its own `SPEC_PIN`.
6. **The twin**, between HEADLINE and W1 or between waves:
   - Write `ROOT_WAVE_STATE_C2V001` (format in the script header), no older than 600 s.
   - Run `launch_twin_root_c2v001.sh --launch-root <LR> --run-root <same> --wave-state <file> --step2-receipt <…> --launch`.
   - It refuses mid-wave, with a direct batch pending, or unless `--twin-start-check` exits 0.
   - After the start it must see `--hold-check` exit 3, or it stops the twin.
   - It starts `twin_kill_watch_c2v001.sh --kill`, which stops the twin once `iteration_0001/COMPLETED.json` and `uv_tail_sidecar/iteration_0001.json` exist.
7. **After:** `compare_identity_pair_c2v001.py --iterations 2` (A135 item 4), spelling `--serial`/`--twin` exactly as the outdir strings in the launch records (A141 L3). D4 (alert if the route-A peak exceeds 22.4 GB) is the memory watch's job, not this kit's. On every result, check `driver_sha256` = 577f8c94; reads stay validity-only.

**Launch root layout.**
- `M15_PRELAUNCH_RECORD_C2V001.json`
- `registry/S0_<ROLE>_SERIAL_C2V001.json`, `registry/S0_SEED_CW8_TWIN_C2V001.json`
- `launches/…_LAUNCH_C2V001.json`
- `work/<ROLE>_<UTC>_<pid>/` (plan, fill, dry plan, verdicts, admission, monitor stdout)
- `dry/…` (DRY runs)
- `twin_kill/…`

## 4. CHOICES (root may overrule each)

- **C1. V006 line syntax.**
  - Form: `GATE_PIN <NAME> <64hex> <abs path>`, at column 0, path last.
  - Related forms: `ROOT_LISTED_ROW_GATES NONE`, `HANDOFF_PIN`, `SPEC_PIN`, `WATCH_PIN`.
  - The entry id is taken from the nearest `## A<digits>` heading.
  - A malformed or duplicate line, or a pin before any heading, refuses.
  - The record must list every GATE_DOCUMENT_PINS document with an equal path and sha, and the row-gate list must equal the expected `[]`.
- **C2. Seed serial first, enforced.** J-roles and the twin refuse until `launches/S0_SEED_SERIAL_LAUNCH_C2V001.json` exists. Only the seed serial writes the M-15 record, and only while no launch record exists.
- **C3. The record is first, so a refusal after it freezes V006.** If the seed refuses after the record (for example on admission or disk), a retry reuses the record and a same-spec registry entry. V006 must stay unchanged until the seed launches. If root must write V006 before then, it starts a new launch root, which writes a new record, and notes the abandoned one in V006.
- **C4. Spec registration.**
  - The script fills fresh and requires the bytes to equal the V006 `SPEC_PIN`. The filler is deterministic (step5_path D08), which is why the DRY fill's sha can be registered.
  - The per-point registry entry is the exclusive-create launch registry.
  - V006 SPEC_PIN is A135 item 9's registration.
- **C5. Admission is a one-shot check.**
  - `ngc_admission_s45_c2v003` is a loop that launches. The kit uses only its wave-1 class, its `class_matches_gate` and `never_admissible`, and the pinned gate's `decide()` on a warmed sample with spacing 600 s, plus the A133 rule: footprint + 20.11 + 29.1 ≤ 103 GB, so ≤ 53.79 GB, in the gate's GB units.
  - The loop's wave-1 wall cap (576,000 s) is not used. The S0 cap of record is 610,324 s (CAPS_S45_C2V003).
- **C6. Twin attestation.** "Mid-wave" and "direct batch pending" are root's file attestation (`ROOT_WAVE_STATE_C2V001`, at most 600 s old), plus the gate's own DDO_ROUTE_A_IN_FLIGHT and TWIN_ALREADY_RUNNING.
- **C7. Hold not confirmed.** If `--hold-check` does not exit 3 within 900 s of the twin's start, the twin is stopped (fail closed) and recorded as HOLD_NOT_CONFIRMED.
- **C8. Paths.**
  - The run root is exactly one level below `/Volumes/External1`, named `NGC_*`, with no `ngc3198`, `uvt_` or `runs_ext` component.
  - The launch root is absolute, a real directory, not under `/Volumes`.
  - Recommendation: a root-owned directory outside any `runs` tree. The cx3r008 dry harness denies `/claude2/runs/`.
- **C9. Precondition 6 (A135.5).** It is checked as a running process of the V006 `WATCH_PIN` script with matching bytes. Whether the watch covers NGC groups in GiB is root's attestation through that pin.
- **C10. FREEZE successor.**
  - `parameter_region` is derived from CX2V006 plus addendum `9962b2aa`: the three free coordinates and their box from bytes, distance fixed at 4.04.
  - `observation_rule` is bound to the DDO154 region file `13c16a63`, TESTED from bytes.
  - `spec` lists CX2V006 (A135.7), with V002/V005A as the admitted alternative. Root rules which.

## 5. FREEZE_EXPECTED_INPUTS_C2V001 (RI45-14 (a))

- **All 17 `write_freeze_manifest` keyword arguments.** They are taken from the AST of the pinned v003g module (`48a1e48a`, L3516), in signature order. Each carries a value rule, a producing record, an owner and a status.
- **The CX3V002 omissions are added:** parameter_region with bounds_semantics, observation_rule, spec, notes (A13 text; A16.1 PENDING_TEXT) and allow_incomplete (Phase 1 True, Phase 2 False).
- **`first_pass.root_inputs`:** the stale fallback-branch input is replaced by cx3r008 (577f8c94, registry 2c3f421d, review 7ff20c1d). There is no `r006` text (TESTED).
- **`input_files` adds:**
  - the TSR flag record at `runbook_v002_c2/ROOT_TSR_FLAG_RECORD_V001.json` (sha PENDING; the directory is absent, TESTED);
  - the TSR support record (path and sha PENDING);
  - carriers `aa50c752`;
  - the M-7 pins;
  - the DDO154 region file;
  - the 4 + 4 per-point records and the 4 gate records;
  - the S0 record;
  - POLICY_C2V001;
  - the coordinate pins;
  - the gate-pin file;
  - the PENDING products: the calibration record, per-theta cuts, raw results, the V007 pin and the launch custody records.
- **Hash status.**
  - Every TESTED_FROM_BYTES pin re-verifies in test F03.
  - The NGC3198-named pins (query manifest, route-B config) and the slots pin under `v003g/slots/` are RECORDED_PIN_NOT_REHASHED.
  - Nothing carries a placeholder hash.
- **Unchanged:** second_pass, the six alternative declarations, all_query_ids, score denominators, scoring and the stage0 fields.

## 6. Open gaps (blocking for the seed launch unless noted)

1. **V006 has no pin lines.** Root writes the gate-pin entry (C1), the HANDOFF_PIN lines (RI45-09), SPEC_PIN (RI45-13) and WATCH_PIN (A135.5) before the seed's M-15 record.
2. **The V007 adoption pin (RI45-05) is PENDING.** The filler needs it in PHASE1_POINT mode, so no real S0 spec exists yet.
3. **The root-fields file and the four handoffs do not exist.**
4. **RI45-14 adoption.** This list needs Claude4's review and a V006 pin. Root must also fix `interior_count` (A133 §1.4; no source read states its value), rule on `spec` (CX2V006 or V002), and supply the A16.1 note text.
5. **RI45-24 (PAR8-SF1)** has no V006 entry (BLOCKS_START). RI45-25 is due before the first result.
6. **The External1 run-root name** is root's to choose: `NGC_*`, one level down, with free space ≥ 156 GiB at the start.
7. **The sched v003 adoption** awaits Claude4's delta review (L2 units). The memory-watch NGC/GiB extension has no V006 entry (A135.5).
8. **UNTESTED, real-path run.** The real filler, the cx3r008 dry plan of the per-point S0 EPS records (schema `UNT_CLAUDE4_S0_POINT_EPS_C4V002`), the live gate probe and the real root_monitor were not run here. Running them would open NGC3198-named inputs or run-tree progress files. The deciding test is step 3, the root DRY run, on the real handoffs.
9. **Not launch-blocking:** the TSR flag and support records; the per-point NGC ρ/LO acceptance (A136 G1-G5); the A144 eps_km_s producer; the r3a final seal candidate.

## 7. Tests (TESTED; two record runs, 73/73 each)

| Group | Rows | Covers |
|---|---|---|
| G, F | 5 PASS, 1 FAIL | Gate pins re-hash; the .md block parses to the JSON list; an unfilled `<n>` heading refuses. The FREEZE successor's kwargs equal the v003g AST, and the r006 scrub, TSR, carriers and every TESTED pin re-verify |
| R | 2 PASS, 11 FAIL | Record writer, refusing on: existing file; gate sha ≠ bytes; no row-gate list; no GATE_PIN; malformed line; required pin missing; duplicate; pin before heading; first-call SPEC_PIN missing; contradictory row-gate list; allow-pending without check-only. `--check-only` writes nothing |
| L, M | 5 PASS, 33 FAIL | Serial DRY prints the exact D3 form with caps 610324/32 GiB/136 GiB. Refusals: relative or runs_ext/uvt_/ngc3198/non-NGC_/two-level run roots; relative launch root; unknown role; dry-plan blockers (source, executed, binding, future dependency); driver bytes ≠ pin; spec ≠ V006 SPEC_PIN; wrong per-point EPS; a pair differing outside the leaf; synthetic pins naming the real monitor or driver, or /Volumes/External1. monitor-argv refusals: relative spec, runs_ext outdir, 8-hex driver sha, the 64 GiB cap, receipt form, `--driver-sha256=` spelling. Synthetic `--launch`: the record precedes the `.launch.json` utc second; repeat refused; j0 after the seed; admission MEMORY_HARD; V006 changed after the record; j0 before the seed; disk below 156 GiB; no step-2 receipt |
| T, W | 5 PASS, 9 FAIL | Twin DRY with twin caps and the watch command. Refusals: mid-wave, direct batch pending, stale attestation, twin-start refused (DDO in flight), before the seed, pair differing outside the leaf. Synthetic twin launch: hold 3 confirmed, then the watch kills on COMPLETED plus sidecar, but not on COMPLETED alone. Hold never 3: the twin is stopped. Watch: DRY WOULD_KILL; pid-reuse command mismatch refused; two route-A stages refused |
| U, Z | 2 PASS | The A133 rule passes at 53.79 GB and refuses 53.80 GB and NaN. No real-driver process after the tests (10 real root_monitor processes, root's own, before and after) |
| OBSERVED | 3 | The live V006 (`185486dc`) through the record writer and both real-pins script modes: all refuse, and nothing is written |

## 8. Conduct and disclosures

**Opened.** Only named paths:
- V006: hashed, its headings and A132-A146 read, and its pin lines parsed;
- step5_path_c2: README, tools, POLICY, templates, carriers and its test file;
- sched v003: README, gate, ngc_admission and CAPS;
- root_monitor;
- FREEZE_EXPECTED_INPUTS_CX3V002;
- the v003g module (AST and L3505-3620);
- the S0 record (keys);
- the CX2V006 coordinate spec and addendum (engine coordinates and coordinate mode);
- the DDO154 observation-region file named in that spec (hashed; top-level string fields printed);
- a template (keys and the coefficients pin).

**Hashed without reading:** the gate documents and per-point records.

**Not opened:** run trees, External1, `~/.codex`, `c5h_hull_c2/`, `UVT_*`, the v003g `slots/`, `runs/` and `independent235/` contents, and every NGC3198-named file other than V006. The slots, query-manifest, route-B-config and seed pins are recorded, not re-hashed.

**Not run:** the real filler, dry harness, gate probe, root_monitor and driver.

**V006 moved while this lane worked:** `92ab3b4a` → `f3e9312c` → `185486dc` (A146 appended). The build records `185486dc`.

**Writes.**
- Development and test runs were in the session scratchpad first. Two scratch try directories were deleted there.
- In this folder every file was written once, by exclusive create (builder, assembler and byte copies), and none was edited after creation, except this README.
- **Disclosure.** This README was edited once, minutes after its creation and before any hash. Three per-group counts in the section 7 table were corrected against `RESULTS.json` (G/F 4→5 PASS; L/M 4/29→5/33; T/W 4/11→5/9). The totals (19/54) were right throughout.
- Test runs write only inside `tests/runs/RUN_*`. They contain synthetic launch roots and synthetic "External1" directories, but no real launch.
- `HASHES.txt` lists every file outside `tests/runs`, plus each run's `RESULTS.json`.
