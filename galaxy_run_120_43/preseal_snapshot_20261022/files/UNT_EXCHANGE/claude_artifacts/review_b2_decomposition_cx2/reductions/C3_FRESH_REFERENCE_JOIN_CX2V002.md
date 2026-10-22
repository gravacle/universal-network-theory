# A97 fresh C3 le3 reference — component join

date -u: `Sun Oct 18 20:09:30 UTC 2026`

**TESTED: 9/9 reduction/join checks passed.** The independent fresh ADV box12/O6/width0.25/P16 evaluation uses the same le3 OFF array and IND input pins as the component calculation. No old le4 reference is used in this chain. The quadrature was performed in the independent `adv_le3` lane; this join performs only saved-vector reductions.

Fresh C3 raw production-minus-ADV sanity maximum: **0.095063978538988181 km/s**, at DDO154_SPARC12_08. It exceeds the unchanged 0.05 raw allowance. The same-state discrete-reference remainder is **3.915090474038152e-12 km/s**; this is a combined quadrature/implementation remainder, not uniquely attributed to one mechanism.

The exact per-row chain now closes from fresh same-le3 ADV through discrete IND, gas-continuum/discrete-star, common-linear-force full continuum, exact denominator and production. Named-only common-linear-force stellar residual remains **0.035622579799763798 km/s**. Actual alias contribution is zero because both compared channels are P16. The separate fresh P16-minus-m0 diagnostic is **0.0870977916345268 km/s** and is not subtracted from the matched-P16 comparison.

Production exact versus the gas-matched discrete-star linear-force reference is **0.035622629866381317 km/s**, including tiny readout/implementation terms; it is not labeled pure stellar-only. All signed row vectors are in the JSON. No scientific reading is advocated and no gate record is modified.

Byte pins:

| File | SHA256 |
| --- | --- |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/run_20261018T200537Z_93548/RESULTS_CX2V001.json` | `0d672be05df87becc9ed5486946d20f23203921796b22b2e7e19b963e5a0cbe3` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/adv_le3/RESULTS_CX2V001.json` | `513c117295a43a6ec6ef778e35476eb3520b6032c0c0217c14ee624f59e16bf4` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/join_fresh_c3_cx2v002.py` | `fd0444e27cb8c1a3dec17aa93ffbe72f9ebafe8f98b1128da2fad7f0d0b81bb3` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/C3_FRESH_REFERENCE_JOIN_CX2V002.json` | `2878a43d0ef96c60d2791bc25a17843f301fd42cf5c2355902a156f93b2cc2b3` |
