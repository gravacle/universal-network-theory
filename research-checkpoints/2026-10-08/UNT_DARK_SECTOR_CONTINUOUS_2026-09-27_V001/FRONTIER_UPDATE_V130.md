# Frontier V130 Shared model tests and source averaging

2026-10-04, approximately 23:38 UTC. V009 continuation. All eleven lanes
remain OPEN in ledger V071. No overall superiority or Stage 3 completion.
All paths below are in joint_parent_continuation unless otherwise stated.

## New completed science

GEOMETRIC_GRADIENT_EXPANSION_V001 derives a changed covariant gradient that
preserves aligned static equations but adds J|K.y|^2/2 during expansion.
Independent algebra and nine arithmetic checks pass. Nonzero stationary
modes require H ell/c>1; at ell100pc and illustrative H70 the squared ratio
is5.4519853e-16. Positive-energy bounds prevent large prepared amplitudes
from hiding this small coupling. A larger curvature-only length does not
give the instantaneous-minimum, kinetic-neglected branch an arbitrarily hot
positive-density past. No inference against all nonadiabatic histories or
UNT is made. Do not repeat this with an inertia or coefficient sweep.

FILTERED_SOURCE_SHARED_CANDIDATE_V001 is a NEW effective static action:
b=S gradPhi, S=(1-ell^2 laplacian)^(-1), followed by the old bounded h(b).
Variation gives D=g-S F(Sg), with BOTH filters and the complete source
contact retained. Its kernel/state/covariant completion are assumed, not
native-derived. Inputs are the old exposed a0=1.0059833281731022e-10,
r=25.51664211557329 and development ell100pc; no new fit occurred.

All29 controls in the new linear Solar test pass in0.0521s. The coefficient
is Cq=.0133029565427473, giving Q2_linear=6.00908255800142e-38 s^-2.

FILTERED_SOURCE_NONLINEAR_BOUND_V001 supplies a stronger result: a complete
nonlinear Gaussian-source bound, sigma1e9m, external field2.32e-10 m/s^2.
Wiener-space contraction is uniform through the soft spectrum. All8 fixed
arithmetic gates pass, L_F=.6478841743, solution norm<=2.4310165e-6, and

    |Q2| <= 1.184193605291823e-34 s^-2.

This bounds the whole anomalous tidal field, not merely a linear remainder.
Existence/uniqueness is within the declared small ball, not globally among
all states. Both endpoint_equations_check and handoff_plan_review_v005
independently accepted the analytic proof; neither reran numerics. The
second reviewer additionally checked continuum integrability and the
background-subtracted variational interpretation. This is not an actual
Solar ephemeris, photon-metric, formation or causal-stability qualification.

The filter preserves the old finite uniform-source endpoint difference.
With its explicit high-field zero-action matching postulate, the retained
vacuum scale at the later a0 is H_vac=50.3528974592 km/s/Mpc. This is NOT
H_today or independent validation: r was originally expansion-calibrated.
The physical absolute-energy matching remains an assumption.

Root and endpoint reviewer also derive the FORMAL isolated far-field result

    v^2=sqrt(GMa0)+[(32/(9pi^2)-1/r^2)GM-2a0ell^2]/R+o(1/R).

It is not an isolated-source existence/remainder theorem or observed-disk
score. Previous100pc Plummer solves belong to the other, linear-source
gradient parent. Both candidates and their different predictions remain.

## Shared cosmology and sparsity remain unclosed

A purely spatial filter leaves the aligned unexcited FLRW branch with
H^2=L+B(1+z)^3+R_rad(1+z)^4+K(1+z)^2. Reuse COSMOLOGY_CLOSURE_TEST_V001:
the already identified conditional matter-era shortfall remains. Restoring
a vacuum endpoint does not supply an owned state/formation/metric law.
Do not repeat its old arithmetic or insert a free abundance unnoticed.

The user asks whether network sparsity at galaxy/cosmic boundaries is actually
understood. It is NOT yet operationally identified. Low acceleration and an
assumed ell are proxies, not measured graph sparsity. Distinguish ordinary
matter density, link degree, correlation length/history, source-weighted
response spectrum and graph volume/spectral dimension. The observable
cosmic horizon is not evidence of a physical low-density network edge.
Galaxy gas also does not end at the last rotation datum. The saved DDO154
profile extends beyond its rotation sample. No common boundary transition
has been derived or measured by this program.

## Custody and next action

Result SHA256 values:

- GEOMETRIC_GRADIENT_EXPANSION_V001_RESULT.json:
  fcec033e8cbf33090c4b58309a1864c7c52ee2fbe05c6c4b5845d1917d200941
- FILTERED_SOURCE_SHARED_CANDIDATE_V001_RESULT.json:
  d25a8aaedef6f51afb246c7a720b3c3fe02089a64d3a1dddf6a723b1675ba015
- FILTERED_SOURCE_NONLINEAR_BOUND_V001_RESULT.json:
  3317646ee61c629c2e4a370c2eb63ff17fb403abf503bc5c0f1cb7154175bd23

All numerical and review workers complete; numerical slot FREE. Heartbeat
freshly checked PAUSED, separate Goal unchanged. No install, other Mac,
heavy/remote job, credit action or publication. Usage-failed old agents were
not restarted. Dirty canonical URM/sealed artifacts preserved; development
V049 only. Source/result files are saved without overwrites.

Next shared-model work must identify one explicit physical state variable
and source-conditioned temporal or metric law, not equate low density with
low acceleration. Specify its effect on both clock and optical response,
its conservation/source work and formation rule. Derive the homogeneous
constraint before a parameter fit or SN/BAO rerun. A matched-acceleration,
different-environment galaxy comparison is a useful discriminator only
after the proposed state law predicts the sign and size of its effect.
Keep actual-source galaxy/optical testing secondary to that shared-law gap.
