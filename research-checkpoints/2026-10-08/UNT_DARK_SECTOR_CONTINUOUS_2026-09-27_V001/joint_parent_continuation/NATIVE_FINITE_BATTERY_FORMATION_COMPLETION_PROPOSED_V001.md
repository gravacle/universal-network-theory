# Finite-battery native completion: one illustrative candidate

Status: **NOT ADOPTED. Source-only proposal; no numerical execution.**

This note specifies one finite Hamiltonian, source family, ruler/volume map,
initial state and preparation duration for every integer N >= 1. It is an
illustrative completion of presently open model inputs, not a derivation from
the BS action, a uniquely preferred realization, or a dark-sector result.
There is no independent microscopic evidence favoring the particular new port
or source law below. Their motivation is narrower: make the missing choices
explicit enough to reject one proposed passive-state formation route without
another source-free spectrum sweep.

In particular, the C_N s^3 identity law below **postulates vacuum-like stress**.
It does not derive, explain away or eliminate dark energy. The batteries are
added degrees of freedom and paid initial resources, not a relabeling of empty
native records. Their cost and this source postulate belong in any eventual
model comparison. All eleven program lanes remain OPEN; no URM, effective
cosmological action, frozen input, release or existing criterion changes here.

## 1. Declared degrees of freedom and reference Hamiltonian

Use the existing two-layer, N-by-N incidence register. For each possible edge
e=(i,j), set n_e=(I-Z_e)/2, sigma_e^+=|1><0|, sigma_e^-=|0><1|, and
X_e=sigma_e^++sigma_e^-. Let d_v be its incident edge count and M=sum_e n_e.
Retain the original node qutrits psi, r, w and one original reservoir b, all
with unique blank |B> and q=|0><0|+|1><1|. This fixes the previously variable
original reservoir count to one per node for this candidate.

Take the native parameter choice d_*=1/2, Delta=0, U>0, Omega>0. Set native
carrier transfer, record feedback and all copy couplings to zero. Give each
of the four original node qutrits the positive onsite gap E_*. Thus

    H_orig = E_* sum_v (q_psi,v + q_r,v + q_w,v + q_b,v),
    C_N = N U/2,
    H_n = C_N I + U sum_v d_v(d_v-1) - (Omega/N) sum_e X_e
          + H_orig.                                             (1)

The constant C_N is exactly the degree-square constant of this tie choice;
it is not subtracted. Equation (1) is the previously studied tie incidence
operator with an explicitly retained, initially invariant native blank sector.
This is not the original numerical benchmark with its other coefficient values.

Add a distinct battery qutrit a_v at every node, with the same blank/occupied
alphabet, and one two-level clock c. Define

    |+>_a = (|0>+|1>)/sqrt(2),  |->_a = (|0>-|1>)/sqrt(2),
    B_v = |B><+|_a,v,          Q_B = sum_v q_a,v,
    H_B = epsilon Q_B,         H_C = E_* |1><1|_c,
    alpha_N = g/sqrt(2N),
    V_p = alpha_N sum_(i,j) [sigma_ij^+(B_Li+B_Rj)
                           +sigma_ij^-(B_Li^dagger+B_Rj^dagger)],
    H_0 = H_n + H_B + H_C + V_p.                                (2)

The new benchmark ratios are fixed prospectively:

    U = Omega = g = epsilon = E_* > 0.                           (3)

The two calibrations E_* and ell_* > 0 are universal constants of this
candidate, not fitted separately for each N or environment. No resonance is
selected from a desired outcome. In particular, an initially isolated edge
costs zero tie diagonal energy while losing one battery occupation costs
epsilon; the proposal does not silently assume a resonant single-edge swap.

Equation (2), rather than an unfilled controller slot, is the complete
Hamiltonian on the declared finite degrees of freedom. There is no additional
wall, drive, reservoir, support energy, switch, reset or unlisted identity
term in this abstract model. It does not assert that a real apparatus can
omit those components: a proposed physical implementation must add and
calibrate any apparatus it actually needs, thereby changing this model.

