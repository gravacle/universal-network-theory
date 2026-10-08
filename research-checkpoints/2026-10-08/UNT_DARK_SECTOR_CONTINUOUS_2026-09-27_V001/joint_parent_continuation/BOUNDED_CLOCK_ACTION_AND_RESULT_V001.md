# Bounded clock model with physical galaxy coupling

2026-10-03. The bounded-clock background is a constructive analytical and
numerical success within its stated constitutive assumptions. It avoids
the quartic clock's forced early radiation-like excess. A finite redshift
test nevertheless rules out two cold illustrative cases if the clock is
kept stationary and aligned throughout a galaxy. The full vector/clock
response, not another fitted galaxy curve, is the immediate question.

This note records the completed arithmetic, supplies an explicit spatial
completion, and qualifies the original minimum-state length estimates.
It does not claim native formation, an observed fit or Stage 3 completion.

## Completed numerical check

BOUNDED_CLOCK_SHARED_PREDICTION_V001.md froze the equations, grid and gates
before execution. The standard-library script completed in0.003 seconds,
peak21.2MB, with all288 controls passing. The largest independent u-variable
or derivative discrepancy was1.293e-13 against1e-10; charge residuals were
at most2.221e-16 against2e-13. No gates changed, observations scored or
existing scientific results rerun. Two internal source-only reviewers
independently checked the constitutive algebra and its interpretation.

With the adopted Hv=60.0641 km/s/Mpc, KB=1, a0=1.2e-10 m/s^2 and
M_b=1e11 solar masses, the arithmetic yields:

| eps | Uniform fractional bound on dust excess | Maximum adiabatic speed km/s | Minimum-state length Mpc | Nominal outer scale kpc |
| --- | ---: | ---: | ---: | ---: |
| .01 | .00498756 | 10566.3 | 140.720 | 5976.0 |
| .0001 | .0000499988 | 1059.89 | 14.4017 | 1307.5 |
| .000001 | .0000005000 | 105.993 | 1.44083 | 281.8 |
| .00000001 | .0000000050 | 10.5993 | .144084 | 60.7 |

The speed is c sqrt(max dP/drho), NOT every coupled propagation speed.
The lengths use the asymptotic Q=Q0 state and a conditional quasistatic
formula; they are NOT solved present-day galaxy predictions. Larger
background charge changes the contact, and the aligned branch can reach
the rate bound before these nominal radii. The next sections make those
limitations explicit rather than silently promoting a convenient scale.

## One explicit spatial completion

