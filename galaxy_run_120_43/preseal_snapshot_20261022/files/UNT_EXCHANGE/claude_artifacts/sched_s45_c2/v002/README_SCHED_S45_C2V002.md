# sched_s45_c2 v002: fixes for the verifier blockers on the step-4 and step-5 scheduling

Claude2, 2026-10-19 (built 11:00–11:45Z). Principal's orders: "Fix the step 4 scheduling rule now" and "we also need to fix Step 5".

**Scope.** Only scheduling, admission and per-call caps change. Every physics input is byte-identical to its predecessor (section 7). Nothing was launched. No result, array, node-diagnostic, C5H, UVT_* or NGC target file was opened.

v002 sits in `sched_s45_c2/v002/`. Every v001 file is unchanged (test Z01).

**Labels.**
- MEASURED: read from bytes or live processes today.
- DERIVED: arithmetic on MEASURED or FORMAL inputs.
- ASSUMED: a stated choice.

Projections are model outputs (UNTESTED as forecasts). The simulation is seeded and replays deterministically.

## 1. What v002 fixes

| Blocker | v001 | v002 |
|---|---|---|
| V2-B1: route-A cap 4 / 100 GB not memory-safe | Phase-locked sim; one spike counted; 100 GB limit above the measured stress point | Random-phase sim (`sim_s45_c2v002.py`). The v001 rule replayed there peaks at 130–168 GB (M03). New memory rule in `machine_gate_s45_c2v002` (section 3), selected by criteria declared before the runs. |
| V1-B1: first NGC call wall 72 h | Below Claude4's corrected U point, 84.77 h | Wave-1 wall 576,000 s (160 h) = 1.5 × 1.25 × 305,162 s, rounded up (N05d). The v001 cap kills all 12 U-regime calls in the sim (M05). |
| V1-B2: NGC reservation falls to 5 GB | `max(5, …)` on missed transients or an unseen tree | Class = reservation 6.0 GB + spike 16.4 GB (Claude4 U). Both are floors in `compute_caps` and on the receipt path (N05b, N11). |
| V1-B2: monitor not matching the pattern | Not checked | Plan refused (N01d). |
| V1-B3: delta overwrites C2 notes | `set.notes` = R9 notes + suffix | Notes are append-only (`apply_sched_delta_s45_c2v002`). A synthetic C2 note survives (X08); setting notes is refused (X09); the v001 defect is reproduced (X10). |

**Verifier notes also addressed.**
- NGC loop:
  - Mis-ordered `requires_groups_complete` plans are refused (N01c).
  - Pooled NGC specs (`route_a.column_workers` ≠ 1) are refused (N01e).
  - A loop wall cap was added (N10).
  - `res_after` is now 10.0 GB, labelled DERIVED from Claude4.
  - The first call's output is measured once per iteration, and the disk walk runs only when everything else admits.
- Gate: a young foreign tree without a worker pool is counted as pooled (G22).
- Basis: the after-route-A reservation was re-measured to 3.5 GB (G25). Y01 now uses D5's MEASURED route-B bytes (2.2 GiB).

## 2. Old vs new rules

| | Old (as proposed) | v001 | **v002** |
|---|---|---|---|
| Step-4 campaign admission | c2v005: process budget 17, route A = 8, `max_concurrent` 6 (R9 ships 1) | gate v001: cap 4, ≤ 100 GB, one 20 GB spike | **gate v002**: route-A cap 2; d1 ≤ 83 GB with 2 spikes + growth; d2 ≤ 72 GB with 1 spike; both limits lowered live by the vm_stat pool; `max_concurrent` 12 |
| Direct batches (packet, no live memory gate) | `max_active` 3 | HEADLINE / SENS 3, DIII 4, POST_S1 2 | **HEADLINE 1, SENS_LO 1, SENS_HI 1, DIII 4, POST_S1 2** |
| Step 5 (NGC) | First point solo to completion, then 1–2 at a time | Solo 2 iterations, then gate v001 with an 11 GB reservation | **Solo 2 iterations, then gate v002 with class 6.0 + 16.4 GB** (floors); spacing 600 s; ≤ 16 running; disk guard; loop cap 30 days |

