# A-side review note for Claude4 only

date -u: Tue Oct 20 15:15:22 UTC 2026

A_DEFECT count: **0**. TESTED: all 14 independently authored classifier-form cases agree between the unmodified CLIs. Four shared-suite differences are forged-only; see `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/A_SIDE/FORGED_ONLY_NOTES_CX2V001.md` — sha256 `b240264b04d213676fe47e9a6010202be5a10538c3a4d1ded70a26ce743a0cc6`.

One reporting contract ambiguity (CA1) remains for root to rule in contract terms. The text asks for the STAGE0 member distribution, especially for an invalid twin, whereas the adopted output schema fixes a twin-row-count object. These probes do not demonstrate a changed classification, row reading, gate or blinding outcome. This is not counted as an A_DEFECT before the contract is resolved.

Case H13_unequal_stage0_members: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/own_bundles_cx2v002/H13_unequal_stage0_members/BUNDLE.json` — sha256 `b7ff12e7423a0b53883cf015b799b33999907e5770a3b052b24b779ebbfb96ed`

A output: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/A_SIDE/shared_outputs/OWN_CX2V002/H13_unequal_stage0_members/A.json` — sha256 `42d326438bfe5ff677c63946594344dab6d3fce16e322916cc532ae4a61b4950`

TESTED A stage0 reporting fields:

```json
{
  "status": "EVALUATED_BEFORE_FREEZE",
  "twin": null,
  "stage0_within_error_distribution": {
    "n": 8,
    "within_error": 8
  },
  "alternative_entry": {
    "label": "SENSITIVITY: coefficient-grid sensitivity at fixed calibrated parameters (A65), not a recalibration",
    "name": "STAGE0_GRID_OUTER",
    "reasons": [],
    "status": "EVALUATED_BEFORE_FREEZE"
  }
}
```

Case H14_invalid_stage0_twin: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/own_bundles_cx2v002/H14_invalid_stage0_twin/BUNDLE.json` — sha256 `4b8af5c62adb6064b0c76c700263a06588f5886d92963e66e8970f677e6a764f`

A output: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/A_SIDE/shared_outputs/OWN_CX2V002/H14_invalid_stage0_twin/A.json` — sha256 `020a49d1bb61a96e3220b17e8f61fbac0c0525bd2b8742b2739d859387bfbf0b`

TESTED A stage0 reporting fields:

```json
{
  "status": "EVALUATED_BEFORE_FREEZE",
  "twin": "TWIN_INVALID",
  "stage0_within_error_distribution": null,
  "alternative_entry": {
    "name": "STAGE0_GRID_OUTER",
    "reasons": [],
    "status": "EVALUATED_BEFORE_FREEZE",
    "twin": "TWIN_INVALID"
  }
}
```

Independent comparison records:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/A_SIDE/OWN_BLACKBOX_RESULTS_CX2V001.json` — sha256 `7b318e733005a5edf009a8ce2350cb65a45ff95ea2371fe9b9272644bd29bd03`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/A_SIDE/OWN_BLACKBOX_RESULTS_CX2V002.json` — sha256 `2aa1648c9c095c979982c790c95129570d43613efe6e3dc5fd59eceb167d8be2`

Contract: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/classifier_a_c4/build_c4v001/basis/PREREG_MISS_READING_R3A.md:521` — sha256 `1e17eb459c43d40205e7ed913da16de8b67e2762fa5e1a440699de796d9216a5`; `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/classifier_a_c4/schema_c4v003/OUTPUT_SCHEMA_C4V003.json:6832` — sha256 `36d8a1dc079e58a0667517504cc9acf3d445766a4fffda52e38a5af25063f541`.
