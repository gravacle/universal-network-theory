# One retained state determines response, pressure and phase transport

2026-09-28. Additive analytical bridge for the SAME positive-inertia mechanical
parent. No numerical worker, fit, change of the frozen force law, new clock
function, or substitution of a relaxed state for the prepared trajectories.

## Result

The held scalar orbits have an exact state label: their classical action I.
The SAME energy function e(I,h) determines their mean polarization, frequency
and homogeneous excitation pressure. Keeping the action and its phase in the
gravitational action supplies a conditional slow-evolution description rather
than inserting a measured mean mu into a stationary equation.

Two constructive restrictions come with that description. First, differentiating
energy across separately prepared amplitudes adds a preparation-action term;
it is not the fixed-state force. Second, a spatially stationary mean state must
satisfy its momentum/phase balance. Generic independently held local orbits do
not automatically form a stationary self-consistent galaxy.

The orbit identities below are exact. The slowly varying phase action is a
leading adiabatic reduction on an explicitly controlled finite band, not an
exact replacement of arbitrary coupled gravity/clock/mode evolution. The
complete system remains COUPLED_SPHERICAL_RESPONSE_PATHWAY_V001.md.

## 1. Exact orbit identities with the actual normalization

For one scalar mode, let b_delta=kappa*delta and use the unweighted physical
momentum p=m*y_dot in proper time. At fixed internal source h its Hamiltonian is

    H_delta=p²/(2m)+U_delta(y,h),
    U_delta=kappa*delta²*y²/2+u4*y^4/4-b_delta*h*y.          (1)

Here m,delta,kappa,u4 are positive. The measure w_delta and common gravitational
factor C are outside this per-mode Hamiltonian. For a finite positive band,
U is strictly convex and confining, with a unique minimum. Every energy
e>e_min(h) has one closed orbit and no separatrix. Define

    I(e,h)=(1/(2pi))*oint p dy
          =(1/pi)*integral_(y_-)^(y_+) sqrt(2m[e-U(y,h)]) dy,
    omega=2pi/T_period.                                    (2)

The actual saved end-ramp y,y_dot fixes e and hence I uniquely. I is not an
occupation chosen to match a galaxy or cosmic abundance. The minimum has
I=0 and is understood as the continuous limit of (2).

Differentiation of this positive orbit integral gives

    I_e=1/omega >0,
    I_h=b_delta*<y>/omega,
    e_I=omega,
    e_h|I=-b_delta*<y>,
    I*omega=<p*y_dot>=2<T_osc>.                            (3)

The moving turning points contribute no boundary term to the first derivatives
of I because the square-root integrand vanishes there. Angle brackets are
the time average on this single held orbit, not a ground-state, thermal or
diagonal-ensemble substitution. For independent modes, the Cesaro mean of a
sum is the sum of their orbit means; incommensurate periods are not required
for that linear statement.

Equations (2)-(3) also provide a response/frequency reciprocity relation:

    partial_I[b_delta*<y>] = -partial_h omega.              (4)

