# Revised native carrier tuple: exact fixed-census constraint

2026-10-05. Analytical only. No numerical producer, retuning, new coupling,
changed formation state or plotting rerun. The missing result below is an
EXACT quadratic energy within a declared number-projected variational
manifold; it is not a full dynamical stability or thermodynamic-phase theorem.

## Recovered anchors and domain

[NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md](NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md)
and [NATIVE_TRANSPORT_TWIST_RESULT_V001.md](NATIVE_TRANSPORT_TWIST_RESULT_V001.md)
already own the signed same-state contact t<n_e T_e>, current work and
pure-gauge relaxed cancellation.
[NATIVE_COLLECTIVE_CARRIER_PHASE_CANDIDATE_V001.md](NATIVE_COLLECTIVE_CARRIER_PHASE_CANDIDATE_V001.md)
owns exact carrier-number phase normalization and conditional-state memory.
[NATIVE_MOBILE_CARRIER_EFFECTIVE_INTERACTION_V001.md](NATIVE_MOBILE_CARRIER_EFFECTIVE_INTERACTION_V001.md)
already proves the j=t Dicke ground anchor and inherited j=.25<t=.5
conditional regular-graph fragmentation preference. Its positive-gap blank-
link virtual reduction is not used here (the revised Delta0,d*2 gives a
different incidence branch).
[NATIVE_ACTIVE_RECORD_DRESSED_TRANSPORT_V001.md](NATIVE_ACTIVE_RECORD_DRESSED_TRANSPORT_V001.md)
already owns active-record ground shifts and blank-record memory controls.

For this calculation HOLD a specified occupied graph G fixed, V vertices,
with d-regular degree where explicitly stated. Same-content carriers are
hard core with exact census Q. First hold records/copies so their fixed-graph
energy is an owned carrier-independent term. Native carrier storage EPQ
also remains. No physical edge length, dimension, volume or density is assigned.

## Exact carrier interaction and boundary-energy bounds

Use carrier occupation p_v=(1+sigma_z,v)/2; incidence n_e is a DIFFERENT
qubit, here held occupied on G. BS07/09/11 give exactly

    T_uv=(sigma_x,u sigma_x,v+sigma_y,u sigma_y,v)/2,
    C_uv=J_uv^2=(1-sigma_z,u sigma_z,v)/2
         =p_u+p_v-2p_u p_v,
    K_G=sum_(uv in G)[j C_uv-t T_uv]
       =sum_edges[j I/2-t(XX+YY)/2-j ZZ/2].             (1)

The identity/current energy is retained. This is an anisotropic
ferromagnetic spin operator, derived from hard-core carrier transfer,
not a fermionic replacement or an independent spin postulate.
For the REVISED tuple t=.1,j=.25, each mismatch block has eigenvalues
j-t=.15 and j+t=.35; occupied-occupied/blank-blank blocks vanish. Therefore

    K_G >= (j-t) B_cut=.15 B_cut,
    B_cut=sum_edges C_uv.                              (2)

If b_min(Q,G) is the minimum occupied/empty boundary over all Q-site basis
sets, the exact carrier ground energy satisfies

    .15 b_min <= E_K,ground <= .25 b_min.               (3)

The upper bound is a basis-state trial (zero mean hopping), not the actual
ground vector. On a held cycle, b_min=2 for0<Q<V, giving .30<=E_K<=.50.
Thus low carrier energy can be carried by small-boundary occupation domains;
it does not require a uniform coherent matter fluid. A ground state's mean
boundary obeys <B_cut><=(5/3)b_min. On a cycle it is<=10/3. These are exact
finite-graph ground constraints, not claims about the executed formation state.

A uniform positive fixed-Q Dicke vector |D_Q> has

    <K_G>=(j-t)d Q(V-Q)/(V-1).                         (4)

For j!=t it is NOT an eigenvector when B_cut varies among Q-site sets:
K_G|D_Q> has basis amplitude proportional to(j-t)B_cut. At Q1 on a
connected regular graph, B_cut=d is constant and the uniform carrier is
the exact ground state, energy(j-t)d. Nonregular graphs additionally have
the owned degree potential: H_car=EP I+t L_G+(j-t)D_G; uniformity then
does not follow. For multiple carriers, finite connected carrier-swap
matrices have a positive ground vector; on a vertex-transitive graph its
one-point density can be uniform even while its occupation correlations
favor clustering. A delocalized superposition of domains is different
from a selected fixed classical droplet.

The old j<t fragmentation proof cannot simply change labels: its

    K_G-(j-t)dQ=t sum(C-T)+2(t-j)sum p_u p_v

has a NEGATIVE pair coefficient at the revised tuple. No inherited
connected-fluid or fragmentation conclusion is imported across this change.

## New exact fixed-Q phase and occupancy energy

To keep Q EXACT, use the normalized variational family

    |Psi(eta,theta)>=Z_Q(eta)^(-1/2)
      sum_(S:|S|=Q) exp[sum_(v in S)(eta_v/2-i theta_v)] |S>,
    Z_Q=sum_|S|Q exp(sum_(v in S)eta_v), sum_v eta_v=0. (5)

