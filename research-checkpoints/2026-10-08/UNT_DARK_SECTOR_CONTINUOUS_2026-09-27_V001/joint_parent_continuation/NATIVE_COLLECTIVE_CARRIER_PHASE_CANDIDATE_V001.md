# An exact carrier/link phase candidate, with its conditional-state memory

2026-09-29. Analytical Stage 1 continuation. No numerical producer, new
preparation, coefficient fit, replacement of a saved state or frozen-file edit.

## Result

There is a minimal exact alternative to calling the held record phase the
transported hard phase: use carrier-number phase together with its conditional
link/record state. Its canonical normalization, hopping coefficients, source
work and absolute energy are already fixed by the native Hamiltonian and actual
state. An exact same-state projection supplies a finite phase-amplitude model
PLUS a determined memory kernel; it does not require a guessed stabilizing
coefficient or a phase-aligned replacement state.

By contrast, a symmetry-preserving reduction of the held, copying-off local
record charges cannot give their own twists a nonzero transport stiffness.
The surviving carrier/link route has a precise remaining question: whether
its actual conditional-state memory admits a common controlled collective
phase reduction, with the same temporal and spatial source response. Alpha
would then be a measurable/matchable ratio, not a symmetry identity.

## 1. The held-record obstruction is exact and narrow

With the stated copying and noncommuting ports off, each retained native
record occupation q_v^r commutes with H. Thus for independent phases phi_v,

    U_r=exp(i sum_v phi_v q_v^r),
    U_r H U_r^dagger=H,
    Tr[U_r rho U_r^dagger H]=Tr[rho H].                 (1)

The energy, first current and every static phase derivative vanish along
this source orbit for ANY density matrix, including a record-coherent one.
A record-raising amplitude can nevertheless rotate under the held onsite
energy. That local temporal phase is not a proof of spatial transport.

Suppose an exact retained isometry W intertwines this symmetry,
U_r W=W U_r,ret. Its compression satisfies

    [W^dagger H W,U_r,ret]=0.                           (2)

An exactly eliminated complementary sector must retain the same Ward null.
Consequently a positive gradient energy assigned to the SAME local-record
twists cannot appear merely by a symmetry-respecting change of variables.
A truncation that freezes a non-invariant conditional state and discards its
response can lose this null; that is an approximation to test, not a derived
record stiffness. Activating copying/ports, changing the physical charge, or
specifying a symmetry-breaking preparation is a different owned experiment.
Equation (1) does not forbid a transported carrier phase or an interacting
collective mode involving more than these conserved local record charges.

## 2. Exact factorization of an actual one-carrier state

In the invariant held one-carrier sector write the Hilbert space as carrier
vertices times all retained link/record variables. The complete Hamiltonian is

    H=sum_v |v><v| tensor H_v
              -t_hop sum_e n_e tensor(A_e+A_e^dagger),
    A_e=|v><u|,
    H_v=H_environment+epsilon_psi I
                        +lambda_J sum_(e incident v) n_e.       (3)

H_environment includes the incidence flips, degree energy and every retained
held record term, including record feedback. There is no mean-link closure.
The current-square term in (3) is compulsory, as derived from BS07/09/11.

For a pure actual state, factor its carrier components wherever P_v>0:

    |Psi>=sum_v sqrt(P_v) exp(-i theta_v)|v>|chi_v>,
    <chi_v|chi_v>=1, sum_v P_v=1.                       (4)

This is an identity, not carrier/environment factorization: the chi_v can
be different and entangled with the carrier. The saved coherent native
vectors allow it without dephasing. For a mixed state the full density-matrix
response must be retained or an explicitly owned purification/ensemble used;
an arbitrary decomposition is not a new measured phase.

Define

    a_v=i<chi_v|chi_v_dot>,
    E_v=<chi_v|H_v|chi_v>,
    c_e=<chi_v|n_e|chi_u> for e:u->v.

Up to the vanishing total normalization derivative, the exact native action is

    L=hbar sum_v P_v(theta_v_dot+a_v)-E,
    E=sum_v P_v E_v
        -2t_hop sum_e sqrt(P_u P_v)
                     Re[exp(i(theta_v-theta_u))*c_e].   (5)

