# Finite density probe dynamics and the memory a collective model must retain

2026-10-03 UTC. Continuation of frontier V116. The actual mixed source
preparation already rules out an exact closed Hermitian evolution of the
bare tagged probe. A local two-site witness makes this a size-independent
finite-time result, not just an uncontrolled Taylor coefficient. An exact
mixed conditional-state reduction retains the missing dynamics and supplies
a state-weighted error bound. Neither result establishes a gravitational
force or rules out an effective geometry acting on an interacting medium.

No numerical worker, new coupling, fitted tolerance or replacement
preparation is used. The parent remains the illustrative BS action, with
active qutrit records, content-0 writers, fragments off and separately
conserved source and tagged-carrier numbers. Its identification with native
UNT rules, formation of the supplied graph, physical rulers and volume,
absolute expansion work and astronomical predictions remain open.

## The exact probe equation does not close on its one body matrix

Use x=tau/hbar, a_sv=|B><s| on the carrier, p_v=p_v^0+p_v^1,
b_v=|B><B| and Q_1=1. In the bounded-degree fixed-G node reference put

    tau_uv=t A_uv (L_u+L_v)/2,
    e_u=L_u(epsilon_psi+j d_u),
    U_uw=-j A_uw(L_u+L_w),
    O_uv=a_1v^dagger a_1u,       C_uv=<O_uv>,
    R_u^s=[a_1u,a_su^dagger]=delta_s1 b_u-|s><1|_u.

C is positive with trace one. The node generator, including all
carrier-dependent current energy, is

    H_node[L]=sum_v L_v { (epsilon_psi+j d_v)p_v
       +(epsilon_r-lambda_R d_v)q_v^r
       +g_w X_0v+g_p(p_v^0 X_0v+p_v^1 X_1v) }
       -sum_edges {t (L_u+L_v)T_uv/2
                    +j(L_u+L_v)p_u p_v} + E_scalar[L].       (1)

Fixed-G graph and writer identity terms do not affect C but remain part
of the complete energy and source work. The comparison reference also
has a separate evolving incidence Hamiltonian: its work is NOT replaced
by E_scalar in this node equation. No such energy is deleted from H[L].
For u!=v,

    i dC_uv/dx =
       -sum_(w,s) tau_uw <a_1v^dagger R_u^s a_sw>
       +sum_(w,s) tau_vw <a_sw^dagger R_v^(s dagger) a_1u>
       +(e_u-e_v)C_uv
       +sum_(w!=u,v)(U_uw-U_vw)<p_w^0 O_uv>
       +g_p<O_uv(L_u X_1u-L_v X_1v)>.                       (2)

The edge uv pair interaction vanishes on both endpoint configurations
connected by O_uv; it has not been dropped from the Hamiltonian. At other
vertices p_w O_uv=p_w^0 O_uv in the one-tag sector. The Hubbard factors
R retain vacancy blocking and cross-content coherences. Replacing them
by an identity is not a finite-density derivation. Writer copying, storage
and feedback commute directly with O_uv but drive the joint quantities in
(2). Differentiating those quantities generates a hierarchy, not an
established finite closure on C alone.

The diagonal identity is especially simple and exact:

    dC_uu/dx=2 sum_v tau_uv Im C_uv.                         (3)

The sign is checked by a single tag on a two-site edge: initially at u,
C_uv=-i cos(t x)sin(t x) for equal onsite energies, so C_uu decreases.

## A local finite time failure of a pure probe replacement

Use the preparation already specified in V116: a tag initially at w,
uniform fixed-Q_0 source mixture on W eligible sites, definite G and blank
records. All d neighbors of w considered here are eligible. Put rho=Q_0/W.
The isolated-clock variant uses W=2N-3. The unmodified homogeneous variant
uses W=V-1. Let u be an occupied-G neighbor of w and B_u=1-p_u^0 on the
initial source sector. Exactly,

    <B_u>=1-rho,
    min_c <(B_u-c)^dagger(B_u-c)>=rho(1-rho).                (4)

A tag hop therefore has coherent amplitude t(1-rho) but squared
transition amplitude t^2(1-rho), not t^2(1-rho)^2. This is conditional
vacancy variance, not an additional mass or gravitational coupling.
First-hop expansion gives

    C_uu=t^2(1-rho)x^2+O_N(x^4),
    C_wu=-i t(1-rho)x+O_N(x^2),
    m_wu=C_ww C_uu-|C_wu|^2
         =a x^2+O_N(x^4),       a=t^2 rho(1-rho).            (5)

The last remainder is even for the real Hamiltonian and real initial
state. Source hopping, active recording and incidence flips do not alter
the leading coefficient: their first-order terms keep the tag at w and
cancel from this conditional-variance coefficient. A definite source
configuration has no such initial classical vacancy variance. This is a
result for the declared mixed preparation, not a density-only universal law.

