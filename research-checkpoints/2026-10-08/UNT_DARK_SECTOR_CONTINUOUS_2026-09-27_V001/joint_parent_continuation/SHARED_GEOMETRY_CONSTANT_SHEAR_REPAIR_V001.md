# A constant shear repair does not close the shared action

2026-10-04. Analytic extension of SHARED_GEOMETRY_KINETIC_SCREEN_V001.
This tests a concrete repair, rather than assuming that the earlier scalar
failure excludes all network explanations. No numerical fit or worker is
needed. The result was independently rederived by handoff_plan_review_v005.

Add beta (Kij Kij - K^2/3) to the saved preferred-foliation action. It vanishes
on aligned FLRW and on the stationary Kij=0 galaxy branch. Thus it is a
plausible one-constant way to change perturbations without changing those
background equations. Beta is a new adjustable constant, not a native result.

Let alpha=1+beta and lambda_0 be the old effective trace coefficient. Shift
elimination in the same principal subhorizon window gives

    C_zeta = 2(1+beta)(3lambda_0-1)/(lambda_0-1-2beta/3),
    c_tensor^2/c^2 = 1/alpha.

At the saved conditional reference lambda_0=.4156872337555513, positive
tensor and scalar kinetic terms require

    -1 < beta < -.876469149366673.

Consequently c_tensor/c > 2.84. The lapse-gradient term does not remove
this tensor mismatch. Observed GW170817/GRB170817A propagation is consistent
with the photon speed at approximately 10^-15 precision under the emission
and propagation assumptions of the analysis. Applying this observation to
the action requires a validity window extending to those wave frequencies;
an unspecified cutoff is not a completed repair.
[Primary observation](https://arxiv.org/abs/1710.05834).

## Restoring tensor speed without abandoning the galaxy response

Replacing the R3 coefficient by xi restores luminality when xi=alpha, but
with F fixed the static equation becomes

    div[(xi-F_plus') grad Phi] = 4 pi G_bare rho.

Setting G_bare=xi G_N recovers the high-field Newton normalization, but the
low-field coefficient becomes 1-F_plus'/xi. Since F_plus' tends to one and
the proposed repair has xi<.12354, that coefficient is negative. A curvature
counterterm alone destroys the inherited ellipticity.

Allow the stronger simultaneous repair xi=alpha, F -> alpha F, and
M^2 alpha=M_N^2. The normalized action now preserves luminal tensors, the
same measured G_N and the full stationary galaxy law:

    S = (M_N^2/2) integral N sqrt(gamma)
        [R3 + Kij Kij - lambda_b K^2 + 2 ell^2 F(X)] + S_m,
    lambda_b = (1+beta/3)/(1+beta),
    kappa = (3lambda_b-1)/2 = 1/alpha,
    X = (a_i a^i - eta K^2/9)/ell^2, ell=a0/c^2.

This changes the homogeneous construction and must be varied afresh. With
x=(cH/a0)^2, y=eta x, Gcal(y)=F_plus-2yF_plus', lapse variation and conserved
dust give

    E(y)=3 kappa y/eta-Gcal(y)=8pi G_N rho/(a0/c)^2,
    q+1=3E/(2yE'),
    y Gcal_y=3 kappa x-3E/[2(q+1)].

The principal scalar trace coefficient then satisfies the exact identity

    lambda_eff = lambda_b - (2eta/9) Gcal_y
               = 1/3 + Omega_b/(q+1).

ALL beta dependence cancels after the three physical normalizations are
enforced. For several conserved fluids replace Omega_b by the sum of
(1+w_i)Omega_i. Omega must use the same measured G_N, not the pre-rescaling
bare coupling.

At H0=73.6 km/s/Mpc, omega_b=.02235 and q0=-.499, the value remains
.4156872337555513, with scalar kinetic coefficient -.845648822135421.
The q0 target was obtained from an exposed standard-cosmology summary; it is
NOT a model-independent direct observation. The exclusion is conditional
on this target, the stated homogeneous/state/metric premises, regular
constraint elimination and a window where these principal terms dominate.
Degenerate limits are not certified by this reduction.

## Scientific decision

Do not spend a numerical scan on the finite constant shear/rescaling family:
it cannot cure the saved problem while preserving the stated mappings.
This does not exclude a dynamically different clock, constrained field,
kinetic mixing, a different physical matter coupling or an inhomogeneous
operational expansion model. Any such alternative must supply its new
equations and observational dictionary, and count its new freedom.

The separate K(X)/J/compression candidate already supplies extra dynamics,
but has unresolved abundance, formation and nonlinear evolution. Its old
conditional thermal successes cannot be spliced into this stationary action.
No all-UNT no-go or Stage 3 completion follows from the constant-repair result.
