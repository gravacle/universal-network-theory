# PREREG_STAGE0_ADDENDUM_V001 — pre-launch facts and registered companions

Written 2026-10-18 after PREREG_STAGE0_V001 (`aee48b02…`, sealed 01:05:50Z) and before any production stage-0 run. The only sampler output that existed when this was written: the 8 toy smoke chains (2 + 16 sweeps each) and the 150 s identity runs, which carry no information about any stage-0 outcome. The sealed prereg is unchanged; nothing below relaxes, replaces or re-weights a sealed rule. Each item adds a registered companion statistic or a reading made necessary by a pre-launch fact.

## F1. Saturated born starts are nearly isotropic (TESTED-POSITIVE)

`starts/STAGE0_STARTS_V001.json`, `starts/STARTS_TIEAVG_V001.json`:
- All 8 born graphs saturate after 128 Births (128/128 slots, U = 0, 768 present edges). Pairwise shared present edges ≤ 29.4% (precondition ii holds); the 8 starts are distinct (iii).
- The seed's C̄ = diag(0, 3, 0) does not survive saturation: the tie-averaged start C̄ diagonals lie in 0.84–1.16, |s| ≤ 0.16, and the largest diagonal equals the declared axis in 6/8 starts (chains 0 and 4 differ).
- So the x/y/z labels are exact symmetry images (c3-rotations), but each start's own C̄ anisotropy is set mainly by its born graph, not by the seed's polarization.

## F2. The actual C̄ read is not c3-covariant on born states (TESTED-POSITIVE)

- Transcribed actual read = operator `read_rows` C̄ to ≤ 5e-13. The tie-averaged read (every min-cost port assignment averaged; RD5 `rd5_tiebias_v002.py`) is c3-covariant to ≤ 4.4e-16.
- The actual read deviates from M C̄ Mᵀ by up to 0.147 on rotated born states; 309–331 of 384 present vertices carry tied port assignments.
- The Hamiltonian is not affected: diagonal energy and channel counts of g(B_k) equal those of B_k (all 8).
- Consequence: the sealed §4 randomization test assumes each chain's C̄ law is c3-invariant. With the actual (tie-broken) read that holds only up to the read-out bias. The sealed statistic is kept and reported; A1 below adds the version whose null is exact.

## A1. Tie-averaged reference-state C̄ (registered companion to §4)

On every 16th measured row (1024 reference-dwell states per process), decode the reference key with the pinned operator's `state_labels` and compute both the actual and the tie-averaged C̄ (`analysis/tieavg_cbar_v001.py`). Apply the sealed §4 statistics to the tie-averaged C̄ (per process and pooled s, q; Ū with the exact 3⁸ randomization; m). Class: START_MEMORY_DETECTED if p ≤ 0.05 or m ≥ 6, else NO_MEMORY_DETECTED. The actual read on the same states is reported next to it.

## A2. Start-graph memory (registered companion)

Because F1 shows that a start's C̄ is mostly its born graph's, the statistic "does the chain remember its own start" uses the start itself: r_k = cosine between the traceless parts of process k's tie-averaged reference C̄ and its start's tie-averaged C̄; r̄ = mean r_k; exact permutation p over all 8! pairings of chains with starts. START_GRAPH_MEMORY if p ≤ 0.05, else NO_START_GRAPH_MEMORY_DETECTED. With WIRING_CHAIN_SPECIFIC (§5) this is the frozen-wiring reading; with WIRING_MIXED it would contradict §5 and is reported as a conflict.

## F3. The sealed flat-quarter rule has no power against drift (TESTED-NEGATIVE as a drift detector)

P0-a (`calib/CALIB_RULES_V001.json`, `calib/CALIB_FLAT_V002.json`, synthetic AR(1), 16 units, n = 16384):
- Family-wise false failure 0.000–0.045 at τ = 10–200 (size as intended).
- Power against a linear drift of 1.72 sd half-to-half: 0.00 at every τ; 0.5 sd: 1.00 at τ = 10, ≤ 0.05 at τ ≥ 50. A drift inflates the series' own τ̂ and variance, so SE_Q grows with the drift.
- Reading registered now: a pass of the sealed flat-quarter leg is **not** evidence of stationarity. The sealed rule still defines the census/U leg of §6.

