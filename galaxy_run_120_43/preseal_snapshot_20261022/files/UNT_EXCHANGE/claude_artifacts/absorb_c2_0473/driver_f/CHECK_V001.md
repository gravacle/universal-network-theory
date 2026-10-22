# CHECK_V001: driver_f (galaxy_m0_forward_c2v003c, RD1 F1-F4)

Independent checker, Claude2 lane. I did not write anything in driver_f except this file. My scripts and outputs are in `absorb_c2_0473/check_driver_f/`.

## Verdict: PASS_WITH_CORRECTIONS

- All four RD1 fixes are correct against the stage code and the saved run.
- No estimate is repaired. The diff touches no numerics.
- The corrections listed below are wording fixes plus one low-severity hardening. None of them blocks.

## Custody (from bytes)

- **HASHES_V003C.txt:** all 25 entries verify.
- **Reviewed driver:** `galaxy_m0_forward_c2v003c.py`, sha `ed326130…bfdf2`.
- **Base driver:** v003b, sha `7ce59e05…2a27`.
- **DIFF_V003B_V003C.txt** is byte-identical to a fresh `diff -u` of v003b against v003c, excluding the header timestamps.
- **What the hunks contain:** F1, F2, F3, F4 and docstrings only. No equation, tolerance, stage argv or stage order is changed.
- **Author suite re-run:** I ran `tests_c2v003c.py` into `check_driver_f/rerun_their_tests/`. It passes 8/8, and its stdout is byte-identical to `RUN_V002.stdout.txt` (`1d7f4301…`).

## Independent re-derivation (`check_f_c2v001.py` `52b4c536…` → `out_v001/CHECK_RESULTS.json` `d13d4ff9…`)

The script runs single-thread with numpy only, in 1.35 s, peaking at 0.32 GB RSS. It executes no stage and uses no Popen. It opens no NGC3198 data and no target data.

| Item | Own derivation | Result |
|---|---|---|
| **F1: JSON path** | I traced the path from the stage code: worker v002 L106 `result` → binding v002 L116 `result` → prediction v005 L57/L225 `source_fixed_point` → adapter L74, which returns the solver result unchanged → solver L104-109 `checkpoint` = `cm.finish`, whose `outcome` is at ckpt L603. The failure keys `type/message/iteration/column_index/stage` are at solver L171-174. | The driver's path `result.result.source_fixed_point.{checkpoint.outcome, history[-1].iteration, failure}` is correct. |
| **F1: saved attempt** (`79855e78…`) | My own walk gives: outcome `CONVERGED_FINITE_FIXED_POINT`; history `[0..4]`; `predictions_available` True; checkpoint `attempts/*.end.json` outcome is CONVERGED; the result's embedded checkpoint identity is `98816902…` = IDENTITY. | The driver classifies it CONVERGED at iteration 4 and passes it. **TESTED-POSITIVE.** |
| **F1: synthetic returns shaped like the real solver** | I built 8 cases: HI failure in iterations 0, 2 and 4; budget exhausted (8); convergence at iterations 0, 3, 4 and 5. | All 8 match my reference rule. No fixed point → `RouteANoFixedPoint`. Convergence at k≠4 → BLOCKED naming k. Convergence at 4 → proceeds. **TESTED-POSITIVE.** |
| **F1: status mapping** | MRO: `RouteANoFixedPoint` derives from RuntimeError and is not a subclass of Blocked, StageFailed or Refusal. | In `cmd_run`, its handler sits after `Blocked` and before `StageFailed`, so the distinct status is reached. Exit code 3 is shared with BLOCKED and FAILED, which is harmless: the monitor reads `finish.status`. |
| **F4: saved IDENTITY** | Decoded caller `physical_parameters` has `mubar` (3, f8) and `Cbar` (3×3, f8). Both are `array_equal` to the default `background_mu`/`background_C`, and the digests `fourier_arguments.mubar/Cbar` match. Offset v003 L66 and L70-72 make exactly these checks. | The new custody check mirrors offset. **TESTED-POSITIVE.** |
| **F4: real checkpoint × variant coefficients** | Same grid, with a one-ulp change to mu or to C. | v003b: OK, which is the defect. v003c: BLOCKED `ROUTE_A_BACKGROUND_MISMATCH`. A byte-identical copy: OK in both. The saved checkpoint passes v003c custody with identity `98816902f71d17f9…`. **TESTED-POSITIVE.** |
| **F3: exhaustive sweep** | I tested every Unicode code point in three positions (`c`, `1c`, `c1`), against the lookup set `{str(i)}`. | 0 false accepts and 0 false rejects. The 798 non-ASCII `isdigit` code points are now refused. All 12 shipped REPRO_RULE_FULL keys are canonical. **TESTED-POSITIVE.** |
| **F2: scanner coverage** | Over 76 v003c run-mode requests: 0 flagged. The only non-numeric, non-hex, non-absolute argv values are `PENDING_SHA256(…)` tokens, which are no-op-Popen artifacts and are skipped by design. The only plain-string globals containing `/` are `OFFSET_SHA` PENDING tokens. A simulate Ctx with a relative outdir is REFUSED at `route_a` before any record or file is written. | **TESTED-POSITIVE.** |

