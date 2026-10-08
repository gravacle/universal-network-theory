# Finite-time spherical dust shadow: prospective protocol V001

2026-09-29. Root alone runs `spherical_dust_shadow_v001.py`. No old source,
state, energy or calibration is edited. This is a finite-time moving-source
method control plus a finite-R residual census, NOT a finite-R trajectory,
an observed halo/lens, a disk replacement or a merger continuation.

## Fixed preparation and complete census

Use exactly the two R=128,8192 spectrum1/reference0 states already present in
the authenticated smooth-disk certificate; collapse only its duplicate disk
thickness labels. Check that every retained source-state field agrees across
those duplicates. The old states remain method controls, not a selected
successful cosmological posterior. Keep their I,e,p,cI2,gstar,Kb,DeltaU,Hcal,
Omega_b,Omega_exc and Omega_Lambda. No new hard abundance or action is fitted.

The NEW ordinary seed is the normalized compact spherical polynomial in
SPHERICAL_SAME_STATE_RELEASE_REDUCTION_V001.md, ell=3.2 kpc and
GM=gstar ell^2. Hard action is initially uniform and both peculiar velocities
vanish. The ordinary seed evolves with the shadow; it is never held fixed.
The late background is exactly the inherited ordinary-dust + finite-R hard
energy + matched-vacuum convention. Ordinary radiation is intentionally absent
from that old background, and its saved-photon/massless-neutrino omission
scale is reported separately, not silently added or fitted away.

Evolve all shells z=q/ell=0,1/16,...,16. This is an output/parameter sampling,
not a radial finite-difference grid: the exact spherical dust shell equation
and its two mu sensitivities evolve independently on the common background.
No finite outer boundary enters their generator. Initial labelled worldtubes
z={1,2,4,8,16} give finite enclosed mass/current ledgers. Sample times are
tau={0,1/64,1/32,1/16} in t_dyn=sqrt(ell/gstar) units, chosen before execution.

## Numerical methods and qualification

Propagate the shell ODE and analytic first/second parameter sensitivities by
RK4 with fixed maximum steps 1/512 and 1/1024 and, independently, adaptive
Dormand-Prince5(4) with rtol=2e-11, atol=2e-13 and step cap1/256.
All three final/sample vectors are retained. No numerical criterion selects
a preferred physical gap or end time. A violated positive f or f+z f_z ends
that trajectory with its failure state preserved, not an artificial reset.

Numerical comparison tolerance is 2e-8 after scaling each state channel by
max(1, its two compared magnitudes). Density and pressure-residual readouts
use 2e-7 with the same explicit scale; these are numerical method comparisons,
not a physical accuracy assertion relative to a tiny halo signal. Arithmetic
identities use 2e-11. Stable zero-source material quadrature uses128 nodes;
64 nodes independently check all fixed sample readouts at2e-10. Actions are
inverted by64 positive-bracket bisections, with no EOS table interpolation.
The previously qualified saved energy/pressure/omega/cI2 are explicit anchors.

Controls: compact source normalization and derivative identities; exact
homogeneous f=1 solution; pressureless homogeneous-sphere first-integral
control with H=kappa=0; analytic parameter sensitivities against symmetric
mu differences at1e-4 and5e-5 (fourth-order extrapolation); material action,
virial and derivative identities; every common-flow mass/current ratio; all
time-method/sample comparisons. Derivative finite-difference tolerance2e-6
is separate from arithmetic controls and never replaces the analytic jets.
The sphere energy control evaluates f_tau^2/2-mu/f+mu, with tolerance2e-8.

Retain the fine RK4 path at all65 time nodes for forcing integration and
sampled extrema. Evaluate the *same* finite-R material at I=I1/(A^3 J),
including the finite pressure and energy not used by the dust generator.
Compare trapezoidal forcing integrals using every fine node versus alternate
nodes descriptively; do not turn that quadrature into a certified fluid error.
All physical result arrays and signed source terms are preserved, not clipped.

## Readouts and strict scope

For every fixed sample store A,H,f,f_tau,f_mu,f_mumu,J,J_z, the two current
densities, retained I,e,p,omega,cI2, exact Newtonian sound coefficient,
signed pressure acceleration, e/(RI)-1,omega/R-1, peculiar v^2/c^2 and both
finite-worldtube excess mass ledgers. Include the initial compactness, current
same-flow ratio, late radiation/H^2 omission fraction, and the coefficient
converting a radiation brightness bound to omitted active mass.

Integrate absolute pressure forcing with the free Hubble-damped velocity and
displacement kernels. Also retain signed pressure-source work along the shadow.
These are accumulated diagnostics. The actual two-fluid Lipschitz/force tube
needed for equation(9) of the reduction remains UNPROVED. Output explicitly
`finite_R_trajectory_qualified=false`; a small residual must not change it.

Likewise retain sampled shell/Jacobian minima and characteristic travel using
the shadow sound speed. These are not continuous-in-time bounds for an actual
finite-R solution. The shadow has no finite outer wall; possible finite-R
interfaces8ell,16ell and watch radius4ell are only prospective non-arrival
diagnostics. Exterior/metric/radiation bounds require their actual hypotheses.
Do not apply the dust separation bound to finite-pressure material.

No ray tracing or full null observable is executed. Enclosed rest-mass excess
is labeled as such, separately from internal/active stress. A future finite
worldtube Born contribution requires its projection and omitted exterior,
metric/slip/flight-time control. A full observed lens cannot be declared from
this result. No desired-sign, halo-size or observational acceptance gate exists.

If the residual does not permit an owned error tube, proceed to the conservative
two-current finite-R system in the reduction, retaining its own boundary flux,
pressure work, acoustic domain, numerical refinement and classical-domain tests.
Do not repeat dust shadows with outcome-selected endpoints to avoid that solver.

## Custody and execution

The worker validates the exact saved certificate wrapper/payload/freeze and all
transitive files, plus the raw photon-reference receipt and the new source,
protocol and reduction. It imports no producer. Threads are fixed to one;
only NumPy/stdlib are used. `freeze` prints the snapshot. Root publishes it as
SPHERICAL_DUST_SHADOW_V001_FROZEN.json. `run` requires exact snapshot equality
and prints one complete canonical result wrapper, never writes a file or
launches another process. Any unfinished domain/method case is retained with
its last state; numerical failures are not a physical rejection. There is no
arbitrary wall deadline and no author execution.
