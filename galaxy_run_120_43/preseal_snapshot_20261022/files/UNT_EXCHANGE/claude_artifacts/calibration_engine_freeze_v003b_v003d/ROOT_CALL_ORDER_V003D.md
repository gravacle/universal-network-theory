# ROOT_CALL_ORDER_V003D (engine `calibration_region_engine_c2v003b`, freeze `prediction_freeze_c2v003d`)

Successor of `calibration_freeze_c2_v003/final/ROOT_CALL_ORDER.md` (`ab5d467e…`). It adds the A13 step 0a of `INTERFACE_C2V003B.md` and Claude4 0475 R1 SF-3 (steps 7 and 8). Every other row is the v003 text.

The order: engine → [record] → select → evaluate members → [reference] → sensitivity → write → register → verify → score.

The runnable toy is `root_call_order/root_call_order_toy_v003d.py`. It runs these steps on synthetic stand-ins and writes only under `root_call_order/root_call_order_runs/`:

```
OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10 <codex python3> -I -B root_call_order_toy_v003d.py --mode 4D|3D
```

Record runs on the final bytes (engine `6ec8b2d0…`, freeze `74e0d406…`):

| Run | Admitted | Members | Status | Checks |
|---|---|---|---|---|
| `run_4D_20261018T030907Z_72900` | 28 | 10 | FREEZE_COMPLETE | verify ok; SF-3 step 7 (7 checks) and step 8 ok |
| `run_3D_20261018T030907Z_72944` | 26 | 10 | FREEZE_COMPLETE | verify ok; SF-3 step 7 and step 8 ok |

The headlines are identical to the v003b toy runs in both modes (`calibration_freeze_c2_v003b/root_call_order_runs/run_4D_20261017T225052Z_53948`, `run_3D_…_53950`).

## Real call vs toy

| Input | Toy | Real |
|---|---|---|
| Region | synthetic region; its sha is logged at step 1 | the DDO154 region file, `13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d` |
| Query manifest | synthetic (`role: 'SYNTHETIC_FIXTURE'`) | `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` (`a2936517…`, `role: 'PROGRAM_PIN'`) |
| Forwards | toy forwards | the real forwards |
| Coordinates (A13) | toy list, `apply_coordinate_mode` | the V001 list + NGC3198 slots V002, with the addendum `coordinate_mode` (V005, or V005A of this folder) |
| Targets | invented rows | the real target rows, only after step 8's checks |

## Steps

