# Expansion coupling from the spatial response gradient

2026-10-04. New analytic candidate screen under V009, independently checked
by endpoint_equations_check. This is an agent algebra review, not external
peer review. No completed galaxy or Solar calculation is rerun.

The smallest changed covariant gradient considered here preserves the
aligned static galaxy equations but does not activate a new late-time
condensate at the adopted 100-pc length. Its expansion correction is
controlled by H ell/c, not by an adjustable occupation alone. This closes
this particular bridge, not the shared-model question or UNT generally.

## Premise and retained assumptions

Use metric signature (-,+,+,+), a unit timelike clock normal u, and spacelike
response vectors y with u.y=0. P projects orthogonal to u. Retain the
linear galaxy source h(g)=g, positive quartic potential, positive measure
C nu(delta), and J_delta=kappa delta^2 ell^2. The static source is zero in
homogeneous FLRW. There is no added constant vacuum offset in this screen.
Ell=100 pc remains a disclosed development choice, not a native prediction.

The NEW premise changes only the spatial derivative operator, from the
fully projected norm to

    G_new = P^(alpha beta) (nabla_alpha y_mu)(nabla_beta y^mu).

The differentiated vector index is no longer projected. This is an actual
change of action, not a consequence already contained in the previous
spatial model. For projected D and extrinsic curvature K,

    G_new = |D_i y_j|^2 - |K_ij y^j|^2,
    Delta L = + J_delta |K_ij y^j|^2/2.

Both the added value and its first variations vanish on an aligned static
foliation K_ij=0. Thus the static field equations, not just the background
action value, agree there. Perturbative dynamics need not agree. In FLRW,
physical q^i=a y^i gives G_new=-H^2|q|^2. An isotropic ensemble or equivalent
orthogonal triad is required; a generic single-vector stress is not assumed
isotropic. The positive kinetic term is m_delta |P nabla_u y|^2/2.

## Lapse variation and stress

For this section c=1; dots are metric proper time after variation. Include
C nu in every integral and define

    T  = C integral nu m_delta |qdot|^2/2,
    V2 = C integral nu kappa delta^2 |q|^2/2,
    V4 = C integral nu u4 |q|^4/4,
    V  = V2+V4,
    B  = C integral nu J_delta |q|^2 = 2 ell^2 V2,
    D  = 3 M^2 - B/2.

With lapse N retained, H_N=adot/(N a), and T_N formed from qdot/N,

    L_hom = N a^3 [-D H_N^2 + T_N - V].

Flat FLRW and minimally coupled ordinary matter give

    3 M^2 H^2 = rho_o + T + V + B H^2/2,
    rho_y = T+V+B H^2/2,
    p_y = T-V-B H^2/2 - (H Bdot+B Hdot)/3.

The field equations are

    m_delta(qddot+3H qdot)
      + kappa delta^2[1-(H ell)^2]q + u4 |q|^2 q = 0,
    (2 M^2-B/3) Hdot = -(rho_o+p_o+2T) + H Bdot/3,
    D addot/a = V-2T-(rho_o+3p_o)/2+H Bdot/2.

These are a background reduction of the changed action. Positive D is not
a certificate of scalar/vector/tensor constraint health or causal stability.

## Decisive conditions

A nonzero constant-q, constant-H mode requires

    u4 |q_delta|^2 = kappa delta^2 [(H ell)^2-1].

For positive potential coefficients it therefore requires chi=H ell/c>1
in SI units. Inertia drops out of this necessary condition. It is not a
sufficient existence or stability proof of a self-consistent de Sitter
branch. Exactly zero classical initial modes still remain zero; spontaneous
quantum preparation or stochastic seeding is not supplied by this action.

The lapse constraint also prevents a large prepared amplitude from hiding
the small geometric coefficient. For nonnegative rho_o, T and V4,

    3 M^2 H^2 = rho_o+T+V4+(1+chi^2)V2,
    B/(6 M^2) <= chi^2/(1+chi^2).

In c=1 conventions, if the separate bare-mode speed assumption J_delta/m_delta
<=1 is imposed, Cauchy-Schwarz yields

    |H Bdot| <= 4 chi sqrt(V2 T) <= 2 chi(V2+T).

This bounds the extra acceleration numerator as well. The speed premise is
conditional; it does not establish the characteristics of the coupled
metric/clock system. Nor does the bound exclude acceleration from a
previously prepared, slowly rolling potential. That possibility retains the
unselected energy, occupation and clock obligations already recorded in
GRADIENT_PARENT_CLOCK_SCREEN_V001.md.

