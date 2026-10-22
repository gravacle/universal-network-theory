# CHECK_V001: independent check of track 1 (cube extension to C5/C6)

Checked 2026-10-17. I launched no run. All my outputs are under `extension_c5c6/check/`, and I deleted nothing. I ran numpy only, under nice 10, with single-thread BLAS and at most 2 processes at a time.

## VERDICT: PASS_WITH_DEFECTS (0 MAJOR, 1 MEDIUM, 4 LOW, 3 INFO)

The build matches the sealed V005 text. The prep successor and driver changes are minimal and behave the same as before. I re-ran two bitwise reproductions and one V7 expectation myself, and all three are bitwise equal. The dry runs are clean, and the specs differ from C4R3 only in the intended leaves.

V006 predates any C5/C6 result, and it keeps V005's statistics and gates unchanged. There is one internal inconsistency (M1). It must be fixed before V006 is sealed.

## 1. Against the sealed V005 text (dbddc02c)
- **V005 rule 3** names exactly this extension. It requires: extending the shape with the smallest Dhat_A(3,4) (cube 12.47 < cylinder 16.66 < sphere 17.57); K = 5 and 6 with the same order-6 unit outer panels; 108/120 nodes; a prep node budget of at least 120; and a per-call cap of at least 6 GiB under separate review.
- **V005 has no rule that decides after the extension.** V005 also states "a change is a new version with its reason recorded". So drafting V006 is the right move.
- **V006 G5/G6 grids** (my own check):
  - each is G4 plus unit panels [4,5] (and [5,6]) per side, all order 6;
  - the orders sum to 108 and 120;
  - the G4 breaks are contained;
  - the C5/C6 spec `composite_grid_spec` equals the V006 grid block;
  - G2/G3/G4/GR in V006 equal V005 (canonical JSON).
- **V006 keeps V005's statistics**, checked from bytes:
  - row_ids, sigma and tau are identical to V005, and tau = 0.25·sigma on every row;
  - the statistic Dhat, the pass test (Dhat(5,6) ≤ 1 and ≤ 0.5·Dhat(4,5), the V005 form shifted by one K), the Picard gate 0.0125 and the tail diagnostic (reported, never adopted) are unchanged;
  - the V005 compare script (49404bc4) is pinned and supplies adapt_result, packet_checks, diffs and validate_recovery.
- **u_i** is the V005 form shifted by one K. The shape-spread term is reported null and labelled UNTESTED, not zero. Correct.
- **FLOOR_LIKE** only labels a NOT_CONVERGED_EXT subtype, and its next step is a new prereg version. V005 D14 (no floor clause) is respected.
- **Predates C5/C6:**
  - `CLAUDE2/runs_ext` (the symlink to External1) is empty;
  - no `*C5*` or `*C6*` outdir exists under `CLAUDE2/runs`;
  - V006 is a DRAFT that is not sealed.
- **R3 bindings:** the bound C4/C3/C2/R result shas in V006 equal the R3 verdict inputs (aac01962, c9c802f4, 1f6b32a4, a83d69bc).
- **No pin of the open V004 addendum.** Neither V006 nor driver v009 contains 17c26616/5bef6552 or a V004 addendum. The only addendum mention in the driver is the inherited NGC V002_ADDENDUM history text from c2v006, which v009 did not add.

## 2. Minimal diffs (recomputed from bytes)
- **Prep:** `diff prep_v008 (bb05f974) prep_v009 (b4b27a1d)` gives exactly one line, 130: `nk>96` becomes `nk>120`.
  - For every nk ≤ 96 this predicate is false in both versions. It is never reached when `composite_grid_spec` is None.
  - So by inspection v009 behaves the same as v008 on every input v008 accepts.
  - There is no other size literal in the file.
- **Driver:** `diff -u v008 (f8e47701) v009 (999331af)` gives 10 hunks, byte-equal to `DIFF_V008_V009.diff` (7f06e403). The changes are:
  - the AUX prep_v009 pin;
  - the 120-node constant;
  - DECLARED_LARGE_GRIDS G5/G6;
  - the `normalize_route_a_numerics` max_iterations (1–32, strict int);
  - the per-call seed `max_iterations`;
  - the prep selection 97–120 (no review pin, recorded in prep_info);
  - LOCAL prep injection for v009.
- **max_iterations is only a loop bound.** I checked this in the serial solver (44d9c23c:110) and the parallel solver (aed4dd59:196): `for iteration in range(start_iteration, max_iterations)`. Otherwise it is only recorded in the controls of the checkpoint identity and the binding's `numerical_controls`, and it reaches the solver through binding_v002:97.

