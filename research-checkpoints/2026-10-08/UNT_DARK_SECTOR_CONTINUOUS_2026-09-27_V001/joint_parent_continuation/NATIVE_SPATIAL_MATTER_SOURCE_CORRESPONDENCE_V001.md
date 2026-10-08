# Spatial matter response and an independent network probe

2026-10-03 UTC. This continues frontier V115 without repeating its source
coefficients or running another numerical worker. The complete energy-source
comparison extends to bounded spatial lapse profiles. Exact record identities
constrain a microscopic lapse interpretation, while the original two-content
carrier algebra supplies a genuinely independent probe. Its preparation,
initial energy and retained record memory are specified below.

These are internally checked mathematical results and a qualified next
experiment, not a completed gravity test. Graph formation, physical rulers,
volume, the dense/sparse gravitational law and cosmic expansion remain open.
The external lapse chart is still a proposed diagnostic coupling, not an
endogenous field derived from matter. A supplied regular graph is not a
formed universe.

## Complete spatial source and finite time control

Use the complete node energy allocation in
NATIVE_ACTIVE_RECORD_MECHANISM_AND_STATE_V001.md, with H[L]=sum_v L_v h_v.
The one-content preparation and definitions are those of V115. Take a definite
initial graph G with maximum degree D and a common time interval [0,T]. Allow
spatially and temporally varying real profiles satisfying

    0<L_min <= L_v(x) <= L_max,

where the bounds are independent of N. No spatial smoothness is needed for
this microscopic estimate. Write m_e=(L_u+L_v)/2 on e=uv, j=lambda_J,
b=|j|+|t|, ell=b+2|lambda_R|, and x=tau/hbar.

In the reference comparison retain the full weighted incidence Hamiltonian,
including degree penalties and flips, but freeze incidence only in its
couplings to the node registers. The exact difference is

    H[L]-H_ref[L]=sum_e Delta n_e W_e[L],
    W_e[L]=j[L_u p_u(1-p_v)+L_v p_v(1-p_u)]
          -t*m_e*T_e-lambda_R(L_u r_u+L_v r_v).

Here Delta n_e=n_e-n_e(G). The edge norms are bounded by L_max*ell; reference
node edge interactions by L_max*b. Onsite recording remains active. The
selected-bit probability argument in V115 now uses

    q_L(s)=sinh(|Omega| L_max*s/N),
    <(Delta n_e)^2> <= q_L(s)^2.

For a bounded node observable O_X the same local interpolation gives

    E_O,L(T) = 2 L_max ell ||O_X|| |X| N
      *integral_0^T q_L(s)^2 exp[4 L_max b D (T-s)] ds
      = O_T(1/N).                                             (1)

This is an expectation bound for arbitrary initial node states, not a
global trace-distance statement or a source-derivative limit. It also holds
for the qutrit carriers below: the edge current-square is the single-occupied
projector, T has norm one, and the record occupation q^r has norm one.

For completeness, define beta_N=N*q_L(T)^2 and
gamma_N=N*q_L(T)^2+N*(N-1)*q_L(T)^4. In the conjugate energy h_v, the direct
incidence correction to its mean is bounded by

    |U_d|[2|d_v(G)-d_*| beta_N+gamma_N]
    +(|Delta|/2+|t|/2+|j|+|lambda_R|) beta_N
    +|Omega| q_L(T).                                          (2)

Add (1) for the bounded, fixed-G node allocation h_v^G. The last term in
(2) retains flip coherence: |<X_e>|<=2 q_L. Thus each local energy error,
and bounded weighted energy averages per declared node, are O_T(1/N).
The conjugate energy is h_v=partial H[L]/partial L_v, not L_v*h_v.

Controlled work includes source jumps:

    W_source=integral sum_v <h_v> dL_v.

Its error per node is bounded by the largest local-energy error times
V^(-1) sum_v TV(L_v). Bounded average total variation is required; bounded
amplitude alone does not control arbitrarily repeated switching.

