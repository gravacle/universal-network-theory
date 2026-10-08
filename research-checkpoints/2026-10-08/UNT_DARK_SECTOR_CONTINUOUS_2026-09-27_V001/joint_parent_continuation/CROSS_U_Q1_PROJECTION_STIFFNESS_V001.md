# S_cross critical Q1 projection-stiffness diagnostic V001

2026-10-06 UTC. Root-owned, bounded local numerical diagnostic. The running
NGC3198 recovery and coefficient calculation retain their ownership and
bytes. This independent manufactured-field calculation writes only its own
new prefix. It does not solve or repeat a galaxy trajectory. Ordinary mode;
no Goal, scheduler, automatic restart, physical-parameter fit or installation.

## Exact issue

The protected disk operator uses a continuous Q1 lapse and continuous Q1
native vector fields, with common positive cylindrical quadrature. Write K
for the scalar gradient form, M for the two-component vector mass form and
B for its gradient coupling, including the actual essential parity masks.
At the homogeneous zero field, the positive spectral weights sum to one.
Eliminating the native modal block gives the exact discrete scalar Hessian

    S_h = K - B^T (M + ell^2 K_vector)^-1 B + D_pressure.

Here K_vector includes the cylindrical radial connection z_R^2/R^2.
The phase-pressure contact is negative, and must not be clipped or removed.
Decompose the native part into

    Q_lock = K - B^T M^-1 B >= 0,
    Q_ell = B^T [M^-1 - (M + ell^2 K_vector)^-1] B >= 0.

Q_lock is the squared quadrature norm of the gradient projection error.
grad(Q1 lapse) is generally discontinuous between cells, and does not belong
to the continuous Q1 vector space. Thus a literal symmetric Jacobian and a
passing finite-difference test do not establish correct critical response.
Q_lock adds stiffness even at ell=0. At a nonzero state, the positive quartic
Hessian also enters the modal block; the present test deliberately isolates
the zero-field spatial defect and does not evaluate that nonlinear state.

For a uniform 1D P1 interior patch, theta=q*h,

    K=4 sin^2(theta/2)/h, M=h*(2+cos(theta))/3,
    |B|^2=sin^2(theta),
    Q_lock=4 sin^4(theta/2)/[h*(2+cos(theta))].

Its long-wave per-volume coefficient is h^2*q^4/12, compared with the native
ell^2*q^4/(1+ell^2*q^2). With radial h=.8 kpc and ell=.1 kpc the coefficient
ratio is 16/3. This analytic illustration is not a certified force bias on
the nonuniform cylindrical grid, nor a diagnosis of each current stall.

## Fixed numerical test

Authenticate the sealed V001 disk source and protocol. Use exactly its
edges(refine,128), shape_quadrature, interpolate and add definitions, with
refine=1 and 2, ell=.1 kpc, the same two-component essential masks, and no
change to any force operator, phase law, source data or running producer.
No measured velocities enter this calculation.

Use the three source-independent prospective directions already declared
in the disk protocol, p=2,3,4:

    psi=(1-R^2/128^2)^p*cos(pi*z/(2*128))^p,

and one fixed interior direction, zero outside 8<R<48 and .1<z<24 kpc:

    psi=sin(pi*(R-8)/40)^4*sin(pi*(z-.1)/23.9)^4.

Set essential outer scalar values to zero and normalize each nodal trial by
its maximum absolute value. Assemble K[psi], b=B*psi, and the literal vector
mass/gradient forms with the original four-point quadrature. Solve M*y=b
and (M+ell^2*K_vector)*y_ell=b using positive diagonal-preconditioned CG,
true relative residual <=1e-10, at most600 iterations. CG is used only on
these positive blocks; it is not used on the indefinite coupled galaxy
Hessian. Publish failures and incomplete directions rather than alter them.

Report K, projected energy, Q_lock, Q_ell, their ratios and refinement
changes for all eight direction/mesh cases, with actual linear residuals.
Verify literal matrix symmetry, an independently known SPD 2x2 solution,
and an unmasked R>0 affine-potential patch whose constant gradient is exactly
representable and whose cylindrical K integral is known independently. Also
evaluate the Schur energy identity by direct variational evaluation. Numerical
identity gates: symmetry<=2e-12, SPD solution<=2e-12, identity error<=1e-8
relative to K; affine K/projection errors<=2e-12. Nonnegativity tolerance1e-8*K addresses cancellation only;
it does not regularize the operator. There is no observational success gate.

Direct Schur identities alone are residual contractions, not independent
accuracy certificates. For each solve report its direct energy and a bound
on unresolved projection energy: r^T A^-1 r <= sum(r_i^2/Mdiag_i)/c,
c=(2-sqrt(3))/4. This conservative mass bound follows from the four-point
Q1 interpolation matrix (smallest squared singular value1/9), nodal squared
shape sum4/9, and min/max cylindrical quadrature weight>=2-sqrt(3).
Adding the positive ell energy preserves the mass lower bound. The exact
minimum lies between direct energy minus this bound and direct energy.
Report uncertainty on raw Schur energies and qualify ratios only when the
denominator exceeds that uncertainty plus the adopted numerical allowance
1e-8*K. The algebraic bound is exact in exact arithmetic; reported binary64
values and this allowance are numerical diagnostics, not rigorous intervals
for floating-point roundoff. Undefined/nonfinite diagnostics are explicit None;
seal failed partials before deriving them.

Exclusive manifest, per-case diagnostic checkpoints, result and receipt
bind source/protocol/input/output hashes. Do not overwrite existing files.
This short diagnostic has no automatic continuation. If interrupted,
recover its published case checkpoints and partial directions before a
new version or repeat. A completed test is progress, not a stopping point.

## Consequence and smallest faithful alternatives

If the projection stiffness is appreciable, a converged coarse disk still
requires a compatible-space or refinement comparison. Extending Newton
allowances does not correct this spatial defect. A possible faithful next
discretization keeps the nodal lapse/source/clock and uses broken Q1 modal
vectors with a symmetric interior-penalty representation of the SAME ell
gradient energy. Both consistency flux terms, positive coercive penalty,
axis regularity, cylindrical connection and parity/boundary terms are
required. A jump penalty alone would change the discretized PDE.

A matched staggered construction can also cancel the critical quadratic
exactly, but its scalar stiffness, modal mass/coupling and divergence must
come from one energy and one positive reconstruction. It needs a new scalar
source trace and cannot copy the old nodal sheet load. Neither approach may
clip the pressure susceptibility, change the quartic law, choose boundary
states from velocities, or turn an unconverged field into evidence.

The diagnostic does not establish a stationary galaxy, formation, stability,
full metric, FLRW junction, lensing, joint superiority or absence of dark
components. Its purpose is to remove a concrete numerical ambiguity on the
shortest route to the shared galaxy-and-expansion test.
