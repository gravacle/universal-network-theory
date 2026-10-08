# Independent common-history mechanism review

2026-09-28. **The declared clamped mechanical calculation and its independent
integration check pass. The result is oscillatory memory, not a universal
one-sided delay.** It changes no galaxy force law, source or observation.

## Equation and source audit

The implementation uses the specified positive scalar mechanical parent with
kappa=u4=A=m=Lambda=1, the inherited bounded-source scale, and fixed initial
rest states. The same bump-integral history is used at all three amplitudes,
with globally shared ramp durations 8/16 and holds 0/8/16. These times are in
an uncalibrated unit, not galaxy ages or native UNT time.

The cubic equilibrium formula solves `y³+delta²*y=delta*h`. The equation of
motion is `y_ddot=delta*h-delta²*y-y³`. The full potential written as positive
squares is exactly equivalent to

`E = Kb*g²/2 + sum w*(v²/2+delta²*y²/2+y⁴/4) - h*B`,
`B=sum w*delta*y`, `F=Kb*g-h′*B`, `E_dot=F*g_dot`.

Thus kinetic energy, contact, interaction and external work are retained.
Weights include the delta-density factor once, in both kinetic and potential
terms. Each positive lower cutoff has its matching `Kb=(1-gap²)/2`; no
excluded-mode contact is hidden. The analytic full-band force comparison is
reported as a physical finite-band difference, not demanded to vanish.

The 12 batches are exactly two cutoffs × two ramp durations × three numerical
resolutions. Each holds three amplitudes and three observations: 108 stored
states in total. The main gap=.001, order128, dt=.005 census has 18 observations.
The lower-cutoff sensitivity is a second finite-band model, not a proof for
an arbitrarily excited zero-gap continuum.

## Independent numerical validation

`common_history_independent_audit.py` authenticates all frozen inputs and the
saved payload. It independently reconstructs all 108 states using the expanded
energy, and solves the static cubic by bisection rather than the production
hyperbolic formula. Polynomial measure moments through degree six, force,
polarization, kinetic/total energy, excitation, work and envelopes all pass.
There are 1,320 arithmetic comparisons; maximum scaled residual is 5.523e-12,
including the coarser saved work ledger. The original finest maximum monitored
work-ledger residual is approximately 3.935e-13 in Kb*G² units.

A separately implemented velocity-Verlet trajectory checks the most nonlinear
declared amplitude G=.04 at T=8, gap=.001, order128. It uses independent 128-node
bump integration and trapezoidal `F dg` work, not the production RK stages or
ramp routine. Halving dt=.0025 to .00125 gives the expected approximately
fourfold errors. Across all three observation times, the finest force differs
from RK4 by at most 6.463e-8 in units of G; Richardson extrapolation differs
by at most 5.225e-12. Finest work discrepancy is 2.600e-8 in Kb*G² units,
falling to 3.029e-13 after extrapolation. All are within the original 2e-6
cross-resolution criterion. No second galaxy/PDE calculation was performed.

The maximum change in sampled D/G between gaps .001 and .002 is 4.129e-6.
The original quadrature/time-step comparisons and every signed state remain
stored. Equal dimensionless age alone is not claimed to produce exact curve
collapse because the dimensionless cutoffs and bounded-source ratio change
with amplitude.

## All 18 main signed observations

Entries are `D_actual/G`; columns retain the fixed amplitudes. The respective
relaxed values are 0.00293803, 0.01168042 and 0.04553192.

| Ramp duration | Hold | G=.0025 | G=.01 | G=.04 |
|---|---:|---:|---:|---:|
| 8 | 0 | -0.37628914 | -0.37576281 | -0.36739256 |
| 8 | 8 | -0.06363242 | -0.05405656 | +0.04479973 |
| 8 | 16 | +0.04421165 | +0.06662944 | +0.12048719 |
| 16 | 0 | -0.04785461 | -0.04494999 | -0.00235835 |
| 16 | 8 | -0.00432726 | +0.01025135 | +0.09151884 |
| 16 | 16 | -0.00208820 | +0.02249120 | +0.04825452 |

Ten instantaneous values are negative and eight positive. Twelve are below
their relaxed value, six above. All six end-ramp values are negative; those
signs are preserved, not removed as inconvenient phases. Excitation remains
positive and the exact energy/force envelopes hold. A negative derivative with
respect to an externally clamped source is not a demonstrated instability of
the positive full Hamiltonian or a solved gravitational motion.

This establishes a concrete conservative memory channel under one shared
history, while rejecting a universal claim of always-smaller polarization,
monotonic relaxation or a chosen-sign delay for this parent. A later orbit mean
can be calculated from the retained energies without pretending they dissipated;
the actual finite-time states remain the primary results above. Neither these
states nor a phase mean may be substituted into the stationary galaxy equation
as an inferred `mu_age`.

## Custody

- Original freeze: `13d05e24680166cb903e02fb961717a2bef1a89771a1d76c80156ab50cbe76ef`.
- Original result: `e57f1f93254a610abc9b08ef5df355d74035efa762079ffd43e89205bc0f715a`.
- Independent audit script: `be1bfa804c4e350941d7b57f0fa79a68d0019fb52bc5bacd5994036600b7e4e7`.
- Independent states and comparisons: `COMMON_HISTORY_INDEPENDENT_REVIEW_DATA.json`.

No frozen source or result was modified during the audit.
