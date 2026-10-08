# Energy source bounds at the first degree tie

2026-09-30. Exact source-only analysis of the projected matching family.
No numerical run, parameter scan, new interaction, source adoption or change
to the reviewed strict-regular bounds or sealed handoff files.

## Decision

The first degree tie does create the already derived first-order collective
ladder, instead of the fourth-order switch channel. However, inside its exact
projected matching model the complete node-energy source still has bounded
total ground-state transition weight. A single-node anchored source has
weight at most Omega^2/(4N). The larger collective bandwidth alone therefore
does not establish a stronger finite-time gravitational response.

This is an exact statement about PHP and its consistently projected source.
It is not a uniform approximation theorem for the full parent. A possible
static mechanism still depends on the source-weighted gaps, and a physical
claim still requires the same state, clock, position, volume and absolute
work assignments as the preceding source notes.

## Native boundary and complete local energies

Use the carrier-free, uniform held-record sector of
`NATIVE_DEGREE_SWITCH_CHANNEL_V001.md`, with N vertices in each layer,
N>=2, U>0, Omega>0 fixed and h=Omega/N. Copying and other ports are off.
Write a=Delta-2 lambda_R q, with uniform record occupation q=0 or1. The
first boundary is the exact conditional coefficient relation

    kappa=a+2U(1-2d_*)=0,    d_*=1/2+a/(4U).

It is not the inherited positive-cost branch and is not a density threshold
selected by a derived formation law. At this relation the existing local
energy partition becomes

    h_v=c0+U d_v(d_v-1)-(h/2) S_v,
    S_v=sum_(e incident v) X_e,
    c0=U d_*^2+epsilon_r q,
    H=C_N+2U C_inc-h sum_e X_e,
    C_N=2N c0,    C_inc=(1/2) sum_v d_v(d_v-1).          (1)

Fixed scalar spectators can be included if allocated uniformly and retained
in c0. No unspecified controller or source-dependent spectator is covered.
The absolute constant is retained; its cancellation from a centered source
below does not determine its physical volume dependence.

Let P project onto ALL matchings, including the empty graph and every edge
count m=0,...,N. On P all d_v are0 or1. Set

    S_i^L=sum_j P X_ij P,    S_j^R=sum_i P X_ij P,
    S=sum_i S_i^L=sum_j S_j^R,
    H_P=P H P=C_N P-h S.                                (2)

For normalized uniform m-matching states the existing exact invariant
singlet block has

    <m+1|H_P|m>=-Omega(1-m/N)sqrt(m+1).                 (3)

Every matching connects to the empty graph by deletions. Thus the projected
flip graph is connected and H_P has a unique strictly positive ground |0>,
invariant under independent permutations of both layers and under layer
exchange. This is a stationary ground representation, not the original
blank preparation evolved to a selected age. A node-dependent source reaches
nontrivial within-layer representations; the radial block (3) alone does not
give its excitation gaps or weights.

## Source ownership and an exact star norm

Retain the previous adopted affine node-lapse chart, with a real centered
dimensionless profile u, sum_v u_v=0:

    H_P(theta)=P sum_v(1+theta u_v) h_v P,
    T_u=partial_theta H_P
       =-(h/2) sum_ij (u_i^L+u_j^R) P X_ij P.           (4)

The derivative uses the same fixed P and complete local energies as (2).
It is not obtained from an independently fitted spectral coefficient.
The raw second contact is zero in this explicitly affine projected chart.
An effective description obtained by eliminating full-parent states instead
must retain the induced source dressing, connection and contact terms.

Fix all edges not incident to left vertex i. The allowed matching states in
that fixed exterior are either i empty, or i joined to one of r free right
vertices. Therefore S_i^L on this block is the adjacency of a star with r
leaves, whose nonzero eigenvalues are +/-sqrt(r), with 0<=r<=N. The empty
exterior attains r=N, so, exactly,

    ||S_i^L||=||S_j^R||=sqrt(N),
    ||S||<=N sqrt(N),    ||H_P-C_N P||<=Omega sqrt(N).   (5)

This proof covers every matching, not a sample or only the radial block.
The last bound is not an assertion of an exact bandwidth asymptotic.

## Ground subtraction sharpens the anchored weight

For the already declared anchored profile
u_L=(1-1/N,-1/N,...,-1/N), u_R=0,

    T_anchor=-(h/2)(S_1^L-S/N).                        (6)

The generic operator-norm bound from (5) is Omega/sqrt(N). A ground-state
spectral weight is smaller because S|0>=s0|0>. With P_ex=P-|0><0|,

    P_ex T_anchor|0>=-(h/2) P_ex S_1^L|0>,
    W_anchor=||P_ex T_anchor|0>||^2
            =(h^2/4) Var_0(S_1^L)
            <=h^2 N/4=Omega^2/(4N).                   (7)

Layer permutation symmetry also gives <S_1^L>=s0/N and hence the zero
mean of (6). Ground subtraction is explicit; a scalar piece of S cannot
be counted as a transition.

