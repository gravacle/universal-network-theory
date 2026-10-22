# CHECK_V001: independent check of V006 R1 (extension_c5c6/v006_r1)

Checked 2026-10-17. Nothing launched. All my outputs are under `v006_r1/check/`; nothing outside it was written, moved or deleted. Python `-I -B`, nice 10, single-thread BLAS, at most 4 processes. No NGC3198 file opened. ~/.codex not touched.

## VERDICT: PASS (0 MAJOR, 0 MEDIUM, 1 LOW, 6 INFO)

Each CHECK_V001 (849d1b8d) finding M1, L1, L2, L3, L4 is applied and TESTED. The decision semantics of the V006 draft are unchanged; the only semantic changes are the five findings. The specs differ from the reviewed M16 specs only in `/label` and `/numerics/route_a/max_iterations`. Caps are in the launch record only. My own dry runs are clean. Both test suites pass on my rerun.

**Seal state: NOT ready.** (i) holds. (ii) is PENDING: `extension_c5c6/check/REVIEW_V009_PREP_V009_V001.json` does not exist (checked from disk).

## 1. Pinned inputs (sha256 from bytes)
All unchanged: V006 draft f90ab96c, draft compare e6475f38, draft tests 87506f45, CHECK_V001 849d1b8d, M16 specs (C5 N8 c8321156, C5 N1 c7d6b722, C6 N8 b7bf831f, C6 N1 19b651bf), LAUNCH_EXT_V001 a869567e, driver v009 999331af, V005 compare 49404bc4.

All 16 R1 shas in the author's return match my hashes. `HASHES_V002.txt` has 141 entries, and all of them verify. Together with HASHES_V002.txt itself they are exactly the files on disk outside check/.

## 2. Finding by finding

| finding | applied as | my evidence | status |
|---|---|---|---|
| **M1** | max_iterations 32 in `cases[C5,C6].route_a_numerics` (V3 term), in `criterion.gates` and in `fixed_across_extension_cases`. V1 (iii) is restated: 32 is the c2v009 ceiling, so the next step is a driver successor plus a new prereg, with no rerun under R1. All 4 specs carry 32. | Spec diff vs M16: only `/label` and `max_iterations` 16→32 (all 4). Probe: under R1, 16, 33 and workers 4 are rejected (V3 → INCOMPLETE); 32 is admitted. Driver `ROUTE_A_MAX_ITERATIONS_MAX = 32` (L243). | TESTED, fixed |
| **M1 caps** | Output: C5 96 GiB, C6 128 GiB. Wall: 50400 / 68400 / 75600 / 104400 s. RSS unchanged. | I recomputed every cap from ESTIMATES_V001 (a51d6281) with the stated rule `3600·ceil(1.5·(route_A(32)+route_B_prop)/3600)`. Route A(32) = 11465 / 15748 / 30100 / 41311 s, and every cap matches. Output worst case at 32 iterations is 79.8 / 109.5 GiB (from the G4 route-A bytes 11572753195 over 7 iterations). The per-iteration layout is confirmed in the C4 route-A tree (checkpoint iteration_0000..0006, node_diagnostics per iteration). | TESTED, fixed |
| **L1** | V3 requires the bound result sha for C4/C3/C2/R when the bracket block equals R3; under a later R(n) it is only reported. | Probe: a mutated C4 sha under R3 → INCOMPLETE (`bound_result_sha256 … != registered aac01962…`); the same under R(n) is not enforced. A C3 result in the C4 slot fails on grid and sha. C3/C2/R mismatches fail their own V3 but do not move the decision (they are diagnostic roles; X1 reads C4–C6). | TESTED, fixed |
| **L2** | The compare calls the pinned V005 `v005_admissibility(pre5)`. A failing v005 case gets `V005_INADMISSIBLE` and V005's own inadmissible_next_step. | The R1 `binding_inputs.v005_admissibility` condition, next step and deciding_test equal V005's text exactly. Real execution: PASS_BITWISE_EQUAL. The deciding result is 01bc9557 and its finish is 2aa72616 (I hashed both). Probe with an inadmissible v005: C4/C3/R fail V3, C2 (v001) and C5/C6 are unaffected, the outcome is INCOMPLETE, and the C4 next step equals V005's text. Passing `None` also gives INCOMPLETE. | TESTED, fixed |
| **L3** | Carries `K0_max_rel_diff_vs_C2` (the same expression as V005 main) and `field_diagnostic` (V005 `packet_checks`/`ring_diagnostic`). `--no-field-diagnostic` now works. | My real-bytes E2E rerun (test_mode false, pinned R1 prereg) gives K0 = C4 0.2968, C3 0.1792, C2 0, R 0.00067, and 12 ring rows per present case. With the flag, the field is null, the ring block is absent from the table, and the gates and decision are identical (T26). | TESTED, fixed |
| **L4** | `cases[C5,C6].outdirs` has primary_N8 and alternate_N1 (outdir and receipt) on the External1 real path. The compare reports `registered_outdir` and does not decide on it. | Probe: N8 → `primary_N8`, N1 → `alternate_N1`, and the outcome is the same. | TESTED, fixed |

