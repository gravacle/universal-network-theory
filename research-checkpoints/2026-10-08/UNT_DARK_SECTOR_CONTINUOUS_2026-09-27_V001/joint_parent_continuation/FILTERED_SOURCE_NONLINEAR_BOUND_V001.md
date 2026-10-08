# A nonlinear finite source bound for the averaged response

2026-10-04. Analytic test of FILTERED_SOURCE_SHARED_CANDIDATE_V001, not of
the previous linear-source gradient parent. The goal is to bound the ENTIRE
anomalous static Hessian without assuming that a small linear answer is the
full nonlinear answer. Use a declared Gaussian ordinary source of standard
deviation sigma=1e9 m, the already fixed Solar GM, uniform external field
e=2.32e-10 m/s^2, ell=100 pc and the same a0, r and spectrum. This is not a
measured Solar model, time-dependent ephemeris calculation or causal proof.

## Function space and fixed point

For Fourier convention f(x)=integral fhat(k) exp(ik.x) d^3k/(2pi)^3, use
the Wiener norm ||f||_A=integral |fhat(k)| d^3k/(2pi)^3. Vector norms are
Euclidean and matrix norms induced operator norms. Products obey the Banach
algebra bound. Constants belong to its unitization. Real fields are retained.

Let n be the external unit vector, b=e(n+v), and F(b)=(Dh)^T P/Kb as in the
candidate. The longitudinal Fourier projector is Pi_L=kk^T/k^2. Relative to
the constant background, the exact STATIC equations are equivalent to

    v=v_N + S_ell^2 Pi_L [F(e(n+v))-F(en)]/e,
    v_N=S_ell g_N/e.

The multiplier S^2 Pi_L has norm at most one in this space. This uses the
self-adjoint outer filter and cannot be applied to the old local source law.
We seek the decaying perturbation in the ball ||v||_A<=r0=.01. Existence and
uniqueness claimed below are IN THIS BALL, not among all possible states.

## Uniform response bounds including the soft spectrum

Define z=(e/gs)^2, F0=(1+z)^(-1/2), gamma=z/(1+z). Then

    h/he=(n+v)[1+gamma(2n.v+v.v)]^(-1/2),  he=e F0.

For t0=gamma(2r0+r0^2)<1, absolutely convergent binomial series bound its
first derivative J and the derivative of J by

    Jmax=(1-t0)^(-1/2)+gamma(1+r0)^2(1-t0)^(-3/2),
    DJmax=3gamma(1+r0)(1-t0)^(-3/2)
           +3gamma^2(1+r0)^3(1-t0)^(-5/2).

No numerical differentiation is used for these estimates. For each delta>0,
write y=y0(n+w), where y0 is its external positive equilibrium, and put
eta=kappa delta^2/(kappa delta^2+u4 y0^2). The exact mode equation becomes

    [I+2(1-eta)nn^T]w
      +(1-eta)[2(n.w)w+(w.w)n+(w.w)w]=h/he-n.

The constant inverse matrix has norm <=1. On ||w||_A<=s0=2r0, the nonlinear
remainder has norm <=3s0^2+s0^3 and Lipschitz constant <=6s0+3s0^2. If

    Jmax r0+3s0^2+s0^3 <= s0,   6s0+3s0^2<1,

each mode has a unique local solution with dependence on v bounded by

    Lw=Jmax/(1-6s0-3s0^2).

These estimates are uniform down to delta->0. No gapped truncation or
uniform adiabatic time approximation is used; the measure-zero delta=0
point is not divided by y0. The positive P-weighted average wbar obeys the
same bounds. In particular

    F/e = pref J(v)(n+wbar),   pref=F0 P(he)/(Kb e).

An analytic spectral upper bound avoids relying on a rounded numerical
quadrature for contraction. If he/gc >= .9+.9^3, every t_delta satisfying
t_delta+t_delta^3=he/[gc(delta/Lambda)^2] is >=.9. Hence

    pref <= pref_max=F0^2/(1+.9^2),
    Lip(F/e) <= L_F=pref_max[Jmax Lw+DJmax(1+s0)].

All gate inequalities above are checked before claiming contraction. The
bound is deliberately conservative; it is not the fitted local response.

## Finite source input and the Hessian bound

For rho=M exp(-R^2/(2sigma^2))/(2pi sigma^2)^(3/2), the exact Fourier input
norm is

    epsilon=||v_N||_A=GM/(pi ell^2 e) exp(x) E1(x),
    x=sigma^2/(2ell^2).

No special-function library is needed for an upper enclosure:

    exp(x) E1(x)=integral_0^infinity exp(-t)/(x+t) dt
      <= log((1+x)/x)+exp(-1).

This follows by splitting the integral at t=1 and bounding each positive
piece. Use this epsilon_upper, not a truncated small-x asymptotic value.
If L_F<1 and epsilon_upper<=(1-L_F)r0, Banach contraction supplies a
nonlinear static solution in the ball with

    ||v||_A<=epsilon_upper/(1-L_F).

The anomalous total force is delta g=Pi_L S [F(b)-F(en)]. Because
sup_k |k|/(1+ell^2 k^2)=1/(2ell), its spatial Hessian satisfies

    ||Hessian(delta Phi)||_infinity
      <= e/(2ell) L_F epsilon_upper/(1-L_F),
    |Q2|=|Hzz-Hxx|
      <= e/ell L_F epsilon_upper/(1-L_F).

The last step uses twice the operator norm. It is valid for the axisymmetric
source/external configuration and bounds the traceless central quadratic
coefficient, as well as that component difference elsewhere. The trace is
not assumed zero. The bound covers the full nonlinear anomalous field, not
only its deviation from the linear approximation. It may be much looser
than the actual coefficient.

## Fixed arithmetic and scope

Before execution use r0=.01, s0=.02, lower spectral root .9, and exactly the
source/constants stated above. Test the domain, modal self-map, modal
contraction, positive spectral-root margin, outer contraction and outer
self-map. Also check the units relation Q_bound=2 Hessian_bound and the
two equivalent filtered-input prefactors at scaled 2e-12. A failed gate
stays a failed certificate; do not loosen r0 or source width after seeing it.
Record all margins and the absolute bound regardless of its attractiveness.

This analytic result, if its gates pass, is a conditional existence/uniqueness
and force-Hessian bound for an adopted static action and Gaussian source.
Binary64 checks with large margins are not directed-rounding formal proofs.
It does not establish the actual Solar source, external-field evolution,
photon metric, time dependence, galaxy formation, or cosmology. In a
covariant completion the filter's metric variation must also be retained.

## Completed result

All eight frozen gates pass. L_F=.6478841742923833, input norm bound
8.559993697232982e-7 and solution norm bound2.4310164645484777e-6 give
|Q2|<=1.184193605291823e-34 s^-2 for the whole nonlinear anomaly. Arithmetic
took0.00053s internally. Result SHA256:
3317646ee61c629c2e4a370c2eb63ff17fb403abf503bc5c0f1cb7154175bd23.
No post-result change to a parameter or numerical gate occurred.

Both endpoint_equations_check and handoff_plan_review_v005 independently
accepted the stated proof without rerunning numerics. The second reviewer
confirmed soft-endpoint integrability (polarization weight proportional to
delta^(7/3)), the full contact and two-filter variation, and the Gaussian
norm. Use background-subtracted variations for the infinite uniform
external field. Both reviews retain the scope above; neither establishes
observational or cosmological superiority.
