# Smooth-disk release certificate: prospective protocol V001

2026-09-29. Source/protocol before execution. Root is the sole producer.
The worker is `smooth_disk_release_certificate_v001.py`; no old source or
saved result is modified. This is an initial constraint/response certificate,
not a finite-time galaxy evolution, a reconstructed metric or a data fit.

## Complete state and source census

Use spectrum index 1 and reference 0 from the authenticated finite-gap V002
screen, retaining both R=128 and 8192 states with their original I, omega,
eII, energy, pressure, gstar, finite-spectrum DeltaU and background reference.
They are METHOD CONTROLS, not newly viable joint BBN/cosmological candidates.
No action rephasing, zeroing of energy or substitution of ground populations.

Keep a=3.2 kpc, GM=gstar*a^2 and both new synthetic thicknesses b/a=1/8,1/16.
These are physical source alternatives, not convergence copies or measured
disk thicknesses. Use all R_coordinate/a={0,1/2,1,2} and z/a={0,1/4,1/2,1}:
four state/thickness cases, 16 witnesses each, 64 physical readouts. Geometry
is evaluated once per thickness, then mapped without a repeated solve.

The seed is nonrotating ordinary rest mass initially comoving with the
cosmic normal, not a supported disk or a permanently imposed potential.
CMC K_ij=-(H/c)gamma_ij, zero free TT/shear data, uniform physical hard I,
zero spatial hard phase gradient, zero soft modes, and the independent
geodesic preferred clock fix the initial state. Ordinary homogeneous matter,
hard pressure and matched vacuum remain in the background. No finite-time
matter, phase, geometry or clock evolution is executed here.

## Exact formulas and independent controls

The proof is `SMOOTH_DISK_CLOSED_RELEASE_ORACLES_V001.md`, pinned SHA256
`5f5f2985167b47751aeceb78b823fb327aa58074b58e18a6d8856cd32bc7f7aa`.
`SMOOTH_RELEASE_CURRENT_BOUND_ADDENDUM_V001.md` supplies the independently
checked gradient bounds. The exact conformal constraint has a unique positive
asymptotic solution when U<1. The worker certifies that condition and its
brackets; psi=1+u remains a first iterate with a NONZERO recorded constraint
residual. No claim of a numerical psi reconstruction is made.

All elementary geometry calculations are dimensionless before SI conversion.
The explicit analytic potential gradient/Hessian is independent of a small
two-coordinate second-order chain-rule implementation. That implementation
also differentiates the positive density for the current coefficients.
Synthetic polynomial/fractional-power checks qualify the chain rule.

Fourth-order finite differences independently check both fields' two first
and three second derivatives at h/a=2^-10 and 2^-11, all witnesses retained.
The scalar source is continued evenly in Cartesian x through x=0; cylindrical
Delta D=D_RR+D_R/R+D_zz uses 2D_RR+D_zz exactly on the axis. Neither step
is silently selected. The full discrepancies and derivative estimates are
saved even if a control fails.

Fixed arithmetic tolerance: 2e-11. Fixed FD tolerance: 1e-6. Scaled errors
use max(the explicit contribution scale, absolute analytic component).
Potential gradient scale is 1, potential Hessian scale is the analytical
dimensionless tidal bound 1/[bbar(1+bbar)^2]. Density scales are Dmax/bbar
and Dmax/bbar^2. Thus zero components do not create singular relative tests,
and the scale is determined by the declared source before any outcome.
The two steps are independent derivative controls, not a rigorous finite-
difference error theorem or a posteriori tolerance change.

Exact controls include positive density, global density/tidal bounds, origin
vertical curvature, the Poisson trace, cylindrical regularity, inherited
action-pressure and sound-speed identities, excitation/vacuum cosmological
normalizations, and the explicit first-iterate Hamiltonian residual. The
momentum constraint vanishes by the declared initial data, not a numerical
small-residual claim. Density/pressure units retain c^2 explicitly.

Total rest mass M is exact from the source's asymptotic Poisson flux. As
elementary finite-radius controls only, use dimensionless radius 1024 and
angles 0,pi/4,pi/2. The normalized radial flux obeys

    [r/(r+1+bbar)]^3 <= r^2 phi_r/(GM) <= 1+1/r.

These bounds tend to one; a finite spherical flux is not called the full
mass or used to truncate the infinite positive source.

## What is read out

For every case/witness retain the source and potential, gradient/Hessian,
psi bracket, exact focusing interval, hard density/pressure tau^2 intervals,
and initial tau^3 orthonormal velocity and tau^4 normalized canonical-current
coefficients with the addendum's rigorous metric-error bounds. Signed
Laplacian/current intervals are not clipped. These are Taylor COEFFICIENTS
at the initial slice, not finite-tau predictions with an assumed remainder.

Record L_N and the separate frozen Newtonian-source central caustic/sufficient
times. Explicitly mark the ACTUAL evolving system's interval caustic status
as unevaluated: an initial tidal bound cannot be used as an interval bound.
The point-mass vacuum tau^4 coefficient is a separate algebraic oracle.

The worker retains all outcomes and reports FAILED_CHECKS if any prospective
control fails. An unqualified contraction domain is not silently evolved or
replaced. There is no physical desired-sign, response-size or observational
acceptance threshold. Inferred joint states can later reuse the geometry
and same bounds through a separate complete saved-arithmetic census.

## Custody and execution

Only stdlib is used. No scientific producer is imported, and there is no
orbit inversion, quadrature, eigensolve, constraint PDE or time propagation.
The inherited transport bytes, decompressed payload hash, wrapper/freeze and
recursive source ancestors are checked. The global reference result, source,
protocol and both new proofs are included in the snapshot, with paths
confined to the project root. Run mode requires exact snapshot equality.

`freeze` prints the entire source snapshot to stdout; root publishes it with
apply_patch as `SMOOTH_DISK_RELEASE_CERTIFICATE_V001_FROZEN.json`. `run`
prints a complete result wrapper, canonical payload SHA and freeze SHA to
stdout. Root publishes it as `SMOOTH_DISK_RELEASE_CERTIFICATE_V001_RESULTS.json`.
The worker writes no file. Root inspects payload status, not merely process
exit. No science execution is performed by the author or preflight reviewer.

Constants are computational SI normalizations: c=299792458 m/s,
G=6.67430e-11 m^3 kg^-1 s^-2 and pc=3.085677581491367e16 m. They are not
independently fitted inputs; no new precision claim or uncertainty likelihood
is inferred from their displayed digits. The incomplete native source/clock
dictionary and the rapid-averaging premise of the adopted hard-fluid action
remain distinct from these exact conditional initial-state bounds.
