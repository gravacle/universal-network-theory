# A physical clock state, not a coordinate escape

2026-10-05 UTC / October 4 local. Analytical continuation of frontier V132.
Root and two independent internal analysts checked the PN variation below.
This is a conditional dynamical completion of the static filtered candidate;
it is not already a covariant native UNT derivation.

## The state that matters

With signature (-,+,+,+), c=1, Q=sqrt(-partial T squared),
u_mu=-partial_mu T/Q and P the orthogonal projector, the exact identity is

    A_mu = -P_mu^nu partial_nu ln Q.

Coordinates transform both metric and T and cannot change A_mu A^mu.
Relabeling T by a monotone function leaves u unchanged. A different foliation
is a physically different state. In the weak-field slow-motion limit write

    T=t+pi, v_T=-grad pi,
    Xi=Phi-pi_dot+|grad pi|²/2, A_i=partial_i Xi.

The local covariant antecedent and these conventions are described in
[Blanchet and Skordis, sections 2–3](https://arxiv.org/html/2404.06584v2).
The filter and the following conditional completion are separate assumptions.

For Phi_e=g_e.x the exact PN choice
`pi=t g_e.x+|g_e|²t³/6` has Xi_e=0 and v_T=-t g_e. This is a freely falling
clock, not removal of physical acceleration by a coordinate label. A moving
satellite can in principle retain its internal Xi while its clock falls
with the center. Neither this construction nor its name selects or globally
matches that state to the Galactic and Solar clock.

## Minimal fixed-filter dynamics has an exact obstruction to formation

Let S=(1-ell² Delta)^(-1) be the fixed self-adjoint spatial filter, b=S grad Xi,
and let W(b) denote the relaxed energy divided by 4piG, including the fixed
endpoint, with grad_b W=-F(b)/(4piG). Adopt the explicit PN action

    L=integral [-|grad Phi|²/(8piG)-rho_b Phi-W(b)] d³x.

In this formula S, its spatial measure and its boundary domain do not vary
with pi. A fully clock-dependent covariant filter could change the result
and has not been supplied by writing this PN action. Source variation gives

    rho_T=div[S F(b)]/(4piG),
    Delta Phi=4piG(rho_b+rho_T).

Here rho_T is a response contribution to the constraint, not a population
of record particles. The clock variation is especially useful:

    delta L_int=-integral rho_T delta Xi,
    delta Xi=-delta pi_dot+grad pi.grad(delta pi),
    rho_T_dot+div(rho_T v_T)=0.

Along every smooth characteristic,

    rho_T(t,X(t))=rho_T(0,X(0))
                     exp[-integral div(v_T)(s,X(s)) ds].

Thus exactly zero initial response remains zero, without inflow. This holds
at nonlinear PN order for the stated completion, not merely at linear order.
Moving baryons alone cannot create a new response charge under this law.
The static MOND-like branch may exist, but its charge must be prepared or
transported into the domain. Adding independently selected initial charge
per galaxy does not explain its selection from ordinary sources.

The saved K=0 FLRW result, Delta(Upsilon_dot+H Upsilon)=0, is consistent
with this restriction for nonzero modes. A uniform external acceleration is
harmonic boundary data; zero charge alone does not fix it. Neither setting
rho_T=0 nor the local continuity equation proves that every harmonic field
vanishes. Boundary effects must not be confused with new volume charge.

## Caustics are a missing dynamical regime, not a demonstrated repair

Exactly A=0 implies Q=Q(T). A relabeling then gives proper time tau obeying
partial tau squared=-1: the clock congruence is geodesic and must remain
single-valued. In a Newtonian potential its flow Jacobian satisfies

    J_ddot=-(Hessian Phi) J, det J != 0.

For a central harmonic attractive well Phi=omega²R²/2 and initially resting
clock paths, J=cos(omega t) I, so the first focus is t=pi/(2omega). For the
center of a Newtonian Plummer source omega²=GM/a³. This illustrative local
calculation is not a full time-dependent galaxy or Galactic tidal history.

Uniform external acceleration alone does not focus paths; tidal curvature
does. At a caustic the smooth characteristic argument loses its premise.
It does NOT follow that charge has been created, that the preferred normal
has a unique continuation, or that the desired stationary force results.
An explicit regularization and conserved work/current are required.

If A=0 is chosen globally, F(0)=0, so this acceleration response supplies no
galaxy modification beyond its constant endpoint. Selective freely falling
patches cannot simply be declared independently for inconvenient systems.

## Next minimal premise to test

A term quadratic in the expansion K=div u has zero value AND first variation
on an aligned static K=0 background but supplies a nontrivial clock equation
in time-dependent states. Test a constant coefficient beta in the ADM action

    (M²/2) integral N sqrt(gamma)
           [R3+Kij Kij-(1+beta)K²-2J(A²)], M²=1/(8piG).

This is one new dimensionless coefficient and an actual new operator;
it is not implied by existing graph rules. The filtered static response is
retained only with its separately declared extension. Check its full scalar
constraints, background lapse equation, high-frequency propagation and
current before any numerical formation run. In particular, its stationary
invisibility does not make it invisible in cosmology. The earlier
TRACE_CLOCK_CLOSURE_AUDIT remains valid; a positive constant regulator is
not an arbitrary replacement for the already failed imposed expansion law.

The compact-dwarf result remains a warning for its declared external-field
state. This derivation neither removes that result nor supplies a fitted
alternative. It identifies exactly which state-selection physics is missing.