It is an exact check on a proposed common state description, not a new fit.
The action-angle and slowly expanding oscillator method has a primary
precedent in [Masso, Rota and Zsembinszki, section III](https://arxiv.org/pdf/astro-ph/0501381).
Our I includes 1/(2pi), so omega is angular frequency. Their homogeneous
scalar results do not supply our native state, acceleration coupling,
constraint equations or volume matching; those are retained explicitly here.

## 2. A held mean force is the derivative at fixed action

For the existing bounded source

    h(G)=G/sqrt(1+G²/g_s²),
    K_b=kappa*sum_j w_j,

the complete local weak-field mechanical energy at prescribed G is

    W_I(G)=K_b*G²/2+sum_j w_j*e_j(I_j,h(G)).

Thus its fixed-action derivative is exactly

    F_I(G)=partial_G W_I|I
          =K_b*G-h'(G)*B_bar,
    B_bar=sum_j w_j*b_j*<y_j>_(I_j,h).                     (5)

The matched additive constant has zero derivative and is unchanged. The
contact K_b*G²/2 is included here to display the complete mechanical force;
it must NOT be added again to the extra covariant action, where the matched
Einstein sector already supplies it. Setting all I=0 recovers the previously
eliminated stationary mechanical branch.

For the separately proved zero-rest, nonnegative monotone source histories,
every held orbit stays at y>=0. Its exact averaged equation and Jensen's
inequality give

    kappa*delta²*<y>+u4*<y>³
      <=kappa*delta²*<y>+u4*<y³>=b_delta*h,
    <y><=y_min(h).

Consequently the held mean F_I at those ACTUALLY prepared actions is at least
the relaxed force at the same G, strictly for excited positive-weight modes.
This establishes the sign without fitting the six computed examples. It is
not an instantaneous lag theorem, a statement about arbitrary initially
excited states, or a guarantee of a stationary gravitational solution.

If instead each final G is prepared in its own ramp, the actions are
I_j=I_j(G,T,history). The chain rule is

    dW_prepared/dG = F_I(G)+sum_j w_j*omega_j*dI_j/dG.       (6)

The second term is a change of retained state across experiments. It does
not vanish because the histories share a duration or shape. An exact example
is a zero-rest instantaneous quench: e_j(I_q,j(h),h)=0, and hence

    b_j*<y_j> = omega_j*dI_q,j/dh.                         (7)

This explicitly prevents identifying a quench-family force integral with
an absolute-energy endpoint. PREPARED_STATE_FORCE_VOLUME_CONSEQUENCES_V001.md
records the corresponding same-parent volume/work consequences.

The new common-ramp held-mean result and its deep-field quench limit describe
actual prepared families. They do not justify promoting that family to an
autonomous static law with I eliminated as a freely chosen function of G.
In particular, for a fixed positive finite band each e(I,h) is smooth and
even in h, so locally

    F_I(G)=[K_b-sum_j w_j*chi_j(I_j)]*G+O(G³),
    chi_j(I)=-e_j,hh(I,0).                                 (8)

The bracket is a computable state-dependent coefficient, not a declared
positive floor or an automatically cancelled contact. Taking the actions
to zero with a prepared deep-field family, taking the gap cutoff to zero,
and varying G at fixed actions are distinct operations. The universal held
quench coefficient uses its stated ordered limits; an instantaneous finite-age
response or a fixed-gap weak-field limit need not have that coefficient.

## 3. Keep phases and volume when the source is allowed to move

First restrict to the exact radial scalar reduction of the parent, or to
homogeneous fixed-polarization oscillations at h=0. An arbitrary rotating
vector source can have transverse/angular actions and transport connections;
one scalar I per mode is not a complete replacement for that problem.

For the scalar sectors, the leading slow averaged extra action can be written

    S_av,extra = C*integral sqrt(-g) {
        sum_j w_j[I_j*u^mu*partial_mu theta_j-e_j(I_j,h(a))]
        -DeltaU },                                        (9)

in addition to the SAME Einstein and ordinary-matter actions. In a spherical
reduction h(a) denotes the signed radial acceleration source. This notation
does not identify the oscillator phases theta_j with the preferred clock T.
The metric-dependent u and a, and their lapse/shift variations, remain in (9).

Why there is no silently omitted first-order scalar connection: locally choose
theta=0 at a turning point. For the time-reversal-invariant natural Hamiltonian
(1), y(theta) is even and p(theta) is odd. A derivative of y with respect to
the slowly varying source or proper-volume parameter at fixed theta is even.
Its averaged canonical connection <p*partial_parameter y> therefore vanishes
in this local convention. Periodic total derivatives can change the convention
but not the averaged physical momentum test in section 5. This argument does
not eliminate higher adiabatic corrections or vector-orientation connections.

Varying the retained phase and action gives, to the same averaging order,

    nabla_mu(I_j*u^mu)=0,
    u^mu*partial_mu theta_j=omega_j(I_j,h).                 (10)

These are transport/evolution equations, not permission to choose a different
I_j independently at every future field strength. If a nonadiabatic formation
or transfer event changes I, its work and state production must be supplied by
the actual unaveraged parent; (10) is not applied through that event.

In the spherical metric of the companion note, with all momenta defined after
removing the common angular factor 4pi, the canonical phase momentum is

    J_j=C*L*R²*w_j*I_j.

The averaged mode Hamiltonian and radial momentum contribution are

    H_mode,av=N*C*L*R²[sum_j w_j*e_j(J_j/(C L R² w_j),h(a))
                       +DeltaU]+beta*sum_j J_j*theta'_j,
    H_r,mode=sum_j J_j*theta'_j,
    J_dot_j=(beta*J_j)',
    theta_dot_j=beta*theta'_j+N*omega_j.                   (11)

In particular I is diluted by proper-volume expansion; J, not I, is constant
under beta=0 normal threading. Dropping the volume factors would give the
wrong cosmological pressure. The action-angle reduction is leading order in
slow parameter variation; it is not a declaration that the old instantaneous
metric canonical momenta are exactly unchanged at all orders.

The functional lapse derivative of (11) is also not its bracket alone.
It gives the averaged normal density

    rho_mode,av=C[sum_j w_j*e_j+DeltaU+a*B_bar*h'(a)
                    +(R²*B_bar*h'(a))'/(L*R²)].            (12)

Here h' in the product means dh/da; the outer prime is a radial derivative.
This agrees with the direct orbit average of the exact spherical density.
The derivative is at fixed canonical J, which is independent of lapse.
Metric spatial variations must likewise retain I=J/(C L R² w) and h(a).
At nonzero acceleration, I*omega-e alone is NOT the full anisotropic or
inhomogeneous gravitational stress.

## 4. Homogeneous pressure is determined by the same orbit energy

On aligned FLRW, a_mu=0 and h=0. With scale factor a_FRW, equation (10) becomes

    a_FRW³*I_j = constant,
    rho=C[sum_j w_j*e_j(I_j,0)+DeltaU],
    p=C[sum_j w_j*(I_j*omega_j-e_j)-DeltaU].               (13)

These follow by lapse and scale-factor variation of (9), or by averaging the
already independently varied parent stress. They are not assigned equations
of state. Indeed I*omega=2<T_osc> gives p_exc=<T_osc-V0>, and the continuity
equation follows directly from I_dot=-3H I.

For one quadratic-dominated mode, omega0=delta*sqrt(kappa/m),

    e(I,0)=omega0*I+[3u4/(8m²*omega0²)]*I²+O(I³).

Its leading energy redshifts as a_FRW^-3 and leading pressure vanishes; the
displayed positive correction determines the first nonzero pressure. In the
quartic-dominated limit

    e(I,0)={ pi*u4^(1/4)*I / [sqrt(m)*B(1/4,3/2)] }^(4/3),
    p_exc=e/3.                                             (14)

The mixed potential has 0<=<p_exc>/<rho_exc><=1/3 by the existing virial
identity. At a finite positive gap, dilution eventually reaches the quadratic
regime, provided the mode remains fast compared with expansion. No statement
that every gapless mode is fast is made.

More generally the intrinsic averaged mode work equation is

    u·partial(sum_j w_j e_j)
       +theta_exp*sum_j w_j*I_j*omega_j
       =-B_bar*u·partial h,                               (15)

where theta_exp=nabla_mu u^mu, not an oscillator phase. The source term is
the same force work as in (5). The complete inhomogeneous stress additionally
contains the acceleration variations in (12); it cannot be obtained by treating
h as a metric-independent thermodynamic knob.

A useful computed phase-pressure function is available locally wherever
e_II>0: eliminate I from Q_j=e_I and set

    P_j(Q_j,h)=I_j*Q_j-e_j(I_j,h),
    partial_Q P_j=I_j,
    partial_h P_j|Q=+b_j*<y_j>.                            (16)

This Legendre function is fixed by (1), not an arbitrary fitted function.
The exactly harmonic limit has e_II=0 and must retain I as a multiplier
enforcing Q=omega0; no regular inversion is asserted there. Where convexity
or branch uniqueness fails, retain (9) instead of imposing an unproved
Legendre closure. In the quartic limit P=27Q^4/(256 alpha³), with
e=alpha I^(4/3). Q_j=u·partial theta_j is NOT
sqrt(-partial T squared), so this does not derive a native khronon K(Q).

The convexity qualification is substantive even for this parent. Around the
tilted minimum y_star, let k_eff=kappa*delta²+3u4*y_star² and
omega_star=sqrt(k_eff/m). A small displacement of peak amplitude A_osc has

    (omega-omega_star)/omega_star
       =[3u4*(kappa*delta²-7u4*y_star²)/(8k_eff²)]*A_osc²
          +higher-amplitude terms,
    e_II(0,h)=3u4*(kappa*delta²-7u4*y_star²)/(4m*k_eff²).

The cubic term about the displaced minimum produces the negative contribution.
Thus the positive and strictly convex coordinate potential can have a
SOFTENING frequency at fixed h. One cannot infer a convex phase energy,
positive effective compressibility or fluid perturbation stability just from
positive mechanical inertia. At h=0 the displayed coefficient is positive;
the homogeneous pressure result (13)-(14) is unaffected.

## 5. The extra stationarity condition supplied by the momentum constraint

Take beta=0 and time-independent N,L,R,h,I. Then

    theta_j(t,r)=N(r)*omega_j(I_j(r),h(r))*t+theta_j0(r),
    partial_t H_r,mode
       =C*L*R²*sum_j w_j*I_j*partial_r(N*omega_j).          (17)

Thus a static mean geometry and ordinary-matter state with no compensating
radial momentum require BOTH its initial momentum constraint and

    sum_j w_j*I_j*partial_r(N*omega_j)=0.                  (18)

Spatially constant redshifted frequency N*omega_j for every occupied mode
is sufficient; it is stronger than the summed condition. Alternatively an
actual matter/geometry current could participate, but it has to be evolved
with its stress/work. A collection of separately clamped orbit means does
not supply either condition by itself. Choosing I(r) afterward to enforce a
desired rotation curve would not derive a prepared state.

This is not merely an angle-coordinate argument. For the original scalar
orbit at fixed N(r), write p_phys=m*y_dot/N, K=p_phys²/(2m), and V=U_delta.
The exact equation, followed by the held local orbit average, gives

    partial_t <p_phys*y'>
       =N*partial_r<K-V>+N*<V_h>*h_r+2N'*<K>
       =I*partial_r(N*omega).                             (19)

The second equality uses (3), <K-V>=I*omega-e and
e'=omega*I'+e_h*h_r. It directly confirms the physical secular momentum
source in (17). Smooth local phase averaging must have the same result.
Here the average is uniform over the orbit phase at FIXED coordinate time.
For local y-only observables it equals the held time mean, but the secular
p_phys*y' momentum itself need not possess a finite infinite-time Cesaro mean.

Equivalently define intrinsic E=sum w e and Pi=sum w(I*omega-e). Then

    Pi'+(E+Pi)*N'/N-B_bar*h_r
       =(1/N)*sum_j w_j*I_j*(N*omega_j)'.                  (20)

The stationary condition is a pressure, gravitational-weight and source-force
balance, not just a constitutive force curve. The full acceleration-dependent
stress still follows from (9) or (11). Randomizing initial phases can cancel
initial mean momentum; it does not by itself cancel the common secular term
on the right of (17).

## 6. Domain of the averaging and the smallest useful next calculation

For each retained scalar mode, require a bounded nonseparatrix orbit and a
window containing many periods while h, proper volume and the relevant
metric/clock parameters change only a small fraction on that window. A fixed
finite positive band supplies a lower small-amplitude frequency, but the
actual source-driving errors and H/omega must still be checked. At I=0,
angle coordinates are singular; a controlled moving-minimum calculation or
the unaveraged modes must bound the excitation rather than assigning a phase.

The normal acceleration itself is part of the coupled constraints. Even if a
Newtonian metric potential varies slowly, a prepared preferred clock can
oscillate at mode frequencies. FINITE_MODE_CONSTRAINED_RESPONSE.md gives
explicit examples. Slow external h in a laboratory-style hold is therefore
not proof of an adiabatic autonomous galaxy solution. The collective clock
charge, matter current and lapse/shift constraints must be retained and
checked before using (9)-(12). No claim of a uniform gapless averaging theorem,
new spatial propagation speed or complete nonlinear stability is made.

There is nevertheless a small informative calculation available from the
already saved scalar end-ramp states, without further time propagation:

1. Compute each positive orbit action from (2), retaining every preparation,
   mode, cutoff and quadrature weight already fixed in the saved census.
2. Recover the existing held mean through e_h at FIXED I, and verify (3)-(4)
   with independently controlled quadratures/inversions. Do not differentiate
   between separately prepared amplitudes.
3. Holding those same actions, solve the monotone relation I(e,0)=I_saved.
   This predicts the energy and pressure after a SPECIFIED adiabatic return to
   h=0, with the return work recorded. It is a conditional continuation of
   the actual state, not an assertion that the return occurred in the universe.
4. If an inhomogeneous averaged state is proposed, test (18) and the full
   constraints before attempting a stationary field solve.

This establishes a shared response/stress state map instead of independent
DM-like and DE-like knobs. It still needs the native source, absolute volume,
physical inertia and preparation/production matching described in
NATIVE_SOURCE_BRIDGE_DECISION.md. The saved native writer responses can be
active, so they must not be replaced by these passive scalar actions without
that matching. No new dark abundance, damping, independent vacuum constant
or per-radius age has been introduced.
