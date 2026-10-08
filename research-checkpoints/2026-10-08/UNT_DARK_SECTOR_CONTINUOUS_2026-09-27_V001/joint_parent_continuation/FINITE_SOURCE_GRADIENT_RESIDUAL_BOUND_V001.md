# Finite-source gradient-parent residual bound

2026-10-04. Prospective scalar diagnostic, source authored without execution.
This replaces the proposed radial reconstruction with analytic Fourier norm
bounds and one-dimensional positive spectral enclosures. No nonlinear field
solution, parameter fit, or new cosmological completion is supplied.

## Frozen preparation and observable

Retain the explicitly changed linear-source, positive-gradient parent and
the external equilibrium of LINEAR_GRADIENT_EXTERNAL_QUADRUPOLE_V001.
Use its a0, GM, ge=2.32e-10 m/s^2, and gc=3*pi*a0/8. The three lengths
ell={1,10,100} pc were already declared illustrations, not fitted lengths.
The ordinary source is now explicitly a Gaussian control:

    rho(r)=M exp[-r^2/(2 sigma^2)] / [(2*pi)^(3/2) sigma^3],
    sigma=10^9 m.

This is not a measured Solar density profile or a statement about the Solar
radius. Its Fourier form factor is exp[-k^2 sigma^2/2]. The readouts are
R={1,10,30} AU, with one AU exactly 149597870700 m:

    Q_R=-15/(4*pi*R^2) integral Phi(R,Omega) P2(cos theta) dOmega.

Q_R equals Q2 for a purely quadratic anomalous potential. It is a finite
surface readout, not the exact Cassini estimator and not an origin Hessian.
The isotropic Newtonian field and the isotropic gradient cusp contribute
zero to this readout.

## Exact inequalities used

The weight is dW=2s ds, 0<s<1. Define t+t^3=ge/(gc*s^2), a=1+t^2,
z_e=ge/a, and a_s=1/(gc^2*s^4). The smallest modal t is t0=t(1).
Use the analytic lower bound mu_floor=t0^2/(1+t0^2)<=K_T(k), not a
quadrature estimate of K_T(0). Put

    G2=2*pi^(1/4)*GM/(mu_floor*sqrt(sigma)),
    Gstar=2*GM/(pi*mu_floor*sigma^2).

For the FULL self-consistent linear response, Fourier positivity gives

    ||v_s||infinity <= U_s
        = GM/(pi*mu_floor*ell^2) log[1+2ell^2/(a*sigma^2)],
    ||v_s||2 <= V_s
        = min[G2/a, sqrt(2*pi)*GM/(mu_floor*sqrt(ell)*a^(3/4))].

The first bound follows from exp(z) E1(z)<=log(1+1/z), z=a*sigma^2/(2ell^2).
These are bounds on the linear Solar perturbation, not on the unknown
nonlinear field. Let u_s=a*U_s/ge. The nonlinear residual and a coercivity
lower coefficient of this linear trial obey

    ||r_s||2 <= B_s=t^2 (3u_s+u_s^2) V_s,
    a_star(s)=1+(3/4)t^2 max(1-u_s,0)^2.

They use the exact secant inequality

    [|z+e|^2(z+e)-|z|^2z].e >= (3/4)|z|^2|e|^2.

With Gamma=integral dW/a_star and S=integral dW B_s^2/a_star,
Gamma<1 gives the error estimate

    ||nonlinear-minus-linear||_A <= sqrt[S/(1-Gamma)],

where A includes ell^2 integral dW |grad error_s|^2 and the positive
weighted field term. This is conditional on the stated boundary-fixed
finite-energy static solution; strict convexity supplies uniqueness, not a
formation history. Eliminating the metric uses the longitudinal projector.
No isolated radial maximum principle is used in this external-field problem.

The Poisson adjoint of Q_R has value 3/(4*pi*R^3) at its shell, grows as
r^2 inside and decays as r^-3 outside. Its squared L2 norm is
3/(14*pi*R^3). Consequently,

    |Q_R,nonlinear-Q_R,linear|
       <= sqrt[3/(14*pi)] sqrt[S/(1-Gamma)] /(ell*R^(3/2)).

The bound correctly becomes unbounded as R tends to zero. A loose bound is
inconclusive, not a physical failure or a large predicted correction.

### Independent quartic-capacity bound, with no Gamma denominator

Retain also the exact identity, F(z)=|z|^2 z,

    [F(x+e)-F(x)].e=|e|^4/4+|x+e/2|^2|e|^2
                    +2[(x+e/2).e]^2.

