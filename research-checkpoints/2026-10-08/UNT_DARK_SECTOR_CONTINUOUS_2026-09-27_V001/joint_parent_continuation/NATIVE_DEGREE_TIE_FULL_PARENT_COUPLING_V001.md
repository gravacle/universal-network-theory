# Coupling beyond the matching projection at the first degree tie

2026-09-30. Source-only continuation of the reviewed projected source and
static bounds. No numerical calculation, change of coefficients with N,
new term, parameter adoption or alteration of previous evidence.

## New result and remaining control problem

The coupling from the complete matching space into the excluded parent space
has an exact norm bounded by 2Omega/sqrt(3), independent of N. The anchored
energy source connecting those spaces is smaller, O(Omega/sqrt(N)). These
are full-parent off-block statements, not bounds on a truncated fourth-order
Hamiltonian. Exact endpoint-slide counting proves them below.

They do not alone transfer the projected static theorem to the full parent.
Even an additional uniform eliminated-resolvent gap would give an O(1)
self-energy norm bound, too coarse to preserve the currently proved
O(N^(-1/2)) source-gap lower bound by norm perturbation alone. An exact bare
second-order sector cancellation identifies a sharper possible route, but
does not supply its uniform higher-order remainder. The missing statement is
now a source- and representation-resolved control theorem, not merely a
small individual edge flip or a bare 2U gap.

## Family and illegal additions

Use precisely the first-tie held uniform-record, blank-carrier parent of
`NATIVE_DEGREE_TIE_PROJECTED_SOURCE_BOUND_V001.md`, N>=2:

    H=H0+V,  H0=C_N+2U C_inc,  V=-h sum_e X_e,
    C_inc=(1/2)sum_v d_v(d_v-1),  h=Omega/N,
    U>0, Omega>0 fixed, kappa=0.                        (1)

P contains all matchings, P_m those of size m, and Q=1-P. The complete local
energy and centered affine lapse source remain unchanged. Copying, formation
and other ports are off. Choosing this coefficient boundary and a stationary
ground still has not been derived from physical density or native formation.

Deleting an edge from a matching stays in P. Its only Q transitions are
illegal additions, of two types:

* An edge joins a matched vertex to an unmatched vertex. There are
  2m(N-m) choices. The new graph has one degree-two vertex, bare cost2U,
  and exactly two matching parents: deleting either edge of its length-two
  path restores a matching.
* An edge joins two matched vertices but is not already present. There are
  m(m-1) choices. The new graph has two degree-two vertices, bare cost4U,
  and exactly one matching parent: only deleting the central edge of its
  length-three path removes both violations.

Other connected components are untouched matching edges. Distinct m lead
to Q graphs with distinct total edge count m+1, so their coupling images are
orthogonal. No other Q topology can be reached in a single flip from P.

## Exact norm of the full off block

Let A_move be the adjacency on m-matchings that moves one endpoint of one
occupied edge to an unmatched vertex. There are 2m(N-m) such neighbors per
graph. Each off-diagonal Gram entry comes from exactly one shared length-two
path; length-three outputs contribute only to the diagonal. Consequently,

    (QVP_m)^dagger(QVP_m)=h^2[r_m I+A_move],
    r_m=2m(N-m)+m(m-1).

The Gram matrix is nonnegative, symmetric and has constant row sum. Its
largest eigenvalue is that row sum, regardless of connectivity of A_move:

    ||QVP_m||^2=h^2 m(4N-3m-1),
    ||QVP||=B_N:=h max_(0<=m<=N) sqrt[m(4N-3m-1)]
       <=h(4N-1)/sqrt(12)<2Omega/sqrt(3).               (2)

The maximum in the definition is over integers. The upper bound simply
maximizes the concave quadratic over real m; it is not a fitted estimate.
For m=0 the coupling is zero, and for m=N the move adjacency is zero but
the diagonal m(m-1) remains. These endpoints are included.

## Same-source off-block suppression

Let S_i be the full flip star at a fixed left vertex i, and S=sum_e X_e.
The complete centered anchor source is

    T_anchor=U[d_i(d_i-1)-(1/N)sum_L d_v(d_v-1)]
                       -(h/2)(S_i-S/N).               (3)

Its diagonal degree terms have no Q-to-P matrix element. In the incidence
matrix Q S_i P, each matching has at most N-1 illegal row-i additions, and
each resulting Q graph has at most two matching parents reached through
that same star. The maximum row/column-sum norm inequality gives

    ||Q S_i P||<=sqrt[2(N-1)],
    ||Q T_anchor P||
      <=(h/2){sqrt[2(N-1)]+B_N/(hN)}
      <=Omega/(2N){sqrt[2(N-1)]+(4N-1)/(N sqrt(12))}.    (4)

This is O(Omega/sqrt(N)). For any centered |u_v|<=1, the magnitude of each
off-block edge-source coefficient is at most its coefficient in V, so the
nonnegative matrix comparison also gives ||Q T_u P||<=B_N. Neither claim
bounds T_u acting on a fully dressed Q component of the ground.

An exact source distinction is especially important. The two-plane source
with u_L=+1,u_R=-1 is zero on P, but in the full parent it is

    T_plane=U[sum_L d_v(d_v-1)-sum_R d_v(d_v-1)].        (5)