This is a comparison family, not an autonomous reduction, a freely
available state filter or a replacement of blank-record formation.
At eta=theta=0 it is |D_Q>. For V>=4 define

    b=Q(V-Q)/[V(V-1)],
    D_Q=Q(Q-1)(V-Q)(V-Q-1)/[V(V-1)(V-2)(V-3)].         (6)

Q1 and endpoints have D_Q=0. Local mean occupancy changes as
delta<p_v>=b eta_v+O(eta^2). On a d-regular graph the first energy
variation vanishes and the exact quadratic terms are

    Delta E_phase=t b sum_edges(theta_u-theta_v)^2,
    Delta E_occupancy=(t b/4)sum_edges(eta_u-eta_v)^2
       -(j-t)D_Q[2sum_edges eta_u eta_v
                              +d sum_v eta_v^2/(V-1)]. (7)

There is no phase/amplitude cross term at this order. An explicit finite-
census derivation uses X=sum eta_v p_v and f_k=(Q)_k/(V)_k. Uniform
sampling gives <X^2>=b sum eta^2 and, for B_pair=sum_edges p_u p_v,

    Cov(B_pair,X^2)=D_Q[d sum eta^2/(V-1)
                                      +2sum_edges eta_u eta_v].

Also each exchange pair has the exact weight
Z_(Q-1)^(excluding u,v)/Z_Q: C gives(e^eta_u+e^eta_v)times this weight,
T gives2e^((eta_u+eta_v)/2)cos(theta_u-theta_v)times it. Expanding the
result, with B_cut=dQ-2B_pair, gives(7); no unprojected product-state
number fluctuation or fitted compressibility is involved.

For a nonuniform adjacency eigenmode of eigenvalue a and zero vertex sum,

    Delta E_occupancy/sum eta^2
       =(t b/4)(d-a)-(j-t)D_Q[a+d/(V-1)].              (8)

On HELD C6 with Q3, d2, a1: b=.3,D_Q=.1. Revised t=.1 gives
.0075-.021=-.0135. Meanwhile its phase quadratic coefficient is
t b=.03 and phase Hessian eigenvalue2t b=.06, POSITIVE. In occupancy
coordinates delta<p>=.3eta, the same energy coefficient is-.15 per
sum(delta<p>)^2. The declared Dicke comparison is therefore not a local
minimum against this number-preserving modulation. For the recovered
oldt=.5,j=.25 comparator the same coefficient is+.0725. Neither number
is an observational fluid sound speed or physical-volume compressibility.
Q3 here is an analytical census, never executed as a new worker. The
completed unclamped K3,3 formation gate and the separately prepared nodal-
source gate have Nc1, for which
D_Q=0 and this particular fixed-graph occupancy direction is positive.
Their actual full graph/record dynamics are different still.

## Records, dynamic graph and relaxed-source qualifications

For held degree2 at ER1,lambdaR.5, the record detuning vanishes. Uniform
active carrier copying is exactly g sum_v p_v X_r,v>=-gQ. All records
in X=-1 saturate this bound for every carrier state, so the conditional
ground energy is shifted by-gQ, with no change to fixed-Q topology or
carrier stiffness comparisons. This is the prior ground-state application,
not a newly prepared record phase. Actual initially blank records give
the prior exact mixture over static onsite potentials g sum sigma_v p_v;
they are not the all-lower X=-1 branch. With no writer, unoccupied nodes
also have no copy gap; no global adiabatic elimination follows.

Incidence flips change degree, record detuning and conditional hopping
coherences. The full phase contact remains t<n_e T_e>, never a product
of averages;(7) is not its full actual-state memory or fluctuation kernel.
At fixed H a state twist has real endpoint work. A consistently conjugated
Hamiltonian with vertex-gradient hopping phases is pure gauge and its
fully relaxed curvature vanishes through contact/current cancellation.
Positive phase contact, occupancy Hessian and relaxed stiffness are thus
three distinct experiments. Fixed boundaries, cycle holonomy and complete
physical-source contacts would need their own specification.

Constructively, clustering would mean dynamically earned carrier/record
correlations and occupied-region boundaries from the SAME native action.
The boundary energy in(2) is energy per graph cut, not physical area/tension.
One could investigate whether these domains provide a reproducible material
state and environmental response, retaining their formation/preparation and
source costs. Homogeneous low-energy mobile matter is not justified by a
positive hopping contact alone. Native pressure, physical deformation and
galaxy/expansion matching still require the same full energy and earned
clock/ruler/volume map; no bulk,3D or superiority claim follows here.

Independent read-only algebra review PASSED the spin block, cut bounds,
fixed-Q covariance/Hessian and both C6 coefficients before this note was
saved. This is internal mathematical review, not numerical/observational
evidence. No producer or worker was launched. Parent owns log/ledger.