The reference remainder can be bounded uniformly in network size. Write
the autonomous node Hamiltonian as sum_Z h_Z with |Z|<=2 and define

    J=sup_v sum_(Z containing v)||h_Z||.

Constant terms can be omitted for this commutator bound, but not for work.
One conservative bound, at L=1 and maximum graph degree D, is

    J <= |epsilon_psi|+|epsilon_r|+|lambda_R|D
                       +|g_w|+|g_p|+D(|t|+|j|).

For an observable on m sites the connected commutator expansion proves

    ||ad_H^k O_X|| <= (2J)^k (m)_k ||O_X||,                 (6)

where (m)_k=m(m+1)...(m+k-1). Each commutator adds at most one site;
the sum of interaction norms touching that support is at most its size
times J. Unitary conjugation makes the derivative bound valid at every
age. Leibniz gives fourth-derivative bounds 120(2J)^4 for C_ww C_uu
and 840(2J)^4 for |C_wu|^2. Taylor's theorem therefore gives

    |m_wu(x)-a x^2| <= 640 J^4 x^4,
    x^2 <= a/(1280 J^4)  =>  m_wu(x)>=a x^2/2.             (7)

This is a conservative but nonzero size-independent interval when t!=0
and rho stays away from zero and one. No fourth-order coefficient is fit.
It uses bounded-degree NODE interactions; J is not asserted uniformly
bounded for the full incidence Hamiltonian.

For any trace-one positive C, its two-site minor obeys

    m_wu <= (1-Tr C^2)/2 <= 1-lambda_max(C),
    min_(pure P) (1/2)||C-P||_1=1-lambda_max(C).             (8)

Every bare Hermitian probe evolution from the initially pure localized
tag remains pure, even with an arbitrarily fitted time-dependent h.
Equations (7)-(8) give a nonvanishing finite-time error against ALL such
replacements. This does not depend on reconstructing a growing global C.

Transfer to the full dynamic-incidence parent uses V116's local comparison,
not a new global norm assumption. If the three relevant entry errors are
epsilon_ww, epsilon_uu, epsilon_wu, then

    |m_full-m_ref| <= epsilon_ww+epsilon_uu+2 epsilon_wu.     (9)

These errors vanish at fixed x as N grows. Thus the strictly positive
reference bound survives in the full parent for sufficiently large N at
fixed interior filling and a fixed positive x in (7). At equal actual
clock phase, add the qualified phase-inversion/time-alignment error from
V116; the entries have bounded reference derivatives by (6). This error
also vanishes at fixed phase. A microscopic-time comparison must not be
silently labeled an equal-clock comparison.

For context, the full neighbor covariance is

    Gamma_uv=t^2 rho(1-rho)
                   [delta_uv-(1-delta_uv)/(W-1)].            (10)

Its trace gamma=d t^2 rho(1-rho) gives
lambda_max(C)=1-gamma x^2+O_N(x^4) and
Tr C^2=1-2 gamma x^2+O_N(x^4). The uniform finite-window claim here rests
on the LOCAL witness (7)-(9), not an unproved global remainder for (10).

## The exact amount a Hermitian commutator cannot explain

At a usable internal phase write D_C=dC/dTheta and C=sum_lambda lambda P_lambda.
For every Hermitian h, the residual D_C+i[h,C] has the same spectral-block
diagonal

    J_C(D_C)=sum_lambda P_lambda D_C P_lambda.

Pinching is contractive in trace and Hilbert-Schmidt norms; all off-block
entries can be canceled by

    P_lambda h_* P_mu=i P_lambda D_C P_mu/(mu-lambda),
                                               lambda!=mu.

Consequently

    min_(h=h^dagger)||D_C+i[h,C]||_(1 or HS)
                         =||J_C(D_C)||_(1 or HS).           (11)

Keep entire degenerate eigenspaces. Commuting blocks of h are undetermined,
and near-degenerate inversion can be ill-conditioned. This is a diagnostic
reconstruction, not a predictive local Hamiltonian or gravitational field.
It does not identify the remainder with irreversible noise: reversible
correlations and memory in the globally unitary state suffice.

For any prospectively declared h_eff and residual R_Theta,

    (1/2)||C(Theta)-U_eff C(0)U_eff^dagger||_1
                   <= (1/2) integral_0^Theta ||R_s||_1 ds.   (12)

The derivative is at the same actual clock. Constant spectrum is necessary
for exact bare Hermitian closure, but not sufficient for locality, a
complete source vertex, or predictions without fitting the probe.

## An exact mixed conditional reduction that keeps the background