The flip halves and uniform constants cancel. Equation (5) annihilates P
and has QT_planeP=0, yet is generally nonzero within Q. Thus its full
response is not proved zero by the projected two-plane selection rule.
Dressing through Q can activate this source; whether it does so with useful
weight or static response remains a separate calculation/control problem.

## What the exact resolvent formula still requires

At an energy E below the spectrum of QHQ, write

    R_Q(E)=(E-QHQ)^(-1),
    H_eff(E)=PHP+Sigma(E),
    Sigma(E)=PHQ R_Q(E) QHP.

If g_Q=dist(E,spectrum(QHQ))>0 is known, (2) proves

    ||Sigma(E)||<=B_N^2/g_Q,
    ||Q psi||<=B_N ||P psi||/g_Q.                      (6)

At the full finite-N ground E0, g_Q is positive: the connected stoquastic
parent has a unique strictly positive ground, which cannot lie wholly in Q.
This finite positivity is not an N-uniform lower bound. The available bare
2U separation of H0 is not a statement about the interacting QHQ at E0.

Even granting an additional fixed g_Q of order U, (6) only bounds the
self-energy by O(Omega^2/U). A direct norm/Weyl comparison with the proved
projected source-gap lower bound

    delta_N=Omega sqrt(N)/[sqrt(2)(N+1)]

therefore becomes inconclusive for large N at fixed Omega/U. This does not
prove that the actual gap closes or the projected result fails; delta_N is
a lower bound, not an asserted exact gap. It shows precisely why that
available norm estimate cannot certify the lift. No U or Omega scaling
with N is introduced to bypass the issue.

The effective source is not just PTP. In the same fixed-P chart, at fixed E,
the affine full source H(theta)=H+theta T gives

    partial_theta H_eff=PTP+PTQ R_Q QHP+PHQ R_Q QTP
                              +PHQ R_Q QTQ R_Q QHP.    (7)

Energy dependence also introduces the normalization factor involving
1-partial_E Sigma, and further source derivatives generate contacts even
though the raw parent is affine. For (5), the last term in (7) need not
vanish despite PTP=QTP=0. Bounds on the off-block source alone cannot drop
QTQ, these contacts, or the actual ground-state preparation.

## A structured second-order cancellation to preserve

There is one exact algebraic hint for the needed finer control. Use the bare
denominator only to define the fixed-N second-order coefficient

    K2=PVQ(C_N-QH0Q)^(-1)QVP.

The cost2U output Gram is h^2[2m(N-m)I+A_move]; the cost4U Gram is
h^2 m(m-1)I. Thus

    K2|_(P_m)=-h^2[2m(N-m)I+A_move]/(2U)
                               -h^2 m(m-1)I/(4U).     (8)

On the right-trivial subspace, the right-endpoint moves keep the occupied
left subset and contribute m(N-m)I. Left-endpoint moves form the Johnson
graph on m-subsets: one occupied vertex is replaced by one unoccupied one.
Its singlet adjacency eigenvalue is m(N-m). For
f(A)=sum_(i in A)x_i, sum_i x_i=0, direct replacement counting gives
A_Johnson f=[m(N-m)-N]f. Hence

    K2_singlet(m)=-h^2[8m(N-m)+m(m-1)]/(4U),
    K2_standard(m)=K2_singlet(m)+h^2 N/(2U),
    K2_standard-K2_singlet=Omega^2/(2UN)>0.             (9)

The standard formula applies for 1<=m<=N-1; the endpoint standard spaces
are absent. Layer exchange gives the identical other standard sector.
The large common second-order shift is therefore not itself an O(1)
singlet-standard split: that difference is only O(1/N) and has a favorable
sign at this order.

Equation (9) is not a controlled large-N effective Hamiltonian or a source
response prediction. The interacting resolvent includes Q flips and the
energy shift from C_N; replacing it by the bare denominator, then growing N
at fixed coefficients, requires a remainder theorem not established here.
The same warning applies to differentiating (8) without its source dressing.

## Narrowed next theorem

The useful next target is a uniform, representation-resolved estimate on the
interacting self-energy and its source derivatives, retaining the common
part and bounding the singlet-standard difference on the actual low states.
Equation (9) shows why a bound on ||Sigma|| alone can throw away the relevant
cancellation. Equation (5) separately requires control of the layer-odd
singlet channel absent from PHP. A demonstrated source-relevant contribution
outside these controls could identify a new full-parent channel; failure to
prove a bound alone would not. The present inequalities do not prejudge its
sign, size or physical usefulness. Another projected radial spectrum would
not answer this question.

Ancestry: `NATIVE_DEGREE_SWITCH_CHANNEL_V001.md`;
`NATIVE_DEGREE_TIE_PROJECTED_SOURCE_BOUND_V001.md`;
`NATIVE_DEGREE_TIE_PROJECTED_STATIC_BOUND_V001.md`; and the same full local
energy/lapse convention retained in those notes. Equations (2), (4), (5) and
(8)--(9) are the new exact off-block and bare-coefficient results. No
autonomous formation, physical volume, absolute-pressure normalization or
shared galaxy/cosmology closure is claimed.