The port is a new instance of the BS12 interaction slot, not a consequence of
BS10 copying. It is Hermitian and invariant under native node permutations,
layer interchange and simultaneous occupied-content swaps. Its |->_a sector
is dark. The original blank qutrit sector and the battery span{|B>,|+>} are
exact invariant sectors, not numerical truncations. The port satisfies

    [M+Q_B,V_p]=0,

but the original sum X_e term does not conserve M+Q_B. No battery depletion
is therefore identified term by term with the native edge energy or with M.

## 2. One complete source and ruler assignment

For each node write S_v^+=sum_(e incident v) sigma_e^+ and S_v^-=(S_v^+)^dagger.
Fix the complete local allocation

    K_v = U d_v(d_v-1) - Omega/(2N) sum_(e incident v) X_e
          + E_* (q_psi,v+q_r,v+q_w,v+q_b,v) + epsilon q_a,v
          + alpha_N (S_v^+ B_v+S_v^- B_v^dagger) + H_C/(2N),
    K = sum_v K_v = H_0-C_N I.                                 (4)

The port is assigned to its battery endpoint; the native X energy is split
equally over its two endpoints; the clock is allocated uniformly. These
localization choices are extra postulates, not a uniquely determined stress
tensor. They matter for a nonuniform source and are frozen here.

Let s=exp(eta)>0, L>0 and |theta|<1. Set u_L=+1, u_R=-1 and define the whole
source-dependent Hamiltonian, including controller and boundary energies, by

    h_v(s) = (U/4) s^3 I + s^(-1) K_v,
    H(L,theta,s) = sum_v L(1+theta u_v) h_v(s).                   (5)

The candidate domain for bounded source probes is 1/2 <= L,s <= 2 and
|theta| <= 1/2. Equation (5) specifies all derivatives and contact terms in
this source family; no additional c(s)I can be selected later. For example,
at uniform lapse and zero tilt,

    E(s) = s^(-1)K + C_N s^3 I,
    E_,eta = -s^(-1)K + 3 C_N s^3 I,
    E_,etaeta = s^(-1)K + 9 C_N s^3 I,
    H_,Ltheta = sum_v u_v h_v(s).                              (6)

Use an explicitly imposed three-dimensional cell ruler: two rows of N
calibrated cubic cells of side s ell_*, with centers

    r_Li = s ell_* (i-1/2, +1/2, 0),
    r_Ri = s ell_* (i-1/2, -1/2, 0),    i=1,...,N,
    V_phys(N,s) = 2N ell_*^3 s^3.                              (7)

The all-to-all incidence graph is not declared to be the distance metric.
Equation (7) is an externally calibrated ruler assignment, with nonlocal
couplings allowed. It supplies no emergent locality, Lorentz symmetry or
spacetime dimension theorem. If labels are permuted, their ruler assignments
must be permuted with them; no hidden preferred numerical node is selected.

The clock unit is tau_*=hbar/E_* and v_*=ell_*/tau_* is a unit conversion, not
a derived signal speed. To make the source dictionary explicit, an operational
uniform acceleration parameter is defined by theta=a_ext s ell_*/(2 v_*^2).
Identifying it with actual gravitational acceleration or v_* with the measured
speed of light is not established. No full metric/shear or gravitational
field action is supplied by this restricted finite source family.

At the same fixed state, the complete energy-conjugate pressure is

    p = [<s^(-1)K>-3 C_N s^3]/(3 V_phys),
    rho_C = C_N s^3/V_phys = U/(4 ell_*^3),  p_C=-rho_C.          (8)

The second equation is the explicitly inserted vacuum-like component, not a
formation result. The other energy, including every port and clock term,
has the chosen homothetic pressure contribution rho_K/3. Neither pressure
is a relaxed-state derivative or evidence of cosmological acceleration.
The model cannot remove its identity-energy ambiguity by normalized dynamics;
it resolves that ambiguity by a counted new postulate. The old bare tie
dipole is not the full new source: batteries and ports now also contribute.

## 3. One paid, finite-time rule with no release operation

At L=1, theta=0, s=1, prepare exactly the product state

    |Psi_0> = |all edges empty> |all original qutrits B>
              tensor_v |+>_a,v tensor (|0>_c+|1>_c)/sqrt(2).     (9)