## 3. Nothing else changed in V006 semantics
- **Leaf diff of the prereg JSON (V006 draft vs R1):** every changed leaf belongs to one of the following: M1 (`route_a_numerics`, specs, gates, V1/V3 next steps, `fixed_across_extension_cases`), L1 (`bound.result_sha256_enforced`), L2 (`binding_inputs.v005_admissibility`), L3 (`diagnostics_reported`, X4 diagnostics sentence), L4 (`outdirs`), or the bookkeeping blocks (status, revision, revision_r1, supersedes_draft, predates_state, resources_note, max_iterations_independence).
- **These blocks are canonical-JSON equal to the draft:** `grids`, `row_ids`, `tau_km_s`, `quoted_sigma_km_s`, `carried_from_r3`, `unchanged_from_v005`, `scope_untested`, `extends`, `plan_item`, `context_not_used_by_the_decision`.
- **Decision rules X1–X3 are byte-equal.** X4 differs only by the added diagnostics clause.
- **Compare diff (e6475f38 → a7816746):** it contains only the pin, the L1/L2/L3/L4 code, the table refactor (now adds the R and ring columns) and docstrings. `v009_admissibility`, `route_a_inputs_gate` (V7) and the decision block are unchanged.
- **My decision-equivalence probe** (`tools/chk_draft_vs_r1_decisions.py`, `CHK_DRAFT_VS_R1_V001.json`): 100 synthetic (d45, d56) pairs with C5/C6 deltas in {0 … 10}·tau, including ±1e-7 around the boundary. I ran the draft at max_iterations 16 and R1 at 32. The decision dicts (outcome, subtype, reasons, u_i, next step) are identical in 100/100, and the evaluate output keys are identical.
- **V7 still valid for the 32-iteration seeds.** prep v009 names `max_iterations` only in the `prepare_inputs` signature (L41). It is never used in the body and is not accessed indirectly (no locals/vars/kwargs). The C4 IDENTITY `inputs_sha256` keys contain no max_iterations; it sits in `controls`. The author's M32 smoke files equal the registered M16 expectations in every digest leaf: C5 85 equal leaves, C6 87. The only differences are seed path/sha, max_iterations, timings and RSS. **I did not rerun the operator evaluation itself on the M32 seeds** (UNTESTED by me; the author reports it TESTED-POSITIVE).
- No pin of 17c26616, 5bef6552 or any V004 addendum appears in R1 (string search).

