# Exact single-phase characteristic-crossing screen

2026-09-29. Analytical result and prospective quadrature-only diagnostic.
No producer, new EOS, fitted gap, shock prescription or merger simulation.
This uses the explicitly adopted scalar alpha-one current on the geodesic
zero-soft branch. It is not a proof that the native BS system is a fluid.

## Result and the scope of the contradiction

The retained positive harmonic-plus-quartic EOS has **genuinely nonlinear
relativistic acoustic characteristics at every finite positive action**.
A smooth compressive simple wave therefore loses its classical single-phase
description in a finite, explicitly calculable time on a prescribed flat
patch. A stronger weighted-gradient identity covers interacting wave
families while their state rectangle stays away from vacuum. This is an
actual limitation of a smooth single-phase continuation, not a numerical
failure and not an exclusion of the model before that event.

Positive material energy does not permit a globally Minkowski self-gravitating
solution. The flat problem below is a local material test. Section 5 specifies
what must additionally hold to turn it into a coupled-gravity certificate.
Neither its width nor elapsed time is fitted to an observed collision.

## 1. Exact EOS and Riemann invariants

Initially use c=1 and local inertial coordinates (t,x). Set

    rho=C beta e(I), p=C beta[I omega-e], omega=e_I,
    s^2=dp/drho=I e_II/omega, W=rho+p=C beta I omega,
    q=ln I, y=atanh v,
    D=cosh(y) partial_t+sinh(y) partial_x,
    S=sinh(y) partial_t+cosh(y) partial_x.

The exact current and Euler equations reduce to

    Dq+Sy=0,       Dy+s^2 Sq=0.                              (1)

Define F(I)=integral_0^I s(J) dJ/J. For a finite positive gap the integral
converges at zero action because s=O(sqrt I). With

    r_+=y+F(I), r_-=y-F(I),
    lambda_+=(v+s)/(1+vs), lambda_-=(v-s)/(1-vs),

equation (1) gives

    (partial_t+lambda_+ partial_x)r_+=0,
    (partial_t+lambda_- partial_x)r_-=0.                     (2)

The speed s is in light-speed units; physical characteristics are c*lambda.
The density factor C beta and the vacuum constant do not enter s or (2),
but remain in the stress sourcing the metric. Nothing here resets them.
Initial phase data are fixed by theta_x=-omega Gamma v and
theta_t=omega Gamma, not chosen independently of I and v.

For either family, with its other invariant held fixed,

    partial lambda_+ / partial r_+
       =(1-lambda_+^2) G/[2(1-s^2)],
    partial lambda_- / partial r_-
       =(1-lambda_-^2) G/[2(1-s^2)],
    G=1-s^2+d ln s/d ln I.                                  (3)

Thus it is G, not merely positive e_II or increasing p/rho, that decides
genuine nonlinearity.

## 2. A global positive-G certificate for the retained oscillator

For V(z)=k z^2/2+u z^4/4, k,u,m>0, use turning amplitude b and

    Q=k+(u b^2/2)(1+sin^2 theta),
    t=(u b^2/2)(1+sin^2 theta)/Q,          0<t<1.

Let alpha=<t>_P with positive normalized weight Q^(-1/2), and
beta_a=<t>_A with weight cos^2(theta)*sqrt Q on [0,pi/2]. These are not
the spectral weight beta. The already proved period/action identities give

    d ln omega/d ln b=alpha,
    d ln I/d ln b=2+beta_a,
    s^2=alpha/(2+beta_a),                 0<s^2<1/3.          (4)

A dot in this paragraph means d/d ln b. Since tdot=2t(1-t), normalized
weight differentiation gives the exact covariance identities

    alpha_dot=2alpha-3<t^2>_P+alpha^2 >= -alpha(1-alpha),
    beta_a_dot=2beta_a-<t^2>_A-beta_a^2
                 <=2beta_a(1-beta_a)<=1/2.

Consequently

    d ln(s^2)/d ln I
      =[alpha_dot/alpha-beta_a_dot/(2+beta_a)]/(2+beta_a)
      >=-5/8,
    G>1-1/3-5/16=17/48>0.                                  (5)

The bound is deliberately conservative and does not claim s^2 is monotone.
It requires no subtraction of close oscillator frequencies or third
action derivatives. It covers every finite positive-gap, positive-action
state of this EOS. The zero-action boundary and exact dust limit require
their separate treatment below. In the pure quartic limit s^2=1/3 and
G=2/3, so the limiting fluid is also genuinely nonlinear.

## 3. A fully specified smooth simple-wave test

Given one retained cosmic action I_b>0, prescribe the NEW local data

    I_0(x)=I_b exp[A f(x/L)],
    y_0(x)=F(I_0(x))-F(I_b),
    f(xi)=exp[-xi^2/(1-xi^2)] for |xi|<1, and 0 outside.
                                                               (6)

