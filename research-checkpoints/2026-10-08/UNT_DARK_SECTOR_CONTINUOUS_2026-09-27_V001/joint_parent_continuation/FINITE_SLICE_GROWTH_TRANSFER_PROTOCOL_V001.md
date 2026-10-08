# Prospective finite-slice transfer census V001

Root alone freezes and executes finite_slice_growth_transfer_v001.py. No
source is imported or propagation performed by its author. This protocol
uses FINITE_SLICE_GROWTH_TRANSFER_DERIVATION_V001.md, including its corrected
degree-four free initial-dipole angular kernel. This is a new conditional
late-time initial-value test, not a primordial, CMB or observed-growth fit.

## Physical census and initialization

Retain all335 histories in the five authenticated BAO background results,
with their1,340 mechanical labels and18 old-reference mappings. Reference
calibration, BBN proxy and Pantheon/BAO exposure remain unchanged. There is
no new hard gap, abundance, initial power spectrum or physical oscillator
time. Preserve the matched vacuum and ordinary massless3.044 radiation.

For each history use k={0.0001,0.001,0.01,0.1} Mpc^-1 and A_i=101. Keep
both exact initial columns (Psi_i,Psi_i'/Hc_i)=(1,0),(0,1), with initial
common velocity, delta_j/(1+w_j) and shear-zero angular distribution given
by Eq4/5 of the derivation. Q=0 and soft-zero internal data are declared;
the preferred clock starts pi=0 and is reconstructed using cosmic pi_dot=Phi.
This two-dimensional subspace is NOT every allowed initial state or an
inferred growing mode. Unit normalization is not a physical unit perturbation.

Baryons are pressureless; ordinary photons and neutrinos collisionless and
massless on this finite interval. Their equal initial brightness remains
equal, allowing one angular distribution with the full combined ordinary
radiation density. This does not suppress their shear. It is not a precision
reionization, gas-pressure or massive-neutrino model. The same idealizations
apply to the pressureless hard/CDM comparator at the identical Hcal, Omega_m,
ordinary radiation and Omega_b. The comparator's baryon/hard contrasts
coincide exactly; at fixed background its transfer is independent of their
dust split, so a multi-history process may cache that solution with this
identity explicitly recorded. Each history still retains its own abundance.

Output epochs are A={101,81,61,41,21,11,6,3,2,1}, all included without
selection. Preserve signed potentials, Weyl/slip, species densities and
velocities, comoving contrasts, clock and Hamiltonian residual. Do not divide
through a zero contrast to create a spurious growth rate. No sigma8, f sigma8,
TT/TE/EE likelihood, initial-amplitude fit or observational-success gate.

## Numerical representation fixed before outcomes

Use the exact sealed BAO Kernel and Background definitions, authenticated
before import; no ancestor run/main is called. Evaluate the background at
each stage using x=t_i-t, t=log(r/r1), not an interpolated EOS. Integrate the
conformal-length scalar with d eta_bar/dx=lambda/(3aHbar), checking it against
fresh original-kernel Gauss64 integrals at every output. eta_bar=(Hcal/c)
(eta-eta_i), K=ck/Hcal. The clock is Pclock=Hcal*pi and its equation instead
uses lambda*Phi/(3Hbar). These normalizations must not be interchanged.

Radiation uses Ghat=exp(iK mu eta_bar)(F+4Phi), retaining even real and odd
imaginary parts on0<=mu<=1. Exact instantaneous moments determine Phi and
Phi' as in the derivation; no finite-difference metric derivative or low-l
closure is introduced. The fixed Gauss angle orders for increasing k are
{8,16,64,512}; doubled orders are {16,32,128,1024}. Before evolution evaluate
the logarithmic Gaussian derivative bound for every monomial through degree4
at the matter-lower-bound maximum streaming phase. Twice the sum of those
monomial bounds must be <=1e-12 for both orders. This is a kernel bound,
not a substitute for a coupled-solution convergence check.

Use explicit Dormand-Prince5(4) on the integrating-factor variables, with
maximum-component rather than dimension-diluted RMS error control. Coarse
rtol=1e-8, atol=1e-10; tight rtol=2e-9, atol=2e-11. Conformal-length component
uses rtol=2e-12, atol=2e-13 for both. Step changes use safety0.85 and factors
bounded to[0.2,4]. The initial x step is1e-3, maximum x step0.05. Hit every
declared output exactly; no dense-output interpolation. On top of adaptive
control, cap streaming phase to0.6 per coarse step and0.3 per tight step.
The conservative cap follows |dlog Hc/dx|<=1/2 and lambda/3<=1/2:
dx<=2 log[1+phase_cap*Hc_start/K]. No arbitrary wall-time/step-count cutoff.
Reject a step on error, not a physical instability; nonfinite arithmetic
or floating-point step underflow raises an explicit technical error. Root
retains that failed invocation and marks its history unfinished; a missing
science payload must not be labeled complete or discarded from the census.

Three complete propagations per k are retained: coarse time/base angle;
tight time/base angle; tight time/doubled angle (the reported primary).
All initial data and each run's output samples, step/error statistics and
actual timing remain. Time and angle comparisons are separate; the allowed
normalized maximum difference is3e-6, using max(1,max_epoch|primary|) for
each named observable and basis column. This floor is a stated absolute
transfer-unit convention, not division by a nearly cancelled final answer.
The two refinements use unchanged physical data.

Numerical controls also include:

- Synthetic DOPRI tableau/order checks and a complex-frequency scalar
  exponential against its exact solution, with tightened resolution.
- Exact EdS pressureless propagation of BOTH finite-slice metric columns,
  with zero ordinary-radiation density: Psi=Psi_i+(2/5)q_i[1-(a_i/a)^(5/2)],
  q=q_i(a_i/a)^(5/2). Reconstruct theta/delta from the exact constraints and
  compare the cosmic-clock integral too, at the same3e-6 transfer tolerance.
- Initial Hamiltonian/momentum/shear conditions, direct angular moments,
  positive normalized Gauss weights and exact polynomial moments through
  degree6: normalized2e-11 (not a radiation truncation).
- Independent radiation monopole/Euler moment identities and direct
  derivative of the shear relation: normalized2e-11 on fixed sample states.
- Propagated Hamiltonian residual normalized by the sum of absolute terms,
  with floor1: <=2e-7. This constraint is monitored, not solved away after
  each step. The shear/momentum reconstruction identities are labeled as
  algebraic, not independent Einstein tests.
- Conformal-time quadrature: phase error K*|eta_bar-eta_bar_quad|<=2e-8;
  primary/check background quadratures must agree to relative2e-11.
- Exact pressureless hard/baryon equality and finite-gap-to-dust identity
  for the inherited Delta=0 rows: normalized2e-11.

Large transfer gains do not fail a scientific gate. Report the largest
accepted-step sampled density, potential, velocity and preferred-clock tilt
per basis, and an illustrative0.01/max coefficient. This is neither a
continuous supremum bound nor a measured allowed primordial amplitude.

## Custody, benchmark and publication

The worker freezes all five original BAO result wrappers, their common freeze,
their flattened authenticated ancestors, this code/protocol/derivation and
the Q=0/physical-time interface notes. Verify raw hashes, payload hashes,
exact5x67 mapping, statuses and absence of producer-control failures. No
science producer runs during the freeze command.

The benchmark is the first finite-gap history in original background/record
order and ALL four k values, both columns, three resolutions and its matched
dust comparator. It is explicitly incomplete. Root inspects actual timing
and memory before full execution. Modes run-case0..334 publish one history
and comparator, allowing exact immutable per-history recovery; no result is
overwritten or silently skipped. The complete census is all335 histories,
not the benchmark or a successful subset. Source-only technical packaging
changes require separate versioning if frozen; no outcome-based tolerance,
k, state or resolution change is permitted.

Output is stdout only; no packages, network calls or hidden writes. Set
threads1 before NumPy. Retain ordinary JSON for all samples and scalars; no
335-fold covariance or unrelated data is duplicated. No numerical worker
has run when this protocol is authored.