An unbounded physical-position source is not covered. Readout weights of
size R_N at most give an O(R_N/N) estimate from (1). An applied profile
1+g dot R/c^2 can lose positivity on growing two-sided patches, and growing
L_max changes both q_L and the locality exponential. No physical ruler,
fixed-gradient infinite-volume limit or interchange of source derivatives
and size limits follows from (1).

## Exact energy of the matter preparation

First keep the original one-content sector. For V>2 and uniform fixed-Q
carrier state sigma_0, let M=sum_v m_v p_v with sum_v m_v=0, and set

    s=Q(V-Q)/[V(V-1)],    k=(Q-1)/(V-2).

For the tangent delta sigma=sigma_0 M, fixed-Q combinatorics give

    delta<p_v>=s m_v,
    delta<p_u p_v>=s k(m_u+m_v),       u!=v.

Blank records, uniform writers and definite regular G imply exactly

    delta E_initial[L]=s sum_v m_v {
      [epsilon_psi+j*d*(1-k)] L_v-j*k*sum_(u~v) L_u}.           (3)

The proof retains the complete initial carrier-dependent diagonal energy
(epsilon_psi+jd) sum L_v p_v-j sum_edges(L_u+L_v)p_u p_v.
Graph/writer constants have zero tangent; initial hopping, flip and copy
means vanish, as do blank-record storage means. These terms remain in H.
Equivalently the braces in (3) are

    [epsilon_psi+jd(1-2k)]L_v+jk*(Delta_G L)_v.

Uniform L therefore gives zero initial mean-energy change. For the normal
bipartite profile L=1+alpha*eta, its nonconstant part is
alpha*(epsilon_psi+jd)*eta_v, agreeing with the complete normal source.
For V115's pair channel, sigma_eta=sigma_0[I+eta(p_a-p_b)], equation (3)
times eta is the EXACT finite mean-energy change, not only a tangent.
Arbitrary M requires its own positivity and apparatus construction.
This coefficient is not automatically an inertial or gravitational mass.

## A protected microscopic record constraint

In the invariant one-content record sector define

    X_v=|s><B|+|B><s|,
    Y_v=i(|s><B|-|B><s|),
    D_v=< (epsilon_r-lambda_R*d_v) Y_v >.

D_v is a joint expectation, not a product of separate means. With fragment
couplings off and no additional active ports, the FULL changing-incidence
parent obeys

    d<X_v>/dx=L_v D_v.                                       (4)

All copying terms commute with X_v in this invariant sector. At any common
usable internal phase Theta with nu=dTheta/dx,

    I_vz=D_z*d<X_v>/dTheta-D_v*d<X_z>/dTheta
        =(L_v-L_z)D_v D_z/nu.                                (5)

After a native matter preparation the subsequent Hamiltonian has L=1, so
I_vz=0 for every state, including correlated states and arriving carriers.
A lapse representation required to match the SAME exterior X_v,D_v histories
must therefore have equal exterior L_v,L_z wherever their product D_v D_z
is nonzero. To linear order it requires ell_v=ell_z there. For the original
regular, blank-record preparation, D_v=-2 delta_d(g_w+g_p*rho)x+O(x^3), so
there is a nontrivial small positive interval when delta_d!=0.

This is a constraint on that microscopic dictionary. It does NOT reject
source-region-only profiles, additional spatial-metric channels or a
coarse-grained geometry using a different justified probe algebra. Uniform
clock rescaling remains relationally invisible. Fixed readouts in (4) have
no bare source contact; weighted coordinate readouts or added ports must
retain their contacts/commutators. Retiming cannot spoil an identically zero
native I_vz.

The limitation is important: reproducing every microscopic equation using
a changed generator is a stronger requirement than emergent metric behavior.
Equation (5) is not a no-go theorem for gravity or for UNT.

## Two native contents provide an independent probe

BS07 through BS10 already conserve carrier Q_0 and Q_1 separately, with
fragments and extra ports inactive. Use content 0 for source matter and
content 1 for a tagged probe. Both move under the same parent, including
recoil, exclusion and record interactions. No new force or carrier mass
coefficient is introduced. A content label is not an identification with
a photon, and this choice does not prove universal coupling.