For general real profiles the positive Gram form
<0|(P h_v P) P_ex (P h_w P)|0> is invariant under S_N x S_N and layer
exchange. The two standard-representation blocks have equal coefficients
and no mixed block. The uniform source H_P has no transitions; the other
layer-constant source is identically zero because
P(sum_L h_v-sum_R h_v)P=0. Both singlets are therefore absent. It follows
without diagonalizing H_P that

    W_u=||P_ex T_u|0>||^2=w_N Q_u,    w_N>=0,
    Q_u=sum_L(u_v-mean_L u)^2+sum_R(u_v-mean_R u)^2,
    w_N<=Omega^2/[4(N-1)].                             (8)

Here (7) and Q_anchor=(N-1)/N give the last inequality. For |u_v|<=1,
Q_u<=2N, including odd N, and consequently

    W_u<=Omega^2 N/[2(N-1)].                           (9)

These are exact projected-model sum rules. A two-plane profile has W=0,
not merely the upper bound (9). No finite-N spectrum or fourth-order
expansion was used.

## What the weight does and does not constrain

Let dmu_u be the positive ground-to-excited spectral measure for T_u within
the entire projected model, with gaps Delta=E_n-E_0>0. Its integral is W_u.
For the PLUS source H_P+theta T_u use the same response sign as the preceding
bridge: delta<T_u>=-chi_u*delta theta. The causal kernel is zero for t<0.
For t>=0 and positive imaginary-frequency argument zeta,

    chi_u(t)=(2/hbar) integral sin(Delta t/hbar) dmu_u,
    |chi_u(t)|<=2W_u/hbar,
    chi_u(i zeta)=integral 2Delta/[Delta^2+(hbar zeta)^2] dmu_u
                 <=W_u/(hbar zeta).                   (10)

The time-integrated absolute bound over a fixed window T is 2T W_u/hbar.
There is no corresponding pointwise bound at an undamped real-frequency
resonance, and chi_u(0)=2 integral dmu_u/Delta still requires the actual
weighted gaps. Ground passivity and this positive measure must not be
transferred to a nonstationary formed state without a separate derivation.

For independently calibrated positions x_v=R_N u_v and acceleration alpha,
theta=alpha R_N/c^2 and Z=sum_v x_v h_v/c^2. Thus

    W_Z=w_N Q_x/c^4,
    W_Z/V_N<=Omega^2 Q_x/[4(N-1)c^4 V_N],
    W_Z<=Omega^2 ell^2/(4N c^4) for a fixed-length ell anchor.       (11)

Here V_N exists only if separately supplied by the physical construction.
No identification of record count or N with volume is made. For a bounded
profile (11) is at most Omega^2 N R_N^2/[2(N-1)c^4 V_N]. Fixed physical
acceleration and fixed dimensionless theta are different as R_N changes.
The pressure and identity-source freedom remain subject to the common
energy and volume-work test, not fixed by these transition bounds.

## Why this does not yet bound the full parent source

The matching space is not invariant under H: forbidden additions create
degree-two vertices. The bare gap outside P is2U, but the projected band
has a growing norm bound (5). The strict-regular isolation theorem cannot
simply be continued through kappa=0, nor can a bare gap substitute for a
bound on the interacting eliminated resolvent. Even a controlled effective
Hamiltonian must be matched with the same dressed source and contacts.

A coarse exact full-parent estimate illustrates the changed scaling. For
every integer d>=0, d<=1+d(d-1)/2, so the edge count M obeys
M<=N+C_inc/2. Combining this with the existing flip expectation bound
|<h sum X>|<=2Omega sqrt(<M>), for c_inc=<C_inc>, gives

    <H-C_N>>=2U c_inc-2Omega sqrt(N+c_inc/2)
           >=[2U-Omega/(2sqrt(N))]c_inc-2Omega sqrt(N). (12)

The empty graph is a trial state of energy C_N. If
2U>Omega/(2sqrt(N)), the full ground therefore has

    <C_inc>_0<=2Omega sqrt(N)/[2U-Omega/(2sqrt(N))].      (13)

This O(sqrt(N)) upper bound is not a projection-leakage certificate and
does not import (7)--(11) into the full parent. It is consistent with why
the previous strict-phase O(1) defect argument needs a new proof here.

## Consequence for the next decision

The first-order radial channel is not, by itself, an escape from bounded
source weight. Before treating the tie as a candidate physical soft window,
the next substantive issue is a same-source full-parent projection/control
bound, or a source-weighted inverse-gap result in the projected standard
sectors explicitly kept conditional on that missing control. Another radial
eigenvalue histogram would not answer either question. No new run is proposed
by this note, and no stationary formation, physical degree tuning, absolute
pressure or cross-domain normalization has been supplied.

Source ancestry: `recovered_sources/BS_MICRO_ACTION.md` in the enclosing
program; `NATIVE_DEGREE_SWITCH_CHANNEL_V001.md`, especially section6;
`NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md`;
`NATIVE_REGULAR_GRAPH_UNIFORM_SOURCE_BOUND_V001.md`;
`NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`; and
`NATIVE_SHARED_WORK_INTEGRABILITY_V001.md`. The new results here are the
projected star-source bound (7), its complete profile consequence (8)--(9),
and the stated separation from full-parent control.