The old pure one-carrier construction is not directly applicable to the
current mixture. Embed the physical one-tag sector in tag position times
the source/record/link environment. The tag-v component is supported only
where p_v^0=0. This is an embedding with constraints, not an added species
state. Write the actual aged density operator in blocks rho_uv. Bare
coherence is C_uv=Tr_environment rho_uv, with both endpoint vacancy
constraints already in these blocks.

Let P_v project onto supp(rho_vv), choose an isometry W_v onto that
support, and put W=direct_sum_v W_v, P=WW^dagger, Q=1-P. Positivity implies
P rho P=rho: a kernel vector of any diagonal block is annihilated by the
whole positive operator. The retained mixed blocks and readout are

    R_uv=W_u^dagger rho_uv W_v,
    C_uv=Tr[W_v^dagger W_u R_uv].                           (13)

The overlaps W_v^dagger W_u must stay. The hopping block of K=W^dagger H W
is -t W_u^dagger n_uv W_v (or its complete spatial-source weight).
Its rectangular matrix replaces a scalar hopping amplitude. All onsite,
record, current and absolute baseline terms also remain in K.

The preparation tangent from V116 obeys -rho<=delta rho<=rho initially
and after common unitary aging. Hence P delta rho P=delta rho and this
mixed support contains that source-preparation tangent exactly. A source
history changing the evolution before the chosen age can instead rotate
the support; it requires its initial complementary forcing or a qualified
new chart. Do not assume the same inclusion for arbitrary interventions.

H in this support construction can be the full parent or a declared node
reference; using the latter still needs its separate comparison error.
Freeze this projection at a declared matching age. For constant H set
B=QHW, H_Q=QHQ, V_P(x)=W^dagger exp(-iHx)W and
V_Q(x)=Q exp(-iHx)W. They obey

    i dV_P/dx=K V_P-i integral_0^x B^dagger
                       exp[-iH_Q(x-s)]B V_P(s) ds,
    V_Q(x)=-i integral_0^x exp[-iH_Q(x-s)]B V_P(s) ds.        (14)

The exact full density is (W V_P+V_Q)R_0(W V_P+V_Q)^dagger.
An arbitrary probe readout must retain its P-Q cross and Q-Q terms.
Using only V_P R_0 V_P^dagger would discard escaped amplitude and can
lose normalization. Equation (14) is a constructive memory description,
not evidence that the memory is small.

Duhamel gives a state-weighted error certificate for dropping it:

    epsilon_rho(T)=integral_0^T
                ||B exp(-iKs) sqrt(R_0)||_HS ds,
    (1/2)||rho_exact(T)-W exp(-iKT)R_0 exp(iKT)W^dagger||_1
                      <= min(1,epsilon_rho(T)).             (15)

The proof compares normalized density amplitudes in Hilbert-Schmidt norm;
it does not require the norm of the full extensive H. Apply the bound
separately to normalized positive and negative parts of a preparation
tangent, with their trace weights, to control its response. A fixed
observable then has absolute error at most 2||O||epsilon_rho.

Under H[L]=sum L_v h_v, the same complete h_v fixes K, B and H_Q source
vertices. Differentiating the memory includes BOTH B endpoints and the
complementary propagator. A moving W adds its connection, readout changes
and boundary terms. A guessed onsite potential is not this source.

Explicitly, for a fixed retained frame and declared source direction
V_mu(s)=sum_v f_mu,v(s) h_v, put B_mu(s)=Q V_mu(s)W and
V_mu,Q=Q V_mu Q. The first variation of the memory B^dagger U_Q(t,s)B is

    B_mu(t)^dagger U_Q(t,s)B+B^dagger U_Q(t,s)B_mu(s)
      -i integral_s^t B^dagger U_Q(t,u)V_mu,Q(u)U_Q(u,s)B du.

This derivative is fixed by the original energy source, not an adjustable
extra response. It is needed even when a fitted projected K alone appears
to reproduce a baseline probe trajectory.

Support rank can be combinatorial: the initial uniform source mixture has
rank binom(W,Q_0), and unitary evolution preserves this global rank.
An exact isometry carrying the entire state cannot have smaller dimension.
Thus (13)-(15) solve the correct mixed-state formulation and its error
accounting, not yet the useful few-field collective reduction. An
observable-only or dressed reduction can still be much smaller, but its
neglected correlations and readout must be justified rather than erased.

## A finite interval restriction on a common energy source

The complete source changes hopping as well as onsite energy. Linearizing
(3) at L=1, with L=1+epsilon ell, gives

    delta dC_uu/dx=2t sum_v A_uv Im delta C_uv
              +t sum_v A_uv(ell_u+ell_v)Im C_uv.             (16)

