# A curved regional state must have positive ordinary matter

2026-10-05 UTC. Prospective bounded test of the SAME constant-trace action,
not a new cosmological fit. The purpose is to test the negative-curvature
opening identified in REGIONAL_CLOCK_BUDGET_IDENTITIES_V001. The plane code
cannot access negative proper-volume mean curvature. No earlier evolution
is rerun. Internal independent review has checked the geometry and equations.

Use a compact Sol mapping torus, with metric

    ds3^2=dz^2+exp(2az) dx^2+exp(-2az) dy^2,
    (x,y,z) ~ (exp(-aL)x,exp(aL)y,z+L).

The transverse lattice is in the eigenbasis of a hyperbolic SL(2,Z) matrix
with positive integer trace T>2. It is NOT a rectangular torus. Then
aL=acosh(T/2), k=2pi/L, and Ric=diag(0,0,-2a^2), R3=-2a^2. The trace
and curvature scale are disclosed state choices, not network predictions.

On one preferred slice take N=1, zero ordinary momentum, W(0)=0 and
Lambda=0. Removing the predecessor's endpoint here is an explicit
zero-endpoint diagnostic, not a claim that its expansion calibration survives.
Let K=3H+d cos(kz). The trace-free mixed shear has diagonal entries
((-c+e)/2,(-c-e)/2,c), c=C cos(kz), e=D sin(kz), where

    C=2F k^2 d/[3(k^2+3a^2)], D=2F a k d/(k^2+3a^2),
    F=1+3beta/2=1.75, beta=.5.

This solves c'-ae=(2F/3)K'. It is the global minimum L2 shear for this K
on the compact quotient: it is the conformal Killing derivative of
Wz=F k d sin(kz)/[2(k^2+3a^2)]. Additional divergence-free trace-free
shear is orthogonal and increases its mean squared norm. That does not mean
the minimum-shear choice optimizes local density among all tensor states.

Define h=k^2/(k^2+3a^2), t=d/H, r=rho_bar/(M^2 H^2), q=(1-Fh)/3.
The mean Hamiltonian fixes the curvature, not an extra mass reservoir:

    a^2/H^2=3F-r+F q t^2/2,
    Q_D/H^2=q t^2,
    rho(u)/(M^2 H^2)=r+2F t u+F A t^2(2u^2-1)/6,
    A=1+Fh-2Fh^2, u=cos(kz).

Density positivity is checked at the endpoints and the interior quadratic
vertex, if present. Entirely expanding states require 0<=t<3. Geometry
also requires a^2>0. The first positive-Q integer trace at beta=.5 is24.

## Frozen decision and numerical controls

Use traces [3,10,24,50,1000,1000000] and mean-density ratios
r=[.15,.3,1,3,7]. These are development controls, NOT measured posterior
values or a fitted population. The large-trace/high-density cases check
whether failure in low-density states is wrongly promoted to a theorem.
Find the maximal density-admissible t in [0,3] by the exact quadratic
minimum and80 bisection steps; report curvature admissibility separately.
For q>0 the kinematic contribution grows with t, so this supplies an upper
bound on the entire expanding admissible interval, not just sampled states.
For q<=0 positive kinematic acceleration is unavailable.

The decision quantity is Q_D/H^2-r/(2F). Positive values are only a
NECESSARY favorable kinematic budget for zero-endpoint dust acceleration;
the full equation also contains <K Ndot>/H^2. No Ndot=0 assumption is used
to call a state a successful accelerating cosmology. Neither lapse evolution,
formation nor light-cone observations are supplied by this calculation.

Qualification gates fixed before execution: relative/absolute-normalized
Hamiltonian and momentum residuals <=1e-11; analytic moments vs4096 equally
spaced phases <=1e-11; exact density minimum vs phase sample differs by no
more than1e-5 in H-normalized density and is no larger than the sample
minimum by more than1e-11; bisection endpoint minimum has absolute error
<=1e-10 unless the allowed interval reaches3. These are arithmetic gates,
not tolerances on whether the physical decision is favorable. Exact signs
and margins are saved without a tuned scientific threshold.
