# Which native soft spectrum would give flat rotation curves?

Analytical continuation, 2026-09-28. No new field solve or fitted exponent.
This generalizes the already specified positive separable elastic parent,
not the original BS Hamiltonian. It identifies a microscopic target that
can be tested independently of galaxy velocities.

## Exact low-source exponent and coefficient

For a mode with energy

    V_delta = kappa (g-delta*y)^2/2 + u*y^4/4,

retain positive constant kappa,u and replace the previously adopted density
`nu(delta)=A*delta` by `nu(delta)=A*delta^alpha` on `(0,Lambda)`.
Assume `-1<alpha<3`, set `b=(alpha+1)/4`, so `0<b<1`.
At the unique relaxed minimum, with `z=delta*y/g` and `g>0`,

    delta^4=(u/kappa) g^2 z^3/(1-z),
    V_delta=kappa*g^2*(1-z)*(2-z)/4.

The exact change of variables gives

    W(g)= A*kappa^(1-b)*u^b*g^(2+2b)/16
          * integral_0^zmax z^(3b-1)*(1-z)^(-b)*(3-2z)*(2-z) dz.

Both endpoints are integrable precisely for the stated interval. As `g->0`,
`zmax->1`; writing `B` for the beta function,

    I(b)=6B(3b,1-b)-7B(3b+1,1-b)+2B(3b+2,1-b)
        =12B(3b,1-b)/[(2b+1)(2b+2)].

Thus

    W(g) ~ C_b A*kappa^(1-b)*u^b*|g|^(2+2b),
    C_b = 3B(3b,1-b)/[4(2b+1)(2b+2)],
    F(g) ~ 3B(3b,1-b)/[4(2b+1)]
           * A*kappa^(1-b)*u^b*g*|g|^(2b).

The low-field force exponent is

    p = 1+2b = (alpha+3)/2.

For alpha=1, b=1/2, the coefficient reduces to the prior exact result
`W ~ pi*A*sqrt(kappa*u)*|g|^3/16` and `F~3*pi*A*sqrt(kappa*u)*g|g|/16`.
The finite upper-cutoff correction begins at order g^4 in W. The already
adopted bounded-source completion adds another analytic order-g^4 term,
so neither changes this leading exponent when alpha<3.

At alpha=3 the borderline tail produces a g^4*log(1/|g|) behavior instead.
For alpha>3 the leading relaxed energy is analytic quartic and depends on
the ultraviolet cutoff; for alpha<=-1 the number/contact integral diverges
at the lower endpoint without another infrared prescription. A nonzero
lower cutoff restores the finite-mode analytic small-g limit. These are
different regimes, not reasons to extend the beta formula past its domain.

## Why the exponent is an observable selector

In an isolated spherical far field of finite baryonic mass, the specified
gravity interface gives `F(g)/K_b = GM/r^2`, up to its owned physical units.
For `F~g^p`,

    g ~ r^(-2/p),
    v_circular ~ r^(1/2-1/p)
               = r^[(alpha-1)/(2(alpha+3))].

Exactly flat limiting circular speed therefore selects **alpha=1** in this
parent class. Alpha=0 gives `v~r^(-1/6)`; alpha=2 gives `v~r^(1/10)`.
This is a far-field scaling statement, not an approximation to every finite
disk radius or a fit to NGC3198. The finite thermal/quantum/rate window still
determines whether the low-field continuum limit is physically accessible.

The attractive feature is that the needed exponent can be sought in the
network without using rotation-curve data: does its *owned source-coupled
adjustment spectrum* have a linear small-delta density?

## Translate to a graph/Hessian measurement without confusing dimensions

If a properly derived quadratic adjustment eigenvalue obeys
`lambda=kappa*delta^2` with the same positive kappa, then the corresponding
weighted spectral density is

    rho_lambda(lambda) = A/(2*kappa^((alpha+1)/2))
                         * lambda^((alpha-1)/2).

The flat-curve selector alpha=1 means a **constant weighted density of small
positive stiffness eigenvalues**. Under an additional constant-inertia,
linear-dispersion interpretation it resembles a two-dimensional internal
mode count. It does not imply that physical space is two-dimensional, nor
does the existing two-dimensional Dirac comparison automatically supply
these classical adjustment coordinates.

Counting eigenvalues alone is insufficient. The same native reduction must
also establish:

1. The source and contact structure `kappa(g-delta*y)^2/2`, including the
   source overlap proportional to delta and the absence of an independent
   pinning floor in the relevant regime.
2. The leading positive quartic stabilization, its possible cross-mode
   interactions, and whether a separable reduction is controlled.
3. Positive appropriately weighted density, physical volume normalization,
   inertia, prepared state and a relaxation rate fast enough for this static
   response. A signed or population-inverted quantum response is not this
   passive density merely because its transition-frequency count agrees.
4. An increasing-size soft window rather than a fit to a few discrete lines;
   finite size, history, temperature and observation time can delimit it.

These conditions specify a compact native-theory task: derive the physical
source-coupled stiffness and nonlinear energy in the actual formed network,
then check its scaling. They do not authorize selecting an exponent from
the desired galaxy answer. If the native conditions produce a different
exponent or cross-mode structure, retain and solve that result rather than
silently imposing the separable model.
