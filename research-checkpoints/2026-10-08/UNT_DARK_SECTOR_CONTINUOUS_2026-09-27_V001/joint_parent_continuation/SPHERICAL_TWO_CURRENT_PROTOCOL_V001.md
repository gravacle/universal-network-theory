# Conservative finite-R two-current release: prospective protocol V001

Inert source/design qualification; no producer or quadrature was executed by the
author. Root alone freezes and runs. This is an actual finite-pressure solution
of the declared cold, weak-field two-current action reduction, not an exact GR
solution, halo fit, lensing observable, collision model or pressure-residual
substitution. Existing shadow and all earlier failed/qualified runs are intact.

## Inputs and fixed census

`spherical_two_current_v001.py` authenticates the complete saved spherical
shadow result, its freeze and result review; recursively binds every member of
the shadow freeze; and binds its own source, design and this protocol. It imports
no earlier producer. The smooth-release coefficient receipt is already a member
of that frozen ancestry. Each input uses the exact original spec1/ref0 state at
R=128 or8192, beta=.005, ell=3.2kpc, compact polynomial baryon seed of unit mass,
initial uniform cosmic hard action, and the inherited baryon/hard/vacuum
background. There is no parameter/phase-profile selection after these outcomes.

The ordered census is R=[128,8192], L=[8,16], dx=[1/16,1/32,1/64], nested in that
order:12 cases,128 through1024 cells per species. L is an exterior numerical
interface, not a halo size. Times are0,1/64,1/32,1/16 in the already defined
dynamical unit; watch radius is4. Root runs case0 first to measure actual cost,
then retains every completed, failed or unstarted case. Any change to this
prospective source/settings after an outcome requires an additive repair.

## Semidiscrete equations and material

The accompanying design gives the full equations. Each species has its own
ordered moving spherical cell mesh and fixed positive cell masses; cell action
is fixed by its hard mass, exact volume and A^-3. Face masses are half the
adjacent cell masses, with the last half-cell at the outer face and the origin
fixed. Canonical momenta are A*w*v. There is no Eulerian remap, density floor,
artificial viscosity, mass exchange or phenomenological hard profile.

The scalar zero-source quartic material is evaluated from its exact action,
period and moment integrals using64-point Gauss-Legendre primary quadrature.
128 points independently checks every saved material sample. Dimensionless
amplitude-squared r has bracket[2i/sqrt(1+2i),2i], i=I/R^3; eight safeguarded
Newton steps use the analytical action derivative(1+r)/(2Omega). The recovered
action must agree to relative2e-11; failure is retained, never silently used.
There is no EOS interpolation. Stable Omega-1 and dE=Omega-1-p/(RI) retain the
R8192 internal/pressure scale without subtracting nearly equal unit energies.
The actual nonrelativistic sound speed is cN²=(omega/R)cI²c², not cI²c².

Pressure force is the exact derivative of the retained finite-cell internal
energy. Gravity is the exact derivative of the same piecewise-constant
two-species self/background energy; a sorted union of the two meshes evaluates
all potential integrals and face derivatives without a dense pair matrix.
NumPy longdouble accumulators are used internally for potential sums/differences;
their actual mantissa width is reported, not presumed portable extended
precision. Published state numbers remain ordinary doubles. Constant spherical
exterior potentials cancel from interior force derivatives.

The hard outer traction is the same homogeneous pressure at that A. It is a
declared conditional boundary, not an impermeable fixed wall. The origin is
regular with zero face velocity; no artificial inner sink is introduced.

## Prior domain and numerical integration

Stage guards require finite ordered positive volumes, A>=1 within2e-14 roundoff,
|v|<=2, hard I/Ibar(A) in[.25,4], and each cell V/Vinitial in[.25,4]. No stage
is clipped. A violation, including an intermediate numerical trial, returns an
unfinished retained case rather than a physical exclusion or a hidden smaller
step retry. The exact zero-source bound eII<=1/R² supplies the prior speed bound
2+sqrt(4I1/(R³epsilon)). Before evolution require T times this bound less than
L-2T-4. It supplies a conditional continuum exterior-domain bound while the
guards hold; checking discrete stages is not a rigorous interval theorem.