On HEADLINE and SENS at 3: they reach 130.5 GB in the all-32-iteration row; at 2 they spend 0.17–0.63 % of the time above 83 GB. Section 8 item 4 restores the speed.

## 3. The v002 memory rule (`machine_gate_s45_c2v002`, `6e8f2159…`)

- **counted** = Σ over run trees of max(live top-MEM footprint, phase reservation).
  - Route-A reservation: 11 GB (MEASURED).
  - After-route-A reservation: 3.5 GB. MEASURED K128 post-loop max is 3.5 GB; after-route-A max is 2.7 GB, including D5's stages 03–07.
- **d1 MEMORY_HARD:** counted + head reservation + the 2 largest spikes among route-A calls and the head + the growth of pooled route-A calls ≤ hard_eff.
  - Spikes: DDO pooled 20 GB (MEASURED +16.8 to +20.6 GB); NGC 16.4 GB.
  - Growth: 0.2228 GB/iteration (DERIVED) × (32 − 6) = 5.79 GB per pooled call.
- **d2 MEMORY_KNEE:** counted + head reservation + the largest single spike ≤ knee_eff.
- **Limits.**
  - knee = 72 GB, MEASURED: 72.0 GB of run footprint ran with the compressor flat (08:42:39Z); compression began at 76.7 GB (08:18:41Z).
  - hard = 83 GB, MEASURED: 83.2 GB ran with swap flat (08:19:19Z).
  - Live: pool = Σ run footprints + vm_stat free + file-backed. knee_eff = min(72, pool − 2); hard_eff = min(83, knee_eff + 11). The pool MEASURED 81.7 GB at 11:05Z and 79.9 GB at 11:36Z, so the static limits bind now.
  - vm_stat unreadable → PROBE_FAILED (P10).
- **What this allows.**
  - DDO: 1 route-A call + up to 11 after route A, or 2 route-A calls + 2 after (G18b).
  - NGC: up to 8 in route A when alone (G23).
  - `memory_pressure` is never read (G17).
- **Selection.** Criteria were declared before the runs and must hold in every seed of the expected and all-32-iteration rows, both wave shapes:
  - time above 83 GB ≤ 0.1 %;
  - peak < 110 GB;
  - time above 72 GB ≤ 2 %.

  | Variant | Result |
  |---|---|
  | cap 2/3 without the growth reserve | Fails (stress32: 0.34–0.76 % above 83 GB; cap 3 peaks at 113.7 GB) |
  | cap 2/3 with growth | Passes; identical results, because cap 3 never binds |
  | **Chosen: cap 2, 2 spikes, growth on** | Expected rows peak 71.8 GB; stress32 rows peak 84.7 GB, above 83 GB 0.02–0.05 % of the time (M04) |

## 4. Caps

| Class | wall | RSS | output | Basis |
|---|---|---|---|---|
| DDO K128 tail-ON (campaign, HEADLINE, SENS, POST_S1) | 100,800 s (28 h) | 64 GiB | 56 GiB | Unchanged from v001. Verifier 2 checked the margins. Y01: 32 × 1.575 + 2.2 (D5 route B, MEASURED) = 52.6 GiB ≤ 56. |
| DIII tail-OFF | 46,800 s (13 h) | 16 GiB | 96 GiB | Unchanged |
| **NGC K32, wave 1** | **576,000 s (160 h)** | 32 GiB | 136 GiB | 1.5 × 1.25 × the Claude4 U point; Claude4 A61 RSS; output DERIVED (UNMEASURED node logs) |
| NGC class (gate) | — | — | — | Reservation 6.0 GB, spike 16.4 GB, after route A 10.0 GB; floors |

Caps that would have killed calls, now replaced:

| Old cap | Why it kills calls | Test |
|---|---|---|
| R9 output cap 12 GiB | Below a full tail-ON call | Y01b |
| R9 wall cap 8 h | Below the slowest call | Y03b |
| RI45-12's 12 h / 5 GiB | Kills 12 of 12 NGC calls | sim `proposed_caps` |
| v001 NGC wall 72 h | Kills 12 of 12 NGC calls at U | M05, N05e |

## 5. Simulated durations (compute only; median of seeds; NGC point E for the low and expected rows, U for high)

