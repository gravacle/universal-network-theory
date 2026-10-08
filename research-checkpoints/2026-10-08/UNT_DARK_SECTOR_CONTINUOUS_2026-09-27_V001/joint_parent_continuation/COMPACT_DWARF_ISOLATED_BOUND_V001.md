# Isolated compact source: a critical-response upper bound

2026-10-05 UTC. Frozen protocol before the unit calculation. This is a new
isolated-state test of the SAME bounded-source, ell=100 pc static candidate.
It neither inherits the external-field contraction nor fits a new length.

## Nonlinear comparison that avoids a fourth-order numerical solve

Consider any regular, bounded, spherically symmetric outward-force solution
with g(R)>=0, g(R)->0 at infinity, and the standard Yukawa inverse on all
space. The signed radial vector is grad Phi, with inward acceleration
-grad Phi. Write b=Sg, c=S F(b). S restricted to radial vectors is

    S1=[1-ell² L1]^(-1),
    L1=d²/dR²+(2/R)d/dR-2/R²,
    g=g_N+S1 F(b), b=S1 g.

The radial resolvent is positivity preserving. For the frozen positive
quartic modal energy, its equilibrium obeys 0<=P(h)<=Kb h. The bounded
source h(b)=b/sqrt(1+b²/gs²) therefore gives

    0<=F(b)=h'(b)P(h)/Kb<=h'(b)h(b)<=b.

No monotonicity of F' is assumed; its derivative can change sign. It follows

    g_N<=g<=g_N+S1²g
         <=sum_(j=0)^N S1^(2j)g_N+S1^(2N+2)g.

For bounded g vanishing at spatial infinity, the last term vanishes at
each fixed point. One proof uses the n-fold Yukawa convolution density:
its maximum falls as n^(-3/2), so its mass in every fixed bounded set tends
to zero. Split a bounded g into that set and a tail smaller than epsilon.
Consequently g<=g_crit=(1-S1²)^(-1)g_N, the critical linear-response branch.
The upper comparison branch need not itself vanish at infinity.

This comparison is conditional on an outward isolated branch and does not
prove existence, general nonspherical uniqueness, or source formation.
It does not apply to an arbitrary nonzero external-field/tidal boundary.

## Critical Green function and global force bound

The critical Fourier susceptibility is 1/(1-f²), f=(1+ell²k²)^(-1).
For a point source, after an irrelevant potential constant is removed,

    Phi_extra=GM R/(4ell²)+GM[1-exp(-sqrt(2)R/ell)]/(4R),
    g_extra=GM/(4ell²)
         +GM[(1+x)exp(-x)-1]/(4R²), x=sqrt(2)R/ell.

Its dimensionless force kernel has the manifest representation

    4ell² g_extra/(GM)=2 integral_0^1 u[1-exp(-xu)]du.

It lies between zero and one. Superposition and the triangle inequality
give |g_extra,crit|<=GM_total/(4ell²) for every positive extended source.
For the spherical nonlinear solution compared above, this implies

    0<=g-g_N<=GM_total/(4ell²).

This is not the assertion that every filter weakens every nonlinear force;
it is an explicit upper comparison using F<=b and radial positivity.

## Same frozen observational benchmark, new boundary state

Use ordinary source/tracer Plummer a=28 pc, M=340,1020,3400 nominal solar
masses, ell=100 pc, aperture 67 pc and GM_sun=1.3271244e20 m³/s². No inferred
dark mass, additional central mass, external acceleration or orbital fit.
The stationary stress-virial argument from the previous compact-source test
gives, without any isotropic /3 assumption,

    <v²><=3pi GM/(32a)+a GM/(2ell²),
    sigma_LOS,ap²<=<v²>/Fap, Fap=Rap²/(Rap²+a²).

Same caveats apply: stationary tracer, positive stellar population and mass
profile, surface-stress boundary, representative aperture weighting, actual
ellipticity, binaries and selection. This is not a Gaussian-estimator
likelihood or observational confidence exclusion. If even this isolated
upper bound is low, merely removing uniform external-clock acceleration
cannot rescue these frozen spherical stationary stellar models.

The calculation also reports the necessary ell ceiling for this UPPER bound
to reach the exposed 3.7 km/s reference, when its denominator is positive.
This is not a fitted/adopted length, sufficient fit, or blind prediction.
Do not replace ell=100 pc in any prior artifact.

## Frozen numerical checks

Use analytic Green and virial formulas, with one tiny numerical job. Check
the kernel representation at x=.01,.1,1,10,100 with 64/128-node quadrature
to scaled 2e-10 against the closed form, positivity and <=1. Check Plummer
mean radius, Newtonian virial and aperture integrals with 256 nodes to 2e-9.
Check linear mass scaling and the necessary-ceiling inversion to 2e-12.
The analytical comparison, not the node count, supplies the physical bound.
No differential solve, old calculation rerun or criterion adjustment.
