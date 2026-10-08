# A common native clock and carrier-locality window with active records

2026-10-03. Analytical continuation, no new numerical run or fitted constant.
This supplies a constructive conditional bridge after the connected-state
energy screen. It does NOT supply the preparation of the required graph.

## What changes scientifically

The old carrier-locality theorem assumed blank records and copying off.
The following bound retains local copying, record feedback and their quantum
correlations. It compares full native evolution with a reference that freezes
ONLY the carrier's graph, not the incidence or the record environment.

A separate clock check shows why simply carrying over the old held record
raising phase can fail: at inherited degree two its rate tends to zero.
Keeping the already present writer coupling active instead supplies an exact
local dressed-clock candidate with a nonzero gap, including degree two.
That candidate and the carrier theorem apply to the SAME explicitly prepared
state family. No space dimension, SI ruler, photon or gravity law is inserted.

## 1. Carrier locality with active local copying

Take one original BS slab, one carrier, ports off, initial definite incidence
graph G of maximum degree D independent of N, and carrier initially at v0.
Other node registers may be correlated; arbitrary local BS10 copying and
record feedback are retained. A mixed node state may be purified. Definite
incidence G is a declared preparation, not an outcome of the blank-state run.

Let H0 equal the complete H except that in carrier hopping and current-square
terms n_e is replaced by its initial value n_e(G). The record-feedback term
still contains the ACTUAL incidence operator. In the one-carrier sector,

    H-H0 = sum_e Delta n_e V_e,
    V_e=lambda_J(P_u+P_v)-t T_uv,   c=|lambda_J|+|t|,
    Delta n_e=n_e-n_e(G)=sigma_e Q_e,

where Q_e projects onto bit e differing from G and sigma_e is its fixed sign.
This H0 generally entangles carrier, records and incidence; it is not a
factorized clean-graph propagator.

Only the native flips change incidence bits. The prior selected-bit Dyson
parity argument therefore remains valid, including all local copying:

    ||Q_e1 ... Q_ek U0(s) P_G|| <= q_s^k,
    q_s=sinh(|Omega|s/(N hbar)).

The remaining interaction-picture evolution commutes with each selected bit;
odd insertion count is required to change it. The same statement applies to
the actual H. It is an operator bound, not independence of bit probabilities.

For a carrier set S of size s_S and position projector R_S, only at most s_S*N
edges touch S. Distinct disjoint-edge products V_e V_f vanish. The number
of ordered overlapping pairs is at most s_S*N^2+N*s_S^2, by summing squares
of the degrees in this touching-edge set. With psi_s=U0(s)psi_initial,

    ||(H-H0) R_S psi_s||
       <= c sqrt[s_S N q_s^2+(s_S N^2+N s_S^2)q_s^4].

For each cross term the commuting JOINT projector Q_e Q_f is inserted on
both sides before its probability is bounded by q_s^4. No product of
carrier and incidence expectations is substituted.

Every H0 term except hopping along G commutes with the carrier position
weight exp(mu*dist_G(v,v0)), even when copying entangles the registers.
For the radius-d ball S_d and mu>0, the inherited weighted-norm argument gives

    ||(1-R_d) U0(s)psi_initial|| <= exp(-mu*d+v_mu*s),
    v_mu=|t| D sinh(mu)/hbar.

Unreachable components have zero reference carrier support. In each incidence
block the signed adjacency and signed degree norms are at most N, so
||H-H0||<=cN. Duhamel's identity now yields the full-state bound

    ||[U(T)-U0(T)]psi_initial|| <= E_N(T),
    E_N(T)=(c/hbar) integral_0^T {
       sqrt[s_d N q_s^2+(s_d N^2+N s_d^2)q_s^4]
       + N exp(-mu*d+v_mu*s)} ds.

The reduced-carrier half trace distance and any carrier-event probability
difference are at most min(1,E_N). For fixed D>=2, fixed coefficients and
fixed T, take d=ceil(log(N)/(2log(D))), mu=3log(D). Then s_d=O(sqrt(N)),
E_N=O(N^-1/4); the tail term is O(N^-1/2). For D<=1, the reachable component
has at most two nodes; use it as S with zero tail to obtain O(N^-1/2).
These are conservative fixed-window bounds. Their constants can be large;
the old longer-time window is NOT transferred. A bound above one is uninformative.

This proves operational locality relative to a prepared bounded-degree graph
while the record environment remains active. It is not a strict light cone,
a physical velocity, or evidence that the graph formed under these dynamics.

## 2. Check the old held phase before promoting it

With all copy terms off, take the norm-one fixed-content record observable
A_v=|x><B|. For initial degree d0=d_G(v),

    a_dot=i(omega_v*a - lambda_R <(d_v-d0)A_v>/hbar),
    omega_v=(epsilon_r-lambda_R d0)/hbar.

The same selected-bit bound gives, in the ACTUAL full state,

    <(d_v-d0)^2> <= w_N(t)^2,
    w_N(t)=sqrt[N q_t^2+N(N-1)q_t^4].

Consequently

    |a(t)-a(0)exp(i omega_v t)| <= L_N(t),
    L_N(t)=(lambda_R/hbar) integral_0^t w_N(s) ds,
    |nu_v(t)-omega_v| <= lambda_R*w_N(t)/(hbar*|a(t)|).

