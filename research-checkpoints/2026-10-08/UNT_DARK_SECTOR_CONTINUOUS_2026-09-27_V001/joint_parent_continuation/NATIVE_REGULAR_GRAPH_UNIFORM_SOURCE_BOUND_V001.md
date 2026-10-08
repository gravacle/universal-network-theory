# Uniform bounds on native low band source weight

2026-09-30. Source-only continuation of the independently reviewed regular
graph energy-source selector. No numerical run, fourth-order remainder
extrapolation, eigensolver, parameter adoption or physical-volume assignment.
The earlier selector and sealed handoff files are unchanged.

## Decision

For the stated isolated degree-two family, the EXACT compressed energy source
has a norm bounded independently of N. Its total ground-to-low-band spectral
weight therefore stays bounded even when the number of soft modes grows.
Permutation symmetry sharpens this result: for the single-node anchored
profile already declared by the selector, the weight is at most O(1/N).
These bounds apply to the full finite Hamiltonian, not its fourth-order
switch approximation.

They constrain finite-time and positive-imaginary-frequency response, and bound the
complete ground-state work throughout a fixed positive-lapse window. They
do not alone bound static inverse-gap susceptibility: spectral weight can
concentrate at increasingly small gaps. The exact condition that such a
remaining static mechanism must meet is given below, with its preparation,
clock, source and physical-volume assumptions explicit.

## Family and isolated band

Use precisely the centered carrier-free, uniform fixed-record sector of
`NATIVE_REGULAR_GRAPH_ENERGY_SOURCE_SELECTOR_V001.md`, with k=2, N>=3,
U>0, Omega>0 fixed, and h=Omega/N. No formation or additional dynamical ports
are introduced. With k_v=d_v-k and K=sum_v k_v^2,

    H=C_N+U K+V,     V=-(Omega/N) sum_e X_e,
    h_v=c0+U k_v^2-(Omega/(2N)) S_v,
    S_v=sum_(e incident v) X_e,     sum_v h_v=H.           (1)

The complete uniform onsite constant c0 and C_N=2N c0 remain in the energy
and source ledger. Other spectator factors are either absent or fixed scalar
energies allocated uniformly; an unspecified source-dependent controller is
not included in this theorem. Nonuniform scalar allocations can be kept as
their explicit affine source baseline, but cannot be mistaken for transition
weight. Actual external source/support implementation and its work remain
additional physical obligations.

Define the existing constants

    beta_N=min(k,N-k),      b_N=1+2k(1-k/N),
    q_N=sqrt((beta_N+1)/N), a_N=U-Omega q_N,
    r_N=(Omega/U)[sqrt(b_N)+q_N] < 1.                    (2)

The strict condition r_N<1 is required; it implies a_N>0. The existing
uniform theorem proves that exactly rank(P) eigenvalues lie below C_N,
where P is the bare regular-graph subspace, and all other energies lie above
C_N+2U(1-r_N). Let Pi be the EXACT spectral projector onto this low band.
For fixed Omega sqrt(5)<U with a strict margin, (2) holds for all sufficiently
large N. It is not asserted for the inherited Omega=U=1. No coefficient is
changed with N to manufacture isolation.

The full incidence ground |0> is unique, strictly positive, permutation
invariant and layer-exchange even. Spectral transport of Pi preserves the
bare regular representation. These are the stationary ground assumptions;
they are not properties of the original finite-age formed preparation.

## Every low band vector has a uniform defect bound

The existing star inequality applies to every normalized vector, not just
an eigenvector. With kappa=<K>,

    |<V>| <= Omega sqrt(2 b_N kappa)+Omega q_N kappa.

Every normalized vector in Ran(Pi), including an arbitrary superposition,
has <H-C_N><0. Hence

    0 >= a_N kappa-Omega sqrt(2 b_N kappa),
    kappa <= Kmax_N := 2 Omega^2 b_N/a_N^2.              (3)

This use of the whole spectral subspace is essential for an operator-norm
bound. A bound on individual energy eigenstates alone would not suffice.

Choose any real centered dimensionless profile u_v, sum_v u_v=0,
|u_v|<=1, and define the energy-valued source

    T_u=sum_v u_v h_v.                                  (4)

The c0 term cancels because the profile is centered, not because absolute
energy has been discarded. Apply the same individual-star estimates before
summing their absolute values. Their weighted version gives

    |<T_u>| <= (U+Omega q_N) kappa
                       +Omega sqrt(2 b_N kappa).         (5)

The right-hand side increases with kappa>=0. At (3),
Omega sqrt(2 b_N Kmax_N)=a_N Kmax_N, so

    ||Pi T_u Pi|| <= L_N := 2U Kmax_N
                          =4U Omega^2 b_N/a_N^2.        (6)

For fixed coefficients in the stated domain, L_N=O(Omega^2/U), uniformly
in large N. The growing norm ||V||=Omega N never replaces the statewise
star estimate. No inverse spectral gap within Pi was used.

## Exact weight and symmetry improvement