## 4. Dry runs (mine, guarded: no process creation, writes only under check/)
Driver v009 999331af, the 4 R1 specs:
- **All four ran clean:** each exits 0, plans 12 stages, and has `binding_blockers` [], `remaining_refusals.unexplained` [] and `beyond_pending_inputs` 0. The only refusal class left is PRODUCED_BY_THIS_CALL (4 fields).
- **Route-A setup:** prep v009 b4b27a1d is used at 108 and 120 nodes per axis. The N8 calls run route A on the parallel worker with `--column-workers 8`.
- **Seeds:** my per-call seeds are byte-equal to the author's (C5 18eb99dc, C6 95ac9b44). Against the M16 seeds, the leaf diff is exactly `/numerical_inputs/max_iterations` and its mirror `/c2_changed_fields/changed/5/new` (16 → 32).
- **Other simulated inputs:** all 12 input files equal the author's once the report directory is substituted. The plan differs only in the fs_manifest sha, and the manifest embeds the report directory.
- **Negatives (author's logs, read):** MAXIT 33 is refused ("must be an int in 1..32, not 33"), and v008 refuses C5 ("108 nodes/axis > 80 … declared P-88 grid").

## 5. Tests (my reruns)
- R1 suite (c9bc0cf7) → `check/tests_r1_rerun_V001/`: **30/30 PASS**, stderr empty.
- V006 draft suite (87506f45) → `check/tests_v006_draft_rerun_V001/`: **18/18 PASS**.

## 6. Launch record and seal preconditions
- **Commands:** the four monitor commands match LAUNCH_EXT_V002.json (pinned monitor ba031c23, driver 999331af, M32 spec shas, real-path outdirs and receipts, caps as in §2).
- **C6 start gate:** the grep string matches the driver's event writer byte for byte (`json.dumps(stage=…, event='finished', …)`, L1279/L1340) and the format seen in the C4 progress.jsonl. The `finished` event is written after the route-A process exits, whatever its exit code. The receipt fallback covers a C5 that ends early.
- **Disk:** External1 has 3723 GiB free.
- **(i) holds:** `runs_ext`, through the symlink and the real path, holds only `.metadata_never_index` and `.speedtest`, and nothing under `CLAUDE2/runs` names C5 or C6.
- **(ii) pending:** the review record is absent. `SEAL_READY_V006_R1_V002.json` (7562c6d4) correctly says `ready_to_seal: false`.

## 7. Findings
**L1 (LOW): Three places name the superseded SEAL_READY record.**
- The places are the R1 prereg `status` string, LAUNCH_EXT_V002.json `preconditions[0]`, and the header of LAUNCH_EXT_V002.commands.txt. All three point to `SEAL_READY_V006_R1.json` (79a5e38b, superseded; its tests field named the draft rerun) instead of `SEAL_READY_V006_R1_V002.json`.
- It does not affect the decision, and the preconditions in the two records are the same.
- Fix without re-pinning: SEAL_RECORD_V006_R1 names `SEAL_READY_V006_R1_V002.json` (7562c6d4) as the seal-ready record. Correct the text if an R2 is cut for any other reason.

**I1 (INFO): Turning the field diagnostic back on brings back V005's coupling.** An exception inside `ring_diagnostic` is caught with V4 and V5 set to False, because it shares the try with `packet_checks`. This is identical to V005 main, and the V006 draft avoided it only by never computing the field. The risk is low: at G6 the arrays are about 8×1.73M complex per batch, and on real data the gates are identical with and without the flag (T26).

**I2 (INFO): L1 enforcement only changes the decision for C4.** The C3, C2 and R sha mismatches show up as V3 failures in their gate entries. Those are diagnostic roles, X2 uses the carried R3 inner control, and so the outcome is unchanged. This is consistent with V006's roles.

**I3 (INFO): `registered_outdir` compares unresolved path strings.** A CASES path given through the `CLAUDE2/runs_ext` symlink reports None (probe). This is reported only, and LAUNCH's `cases_file_content` uses the real path.

**I4 (INFO): The carried V005 next step refers to V005's gate numbering.** The V005 inadmissible_next_step is carried verbatim, as L2 asked. Its "gate V1 (iii)" means V005's V1 (iii) (BLOCKED_ROUTE_A), not R1's V1 (iii) (route-A budget). The ambiguity is for a reader only.

**I5 (INFO): Cap margins.**
- The C6_N8 RSS cap of 32 GiB is 1.499× the modelled 21.35 GiB, so CHECK_V001's "≥1.5×" was off by 0.001. The author disclosed this and left the cap unchanged.
- The output caps sit at 1.20× (C5) and 1.17× (C6) over the 32-iteration worst case, as CHECK_V001 specified. That margin is lower than the 1.5× used for wall and RSS.
- The worst case needs route A to converge at the last iteration. A miss falls under V1 (i): a rerun from zero with the cap raised.

**I6 (INFO): R1 never mentions V004.** It neither pins nor names the V004 addendum. The cite by name appears only in SEAL_READY `decision_file_pins`. This is consistent with the rule.

## Files (v006_r1/check/)
CHECK_V001.md, HASHES_CHECK_V001.txt, LEAFDIFF_PREREG_V006_vs_R1.txt, CHK_DRY_SUMMARY_V001.json, CHK_DRAFT_VS_R1_V001.json, tools/{chk_guard_r1.py, chk_dry_summary.py, chk_draft_vs_r1_decisions.py, chk_leafdiff_prereg.py}, dry/{C5,C6}R3_A2F10_EXT_{N8,N1}/, logs/, tests_r1_rerun_V001/, tests_v006_draft_rerun_V001/ (+ stdout/stderr).
