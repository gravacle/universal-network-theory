# Independent two-current saved-result audit V001

All 12 prescribed cases are present, `COMPLETE_FINITE_R_NUMERICAL_CASE`, with
zero producer failures. The independent saved-array audit passes 1,023,612
arithmetic entries and authenticates 135 files. The producer's 598,200 checks
are retained separately; these are numerical entries, not physical tests.
No scientific producer, equation of state, quadrature, RHS, trajectory or
compiler was rerun.

## Exact binding and audit coverage

- Scientific freeze:
  `0c698bc6c9867d7afdb32f2dc51f9b776a14f6512a5e302ec8b28aa0c9057c82`.
- Custody/resource-controller freeze:
  `4c55e7748a32607d0289fd86979375240bced1f63437e40c60ccff365be4e9d4`.
- Saved-only reproducer `spherical_two_current_saved_audit_v001.py`:
  `f952c8280697ae8495ed4440216e13261c04c4412cc3bc92d91901402136a478`.
- Full audit `SPHERICAL_TWO_CURRENT_SAVED_AUDIT_V001.json`:
  `6f8147e075df6a0b0f329487720e9de60f0b6058068603313a843fb8595716f8`.

The audit binds every raw case, RUN receipt, intent, freeze and frozen member;
base64 stdout equals the exact saved scientific JSON, stderr hashes/lengths
match, case dictionaries and payload hashes agree, and each invocation has
zero exit code without resource/monitor/validation failure. Maximum sampled
group RSS is 95,436,800 bytes. The slowest producer is case5, 27.536 seconds
(the encompassing supervisor timing is longer). All original continuum,
interval/shock, full-metric and observation flags remain false.

Independent algebra reconstructs fixed masses, exact spherical volumes,
density/action ratios, stored spatial gradients, canonical velocity/kinetic
energy, pressure normalization and force, material enthalpy/sound identities,
internal/active-stress omissions, and all saved work/energy balances. An
independent elementary integration of the saved piecewise-constant densities
reconstructs the self/background energy, face-force derivatives and potential
span; it is not a new field solve. All three saved time-method vectors reproduce
the original state/velocity/volume/action comparisons. Maximum reproduced
state discrepancy is 7.547e-10 against the existing 2e-8 gate; total energy-work
defect is 4.17e-15 and hard-specific mechanical-work defect 6.39e-14 against
the existing 2e-7 gates. Stored pressure accelerations reconstruct within
4.81e-13; gravity accelerations within 2.23e-16 in the recorded normalization.

Synthetic perturbed states/energies underlying the producer's directional
finite-difference tests, and all GL128 comparison arrays, were not separately
saved. Their counts/maxima are authenticated, not independently reevaluated.
This limitation is explicit in the audit output.

## Actual finite-pressure result and spatial comparisons

The final time is 1/16 dynamical unit, about 1.6634 Myr, with
A=1.0001252133. Both currents move and gravitate in the declared weak-field
rest-gravity reduction. The finest results demonstrate a real pressure/current
contrast, not merely a pressure residual evaluated on the old dust trajectory:

| Readout at final time | R128 | R8192 |
|---|---:|---:|
| maximum I/Ibar(A) | 1.046135 | 1.053834 |
| most inward hard v/vdyn | -0.118100 | -0.155389 |
| most inward ordinary v/vdyn | -0.155518 | -0.155518 |
| maximum absolute pressure acceleration/gstar | 1.78257 | 6.009e-7 |
| maximum omitted hard active stress/rest | 6.7931e-6 | 4.0788e-13 |

For R128 the pressure maximum is outward around r/(A ell)=0.371; it
materially reduces hard infall. R8192 is close to the cold response in these
finite-time integrated fields, but its tiny central pressure maximum is not
spatially resolved (see below). The minimum sampled cell-volume ratio is
0.9489001; no recorded guard or cell-order failure occurred. This does not
prove an interval bound or authorize post-crossing continuation.

The saved collector retains all 12 grid-pair and six domain-pair comparisons
at all four times, signed extrema, volume-weighted RMS and observed orders.
Nested cell mass/volume integrals are restricted to common initial labels
inside label radius4, without extrapolation. These are Lagrangian label
comparisons, not an unlabelled Eulerian interpolation. It separately reports
enclosed excess masses at fixed comoving radii .25,.5,1,2,4.

At final time, medium-to-fine weighted RMS changes relative to the finer
signal are 0.1263% (R128 hard velocity), 0.2167% (R8192 hard velocity),
0.3237%/0.5984% for the corresponding hard density contrasts, and 0.7852%
for ordinary velocity. Observed orders are about1.992/1.955 for hard velocity,
1.984/1.784 for hard density contrast, but only1.419 for ordinary velocity.
These are descriptive error estimates, not posthoc acceptance cutoffs or a
universal second-order theorem. Constant-background pressure normalization
can make a relative pressure error look artificially small; density-contrast
and force diagnostics must not be replaced by that number.

Changing L8 to L16 at fixed width changes watch-region hard velocity by at
most 6.05e-13 vdyn and action contrast by about2.30e-13 at final time. This
supports the chosen early-time exterior separation for these readouts and
the spherical constant-exterior-potential cancellation. Global U and W across
different boxes are not comparable as if the same total mass were enclosed.
No derived infinite-domain or late-time boundary condition is established.

At fixed comoving radius ell, the finest induced hard excess is only about
3.4433e-9 (R128) or3.4516e-9 (R8192) of the ordinary seed mass. At radius
ell/2 the hard/ordinary excess ratios are3.0216e-9 and3.4309e-9. These
are early-time density readouts, not observed lensing or a formed dark halo.
The inherited omitted ordinary-radiation H-squared fraction is about7.72e-5;
small absolute approximation debts cannot certify this much smaller
incremental gravitational signal.

## Unresolved central consistency and next certification

There is a concrete regular-origin discretization issue, not a failed time
integrator. In the cold runs the central action ratio is about1.0421 while
neighboring cells approach1.0538; the inward pressure magnitude at the first
face grows from2.8904e-7 to6.0092e-7 gstar when dx halves1/32 to1/64.
The shrinking central volume can make weighted fields converge while a
pointwise central derivative fails to do so. It must not be hidden by an
outcome-selected central mask.

An exact diagnostic explains why this can occur. For uniform density rho in
a smooth external potential phi=kappa*r^2/2, the initial first two cell-average
potentials differ by (36/35) kappa*dx^2. The first face's half-adjacent-mass
lump is4 times the first-cell mass. The present variational face force
therefore gives a1=-(27/35) kappa*dx, not the continuum -kappa*dx. This
relative origin-cell defect does not vanish as dx shrinks, although its
affected volume does. Energy consistency of the current semidiscrete method
is real; it alone does not ensure regular-origin consistency.

A prospective continuum version should first qualify regular affine radial
motion/harmonic forcing at the origin and the compact-source edge, using an
energy-consistent kinetic/spatial discretization—not an ad hoc force multiplier.
It should retain V001, declare observable norms and error targets before new
outcomes, repeat the width/domain/time ladder and include central pointwise
or clearly defined fixed-radius diagnostics. A consistent mass-matrix or
independently regular-origin finite-volume method is a possible construction,
not an implemented/qualified repair here. Until then keep
spatial_continuum_qualified=false, even though the weighted convergence is
useful evidence. Longer times additionally require characteristic/order and
shock-domain monitoring; full metric/lensing/merger claims require their
separate physical equations and error budgets.