Variation of the complete variables, with their normalization constraints,
is equivalent to the original Schrödinger equation. The canonical charge
conjugate to theta_v is hbar*P_v, not record count, node count or an assumed
unbounded oscillator action. The common phase is redundant at fixed total
carrier number. At P_v=0 the phase chart is undefined; use the original
vector or another chart, rather than assign it an artificial phase.

The redundancy

    theta_v->theta_v+lambda_v,
    chi_v->exp(i lambda_v)chi_v

leaves (4)-(5) invariant: a_v->a_v-lambda_v_dot and
c_e->exp[i(lambda_u-lambda_v)]c_e. Therefore the invariant phase differences
include the conditional-state connection. Removing a_v or replacing c_e
by <n_e> omits a genuine part of the same-state dynamics. This redundancy
does not impose a spacetime boost symmetry or determine a propagation speed.

In particular

    <n_e A_e>=sqrt(P_u P_v) exp[i(theta_v-theta_u)] c_e.

The current, work and phase Hessian derived from (5) are exactly the previously
qualified joint native quantities, including their possible signed curvature.
They are not products of separate link and carrier averages. Link history and
records enter through chi_v, its connection and its source response, while
the transported phase is canonically carrier-number phase.

## 3. A same-state reduced model and its exact missing term

At an already owned age w, choose the conditional chi_v from THAT actual
vector. Let S be its occupied carrier support and define the fixed isometry

    W_w |v>=|v>|chi_v(w)> for v in S,
    P=W_w W_w^dagger, Q=1-P.

Then P|Psi_w>=|Psi_w> exactly. No arbitrary state is assigned to an empty
carrier vertex: its later arrival belongs to Q until a new chart is needed.
Every carrier onsite source sum V_v P_v and every carrier-number phase twist
preserves this retained subspace at its initial time. Thus all these initial
source directions are represented exactly, not merely one chosen readout.
Arbitrary retained coefficients form a phase/amplitude chart; this does not
claim that onsite phase sources alone prepare arbitrary carrier populations.

Its native compression has matrix entries

    (H_P)_vv=E_v(w),
    (H_P)_vu=-t_hop <chi_v(w)|n_e|chi_u(w)>              (6)

on a possible edge, with every diagonal baseline retained. This is an explicit
minimal candidate Hamiltonian, not a claim that its subspace is invariant.
Let L_Q=Q H W_w. The exact projected initial-value equation is

    i hbar phi_dot(t)=H_P phi(t)
       -(i/hbar) integral_w^t L_Q^dagger
           exp[-i QHQ (t-s)/hbar] L_Q phi(s) ds,        (7)

with phi(w)=W_w^dagger Psi_w. The otherwise present initial-Q forcing is
exactly zero by construction. Equation (7) retains all the eliminated
conditional-state response. It is a causal initial-value memory equation,
not an assertion that a single local Hermitian phase action already suffices.

The independent resolvent form is

    G_P(z)=[z-H_P-Sigma(z)]^(-1),
    Sigma(z)=L_Q^dagger(z-QHQ)^(-1)L_Q.                 (8)

For a real E0 outside the complementary spectrum,

    Sigma'(E0)=-L_Q^dagger(E0-QHQ)^(-2)L_Q,
    M_ret=1-Sigma'(E0) >= 1.                           (9)

Thus even a legitimate local spectral expansion has a retained normalization
from omitted amplitude, not only a changed hopping. The derivative expansion
requires a stated distance from the complementary poles and bounded higher
terms. M_ret is a first-order Schrödinger spectral normalization; it is not
automatically the positive-hardening fluid's mechanical mass or e_II.

Without a spectral approximation there is still a finite-window control:

    ||Psi(t)-W_w exp[-i H_P(t-w)/hbar]phi(w)||
                     <=min(2, ||L_Q||*|t-w|/hbar).     (10)

It follows by Duhamel comparison with PHP+QHQ. This is an absolute state
error, not a relative bound for a tiny transport probability. An actual
projection calculation must retain its measured leakage/poles; it may not
freeze chi_v merely because that produces an attractive phase model.