The records must now be full qutrits. For fixed G and writer content 0,
the conditional record Hamiltonian along carrier paths is

    h_v^record=delta_d q_v^r+(g_w+g_p p_v^0)X_0v
                                    +g_p p_v^1 X_1v.         (6)

X_0 and X_1 do not commute. The complete energy allocation uses total
carrier occupation p=p^0+p^1 and replaces the old one-content copy term by
g_w X_0+g_p(p^0 X_0+p^1 X_1). All its graph/current/transport energies
remain. In particular J_e^2=p_u+p_v-2p_u p_v still holds.

The original one-content record identity must not be reused unchanged.
With Y_01=i(|1><0|-|0><1|), a_s=g_w P_w^s+g_p P_psi^s, and
delta_v=epsilon_r-lambda_R*d_v, the exact equations are

    d<X_0v>/dx=L_v <delta_v Y_0v+a_1v Y_01v>,
    d<X_1v>/dx=L_v <delta_v Y_1v-a_0v Y_01v>.                  (7)

Replacing D in (5) by the corresponding full joint readout restores the
algebraic identity, with its same microscopic-dictionary limitation. There
is no nontrivial fixed record-only axis commuting with BOTH X_0 and X_1:
commutation with their squares forces diagonality, then commutation with
each X_s equates all three diagonal entries. Initial vanishing of a mixed
term in (7) is not an all-time simplification.

### An explicit source preparation with a separate probe

Initially place the single content-1 carrier at w. On the remaining
W=V-1 nodes take the uniform fixed-Q_0 mixture of content-0 carriers.
Keep definite G, blank records and uniform content-0 writers. Choose source
sites a,b distinct from w and use the same local amplitude-transfer channel,
now with A=|0,B><B,0| on a,b, K_1=sqrt(eta) A and
K_0=sqrt(I-eta A^dagger A), 0<=eta<=1. Then exactly on this initial support,

    sigma_eta=sigma_0[I+eta(p_a^0-p_b^0)].                    (8)

The full qutrit identity AA^dagger-A^dagger A is
p_a^0 B_b-B_a p_b^0, NOT globally p_a^0-p_b^0. Equation (8) works because
the initial pair contains no content 1. Do not apply it to an aged state
after the probe moves without recomputing the actual channel.