Let Pi_ex=Pi-|0><0| and define the nonnegative ground-state low-band measure

    dmu_u(Delta)=sum_(n in low,n!=0)
           |<n|T_u|0>|^2 delta(Delta-E_n+E_0) dDelta,
    W_u=integral dmu_u=||Pi_ex T_u|0>||^2.               (7)

All gaps Delta are positive at finite N. Ground subtraction is explicit.
The ground mean of a centered T_u is zero by the node/layer symmetries, but
the definition does not silently use Pi in place of Pi_ex. From (6),

    W_u <= L_N^2.                                      (8)

There is a useful stronger shape dependence. The Gram matrix
M_vw=<0|h_v Pi_ex h_w|0> is invariant under independent within-layer
permutations and under layer exchange. Its single-layer standard blocks
are equal scalar matrices; mixed standard blocks vanish. The uniform source
is H and has no transitions. The selector's EXACT degree-two two-plane null
removes the other singlet. Consequently, for arbitrary real profiles,

    W_u=w_N Q_u,   w_N>=0,
    Q_u=sum_L(u_v-mean_L u)^2+sum_R(u_v-mean_R u)^2.      (9)

This is an exact selection rule for the present ground/band, not an ansatz
for graph geometry. It includes any degeneracies inside the band by using
the full projector; no eigenbasis choice enters.

For even N, choose N/2 entries +1 and N/2 entries -1 on EACH layer.
For odd N, choose (N-1)/2 of each sign and one zero on EACH layer. Each
layer is centered and bounded, and Q_u=2m_N with

    m_N=N (even N),    m_N=N-1 (odd N).

Applying (8) to this prospectively specified algebraic test profile gives

    w_N <= L_N^2/(2m_N).                                (10)

For the already specified anchored profile
u_L=(1-1/N,-1/N,...,-1/N), u_R=0, Q_u=1-1/N. Therefore

    W_anchor <= L_N^2(1-1/N)/(2m_N) <= L_N^2/(2N).       (11)

The first bound is slightly stronger at even N. A layer-constant profile
has Q_u=0 and hence exact W=0, rather than merely a small upper bound.

## Finite time and frequency versus the static limit

With the established PLUS-source convention H(theta)=H+theta T_u, the change
is delta<T_u>(t)=-integral chi_u(t-s) delta theta(s) ds for this response
contribution. The kernel below is not the oppositely signed functional
derivative delta<T_u>/delta theta. For t>=0 its retarded form (zero for t<0)
and its positive imaginary-frequency susceptibility are

    chi_u(t)=(2/hbar) integral sin(Delta t/hbar) dmu_u,
    chi_u(i zeta)=integral 2Delta/[Delta^2+(hbar zeta)^2] dmu_u,
    zeta>0.                                            (12)

They obey the exact bounds

    |chi_u(t)| <= 2 W_u/hbar,
    |integral_0^T chi_u(t) dt| <= 2 T W_u/hbar,
    0 <= chi_u(i zeta) <= W_u/(hbar zeta).              (13)

These bounds concern the retained low-band contribution only, not hidden
high-band contacts or the complete physical response. A fixed positive
imaginary-frequency argument zeta, or finite readout time, cannot evade the
weight suppression merely by packing more states into that band. No analogous
pointwise bound at an undamped real-frequency resonance is claimed.

In contrast,

    chi_u(0)=2 integral dmu_u/Delta                       (14)

has no uniform upper bound from (8)--(11) alone. A simple logical counterexample
is a family of abstract measures W_N delta(Delta-Delta_N) with W_N->0 but
Delta_N vanishing more rapidly. This is NOT an asserted BS spectrum; it shows
why a weight theorem is not an inverse-gap theorem. Taking infinite response
time before the large-N limit can change the conclusion. No static passivity
or relaxation claim follows for a nonstationary prepared state from (12).

## Complete finite lapse work is also bounded without a low band expansion

For the same fixed profile u, set ell_v=1+theta u_v and |theta|<=epsilon<1.
Use the complete source H(theta)=sum_v ell_v h_v, with the same microscopic
clock, coefficients, and affine source chart. Let

    a_N(epsilon)=U(1-epsilon)-Omega(1+epsilon)q_N >0,
    B_N(epsilon)=Omega^2(1+epsilon)^2 b_N/[2a_N(epsilon)].

The weighted diagonal cost is at least U(1-epsilon)K, and the flip estimate
is multiplied by at most (1+epsilon). Minimizing the resulting quadratic
in sqrt(kappa), while a regular computational graph remains a trial state,
proves for the EXACT full ground energy

    C_N-B_N(epsilon) <= E_0(theta) <= C_N.               (15)

For fixed epsilon and sufficiently large N, B_N=O(1); no low-band projection
or perturbative denominator enters. The ground energy is concave in theta,
and E_0'(0)=0 by symmetry. Thus

    0 <= E_0(0)-E_0(+/-theta) <= B_N(epsilon),
    E_0(0)-E_0(+/-theta)
       =integral_0^theta (theta-t) chi_full(+/-t;0) dt,  0<=theta<=epsilon,
    0 <= [2E_0(0)-E_0(theta)-E_0(-theta)]/theta^2
                                    <=2B_N(epsilon)/theta^2.       (16)

