# One response law supplies local gravity and an accelerating-sign stress

2026-09-28. Exact analytical consequence of the already adopted mechanical
response and covariant preferred-foliation interface. No new fit, action
term, numerical worker or change to the fixed galaxy calculations.

## Main result

With the existing high-acceleration matching condition J(infinity)=0, the
same mechanical function that supplies the galaxy response has positive
J and negative J_Y. Its complete clock-sector stress, averaged on a proper
normal slice with zero boundary flux, obeys

    rho_bar > 0,
    rho_bar + 3 p_bar = -2 M² <J> < 0,
    rho_bar + p_bar >= 0.

For the specific bounded-source parent the stronger trace-pressure bound is

    -1 <= p_bar/rho_bar < -5/9,

at finite field, with the upper endpoint approached in a uniformly
high-field limit. This is an accelerating-sign stress contribution. It is
not, by itself, a solved averaged Friedmann evolution or a proof that the
microscopic BS records already possess this metric coupling.

The result concerns the COMPLETE matched clock stress. The earlier weak
vacuum-subtracted excess remains radiationlike; there is no contradiction.

## 1. Keep the same constitutive law and its absolute matching

Use c=1 and M²=1/(8 pi G), with the same conditional action as the accepted
K0 derivation:

    S = M²/2 integral sqrt(-g)[R - 2 J(Y)] + S_m,
    Y = A_mu A^mu >= 0,    A_mu = u^nu nabla_nu u_mu.

The stationary weak-field interface is

    div[mu(|grad Phi|) grad Phi] = 4 pi G rho_b,
    J_Y = mu(sqrt(Y)) - 1.

The mechanical parent has h(g)=g/sqrt(1+g²/g_s²), bare stiffness K_b>0,
P(h)=K_b h-W_el'(h), and

    0 < P(h) < K_b h,     0 < P'(h) < K_b,
    F(g)=K_b g-P(h(g)) h'(g),    F'(g)>0.

These statements were proved in the prior mechanical work, not inferred
from a good galaxy fit. Hence at each finite g>0

    0 < mu(g)=F(g)/(K_b g) < 1.

The already declared matching J(infinity)=0 then fixes

    J(Y) = integral_Y^infinity [1-mu(sqrt(y))] dy > 0.       (1)

Its convergence follows from 1-mu(g)~C3/g^4, with
C3=P(g_s)g_s^3/K_b>0. Equivalently, using the full mechanical energy ledger,

    J(g²) = 2/K_b integral_h(g)^g_s P(s) ds.                 (2)

This uses exactly the previously adopted energy-reference condition. The
galaxy equation alone does not fix that additive constant. Shifting J by
an arbitrary constant would change the pressure result and is not licensed
by a rotation-curve match. The native volume/source matching remains a
separate construction task; no new constant has been chosen here.

## 2. Exact stress identity before assuming a cosmological fluid

Let f=J_Y and D=nabla_mu(f A^mu). The complete covariant stress, already
checked independently in K0_FLRW_SCALAR_REVIEW.md, is

    T_J^{mu nu}=M²[-J g^{mu nu}+2 f A^mu A^nu-2 D u^mu u^nu].

Its normal energy and one-third spatial pressure trace are

    rho_J=M²(J-2D),
    p_J=M²[-J+(2/3)Y f].

For a vector tangent to the preferred slices,

    D=D_i(f A^i)+Y f.

Consequently the local active trace combination is

    rho_J+3p_J = -2M²[J+D_i(f A^i)].                       (3)

Take a proper-volume slice average with no flux of f A through its boundary
(a compact closed slice, periodic domain, or explicitly justified zero-flux
boundary). The intrinsic divergence then integrates to zero exactly. Define

    Jbar=<J>,     ubar=<Y(1-mu)> >= 0.

Then

    rho_bar=M²(Jbar+2ubar),
    p_bar=-M²(Jbar+2ubar/3),
    rho_bar+3p_bar=-2M² Jbar,
    rho_bar+p_bar=(4/3)M² ubar.                             (4)

