# DELTA: engine v003b, freeze v003d, ROOT_CALL_ORDER_V003D and orchestrator v005a pins

Claude2 lane, 2026-10-18 UTC. Source: Claude4 0475 R1, `REVIEW_CALIBRATION_V003A_0475_V001.md` (`87751def…`) and `CARRYOVER_V001.md` (`4d350947…`).

Physical status: not_assessed. Everything is synthetic. No NGC3198 target or velocity file was opened, nothing was launched, there was no network access, single-thread BLAS was used, and at most 3 processes ran at once (`nice -n 10`, codex python `-I -B`).

## Modules (sha256 from bytes)

| File | sha256 | Predecessor |
|---|---|---|
| `calibration_region_engine_c2v003b.py` | `6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3` | engine v003a `193841fa…` |
| `prediction_freeze_c2v003d.py` | `74e0d4060e443755486fba3aa0775060d2909c2bb78df9d948f346159112b67d` | freeze v003c `3d58b5fb…` |

**Diffs.**
- `DIFF_ENGINE_c2v003a_to_c2v003b.diff`: 4 hunks, +97/−3.
- `DIFF_FREEZE_c2v003c_to_c2v003d.diff`: 12 hunks, +279/−10.

**AST delta** (`tests/runs/AST_DELTA_V003BD.json`, FORMAL).
- **Engine.** It adds `_clean_zero_columns`, and changes only `identifiability_report`, the docstring, `MODULE_NAME` and `PREDECESSOR`.
- **Freeze.** It adds:
  - the rule constants, which equal the engine's (TESTED);
  - `_identification_rule_reasons`, `_record_identifiability_reasons`, `_record_status_reasons`, `_member_key` and `_check_record_binds_selection`.

  It changes only `_edge_t`, `_sensitivity_plan`, `evaluate_sensitivity` (the reason text), `_validate_admitted_region`, `write_freeze_manifest`, `_verify_bytes`, the docstring and `MODULE_NAME`.
- **Unchanged** (AST): the v003b fixed-distance mode (`apply_coordinate_mode`, `_build_spec`, labels, `headline_conditions`) and the v003c relabel refusal and run-coordinate binding.

## What changed

### Engine v003b: SF-2 engine part, exactly as specified, nothing else

In `identifiability_report`, after `_fix_signs`, each exactly-zero scaled column j is handled as follows:
- the right vector with the largest |V[k][j]| becomes +e_j;
- every other right vector gets 0 on those columns and is renormalised.

**Two implementation notes beyond the specification text, both forced by the engine's own `_check_identifiability`.**
1. **Multi-carrier fallback.** When more than one null vector carries the column (n > m, or two zero columns), the remaining carriers are re-orthonormalised (modified Gram-Schmidt). The literal recipe is not orthonormal there: U3 needed this in 200 of 200 n = 15 cases.
2. **Revert.** If the cleaned basis still fails the tolerances, the uncleaned basis is kept and a NOTE says so.

**Reporting.** A `NOTE (v003b SF-2)` in `identifiability.reasons` names the columns. With no exactly-zero column, the report is identical to v003a's (U2, 400/400).

### Freeze v003d: SF-1, the SF-2 freeze part, and v003b/v003c kept

**SF-1, writer and verifier (`_check_record_binds_selection`, on the mandatory pinned record).**
1. **Selection recomputed.** `select_representative_points` is recomputed from the record's run. The run's region path is replaced by the pinned, sha-verified region file. The frozen `admitted_region` must be byte-equal (canonical) to the recomputation. The selection points (writer) and every member list (writer and verifier) must equal the recomputed points: log_index, role, u, projection and θ.
2. **Status and flags.** Status, stage, ok, flags, truncation causes, truncation evidence and coverage are cross-checked against the record.
3. **Identification rule re-applied** in `_validate_admitted_region`.
   - **Structural form**, always: the frozen singular values are now required.
   - **Exact form**, with the record:
     - the effective tolerance must follow the engine formula;
     - the partition must follow IDENTIFICATION_RULE;
     - V must be orthonormal and diagonalise the recorded SᵀS;
     - the frozen basis must equal the record's.

**SF-2, freeze part.**
- `_edge_t` has the engine's face slack (U4: 0.2257 = 1e-12/4.43e-12, where v003c gave 0).
- A side is skipped when s ≤ 1e-12 or s·max|d| ≤ 1e-9. So a genuine outward component at a face still spends no NGC3198 call.
- The skip reason states the rule; it was F:1797 / v003c:2043.

### ROOT_CALL_ORDER_V003D.md (SF-3)

- **Step 7.** Verify the record at `input_bindings.calibration_record.path`. That path must be in the step-1b registry, and its sha must equal both the registry line's sha and the step-6 logged sha.
- **Steps 7 and 8.** Require `input_bindings.observation_region.sha256 == 13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d`. Step 8 checks this on the manifest bytes that hash to the logged sha, before targets are opened.
- **Toy.** The successor toy `root_call_order/root_call_order_toy_v003d.py` implements both. Diff against the v003b toy `adeb8b3e…`: `root_call_order/DIFF_root_call_order_toy_v003b_to_v003d.diff`.