Evolve with the already-on, time-independent H_0 for exactly T=tau_*.
The output is the entire joint density matrix at T. There is no turn-on or
turn-off pulse in this rule, no discard from the energy ledger, no postselection,
no dephasing, no Gibbs channel and no ground-state substitution. The clock
is decoupled from the registers except through the common source assignment;
its reference phase advances by one radian at T. This is a stipulated finite
readout convention, not a physical timing device whose precision/backreaction
has been derived. Computing the unmeasured state at T is not a free physical
measurement or a battery recharge.

The initial resources are explicit:

    <H_0>_0 = C_N + 2N epsilon + E_*/2,
    <V_p>_0 = <sum_e X_e>_0 = 0,
    S(total)_0=0,  Q_B(0)=2N.                                  (10)

The occupied |+> states require prepared purity and an internal alignment;
they are energy eigenstates of H_B, not a hidden coherent superposition of
empty and charged battery energies. The clock does require energy coherence.
The original native blank is itself not assumed to be a ground state of H_n.
The total initial pure-state ergotropy, if arbitrary global operations were
available, is <H_0>_0-E_min(H_0), fixed by this Hamiltonian, not merely 2N epsilon.
No work or entropy cost for producing (9) from a thermal source is claimed
to be zero. It is the paid initial resource; repeating the protocol requires
fresh resources or a separately accounted restoration operation.

During the fixed-source evolution the exact ledger is

    Delta<H_n> + Delta<H_B> + Delta<H_C> + Delta<V_p> = 0,
    Delta<H_C> = 0.                                             (11)

Loss of epsilon Q_B is not, by itself, the deposited edge energy. Correlation
and interaction energy can have either sign and are retained. If sources are
instead externally varied, the corresponding additional work is
integral dt <partial_t H(L,theta,s)>; no such variation occurs in (9)--(11).
No actual strain actuator is invoked and then omitted from this formation
experiment. Real source actuation would need its own accounted apparatus.

The global unitary keeps total von Neumann entropy zero. In the invariant
sector the clock remains a pure product, so

    S(native edges)=S(batteries) <= 2N ln(2),
    I(edges:batteries)=2 S(native edges).                        (12)

These are resource identities/bounds, not a claim that the output is thermal.
All correlations remain part of the output. A finite closed system supplies
no generic irreversible attractor. Nothing here guarantees a passive reduced
native state at the chosen time; that is a prospective rejection question.
Even instantaneous native passivity would not release the native subsystem
from the still-active ports or justify its replacement by the old ground state.

## 4. What is already provable, and what is not

This normalization does not make ||V_p|| uniformly extensive. Suitable
coherent, densely occupied product states can give an O(g N^(3/2)) port
expectation. The relevant stability statement is instead a lower bound on
the complete reference energy. Write m=<M> and x=m/N. Operator Cauchy and
S_v^+S_v^- <= N d_v give

    |<V_p>| <= 2 sqrt(2) g sqrt(N m),
    sum_v <d_v(d_v-1)> >= 2m^2/N-2m,
    <H_0>/N >= U/2+2U x^2-2U x-Omega-2sqrt(2)g sqrt(x).         (13)

All parameters here are positive and H_orig, H_B and H_C are nonnegative.
The scalar right side is bounded below and coercive for U>0. Thus the model
is stable from below with an N-independent lower energy-density constant,
and fixed reference energy density bounds the mean degree. This is not a
bound on the full interaction norm, an all-N state-preparation theorem, or
a uniform source-response estimate. The displayed bound is at the reference
source; no unproved numerical source-domain constant is claimed.

At each fixed N, orthogonal native-flip and battery-hole channels give the
initial expansion

    <M(t)> = (Omega^2+N g^2)(t/hbar)^2+O_N(t^4).                 (14)

Reality of H_0 and the initial basis state in the active battery basis makes
this expectation even in t. The remainder is not uniform in N. Equation (14)
therefore does not prove a nonzero degree at any N-independent finite age.
The known empty-state speed bound applied to the old Hamiltonian cannot be
reused after adding V_p; the new incidence-changing port is precisely a new
premise. Conversely, simply seeing a nonzero short-time population would be
an automatic, uninformative test of the new exchange term.

