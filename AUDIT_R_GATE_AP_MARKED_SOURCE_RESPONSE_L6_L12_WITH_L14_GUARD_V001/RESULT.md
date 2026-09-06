# Result

Verdict: **PASS -- hostile marked-source response audit**.

- Target packets: L6 `35/35`, L8 `35/35`, L10 `29/29`, L12 `29/29`,
  compiled ladder `23/23`, and L14 screen `5/5`.
- Hostile verifier: `309/309`.
- L6/L8: all six complete vectors have independent full-space parity within
  `4e-11`.
- L10: the separate complete-vector calculation has maximum target error
  `4.4055e-4` and maximum coarse/fine change `8.1594e-4`.
- L12: the separate complete-vector calculation has maximum target error
  `8.6326e-4` and maximum coarse/fine change `7.8897e-4`.
- L14: no response was run. The independently reconstructed dominant payload
  alone is `101895864328` bytes, above the `42949672960`-byte guard; the
  target conservative upper bound is `101895903752` bytes.
- Discrepancies: none.

The L10/L12 cross-check is approximate empirical corroboration, not exact
parity. Its remainders are raw unassigned numerical terms. All radii in this
packet are finite support-graph distances only.

Gate A-P remains **OPEN**. This audit does not claim an L14 result, a locality
or scaling law, physical boundary behavior, a continuum or Ward limit, a
phase, a graviton, or gravity.