## 3. Bitwise reproduction (my own script, `tools/chk_prep_v009_repro.py`)
My script has two parts:
- It loads prep v008 and prep v009, both patched as in the saved request, calls `prepare_inputs(**seed.numerical_inputs)` on each, and compares every output key in memory.
- It compares the v009 outputs with the saved route-A IDENTITY and with iteration_0000/START, through the pinned cache facade.

| prefix | v008 = v009 (18 output keys; 2 callables code-equal; source_pins) | IDENTITY inputs_sha256 | START (6) | node diag (2) | verdict |
|---|---|---|---|---|---|
| C4 = KMAX_A2F10_C4_V005_RUN_V001 (G4, 96) | all equal | 26/26 | 6/6 | 2/2 | **PASS_BITWISE** (414 s) |
| C3 = KMAX_A2F10_C3_V005_RUN_V001 (G3, 84) | all equal | 26/26 | 6/6 | 2/2 | **PASS_BITWISE** (294 s) |

I did not re-run C2 (G2); for it only the author's PASS_BITWISE exists. Outputs: `repro2_C4/`, `repro2_C3/`. The `repro_C*` directories are a first attempt that aborted on undigestable callables; they are kept and are not evidence.

**V7 expectation for C5, recomputed independently** (`tools/chk_v7_expect.py`, `v7_C5/`):
- Source: the per-call seed from my own v009 dry run. Its sha c8d32557 equals the smoke seed. It has max_iterations 16 and 108 nodes.
- Prep v009 operator evaluation gives 5 identity digests + 21 fourier_arguments + 6 START digests, all equal to `PREP_V009_SMOKE.json` (9b585caa): **PASS_BITWISE**.
- I did not re-run C6; it rests on the author's smoke file only.

Prereg V006 tests: re-run into `rerun_author_tests_V001/`: 18/18 PASS.

## 4. Dry runs and key lint
- **My own dry runs** under v009, C5 N8 M16 (c8321156) and C6 N8 M16 (b7bf831f), each run in my own guard (no process creation, writes only under check/):
  - both exit 0 with 12 stages planned and 0 binding blockers;
  - `remaining_refusals.unexplained` = [], and the only class left is PRODUCED_BY_THIS_CALL (4 fields);
  - the seed changes include max_iterations 16 and 108/120 nodes;
  - the route-A request uses the parallel worker (9dbdaf11) with `--column-workers 8` and has prep v009 injected.
- **Simulated inputs and plan** equal the author's `dryrun_b2` files once the report-directory path is replaced. The only plan difference is the fs_manifest sha, and that manifest is itself equal once the path is replaced.
- **Author's dryrun_b2 job table, read only:** the negatives are refused (G5 orders, 132 nodes, MAXIT 0/33/bool, MAXIT 9 admitted). v008 refuses C5. POS MAXIT 8 admitted runs.
- **R3 admitted specs blocked under v008/v009:** confirmed (route_a_custody seed BLOCKED). The cause is that the v005 and v009 G4 per-call seeds (fc70a262 vs f7bf4923) differ only in the leaf `/c2_changed_fields/driver` (`galaxy_m0_forward_c2v005` vs `..._c2v006`). numerical_inputs are identical.
- **Leaf diff, mine, of C5/C6 against the C4R3 run's `inputs/call_spec.json`** (3ea94efe, the generator's pinned source): only `admit` (becomes {}), `label`, `numerics.composite_grid_spec.*` and `numerics.route_a.{column_workers, max_iterations}` change. Brackets equal the R3 block 7946b857. N8 and N1 differ only in column_workers and label.
- **Override-key lint** (canonical decimal keys): PASS by the generator's rule. No override key changed from C4R3.
- **HASHES.txt:** all 947 entries verify from bytes, and the file set equals the directory (outside check/).

## 5. Findings

