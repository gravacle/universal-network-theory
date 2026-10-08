# Revised degree-two reference: joint matter gap and source-before-reduction gate

2026-10-05 UTC. Continues NATIVE_DEGREE_TWO_VIRTUAL_STIFFNESS_V001.md and
NATIVE_ACTIVE_RECORD_DRESSED_TRANSPORT_V001.md. New q4-eligibility-specific
and combined-spectrum applications; no replay of their proofs or AO workers.
Native/independent analytical review agrees on the degree and record bounds.
This is a constructive next reference path, not a selected physical phase.

## Why the saturated comparator stays a hold

On the revised d*=2 diamond parent, remove one edge from saturated n=1.
The two degree penalties drop by6. Record feedback changes by
.5(q_u+q_v)<=1. With Nc1, .25(P_u+P_v)-.1T_uv is positive semidefinite.
Storage and active copying are unchanged. Therefore

    H_(n-e)-H_n = -6+.5(q_u+q_v)-.25(P_u+P_v)+.1T_uv
                <= -5 I.                             (1)

The saturated reference can own a held matter pole but is not an autonomous
ground phase under this degree law. This sharpens the resident FF slice
qualification at the actual tuple; it does not determine decay rates,
barriers or metastability with incidence flips restored. No coefficient
is changed to erase it. Support preparation/maintenance remains counted.

## A whole joint sector gap before incidence flips

Keep the SAME revised parent and prospectively supplied simple q4 bipartite
eligible graph, with equal half sizes and nonempty degree-two subspace P.
Use Nc1, one conserved carrier content x, record alphabet B/x, other copies/
ports off. Here H0 has incidence flips off, while actual carrier hopping,
current, record feedback and g=.1 carrier copying remain ON. Incidence n
is block diagonal, but records/carrier need not be frozen or factorized.

For P, record storage exactly cancels feedback, the current term is2j=.5,
and occupied adjacency has norm2. Hence the ENTIRE P spectrum obeys

    spectrum(P H0 P) subset [1.2,1.8].                (2)

For Q=1-P, node degree/record energy is

    f(d,q)=(d-2)^2+q(1-d/2),
    min_q f(d,q) = [4,1,0,1/2,3] for d=0,1,2,3,4.

Equality of the two bipartite degree sums forces at least two defects;
their total minimum is>=1. The carrier operator jD-.1A is>=.15D, and
copying is>=-.1I. A carrier at degree>=2 gives H0>=2.2; degree1 requires
total node cost>=1.5 and is stronger; degree0 stronger still. Thus

    Q H0 Q >= 2.2 I,
    separation(Q,P) >= .4.                           (3)

This retains the actual noncommuting record/copy matrices. It supplies a
legitimate starting separation for joint Schur/Sylvester analysis. It is
not an all-orders finite-h phase or a band/metric proof. A single-content,
B/x sector cannot claim a gap to every retained other-content memory.

## What virtual flips select in the no-carrier reference

For Nc0, copies/ports off and fixed record occupancy q_v=0 or1, one native
link flip leaves P. Two distinct flips cannot return to P on the simple
diamond graph. The EXACT second-order diagonal coefficient at h=0 is

    E2(n,q) = -h^2 sum_e [
       (1-n_e)/(2-(q_u+q_v)/2)
          +n_e/(2+(q_u+q_v)/2)].                      (4)

Let V be number of vertices, Q_rec=sum_v q_v, and A_+,A_- count mismatched
record occupancies across unoccupied/occupied edges. Both the occupied and
complementary eligible subgraphs have degree2, giving

    E2 = -h^2[V+Q_rec/3-A_+/12-A_-/60].               (5)

Uniform occupied records minimize this coefficient: E2=-4h^2V/3, versus
-h^2V for blank records. One hole in the occupied word changes two absent
and two present edge denominators, giving cost8h^2/15. This is a new sparse
q4 application of the earlier complete K(N,N) virtual-stiffness result;
its different eligible-edge count is physical input. It is not a universal
sign conclusion inferred from the complete-slab result.

At Nc0 these record occupations are conserved. The coefficient does not
dynamically write records or demonstrate thermalization. No controlled
remainder at Omega=.6 is supplied by quoting a Taylor coefficient. With
one global sparse family and the inherited h_N=Omega/N, the coefficient
8h_N^2/15 vanishes in the fixed-coordination thermodynamic limit. A local
cell/block meaning for h would be an ADDITIONAL scaling premise. Pure-ring
O(h_N^6) dynamics likewise cannot simply be promoted to a finite bulk clock.

## The actual joint object to derive next

Keep P/Q/source ownership fixed BEFORE reduction. For the complete finite
parent H[J] define A=PHP, W=PHQ, B=QHQ and R(z)=(z-B)^(-1). Then

    K_P(z,J)=A+W R(z) Wdagger.                        (6)

