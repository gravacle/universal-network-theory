# Retaining the same response modes supplies a cosmological equation

2026-09-28. New conditional covariant completion of the existing classical
mechanical parent. No numerical worker, new fit, change to the frozen static
candidate, or claim of an already derived native BS continuum.

## Result

The positive-inertia coordinates previously used to derive the static force
can be kept as explicit degrees of freedom in a definite covariant action.
Static elimination gives **exactly the existing matched J(Y)**. On an aligned
homogeneous background their excitations instead obey a calculable oscillator
equation with expansion friction. Rapid quadratic oscillations carry
matter-like energy, and rapid quartic oscillations carry radiation-like
energy. Neither conclusion requires appending an arbitrary clock function
K(Q) or a phenomenological fluid to the equations.

This is an existence and equation-of-motion result for a specified completion.
Its mode inertias, actual excitation and production history still need the
native matching. In particular, perfectly homogeneous initially unexcited
classical modes remain unexcited: the static galaxy calibration does not
predict a cosmological matter-like abundance.

## 1. Complete parent and one explicit covariant completion

Use c=1, signature (-+++), M²=1/(8 pi G), and the preferred normal

    u_mu=-partial_mu T/sqrt(-partial T squared),
    P_mu_nu=g_mu_nu+u_mu*u_nu,
    a_mu=u^nu nabla_nu u_mu,   Y=a_mu*a^mu.

