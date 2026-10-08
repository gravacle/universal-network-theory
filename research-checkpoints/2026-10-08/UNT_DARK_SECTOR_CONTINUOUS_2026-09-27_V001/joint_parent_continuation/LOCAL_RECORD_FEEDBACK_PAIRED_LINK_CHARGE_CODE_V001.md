# Paired-link charge code and forward junction constraints: conditional V001

2026-10-05 UTC. NEW bounded microscopic-completion candidate. No pair material,
species charge, binding energy, junction, source law or physical phase is adopted.
No Hamiltonian, state, producer, sampler or six-strain result is rerun. The prior
chi2 constraint remains valid for its ONE-PARTICLE link realization; it is not
a no-go for every faithful incidence code. All failed mechanical/expansion
branches and the charging-only negative directions remain at their old scopes.

## One original bit, two conserved particles

Supply four distinct fermion modes per eligible link, ordered Aup,Adown,Bup,Bdown.
Use the fixed sector N_up=N_down=1 and the two-dimensional endpoint-paired code

    |A>=c_Aup^dagger c_Adown^dagger |vac>,
    |B>=c_Bup^dagger c_Bdown^dagger |vac>,
    W|n=0>=|A>, W|n=1>=|B>, Z=1-2n.

The pair transfer and its complete signed coupling are

    Pplus=c_Bup^dagger c_Bdown^dagger c_Adown c_Aup,
    Hpair=-h(Pplus+Pplus^dagger).                            (1)

With the stated Fock ordering Pplus|A>=|B>, Pplus^dagger|B>=|A>, and the other
two actions vanish. Thus W^dagger Hpair W=-hX with unit matrix elements.
The even quartic transfer preserves each endpoint's fermion parity, the two
spin-species numbers and total link number2. Operators on disjoint mode sets
are even and commute under CAR. The link is encoded ONCE, not by independent
endpoint bits. Distinct record/private-return mode pairs may share the same
electrostatic conductor potential without sharing these fermion modes.

Exact closure requires all single-particle transfer ports and other parity-
breaking interactions to be genuinely absent or forbidden by an owned local
selection rule. Global fermion parity alone does NOT forbid a single hop.
Pair closure is an operator hold, not an energetic proof: paired states can
still lie above split states. Autonomous low-energy selection requires actual
binding, orbital/support and gap data; no favorable pair-binding term is added.

For particles of physical charge e include one actual neutralizing charge -e
at each endpoint. The relative endpoint charges then are

    Q_A=e(n_A-1)=eZ, Q_B=e(n_B-1)=-eZ.                      (2)

The original incidence flip transfers2e from A to B. A single charge-e fermion
in each record/private-return pair has qR=e, so qstar=e and chi=qR/qstar=1.
This is a SAME-SPECIES pairing interpretation of equal charges, rather than
changing the fundamental charge to rescue a result. All neutralizing charges,
particles and complete record content labels remain physical inventory.

## Gauge paths, stored energy and count

For the physical A-to-B path adopt the already declared passive convention
Pplus -> exp[-2ie(chi_B-chi_A)/hbar]Pplus. Its Wilson-dressed transfer is
D=exp[2ie integral_path A.dl/hbar]Pplus. Then

    Hpair=-h(D+D^dagger),
    I_B=(i(2e)(-h)/hbar)(D^dagger-D),
    H_a=-I_B, H_aa=-(2e/hbar)^2 Hpair.                     (3)

At zero path phase I_B=(2e/hbar)hY. The charge-e record transfer instead uses
its own private-return path and content-resolved even bilinear, as in the
pinned private-mode note. Scalar potentials, local Gauss constraints, moving
charges/path contacts and full field momentum remain compulsory. Charge
continuity or quartic parity selection alone does not prove those Ward laws.

Every eligible link has TWO physical fermions even when its incidence is
logically blank. At fixed M eligible links and V vertices the declared link
and private-record codes contain2M+V physical particles, before extra memory,
carrier, material and apparatus inventory. Their rest/chemical/reference
energies cannot disappear when support or count grows. If the complete paired
endpoint energies are E_A,E_B, their compression includes
(E_A+E_B)I/2+(E_A-E_B)Z/2. Endpoint degeneracy must be independently earned
to make this only a fixed-size identity. Double-occupancy binding/self energies,
private-level record costs, backgrounds and mechanical installation are kept
once, not chosen to cancel A_R or change the native copy resonance.

Under the same disclosed five-island circuit the passive floor is

    A_R>=max(lambda^2/(4U),lambda chi/4).

For U=1,lambda=1/2,chi=1 it is A_R>=1/8. A_R=1/8 has C_gp=0;7/40 and1/4 are
strict interior for that inequality. These are admissible conditional branches,
not selected physical parameters. The separate one-particle link with the same
single-record species still has chi2 and A_R>=1/4. The exact charge-normalized
finite-F plate identity in the private-mode note applies wherever each passive
realization exists. No new charge code repairs or reruns the retained charging
shear results, and no pinned or moving clock conclusion is changed by this code.

## Single-hop leakage and controlled virtual pairs

Let Hsp=-J sum_sigma(c_Bsigma^dagger c_Asigma+h.c.) be an actual nonzero
single-hop term. In the fixed two-species sector the split states are
|s1>=c_Aup^dagger c_Bdown^dagger|vac> and
|s2>=c_Adown^dagger c_Bup^dagger|vac>. In the ordering above,

    QHsp|A>=QHsp|B>=J(-|s1>+|s2>),
    PHsp QHsp P=2J^2(I+X), ||QHspP||=2|J|.                (4)