P contains actual records, carrier and incidence, and B contains their
virtual degree defects; it is not an incidence-only energy denominator.
The actual half-edge source projected to degree2 is already nontrivial:

    A[L]=epsilon sum_v L_v P_v
       +sum_e n_e m_e[j(P_u+P_v)-tT_uv]
       +(lambda_R/2)sum_v q_v (L_G(n) L)_v
       +g sum_v L_v P_v X_v,    m_e=(L_u+L_v)/2.       (6a)

Record storage cancels feedback at UNIFORM source, not arbitrary L. The
third term generally does not commute with record X. Uniform-source/all-X
controls therefore cannot replace the nonuniform coupled source action.
At fixed z and projector, a physical source variation gives

    dK=dA+dW R Wdagger+W R dWdagger+W R dB R Wdagger,
    d2K=d2A+d2W R Wdagger+W R d2Wdagger+2dW R dWdagger
        +2dW R dB R Wdagger+2W R dB R dWdagger
        +W[R d2B R+2R dB R dB R]Wdagger.              (7)

All direct contacts, controller/source dependence of support/projectors
when applicable, and complementary memory remain. A frequency-dependent
Schur kernel is not yet a pole-normalized inertial/metric coefficient:

    K_z=-W R^2 Wdagger,
    full_norm=phi_dagger (I-K_z) phi,
    E_J=(phi_dagger K_J phi)/full_norm.               (8)

At a stationary momentum minimum, the actual curvature also retains the
within-P eigenvector relaxation, in addition to explicit K_kk and this
norm. Do not replace it by a hop probability, averaged incidence or raw
Schur coefficient. Uniform complete lapse provides the exact Ward control
K(z,L)=L K(z/L,1), including port/reference sourcing. This alone still leaves
the kinetic ruler C/E0 invariant on fixed physical support.

An incidence-only effective comparator is useful but conditional. If
H_loop acts only on degree-two incidence and records are all X=-1, then

    H_joint = H_loop+(epsilon+2j-g-2t)I+t L_G(n).

Every degree-two graph Laplacian annihilates the SAME uniform carrier
vector. A loop-ground state times that vector has exact addition1.2 and
saturates the lower bound. Nonzero momentum couples to incidence fluctuations
and the full complementary resolvent. Thus quantum loop superposition may
support3D propagation even though each frozen word is a set of cycles;
neither the uniform k0 result nor n replaced by1/2 proves rank-three C.
If the loop ground has a specified momentum and isotropic mean occupied
incidence1/2 in each port class, the carrier Bloch product gives excess
energy<=t a_*^2|k|^2/3+O(k^4). A twice-differentiable lowest fiber band then
has 0<=C<=(2t a_*^2/3)I. This is an upper bound, not positive rank/residue.

The actual revised finite-h parent has record/carrier-dependent O(h^2)
terms and modified higher ring terms. GL6AO's isolated pure-loop63/8 cannot
be appended to it as if this joint effective Hamiltonian were already
derived. No resident packet recovered an actual3D joint pole/curvature.

Next native scientific action: use (3),(6)-(8) to derive the actual coupled
degree-two matter/source kernel in one fixed source chart, retaining those
defects, and determine its physical scaling domain BEFORE borrowing any
collective phase/cone. The exact held-diamond full-copy calculation remains
a comparator. Both must face the common kinetic/census hypothesis and all
Stage3 observations; neither is declared the universe or a superior model.

## Actual finite-flip complementary resolvent: new analytical advance

The h=0 gap alone would not control the FULL B=QHQ. The following stronger
bound does, in a stated large-N sparse family, without building a large
state array. Keep the same simple, regular q4 eligibility on2N vertices,
M=4N eligible bonds, revised tuple and inherited h=Omega/N=.6/N.
Let D_def=sum_v Bad_v, Bad_v=1_(d_v!=2). Pointwise node/carrier surplus
sharpens the earlier bound to

    H0 >= 1.2 I + (1/2) D_def.                       (10)

Indeed f_min-(1/2)Bad is [3.5,.5,0,0,2.5] at degrees0,...,4. Its value
at the carrier plus .15d_carrier is always>=.3, after eps1-copybound.1.
No background offset is counted twice.

For edge e define R_e=both endpoints degree2, Q_e=1-R_e. R_e X_e R_e=0,
and Q_e<=Bad_u+Bad_v. In any normalized state, Cauchy gives

    |<sum_e X_e>| <= 2 sqrt(M sum_e<Q_e>)+sum_e<Q_e>
                  <= 4 sqrt(M<D_def>)+4<D_def>.

Consequently the FULL active-flip parent obeys

    <H> >= 1.2+c<D_def>-4h sqrt(M<D_def>), c=1/2-4h. (11)

On global Q, D_def>=2. If c>0 and c^2>=2h^2 M, the right side is increasing
for <D_def>>=2. Hence

    Q H Q >= [2.2-8h-4h sqrt(2M)] I.                 (12)

N>=576 is a conservative explicit sufficient domain. At N576, h=1/960,
M2304, c=119/240, this gives

    Q H Q >= (263/120-sqrt(2)/5) I,
    delta = 47/120-sqrt(2)/5 >0                       (13)

