# sched_s45_c2 v001: step-4 and step-5 scheduling set from measured resources

Claude2 build for root, 2026-10-19 (built 09:39–10:40Z). Principal's orders: "Fix the step 4 scheduling rule now" and "we also need to fix Step 5".

**Scope.** Only scheduling, admission and per-call caps change. Every physics input is byte-identical to its predecessor: the driver, specs, numerics and thresholds (section 7).

**What was run.**
- Synthetic tests: mock driver under the real pinned root monitor.
- The schedule simulation.
- Read-only measurements of the live step-2 runs.

Nothing was launched. No result, array, node-diagnostic, C5H, UVT_* or NGC target file was opened.

**Labels.**
- MEASURED: read today from bytes or live processes.
- DERIVED: arithmetic on MEASURED or FORMAL inputs.
- ASSUMED: stated choice.

All projections are model outputs (UNTESTED as forecasts). Their arithmetic is deterministic and replayed: `SIM_S45_C2V001_R3.json` was re-run and was identical apart from `utc`.

## 1. Bottom line (compute only; expected [low–high])

Root work, certificate production and per-call acceptance are not modelled.

| Path (6 NGC members + 6 sensitivity calls) | Launch-order waves [1]+19×[6]+[5] | Engine-shaped waves (ASSUMED) |
|---|---|---|
| Old, as shipped: R9 `max_concurrent 1`; step 5 first call solo to completion, then 1 at a time | 904.6 h [703.0–2108.8] | 904.6 h [703.0–2108.8] |
| Old, as proposed: `max_concurrent 6`, budget 17; step 5 then 2 at a time | 364.1 h [275.7–1065.0] | 341.7 h [249.3–1076.9] |
| **New** (this build) | **183.0 h [137.5–480.6]** | **171.3 h [130.1–442.4]** |
| New, with the target-free NGC probe run during the campaign | 181.5 h [136.4–479.0] | 169.8 h [129.0–440.9] |

These are the HEADLINE11 + campaign + step-5 times from T0 (`end_to_end_M6_S6`).

**Caps that would have killed calls, now replaced.** Each row is MUST_FAIL-tested (Y01b, Y03b; section 6):

| Old cap | Why it kills calls | Basis |
|---|---|---|
| R9 / V005A per-call output 12 GiB | below a full tail-ON call | MEASURED 13.9–26.5 GB |
| R9 per-call wall 8 h | below the slowest K128 call | DERIVED worst 11.7 h solo |
| R-D8's proposed 29 GiB RSS for direct tail-ON calls | below the transfer peak | MEASURED ps-RSS peak 29.7–32.6 GB |
| RI45-12's proposed NGC caps (12 h, 5 GiB) | **every NGC call is killed** (sim `proposed_caps`: 12 of 12) | — |

## 2. What changed, file by file (exact diffs)

| Successor (this folder) | Predecessor | Change | Diff |
|---|---|---|---|
| `campaign_s45_c2v001.py` `1d8a7189…` | `campaign_c2v005.py` `d35d5d4a…` | Admission only. The c2v005 budget test (`cur + peak > budget`, L203) is replaced by `gate.decide(...)`. Also changed: `MODULE_NAME`; the pinned gate loader; a refusal for a call the gate could never admit; a sleep when the gate holds the head with nothing running; summary keys `gate` and `gate_log`. Unchanged: validation, call dirs, monitor command, caps, resume, records and every c2v005 summary key. | `DIFF_campaign_c2v005__campaign_s45_c2v001.diff` |
| `machine_gate_s45_c2v001.py` `6d0c45f8…` | c2v005's rule: `spec_weights` + budget 17, i.e. route A = 8 processes, so at most 2 calls in route A | New shared gate (section 3). Pinned by sha256 inside the campaign and NGC modules. | new file |
| `RUN_CONFIG_DDO154_CX2V006R9_S45_C2V001.json` `5d441ff1…` | R9 `721c7230…` | 8 leaves change: `campaign` pin; `max_concurrent` 1 → 12; `per_call.wall_cap_s` 28800 → 100800; `per_call.output_cap_bytes` 12 GiB → 56 GiB; `disk_guard.per_call_bytes` 12 GiB → 56 GiB; `orphan_wait.cap_s` 29400 → 101400; `notes` (appended). | `DIFF_RUN_CONFIG_R9__S45_C2V001.diff`, `DELTA_REPORT_R9_TO_S45_C2V001.json` |
| `SCHED_DELTA_S45_C2V001.json` `c1f1f085…` | — | The same changes as a delta. At H3 root applies it to C2, R9's H3 successor: `apply_sched_delta_s45_c2v001.py C2.json SCHED_DELTA_S45_C2V001.json C2_S45.json REPORT.json`. The tool refuses any non-scheduling path (X04) and recomputes the campaign sha from bytes (X05). | — |
| `DIRECT_BATCH_PARAMS_S45_C2V001.json` `307a64aa…` | `templates_v004` (caps null; `max_active` 3) | Parameters only, for C1's `cfg.route_a_admission` and `cfg.caps`. `max_active`: HEADLINE 3, SENS_LO 3, SENS_HI 3, DIII 3 → 4, POST_S1 2. Per-case caps (section 4). Guard v010, launcher v011 and binder v009 are unchanged; their conditions L329 and L347 accept these values (D01). | `DIFF_DIRECT_BATCH_PARAMS_vs_templates_v004.txt` |
| `ngc_admission_s45_c2v001.py` `a08cb3bb…` | RI45-12 as proposed (prose): first point solo to completion, then 1–2 at a time; 12 h / 5 GiB caps | New step-5 admission loop (section 5). Inert until root writes a launch plan under a V006 entry. | new file |

