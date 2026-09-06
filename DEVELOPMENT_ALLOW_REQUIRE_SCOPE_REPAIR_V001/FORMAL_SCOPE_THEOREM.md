# Formal scope theorem for `ALLOW`, `REQUIRE`, and `SELECT`

**Packet:** `DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001`  
**Document:** `FORMAL_SCOPE_THEOREM.md`  
**Claim class:** formal definitions and exact finite counterexamples  
**Status:** development theorem; no canonical ledger amendment is made here

## 1. Question and claim boundary

The historical `D-4` rule correctly prevents a fixed carrier's dynamics from
being credited with constructing the state space on which that dynamics was
already defined.  Taken without the words **fixed parent**, however, the rule
is too broad: a larger parent may contain the carrier label or carrier degrees
of freedom as dynamical variables.  Evolution of that larger parent can then
move an occupied state between different effective carrier fibers.

This document supplies the missing scope distinction.  It formalizes the
existing `ALLOW/REQUIRE/SELECT` ladder from
`LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001` and separates five objects that may
not be interchanged:

1. an admissibility predicate;
2. its characteristic projector, after a representation has been chosen;
3. a family of constraint generators;
4. an occupied state; and
5. a dynamical or coarse-graining map.

It does **not** establish a dynamical carrier for the record program, identify
a microscopic gravity algebra, derive a continuum symmetry, or amend any
sealed historical statement.  It states what a future enlarged-parent result
would have to prove.

## 2. Typed objects

### Definition 2.1 -- parent and admissibility

A parent specification `P` consists of all data held fixed while a dynamical
question is asked.  Depending on the model, this can include a carrier,
topology, couplings, boundary conditions, controller, and the state-space
representation.  Let its state space be `X_P` in a classical model or
`H_P` in a quantum model.

An **admissibility predicate** is a map

\[
 A_P:X_P\longrightarrow\{0,1\}.
\]

Its admissible set is

\[
 {\cal A}_P=\{x\in X_P:A_P(x)=1\}.                 \tag{AR01}
\]

In a quantum model the corresponding admissible subspace is denoted
`K_P subset H_P`.  When it is closed, its orthogonal projector is

\[
 \Pi_P=\operatorname{proj}_{K_P}.                   \tag{AR02}
\]

Equation (AR02) is a representation of the predicate after `H_P` and `K_P`
have been supplied.  The words "allowed" or "required" alone do not produce
an operator.

### Definition 2.2 -- constraint generators

A **constraint presentation** of `K_P` is a family of operators
`{C_{P,a}}` for which, after any required eigenvalue shifts,

\[
 K_P=\bigcap_a\ker C_{P,a}.                          \tag{AR03}
\]

The family in (AR03) is extra structure.  It is not determined uniquely by
the subset `K_P`.  Its products, commutators, reducibility relations, boundary
terms, and possible structure coefficients belong to the generator
presentation, not to the truth table of `A_P`.

### Definition 2.3 -- occupancy

An **occupancy** is the actual state.  Classically it is a point
`x_t in A_P` or a probability measure `mu_t` supported on `A_P`.  Quantum
mechanically it is a density operator `rho_t` satisfying

\[
 \rho_t=\Pi_P\rho_t\Pi_P,
 \qquad \rho_t\ge0,
 \qquad \operatorname{Tr}\rho_t=1.                 \tag{AR04}
\]

Occupying one allowed alternative does not make every other alternative
forbidden and does not prove a singleton requirement.

### Definition 2.4 -- fixed-parent dynamics

A fixed-parent dynamics is a family `D_P^t` acting on states of the already
specified parent.  It is **admissibility preserving** when

\[
 D_P^t({\cal A}_P)\subseteq {\cal A}_P              \tag{AR05}
\]

in the classical case, or, in the quantum case, when every state obeying
(AR04) is mapped to another state obeying (AR04).  Unitary, Lindblad, channel,
and discrete update maps are all covered by this definition.

