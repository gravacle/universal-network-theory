# RO1 readout rule: implementation V002 (c2v002 successors; Claude2 root lane)

**What this is.** This document implements ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM **A49**, on top of V004 A42.2 and V005 A48 (AMB-14, AMB-15).
- It is a successor of `RO1_IMPL_V001.md`, which remains the reference for locations, design and the c2v001 tests.
- Every c2v001 file is kept unchanged (`HASHES.txt`, `5422e799`).
- Everything new uses c2v002 names. Outputs are in `out/c2v002/`, and `HASHES_V002.txt` covers every file.
- No route-A or route-B run was launched. Replays read saved checkpoints only. No NGC3198 target was opened, and C5H was not read.

## 1. What changed in c2v002 (all diffs in `diffs/c2v002/` and `driver_patch/c2v002/`)

**A49.1: the message set.** `RO1_MESSAGES` is now the three exact raised texts:

| Message | Source | Status |
|---|---|---|
| `NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH` | e9be043b L208 | caught |
| `DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed` | L205 | **new**, caught |
| `NON_TIMELIKE_COLUMN` | L184 | kept, unreachable |

The DEGENERATE entry is the full text that L205 raises. The condition is still an exact match on `str(exc)`, so the bare token `DEGENERATE_RADIAL_EULER` is not caught (TESTED). All other conditions are unchanged: `type(exc) is ValueError`, and the solve must have returned converged. The record format is unchanged too, including `rule`, so the C6 record is byte-identical to c2v001.

**Bindings** (one constant changes, plus two docstring lines):

| File | sha256 | Successor of |
|---|---|---|
| `ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py` | `86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885` | c2v001 `a28ee6ff` |
| `ngc_composite_full_coupled_binding_v002_uvtail_ro1_c2v002.py` | `52dc4065da6b0307d1a37bb63bf22921edd08709a763b0ed5a114e8c2b0f2226` | c2v001 `06a1ba9c` |

**Workers** (`tools/make_ro1_workers_c2v002.py`; each re-pins `LOCAL['binding']` and adds one docstring line):

| File | sha256 | Successor of |
|---|---|---|
| `ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002.py` | `9f74d4652dbbc237f2d38951440a9a95875251fb2cd286499b404a0cf35a8ad1` | `fc698c3c` |
| `ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002.py` | `d676ecb2c05e8017a4ffbde74a01e7a7ec1a4290149baa6cbfe62435bb573d97` | `867d2c87` |
| `ngc43_composite_coupled_root_worker_v002_uvtail_ro1_c2v002.py` | `6559ff6a364adbd5d23c04378b74e8fb6adfb8681b52f20451bc8582dce3a593` | `856de207` |
| `ngc43_composite_coupled_root_worker_v002_parallel_uvtail_ro1_c2v002.py` | `4065fe58e9f5c6734c15ab193de95c69392d477eff8d26c0e6254d49483f2292` | `33aea49e` |

**Driver patch** (`driver_patch/c2v002/`).
- `DRIVER_V009EXT_RO1_c2v002.diff` against `999331af` (+81 / −2 lines) reproduces the test vehicle `galaxy_m0_forward_c2v009_ro1_TESTVEHICLE_c2v002.py` (`db1183bc`).
- `VEHICLE_c2v002_vs_c2v001.diff` holds the changes since c2v001:
  - the six `RO1_ROUTE_A` pins;
  - `RO1_MESSAGES`;
  - **hunk 6 (A49.3).** `ngc_read_route_a_result` (v009 L4095) now computes `ro1_outcome`. When `ro1.fired`, it returns `rows None, speeds_km_s None, valid False, ro1, reasons ['RO1: …']` instead of raising TypeError. A non-fired result is handled exactly as before.
- **A49.2** (the compare requires `ro1.armed is True`): the patch already writes `armed` (unchanged from c2v001).
- The rebase guide is `REBASE_NOTE_V010_c2v002.md`.

## 2. Tests (c2v002; all five suites rerun; `out/c2v002/`)

| Suite | Result | What it shows |
|---|---|---|
| (a) synthetic `TEST_SYN_RO1_C2V002_RUN2.json` | **105/105** | See below. |
| driver patch `TEST_DRIVER_PATCH_C2V002_RUN2.json` | **7/7** | Applies to `999331af` and reproduces the vehicle. The only changed sources are the four expected functions. Non-RO1 records are unchanged. RO1 records → CONVERGED, including a real DEGENERATE result. Inadmissible records are unchanged, including the bare-token and other-ValueError refusals. DP6: the V007 compare's `check_ro1_record` reads the records. **DP7 (A49.3):** RO1-fired NGC results (NO_SUBLUMINAL, DEGENERATE) → `rows None`, `valid False`, `ro1` block, no TypeError; v009-EXT raises TypeError on them. Non-fired results are identical to v009-EXT (synthetic 43-row manifest; no NGC data opened). |
| AMB-14 `TEST_SEED_RTOL_FACTOR_C2V002.json` | **4/4** | Unchanged: absent = 1.0 = v009-EXT = the saved C6 seed; 0.1 changes only `source_rtol`. |
| (b) real-data identity `TEST_REALDATA_IDENTITY_C2V002.json` | **10/10** | See below. |
| (c) C6 replay `TEST_C6_REPLAY_C2V002.json` | **6/6** | See below. |

