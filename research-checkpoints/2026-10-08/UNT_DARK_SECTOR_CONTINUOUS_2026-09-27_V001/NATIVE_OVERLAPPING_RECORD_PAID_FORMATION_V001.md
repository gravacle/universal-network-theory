# Overlapping native record-paid formation: exact ledger and competing channels

2026-09-27. Analytical extension of
`NATIVE_RECORD_PAID_LINK_FORMATION_V001.md`, using BS06, BS08, BS10 and
BS11 of `recovered_sources/BS_MICRO_ACTION.md`. This derives a shared-record
connected-path energy channel, not a tensor product of isolated cells. The
full native dynamics and each conditional comparison are distinguished below.
No numerical computation is used in this note.

## 1. Complete shared-degree identity

Consider one bipartite slab, with carriers/reservoirs blank and prospective
writer contents fixed. Copying can be active on declared sites; its coefficient
and switching belong to the preparation protocol. Let U=U_d>0,
h=Omega/N, M=sum_e n_e, Q=sum_v q_v and

    a=4U d_*-Delta-2U.

Relative to the empty-graph, blank-record energy E_empty (INCLUDING the
2NU d_*^2 baseline and every fixed writer/spectator energy), the exact native
diagonal operator is

    H_diag-E_empty=-a M+2U sum_v C(d_v,2)
                         +epsilon_r Q-lambda sum_v q_v d_v.       (1)

Choose the N-independent relation

    lambda=2U,                 epsilon_r=a+2U.

Then the following is an operator identity, not an expectation closure:

    H_diag-E_empty=a(Q-M)+2U R,
    R=sum_v[(1-q_v) d_v(d_v-1)/2
                      +q_v(d_v-1)(d_v-2)/2] >= 0.                (2)

Nonnegativity uses integer degree: an occupied isolated vertex contributes
one to R. All degree and occupation operators commute, so (2) also applies
to coherent states and mixed states without replacing their moments by means.
The full Hamiltonian still contains -h sum_e X_e plus the local copy terms.
Neither Q-M nor R is conserved by those terms.

A path with one blank degree-one root, an occupied degree-one tip and occupied
degree-two interiors has Q=M and R=0. An all-occupied simple cycle likewise
has Q=M and R=0. Thus paths of arbitrary length, their mergers and eventual
cycle closure can share exactly the empty initial diagonal energy at fixed
coefficients. The stored record energy is paid by the ACTUAL overlapping
graph and feedback terms. R=0,Q=M does not specify a unique graph: paths
with two blank endpoints and paths with two occupied endpoints can also
balance globally; cycles and disconnected unions are allowed.

More locally, add a previously absent edge uv and write a previously blank
record at v. If the pre-addition degrees are d_u,d_v, then

    Delta E=epsilon_r-a+2U(d_u+d_v)
                             -lambda(q_u+d_v+1)
           =2U(d_u-q_u).                                      (3)

Consequently the endpoint resonance tests the donor's d_u=q_u, independently
of the target's prior degree. It holds for an occupied degree-one tip, but
ALSO for an unused blank degree-zero donor. This exact degeneracy is the
main formation competition that a connected-growth calculation must retain.

## 2. Two balanced local channels and an owned detuning schedule

Hold all other graph incidences and records fixed ONLY to define a local
comparison. For a qualified donor d_u=q_u, one candidate edge n and target
record q have

    H_local=C+(-a+2U d_v)n+(a+2U-2U d_v)q
                                     -2U nq-hX_n+gX_q.         (4)

Both endpoint energies coincide. The two intermediate energies coincide
at +U precisely when a=2U d_v-U. Thus:

* A fresh isolated blank target (d_v=0) has the balanced diamond at a=-U,
  epsilon_r=U. This is the fixed-coefficient beating channel independently
  derived in the assertion-threshold review.
* A blank degree-one root has the balanced diamond at a=+U,
  epsilon_r=3U. At a=-U its intermediates are instead -U and +3U;
  the fresh-target transfer formula cannot be reused for closure or merger.

For either balanced diamond the endpoint-parity blocks have off-diagonal
couplings g-h and g+h and common second diagonal U. Their gaps are
R_+=sqrt(U^2+4(g-h)^2) and R_-=sqrt(U^2+4(g+h)^2).
Writing Rbar=(R_-+R_+)/2 and deltaR=R_--R_+=8gh/Rbar, the half-integer
timing construction gives joint transfer at least
1-[pi deltaR/(4Rbar)]^2 at a time of order N, with fixed nonzero U,g,Omega.
This is a conditional four-state result, not a full-slab invariant sector.
The two-plus-state endpoint parity convention changes only unobservable
basis signs, not the gaps or probability bound.