The remaining metric-eliminated quadratic variance is nonnegative. Holder's
inequality and maximization over T=integral dW a_s|e_s|^4 therefore give

    ell^2 ||grad error||^2 <= (3/4) I4,
    I4=integral dW integral d^3x a_s^(-1/3)|r_s|^(4/3)
       <= integral dW t^2 (3+u_s)^(4/3) u_s^(2/3) V_s^2,
    |Q_R,nonlinear-Q_R,linear|
       <= 3 sqrt(I4)/(sqrt(56*pi)*ell*R^(3/2)).

This does not require Gamma<1 or uniform small relative perturbations.
Keep both bounds; their minimum is a mathematical improvement for the SAME
model and parameters, not a new physical fit.

## Continuum tail and finite-band enclosures

Freeze eta=10^-36 and nested log-s partitions with 16384,32768,65536 cells.
On each cell, t^2 and u_s decrease with s, while V_s increases. Use their
endpoint combinations to enclose B_s and a_star, multiply by the exact
positive weight s_hi^2-s_lo^2, and sum lower and upper enclosures. This
is not a midpoint approximation or a fit to the desired answer.

For the omitted interval 0<s<eta, the exact safe bounds are

    Gamma_tail <= eta^2,
    S_tail <= Bsoft^2 eta^2,
    Bsoft=G2 [3Gstar/ge+(Gstar/ge)^2].

The stronger eta^(10/3) bound for an a-weighted residual is NOT substituted
for this a_star-weighted tail. Very soft modes can have a_star only one.
Small-source relative linearity is not assumed uniformly in s.

For the separate quartic-capacity bound, eta^(10/3) is valid:

    I4_tail <= (3/5) G2^2 (3+u_star)^(4/3) u_star^(2/3)
                       (gc/ge)^(2/3) eta^(10/3),
    u_star=Gstar/ge.

Its finite-band endpoint envelopes use decreasing t^2,u_s and increasing
V_s^2. It has no a_star factor and does not inherit the weaker S-tail.

All displayed continuum inequalities are analytic. Their binary64 endpoint
evaluations are not a directed-rounding interval proof. Numerical controls
therefore retain the assigned 10^-10 arithmetic allowance, test nesting,
and require the final two upper estimates of Gamma, S and I4 to change by less
than 1%. Failure remains an unqualified receipt; neither the grids nor the
criterion are changed after looking at a bound. The enclosures and their
widths remain visible even when the numerical controls pass.

## Optional connection to the saved point-source linear coefficient

For the same linear parent, Q_R has Fourier window

    W(x)=15 j2(x)/x^2=(15/16) integral_-1^1 (1-u^2)^2 cos(xu) du.

Thus |W|<=1 and 0<=1-W<=min(2,x^2/14). Set
D=sigma^2/(2ell^2)+R^2/(14ell^2) and qc=sqrt(2/D)>1. The previous
point-source quadrupole integrand f(q)>=0 has conservative envelopes

    f<=Clo*q^2 (q<=1), Clo=4/(15*pi*mu_floor^2),
    f<=Chi*(q^-2+2q^-4+q^-6) (q>=1), Chi=8*M2/(15*pi),
    M2=(ge/gc)[2 atan(1/t0)+t0/(1+t0^2)].

Therefore the finite-source/readout change from the exact linear point
coefficient is bounded by GM/ell^3 times

    D*Clo/5
    +D*Chi[(qc-1)+2(1-1/qc)+(1-1/qc^3)/3]
    +2*Chi[1/qc+2/(3qc^3)+1/(5qc^5)].

The saved point coefficient remains a numerically qualified approximation,
not an exact constant. Report this correction bound and the nonlinear
difference bound separately. A combined nominal interval does not erase
the inherited point-quadrature uncertainty or become a Cassini likelihood.

## Execution and claim ceiling

The companion has no work on import and requires --run. It imports no
producer, authenticates the saved point result, uses one NumPy thread,
and creates one exclusive result or failure receipt. Ceiling: 120 seconds,
256 MiB, checked between refinements. No PDE, optimizer, fit, trajectory,
software installation, or other-account work occurs.

Controls include cubic/source identities, the quartic secant identity,
the adjoint normalization, Gaussian/window moments, positive enclosure
ordering, nested refinement, and saved-result custody. No astrophysical
success threshold is used. This is a diagnostic of an expressly changed
effective parent. Native source/length selection, dynamical formation,
causality, the photon metric, measured Solar structure, and shared
accelerating cosmology remain unresolved.
Selecting a particular ell after examining Solar certificates would be
development selection/calibration, not a new Solar prediction. Any later
galaxy evaluation must retain that same disclosed ell without retuning.