For nonzero/time-dependent sources, source dependence of H_P, L_Q and QHQ
must all be differentiated or evolved. Keeping only the explicit contact in
(6) would omit the current response and can break the pure-gauge null. A
time-dependent choice of retained W also needs its own Berry connection.
These terms are determined by the chosen native state and source; no free
alpha has been inserted by this reduction.

## 4. Which common-phase coefficient is an output?

If one controlled collective reduction of (5)-(8) admits a local phase/action
description with positive e_II, its temporal and spatial quadratic coefficients
must be extracted from the SAME state, source quotient and frequency window.
For the conditional hard phase they would have to satisfy

    K_time=C beta/e_II,
    K_space=C beta*alpha*I/omega,
    K_space/K_time=alpha*I*e_II/omega=alpha*cI2.         (11)

The exact native number normalization fixes the phase/source conjugacy.
A shared phase rescaling changes both coefficients together, not the ratio.
But chemical-potential sources V_v P_v are not automatically gravitational
lapse/strain sources: the latter vary all relevant energy terms and contacts.
The source/work map, proper time and spatial metric/volume calibration still
have to identify the two physical experiments before (11) is alpha in a
relativistic action. A graph derivative and microscopic boundary tau alone
produce only a graph/clock response ratio.

Native charge continuity enforces the full Ward relation. It does not fix
e_II, the memory poles, the spatial Hessian or physical units separately.
Allowed changes of t_hop preserve the native U(1), content and permutation
symmetries while changing spatial phase energy without changing the Berry
coefficient hbar. No admissible coarse-graining can turn that freedom into
a universal coefficient-one theorem without an additional physical symmetry,
state/limit selection or source calibration.

For a fully specified native Hamiltonian, state, retained map and physical
dictionary, alpha is nevertheless not arbitrary: the combined response fixes
it or rejects the proposed local hard-phase description. The exact held
single-link affine incidence action, with e_II=0 and finite capacity, cannot
be divided into (11) and relabeled a positive-quartic phase fluid. An interacting
carrier/link collective limit is the surviving route, rather than that
single-link substitution.

## 5. Absolute energy and volume do not follow from phase transport alone

Equation (5) keeps the complete native energy. At the matching age its
compression (6) has exactly the same expectation, not a new chosen band zero.
Under a physical source lambda and a varying retained isometry,

    partial_lambda H_P = W^dagger H_lambda W
                 +W_lambda^dagger H W+W^dagger H W_lambda. (12)

Connections, complementary memory, source work and boundary/creation terms
cannot be discarded when a physical volume variation changes the retained
space. A coarse-graining is not itself node creation or volume expansion.

There is a sharp remaining identifiability limit: adding c(V_phys) times the
identity leaves every normalized fixed-volume phase/current response unchanged,
but changes volume work by c'(V_phys). Therefore even a successful complete
temporal/spatial transport match cannot determine absolute vacuum stress from
that channel alone. The existing controller/volume-source or creation-plus-
independent-volume ledger is the distinct observable that resolves it. It
must use the same state and count its energy once.

This is the constructive endpoint, not a larger simulation queue: the exact
candidate (5) provides an owned collective carrier/link phase; (7)-(10) say
precisely when replacing its conditional-state dynamics by a local phase law
is controlled; (11)-(12) specify the joint source and energy match. No new
finite run is needed to establish these identities, and no favorable
preparation, stabilizing coefficient or physical metric has been assumed.

## Read-source identities

* `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
* `NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md`:
  `6e9cc504ae81841c55d73c84f91239ce407e84455f11efc10a32ed8724d4b45a`.
* `NATIVE_CARRIER_RULER_PATHWAY_V001.md`:
  `4277871cd49f7e45169f3fd7db0b5d49b9b66651f6b4ac257d794a5230254db8`.
* `NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md`:
  `335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c`.
* `NATIVE_SOURCE_BRIDGE_DECISION.md`:
  `c82040f7bebbdefcec4e782f8afb86c6c1c3f2367775f5fd2e6dbbe6159c737a`.
* `NATIVE_VOLUME_INCREMENT_PATHWAY.md`:
  `c60b04d6584bf12b7db9ce5b52815c0010aeb13fe0a2a86324cbedd929cf4c6a`.

These are mathematical and source identities, not an observational validation
of the newly identified conditional collective route.
