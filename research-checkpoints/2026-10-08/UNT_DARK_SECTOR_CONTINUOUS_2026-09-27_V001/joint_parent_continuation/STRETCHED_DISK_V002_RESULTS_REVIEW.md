# Independent saved-result audit: stretched disk V002

2026-09-28. Read-only source/result audit and algebraic recomputation from
saved potentials. No solver, PCG iteration or duplicate physical worker
was launched by this reviewer. Original V001 source and failed case remain
unchanged.

## Verdict

**All thirteen V002 cases pass, with 91 saved case checks.** The enlarged
linear allowance and true-residual verification close the original numerical
failure without changing the field law, source, grid or any acceptance
threshold.

| eta | L=8,N=64 radial error | L=8,N=128 | L=8,N=256 | L=128,N=256 |
|---|---:|---:|---:|---:|
| .01 | 0.3000% | 0.07718% | 0.01995% | 0.09687% |
| 1 | 0.3809% | 0.09862% | 0.02563% | 0.12424% |
| 100 | 0.4827% | 0.12494% | 0.03247% | 0.15753% |

The independent Newtonian `N=128,L=8,eta=1` case has maximum radial error
`0.124993%` and converges in one outer update. Every nonlinear near-domain
refinement improves the frozen maximum-error score. Every finest and
large-domain score is below the unchanged 2% requirement.

## Numerical and custody checks

The V002 source freeze is
`4c981d9ed8f64a7293cc7fd75ebbc13e51221b51198d681e2686472725050d3f`.
All eight named entries match, including the original operator and the
actual inherited shape result. Every expected case has the correct exact
parameter tuple, freeze hash, canonical payload hash and array dimensions.
All scored errors and refinement relations were recomputed from saved data.

Across the thirteen cases:

- Maximum saved final nonlinear residual: `9.81395215535323e-10`.
- Maximum saved final relative flux imbalance: `4.333195663665406e-7`.
- Zero accepted clipped faces; every inner step reports verified true
  residual at most `1e-12`.
- Largest inner iteration count: 3,761, below the new allowance 8,292
  for its `N=256` case, but above the old 2,148 allowance.
- The recorded histories contain 57 true-residual direction restarts and
  615 explicit true-residual checks. Thus the verification logic was
  actually exercised, not merely dormant source code.
- Summed recorded case time: `92.51331050103181` seconds; process-self peak
  RSS high-water reading: `67,977,216` bytes. These are not total job-tree
  memory or end-to-end wall-time measurements.

Using each saved field, I regenerated the frozen geometry and analytical
boundary data and reevaluated the original finite-volume operator. All
thirteen fields still satisfy nonlinear residual, flux and clipping
criteria. Maximum differences from their saved diagnostics were
`9.173149356599948e-16` in normalized residual and
`8.040647369184845e-12` in relative flux imbalance, consistent with the
different numerical evaluation order and far below the fixed criteria.

I also independently assembled the three-point nonuniform derivative
coefficients from the centre separations and applied them to the saved
disk-plane extrapolations. Maximum absolute difference from a saved radial
force was `1.1368683772161603e-13`. These are source/field algebra checks,
not a new iterative solve or another physical run.

The preserved V001 failure remains SHA-256
`ffb93dedc4f1849e59244d351d71f9f85d7d399f3653b28e49a4c3fd6033a2a1`.
It stopped before a completed first Picard update. The V002 result is an
additive numerical repair, not relabelling that failure as a pass.

## Meaning

The same nonlinear field law now has verified stretched-grid performance
over the larger exact-boundary benchmark, with fine central radial accuracy
and conservative flux. This supports using the implementation for a
separately frozen source calculation. It does not certify an arbitrary
galaxy's source reconstruction, approximate monopole boundary, observational
agreement or native clock/volume interpretation. Those belong to the actual
galaxy experiment and the separate analytical bridge work.
