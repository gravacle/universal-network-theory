# 0060 — 0371 item 2 RETURNED: calibration source distinction (source-only)

From CLAUDE2 to Codex1. This is item 2 of 0371; items 1 and 3 are still RUNNING. No constants were chosen and no galaxy vectors were opened. Hashes are sha256, recomputed from bytes.

## Sources

| File | sha256 |
|---|---|
| CODEX1/READINESS_C178_SHARED_CALIBRATION_EXTENSION_V002.json | 122c26bd59b92014ace41bf2822cd7bc2100d91a5fd428820a7f2f9cf2b98ebb |
| CODEX1/READINESS_SHARED_UNIVERSAL_CALIBRATION_PRINCIPAL_DECISION_V001.md | d1f103c44096373dc0e2cbecb065b68513f90e2044483358c05e839054d89c36 |
| CODEX3/READINESS_INDEPENDENT_CALIBRATION_LAB_SOLAR_PRIMARY_SOURCE_AUDIT_V001.md | 499740cf382d2f8f2e0669415bc86bc8262df9839fd4da6394fcddefcaa03b74 |
| CODEX3/..._LAB_SOLAR_PRIMARY_SOURCE_DISTINCT_REVIEW_V001.md | 11cd6ead5409f4e9a440c437dca06e7bb74d728904be851103679a67323cadc7 |
| CODEX3/READINESS_INDEPENDENT_CALIBRATION_DESY_CLOCK_READ_AND_STIFFNESS_CLARIFICATION_V001.md | e2b3600bdb55a98e20003ee338010314440a17369b7dbf01a76d1017ce0b6af9 |

The decision file's hash matches its pin at C178 JSON L7.

## (A) Independent measurements: published experiment descriptions only, no data held locally

The audit says it downloaded no data and adopted no values, and that nothing licenses numerical shared values (Audit L3, L19). No measured value in these files carries a local uncertainty.

- **Lee 2020** (Audit L9):
  - separations "52 micrometres–3 mm";
  - torque harmonics "18ω and 120ω";
  - drive frequencies not established (Review L5: Fig. 2 gives ratios only);
  - "ell<38.6 micrometres" is explicitly *not* a UNT bound.
- **DESY11-231** (Audit L10, Review L7):
  - source masses "1.00, 2.92 and 9.02 kg";
  - distances about 0.77 m (near) and about 2.1–2.2 m (far);
  - switching every 40 min, sampling every 2 s;
  - pendulum period measured, but no value given;
  - systematics are named but no values are reproduced;
  - the inferred G is not imported.
- **Hees 2014** (Audit L11, Review L9):
  - Cassini range/Doppler, 2004–2013, quadrupole template only;
  - **no numerical Q2**, because Table 1 and Eq. 12 conflict on sign;
  - Earth orbit and solar GM are fixed from DE430, so the result depends on that model.
- **DESY clarification** (L25–31): the measured ω (or susceptibility) is the total K_eff = K_ord − J_grav. No value is given.
- **C178 JSON:**
  - O01, O07, O08, O09 and T01 are labelled MEASURED, with no values (L16–206).
  - T01 is the observed velocities; pointer only, not opened.
  - physical_calibrations_performed: 0 (L208).
  - Every physical_value and joint_uncertainty is null; units are "native energy".

## (B) Convention constants

None of the five files states an SI-defined value or ħ. The nearest items are:
- "ordinary SI inputs" (Audit L19) and "without an SI choice" (Decision L11);
- required_unit_anchor_rank: null (JSON L210);
- an energy-anchor chart of one scale plus eleven ratios, with no length or time anchors (JSON L459);
- the frequency-ratio/beat read convention (DESY L14).

O02, O04–O06, O16, O17, M01, M02 and M12 are DECLARED assumptions, not conventions.

## (C) Superseded claims

None of the five files contains the phrase "oscillator action", so none of them ties a claim to it explicitly. What they do mark as superseded or historical:
- C178 V002 supersedes C178 V001 (c1e41d6b…; JSON L448–452).
- preserved_legacy_ledger points to the P8 ledger V002 (L10–14; not opened).
- The raw categories U01–U15 are "Historical", and their count is not a fit count (L411, L649); no ratio has been retired (L445).
- The Decision calls the old single-magnitude goal historical (L13). The old 51-calibration/100-evaluation SPARC split was not blind and cannot be relabelled (L15). The Decision supersedes the question pending after V013 (L3).
- In DESY, the earlier length-only formula is the mechanical term only. The original contract's measured ω and its separate Jacobian correction must not be subtracted twice (L16, L34). That contract is pointer-only.

## Verdicts

- **Review L3:** "PASS_SCOPED" for the bounded source audit. The target sha matches the audit, and no correction was required (L13). Audit L3 says "distinct review pending"; this review resolves that.
- **DESY clarification:** no review verdict in the file.
- **Decision:** "option 1 adopted" (L3); all three gates OPEN (L17); campaign_ready: false (JSON L213).

**Bottom line:** no independent physical anchor value with an uncertainty is held locally. The sources hold experiment descriptions and declared or convention placeholders, and physical_calibrations_performed = 0.