**One line in the S4-R-B4b campaign entry** (still to be built; it is not built here). On the parent module object the core loaded (`calibration_core_cx2v006r9` → `O`), before `Context(config)`:

```python
O.CAMPAIGN_MODULE_NAME = 'campaign_s45_c2v001'   # record it in the launch record; PROCESS_BUDGET_MAX stays 17
```

Tests against the parent's own lines L1753–1757, executed from its bytes:
- K01: without this line the parent refuses (MUST_FAIL).
- K02: with it, the parent accepts.
- K03: the parent's `CampaignExecutor.campaign_dict` runs under the new module.

**Cache id: unchanged.** Neither the parent formula (L1774–1780) nor the r9 wrapper (L52–53) hashes any changed key.

**Root's H3 C4-6 step must carry the new caps.** The adoption derivation must carry `per_call` and `disk_guard.per_call_bytes` exactly as in the successor, because L1912–1924 compare them. At the same step, root sets `measured_per_call_bytes` from the largest measured tail-ON receipt (left at R9's value here).

## 3. The rule (machine_gate_s45_c2v001)

The head of the FIFO queue starts only when all of the following hold:

| # | Check | Value | Basis |
|---|---|---|---|
| a | count | < `max_concurrent` (12) | DERIVED: core limit 24 / after-route-A weight 2 |
| b | pooled (8-worker) calls in route A, machine-wide, head included | ≤ **4** | DERIVED from memory (below) |
| c | busy-core weights + the head's | ≤ 24 | Route A 3.25 (MEASURED iterating mean; re-measured 2.77 on C3T). After route A: `column_workers` 2, an upper bound (MEASURED 0.8–1.0). Foreign runs: max(phase default, measured cores over 60 s). |
| d | Σ max(live footprint, phase reservation) + head's 11 GB + 20 GB spike headroom | ≤ 100 GB | See the memory table below. Live footprint is top MEM per driver process group, the A130 metric. |
| e | swap used | ≤ 8 GB | the A130 watch alert level |
| f | since the youngest root monitor on the machine, and since this launcher's own last start | ≥ 120 s | applies to any launcher |
| g | CPU-sample history | ≥ 60 s | — |
| h | ps and swap readable | — | fail closed |

**Memory inputs for check d.**

| Phase | Reservation | Basis |
|---|---|---|
| Route A | 11 GB | MEASURED K128 steady footprint: median 9.7–9.9, max 10.1–11.8 GB outside transfer windows |
| After route A | 4.4 GB | DERIVED: model 4.095 GiB. MEASURED reference stage 0.6–1.6 GB. |
| Spike headroom (one transfer) | 20 GB | MEASURED +16.8 to +19.9 GB above steady, lasting 37–41 s |

**Post-loop.** A tree whose 8-worker pool has exited while its driver has not yet logged `route_a finished` is in the route-A post-loop. MEASURED: 18–40 min per call at 0.8–1.0 core and ≤ 3.8 GB. The gate weighs and reserves it as after route A, which frees its route-A slot. Weights never rise during a call.

**What it never reads.** `memory_pressure` is never read (G17). MEASURED: it reported 85–86 % free at 83 GB of run footprint.