**(a) Synthetic, 105 checks.**
- **S0 (1).** The real e9be043b raise sites raise exactly the c2v002 texts: L208 NO_SUBLUMINAL, **L205 DEGENERATE**, L184 NON_TIMELIKE (via `rotating_log_lapse`). Both bindings carry that set; c2v001 lacks DEGENERATE.
- **S1, per galaxy (30 each, DDO154 and NGC3198):**
  - 2 identity;
  - **8 caught**: real NO_SUBLUMINAL; real **DEGENERATE through the real L205 path**, with the base's traceback ending at L205 and denominator 0.0; both messages plus DEGENERATE injected at the streaming call and at an HI column;
  - 14 unchanged after convergence: the DEGENERATE bare token, a DEGENERATE ValueError subclass, suffix, lowercase, subclass, RuntimeError, two args, other ValueError, TypeError, ZeroDivisionError, KeyError, real unresolved, HI errors;
  - **5 unchanged before convergence**, including **DEGENERATE raised inside the solve**;
  - 1 check that c2v002 equals c2v001 on every case except the three DEGENERATE-exact ones.
- **S2 (44).** 4 c2v002 workers against their 4 uvtail bases × 11 cases, including real DEGENERATE (base fails, RO1 records it) and pre-convergence DEGENERATE (both fail identically).

**(b) Real-data identity, 10 checks.** A2F10 iteration 4. Only the two RO1 c2v002 workers ran. The uvtail and c2v001 outputs of `out/runs/REALDATA_A2F10_IT4_V003` were reused. c2v002 equals the uvtail outputs and the c2v001 outputs exactly (serial and parallel), serial equals parallel, and each prediction equals the saved A2F10 route-A run exactly.

**(c) C6 replay, 6 checks.**
- The uvtail base fails exactly as the saved C6 attempt did.
- The RO1 c2v002 parallel worker records the refusal at query 3, R 1.48 kpc, φ π/4, call 86. Numerator `−4.207196855085204e-29`, denominator, pgrad, v² and the call arguments are bitwise equal to DIAG_V001.
- The patched driver gives CONVERGED; custody returns iteration 8; the compare reads `ro1` with no codes. The unpatched driver refuses.
- **RC5, byte-identity:** the c2v002 result.json equals the c2v001 V003 RO1 parallel and serial result.json exactly (one canonical digest, `050a6dcc…`). Only elapsed time, `input_pins` and the declared solver pin are excluded, and the arrays are compared by bytes.

**Disk.**
- One RO1 worker on C6 writes the 320 MB prepared arrays. The uvtail base writes none. The c2v001 serial and parallel outputs were reused rather than recomputed.
- The A2F10 suite ran 2 workers instead of 4.
- `out/c2v002` is 562 MB. The tree is 3.2 GB.

**Superseded c2v002 attempts** (kept). Both were harness defects, not code defects:
- `runs/SYN_V001` (99/105): the test's `case_msg` did not uppercase `real_degenerate`.
- `runs/DRIVER_PATCH_V001` (6/7): DP5 still treated the DEGENERATE text as inadmissible. It is admissible under A49.1; that case was replaced by the bare-token case.

## 3. TESTED / UNTESTED

**TESTED**
- The A49.1 set, the L205 real path caught after convergence, DEGENERATE before convergence failing unchanged, and the exact-text condition.
- c2v002 equals c2v001 everywhere else.
- No-refusal identity on real data; C6 byte-identity.
- The A49.3 NGC reader on synthetic NGC results.
- AMB-14 and AMB-15 as in V001.

**UNTESTED**
- NGC3198 real-data replay.
- RO1 with the tail on.
- A launched worker with the real prep and solver.
- v010 itself.
- The NGC reader on a real NGC route-A-only result.

## 4. What blocks applying the patch to v010

1. **v010 does not exist.** Re-apply hunks 1–6 and wire the c2v002 workers (`REBASE_NOTE_V010_c2v002.md`).
2. **V007 compare `0621b336` mismatch.** Its `READOUT_REFUSALS` is still the two A42.2 messages, so a DEGENERATE event reads `RO1_EVENT_REFUSAL` (TESTED, DP6). Its failure-message classifier (L408) has the same list. The compare lane must adopt the A49.1 set as exact texts, including the full L205 string.
3. **No independent check yet** of the RO1 c2v002 successors and the patch (A46 open item).
4. **Checkpoint identity changes with the worker.** V007 tail cases use the c2v002 workers from their first launch (A49.4).