A prospective schedule joining the two channels needs no new Hamiltonian
term: fix d_*, U, lambda=2U and Omega, and change the existing coefficients

    Delta(a)=4U d_*-2U-a,        epsilon_r(a)=a+2U,
    -U <= a <= +U.                                            (5)

For example d_*=2 gives Delta in [5U,7U] and epsilon_r in [U,3U]. The
native extensive margin holds throughout for |t_hop|<U with an appropriate
positive delta_E. Carriers may remain blank; all coefficients stay positive
where BS requires positivity. The degree baseline remains fixed. Exactly,

    partial H/partial a=Q-M,
    W_detuning=integral dt adot(t) <Q-M>_t.                    (6)

Equation (6) is zero on an ideal Q=M configuration, but the actual evolution
leaves that manifold; its work must be measured/retained. Copy switching
likewise contributes sum_v integral dt gdot_v <X_qv>. These are owned control
work terms, not claims that the controller is autonomous or costless.
The constant-coefficient fresh channel alone is feasible with
a=-U, epsilon_r=U, d_*=(Delta+U)/(4U), Delta>4U+|t_hop|.

## 3. Exact conditional many-donor competition

Take a fresh target and m candidate donors whose background degrees satisfy
d_u=q_u. Fix their other incidences only in this comparison, use a=-U, and
retain EVERY one of these m edge flips and the target copy term. With
k=sum_{i=1}^m n_i, the exact comparison Hamiltonian is

    H_star=C+U(k-q)^2-h sum_i X_i+gX_q.                        (7)

The shared target degree produces the k^2 term; omitting it would incorrectly
turn the calculation into independent diamonds. Permutation symmetry of the
candidate edges and an initially empty star imply equal probabilities for
each particular state k=1,q=1 at every time. A specified connected-append
edge therefore receives exactly 1/m of the TOTAL one-edge/record success.
Unused blank donors and occupied tips are indistinguishable in (7).

The comparison reduces exactly to 2(m+1) symmetric Dicke states. The k to
k+1 hopping is -h sqrt((k+1)(m-k)); the q coupling is g. Higher k remain
in this matrix and must not be discarded. For fixed Omega, the initial
collective hopping scales Omega sqrt(m)/N, not Omega/N. This supplies a
small, analytically specified comparison without assuming either dilute
occupation or isolated-cell timing.

For fixed m and h,g small compared with U, second-order elimination gives
the local pair matrix element +2hg/U from the two +U intermediate states.
It does not select the connected donor. This is a finite-dimensional
perturbative statement; it is not a uniform-in-N elimination of the full
native slab, whose other edges remain dynamical.

## 4. Smallest full-native competition witness

For N=2 label the four edges x=a0-b0, y=a0-b1, u=a1-b0 and v=a1-b1.
Fix q_b0=1 and q_a0=q_b1=0, and activate copying only at a1 with record q.
Carriers/reservoirs are blank. These record/writer restrictions are invariant;
none of the four graph links is frozen. At a=-U the exact 32-state diagonal
polynomial, relative to the same E_empty, is

    E/U=1+q-x+y-u+v-2q(u+v)
                         +2xy+2uv+2xu+2yv.                    (8)

The initial basis state is (x,y,u,v,q)=(1,0,0,0,0). The connected append
target (1,0,1,0,1) and disconnected-seed target (1,0,0,1,1) both have E=0.
Freezing the background row x=1,y=0 reduces (8) to (u+v-q)^2, the m=2
comparison (7); its two target probabilities are exactly equal. In the full
model their diagonal difference under exchange is instead

    E(x,y,u,v,q)-E(x,y,v,u,q)
                          =-2U(u-v)(1-x+y).                    (9)

Background flips therefore break the comparison symmetry. The full test
must retain them and measure append and seed separately, total q=1,u+v=1
success, and background-row departure. It should compare (7), not identify
its projected dynamics with the full slab. Finite-time preference is an
output, not an acceptance requirement.

