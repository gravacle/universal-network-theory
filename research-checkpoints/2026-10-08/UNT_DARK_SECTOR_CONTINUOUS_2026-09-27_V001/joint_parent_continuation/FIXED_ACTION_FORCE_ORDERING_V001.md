# Exact ordering of the finite-field scalar response

2026-09-29. Analytical result derived during preflight, before the finite-field
outputs were viewed. Independently checked by the parent and analytical peer.
No new worker, fit, numerical acceptance gate or alteration of frozen files.

For the declared positive harmonic-plus-quartic scalar mode,

    U(y)=delta^2 y^2/2+y^4/4-delta*h*y,  delta>0, h>0,

let y_star be the unique minimum. Every nonconstant bounded orbit, whether or
not it crosses zero, obeys the strict period-average ordering

    0 < <y> < c < y_star,                                (1)

where c is the midpoint of its turning points. This does not require the
nonnegative-orbit restriction of the earlier Jensen argument.

## Proof

Write the turning points as c-r,c+r, r>0. Their equal energies imply

    c^3+(delta^2+r^2)c=delta*h,

so c>0 and c<y_star. The exact time weight at y=c+r cos(theta) is proportional
to `1/sqrt(Q)`, where

    Q=(y+c)^2+2delta^2+2c^2+r^2.

Pair theta and pi-theta. Put `u=r|cos(theta)|`,
`A=6c^2+2delta^2+r^2` and `Q_plus/minus=A+u^2 +/- 4cu`.
The paired signed displacement numerator is

    u*(1/sqrt(Q_plus)-1/sqrt(Q_minus)) < 0

away from u=0. Integrating gives `<y><c`.

The paired y numerator is positive immediately if u<=c. For u>c,
positivity is equivalent to

    (c+u)*sqrt(Q_minus) > (u-c)*sqrt(Q_plus).

Both sides are positive; their squared difference is exactly

    (c+u)^2 Q_minus-(u-c)^2 Q_plus
      =4cu*(4c^2+2delta^2+r^2-u^2) > 0,

because u<=r. Thus every paired contribution is positive and `<y>>0`.
This proves (1) for arbitrary finite action. At zero action the orbit reduces
to the minimum and `<y>=c=y_star`; negative h follows by reflection.

## Same-spectrum force and ideal-work consequences

For positive weights, fixed actions, `Kb=sum(weights)`, and the inherited
bounded source h(G)>0, h'(G)>0 at G>0, define

    D_I(G)=G-h'(G)*sum weights*delta*<y>_I / Kb.

The relaxed reference uses the SAME spectrum, contact and source map, replacing
each mean by its minimum. If a positive spectral weight is excited,

    D_relaxed(G) < D_I(G) < G.                          (2)

If every action is zero the first inequality is equality. The reference force
is itself positive: the minimum equation gives `delta*y_star<h`, hence
`D_relaxed>G-h'h>=0` for the adopted bounded map. The inequalities are
pointwise constitutive statements, not a comparison theorem for disk fields.

The exact fixed-action energy derivative is `dW_I/dG=Kb*D_I`. Consequently
its ideal fixed-volume source-work difference from G=0 lies above the
same-spectrum relaxed work and below `Kb G^2/2`. Initial excitation and the
unchanged matched constant must still be retained in the absolute energy;
this integral does not describe an actually executed adiabatic trajectory.

## Scope

Excitation cannot strengthen the relaxed scalar polarization in this model;
it moves the constitutive relation toward the bare response. This is a useful
constraint on a common-state solution, not an adjustable correction curve.
It does **not** prove monotonic ordering between two different positive actions,
positivity of D_I'(G), static or dynamical stability, or spatial locality.
The theorem is for exact period means at fixed scalar actions. It does not
bound instantaneous coherent forces, identify an isotropic vector ensemble,
establish physical adiabatic preparation, or solve the retained clock/metric
constraints. It makes no new galaxy-data or cosmological claim.
