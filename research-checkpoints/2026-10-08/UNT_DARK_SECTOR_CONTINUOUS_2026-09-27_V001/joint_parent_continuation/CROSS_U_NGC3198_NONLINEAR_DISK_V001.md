# S_cross shared-law measured NGC3198 disk: first nonlinear solve V001

2026-10-06 UTC. Prospective root-owned local calculation on this Mac. This
uses V003 Eq5, the already specified independent-polarization S_cross action.
It preserves S_dual results as evidence for a distinct action. No Goal,
heartbeat, scheduler, automatic resubmission or new coordination system.

The uncompressed homogeneous action is the same EH+P(X)+ordinary action as
the current epsilon comparison. Hold its physical A/I0/Q0, ordinary inventory,
Hstar, rG=.98/.99 and background charge solution fixed. All four global
epsilons 1e-6,1e-5,1e-4,1e-3 are retained; none is selected by this test.
Background supernova distances transfer; perturbation and formation
qualifications do not. Mbare²C=2MN², C=1.98, ell=100pc, and gc=3pi a0/8.
a0=1.0059833281731022e-10 m/s². This is an effective calibrated action with
disclosed functional and state assumptions, not a microscopic derivation.

## Equations, units and physical approximation

Aligned U, phi=omega*t, no phase/mode transients, local finite outer lapse and
all modal fields fixed to their homogeneous values. Native modes are two
independent meridional vector components. In L0=1kpc, acceleration unit a0,
write logN=B*psi, B=a0 L0/c², X/Q0=qbar*exp(-B*psi). All charged P(X)
values must remain strictly inside 1<(X/Q0)²<1+eps at every nodal and
quadrature state, including every accepted Newton step. No clipping.

The leading static lapse equation, including active phase pressure, is

    div(grad psi-Z)=kappa*(delta rho_norm+3 delta P_norm)+sheet,
    -ell² Delta_vector z_j+z_j+|z_j|²z_j/(gc² xi_j^4)=grad psi,
    Z=sum_j w_j z_j, kappa=2 Hstar_SI² L0/(C a0).

The density unit is 2Mbare²Hstar². No second .99 factor multiplies the source.
P(X) and its conserved outer charge are the actual saved law. Cancellation-
safe differences are algebraically identical to it. The static source
Jacobian is -kappa B(D_phi_norm+3W_norm), retaining its negative curvature.
This is a weak metric lapse problem: native quadratic Hilbert stresses,
unenhanced background curvature contacts and the full spatial Einstein
metric are not silently treated as solved. Report max|logN| and phase source
sizes. The exact finite-pressure bound is
|delta P|<=eps/[4+3eps+4sqrt(1+eps)] |delta rho|.
The full FLRW junction, conserved exterior current, selected formation and
stability are remaining physical qualifications, not fitted interior halos.

At the axis: z_R=0 and natural normal derivative of psi,z_z zero.
At the sheet: z_z=0 and natural derivative of z_R zero. The sheet appears
only in the metric load, with F_z(0+)=2pi GN Sigma/a0. The poloidal vector
gradient energy includes z_R²/R². At both remote faces psi=z_R=z_z=0;
that finite wall is a disclosed prepared state, not an exact isolated
cosmological exterior. No old arbitrary potential-offset boundary is used.

## Source, observable and numerical contract

Use all four existing HI/H2 tail variants from galaxy_density.py and the
unchanged source-data part of NGC3198_FIXED_DENSITY_PROTOCOL.md. Keep all
24 HI,23 stellar and10 measured H2 profile entries, the original distance,
helium and M/L conventions. The old AQUAL law/numerical physics in that
protocol do not transfer. Source interpolation, missing entries, tails,
warp, thinness and measurement exposure remain disclosed. Integrate R Sigma
against each linear plane basis with 16-point quadrature split at every
measurement knot; compare 32-point and exact annular total (<=1e-11 relative).
Use all43 existing rotation rows/errors, without fitting a source or deleting
rows. Velocity residuals are descriptive, not a covariance-qualified likelihood.
No observational success threshold or favorable outcome selection exists.

