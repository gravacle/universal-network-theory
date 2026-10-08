# Native formation closure algebra proposed

2026-09-30. Source-only algebra and an exact conditional sector reduction of
the original BS07–11 operators. NOT ADOPTED as a physical completion or a
numerical protocol. No preparation, coefficient, source calibration, worker,
new interaction, or replacement stress is selected here.

The first record-writing coherences do not close on separate carrier and
record density matrices. Their exact derivatives require link–carrier–record
currents, joint writer/carrier content weights, and record–reservoir
coherences. These terms can instead be retained without a memory approximation
in an explicit invariant one-content sector of the original action. This is
an exact embedding, not a proof that its dimension is minimal or scalable.

## Scope and inherited results

Work on one finite BS slab, with constant real coefficients and no active
BS12 ports. Every formula is an operator identity before taking an expectation
in an arbitrary supported state. The Heisenberg convention is
`hbar dot O = i[H,O]`. A noncommuting port adds its actual commutator; it is not
silently discarded from a completed apparatus. Externally changed coefficients
also require their explicit time derivatives and switching-work ledger.

`NATIVE_TEMPORAL_KERNEL.md`, section 1, already derives conservation of total
carrier occupation and content counts, conservation of writer projectors, the
record-production current, and its reversible sign. Its section 2 supplies the
record double-commutator sum rule. Those are premises, not new results here.
`NATIVE_ENERGY_SOURCE_PRESERVATION_V001.md`, equations 3–11, already gives
source leakage and exact source-dependent memory. This note does not rederive
that memory formula. Its contribution is the next explicit formation links
and a formation-inclusive invariant restriction retaining all three BS10 copy
types, rather than one conditional environmental vector per carrier position.

The binary-content idea itself is also inherited.
`RECORD_ADDITION_PROTOCOL.md` keeps two records in a 16-dimensional
same-content block with fixed writers, but explicitly omits carrier-to-record
and reservoir copying. `NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md`, equations
5–6, uses a single-content fragment block for a different channel argument.
The all-register restriction below retains those omitted native copy terms;
it does not claim discovery of the earlier binary restriction.

## Local algebra and the current sign

For any content register, let

    P_B = |B><B|,   P_x = |x><x|,   E_x = |x><B|,
    X_x = E_x + E_x†,
    V_x = i(E_x† − E_x),   Z_x = P_x − P_B,   x = 0,1.

Here `V_x` has the same sign as the target current in
`NATIVE_TEMPORAL_KERNEL.md`, not the opposite conventional Pauli Y in the
ordered binary basis `(B,x)`. For a control `a` and record target `r`, define

    K_a = sum_x P_x^a X_x^r,
    I_a = sum_x P_x^a V_x^r.                              (1)

Thus `K_a` is exactly BS08 and `[K_a,q_r] = −i I_a`. The elementary identities
needed below are

    [q,V_x] = −i X_x,          [q,X_x] = i V_x,
    [P_y,V_x] = −i delta_xy X_x,
    [P_y,X_x] =  i delta_xy V_x,
    i[X_y,V_x] = −M_yx,       i[X_y,X_x] = A_yx,          (2)

where

    M_xx = 2 Z_x,   A_xx = 0,
    M_yx = |y><x| + |x><y|,
    A_yx = i(|y><x| − |x><y|),              y != x.

For example, `[X_y,V_x] = i(|y><x|+|x><y|)` when the two contents differ.
These off-diagonal record-content terms cannot be suppressed in the general
qutrit model merely because its content energies are degenerate.

At node v, put `a = psi_v` or `w_v`, with couplings `g_a = g_psi_r` or `g_wr`.
Let `d_v = sum_(e incident v) n_e` on this slab. The inherited count identities
take the explicit local form

    hbar dot q_v^r = g_psi_r I_psi_v + g_wr I_w_v,
    hbar dot q_vk^b = g_rbk I_(r_v→b_vk).                  (3)

