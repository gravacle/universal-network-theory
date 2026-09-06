# Hostile audit — connected L8 circuit depth trajectory V001

## Disposition

**PASS_CONTROLLED_NUMERICAL_DEPTH_TRAJECTORY.** I independently rebuilt the full 65,536-state circuit at depths 0 through 8 without importing the target implementation or its result. No material defect was found.

The finite census is 16 clusters partitioning 256 retained heads, 24 unique owner-once supports per depth, eight of them inter-ring, and 192 gate records. All 24 cumulative supports and all eight rungs are active at every positive depth. Gate endpoint changes have the declared current signs; the largest independent gate-ledger error is recorded in `INDEPENDENT_RESULT.json`.

## Traffic and controls

The audit separately reconstructed cumulative-net throughput and gate-event absolute traffic. Event traffic is the sum of all 192 event magnitudes and is strictly increasing at every positive step. Net throughput is the sum of magnitudes only after signed per-edge accumulation; it is not granted monotonicity. Cancellation is numerically visible: cumulative ring throughput falls from depth 2 to 3 even while event traffic rises, and event traffic exceeds total cumulative-net throughput after depth 1.

The independent envelopes reproduce retained totals, correlations, raw residuals, norm error, and number-law change. The former `5e-13` retained-L8 tolerance would fail against the reconstructed `7.105427357601002e-13` drift, while the documented pre-audit `1e-12` execution tolerance passes. The numbers verify the necessity and sufficiency of that repair; the packet's statement is the provenance evidence for its timing.

## Claim custody

The read is the complete failure-inclusive product PVM. Attachment remains inherited adopted `alpha=r0`, not a bare-F3 derivation. Tuple labels are finite-family enumeration, not a physical grid, and circuit depth is not continuum time. Raw residuals remain unassigned: they are not defects and are not promoted to exact zeros. This audit promotes no critical/scaling law, lineage identity, continuum limit, Ward identity, or gravity claim.