A coarse-graining, conditioning, reconstruction, or effective-description map
is a different typed object, here denoted `E`.  It may associate different
effective state spaces or effective constraints to different parent states;
it is not silently identified with `D_P^t`.

## 3. The `ALLOW/REQUIRE/SELECT` ladder

Let `v:X_P -> V` be a declared property or reporting map.  Its attainable
set on the parent is

\[
 S_P(v)=\{v(x):x\in{\cal A}_P\}.                    \tag{AR06}
\]

The three rungs are:

\[
 \begin{aligned}
 \operatorname{ALLOW}_P(v=a)
 &\Longleftrightarrow a\in S_P(v),\\
 \operatorname{REQUIRE}_P(\phi)
 &\Longleftrightarrow
   \forall x\in{\cal A}_P,\ \phi(x),\\
 \operatorname{SELECT}_{P,D,\mu_0}(v=a)
 &\Longleftrightarrow
   \text{the declared trajectory or limiting law from }\mu_0
   \text{ selects the }v=a\text{ occupancy}.        \tag{AR07}
 \end{aligned}
\]

For completeness, the missing third modal value identified in the earlier
history is

\[
 \operatorname{FORBID}_P(v=a)
 \Longleftrightarrow a\notin S_P(v).                \tag{AR07a}
\]

`FORBID` completes the modal classification of a value relative to one
parent.  Origination is not a fourth truth value on that axis.  It is a
historical proposition about an occupancy or effective fiber at two times and
therefore needs a declared dynamical parent.

For a numerical requirement,

\[
 \operatorname{REQUIRE}_P(v=a_*)
 \Longleftrightarrow S_P(v)=\{a_*\},                \tag{AR08}
\]

provided `A_P` is nonempty.  A selection statement must declare what
"selects" means: finite-time deterministic arrival, an absorbing class,
almost-sure convergence, a unique stationary distribution, spontaneous phase
selection, or another explicit rule.  The bare fact that one state is actual
is occupancy, not a dynamical selection theorem.

The exact logical relations are:

1. `REQUIRE_P(v=a)` implies `ALLOW_P(v=a)` when `A_P` is nonempty.
2. `ALLOW` does not imply `REQUIRE`.
3. An admissibility-preserving `SELECT(v=a)` implies `ALLOW(v=a)`.
4. `SELECT` does not imply `REQUIRE`: alternatives may remain admissible even
   when a particular dynamics attracts every declared initial state to `a`.
5. `REQUIRE` does not supply a parent-selection mechanism.  A singleton
   consistency set can exist without a dynamical account of why that parent
   was realized.

This is the general form of the existing alpha ladder:

- finite recordhood can allow a non-singleton set;
- embedding in one fixed realized sector can require every same-sector record
  to inherit that sector's common value;
- a complete-universe numerical requirement would be a separately proved
  singleton theorem; and
- `SELECT_parent` is an independent dynamical proposition and may not exist.

The host-sector use of `REQUIRE` is therefore not a production operator.  It
is a universal conditional statement inside a parent whose sector is already
fixed.

## 4. Frozen-parent theorem

### Theorem 4.1 -- occupancy evolves; the frozen admissible set does not

Let `P` be fixed, let `A_P` be the predicate supplied as part of `P`, and let
`D_P^t` obey (AR05).  Then for every admissible initial state,

\[
 x_0\in{\cal A}_P
 \quad\Longrightarrow\quad
 x_t=D_P^t(x_0)\in{\cal A}_P,                       \tag{AR09}
\]

while the set appearing on both sides is the same `A_P`.  Quantum
mechanically,

\[
 \rho_0=\Pi_P\rho_0\Pi_P
 \quad\Longrightarrow\quad
 D_P^t(\rho_0)=\Pi_P D_P^t(\rho_0)\Pi_P.            \tag{AR10}
\]

Thus internal dynamics on a frozen parent can change occupancy, correlations,
reachable subsets, and stationary measures without changing the definition of
that parent's admissible space.

