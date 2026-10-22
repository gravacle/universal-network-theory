# RO1 readout rule: implementation V001 (Claude2 root lane)

**Rulings implemented.**
- ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM **A42.2 (RO1)**.
- ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM **A48**:
  - **AMB-15**: the record sits at `result.route_a_outcome.ro1`.
  - **AMB-14**: `route_a.seed_source_rtol_factor`.

**Scope.**
- Written only under `ro1_readout_c2/`.
- No route-A or route-B run was launched.
- Replays used saved checkpoints read-only.
- No NGC3198 target was opened, and the C5H run was not read.
- Hashes are computed from bytes (`HASHES.txt`).

## 1. Where things are (TESTED, code reading; sha256 prefixes from bytes)

**Readout call path.**
- Worker → binding:
  - uvtail workers: serial `d223ad61` L135 and parallel `dac9efcb` L139 call `mods['binding'].evaluate`.
  - The same workers write `result.json` / `finish.json` at L144–147 (L148–151 in the parallel worker), and `failure.json` plus a re-raise at L148–152 (L152–157).
  - NGC workers: `5a330089` L141 and `58359035` L145.
  - C6's own worker was `9dbdaf11`: L103 calls the binding, L114–118 write the failure.
- Binding → prediction:
  - uvtail DDO binding `5e4fb5da`: the solve callback is L110–121 and calls the composite adapter at L113. `prediction.evaluate` is at L126–134, with `streaming_module` at L130.
  - NGC binding `e666bede`: L103–114 and L120–128.
- Prediction v005 `54136c71`:
  - L55 `coupled_module.solve(...)`.
  - L56–58: if not `converged_finite_fixed_point is True`, it returns `predictions_available False` and **no readout runs**.
  - L118–136 `local(phi)`; L128–131 `pressure_streaming_speed`; L139 the centre call; L156 the angular stencils; L221–222 `predictions_available True`.

**Raise sites** (`galaxy_baryonic_source_forward_v002` `e9be043b`, the module both preps load):
- `NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH`: L207–208, in `pressure_streaming_speed` (L189–209).
- `DEGENERATE_RADIAL_EULER`: L204–205, in the same function.
- `NON_TIMELIKE_COLUMN`: L183–184, in `rotating_log_lapse` (L171–186). That function has **no caller** in `helpers/` or in any `claude_artifacts/**/*.py` (grep). It is therefore unreachable from the route-A readout.

**How convergence is known.**
- The readout runs only after prediction L56 has seen the solve return `converged_finite_fixed_point True`.
- The solver returns that at uvtail serial `8ef3079b` L234–239.
- Its `_finish` (L121–127) writes `attempts/<token>.end.json` with outcome CONVERGED **before** returning. That is why C6's end record says CONVERGED although its worker failed.

**Driver v009-EXT `999331af`.**

