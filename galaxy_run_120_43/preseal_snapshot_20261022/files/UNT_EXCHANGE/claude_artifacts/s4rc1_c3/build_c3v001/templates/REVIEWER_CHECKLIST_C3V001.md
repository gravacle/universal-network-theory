# S4-R-C1 reviewer checklist (c3v001)

**For:** distinct-lane reviewers of the per-point CP-1 records: EPS (section E), LO caps (section K) and the LO envelope (section L).
**Builder:** Claude3 lane (A122). **Tool reviewer:** Codex1 under A115.
**Templates:** `REVIEW_TEMPLATE_EPS_C3V001.json`, `REVIEW_TEMPLATE_LO_CAPS_C3V001.json`, `REVIEW_TEMPLATE_LO_ENVELOPE_C3V001.json`.

## Rules for every review

- **Distinct lane.** The reviewer lane must be one that root approved as a signer (brief section 6 Q8). It must not be the CP-1 operator lane, and it must not be Codex2, which authored the producers. The tools refuse any other lane.
- **No self-approval.** The tools never write, edit or approve a review. Write each review in your own lane folder, outside the runner's output root, by exclusive create. Then give root the path and the sha256 taken from its bytes.
- **Physics first (A115).** Block only on a defect that an honest pinned producer could reach on these records, or on anything that could change a physics reading. Robustness against forged inputs is a NOTE.
- **Readings are preserved (R2, 0674).** Report a failed or blocked value exactly as measured. Never cure it by changing caps, settings or shells after a number has been seen.
- **Labels.** Mark each item TESTED (you checked it from bytes), FORMAL (inferred from code) or UNTESTED.

## E. EPS review, one per point (adapter v003 `4de70486`, L182-188)

| # | Check |
|---|---|
| E1 | **Scope.** `point_sha256` is the point's key in the 31-point table. `custody_sha256` is the digest of the record's `custody`, which equals the value in `STAGE_CONTEXT`. The record's `producer` is the canonical `point_response_producer_cx2v002.py` pin, `a1dcdea8`. |
| E2 | **Registered and complete.** `settings` is `registered`. `full_registered_search_executed` and `coverage_complete` are both true. There are 178 unit shells, [4,5] to [181,182], and 14 dense audits. |
| E3 | **Discrete rule.** `registered_discrete_verdict` is `CERTIFIED` and every shell has `refinements` in {0,1}. Note any shell with `refinements` 1. |
| E4 | **Dominance.** On every shell, `eps` ≥ `eps_envelope` ≥ 0. `eps_max` and `eps_max_shell` are consistent. The adapter re-checks every candidate; you check that the values are plausible. |
| E5 | **Audit ratios.** Record the minimum and maximum `dense_over_production` over the 14 audits. A ratio well above 1 means the production search under-resolves that shell: reject, or flag for root. |
| E6 | **Magnitude (Q10).** Record `eps_max` and its shell. The guard applies no magnitude gate to per-point EPS. For comparison, the anchor's V006 `eps_max` is 6.4e-4 on [2,3], and the sampled \|1−q\| at corner_00 on [4,5] was 0.0125. Flag a large value for root's per-point remainder question; do not reject on magnitude alone. |
| E7 | **Anchor only.** `ANCHOR_EPS_CROSSCHECK_*` reads AGREE: 178 overlapping shells, with the relative differences in envelope and dominating value within the tolerance root set. |
| E8 | **Stage record.** `STAGE_EPS` has `ok: true` with every check true, and the record bytes re-hash. Timing and RSS are present; they are information only. The context source pins match the anchor (`source_pins_match_anchor`). |
| E9 | **Convention.** The values are search lower bounds on the continuous supremum. Approve only as the registered numerical convention: `accepts_registered_numerical_estimate_not_rigorous_sup: true`. |
| E10 | **Distinctness.** E-rules above hold. The review binds the exact `numeric_ref` pin and `adapter_sha256` `4de70486…`. |

## K. LO cap review, one per point (lo_core `12d36305` L416-439; facade c3v001)

**Not fillable until root rules Q1–Q5 and Q8–Q10 (0674).**

| # | Check |
|---|---|
| K1 | **Root ruling.** Root's ruling on Q1–Q5 exists and is pinned in `root_ruling`. |
| K2 | **Frozen first.** The caps follow root's adopted rule (Q1) and were frozen before any LO number for the point was seen (R2). The cap file predates every LO record of the point. |
| K3 | **Coverage.** The components cover every source in every route-A and route-B stage roster, using total-variation masses for signed offsets. |
| K4 | **Shapes.** `component_column_TV_mass_caps_kg` has shape (n_components, 4·(len(s_edges)−1)). `mass_convention` is `ACTUAL_PROPER_SOURCE_TOTAL_VARIATION_PER_COLUMN`. |
| K5 | **Limits.** The stars multiplier cap is given, and `gas_z_abs_max_m` ≤ `z_src_max` (32 kpc). |
| K6 | **Readout caps.** `row_ids`, `R_m` and `tau_km_s` equal the custody row contract, and so does `row_contract_sha256`. The speed caps and the uncertainty carrier follow root's Q4 ruling and are set in the cap contract, not in custody. |
| K7 | **Enforcement (Q2).** The module is pinned and reviewed. It rejects every constructed and consumed state outside the caps, under root's definition of `reject_before_consume`, and the complete stage inventory was reviewed. |
| K8 | **Producers.** `producer_sha256` is `12d36305…` and `response_producer_sha256` is `a1dcdea8…`. |
| K9 | **Scope.** `identity` and `custody` are the full dicts of this point. lo_core compares them by dict equality. |
| K10 | **Distinctness.** The reviewer lane is root-approved and distinct from the cap author and the operator. |

## L. LO envelope review, one per point (lo_envelope_adapter_c3v001)

**Not fillable until K is complete and a real LO record exists.**

| # | Check |
|---|---|
| L1 | **Record.** Schema `UNT_POINT_LO_NUMERICAL_CX2V001`, kind `PRELAUNCH_CONDITIONAL_SOURCE_ENVELOPE`. The core verdict is `CONDITIONAL_NUMERICAL_EVIDENCE_REVIEW_REQUIRED` with `blockers` `[]`. `facade_verdict` is PASS and `production_admissible` is false. |
| L2 | **rho.** Registered settings, full search, 9 shells [4,5] to [128,182], producer `a1dcdea8`. |
| L3 | **Nodes.** In `node_envelope`, `N_perp` and `N_z_plus` match the point's production nodes. Record `maximum_source_envelope_J`. |
| L4 | **Thresholds.** Every shell max is ≤ 0.005 τ and the sum is ≤ 0.05 τ. The adapter recomputes both, along with every per-row ratio. |
| L5 | **Inflation, at the anchor.** Record the envelope against LO_CERT_V004 (`1c384f76`, actual state, 3.95e-4 τ on (128,256] at K256). Compare only overlapping shells, like for like. Report the factor; it is a reading, not a gate. |
| L6 | **Condition.** The record's `condition` text is acknowledged verbatim, and an enforcement module exists (K7). |
| L7 | **Blocked records.** Never approve a BLOCKED record. `CONSERVATIVE_CAP_ENVELOPE_ABOVE_THRESHOLD` means the bound cannot certify the point. It is not a NON_LAPSE_TAIL_MATERIAL finding, and the caps are never re-tuned (R2). |
| L8 | **Distinctness.** As K10. The review binds the exact `numeric_ref`, `adapter_sha256` and `facade_sha256`. |
