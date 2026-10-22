# D7 recovery R2: independent adversarial check V001

VERDICT: **PASS_WITH_CORRECTIONS**. All R2 artifacts pass. One correction applies to the builder's narrative only: the C2R/S2R/Y2R status. No artifact needs to change.

Checked on 2026-10-17. Pins were checked from bytes: prereg dbddc02c, compare 49404bc4, R1 b3938db2, R2 ff7cf806, driver v001 75b0c08a, driver v005 2aef51c4, monitor ba031c23.

Read scope:
- For the D7R1 runs and the prefix runs I read only stage listings, `*_failure.json`, `*_iterations.jsonl`, finish.json (status, reasons and sha), launch.json, monitor-log tails and stderr.txt.
- I did not open any result.json, request.json, rotation or speed data, or NGC3198 target.
- The checker launched nothing and wrote nothing outside `check/`.

## Re-derivations

The checker scripts are in `check/`; each wrote the output named alongside it.

| # | What | Result |
|---|---|---|
| C1 | Miss set, built from stage listings plus the failure and iteration files (`c1_scan_runs_c2chk.py` -> `C1_RUN_SCAN_V001.json`) | C3R 3,4,46,47,48,49; S3 46,47,48,49; Y3 3,4,46,47,48,49. In every run, ok ∪ fail covers 0-71 with no overlap and no orphan iteration files. Every miss is MASS_ENTHALPY_NOT_BRACKETED with exactly 2 iterations. All three runs are FAILED_AT_STAGE at fs_rotation. |
| C2 | My own W1, written from the prereg `W1_widening_rule` text without the builder's code (`c2_w1_r2_validator_c2chk.py` -> `C2_W1_R2_VALIDATOR_V001.json`) | **3,4:** entry used = fs template [1.5125e8, 3.025e8], confirmed against the iteration Hc values and the launched spec. r<0 at both ends, and hi < 1.05·template_hi, so hi -> 3.17625e8 (step A). **46-49:** entry used = R1 [3.025e8, 3.17625e8]. r>0 at both ends, and lo > template_lo, so lo -> 1.5125e8 (step A). The cases agree on every column, so no conflict or hull is needed. My R2 is canonically equal to the builder's R2. Only `fs_absolute_overrides` changes. The launched D7R1 specs' brackets equal R1. |
| C2 | Sealed validator: `validate_recovery` loaded from kmax_compare_c2v005.py (49404bc4) | R2 -> `[]`, R1 -> `[]`, and main()'s file-schema check passes. Five mutations are all refused: R1 entry 5 reverted, new entry 3 not containing the template, rfs_factors changed, anchor entry 46 removed, anchor entry 46 narrowed. The validator is live. |
| C2 | Exhaustion | None of the entries R1 widened (5-9, 45, 50) missed again, so BRACKET_RECOVERY_EXHAUSTED does not apply. On the task's "step B on an R1 entry" wording: for 46-49, lo/2 = 1.5125e8, the same value step A gives, so the numbers do not depend on the reading. |
| C3 | Spec deep-diffs of all 10 R2 specs against their R1 counterparts (`c3_spec_diffs_c2chk.py` -> `C3_SPEC_DIFFS_V001.json`) | Every spec differs only in `/label` and fs entries 3, 4 and 46-49. RR2 also differs in `/admit/*`: the R1 RR template had PENDING placeholders. C4R2/S4R2/Y4R2 keep the PENDING admits. Every spec's brackets equal R2, all picard passes are 6, and override-key lint finds 0 bad keys. |
| C4 | All 7 filled-spec dry-runs rerun by the checker under nice -n 10 with the pinned drivers (`dry-run --spec --report-dir`; `c4_dryrun_eval_c2chk.py` -> `C4_DRYRUN_EVAL_V001.json`) | All 7 exit 0 with empty stderr. Report spec and driver shas match. pin_problems and scipy_imports are empty. The fs table covers 0-71 and equals R2. Against the R1 dry-runs, only columns 3,4,46-49 differ. Stages planned go from 11 to 9. **v005 cases:** binding_blockers, unexplained, beyond-pending and stage_admission_refused are all empty. The only remaining refusal is PRODUCED_BY_THIS_CALL custody.offset_finish_sha256. My stdout is byte-identical to the builder's, and the summaries are equal once paths are ignored. |
| C5 | LAUNCH_R2.json and HASHES (`c5_launch_hashes_c2chk.py` -> `C5_LAUNCH_HASHES_V001.json`) | 7 argv lines. Each has the correct python, `-I -B`, monitor, driver and driver sha, spec sha, outdir `KMAX_A2F10_<NAME>_D7R2_RUN_V001` and receipt. Caps are v001 21600 and v005 28800, with rss 3221225472, output 17179869184 and poll 2.0. For the six R1-rerun cases these equal the R1 launch.json caps. The shell strings round-trip to the argv. The comparison flag points to the R2 path. HASHES.txt and HASHES_ADDENDUM.txt: 106 entries, all match their bytes. |
| C6 | Builder evidence file against the checker scan (`c6_evidence_agree_c2chk.py` -> `C6_EVIDENCE_AGREE_V001.json`) | All 16 missed entries agree on failure and iteration hashes, residuals, entry used, and W1 result and step. Finish status, reasons and sha agree, as do the spec shas. |

## Findings

**N1 — correction (narrative only).** The builder said C2R, S2R and Y2R are "still running on R1" and that stopping them is root's call. That is wrong as of the check:
- All three finish.json files read `COMPLETED`. They finished at 18:43-18:44Z, before the R2 build at 18:45Z.
- All 72 columns completed in each of the fs, rfs, le1, le2 and le3 passes, with no failure files.
- Effects:
  - No R2 entry is missing.
  - Per D7 step 4 and later_invocations, these cases are still superseded by C2R2, S2R2 and Y2R2 for the comparison.
  - There is nothing for root to stop.

**N2 — note.** RR has no R1 attempt. LAUNCH_R2 uses the task's literal v005 caps (rss 3 GiB). The R V005 prefix run itself was launched with rss_cap 4294967296. Observed v005 D7R1 peaks are at most 1.834e9 B, which leaves about 1.75x headroom. This is not a defect.

**N3 — note.** Root launched all seven R2 calls at 18:51:39Z, during this check. Each launch.json's spec sha, driver sha and caps equal LAUNCH_R2. The outdirs were absent at build time, as the builder stated.

**N4 — note, completeness.** The first C3 V005 attempt ran on the anchor block. It missed 3,4,6-9,45-50, with the same residuals as C3R on 3,4 and 46-49. Every one of those columns is covered by R1 ∪ R2, so no evidenced widening is left out.

**N5 — note, open.** The R V005 prefix run is still on fs columns with the anchor block and has no failure files so far. RR2 runs on R2. Any later column miss in any case, including RR2, goes to R3 under later_invocations.