The primary fixed-step RK4 uses half of
min(1/1024,.15*dx/prior_speed). Coarse RK4 uses that full step. Independent
Dormand-Prince5(4), rtol2e-11/atol2e-13, cannot exceed the same full step. Each
method lands on the four times exactly. Canonical momentum errors are scaled by
the inverse face mass, so a tiny cosmic density cannot hide velocity error;
hard-specific work integrals likewise scale by the inverse total hard mass.
This is a conservative CFL/time cap, not a proof against shell crossing.

## Prospective checks, not physical-success thresholds

Before the first trajectory, require homogeneous gravity and pressure nulls,
unit compact-seed mass, rest/action normalization and the same saved material
anchors. Directional gravity-energy derivatives are checked jointly and per
species/per unit mass. A separate nonuniform hard-mesh control checks the
pressure/internal-energy derivative. Central differences at1e-4 and5e-5 are
Richardson-combined; derivative tolerance is2e-6 in the stated dimensionless
per-mass scale, without selecting signs. Failed prerequisites stop before
physical evolution. These derivative tests evaluate only this owned numerical
operator, not a galaxy observation.

Arithmetic tolerance is2e-11; same material and64/128 comparisons use relative
2e-10. Time state comparisons use2e-8 scaled by max(1,magnitude), with independent
velocity, volume and action-ratio comparisons at2e-7. The primary saved material
also checks recovered action, enthalpy/virial identity and the exact sound upper
bound. Total and mechanical energy/work defects use2e-7 with max(1,magnitude)
normalization; the hard mechanical ledger is additionally tested per hard rest
mass, preventing the small hard mass from hiding its pressure-work error.
Fixed-label masses must agree at arithmetic tolerance. All counts, maxima and
failures are retained; numerical entries are not independent physical tests.

The ten integrated ledger entries, in order, are total gravitational mechanical
work, outer traction work, Hubble work on K+U, Hubble work on W, their predicted
total-action-energy change, characteristic travel diagnostic, pressure-kick
work, hard gravitational work, hard Hubble K+U work and complete hard mechanical
work. The same discrete energy gives both forces and these budgets. Homogeneous
internal energy is shown separately, never silently dropped from the ledger.

An additional pressure-off RK4 control removes only the pressure kick, retains
the identical background, and compares both discrete meshes against the old
saved shadow at its shared1/16 labels. This is descriptive spatial-method
evidence. It is not called the actual finite-R trajectory, and its unphysical
pressure/internal-energy budget is not used to qualify the full fluid.

## Saved outputs and spatial qualification

Each case retains all three time-method state vectors, primary snapshots for
both species including densities, masses, velocities, accelerations and
gradients; all material/pressure fields; action ratios; energies and signed work;
time/material controls; worst stage guards; root errors; dust-control signed
differences; physical units; inherited radiation omissions and measured runtime
and self RSS. Errors retain their traceback, last or failing state and completed
method vectors. A nonfinite failing state is retained losslessly as explicit
little-endian IEEE754 bytes plus a JSON display with null nonfinite entries;
nonfinite control values remain failures, never a passing zero. A model-domain
construction failure is caught as its own retained case. No producer-owned file
writes, subprocesses, checkpoint edits or
compiler calls are present. `freeze` and `run-case INDEX` print JSON only; root
must preserve complete stdout through its existing lossless capture mechanism.

A completed case is only a qualified semidiscrete/time/material calculation.
Its `spatial_continuum_qualified` flag remains false. A subsequent saved-array
collector must compare all three widths at common physical positions/labels,
retain signed density, velocity, pressure, mass and energy differences and
observed orders, and compare identical widths across both L values inside the
watch region. No spatial accuracy/success cutoff is invented here. Poor or
non-monotone spatial behavior, steepening, guard failure or broken ordering
must remain visible; there is no post-shock extension. No continuum or
finite-R physical inference follows merely from a passing time-integrator test.

The reduction omits relativistic inertial/active-gravity corrections and ordinary
radiation from its inherited late-time generator. It reports dE, enthalpy and
active-stress corrections, velocities, potential span and the owned radiation
budget separately. Their small absolute values do not prove precision for a
much smaller incremental lensing signal. The result is neither observed lensing
nor a claim that a galactic state has formed or equilibrated. It does not solve
the full nonlinear Einstein initial constraints or evolve a same-metric Weyl
observable: initial flat-volume/Newtonian constraint errors remain part of the
stated weak-field reduction, not an exact CMC-to-observation identification.
