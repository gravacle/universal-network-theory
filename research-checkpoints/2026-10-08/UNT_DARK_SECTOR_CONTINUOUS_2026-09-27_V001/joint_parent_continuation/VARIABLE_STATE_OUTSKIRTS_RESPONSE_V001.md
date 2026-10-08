# Variable network state and galaxy-outskirts response V001

2026-09-29. Analytical scope/constitutive test for the declared alpha-one
scalar candidate. No new force calculation, population, fit or frozen edit.

## 1. What now varies, and what the old calculations already varied

The old disk calculations already used spatially varying stellar/gas
density, nonspherical geometry and a spatially varying gravitational field.
They did not assume a galaxy of uniform baryonic density. Their conditional
response law, however, was supplied by a fixed or relaxed medium-state
prescription rather than a solved spatial redistribution of the common
cosmological hard action.

The new scalar BVP has a genuinely different state variable I(x). Its
constitutive response depends on BOTH lapse and acceleration:

    N omega(I,h(g))=mu,   g=|D ln N|,
    F(N,g)=h'(g)[B_soft(g)+beta B_H(I,h)],
    B_H=-e_H,h.                                           (1)

The common outer state fixes mu; there is not one adjustable mu or abundance
per radius. On a convex occupied branch e_II>0,

    dI=[-omega d ln N+B_H,I dh]/e_II.                     (2)

The lapse-depth and source-frequency contributions compete. Deeper lapse
increases I in the intrinsic h=0 hardening limit. A finite source can change
the frequency in the other direction. Therefore neither a universally
increasing nor a universally decreasing radial hard density should be
assumed before solving the field/state equations.

The gravitating density is not just beta e_H or record count:

    rho_mode=C[E+DeltaU+a.F+div F],
    S_ij=C[(Pi-DeltaU)gamma_ij-a_(i F_j)].                 (3)

Its density, intrinsic pressure, anisotropy and polarization divergence all
vary. The same metric must predict dynamics and lensing. In particular a
spatial network concentration is permitted, but its energy cannot be erased
while interpreting it as a replacement for a conventional halo.

## 2. Why a freely assigned radial I is not the same model

Let E=sum_soft w e_min+beta e_H and
Pi=-sum_soft w e_min+beta(I omega-e_H). These are the on-shell EOS functions.
Their exact differential is

    dPi=beta I d omega+B_total dh,
    E+Pi=beta I omega.

Because a_i=D_i ln N and F is parallel to a,
F^j D_j a_i=F D_i g. Substituting (3) into static stress conservation gives

    D_j S^j_i+(rho delta_i^j+S^j_i)a_j
                         =(C beta I/N) D_i(N omega).     (4)

Thus assigning I(x) arbitrarily and treating its EOS stress as a static
source leaves an exact uncompensated force unless the common-phase condition
holds (or I is empty). Canceling (4) by an external support force would be a
different, explicitly supported construction, not a solved galaxy.

There is a distinct off-shell check that should not be conflated with (4).
If the actual action is held at theta=mu t, Q=mu/N, but I is arbitrary,
its pressure before imposing the I equation is I Q-e, not I omega-e.
The I equation is Q-omega=0 and its static conservation residual is

    C beta(Q-omega) D_i I.                               (5)

A constant I could accidentally make (5) vanish while still violating the
I equation. Conservation alone therefore cannot certify an imposed profile.
Equations (4) and (5) describe two different invalid shortcuts; the valid
solution satisfies the action equation and conservation together.

Nor does writing theta=mu(x)t avoid the issue: a spatially varying mu creates
a phase gradient proportional to time and hence a current. It is not the
stationary zero-flow state used in the BVP.

For example, the local linear hard phase/current equations about an occupied
uniform state, using delta theta=omega V and d=delta I/I, are

    d_dot=3 Psi_dot-p^2 V,
    V_dot=Phi+c_I^2 d-(B_H,I/omega)delta h,                (6)

