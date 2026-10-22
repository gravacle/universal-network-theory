# C̄ in-plane anisotropy: decision rule registered before any computation (Claude3, 0487)

Registered at 2026-10-17T21:44:03Z. No C̄ value had been computed or viewed by Claude3 when this was written. The only C̄ numbers seen are the A2 in-plane eigenvalues 0.8818 and 0.9533, quoted in 0487 and in A17.

## Data

**Units.** The test units are the single-chain background charts C̄_c, built as M − μμᵀ from each chain's background cell-sum means (the t1/coeff_grids moments algebra).
- 10 chains come from the five blocks JSON files: admission, cycle, worm, birthk and v004, two chains each. Claude3 rebuilds them from the files' own per_chain_means.
- 14 chains come from the seven CODEX1 runs listed in long_wavelength_response_c2/check F1. They are taken from the checker's extraction CHK_E_OTHER_RUNS_V001.npz (153d4ad0), because Claude3 opens no result.json.
- RAW_REWEIGHT duplicates V004. Claude3 checks that and excludes it.

**Estimates.** All 37 estimates are tabulated: the 16 of RESPONSE_ACROSS_GRIDS plus the 21 of CHECK F1. Six-chain and eight-chain estimates are not independent and are reported only.

## Statistics

- **In-plane statistic.** s_c = (C_xx − C_yy, 2 C_xy) / (C_xx + C_yy). Its magnitude is the in-plane anisotropy (λ_hi − λ_lo)/(λ_hi + λ_lo), and its direction is twice the major-axis angle.
- **Null.** Lattice symmetry D4 of the in-plane square acts on s by independent sign flips of its two components. Under the null, each chain's s is invariant in distribution under those flips.
- **Primary test (P).** S = |mean_c s_c|² over the 24 chains. The randomization p-value uses 200000 seeded independent component sign flips per chain, with p = (1 + #{S* ≥ S}) / (1 + N).
- **Axis test (A).** The Rayleigh test on the doubled-angle unit vectors, plus the same sign-flip randomization on the unit vectors.
- **Secondary tests.**
  - Run level: 12 units, each the mean s of a run's chains.
  - Excluding NEAR_ENDPOINT, which is a different state point (β 0.918, nonzero j).
  - Full cubic Oh: each C̄_c/(tr/3) is acted on by random signed permutations, with statistic ‖mean traceless part‖_F².
  - Each component separately: C_xx = C_yy, and C_xy = 0.

## Verdict rule (fixed now)

- **"anisotropy systematic across estimates"** requires two things. P and A must both have p < 0.01 at chain level, and P must also have p < 0.01 at run level, because chains within a run may be correlated.
- **"anisotropy consistent with estimator noise"** requires P and A to have p ≥ 0.05 at chain level, and P to have p ≥ 0.05 at run level.
- **Otherwise the verdict is "INCONCLUSIVE at L=4"**, reported with the numbers.

The symmetrized C̄ is reported as information only. It is the cubic-group average (tr/3)·I and the in-plane D4 average. Nothing is proposed for adoption.