Use c=1 and phi dimensionless in this section; physical a0 means a0/c^2
in inverse-length expressions. As a credited effective architecture, take
the metric, unit-timelike vector U and scalar structure in
[Skordis and Zlosnik equation5](https://arxiv.org/html/2007.00082v3):

    S=integral sqrt(-g)/(16 pi G_tilde) [
       R - KB F_ab F^ab/2 + 2C a^b partial_b phi
       - C Y - C J(Y) + 2 K(Q) - lambda(U^2+1)] + S_ordinary[g],
    C=2-KB, F_ab=2 nabla_[a U_b], a^b=U^a nabla_a U^b,
    Q=U^a partial_a phi,
    Y=(g^ab+U^a U^b)partial_a phi partial_b phi.

This supplies the missing acceleration-phase operator and common matter
metric as explicit ADOPTED physics. We choose K=8 pi G_tilde P_bounded,
with P from the frozen note, and the new spatial function

    b=(1+lambda_s)a0, lambda_s>0, 0<KB<2,
    J(Y)=lambda_s[sqrt(Y)sqrt(Y+b^2)-b^2 asinh(sqrt(Y)/b)],
    j(Y)=J_Y=lambda_s sqrt(Y)/sqrt(Y+b^2).

This J is specified, not an adjustable function after comparison. It is
NOT the earlier soft-spectrum galaxy law: none of its old fits transfers.
The full displayed action defines energy/stress by metric variation, but
its bounded branch, formation and coupled perturbations are unproved.

In a spherical aligned weak-field window where the clock source/mass and
time dependence can actually be neglected, let

    Ghat=G_tilde/(1-KB/2), GN=(1+1/lambda_s)Ghat,
    gNhat=Ghat M_b/R^2, gN=GN M_b/R^2.

The positive scalar gradient obeys j(g_phi^2)g_phi=gNhat, hence

    g_phi^2=[gNhat^2+gNhat sqrt(gNhat^2+4 lambda_s^2 b^2)]
            /(2 lambda_s^2),
    g=gNhat+g_phi.

It gives g~sqrt(gN a0) at low field. At
gN >> (1+lambda_s)^2 a0 it instead gives

    g/gN=1+(1+lambda_s)^3 a0^2/(2gN^2)+higher orders.

These are derived conditional limits, not disk solutions or measured fits.
The static spatial response is elliptic away from zero gradient; its
degenerate zero-field limit is not a complete stability certificate.

In this completion G_cos=G_tilde, so

    G_cos/GN=(1-KB/2)lambda_s/(1+lambda_s)<1.

Cosmic normalization must use that same ratio. Taking lambda_s to infinity
is not an innocuous way to identify the two constants: at fixed gN the
force tends gN+sqrt(a0 gN), and the high-field expansion is nonuniform.
The scalar/vector benchmark's equation6 explains the conditional static
mass term; its published observational successes are not used as ours.

Count seven phenomenological constants/state numbers: a0, A, eps, Q0,
I0, lambda_s and KB, as well as the adopted functional and coupling choices.
GN and c set measured units. Redundant scalar origin is not an extra fit.
The constants need not all be free after native derivation, but none is
secretly fixed by nomenclature. Initial perturbations and formation remain
additional unresolved inputs. No dark record halo has been introduced;
an independent cosmological charge abundance nevertheless remains.

## A response coefficient is not automatically a physical pole

For a current cosmological state Qbar>Q0, at fixed coordinate phi_dot,

    partial_N [N P(phi_dot/N)]=-rho,
    partial_N^2 [N P(phi_dot/N)] at N=1 = Qbar^2 P_QQ,
    delta^2(NP) = P_QQ(delta phi_dot-Qbar delta N)^2/2.

The scalar variation and source contact therefore belong together. At fixed
canonical charge Pi=a^3 P_Q, the Hamiltonian is N a^3 rho(Pi/a^3), affine
in N. Its bare second lapse derivative vanishes. These different held
variables are not contradictory predictions and cannot be interchanged.

Define a fixed-velocity contact normalization, not an established pole:

    mu_contact^2=8 pi G_cos Qbar^2 P_QQ/[c^4(2-KB)],
    mu_contact^2 c_ad^2
      =8 pi G_cos(rho+P)/[c^4(2-KB)]
      =3(Hv/c)^2 q d/(2-KB).

For the bounded model its curvature factor is S_local=q d/c_ad^2;
at zero charge this tends S0=4/(eps^2 D). S_local increases with q.
The numerical table used S0, not an inferred present-state S_local.
This identity is generic to this shift-symmetric clock response, not unique
UNT evidence. A physical pole/range requires eliminating the FULL coupled
constraints on the same charged background with the actual boundary data.

## A finite redshift test of the aligned branch

Consider the exact static spherical line element
ds^2=-N(R)^2 c^2 dt^2+B(R)^2 dR^2+R^2 dOmega^2. Let the vector be aligned
with static observers and phi=omega t+psi(R). Then Q=omega/N. The bounded
branch therefore imposes, between outer and inner points,

    Delta ln N = ln(N_out/N_in)
       < ln(Qmax/Q_out) <= .5 ln(1+eps).

No arbitrary potential zero or constant rescaling of coordinate time can
remove this lapse-ratio bound. A radial psi does not affect Q while the
vector is aligned. Circular geodesics have v_c^2/c^2=d ln N/d ln R, using
the local orbital speed and circumferential radius. A flat-speed interval
thus requires

    (v_flat^2/c^2) ln(Rout/Rin) < .5 ln(1+eps).

For the same illustrative mass/a0, BTFR gives v_flat=199.7683 km/s.
One radial decade requires Delta ln N=1.02241518087e-6. Even at the most
permissive zero outer charge, eps must exceed2.04483245240e-6. The eps=1e-6
and1e-8 rows can sustain at most0.48904 and0.0048904 decades respectively
within this aligned bounded branch. This is a necessary-condition failure
of those illustrative realizations, NOT a new empirical fit or a rejection
of every vector/clock network. The other two rows merely avoid this bound.

Nonzero outer cosmic charge tightens it to ln(Qmax/Qbar). Matching to the
SAME background is compulsory; replacing Qbar by Q0 inside a galaxy is
a changed preparation unless its dynamics and energy are demonstrated.

## The constructive alternative must solve the vector and clock

A spatial vector or time-dependent phase can alter Q. Its freedom is not
an arbitrary rescue function. In the static local orthonormal frame set
q_t=omega/N, w=psi'/B, and U=(cosh theta,sinh theta). Then

    Q=cosh(theta)q_t+sinh(theta)w,
    p=sinh(theta)q_t+cosh(theta)w, Y=p^2.

For a future-directed timelike phase gradient q_t>|w|, the minimum Q
over allowed vector orientations is sqrt(q_t^2-w^2). Thus where q_t
already exceeds Qmax, an orientation rescue requires
w^2>q_t^2-Qmax^2. This is only a kinematic requirement; it does not pay
the vector's gradient energy or solve its field equation. A spacelike
phase gradient needs separate treatment, not this timelike formula.

The radial equations have now been derived and independently checked below.
The next calculation must SOLVE them with a specified background and
central source, not derive the same equations again. Establish whether a
regular branch can meet the force, finite-redshift and bounded-Q requirements
simultaneously. Do not fit a radial Q, orientation or phase profile. A native
waveform job is relevant only if it fixes a named coefficient or state
selection in this physical problem.

## Complete stationary radial equations

Here c=1, a prime denotes d/dR and n_lapse=ln N, not the charge density.
Retain the unit-vector rapidity theta. Define

    e=[cosh(theta)n_lapse'+sinh(theta)theta']/B,
    Lx=KB e^2+2C ep-C p^2-C J(p^2)+2K(Q),
    Dp=C[e-p(1+j)], Z=KB e+C p.

The Maxwell and acceleration terms are exactly KB e^2 and2C ep.
Up to the gravitational boundary term the reduced exterior action is

    integral dR [2N(B+1/B)+4R N'/B+NB R^2 Lx],

times the common angular/time normalization. The scalar shift current and
vector orientation equations are

    Cflux=2NR^2[cosh(theta)Dp+sinh(theta)K_Q], Cflux'=0,
    sinh(theta)[Z'+2Z/R]=B[Dp Q+K_Q p].

The two diagonal metric equations are

    0=2B-2/B+4R B'/B^2
      +B R^2[Lx-2Z cosh(theta)n_lapse'/B
                -2q_t(sinh(theta)Dp+cosh(theta)K_Q)]
      -[2R^2 cosh(theta)Z]',

    0=2(1-B^-2)-4R n_lapse'/B^2
      +R^2[Lx-2Ze-2w(cosh(theta)Dp+sinh(theta)K_Q)].

These are vacuum EXTERIOR equations; ordinary source/interior matter terms
must be added or matched, not discarded when setting a galaxy boundary.
Keep them undivided at theta=0; dividing by sinh(theta) can lose branches
or manufacture a singular numerical problem.

The off-diagonal metric equation was NOT dropped by assuming a diagonal
metric. Before fixing it, use ds^2=-N^2dt^2+B^2(dR+Vdt)^2+R^2dOmega^2.
Then q_t=(omega-V psi')/N and
e=[(N cosh(theta))'-(BV sinh(theta))']/(NB). Varying V and subsequently
putting V=0 gives, after the orientation equation,

    E_V=(B^2 q_t/N) Cflux.

The stationary Einstein-Hilbert shift variation is zero there. Thus with
omega!=0 and no additional radial energy flux, the full stationary
off-diagonal constraint REQUIRES Cflux=0. It is not a freely omitted field
equation. Under that condition the other equations simplify to

    e=p(1+j)-tanh(theta)K_Q/C,
    sinh(theta)[Z'+2Z/R]=B K_Q w/cosh(theta),
    Lx-2Ze=-KB e^2-C[p^2+J]+2K.

Consequently an EXACTLY aligned stationary configuration requires K_Q w=0.
Where K_Q!=0, this forces w=0 and then e=0, hence N'=0. A spatially
varying lapse therefore needs the non-aligned branch or time dependence.
For the bounded law K_Q=0 only at isolated clock rates; alignment cannot
generally maintain the minimum rate while N varies either. The earlier
spherical galaxy formula is an approximation requiring controlled neglect
of these terms, not an exact static solution of the completed action.

This does not contradict using a leading weak-field approximation; it
identifies the previously neglected response and the regime that must be
checked. Cosmological time dependence and any incoming/outgoing matter
flux change the stationary constraint. They must be included explicitly
when matching the galaxy to an expanding, charged background.

## An exact constructive branch and the state selection question

The aligned restriction does NOT exclude regular expanding solutions.
For an exact de Sitter patch put f=1-Hv^2 R^2, N=sqrt(f), B=1/N,

    tanh(theta)=Hv R,
    phi=Q0[t+ln(f)/(2Hv)].

Then q_t=Q0/N, w=-Q0 Hv R/N, but Q=Q0 and p=e=0 exactly. The clock is
regular in the expanding flat slicing, whose proper time is
tau=t+ln(f)/(2Hv). The divergent static-chart boost near its horizon is
not a divergent local clock rate. This explicitly demonstrates how the
vector/clock degrees of freedom evade the aligned lapse restriction.
It is the zero-charge limiting vacuum, not the present charged universe.

More generally, wherever a smooth synchronous geodesic time tau exists,

    U_mu=-partial_mu tau, phi=Q0 tau,
    F_mu_nu=0, a_mu=0, Y=0, Q=Q0, K_Q=0.

The complete constrained variation leaves just the vacuum stress from K0.
This is not justified merely by substituting zero terms in the action:
write s_constraint=U^2+1 and Theta=nabla_mu U^mu. At this background,
delta Y=-Q0^2 delta s_constraint and
delta(a^mu partial_mu phi)=-(Q0/2)U^mu partial_mu delta s_constraint.
After integration, the non-vacuum first variation is canceled by the
normalization multiplier lambda=C(Q0 Theta+Q0^2), with the action's stated
sign convention. Transverse vector and scalar equations have no leftover
source. Einstein-Lambda geometries are therefore a competing exact branch,
locally also around a mass where such a geodesic slicing is regular.

This result establishes neither global caustic freedom nor perturbative
stability. That branch uses the Einstein prefactor G_tilde, not automatically
the MOND branch's locally calibrated GN. It gives Einstein gravity, NOT
the desired galaxy enhancement. The action admits it without a record halo;
it does not automatically select the modified-force branch. An actual
cosmological charge/history and baryonic formation must determine the
branch. Choosing the desired phase profile after fitting a rotation curve
would evade that scientific obligation rather than satisfy it.

The next decisive question is now sharper: does nonzero conserved cosmic
charge, with a specified ordinary-matter formation history, select a regular
tilted solution with the modified galaxy force, or does it evolve toward
the competing Einstein branch? Work from the derived radial equations and
retain the time-dependent terms where a stationary approximation fails.
First derive the charged small-source/asymptotic boundary response needed
to pose that problem; do not restart the already-completed source algebra,
polynomial screen, homogeneous grid or old galaxy fits. A branch choice
must not masquerade as an independent prediction.

## Cosmological charge transport cannot be frozen away

The static orientation equation imposes an additional sign test. For
K_Q>0, B>0 and D_Z=Z'+2Z/R>0, theta and w have the same sign, giving
Q=q_t cosh(theta)+w sinh(theta)>=q_t. Such a tilt cannot lower the clock
rate to escape the lapse cap. A rate-lowering tilt requires D_Z<0.
In the intended leading deep-MOND fields e=p=v^2/R, one has
Z=2v^2/R and D_Z=2v^2/R^2>0. This sign survives corrections only when
their derivatives satisfy |delta Z'+2delta Z/R|<2v^2/R^2; pointwise
closeness of the fields alone does not establish it. This restricts the
static zero-current approximation, not every cosmologically matched branch.

The complete shift-symmetric phase current of the proposed action is,
apart from the common normalization,

    j^mu=C a^mu-C[1+J_Y](g^(mu nu)+U^mu U^nu)partial_nu phi
          +K_Q U^mu,
    nabla_mu j^mu=0.

In a homogeneous flat FLRW geometry written with areal radius R,

    ds^2=-dt^2+[dR-H(t)R dt]^2+R^2dOmega^2,
    U^mu=(1,HR,0,0), phi=phi(t).

Exactly F=a=Y=0, Q=phi_dot and j^mu=K_Q U^mu. Therefore, putting
nu=K_Q (proportional to the physical charge n=P_Q),

    partial_t nu+R^-2 partial_R(R^2 H R nu)
       =nu_dot+3H nu=0.

A fixed-areal-radius boundary carries charge flux4 pi H R^3 nu per cosmic
time. A moving boundary uses j^R-R_b_dot j^t; the relative flux vanishes
at a comoving boundary but its location and data evolve. One cannot impose
both frozen charged cosmological data and zero radial flux in a static
areal chart and claim that nothing physical changed.

The first linear charged-background bridge has also now been derived.
Use cosmic proper time, Newtonian-gauge lapse Psi, U_i=partial_i alpha,
and phase phi=phi_bar(t)+varphi. Define

    E=alpha_dot+Psi, chi=varphi+Q alpha,
    gamma=varphi_dot-Q Psi, Z_linear=KB E+C chi.

Since Qdot=-3H c_ad^2 Q, chi_dot=gamma+QE-3H c_ad^2 Q alpha.
Expanding the OWNED action to quadratic order, the terms that vary with
the longitudinal vector are proportional to

    a [ KB |grad E|^2+2C grad E dot grad chi-C |grad chi|^2
        +K_Q{2 grad alpha dot grad varphi+Q |grad alpha|^2} ].

The last two terms retain the background-charge contribution from unit
normalization. Varying alpha at fixed varphi gives, for nonzero spatial
wavenumber with appropriate boundary conditions,

    Z_linear_dot+H Z_linear=K_Q chi+CQ(E-chi).

Internal review separately checked this against the primary action's
linear cosmological equations. The new J_Y(0)=0 is consistent with this
linear expansion. It is not the nonlinear galaxy equation; the cubic
spatial constitutive response and full constraints must be retained for
that problem. Z_linear is not the static radial Z, although their spatial
gradients correspond in the relevant perturbative limit.

Let zeta=Q/H and Omega_enthal=8 pi G_cos(rho+P)/(3H^2), with c=1 and
rho,P the CLOCK sector. Then K_Q/H=3 Omega_enthal/zeta and exactly

    (C zeta-KB) E/chi = C(zeta+1)-3 Omega_enthal/zeta
                        +Z_linear_dot/(H chi).

This form assumes chi!=0,H!=0; use the unnormalized equation otherwise.
Freezing Z_linear would discard the LAST term. The exact resulting error
in E/chi is Z_linear_dot/[H chi(C zeta-KB)]. A small denominator demands
a better dynamical treatment; it is not an established physical pole.
Neither this equation nor small HR establishes a propagation speed. Since
the wavenumber cancels from this identity, a subhorizon wavelength alone
does not bound the neglected time term. At zero charge avoid normalized
fluid0/0 expressions and use the action directly.

The next task is to use this retained-current response with the remaining
coupled metric/phase equations to set a controlled galaxy boundary problem.
Specify an ordinary-source/formation history and common cosmological charge,
count Q0/H among its physical inputs, and test rather than assume the
smallness of the discarded time response. Keep full nonlinear clock terms
if delta Q approaches the bounded-rate margin. This is a calculable
network clock/expansion effect, not permission to fit an arbitrary flow.

The homogeneous background and the conditional galaxy limits are now
explicit, but the matched combined solution is NOT established. Lens and
growth predictions require that solution and its constrained perturbations.
The two distinct CMB investigations, early thermal preparation and all
other ledger obligations remain open. This is constructive model progress,
not yet a demonstrated reduction of independent abundance assumptions.

## Reproducible evidence

The original protocol, script and JSON remain unchanged:

| File | SHA256 |
| --- | --- |
| BOUNDED_CLOCK_SHARED_PREDICTION_V001.md | a95ba5941d3b73fd57d415b7faeb37afe8d85ade571b0b77b8f676f87c27708f |
| bounded_clock_shared_prediction_v001.py | dd3d22e143e10b977fb7c0d6a2ce0a7cd260e0ddb077e3a9cf56e9e471f0b896 |
| BOUNDED_CLOCK_SHARED_PREDICTION_V001_RESULT.json | 0c1f13e816c7026f861bf6a4e486792882133fc91a3cd64672caa558e43bdc73 |

Redshift illustrations are direct arithmetic with those same constants,
not a new dataset. No external observation, software install, parallel
numerical job, sealed artifact, release or independent final review occurred.