Record-to-reservoir copying leaves q_r unchanged at that instant, but does
not leave the record-writing coherence unchanged. Nor is copying a transfer
of occupation from the control: the control projector is unchanged while
the target occupation changes. Equation (3) is not a monotonic accumulation
law, an energy-per-record assignment, or a SEALED verdict.

Precisely, the inherited conserved operators are
`N_psi,x=sum_v P_x^(psi_v)` for each content x, their sum N_psi, and every
individual writer projector `P_x^(w_v)` (hence every writer occupation).
Their commutators with the ports-off bulk H vanish. Local carrier occupation
can move by (4); record and reservoir occupations generally change by (3).
Conserved writer projectors do not imply constant writer off-diagonal
coherences or absence of writer–target correlations in a larger state.

## The first coherence equations in the full qutrit model

For an oriented edge e:u→v, write the content-resolved BS07 terms as

    S_e,x = E_x^(psi_u)† E_x^(psi_v),
    T_e,x = S_e,x + S_e,x†,
    J_e,x = i(S_e,x − S_e,x†).

Let `sigma_ve` be +1 at the head, −1 at the tail, and zero otherwise. Direct
commutation of `−t n_e T_e` gives

    hbar dot P_x^(psi_v) = t sum_e sigma_ve n_e J_e,x.    (4)

No BS10 copy term changes a carrier control occupation. The BS11 current
square is exactly

    (J_e)^2 = q_u^psi(1−q_v^psi) + (1−q_u^psi)q_v^psi,  (5)

including in the full qutrit space. It is diagonal in carrier occupations,
so it commutes with the local carrier-content projectors in (4).

Define the two hopping contributions

    C_v^V = t sum_(e,x) sigma_ve n_e J_e,x V_x^(r_v),
    C_v^X = t sum_(e,x) sigma_ve n_e J_e,x X_x^(r_v).