**Why the route-A cap is 4, not 6** (`SIM_S45_C2V001_R3.json` VARIANT rows, expected / 32-iteration):

| Cap | Simulated peak total footprint | Expected campaign time |
|---|---|---|
| 6 | 127 / 141 GB | 123.5 h (launch-order waves) |
| 4 | 85–104 / 88–118 GB | 134.8 h (launch-order waves); 123.1 h vs 122.6 h (engine-shaped) |

- With cap 6, the 32-iteration peak of 141 GB is above the 137.4 GB of physical memory.
- The memory basis for the threshold is MEASURED: the compressor grew from 13.4 to 60.1 GB when the run footprint reached 77–83 GB (swap stayed flat at 1.8 GB).

**Measured artefacts** (in `measured/`; the extract and samplers read only stage/event/iteration/elapsed fields, footprints, CPU times and sizes):

| Measurement | Values |
|---|---|
| Timing | Setup 541–959 s for the K128 class (1293 s for KHI). Cycle 107–320 s for K128 (C6T 319–450 s). 6–8 iterations. Post-loop 575–2375 s. Manifest 47–1580 s. |
| Output | Route A averages 1.50–1.58 GiB per iteration (C4T, S4T, C4T_A, C4T_D5). Marginal growth 0.26–0.91 GiB per iteration (du time series). External1 has 3273.2 GiB free. |
| Footprint | Watch CSV snapshot, 159 rows to 09:39Z, plus the live samplers at 15 s and 2.8 s. |
| Cores | `LIVE_MEASURE_20261019T100441Z.json` |

## 4. Caps