| Step | Lines | What happens |
|---|---|---|
| Computed route-A request | L2252–2284 | worker = `SCRIPTS['route_a']` L158 (`c4cb6826`), or `PARALLEL_ROUTE_A['worker']` L239 (`9dbdaf11`) for N > 1 |
| Stage run | L2279 | a nonzero exit raises StageFailed "stage(s) exited nonzero" at L1341–1344 (C6's call result) |
| result.json | L2290–2295 | → `route_a_outcome_record` L1363–1397 |
| Coupling | **L1388** | CONVERGED only if `predictions_available is True` |
| Custody | L2299–2316 | `route_a_custody` L1444–1508 → `require_route_a_fixed_point` L1400–1419. A non-CONVERGED record raises StageFailed ROUTE_A_RESULT_INCONSISTENT at L1414–1416. |
| Route B | L2322–2326, from L2350 | custody identity and iteration feed the route-B stages |
| Rows and record | L2318–2321, L2920–2921 | `route_a_rows`; `route_a_outcome` is copied into the call result |
| Admitted route A | L2244–2250 | `finish.json` must be RETURNED_ACTUAL_RESULT, and the result sha must match |

**Where `source_rtol` lives (AMB-14).**
- The path is: seed `numerical_inputs.source_rtol` → binding `controls['source_rtol']` (DDO L117, NGC L110) → composite adapter `75092cf6` L11/L70 → uvtail solver L44.
- The solver validates it at L75/L77, records it in the checkpoint identity controls at L110, and uses it in the bound: L219 serial and L336 parallel, `bound = source_atol_J + source_rtol*scale`.
- The tail controller does not read it.
- The driver writes the seed in `per_call_seed` (L916–959).

## 2. What was written

**Where RO1 lives: the binding successors.**
- The binding is the only place where the solve callback's return and the readout meet. The worker sees a single `binding.evaluate` call.
- The worker successors only re-pin `LOCAL['binding']`.
- All successors are based on the uvtail_c2v001 route-A files. Diffs are in `diffs/`.

**Bindings.**

| File | sha256 | Base |
|---|---|---|
| `ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v001.py` | `a28ee6ff…` | `5e4fb5da` (+82 / −10 lines) |
| `ngc_composite_full_coupled_binding_v002_uvtail_ro1_c2v001.py` | `06a1ba9c…` | `e666bede` (identical RO1 text) |

What each binding does:
1. Wraps the streaming and metric modules the readout calls in pass-through recorders: same function, same keyword arguments, same return object.
2. Sets `ro1['solved']` only once the solve has **returned**.
3. Wraps `prediction.evaluate` in `except ValueError`. A refusal is caught only if all three hold:
   - `type(exc) is ValueError`;
   - `str(exc)` is in `RO1_MESSAGES = (NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH, NON_TIMELIKE_COLUMN)`;
   - the returned solve is converged.
   Anything else re-raises the same exception object.
4. When it does catch a refusal, it returns the converged solve with `predictions_available False`, `rows None`, `readout_status ROUTE_A_READOUT_NO_CIRCULAR_BRANCH` and a `route_a_readout_refusal` record. The rest of the binding return, including the checkpoint summary and `uv_tail`, is unchanged.

**Record fields.** The record uses the V007 FIELDS.md event names:
- `code`, `refusal` (= `message` = `str(exc)`), `rule`, `after_convergence: true`;
- `query` (1-based roster position), `query_id`, `phi_rad`, `R_kpc`, `R_m`;
- `numerator`, `denominator`, `pgrad`, `v2_over_c2`: `pressure_streaming_speed`'s own L201–203 arithmetic on the failing call's arguments;
- `streaming_call_index`, `streaming_arguments`, `raised_by`.

**Workers** (generated by `tools/make_ro1_workers_c2v001.py`; two edits each, +3 / −1 lines):

| Worker | sha256 | Base |
|---|---|---|
| DDO serial | `fc698c3c…` | `d223ad61` |
| DDO parallel | `867d2c87…` | `dac9efcb` |
| NGC serial | `856de207…` | `5a330089` |
| NGC parallel | `33aea49e…` | `58359035` |

**Driver patch.** Files: `driver_patch/DRIVER_V009EXT_RO1_c2v001.diff` against `999331af`, the test vehicle `galaxy_m0_forward_c2v009_ro1_TESTVEHICLE_c2v001.py` (`118c3260`, which the diff reproduces), and `REBASE_NOTE_V010.md`. The diff:
- **Pins** the RO1 workers and bindings (`RO1_ROUTE_A`).
- **RO1 classification.** `route_a_outcome_record` gains one `elif`: an **armed** attempt with an admissible record on a converged outcome → CONVERGED, and route B proceeds on the checkpoint. Armed means the result.json `input_pins` hold a pinned RO1 binding and the start.json `worker_pin` is a pinned RO1 worker.
- **AMB-15.** Every outcome record carries `ro1 = {rule 'RO1', fired, events, armed, worker_sha256, binding_sha256}`. It reaches the call result as `result.route_a_outcome.ro1` (L2920).
- **AMB-14.** It adds `numerics.route_a.seed_source_rtol_factor`, a finite number in (0, 1]. The seed becomes `source_rtol × f`. A spec without the key is byte-identical to v009-EXT.
- Every other classification is unchanged.

## 3. Tests (logs and JSON in `out/`, runs in `out/runs/`)

| Suite | Result | What it shows |
|---|---|---|
| (a) synthetic `TEST_SYN_RO1_C2V001.json` | **86/86** | Real prediction v005 and real streaming v002 on stub physics. S1 in-process bindings (DDO and NGC, 25 cases each): 2 identity, 5 caught after convergence (the real NO_SUBLUMINAL refusal, plus both messages injected at the streaming call and at an HI column), 14 unchanged after convergence (real DEGENERATE, real "Pressure radial derivative unresolved", message plus suffix, lowercase, ValueError subclass, RuntimeError, two args, DEGENERATE, another ValueError, TypeError, ZeroDivisionError, KeyError, HI ValueError, HI RuntimeError), and 4 unchanged before convergence (both messages, RuntimeError and TypeError raised inside the solve). S2: 4 RO1 workers against their 4 uvtail bases × 9 cases, run as subprocesses through the driver's LOCAL-item mechanism. |
| driver patch `TEST_DRIVER_PATCH_C2V002.json` | **6/6** | Applies to `999331af` and reproduces the vehicle. Only 3 functions change. Non-RO1 classifications are unchanged. RO1 → CONVERGED. Inadmissible records keep their old classification. The V007 compare's own `check_ro1_record` reads the records. |
| AMB-14 `TEST_SEED_RTOL_FACTOR_C2V003.json` | **4/4** | Seed absent = explicit 1.0 = v009-EXT = the saved C6 seed `95ac9b44`, byte for byte. With 0.1, `numerical_inputs` differ only in `source_rtol` (0.01 → 0.001). Dry-run plans are identical apart from declared fields. The binding hands the solve only the changed tolerance. |
| (b) real-data identity `TEST_REALDATA_IDENTITY_C2V003.json` | **13/13** | A2F10 converged iteration 4 (replay inputs of the route_a tests), 4 workers (uvtail and RO1, serial and parallel). RO1 = uvtail exactly, serial = parallel apart from the declared solver pin, and every prediction output equals the saved A2F10 route-A `result.json` exactly. |
| (c) C6 replay `TEST_C6_REPLAY_C2V003.json` | **6/6** | C6 iteration-8 checkpoint. The uvtail base fails exactly as C6 did. The RO1 parallel and serial workers record the refusal at query 3, R 1.48 kpc, φ = π/4, call 86. Numerator, denominator, pgrad, v² and all 7 call arguments are bitwise equal to DIAG_V001 `EXACT_C6_IT8_V001`. They keep the converged solve (identity `e3815c48`, iterations 0–8). The patched driver gives CONVERGED; custody on the C6 checkpoint returns iteration 8 and the START response route B reads; the V007 compare reads `ro1` with no codes. The unpatched driver refuses the same result with ROUTE_A_RESULT_INCONSISTENT. |

**Superseded attempts** (kept, never edited). Each was a harness defect, not an RO1 defect:

| Run | Outcome | Cause |
|---|---|---|
| `SYN_PROBE_V001` | 86/86 | earlier record field names |
| `REALDATA_A2F10_IT4_V001` | 1/13 | the stand-in demanded the full prepared-dict digest, but the checkpoint stores only the two arrays |
| `REALDATA_A2F10_IT4_V002` | 11/13 | earlier binding/worker shas; the serial-against-parallel check did not exempt the declared solver pin (re-evaluated with the exemption by `tests/recheck_realdata_serial_parallel_c2v001.py` → `out/RECHECK_REALDATA_SERIAL_PARALLEL_V002_C2V001.json`, 2/2) |
| `C6_IT8_REPLAY_V001` | 4/6 | compared an encoded residual against a decoded one |
| `C6_IT8_REPLAY_V002` | 6/6 | interim driver vehicle `13615b2d` |
| `DRIVER_PATCH_V001` | 5/5 | interim driver vehicle `13615b2d` (ro1 only on armed attempts); no DP6 |
| `SEED_RTOL_FACTOR_V001` | 3/4 | dry-run config shas embed the report-dir path |
| `SEED_RTOL_FACTOR_V002` | 4/4 | interim driver vehicle `13615b2d` |
| seed log `RUN_V001` | — | syntax error, no run directory |

## 4. TESTED / UNTESTED

**TESTED**
- RO1 catches only the two named messages, only as exact `type(exc) is ValueError` with exact `str`, and only after a returned converged solve. Everything else propagates as the same object (synthetic S1/S2).
- No-refusal outputs are exactly the uvtail outputs, on synthetic and on real A2F10 data, and equal the saved A2F10 run.
- C6 replay: record values bitwise equal to DIAG; converged result and checkpoint handed to route B; the driver classifies CONVERGED (vehicle).
- AMB-14 seed, normalization and dry-run identity; AMB-15 record path read by the V007 compare's own function.

**UNTESTED**
- NGC3198 real-data replay (NGC is synthetic only).
- RO1 with the UV tail ON. The RO1 change does not touch the tail path, but this has not been run.
- v010 integration: v010 does not exist.
- A launched worker with the real prep and solver. By rule, only the prep and composite stand-ins ran.
- `ngc_read_route_a_result` (v009 L4083) on an RO1 result. It would raise TypeError on `rows None`; that is the NGC route-A-only path.
- Whether a V007 identity-gate builder sources part_c from these tests.

## 5. What blocks applying the patch to v010

1. **v010 does not exist.** Hunks 1–5 have to be re-applied, and the worker wiring done at v010's uvtail route-A launch sites (`driver_patch/REBASE_NOTE_V010.md`). The v009-EXT diff does not wire the workers, because v009-EXT passes no UV-tail flags.
2. **The message set (root to confirm before the V007 seal).** A42.2 names NON_TIMELIKE_COLUMN, which the readout can never raise. DIAG §5 and VERIFY §5 named DEGENERATE_RADIAL_EULER, which is reachable at L205. As ruled, DEGENERATE still fails the call (TESTED, both the real and the injected case). Changing the set means editing `RO1_MESSAGES` in both bindings and the driver, and re-pinning.
3. **No independent check yet.** The RO1 successors and the patch have not had one (A46 open item). The uvtail bases are still under their own final check.
4. **Checkpoint identity changes with the worker.** An RO1 worker's checkpoint IDENTITY differs from a uvtail worker's in `caller.worker`, the binding code pin and `composite_full_driver.driver`. V007 runs must therefore use RO1 workers from their first launch.
5. **FIELDS mismatches and notes.**
   - FIELDS has no `armed` field, so the compare cannot tell whether RO1 was installed. Recommendation: for `ro1_required` cases, require `route_a_outcome.ro1.armed is true`.
   - An event whose refusal was not raised by `pressure_streaming_speed` has `numerator` and `denominator` null. The compare reads that as a loud TYPE_num code (DP6). The real readout never produces such an event.
   - `ro1` is present on every route-A outcome, as AMB-15 says. With non-RO1 workers it reads `armed false, fired false`.
