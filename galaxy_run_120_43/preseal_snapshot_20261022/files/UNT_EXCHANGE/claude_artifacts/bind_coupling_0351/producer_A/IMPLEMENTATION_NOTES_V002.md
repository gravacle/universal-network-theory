# Bind-coupling producer V002: changes after the distinct review

Producer V001 (607ebc4d…) received PASS_WITH_NOTES with no SHOULD-FIX. IMPLEMENTATION_NOTES_V001 still applies, and the reviewer agreed with all six interpretation points.

The reviewer confirmed the contraction with an independent full-space Feshbach oracle on asymmetric generic toys:
- the degree-6 term equals −C_yx to within 1e-10;
- degrees 2–5 vanish;
- relabelling invariance holds.

| Note | V002 change |
|---|---|
| N1: a block entirely below E1 was labelled RESONANT | New status BELOW_E1_PREMISE_VIOLATED, used when the gap plus uncertainty is below 0 and min\|w−E1\| minus uncertainty is above the margin. min\|w−E1\| is reported for every block. No inverse is formed. Test V2a. |
| N2: the spec is not yet in CODEX1 | The launch order must place `BIND_COUPLING_REFERENCE_FROZEN_SPEC_V001.json` in CODEX1. Otherwise the run exits 2 with E_PIN_SPEC_MISSING. |
| N3: realization positivity not checked | U_d > 0, Δ_edge > 0 and d* ≥ 1 are checked exactly, with exit 2 on failure (test). (W) remains a float64 check whose result is recorded. |
| N4: inverse non-negativity not gated | Per block, `negative_inverse_entries_beyond_tolerance` (tolerance 1e-9·max\|R\|) is recorded and enters the inverse gate (check failure). Test V2b. |
| N5: global remainder bound | Stated verbatim, alongside the s-form inequality. |
| N6: negative-contribution failure branch not exercised | Exercised by a non-Z-matrix toy block (V2b). |

The output schema is now BIND_COUPLING_REFERENCE_OUTPUT_V002. No native computation was run. Synthetic suite: 26/26.
