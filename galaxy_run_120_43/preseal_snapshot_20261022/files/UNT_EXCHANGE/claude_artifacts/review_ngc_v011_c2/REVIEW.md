# Review: NGC driver v011 cx3v003 (Claude2 independent lane)

date -u: Sun Oct 18 13:11 UTC 2026. The review was refute-by-default and used only my own scripts in `tools/`. I launched nothing. The only runs were dry runs and saved-state prep/operator replays. I did not open any NGC3198 observed or target velocity file, and I did not touch the forbidden C5H run directory (an audit hook in `tools/guarded_dry_run_c2r.py` refuses it). Nothing was deleted.

**Object.** Driver `galaxy_m0_forward_c2v011_cx3v003.py` (d120eead), its NGC route-A and route-B successors, and Codex3 packets 0579, 0582, 0585 and 0587, all under dispatch 0517.
**Base.** Driver v010 r4 (b9ae92d5).

## VERDICT: PASS_WITH_FINDINGS

- No BLOCKING finding for the source build.
- Five SHOULD_FIX items and eight NOTEs.
- This is not production readiness. The pending EPS/LO certificates, the open original-spec B0 gate and the items below all stand.

## Structure (TESTED)

v011 is byte-for-byte v010 r4 up to its `__main__` guard. A 987-line appendix follows (`tools/shadow_census_c2r.py`).

The appendix rebinds exactly 8 v010 names: `cmd_dry_run`, `cmd_run`, `execute_chain`, `normalize_spec`, `route_b_static_refusals`, `uvt_binding_blockers`, `uvt_route_a_monitor` and `final_rows_check`.

- Each rebinding passes straight through unless the call is NGC3198 with `numerics.uv_tail`.
- The exception is `final_rows_check` (F1 below).
- `_execute_ngc_v011_chain` differs from v010 `execute_chain` in 9 hunks. All are NGC-only: the seed is produced in-driver, the anisotropic grid edge is used, prep is v011, and `attempt_result=ra` is passed for NGC.
- All 1,601 hashes in Codex3's HASHES_V001.json re-verify from bytes.

