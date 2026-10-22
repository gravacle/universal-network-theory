# D7 recovery R3 — independent adversarial check V001

Verdict: **PASS**. No corrections are needed. Checked 2026-10-17 at about 20:10Z.

## Scope and read discipline
- **Failed R2 runs (C4R2, S4R2, Y4R2).** Read only:
  - finish.json status and reasons
  - stage listings
  - column `*_failure.json` and `*_iterations.jsonl`
  - stage stderr.txt
  - launch.json
  - the monitor log tail

  Not opened: result.json, inputs/, column_XXXX.json, *_source.npz, and the rotation/ directory, including rotation/failure.json.
- **Admitted prefixes.** For each prefix, only reference/start.json, reference/finish.json and body/finish.json were hashed.
- **Other.** No NGC3198 target was opened and nothing was launched. Writes went only to `check/`. The stop record was read only. Its sha is f8a99d55b202a5c17635c860297e7f0a599de079c7d3dc86891c25730f7c9149, which matches the value the builder reported.

## C1. Miss set and W1, re-derived (`c1_w1_rederive_r3chk.py` → `C1_W1_REDERIVE_V001.json`)
I implemented the declared W1 text myself, from `amendment_v005.d7_recovery.W1_widening_rule`.
- **Status of all three runs.**
  - finish.json: FAILED_AT_STAGE, ["stage(s) exited nonzero: ['fs_rotation']"]
  - fs_rotation stderr: "Missing complete72 successful columns"
  - Every index 0-71 is accounted for, and no column has both a success file and a failure file.
- **Miss set.** C4R2 {2,66,67,68}, S4R2 {66,67,68}, Y4R2 {2,71}. These match the builder exactly.
  - Every failure is ValueError MASS_ENTHALPY_NOT_BRACKETED, so there is no "no bracket source" case.
  - The other R2 runs (C2R2/S2R2/Y2R2/C3R2/S3R2/Y3R2/RR2) have no `*_failure.json` in any stage.
- **Evidence.** Each iterations file holds exactly the two endpoints of the entry in the launched filled R2 spec. All five columns had no override key, so the entry is the template [1.5125e8, 3.025e8].
  - Every residual pair is r(lo) < 0 and r(hi) < 0, meaning the root is above hi.
  - The residual values and the failure and iterations shas equal the builder's evidence file.
- **W1.** hi = 3.025e8 < 1.05·t_hi, so this is step A: hi becomes 3.17625e8 and lo is kept.
  - Columns widened by R1/R2 are {3-9, 45-50}. None of the missed columns is in that set, so there is no step B and no BRACKET_RECOVERY_EXHAUSTED.
- **Cross-case.** Columns 2 (C4R2, Y4R2) and 66/67/68 (C4R2, S4R2) have the same "from" entry and the same result in every case. There is no conflict.
- **Expected R3** = R2 fs table plus {2,66,67,68,71: [1.5125e8, 3.17625e8]}. This is **equal** to the builder's R3.

## C2. R3 contents and the sealed validator (`c2_r3_validator_r3chk.py` → `C2_R3_VALIDATOR_V001.json`)
- **Pins.** compare is 49404bc4…, prereg is dbddc02c…, and R3 is 7946b857….
- **Acceptance.** Both the main() file-schema check and `validate_recovery(pre, R3)` return [].
- **Against R2.**
  - Only `fs_absolute_overrides` changed.
  - Added keys are exactly 2, 66, 67, 68, 71. Nothing was removed or changed.
  - The anchor, R1 and R2 are each contained entry by entry.
- **Key lint and metadata.** The key lint `0|[1-9][0-9]*` passes.
  - widened_entries for the new keys are correct.
  - R2 widened_entries are carried over verbatim.
  - The evidence pointer shas match the file bytes.
- **Tampers.** I wrote five tampered copies, all different from the builder's two. The validator refused every one:
  - T1 removes entry 46 → "removed" and "R1 entry … not contained"
  - T2 changes rfs_factors → "non-override key rfs_factors changed"
  - T3 narrows rfs[71] → "narrowed or moved"
  - T4 sets new fs[71] narrower than the template → "does not contain its template"
  - T5 adds an extra rule key → schema refusal