There are also prospective exact short-time checks. Put tau=T/hbar and
H'=H-E_empty. Both target probabilities equal h^2 g^2 tau^4+O(tau^6).
Their H'^2 and H'^3 matrix elements from the initial state are respectively
-2hg and -2Uhg, and their H'^4 elements coincide. Path enumeration gives

    (H'^5)_append,initial-(H'^5)_seed,initial=40U h^3 g,
    (H'^6)_append,initial-(H'^6)_seed,initial=320U^2 h^3 g,
    P_append-P_seed=-(2/3)U^2 h^4 g^2 tau^8+O(tau^10).          (10)

For an independent hand check, only four-flip paths containing x twice or y
twice distinguish these elements. Summing their intermediate-energy sums
gives -20U for each background edge. Summing their second complete homogeneous
energy polynomials gives -52U^2 for x and -268U^2 for y. Each path's flip
product is -h^3g. Equation (10) predicts the earliest contrast, not the sign
at an isolated-diamond transfer time.

## 5. Constructive use and next decision

The exact ledger establishes an extensive-capacity resonant path/cycle
channel using shared records and fixed native coefficients. It does not yet
establish a finite-density CONNECTED preparation probability. The actual
competition is now explicit, rather than an unspecified scaling objection.

A prepared matching pool removes the unused-blank donor competitor: occupy
one endpoint record of each edge and leave the other endpoint blank. At
a=+U, writing a blank root can merge it with another occupied tip. The first
merge into a single-edge component cannot close that component, because its
own edge is already present. Once components grow, however, closing the
target's own path is also resonant. Degree-only energy does not distinguish
that closure from a merger with a different path. A matching-pool protocol
must therefore account for component populations or an explicit port-based
choice; it cannot announce a single spanning cycle from the diagonal ledger.

The full 32-state witness is the smallest decisive next measurement of this
competition, with one frozen prospective coefficient set and no new terms.
After it, the exact 2(m+1) star identifies the appropriate collective
comparison, while (5)-(6) supply a separately declared, work-accounted merger
schedule to test. None of these steps resets the baseline energy, assumes
cooling, hides excited population, changes h=Omega/N, or imports a spatial
metric.

## 6. Controlled collective formation in the comparison, with no population deletion

There is a useful large-N theorem for the EXACT symmetric star (7). Fix
0<g<=U/4 and Omega, allow 1<=m<=N, and define alpha=h sqrt(m). In the Dicke
basis, write H_star-C=H0+alpha W_m. H0 is block diagonal in k with

    H0(k)=[[U k^2,g],[g,U(k-1)^2]],
    E_k,plus/minus=U[k^2+(k-1)^2]/2
                        +/- sqrt[U^2(2k-1)^2+4g^2]/2.          (11)

The k=0 and k=1 blocks have identical two eigenvalues
E_minus/plus=(U +/- sqrt(U^2+4g^2))/2. The four-dimensional subspace P
containing BOTH complete blocks is spectrally isolated from every k>=2,
uniformly in m. Its smallest separation is

    delta=[sqrt(U^2+4g^2)+sqrt(9U^2+4g^2)]/2-2U > 0.           (12)

Indeed E_2,minus lies delta BELOW E_plus and at least U above E_minus;
E_2,plus is over 2U above E_plus. For k>=3,
E_k,minus>=U(k-1)^2-g and E_plus<=U+g, so the separation is larger.
The selected quartet is NOT the four lowest levels: E_2,minus intervenes.
In particular this construction retains the initial state's upper-branch
population; it does not cool or project it away.

The operator W_m has adjacent-k coefficients
sqrt((k+1)(1-k/m)), bounded by sqrt(k+1). Although its full norm grows with
m, this causes no uncontrolled perturbative step. On the union of the two
circles |z-E_minus/plus|=delta/3,

    ||W_m(H0-z)^(-1)|| <= 8/delta,                           (13)

uniformly in m. To check the bound, split W into lowering and raising parts;
each weighted shift times the block resolvent has norm at most the supremum
of sqrt(k+1)/dist(z,spectrum H0(k)). For k=0,1 this is at most
3sqrt(2)/delta; for k=2 it is at most 3sqrt(3)/(2delta); the displayed
quadratic lower bound controls every k>=3 more strongly. More precisely,
the raising supremum is at most 3sqrt(2)/delta and the lowering supremum
at most 3/delta, so their sum is less than 8/delta.

