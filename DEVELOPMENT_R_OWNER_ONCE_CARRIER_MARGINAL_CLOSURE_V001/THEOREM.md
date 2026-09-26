# Exact carrier-marginal closure of the owner-once accumulation history

Date: 2026-09-22

Status: `CANDIDATE_EXACT_FINITE_THEOREM__PRE_TARGET_AND_HOSTILE_VERIFICATION`

## 1. Scope

Fix one finite parent size `L` and the frozen owner-once accumulation history
defined in the
[`Scalable Relational Accumulation` protocol](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md).
Immediately before zero-based event `n`, the exact prefix-lineage theorem gives

\[
 S\subseteq\{0,\ldots,n-1\}.
\]

The event site `e_n=n` is therefore fresh: `e_n` is absent from every lineage
mask in the input support.  Carrier transport acts as identity on lineage.

This note determines the unconditional reduced dynamics of the carrier
degrees of freedom during that first owner-once pass.  It does not discard or
identify lineage states in the full model.  It asks what remains after the
lineage register is physically unread and mathematically traced out.

## 2. Carrier admission channel

Let `P^0_e=I-n_e` and `P^1_e=n_e` be the projectors onto a blank and occupied
carrier target at site `e`.  Let hard-core creation be

\[
a_e^\dagger|C\rangle=
\begin{cases}
|C\cup\{e\}\rangle,&e\notin C,\\
0,&e\in C.
\end{cases}
\]

For `c=cos(phi)` and `s=sin(phi)`, define

\[
K_{0,e}=P^1_e+cP^0_e,
\qquad
K_{1,e}=-is\,a_e^\dagger P^0_e.                 \tag{1}
\]

They obey

\[
K_{0,e}^\dagger K_{0,e}+K_{1,e}^\dagger K_{1,e}
=P^1_e+(c^2+s^2)P^0_e=I.                        \tag{2}
\]

Consequently

\[
\Phi_e(\sigma)=K_{0,e}\sigma K_{0,e}^\dagger
               +K_{1,e}\sigma K_{1,e}^\dagger          \tag{3}
\]

is a completely positive trace-preserving carrier channel.  The frozen angle
is `phi=pi/4`, so `c=s=1/sqrt(2)`.

## 3. Theorem CMC-1 -- exact carrier-marginal closure

Let `rho_n` be any joint lineage--carrier density operator supported on the
exact prefix block immediately before fresh event `e_n`.  Then

\[
\operatorname{Tr}_S\!\left[
U_A(e_n)\rho_nU_A(e_n)^\dagger
\right]
=
\Phi_{e_n}\!\left(\operatorname{Tr}_S\rho_n\right).
                                                               \tag{4}
\]

If the following carrier transport is `I_S tensor T_n`, the complete reduced
recursion is

\[
\sigma_{n+1}
=T_n\Phi_{e_n}(\sigma_n)T_n^\dagger,
\qquad
\sigma_n=\operatorname{Tr}_S\rho_n.              \tag{5}
\]

Thus a lineage-erased carrier model initialized with the same carrier state
and iterated with the same channels `Phi_(e_n)` and transports `T_n`
reproduces the exact carrier marginal after every admission, at every
intermediate transport time, and after every event of the declared one-pass
history.

### Proof

On the pre-event prefix space define lineage isometries

\[
J_0|S\rangle=|S\rangle,
\qquad
J_1|S\rangle=|S\cup\{e_n\}\rangle.              \tag{6}
\]

Freshness makes their ranges orthogonal:

\[
J_i^\dagger J_j=\delta_{ij}I.                    \tag{7}
\]

The frozen admission unitary restricted to the prefix support is the
isometry

\[
V_n=J_0\otimes K_{0,e_n}+J_1\otimes K_{1,e_n}.   \tag{8}
\]

For an occupied target it leaves `|S,C>` unchanged.  For a blank target it
gives exactly

\[
c|S,C\rangle-is|S\cup\{e_n\},C\cup\{e_n\}\rangle,
                                                               \tag{9}
\]

