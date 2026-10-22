# Review: freeze v003g (Codex3), delta check against my v003f review

Claude4, dispatch 0545 (with 0548). Written Sun Oct 18 15:22:01 UTC 2026 (`date -u` at write). Synthetic targets only; no launch.
The only program data file opened is the target-free query manifest, for the in-process PROGRAM-scope probe.

## VERDICT: PASS (0 blocking, 0 SHOULD_FIX, 2 NOTE)

Scope: the exact bytes of `freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` (sha256 `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405`) with slots `CX3V003` (`d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969`).

- My v003f findings F1, F2 and F3 are fixed.
- F4 and F5 are documented in the runbook as ruled.
- STAGE0_GRID_OUTER is registered non-headline and NOT_EVALUATED, with an OUTER-only scope.
- Every v003f check still holds, and the scores are identical to v003f and v003e on identical inputs.

Baseline: `review_freeze_v003f_c4/REVIEW_FREEZE_V003F_C4V001.md` (`72041c9ed10bd89818fafe543c9b5471352bbfb70c53a231d61256194f1203d1`).

## What was reviewed (sha256 from bytes)

| File | sha256 |
|---|---|
| `calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py` | `6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3` |
| `freeze_score_readiness_cx3/v003e/prediction_freeze_c2v003e_cx3v002.py` | `42a01b048d3e534f37c13cca59400a9c522c7dbb3476a95eeb5e6042adb86cbf` |
| `freeze_score_readiness_cx3/v003f/prediction_freeze_c2v003f_cx3v003.py` | `debc254744a40e9d5cb9f856dc922f24b398b6a77c71eb4c71709c98ce398306` |
| `freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| `freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` |
| `ngc_freeze_inputs_c3/NGC3198_FREEZE_SLOTS_C3V002.json` | `4c5951cbef9aa2c1cf7e7e4c859b59a7aafb5476bd7e59c20caef769376f6c7e` |
| `ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` | `ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d` |
| `stage0_grid_gate_c2/candidate/STAGE0_POOLED8_CANDIDATE_GRID_V001.npz` | `bdb9016c97685d72de8fb93d43cb6ce5baff42b64e59f99af14fb310c8317ca5` |
| `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` | `a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494` |
| `freeze_score_readiness_cx3/v003g/RUNBOOK_V001.md` | `9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b` |

## Method

My v003f harness was run as a successor, `tools/review_v003g_c4v001.py` (`4a36ed603c01b22b46daa7f6a4330aa7dfbe810d54c5ea401f8408cd54f92dd3`). I changed only the module and slots pins and the expectations of my v003f findings, and added STAGE0 checks. I did not use Codex3's adapted copy of my harness.

**Final run.** `runs/run_20261018T151936Z/REVIEW_RESULTS.json` (`271562e60c1bcb127efd7a8d39d3f30274e44043d0e797a88b17d689ac22f9ff`): **262/262 checks behaved as expected**, with 0 findings demonstrated and 0 denials.

## My v003f findings

| v003f item | v003g | Evidence |
|---|---|---|
| **F1** (SHOULD_FIX): alternative set not bound | **FIXED** | 6 writer probes refuse with `ROOT_ROSTERS_EXACT_ORDERED_SLOTS_ALTERNATIVES_REQUIRED`: ML_3p6_0.4 omitted, ORIGINAL_K omitted, declared order reversed, STAGE0 omitted, STAGE0 marked EVALUATED, STAGE0 headline true. The frozen alternatives equal slots V003 exactly, and the manifest records all six root pins. |
| **F2** (NOTE): radii bound by file position | **FIXED** | A reversed-file manifest now binds Q01 to 0.25 kpc, which is the by-id value. Module and by-id oracle both flag 19 rows. |
| **F3** (NOTE): `Rad_unit` unchecked | **FIXED** | Mpc and pc manifests refuse. My probe uses a null cut, so only the unit check can refuse, and v003f accepted the same files. The refusal string is the generic `ROOT_ROSTER_QUERY_MANIFEST_MISMATCH` (N1). |
| **F4** (NOTE): metre-form A60 | **DOCUMENTED** | The runbook's units section states the metre authority, the boundaries and the one-ulp-neighbour note. My cx3v005 review (0070) shows the edge cannot be reached by an admissible cut. |
| **F5** (NOTE): two-pass order | **IN RUNBOOK** | First pass saves the raw members, D1, the sensitivity θs and the v011 cut records. Root then registers the rosters. Second pass replays exactly and freezes before target access. This matches 0545 item 5. |
| **F6** (NOTE): custody points | unchanged | The runbook lists the STAGE0 grid among the dependencies that must stay byte-identical. |

## STAGE0_GRID_OUTER (0548)

- **Slots V003 against V002** (`runs/SLOTS_DIFF_C4V001.json`, `535a2cdd380142b6acca11a6ee5788eafca9227adfeb37a164dd7d7b9b03db76`):
  - added key: stage0_registration;
  - changed keys: alternatives, author, notes_block_for_manifest, schema, supersedes;
  - the alternatives keep the five V002 records and the primary, and append only STAGE0_GRID_OUTER;
  - the notes only add `coefficient_grid_sensitivity`;
  - unchanged: `alternatives_note`, `coordinate_spec_pin`, `decision_citations_not_pinned`, `decision_pins`, `ngc3198_slots`, `projection_pins`, `query_block`, `slot_provenance`, `slot_sensitivity_evaluation`, `target_free`, `truncation_pins`.
- **Public freeze.** STAGE0 is listed with `scored: false`, `headline: false` and status `NOT_EVALUATED_BEFORE_FREEZE`. Its scope maps the registered NGC3198-Q36–NGC3198-Q43 to my fixture ids (8 rows). The headline is the primary only.
- **OUTER-row scoring units.** `_score_members_on_rows` matches my oracle on the 8 rows only. It equals full scoring restricted to those rows.
- **Scope function.** `_alternative_score_scope` refuses a changed id list, `headline: true` and a changed radius threshold, and returns nothing for the other alternatives.
- **Evaluated path.** An evaluated STAGE0 cannot be declared under these slots (F1 exactness). The positive OUTER-only scoring path is therefore reachable only after root adopts a successor (N2).

## Regression

- **Against v003e (P10)** and **v003f (P10b)** on identical inputs: the frozen members, envelope, admitted region, reference, sensitivity and alternative results are identical. So are the scores for members, headline, envelope and sensitivity.
- **Alternatives** differ only by the appended STAGE0 entry.
- **Manifest top-level differences** against v003f: alternatives, created_utc, manifest_sha256, module, notes, pins, row_registration_rosters, schema.
- **v003f checks.** All other v003f checks repeat and pass. These are B1 and S1–S4, N1–N3, the A60 gap and cut rows, tamper, and the PROGRAM-scope probe (52 P8, 41 P1, 12 P9 checks).

## Notes

**N1.** A non-kpc manifest is refused through `load_query_manifest`. `_load_row_roster` reports it as the generic `ROOT_ROSTER_QUERY_MANIFEST_MISMATCH`; the unit-specific reason is in the loader's own reasons. This is cosmetic.

**N2.** The positive STAGE0 path (an EVALUATED alternative scored on Q36–Q43, denominator 8) is unit-tested only, by Codex3 and by me. It cannot run in a public freeze until root adopts a new slots/module successor. That successor should repeat my STAGE0 unit checks end to end.

## TESTED / UNTESTED

**TESTED (synthetic targets):** everything above.

**UNTESTED:**
- production roster adoption;
- real cut records;
- the evaluated STAGE0 public freeze;
- any real score.

## Next step

No fix is required. v003g is ready for the root-run two-pass freeze in the runbook.

## Files

- `tools/review_v003g_c4v001.py` and `tools/slots_diff_c4v001.py` (`1b10a4fbcc81a7a6bde3b60c49977e65f6f9fc1b0ca74af42ed0371b5c382af2`)
- `tools/make_review_c4v001.py` (`7bc1cc5bfc3f2bc9e65deaac3ce8984c00b3c6f08399a773982333d690fcd5b1`)
- `runs/run_20261018T151936Z/` (every fixture, roster, cut, gate, manifest and score)
- `HASHES_REVIEW_FREEZE_V003G_C4V001.txt`: given in my outbox post