| T0 → step 5 done (HEADLINE11 + 120-call campaign + step 5, 6 NGC + 6 sensitivity) | low | expected | high |
|---|---|---|---|
| Old, as shipped (R9 `max_concurrent` 1; NGC 1 at a time) | 949.4 | 1091.9 | 2450.7 |
| Old, as proposed (`max_concurrent` 6; NGC 2 at a time) | 418.7 / 392.7 | 468.7 / 452.3 | 1269.0 / 1279.4 |
| **v002** (launch-order / engine-shaped waves) | **202.4 / 191.7** | **252.8 / 241.1** | **736.8 / 714.2** |
| v002 + packet successors on the gate (not built) | 198.8 / 188.1 | 245.5 / 233.8 | 715.3 / 692.7 |

**Hours saved, expected.**
- v002 vs old-as-proposed: 215.9 h (launch-order) / 211.2 h (engine-shaped).
- v002 vs as shipped: 839.1 / 850.8 h.

| Part (expected) | Old shipped | Old proposed | v002 |
|---|---|---|---|
| Campaign, 120 calls (launch-order / engine-shaped) | 699.0 | 235.3 / 219.0 | **163.9 / 152.2** (low 120.7 / 109.9; high 496.5 / 473.9) |
| Step 5 (E / U) | 383.0 / 1016.8 | 223.5 / 593.2 | **70.5 / 178.4** (with the probe 66.0 / 175.1) |
| HEADLINE11 (packet) | 9.9 (`max_active` 3) | 9.9 | 18.5 at `max_active` 1 (11.1 on the gate) |

- **v001's figures were optimistic.** v001 printed 171–183 h end to end. That came from the phase-locked sim (memory-unsafe rule) and root's older 17.6 h NGC point. Claude4's corrected E point is 31.90 h.
- **The v001 rule replayed with random phases** gives expected campaigns of 138.7 / 126.7 h, but peaks of 129.6 / 143.6 GB.
- **The 48 h wave cap.**
  - It holds in the low and expected rows: no late starts; latest start 14.9 h into a wave.
  - In the all-32-iteration engine-shaped rows it leaves 2 (stress32) to 14 (high) calls NOT_STARTED (latest start 49.2 / 67.6 h).
  - Old-as-proposed leaves 12 / 26 in the same rows.
  - `campaign_wall_cap_s` stays 172,800 s; it is a root ruling if 32-iteration calls appear.
- **Cross-check.** The sim reproduces LAUNCH_ORDER's 209.75 h and 356.49 h (M01).

## 6. Files (sha256 prefixes; full values in `HASHES_S45_C2V002.txt`)

| File | sha256 | What |
|---|---|---|
| `machine_gate_s45_c2v002.py` | `6e8f2159` | Shared gate (section 3). Diff: `DIFF_machine_gate_s45_c2v001__c2v002.diff` |
| `campaign_s45_c2v002.py` | `59e0f4fd` | c2v005 + gate admission; vs v001 only the gate pin, name and never-admissible call change. Diffs vs c2v005 and v001 |
| `ngc_admission_s45_c2v002.py` | `3166488c` | Step-5 loop (section 2). Diff vs v001 |
| `RUN_CONFIG_DDO154_CX2V006R9_S45_C2V002.json` | `05a2f987` | R9 + delta: the same 8 leaves as v001. The campaign pin is v002; notes are appended. Diffs vs R9 and vs v001 successor |
| `SCHED_DELTA_S45_C2V002.json` | `066683b6` | `set` (scheduling paths) + `append.notes` |
| `apply_sched_delta_s45_c2v002.py` | `2a18b280` | Append-only notes |
| `DIRECT_BATCH_PARAMS_S45_C2V002.json` | `5ada605b` | `max_active` and caps for C1 |
| `SIM_S45_C2V002.json` / `sim_s45_c2v002.py` | `b2978fc3` / `cec61f90` | Random-phase sim |
| `PHYSICS_PINS_S45_C2V002.json` | `f64577ca` | 78 pins equal to bytes; numerics `4b2a5a87…` equal to R9 |
| `measured/MEASURED_BASIS_REFRESH_20261019T110027Z.json` | `ca6a86f8` | v001 extractor re-run on the watch snapshot to 10:59Z |
| `tests/test_sched_s45_c2v002.py` | `7b6366d2` | 122 rows |
| `test_runs/RUN_20261019T113406Z_58084/TEST_RESULTS.json` | `d3612a8a` | Final run |
| `build_params_s45_c2v002.py`, `pin_compare_s45_c2v002.py` | `1216ced0`, `0c4780e2` | Builders |