Here A>0 and L>0 describe this explicitly new compressive preparation;
they are not inferred merger data or a state already created by the old
formation pulse. It has finite positive density, subluminal velocity,
smooth compact perturbations and r_-=-F(I_b). Its density/momentum/energy
and any gravitational constraint solution must be retained. The right
flank is compressive because I_0 decreases while lambda_+ increases with I.

Let Lambda(xi)=lambda_+[I_0(xi),y_0(xi)]. The exact flat solution until the
first characteristic intersection is

    x=xi+c Lambda(xi)t,
    r_+(t,x)=r_+(0,xi),
    t_*=-1/[c min_xi Lambda'(xi)] < infinity.                 (7)

At t_* the map's Jacobian vanishes and a spatial derivative diverges;
I and v themselves remain inside their initial ranges. Thus the classical
domain ends before an assumed entropy reset or stream crossing can be used.
This is not a statement that density must already be infinite at t_*.

A certified upper bound needs no spatial root finder. At xi=L/2 put
I_*=I_b exp[A exp(-1/3)] and evaluate the exact EOS there. Then

    Lambda_q=(1-Lambda^2) s G/(1-s^2)>0,
    t_* <= 9 exp(1/3) L/[16 c A Lambda_q(I_*)].               (8)

The exact minimum in (7), or enclosing bounds on it, can refine this
witness. The EOS and one Riemann integral determine (8); no PDE is needed.

For an independently checkable cold expansion in inherited m=kappa=u4=1
normalization with k=R^2,

    e=R I+3I^2/(8R^2)+O(I^3/R^5),
    s_b^2=3I_b/(4R^3)+O(I_b^2/R^6),
    y_0=2s_b[exp(A f/2)-1]+O(s_b^3),
    Lambda=s_b[3exp(A f/2)-2]+O(s_b^3).

Thus fixed fractional-density waves have t_*=O[L/(c s_b A)] as they
become cold. They do NOT demonstrate gap-independent prompt collisions.
For exact dust s=0, the same family (6) has v=0 and no flat-space crossing.

A different, explicitly prescribed converging dust velocity gives a
different result. For example v_0(x)=-V(x/L)exp[-(x/L)^2], with 0<V<1,
and positive I_0, free dust has x=xi+c v_0(xi)t and first crossing
t_*=L/(cV). Fixed converging velocity, not low pressure alone, supplies
that finite time. This second state is not the limit of (6) at fixed A.

## 4. Two interacting families: a stronger local classical-domain test

In the flat system let alpha_x=partial_x r_+ and beta_x=partial_x r_-.
Choose any smooth integrating factor h(r_+,r_-) satisfying

    partial_- h=(partial_- lambda_+)/(lambda_+-lambda_-).

Along a plus characteristic the exact weighted gradient w=exp(h)alpha_x
obeys

    D_+ w=-a(r_+,r_-) w^2,
    a=exp(-h) partial_+ lambda_+>0,
    1/w(t)=1/w(0)+integral_0^t a ds.                        (9)

This follows by cancellation of the alpha_x beta_x term; it does not
freeze the other family. If the initial invariant rectangle obeys
min r_+ > max r_-, it stays away from I=0, while finite extrema bound
rapidity and I above. On that compact rectangle a has a positive minimum
a_min. Any w(0)<0 then forces classical breakdown no later than
-1/[a_min w(0)], unless another classical failure occurs earlier.
The analogous minus-family calculation is available with indices swapped.
This is a conditional finite-state theorem, not a uniform theorem through
vacuum, I=0 or the coincident dust characteristics.

## 5. Exact gravitational source terms and the local-patch qualification

A planar metric chart illustrates the terms that the flat screen omits:

    ds^2=-N^2 dt^2+A_g^2 dx^2+B_g^2(dy^2+dz^2),
    e0=N^-1 partial_t, e1=A_g^-1 partial_x,
    a_N=e1 ln N, K1=e0 ln A_g, Kp=e0 ln B_g, Lp=e1 ln B_g.

In this paragraph D=cosh(y)e0+sinh(y)e1 and
S=sinh(y)e0+cosh(y)e1, replacing their flat-coordinate expressions.
The exact current/Euler system has

    Dq+Sy=-Theta_geom,
    Dy+s^2 Sq=-a_geom,
    Theta_geom=cosh(y)(K1+2Kp)+sinh(y)(a_N+2Lp),
    a_geom=a_N cosh(y)+K1 sinh(y).

Its invariants therefore satisfy

    partial_t r_±+lambda_±^g partial_x r_±=S_±,
    lambda_±^g=(N/A_g)(v±s)/(1±vs),
    S_±=-N[a_geom±s Theta_geom]/[cosh(y)±s sinh(y)].        (10)

For FLRW this includes S_±=-H(v±3s)/(1±vs), rather than setting expansion
to zero while keeping its state normalization. The metric and its sources
still must satisfy the full Einstein/current constraints; equation (10)
is not a replacement for them or a planar model of an observed merger.

There is a rigorous conditional forced-gradient version. Write
p=-partial_x r_+>0, b=partial_x r_-, and take explicit x derivatives of
lambda_+^g,S_+ at fixed r_±. Suppress these plus-family subscripts in
the following formula. Along a plus characteristic,

    D_+ p=lambda^g_{,+} p^2+
       [S_{,+}-lambda^g_{,-} b-lambda^g_{,x}]p
       -S_{,-}b-S_{,x}.                                    (11)

If actual interval bounds give lambda^g_{,+}>=a0>0, the absolute values
of the square-bracket coefficient and final forcing bounded by B0,C0,
then D_+p>=a0 p^2-B0 p-C0. With

    p_+=(B0+sqrt(B0^2+4a0 C0))/(2a0),
    p_-=(B0-sqrt(B0^2+4a0 C0))/(2a0),

p(0)>p_+ implies breakdown no later than

    T_cert=ln[(p(0)-p_-)/(p(0)-p_+)]/sqrt(B0^2+4a0 C0).  (12)

For B0=C0=0 use T_cert=1/[a0 p(0)]. These are conditional ACTUAL-INTERVAL
bounds, not initial-only estimates. If the other family or geometry loses
regularity first, the intended smooth continuation has already failed.

To use the flat screen as a controlled local approximation requires a
qualified scale separation: small curvature over the packet and proposed
time interval, small expansion change H T, and an actual bound on the source
and transverse-gradient corrections. Schematically curvature bounds must
control |Riemann| L^2 and |Riemann|(cT)^2 in physical units. A small initial
Newtonian potential alone supplies neither interval certificate. Near the
flat blow-up point a naive small-error argument is not uniform; use a
forced criterion such as (11)-(12) or stop short of that region. A Minkowski
failure time without these checks is NOT a coupled-gravity merger exclusion.

## 6. Minimal prospective numerical use, if requested

The theorem itself needs no producer. An inexpensive optional EOS/readout
packet could retain all 1340 authenticated inferred labels, with their 1180
finite states and 160 exact-dust labels separated, and no new action fit.
Use (6) with the prospectively declared A=ln2 and L=the old 3.2 kpc source
scale. These are NEW synthetic initial-state choices, not observed merger
widths/amplitudes; no physical success threshold is attached. Preserve the
four spectrum labels even where their material normalization duplicates.

For each finite EOS, compute positive endpoint-safe action/period quadrature,
the covariance expression (5), the one Riemann integral and the witness
(8). Freeze quadrature/refinement and independent derivative checks before
root execution. Report t_witness/(L/c), t_witness/t_dyn and H*t_witness;
none by itself certifies the uncomputed curvature/current bounds. Dust
labels report the separate degenerate result, not a divided-by-zero time.
No spatial evolution, halo, collision age or fitted detector threshold is
needed. Memory is O(number of quadrature nodes), and the existing EOS
limits supply harmonic/quartic controls. A selected quadrature tolerance
is a numerical qualification, not an observational tolerance.

## 7. What a post-crossing merger prediction would additionally own

The current fixes one momentum at each point. Decreasing s does not add
phase-space dimensions. After its classical-domain boundary, predicting
two interpenetrating streams needs one of the following genuinely NEW
specifications, unless independently derived from native dynamics:

* a kinetic distribution with initial momentum structure and an interaction/
  collision law, retaining its same stress and gravitational coupling;
* multiple transported phases with their populations, interactions and
  interference/readout rule;
* a specified dispersive gradient operator with its coefficient, extra
  initial data, stress and physical validity scale;
* an entropy/shock completion with an energy/entropy channel and admissibility
  rule, not silently replacing the conservative EOS after the event.

Finite current conservation alone does not select among them. For an
observed lensing-offset merger, initial material velocities/actions, ordinary
gas versus stellar physics, constraints and the same-metric null readout are
also required. No offset follows by relabeling this one-phase fluid as
collisionless matter. The constructive result is a precise, calculable
endpoint of its existing classical prediction and a list of the actual
new constitutive data a further continuation would have to supply.

## Custody

- PREPARED_ACTION_COMPRESSION_DERIVATION_V001.md:
  `4e95a23d32367941948deb088e7f192b1f5269923d216c802586376d7d950d33`.
- HARD_MODE_COLD_HISTORY_CONSTRAINT_V001.md:
  `c4f80c78a6af1fadb472bc6bef9d3fb54302cc9b00ef0ae728a149b70b0bf067`.
- MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md:
  `64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3`.
- CLOSED_RELEASE_LENSING_AND_COLLISION_CONTINUATION_V001.md:
  `d7155fa296a29d64c93d7cc047c9498516fde61f100a7c7fff2529e8af583507`.

The positive-G covariance proof has been independently checked by the
native-scope lane. All characteristic/source formulas above are explicit
derivations for this retained EOS, not imported phenomenological transport.
