# DELTA_V002_V003: the calibration engine and prediction freeze, v002 to v003

Claude2 lane. UTC 2026-10-17. Physical status: not_assessed.

Everything below is synthetic. No project forward model, no NGC3198 velocity, no network, single thread. Runtime: codex python 3.12 `-I -B`, numpy 2.3.5.

Two real files were opened, both hash-verified and both permitted by the rules:
- the target-free NGC3198 query manifest (`a2936517…`, ids and radii only);
- the DDO154 calibration region (`13c16a63…`), used by the v002 engine self-test and Claude3's suite.

Line numbers are v003 lines. Mechanical diffs: `DIFF_ENGINE_c2v002_to_c2v003.diff` (43 hunks) and `DIFF_FREEZE_c2v002_to_c2v003.diff` (60 hunks).

| File | v002 sha256 | v003 sha256 | v003 lines |
|---|---|---|---|
| engine | `248ba5f9…c994c02e05` | `ec509648cd7324692fac57d1c710e261555b540c82dddec72aa2384fff51fcc7` | 2934 |
| freeze | `613f3438…ec85314b` | `f670d14b74fdddca7f90566c7321f3658c4828c782aead2552e2cde55e5e8028` | 2966 |

## 1. The v002 internal checker (CHECK_V001)

| Item | v002 location | v003 lines | Change | Evidence |
|---|---|---|---|---|
| **D1**: an invalid row is all-or-nothing | freeze `_call_forward` L1071–1079; `_validate_members` L1598–1608 | freeze `_call_forward` 1313–1379 (rule at 1369–1374); verifier 1909–1917 | <ul><li>An evaluation is valid only when the flag `is True` and all 43 ids are present and finite. Otherwise `row_valid` is all False.</li><li>Finite values from an invalid evaluation are kept for diagnosis only.</li><li>The verifier refuses partial `row_valid`.</li></ul> | checker F2a, F2b PASS; v003 D1.1, D1.2 |
| **D2**: the member set is bound to the frozen selection | writer L1993–2001, L2037; verifier L1832–1837 | `_selection_plan` 912–947; selection 1231–1240 and frozen rule fields 1296–1302; writer 2405–2423; verifier 2002–2011 and 2172–2175 (alternatives 2191–2193) | <ul><li>The selection rule is a pure function. Its inputs (all admitted projections, `selection_interior_count`, `selection_anchor_log_index`) and its output (`selected_points`) are frozen in `admitted_region`.</li><li>The writer requires every evaluation's (log_index, role) list to equal the selection, in order.</li><li>The verifier recomputes the selection and compares the members against it.</li></ul> | checker F1e PASS; v003 D2.1–D2.4 |
| **D3/S12**: the query-manifest pin and the id binding | writer L1961, L2011–2021 | writer 2369–2396, 2466–2472; verifier `_validate_input_bindings` 2240–2275; re-binding from bytes 2637–2644 | <ul><li>New writer argument `query_manifest={path, sha256, role}`. `load_query_manifest` must succeed, and `query_ids` must equal its ids in order.</li><li>The file must be in `input_files`.</li><li>`role='PROGRAM_PIN'` requires sha256 `a2936517…` exactly. The program manifest cannot be bound under any other role.</li><li>The verifier re-reads the pinned manifest and re-binds the ids.</li></ul> | checker F6i, F6j PASS; v003 D3.1–D3.7 (D3.1 uses the real target-free manifest) |
| **D4**: engine-ready dicts and one step rule | freeze L626–629 and L551–555 / L1313–1315; engine L256–259 | `_engine_coordinate` 771–781; freeze step rule 680–688; the engine rule is unchanged | <ul><li>`engine_coordinates` now have nine fields in the engine's spellings (`shared`/`DDO154`; `NONE`/`BOX_ENDS`/`{step_natural}`).</li><li>Both modules apply one rule: trial ± step must lie inside [lower, upper]. Nothing is silently clipped.</li></ul> | checker F0b PASS; v003 D4.1–D4.4 |
| **S6**: one truthiness rule | engine L151–152; freeze L1060 | engine `_is_true` 290–293; freeze `_call_forward` 1339 | Both modules accept only `x is True`. `np.True_` is invalid in both. | checker S6 PASS; v003 S6.1 |
| **D8**: echoes on refusal paths | scorer L2317, L2330, L2348 | scorer 2823–2869 | <ul><li>`target_rows_sha256` and the actual manifest file sha are computed before any refusal.</li><li>The registered file sha is echoed as `manifest_file_sha256_registered`.</li><li>Nothing is parsed before the identity checks.</li></ul> | checker F6b PASS; v003 D8.1, D8.2 |