The last term is a mandatory current-source contact. At common phase the
left side becomes nu*d(delta C_uu|Theta)/dTheta plus
(delta nu|Theta)*dC_uu/dTheta. Omitting that clock response is also invalid.

With V116's isolated native clock, native matter preparation leaves its
reference rate Delta_c unchanged, while a lapse gives Delta_c L_c.
Matching the SAME exterior occupations AND coherences over a common phase
interval necessarily requires, even at finite source,

    sum_v A_uv[(L_u+L_v)/(2L_c)-1]Im C_uv(Theta)=0           (17)

at every measured u and age. Compare source values at the corresponding
source-history age. A spatially uniform lapse is relationally invisible.
On a bipartite graph L_u=L_c+s eta_u is another exact edge-average null;
it need not be invisible in the off-diagonal equation (2). Current zeros,
cycles and partial exterior observation can produce further nulls. No
generic full-rank assumption or uniform-lapse conclusion is made here.

There is an exact test for the remaining STATIC profile ambiguity. Orient
the edges and let D_U be the signed edge-incidence matrix restricted to the
actually measured vertices U. Set (S ell)_uv=ell_u+ell_v with
ell_v=L_v-L_c, and I_e(Theta)=Im C_tail(e),head(e)(Theta). On a nonzero
phase interval J_phase define the positive matrix

    G_phase=integral_(J_phase) diag(I) D_U^T D_U diag(I) dTheta.

The continuity constraints force every edge average to equal L_c precisely
when ker(G_phase) intersect im(S)={0}. For a declared profile basis F,
replace im(S) by im(SF). This follows because the quadratic form is the
integral of ||D_U diag(I) S ell||^2. Full rank of G_phase is sufficient
but stronger than needed. Nonzero current on every edge is NOT sufficient
on a cyclic graph. Missing interior measurements must not be supplied as
extra rows. Complete filling, where all currents vanish, is an exact
counterexample to any automatic identifiability assertion.

Even when this condition holds, each connected bipartite component retains
its own staggered freedom L_v=L_c+s eta_v; isolated vertices are not
constrained. Positivity bounds s. Equation (2) and the source/record readouts
must decide these directions. No numerical rank or physical-field fit has
been performed or claimed here.

This necessary condition operates over the whole interval, not only at
the source onset. Its domain is the declared microscopic C dictionary.
A justified dressed readout or additional spatial geometry can have
different contacts; failure of (17) would reject this dictionary, not
gravity or UNT in general. The full parent adds the already bounded local
incidence corrections, and derivative statements require their actual
joint current readouts rather than differentiating expectation bounds.

## Scientific disposition and next calculation

The finite-density background cannot be replaced by a pure bare probe with
averaged hopping at vanishing error in the declared preparation. This is
a substantive restriction on the prospective collective model. It is not
an argument for a record halo, a MOND derivation or a claim that any form
of memory must be gravitational.

The surviving common-source test must compare TWO interacting, memory-
retaining descriptions on the same preparation and clock. Use complete
source-side energy response to fix a restricted source family before
withheld probe data; retain V116's condition ker(R_E) subset ker(R_P).
Apply (17) to remove incompatible static source directions and use (2)
to test directions left invisible by occupation continuity. Do not fit
an arbitrary h_* from C and call that a predicted metric. A reduced local
field requires a specified retained observable/dressing map and a small
error such as (15), not only exact formal projection identities.

The present construction has not supplied the required physical spatial
coarse window, source formation law or few-field reduction. These remain
the next decisive obligations before additional galaxy/expansion fitting.
No new astronomical score is claimed; all eleven dark-program lanes remain
open and both CMB investigations remain distinct.

## Evidence and review

Parent definitions: recovered_sources/BS_MICRO_ACTION.md, BS07 through
BS11, SHA256 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec.
Preceding state, source and clock:
NATIVE_SPATIAL_MATTER_SOURCE_CORRESPONDENCE_V001.md,
SHA256 6d626c6d9716aae6b951da7efecd0d8fe56f29c250b0575c9282dec63843ff6a.
Earlier exact pure-state projection:
NATIVE_COLLECTIVE_CARRIER_PHASE_CANDIDATE_V001.md,
SHA256 f3dad63532285add3f890b0c15e9fad4c4968226904e66cf43e6e110966eb6fa.

Root derived the local finite-window strengthening and checked the density
amplitude bound. Existing nonerrored reviewers v005_resume_review,
endpoint_equations_check and handoff_plan_review_v005 independently checked
the vacancy/spectral algebra, complete probe/source equations, and mixed
support/memory construction respectively. Review is internal mathematical
review, not outside peer review or observational confirmation. No
usage-errored agent was restarted or replaced.