For illustration use H=70 km/s/Mpc, not a fitted or newly measured value.
At ell=100 pc, chi is about 2.34e-8 and chi^2 about 5.45e-16. Activation
would instead require ell>c/H, about 4.28 Gpc at this H, or a different
operator. Neither arbitrary large initial amplitudes nor a new inertia
value changes this threshold. No length or coefficient is fitted here.

## Numerical verification fixed before execution

GEOMETRIC_GRADIENT_EXPANSION_V001.py performs only inexpensive unit arithmetic
and local algebra controls; it is not a cosmological integration or an
observational test. Inputs are H70, ell100pc, c=299792458 m/s and the exact
IAU parsec expression 648000 AU/pi with AU=149597870700 m. It checks the
Lorentzian contraction against the projector identity on three declared
matrices; verifies a centered lapse derivative against the analytic
constraint; and exercises the positive-energy bound on four declared
dimensionless configurations. Algebra controls use relative/absolute
2e-12 and the finite-difference lapse check 2e-8. The physical decision is
the analytic chi>1 condition, not a tolerance fitted to the result.

## What this changes in the shortest path

Do not run a clock-inertia or amplitude sweep to repair this particular
late-time geometric activation mechanism. It cannot change the necessary
condition. A coefficient multiplying the new operator would be another
assumption; at the stated scales an activation coefficient would have to
exceed 1/chi^2, about 1.8e15, with a new stability and galaxy matching burden.
This is not automatically an independent dimensional scale: for example,
c^2/a0 is already constructible from the galaxy acceleration scale. But
choosing an operator to use it, and selecting its dimensionless coefficient,
remain physical premises until derived or independently tested.

The next useful question is operational: can an explicit network
clock/ruler/redshift law produce a consequential measured expansion
prediction while preserving the same galaxy mechanism? A coordinate or
unit redefinition alone cannot change observables. An arbitrary chosen H(z)
or a separately prepared negative-pressure energy budget is not the missing
shared explanation. Audit that alternative before another costly solver.

The previous one-invariant and trace-clock restrictions in
SHARED_CONSTITUTIVE_ALTERNATIVE_SCREEN_V001.md and
TRACE_CLOCK_CLOSURE_AUDIT_V001.md remain saved; this result does not rerun
or enlarge their domains. Early radiation, primordial fluctuations, lensing,
growth, mergers and both separate CMB lanes remain unaddressed by this test.

## Executed result and the larger coupling alternative

The 9 local arithmetic/algebra controls passed in about 0.09 s of command
elapsed time. Saved chi=2.3349486663870648e-8, chi^2=5.451985274662733e-16,
critical H=2.99792458e9 km/s/Mpc and critical length=4.2827494 Gpc. No worker
remains live. Result source SHA256 is
83dfef72b0084f6353a5a6031a1e46c174aff2c8d4d91d5dcee628c3fa6e882f.
The JSON retains the pre-execution note hash; this appended interpretation
is not part of that earlier frozen note.

Root and the same independent analyst also checked whether replacing ell
in ONLY the curvature coupling by another length L rescues the proposal.
It is a new coupling, not a change to the already calibrated static length.
Retain nu=A delta, Kb=kappa A Lambda^2/2, gc^2=kappa Lambda^4/u4 and
C=2M^2/Kb. On the nonzero stationary branch x=H^2 L^2>1,

    V2=M^2 gc^2(x-1)/3,
    V4=M^2 gc^2(x-1)^2/6.

At constant H this is stationary. At varying H, eliminating q at that value
is only an INSTANTANEOUS-MINIMUM, KINETIC-NEGLECTED TRACKING APPROXIMATION:

    F_hom=-3M^2 H^2+M^2 gc^2(x-1)^2/6,
    rho_o=F_hom-H partial_H F_hom
         =M^2[3H^2-gc^2(x-1)(3x+1)/6].

At its nonzero vacuum root,

    gc^2 L^2=18x/(3x^2-2x-1),
    partial rho_o/partial H^2=-M^2(9x^2+3)/(3x^2-2x-1)<0.

At arbitrarily large H the same tracking formula has negative ordinary
density. Moving L changes the vacuum scale but cannot give this branch a
continuous arbitrarily hot ordinary-radiation past. No coefficient sweep is
needed. This is not a proof against a nonadiabatic history or of a full-system
ghost. With constant inertia, the selected q(H) has

    T/V2=3/[8 omega_max^2] [xdot/(x-1)]^2.

Near x=1 the kinetic-neglect premise can fail, and a soft continuum cannot
be assumed uniformly adiabatic. Those qualifications are essential; no
unperformed time-dependent calculation is claimed.