| # | Call | Must hold before the next step |
|---|---|---|
| 0a | A13 only: `F.apply_coordinate_mode(coordinates=…, coordinate_mode=<addendum coordinate_mode>)` | Only the scope and role of the single DDO154 distance change (to `ddo154_fixed` / `fixed`), at 4.04 Mpc. |
| 0 | `F.make_freeze_coordinate_spec(coordinates=…)` | <ul><li>Every coordinate has units, a scope and a kind; kind `other` never carries Mpc/deg or a distance/inclination name (v003c).</li><li>NGC3198 has exactly one distance slot (13.8 Mpc reference) and one inclination slot.</li><li>One step rule: trial ± step lies in the box.</li><li>Returns `spec` and the engine-ready `engine_coordinates`.</li></ul> |
| 1 | `E.run_calibration_region(forward=DDO154 forward, coordinates=fs['engine_coordinates'], observation_region_path, observation_region_sha256=13c16a63…, …)` | <ul><li>Pass `engine_coordinates` unchanged (D4).</li><li>**Log the region sha256 used here** (SF-3; real: `13c16a63…`).</li><li>Freeze only when `status == 'COMPLETE'`.</li><li>Other statuses are results to register, not to retry silently.</li><li>v003b: an exactly-zero scaled-Jacobian column shows as a `NOTE (v003b SF-2)` in `identifiability.reasons`.</li></ul> |
| 1b | `E.write_calibration_record(run=run, record_path, registry_path)` | <ul><li>Call it for **every** run, whatever its status (P34-16).</li><li>Log `record_file_sha256` and the registry path.</li><li>Pin the record in `input_files` at step 5.</li></ul> |
| 2 | `F.select_representative_points(exploration=run, interior_count=k, spec=fs['spec'])` | <ul><li>Pass the **run output itself** (the run that was recorded at 1b).</li><li>v003d: the writer and the verifier recompute this selection from the pinned record and require byte equality (SF-1), so a run edited after 1b refuses at step 5.</li></ul> |
| 3 | `F.evaluate_envelopes(forward_ngc, points=sel['points'], spec, query_ids, budget)` | <ul><li>Pass `sel['points']` unchanged (D2).</li><li>`status` must be COMPLETE.</li><li>Repeat once per EVALUATED alternative, on the same points.</li></ul> |
| 3b | `F.select_reference_member(selection=sel, evaluation=ev)` | At least one member is valid. The reference is frozen here, before any target access. |
| 4 | `F.evaluate_sensitivity(forward_ngc, reference, selection, spec, query_ids, null_direction_rule, budget)` | <ul><li>`status` is COMPLETE.</li><li>Every near-null direction and every declared coordinate is displaced on both sides (D6).</li><li>v003d: the box edge has the engine's face slack; a side is skipped only when its largest coordinate move is ≤ 1e-9.</li></ul> |
| 5 | `F.write_freeze_manifest(…, code_files=[freeze, engine], input_files=[region file, query manifest, calibration record], allow_incomplete=False)` | <ul><li>v003c/v003a checks unchanged.</li><li>v003d (SF-1): the record's status, stage and flags equal the frozen ones; IDENTIFICATION_RULE holds with the record's report; the selection recomputed from the record equals the frozen one byte for byte.</li><li>The writer re-verifies its own bytes, then writes the registration file.</li></ul> |
| 6 | **register** | <ul><li>Before any NGC3198 target is opened, log `manifest_file_sha256`, `registration_file_sha256` and `record_file_sha256` in a FROM_ message, next to the step-1 region sha and the step-1b registry path.</li><li>No module can enforce this timing (D8).</li></ul> |
| 7 | `F.verify_freeze_manifest(…)`, `F.verify_registration(…)`, `E.verify_calibration_record(record_path=<input_bindings.calibration_record.path of the verified manifest>, registry_path=<the step-1b registry>)` | <ul><li>All are ok.</li><li>**SF-3:** `input_bindings.calibration_record.path` is a record line of the **step-1b registry** (realpath), and its `sha256` equals that line's `record_file_sha256` **and** the step-6 logged `record_file_sha256`. Verify the record on that bound path, not on the path the writer was given.</li><li>**SF-3:** `input_bindings.observation_region.sha256 == 13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d` (toy: the sha logged at step 1).</li><li>The verifier recomputes the selection from the bound record (v003d), the envelope, the reference, the sensitivity plan and the freeze status.</li></ul> |
| 8 | `F.score_after_freeze(freeze_manifest_path, registration_path, expected_manifest_file_sha256=<logged at step 6>, target_rows)` | <ul><li>**Before the target rows are opened (SF-3):** read the manifest bytes, require their sha256 to equal the logged `manifest_file_sha256`, and require `input_bindings.observation_region.sha256 == 13c16a63…` again.</li><li>Targets are opened only now. The expected sha comes from the external log, never from the registration file.</li><li>The headline is the member-count distribution plus the reference member.</li><li>Also check `freeze_status`, `query_manifest_role == 'PROGRAM_PIN'`, `query_manifest_is_program_pin` and `region_possibly_truncated`.</li></ul> |

## What the SF-3 rows catch (TESTED, `tests/test_sf3_call_order_v003bd.py`, 7/7)

- **S3a.** A second, self-consistent run is recorded in another registry and frozen with its record pinned. The v003 steps 7/8 pass. The new step 7 refuses: the bound path is not in the step-1b registry, and its sha differs from the logged one.
- **S3b.** A self-consistent forged region file (widened rectangles, its own sha) is used for a run recorded in the step-1b registry. The v003 steps 7/8 pass. The new steps 7 and 8 refuse on the region sha.
- **Honest run.** Both orders pass.

**Residual (unchanged, D8).** A forgery that is also logged at step 1 and step 6 is indistinguishable here. Only the external log's timing separates it.