## 7. Tests and physics

**Tests.** 122 / 122 pass (74 MUST_PASS, 48 MUST_FAIL). 0 audit denials. Subprocesses: only ps, top, sysctl, vm_stat and the pinned python running the mock. Run time 151 s.

**Physics.** 78 pins equal their bytes; the numerics canonical sha256 equals R9's. The changed top-level keys are campaign, max_concurrent, per_call, disk_guard, orphan_wait and notes. The cache id is unchanged (the parent formula reads none of them).

**Parent orchestrator** (K01, K01b, K02):
- it refuses `campaign_s45_c2v002` without the entry line;
- it also refuses it under the v001 entry line;
- it accepts it with `O.CAMPAIGN_MODULE_NAME = 'campaign_s45_c2v002'`.

## 8. For root (adoption)

1. **Review.** Have a Claude lane other than Claude2 review the v002 delta (the diffs in section 6), then write the admission entry pinning:
   - the gate `6e8f2159`;
   - the campaign `59e0f4fd`;
   - the successor config `05a2f987` (at H3: C2 + `SCHED_DELTA_S45_C2V002` via `apply_sched_delta_s45_c2v002`);
   - NGC `3166488c`;
   - direct params `5ada605b`.
2. **Campaign entry line.** The S4-R-B4b entry must set `O.CAMPAIGN_MODULE_NAME = 'campaign_s45_c2v002'` before `Context(config)`. The v001 line no longer works. The H3 C4-6 derivation must carry `per_call` and `disk_guard.per_call_bytes` as in the successor.
3. **Step 5.**
   - Put the NGC `work_dir` on External1. MEASURED: `/` has 281.5 GiB free, and the disk guard needs 292 GiB for 2 NGC calls.
   - Confirm on the seed that `hi_panels_per_side` is 8 and `source_azimuth_count` is 32 (Claude4 N4). The 32 GiB RSS cap and the 16.4 GB spike rest on them.
4. **Direct batches.**
   - C1 copies `DIRECT_BATCH_PARAMS_S45_C2V002` (HEADLINE/SENS `max_active` 1).
   - A direct batch must not start while the campaign or the NGC loop has calls running.
   - Recover the speed with guard/launcher/binder successors on `machine_gate_s45_c2v002` (Codex1 builds, Claude3 reviews): HEADLINE11 18.5 → 11.1 h expected.
5. **Disk.**
   - At MEASURED K128 output (13.9–20.2 GB per call) the campaign does not halt on the 56 GiB guard.
   - At 26.5 GB per call (C6T-class) the second 24-call engine wave halts (1076.7 < 1364 GiB).
   - NGC outputs (DERIVED ~90 GiB each) do not fit beside the campaign, so the R-D17 / D3 ruling is still needed.

**Still unmeasured.**
- Full tail-ON route-B footprint and bytes (D5 is still in route B).
- Memory and output growth beyond 8 iterations (DERIVED vf).
- The NGC first call (iteration events under cx3r008; node-log and readout bytes).
- Run footprint between 83 and 137 GB.
- Pool behaviour when other lanes grow.

## 9. Build disclosures

- **Drafting.** Every v002 file was drafted in the session scratchpad and published here by exclusive create. No file in this folder was edited after creation.
- **Duplicate file.** `SIM_S45_C2V002.stdout.txt.tmp` is a byte-identical duplicate of `SIM_S45_C2V002.stdout.txt`, left behind by a shell redirect. It was kept, not deleted.
- **Development test runs.** `test_runs/RUN_20261019T113108Z_42844` (117/120: two inverted MUST_FAIL assertions, and the NGC disk guard binding on `/` with 281 GiB free) and `RUN_…113322Z_55900` (N and M blocks only) are development runs. The test file was fixed before it was published; only `RUN_…113406Z_58084` is the final run.
- **Measurement.** It was read-only: a watch-CSV snapshot, the v001 extractor (stage/event/iteration/elapsed fields and `du` sizes only), and vm_stat/top/ps.