## 5. One fixed rejection calculation, specified before outcomes

Propose exactly one calculation after separate root adoption and source
review: N=2, the ratios (3), and T=hbar/E_*. No parameter scan, time scan,
resonance fit, new preparation, port-off rerun or added bath is included.
The original blank qutrits and decoupled clock factor out exactly. The active
edge/battery Hilbert dimension is 2^4 times 2^4 = 256; the native reduced
matrix has dimension 16.

The question is whether this finite paid rule overcomes the inherited degree
limitation while satisfying a necessary condition for passive native-state
preparation. The old empty-state bound at this same N and time is
`<M>/N <= (Omega T/hbar)^2/N = 1/2`. The candidate must therefore certify a
mean degree strictly above 1/2, not merely a positive formation probability.
This uses equation (3) of `NATIVE_EMPTY_EDGE_DENSITY_TIME_BOUND_V001.md`
and its cited primary incidence-speed theorem: the flip coefficient remains
h=Omega/N=E_*/2, not h=E_*; the original preparation has M=0; and all the
old diagonal/onsite terms commute with M. The bound is independent of U and
the coefficient branch, so no positive-cost-branch bound is being imported
into the tie. The new incidence-changing V_p violates that theorem's old
commutator premise; diagonal feedback or BS10 copying alone would not do so.
At the same output, any certified nonzero entry of [rho_n(T),H_n] rejects
native passivity. Noncommutation is a sufficient rejection witness for a
finite-dimensional passive state, without guessing a desired ground vector.