above the entire P maximum1.8. Lower bound on Q is about1.908824. Bounds
improve with increasing N. This is actual finite-h control with arbitrary
carrier/record/eligible-incidence superpositions; noneligible links, other
record contents/ports and a formed physical phase are not included.

Two distinct single-link flips cannot return a degree-two word on a simple
graph. Thus EXACTLY PHQ QHP=h^2 M P, equal to P/400 at N576. For real z<=1.8,
the full self-energy in (6) is negative semidefinite and

    ||W(z-B)^(-1)Wdagger|| <= h^2 M/delta
                          =1/(400delta) at N576.     (14)

This closes the complementary-resolvent qualification for this family,
not the within-P matter pole, positive rank-three curvature or proper metric.
Source variations still require the actual vertices and a retained causal
domain; the uniform-source bound is not a field equation for arbitrary L.

An explicit source-open domain is available. At L_v=1+f_v, |f_v|<=epsilon,
the degree/record half-node term has norm<=5, and Nc1 carrier storage/current/
hop/copy plus incidence increments give

    ||H[L]-H[1]|| <= rho=(5V+4.9)epsilon,
    source gap >=delta-2rho,
    W_L W_Ldagger <=(1+epsilon)^2 h^2 M P.            (14a)

For 2rho<delta and real z<=1.8+rho, the full source self-energy norm is
bounded by (1+epsilon)^2h^2M/(delta-2rho). The sufficient source amplitude
window shrinks as1/V; it is not a uniform finite-amplitude bulk chart.
Fixed projector/eligibility/source ports remain part of this statement.

## Concrete leading joint kernel and normalization fork

At h=0 the actual degree2 carrier/record block for word n is
A_n=1.5I-t A_n(carrier)+g sum_v P_v X_v. A single added/removed edge has
defect block B_e^plus/minus=A_n+Delta_e^plus/minus, where

    K_e=j(P_u+P_v)-tT_uv,
    Delta_e^plus=2I-.5(q_u+q_v)+K_e,
    Delta_e^minus=2I+.5(q_u+q_v)-K_e.                 (15)

These matrices generally DO NOT commute with A_n. The true h^2 coefficient
at fixed z is h^2 sum_e(z-B_e)^(-1), diagonal in incidence words but an
operator on carrier/records/frequency. At midpoint L, use the actual (6a),
defect increments m_e Delta_e and flip vertices -h m_e, yielding

    K2(z,L)=h^2 sum_e m_e^2
              [z-A_n[L]-m_e Delta_e]^(-1).            (16)

No scalar2+/-q substitution replaces these operators. This earns an explicit
common-action object whose complete source contacts can be evaluated, rather
than importing a pure-loop stiffness or fitted volume energy.

For the inherited global sparse normalization, h^2 M=4Omega^2/N. In a fixed
complementary-gap domain, (14) therefore forces incidence-mediated virtual
feedback to vanish in operator norm as N grows. It does not erase direct
fixed-g record dressing. Proper-clock/cell interpretation and limit ordering
must be resolved before claiming a finite bulk constitutive law.

A constructive ALTERNATIVE under investigation is a fixed proper LOCAL
bond matrix element h_proper on an owned bounded-degree formed graph.
Ordinary extensivity allows ||h_proper sum_e X_e||<=4h_proper N. Its source
vertex is h_proper(L_u+L_v)/2, with the same complete half-edge action.
This physical scaling premise can keep virtual record/loop scales finite
relative to fixed proper probes. It is NOT the earlier Omega/N family,
and it cannot be applied to N^2 possible links without a new locality/support
contract. No h_proper is chosen here from a desired galaxy or expansion
outcome, and the large-N finite-h bound(13) is not imported into that new
family. Its phase, normalization, source/census contacts and physical ruler
must be checked anew. No favorable E(V), hidden donor or record mass is added.

Current exact next native action: determine the scaling/reference domain of
the common kinetic/census hypothesis, then evaluate (16) and its actual
nonuniform source vertices in that same domain, before any observational fit.
The inherited global family and disclosed local-bond alternative remain
distinct; all old completed/failed evidence is preserved. No numerical job
is needed or running for equations(10)-(16); analytical reviews are active.

The next working local family and its immediate matched-reference growth
comparison are specified in LOCAL_PROPER_BOND_NORMALIZATION_V001.md. It
does not inherit the global-family full-Q bound just proved here.

One additional IR warning prevents a false matter-curvature inference.
If a translated degree-two P-ground trial supplies a given total-momentum
character, its variational energy is1.2; block positivity bounds the full
fiber energy below it withinO(1/N). But a short-period incidence word supplies
only characters compatible with its stabilizer, and incidence can carry
the momentum. A fixed matched vacuum, nonzero carrier-addition residue and
uniform analytic pole window are required before interpreting any flat
lowest-total-momentum limit as a vanishing matter C. No such interpretation
or physical dimensional no-go is claimed.
