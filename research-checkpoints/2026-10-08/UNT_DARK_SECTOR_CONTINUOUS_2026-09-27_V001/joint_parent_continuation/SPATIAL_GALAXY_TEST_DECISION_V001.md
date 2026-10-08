# From local response to a spatial galaxy test V001

2026-09-29. Analytical implementation decision. No numerical producer, new
observation, fitted density, parameter selection or frozen edit.

## Shortest defensible spatial diagnostic

The material census supplies F(N,g), hard I(N,g), E, Pi and their local
derivatives. It does not supply an outer clock or a hard-density profile.
The minimal spatial extension is the existing axisymmetric thin-disk source
problem with the SAME phase solve in every cell and the hard reaction term
kept in the bulk equation. It can first be tested as an explicitly clamped
source/boundary diagnostic. It becomes a galaxy prediction only if its
phase/metric boundary and ordinary support are physically matched.

Use an already owned stellar/gas surface-density profile and its existing
source alternatives. Do not choose a profile, global reference or boundary
radius from the new force residual. The numerical domain is a resolution/
boundary-control device, not a fitted halo radius. No local I or chemical
potential is an independent input.

In the declared weak-field, background-subtracted approximation, c=1,

    div D=4 pi G Kb delta(rho_b+S_b)+delta(E+3Pi),
    D=Kb grad Phi-F(N,g) grad Phi/g,
    N=exp(Phi), g=|grad Phi|, N omega(I,h)=mu.             (1)

This is a two-variable material law plus a nonlinear reaction equation,
not the old mu(g) PDE with a rescaled coefficient. The full metric equations
remain the reference; terms such as g^2, a.F, baryonic rotational stress,
frame dragging and cosmological time derivatives must be retained or bounded
at a common approximation order, as in the reviewed BVP. The constant DeltaU
cancels in the perturbation source, not in the parent or cosmic matching.

## 1. A direct disk-normalization check that needs no halo model

Let the leading ordinary source be a thin disk Sigma(varpi)delta(z),
reflection symmetric about z=0. Provided the hard/soft volume densities
remain finite through the sheet, integrating (1) gives exactly at this order

    D_z(0+)=2 pi G Kb Sigma,
    [Kb-F(N,g)/g] g_z=2 pi G Kb Sigma,
    g=sqrt(g_varpi^2+g_z^2).                             (2)

N and |g| are continuous across the sheet; the normal component reverses
sign. Thus the scalar hard I is continuous on a single branch, and no
artificial hard surface mass should be introduced. If ordinary surface
stress is kept at higher order, its trace enters the same jump consistently.

At fixed N and tangential field, the derivative of the left side with respect
to g_z is

    K_T g_varpi^2/g^2+K_L g_z^2/g^2.                    (3)

Positive local principal coefficients therefore give a unique monotone
normal-flux inversion on that branch. Equation (3) uses the phase-equilibrium
K_L, including its B_I^2/e_II term. It is an exact qualification of the
spatial implementation, not another constitutive fit.

An integrated finite-volume check is equally direct:

    integral_boundary D.n dA
       =4 pi G Kb integral_domain delta(rho_b+S_b)dV
                                +integral_domain delta(E+3Pi)dV. (4)

The second volume integral cannot be dropped or replaced by a freely fitted
mass. These two identities, the common-frequency residual, and the complete
metric/conservation residuals are the core spatial checks. Existing disk
benchmarks can qualify the numerical operator without inventing a new source.

## 2. Cold boundary matching concerns mu/N, not just force accuracy

The boundary phase datum is the gauge-invariant ratio Q_b=mu/N_b. At fixed
boundary source h, its infinitesimal action sensitivity is exactly

    delta I_b/I_b=delta ln Q_b/c_I,b^2.                  (5)

With a varying source the full relation is

    delta I_b/I_b=[delta ln Q_b+(B_I/omega)delta h_b]
                                                        /c_I,b^2. (6)

Consequently a boundary potential error that is negligible for a force-only
solver can be important for a cold state. For a declared fractional action
accuracy epsilon_I, the fixed-h phase ratio must be controlled to
epsilon_I*c_I,b^2. This is an error-propagation identity, not a new numerical
tolerance or an observational exclusion. The field census determines how
that sensitivity changes at finite field.

Rescaling N and mu together does not change (5). Setting Phi=0 at a numerical
wall while holding mu to a different cosmic time normalization is not a
harmless gauge change. Likewise, uniform cosmic I_b, an arbitrary N_b and a
nonuniform h_b cannot all be imposed independently.

If the outer data are only clamps, report the response conditional on those
clamps and retain domain/phase-boundary sensitivity. Do not claim that a
small acceleration change between boxes has certified the cold density.
The already derived static Helmholtz resonance and finite-norm issues also
remain. No boundary radius is to be optimized against the galaxy curve.

## 3. The number and supply ledger distinguishes two state experiments

The full square-root phase action has exactly conserved current

    J^mu=C beta I U_theta^mu,   nabla_mu J^mu=0.

For any stated worldtube enclosing a patch,

    Q_D(t_f)-Q_D(t_i)=-integral_worldtube J^mu dSigma_mu.  (7)

On an aligned static slice Q_D=C beta integral I sqrt(gamma)d3x. The
current is then spatially zero, but this does not imply that the present
inventory equals the initial cosmic inventory: action may have entered
during formation. A fixed cosmic mu static BVP is an open-reservoir
equilibrium prescription unless that history or total inventory is supplied.
It must not be reinterpreted afterward as a closed collapse calculation.

For the hard-fluid part of a stationary source with phase frequency mu,
the Killing-energy flux is mu times its action flux. During nonstationary
assembly the polarization/source/gravitational work must also be retained;
there is no claim that mu times (7) is the entire energy ledger. In no case
is an imported positive excitation energy free or subtracted from DeltaU.

A closed-patch experiment instead fixes the initial total action and its
worldtube flux (zero if genuinely closed). If seeking an equilibrium of
that experiment, mu is determined by the inventory constraint, not fitted
to a rotation curve. Such a finite closed patch cannot simultaneously be
treated as an unspecified infinite cosmic reservoir. A material reflecting
wall would require its own support and is not inserted here.

## 4. Scientific decision after the local census

If an occupied branch and appropriate local coefficients survive, implement
(1)-(4) using the already owned axisymmetric source. First identify it
explicitly as a clamped-source diagnostic unless an actual outer state is
available; save its action inventory, matching sensitivity and all metric/
support errors. A successful local or clamped solve does not prove that
cosmic initial data select its aligned static clock.

If the cold outer phase/flux remains undefined for a claimed prediction,
the cleaner next physical test is the closed initial-value branch already
derived in COMMON_ACTION_GALAXY_BOUNDARY_AND_INITIAL_STATE_V001.md: constrain
the metric from common cosmic density/velocity initial data, conserve the
hard current, and evolve ordinary matter with the same network fluid.
The normalized transfer basis and exact local two-fluid oracle make that
test executable without a fitted halo radius. Its geodesic, soft-zero
Q=0 realization is an explicit initial state, not all allowed Q=0 data
and not automatically the accelerated static branch.

The choice is therefore between two precisely labeled state experiments,
not between adding a free density profile and postponing all work until a
native derivation exists. Either can be tested now as the declared effective
parent. Only a matched boundary/history turns its spatial response into an
observational galaxy prediction.

This note uses the settled BVP (64d98fff...), variable-state conservation
note (62dd5560...), common-action initial-state note (2eb30bb5...), and
finite-field derivative note (cb8ec369...). All formulas are analytical;
no numerical result or new acceptance threshold is claimed.