The reference criterion concerns a Hamiltonian with cyclic work potentials
vanishing at their endpoints: passivity requires both commutation and ordered
energy populations. See Allahverdyan, Balian and Nieuwenhuizen,
[Maximal work extraction from quantum systems](https://arxiv.org/pdf/cond-mat/0401574),
equations (2), (6)--(8) and the intervening stationarity argument. Here V_p
remains live. Thus this screen concerns only the mathematical pair
(rho_n,H_n), a necessary native-reference preparation condition. It is not a
whole-apparatus work/passivity witness or a credit for extractable work after
free decoupling. Any actual operation must retain its change to V_p and all
other energy in (11).

Use one prospectively fixed exact-rational action polynomial, not a fitted
floating-point tolerance. In units E_*=hbar=1, all active N=2 matrix entries
are rational and

    ||H_active|| = ||(H_0-H_C)|_active|| <= 1+8+2+4+4 = 19,
    P = sum_(k=0)^128 (-i H_active)^k/k! |Psi_0,active>,
    delta = (130/111) 19^129/129!,
    ||P-Psi(T)||_2 <= delta,
    gamma = 2 delta+delta^2.                                   (15)

The bound follows from the exponential tail with subsequent term ratio at
most 19/130. The five norm contributions are the retained identity, degree
penalty, native flips, batteries and port. In this logical battery basis the
initial vector is a basis vector, so no unowned square-root approximation is
needed. Form sigma_n=Tr_B |P><P| without normalizing P to hide its error.
Then ||sigma_n-rho_n||_1 <= gamma. Consequently

    |Tr(M sigma_n)/2 - <M>/2| <= 2 gamma,
    |[sigma_n,H_n]_(a,b)-[rho_n,H_n]_(a,b)| <= 22 gamma.         (16)

Here the restriction of H_n to the invariant native blank-qutrit sector has
norm <=11; this is not its norm on excited original qutrit sectors. Compare
rational real and imaginary components separately.
The fixed 16-by-16 commutator census is lexicographic in the declared edge
bit order (11,12,21,22); retain the first certified witness and the maximum,
not a retrospectively chosen time or observable. Also retain trace, the
complete energy ledger (11), battery occupation, native degree and port
energy with bounds derived from the same delta; they are consistency evidence,
not additional physical fitting criteria.

Disposition is fixed:

- A degree upper enclosure <=1/2 rejects the specified density objective.
- Any commutator real or imaginary component whose magnitude exceeds
  22 gamma rejects its native-reference passive-state formation target at T.
- A degree interval straddling 1/2 or an unresolved commutator is INCONCLUSIVE,
  not permission to increase precision, alter T or infer exact passivity.
- Even a degree lower enclosure >1/2 and no resolved commutator witness mean
  only that this rejection screen did not reject. They do not certify exact
  commutation, population ordering, passivity, autonomous release or a ground
  state. No positive physical or URM qualification follows.

The test is deliberately a falsifier, not a general passivity certificate.
If it rejects, do not repair the claim by tracing away interaction energy,
switching off V_p for free, projecting onto the ground or searching other
times. A changed mechanism would require a distinct candidate and reason.

Prospective finite caps: one root-owned worker, 30/35 seconds soft/hard CPU,
45 seconds wall time, 256 MiB RSS, one thread, 4 MiB output; at most 128
Hamiltonian-vector products on dimension 256, one reduced matrix, one
16-by-16 commutator census, and 8,192 bits per stored rational numerator or
denominator. Resource or exact-arithmetic overflow yields retained failure
or partial evidence, never a truncated success. No child/source implementation
or execution authority is created by this note; a fixed implementation and
its guards must be independently reviewed before root decides to run it.

## 6. Explicit postulate and calibration count

The existing operators/action supply the edge register, degree penalty,
native flips, qutrit alphabet, initial-state obligation and a place to specify
Hermitian boundary ports. They do not supply the choices below. This candidate
adds eight declared modeling choices, plus two independent unit calibrations:

1. The particular tie/decoupling choice and positive onsite gaps in (1).
2. One added battery qutrit per node and one finite coherent clock.
3. The exchange port, 1/sqrt(2N) scaling and benchmark ratios (2)--(3).
4. The complete local energy allocation (4).
5. The whole source law (5), including its vacuum-like identity component.
6. The imposed cubic-cell ruler, volume and acceleration dictionary (7).
7. The paid, uncorrelated pure initial state (9).
8. The single fixed observation duration T=tau_*, with no release operation.

E_* and ell_* are the two calibrations. The fixed finite rejection design is
a testing choice, not a further physical law. There is no independent evidence
that these choices describe actual matter, gravity, a cosmological environment
or the single-link strain device in the earlier proposal. This candidate does
not inherit that proposal's exponential deformation or unspecified actuator.

A result from the one finite test can decide whether to discard this proposed
passive-formation route. It cannot establish large-N fixed-age formation,
physical volume from incidence, a passive stationary universe, cold dark
matter, MOND, dark energy, a continuum gravitational action or observational
agreement. The separate conditional CMB program is neither blocked nor
promoted by this illustrative native candidate.

## Source custody and review scope

Paths below are relative to this note's directory J. These are read premises,
not outcome files for this new proposal:

| Source | SHA-256 |
| --- | --- |
| `../recovered_sources/BS_MICRO_ACTION.md` | `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec` |
| `NATIVE_TIE_PHYSICAL_CLOSURE_DECISION_V001.md` | `fc8d274d7c4cde4ad196e2068993e9a9dc76b0844b47c7b8c3d7531421d35114` |
| `NATIVE_SINGLE_LINK_STRAIN_COMPLETION_PROPOSAL_V001.md` | `10ac410adb17d0f14650b3ad64db232300489cfab0c9bd09bda1468ac7d1f3bd` |
| `NATIVE_OPERATIONAL_SOURCE_CLOCK_VOLUME_CANDIDATES_V001.md` | `fbddff9520f898bf888600ac62a03729d25b7cf4ad230196b04505f81853304b` |
| `NATIVE_EMPTY_EDGE_DENSITY_TIME_BOUND_V001.md` | `148fe4cd60b740fa7daa5d06f99907e92d027449c248b7bbb6df6856533ccc7e` |
| `NATIVE_DEGREE_TIE_FULL_PARENT_ODD_RESPONSE_V001.md` | `ac17bd126aa2f05032b674180b36caa72faa6164879aa3ab8b9960e57b86a815` |

The reference lower bound (13) was separately challenged by
short_path_adversarial using hand algebra. That limited check is not an
independent review of this whole completion or its proposed finite test.
No new coefficient/rate evaluation, Hamiltonian construction, solver import,
worker, runtime test, physical measurement or source-response result is claimed.