**M1 (MEDIUM, TESTED): V006's pre-named V1 (iii) next step is rejected by V006's own V3 gate.**
- V1 (iii) says that a route A without a fixed point within 16 iterations is rerun "with max_iterations 32". But V3 requires `numerics.route_a.max_iterations == 16`, from `cases[].route_a_numerics`.
- Probe P1 (`CHK_COMPARE_EXTRA_V001.json`): a valid synthetic C5 with max_iterations 32 gives INCOMPLETE, with C5 failing V3 on `route_a numerics {..32} not {16..}`. That path can never decide under V006.
- **A rerun with 32 also recomputes from zero.** max_iterations is in the checkpoint identity controls, so a 16-iteration checkpoint cannot be resumed.
- **The author's own pessimistic projection sits at that edge.** The G6 model in `ESTIMATES_V001.json` gives residual/bound 1.14 at index 13 with ratios ≈ 0.95. That points to about 1.03 at index 15, which is not converged within 16. My recomputation of the saved histories confirms the measured inputs: G4 ratios 0.453 → 0.664, accepted at index 6.
- **Fix (pre-seal):**
  - **(a) Preferred:** set max_iterations 32 (the v009 ceiling) in the C5/C6 specs and in V006. It is only a loop bound, so it computes the same arrays if route A converges earlier.
    - Raise the C6 output cap to about 128 GiB (G4 route A measured 11 GiB over 7 iterations, so G6 is about 2.9 GiB per iteration, about 93 GiB at 32, plus route B).
    - The C6 N8 wall cap of 64,800 s still covers about 43k s at 32 iterations.
    - The C5 output cap of 64 GiB covers about 41 GiB at 16 iterations and about 75 GiB at 32, so it rises to about 96 GiB.
  - **(b) Alternative:** register max_iterations ∈ {16, 32} in V3, with 32 allowed only on the V1 (iii) path.

**L1 (LOW): The V006 compare does not enforce the bound C4 result sha (aac01962); it only reports it.** V3 (grid, cube, R3 block, v005) still admits only C4R3-like runs; probe P3 shows a C3 result placed in the C4 slot fails V3 on grid. Enforce the sha when `--bracket-recovery` is R3.

**L2 (LOW): V006 does not execute V005's v005-admissibility condition for C4/C3/R.** That condition is the deciding test, which must be PASS_BITWISE_EQUAL, with finish result_sha256 equal to its bytes. I verified it holds now (PASS_BITWISE_EQUAL, sha OK, driver 2aef51c4). Either execute it or record it as carried from R3.

**L3 (LOW): V006 drops a diagnostic V005 registered.** V005 states "K0 drift between grids is reported, not hidden", and its compare reports `K0_max_rel_diff_vs_C2` and `field_diagnostic`. The V006 compare reports neither, and its `--no-field-diagnostic` flag is a no-op. Carry the diagnostic (reported, not decided).

**L4 (LOW): The N1 alternate outdirs are not registered in V006.** The N1 alternates launch to `..._C5R3_N1_RUN_V001` / `..._C6R3_N1_RUN_V001`, but V006 `cases[].outdir` names only the N8 directories. This does not affect the decision (the compare reads the CASES map). List both in V006.

**I1 (INFO): S5 (cross-driver) is correctly scoped as UNTESTED in run mode at G4.**
- It stands on the same footing as R3, whose Dhat(2,3) already mixed C2 under v001 with C3 under v005.
- Extra evidence I found:
  - the G4 seeds differ only by the annotation;
  - the prep inputs are bitwise equal (section 3);
  - the body stage diff from gal_c2v003 to gal_c2v004 is admission/validation only for DDO154 (D3: "J = last → the full form (DDO154, as before)").
- I did not inspect the other 10 stage diffs (UNTESTED).

**I2 (INFO, projection, UNTESTED):**
- Continuing the measured cube q = 0.3965 geometrically gives Dhat(4,5) ≈ 4.94 and Dhat(5,6) ≈ 1.96, which is CONTRACTING_ABOVE_TAU (probe P5).
- An ADOPT at K = 6 needs faster contraction than measured.
- The next step for that outcome (K = 7/8, 132/144 nodes, prep budget ≥ 144) is already registered.

**I3 (INFO): Probe P4 is a construction artifact.** P4 (Dhat 5 → 1 built by float addition) lands just above 1 and gives CONTRACTING_ABOVE_TAU. The author's T11 avoids this with 1 − 1e-9. Not a defect.

**Estimates and caps:** re-derived from the saved C4 route-A sizes and residual histories, and consistent with ESTIMATES_V001 (a51d6281).
- Caps: RSS 24/32/8/12 GiB, at least 1.5× each modelled peak.
- Machine: 128 GiB and 18 cores.
- The monitor sets single-thread BLAS itself (root_monitor_c2v001 L26, L137).
- The V005 per-call cap of at least 6 GiB is met.

## Files (check/)
CHECK_V001.md, HASHES_CHECK_V001.txt, CHK_COMPARE_EXTRA_V001.json, tools/{chk_prep_v009_repro.py, chk_v7_expect.py, chk_guard.py, chk_leafdiff.py, chk_compare_extra.py}, repro2_C4/, repro2_C3/, v7_C5/, dry/C5_N8/, dry/C6_N8/, rerun_author_tests_V001/, plus logs.