Use axisymmetric Q1 fields, common positive 2x2 quadrature for the residual,
contact and its symmetric Hessian, with 32 positive spectral nodes and
weights w=2xi dxi. Numerically store modal variables sqrt(w_j)z_j. The coarse
radial mesh is 0..2kpc in .2kpc steps,2..50 in .8kpc steps, then16 geometric
nodes51..128kpc. Vertical mesh is0..1 in .05kpc steps, then24 geometric nodes
1.08..128kpc. This first solve is explicitly UNQUALIFIED for resolution,
quadrature/exterior sensitivity, full metric, formation or superiority.
It is an actual nonlinear measured-source calculation rather than an old-law
force proxy. Subsequent useful work is mesh refinement (halve inner spacings
and double outer nodes), modal quadrature comparison16/32, and independent
outer extent256kpc with matched inner mesh, retaining every outcome.

Start every case at the unchanged homogeneous zero field. Solve the declared
stationary residual, allowing an indefinite Hessian. BiCGSTAB uses positive
absolute-diagonal symmetric preconditioning only; it does not alter the
physical operator. Max600 inner iterations, max30 Newton updates, residual
target1e-8 relative to the initial preconditioned source norm. Inner target
min(.001,max(1e-10,.05sqrt(current error))). Accepted steps must reduce the
same current residual merit by the fixed Armijo criterion1e-4 and remain
inside P(X); max32 half-step trials. Failure or a singular/broken linear
recurrence is saved as numerical branch failure, not an all-UNT exclusion.
Three declared source-independent trial directions test the actual Hessian:
q_p=(1-R²/Rwall²)^p cos(pi z/(2Zwall))^p, p=2,3,4,
with modal direction=grad scalar and actual parity.
Negative curvature certifies an unstable stationary energy direction;
positive sampled directions do not certify stability. Do not force SPD.

All16 eps/tail cases are retained. The root performs numerical execution;
other agents review source and saved results only. Publish the source/input
manifest before calculation, and exclusive authenticated complete field and
history checkpoints at zero and after each accepted Newton step. Preserve
failed linear histories in each case result. Any interruption must first
recover the latest authenticated accepted state and inspect partial work;
this V001 has no automatic resume/replay loop. A later recovery must preserve
the partial Krylov attempt and reconstruct its unfinished linear solve from
the saved accepted state, not restart completed cases. Root must save the
exact next action in the existing continuation log before an execution
boundary. No reliable duration or successful galaxy result is promised.

Before the first source solve, qualify the shared nonlinear Jacobian by a
central finite difference (relative error<=1e-7), its adjoint symmetry
(<=2e-12), and the indefinite BiCGSTAB solver on an independently known
2x2 saddle solution (<=2e-12). These are numerical implementation controls,
not new observational evidence. Report outer metric face flux against the
sheet plus signed clock-volume source; it is a coarse discretization
diagnostic and is not automatically forced to pass. Retain all-row, R>=2
and R>=8 descriptive RMS and nominal error-weighted residuals.

The velocity readout is the nodal midplane derivative reconstructed with
np.gradient(edge_order=2), then linearly interpolated at all43 radii. This
readout also needs spatial convergence; it is not the exact cellwise Q1
derivative. Shared2x2 quadrature defines a consistent discrete variational
functional but does not exactly integrate its quartic potential. A later
integration-order check is required as well as mesh/mode/outer checks.
Save the positive native normal-density scale, acceleration coupling scale,
and its integrated Gauss-source size relative to sheet source as concrete
weak metric remainder diagnostics. Those are not the full spatial-stress
bound. Bind every field checkpoint and commit in the final receipt. A
completed batch with any unresolved branch residual exits3 and explicitly
reports retained numerical failures; residual convergence alone does not
change any physical qualification flag.