## A3. FQ-WC, a powered flat-quarter companion (registered; reported, no change to §6 classes)

`calib/calib_flat_v003.py`: SE_Q from the series with each quarter's own mean removed, with the first-order demeaning-bias correction τ_c = τ_w / (1 − 2cτ_w/q), s²_c = s²_w / (1 − 2τ_c/q), SE_Q = sqrt(2 τ_c s²_c / q), flat iff max_j |Q_j − x̄| ≤ 2.91 SE_Q (unassessable or 2cτ_w ≥ q fails).
- Measured (`calib/CALIB_FLAT_V003.json`): family-wise false failure 0.027 / 0.077 / 0.153 / 0.207 at τ = 10 / 50 / 100 / 200; power at 1.72 sd 1.00 / 1.00 / 0.97 / 0.78; at 1.0 sd 1.00 / 0.99 / 0.79 / 0.41.
- DRIFT_FLAG = FQ-WC fails in any (series, process) unit; reported with the measured size at that unit's τ̂. The §6 k = 0 drift reading is labelled "drift-checked" only when FQ-WC passes in every unit.
- Split-R̂ over the 4 quarters × 8 processes (32 segments) is reported for both census series, descriptive only.

## F4. Rule size and power on synthetic AR(1) (P0-b, TESTED on synthetic data only)

`calib/CALIB_RULES_V001.json` (8 chains × 16384, blen 2048, per-column failure probabilities; P(all 778) = (1 − p)^778, independence assumed):

| true τ | p_col R-LIT | P(all) R-LIT | p_col R-MA | P(all) R-MA | Rhat leg failures |
|---|---|---|---|---|---|
| 50 | 0/1500 | ≥ 0.21 (95% bound), point 1 | 0/1500 | ≥ 0.21, point 1 | 0 |
| 100 | 6.7e-4 | 0.60 | 0/1500 | ≥ 0.21, point 1 | 0 |
| 150 | 0.0153 | 6e-6 | 0/1500 | ≥ 0.21, point 1 | 0 |
| 200 | 0.128 | 5e-47 | 0.001 | 0.46 | 0 |
| 300 | 0.60 | ~0 | 0.041 | ~0 | 0 |

Reading: for a perfectly mixed sampler at this design, R-LIT is passable only if τ_max ≲ 100 sweeps, although its threshold nominally admits 409.6; R-MA is passable up to τ_max ≈ 150–200. The Rhat leg never failed spuriously (0 of 6,500 synthetic columns), so any Rhat > 1.1 in stage 0 is read as between-chain disagreement, not noise.

## F5. Worker identity and smoke (TESTED-POSITIVE)

- `identity/IDENTITY_TEST_V001.json`: the C2V001 worker with one argument writes a progress journal byte-identical to the pinned worker V004 over the 115-line common prefix (≈ 110 burn-in sweeps). In spec mode at the original seed/start (SeedSequence(2026101702) stream 0, registered seed, V004 schedule and caps) its chain-0 sweep records equal V004's chain-0 records in every chain-local field over 110 sweeps; the global counters differ by a constant +1 channel enumeration and +12 budget checks, which is V004's chain-1 initial-path admission in a 2-chain call.
- `smoke/SMOKE_CHECK_V001.json`: all 8 smoke chains were admitted from their declared start (harness observer key = manifest key = spec key), completed the sampler and the all-k analysis, and committed every row. With 16 rows (blen = 2) each process's own sampler analysis reports `failed` on the τ leg, as expected; the external evaluator is the rule.
- Evaluator check A0 (`analysis/A0_BIRTHK_V002.json`): on the 2-chain BIRTHK capture it reproduces the sampler's own Rhat and τ for all 778 columns bit for bit (max difference 0.0), every column status, the 6228 exact-invariant columns, d2logZ to 1.2e-9 and the b7 grid to 8.9e-16. Check A0b: the transcribed `_rhat`/`_sokal_tau` equal the pinned sampler's functions bit for bit on 1,877 synthetic cases.