**Proof.** Equations (AR09) and (AR10) are exactly the preservation condition
(AR05), iterated or evaluated at `t`.  The predicate and projector carry no
time argument because they are data in the fixed specification `P`.  A rule
that changes them is a family `P(t)`, a dynamics on a larger parent, or an
effective-description map; it is not `D_P^t` as typed above.  QED.

### Corollary 4.2 -- the scoped `D-4` rule

Within a frozen parent, asking `D_P` to construct `A_P` is circular if `D_P`
was already defined as a map on `A_P` or `H_P`.  The legitimate questions are
which admissible occupancy is reached, what invariant or attracting subsets
exist, and what dynamics selects among them.

This corollary does not say that every physically meaningful permission is
fixed at every descriptive level.  It says only that changing the effective
permission requires exhibiting the additional variables or map that owns the
change.

### Exact Example 4.3 -- selection without changed permission

Take

\[
 {\cal A}_P=\{0,1\},\qquad D(0)=0,\qquad D(1)=0.    \tag{AR11}
\]

After one update every initial occupancy is `0`; hence the declared dynamics
selects `0`.  Nevertheless `1` remains in the parent set `A_P`.  The image
`D(A_P)={0}` is a reachable or post-update subset, not a retrospective rewrite
of the original admissibility predicate.  This proves exactly that
`SELECT(0)` need not imply `REQUIRE_P(0)`.

The identity map on the same two-point set proves that `ALLOW(0)` and
`ALLOW(1)` need not supply any selector at all.

## 5. Enlarged-parent theorem

### Definition 5.1 -- carrier fibers

Let `c` range over carrier or parent labels.  An enlarged state space can have
the direct-sum form

\[
 \widetilde H=\bigoplus_{c\in C}H_c,
 \qquad
 \widetilde K=\bigoplus_{c\in C}K_c,
 \qquad
 \widetilde\Pi=\bigoplus_{c\in C}\Pi_c.             \tag{AR12}
\]

The label `c` is dynamical only if the enlarged parent supplies an evolution
with off-diagonal fiber maps

\[
 V_{c'c}:H_c\longrightarrow H_{c'},\qquad c'\ne c. \tag{AR13}
\]

A block-diagonal dynamics preserves every carrier label and does not establish
carrier formation.

### Theorem 5.2 -- effective fiber support may change along an enlarged-parent
history

Suppose `D_tilde` preserves the global admissible space `K_tilde` but contains
a map (AR13) whose restriction to `K_c` is nonzero and which satisfies

\[
 V_{c'c}(K_c)\subseteq K_{c'}.                       \tag{AR14}
\]

Then a history can begin with occupancy in `K_c` and develop nonzero support
in `K_c'`.  Conditional on the `c'` fiber, the applicable effective predicate
is `A_c'`, even though the single global predicate `A_tilde` remains fixed.
Complete transfer from `K_c` to `K_c'` requires the additional condition that,
for some admitted `psi in K_c`, the evolved state is nonzero and lies wholly
in `K_c'`.

**Proof.** Choose `psi in K_c` with `V_{c'c}psi != 0`.  By (AR14), the
transferred component lies in `K_c'`; this proves destination support, not the
absence of residual support in other fibers.  Conditioning on `c'` therefore
uses `A_c'`.  If the additional complete-transfer condition holds, the final
occupancy lies wholly in `K_c'`.  Global preservation follows from
`D_tilde(K_tilde) subset K_tilde`.  There is no contradiction with Theorem
4.1 because the frozen parent in that theorem is now the enlarged parent
`(H_tilde,K_tilde,D_tilde)`, not one isolated fiber.  QED.

### Exact Example 5.3 -- two-fiber carrier transfer

Let

\[
 \widetilde H=\mathbb C^2_c\otimes\mathbb C^2_x,
 \qquad
 \widetilde K=\operatorname{span}\{|0,0\rangle,
                                    |1,1\rangle\}.   \tag{AR15}
\]

