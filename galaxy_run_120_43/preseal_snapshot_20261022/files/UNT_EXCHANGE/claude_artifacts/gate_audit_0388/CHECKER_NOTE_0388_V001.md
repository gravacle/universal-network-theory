# CHECKER_NOTE_0388_V001

Checker: Claude helper, separate from the author.
Under review: GATE_AUDIT_0388_V001.md, sha256 818d015da3fa19dc3202fb552367d6e6d70479223e9bb497e73fad6875d7eeca (verified).

## Verdict: CONFIRMED_WITH_CORRECTIONS

Every quoted stale statement exists at its cited path and line or key. All ASM lines at or after 754 sit at the cited line +13 in the current bytes, which confirms the author's shift note. Every cited later decision exists.

- **Confirmed without change:** rows 1, 2, 4, 5, 6, 7, 9, 11, 12 and 13.
- **Needs correction:** rows 3, 8, 10, 14, 15 and 16.
- **The four NEEDS-CODEX rows (4, 9, 13, 15):** all are justified, and none pre-empts a Codex decision.
- **No physics, calibration or state decision is made anywhere in the audit.**

## Per-row discrepancies

### Row 3 (COMPLETED): too broad
V030 `next_actions[1]` reads: "Review#### uncertainty join and#### corrected literal geometry extractor; root-only metadata extraction after code/review, no physical source adoption by parsing."

- COMPLETED is supported only for the extractor and ordinal-contract clause. Evidence: V002 `contract_status` "PASS_SOURCE_SPECIFIC_ORDINAL_CONTRACT_…", and ASM L1127 and L1139 (both current numbering).
- The uncertainty-join clause is not shown complete. V030 `query_metadata_v029/uncertainty_model` is still "OPEN", and ASM L1127 says no likelihood is adopted.
- The omitted phrase "no physical source adoption by parsing" supports row 4.

### Row 8 (SUPERSEDED): partly overstated
The field `working_bridges/common_clock_and_physical_units` also covers physical units.

- Only the microscopic clock/light-derivation prerequisite is superseded (ASM L1095 and L1139; CI L114).
- Physical units and normalization remain a requirement within the run (CI L116 "each dimensional prediction needs … normalization"; DIR L9; row 7).
- Correction: split the row into SUPERSEDED (the microscopic prerequisite) and WITHIN-CAMPAIGN (the units).

### Row 10 (SUPERSEDED): partial quote
The full V030 `readiness_gates_v014/G3` reads: "Independent universal constants and galaxy inputs, source/state uncertainty and honest object-level exposure; frozen predictions on separated test data. OPEN."

- The first three clauses are kept as requirements within the run:
  - CI L114: shared constants are "independent of the predicted velocities, counted and sensitivity-tested".
  - ASM L1136 carries the uncertainty alternatives.
  - ASM L1129: "NGC#### is development-exposed, not blind".
- The specific claim is confirmed: the blind or separated-roster prerequisite is superseded (CI L114; ASM L1129, L1137) while freeze-before-scoring is kept (CI L114; ASM L1137; V030 `freeze_clarification`).
- V030 `empirical_roles_route_note` still permits designated calibration galaxies that are separate from the prediction galaxies. That option is not superseded.

### Row 14 (SUPERSEDED): overstated; no conflict
CI L108 itself requires "the same state" for every prediction in a family member. ASM L1147 ("an independently admissible collective state") was left unchanged by Codex after the staging paragraph, and it reads consistently as one state per member.

This is a reframing, not a supersession. Correction: change the disposition to "no conflict, reading clarified".

### Row 15 (NEEDS CODEX): disposition stands; evidence missing
- **Uncited source.** CI L116, mirrored in DIR L113, says: "Previously explicit cosmological-comparison staging is not silently replaced by this gate audit." The row does not cite it.
- **Principal-settled sequence.** CI L81 calls the DE-before-120/43 order a sequence that "the principal has now settled". Moving it therefore needs Codex to present the concrete relation, and possibly to ask the principal (CI L116). Codex cannot place it unilaterally.