## 2. Claude4's final review (REVIEW_0462_V001 and FROM_CLAUDE4/0026)

### Blocking items A1–A5: rechecked in v003

All five still hold:
- **A1**: checker E1a–E1f PASS; v003 A1.
- **A2**: checker E2a–E2c; v003 A2.
- **A3**: checker F1a–F1e; v003 A3.
- **A4**: checker F6h; v003 A4 and D3.4/D3.5.
- **A5**: covered by D1.

### Should-fix items S1–S12 and the P34 items

| Item | v002 location | v003 lines | Change (choices in bold) | Evidence |
|---|---|---|---|---|
| **S1**: an overflowed Jacobian must not hang | engine L1188–1201 | `_numeric_guard` 198–212; SVD guard 1360–1367; FD quotient 1218–1224; `_check_identifiability` 1586–1588; Lawson 1646–1651; simplex 1686–1692; repair 2155–2170; march doubling guard 1943–1948; run status 2672–2677 | <ul><li>Before any `numpy.linalg` call, non-finite input or **any \|entry\| > 1e150** is refused with a `NUMERIC_RANGE` reason. The run ends `NUMERIC_RANGE_REFUSED`.</li><li>The simplex keeps its pivot cap and gains a **60 s wall guard** (`WALL_LIMIT`). The Lawson loop keeps its fixed iteration count and gains the same wall guard.</li><li>A march side stops after **64 doublings**.</li></ul> | checker E6 PASS; v003 S1.1 (1e307 forward, no hang, 30 s alarm), S1.2, S1.3 |
| **S2**: the repair must not move unidentified directions | engine L1880–1938 (`numerical_rank` phase; clip at L1905) | repair 2137–2201; `_step_fraction_inside` 1493–1505 | <ul><li>Claude4's fix is applied: the step **length is truncated** to stay in the box, and the step itself stays in span(identified).</li><li>**The v002 `numerical_rank` phase is removed**, because it moved near-null directions by design. S3 now identifies the directions it existed for.</li><li>`trial_projection` and `seed_projection` are both still reported.</li></ul> | v003 S2.1, S2.2; v002 engine self-test T6 shows A1 at tol 0.01 still found via the identified phase |
| **S3**: identification depends on the box | engine L1206–1216 | constants 99–107; rule 1382–1406; `_classify_directions` 1434–1448 | Claude4's stated fix:<ul><li>Identified iff the relative rule holds **or s_i ≥ z = 2.865260238532134**, the absolute threshold (E2-F2(a): a full-box move changes the σ-scaled vector by at least one half-width). `identified_by` is reported per direction.</li><li>The minimum tolerance is enforced: effective = max(tol, **1e-6**, max(m,n)·eps). A smaller request is raised to the minimum and noted.</li><li>Near-null s ≥ 1 gives a warning, and s ≥ z gives a FLAG. With the threshold at z, the FLAG cannot fire on v003's own reports; it guards supplied reports, which `_check_identifiability` recomputes.</li></ul> | v003 S3.1, S3.2; P2 B01w now FAILs by design (see §4) |
| **S4**: halving and wasted minus-side calls | engine L1012–1054 (already fixed in v002) | 1161–1173; detail 1235 | <ul><li>Kept from v002: per-side halving, and no minus call after a failed plus side.</li><li>Added: a clipped side shorter than `min_step` is dropped, giving a one-sided difference that reuses f0 (review T6c).</li></ul> | v003 S4.1 |
| **S5**: identifiability content checks | engine L1348–1407 | 1566–1631 | <ul><li>Kept from v002: names, orthonormality, sorted s, and ‖S v_k‖ = s_k.</li><li>Added: the identified set is recomputed under the S3 rule, an effective tolerance below the minimum is refused, and the numeric-range guard is applied.</li></ul> | v003 S5.1 |
| **S7**: `to_unit` reasons | already fixed in v002 (L638) | 776–806 | unchanged | v003 S7.1 |
| **S8**: a hull_box/right_vector mismatch | freeze L894–936 (WARNING only) | 1155–1193 | A malformed entry, an inf key, a key set different from the identified set, or a range mismatch now **refuses**. | v003 S8.1, S8.2 |
| **S9**: the forbidden-name scan | freeze L120–125, L285–296 | 160–177; 384–413 | <ul><li>Added names: the scorer outputs (`observed_speed_km_s`, `quoted_sigma_km_s`, `signed_residual_km_s`, `sigma_ratio`, `fractional_error`, `within_error`, `within_error_count`, the count fields, `band_overlap*`, `target_rows_sha256`) and **`velocity`**.</li><li>Any dict whose key set is exactly {id, velocity, sigma} (P46) is refused.</li><li>**Choice:** `observed_speed_km_s` is also a DDO154 region field name. DDO154 rows must therefore be pinned as a file, not embedded in the manifest.</li></ul> | v003 S9 ×3 |
| **S10**: fail closed instead of raising | freeze L285–303, L455–597, L898–902; engine (partly v002) | `_fail_closed` engine 179–195, freeze 278–294 (applied to every public function); iterative scan 384–413; type guards 601–607; `_safe_str` and `_safe_repr`; `_call_forward` try/except 1340–1379; `_validate_manifest_structure` 2114 | <ul><li>Unanticipated exceptions become ok=False / `INTERNAL_ERROR`.</li><li>**A call that does not match the keyword-only signature still raises TypeError**, because the interface contract (X0) requires it.</li><li>The scan is iterative, with a depth cap of 200 and cycle detection.</li></ul> | v003 S10.1–S10.4, S8.2; P2 `M-*.never_raises` PASS in v002 and v003 |
| **S11**: the region and its label | freeze L1807–1808, L1956–1957 | writer 2358–2362; verifier 2138–2142 | `parameter_region` must be a non-empty dict whose **`bounds_semantics` equals `COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS`**. A different label is refused, not just a missing key. | v003 S11 ×3, S11.v; checker F7c now FAILs by design (§4) |
| **S12** | = D3 | | | |
| **P34-06**: one failed point must not void 43 queries | freeze `_pointwise_envelope` L1088–1098 | 1381–1397; reporting 1494–1503; headline 2926 | <ul><li>A query is valid iff every selected member was evaluated (A3, status COMPLETE) and at least one member is valid.</li><li>The band is taken over the valid members. `n_excluded_invalid` and `n_unevaluated` are recorded per row.</li><li>A failed member is visible, scores 0, and is counted in `n_members_invalid`.</li></ul> | v003 P34-06.1, .2; C3 F3b/F3c FAIL by design |
| **P34-15**: self-hash with ≥11 int keys | freeze L202–203 | freeze `_canonical_bytes` 297–303 (via `_plain`); engine `_jsonable` and `_canonical_bytes` 215–251; writer re-verifies its own bytes 2559–2566 | <ul><li>Keys are normalised to str before sorting, consistently, in both modules.</li><li>`1` and `"1"` together raise ValueError, and callers fail closed.</li></ul> | v003 P34-15.1, .2 |
| **P34-14**: the anchor must be admitted | freeze L939–964 | 950–985 and 1194–1229 | <ul><li>The anchor member is the engine's `primary_anchor`, which is always an admitted entry. It falls back to an admitted `anchor`.</li><li>With the run output (layout A), every admitted point is **re-classified against the closed rectangles** of the hash-verified region, and a failure refuses.</li><li>**The writer requires `admission_reverified`**, so a real freeze must pass the `run_calibration_region` output to `select_representative_points`.</li></ul> | v003 P34-14.1–.3 |
| **P34-11**: the boundary cause | engine L1669–1732 | `BOUNDARY_CAUSES` 109–121; march 1918–1986; budget 2305 | Every side record carries `boundary_cause` and `first_non_admitted_kind`. Round 0 is also stored in `exploration.boundary_cause`. A rejection, an invalid evaluation, an admitted box edge, a face with no evaluation, the doubling guard and an unfinished side are all distinguished. | v003 P34-11.1, .2 |
| **P34-16**: a registration record for every calibration run | none | `exploration_fingerprint` 2713–2738; `write_calibration_record` 2770–2874; `verify_calibration_record` 2876–2934; run output 2701–2703; freeze `_fingerprint` 987–991, binding 2473–2496, verifier 2645–2655 | <ul><li>Each run gets a canonical, self-hashed, exclusive-create record, whatever its status (INPUT_INVALID included).</li><li>The record is appended to a JSONL registry whose `registry_prefix_sha256` chains every earlier line.</li><li>The freeze recomputes the exploration fingerprint. A **pinned record is bound and must carry that fingerprint**.</li><li>**Choice:** pinning the record is recommended in ROOT_CALL_ORDER, not required by the writer. The scorer reports `calibration_record_bound`.</li></ul> | v003 P34-16.1–.6; toy `calibration_record_bound: true` |