The preferred-foliation interface and a_i=D_i ln N are imported explicitly
from [Blanchet and Marsat, section II and equations (3.2)-(3.4)](https://arxiv.org/pdf/1107.5264). The oscillator completion below is our
conditional construction, not a result attributed to that paper.

Keep the previous bounded source and its SAME potential parameters:

    h_mu(a)=a_mu/sqrt(1+Y/g_s²),
    V0_delta(y)=kappa*delta²*y²/2+u4*(y²)²/4,
    nu(delta)=A*delta on (0,Lambda),
    K_b=kappa*integral nu ddelta,
    C=2M²/K_b=1/(4 pi G K_b).

Here u4>0 denotes the earlier quartic coefficient u, not the unit vector.
A finite band or finite positive weighted sum can replace this integral.
Give each coordinate y_delta^mu the constraint u_mu y_delta^mu=0 and define

    v_delta^mu=P^mu_nu*u^alpha*nabla_alpha y_delta^nu,
    m(delta)>0.

The proposed action is

    S = integral sqrt(-g) [ M² R/2
          + C { integral nu [m*v²/2 - V0_delta(y)
                              + kappa*delta*h_mu*y^mu] ddelta
                  - DeltaU } ] + S_ordinary.                    (1)

The constraint can be enforced with a multiplier, or the spatial y variables
can be used directly in preferred coordinates. All variations below retain
it. Positive m fixes the same per-mode kinetic convention as
FINITE_TIME_SOFT_RESPONSE_PATHWAY.md; it is not a value fitted to cosmology.
The measure and coefficients in (1) are spacetime-independent scalars in
the action, not a separately conserved material number density. Making
them functions of density or strain would change (1) and its pressure.

No arbitrary new vacuum term is supplied. DeltaU is the ALREADY declared
high-acceleration matching value from SAME_PARENT_FORCE_VOLUME_LINK.md:

    DeltaU=K_b*g_s²/2-W_el(g_s)=integral_0^g_s P(s) ds > 0,
    P(s)=K_b*s-W_el'(s).

Its microscopic absolute-volume justification is not improved merely by
writing (1). A further constant would still alter cosmology while leaving
the force unchanged; no such constant is introduced here.

### Exact static identity, including the contact

For prescribed g=|a|, the complete earlier mechanical energy is

    E_complete=K_b*g²/2
           +integral nu [m*v²/2+V0_delta(y)-kappa*delta*h.y].

At a stationary aligned configuration, projected normal velocities vanish.
Minimizing the bracket gives

    U(g)=W_b(g)-K_b*g²/2=W_el(h)-K_b*h²/2,
    L_extra,static=-C[U(g)+DeltaU]=-M² J(Y),
    J(Y)=2[U(sqrt(Y))+DeltaU]/K_b.                           (2)

Thus J_Y=mu-1 and J(infinity)=0 are unchanged. The bare K_b*g²/2 is
already supplied by the weak-field Einstein sector in this matching; adding
it again to L_extra would double-count the contact. The full weak-field
mechanical energy, not the interaction bracket alone, is nonnegative.

Static metric/clock variations also agree with the existing J action:
the y equations remove its implicit variation (the envelope identity), and
variation of m*v² vanishes at v=0. This does not license using the static
J stress for time-dependent excited modes; their additional terms must be
varied from (1).

## 2. The mode and work equations before a fluid interpretation

At fixed metric and clock, constrained y variation gives

    m[P nabla_u v + theta*v] + kappa*delta²*y
                         +u4*y²*y = kappa*delta*h,
    theta=nabla_mu u^mu.                                      (3)

For the local per-mode energy e0=m*v²/2+V0_delta, contraction with v yields

    nabla_u e0 + theta*m*v² = kappa*delta*h.v.                  (4)

The right side is actual source work. Including interaction energy gives

    nabla_u(e0-kappa*delta*h.y)+theta*m*v²
                          =-kappa*delta*(P nabla_u h).y.        (5)

These are mode-energy identities, not a replacement for the full covariant
stress tensor in an inhomogeneous geometry. The metric, clock and modes
exchange energy through the same action. In a locally clamped nonexpanding
source experiment, including the bare contact recovers precisely

    dE_complete/dt = [K_b*g_vector-(D_g h)^T B].g_dot,
    B=integral nu*kappa*delta*y ddelta.                         (6)

Thus retained excitations do not create energy for free. Formation, forcing,
switching and any reservoir must supply their actual energy once.

## 3. Derive the homogeneous stress rather than assign w

Take ds²=-N(t)²dt²+a(t)² dx² and T=t. Homogeneous fields have a_mu=0.
For physical spatial components q_delta^i=a*y_delta^i,

    v²=|q_dot|²/N²,
    S_modes= C integral dt N*a³
         { integral nu [m*|q_dot|²/(2N²)-V0_delta(q)] -DeltaU }.
                                                                  (7)

The connection term in nabla_u y is essential: it cancels the derivative
of 1/a in y=q/a. Dropping it would give a different cosmological model.

There are three checks on using (7) for stress, rather than only for mode
motion:

* Lapse variation is taken before N=1. The acceleration coupling has first
  lapse variation proportional to the spatial divergence of B, which is
  zero for the homogeneous fields with the stated homogeneous/periodic
  boundary conditions. It is not discarded just because its value is zero.
* In diagonal Bianchi I, q_i=a_i*y^i reduces the projected derivative to
  q_dot_i/N. Varying a_i at fixed original y differs from varying it at
  fixed q only by the q equations of motion and endpoint terms. On shell
  each diagonal pressure is therefore the same reduced Lagrangian.
  Symmetric shape variations around FLRW give the same cancellation.
* The shift enters this homogeneous normal-derivative action through spatial
  derivatives/rotations; its momentum equation has no homogeneous source.
  The acceleration coupling likewise has no homogeneous shift source.
  Spatially homogeneous clock variations preserve its normal; arbitrary
  first clock variations reduce to homogeneous spatial divergences. These
  observations do not eliminate the clock constraint in an inhomogeneous
  perturbation problem.

Consequently, on this homogeneous on-shell branch define

    T_osc=integral nu*m*|q_dot|²/2,
    V2=integral nu*kappa*delta²*|q|²/2,
    V4=integral nu*u4*|q|^4/4.

The metric variations give

    rho = C[DeltaU+T_osc+V2+V4],
    p   = C[-DeltaU+T_osc-V2-V4].                            (8)

An isotropic mode ensemble is sufficient for a homogeneous FLRW state.
The convective-only action also has the displayed on-shell isotropic
homogeneous spatial stress; this is not a claim that its general vector
perturbations lack anisotropic stress. No Maxwell-type spatial kinetic term
or hidden elastic gradient has been substituted for (1).

In proper time the actual background equations are

    m(q_ddot+3H*q_dot)+kappa*delta²*q+u4*|q|²*q=0,
    3M²(H²+k/a²)=rho_ordinary+rho,
    -2M²(H_dot-k/a²)=rho_ordinary+p_ordinary+2C*T_osc,
    rho_dot+3H(rho+p)=0.                                    (9)

The matched constant remains rho_vac=C*DeltaU=M²J(0), with p_vac=-rho_vac.
These equations now determine evolution once actual mode initial data and
inertias are supplied. They are not inferred by naming an occupation a fluid.

## 4. What fast oscillations actually contribute

Average on an interval long compared with the occupied mode periods and
short compared with H^-1 and coefficient variation. Bounded oscillations
obey, to that adiabatic accuracy, the virial identity obtained directly by
averaging d(m*q.q_dot)/dt:

    2<T_osc>=2<V2>+4<V4>.

Therefore the EXCITATION stress is

    <rho_exc>=C[2<V2>+3<V4>],
    <p_exc>=C<V4>,
    w_exc=<V4>/[2<V2>+3<V4>] in [0,1/3].                    (10)

This includes vector motion/angular momentum when the bounded-motion virial
average exists. It is not an assumed equation of state.

For a quadratic-dominated mode, omega_delta=sqrt(kappa/m)*delta is constant,
|q| scales as a^-3/2 and its averaged energy as a^-3. For a quartic-dominated
mode, its typical amplitude scales as a^-1 and energy as a^-4. The positive
quadratic term eventually dominates a diluting finite-delta oscillator.
Mixed regimes obey (9), not an imposed interpolation in a. Modes with
omega comparable to H cannot be assigned (10) without solving their motion.
A zero-cutoff spectrum contains such modes for constant m, so the entire
continuum is not automatically cold matter.

The acceleration equation makes the separation transparent:

    rho+3p=C[-2DeltaU+4T_osc-2V2-2V4].

Its rapidly oscillating excitation average is
C[2<V2>+6<V4>] >= 0. These excitations do not replace the negative-pressure
matched part; they can coexist with it in the SAME action. Slow displaced
modes can temporarily have negative pressure, but that is an initial-value
solution of (9), not another vacuum normalization derived from the force.

## 5. What has and has not become a prediction

The static law fixes neither m(delta) nor q_delta,q_dot_delta. Equation (3)
in exactly homogeneous FLRW has no force on an initially zero coordinate.
Uniqueness gives q=q_dot=0 forever from those classical initial data.
Expansion friction redshifts existing excitation; it is not a production
mechanism or a thermal bath. Quantum production would require a quantized
state calculation and is not contained in this classical result.

This action retains invariance under monotone relabeling of T because it
uses only normalized u. It does not insert a homogeneous function of
Q=sqrt(-partial T squared) or its freely normalized conserved clock current.
The distinction from the additional K(Q) used in
[Blanchet and Skordis, sections 2 and 4](https://arxiv.org/html/2404.06584v2)
is substantive: matter-like energy here
resides in explicit oscillator states and has the work ledger (4)-(6).
Its abundance remains an actual-state datum, not a new integration constant
silently calibrated to a desired matter fraction.

Likewise the static force, clock-degeneracy and lensing conclusions of the
old K=0 action describe the eliminated stationary branch. Excited modes
generally modify the time-dependent stress and source susceptibility.
The full metric/clock/vector perturbations of (1) must be solved before
claiming clustering, sound speed, lensing of excitations or an acoustic
spectrum. Positive mode inertia alone does not prove absence of a coupled
constraint instability or establish a causal continuum limit. No spatial
mode-gradient operator was specified, and one must not supply its propagation
speed by analogy with an ordinary scalar field.

## 6. A narrow native matching target

This result replaces an arbitrary cosmological function with four measurable
requirements for the SAME prospective native physical source:

1. Its complete contact, quartic energy and source-weighted soft spectrum
   must match the mechanical channel, including the actual prepared state.
2. Its retarded pole frequencies and source residues must fix m(delta).
   NATIVE_SOURCE_BRIDGE_DECISION.md already provides the exact native
   first-moment constraint; for an owned constant-m identification it is
   A*kappa²*Lambda^4/(4m)=gamma²*h_N*sum(v_e²<X_e>)/hbar².
   It must pass with the actual sign and normalization, not a passive
   substitute for an active state.
3. Its preparation/work must determine oscillator energy and population
   per proper volume. Already counted carrier/rest energy cannot be counted
   again as additional excitation. The classical zero-state test above
   is a decisive check against claiming autonomous homogeneous production.
4. Its volume/clock matching must justify (1)'s measure, time and inherited
   DeltaU. Those are different derivatives from normalized fixed-geometry
   state evolution.

There is also a direct compatibility check with the declared static
response window. In the same clamped mechanical channel the earlier convex
energy certificate gives |F_actual-F_relaxed|²<=2K_b*E_exc. Cosmological
excitation cannot simply be declared invisible to the galactic response;
its actual source-weighted phases, population and work must be used. This
sufficient worst-case bound is not a claim that incoherent modes saturate it.

The constructive advance is an explicit common action and evolution law:
the same modes can carry a calculable matter-like excitation contribution
while their relaxed energy supplies the existing force and matched vacuum
part. The next identification is the native inertia and actual production
of these modes, not the invention of a free w(a) or another force fit.
