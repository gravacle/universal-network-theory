# ROOT_CALL_ORDER: v003 (engine `ec509648…`, freeze `f670d14b…`)

The order is: engine → [record] → select → evaluate members → [reference] → sensitivity → write → register → verify → score.

The runnable toy is `root_call_order_toy.py`. It follows these steps exactly on synthetic stand-ins and writes only under `root_call_order_runs/`:

```
OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 <codex python3> -I -B root_call_order_toy.py
```

Record run `root_call_order_runs/run_20261017T143415Z_55821/`:
- **Engine:** COMPLETE, 28 admitted, with causes `march_reached_box_edge` and `admitted_point_on_box_face`.
- **Freeze:** 10 members; FREEZE_COMPLETE; `calibration_record_bound: true`.
- **Checks:** verify ok, registration ok, registry chain ok.
- **Score:** the member-count distribution is min 0 / median 0 / max 43 (on invented targets), and the reference member scores 0.

The real call differs only in its inputs:

| Input | Toy | Real |
|---|---|---|
| Region | synthetic region | the DDO154 region file (`13c16a63…`) |
| Query manifest | synthetic manifest (`role: 'SYNTHETIC_FIXTURE'`) | `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` (`a2936517…`, `role: 'PROGRAM_PIN'`) |
| Forwards | toy forwards | the real forwards |
| Targets | invented target rows | the real target rows, after step 7 |

| # | Call | Must hold before the next step (otherwise the call refuses or the step stops) |
|---|---|---|
| 0 | `F.make_freeze_coordinate_spec(coordinates=…)` | <ul><li>Every coordinate has units, a scope and a kind.</li><li>NGC3198 has exactly one distance slot (13.8 Mpc reference) and one inclination slot, each with a sensitivity.</li><li>One step rule: trial ± step lies in the box.</li><li>Returns `spec` and the engine-ready `engine_coordinates`.</li></ul> |
| 1 | `E.run_calibration_region(forward=DDO154 forward, coordinates=fs['engine_coordinates'], observation_region_path, observation_region_sha256, …, ddo154_distance={'name', 'modulus_half_width_multiple'}, …)` | <ul><li>Pass `engine_coordinates` unchanged (D4).</li><li>The distance coordinate's box equals the `distance_summary` box.</li><li>Freeze only when `status == 'COMPLETE'`, then read `region_possibly_truncated` / `truncation_causes`.</li><li>`NUMERIC_RANGE_REFUSED`, `NO_ADMITTED_POINT_FOUND` and the other statuses are results to register, not to retry silently.</li></ul> |
| 1b | `E.write_calibration_record(run=run, record_path, registry_path)` | <ul><li>Call it for **every** run, whatever its status (P34-16).</li><li>Log `record_file_sha256`.</li><li>Pin the record in `input_files` at step 5; the writer then binds it by `exploration_fingerprint`.</li></ul> |
| 2 | `F.select_representative_points(exploration=run, interior_count=k, spec=fs['spec'])` | <ul><li>Pass the **run output itself**: admission is re-verified against its hash-verified region (P34-14), and the region and fingerprint are recorded.</li><li>The anchor member is the engine's primary anchor.</li><li>A malformed or inconsistent `hull_box` refuses (S8).</li></ul> |
| 3 | `F.evaluate_envelopes(forward_ngc, points=sel['points'], spec, query_ids, budget)` | <ul><li>Pass `sel['points']` unchanged (D2).</li><li>`status` must be COMPLETE.</li><li>An invalid evaluation is invalid at all 43 rows (D1), is excluded from the envelope (P34-06), and scores 0.</li><li>Repeat once per EVALUATED alternative, on the same points.</li></ul> |
| 3b | `F.select_reference_member(selection=sel, evaluation=ev)` | At least one member is valid. The reference is frozen here, before any target access. |
| 4 | `F.evaluate_sensitivity(forward_ngc, reference, selection, spec, query_ids, null_direction_rule, budget)` | <ul><li>`status` is COMPLETE.</li><li>Every near-null direction and every declared coordinate is displaced on both sides (D6).</li></ul> |
| 5 | `F.write_freeze_manifest(out_path, registration_path, parameter_region={…, 'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'}, observation_rule, spec, selection, alternatives, alternative_evaluations, reference, sensitivity, query_ids, query_manifest={'path', 'sha256', 'role'}, code_files=[freeze, engine], input_files=[region file, query manifest, calibration record], notes, allow_incomplete=False)` | <ul><li>`query_ids` equal the pinned manifest's ids, in order (D3).</li><li>`code_files` contain the executing freeze module, and `input_files` contain the region file and the query manifest (A4/D3).</li><li>The members equal the selection (D2), and the S11 label is present.</li><li>The writer re-verifies its own bytes and only then writes the registration file.</li></ul> |
| 6 | **register** | <ul><li>Before any NGC3198 target is opened, log `manifest_file_sha256`, `registration_file_sha256` and `record_file_sha256` in a FROM_ message.</li><li>The toy writes `EXTERNAL_REGISTRATION_LOG.jsonl` as a stand-in.</li><li>No module can enforce this timing (D8 limitation).</li></ul> |
| 7 | `F.verify_freeze_manifest(…)`, `F.verify_registration(…)`, `E.verify_calibration_record(record_path, registry_path)` | <ul><li>All are ok.</li><li>The verifier recomputes the selection (D2), the envelope, the reference, the sensitivity plan and the freeze status.</li><li>It re-reads every pin from bytes, re-binds the ids to the pinned query manifest, and re-checks the bound record's fingerprint.</li></ul> |
| 8 | `F.score_after_freeze(freeze_manifest_path, registration_path, expected_manifest_file_sha256=<the hash logged at step 6>, target_rows)` | <ul><li>Targets are opened only now.</li><li>The expected sha comes from the external log, never from the registration file.</li><li>The headline is the member-count distribution plus the reference member.</li><li>Also check `freeze_status`, `query_manifest_role == 'PROGRAM_PIN'`, `query_manifest_is_program_pin` and `region_possibly_truncated`.</li><li>Every refusal still echoes the target-row hash and the file hashes.</li></ul> |