The antisymmetric paired state is dark in this symmetric example, but the
WHOLE two-state code is not invariant for J!=0. If a justified complementary
gap is Gamma, the exact energy-dependent Feshbach self energy has norm at most
4J^2/Gamma within that resolvent domain. Its energy dependence, diagonal shift,
source derivatives, encoder and complementary contacts must all be retained.

Only in the separately declared degenerate-pair/equal-split-gap example,
with both split states at E_pair+Delta and Delta>0, second-order compression is

    Sigma2=-(2J^2/Delta)(I+X).                              (5)

Thus virtual pair hopping h_eff=2J^2/Delta comes with an equally large common
shift. That shift is source- and count-dependent; it is not a removable cosmic
or gravitational identity. Equation(5) is not an all-order replacement for
(4)'s full resolvent or evidence that the native h=.2 is realized microscopically.

## A paired code does not inherit a one-particle strain law

On a frozen orthonormal two-particle orbital manifold, with all fixed-charge
positions homothetically dilated and only nonrelativistic kinetic plus Coulomb
interactions, U_a^dagger Hphys(a)U_a=T/a^2+V_C/a+E_rest I.
The two endpoint Slater words differ in TWO occupied orbitals. Every one-body
operator therefore has zero bare offdiagonal matrix element between them.
An actual two-body Coulomb pair-transfer matrix can be nonzero; if that is the
only direct offdiagonal operator, then in an independently fixed code gauge

    h_direct(a)=h_pair,C/a,
    h_direct'(1)=-h_pair,C, h_direct''(1)=2h_pair,C.        (6)

This holds only for that complete fixed-orbital Coulomb class and an owned
signed pair matrix element. It neither supplies parity isolation nor chooses
its magnitude/sign. Coulomb energy already in the complete capacitance/Gauss
reduction is counted once. Additional pair interaction, orbital relaxation,
magnetic, material and support terms need their own action and contacts.

For a virtual-pair mechanism J(a) may have its own one-body T/a^2+V/a law,
but Delta(a) includes the full split/pair charging, binding and reference
energies. Already at second order,

    h_eff'(a)=4JJ'/Delta-2J^2 Delta'/Delta^2.               (7)

The common shift in(5) is -h_eff and carries -h_eff'(a). One cannot infer these
from h_eff(1), or reuse the earlier ONE-PARTICLE h_T/a^2+h_V/a contacts for a pair.
An unspecified quartic amplitude has no physically derived strain law at all.
Fixed-proper native h on undistorted count replication remains a separate hold.

The next bounded decision is the actual pair-selection mechanism and complete
pair/split energies and geometry, followed by their forward transfer vertices
and direct contacts. For a changing code W(F) keep all W derivatives and the
full Hphys derivatives before any mixed charging/X response contraction.
Native midpoint versus node-owned charging source gradients, private-return
readout, ordinary carrier charge, support/supply and common probe calibration
remain open. This candidate advances an admissible microscopic charge code;
it does not select a universe, positive mechanical branch, force or expansion law.

## Frozen resident ancestry

Paths are relative to joint_parent_continuation except the program paths.
All eleven byte streams were checked before this exclusive note was written.

| Input | SHA256 |
|---|---|
| LOCAL_RECORD_FEEDBACK_CHARGED_JUNCTION_STRAIN_CONSTRAINT_V001.md | d616af4efb0f5c3e4195a93f5cb32e37739a5a63c53841c1a53ce55fc76f584d |
| LOCAL_RECORD_FEEDBACK_PRIVATE_MODE_RETURN_CODE_V001.md | 92dca94c2fe0a3e073bdcc2ba897e423d3f00706c37bc0e66d2e8e1bb8537724 |
| LOCAL_RECORD_FEEDBACK_FIVE_ISLAND_PASSIVE_COMPLETION_V001.md | 124f68b600130afcb3935e11c43c1f939a804892b2794c25f89c29a0892f8693 |
| LOCAL_RECORD_FEEDBACK_COMPLETE_STRAIN_SOURCE_CONTRACT_V001.md | cc363bf1885917a9beededadb8d49b5d898c951bd54a1e2d2ad6ce5003ebaf63 |
| LOCAL_RECORD_FEEDBACK_MAXWELL_LIGHT_SOURCE_CONTRACT_V001.md | accff52211c47cbd92d44f1442a2b3754359ac2f1d02be012008fbeb2965d63e |
| LOCAL_RECORD_FEEDBACK_FLOATING_RETURN_COMPLETION_V001.md | 255ea0ca5f86cc711cae2ff5e746d8e9b005c2156b934818ded7789f9461f2a4 |
| LOCAL_RECORD_FEEDBACK_FLOATING_CAP_COUNT_COMPLETION_V001.md | 97562eae265f43cef842a5cfb125aede1d8edce2b7b6e21a0292634b3d3a21c7 |
| LOCAL_PROPER_BOND_NORMALIZATION_V001.md | 9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b |
| program-worktree/LANE_GRA_GA_F3_Q4_FU09B_ENCODED_CHARGE_CURRENT_LIFT_V001/THEOREM.md | 374168c75f928cdbce55ca790157ba00df2d3a7f2045611d805d1b1b3c090336 |
| program-worktree/MODEL.md | 3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607 |
| program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md | 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec |
