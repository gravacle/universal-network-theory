# sched_s45_c2 v003: A140 N1–N5 (foreign-tree classes by driver, the twin hold, NGC and DDO output caps, one wall constant)

Claude2 (root workflow), 2026-10-19, built 14:20–15:10Z. Ruling: A140 (`FROM_CODEX/0706`), on Claude4's review of v002 (`FROM_CLAUDE4/0192`, N1–N5).

**Scope.** Only scheduling, admission and per-call caps change. Physics inputs are byte-identical: 78 pins equal their bytes, and the numerics canonical sha256 `4b2a5a87…` equals R9's. Nothing was launched. No result, array, node-diagnostic, C5H, `UVT_*`, run-tree or NGC target file was opened.

**Folder.** Every v002 file is unchanged (test Z04 checks all 27 non-test entries of `HASHES_S45_C2V002.txt` against their bytes). `DIRECT_BATCH_PARAMS_S45_C2V003.json` (`b7fdaf10`) is root's own file, published under A139 at 14:05Z, before this build. This build did not write it or change it. The v003 direct-batch successor is therefore named `…C2V003A.json`.

**Labels.**
- MEASURED: read from bytes or from the live machine.
- DERIVED: arithmetic on MEASURED or FORMAL inputs.
- ASSUMED: a stated choice.
- FORMAL: read from cited bytes.

Simulated durations are model outputs (UNTESTED as forecasts). The sim is seeded and replays deterministically.

## 1. What changed (and nothing else)

| Item | v002 | v003 |
|---|---|---|
| **N1** foreign trees | Every foreign tree used the generic class: 11 GB plus a 20 GB spike, counted as pooled (+5.79 GB growth) when it had ≥ 4 processes or was young. One serial NGC tree refused a second DDO route-A call (84.59 GB). Three such trees refused every start. | **Classed by driver.** A monitor whose `--driver-sha256` is cx3r008 (`577f8c94`) gets its spec leaf `numerics.route_a.column_workers` read once. The leaf decides the class: **NGC_SERIAL** (= 1): 6.0 GB + 16.4 GB spike, not pooled, 10.0 GB after route A. **NGC_TWIN** (> 1): 11.0 + 50.3 = 61.3 GB, pooled. **NGC_UNIDENTIFIED** (leaf unreadable): sized as the twin. Every other driver keeps the v002 generic class unchanged. |
| **N1** sizing check | none | `check_foreign_classes` runs at `Gate()`. It refuses a serial class below the RI45-12 U peak (20.11 GB) or the U steady (3.72 GB), and a twin class below the cw8 U transfer peak (61.3 GB). v002's twin sizing, 36.8 GB, fails this check (G33b, G33c). |
| **N2** twin hold | The gate did not know about step5_path L146. It admitted a DDO route-A call beside the twin (G34e). | **While a twin is in route A, every family-DDO head is refused with `TWIN_HOLD`.** The campaign's calls are family DDO. NGC_SERIAL heads are not held; memory refuses them (83.7 GB). An unidentified tree holds only until 22,752 + 600 s. An overdue twin keeps holding and is flagged. |
| **N2** predicates for root | none | `twin_hold()` and the CLI `--hold-check` gate direct batches (exit 0 clear, 3 hold, 2 probe failed = hold). `twin_start_check()` and `--twin-start-check` gate the twin itself. The twin class goes through the memory rule, and the check also refuses on `DDO_ROUTE_A_IN_FLIGHT` or `TWIN_ALREADY_RUNNING`. |
| **N3** S0 NGC output cap | 136 GiB loop value, labelled a derived estimate. step5_path still used 64 GiB. | The named constant `NGC_S0_OUTPUT_CAP_BYTES` = **136 GiB** sits in `ngc_admission_s45_c2v003` and `caps_s45_c2v003`. `CAPS_S45_C2V003.json` gives the S0 serial caps for root's commands: wall 610,324 s, RSS 32 GiB, output **146,028,888,064** (was 68,719,476,736). The twin caps are unchanged. |
| **N5** DDO output cap | 56 GiB | **80 GiB** for `per_call.output_cap_bytes`, `disk_guard.per_call_bytes` and the tail-ON direct-batch caps. Margin: 1.52 × the 32-iteration MEASURED-rate projection (52.6 GiB). |
| **N4** DDO wall cap | 100,800 s, set in two builders | **One named constant**, `caps_s45_c2v003.DDO_TAIL_ON_WALL_CAP_S = 100800` (PROVISIONAL). The delta, the config successor, the orphan wait (wall + 600 s) and the 31 tail-ON direct-batch caps all derive from it. The literal appears once in v003's code (Y05). |

The gate's limits, reservations, spikes, growth, route-A cap, cores, swap, spacing, warm-up, probe and phase rules are v002's. With no cx3r008 tree on the machine, v003 decides exactly as v002:
- G38 checks 54 decision batteries;
- M01 replays v002's chosen-variant campaign rows, and they come out equal seed by seed.

## 2. Re-simulation: S0 ×4 serial + the cw8 twin beside HEADLINE11 and the campaign

**Model.** `sim_s45_c2v003.py` keeps every v002 model function and adds a joint engine.
- **HEADLINE11.** The packet ramp rule at max_active 1, from T0.
- **Campaign.** The campaign waves start when HEADLINE ends.
- **S0 ×4.** Four serial NGC calls, Claude4 RI45-12 E/U segments. They have their own launcher through the gate, with spacing 600 s.
- **The twin.** Claude4 §7 transfer peaks: 33.5/49.6 GB at iteration 0 and 45.2/61.3 GB after (E/U). Iteration 1 ends at 1.98 h (E) / 3.16 h (U). The planned stop is the 22,752 s wall.
- **Twin start.** Root starts the twin at the first poll after HEADLINE ends with no direct-batch call pending and no wave half-admitted:
  - OLD = gate v002 + root's A133 103 GB procedure, with no hold;
  - NEW = `twin_start_check` + `TWIN_HOLD`.
- **S0 modes.**
  - **H2:** S0 eligible at T0.
  - **preW1:** S0 eligible 2,400 s before W1, so all four are in route A when W1 starts. This is the W1-halt case.
  - **twin_first:** S0 eligible after the twin stops.
- **Seeds and rows.** 3 seeds, wave shapes LAUNCH_ORDER and ENGINE_SHAPED, and DDO rows expected (NGC E), high (U) and stress32 (U).

### Durations, median hours from T0 to the campaign's end (LAUNCH_ORDER / ENGINE_SHAPED)

| Row | expected: OLD | expected: NEW | high: OLD | high: NEW | stress32: OLD | stress32: NEW |
|---|---|---|---|---|---|---|
| no S0, no twin (both rules equal) | 182.75 / 170.70 | same | 557.49 / 535.92 | same | 379.90 / 389.51 | same |
| S0 H2, no twin | 186.73 / 174.72 | 189.76 / 177.13 | 561.67 / 543.17 | 564.82 / 545.98 | 400.05 / 408.76 | 409.30 / 416.18 |
| S0 H2 + twin | 189.00 / 175.54 | 194.58 / 181.13 | 561.67 / 543.17 | 566.46 / 545.98 | 406.30 / 409.82 | 409.30 / 419.56 |
| S0 preW1, no twin | 204.33 / 192.57 | 200.10 / 192.73 | **618.62\* / 597.42\*** | 596.76 / 570.38 | **437.94\* / 447.58\*** | 426.25 / 418.64 |
| S0 preW1 + twin | 204.33 / 192.57 | 205.20 / 193.63 | **618.62\* / 597.42\*** | 599.02 / 574.04 | **443.97\* / 447.99\*** | 427.79 / 419.80 |
| twin first, then S0 | 205.08 / 192.82 | 207.10 / 198.05 | 614.22† / 597.16† | 603.74 / 576.83 | 439.70† / 446.79† | 430.73 / 422.59 |

\* W1 NOT_STARTED: W1 waits 53.4 h, past the 48 h wave cap. That is the CAMPAIGN_NOT_STARTED INFRA halt; the sim lets W1 start late so that a duration can be printed.
† OLD leaves extra calls NOT_STARTED in W2, because S0 ×4 is in route A after the twin: high 6 (LAUNCH_ORDER) and 22 (ENGINE_SHAPED; baseline 14); stress32 6 and 10 (baseline 2).

**W1 halt risk.**
- **OLD.** When S0 ×4 is in route A at W1, W1 waits 17.85 h at E and 53.4 h at U. At U that is a halt, in all four rows (high and stress32, both shapes). It is the N1 throttle: three generic-sized trees refuse every start.
- **NEW.** W1 starts at once in every row (median wait 0.0–0.15 h; with twin_first, 6.37 h, which is the twin's own window). In all 36 NEW rows the NOT_STARTED counts equal the no-S0 baseline. That baseline is 0, except the pre-existing v002 32-iteration engine rows: 14 (high) and 2 (stress32), the same under both rules (M04).

**Throttle that remains (MEASURED rule, reported).**
- With S0 ×4 in route A, the campaign runs one DDO route-A call at a time: a second one needs 97.59 GB, above 83 (G32c).
- The NGC after-route-A reservation is 10.0 GB, against the generic 3.5 GB. That accounts for most of the +2.4 to +9.7 h in the S0-H2 rows.
- The twin hold itself costs 0–4.8 h (H2/preW1, median) or 6.33 h (twin_first).

### Memory (max over seeds; GB as the gate counts them)

| | OLD | NEW |
|---|---|---|
| Peak, expected rows | 83.88 (twin beside W1's route A for 0.675 h) | 71.80 (= baseline) |
| Peak, high rows | 95.71 (twin_first; twin beside DDO route A for 4.22 h) | ≤ 92.86 (twin_first after the twin window; preW1 88.0 / 89.9); baseline 84.74 |
| Peak, stress32 rows | 99.27 | 92.86 (twin_first), 84.74 otherwise |
| Peak inside the twin window | up to 99.27 | ≤ 70.1 |
| Twin beside a DDO route-A call | up to 4.22 h | 0 h in every row (M06) |
| Time above 100 GB | 0 | 0 |

- NEW expected/stress32 rows meet v002's declared criteria (M07): peak < 110 GB; > 83 GB at most 0.041 % of the time; > 72 GB at most 0.40 %.
- **Consequence of the U classes.** The twin and a serial NGC call in route A cannot run together under the gate (61.3 + 22.4 = 83.7 > 83; G35d), so the identity pair runs one after the other. In H2 the NEW twin waits until S0 leaves route A and memory admits it: medians 37.4–38.5 h (E) and 87.1–105.9 h (U). twin_first starts it at HEADLINE's end and delays S0 and W1 by the twin's 6.33 h.

### Disk (N5; the parent's HALTED_DISK rule: free ≥ n_calls × per_call_bytes + 20 GiB before each wave)

External1 free space, MEASURED at 15:02Z, is **2,877.48 GiB** (`measured/DF_EXTERNAL1_20261019T150218Z.txt`). v002's basis read 3,273.2 GiB at 11:00Z; the difference is the dark-sector move (0705). With HEADLINE11, at the 80 GiB guard:
- **ENGINE_SHAPED wave 15 (24 calls; needs 1,940 GiB) halts even at the MEASURED 13.9 GB per call** (1,582.9 GiB free).
- With 20.2 GB per call and S0 ×4 outputs (51.5 GB each, ASSUMED), ENGINE_SHAPED wave 9 halts (1,839.1 GiB).
- LAUNCH_ORDER halts only at 20.2 GB per call with S0 (wave 20) or at 26.5 GB per call.
- At v002's 56 GiB, ENGINE_SHAPED wave 15 now halts at 20.2 GB per call (996.2 < 1,364).

So the disk does not cover 80 GiB × 24-call waves on today's free space. The guard rule and the space are R-D17/D3 matters for root. The cap value itself is A140's.

## 3. Root procedures (A140 N2, N3, N4)

1. **Direct batches.** Before each batch, run `<PY> -I -B v003/machine_gate_s45_c2v003.py --hold-check`. Start the batch only on exit 0.
2. **The twin.**
   - Start it only when `--twin-start-check` exits 0 (it samples for 60 s) **and** no direct batch has a call pending or in route A. The packet does not read the gate.
   - The campaign holds itself (`TWIN_HOLD`) for at most 22,752 s.
   - The NGC loop is not held, but its starts are refused on memory while the twin runs.
3. **S0 commands (N3).** The serial S0 calls use `--output-cap-bytes 146028888064`. The other caps are unchanged (`CAPS_S45_C2V003.json`).
4. **N4, after the step-2 receipts.** Copy `caps_s45_c2v003.py` to a new folder and change `DDO_TAIL_ON_WALL_CAP_S` (and its status text). Then run:

   `build_params_s45_c2v003.py --caps NEW/caps.py --caps-sha256 H --out-dir NEW --tag S45_C2V004`

   This regenerates the delta, the config successor, the orphan wait and the direct-batch caps. Y05c runs exactly this path on a synthetic constant. Only the wall leaves move, and the campaign and gate pins stay v003's.
5. **Adoption entry** (after a non-Claude2 lane reviews the delta):
   - pins: gate `736a3438`, campaign `011a2677`, NGC loop `bdb44eeb`, config successor `d9241676`, delta `aad1681a`, direct params `4adc296b`, caps module `6831829e`;
   - campaign entry line: `O.CAMPAIGN_MODULE_NAME = 'campaign_s45_c2v003'` (the v002 line is refused, K01b);
   - at H3: C2 + `SCHED_DELTA_S45_C2V003` via `apply_sched_delta_s45_c2v002` (`2a18b280`, unchanged).

Claude4's other NOTEs are not changed here (V1 race, V2 at H3, N6–N12). A139's direct-batch file `b7fdaf10` remains the predecessor of record. `…C2V003A` keeps its packet_read (guard011 / launcher012 / bind010), its max_active values, its case lists and its templates (D03, D04).

## 4. Files (sha256 prefix; full values in `HASHES_S45_C2V003.txt`)

| File | sha256 | What |
|---|---|---|
| `machine_gate_s45_c2v003.py` | `736a3438` | Gate (section 1). Diff: `DIFF_machine_gate_s45_c2v002__c2v003.diff` |
| `campaign_s45_c2v003.py` | `011a2677` | Gate pin and module name only. Diff vs v002 |
| `ngc_admission_s45_c2v003.py` | `bdb44eeb` | Gate pin, family NGC_SERIAL, class-equals-gate refusal, N3 constant. Diff vs v002 |
| `caps_s45_c2v003.py` | `6831829e` | Named caps: N4, N5, N3 |
| `build_params_s45_c2v003.py` | `fb87a1f3` | Builder (`--caps --out-dir --tag` for N4). Diff vs v002 |
| `SCHED_DELTA_S45_C2V003.json` | `aad1681a` | `set` (8 scheduling leaves) + `append.notes` + `caps_source` |
| `RUN_CONFIG_DDO154_CX2V006R9_S45_C2V003.json` | `d9241676` | R9 + the delta. Differs from the v002 successor only in the campaign pin, the output cap, the disk guard and notes (X13). Diffs vs R9 and vs v002 |
| `DELTA_REPORT_R9_TO_S45_C2V003.json` | `d0bcf73d` | Changed paths; unchanged top-level canonical shas |
| `DIRECT_BATCH_PARAMS_S45_C2V003A.json` | `4adc296b` | Successor of `b7fdaf10`: 31 tail-ON output caps of 80 GiB, the hold predicate, texts. Diffs vs `b7fdaf10` and vs v002 |
| `CAPS_S45_C2V003.json` | `35f66b6a` | Every cap with its basis; S0 and twin command caps |
| `PHYSICS_PINS_S45_C2V003.json` / `pin_compare_s45_c2v003.py` | `a801d11c` / `b0101b83` | 78 pins equal; scheduling keys only |
| `SIM_S45_C2V003.json` / `sim_s45_c2v003.py` | `82e8dd1e` / `aee03415` | Re-simulation (section 2); 105.9 s |
| `tests/test_sched_s45_c2v003.py` | `dd05a90e` | 176 rows |
| `test_runs/RUN_20261019T150426Z_99531/TEST_RESULTS.json` | `f7fe29fd` | Record run |
| `measured/DF_EXTERNAL1_20261019T150218Z.txt` | `da11cee7` | `df -k` of External1 and `/` |

## 5. Tests

**Result.** 176 / 176 pass: 104 MUST_PASS and 72 MUST_FAIL. There were 0 audit denials. The only subprocesses were ps, top, sysctl, vm_stat (one each, live rows) and the pinned python for 50 mock calls under the real root monitor. Wall time 92.5 s. The v002 rows are kept against the v003 objects.

**New rows, by item.**
- **N1:**
  - G30–G33c (classes, the v002 throttle shown at 84.59 and 100.79, sizing floors, undersized classes refused);
  - G38 (no cx3r008 tree = v002);
  - G39 (classifier);
  - P11–P13 (argv and spec parsing);
  - S07 / S07b (spec read once per tree).
- **N2, MUST_FAIL for twin overlap:**
  - G34 / G34b (TWIN_HOLD);
  - G34e (v002 admits beside the twin);
  - G35 / G35c / G35d (twin start refused with DDO route A in flight, with a second twin, beside a serial);
  - G36 / G37 (unidentified and overdue);
  - G40 (predicate);
  - S08 / S09 / S10 (hold_check, twin_start, CLI exit codes 3 / 0 / 2);
  - C09 (the campaign admits nothing while a synthetic twin is in route A, then completes);
  - N14 (the NGC loop is not held).
- **NGC class sizing, MUST_FAIL:** G33b, G33c, N13b (a loop class that differs from the gate's is refused).
- **N3:** Y06, Y06b, N12.
- **N4:** Y05 (one literal), Y05b, Y05c (end-to-end rebuild from one changed constant), Y05d (refused without the caps sha).
- **N5:**
  - X12;
  - Y01 (1.52 × the 32-iteration projection);
  - Y01c (MUST_FAIL, reported: at the C6T rate a 32-iteration call reaches 80 GiB near iteration 26.5).
- **Direct params:** D03–D06.
- **Sim:** M01–M09.
- **Pins:** Z01–Z04.
- **Live:** L01 / L02 read only the argv of 10 live monitor trees (0 cx3r008). They read no spec or progress file.

## 6. Still unmeasured, and build disclosures

**Still unmeasured.**
- The twin's steady footprint and busy cores (ASSUMED in the sim: 8 × 1.73 GB + the serial steady; 3.25 cores).
- The first NGC call's footprints and outputs.
- The step-2 receipts that N4 waits for.
- DDO output beyond 8 iterations.
- S0 output bytes (the disk rows ASSUME 51.5 GB).

**Build disclosures.**
- **Drafting.** Every v003 file was drafted and run in the session scratchpad first: a development copy with the same sources, 176/176. Each was then published here by exclusive create. No file in this folder was edited after creation.
- **Stdout files.** `BUILD_PARAMS_S45_C2V003.stdout.txt`, `PIN_COMPARE_S45_C2V003.stdout.txt`, `SIM_S45_C2V003.stdout.txt` and `TEST_STDOUT_S45_C2V003.txt` are the console output of the record runs.
- **Read for this build** (named paths only; no recursive search):
  - 0192, 0706, 0705, 0704, 0700;
  - A133 (sha `cd92ef91`; wave and NGC sections);
  - RI45-12 estimate V002, and §7 lines of V001;
  - step5_path README, CAPS and POLICY;
  - the parent orchestrator's disk-guard lines;
  - guard c2v011 lines 1–40, 295–312, 329 and 347, and the packet successor diffs;
  - the v002 folder.