in a frozen background. A time-dependent background adds
-(omega_dot/omega)V; this is the already derived +3H c_I^2 V on the
homogeneous h=0 FLRW branch. At h=0, parity gives B_H,I=0. A prescribed static density with V=0
must still satisfy the spatial gradient of the second equation. Otherwise
it starts flowing or needs a stated external force/current. The complete
metric response includes polarization and ordinary matter, not (6) alone.

## 3. Finite-field phase response is not the cosmic K0

Implicit differentiation of (1) gives

    I_g|N=h' B_H,I/e_II,
    I_N|g=-omega/(N e_II).

Let chi_soft=dB_soft/dh on its specified static minima. Then

    F_g|N=h'' B_total
          +h'^2[chi_soft+beta(B_H,h|I+B_H,I^2/e_II)],
    N F_N=-beta h' omega B_H,I/e_II.                     (7)

The local principal coefficients are

    K_trans=Kb-F/g,
    K_long=Kb-F_g|N.                                    (8)

The positive B_H,I^2/e_II contribution is absent from a fixed-action force
table. At the SAME local state and convex branch it implies the exact
inequality

    K_long,phase=K_long,fixedI
                         -beta h'^2 B_H,I^2/e_II
                  <= K_long,fixedI.                     (9)

At zero source B_H,I=0 by parity; the enormous lapse-density response can
still enter the lower-order self-gravitational term. At finite source the
soft nonlinearity, bounded-source h'', hard response and phase redistribution
must all be evaluated. No coefficient in (8) can be replaced indiscriminately
by its tiny cosmic limit K0. Similarly the previously derived ell0 is a
linear cosmic static-response length, not a maximum galaxy/halo radius or
an exclusion of support at a different local state.

## 4. Minimal decisive local nonlinear comparison, before a galaxy solve

Use each retained finite-R calibrated design without changing its gstar,
S, spectrum, baseline, energy or common cosmic action. Keep the already
exposed physical acceleration probes

    g_phys={1e-12,1e-10,1e-8} m/s^2.

Convert to the design's dimensionless source consistently. First fix N=1
and mu=omega(I_b,0). This is a local constitutive diagnostic at the cosmic
lapse normalization, NOT a global spacetime with zero lapse gradient and
nonzero acceleration: N and its local first spatial derivative are
independent jet data at a point.

At each probe solve e_I(I,h)=mu on the boundary-connected convex branch,
including a legitimate empty branch if Q<=e_I(0,h). Preserve a missing
root, fold or nonconvex branch as an outcome, rather than clipping I or
changing mu. Evaluate the actual I/I_b, E, Pi, F, F_N, K_trans and K_long.
At the identical field also evaluate the unchanged-I_b response. This
directly tests the shortcut used by a fixed-state force table without
inventing a galaxy potential or fitting a density function.

The exact parametric extension is

    N(I,g)=mu/omega(I,h(g)),
    dN/dI|g=-N e_II/omega.                              (10)

It displays branch folds and the admissible empty endpoint without selecting
a favorable radial action. A later BVP supplies the actual N(x), g(x) and
common boundary data; it must not interpolate independent best-fit states
at different radii. Positive local coefficients are an existence condition,
not proof of full static uniqueness, dynamical formation or clock stability.

The 360 finite-R designs are a new, explicitly declared scalar-state
calibration census. They are not the earlier six coherent pulse states,
and this local comparison does not change their identity into such a
preparation. All references and gaps should remain retained; no outskirts
residual selects the state. No worker is implemented or run in this note.

## Source scope

This derives from MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md
(`64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3`),
the common-action boundary/initial-state note
(`2eb30bb54416d31a69109b1d48795789a208b2418bfb237cfd81a291ec006c26`),
and the read prospective FINITE_GAP_SHARED_SCREEN_PROTOCOL_V001.md.
The exact constitutive derivatives are analytical checks, not an independent
audit of the newly saved 360 numerical branches.