For fixed T, L_N=O(N^-1/2). A uniform initial amplitude |a_v,N(0)|>=a_*>0
is required for a uniform rate conclusion; separately nonzero amplitudes
that vanish with N do not suffice. At the inherited epsilon_r=1,lambda_R=1/2,
degree1 has limiting rate+1/2, degree2 rate0, and degree>=3 a negative rate.
A negative oriented phase can still be a clock; it fails only the old fixed
positive-orientation convention. Degree2 lacks a nonzero limiting tick rate.
This is not a claim of exactly zero drift at finite N or of failure of every
possible clock. The saved formed 16D state is not this definite-G preparation.

## 3. Constructive remedy: a continuing-writer dressed clock

Use the SAME prepared G, now records initially blank, all writers fixed in
one occupied content x, one localized carrier, and the existing g_wr=g=1
left on. Carrier-to-record and fragment copying are off for this explicit
clock example; theorem1 permits them but this clock formula does not.
All full incidence dynamics, record feedback and carrier energy remain.
This is a separately declared protocol, not an alteration of the saved
writer-off clock result or a claim that records have become irreversible.

On the invariant record subspace (|B>,|x>), define conventional matrices
Q=diag(0,1), Z=diag(1,-1), X=[[0,1],[1,0]], Y=[[0,-i],[i,0]]. Put

    epsilon_d=epsilon_r-lambda_R d0,
    h_d=epsilon_d Q+gX,
    Delta_d=sqrt(epsilon_d^2+4g^2),   omega_d=Delta_d/hbar,
    B_d={ (epsilon_d X+2g Z)/Delta_d - iY }/2.

B_d is the normalized energy-raising operator: [h_d,B_d]=Delta_d B_d,
||B_d||=1. Extend it by ZERO on the unused qutrit content, not by a full
qutrit identity in the Pauli formula. Its initial amplitude is exactly
beta0=g/Delta_d>0. Its phase convention is fixed by the original real writer
coupling; no time-rotated drive or fitted tick frequency is introduced.

In the actual full Hamiltonian,

    [H,B_d]=Delta_d B_d-lambda_R(d_v-d0)[Q,B_d],
    ||[Q,B_d]||<=1,
    |beta(t)-beta0 exp(i omega_d t)| <= L_N(t),
    |nu_B(t)-omega_d| <= lambda_R*w_N(t)/(hbar*|beta(t)|).

For fixed degree bound D and g!=0, let
b_min=min_(0<=d<=D)|g|/Delta_d>0 and omega_min=min Delta_d/hbar>0.
The explicit sufficient whole-window certificate is

    L_N(T)<b_min,
    lambda_R*w_N(T)/[hbar*(b_min-L_N(T))]<omega_min.

It holds for sufficiently large N at each fixed T. In particular degree2
has beta0=1/2 and omega=2 at inherited units: the old held A zero-gap problem
does not eliminate this different active-writer clock. For any bounded degree,
the same prepared family simultaneously has this clock and theorem1's
active-record carrier locality. No large Hilbert-space simulation is needed
to establish these conditional statements.

B_d is a fixed combination of existing local X,Y,Q readouts using the
DECLARED initial degree d0. Redefining it with the instantaneous degree
would add moving-basis terms. A real clock experiment still needs calibrated
readout ports, disturbance/error accounting and synchronization; a phase
expectation is not automatically a single-shot nondemolition clock.

The readout connection uses the existing writer port, not a newly rotated
drive. A writer modulation delta_g couples to X and has switching work
W_switch=delta_g<X>. Its differential population response is

    delta(d<Q>/dt)=-delta_g<Y>/hbar,
    Re beta=(epsilon_d<X>+2g<Z>)/(2 Delta_d),
    Im beta=-<Y>/2.

Thus the quadratures have an owned population/response construction. Source
calibration, pointer preparation, disturbance and repeated-preparation work
still have to be included in any actual clock measurement.

## Scientific next step, not a completion claim

The connected-state energy bound remains in force. Prepared G carries
nonzero energy/work; the continuing-writer clock does not make that initial
graph appear from blank links. The theorem also leaves three-dimensional
geometry, autonomous source/volume evolution, physical gravity and observed
redshift unproved. Those are independent obligations, not numerical failures
that a larger cell sweep could clear.

The next source comparison should retain this explicit clock, its readout
and the full transport/formation state when applying the already declared A/B
couplings. In particular a universal common rescaling and a differential
transport rescaling are distinguishable only through relational observables
and their complete controller work. Do not prescribe an accelerating q(t).

## Prior work and review

The selected-bit parity and weighted carrier estimate come from
NATIVE_CARRIER_FINITE_TIME_LOCALITY_V001.md; the populated/active extension,
localization argument and clock applications above are the new combination.
The original BS04–11 action, prior phase-clock and active-formation algebra
fix the operators. All original storage/current/degree terms are retained.
The active gap sqrt(epsilon_d^2+4g^2) was already stated in
NATIVE_FINITE_GAP_FORMATION_V001.md. The new clock increment is the accessible
eigenoperator and its full-incidence finite-window certificate, not that gap
or the older clamped-degree formation calculation.

Root independently checked the active Gram/localization proof and derived
the held and dressed clock formulas. Agent handoff_plan_review_v005 supplied
and checked the sharp active Gram count and independently checked the dressed
clock, including its qutrit support and finite-window certificate. Agent
endpoint_equations_check independently verified the held-clock bound and
required the uniform initial-amplitude qualification. This is source-only
agent review, not a new physical observation or an external peer review.