## The seven checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | DDO plan identity, v011 against v010 r4, with the B0-EMPTY rule | **TESTED PASS 6/6, plus 1 NO_EVIDENCE.** A2F10, ADMIT_ROUTE_A_C2V005, RULE_FULL_C2V001, C4T tail-ON continuum, C4T-D5 nodes_v001 and Z2_OFF_RO1 complete with non-empty plans, every file identical. The only byte difference is the driver path/sha inside DRYRUN_REPORT.json. C4R3 (historical) refuses identically in both drivers at seed custody: no evidence. | `B0_REVIEW/B0_REVIEW_RESULTS.json`; method in `tools/b0_review_c2r.py`. Each driver runs in its own process with the same report-dir path; no other substitution is allowed. |
| 2 | NGC route B successors are galaxy-parameterized | **TESTED PASS.** All 11 stage successors differ from their reviewed bases only by: the binding pin, passing the checkpoint `caller`, cut and effective-count helpers, the offset grid via the shared helper, and a stricter checkpoint-seed check. The binding is NGC-only. It adds registered H2 continuum to the tail source once, plus a separate finite H2 packet used only for I1-T. The reuse PROFILE is the shared multi-galaxy f5becd45, not a DDO file. Per-call Eref/γ (×s) and ℓ_F reach the seed. D≠13.8 and i≠72 are refused for both specs (4/4). In the dry runs, every executed route-B stage script equals a V011_B_STAGES pin. | `diffs/*.diff`; `CONTRACTS/CONTRACTS_C2R.json` (seed_checks, dry_runs) |
| 3 | Route A binds A2 2e3a36d8 and refuses fe5a2f06 when the tail is ON | **TESTED PASS.** For both A and B specs, normalize refuses: fe5; coefficients absent; A2 path with fe5 sha; fe5 path with A2 sha; `enabled:false` (10/10). Full dry runs with fe5 refuse before any report on both routes. The registered dry runs use the NGC worker e8ccc0d5; the A2 sha is present and fe5 appears nowhere in the report. Prep COEFFICIENT is A2. My reports equal Codex3's DRY_NGC_A/B_CX3V003 except for hashes derived from the report-dir path. | `CONTRACTS/` |
| 4 | T120L 120×120×80 at iteration 0 reproduces phase23 T120L_hovr (e6453d52) | **TESTED PASS, 14/14 bitwise.** The prep arguments came from the **driver's own** `normalize_spec` and `_ngc_v011_seed` on CALL_NGC_V011_A, not a hand-edited seed. Bitwise equal: k_physical, dk_weights, source_hessian_grid, fixed_source, initial_gas and current_source. A first-principles leggauss rebuild of the grid, independent of the helper, also equals the saved k_physical and dk_weights. The operator was recomputed on blocks [0,48k), [768k,816k) and [1104k,1152k): weighted_responses and wavevectors bitwise. All fa scalars equal. Wall 118 s, peak RSS 1.41 GB, 0 gas iterations. | `T120L_RECHECK_C2R.json` |
| 5 | Outer-gas truncation wiring | **TESTED PASS on mechanics, with findings F2 and F3.** Run on the real target-free roster (4,992 columns = 156 radii × 32 azimuths) with a 30.347 kpc **test fixture**, which is not a confinement finding. The whole cut radius and every azimuth are dropped. 1,440 columns are kept, with no renormalization. The dropped HI mass fraction 0.190808 is recomputed independently and recorded in the prep custody and the checkpoint source_parameters. A 2e-14 fraction tamper, a non-roster radius, an uncertified status, a different control point and a wrong full-roster digest are all refused. The prep control digest equals the route-B ni digest. Stars and H2 are untouched. Route-B effective count is 45, equal to route A's kept prefix. Route A and route B agree on the beyond-cut rows (Q37–Q43). The reason string is a v003e built-in registered reason. | `CUT_WIRING/CUT_WIRING_C2R.json` (19/20; the 1 fail is F3) |
| 6 | Tail added exactly once per NGC lapse site | **TESTED PASS (static).** The AST census of `uvt.*` calls is identical in all 11 stage successors and their bases. The binding has no added or removed tail calls. The driver chain has the same 8 `uvt_argv` sites and the same plan, identity-check and admitted-check calls. The tail source is stars_registered with H2 as one extra component, once; the H2 packet rings feed only the I1-T comparison. In-grid fixed source (cube K=2) and tail (outside cube K=2) are complementary. Runtime additivity is UNTESTED. | `TAIL_SITES_C2R.json` |
| 7 | The assembly comparator against the v009 parent detects only the intended INVALID semantics | **TESTED PASS, with finding F1.** The cmd_run assembly block is AST-text identical across v009, v010 r4 and v011. Across 13 synthetic cases, v009 and v011 differ exactly on the cases that contain a well-formed outer-cut row. Every malformed variant is refused identically: finite speed, unregistered reason, missing valid flag, 42 rows, mixed ids, all rows invalid. **The widening:** v011 accepts QUERY_BEYOND_OUTER_GAS_CUT on an interior row (Q20 alone) as COMPLETED. | `ASSEMBLY_SEMANTICS_C2R.json` |

## Findings

**F1, SHOULD_FIX: outer-cut INVALID rows are not tied to the cut at assembly.**
- v011 `final_rows_check` maps QUERY_BEYOND_OUTER_GAS_CUT to the inner reason for any NGC3198-Q row. It is not gated on tail-ON or on a pinned cut, and it does not check that the rows are exactly {q : R_q ≥ cut}.
- freeze v003e also admits this reason with `registration: None`.
- Result: an interior mislabelled row is accepted (TESTED).
- The impact is bounded: such a row can only become an INVALID_AS_MISS, never a hit.
- Fix: in the NGC v011 assembly, require `normalized_spec.numerics.ngc_outer_gas_cut`, and require the outer-INVALID set to equal the rows at or beyond `first_unconfined_R` from that record.

**F2, SHOULD_FIX (root ruling): a real cut is likely to fail the whole call instead of marking rows INVALID.**
- With the 30.35 kpc fixture, Q36 (between the last retained route-B node at 29.63 kpc and the cut) makes the column mean raise NGC_QUERY_BELOW_CUT_OUTSIDE_INTERPOLATION_SUPPORT.
- Any cut at a GL node leaves a gap below the cut like this. With the query spacing near the cut (~0.7 kpc gap here), this case is typical, not rare.
- Failing closed is correct under 0518, because the gap rows have no registered reason. But it means the A14 C3 path, as wired, will probably produce no result.
- Root must register the gap-row treatment (or the cut radius definition) before a cut is used.
- Codex3 typed this as a limitation; this review quantifies it on the real roster.