For sufficiently small alpha/delta, the resolvent Neumann series on these
contours converges uniformly. Its contour integrals give an exact spectral
projector P_alpha with ||P_alpha-P||=O(alpha). The direct-rotation unitary
from P to P_alpha is likewise I+O(alpha). Its effective four-state generator
is

    H_eff=P H0 P+alpha P W_m P+O(alpha^2),                    (14)

with constants depending on U,g, not m,N. These statements follow directly
by integrating the uniformly convergent series: the zeroth-order projector
is P, and the first-order rotation is off-diagonal, so its commutator with
H0 has zero P-to-P block. Integrating z times the same resolvent controls
H P_alpha uniformly and proves the second-order remainder in (14), without
treating (13) as a bound on ||W_m||.

The leading generator in (14) is precisely the balanced isolated diamond
with link flip alpha rather than h. Let T_alpha be its declared half-integer
beating time from Section 2; T_alpha=Theta(hbar/alpha) at fixed U,g.
The exact star evolution and this diamond differ in state norm by at most

    C(U,g)[alpha+alpha^2 |T|/hbar]

on P initial states for |T|=O(hbar/alpha). This follows by rotating to the
exact spectral subspace, bounding the O(alpha) initial complement and using
the unitary Duhamel estimate on (14). Combining it with the diamond's
O(alpha) target-state norm error proves

    P_star(k=1,q=1;T_alpha)>=1-C'(U,g) alpha^2.                (15)

All constants have the required inverse-energy dimensions. Equation (15)
is an asymptotic bound for alpha sufficiently small, not a numerical error
bar for the N=2 witness. For m proportional to N, total one-edge/record
formation is 1-O(N^-1) at T=Theta(sqrt(N)); a PARTICULAR connected-append
edge still receives exactly 1/m of that success. For fixed m the time is
Theta(N) and the total error is O(N^-2).

This theorem advances the collective scaling calculation while exposing
the precise selection problem. It applies only to the explicitly defined
conditional star: transferring it to the full slab requires controlling
the omitted background flips over these growing times. The fixed-time
prepared-graph comparison bound does not do that automatically.

## 7. An all-time sparse bound for the full single-writer competition family

The N=2 fixture has a full-native extension with one initial edge, one fixed
occupied endpoint record and one active fresh writer, for every N>=2.
No graph links are frozen. In this invariant record sector 1<=Q<=2. At
a=-U define k_v=d_v-q_v and K=sum_v k_v^2. The exact diagonal identity is

    H_diag-E_empty=U sum_v(k_v^2-k_v/2)-UQ/2
                                      >=(U/2)K-U.             (16)

The integer inequality k^2-k/2>=k^2/2 is valid for positive and negative k.
The statewise star-projector proof in
`NATIVE_UNIFORM_REGULAR_DEGREE_BOUND_V001.md` also permits the target degree
to be the quantum record projector q_v: graph-star flips commute with q_v,
and one conditions its two target-degree blocks before taking their maximum.
For P_v=1_(d_v=q_v), P_v S_v P_v=0 and
||Q_v S_v P_v||^2<=3N. On Q_v, d_v<=2(d_v-q_v)^2. The same summation gives

    |<V_flip>|<=Omega sqrt(6<K>)
                                  +Omega sqrt(2/N)<K>.        (17)

This does not require feasible degree lists or a classical q state; it is
a quadratic-form estimate and remains valid with graph/record entanglement.
The copy energy has absolute mean at most |g|. The initial complete energy
relative to E_empty is exactly zero. Therefore energy conservation gives,
at EVERY time, with A_N=U/2-Omega sqrt(2/N)>0,

    A_N<K>-Omega sqrt(6<K>) <= U+|g|,
    sqrt(<K>) <= [sqrt(6)Omega
           +sqrt(6Omega^2+4A_N(U+|g|))]/(2A_N).                (18)

Finally 2M=Q+sum_v k_v<=Q+K as an operator inequality, so
<M><=1+<K>/2. For fixed native coefficients and sufficiently large N, the
entire full graph thus retains O(1) expected occupied edges for all times
in this single-writer resource sector, despite N^2 active possible links.
This is an actual-dynamics bound, not a ground-state or frozen-star claim.
It prevents a hidden dense background from being assumed away. It does not
bound the phase accumulated from those O(1) background excitations, choose
append over seed, or supply a finite-density writer resource protocol.
