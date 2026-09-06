# Independent hostile read-only audit

**Date:** 2026-09-06

**Verdict:** `PASS`

An independent hostile reviewer inspected the staged Authenticated
Accumulation Screen V001 without editing its artifacts. A replay from a
temporary copy passed `49/49` checks and reproduced
the original `FINAL_HOSTILE_RESULT.json` with SHA-256
`27a4247e79d11454fa8db28a187b55125e7c586c5130b30204a22a023b92e162`.
All frozen custody hashes matched. The reviewer then identified one minor
telemetry-label discrepancy: the reported maximum omitted the target--blind
pair. The final verifier was repaired to take all three pairwise maxima; its
verdict and check census are unchanged, and the corrected result has SHA-256
`3adf5162a97cab659d9a0ef3a4b80ac3daa4ff82b6802a6b45a8c1c06bb00434`.

The target, repaired blind, and dense-adjudication spreads for `W_1`, `W_2`,
and `W_3` were respectively `0`, `2.832e-13`, and `1.899e-12`. Independently,
a fresh complete 256-state order-36 series propagation returned

```text
W3 = -0.28406635505827449
```

This differs from the dense adjudication by `1.33e-15`; its norm error was
`8.88e-16`. The conservative adjudication upper bound
`-0.2840663550202991` therefore remains strictly negative.

The reviewer confirmed that the repaired blind full row properly remains
`UNRESOLVED_HISTORY_L`, because its maximum norm drift
`1.3402301490827995e-10` exceeds the frozen `1e-10` guard. It is used only as
corroboration. The complete dense adjudication is fail-closed to the sign
Boolean and cannot authorize a positive sector.

No L6, L8, L10, or L12 history and no spectral/Krylov output exists in either
packet. The frozen implication was confirmed:

1. the first three `W_n` must be positive for an admissible L4 sector;
2. the independently reconstructed L4 `W_3` is strictly negative;
3. an admissible L4 sector is necessary for the common L4--L12 intersection;
4. therefore `NO_COMMON_ACCUMULATION_SECTOR_L4_L12` and the mandated halt
   follow.

The ledger and continuation claim boundaries were also reviewed. They
correctly state a bounded same-port-history obstruction, not a generic
accumulation no-go. Continuum behavior, emergence, and gravity remain
downstream and open.