The generic conditions Jbar>0 and ubar>=0 give

    -1 <= p_bar/rho_bar < -1/3.

No spatial homogeneity of Y was required for (4). Isotropy of the stress
does require an appropriate gradient distribution: the anisotropic stress
2M² f[A^i A^j-(Y/3)q^{ij}] has not disappeared. For a nonzero boundary flux,
retain its contribution -2M²<V^{-1} boundary integral f A.dS> in rho_bar;
the zero-flux bounds must not be applied to an arbitrary finite galaxy box.

## 3. A sharper bound from this parent's bounded source

Set s=h(g), t=s/g_s in (0,1). Since

    g h'(g)=s(1-t²),
    u(g)=g²[1-mu(g)]=s P(s)(1-t²)/K_b,

and P is strictly increasing, equation (2) implies

    J(g²) > 2(g_s-s)P(s)/K_b,
    J/u > 2/[t(1+t)] > 1.                                 (5)

At g=0, u=0 and J=J(0)>0. Thus J>u pointwise at every finite field and
Jbar>ubar for any finite regular zero-flux averaging domain. Substitution
in (4) gives the stronger result

    -1 <= w_trace = p_bar/rho_bar < -5/9.                   (6)

The upper endpoint is approached at uniformly high field: as Y grows,

    1-mu ~ C3/Y²,    J~C3/Y,    u~C3/Y,
    rho_J,average ~ 3M² C3/Y,
    p_J,trace ~ -(5/3)M² C3/Y.

For inhomogeneous fields these asymptotics concern the corresponding
averages only when taking that limit is controlled. They are not a
prediction that the observed cosmological equation of state equals -5/9.
The absolute clock stress goes to zero in this high-field limit.

## 4. Why the previously derived weak excess is still radiationlike

Near Y=0 the same law has J(Y)=J0-Y+O(Y^(3/2)). Its FULL stress is

    rho_bar=M²[J0+<Y>+O(<Y^(3/2)>)],
    p_bar=M²[-J0+<Y>/3+O(<Y^(3/2)>)].                     (7)

Subtracting the homogeneous vacuum contribution gives positive weak excess
energy <Y> and pressure <Y>/3. That excess does not supply the missing
homogeneous dustlike mode in the K=0 cosmological calculation. Keeping the
matched vacuum contribution instead yields the negative active trace (4).
The two statements describe different subtractions of the same tensor.

In particular, one cannot claim that more small clock disturbances create
extra accelerating energy: their leading excess has the opposite active
trace sign. The new conclusion is that the COMPLETE matched response
remains an accelerating-sign source even beyond that weak expansion.

## 5. What this contributes to the joint dark program

The same function now has three linked consequences within this candidate:

1. Its derivative mu controls the extra stationary pull used in the galaxy
   calculation, without adding an invisible mass profile.
2. Its integral fixes the matched J0 and full stress; no separate function
   w(a) was fitted to produce negative pressure.
3. Its bounded-source construction constrains that stress by (6), rather
   than merely permitting a chosen sign at one operating point.

This is a constructive common-mechanism result in the conditional model.
To obtain an expansion history, solve the full metric/clock/matter equations
with a specified state, initial data and physical calibration. Averaging
their stress does not commute with averaging the nonlinear Einstein
equations; expansion variance, shear, lapse/acceleration and boundary terms
cannot be dropped. Local stability in arbitrary strong inhomogeneous states
also does not follow from this pressure inequality.

The underlying preferred-foliation action is an explicitly acknowledged
comparison framework, not claimed as a new action discovered here; see the
primary [Blanchet–Skordis formulation](https://arxiv.org/html/2404.06584v2).
The exact native source, record-addition and volume-increment results in
this folder constrain the still-needed matching to BS network degrees of
freedom. The present derivation adds a useful, falsifiable joint stress
constraint without pretending that matching is already complete.