## Corrections and defects

None of these is blocking. Most severe first.

1. **D1 (should-fix, low): F1 makes the admitted attempt decision-relevant, but the attempt is still not tied to the checkpoint (RD1 F6).**
   - **Failure scenario:** `admit.route_a` pairs a failed attempt with a good checkpoint from another run. The call ends `ROUTE_A_NO_FIXED_POINT`, which mislabels a tooling or spec error as a model outcome. That is the mislabel F1 exists to prevent.
   - **Fix:** require `source_fixed_point.checkpoint.identity_sha256 == IDENTITY.identity_sha256`. The field exists in the saved result and equals `98816902…`. Optionally also require that the `attempt` token matches an `attempts/<token>.end.json`.
   - Computed route A is not affected, because the attempt and checkpoint come from the same run.
2. **D2 (wording): the F1 docstring and class comments say worker v002 writes `result.json` with exit 0 "for every solver outcome". That holds only for returned outcomes.**
   - Some failures raise instead, and those propagate to worker `failure.json` with a nonzero exit, ending `FAILED_AT_STAGE`, not `ROUTE_A_NO_FIXED_POINT`. These are:
     - solver `ValueError`s outside the column try: nonfinite gas source, residual, bound or relaxed gas (L190-199, L215);
     - prediction v005 errors after convergence: nonreal query metric (L81), query HI column (L93-99), steps and weights (L109-117).
   - **Status:** UNTESTED. The deciding test is a toy solver or prediction raising `ValueError` through the real worker path. Pre-existing behaviour, outside RD1 F1, but it should be stated, not covered by "every".
3. **D3 (wording): the `cmd_run` comment says abspath keeps an absolute outdir "byte-for-byte".**
   - `os.path.abspath` normalizes `.`, `..`, `//` and trailing `/` lexically. Only symlinks are left unresolved.
   - Edge case: `/symlink/../x` is redirected lexically. It has no effect on any current spec.
4. **D4 (note): classification asymmetry.**
   - `converged_finite_fixed_point` False together with outcome token CONVERGED is classified `ROUTE_A_NO_FIXED_POINT`, not `INCONSISTENT`.
   - The real solver cannot produce this, because the flag and token are set in the same return (L170, L210, L216). It is only a cross-check gap.
5. **D5 (scope note): RD1 F1 correction items 4 and 5 are only partly closed. This is outside the driver.**
   - `route_a_outcome` is written to `result.json`.
   - Campaign `_record_from_receipt` copies only valid/status/speeds/reasons. The campaign record therefore carries `driver_status` `ROUTE_A_NO_FIXED_POINT` and the reason text, but no structured `route_a_outcome` or `converged_iteration`.
   - It still counts the call in `n_failed`.
   - The calibration-protocol treatment of BLOCKED versus no-fixed-point points is not addressed.
   - The monitor and campaign need no path fix: neither sets a Popen cwd (monitor L147, campaign L153), so the driver's abspath resolves against the same cwd they use.

No sign-convention errors, no misread JSON paths, and no PSD, sign or estimate repair were found. Nothing in the diff makes a causal claim beyond what the stage code supports, apart from the wording in D2.

## Not tested

- No real route-A run or stage was executed, as the rules require.
- F1 failure outcomes are tested on synthetic returns shaped like the real stage code. The only real outcome available is the saved CONVERGED-at-4 attempt.
- D2 is code-read only.
