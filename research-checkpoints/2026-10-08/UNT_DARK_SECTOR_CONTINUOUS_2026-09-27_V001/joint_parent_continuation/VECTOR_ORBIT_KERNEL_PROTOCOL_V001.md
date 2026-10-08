# Universal vector-orbit kernel: prospective numerical qualification

2026-09-29. Five synthetic central-oscillator cases only, not a new physical
population, preparation, galaxy law or 4,614-mode census. The parent owns the
single execution and publication. `vector_orbit_kernel_v001.py freeze|run`
prints JSON only and never overwrites existing evidence.

## Fixed equations and selected response

Set k=m=b=1 and u=r in {0,1e-4,.01,1,100}. The unforced trajectory starts at
y=1, ydot=0 and obeys yddot=-y-u*y^3. Its energy is 1/2+u/4. Compute its
period T by the positive endpoint-safe angle integral at 64 and 128 Gauss
nodes; P=T/2. Use the 128-node period in both independent ODE resolutions.

The transverse equation is xi_ddot+(1+u*y^2)xi=1. Select the unique
P-periodic forced solution. Do not add a homogeneous angular-momentum or
ellipticity component. The unforced rotational solution y is anti-periodic
over P: both homogeneous Floquet multipliers are -1, not absent modes.
The retained longitudinal comparison is

    xi_parallel=(1+u*y^2)/(1+u)^2.

These are per unit mode force F in H-F dot y, not per arbitrary gravity or
photon source. The isotropic trace is conditional on the state/gauge and
orientation assumptions of ISOTROPIC_VECTOR_ORBIT_RESPONSE_V001.md.

## Stable exact transverse quadrature

Let K=1+u, eta=u/(2K), and L(q)=asin(sqrt(q))/sqrt(q*(1-q)), with L(0)=1.
The removable-singularity formula in the analytical note implies

    xi_yy(y)=2eta L'(eta*(1-y^2))/K,
    xi_y(y)=2eta*y/K int_0^1 L'(eta*(1-y^2*s^2)) ds,
    xi(y)=L(eta)/K
             +2eta*y^2/K int_0^1 (1-s)L'(eta*(1-y^2*s^2)) ds.    (1)

Thus no subtraction R(0)-R(y) or division by y^2 is necessary. Evaluate L
and L' by their positive power series through degree64:

    L(q)=sum a_n q^n, a_0=1, a_n=2n*a_(n-1)/(2n+1).

For 0<=q<=eta<1/2 the omitted tails are bounded by
q^65/(1-q) and q^64*(65-64q)/(1-q)^2 respectively. Save these bounds.
Compare L against its independent arcsine expression (q=0 handled exactly)
and check 2q(1-q)L'+(1-2q)L=1 at the predefined q fractions
{0,1/8,1/2,7/8,1} times eta. This is not outcome-adaptive precision.

Use 64/128 Gauss nodes for both the positive inner integrals in (1) and the
outer time mean with y=sin(theta), time weight
[1+u*(1+sin^2(theta))/2]^-1/2. The underlying series degree makes the inner
64-node rule exact up to the bounded series truncation and roundoff; the
outer time average remains an independent 64/128 convergence test.

At y={-1,-3/4,-1/2,-1/4,0,1/4,1/2,3/4,1} check the variational equation
using xi_yy*ydot^2+xi_y*yddot and the exact unforced energy. Check the parallel
equation similarly, parity, the center derivative and the proven pointwise
bounds. No divided-difference derivative is required.

## Independent half-period shooting problem

Independently integrate y,ydot, the two transverse homogeneous fundamental
columns and the inhomogeneous column with zero initial data. Use ordinary
fixed-step RK4 with 1024 and 2048 steps PER half period. Retain a full period
for the independent symmetry and angular-momentum tests, but solve the BVP
from its first-half monodromy M and inhomogeneous endpoint d:

    (identity-M) z_initial=d.

Also integrate the three column position integrals as augmented ODEs, so the
mean of the resulting forced solution is obtained from the ODE, not from the
analytic susceptibility or a separate fitted constant. The second half tests
the solved response's P-periodicity and y anti-periodicity independently.

For BOTH step sizes retain the Floquet trace/determinant, det(identity-M),
condition number, source/periodic endpoint residuals, direct orbit energy
error, mean susceptibility and profiles at nine equally spaced full-period
times. Compare profiles and their time derivatives with (1). The derivative
comparison is normalized by max(1,sqrt(1+u)); do not use relative error at a
zero derivative. Check the initial forced velocity is zero by reflection.

The induced first-order angular momentum is y*xi_dot-ydot*xi. Its full-period
mean must vanish for the selected solution; use the saved ODE mesh and retain
the raw mean. The second homogeneous column has conserved Wronskian one,
demonstrating the excluded free angular-momentum sector, rather than pretending
there was no neutral mode. An arbitrary real switch-on need not select this
same response; no dynamical attraction is asserted.

## Frozen numerical targets and full reporting

Analytic series, quadrature, derivative residual, parity, harmonic-limit and
pointwise-bound controls use2e-11 absolute/declared-scale tolerance. The
uniform series-tail bound itself must be<=2e-12. RK4 orbit, monodromy,
periodicity, mean/profile, mean-angular-momentum and Wronskian controls use
2e-7 with scales max(1,initial energy) for energy,
max(1,sqrt(1+u)) for velocity-like quantities and unity otherwise. Coarse/fine
susceptibility and profile comparisons use the same2e-7. The raw errors and
all outcomes are retained even on failure; no tolerance changes after seeing
results are allowed by this protocol.

Save all five cases, both ODE resolutions, both quadratures, exact bounds,
the conditional isotropic susceptibility and weak-excitation coefficients.
The first-order small-r expansion is a descriptive comparison, not a new
asymptotic error gate without an independently derived remainder bound.
At r=0 the complete harmonic solution xi=1 is an exact numerical control.

This entails30,720 short11-component RK4 steps in total, plus small positive
quadratures. The largest saved working array is4097 by11; only the nine fixed
profile witnesses and aggregate controls are published. There is no full
physical-mode census, source pulse, fit, parameter search, package installation,
large matrix, physical run deadline or checkpoint engineering.

Freeze includes this protocol, code and the exact two analytical source notes;
the vector note's settled identity is checked explicitly. No source from the
earlier scalar numerical workers is imported or mutated.