### Orchestrator v005a (`orchestrator_v005a/ORCHESTRATOR_V005A_PIN_NOTE.md`)

- **Pin chain.** Coordinate spec V002 (engine pin → v003b) → addendum V005A → config V005A. There is no orchestrator code change.
- **Cache id: unchanged, TESTED.** The engine sha and the coordinate-spec sha are not inputs of the cache id formula. A read-only dry plan of the real config gives `3a1374dfbf0df2f3ea0e48ae2eb76ebdccf0b05568ed0940682383a2b0fb781c` under both V005 and V005A, and the plans are otherwise identical except for the config sha and pid.

## Tests (all on the final bytes above)

| Test | Old bytes | New bytes |
|---|---|---|
| SF-2 unit, `tests/test_sf2_unit_v003bd.py` (13/13) | v003a leaks > 1e-12 in 196/400 (max 9.3e-11); freeze `_edge_t` = 0 at a face | exactly clean in 400/400, checks pass, partition unchanged; no-zero-column report identical; slack = engine |
| SF-2 D6 chain (r2 Part D port, 288 FACE + 288 CONTROL; on engine v003a + freeze v003a all 576 rows equal r2's PARTD rows: displacements, skips, ratios, partitions) | engine v003a + freeze v003a: **108/288** (42 lost, 66 cut, min band ratio 0.373); engine v003a + freeze v003c: **108/288**, identical | engine v003b + freeze v003d: **0/288** (min ratio 1.0). CONTROL 0/288 in every pair. Freeze v003d alone on engine v003a: 0 lost, but 93 cut → the engine half is what closes it |
| SF-1 scenarios, `tests/test_sf1_scenarios_v003bd.py` (26/26): A1/A1b V2-F2 status, A2 V6-1 basis swap, A3 V4-F1 projection steering, A4 V4-F2 relabel, A4b relabel before 1b, A5 OBS-V rotation | v003c writes every edited freeze FREEZE_COMPLETE and verifies it (7/7 reproduced) | v003d writer refuses all 7; the v003d verifier refuses all 7 manifests written with every v003d SF-1 check switched off; honest H0 is written and verified by both; honest BUDGET_EXHAUSTED is refused (A3) by both |
| SF-1 rule unit, `tests/test_sf1_rule_unit_v003bd.py` (7/7) | v003c has no rule re-application | a relabel within [MIN·s_max, eff·s_max) passes the structural form and is refused by the exact form; rotated basis, edited eff and s = 0 relabel are refused |
| SF-3 call order, `tests/test_sf3_call_order_v003bd.py` (7/7) | the v003 steps 7/8 accept a second record from another registry (S3a) and a forged-region freeze (S3b) | the new step 7 refuses S3a; the new steps 7/8 refuse S3b; honest passes both |
| Regression: the v003c suites, path-wrapped (`regression/`), for EA (engine v003a) and EB (engine v003b) | v003c: T1 54/54, T2 10/10, checker_v003 52/52, v003_selftest 64/64, x1_attack 41/41, x1_probes 19/19, guard 30/30 | v003d: **identical, check by check**, in all 13 suite-variants (`regression/REGRESSION_COMPARE_V003C_V003D.json`: 0 status changes). T2 is EA only, because its engine comes from orchestrator c2v004's own pin |
| Root call order toy, 4D and 3D | v003b toy runs | FREEZE_COMPLETE; headlines identical to v003b's; SF-3 checks ok |

## SF-2 real-run relevance: UNTESTED (`deciding_sf2/DECIDING_SF2_V001.md`)

- **No real seed Jacobian exists.** Calibration has not started, and every real run is a single forward at the anchor θ.
- **Deciding test.** It is ready to run on the first real record: `deciding_sf2/deciding_test_sf2_on_record.py`. It was self-tested on the toy record.
- **Bounding test at the real shape** (12 × 3, TESTED on synthetic matrices). A leak arises only if a varying coordinate's FD column is exactly zero. Then it arises only at position 1 (`gamma_over_Eref`) with column scales spanning ≥ 2.5 decades (8–25 of 2000). v003b cleans every case.

## Limits (UNTESTED, with the deciding test)

- **Real inputs** (real forwards, real region, PROGRAM_PIN manifest). Deciding test: the real ROOT_CALL_ORDER_V003D run.
- **Residuals no module can close.**
  - A forgery made before step 1b that is coherent: a re-recorded run with a self-consistent S, V and partition, or a rotation inside an exactly degenerate null subspace.
  - A forgery logged at steps 1 and 6.
  - Only the external log's timing separates either. This is unchanged.
- **Engine-side B2 adapter suite** (927/935 in R1) was not re-run on v003b. The engine change is covered here by U1–U3, by the D6 chain, and by every freeze suite in variant EB. Deciding test: run the R1 V1-AD adapter on v003b.
- **Not addressed in this revision** (R1 "also worth fixing"): V7-N1, V6-4 and V4-N3. They are a candidate next revision.
- **Independent review** of these bytes is pending, through the checkers' `check/` folder.