### Row 16 (SUPERSEDED): two mischaracterizations
1. V030 `empirical_roles/legacy120` is not stale. It already says to replace the partition with a sized manifest, with "no inherited job count", which agrees with CI L112/L114 and ASM L1137. The stale item is `full_120_43_deferred` true.
2. CI L79 is more than a label. It carries a principal-level gate that no row lists: "Essential mechanism work belongs before the substantial 120/43 campaign … do not run a knowingly inadequate model." It belongs with row 15 as NEEDS CODEX, to decide whether CI L112 ("model terms are largely identified … We don't need to stop") discharges it.

### Minor points
- **Row 13 wording.** "the one state item that must come before scoring" is inaccurate. CI L108 also freezes the constraints, the map, the calibration protocol and the joint rule before comparison. The documentary suggestion for the field does not pre-empt anything.
- **Header claim** that "V030 predates every … decision cited". V030 `created_utc` is 2026-10-15T16:37:10Z. I verified the claim against the timestamped items:
  - the principal paragraphs, recorded at 22:58 and 23:09 UTC (DIR L105, L115);
  - DIR L3 (22:35 UTC) and DIR L23 (21:38 UTC).

  DIR L9, L63 and L95 carry no timestamp, so the claim cannot be checked for them.

## Missing-inputs section and covariance
- Every listed entry is recorded in the sources as missing, OPEN, null, unclassified or "not zero":
  - ASM L1121–1127;
  - CI L75 and L116;
  - V030 `uncertainty_model`, `prediction_relevant_uncertainty_region`, `calibration_observation_model`, `independent_shared_parameter_region`, `lensing_validation_source`, `cosmological_validation_source`, and the `DDO154_distance_datum` phrase;
  - V002 `status`.
- No values are printed, and the `S1_above_sampled_range` count is not reproduced.
- **Covariance claim: confirmed.**
  - CI has 0 hits for "covarian".
  - The DIR (5), ASM (11) and V030 (7) hits all concern native or theoretical covariance.
  - None records an observational covariance as missing.
  - The only related requirement is CI L70, "propagate uncertainty and parameter-state correlations".
  - Observational covariance would fall under the OPEN `uncertainty_model` and the unchosen likelihood, which are already listed.

## Source sha256 at check time (2026-10-15, about 18:16 CDT)

| Source | sha256 | Note |
|---|---|---|
| CI | 6b1d2221f93865c7d805cb229d0503928213ee0ba3f5f5624ea4b4c8be4d5bf6 | 116 lines |
| DIR | e5a547725ac39edf863681864db19fde709a17a1c0ba19fc557665b160959bc1 | 115 lines |
| ASM | 9877ad1678630b75f5aa3af3dbd7e59d3274b898b7387a67581e09865622bf9d | 1196 lines; audit's ASM line ≥754 corresponds to current line +13 |
| V030 | 97a29a71514f1e636c3520f0147571276760f36a1a9154afa79f3977b1acf3a2 | |
| V002 | 31fa7e61b950c463607bd1ca24ec7240768d6b8244d95a2834dae7e714c5bf70 | status keys only |
| 0388 brief | 3734ab00bc7cb7251e39b486b0bf7ea22d0eb038a257cce7508bb75a1cada7c2 | |

## Exposure
- No observed galaxy value was displayed.
- ASM metadata lines were read with every digit masked.
- V030 and V002 were read through `python3 -I -B` key reads with digits masked. The DDO154 datum was tested only for a phrase match and was never displayed.
- Unmasked numbers that did appear were non-observational only: DIR run-receipt check counts and RSS bytes, and V030 `created_utc`.
- No file whose name contains Newton, ROTATION, FIT, TRIAL, MOM1, rotmod or MassModels was opened.
- No target velocities, rotation curves or validation outcomes were opened.

## Execution statement
Nothing was executed apart from read-only operations:
- grep and awk line reads, with masking;
- masked JSON key reads using `python3 -I -B`;
- shasum.

No network was used. Nothing was written under Universal Network Theory. This note was created exclusively (noclobber).