## 3. The 0470 binding decisions B5–B10: rechecked in v003

None of the code for these decisions changed in v003; every one is still covered:
- **B5 (D5)**: checker F3a–F3e and F4 PASS.
- **B6 (D6)**: F5a–F5d PASS.
- **B7 (D7)**: E3a–E3c and F0d PASS.
- **B8 (D8)**: F6a–F6g PASS, plus the extra echoes above.
- **B9 (D9)**: F7a and F7b PASS. F7c fails only on S11 (§4).
- **B10 (D10)**: E4a, E5a–E5e, F9a–F9c PASS.

One D9-adjacent tightening: non-primary alternatives must now also use the frozen selection (D2). This closes v002's open limitation 3. An alternative with its own calibration needs its own freeze.

## 4. Regression results (final bytes `ec509648…` / `f670d14b…`)

| Suite | Result | Failures, all triaged |
|---|---|---|
| (a) v002 checker, unchanged (`eb03c94e…`) via `regression/checker_v002/run_checker_v003.py` | **62/63 PASS** (the record run has 63 result entries; CHECK_V001's "62" is off by one) | <ul><li>All seven v002 failures now pass: F0b, F2a, F2b, F1e, F6i, F6j, S6.</li><li>**F7c FAILs by design (S11).** Its fixture passes `parameter_region={'bounds_semantics': 'x'}`, which v003 refuses. It is not a D9 defect: v003 S11 `s11_label` exercises the same refusal.</li><li>The wrapper adds one adapter: the synthetic Q01–Q43 manifest as `query_manifest`, appended to `input_files`. F6i is therefore refused for the missing region pin, not the missing manifest pin. v003 D3.4 tests the manifest-pin refusal directly.</li></ul> |
| (b) Claude4's B2 runner `b2_run_all.py` (`10d55a04…`), unchanged, `--engine/--freeze` set to byte-identical copies in `regression/b2_claude4/modules_v003/` | <ul><li>P2: 120 PASS / 75 FAIL / 22 SKIP, the same as the adapted copy.</li><li>c3_synth: 2 PASS / 4 FAIL / 9 ERROR.</li><li>probe: exit 1.</li></ul> | <ul><li>These suites call the **v001 signatures**, so most failures are TypeErrors on the v002 interface.</li><li>Baseline: the same runner against **v002** (`out_v002_baseline/`) gives 121/74/22, the same c3_synth result, and probe exit 1.</li><li>**The only status difference from v002 is P2 `B01w`, PASS→FAIL**: at tol 0.25 direction 2 has s ≥ z and is now identified, which is S3 by design.</li><li>The copies were needed because the c3_synth runner refuses a scratch directory inside the module directory (first attempt, `superseded_prefinal/`).</li></ul> |
| (c) Claude3's v001 suite `fixtures_0462_c3v001.py` (`670891a6…`) through `regression/c3_suite_v001/shim_v001_api/` (ADAPTER_NOTES.md) | 10/15 cases PASS: X0, E0, E1, E2, E4, E5, E6, E7, F1, F2 | <ul><li>**E3** expects `NO_ADMITTED_POINT` / `empty_region=True`; that is A1 by design.</li><li>**F3**, 7 checks: no `evaluation_log` (removed in v002); the median `central` (D5); one raising point voids all queries (P34-06); per-row NaN validity (D1); a budget-truncated envelope "valid" (A3).</li><li>**F4**: refused by D2, because the suite freezes `make_points` that are not a selection.</li><li>**F5 and F6** cascade from F4.</li><li>No engine algorithm regression was found: E0–E2 and E4–E7 pass on the analytic toys.</li></ul> |
| (d) v002 engine self-test, path adapted | 73/75 | **T6** "near-null shift recorded for numerical-rank repair" fails because the phase was removed (S2). **T15** "np.True_ accepted" fails because S6 changed it. Both are by design. T6's A1 case (tol 0.01) is still `COMPLETE`. |
| (d) v002 freeze self-test, adapted (AD-S1…S5 in the file) | 97/99 | **CX1.8** expects a strict 0/43 envelope (P34-06 by design). **SC.1** expects a NaN member to score 42 (D1 by design: it scores 0). |
| (d) v002 freeze mutants, re-run against the v003 baseline (AD-M1…M4) | 12/12 killed | |
| v003 self-test `regression/v003_selftest/selftest_v003.py` | **64/64** | In the first run, S4.1 had a fixture error in my own expectation (it matched column b's stencil). It was corrected; that run is under `superseded_prefinal_runs/`. |
| `root_call_order_toy.py` | engine COMPLETE, FREEZE_COMPLETE, all verifications ok, registry chain ok, record bound | |

No v003 defect is open from any suite. Every listed failure is either a v001/v002 expectation that v003 changes on purpose (A1, D1, D2, D5, P34-06, S2, S3, S6, S11), or a TypeError on an old signature.

## 5. Kept, open and untested

**Kept from v002**: the API, apart from the new writer argument `query_manifest` and the new engine functions `exploration_fingerprint`, `write_calibration_record` and `verify_calibration_record`. Also kept: every v002 refusal, the INNER_SAMPLE/truncation logic, the D5–D10 outputs, registration and identity, and inert import.

**Open:**
- **Root decision:** the S3 threshold z and the 1e-6 minimum tolerance are choices. FD-truncation artefacts above 1e-6 relative can still be promoted by the relative rule (E2-M2), so root should set `null_tolerance` above its forward's measured FD level.
- Wall-clock guards make an extreme numeric case machine-speed dependent. Every trip is recorded as `WALL_LIMIT` or a reason.
- Registration timing (D8): the module cannot prove the hash was logged before target access.
- One-at-a-time sensitivity (v002 limitation 1).

**Untested:**
- real forwards and the real 15-coordinate spec;
- FIFO pins;
- LAPACK builds other than Accelerate arm64;
- Claude4's B1 oracle differential and B3 mutants, which are not in this pass.
