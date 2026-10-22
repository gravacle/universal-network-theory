# REVIEW_PREREG_V003_C3_V001 — Claude3 distinct review of KMAX pre-registration V003 and the factor-10 specs (dispatch 0474)

Reviewer: Claude3 (Claude Code 2.1.302, model claude-fable-5-1). Read-only everywhere outside this directory; no launches; no NGC3198 velocity opened. Every number below was produced by `review_evidence_c3v001.py` (output `REVIEW_EVIDENCE_V001.json`) and the two extraction scripts; hashes are from bytes.

## Verdict: PASS_WITH_CORRECTIONS

The two intended changes are the only substantive changes; thresholds, gates, criteria and the decision rule are byte-identical to V002; the factor-10 values are the seed scan's factor-10 candidate bitwise; the admission blocks match the factor-10 stage outputs; the seal precedes the run's result. Four corrections, none of which touches a criterion.

## Bytes reviewed

| Object | SHA256 |
|---|---|
| `kmax_prereg_v003_c2/KMAX_MATRIX_PREREG_V003.json` | `8e36b64355f75a49a40c15f3e842f089740aae94547d66a709033bd9d66cddab` |
| `kmax_prereg_v003_c2/kmax_compare_c2v003.py` | `42e5dc266435246919c28515759fcaeb9aae7068c6a84e3ad258e04efe6b6e32` |
| `kmax_prereg_v002_c2/KMAX_MATRIX_PREREG_V002.json` | `0024b63ecf9c4c4aa3b4ae88db3084b956c12760696b69963f4fa514354c9e10` (equals V003 `supersedes.sha256`) |
| `CLAUDE2/specs/CALL_A2_ANCHOR_F10_C2V001.json` | `a93c95b95c1f112b7293ffd598371335227cb93d7334981be33e368c6cd9f52b` (= F10 run `inputs/call_spec.json` = F10 `launch.json pins.spec`) |
| seed-scan NEXT spec (factor 3) | `fe1ad000a4ff35d84f16e7aceeb1e1d597d2b7885218f2c5d8e968ffce995560` |

## Checks