## C3. Spec diffs against R2 counterparts (`c3_spec_diffs_r3chk.py` → `C3_SPEC_DIFFS_V001.json`)
- **Diffs.** I deep-diffed all 10 specs against their R2 counterparts. The R2 filled specs are the counterparts for C4/S4/Y4. Each diff is exactly `/label` changed plus added `fs_absolute_overrides/{2,66,67,68,71}`.
- **Brackets.** `numerics.brackets` equals the R3 block, and the admit block is unchanged from R2.
- **Launched specs.** The filled R2 C4/S4/Y4 specs are byte-identical to the specs the failed runs launched: the path and sha are in their launch.json.
- **Admit hashes.** For F10, C3 V005, R V005 and C4 V005, I hashed the admit start/finish shas from bytes and they all match. route_a identity and result shas were not re-hashed, because that would mean reading result.json. The v005 dry-run reports stage admission with no refusals.
- **Key lint.** Passes on every spec.
- **Spec shas.** These equal the builder's table: C2R3 afca6330…, S2R3 40194522…, Y2R3 e8a12f08…, C3R3 0b5732f9…, S3R3 32b0943f…, Y3R3 4fec450b…, RR3 2ab609b6…, C4R3 3ea94efe…, S4R3 e047bcd4…, Y4R3 754c938b….

## C4. Dry-runs (`c4_dryrun_eval_r3chk.py` → `C4_DRYRUN_EVAL_V001.json`)
- **Reruns.** I reran two dry-runs under the pinned drivers at nice 10, in `dryrun_chk_r3/`:
  - Y2R3 on v001 (75b0c08a…)
  - C4R3 on v005 (2aef51c4…)

  Both exited 0 with empty stderr and 9 stages.
- **fs tables.** For both reruns, the fs table built from `fs_controls_*.json` covers 72 columns and equals R3 and the builder's tables.
- **Inputs and reports.** All simulated inputs are equal to the builder's once paths are normalized. The only report differences are shas of path-bearing files: pending probes, the manifest argv sha, and the identity probe shas.
- **C4R3 v005 checks.**
  - binding_blockers, unexplained_refusals, refusals_beyond_pending_inputs and stage_admission_refused are all [].
  - The only remaining refusal is PRODUCED_BY_THIS_CALL custody.offset_finish_sha256.
  - pin_problems and scipy_imports are both [].
- **Builder dry-runs.** I evaluated all 10 independently and all pass:
  - fs table equals R3 with no duplicates
  - against the R2 dry-run, the differing columns are exactly [2,66,67,68,71]
  - spec and driver shas match, 9 stages, no pin or scipy problems, empty stderr
  - for v005, 0 blockers and 0 unexplained or beyond-pending refusals

## C5. Launch and hashes (`c5_launch_hashes_r3chk.py` → `C5_LAUNCH_HASHES_V001.json`)
- **argv and caps.** In LAUNCH_R3, argv and caps equal LAUNCH_R2 apart from the R2→R3 name changes. C4/S4/Y4 follow the C3R3 shape: v005, wall 28800 s.
- **Pins and binding.**
  - Spec shas equal the file bytes. The R3, prereg and monitor pins are ok.
  - templates_pending is {}.
  - The comparison binding covers all 10 cases, and the flag points at R3.
- **HASHES.txt.** All 146 lines verify from bytes, and no file outside `check/` is unlisted.
- **File shas.** LAUNCH_R3.json is 17272504…, LAUNCH_R3.md is dbbf131c… and HASHES.txt is 2cceebf8…. All three equal the builder's values.

## Notes (none needs a correction)
1. **The R3 runs are already running, launched by root.** All ten were launched at 2026-10-17T20:05:12Z, after LAUNCH_R3, which is dated 20:03:29Z. This check therefore ran after launch. The builder's "none exists yet" was true when it built.
   - Each launch.json pins the spec path and sha checked here, and the spec bytes have not changed since. Driver, monitor and caps all match.
   - At 20:10Z all ten were in 01_offset, with no failures and no finish.json.
2. **The sealed validator only enforces containment of the anchor and R1.** It does not check that R(n) contains R(n-1). As a probe, I reverted R2 entry 3 to the template and the validator accepted it. This is the behaviour the prereg declares ("does not contain every R1 entry"). C2 checks independently that R3 contains R2. Later invocations need the same checker-side check.