Conditioned on `c=0`, the effective internal admissible subspace is
`K_0=span{|0>_x}`; conditioned on `c=1`, it is
`K_1=span{|1>_x}`.  The exact unitary

\[
 U=X_c\otimes X_x                                  \tag{AR16}
\]

preserves `K_tilde` and sends

\[
 |0,0\rangle\longmapsto |1,1\rangle.               \tag{AR17}
\]

The effective internal permission has changed with the occupied carrier
fiber.  Nothing in the fixed `c=0` fiber generated that change; the enlarged
parent owns it through the explicit carrier-flipping operator (AR16).

This example is a type counterexample to the unscoped sentence "dynamics
never changes permissions."  It is not evidence that the record program's
physical parent contains the required fiber variable or coupling.

### Corollary 5.4 -- formation is a lawful enlarged-parent question

The question "does a carrier arise?" is ill-typed only when asked of dynamics
defined after that carrier was frozen.  It becomes well-typed when one gives:

1. a larger state space containing distinguishable carrier fibers;
2. an admissible global subspace;
3. an owned off-diagonal transition between fibers;
4. a before/after occupancy criterion; and
5. complete conservation and boundary accounting for that transition.

Absent these objects, carrier formation remains open rather than prohibited.

## 6. Predicates, projectors, and generators do not share an automatic algebra

### Lemma 6.1 -- common-basis characteristic projectors commute

For Boolean predicates `A` and `B` on one finite configuration set `Omega`,
their characteristic projectors on `ell^2(Omega)` are

\[
 \Pi_A=\sum_{x\in\Omega}A(x)|x\rangle\langle x|,
 \qquad
 \Pi_B=\sum_{x\in\Omega}B(x)|x\rangle\langle x|.    \tag{AR18}
\]

Both are diagonal in the same basis, so

\[
 [\Pi_A,\Pi_B]=0.                                   \tag{AR19}
\]

Equation (AR19) is the Boolean intersection algebra of two predicates.  It
does not establish the commutator algebra of the constraint generators that
present those predicates, and it has no automatic spacetime interpretation.

### Exact Counterexample 6.2 -- one admissible projector, different generator
commutators

On `C^3`, let

\[
 \Pi=\begin{pmatrix}1&0&0\\0&0&0\\0&0&0\end{pmatrix},\quad
 C=\begin{pmatrix}0&0&0\\0&1&0\\0&0&2\end{pmatrix},\quad
 D=\begin{pmatrix}0&0&0\\0&1&1\\0&1&2\end{pmatrix}. \tag{AR20}
\]

The lower two-by-two block of `D` has determinant `1`, hence

\[
 \ker C=\ker D=\operatorname{im}\Pi
 =\operatorname{span}\{(1,0,0)^T\}.                 \tag{AR21}
\]

Both generators therefore encode the same admissible subspace, and both
commute with its projector.  But

\[
 [C,D]=
 \begin{pmatrix}0&0&0\\0&0&-1\\0&1&0\end{pmatrix}
 \ne0.                                              \tag{AR22}
\]

Thus the admissible subset or characteristic projector does not determine a
constraint-generator algebra.  Conversely, replacing a constraint by a
nonzero scalar multiple or another operator with the same kernel changes its
normalization without changing the permission.

### Lemma 6.3 -- noncommuting projectors require non-Boolean representation
data

Projectors such as `|0><0|` and `|+><+|` on a qubit do not commute.  They are
projectors for quantum propositions in different measurement contexts, not
characteristic functions of two subsets of one common classical configuration
basis.  Therefore noncommutation is possible, but it comes from the supplied
operator representation.  It cannot be inferred from the English modal words
`ALLOW` and `REQUIRE`.

## 7. Consequences for the proposed commutator pipeline

The expression

\[
 [O_A,O_B]                                           \tag{AR23}
\]

is undefined until `O_A` and `O_B` are constructed as operators on one common
space with declared domains and normalization.  The following dispositions
are exact.