| Class | wall_cap_s | rss_cap_bytes | output_cap_bytes |
|---|---|---|---|
| DDO K128 tail-ON (campaign, HEADLINE, SENS, POST_S1) | 100800 (28 h) | 64 GiB (R9's value, unchanged) | 56 GiB |
| DIII tail-OFF | 46800 (13 h) | 16 GiB (R-D5) | 96 GiB (R-D5) |
| NGC K32, wave 1 | 259200 (72 h) | 32 GiB | 136 GiB |

**Basis for each cap.**
- **Tail-ON wall.** ≥ 1.5 × 1.25 × the 11.7 h worst solo call = 21.9 h (Y03). The worst call is 32 iterations of the MEASURED longest cycle, plus the MEASURED longest setup and post-loop, plus TIMING_V003's U route B.
- **Tail-ON RSS.** 2.1 × the MEASURED ps-RSS transfer peak (32.6 GB), and 3.4 × the 18.79 GiB model (A61).
- **Tail-ON output.** ≥ 32 iterations × 1.575 GiB + 1 GiB = 51.4 GiB (Y01). That is 2.3 × the largest measured call (26.5 GB).
- **DIII wall.** ≥ 1.5 × 1.25 × 6.61 h DERIVED, and 2.75 × the MEASURED 4.72 h C5H call. R-D5's 12 h is 0.4 h short of that.
- **NGC wall.** 1.28 × root's DERIVED upper bound of 56.3 h.
- **NGC RSS.** ≥ 1.5 × the DERIVED serial peak of 15–20 GB: the u4 map's state-16 transient, with q = 17 ASSUMED.
- **NGC output.** 1.5 × a DERIVED 89.7 GiB: 16 iterations × the MEASURED DDO per-iteration outputs, scaled by NGC columns (× 8.67: node diagnostics) and waves (× 1.30: arrays and checkpoints). The 32 GiB in the old NGC plan and the 64 GiB in the design would have killed the first NGC call near iteration 6 or 11 (DERIVED).
- **Later NGC calls.** Caps are computed from the first call's 2nd completed iteration, and are never below wave 1 (N03, N05):
  - RSS = 1.5 × (rss₁ + 14·slope)
  - output = 1.5 × (out₂ + 14·Δout + 10 GB)
  - wall = 1.5 × 1.25 × (prep + 16·t_iter) / 0.7

## 5. Step 5 (ngc_admission_s45_c2v001)

- **Order.** Root's plan order: NGC headline members, then ORIGINAL_K, then sensitivity. S4-POST-S1 goes first through the packet (POST_S1, `max_active` 2) together with the per-point certificates.
- **Dependencies.** `requires_groups_complete` (for example, the sensitivity calls wait until every headline member has finished: D1). If a required call fails, the dependent calls are left NOT_STARTED for root (N06).
- **First call.** It runs solo until it has completed 2 route-A iterations; then caps and the reservation are computed. A plan carrying a probe's `measured_basis` skips the solo phase (N07).
- **Admission.** Every start passes the shared gate:
  - weight 1.0 core in route A (MEASURED serial analog 0.8–1.0) and 2.0 after;
  - reservation = iteration-0 peak + half the projected state-build transient: 11 GB DERIVED until measured, then 10.4 GB on the u4 model;
  - 600 s spacing, at most 16 running.
- **Disk guard.** Before each start: free ≥ Σ remaining output caps + the head's cap + 20 GiB (N07).

**Simulated step-5 times** (FINAL_SUMMARY → last NGC call, M6 S6; expected [low–high]):

| Rule | Time |
|---|---|
| RI45-12 caps as proposed | all 12 NGC calls killed (5 GiB RSS at the first state build) |
| Solo, then 1 at a time | 211.2 h [140.4–675.6] |
| Solo, then 2 at a time | 123.3 h [82.0–394.2] |
| **New** | **38.7 h [26.4–119.5]** |
| New + probe | 37.1 h [25.3–117.8] |

- With ORIGINAL_K (6 more calls): 316.8 / 176.0 / **50.2** / 48.6 h.
- M = 4 to 10 and S = 2 or 6: see `step5` in the sim.

**The probe.** It is RI45-12 (i) run as a measurement: one target-free NGC K32 call during the campaign, on idle cores.
- Effect on the campaign: at most +0.04 h (sim).
- What it does: sets wave-1 caps from measurement and removes the solo phase.
- It needs a V006 ruling and a registered target-free spec at a non-admitted point. Only its receipt, footprint and timing are read.

## 6. Tests: 85 / 85 pass (55 MUST_PASS, 30 MUST_FAIL)

Run: `test_runs/RUN_20261019T102317Z_73997/TEST_RESULTS.json` `df66acd8…`. Audit hook: 0 denials; subprocesses were only ps, top, sysctl and the pinned python.

| Group | Rows | What it checks |
|---|---|---|
| G | 24 | Every gate check, both accept and refuse, at its boundary. Includes: live footprint over reservation; post-loop slot release; foreign measured cores; fail-closed probe and swap; no `memory_pressure`. |
| P | 8 | Parsers. P06 fixes a probe bug found while measuring: a monitor's own `ps` child with a recycled lower pid was taken for the driver. |
| S | 6 | Stateful sampling, rate limit, 60 s core measurement, post-loop detection, spacing from foreign monitors. |
| C | 10 | Through the real monitor and the mock driver: refusals byte-identical to c2v005 (9 cases); end to end FIFO with the route-A cap binding; c2v005 summary keys kept; old rule slower on the same calls (19.2 s vs 12.4 s); wave wall cap gives NOT_STARTED; resume; no-deadlock refusal; gate pin; spacing. |
| K | 6 | The parent c2v005 from its own bytes: L1753–1757 refuse without the entry patch and accept with it; `campaign_dict` runs; L1724–1751 accept the successor config and refuse `disk_guard` < output cap. |
| X, Y | 13 | The delta reproduces the successor bytes from R9; only scheduling paths change; physics keys are byte-identical; the tool refuses numerics and a wrong campaign sha; every file pin matches its bytes; caps ≥ measured × margin; R9's caps fail the same tests. |
| D | 4 | Guard v010 L329 and L347 conditions, evaluated from its bytes, accept the parameters and refuse 7 and a float wall. `max_active` equals the sim's memory choice, and one more breaks it. |
| N | 10 | NGC loop: refusals, solo-then-computed caps, D1 ordering, failure propagation, disk guard, probe basis, spacing, gate pin. |
| Z | 2 | Physics and predecessor files unchanged from bytes. |
| L | 2 | Live read-only probe. A hypothetical campaign head now would wait on MEMORY_LIMIT (101.4 > 100 GB) under the running step-2 load. |

## 7. No physics input changed

`PHYSICS_PINS_S45_C2V001.json` checks 78 pins against their bytes; all are equal.
- **Successor config pins:** driver r5 `b5cc62af`, monitor, coordinate spec and addendum, taxonomy, observation region, registered anchor, custody deriver, state enumerator, python.
- **Templates:** the 33 template specs and their drivers in templates_v004.
- **Other pins:** the NGC driver cx3r008 `577f8c94` and R9 itself.

Numerics: canonical sha256 `4b2a5a87…` for both R9 and the successor. The changed top-level keys are exactly campaign, max_concurrent, per_call, disk_guard, orphan_wait and notes. No driver, spec, numerics or threshold file was written. Z01 shows the predecessors are unchanged:
- campaign_c2v005, orchestrator c2v005 `c75a889f`, wrapper and core r9;
- templates_v004, V005A config, the r5 and cx3r008 drivers, the root monitor.

## 8. For root

1. **Pin and rule.**
   - Pin the successor config: `5d441ff1` now; at H3, C2 + `SCHED_DELTA`.
   - Rule the campaign entry line in V006 (section 2).
   - Copy `DIRECT_BATCH_PARAMS` into C1. This supersedes R-D8's 29 GiB RSS proposal and R-D5's 12 h wall.
   - For step 5, adopt `ngc_admission` and the wave-1 caps; RI45-12's proposed caps kill every call.
2. **Disk binds before cores.** External1 has 3273 GiB free (MEASURED) and nothing is deleted.
   - At 26.5 GB per call, the second 24-call engine wave halts (HALTED_DISK): free 1077 GiB, needs 1364 GiB.
   - NGC outputs (DERIVED ~90 GiB each, 1.1–1.6 TiB for 12–18 calls) do not fit beside the campaign's 2.4–3.2 TB.
   - Root's R-D17 / D3 relocation or retention ruling is needed before campaign round 2 and before step 5.
3. **Under cx3r008, NGC route A is not run by the driver** (u4 map §1.5; Claude4). If root's interface-A call does not log iteration events in its outdir, the loop holds the first call solo until it ends, then sets caps from its receipt. That is slower but safe.
4. **Direct-batch speed needs the planned packet successors:** guard v011, launcher v012, binder v010 on the shared gate, with Codex1 building and Claude3 reviewing the delta.
   - Gain: HEADLINE11 9.54 → 7.98 h expected, SENS9 8.69 → 7.19 h.
   - They are also what lets DIII4 and SENS run beside step 5.
   - Not built here (packet code; smallest change first).
5. **Re-measure when route B exists.** When C4T R2's route-B stages run, measure their footprint. If it stays ≤ 2 GB, set `res_after_gb` to 1.25 × that measurement (gate v002). This adds route-B concurrency, and removes nothing.

## 9. Build disclosures

- **Edited during the build.** Files in this folder were edited in place before HASHES.txt; nothing was pinned before it.
- **Superseded runs, kept:**
  - `SIM_S45_C2V001.json`: gate `4f24d937`, route-A cap 6.
  - `SIM_S45_C2V001_R2.json`: final gate, older direct-batch section.
  - Both come from earlier states of `sim_s45_c2v001.py`, which are not kept. Only R3 replays.
  - `work/`: provisional runs.
  - `test_runs/RUN_20261019T101022Z_8767` and `…101258Z_22873`: development runs.
- **Probe bug.** `measured/LIVE_MEASURE_20261019T094945Z.json` was taken before the P06 probe fix. Its CPU column has artefact zeros (not used). Its footprint column is valid; the sim uses it for the 30.5 GB peak. The spike sampler kept only samples with ≥ 4 processes, which excludes those artefacts.
- **Unpinned measurement loaders.** `measure_live` and `sample_spikes` load the gate by path, not by sha; the files they wrote record their own inputs.

## 10. Files

**Code:**
- `machine_gate_s45_c2v001.py`, `campaign_s45_c2v001.py`, `ngc_admission_s45_c2v001.py`
- `apply_sched_delta_s45_c2v001.py`, `build_params_s45_c2v001.py`, `pin_compare_s45_c2v001.py`
- `sim_s45_c2v001.py`
- `tests/test_sched_s45_c2v001.py`, `tests/mock_driver_s45_c2v001.py`
- `measured/*.py`

**Data:**
- `RUN_CONFIG_DDO154_CX2V006R9_S45_C2V001.json`, `SCHED_DELTA_S45_C2V001.json`, `DELTA_REPORT_R9_TO_S45_C2V001.json`
- `DIRECT_BATCH_PARAMS_S45_C2V001.json`
- `SIM_S45_C2V001_R3.json` (final), `PHYSICS_PINS_S45_C2V001.json`
- `measured/MEASURED_BASIS_S45_C2V001.json` `e59436f8…` and its inputs
- diffs `DIFF_*`
- `HASHES.txt`: the sha256 of every file here, from bytes.