Here chi_full(theta;0)=-E_0''(theta)>=0 includes ALL excited states in this
affine zero-contact raw chart. It is not the low-band chi in (12). Positive
node lapses retain the finite connected stoquastic hypercube and unique ground,
so the displayed derivatives exist at every finite N. Equation (16) bounds
finite-source work and averaged curvature, not a pointwise static curvature
uniform in N. Eliminating high states in another description requires their
induced contacts, not deleting their contribution to this work.

## What physical normalization would have to satisfy

For an independently calibrated node profile x_v with centered origin, write
x_v=R_N u_v, |u_v|<=1. With physical acceleration alpha,

    theta=alpha R_N/c^2,      Z=(R_N/c^2)T_u,
    W_Z=(R_N^2/c^4)W_u.

The more precise identity is W_Z=w_N Q_x/c^4, where Q_x is the within-layer
centered squared-length sum. If a separate physical construction supplies a
volume V_N, then

    W_Z/V_N <= L_N^2 Q_x/(2m_N c^4 V_N),                (17)

also bounded by L_N^2 R_N^2/(c^4 V_N) from (8). No V_N proportional to N is
assumed by the theorem. The anchored profile of fixed calibrated length ell
instead has W_Z <= L_N^2 ell^2/(2N c^4).

For example, IF V_N is extensive and R_N remains bounded, low-band weight
and fixed-time/positive-imaginary-frequency response per volume vanish. IF a physical three-
dimensional family instead has R_N proportional to V_N^(1/3), the bound is
O(V_N^(-1/3)) at fixed microscopic zeta>0 or finite time. These are conditional
scaling consequences, not emergent dimensions. The positive-lapse window in
physical acceleration shrinks as |alpha|<=epsilon c^2/R_N when R_N grows;
one must not describe fixed theta as fixed physical acceleration.

A proposed nonzero limiting static susceptibility density would have to
overcome the suppressed weight through a correspondingly small weighted gap.
When the LOW-BAND W_Z and LOW-BAND chi_Z(0) are nonzero, define their
harmonic mean gap (not a quotient involving the full high-band response)

    Delta_H=2W_Z/chi_Z(0).

If this low-band chi_Z(0)/V_N >= chi_star>0 is independently required, the necessary condition is

    Delta_H <= 2L_N^2 R_N^2/(c^4 V_N chi_star),           (18)

or the sharper Q_x bound from (17). This is a necessary weighted spectral
condition, not a proof that the dynamics reaches its static state on a single
time hbar/Delta_H. Formation/readout times and the full two-time response
must be owned before exploiting this nonuniform limit.

Likewise (15)--(16) imply ground work per volume vanishes on a fixed theta
window if V_N grows. They do NOT rule out every nonanalytic response in a
shrinking physical-field window. For instance, a hypothetical total cubic
work proportional to V_N|alpha|^3 can remain O(1) when V_N is proportional
to R_N^3 and alpha is proportional to 1/R_N. This example diagnoses the limit
ordering; it neither derives nor inserts a cubic constitutive law.

Uniform source/clock rescaling, rescaling the anchored profile with N, or
choosing a new volume law to keep a plotted weight finite changes the physical
test. The same absolute energy, volume derivatives, source contacts and
coupled-pressure identity from the shared-work note must be retained. Nothing
here calibrates c(V), a gravity equation, dark abundance or a formation state.

## Exact next decision

This theorem already supersedes the need for an eigenvalue histogram as the
next large-N screen. A proposed stationary density-response mechanism in this
family must first specify the physical source geometry, clock, V_N and the
observation-time/source-field limit. If it claims a nonzero static response
FROM THIS LOW BAND, it must derive the inverse-gap weighted concentration
satisfying (18), with nonlinear response and state preparation, rather than
infer it from soft mode counts. If it claims a low-band finite-time response
outside (13),(17), it fails
the stated family without needing a larger numerical sweep.

The earlier small N=3,4,5 exact oracle remains a source-implementation check,
not a substitute for these conditions. No oracle code was created or run by
this note. No source parameter, bath, initial-age selection, or alteration of
the original prepared-state evidence is authorized.

## Sources read and not claimed as new

- `NATIVE_REGULAR_GRAPH_ENERGY_SOURCE_SELECTOR_V001.md`, SHA-256
  `daa31272997620537d7d0395d587d2fe954617d9796f52570f8018d6019adacb`:
  the centered family, complete energy partition, exact source representations
  and degree-two two-plane null. Its independent review is complete.
- `../NATIVE_UNIFORM_REGULAR_DEGREE_BOUND_V001.md`: statewise star bound,
  exact isolated band and finite-N conditions. Its ground-only estimate is
  extended here to arbitrary vectors in that band before bounding the source.
- `NATIVE_SHARED_WORK_INTEGRABILITY_V001.md`: complete conservative state
  branch, physical source normalization, contacts and force/pressure linkage.
- `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`: PLUS-source response sign,
  adopted lapse/position premise and original nonstationary-state ceiling.