1. **If `O_A` and `O_B` are the common-basis characteristic projectors of
   admissibility predicates, their commutator is exactly zero by Lemma 6.1.**
   This is a useful null control and a statement about Boolean compatibility.
   It is not Poincare, Virasoro, diffeomorphism, or gravitational closure.
2. **The zero projector commutator does not determine the constraint-generator
   commutator.** Counterexample 6.2 rules out that inference exactly.
3. **The constraint generators do not determine the dynamics without an
   independently supplied Hamiltonian, channel, or action.** Their common
   kernel specifies admissibility, not which occupancy evolves into which.
4. **A commutator between dynamics and a fiber projector has a typed meaning.**
   In an enlarged parent, `[H_tilde,Pi_c] != 0` diagnoses transfer between
   carrier fibers.  It does not by itself violate global admissibility or
   prove that the destination fiber is a physical record carrier.
5. **A scaling exponent cannot be injected into an exact zero to create an
   anomaly.** If `[Pi_{A,L},Pi_{B,L}]=0` for every finite `L`, then every
   scalar rescaling of that same finite operator is still zero.  A nonzero
   central term can arise only from a separately derived limiting generator
   algebra, including its projection, subtraction, normalization, domains,
   and regulator limit.  It cannot be inferred from `z=1`.
6. **If the named spacetime generators have not been constructed, their
   anomaly is undefined, not zero.** This is the direct application of the
   program's zero-of-the-named-object discipline.

A lawful algebraic-scaling screen must consequently keep two families
separate:

\[
 \begin{array}{ll}
 \text{predicate/projector family:}
   &\text{exact Boolean null control},\\[2mm]
 \text{native dynamical family:}
   &H,\ Q,\ \text{translation},\ n_k,\ J_k,
     \text{and any derived local energy/current modes}.
 \end{array}                                         \tag{AR24}
\]

Only the second family can be screened for a native low-energy dynamical
algebra.  Even there, `z=1` is at most a finite-size scaling prerequisite.  It
does not supply Lorentz boosts, stress modes, a central extension, Jacobi
closure, or the limit in which a continuous algebra would have to emerge.

## 8. Repaired scope rule

The formal replacement for the overbroad doctrine is:

> **Within a frozen parent, internal dynamics changes occupancy inside the
> parent's admissible space; it does not change the definition of that
> parent's permissions.  Effective permissions may change along a history
> only when an enlarged parent, external parent family, or explicitly declared
> coarse-graining map contains and owns the variables responsible for the
> change.**

This rule preserves the non-circularity guard: one may not derive a carrier
from dynamics that presupposed that carrier.  It also preserves the collective
question: a larger physical parent may produce different effective carrier
fibers, but the fiber variable, transition, accounting, and reconstruction
must be exhibited.

## 9. Claim classification

**Proved formally in this document**

- Theorem 4.1 for a frozen parent.
- The logical implications and non-implications in the
  `ALLOW/REQUIRE/SELECT` ladder.
- Theorem 5.2's support-transfer statement and the exact complete-transfer
  finite witness (AR15)--(AR17).
- Common-basis projector commutativity.
- The exact same-kernel/noncommuting-generator counterexample
  (AR20)--(AR22).
- The impossibility of manufacturing a nonzero commutator or anomaly by
  scalar-rescaling an exact finite zero.

**Adopted definitions**

- The typed meanings of parent, admissibility, occupancy, selection, and
  effective fiber.
- Admissibility preservation as the boundary of a frozen-parent dynamics.

**Conditional**

- Any application of the enlarged-parent theorem to a physical record carrier;
  this requires the objects listed in Corollary 5.4.
- Any low-energy comparison with a continuous spacetime algebra.

**Open**

- Whether the record program's current physical parent contains dynamical
  carrier variables.
- Whether accumulated records produce state-dependent effective permissions.
- Whether native dynamical generators close on a Poincare, Virasoro, or other
  continuous algebra.
- Any anomaly limit, continuum limit, universal coupling, backreaction,
  macroscopic emergence, or gravity claim.