For W>2 let s_0=Q_0(W-Q_0)/[W(W-1)], k_0=(Q_0-1)/(W-2),
d'_v=d-A_vw, and m_v=delta_va-delta_vb. The exact initial mean-energy
change for the spatial source is

    (E_eta[L]-E_0[L])/eta = s_0 sum_(v!=w) m_v {
       [epsilon_psi+j*d'_v*(1-k_0)]L_v
       -j*k_0*sum_(u~v,u!=w)L_u-j*L_w*A_vw}.                (9)

Here A_vw is adjacency, not the channel operator A. Edges not touching w
give the fixed-Q_0 covariance on the reduced graph; an edge uw contributes
j L_w(1-p_u^0) initially, supplying the last term. At L=1 equation (9)
reduces to -2j(1-k_0)s_0*(A_aw-A_bw). It vanishes when both source sites
have the same adjacency to the initial probe, including both nonneighbors.
Regularity by itself is insufficient after pinning a probe initially.

The carrier entropy change is exactly

    Delta S=-s_0[(1+eta)ln(1+eta)+(1-eta)ln(1-eta)].          (10)

Zero mean-energy change is therefore not a free preparation. An explicit
apparatus dilation, retained correlations and reading costs remain physical
obligations. Subsequent evolution does NOT clamp the probe or source.

For a clock site outside the initial probe and source sites, an embedded
content-0 record clock has the original nonzero initial amplitude and rate
with local filling Q_0/W. Its later derivatives must include (7). Bounded
local commutator norms give a small size-independent working interval by
the amplitude/rate continuity argument of V115, now on qutrits; the old
single-content numerical constants are not asserted unchanged. Longer
coarse-graining windows require renewed clock qualification.

## What record memory can transmit

For independent initial blank records, conditional carrier histories have
the exact factor

    F[p^+,p^-]=product_v <B|U_v[p^-]^dagger U_v[p^+]|B>,      (11)

with chronological THREE-dimensional record propagators from (6). This is
one factor in a coherent path sum, not a classical path probability. It
does not discard current-pair energy, exclusion or carrier hopping.

Consider specified source histories S, probe histories P, and their removal
controls at fixed G. If the union of sites visited on either source branch
is disjoint from that visited on either probe branch, then sitewise
factorization proves

    F_SP F_empty=F_S F_P.                                   (12)

The cross-multiplied form is valid even at influence zeros. The empty
control on a physical common background has F_empty=1. Thus record memory
is local in space but persistent in time: visits at DIFFERENT times to the
same record can interact. Neighboring carrier occupations can also interact
through the direct current term, and exclusion acts on coincident attempts.

Equation (12) is not a vanishing-response theorem for the summed quantum
paths. Virtual excursions, later encounters and finite-density collective
mediation remain. In particular other source-content carriers can carry a
disturbance from the preparation region to the probe without one identifiable
prepared particle arriving. Finite-N incidence mediation also remains;
its fixed-time comparison, not all possible limits, is controlled by (1).
Do not impose an uncosted no-encounter postselection. Initial correlated
records or active fragments require their corresponding joint boundary or
larger local propagator, not (11) unchanged.

## The next observable is probe coherence as well as transport

Use a_1v=|B><1| on the carrier register. In the single-probe sector the
matrix C_uv=<a_1v^dagger a_1u> is positive with trace one. It retains both
probe occupation and coherences accessible to a declared interference
readout. Under (8), the actual preparation derivative is

    b_uv(x)=Tr[sigma_0(p_a^0-p_b^0)
                        (a_1v^dagger a_1u)(x)].              (13)

Use Hermitian real and imaginary parts as separate readouts. The initial
tagged-probe matrix is unchanged by (8). The signed initial tangent has
trace norm 2s_0; applying (1) to its two positive parts controls (13) by
2s_0 E_O,L. Spatial propagation and the clock response must both be retained.
For a common invertible phase with unchanged initial clock phase,

    b_uv|Theta=b_uv-(dot C_uv/nu)*Im[b_B/beta_B].              (14)

An affected clock alone is not a distant force. Source-copy effects on
coherences are not obtained just by tracking source occupation arriving at
another node. Nor may the record influence's magnitude replace its phase.

For comparison use the SAME complete energy-source kernel from
NATIVE_FORMED_STATE_SOURCE_MATCHING_V001.md, now evaluated in this qutrit
preparation. A declared effective source description must match all chosen
real/imaginary probe entries with one profile, with the same clock,
preparation boundaries, source work and any explicit readout contacts.
Fitting a new profile to each entry or retaining only its favorable real
part is not a common-source test.

This test is still insufficient to establish gravity unless its spatial and
temporal coarse-graining window, physical probe dictionary and errors are
qualified. The native uniform source is an internal-clock null direction,
not a free fitting parameter. The exact microscopic restriction (5), its
qutrit version (7), and local memory (12) constrain proposed interpretations
but do not prove a collective metric or eliminate every such possibility.

## Exact separation of connected probe effects

There is a useful separation BEFORE choosing an approximate continuum
description. Organize frozen-G paths in an enlarged product of two
single-content hard-core species, imposing the original qutrit restriction
by a cross-exclusion indicator A_01 on both contour branches. This is only
a bookkeeping enlargement, not a new physical state space. Include initial
and readout endpoint restrictions in A_01.

The diagonal current energy has the cross-content part

    V_01=-2j sum_(uv in G)(p_u^0 p_v^1+p_u^1 p_v^0),
    D_01=exp[-i integral(V_01^+-V_01^-)dx].

Same-content interactions, linear degree energies, and hopping amplitudes
belong to the respective single-species path factors. Let F_01 be the
joint record influence, F_0,F_1 the removal controls, and
C_r=F_01-F_0 F_1. Then the exact algebraic identity is

    A_01 D_01 F_01 = F_0 F_1
         +(A_01 D_01-1)F_0 F_1+A_01 D_01 C_r.                (15)

The three terms are an independent reference, the direct-current/exclusion
correction, and the shared-record correction INCLUDING its interference
with direct effects. Values assigned on forbidden overlapping paths are
formal extensions: A_01 removes them from the physical left side, and the
right-side terms cancel them exactly. These complex terms are neither
probabilities nor separately measurable forces.

For (8), with a fixed initially localized probe and a trace-zero source
tangent, the independent path sum factorizes and has zero source response.
After the full coherent sums the actual probe preparation response is thus

    b_O=b_O,direct/exclusion+b_O,shared-record.               (16)

For O=a_1u^dagger a_1v, use the enlarged probe insertion |u><v|. The ket
endpoint requires source vacancy at v and the bra at u, with source endpoints
identified by the background trace. Both constraints belong inside A_01.
Putting them instead in a bath-dependent factor common to all three terms
would invalidate the independent-term null. There is no additional dynamical
contact for this fixed readout.

Collective background mediation is not a third independent force to add to
(16). It occurs through the source-tagged background histories inside both
connected corrections. Thus (15) retains the possibility that an intervening
medium transmits the source perturbation. It does not assume that only an
identifiable prepared particle can carry an effect to the probe.

Clock corrections must also be retained. If the reference clock is affected,
apply (14) using its FULL response; (16) alone concerns fixed generator age.
A changed clock cannot be assigned to a probe force by redefining a term in
the decomposition.

## A predictive common source test

For each Hermitian probe readout O_a, define the single relational row

    Q_B(x)=[B(x)/beta_B(x)-B(x)^dagger/beta_B(x)^*]/(2i),
    O_hat_a(x)=O_a(x)-[dot o_a(x)/nu(x)]Q_B(x).

Let D_A be the tangent of the actual preparation channel in (8), using the
full qutrit transfer A. With its zero initial clock tangent,

    b_a^Theta=<D_A^dagger O_hat_a(x)>,
    R_av^Theta(x,s)=i*1_(s<x)<[h_v(s),O_hat_a(x)]>.           (17)

The same O_hat is used for the native preparation and complete source
columns. No stationary or thermal replacement is made. Source-dependent
readouts add their contacts; fixed occupation and coherence quadratures
avoid that unnecessary extra dependence. Uniform-lapse columns cancel at
fixed internal phase, retaining their separate work accounting.

Declare a real source space ell_v(s)=sum_mu c_mu f_mu(v,s) independently
of the probe outcomes, and integrate (17) against each f_mu. Stack rows
for occupation and both coherence quadratures over the qualified phase
window in the SAME experiment. Denote the resulting columns by R. A common
source requires

    b=R c.                                                  (18)

Any left-null witness z satisfying R^dagger z=0 must therefore satisfy
z^dagger b=0. A nonzero orthogonal residual, beyond prospectively established
numerical and approximation errors, rejects that declared source space.
An arbitrary space-time profile can make the range full and the test
vacuous; that is not a success. A numerical rank cutoff or error tolerance
must not be selected from a desired outcome. Equation (18) is an exact
criterion, not a completed numerical score.

Compatibility after fitting c to the probe is still not prediction. Suppose
independent source-side rows E fix R_E c=b_E, while withheld probe rows are
R_P c. For a consistent finite source system, its probe prediction is unique
despite null/gauge freedom precisely when

    ker(R_E) is a subset of ker(R_P).                       (19)

If (19) fails, source-side determination is incomplete and the remaining
freedom must not be tuned on the probe. Shared constants across different
densities or preparations do not mean identical fields: the source law
must generate the appropriate profile in each case. Combining different
probe preparations under one c additionally requires a qualified negligible
probe-backreaction regime or an explicit accounting of that backreaction.
Neither is assumed merely because the probe carries a different label.

Equations (15)-(19) advance the next step from a qualitative request for
"one source" to a concrete test of connected phase and transport, with a
source-side identifiability condition. They do not yet provide the missing
physical coarse-graining window or predict a gravitational field.

## A prepared native reference clock beyond the initial interval

The small clock interval of the homogeneous preparation is not the only
available diagnostic. The following is a SEPARATELY DECLARED preparation,
not a repair to its saved results or a claim of naturally formed apparatus.
Isolate one vertex in each layer of the supplied G; the remaining 2N-2
vertices can retain a d-regular bipartite bulk. Initially put no carriers
on the isolated pair and keep the same active content-0 writers and blank
records. Do not delete any potential edge or its native Omega/N flip from
the FULL Hamiltonian. Graph preparation and the clock apparatus are supplied.

In the fixed-G node reference, a chosen isolated clock c remains carrier
empty and its record evolves with h_c^R=epsilon_r*q^r+g_w*X_0. Define

    Delta_c=sqrt(epsilon_r^2+4g_w^2),
    B_c=[(epsilon_r X_0+2g_w Z_0)/Delta_c-iY_0]/2,
    Z_0=|B><B|-|0><0|,    beta_c0=g_w/Delta_c>0.

The operator is embedded in the full qutrit, with zero third-state block.
Exactly [h_c^R,B_c]=Delta_c B_c, and hence

    beta_ref(x)=beta_c0 exp(i Delta_c x).                   (20)

This expectation never vanishes in the reference. The clock's degree and
writer energy constants still belong in H and its source work.

For the full model, apply (1) also to the bounded local operator

    A_c=i[epsilon_r q^r+g_w X_0
                     +g_p sum_s P_psi^s X_s,B_c].

Its reference mean is dot beta_ref. The remaining exact derivative term
-i lambda_R d_c[q^r,B_c] has mean magnitude bounded by
|lambda_R| ||[q^r,B_c]|| N q_1(T)^2, since all clock-incident bits start
blank. Here q_1=sinh(|Omega|T/N), for L=1. Thus uniform amplitude and
derivative errors epsilon_0,epsilon_1 are O_T(1/N) for every fixed T.
Sufficient explicit conditions are

    epsilon_0 <= beta_c0/2,
    epsilon_1+Delta_c epsilon_0 <= beta_c0 Delta_c/4.

They imply |beta_full|>=beta_c0/2 and phase rate nu_full>=Delta_c/2
throughout [0,T]. The ratio beta_full/beta_ref stays in a disk excluding
zero, so the continuously unwrapped phase error is bounded by
arcsin(epsilon_0/beta_c0); inverse phases are controlled on a common interior
endpoint range. This is not merely a positive rate at one initial instant.

Under bounded positive L, replace (20) by
beta_c0 exp[i Delta_c integral_0^x L_c(s)ds], retaining the clock's OWN
lapse. For piecewise smooth schedules use one-sided rates at switches.
An externally clamped clock or changing an age-scheduled protocol into a
phase-scheduled one is a different intervention. Fixed B_c has no explicit
source readout contact.

For this variant the source population in (8)-(10) occupies only the bulk
apart from its initial probe site: replace W by 2N-3 and restrict those
energy sums to the bulk. The frozen isolated clocks contribute constants
with zero initial preparation tangent, not zero absolute energy.

### A slowly growing comparison window

The explicit bound, not just its fixed-T notation, supports a stronger
statement. Put kappa=4 L_max b D>0. Since sinh z<=z cosh z for z>=0,

    E_O,L(T) <= [4 ell |Omega|^2 L_max^3 ||O|| |X|/kappa^3]
      *cosh^2(|Omega| L_max T/N)*exp(kappa T)/N.             (21)

Here integral_0^T s^2 exp[kappa(T-s)]ds<=2 exp(kappa T)/kappa^3.
Fix a positive a with a*kappa<1 BEFORE taking the size limit and set
T_N=a log N in microscopic x units. Equation (21) then vanishes as
O(N^(a*kappa-1)); the direct degree terms in (2) are
O(log^2 N/N+log^4 N/N^2), and the flip-coherence term is O(log N/N).
The same estimates applied to A_c and its wrong-degree term make both
clock errors vanish on this logarithmic window. Equation (20) supplies
the nonvanishing reference amplitude needed to transfer the phase and
rate bounds. The kappa=0 decoupled case is not obtained by dividing by
kappa; (1) can instead be integrated directly there.

This qualifies a growing time window for fixed-support bounded local
expectations and the exact local preparation derivatives, WITHOUT taking a
static response or differentiating the extensive external-source limit.
For source work, average profile total variation times the displayed
energy error must also vanish. The result is conditional on the supplied
bounded-degree family and fixed coefficient bounds. It neither proves a
continuum/local thermodynamic limit on growing spatial regions nor makes a
practical finite-size error small without evaluating its constants.

For the isolated clock alone, reference observables never spread beyond its
one node. Replacing the commutator exponential in (1) by this direct local
count gives E_O,c <=(2/3)ell |Omega|^2 L_max^3 ||O_c||
cosh^2(|Omega|L_max*T/N)*T^3/N, plus the derivative's O(T^2/N)
wrong-degree term. The clock alone therefore admits T_N=o(N^(1/3)) under
this estimate. The generic BULK comparison retains the logarithmic bound;
the stronger clock-only result is not a larger collective-physics window.

Raw incidence changes per vertex still vanish in this window. A collective
effect there must therefore be carried by the retained interacting node
medium or by operational readouts, not asserted macroscopic raw-link
rearrangement. A different time/size limit could behave differently.

Two apparatus obligations are not solved by (20)-(21). Disconnected reference
clocks require owned readout, signal comparison and synchronization. A
periodic finite record does not itself store an unwrapped cycle count.
Extra reading/counter ports can disturb the isolation and must be included
when implemented. The result is a controlled expectation-phase reference,
not unlimited autonomous timekeeping, a naturally formed cosmic clock,
an observational measurement or a change to physical units.

## An exact finite density limit on bare probe coherence

The preceding construction leads to a concrete constraint on a collective
reduction, independent of graph geometry or the short-time expansion. Keep
Q_1=1 and 0<=Q_0<=V-1. For a normalized mode phi, use the SAME matrix
C_uv=<a_1v^dagger a_1u> as above and define

    A_phi=sum_v phi_v^* a_1v,
    phi^dagger C phi=<A_phi^dagger A_phi>.

A_phi maps this sector into Q_1=0. On that target sector exactly

    A_phi A_phi^dagger=sum_v |phi_v|^2(1-p_v^0).             (22)

Creation at one site followed by removal at a different site gives zero
there. Source occupations commute with A_phi. In a definite source
configuration S, the Q_1=1 operator A_phi^dagger A_phi has rank at most one
on the allowed probe positions and its sole possible nonzero eigenvalue is
w_H=sum_(v not in S)|phi_v|^2. Consequently its sharp sector norm is

    ||A_phi^dagger A_phi||=1-sum_(r=1)^Q_0 w_(r),           (23)

where w_(r) are the Q_0 smallest weights |phi_v|^2. The normalized sharp
state has source set S minimizing that sum and probe amplitudes phi_v on
its holes, divided by sqrt(w_H). This is a state-space construction, not
a claim that the native dynamics prepares that state at a chosen age.
Arbitrary record entanglement does not change the operator result.

The same source-configuration blocks give the stronger state-specific bound

    A_phi^dagger A_phi <= 1-sum_v |phi_v|^2 p_v^0,
    phi^dagger C phi <= 1-sum_v |phi_v|^2 <p_v^0>.           (24)

The identity on the right is restricted to the Q_1=1 sector. This retains
actual source marginals for a localized mode rather than treating all
source configurations as equally occupied. It is a kinematic exclusion
bound, not a fitted density response, a phase transition or a quasiparticle
pole residue. Density here is carrier filling, not calibrated physical
mass per volume.

Equivalently C <= diag(1-<p_v^0>) as a matrix inequality. Uniform actual
source marginals rho_0 therefore bound EVERY eigenvalue of C by 1-rho_0,
including localized modes. A pure tagged state can be supported only on
sites with zero source occupation probability. The initially localized
probe in (8) obeys this: its site was explicitly excluded from the source
preparation. No initially mixed-state assumption is needed for the bound.

For an equal-modulus mode on all V nodes, (23) gives the exact ceiling
phi^dagger C phi<=1-rho_0, rho_0=Q_0/V. Thus a replacement by the pure
extended matrix P_phi=|phi><phi| has trace distance

    (1/2)||C-P_phi||_1 >= rho_0.                            (25)

This error does not vanish at fixed nonzero filling. The bound is sharp:
uniformly mix source sets of size Q_0, putting a coherently phased probe
on the holes of each set. Its marginal is exactly

    C=(1-rho_0)P_phi+[rho_0/(V-1)](I-P_phi).

This mixed construction supplies a sharpness example only, with its own
preparation obligations. Pure probe coherence on a common hole subspace
remains allowed; a pure eigenmode must have at least Q_0 zero-weight nodes.
There is no theorem here that every tagged probe must decohere.

The earlier exact one-carrier phase projection allowed distinct conditional
environment states and their overlaps. It is not invalidated by (22)-(25).
What fails is dropping those overlaps and identifying a pure amplitude
vector with the actual bare-probe matrix C in a finite-density background.
An owned purification of the actual mixed state or a dressed collective
probe must retain the background correlations, normalization and complete
source vertex. Calling such a dressing a metric does not supply these terms.

These all-state bounds apply to the full changing-incidence Hamiltonian
whenever its separate carrier numbers are conserved. They do not rely on
transferring a globally extended observable through the local bound (21):
its support grows with V, so that would require a separate estimate.
They constrain an approximate description, not gravity in general.

## Scientific disposition and continuation

The previous proposed comparison of source-density arrival at order x^2
with a lapse-driven density response at higher order is not promoted to a
gravity rejection: it compares transport of source matter with a field
intervention, not an independent gravitational tracer. Equations (8)-(14)
replace that inadequate diagnostic without modifying the native couplings.

The connected separation and predictive common-source criterion are now
available in (15)-(19), with a prepared clock and an explicit logarithmic
comparison window in (20)-(21). Next qualify the SPATIAL coarse description
and source-side dictionary of the retained interacting node medium in that
window, enforcing the actual probe-normalization bounds (22)-(25); a longer
clock is not a derived field. Freeze
the actual graph family, density preparation, clock/readout and source
space before any numerical outcome; do not invent a physical scale or
long-time clock qualification to obtain a favorable result. If the present
finite-time preparation cannot supply the needed collective limit, change
and test that physical premise explicitly rather than repeat local onset
coefficients. Formation and the same-model galaxy/expansion work remain
central, followed by every required Stage 3 lane.

Root derived the initial-energy and finite-density coherence identities and
assembled this continuation.
v005_resume_review independently checked (1)-(3) and (8)-(10), including
the restricted-support qutrit qualification, and checked (22)-(25), including
sharpness and the distinction from a pole-residue calculation. endpoint_equations_check
independently checked (4)-(7), the common-commutant result, and the native
isolated-clock amplitude/derivative comparison (20). Root derived (21) by
the displayed integration of (1); endpoint_equations_check independently
checked its constants and growing-window scope, and supplied the stronger
clock-only local estimate without extending the bulk claim.
handoff_plan_review_v005 derived (11)-(12) and (15)-(19), identified the
independent probe/coherence channel, and challenged the scope of both
putative long-range and no-go claims. Root reconciled the enlarged-path
endpoint restrictions and the preparation/backreaction scope. Review is
internal, not external peer review.
No numerical history, astronomical comparison, fitted constant, tolerance,
release artifact or sealed historical file changed.