**F3, SHOULD_FIX: route A accepts what route B refuses.**
- `ngc_grid_cut_cx3v001.apply_cut` (route-A prep) accepts `classification_evidence: {}`.
- The route-B binding (`ngc_cut_record`) and the column mean require a non-empty dict.
- Result: a full route-A solve can run and then fail at route B. Apply the same non-empty rule in apply_cut.

**F4, SHOULD_FIX (coordinator): drift against A55.**
- v011 is built on v010 r4: tail lib c28d4209 with the 0.6 GiB guard, and a K_big 16 NGC config, as 0517 specified.
- A55 (13:05Z, after 0517) sets production K_big = 128 for "every tail-corrected case" and seals **v010 r5** (a pin swap).
- Before any NGC tail-ON launch, root must rule whether NGC route A/B uses K_big 128 or the N-test K_big 16. Then rebuild v011 on r5 and rerun B0 (r5 against v011) with the B0-EMPTY rule.

**F5, SHOULD_FIX: an unused key is silently accepted.**
- `numerics.k_domain` passes `_strict` in the v011 normalize and is then dropped (TESTED: accepted with arbitrary content).
- Refuse it, or forward it.

**Notes:**
- N1. The full original all-DDO-spec B0 gate is still BLOCKED by the six historical R3 equal refusals. Under B0-EMPTY they are no evidence (C4R3 was reproduced here). This is not a v011 defect, and root owns the ruling.
- N2. The "route A" and "route B" dry runs plan the identical chain: route A is computed in-driver because route_a_inputs is pending. The tail-ON path that admits a supplied NGC route A (route_a_inputs with tail-ON checkpoint identity) is not exercised: UNTESTED.
- N3. `headline_rule` text names only QUERY_INSIDE_INNERMOST_NODE even when outer-cut rows are present. Cosmetic.
- N4. A top-level JSON list spec raises AttributeError in v011, where v010 raises a Refusal. The exit code is the same (99), and no registered spec is affected.
- N5. NGC tail-OFF with fe5 still normalizes. This is inherited from v010 and outside 0517's tail-ON scope.
- N6. Route-B `ngc_cut_record` trusts the record's mass and roster fields. The full recheck happens only where the reference stage reruns `apply_cut`, and the column mean builds `caller` from the seed ni (a self-comparison). Custody relies on the cut record carried in the rotation records.
- N7. The prep successor also changes `initial = None if analytic_initial_azimuth`. This is outside the dispatch scope but preserves semantics: the analytic branch overwrites it, as the initial arrays re-check bitwise.
- N8. NGC route-A runtime I1-T is NOT_EVALUATED in the controller. A52.4 requires it before any NGC N-test is read (Codex3 typed blocker I1T_RUNTIME_GATE, confirmed). The monitor is raw M_T_NOT_NORMALIZED, and the controller handles null v_ref/tau.

## UNTESTED here

- Real stage execution, end to end.
- Physical confinement or a physical cut.
- Nonlinear cut feedback, and route-A pressure stencils that straddle the cut.
- The production EPS/LO certificates.
- The run-mode path past the static refusals (no launch allowed).
- The GL10 alternative.

## Files

- Tools: `tools/` (guarded_dry_run_c2r, b0_review_c2r, b0_specs_c2r.json, contracts_c2r, t120l_recheck_c2r, cut_wiring_c2r, assembly_semantics_c2r, tail_sites_c2r, shadow_census_c2r).
- Results: `B0_REVIEW/`, `CONTRACTS/`, `T120L_RECHECK_C2R.json`, `CUT_WIRING/` (holds the test-fixture cut records, clearly labelled TEST_FIXTURE), `ASSEMBLY_SEMANTICS_C2R.json`, `TAIL_SITES_C2R.json`, `SHADOW_CENSUS_C2R.json`, `MALFORMED/`, `diffs/`.
- `HASHES.txt` covers every file here, hashed from bytes.