which is the declared admission law.  Expanding `V_n rho_n V_n^dagger` and
tracing lineage eliminates both cross terms by (7).  The two diagonal terms
are precisely (3) applied to `Tr_S rho_n`, proving (4).  Lineage-blind
transport commutes with the partial trace, proving (5).  Induction from the
common blank initial carrier state proves the complete history statement.
QED.

The proof permits arbitrary correlations or entanglement between old lineage
bits and the carrier state.  Fresh support and future lineage blindness are
the essential facts.

## 4. Direct consequences for the frozen ledgers

At a fresh event,

\[
\Pr(\mathrm{ALLOW})=\operatorname{Tr}(P^0_e\sigma_n),
\qquad
\Pr(\mathrm{blocked})=\operatorname{Tr}(P^1_e\sigma_n),
\qquad
\Pr(\mathrm{reverse})=0,                          \tag{10}
\]

and

\[
W_n=s^2\Pr(\mathrm{ALLOW}).                       \tag{11}
\]

At `phi=pi/4`, (11) is the frozen identity `a_L(n)=2 W_n`.

Every unconditional observable of the form `I_lineage tensor O_carrier` is
reproduced by the reduced channel, including:

- carrier occupations;
- sharp-`q` sector weights and mean carrier density;
- oriented-edge currents and their time integrals;
- the actual and null carrier histories; and
- the actual-minus-null connector-current diagnostic.

The null-admission branch is carrier transport without (3):

\[
\sigma^{\mathrm{null}}_{n+1}=T_n\sigma_nT_n^\dagger.     \tag{12}
\]

The explicit lineage register is therefore a Stinespring record of the
admission outcomes for this one-pass engine.  It retains exact custody and
history information, while unconditional carrier measurements cannot
distinguish that dilation from its reduced channel.

## 5. Exact boundary

CMC-1 does not reconstruct or erase the significance of:

- a selected lineage mask;
- a lineage-conditioned carrier state;
- joint lineage--carrier correlations;
- common-lineage residence or ancestry; or
- canonical lineage encodings and custody digests.

The theorem does not apply after the first revisit, when the cursor or event
schedule depends on lineage, under lineage postselection, or when a future
Hamiltonian or measurement reads a sealed lineage bit.  It is also not an
automatic complexity reduction: an exact density matrix or complete Kraus
ensemble may remain large.

The fair lineage-erased comparator is the same ladder plus (3), not the closed
ladder Hamiltonian by itself.  Comparing the full history only with closed
transport detects the already-declared admission/injection channel; it does
not isolate a lineage effect.

CMC-1 proves no Gate, Record--Geometry Realization Law, alpha statement,
thermodynamic limit, continuum statement, or gravity conclusion.

## 6. Repository scope distinction

CMC-1 applies only to the frozen owner-once accumulation engine.  It must not
be generalized to all record constructions in the repository.  For example,
the separate GL6T construction has an explicit record-sensitive Hamiltonian

\[
H_\star=\sum_a[-hP^K_aX_a+\Delta n_a],            \tag{13}
\]

in which retained-record projectors select future link dynamics.  CMC-1
neither reduces nor refutes that separately constructed finite parent.

The exact follow-up question is whether a proved same-parent composition
identifies the accumulation history's accepted `F_e`/spent-lineage bits with
the `K_a` projectors read by GL6T while preserving all controls.  Without that
composition, importing (13) into the accumulation engine would be a change of
model rather than a consequence of CMC-1.

## 7. Source grounding

- [Fresh owner-once schedule and first-revisit stop](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md#L29-L47)
- [Admission generator and sealed lineage](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md#L49-L68)
- [Actual/null current comparison](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md#L96-L121)
- [Exact prefix support and lineage-blind transport](../DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/PROTOCOL.md#L18-L49)
- [Registered-observable boundary](../DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/PROTOCOL.md#L51-L69)
- [PLB induction and operator intertwining](../DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md#L8-L69)
- [Accepted insertion and owner-once ancestry](../L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md#L78-L95)
- [Seed admission and transport implementation](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py#L95-L184)
- [Streamed admission implementation](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_streamed_history.py#L133-L225)
- [Separate GL6T record-reading theorem](../LANE_CROSS_RFT_GRA_GL6T_F3_LINEAGE_GATED_Q4_E2_RESPONSE_V001/THEOREM.md#L105-L151)