All omitted register labels in the next equations refer to the same node v.
For either control a, the full ports-off BS Hamiltonian gives

    hbar dot I_a
      = (epsilon_r − lambda_R d_v) K_a
        − sum_(a',x,y) g_a' P_x^a P_y^a' M_yx^r
        + sum_(k,x) g_rbk P_x^a X_x^r X_x^bk
        + 1_(a=psi_v) C_v^V,                             (6)

    hbar dot K_a
      = −(epsilon_r − lambda_R d_v) I_a
        + sum_(a',x,y) g_a' P_x^a P_y^a' A_yx^r
        − sum_(k,x) g_rbk P_x^a V_x^r X_x^bk
        + 1_(a=psi_v) C_v^X,                             (7)

where `a'` runs over `psi_v,w_v`. For `a'=a`, orthogonality of its content
projectors reduces the second term of (6) to
`−2 g_a sum_x P_x^a Z_x^r`; the corresponding term of (7) is zero.
For distinct controls, both their joint content weights and record-content
coherences remain. All products in the displayed terms have their indicated
tensor-factor ordering; no expectation is factorized.

These equations include every bulk term acting nontrivially on I_a or K_a.
The incidence generator alone commutes with them. Record feedback supplies
the operator detuning `epsilon_r−lambda_R d_v`, not its average. Current-square
feedback commutes directly with them by (5), but this is not an absence of its
later influence: it changes the carrier currents appearing in C_v. For
example, if f joins the tail u of e to a third vertex w,

    i[(J_f)^2, J_e,x] = (1−2q_w^psi) T_e,x;              (8)

the corresponding head-adjacent expression has the opposite sign, and
`[(J_e)^2,J_e,x]=0`. Multiplication by `lambda_J n_f` gives that term's
contribution to `hbar dot J_e,x`. Thus even this feedback produces neighboring
occupation–transport correlations, not a closed one-edge scalar current.

The incidence dependence in (6) also propagates the hierarchy. With
`Y_e^a` the conventional link Pauli Y, BS06 gives
`hbar dot n_e = h_N Y_e^a`. Consequently the exact derivative of `d_v K_a`
contains `h_N sum_(e incident v) Y_e^a K_a` as well as `d_v hbar dot K_a`.
Keeping an average degree while dropping its correlation with the writing
coherence changes this operator equation.

For clarity, the outgoing reservoir current has its own short exact link.
Write `K_rb = sum_x P_x^r X_x^b` and `I_rb = sum_x P_x^r V_x^b` for fragment k.
Then

    hbar dot I_rb
      = epsilon_bk K_rb − 2 g_rbk sum_x P_x^r Z_x^b
        + sum_(a,x) g_a P_x^a V_x^r V_x^b,
    hbar dot K_rb
      = −epsilon_bk I_rb
        + sum_(a,x) g_a P_x^a V_x^r X_x^b.              (9)

Other fragments do not add direct commutators to (9): their control
projectors commute and their targets are distinct. They still affect the
joint state and the writing equations (6)–(7). A finite fragment cannot be
traced out and replaced by a fresh blank while calling these same closed
equations exact.

## What separate marginal states miss

The required joint observables are already visible before any long-time or
large-N limit:

- `P_x^psi V_x^r` and `P_x^w V_x^r` determine the first record-production rate.
- `n_e J_e,x V_x^r` and its X counterpart connect carrier transport to the
  next writing rate.
- `d_v P_x^a X_x^r`, `P_x^psi P_y^w M_yx^r`, and the A counterpart retain
  incidence feedback, competing controls, and cross-content coherence.
- `P_x^a X_x^r X_x^b`, `P_x^a V_x^r X_x^b`, and `P_x^a V_x^r V_x^b` connect
  active formation to the actual finite reservoir.

There is an elementary same-marginal obstruction, not just a missing-variable
count. In a one-content, one-carrier two-node sector, let |L>,|R> be its carrier
positions and |v_+>,|v_-> the eigenstates of V on the left record with
eigenvalues +1,−1. Consider the two admissible diagnostic states

    rho_+ = (|L><L|⊗|v_+><v_+| + |R><R|⊗|v_-><v_-|)/2,
    rho_- = (|L><L|⊗|v_-><v_-| + |R><R|⊗|v_+><v_+|)/2. (10)

All other registers can be the same independent states. Both complete carrier
marginals are `( |L><L|+|R><R| )/2`; both left-record marginals are I/2. But
`<P_L^psi V_L^r> = +1/2` or `−1/2`. Their carrier-induced record rates differ
by `g_psi_r/hbar`. These are a counterexample family, not a proposed mission
preparation or a claim that either has been formed in the project. A fixed
writer contributes the same zero marginal V expectation in this example.
Thus an exact universal closure using only the separate carrier and record
density matrices cannot reproduce even (3) when `g_psi_r != 0`.

## An exact formation inclusive sector

Here is a useful sufficient reduction that retains these correlations instead
of modeling them. It is conditional on support, not a projection chosen after
observing an outcome. Let V be the number of retained nodes and E the number
of their dynamical BS links. Restrict all carriers, records, and K fragments
per node to `{B,0}`; fix each writer in a specified basis state
`w_v ∈ {B,0}`; and retain exactly P carriers in total. Do not specify where
those carriers are, their link/record correlations, or the target preparation.
Every state supported on this sector is allowed at the algebraic level.

All BS07–11 terms preserve this sector. Carrier transfer preserves total P
and content. Copying has no occupied content-1 control on this support and
never changes its own control. The onsite and feedback terms preserve it.
The full Hermitian H therefore has no matrix element between this sector and
its complement. There is no need to turn formation off.

Use binary occupations `p_v=q_v^psi`, `r_v=q_v^r`, `b_vk=q_vk^b`, and denote the
fixed writer occupation by `w_v=0 or 1`. With X_r and X_b the binary target
flip operators, the exact restriction is

    H_sector = H_inc + epsilon_psi P + epsilon_w sum_v w_v
      + epsilon_r sum_v r_v + sum_(v,k) epsilon_bk b_vk
      − t sum_(e:u→v) n_e T_e
      + sum_v (g_psi_r p_v + g_wr w_v) X_rv
      + sum_(v,k) g_rbk r_v X_bvk
      − lambda_R sum_(e:u→v) n_e(r_u+r_v)
      + lambda_J sum_(e:u→v) n_e(p_u+p_v−2p_u p_v).     (11)

H_inc includes the original complete degree penalties and their identity
terms, with `h_N=Omega/N`; no baseline is subtracted. Carrier transfer is the
hard-core binary qutrit restriction, not a fermionic hopping operator with
an inserted sign convention. The writer energy and the carrier onsite
constant are retained. Nonuniform physical source weights must be applied
before reducing an onsite sum to a constant: `sum_v f_v p_v` is not generally
`f P`. Source-dependent identity terms also remain in the energy/source ledger.

This displays the next links particularly simply. Put
`a_v=g_psi_r p_v+g_wr w_v`, `Z_r=2r_v−1`, and use the V sign of (2). Then

    hbar dot r_v = a_v V_rv,
    hbar dot V_rv = (epsilon_r−lambda_R d_v) X_rv
                    −2 a_v Z_rv + sum_k g_rbk X_rv X_bvk,
    hbar dot X_rv = −(epsilon_r−lambda_R d_v) V_rv
                    −sum_k g_rbk V_rv X_bvk,            (12)

and hence, for constant coefficients,

    hbar^2 ddot r_v
      = g_psi_r t sum_e sigma_ve n_e J_e V_rv
        + (epsilon_r−lambda_R d_v) a_v X_rv
        −2 a_v^2 Z_rv + sum_k g_rbk a_v X_rv X_bvk.     (13)

In particular `a_v^2=g_psi_r^2 p_v+g_wr^2 w_v+2g_psi_r g_wr p_v w_v`.
An expectation of (13) is not obtained by substituting separate means.
These equations give the active-record algebra directly within the retained
sector; they do not assert a stationary state, cooling, or positive response.
The separately authored `NATIVE_ACTIVE_FORMATION_ONSET_ROOT_V001.md` studies
the additional conditional blank-target initial family and its short-time
error bounds. That question is distinct from the arbitrary supported-state
identities here; no onset calculation or preparation is repeated in this note.

The exact dimension, before any further symmetry decomposition, is

    dim H_sector = binom(V,P) 2^[E+V(1+K)].              (14)

For a single BS slab, V=2N and E=N^2. The two-node, one-link, one-carrier,
one-fragment-per-node example has dimension 64. It is N=1 in the BS slab
notation, not the previously used N=2, 64-dimensional held incidence/carrier
experiment. No 64-dimensional computation is proposed or executed here.
The dimension remains exponential; (14) is not a thermodynamic scalability
claim. The earlier 16-dimensional two-record block is recovered only after
omitting the reservoir factors and imposing its separately declared copy
restrictions; those were properties of that earlier experiment.

One old simplifying symmetry is explicitly lost rather than assumed. For
two nodes and one carrier, let `Z_c=p_L−p_R`, with conventional carrier
Pauli X_c,Y_c. Keeping carrier-controlled formation gives exactly

    [H_sector,X_c] = i g_psi_r Y_c (X_rL−X_rR).           (14a)

All the other terms of (11) commute with X_c in this two-node sector.
Consequently the previously useful fixed carrier-X bands of writer-only
formation/hold models are not invariant blocks of this full formation
model when `g_psi_r != 0`. This is an operator statement, not a proof that
any particular state mixes, cools, or approaches its ground state.

If a frozen state spans writer basis sectors or both content choices, retain
the necessary sectors and any source/readout-visible coherence between them.
Their weights are not invented. Global content exchange maps the content-0
sector to its content-1 partner, not to itself. A fixed writer pattern may
also break the within-layer permutation group. A further exact decomposition
can use the stabilizer of that pattern and the actual source/port family;
all populated and source-connected irreducible sectors must be retained.
An invariant density matrix need not be supported only on the singlet.
This is an available block decomposition, not a gauge quotient or a promise
that a small block contains a prospectively anchored preparation.

## Source preservation and what is still missing

Let P_sector denote the orthogonal projector of the support just defined,
and Q_sector=1−P_sector. The established invariant restriction gives

    Q_sector H P_sector = 0.                            (15)

For each genuinely specified source insertion F the additional condition is

    Q_sector F P_sector = 0.                            (16)

When a fixed-projector family H(s) is built from the same sector-preserving
native monomials with changed scalar coefficients or spatial weights,
(15) holds at every s. Its first and higher source derivatives then satisfy
(16) as well. The complete restricted source, its identity terms, and its
contacts are obtained by restricting that actual family—not by assigning
record count a new energy. This is why this larger formation-inclusive
embedding can preserve a source exactly while the old one-environment-vector
carrier chart may have QFP nonzero.

A source or port rotating a writer, injecting another carrier/content, or
coupling to a discarded controller need not preserve this sector. Then retain
the source-connected factors/sectors or the already-derived exact memory;
do not replace (16) by a density-source check. A source-dependent choice of
projector introduces its own derivatives/connections. No local lapse, strain
or volume completion is newly chosen by (11)–(16).

For a fixed ports-off slab, complete H_sector energy is conserved, including
copy and correlation energies. Writer occupations are constants but writer
coherences in a larger state can be correlated with the targets. Records and
fragments are not conserved occupations; none is a free resettable bath.
Total unitary entropy is unchanged and reduced correlations must remain.
Changing slabs or externally switching formation requires the original BS05/
BS12 controller/work accounting. The sector proof does not supply it.

The next useful source-only decision is therefore whether an already owned
mission state and complete source family have the support and preservation
properties above. If so, (11) is an exact active-formation representation
ready for a separately specified question. If not, its honest use is to
identify the additional sectors/ports needed. BS section 2.3 still requires
the actual normalized state, source content, blanks, and every crossing
correlation. None is fixed in this proposal, and no initial state is replaced
by a ground state or a selected favorable sector.

This algebra engages the original record/activity fields, but does not close
the physical source, clock, volume, formation-calibration or cosmological
questions. It does not adopt the illustrative battery or single-link strain
proposals, derive vacuum stress, alter an observational gate, or qualify any
of the eleven still-open program lanes.

## Read premise identities

- `../recovered_sources/BS_MICRO_ACTION.md`, BS01–12 and state contract:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
- `NATIVE_TEMPORAL_KERNEL.md`, especially sections 1–3:
  `ad3b095e8a687e76bc7581d79cbb125e92f8b5a61a75e9c8f785a2ebe00fc534`.
- `NATIVE_ENERGY_SOURCE_PRESERVATION_V001.md`, equations 3–11:
  `d0991dd4fd79b77ecb705f384c1b805d9923d132405a384c85168a98f4be1a2e`.
- `RECORD_ADDITION_PROTOCOL.md`:
  `2021e117b74d760cd3d731018cd91f3cba6ef92415beda9d951f9d6a42daff49`.
- `NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md`, equations 5–6:
  `6db32da99d6d346736e193b34b34cb270c242821051296de1be3bf7d86031a39`.
- Separate onset calculation, `NATIVE_ACTIVE_FORMATION_ONSET_ROOT_V001.md`:
  `7edfc2cedb4a74613fd9ae0ddb553c524b5e295447e11df481ca988555045822`.

The displayed closure links and exact restriction were derived by source-only
operator algebra. No numerical matrix construction, import, propagation,
spectrum, or existing producer was executed to create this note.