**1. V002 → V003 diff (18 leaf differences, mechanical recursive diff).** Touched paths: `anchor` (definition text; `physical.gamma` 8.823146682203324e+41 → 2.941048894067774e+42; `physical.common_scale_s` 0.3332538300367979 → 0.10154172268068731; `base_spec` added), `binding_inputs.anchor_base_spec.sha256` (fe1ad000… → a93c95b9…), `cases[6].bound_call` (`call_spec_sha256`, `launch_file`, `outdir`: F3 → F10), `criterion.bracket_precondition_P6.deciding_test` (run name only: "A2_ANCHOR_F3_RUN_V001" → "A2_ANCHOR_F10_RUN_V001"; wording otherwise identical), `status` (run name only), `schema` (V002 → V003 label), `supersedes` (restructured to a path+sha pointer at V002; the sha matches V002's bytes), `change_log_v003` (added). Untouched: `admission_constraint`, `criterion` values, `fixed_across_all_cases`, `grids`, `quoted_sigma_km_s`, `row_ids`, `tau_km_s`, every case other than C2's binding. The claim "every criterion, threshold, gate and decision is unchanged" holds.

**2. Compare script.** `diff` shows three changed lines only: docstring line 3 (V002 → V003 name), docstring line 12 (usage example), and `PREREG_SHA256` (0024b63e… → 8e36b643…). Lines 399–401 refuse any prereg whose byte hash is not the pinned one, so the V002 prereg is refused; the `--test_allow_unpinned_prereg` flag bypasses the refusal and marks the output `test_mode: true`.

**3. Spec diffs (11 pairs).** Wave-1 C3/C4/R and templates S3/S4/Y3/Y4: exactly `label`, `physical.gamma`, `physical.common_scale_s`. Templates S2/Y2: those three plus the four `PENDING(...)` admit directory paths (F3 run → F10 run). Filled S2/Y2: label, the two physical values, the admit directories and the five admit hashes (expected rebinding). The factor-10 values in every spec equal `A2_SEED_SCAN_G2_RUN_V001/result.json candidates[2]` bitwise (`gamma_eval` 2.941048894067774e+42, `scale_s` 0.10154172268068731, factor 10.0). No numerics, grid, bracket, picard or coefficient field changed.

**4. Anchor spec.** `CALL_A2_ANCHOR_F10_C2V001.json` differs from the seed scan's NEXT spec in exactly `label`, `physical.gamma`, `physical.common_scale_s`. Its hash equals the F10 run's `inputs/call_spec.json` and the launch pin. Both anchor runs were launched at 14:35:58Z with `retries_allowed 0`, caps rss 3 GiB / wall 14400 s / output 8 GiB.

**5. Admission (filled S2/Y2).** The two admit blocks are identical. `route_a.result_sha256` = sha256 of `stages/01_route_a/attempt_000/result.json`; `route_a.identity_sha256` = sha256 of the canonical JSON of `stages/01_route_a/checkpoint/IDENTITY.json["identity"]` (the driver's `_read_checkpoint_identity` convention, galaxy_m0_forward_c2v001.py L675–677); `reference.start_sha256` / `finish_sha256` and `body.finish_sha256` match the F10 stage files; all referenced directories exist.

**6. Seal timing.** `SEAL_RECORD_V003.json` utc 15:44:15.67Z; the prereg and compare script were written in the same instant (mtimes 15:44:15.669Z). F10 `result.json` and `finish.json` were absent at the seal and are still absent at review time (run in `le1_rotation`, pass 1 done). At the seal the run was in `le1_columns_00` (15:42:42Z–15:55:04Z), as the seal record states. F3 failed at 15:42:55Z (elapsed 4017.9 s, `KeyError: 70`); V003 was sealed 80 s later.

## Corrections (text and record; no criterion is affected)

- **C1 — stale hash text in the sealed V003.** `anchor.source` still reads "physical and brackets verbatim from anchor_base_spec (fe1ad000)" and `cases[6].bound_call.verified` still reads "launch.json pins.spec sha256 = fe1ad000... = sha256 of anchor_base_spec bytes ...". Both are copied from V002; the true F10 pin is a93c95b9… (verified against the F10 launch.json and `inputs/call_spec.json`). Do not edit the sealed file; record the erratum in the next version or an addendum pinned to V003's hash.
- **C2 — the seal statement is incomplete.** It attests only that `result.json`/`finish.json` were absent. At seal time the F10 stage outputs route_a, reference, body, offset, fs_columns_00–03, fs_rotation, fs_feedback and rfs_columns_00–01 already existed (last of them finished 15:42:42Z), i.e. the FS and RFS column passes named by the deciding test of `bracket_precondition_P6` were on disk before sealing. The thresholds that judge them are unchanged from V002, which was sealed at 15:03:47Z, before the first FS column of either run started (15:25:58Z); so the deciding thresholds were fixed before any such pass existed. The one post-V002 freedom is the anchor switch. Pre-declaration evidence: the F10 spec (label "A2 seed-scan alternative", sha a93c95b9…) was pinned and launched at 14:35:58Z together with F3, before V002's seal; but the V002 prereg text names no alternative anchor. Correction: the seal record or an addendum should list the stage outputs that existed at seal time and cite the 14:35:58Z simultaneous launch as the pre-declaration evidence; future prereg versions should name the declared alternative anchor explicitly.
- **C3 — change log provenance.** `change_log_v003` states the reason for the switch (F3 FAILED at rfs column 70) by run name only. Pin it: F3 `finish.json` (status FAILED, reasons `KeyError: 70`, result_sha256 529f3954…) and the V003 anchor definition should reference the same hash.
- **C4 — cosmetic.** `kmax_compare_c2v003.py` line 12 usage example still names `kmax_compare_c2v002.py`. The `--test_allow_unpinned_prereg` flag must not appear in any production invocation; outputs produced with it carry `test_mode: true`.

## Not checked

The physics of the criterion, thresholds and gates (inherited from V002's independent check); the drivers; any running result. Timestamps are file mtimes and the run's own elapsed-seconds log converted from the 14:35:58Z launch; they are plausibility evidence, not proof of what was read.
