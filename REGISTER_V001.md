# WHERE ATOMS COME FROM — REGISTER V001

**PURPOSE.** Indexed by QUESTION, phrased the way someone would re-ask it. Before opening any
line of work, search this file for the question first.

Every row carries: the question as it would naturally be re-asked · the ruling · **where the
proof is** · and **the exact condition under which the row reopens**. A row with no reopen
condition is closed permanently.

**APPEND-ONLY.** Rows are never edited, only superseded by a later row citing the earlier one.
**This register adopts nothing and derives nothing.** It records where rulings live.

**POINTER RULE (custody §1):** no term appears in a row without a digest, a `file:line`, or a
named ruling behind it.

---

## HOW TO USE THIS REGISTER

Search by the question you are about to ask. If it is here, read the row and its reopen
condition before commissioning anything.

---

## W-01 — CAN A FORMATION CONDITION BE WRITTEN ON K1'S OWN DATA, WITHOUT A STIPULATED SPLIT? (S2; construction pair, build + adversarial audit. **AUDIT REFUTED THE BUILD AND WROTE THE CONDITION THE BUILD DECLARED UNWRITABLE.**)

**RULING: YES — WITH ZERO ADDITION AND NO IMPORTED SPLIT.**

**THE CONSTRUCTION.** Extend loop transport from a single fibre to the section space
`Gamma(L) = C^5` that the build itself derived:

```
(M_gamma s)(v) = W(gamma) · s(v)   for v on the loop
(M_gamma s)(v) = s(v)              otherwise
```

These are **unitary and non-scalar** on `Gamma(L)`. Then

```
<M_dF s, M_c s> = conj(W_F)·W_C·p_0  +  conj(W_F)·(p_1+p_2)  +  W_C·(p_3+p_4)
```

which vanishes **iff 0 lies in the convex hull of three unit-modulus coefficients** — verified
against brute-force simplex minimisation, 1369 grid points, 0 mismatches.

**IT FIRES ON S1'S OWN PUBLISHED CONNECTION.** With `W_F = -1`, `W_C = -i` (S1 §6) and
`p = (1/2, 0, 0, 1/4, 1/4)`, the overlap is `i/2 - i/2 = 0` **exactly**.

**PROPERTIES, ALL CHECKED:** gauge-invariant · correct trivial limit (no formation at
`W_F = W_C = 1`) · **the root can never fire**, independently reproduced · and it
**distinguishes curvature from flat holonomy**, which K1 exists to separate and which the
build's own rival construction could not see (its self-reported defect F1).

**THE ONLY LOAD-BEARING OBSTRUCTION IS DURABILITY.** Over `n` circuits the condition fires —
`0.0247` at `n = 42` — and then **recurs to `0.99994`**. K1 is finite and closed; this is a
**reversible write, not a durable record**, reproduced from first principles on five vertices
rather than inherited.

**WHAT THE BUILD CLAIMED, AND WHY IT WAS WRONG.** It returned a threefold impossibility —
rank, no time, no split. **Two are false and one is overstated.** Its rank theorem was proved
on `L_v0 = C`, an alternative its **own choice ledger had rejected**, and then applied to the
`Gamma(L) = C^5` it had chosen; `|<s, M_dF s>| = 0` on K1's own connection refutes it directly.
Its no-split theorem — resting on `dim = 5` being prime — is refuted: reduced states exist
(the build computed one), a canonical three-way direct-sum split exists, and `C^4 = C^2 (x) C^2`
on the non-root subspace. Only a weaker structural half survives: no *canonical* factorisation.
Its no-time claim is overstated — **circuit count is carrier-supplied discrete time.**
And its "minimum addition" question dissolves: **zero addition suffices.**

**A RESULT INSIDE THE CORRECTIONS THAT MATTERS ON ITS OWN.** A canonical three-way split
**exists on K1 and is derivable from its incidence** — `{v0} / {v1,v2} / {v3,v4}`: the root, the
filled triangle's other vertices, the unfilled triangle's other vertices. The
source/record/environment *shape* the predecessor introduced by imperative is **available here
without being imposed.**

**WHERE THE PROOF IS.** Build `S2_FORMATION_CONDITION_ON_K1_V001.md`
sha256 `248ce856efaef157c68e818dde589d0200bbc1dd9fd9fc1fcc8cdc7bc88734d9`.
Audit `S2_FORMATION_CONDITION_ON_K1_AUDIT_V001.md`
sha256 `0bea11bd4b7764f65c8d44cc8812d43bdcc569d34f51d0c46d82851a2efbd0d5`.
All 16 of the build's file:line pointers resolve; all 5 digests verify at bytes; alpha not
engaged. Numeric corrections carried: the build's §3.4 table is non-reproducible and its
corrected row values are `0.000000 / 0.816497 / 0.816497 / 1.000000`; the recurrence figure
`0.994373` is a window artefact and the true supremum is at least `0.999793`.

**GRADE: ADVERSARIALLY-CHECKED, NOT INDEPENDENTLY-CORROBORATED.** Build and audit share a model
lineage (custody §4). A failure mode common to that lineage passes through both.

**REOPENS IF:** a lineage-independent lane fails to reproduce the firing on S1's connection ·
the convex-hull criterion fails on a carrier where it should hold · or the three-way split's
derivability is shown to depend on K1's particular vertex count rather than on its incidence.

---

## W-02 — DOES A DIRECTED SYSTEM OVER K1 ESCAPE RECURRENCE, AND DOES IT PRODUCE THE NINE? (S3; construction pair. **AUDIT CONFIRMED-WITH-CORRECTIONS — every computable claim reproduced in a fresh independent implementation, no arithmetic error found anywhere.**)

**RULING: THE CROSSING EXISTS. THE LIMIT ESCAPES. SEVEN OF THE NINE HOLD OUTRIGHT; TWO HOLD IN THE LIMIT AND FAIL AT EVERY FINITE STAGE — WHICH IS WHY THE PREDECESSOR RECORDED ONE OF THEM FALSE.**

**THE SYSTEM.** `A_N = M_5(C) (x) M_2(C)^(x)N`, dimension `25·4^N`, embeddings
`iota_N(X) = X (x) I_2` — verified unital, multiplicative, *-preserving and isometric — with
`A_infinity = UHF(5·2^inf)`: simple, unital, infinite-dimensional. **Cost: one qubit per cell,
proved minimal. This is not zero addition.** The record slot is non-abelian by necessity: a
unitary write onto a reset carrier leaves *pure* slot states, and pure states of an abelian
algebra have overlap only 0 or 1.

**THE TRAP WAS REAL AND IS DISARMED BY COMPUTATION.** Repeated circuits of one loop span
**3 dimensions at N=1 and 3 at N=100.** Circuits grow no algebra and escape nothing.

**THE MECHANISM IS NOT WHAT IT LOOKS LIKE, AND THE AUDIT'S CORRECTION IS THE FINDING.**
The escape is **not** "recurrence is gone" — **the carrier's recurrence is untouched**,
`sup |Z_k| = 1`. It is **"the record grew."** And the monotonicity theorem carrying the escape
is a **tautology of any per-cell tensor system**: it holds identically on families that never
form at all. **All the content sits in the divergence `Sum (1 - z_n) = inf`.**

**AND THE ESCAPE IS CONDITIONAL IN TWO WAYS, NOT ONE.** The build flagged the **cell schedule**
— an adversarial schedule locked to the carrier's near-recurrences defeats the crossing
entirely. The audit found the second, flagged nowhere: **the support of the ready state.**

**THE CRITERION, CORRECTED AND PROVED, VERIFIED 10/10 ACROSS ALL FOUR SUPPORT CLASSES.**
With `u = conj(W_F)`, `v = W_C`, characters `chi_0 = uv`, `chi_F = u`, `chi_C = v`,
support `S = supp(p)`, and `G = <chi_a/chi_b : a,b in S>`:

```
FORMATION OCCURS  <=>  G != {1}
```

`|S|=3 -> G=<u,v>` · `S={0,C} -> <u>` · `S={0,F} -> <v>` · `S={F,C} -> <u/v>` ·
`|S|=1 -> never`, which **recovers W-01's "the root can never fire" as a special case.**
**Formation is a group-theoretic condition on where the record sits.**

**THE NINE.** P-2 persistence · P-3 thresholded non-return (**exactly, not asymptotically**) ·
P-4 recoverability · P-5 redundancy · P-6 asymptotic centrality · P-7 sector-hood ·
P-8 inductive compatibility — **all HOLD**, each with its computation.
**P-1 durability-with-irreversibility and P-9 orthogonal reduced supports HOLD IN THE LIMIT AND
FAIL AT EVERY FINITE STAGE**, exhibited with an explicit reversing unitary at N = 1..5.
**P-9 is resolved: `||omega_F^N - omega_C^N|| -> 2.000000000000`. The predecessor recorded it
false because it is a limit property and was evaluated at a finite stage.**

**TRANSPORT (Q5): YES, MULTIPLICATIVELY.** `Phi_{N+1} = Phi_N · Z_{N+1}`, and the difference
functional is compatible with the embeddings. **Firing is absorbing.** And the limit converts
W-01's **binary** convex-hull criterion into a **rate** `lambda = -0.766802`, defined everywhere
off the trivial connection.

**CORRECTIONS THAT MATTER.** A claimed unital embedding of `M_5 (x) M_2^{(x)N}` into
`M_5^{(x)(N+1)}` is **false for every N**, by the divisibility criterion the same section
states. And the universal claim that every non-trivial connection forms is **false** — four
exhibited families never form, one of them **on K1's own published ready state**.

**WHERE THE PROOF IS.** Build `S3_THE_CROSSING_V001.md`
sha256 `cbf1d79679ca2ecf3ee260e8a6467062e3a93260b2325cfc287c261e9b4469cb`;
audit `S3_THE_CROSSING_AUDIT_V001.md` per its sidecar. The build self-reported eleven defects
including a one-character digest error in its own custody block, caught by the pointer rule and
recorded rather than silently fixed.

**GRADE: ADVERSARIALLY-CHECKED, NOT INDEPENDENTLY-CORROBORATED** (custody §4).

**REOPENS IF:** a schedule condition is found that is carrier-intrinsic rather than adversarial ·
the ready-state support condition is shown to follow from the incidence rather than being free ·
the rate `lambda` fails to vary with the connection at S4 · or a lineage-independent lane fails
to reproduce the character-ratio criterion.

---

## ERRATUM AGAINST W-02 — THE RATE AS REGISTERED IS WRONG (registrar error, 2026-08-16)

W-02 records `lambda = -0.766802`. **That number is wrong under every reading and the error is
mine, not the build's.** It is S3's **N = 4000 finite-stage value of an oscillating sequence**,
transcribed into the register as if it were a converged rate. The corrected statement of record:
S3's headline connection `f = 2.0, c = 1.1` is **exactly resonant** (`-11f + 20c = 0`), so its
orbit is not dense in `T^2` and its average is taken over a **subtorus**; it converges to
**`-0.767014993`**, while the generic torus value is **`-0.767507880` = m(0.4+0.3x+0.3y)**.
S3 section 6(f)'s "rationally independent: orbit dense in T^2" is FALSE and section 4.3's
"Weyl equidistribution AGREES" is a false agreement. Every row of S3 section 5.7 is a subtorus
value. **No W-02 verdict is withdrawn** — the crossing, the UHF limit and the nine stand — but
the mechanism sentence and the rate are corrected here.

---

## W-03 — S4, THE MEASUREMENT, AND ITS AUDIT: **THE HEADLINE IS REFUTED. THE STRUCTURE IS NOT UNIVERSAL.**

**RULING: "THE TOPOLOGY IS INERT; FORMATION SEES LOOP INCIDENCE" IS NOT EARNED. THE FIRST HALF
IS TRUE BUT IS A THEOREM OF THE TRANSPORT'S DEFINITION, NOT A FINDING OF THE CONTROLS. THE
SECOND HALF IS FALSE.**

Build `S4_THE_MEASUREMENT_V001.md` (`4277f0ef…`). Audit: six independent lanes re-deriving from
scratch with their own code, refuters attacking each lane's load-bearing claim, a completeness
critic. **31 agents. Every reproducible number in the build reproduced** — worst agreement
`0.0e+00`, and thirteen of thirteen rows of the S3 corpus block verified for the first time.
**The arithmetic was never the problem.**

**WHY THE CONTROLS COULD NOT HAVE FAILED.** All four controls vary exactly **one** object: the
pushforward of the ready state onto the four vertex classes, `pi = (p_00,p_10,p_01,p_11)`.
Control 1 (the fill) is **vacuous** — `pi` is unchanged, so `lambda` is unchanged **by
identity**. And `d2` — the 2-cells, the entire topological content — **enters the formation
functional nowhere**. "Topology is inert" is therefore an **analytic fact about the
construction**, true before any carrier was built. The controls tested nothing.

**AND FORMATION DOES NOT SEE INCIDENCE.** `lambda_B` is a function of the **MULTISET** of the
four class weights — 24 of 24 permutations invariant, worst spread `2.4e-15`. **The incidence
labels are invisible.** Two exact refutations of the build's own key exhibits:
- A carrier **retaining the pinch** (filled triangle + unfilled square at `v0`) reproduces the
  full `0.0634` shift, `|diff| = 0.0e+00`. The pinch is **not necessary** for it.
- Moving weight **off** the pinch with the incidence **untouched** closes the gap continuously
  to exactly zero. The pinch is **not sufficient** either.
- **PINCH AND SPECTATOR ARE THE SAME OBJECT**, exactly: multiplying `Z_k` by
  `conj(u)^k conj(v)^k` leaves `|Z_k|` fixed and maps class `(a,b) -> (1-a,1-b)`, so
  `00 <-> 11` and `10 <-> 01` is an exact symmetry at **every** connection (max deviation
  `6.55e-15` over 2000 samples).

**THE MODALITY NAMED IN S4'S OWN BRIEF AND NEVER RUN: CHARGE.** Named again in the sealed
upstream S2 as "**this is the S4 knob**". The build never ran it; six audit lanes and their
refuters never noticed. The critic ran it: **THEOREM S4-1 FAILS.** Exponents `(1,0),(2,0),(3,0)`
give `|S| = 3` with `rank G = 1`, against S4-1's "rank 2 iff `|S| >= 3`"; and `q = (1,2,2,2,2)`
moves `lambda` from `-0.767508` to `-1.200555`. **The four-class taxonomy is a charge-1
statement.** Winding was also never non-vacuously run; the critic ran it and it **discriminates
the two schedules** — bearing directly on F1, the flag S4 declared undecidable.

**THE UNIVERSALITY QUESTION, ANSWERED EARLY AND NEGATIVELY.** Two of S4's three deepest results
are theorems about the **character lattice of an abelian group** — "`lambda_B` is a function of
`L` alone" is Pontryagin duality on `T^2`, and Theorem S4-1 is the four corners of a square in
`Hom(U(1)^2, U(1)) = Z^2`. **Neither has an SU(2) analogue.** Section 2's foundational sentence,
"every vertex phase of `s` cancels", is **false the moment the holonomy is not a scalar**:
six ready states with **identical class weights** give `|Z_1|` spread **0.4247** under SU(2),
against exactly `0.0` under U(1). **The construction's core is group-specific.**

**FURTHER CORRECTIONS SURVIVING ATTACK.** `B0b` is `log(4/9) = -0.8109302162163288` exactly, so
**nine of nine** carrier rates are exact, not eight; `(pi,pi)` is a **third strict saddle**, not
a local minimum (the build's own table contradicts `chi(T^2) = 0` at `1-2+2 = +1`); the
exceptional-value split is **527/314/213**, not 638/380/258; section 5 misquotes a reopen clause
**the register does not contain**. Lawton's theorem (1983) is missing from the IMPORT AUDIT.

**THE CARRIER AXIS IS A LIST, NOT A FAMILY.** No cellular collapse, quotient, or map connects
any two of the ten complexes. And the entire C*-algebraic layer of W-02 is **absent from S4** —
which silently moves the first factor from `M_5(C)` to `M_V(C)` as `V` runs 4 to 11, and never
says so.

**CORRECTED HEADLINE OF RECORD:** *under a U(1) connection at unit charge with two designated
loops, formation's rate is a function of exactly two things — the pushforward of the ready state
onto the four vertex classes, and (under the canonical clock) the relation lattice of the two
holonomies; the carrier's topology is inert **by construction rather than by experiment**, the
incidence labels are invisible off a dense measure-zero set, and whether any of it survives
charge, a non-abelian group, or a third loop was never tested.*

**GRADE: ADVERSARIALLY-CHECKED on the axes it ran; NOT INDEPENDENTLY-CORROBORATED, and not
adversarially checked at all on the axes it did not run.** Route to corroboration specified:
a lane outside this model lineage; the charge and three-loop runs with the four controls re-run
under each; publication of `d1`, `d2`, grid and seed conventions; this erratum entered.

**REOPENS ON:** the charge run · the SU(2) run · a third loop · a third schedule (only two exist
anywhere on the page, and the A/B dichotomy may be a knife-edge between two arbitrary choices).

---

## W-04 — THE STEP-BACK: FOUR ERRATA, THE EXPLANANDUM ADJUDICATED, AND THE RESIDUE LOCATED

Nine lanes: archaeology at the bytes, two opposed positions argued at full strength, three judges
on distinct lenses, an explanandum lane with literature access, a synthesis required to commit to
one of four recommendations including STOP. **22/22 sidecars verified; 309,047 bytes swept.**

### ERR-1 — S2's CENTRAL CONDITION IS GLOSSED FALSELY, AND THE FALSE HALF PROPAGATED EVERYWHERE

S2 states its gate condition **correctly** at `:414-416` — **(R1)** `dim H >= 2`, **(R2)** `T, T'`
not both **scalars** — and correctly again at `:514`. It then glosses it at `:421` as *"The
connection must be non-abelian in its action"* and titles §4.3 *"Rank 2 with a non-abelian
structure group."* **THE GLOSS IS FALSE.** One line refutes it: `T_F = I`,
`T_C = diag(1,-1)`, `z = (1,1)/sqrt(2)` gives overlap **exactly 0** with commutator **exactly 0**.
**An abelian, commuting, non-scalar connection writes the gate.** The only control S2 offered for
the gloss tested the scalar case — a vacuous control. **The operative variable is SCALARITY, not
COMMUTATIVITY.** The false half propagated into S3, S4, W-03, and into every lane and judge of
this synthesis. **This is the single most consequential undetected error in the corpus.**

### ERR-2 — W-03's UNIVERSALITY KILL IS NOT ESTABLISHED (registrar error in reporting)

**SU(2) has no faithful rank-one representation.** The SU(2) run therefore changed the **fibre
rank**, the **transport's scalarity**, and the **group's commutativity** simultaneously, and the
resulting `|Z_1|` spread of `0.4247` was attributed to the group alone. **That is a three-way
confounded control assigned to one factor — structurally the identical defect W-03 convicted S4's
controls of committing.** W-03's own ruling reads "the controls vary exactly one object" and calls
that vacuity; its own control varied three and named one. **CORRECTED TEXT OF RECORD:** *the core
is specific to **scalar transport on a rank-one fibre**; the gauge group was never independently
varied.* The universality question is **OPEN**, not answered.

### ERR-3 — THE GRAVITATIONAL TERM WAS DROPPED BEFORE ANY CONSTRUCTION, UNRECORDED

`grep -in "gravit"` over all 11 sealed artifacts returns **EXACTLY ONE LINE** in 309,047 bytes:
`FOUNDING_DESIGN_V001.md:13`, inside the target question. **Zero** in S1, S2, S3, S4, their
audits, the register, custody. §1 poses a tri-partite target (gravitational, electromagnetic,
alpha); **§3 declares the object to be the durability map and the gravitational term is simply
gone.** No register row records the drop. Structurally there is also **no action, no coupling
constant, no Gauss law, no plaquette weight, no backreaction** anywhere — and *a U(1) connection
with no action is a fixed background phase assignment, not a field.* **The tri-partite target has
ZERO of three terms built, not one of three: the electromagnetic term is not banked either.**

### ERR-4 — S1 IS UNAUDITED AND ITS ONE STATED REASON IS FALSE

`S1:43-44` claims K1 is *"the smallest complex carrying one face and one independent cycle at the
same time."* **False at the bytes:** two triangles sharing an **edge**, one filled — `V=4, E=5,
F=1`, `chi=0`, `b1=1`, `rank(d2)=1`, **2 invariants** — is K1's complete invariant profile on one
fewer vertex and one fewer edge, **and it has no pinch.** S1 carries **no CHOICE LEDGER, no
IMPORT AUDIT, no FLAG BLOCK, no register row, and no paired default-refute audit**, against
custody §4. **The artifact fixing the carrier, the fibre rank, the gauge group and the
two-invariant split is the only one in the corpus no adversary ever read.** The pinch itself is
provenance *"Carrier chosen by the principal, 2026-08-16"* with no reason recorded; the word
"pinch" enters at S4, retrofitted.

### THE EXPLANANDUM: **PARTIAL-RESIDUE** — MOSTLY SOLVED AND UNRECOGNISED

**The nine crossing properties map one-for-one onto published criteria.** P-5 redundancy is
quantum Darwinism's `R_delta`. **P-9 is verbatim the Spectrum Broadcast Structure condition
`rho_k^i rho_k^j = 0`** (Korbicz et al.). P-7 sector-hood is **Hepp disjointness**. And the
construction meeting them is **the Coleman-Hepp model, with Bell's 1975 objection re-derived as a
discovery** — S3's "P-1 and P-9 hold in the limit and fail at every finite stage, with an explicit
reversing unitary" **is Bell's objection**. Corpus literature contact: Zurek **0**, Hepp **0**,
Bell **0**, Haag **0**, Araki **0**, "superselection" **0**, "decoherence" **1** (an aside).
**The corpus imports its mathematics by name (Mahler 12, Cassaigne 18, Glimm 2, Lawton 1) and
reinvents its physics anonymously.**

### THE RESIDUE — REAL, AND NOT WHAT THE PROGRAM WAS CHASING

**In a gauge theory the physical (gauge-invariant) algebra does not factorize into system and
environment. Every version of the decoherence / einselection / quantum-Darwinism account
presupposes a given tensor factorization — so on gauge-invariant ground it has no place to
stand — and nothing in the literature or in this corpus DERIVES which adjoined boundary degrees
of freedom constitute the record rather than stipulating them.**

**S2 Theorem 2's no-factorization result IS that non-factorization, and the one-qubit-per-cell
adjunction IS the edge-mode construction** (Donnelly-Wall; Donnelly-Giddings) — which exists
precisely because a gauge theory's Hilbert space must be extended to factorize. **The program
arrived there from a direction that field does not take, did not recognise it, and did not stay.**
It arrived by way of **5 being prime**, not by way of the constraint. Corpus occurrences of
"edge mode", "entangling", "Gauss law", "constraint" in the gauge sense: **0**.

### WHAT K1 WAS

**Inert.** The complex is invisible to the functional. Everything that mattered was decided in
**four unledgered choices laid on top of it**: (i) **rank-one fibres** (S1 §3, an inherited
predecessor convention) — which *entails* U(1) and entails S2's no-go; (ii) **loop transport as
scalar multiplication** rather than edge-by-edge parallel transport — the entire content of
Theorem S3-0, already refuted in scope by the corpus's own sealed **COR-F**, which exhibits a
bona fide non-diagonal unitary transport `T` around the same cycle with `T^3` exactly W-01's
operator; (iii) **no action on the 2-cells** — the complete and trivial explanation of "topology
is inert"; (iv) **five vertices being prime** — which forced the central architectural move.
**U(1) was never chosen.** It is the connected automorphism group of a one-dimensional Hermitian
space; the group follows by necessity from the fibre. The U(1)-versus-SU(2) question is malformed.

### RECOMMENDATION OF RECORD: **NARROW**

Publish the one real result — *formation is a function of exactly the weight multiset and the
relation lattice, blind to topology, to incidence labels and to the pinch, with pinch and
spectator exchanged by an exact symmetry* — **with the Hepp / Bell / Zurek / SBS /
Aharonov-Bohm / Lind-Schmidt-Ward placements it lacks.** Enter these errata. Run **exactly two
cheap decisive tests**: (1) **THE ACTION TEST** — write any action (`beta*Re(W_F)`) and sample the
connection; if `lambda` moves the program has a field for the first time, and if it does not the
construction is provably a statement about a fixed background phase; (2) **THE SCALARITY TEST** —
re-run the S2 gate and Theorem S3-0 at **rank two under U(1)xU(1)**, abelian by construction,
commutator exactly zero, non-scalar. **And rename the project.** Confidence HIGH on the diagnosis.

**IF THE SCALARITY TEST RETURNS "S3-0 FAILS", THE HONEST RECOMMENDATION CONVERTS TO STOP** — the
program's spine would then be an artefact of a convention nobody chose.

### THE FINDING THAT GOVERNS HOW EVERYTHING ABOVE IS WEIGHED

**THE AUDITS COMMITTED THE EXACT DEFECT THEY CONVICTED THE BUILDS OF, AT THEIR OWN HEADLINE, AND
NOBODY AUDITED THEM.** Verified twice at bytes (ERR-1, ERR-2). **The corpus's negatives are not
more reliable than its positives — they came off the same production line with the same failure
mode, one floor higher.** Discount an audit finding by the same factor as a build finding.

---

## W-05 — THE TWO DECISIVE TESTS: **NO FIELD. THE CROSSING WAS NEVER NECESSARY. RECOMMENDATION OF RECORD: STOP.**

Both tests W-04 commissioned ran, each verified on two independent lenses (isolation; mathematics).

### ISOLATION HELD ON NEITHER TEST — ALL FOUR VERIFIERS RETURNED "DOES NOT HOLD"

**The action test's positive half is destroyed twice, independently.** Its headline compared two
carriers "differing only in which triangle the 2-cell is glued to." **`K1^F` and `K1^C` are the
SAME 2-COMPLEX** — four explicit simplicial automorphisms carry `FACE_F` to `FACE_C`,
`max|P·D1 - D1·P| = 0.0`. And the entire `0.267` effect is **reproduced bit-for-bit with the face
never moved**, by the transposition `p10 <-> p01` of the class weights alone, **max deviation
`0.000e+00` over 400 random `(p,beta)`**. Its declared held-fixed background (weights 0.45/0.15)
is an unledgered import supplying **100% of the signal**; under every symmetric ready state in the
corpus the effect is **exactly zero**.

**The scalarity test's headline arm is a four-variable move**, driving the face holonomy from
S1's published `W_F = -1` to `+1` — **zeroing the curvature on the one carrier built to separate
curvature from flat holonomy** — with a ready state supported on `v0` alone, so the four non-root
fibres carry weight exactly zero and the computation reduces to W-04's abstract 2x2 exhibit.

**THIS MAKES FOUR CONSECUTIVE CONFOUNDED HEADLINES: S4's controls (caught by W-03), W-03's SU(2)
run (caught by W-04), and now BOTH W-05 tests — the last two committed by lanes that had READ the
conviction and opened with ISOLATION LEDGERS written to prevent it. That is not bad luck. It is a
property of the production line.** Anything from either test requiring an experiment is WITHDRAWN.

### HAS A FIELD: **NO** — ESTABLISHED, NOT MERELY UNESTABLISHED

For any fixed connection the rate is a deterministic function of `(f,c)` and does not depend on
`beta` under either schedule. **The action supplies a PRIOR over a fixed background, not a field:**
no backreaction, no Gauss law, no constraint, no equation of motion. The build's own flag conceded
it — *"What was built is an ENSEMBLE, not a field. The coupling runs one way."*
**And the affirmative claim is not merely unsupported, it is INVERTED:** a genuine topological
change (two 2-cells on one triangle, `chi 0->1`, `b2 0->1`) is **exactly absorbed by
`beta -> 2*beta`, deviation `0.000e+00`**, while two carriers sharing `chi` and `F` differ by
`0.349`. **The action did not make topology matter. It made the plaquette COUNT matter, and the
lane read one for the other.** The "two schedules, opposite verdicts" result is an **order-of-limits
artefact**: `Omega_1 = Z_1`, so A and B coincide exactly at `N=1` and differ by `C(beta)/N`.

### CROSSING NECESSARY: **NO. IT WAS NEVER NECESSARY.**

**LEG ONE — THEOREM S3-0 IS VACUOUS, WHICH IS WORSE THAN FALSE.** W-01's loop transport
`M_gamma` is **literally an element of the gauge group `U(1)^V`** —
`||M_gamma - gauge_op||_F = 0.000e+00` on S1's published connection and over 2000 random ones;
`max||M* X M - X||_F = 9.7e-16` over 2000 random gauge-invariant `X`. **So S3-0 is the identity
that gauge-invariant observables are invariant under gauge transformations.** S3's own proof says
it twice — *"M_gamma is diagonal"* and *"the gauge-invariant algebra is exactly the diagonal"* are
the same fact. **It could not have failed under any variation of rank, group, scalarity or
commutativity — which is exactly why it survived the test designed to break it. The program's
spine is a definition.** Shrink the gauge group to the global U(1) and an ordinary carrier
observable separates the branches at **2.0000000000000004**.

**LEG TWO — THE SLOT IS ALREADY INSIDE THE CARRIER.** S3 §2.5 specifies `R` as non-abelian,
holding both branches as PURE states with overlap the cell's comparison value `Z`, `dim_C >= 4`.
**The compression of `M_5(C)` to `span{M_dF s, M_c s}` supplies exactly that with nothing
adjoined:** `dim_C = 4`, non-abelian, both branches pure (norms `1.000000000000`), overlap
agreeing with `Z` to `6.2e-17` — **on GENERIC ready states**, not the root-delta state.
**S3 proved `dim R >= 4` by the two-non-parallel-vectors argument and then looked for the `C^2`
outside instead of inside.** What the crossing actually bought was ONE thing: **exemption from an
undeclared premise.** "The record must be gauge-invariant" (COR-J, sealed) is applied
**asymmetrically** — fatal inside the complex, waived by fiat outside it, since S3's own F6 says
*"The record slots carry no gauge action."* The same `M_2(C)` is excluded in the carrier and
admitted outside it, by a premise waived at the boundary.

**LEG THREE — RECURRENCE DOES NOT FORCE ADJUNCTION, BY S3'S OWN LEDGER.** The obstruction is real
and is NOT withdrawn: `K1` is finite and closed, `sup|Z_k| = 1`, so no finite stage holds a durable
record. **But that forces infinitely many CELLS, not an algebra outside the carrier.** S3's CHOICE
LEDGER C1 considered the adjunction-free system `M_5(C)^(x)N` and recorded it **"LEGITIMATE BUT NOT
MINIMAL: 24 extra complex dimensions per cell where §2.5 proves 4 is the floor."** It was rejected
on **a dimension count**, not on necessity. The two alternatives rejected on necessity were killed
by S3-0 (the tautology) and by `5 ∤ 9, 5 ∤ 7` (an accident of five vertices being prime).
**Strip the tautology and the prime and nothing forces the crossing at all.**

### THE CONVERSION, HANDLED HONESTLY IN BOTH DIRECTIONS

W-04's condition — *"if the scalarity test returns 'S3-0 FAILS', the recommendation converts to
STOP"* — **DID NOT TRIGGER ON ITS LETTER. S3-0 SURVIVED**, at rank two, abelian, non-scalar, and
non-abelian too. **The conversion is made anyway, on a ground W-04 did not anticipate and which is
strictly stronger: a theorem that FAILS is contentful. S3-0 is VACUOUS.** And the entailment fails
independently of whether S3-0 is true, because the slot is already in the carrier.

### **RECOMMENDATION OF RECORD: STOP — THE PROGRAM AS CONSTITUTED**

*"The object it was built to explain — a forced crossing out of the carrier — does not exist."*
**STOP is not "burn it": it is "the thing you were chasing is not there, and here is the real thing
you found while not finding it."**

### WHAT SURVIVES — THE PUBLISHABLE RESULT

**N1. THE RATE IS A LOGARITHMIC MAHLER MEASURE:**
`lambda = m(p00 + p10·x + p01·y + p11·xy)` — the per-cell decay rate of a branch comparison on a
gauge-theoretic carrier is exactly the Mahler measure of the polynomial whose coefficients are the
ready state's pushforward onto the four loop-membership classes. **The identification is new; it
inherits the entropy theory of algebraic `Z^d`-actions wholesale.** Six to eight pages, one theorem.

**N2. THE MULTISET / INVISIBILITY THEOREM** with its exact involution — *the one thing in the
corpus that survived every attack, including this round's.*

**N3. THE NULL, INVERTED AND CORRECTLY STATED:** the rate is invariant under every absolutely
continuous connection measure, so **no local Wilson action of any form at any finite coupling can
move it** — because the whole resonance structure lives on a Haar-null set. **Averaging does not
blur the resonance structure, it DELETES it.** `P(rank L > 0) = 0`.

**N4. THE VACUITY OF THE SPINE**, as a methodological result that generalises past this program:
**defining transport as scalar multiplication by the holonomy collapses transport into gauge, and
every "the carrier cannot hold it" conclusion downstream is then a tautology.**

**WITHDRAWN — DO NOT PUBLISH OR CITE:** X1 "the 2-cells enter under an action" · X2 "scalarity
governs the gate" (the gate is written at rank one, abelian, scalar, at exactly zero — W-01's own
ruling, reproduced at `3.5e-17`) · X3 T1-2's criterion · X4 "the slot bought rank two" ·
X5 "two physical clocks."

**REDISCOVERY, ALL UNCITED IN 309,047 SEALED BYTES:** P-9 = the SBS condition verbatim (Korbicz) ·
P-5 = quantum Darwinism's `R_delta`, P-2/P-3/P-6 the einselection cluster (Zurek) · P-7 = Hepp 1972
disjointness, the directed system = the Coleman-Hepp model · **"P-1 and P-9 hold in the limit and
fail at every finite stage with an explicit reversing unitary" IS Bell's 1975 objection to Hepp —
the corpus's most celebrated result, and it is fifty years old** (and correct: re-derived honestly
from five vertices, *"a good sign about the machinery and a bad sign about the literature search"*) ·
the flat holonomy carrying all formation weight at strong coupling = discrete Aharonov-Bohm 1959 ·
one-qubit-per-cell on a non-factorizing algebra = Donnelly-Wall edge modes ·
Mahler / Lind-Schmidt-Ward / Lawton 1983.

**THE LEDGER IN ONE LINE:** *the corpus imports its mathematics by name and reinvents its physics
anonymously, and the reinventions are competent — which is why the honest publication is a short
mathematical note with six citations, not a foundations paper.*

---

## W-06 — THE AUDIT OF THE AUDITS: **THREE IMPORTS FOUND. THE SPINE WAS KILLED BY NONE OF THEM. DISPOSITION: STOP-FALLS-REBUILD.**

Commissioned at the principal's direction — *"let's make sure that we aren't importing machinery
that isn't suitable for the record level to destroy observations."* Four legs, eight refuters.
**Answer: IN PART — and the single largest correction is not an import at all.**

### THE THREE IMPORTS

**IMP-1 — THE VACUOUS-CONTROL DISQUALIFIER, AND IT IS THE ONE THAT CARRIED STOP.**
*"It could not have failed under variation, therefore it is void"* entered this record **lawfully**
at REGISTER:191 against one of S4's **CONTROLS**, and was then carried across a category boundary
at :414-416 onto a **THEOREM**. **On a control the norm is sound. On a theorem it is incoherent —
a proved statement cannot fail; that is what "theorem" means.** Applied to Theorem S3-0 it produced
the word "vacuous", and that word carried the STOP. It entered a governing clause with **no digest,
no file:line, no named ruling** — which under custody §1 makes it **flagged, not inherited**.

**IMP-2 — THE GAUGE NON-FACTORIZATION PREMISE**, imported from Donnelly-Wall/Giddings and pinned to
S2's Theorem 2 — **a theorem this register had ALREADY REFUTED two rows earlier at REGISTER:63**,
and which W-04's own ERR-3 disqualifies. *A refuted theorem cannot BE a correct one.* **Registrar
error: both halves of that contradiction are in this register and are corrected here.**

**IMP-3 — IDENTIFICATION BY HEADLINE PARAPHRASE.** Decoherence and Bell attributions matched on
words rather than papers. See the bibliography corrections below.

### AND THE PROCEDURAL VOID

W-04 pre-registered: *"IF THE SCALARITY TEST RETURNS 'S3-0 FAILS', THE RECOMMENDATION CONVERTS TO
STOP."* **W-05 reports the test returned NEGATIVE — "S3-0 SURVIVED" — and converts anyway**, on a
post-hoc ground built from IMP-1. **Replacing a pre-registered falsifier that came back negative
with a post-hoc one is precisely the abuse the experimental-design norm exists to forbid —
committed in the act of importing that norm.** No registered reopen condition fired.

### **BUT THE THING THAT DECIDED THE SPINE WAS NEVER IMPORTED — AND THE CORPUS ALREADY KNEW**

It was an **unledgered stipulation the corpus made about itself**: that loop transport means
**multiplying by the whole-circuit holonomy** `M_gamma`, rather than moving **edge by edge** via `T`
with `T^3 = M_gamma`. S3's CHOICE LEDGER C3 ledgers only *which circuit schedule*; the edge tick
appears in **no alternatives column in any sealed artifact.**

**THE CORPUS'S OWN SEALED AUDIT FOUND THIS AND WROTE IT DOWN AS COR-F, AT
`S3_THE_CROSSING_AUDIT_V001.md:794`, BEFORE W-03, W-04 AND W-05 RAN.** W-04 cited it in one
subordinate clause. W-05 reached past it. `grep -n "COR-" REGISTER_V001.md` returns **two hits in
491 lines, neither in the W-02 row that records S3-0's ruling.** Two independent legs of this audit,
starting from unrelated suspicions, walked straight into it.

> **THE CHAIN WAS NOT UNDER-ADVERSARIAL. IT WAS UNDER-READ.**

**This is a registrar failure, not a lane failure: I registered W-02 without carrying COR-F into it.**

### THE GAUGE-GROUP HYPOTHESIS: REFUTED, AND THE QUESTION RETIRED

The registrar's suspicion — that local `U(1)^V` is a continuum import and global U(1) the
record-native choice — is **WRONG, twice over.**
**(a) `U(1)^V` is derivable from S1's own bytes:** S1 §5 writes `f = da` and verifies `dd = 0`,
deploying K1's cochain complex; the gauge parameter is that complex's **0-cochain**, and U(1)-valued
0-cochains on K1 **ARE** `U(1)^V` by definition. Intrinsic to a bundle over a CW base, not a
discretisation of anything. **(b) It is UNIQUELY correct on K1's own count:** sweeping all **52**
partition subgroups of `U(1)^5`, **exactly ONE** yields S1 §4's invariant parameter count
`2 = b1 + #faces = E - rank(d1)` — the full local group. Global U(1) gives 6; the class group 4.
**And the escape route W-05 advertised is itself the import:** "global U(1)" smuggles in a
cross-vertex phase frame the complex does not contain — the same *"Let"* that FOUNDING_DESIGN's S2
clause exists to catch. **Across all 52 subgroups the invariant separation is exactly zero in
precisely the 4 that CONTAIN the transports, and 1.32-2.00 in the other 48: S3-0 IS TRUE IF AND
ONLY IF IT IS VACUOUS, AND EVERY EXIT FROM VACUITY IS AN EXIT INTO FALSITY.**

### WHAT IS RESTORED — A QUESTION, NOT A HEADLINE

**THE QUESTION S3-0 WAS BUILT TO CLOSE IS RESTORED TO OPEN: can the carrier's own gauge-invariant
algebra hold the record? THE ANSWER: IT SEES THE RECORD AND IT DOES NOT HOLD IT.**
S3 cited the whole gauge law (S1:59-63) and **implemented half of it** — it computed the fixed
algebra with the **connection held fixed**, while S1:63 (`a_e -> a_e + theta_v - theta_u`) *is* the
connection law. Under the FULL action, a **Wilson-line-dressed observable built only from S1's own
edge transports** is gauge-invariant to `4.45e-16` and separates the branches at exactly
**`3*sqrt(3)/10`** where S3's own test returns zero. **So S3:187-188's "indistinguishable by EVERY
gauge-invariant carrier observable" is FALSE, not vacuous** — and on W-05's own criterion, *a
theorem that fails is contentful*. **S3-0's load-bearing BROAD form (S3:16-22, :206-207), the form
that killed CHOICE LEDGER C1's alternatives, is RESTORED FROM VACUOUS TO FALSE.**

**BUT IT RECURS.** Over `n <= 4000` cells the dressed separation returns to `2.221e-16` and falls
below `1e-9` on **1000 of 4000 cells**. **The recurrence obstruction is the one thing in this corpus
that no demolition and no restoration has dented.**

**N4's MECHANISM RESTORED CORRECTED:** not *scalar* multiplication — **FIBRE-WISE-NESS**. Any
fibre-wise unitary lies in the local gauge group at every rank (`dim A^G = 5` at rank 1, 2 and 3,
verified against genuinely non-scalar and non-abelian transports). W-05 named the wrong variable —
**the same error as ERR-1, recurring one floor up.**

### THE CORPUS IS SMALLER AFTER THIS AUDIT, NOT LARGER

- **THE BELL 1975 ATTRIBUTION IS STRUCK AND REPLACED BY HEPP 1972** — two years older; the register's
  own phrase "reversing unitary" occurs **0 times** in the ten non-register artifacts; Bell's abstract
  draws the **opposite** moral.
- **AND BELL'S ACTUAL OBJECTION TRANSPLANTS INTO S3'S SYSTEM AND WORKS.** An explicit
  Hermitian-unitary `R_N`, one factor per slot, has branch cross-expectation of modulus **exactly
  1.000000000000 at every `N = 1..9`** while `|Omega_N|` falls from `4.11e-01` to `8.42e-04`. That is
  Bell's `lambda_n = c` with `c = 1`. **The record is undone at every finite stage by an observable
  of Bell's own type. This is new, and it cuts against the corpus.**
- **THE AHARONOV-BOHM DEMOTION FALLS ON ITS STATED SUBJECT** — it demoted an observation the corpus
  does not contain, and S4:672 asserts its **negation**.
- **NEW, UNCONTESTED: THE CROSSING CONTAINS NO MEASUREMENT.** S3's write map produces Schmidt
  spectrum `[1, 0]` — entanglement entropy `<= 1.6e-15` — on every superposition; the carrier is the
  same pure state in both branches (trace distance `0.0`). **Carrier and record are never correlated.
  The "record" records which of two counterfactual transports was applied — a CONTROL SETTING, not a
  property of any system.**
- **P-5 = quantum Darwinism and P-9 = the SBS condition SURVIVE.** The leg that struck them tested
  Korbicz's **macrofraction-indexed, asymptotic** condition **at single-slot grain**. Both refuters
  caught it; **the audit recorded the error against itself.**
- **ZERO OF NINE crossing properties are novel, and the corrected bibliography is WORSE:** not four
  rediscoveries spanning 1972-2021 but substantially **ONE body of work** (Hepp, Coleman-Hepp, Bell,
  Lanford-Ruelle) rediscovered whole.

### WHAT STAYS DEAD

Theorem S3-0 as stated · "the carrier cannot hold the record, therefore a crossing is necessary"
(dead four times over) · any hope that a different gauge group restores anything · both of W-05's
own test headlines · "has a field: no" · W-03's kill of "formation sees loop incidence" ·
**all four of W-04's errata, attacked and unbroken** · the novelty of the nine.

### **DISPOSITION: STOP-FALLS-REBUILD**

**STOP's OBJECT is correctly dead and the restorations make it DEADER** — a carrier-internal
observable that holds the branch distinction is one more reason nothing forced a crossing.
**STOP's GROUND has flipped sign** — a vacuous spine is a dead end; a false spine with an exhibited
counterexample is a construction site. **STOP's DISPOSITION was issued on an unpointered import
after the pre-registered falsifier came back negative.** The live route: the carrier's own dressed
gauge-invariant algebra over a **wedge-growth sequence** (`V = 4k+1`; `k = 1,6,31,156,781` gives
`V = 5,25,125,625,3125`, every consecutive pair dividing — **so S3's rejection of C1(b)/(c) on
`5∤9` and `5∤7` is an accident of two arithmetic progressions, not a theorem**). Zero adjoined
dimensions, at S2's zero-addition standard. **Cost, stated: the identification `C^25 ≅ C^5 (x) C^5`
is a labelling not derived from incidence, and the untouched recurrence obstruction may kill it.**

### CHAIN RELIABILITY

**Reliable at arithmetic. Unreliable at disposition.** Every demolition's numbers survived four
independent audits. But the demolitions' failure mode is **MISNAMING THE OPERATIVE VARIABLE** —
S2 said commutativity where it was scalarity; W-03 said the group where it was three things;
W-05 said scalarity where it is fibre-wise-ness — **each caught only by the next level, the third
only now, inside the one result W-05 offered for publication.** W-04 wrote the antidote
(*"discount an audit finding by the same factor as a build finding"*), W-05 quoted it, applied it
downward, and **did not apply it to itself. The chain wrote its own discount and did not take it.**
**FIVE consecutive layers have each been caught by the next, and the rate has not fallen. Discount
this layer too.**

---

## W-07 — THE LINEAGE-INDEPENDENT LANE, RUN AT LAST: **THE RECURRENCE OBSTRUCTION WAS MEASURED AT `ord(rho) = 4`. W-06's RESTORATION SURVIVES. W-06's COMPUTATIONAL CONTENT IS NOT ON DISK.**

The lane W-03 specified and nobody ran. All 9 commits of this repo carry `Co-Authored-By: Claude
Fable 5`; this lane is **Claude Opus 5**, so custody §4's shared-lineage caveat does not apply
between it and the corpus it audits. Sealed corrections read first, in full, before any computation:
S3 audit **COR-A…COR-L** including **COR-F** at `S3_THE_CROSSING_AUDIT_V001.md:794`; S2 audit
**COR-A…COR-H**; **S1 entire**; the erratum against W-02.

**WHERE THE PROOF IS.** `W07_RECURRENCE_ISOLATION_V001.md`
sha256 `0f84fa564b1324837f2187070db2a2b5184ad13f9e3ff64f0abd8480a4a24397`. Lane code, conventions, seeds, grid
and outputs: `LANE_W07_RECURRENCE_ISOLATION/`, `SEALS.sha256`, 15 files, all OK.

### W-06 REPRODUCED FIRST, INDEPENDENTLY — TWO OF ITS THREE FIGURES

The dressed observable, rebuilt from S1's own edge transports under the **full** gauge action
(S1:63 on the connection *and* on the section — the half S3 did not implement), is gauge-invariant
at `3.600e-16` (W-06: `4.45e-16`) and separates the branches at `0.384349931183` where every
diagonal S3-gauge-invariant observable returns `6.939e-18`. **S3:187-188 is FALSE, and W-06's
restoration of S3-0's broad form from VACUOUS to FALSE is CONFIRMED from outside the lineage.**
And W-06's recurrence figure reproduces exactly: **`1000 of 4000` cells below `1e-9`, min `6.7e-19`.**

### THE FINDING: **`W_F = -1`, `W_C = -i`, `<W_F, W_C> = Z_4`. S1's PUBLISHED CONNECTION HAS FINITE ORDER 4.**

`1000 = 4000/4` is `ord(rho)`, the order of the branch ratio in `U(1)`. **Isolating that one variable
— carrier, ready state, observable, dressing, `k`-range and code path all held fixed — the effect
disappears five times out of five:**

```
ord(rho) = 4  (S1 published)      1000 of 4000 below 1e-9,  min 6.729e-19
ord(rho) = inf  sqrt2/sqrt3          0 of 4000,             min 1.567e-04
ord(rho) = inf  random seeds 1,2,3   0 of 4000,             min 1.7e-05 .. 3.1e-04
```

Scaling to `K = 1e7`: on the published connection the dressed record is annihilated **to exact zero
on exactly `K/4` cells at every `K`, forever**; off it the separation is **never zero at any `k`**
and the worst near-return floor falls like `~2pi/K`. **THE OPERATIVE VARIABLE IS `ord(rho)`, FINITE
VERSUS INFINITE** — not "the connection", which is too coarse to be a finding.

### AND THE SAME CUT ONE LEVEL DOWN, ON THE FOUNDING OBSTRUCTION

`FOUNDING_DESIGN §4` promotes *"a finite discrete spectrum is recurrent"* to the obstruction the
construction must answer **at the start**. On S1's published connection `sup_k |Z_k| = 1` is
**ATTAINED**, exactly and periodically — `500000` of `10^6` cells at the published ready state,
`250000` at a generic one. On a generic connection and on S3/S4's headline `f=2.0,c=1.1` alike it is
`0.9999999999986` and **`0` cells**: **APPROACHED, never reached.** **COR-E saw half of this and
labelled the number a lower bound. Nothing in this register distinguishes ATTAINED from APPROACHED,
and they are different obstructions** — one is absolute, the other is a Diophantine rate question
nobody has asked. **The corpus has two distinguished connections — S1's, of order 4, and S3/S4's,
exactly resonant (erratum against W-02) — and both are arithmetically degenerate in different ways.**

### CUSTODY: **W-06 HAS NO ARTIFACT AND NO LANE CODE**

`4.45e-16`, `3*sqrt(3)/10`, `2.221e-16`, `1000 of 4000`, `4.11e-01`, `8.42e-04`, the 52-subgroup
sweep, the Bell `R_N` transplant, the Schmidt `[1,0]`, the wedge sequence — **every figure W-06
produced traces to exactly one file: this register.** W-01/W-02 left sealed build+audit artifacts;
W-03/W-05 left ten lane directories. **W-06 left nothing.** By its own IMP-1 test — *"no digest, no
file:line, no named ruling makes it flagged, not inherited"* — **W-06's computational content is
flagged, not inherited, and the disposition of record rests on it.** Mitigating and recorded: two of
its three figures reproduce exactly from an independent reconstruction, which is not what one expects
of numbers that were never computed. **`3*sqrt(3)/10` does not reproduce** — a factor `sqrt(3)` needs
an element of order 3 and `Z_4` has none. Unresolvable while the code does not exist.

### THE 52-PARTITION SWEEP IS A VACUOUS CONTROL

Re-run and the figure is right — `Bell(5)=52`, distribution `{2:1, 3:10, 4:25, 5:15, 6:1}`, unique
winner the discrete partition. **And it could not have come out otherwise:** a `k`-block subgroup
acts through at most `k-1` parameters, so `invariants >= 7-k`, so `2` forces `k=5`. One line, no
sweep. **"Could not have failed" voids a CONTROL** — and this is a control. **W-06's leg (b) is
void; its leg (a) — `U(1)^V` is the 0-cochain group of the complex S1 §5 already deploys in
`f = da` — is an argument, not a sweep, and SURVIVES. The gauge-group hypothesis stays refuted.**

### WHAT THIS DOES NOT ESTABLISH — STATED BEFORE THE VERDICT, NOT AFTER

**No durable record is shown.** Generically `|Z_k|` still returns to within `1.4e-12` of complete
indistinguishability by `k = 10^6`, which may erase a record as thoroughly as exact recurrence.
**The reading is TWO-WAY** — either the founding obstruction is an artefact of a degenerate
connection, **or** it survives generically in quantitative form and only the register's phrasing is
defective. **This lane does not distinguish them and does not score itself as having.** The dressed
observable is a **reconstruction**, not W-06's code. **And this is layer six**: five layers have each
been caught by the next and the rate has not fallen. **Discount this one.** Its likeliest failure
mode is the corpus's recurring one — misnaming the operative variable. It is named `ord(rho)` here.

**GRADE: INDEPENDENTLY-DERIVED (Opus 5 against a Fable 5 corpus), NOT ADVERSARIALLY-CHECKED.** No
refuter has read it. That is the inverse of every other grade in this corpus, and the missing half
is the weaker one.

**NOTHING HERE TAKES ANY OF THE PRINCIPAL'S THREE DECISIONS.** It changes the **shape** of the first:
STOP-FALLS-REBUILD was issued with the recurrence obstruction standing as *"the one thing no
demolition and no restoration has dented"*, and its rebuild cost line reads *"the untouched
recurrence obstruction may kill it."* Both are measured at `ord(rho) = 4`.

**REOPENS / NEXT, AND IT IS ONE CALCULATION, NOT A REBUILD:** `lambda = m(p00 + p10 x + p01 y +
p11 xy)` is the entropy of an algebraic `Z^2`-action; the near-return depth of `|rho^k - 1|` is
governed by the same arithmetic. **Does the record's growth rate outrun the near-return floor?**
Both sides are already computed objects here, and it decides whether the founding obstruction
survives off the degenerate point. **W-07 is superseded if:** a refuter shows the dressed
reconstruction is not W-06's object · `ord(rho)` is shown not to be the operative variable ·
or W-06's lane code is produced and contradicts §2.

---

## ERRATUM AGAINST W-07 — TWO SENTENCES OF THAT ROW ARE FALSE (registrar error, 2026-08-16)

Both found by W-08's refuters, both re-verified by me from the corpus's own bytes before being
carried here (`LANE_W08_REGISTRAR_VERIFY/`, 5 files sealed).

**E-1. W-07's HEADLINE IS FALSE OF THE FIGURES IT NAMES.** W-07 §1 states that *"every recurrence
figure in this corpus was measured"* at S1's order-4 connection. **The corpus states its own test
point verbatim, twice, and it is a different connection:** `S2_FORMATION_CONDITION_ON_K1_AUDIT_V001.md:439-440`
and `S3_THE_CROSSING_V001.md:423-427` both give `f = 2.0, c = 1.1, p = (0.4,0.15,0.15,0.15,0.15)`.
Recomputed independently: `min|Z_k| = 0.024654 at k = 42` and `sup|Z_k| = 0.999941 at k = 377` —
**W-01's registered `0.0247 at n=42` and `0.99994`, the figures STOP-FALLS-REBUILD was issued
against.** That connection is the **exactly resonant** one of the erratum against W-02
(`-11f + 20c = 0`), of **INFINITE order**, where the supremum is APPROACHED and never attained.
At the order-4 point `|Z_k|` takes exactly three values `{1/sqrt(10), 2/5, 1}` and `0.024654` is
`0.2916` from the nearest. **W-07's claim is true of exactly one figure — W-06's `1000 of 4000` —
and W-06 is the lane with no artifact.** The ATTAINED/APPROACHED distinction is not withdrawn; the
claim about where the corpus measured is.

**E-2. "A FACTOR `sqrt(3)` NEEDS AN ELEMENT OF ORDER 3 AND `Z_4` HAS NONE" IS FALSE.** Exactly, in
rationals: with `|s_v|^2 = (3/4, 4/25, 0, 9/100, 0)` (sums to 1) the pair `(v0,v3)` has
`(dF,dC) = (-1,0)`, so `D_k = amp|(-1)^k - 1|`, `amp^2 = 27/400`, `(2·amp)^2 = 27/100 = (3√3/10)^2`
**exactly**. The `sqrt(3)` is in the ready state's amplitudes, not in the group. **`3√3/10` is
reachable on S1's own published connection.** The W-07 *page* listed "a different normalisation"
among three escapes; the *row* did not, and the row is what is corrected. **The custody finding is
untouched — reachability is not reproduction, and W-06's code still does not exist.**

---

## W-08 — THE RACE: **THE DECAY OUTRUNS THE FLOOR, AND THE TWO NEVER COMPETE. THE FOUNDING OBSTRUCTION IS FALSE AS AN INFERENCE. WHAT SURVIVES OF IT IS A SCHEDULE STATEMENT WITH AN EXPONENT.**

Commissioned on W-07's REOPENS clause. Four build lanes (identification, floor, zero set, and a
refuter aimed at W-07), eight refuters on distinct lenses, an isolation audit over **64 comparisons**,
and a synthesis required to commit. **14 agents, 0 errors.** Every finding carried below was
re-verified by the registrar from the corpus's own bytes before entry.

**WHERE THE PROOF IS.** `W08_THE_RACE_V001.md` sha256 `3a9fa0ebfe88b3f19562e6251132fd11faebddca62d30d295f693352bf133e79`. Lane code:
fourteen directories `LANE_W08_*`, each with `SEALS.sha256`, **all verify**.

### THE ANSWER: **YES, UNCONDITIONALLY — AND THE QUESTION COMPARES INCOMMENSURABLES**

**`|Z_k| <= 1` always**, by the triangle inequality on non-negative weights summing to one — so
**`|Omega_N| = prod_{k<=N} |Z_k|` is MONOTONE NON-INCREASING.** Checked, not asserted: over
`k <= 10^6`, `max_k(|Z_k| - 1) = -1.446e-09` at the resonant connection, `0` exceedances anywhere.
**A near-return means that circuit writes nothing. It does not un-write the previous `N-1`.**

> **THE FOUNDING OBSTRUCTION IS FALSE AS AN INFERENCE.** *"It fires, and then it un-fires. A
> reversible write, not a record"* (`S2..._AUDIT_V001.md:447`, repeated `S3_THE_CROSSING_V001.md:429`)
> is drawn from the **single-cell** observable `|Z_k|` and never from the product, **which is the
> object durability is a property of.** W-07 looked for the fault in *where* the obstruction was
> measured. **The fault is in *what* was measured.** The corpus already half-owned this: COR-C
> struck `|Omega_N| <= e^{lambda N}` and replaced it with *"the monotonicity … that §4.3-4.4
> actually prove"* — **the monotonicity was in the record and was never turned on the recurrence
> sentence.** Under-read again, and this time the correction was the registrar's own to make.

**THE DECAY IS LINEAR WITH AN EXPLICIT CONSTANT, WITH NO DIOPHANTINE HYPOTHESIS.** From the
character identity `|Z_k|^2 = 1 - sum_{j<l} w_j w_l |chi_j^k - chi_l^k|^2` (exact `0` residual in
`Fraction` arithmetic over 768 and 336 cases, two independent refuters): for any pair with
`chi_j != chi_l`, `SUM_{k<=K}(1-|Z_k|) >= w_j w_l (K - 1/|sin(tau/2)|)`. Measured densities at
`K = 10^7`, one variable moving: `0.4919` (order-4), `0.4692` (resonant), `0.5295` (rank 1),
`0.4692` (random) — every one far above the proved floor `0.12`.

**THE FLOOR'S ENTIRE CONTRIBUTION IS `O(1)` AND `K`-INDEPENDENT.** At `K = 10^7` the whole
near-return band below `eps = 1e-3` contributes `8.9e-07` of the decay budget; below `1e-6`,
`9.2e-13`. **And the floor can be driven five orders deeper without moving the rate at all** —
approaching the order-4 point, `F(10^6)` falls `2.189e-06 -> 3.226e-11` while `lambda` reads
`-0.767507880` in every row. **THE FLOOR AND THE RATE ARE INDEPENDENT COORDINATES. THEY DO NOT
RACE.** The floor is a property of ONE cell; the rate is a property of ALL of them.

### WHAT ACTUALLY DEFEATS DURABILITY — AND RECURRENCE IS NEITHER

**(1) `G = {1}`.** `|Omega_N| -> 0` **iff** `G = <chi_a/chi_b : a,b in supp(pi)> != {1}` — proved by
Weyl on the *continuous* function `1-|P|` plus the strict triangle inequality, no Diophantine
input. This is **COR-B's four non-forming families re-derived as a criterion**, and it survived all
four refuters who attacked it.

**(2) THE SCHEDULE — AND THIS IS WHERE THE FOUNDING OBSTRUCTION GENUINELY SURVIVES.** Verified by
the registrar: an adversary writing only the `sqrt(K)` cells of smallest `1-|Z_k|` accumulates
`0.606, 0.615, 0.588, 0.601` nats at `K = 10^4..10^7` — **`|Omega| ~ 0.55` forever, with
unboundedly many writes** — while the honest schedule `k_n = n` accumulates `7678 -> 7675061`.
**Durability is a property of the (connection, SCHEDULE) pair, and the corpus has never stated a
schedule stipulation.** The admissible adversarial write density is `K^{-1/2}` at `d_eff = 2` and
`K^{-1/3}` at `d_eff = 1` (measured last-decade exponents `0.5003, 0.5003, 0.6666, 0.6667` against
theory `0.500, 0.500, 0.667, 0.667`).

**AND THIS IS WHERE W-07's ATTAINED/APPROACHED CUT DOES ITS WORK — THE SCHEDULE AXIS, AND NO OTHER.**
At the order-4 point `1-|Z_k| = 0` exactly on `250000` of `10^6` cells, so the adversary has a
**fixed positive** write density at **zero** budget. Off it the density must fall like `K^{-1/2}`
or `K^{-1/3}`. **A difference of EXPONENT — not the "absolute versus cosmetic" dichotomy.**
**W-07 was right that the register distinguished neither, and wrong about which axis it lives on.**

**AND ONE NON-UNIFORMITY, NEW AND IN NO PRIOR ROW:** `lambda < 0` at every non-trivial connection,
but the **onset** diverges — the circuits needed to write one nat run `2, 10, 47, 216, 1000, 4642`
as `t -> 1e-5` on the rank-1 locus, with `lambda = log 0.3` in every row (`K_0 ~ t^{-2/3}`).
**Durability holds for every non-trivial connection and holds uniformly for none.**

### RULING ON W-07

**SURVIVES:** the reproduction of W-06 (a third independent confirmation, `D_1 = 0.384349931183`
to `7.85e-14` from code sharing nothing with W-07's; `1000 of 4000` exact in 60-digit rationals) ·
the **vacuity ruling on the 52-partition sweep**, whose attacker's counterexample was itself wrong
(the discrete partition is the unique winner on **178 of 178** random connected graphs) · the
ATTAINED/APPROACHED observation, relocated · and its own limitation block, which W-08 vindicates.
**FALLS:** `ord(rho)` **as the operative variable** — an exact rational `theta = 1/4 + 1e-13` has
**finite** order `10^13`, so W-07's own sharp form predicts `0` and the observable returns `1000`;
the replacement name `min_k||k theta||` fails too, and the correct name at fixed `(K, tol, amp)` is
the pair `(q, delta)`. **W-07 is superseded on its own clause** — *"superseded if `ord(rho)` is
shown not to be the operative variable."* Plus the two errata above. **The corpus's recurring
defect, committed by the row that named it.**

### THE WEAKEST LOAD-BEARING CLAIM IN THE CORPUS — AND IT IS NOT IN W-08

**`W-01`'s convex-hull criterion as this register states it at `:43`, and specifically the clause
"three unit-modulus coefficients".** Registrar-verified, 200000 draws, one variable moving (the
number of occupied characters, same hull test and grid in both arms):

- **"three" is `p00 = 0`, an incidence fact about K1** — no vertex lies outside both loops. With
  one spectator vertex there are **four** characters, the criterion acquires the closed form
  `cos f + cos c <= 0` (agreeing with the hull on **200000 of 200000**), and **the firing region
  doubles from `0.2507` to `0.4989`** — exactly `1/4` to `1/2`.
- **W-01's own advertised virtue does not survive one added vertex.** *"It distinguishes curvature
  from flat holonomy, which K1 exists to separate"*: sending `f -> -f` alone changes the verdict at
  **99785 of 200000** points on K1 and at **0 of 200000** on the spectator carrier. **The property
  the register advertises as the criterion's virtue is a coincidence of `p00 = 0`.**
- The quantifier is dropped: `iff` is false read literally; `Z_1 = 0 => 0 in conv` is the true half
  and is the one W-01's exhibit travels on.

**No W-01 result is touched — and that is exactly why it has survived seven layers unexamined.**
It is quoted forward by S3, S4, W-03 and every W-08 lane; it is the sentence a rebuild would be
built on; and it is the only load-bearing claim in the corpus never checked on a second carrier by
a lane whose job it was.

### THE ISOLATION AUDIT'S FINDING, WHICH GENERALISES PAST THIS PROGRAM

**The commonest FATAL defect across twelve lanes is not "two variables moved" — it is "ZERO
variables moved."** Five of eleven FATALs are controls that could not have failed, one of them a
control in which the two arms were byte-identical (`difference exactly 0`) and which was reported
as a confirmation. **An isolation ledger cannot detect any of these, because a ledger records what
the author intended to vary.** Three build lanes wrote ledgers; five of the seven FATAL build
confounds sit in the arm the lane's own ledger names as decisive. **Treat "the ledger says one
variable" as evidence of nothing — read the code.**

### WHAT READS TWO WAYS, AND IS SCORED AS NEITHER

**The adversarial schedule** reads as *"durability is a schedule stipulation the corpus never
made"* **or** as *"`K^{-1/2}` write density is not an admissible schedule and the stipulation is
right."* W-08 supplies the exponent, not the admissibility criterion, and does not distinguish
them. **W-07 leg E's five-for-five null** is a density statement, not an isolation of `ord(rho)`.
**And `lambda` can be ~40% slower at degenerate points than generic** — which reads as "degeneracy
helps the record persist" or as "`lambda` is simply non-monotone in `H`"; the second is better
supported and neither is scored. **Every one of those rates is strongly negative, so the race
verdict does not depend on which reading is right.**

### WHAT W-08 DOES NOT ESTABLISH

**No durable record is constructed.** §1 decides a race between two computed objects on K1; it
builds nothing. **The schedule half has an exponent and no admissibility criterion. Nothing off K1
is decided** — all four build lanes ran on K1 alone. **The dressed observable is still a
reconstruction and W-06's code still does not exist.** **And this is layer NINE of one lineage:**
W-07, M1-M4, all eight refuters and the synthesis are Opus 5. Three of them named an operative
variable and the next caught it each time. **Discount this row as one block with W-07, not as an
independent check.** The lineage-independent lane W-03 specified still does not exist for anything
in W-08.

**NOTHING HERE TAKES ANY OF THE PRINCIPAL'S THREE DECISIONS.** It bears on the first: the
disposition's cost line — *"the untouched recurrence obstruction may kill it"* — names an
obstruction that is **false as an inference** and survives only as a schedule statement the corpus
never wrote down.

**REOPENS IF:** a connection with `G != {1}` is exhibited on which `SUM(1-|Z_k|)` is sublinear ·
an **intrinsic** admissibility criterion for schedules is written down under which the corpus's own
`SUM(1-z_n)` test is recovered and the `K^{-1/2}` adversary excluded · **or someone states a
durability observable on which a single-cell near-return DOES undo earlier writes — the one move
that would restore the founding obstruction, and nobody in this corpus has attempted it.**
**NEXT, AND IT IS ONE SCRIPT AGAINST TWO OBJECTS THE CORPUS ALREADY OWNS:** run W-01's criterion,
in this register's own words, on carriers `B1q` and `B0b` (`S4_THE_MEASUREMENT_V001.md:519, :582`)
and report which reading each obeys, quantifier restored. It decides the weakest claim above.

---

## W-09 — W-01's CRITERION OFF K1: **THE OPERATIVE VARIABLE IS ALL FOUR CLASSES OCCUPIED, WHICH NEEDS A PINCH *AND* A SPECTATOR. K1 HAS ONLY ONE OF THEM, AND SO DOES EVERY CARRIER THE CORPUS EVER RAN.**

The computation W-08 named as next. **One script, against carriers the corpus already owns** —
class multisets quoted verbatim from `S4_THE_MEASUREMENT_V001.md:575-590`; nothing new constructed.
`LANE_W09_W01_OFF_K1/`, `SEALS.sha256`, 8 files, all verify. Isolation: hull test, grid, seed and
evaluator identical in every row; **the one thing that moves is which characters the incidence
occupies.**

### THE RESULT

| carrier (S4's own row) | occupied | characters | firing region | `f -> -f` flips |
|---|---|---|---|---|
| `B1` K1 as handed, `B2`, `B1s`, `B3` | `{01,10,11}` | `v u uv` | **exactly 1/4** | 99785/200000 |
| **`B1q` K1-bridged + SPECTATOR** | `{00,01,10}` | `1 v u` | **exactly 1/4** | 99785/200000 |
| `B1p` K1-bridged | `{01,10}` | `v u` | `0` — never fires | 0 |
| **`B0b` ring torus loops meet, `B4` spindle** | **all four** | `1 v u uv` | **exactly 1/2** | **0/200000** |

**BOTH VALUES ARE EXACT, NOT MEASURED.** Three occupied classes reduce, on dividing by one
character, to `{1, e^{i th1}, e^{i th2}}` with the two angles independent uniform — so
**Wendel's theorem (1962)** gives `P(0 in hull) = 1 - 2^{-2}(C(2,0)+C(2,1)) = 1/4`. With all four,
`uv` is determined by `u` and `v`, Wendel does **not** apply, and the closed form does:
`0 in conv{1,u,v,uv} <=> cos f + cos c <= 0` (agrees on **400000 of 400000**), which is exactly
`1/2` because `(f,c) -> (pi-f, pi-c)` preserves the measure and flips the sign.

### AND THE NAMING — W-08's SYNTHESIS NAMED THIS WRONG, AND SO DID I

W-08 §6 called the operative variable *"three unit-modulus coefficients"*, i.e. `p00 = 0`.
**`B1q` refutes that: it has `p00 > 0` and reproduces K1 to the last digit.** The reason is in this
register already — **W-03's involution, `00 <-> 11` and `10 <-> 01`, exchanges K1's occupied set
`{01,10,11}` with `B1q`'s `{00,01,10}` exactly.** K1 has a vertex in **both** loops and none in
neither; `B1q` has one in **neither** and none in both. *Pinch-only and spectator-only are the same
carrier for this criterion, by a symmetry the corpus proved at W-03 and never applied here.*

> **CORRECTED NAME OF RECORD: the operative variable is whether the incidence occupies ALL FOUR
> CLASSES — which requires a vertex in both loops AND a vertex in neither. Not the coefficient
> count, not `p00`, not the pinch.** Every three-class carrier fires on exactly `1/4` and is
> curvature-aware; the four-class carriers fire on exactly `1/2` and are **curvature-blind**.
> **This is the fourth consecutive layer to misname the operative variable, and the third time the
> correct name was already in an earlier row.**

### WHAT FALLS

**W-01's ADVERTISED VIRTUE IS A THREE-CLASS ACCIDENT.** *"It distinguishes curvature from flat
holonomy, which K1 exists to separate"* (`REGISTER_V001.md:47`). Reversing the **curvature alone**
and leaving the flat holonomy untouched changes the verdict at `99785/200000` on every three-class
carrier and at **`0` of `200000`** on every four-class one — `cos f + cos c` is even in `f`.
**The property the register advertises as the criterion's virtue disappears the moment a carrier
carries both a pinch and a spectator, and no carrier the corpus ever ran carries both.** The ten
carriers of `S4:519` include exactly two four-class rows, `B0b` and `B4`; neither was run against
W-01's criterion by any lane before this one.

**NO W-01 VERDICT IS WITHDRAWN.** The criterion is correct on K1, the firing on S1's connection is
correct, and the `FIRE => HULL` direction is unconditional. What falls is its **scope** and its
**stated reason for existing**, both quoted forward unqualified by S3, S4, W-03 and every W-08 lane.

### REGISTRAR DEFECT, RECORDED RATHER THAN PATCHED

`w09c_exact.py`'s hull helper first read `np.diff(..., 0)`, where the second positional argument is
the difference **order**, not the axis — so leg C2 printed `0.000000` and a meaningless agreement
count on its first run. Legs A and B pass `axis=0` by keyword and were never affected; their
figures stand unchanged. The defect and its correction are in the sealed file.

**NOTHING HERE TAKES ANY OF THE PRINCIPAL'S THREE DECISIONS.**

**REOPENS IF:** a four-class carrier is exhibited on which the firing region is not `1/2` · or the
`f -> -f` blindness is shown to depend on the uniform measure on `(f,c)` rather than on the parity
of `cos f + cos c` · or a lineage-independent lane fails to reproduce the two exact values.
**NEXT:** every registered result derived on K1 that is quoted forward without a carrier
qualification — W-01's criterion, W-02's character-ratio criterion, W-03's multiset theorem, N1's
polynomial — should be re-stated with the class-occupancy condition attached. **The corpus has
never run a four-class carrier through anything.**

---

## ERRATUM AGAINST W-09 — "FOUR-CLASS CARRIER" IS NOT A THING (registrar error, 2026-08-16)

W-09 concluded *"of S4's ten carriers exactly two are four-class"* and *"the corpus has never run a
four-class carrier through anything."* **Class occupancy is a property of the LOOP DESIGNATION, not
of the complex.** The four classes are defined by *(is `v` in `gamma_F`? is `v` in `gamma_C`?)*, so
changing `gamma_C` changes them. Exhibited: on **B0b's own complex with S4's own `gamma_F`**,
sweeping every admissible simple cycle for `gamma_C` reaches **16 distinct class multisets** — 8
four-class, 7 three-class, 1 two-class — with `lambda` spanning `log(5/9)`, `log(4/9)`, `log(1/3)`
(`LANE_W10_A_CARRIERS_REFUTE_1/r1_rebuild.OUT.txt:81`). **CORRECTED TEXT OF RECORD:** *two
four-class **designations**, chosen under S4's CHOICE LEDGER C4, which closed the loop-designation
question by fiat.* Nothing in W-09's arithmetic changes — the `1/4` and `1/2` regions and the
curvature-blindness are properties of class occupancy and stand. **What falls is the phrase "the
corpus has exactly two four-class carriers", and with it the implicit claim that occupancy is
forced.** Deciding it needs an **admissibility criterion for loop designations**, which the corpus
has never written — the structural twin of W-08's missing schedule-admissibility criterion.

---

## W-10 — THE SCOPE TABLE: **THE CORPUS DOES CONTAIN CARRIER-INDEPENDENT RESULTS. THEY ARE THEOREMS, NOT MEASUREMENTS, AND THEIR CARRIER-INDEPENDENCE IS A CONSEQUENCE OF THE TRANSPORT CONVENTION W-06 NAMED AS HAVING DECIDED THE SPINE.**

Commissioned at the principal's direction, who **deferred the disposition decision by one step to
obtain it**. Four build lanes, eight refuters, a synthesis with its own verification lane, and the
registrar's own exact re-check of everything that corrects a register row. **13 agents, 0 errors.**

**WHERE THE PROOF IS.** `W10_SCOPE_TABLE_V001.md` sha256 `3b84120c895ea1024ac3de08cb6c5834a230610bdd0ed84c62dcc6917f9a90b1` — full table, ~50 rows, each with a SCOPE mark and
a **BASIS** tag distinguishing *theorem* from *exhibited* from *could-not-have-failed* from
*argued-only*. Fourteen sealed lane directories `LANE_W10_*`, all verify.

### THE ANSWER, IN THE FORM THE DECISION NEEDS

**CARRIER_INDEPENDENT:** N1's identification `lambda = m(p00 + p10 x + p01 y + p11 xy)` ·
W-08's monotonicity and the falsity of the founding obstruction as an inference · W-08's character
identity and its linear floor · W-02's criterion `FORMATION <=> G != {1}` · W-03/N2's multiset
theorem and its exact involution · the schedule result qualitatively · N3 and N4.
**Every one is a statement in `(pi, u, v)` with no carrier symbol in it — so a four-class run is a
CONTROL, not a test.** The table says so in the BASIS column rather than scoring the runs as
evidence.

**AND THE QUALIFICATION THAT MATTERS MOST, WHICH NO REGISTER ROW CARRIES:** they are
carrier-independent **given the transport convention** — whole-circuit scalar multiplication by
`M_gamma`. Under the corpus's own sealed alternative, **COR-F's edge-tick transport `T` with
`T^L = M_gamma`**, the transports are non-diagonal and `||[T_F, T_C]||` is `2.828` on B0b, `2.449`
on K1 and **exactly `0` on B0a — non-zero precisely when class 11 is occupied.** **The incidence
that N2 calls invisible is visible to the corpus's own sealed alternative transport, and COR-F
still has no register row.** Honest mark: **CARRIER_INDEPENDENT ∧ CONVENTION_SCOPED.**

**THREE_CLASS_SCOPED:** W-01's convex-hull criterion and its advertised virtue (W-09, now
reproduced a fourth time on a deterministic grid with a third hull algorithm) · W-02's published
support table, which is **incomplete, not wrong** — six two-element supports exist, three are
listed, and the three omitted are exactly those needing class 00.

**K1_SCOPED:** **the entire C\*-algebraic superstructure, and its hypothesis is the primality of 5**
— `UHF(5·2^inf)`, *"one qubit per cell, proved minimal"*, S3's rejection of its own adjunction-free
alternative, **and W-06's `V = 4k+1` rebuild route.** On B0b, `9 | 81`, so `M_9^{(x)N}` is a directed
system with unital embeddings and **no adjunction at all** — the route's own motivation evaporates
on the very carrier its sequence reaches.

**UNDETERMINED — thirteen rows, none guessed.** Six of the nine crossing properties (**unrunnable:
S3 published no lane directory**) · everything W-06 computed (no artifact) · W-08's four schedule
constants (not reproduced) · the multiset theorem's hypothesis off the non-negative locus.
**P-9 and P-3 are decided here for the first time and are CARRIER_INDEPENDENT.**

### NEW DEFECTS OF RECORD, REGISTRAR-VERIFIED

**N-4 — EVERY RATIONAL CONNECTION IS EXACTLY RESONANT, AND IT CONVICTS THREE MORE PUBLISHED ROWS.**
One line: if `f, c` are rational then `mf + nc` is rational, `2 pi j` is irrational for `j != 0`, so
`j = 0`, and `(m,n) = (r q, -p s)` is a nonzero relation. **Exact census, verified in `Fraction`:**
`f=2.0,c=1.1 -> (11,-20)` (already of record) · `f=2.0,c=2.0 -> (1,-1)` ·
**`S4:973`'s `3.14159, 1.57080`, published in terms as *"they are generic"*, `-> (157080,-314159)`**
· W-10 lane D's own hard-coded `1.3, 2.0 -> (20,-13)`. **S4:973's mislabelling sits inside the
paragraph correcting the corpus's first two mislabelled connections.** **`S4:603`'s `f = 1.0,
c = sqrt(2)` is the ONLY generic connection the corpus publishes — and it is the one S4 used to
verify the entire `lambda` column**, which is why that column survives.

**N-1 — S4's B4 ROW IS UNDER-DETERMINED BY ITS OWN PARAMETERS.** A second spindle — a triangle with
two 2-cells glued to a pentagon with two 2-cells at two points — matches **every published column**
(`V=6 E=8 F=4 chi=2 b=(1,1,2)`, gauge 5, inv 3, curv 2, flat 1, `d1·d2=0`, `gamma_F` bounds,
`gamma_C` does not, independent) and delivers class multiset `{00:1,10:1,01:2,11:2}` with
`lambda = log(1/3)` against S4's `log(1/2)`. **COR-K defect class against S4. And the build lane
hard-coded S4's multiset as its target, so its match could not have failed** — caught by its own
refuter.

**N-3 — S4:599's *"genuinely 4-term and does not factor. QUADRATURE ONLY, -0.810930216216"* IS HALF
WRONG.** The non-factoring half is exact (`p00·p11 = 8/81 != 2/81 = p10·p01`). The other half falls:
`|a+be^{it}|^2 - |c+de^{it}|^2 = 5/27 + (4/27)cos t`, which would need `cos t = -5/4` to vanish, so
**one Jensen branch dominates everywhere** and `lambda = m(4/9 + (2/9)x) = log(4/9)` **exactly**.
Independent Jensen quadrature at `n = 2^22` returns `-0.810930216216329`; branches never cross.
**Non-factoring does not imply no closed form.**

**N-6 — FIVE MORE ZERO-VARIABLE CONTROLS**, two of them inside blocks written to correct earlier
zero-variable controls, and an arms-diff guard that hashes **inputs** while the collapse is in the
**outputs**. **N-7 — the multiset theorem's hypothesis has now been misnamed SIX times, three of
them this round by refuters commissioned to catch misnaming, and my own "real non-negativity" is
one of the six.** Two independent mechanisms produce the invariance — flux coincidence and branch
domination — and no proposed name covers both. **Marked UNDETERMINED; the synthesis declined to
supply a seventh name and so do I.** It touches no registered result: `pi` is a probability vector,
so the corpus never leaves the regime where the theorem is proved.

**N-10 — "S4 WAS NEVER AUDITED" IS TOO STRONG, AND I REPEATED IT.** B1, B1q and B0b had their full
S4 rows — `d1`, `d2^T`, invariants, class multisets, `lambda` by three methods — reproduced in
`LANE_R_MAPS_REFUTER/rm_1_validate.OUT.txt` during the **W-03** round. The correct statement is that
**S4's artifact carries no sealed audit document and its carrier code is not in the repo**; parts of
its table were checked in passing by a lane doing something else.

### WHAT READS TWO WAYS — AND THE SYNTHESIS REFUSED TO SCORE IT, CORRECTLY

**IS "THE FORMATION FUNCTIONAL IS CARRIER-INDEPENDENT" A FINDING OR A RESTATEMENT OF THE
CONVENTION?** *Reading A:* a substantive result — the physics does not depend on the complex, which
is why a short mathematical note is publishable. *Reading B:* transport was **defined** as fibre-wise
scalar multiplication by the whole-circuit holonomy, so only `pi` **can** enter, and the result is an
analytic consequence of an unledgered stipulation — W-04's *"what K1 was: inert"* and W-06's *"the
thing that decided the spine"* both say so. **Both readings are supported. They have opposite
consequences for a rebuild: A says the functional layer is portable; B says portability is what you
get for free when the carrier was stipulated out.** Not scored. **This is the single most
consequential undecided question the table produces.**

### LINEAGE

**Layer TWELVE of one lineage.** W-07 through W-10, every lane and every refuter, are Opus 5. The
last lineage-independent boundary in this corpus is Fable 5 (S1-S4, W-01…W-06) to Opus 5 (W-07 on),
and everything in this round sits on one side of it. Two refuters accepted an upstream construction
byte-identical rather than re-deriving it. **Six consecutive layers have each been caught by the
next and the rate has not fallen. Discount this row as one block with W-07 through W-09.**

**NOTHING HERE TAKES ANY OF THE PRINCIPAL'S THREE DECISIONS.**

**REOPENS IF:** an admissibility criterion for loop designations is written (it would decide N-2 and
the B0b sweep) · COR-F's edge-tick transport is carried into a register row, which would rescope
every CARRIER_INDEPENDENT verdict · S3's lane code is produced, which would make six of the nine
crossing properties runnable · or a **lineage-independent** lane reads this table.
**NEXT, IF ANYTHING:** the convention question above is decidable — run the whole formation
functional under COR-F's `T` instead of `M_gamma` on K1 and on B0b, and see whether the incidence
becomes visible. It is the one experiment that would tell reading A from reading B.

---

## W-11 — THE CONVENTION RULING: **READING B. CARRIER-INDEPENDENCE IS A RESTATEMENT OF THE TRANSPORT CONVENTION. N1 IS NOT, SURVIVES INTACT, AND IS PUBLISHABLE UNDER TWO HYPOTHESES IT DOES NOT CURRENTLY CARRY.**

Commissioned at the principal's direction, who deferred the disposition decision a **second** time
to obtain it. The registrar's test (4 legs), then eleven agents sent to refute it: a uniqueness
attack on `T`, a clock-correspondence attack, a mathematics attack, a full-strength steelman of
Reading A, a blind independent rebuild, one cross-refuter each, and a ruling. **11 agents, 0
errors.** Thirteen sealed lane directories, all verify. Every load-bearing claim re-verified by the
registrar, **including the one that cuts against the registrar's own test.**

**WHERE THE PROOF IS.** `W11_CONVENTION_RULING_V001.md` sha256 `4a71ca885ade912dc672d99c2e8e3b82e3041a3e159527e36658efdc5e3cf027`.
Test: `LANE_W11_CONVENTION_TEST/`. Registrar's check: `LANE_W11_REGISTRAR_VERIFY/`.

### THE RULING, AND IT IS NOT A JUDGEMENT CALL

`W-01` **defines** `(M_gamma s)(v) = W(gamma)·s(v)` on the loop and `s(v)` off it. So `M_gamma`'s
diagonal **is the incidence indicator**, the four classes are the joint level sets of the two
operators' diagonals **by the definition of both**, and

```
Z_k = SUM_v (class character)_v |s_v|^2 = p00 + p10 u^k + p01 v^k + p11 (uv)^k
```

**is reached by substitution. No lemma intervenes. No other outcome was available.** That is what
"restatement" means, and it is prior to K1, prior to B0b, prior to any carrier.
**The corpus owns three-quarters of this and never assembled it:** W-03's *"an analytic fact about
the construction, true before any carrier was built"* (`:191`), W-06's *"not scalar multiplication —
FIBRE-WISE-NESS"* (`:577`), W-10's *"`M_gamma` is literally an element of the gauge group"* (`:409`).

**AND THE SENTENCE CONFLATES THREE CLAIMS OF THREE DIFFERENT STATUSES.** (1) the functional depends
on the state only through `pi` — **restatement**; (2) on the carrier only through `pi` —
**restatement**; (3) `lambda = m(P)` — **theorem with a hypothesis**. Reading A's own wording is
*"the physics does not depend on the complex, **which is why** one short note is publishable."*
**That "which is why" is a non-sequitur and is the whole of Reading A's apparent strength.**

### THE OPERATIVE VARIABLE, NAMED ON THE SEVENTH ATTEMPT — WITH THE GUARD RUN FIRST

Six names have failed in this program, three of them from refuters commissioned to catch misnaming
(W-10 N-7). The ruling grepped the register first and **attached a clause to an existing term
rather than coining a seventh.**

> **`|Z_n|` is a function of `pi` alone IFF the RELATIVE BRANCH OPERATOR
> `Q_n = (branch_F^n)^* (branch_C^n)`, at the tick the record is read, is MULTIPLICATION BY A
> FUNCTION OF THE INCIDENCE CLASS — fibre-wise (`REGISTER:577`) AND class-constant.**

Registrar-verified over 600 cells across four operator families: **AGREE 600, DISAGREE 0**, with
**316 blind and 284 not**, so the test could have failed. **The corpus's convention makes `Q_k`
class-constant diagonal BY CONSTRUCTION** — its diagonal is literally `conj(W_F)^{ka} W_C^{kb}`.
**That sentence is Reading B.** `Q` appears in no register row, and every result in the functional
layer is a statement about it.

### `T`'s CANONICITY — THE REGISTRAR'S OWN DECLARED WEAK POINT, DISSOLVED RATHER THAN DEFENDED

`T` is **not** canonical among all unitaries with `U^L = M_gamma`; that family is
positive-dimensional. **It is canonical under the corpus's own admissibility clause** — S2 audit
CHOICE LEDGER A1 (`:657`), whose clause (c) the ruling **strikes as circular** (it presupposes
fibre-wise-ness, the property at issue) and whose clauses (a) and (b), with locality from S1's own
definition of parallel transport (`S1:52-53`), give a four-line theorem: `U = Lam·T`, COR-F's `T`
times an `(L-1)`-torus of per-vertex phases the carrier does not supply.

**AND THE FINDING NEEDS NEITHER FACT.** The load-bearing result is a **biconditional quantified
over the whole family**, with `U^L = M_gamma` **dropped entirely** — 40 gradient descents over
`U(3)xU(3)`, 18 free parameters, 38/40 converged, positive control `5.49e-12`, **0 non-fibre-wise
solutions**. So the degradation if `T` is not canonical is: from *"the corpus's canonical rival
makes incidence visible"* to *"**every** admissible edge tick does, and the corpus's operator is the
one point of the family at which it does not."* **Logically stronger.**

**AND BOTH HORNS OF THE BRIEF'S DISJUNCTION — MINE — ARE FALSE AS WRITTEN.** The diagonal `L`-th
root `D` restores invisibility, but `D` is not an edge tick: it moves no fibre value and its
diagonal is the class indicator again — **the corpus's own convention at a finer clock**. And
"only the diagonal ones are blind" is false: **correlated non-diagonal pairs are `pi`-blind, 200 of
200, registrar-verified.** The blind set is the **correlated locus**, measure zero for independent
draws — **so every lane in this program that reported "0 of N random draws preserve invisibility"
ran a control that could not have failed.**

### THE COST TO READING B, CARRIED RATHER THAN BURIED

**COR-F's `T` FIRES AT THE TRIVIAL CONNECTION.** `FOUNDING_DESIGN:117-118` and `S2:583`
pre-register *"no formation at trivial connection"*. Registrar-verified at `a = 0`: under
`M_gamma`, `min|Z_n| = 1.000000000000` **exactly** — contact point met; under `T`, `0.429`. At zero
field the transports are pure cyclic shifts and the branches differ because the **paths** differ.
**The edge convention fails the corpus's own pre-registered contact point.** So the corpus has a
*reason* for its convention. **The ruling's distinction, which decides the question and which I
adopt: MOTIVATING A STIPULATION DOES NOT CONVERT ITS ANALYTIC CONSEQUENCES INTO FINDINGS.** Granting
the contact point in full buys the convention a **justification**, not its consequences a
**discovery** — `Z_k = SUM over classes` is still substitution.

### N1 — THE RESULT PROPOSED FOR PUBLICATION — **SURVIVES INTACT**

**N1 is NOT a restatement.** It is a theorem about `(pi, characters)`, and it **survives replacing
`M_gamma`**: under the fibre-wise root `D` — a finer clock, fractional winding, neither branch ever
closed — the identification holds at every tick to `2.5e-16` and the rate is `m(pi)` to `3.9e-07`.
A restatement of `M_gamma` would not survive replacing `M_gamma`. **PUBLISH IT — under two
hypotheses it does not currently carry.** *H1: the relative branch operator is multiplication by a
function of the incidence class — **a stipulation, not a theorem**, and the corpus's own sealed
COR-F exhibits an admissible alternative under which it fails.* *H2: `(conj(W_F), W_C)` generates a
dense subgroup of `T^2`* — without which the limit is the average over the proper closed subgroup,
differing from `m(P)` by `4.8e-04` at the resonant connection and `3.7e-02` at S1's own.
**H2 IS THE ERRATUM AGAINST W-02 (`:162-175`), AND N1 AS REGISTERED DOES NOT CARRY IT.**
**WITHDRAW from N1's framing:** *"the physics does not depend on the complex, which is why one
short note is publishable."* The note is publishable. **That is not why.**

### WHAT READS TWO WAYS, SCORED NEITHER WAY

**THE HOLONOMY READING** — if the corpus's object is *by nature* a closed-loop invariant, `T` is not
a rival at all and mid-path comparison is a category error. **No lane closed it and neither does the
ruling.** What the record shows is that the corpus is **not entitled to it for free: twice, the
warrant offered for the circuit clock is a fact about edges.** CHOICE LEDGER A2 (`S2 audit :658`)
warrants the circuit clock by citing *"edge count is carrier-supplied combinatorics (S1 :16-22)"* —
and `S1:16-22` **is the edge list**; S3's C3 (`:981`) cites COR-F, whose text reads *"edge traversals
**/** circuits"* — **a disjunction cited to close one disjunct**, the edge unit absent from its
alternatives column. All four quotations verified at the bytes. **The verdict survives either
reading, because under the holonomy reading `Z_k = SUM over classes` is still substitution.**

### LINEAGE, AND A DISAGREEMENT LEFT UNADJUDICATED

Every lane, every cross-refuter, the ruling and the registrar are Opus 5. **W-10 says layer twelve;
the brief said thirteen; all five cross-refutations say fourteen. Three numbers for one round, in a
program whose central discipline is applied by number. Recorded, not adjudicated.**

**NOTHING HERE TAKES ANY OF THE PRINCIPAL'S THREE DECISIONS.** It answers the question the second
deferral was for, and it attaches an answer to the second decision: **the Mahler note is
publishable, under H1 and H2 stated, with one framing sentence withdrawn.**

**REOPENS IF:** the holonomy reading is closed in either direction · an admissible operator is
exhibited whose relative operator is class-constant diagonal but which is not fibre-wise, or vice
versa (it would break the biconditional) · or a **lineage-independent** lane reads this row.

---

## W-12 — THE TOPOLOGICAL-CONSTRAINT ROUTE: **CLOSED, ON EVERY CARRIER. THE PROPOSAL WAS THE REGISTRAR'S AND IT IS REFUTED — AND THE REFUTATION UPGRADES N3 FROM ARGUED TO PROVED AND FIXES N1's SECOND HYPOTHESIS AS PURELY ARITHMETIC.**

Commissioned by the principal, 2026-08-17, on an idea borrowed from **DNA supercoiling**: the
linking number `Lk` is an **integer** topological invariant, conserved under every continuous
deformation and changed only by cutting, and the physics is driven by the mismatch it enforces
(`Lk = Tw + Wr`). **The registrar's proposal:** N3 kills every **absolutely continuous** connection
measure — a Wilson action is one — because the resonance structure is Haar-null; a **topological**
constraint is **singular** and so escapes N3's own wording. `S1:102-104` states that Bianchi is
vacuous on K1 because `b2 = 0`; `S4:511-515` owns five carriers with `b2 >= 1` on which it is not,
and no lane ever imposed it. `LANE_W12_BIANCHI/`, 5 files, sealed, all verify.

### THE PROPOSAL FAILS, AND THE FIRST REASON IS THAT BIANCHI IS NOT A CONSTRAINT AT ALL

For a 2-cycle `z`, `SUM_F z_F f(F) = a(boundary of z) = a(0) = 0`. **With the connection given by
edge phases — which is how `S1 §3` defines it — this holds IDENTICALLY for every `a`.** Verified on
B0b over 2000 random connections: `max |SUM_F z_F f(F)| = 1.69e-14`. **Bianchi restricts which
CURVATURE ASSIGNMENTS are realizable; it does not restrict which connections exist.** And it never
pins a single designated holonomy — `W_F` is one face curvature among nine and one relation among
nine quantities leaves any one of them free. `(W_F, W_C)` covers `T^2`: 20000 draws fill **400 of
400** grid cells.

### AND THE SECOND REASON IS A THEOREM THAT CLOSES THE ROUTE EVERYWHERE

> **The map `phi : (R/2piZ)^E -> T^2`, `a |-> (<gamma_F,a>, <gamma_C,a>)`, is a continuous
> homomorphism of compact connected groups, so its image is a CONNECTED CLOSED subgroup of `T^2` —
> hence `{1}`, a circle, or `T^2` — of dimension equal to the R-rank of the `2 x E` incidence
> matrix. For any two DISTINCT designated loops that rank is 2, because a simple cycle has
> `0, +-1` coefficients and two simple cycles are R-dependent only if they share support.
> **So the image is all of `T^2` and `phi` pushes Haar to Haar.**

Verified: rank 2 on every corpus carrier and designation, including an adversarial pair sharing two
of three edges; and the pushforward is uniform on `T^2` to sampling error (`chi2/dof = 1.007, 0.918,
0.914`; **576 of 576** cells occupied on each).

**COROLLARY 1 — NO CARRIER AND NO DESIGNATION CAN CONSTRAIN `(W_F, W_C)`.** Leg A's null is
structural, not a property of B0b. **The topological-constraint route is closed for every complex,
and it cannot be reopened by choosing a different carrier.**

**COROLLARY 2 — N1's HYPOTHESIS H2 IS PURELY ARITHMETIC.** It is a condition on the individual
connection and is **never violable by the carrier or by the loop designation.** The one degenerate
designation that confines the pair — `gamma_C = +- gamma_F`, which CHOICE LEDGER C4's *"any two
loops"* permits — is disposed of twice over: at `gamma_C = +gamma_F`, `uv = 1` and `Z_k = 1` for all
`k`, so `G = {1}` and **W-02's own criterion excludes it**; at `gamma_C = -gamma_F` the pair is
confined to the diagonal circle and H2 genuinely fails, **but only classes 00 and 11 are occupied,
so `P = p00 + p11 xy` depends on the product alone and the subtorus average equals `m(P)` exactly**
— deterministic trapezoid at `2^20`, difference `5.55e-17`. **Whenever formation occurs at all, H2
cannot fail for topological or designational reasons.** This is a strengthening of N1: its second
hypothesis has no structural failure mode.

**COROLLARY 3 — N3 UPGRADES FROM ARGUED TO PROVED, AND FROM K1-SCOPED TO CARRIER-INDEPENDENT.**
W-10's scope table marked N3 carrier-independent on **basis [A], argued only**. Since `phi` pushes
Haar to Haar on every carrier, **any** absolutely continuous measure on connections pushes forward
absolutely continuous on `T^2`, where the resonant set is Haar-null. **So no local action of any
form at any finite coupling can move the rate, on any carrier, for any designation.** Basis [A] -> [T].

### WHAT THIS DOES AND DOES NOT SAY

It does **not** say the borrowed idea was empty: the diagnosis it produced — that the corpus's three
missing admissibility criteria are missing because there is no energy function — is untouched.
**What is now closed is the specific escape hatch N3's wording appeared to leave open.** The wall
that N3 describes is not a feature of K1 and cannot be walked around by changing the carrier.
**A null here reads TWO WAYS and is scored as neither:** the topological route is closed, **or** the
registrar's formulation of it was the wrong one and a different singular constraint — one on the
*state* rather than on the connection — is untested. Nothing here touched the state side.

### REGISTRAR DEFECT, RECORDED RATHER THAN PATCHED

Leg B's diagonal-circle average was first computed by 400000 Monte Carlo draws and printed a
difference of `1.10e-03` — about two sigma of MC noise on a bounded smooth periodic integrand, and
**not evidence of a gap**. Replaced with a deterministic trapezoid, which converges spectrally
there; the difference is `5.55e-17`. The first version and its correction are in the sealed script.

**NOTHING HERE TAKES ANY OF THE PRINCIPAL'S THREE DECISIONS.**

**REOPENS IF:** a singular constraint on the **ready state** rather than on the connection is
exhibited that moves the rate · or a carrier is exhibited whose designated loops are R-dependent
without collapsing the occupied classes to `{00,11}`.

---

## W-14 — THE STATE SIDE, AND A RELEVANCE TEST FOR BORROWED MACHINERY: **THE STATE SIDE IS OPEN AND IS A KNOB, NOT A CHANNEL. THE INVENTORY OF WHAT THIS CONSTRUCTION CAN SEE IS NOW COMPLETE.**

Commissioned by the principal, 2026-08-17, on W-12's own REOPENS clause — *"a singular constraint on
the READY STATE rather than on the connection is untested"* — together with a standing instruction
that borrowed ideas be checked for relevance **at the record level** and **tested, not assumed**.
`LANE_W14_STATE_SIDE/`, 7 files, sealed, all verify.

### THE STATE SIDE IS STRUCTURALLY UNLIKE THE CONNECTION SIDE, AND IS GENUINELY OPEN

W-12 closed the connection side by a theorem: `a |-> (W_F, W_C)` is onto `T^2` with Haar
pushforward, so `lambda` is **constant almost everywhere** in the connection and no absolutely
continuous measure moves it. **On the state side there is no such constant.** Over 4000 uniform
draws on the 3-simplex, `lambda` ranges `-1.331196` to `-0.027776` — **a spread of `1.303420` nats
against exactly `0` across the whole connection torus.** And averaging does not collapse, because
`m` is not affine: `E[m(P(pi))] = -0.673126` against `m(P(E[pi])) = -1.380508`. **There is no N3 for
states, and there cannot be one.**

### BUT IT IS A KNOB, NOT A CHANNEL — AND THAT IS WHAT CLOSES IT

A constraint helps only if it lets the functional **see** something it could not see before. With
`pi` pinned exactly on **B0b, a four-class carrier**, and 60 states differing in **both** within-class
weight and phase:

```
  k        min |Z_k|            max |Z_k|            spread
  1   0.38232295728697   0.38232295728697          3.33e-16
  2   0.98022550160520   0.98022550160520          5.55e-16
 20   0.33432356245583   0.33432356245583          2.78e-16
```

**Exactly blind.** The state reaches the functional only through `pi`. **So a singular constraint on
the ready state selects a `pi` and cannot make the construction sensitive to anything new.** The
"wrong side" possibility is closed — for a different reason than the connection side: not because
the rate cannot move, but because nothing else gets in.

### THE ONE STATE RULE THAT IS NOT A STIPULATION, AND EXACTLY WHAT IT BUYS

Every ready state in this corpus was **chosen**. The exception is **SENSE U**, the uniform state,
where `pi` is fixed by the carrier's own class **sizes**. Under it `lambda` is a function of the
carrier alone — so the carrier does enter. **All seven recomputed values match S4's published
column exactly.** And the channel is narrow:

> **THE CARRIER ENTERS ONLY THROUGH THE MULTISET OF CLASS SIZES, AND S4's OWN TABLE CONTAINS THE
> EXHIBIT UNREMARKED.** `B3` (horn torus), `B1` (K1) and `B2` (K1 both triangles filled) share the
> class multiset `{01:2, 10:2, 11:1}` and differ in **every topological invariant on the page** —
> `chi = 1, 0, 1`; `b1 = 1, 1, 0`; `b2 = 1, 0, 0` — and give the **identical** rate
> `-0.756573585640`, **spread `0.000e+00`**. Nothing about `chi`, `b1`, `b2`, the pinch, the faces
> or the 2-cells survives.

### **THE RELEVANCE TEST FOR BORROWED MACHINERY** — the methodological result of this row

The functional sees **exactly three things: `pi`, `u`, `v`.** Every imported idea acts on some
variable. **Before importing, name the variable and check the functional can see it.**

| the import acts on | status | authority |
|---|---|---|
| the **connection** | **CLOSED.** The map is onto `T^2` with Haar pushforward on every carrier, so no absolutely continuous measure moves the rate | W-12, proved |
| the **ready state** | **OPEN but a KNOB.** It selects a `pi`; it is not a channel and cannot add sensitivity | W-14, exhibited on a four-class carrier |
| the **transport convention** | **THE ONLY LIVE CHANNEL.** Changing it is what makes the incidence visible — at the cost of firing at the trivial connection | W-11 |
| **anything else** | the functional cannot see it at all | the definition of `Z_k` |

**COROLLARY, AND IT SORTS THE TWO BORROWS THIS PROGRAM HAS TRIED.** The only import that can change
what this construction sees is one that changes the transport convention or **adds a dynamics**.
The DNA/topological-constraint borrow acted on the **connection** and was therefore closed before it
was run (W-12) — the relevance test would have predicted it. The kinetic-proofreading borrow adds a
**dynamics**, and is the right kind of import; it remains untested and its literature contact in
this corpus is **zero** (Landauer 0, Hopfield 0, proofreading 0, dissipation 0, entropy production 0,
free energy 0, Bennett 0, detailed balance 0, ratchet 0).

### WHAT READS TWO WAYS

**The narrowness of the carrier channel** reads as *"the construction is blind to the complex, so it
is not about geometry at all"* **or** as *"class-size multiset is exactly the right coarse-graining
and the rest is gauge"*. **Not scored.** W-11's ruling bears on it — the blindness is a consequence
of the convention — but which reading is right is a question about what the object is for.

**NOTHING HERE TAKES ANY OF THE PRINCIPAL'S THREE DECISIONS.**

**REOPENS IF:** an import is exhibited that acts on none of `pi`, `u`, `v` and still moves the rate
(it would refute the inventory) · or the uniform-state rule is shown to be a stipulation after all.

---

## ERRATUM AGAINST W-14 — ITS EVIDENCE WAS A CONTROL THAT COULD NOT HAVE FAILED (registrar error, 2026-08-17)

Raised by the principal, who asked what *"we know it by theorem rather than by exhaustion"* meant.
The audit that question forced is against me.

**W-14 leg B pinned `pi` on B0b and reported 60 states seen identically to `3e-16` as the finding
that the state side is a knob rather than a channel. THAT RUN COULD NOT HAVE FAILED.** `W-01`
defines `M_gamma` diagonal, so `Z_k = SUM_v (class character)_v |s_v|^2` **by substitution**, and
the state cannot enter except through class sums. The run was a check on my implementation of
B0b's class map, not evidence for the claim — **and it is exactly the defect class W-08's isolation
audit named as the commonest fatal one in this program, committed in the row that registers the
test for it.** Under the program's own rule, *"could not have failed" voids a CONTROL, never a
THEOREM*: **leg B is void; the claim stands on the theorem below.**

**THE PROOF W-14 SHOULD HAVE CARRIED, IN TWO LINES.** `Z_k = <s, Q_k s> = SUM_{u,v} conj(s_u)
Q_k[u,v] s_v`.
**(a)** If `Q` has any off-diagonal entry the sum contains a cross-vertex product `conj(s_u) s_v`
with `u != v`, which `pi` does not determine — hold `|s|` fixed and rotate the phase of `s_v` alone
and the term moves. So `pi`-dependence **forces `Q` diagonal**.
**(b)** For diagonal `Q`, `Z_k = SUM_v d_v |s_v|^2`, a function of the class sums **iff** `d_v` is
constant on each class. **QED.**
This also supplies **W-11's biconditional**, which that row verified over 9000 cells rather than
proving. **Both rows now rest on the same two lines.**

**AND THE PROOF PREDICTS WHERE A RUN WOULD SEE SOMETHING, WHICH IS THE TEST LEG B SHOULD HAVE BEEN**
(`LANE_W14_STATE_SIDE/w14_d_proofs.py`, sealed): everything held fixed, **one** off-diagonal entry
added **within a class** — spread over 200 phase draws goes from `2.220e-16` to `1.200e-01`.
**A live failure mode, found exactly where (a) says it is.**

**THE INVENTORY, RE-GRADED.** `connection` — **theorem** (W-12). `ready state` — **theorem** (the two
lines above), not W-14's run. `transport convention` — **theorem** (the same two lines), not W-11's
9000 cells. `anything else` — **definitional**: `Z_k` contains `s`, `W_F`, `W_C` and no other symbol.
**The inventory is closed by proof. W-14's verdict is unchanged and its stated ground is replaced.**

**WHY THIS MATTERS BEYOND THE ROW.** Exhaustion over a sample is structurally blind to measure-zero
sets, and **the interesting sets in this problem are measure-zero** — the resonant connections are
Haar-null (N3), and the `pi`-blind operator pairs are a correlated locus that W-11 found only after
five lanes reported *"0 of N random draws"* and were sampling the wrong set entirely. **This program
has been defeated by exhaustion twice. A closure claim backed by sampling is worth nothing here,
and I made one.**

---

## W-15 — THE REGISTRAR'S ANALYTIC SHAPE, MEASURED: **THE PHRASE TIC IS INHERITED. THE HABIT OF CONVERTING QUESTIONS INTO TWO-VALUED OBJECTS IS THE REGISTRAR'S, AT 2.5x AND 6x THE PREDECESSOR'S RATE — AND IT IS THE DEFECT THE PROGRAM'S FOUNDING QUESTION HAD.**

Raised by the principal, 2026-08-17, from a prose complaint that escalated into a claim about
reasoning: *"You're locked to an x/y way of thinking about almost everything."* Measured on this
register, split at W-07, the Fable 5 / Opus 5 boundary. `LANE_W15_BINARY_AUDIT/`, sealed.

| construction | Fable 5 /1k words | Opus 5 /1k words | ratio |
|---|---|---|---|
| `rather than` | 1.50 | 1.53 | 1.02 |
| `X, not Y` | 3.60 | 2.51 | **0.70** |
| `versus` / `vs` | 0.15 | 0.22 | 1.44 |
| **biconditional (`iff`)** | 0.30 | 0.76 | **2.53** |
| **`two ways` / `two readings`** | 0.30 | 1.75 | **5.85** |

**THE PHRASE-LEVEL TIC IS HOUSE STYLE AND IS NOT THE REGISTRAR'S** — on `X, not Y` the registrar is
**below** the predecessor. **What is the registrar's is structural: biconditionals at 2.5x and
two-way readings at nearly 6x.** The defect is not *talking* in x/y. It is **converting questions
into x/y**, because a two-valued question is decidable by a computation and an open one is not.
Every headline the registrar wrote has that shape: attained/approached (W-07), decay/floor (W-08),
three-class/four-class (W-09), carrier-independent/K1-scoped (W-10), Reading A/Reading B (W-11),
closed/open (W-12), knob/channel (W-14). **Sixteen "reads two ways, scored neither" verdicts in
eight rows is a template, not a judgement** — it wears the form of restraint while performing a
conversion.

### AND THE PROGRAM'S FOUNDING QUESTION HAS THE SAME DEFECT, WHICH IS WHY THIS IS A FINDING

*"A forced crossing — does a durable record live INSIDE the carrier, or must it be adjoined
OUTSIDE?"* **That is a dichotomy, and W-05 established it was malformed:** *"THE SLOT IS ALREADY
INSIDE THE CARRIER … S3 proved `dim R >= 4` by the two-non-parallel-vectors argument and then looked
for the `C^2` OUTSIDE instead of inside"* (`REGISTER:415-422`). **The corpus was spent on an
inside/outside binary that was never real.** So the instrument this registrar has been auditing the
program with carries the program's own defect — **the W-04 pattern (*"the audits committed the exact
defect they convicted the builds of"*) recurring one floor up, structurally rather than locally.**

### THE DISCRIMINATOR, SINCE "USE FEWER DICHOTOMIES" IS NOT A RULE

> **DID THE MATHEMATICS HAND ME THE TWO BRANCHES, OR DID I NAME THEM?**
> `diagonal / non-diagonal` was forced and has a proof under it. `knob / channel` was coined — the
> words are the registrar's and nothing guarantees the options are exhaustive. **Every coined pair
> is a place to look for a third thing.**

**Corroborating evidence from the corpus's own quality ordering:** the two most useful artifacts
this registrar produced are the ones that are **not** two-valued — W-10's **four**-valued scope
table with its BASIS tags, and W-14's relevance test, a **three**-way inventory over `pi`, `u`, `v`.
Both reached further than any of the oppositions.

**REOPENS / APPLIES TO:** every coined pair in W-07 through W-14 is now flagged for a third-option
check. **The first three to check, in order: `knob / channel` (W-14), `finding / restatement`
(W-10 §0.4.1, which W-11 in fact split THREE ways and scored better for it), and
`theorem / exhaustion` (which omits the middle case that carries most real evidence — exhibited
with a live failure mode).**

---

## ERRATUM AGAINST W-11 — ITS HEADLINE NAMES THE WRONG OBJECT, AND TWO LANES SAID SO AND WERE OVERRIDDEN (registrar error, 2026-08-17)

W-11 registered: *"CARRIER-INDEPENDENCE IS A RESTATEMENT OF THE TRANSPORT CONVENTION."*
**Two W-11 lanes returned `REFUTED_AS_POSED` against that framing, independently, and the synthesis
folded them into a seven-to-one majority for READING_B.** `LANE_W11_R_BLIND` (a blind rebuild that
never opened the registrar's code) and `LANE_W11_R_CLOCK` both wrote: **there is no transport
convention to restate.**

**VERIFIED BY THE REGISTRAR** (`LANE_W16_ADVANCE_LATTICE/`, sealed):
`||T_F^3 - M_dF|| = 6.18e-16`, `||T_C^3 - M_c|| = 4.34e-16`. **`M_gamma` lies inside the cyclic group
`T` generates — the corpus's operator is a POWER of COR-F's.** There is **one** transport and **two
schedules on it**: both conventions are rays in one family `Y(mF,mC) = <T_F^mF s, T_C^mC s>`, the
corpus's being `(L_F k, L_C k)` and COR-F's `(n,n)`.

**AND THE OPERATIVE VARIABLE IS THE ADVANCE LATTICE.** Over a `26x26` lattice with 64 same-`pi`
states, one variable moving: **invisible cells `81`, advance sublattice `L_F Z x L_C Z` `81`,
SET EQUALITY `True`**, max spread off the lattice `9.085e-01`. **Invisibility is a property of
WHERE THE RECORD IS READ — whether a branch is mid-loop — not of a choice of transport.**

**W-11's VERDICT SURVIVES; ITS NAME DOES NOT.** Carrier-independence is still not a finding — it
holds exactly on the advance lattice and fails everywhere else, and the corpus reads only there.
**Corrected text of record:** *carrier-independence is a consequence of reading the record only on
the advance lattice `L_F Z x L_C Z`, where both branch operators are simultaneously diagonal.*
**This is the SEVENTH consecutive misnaming of the operative variable in this program, and the
first one where the correct name was supplied, in writing, by lanes the registrar overruled.**

---

## W-16 — A PROCESS AGAINST THE BINARY, PROPOSED FOR THE PRINCIPAL'S SEAL: **THE ESCAPE HATCH WAS NOT MISSING. IT WAS OUTVOTED.**

Commissioned by the principal, 2026-08-17: *"Is there a process more than a log note that can be
used to free ourselves from this tyranny of the binary?"* **A log note will not do it, and this
corpus already proves that** — W-08's isolation audit found three build lanes wrote isolation
ledgers and it did not stop them, with five of seven fatal confounds sitting in the arm the lane's
own ledger named as decisive. **A check that requires self-report gets self-reported.**

### THE FAILURE, MEASURED

Across all workflow journals: **46 agent results, 30 carrying a verdict. `REFUTED_AS_POSED`
returned 2 times (7%). `UNDECIDABLE_AS_STATED`, present in every schema, returned 0 times.**
The mechanism: **the brief poses the binary, which RECRUITS.** Eight of ten lanes answer inside the
frame; the two who reject it are a minority the brief created; the synthesis reads verdicts as
votes; the majority wins; the register records it. **Frame-level findings are destroyed by a step
the registrar wrote.**

**AND A SCHEMA DEFECT UNDERNEATH IT.** `REFUTED_AS_POSED` was an ALTERNATIVE to answering. A lane
that wants to say *"B, and the question is also wrong"* **could not**. Both objectors had to
surrender their answer to raise the objection. **Frame-refusal was made to compete with answering.**

### THE FOUR GATES — mechanical, executed, greppable

1. **THE FRAME LANE RUNS FIRST AND ALONE.** Its brief carries the QUESTION and no candidate
   answers. Its only deliverable is the enumeration of options, each tagged **DERIVED** (with the
   citation that forces it) or **COINED** (a registrar word). Answer lanes are commissioned against
   ITS enumeration. This removes the binarization from the one point where it occurs.
2. **`frame_objection` BECOMES A SEPARATE FIELD, NOT A VERDICT.** A lane answers *and* objects.
   Removing the competition is most of the fix.
3. **A FRAME OBJECTION BLOCKS SYNTHESIS AND IS NEVER A VOTE.** The round re-poses and re-runs, or
   the register headline records the question as unresolved.
4. **AT REGISTRATION, MECHANICALLY:** grep the round's journal for frame objections; **no register
   row may close a question over a frame objection it does not name and address.** This is the
   pointer rule (custody §1) applied to dissent, and its absence is detectable by `grep` and not by
   the registrar's honesty.

### WHAT THIS DOES NOT FIX

**The registrar still writes the frame lane's brief.** Keeping candidate answers out of it is as far
out of the registrar's hands as this goes without a different model — and the lineage-independent
lane W-03 specified still does not exist for anything after W-06. **Whether these gates generalise
past this program is untested.** And gate 1 is itself a coined structure; per W-15's own
discriminator it is a place to look for a third thing.

**ADOPTION IS THE PRINCIPAL'S ACT, NOT THE REGISTRAR'S.** `FOUNDING_DESIGN_V001.md` reads *"PROPOSED,
NOT ADOPTED. Governing only at the principal's seal"*, and no principal act is on disk. **This row
proposes an amendment to custody §1 and does not make one.**

**REOPENS IF:** a round runs under all four gates and still destroys a frame objection · or a frame
lane is shown to inherit the registrar's shape through its brief despite carrying no answers.

---

## W-13 — N1's CONVERGENCE, SETTLED: **TRUE AT THE CORPUS'S OWN PUBLISHED CONNECTION BY BAKER'S THEOREM. FALSE ON A COMEAGER SET AND AT ALL FOUR PUBLISHED RESONANT PAIRS. THE IDENTIFICATION IS NOT NEW — THE THIRD TIME THIS PROGRAM HAS RE-DERIVED A NAMED RESULT.**

The one open mathematical question in the corpus and the ground of the principal's second standing
decision. Four build lanes, four refuters, a ruling that re-derives what they disagree on and
**decides against three of them.** 9 agents, 0 errors. `W13_N1_CONVERGENCE_V001.md` sha256 `a0d131762263bc78b42a7cd2dec45565bb7486991bd29bbf6e4d9ce9bce84097`;
lanes `LANE_W13_*`; registrar's own check at `LANE_W13_REGISTRAR_VERIFY/`.

### THE SHARP HYPOTHESIS — THREE CONDITIONS, AND THE THIRD IS THE ONE THAT DECIDES

`(H2)` `L(theta) = {0}` · **(D1)** a polynomial **homogeneous** Diophantine bound on
`(alpha, beta)` · **(D2)** a polynomial **inhomogeneous** bound on `dist((u^k,v^k), Z(P))`.
**(D1) and (D2) are independent and neither follows from H2.** W-11's H2 alone is **not
sufficient**. And **(D2) is a joint condition on the connection AND the ready state**, because
`Z(P)` is fixed by the state — so the hypothesis that decides N1 is not a condition on the
connection at all. Priority belongs to `LANE_W08_M1_IDENTIFICATION/M1_08_THEOREMS.txt` T2(c),
sealed 2026-08-16, which named it and which the register never carried.

### **N1 IS TRUE AT `f = 1.0, c = sqrt(2)` — UNCONDITIONALLY**

**(D1) and (D2) both follow from Baker's theorem on INHOMOGENEOUS linear forms in logarithms
(Baker III, Mathematika 14 (1967) 220-228) whenever the two loop ANGLES are algebraic reals with
irrational ratio and the ready state has algebraic weights.** `f = 1.0, c = sqrt(2)` is such a pair
— **W-10 N-4's "the only generic connection the corpus publishes", and the pair S4:603 used to
verify its entire `lambda` column.**

**Two lanes ruled the opposite and were overturned.** Lane C: *"N1 is not verified at any named
connection in this corpus and cannot be with present mathematics."* Lane L: *"no effective
Diophantine result covers `u = e^{-i}`, `v = e^{i sqrt2}` … Baker requires algebraic arguments."*
**Both false, on one inference:** *u and v are transcendental, therefore Baker does not apply.*
**The transcendence of `u` is not an obstruction — it is the hypothesis.** What enters the linear
form is the **angle** `f`, not `e^{if}`. **Lane L's refuter confirmed the error instead of catching
it.**

### AND IT IS FALSE ON A COMEAGER SET — MEASURE AND CATEGORY DISAGREE

**THEOREM (Baire).** There is a dense `G_delta` in `T^2` on which **H2 holds** and
`liminf_N A_N = -infinity`. Three independent proofs, one explicit ladder, verified over four
decades: perturbation falling like `1/(2k)` while the depth is held at exactly **3 nats per unit
`k`** (`-3.0627, -3.0081, -3.0004, -3.0000`). **The failure set is Lebesgue-null AND comeager.**
**The corpus's entire N3/W-12 apparatus is measure-theoretic and has no vocabulary for the second.**
**And no counterexample can have algebraic angles** — so the corpus's own pair is safe, and the
corpus's numerics could never have found the failure.

**THE THREE-WAY STATEMENT OF RECORD:** algebraic angles with irrational ratio — **TRUE** (Baker) ·
Lebesgue-a.e. connection — **TRUE** (Borel-Cantelli) · a comeager set — **FALSE** (Baire) · both
angles rational multiples of `pi`, which is **all four published resonant pairs** — **FALSE** ·
`pi` on a curve stratum, **which is S1's own registered ready state** — **OPEN, and it is a
one-variable Sudler product where the classical literature applies.**

### NOVELTY: **NOT NEW, FOR THE THIRD TIME**

*"The rate is a logarithmic Mahler measure"* is the normal state of affairs in this corner —
Lind-Schmidt-Ward 1990, Kenyon-Okounkov-Sheffield 2006, Lyons 2005. **Worse: `Omega_N` is the
transfer product of a scalar quasi-periodic cocycle and `lambda` is its LYAPUNOV EXPONENT, and
using Jensen and the Mahler measure to evaluate it is the opening move of Herman 1983** (*Comment.
Math. Helv.* **58**, 453-502). **Forty-three years old, in every survey of one-frequency
Schrödinger operators, and the word "Lyapunov" occurs twice in the whole sealed corpus, in no
register row and no lane directory.** After Hepp/Bell (W-04) and Cassaigne-Maillot, this is the
third. **Score the novelty claim weak and leaning negative.**

**AND S1's OWN REGISTERED READY STATE IS A 65-YEAR-OLD NAMED PROBLEM.** `p = (1/2,0,0,1/4,1/4)`
gives `pi = (0,0,1/2,1/2)`, so `P = (1/2) y (1+x)` and **`|Z_k| = |cos(pi k alpha)|` exactly**
— registrar-verified to `3.33e-16` over `k <= 2e5`, with the average approaching
`m(P) = -log 2 = -0.693147181`. **That is a Sudler product** (Sudler 1964; Erdos-Szekeres 1959;
Lubinsky 1999). **No lane looked it up.**

---

## ERRATUM AGAINST W-10 — N2 IS STATED WITHOUT ITS HYPOTHESIS, AND N1 AND N2 ARE ONE RESULT (registrar error, 2026-08-17)

`REGISTER:196-197` and `W10_SCOPE_TABLE_V001.md` §3.2 state W-03/N2's multiset theorem —
*"24 of 24 permutations invariant"* — **with no connection qualification**, and W-10 marked it
**CARRIER_INDEPENDENT**. **Registrar-verified, one variable moving (the permutation), same
connection, same estimator, `N = 2e6`, K1's registered weights:**

```
f=1, c=sqrt2   GENERIC     spread 3.670e-06   (Birkhoff noise; all -> m(P))
f=2.0, c=1.1   RESONANT    spread 7.247e-04   6 distinct values
f=pi, c=pi/2   ORDER 4     spread 5.579e-02   2 distinct values
```

**The `S_4` invariance is a theorem about `m(P)`, not about `lambda`.** It holds **exactly where
`lambda = m(P)`, i.e. exactly under W-13's hypotheses.** What survives at *every* connection is only
**W-03's own involution `00<->11, 10<->01`** — registrar-verified at `0.000e+00`, `0.000e+00`,
`1.110e-16` at the three connections above. **N1 and N2 are one result with one hypothesis.**

**AND THE CUSTODY FAILURE IS THE PROGRAM'S NAMED ONE.** This was sealed on disk in
`LANE_W10_B_MULTISET/b4_involution_labels.OUT.txt` leg E on 2026-08-16 — *"W-03's 'the incidence
labels are invisible' is a statement about the GENERIC connection, and the corpus computed almost
nothing at a generic connection"* — attacked and **strengthened** by its own refuter, and entered
in **no register row**, while W-10's scope table states the unqualified opposite one row away.
**Two of the four results this corpus proposes to publish were entangled, the entanglement was
found ten hours before W-13 opened, and it was under-read. Again.**

**REOPENS IF:** a counterexample with algebraic angles is exhibited (it would refute W-13's Baker
argument) · or the Sudler literature settles the curve stratum, which would close the one line
still open.

---

## W-17 — THE FRAME INSTRUMENT, VALIDATED BY RETRODICTION: **IT WORKS AT TWO FIFTHS OF ITS SIZE. AND ITS ONE CERTIFIED CATCH IS THAT THE SENTENCE WHICH LICENSED THE PROGRAM'S CENTRAL STAGE IS AN INVALID INFERENCE THAT SIXTEEN REGISTER ROWS NEVER EXAMINED.**

Directed by the principal, 2026-08-17: a process, applied at route decisions, that challenges the
binary frame — testing not only whether there are more options but **whether the binary is false**.
Instrument: `FRAME_CHALLENGE_V001.md`. Validation: **retrodiction under reading cutoffs** over four
route decisions, each lane forbidden to read the corpus past the point its decision was taken, plus
a cutoff auditor and an instrument auditor told to argue the instrument is ceremony. 7 agents,
0 errors. `W17_INSTRUMENT_VALIDATION_V001.md`, sealed. Reduced instrument: `FRAME_CHALLENGE_V002.md`.

### THE SUBSTANTIVE FINDING — **T1/F5 AT R1, AND IT IS NEW AGAINST THE WHOLE CORPUS**

`FOUNDING_DESIGN_V001.md:63-65`: *"An inductive limit of finite objects is not finite — **which is
precisely how it escapes recurrence**."* That sentence is the founding design's **single stated
escape** from its own §4 obstruction, and `:99-102` sends stage S3 out *"with the inductive-limit
template as the starting point."* **It is the sentence that licensed the program's central stage.**

**IT INFERS NON-RECURRENCE FROM NON-FINITENESS, AND NON-FINITENESS IS NECESSARY, NOT SUFFICIENT.**
Registrar-verified, needing no complex, no gauge group and no fibre — only a commensurate spectrum:

```
   dim = 10, 100, 10000, 1000000     E_n = n     |A(t = 2 pi)| = 1.000000000000000
   contrast, incommensurate spectra: max|A| over t in [1,1e4] = 0.9476 / 0.9618 / 0.9592
```

**An infinite commensurate spectrum recurs exactly, at every dimension including the limit.**
Two lines of arithmetic. **And it was never run:** across all **1696 lines** of this register,
W-01 through W-16, occurrences of **`inductive limit`: 0. `quasi-local`: 0.** Sixteen rows, eleven
adversarial, **and not one examined the escape route that licensed S3.** W-08's *"the founding
obstruction is false as an inference"* attacks a **different** defect — single-cell `|Z_k|` versus
the product — and neither restates the other. **This attacks the ESCAPE, not the obstruction.**

**AND IT IS THE ONE CATCH NO LEAK REACHES**, which matters because the round was contaminated (below):
the instrument's worked examples cover F2 and F4 only; **F5 has no worked example anywhere.**

### THE INSTRUMENT IS PART FAULT MACHINE, AND THE CONTROL THAT PROVED IT WAS OMITTED FROM THE ROUND

The ruling ran the control the round did not: **point the instrument at frames known to be sound.**

| frame | F1 | F2 | F3 | F4 | F5 | fired |
|---|---|---|---|---|---|---|
| **PARITY** (evens / odds) | FIRE | **FIRE** | ok | ok | ok | **2/5** |
| **`diagonal / non-diagonal`** on `U(3)` | FIRE | **FIRE** | **FIRE** | indeterminate | ok | **3.5/5** |

**The second control is W-15's own named paradigm of a binary the mathematics handed over** —
*"`diagonal / non-diagonal` was forced and has a proof under it"* (`REGISTER:1509-1511`).
**F2 fires on evens versus odds**: `f(n) = n+1` carries the odd arm exactly onto the even arm,
symmetric difference `2` of `100000`. **F2 fires on diagonality**: for a 3-cycle `P` and any diagonal
`D`, `(P·D)^3` is diagonal — off-diagonal norm of `U^3` **`0.000e+00`** over 20000 draws, on a
positive-dimensional slab. **A map exists between almost any two arms. F3** voids a predicate whose
cell is measure-zero, and `mu(diagonal) = 0` under Haar while the predicate partitions `U(3)`
exactly — **and this corpus's own interesting sets are all measure-zero** (N3's resonances, W-11's
correlated locus). **F4's verdict is chosen by the lane**: two defensible presupposition sentences
give opposite answers on the same frame.

**AND F1 AS WRITTEN IS TRIVIALLY SATISFIABLE** — two arms always lie in some space. The missing
clause is **EXCLUSION**: exhibit a point in **neither** arm. Parity: `0 of 100000`. Diagonality:
`0 of 20000`. **Both controls clear under it, and F1 keeps every productive result of the round.**

### **RULING: ADOPT TWO TESTS, NOT FIVE.** `FRAME_CHALLENGE_V002.md`

**KEEP `T1` (the null option), run first** — it produced the round's only certified catch at a cost
of two lines. **KEEP `T2` (embed), amended with EXCLUSION + RELEVANCE + PROVENANCE.**
**DELETE `F2` and `F3`. DEMOTE `F4`** to a grep gate: keep the requirement to *write* the
presupposition, drop the requirement to *score* it.

### REGISTRAR DEFECT — **I CONTAMINATED MY OWN EXPERIMENT**

`FRAME_CHALLENGE_V001.md:54-56` carries **R1's own F4 answer as a worked example**, citing a register
row far past that lane's cutoff — and the brief **ordered every lane to read the instrument first.**
The R1 lane detected this itself and refused to certify its own retrodiction, writing:
*"Availability is demonstrated. Discoverability is not."* **A second leak: the session auto-memory
line carried "forced crossing does not exist" — R1's answer — at turn zero.** **Worked examples in a
frame instrument are leak vectors.** V002 carries none.

### WHAT READS TWO WAYS

**Can a frame lane's brief be kept clean by THIS registrar at all?** The round says no on the first
attempt and the fix is mechanical (delete the examples), **or** it says the contamination is
structural because the registrar writes the brief. **Not scored.** The lineage-independent lane
W-03 specified still does not exist for anything after W-06, and **this is layer fourteen of one
block.**

**ADOPTION IS THE PRINCIPAL'S ACT.** `FOUNDING_DESIGN_V001.md` reads *"PROPOSED, NOT ADOPTED.
Governing only at the principal's seal"*, and no principal act is on disk.

**REOPENS IF:** a sound frame is exhibited on which `T1` or amended `T2` fires · or the founding
escape inference is shown to have been tested somewhere in the corpus after all.

---

## W-19 — ATTEMPT TWO, FIRST COMPUTATION: **NO CARRIER OF THIS CLASS WORKS AT ANY SIZE. THE PLATEAU IS A GAUSS IDENTITY. AND THE RESIDUE IS PHASE-INDEXED — ZERO BITS ON THE ELECTRIC RECORD, ONE FULL BIT ON THE MAGNETIC, AND THE COUPLING DECIDES WHICH.**

Commissioned under R-1 as amended. **First row entered under the gates adopted 2026-08-17**: frame
objections reported first and never as votes, and a next step named or the row is returned.
5 agents, 0 errors. `W19_CARRIER_THRESHOLD_V001.md` sha256 `abf83e5b971e9d394abb847e090b6029a32151d5f6fe110e96350faf4b7ef7dd`; lanes `LANE_W19_*`; registrar's own
check at `LANE_W19_REGISTRAR_VERIFY/`.

### THE FRAME OBJECTIONS, FIRST AND SEPARATELY — **BOTH SUSTAINED**

**The question named a minimum without naming the class it minimises over**, and the class does all
the work: degree-2 allowed gives 9 · min degree 3 with multi-edges 9 · simple 12 · girth >= 4 15 ·
girth >= 6 21 · nested-from-both-endpoints unreachable — **every one a correct answer to the question
as written.** And *"report a THRESHOLD, not an impression"* — **the registrar's own instruction** —
rewarded a number and penalised the finding that the number is not the object.

**THE MEASUREMENT THAT SETTLES IT.** Hold carrier, state, coupling, algebra, fragment count and
`delta` fixed; move **only the partition** into disjoint fragments:

```
heawood (L=21)   R_delta on the chosen BFS-cut partition : 5 of 5
                 over 200 random equal-size disjoint partitions : mean 0.400, max 2, ZERO in 127
```

**`R_delta` as computed is a property of the partition, and the partition was chosen — correctly and
knowingly — to be the one the Gauss law guarantees.**

### THE NUMBER, DELIVERED AND MARKED — AND LANE A's PROOF IS FALSE

`L = 12` simple (`tri_chain12`, V=8, cubic, girth 3), `L = 9` multigraph. **Lane A claimed 21
(Heawood) and marked it PROVED**; the proof conflates *girth through `l` >= 6* with *global girth
>= 5*, and cycles avoiding `l` are unconstrained. Both counterexamples were run **through lane A's
own code at lane A's own coupling.** Exhaustive: no simple graph on `V <= 7` with min degree 3
reaches `d = 5`; `V >= 8` forces `L >= 12`; **2520 of 19355 labelled cubic graphs on 8 vertices
attain it.** General floor `L_min = ceil(3(P+2)/2)`.

### **BUT UNDER A CRITERION THAT CAN FAIL, NO CARRIER OF THIS CLASS WORKS — AT ANY `L`**

Pin the criterion: **P1** gauge-invariant system algebra · **P2** fragments pairwise disjoint ·
**P3** `|F| <= |E|/2` · **P4** four points · **P5** *the plateau must be able to fail.*
**The obstruction is structural, not computational, and two halves exhaust the class:**

**(1) WHERE THE GAUSS LAW CARRIES THE PLATEAU, P5 FAILS IDENTICALLY. REGISTRAR-VERIFIED:**
if `F` contains a `u`-`v` cut of `G - l`, then `Z_l · prod_cut Z = I` on the physical sector —
**`0.000e+00`** — so `I(S:F) = H(S)` **exactly, for every state.** Measured on three independent
Haar physical states sharing nothing but the constraint: `I/H(S) = 1.000000` on all three.
The ruling's own arms: ground state at `g^2 = 0.50`, ground state at `g^2 = 3.00` **where
`H_elec(S) = 0.001283` — an EMPTY record** — and two Haar states, **all giving `1.000000 x5`.**
**"Could not have failed" voids a control, and this was being read as evidence.**

**(2) WHERE P5 CAN BE SATISFIED, THE PLATEAU HAS NO GAUGE CONTENT.** On `d = 1` carriers a plateau
is carried by the state and does fail — `R_delta = 5` for a constructed electric GHZ, **`0` for the
ground state at every coupling and for Haar.** And what it certifies is **a classical repetition code
in the X basis, whose curves are identical on `L` bare qubits with no Gauss law and no plaquettes.**
**Zero variables moved with respect to gauge invariance.**

### **THE FINDING: THE BOUNDARY-ALGEBRA DEPENDENCE IS REAL AND IT IS PHASE-INDEXED**

One object moves — the algebra assigned to the system link. `EXT` = full matrix algebra in the
extended Hilbert space; gauge-invariant = `alg{X_l}`, the only non-trivial gauge-invariant
subalgebra of a single link.

| record | `EXT/H(S)` | gauge-invariant`/H` | **difference** |
|---|---|---|---|
| **ELECTRIC**, non-enclosing `F` | `1.000000000` | `1.000000000` | **`0.000000000` bits, exactly, on every fragment** |
| **MAGNETIC** (the exact `g^2 -> 0` ground state) | `1.000000000` | **`0.000000000`** | **`1.000000000` bits. Full swing.** |

**Small `g^2` is where the ground state is magnetic and the algebra disagreement is one full bit.
Large `g^2` is where it is electric and the disagreement is exactly zero.** So *which boundary
algebra* is **not a free convention — it is undetermined precisely in the phase the dynamics selects
at small coupling**, and Gauss-forced in the other. **This is W-04's residue, located, with a
Hamiltonian and a coupling underneath it for the first time — and it is the only thing in this round
that required attempt two's genuine dynamics to say.**
Consequence recorded: the algebra choice also moves the plateau count, so the answers now on the
table are **8, 9, 12, 15, 21 and unreachable — all correct under different unstated conventions.**

### NEXT STEP — NAMED, AS THE STANDING RULE REQUIRES

**ONE RUN. `Z_2` GAUGE + STATIC CHARGE ON `tri_chain12`, MAGNETIC SYSTEM REGION, CRITERION PINNED IN
WRITING BEFORE ANY STATE IS BUILT.** `S` = the triangle `{1,2,3}` — the smallest region on a simple
min-degree-3 carrier whose gauge-invariant algebra is **non-abelian and carries a Wilson loop**.
Nine environment links, four disjoint fragments **declared before the state is computed**.
**The isolated variable is the charge sector and nothing else**: `G_v = +1` everywhere versus
`G_v = -1` at two vertices, arms byte-identical apart from the sign pattern — **and the diff printed**.
Physical dimension `2^13 = 8192` with matter against `2^22` on Heawood, a **512x saving**, so there
is no ceiling. **And the question is INVERTED: do not ask where the plateau appears — ask where it
can fail.**

**REOPENS IF:** a carrier in this class is exhibited satisfying P1-P5 · or the phase-indexing of the
algebra disagreement fails to reproduce on a second carrier.

---

## C-1 — **A CLAIM, NOT A FINDING: THE RECORD IS GAUGE-VARIANT.** (registrar, 2026-08-17)

**A new row type, entered at the principal's direction** — *"if we engage in fitting we find it, we
slap our own hands and get on with it; we can't tiptoe around the process if we hope to learn
something."* **Detection changes the calculus:** the sham-target test caught a live doubt in one
script, so the cost of a wrong claim has fallen and the optimal boldness has risen. **A CLAIM row is
a commitment stated flat so it can be shot at.** It is not evidence and must never be cited as one.

> **C-1. THE RECORD IS GAUGE-VARIANT. That is why every gauge-invariant measurement this program
> has made has come back either FORCED or FLAT.**

**THE EVIDENCE, ALL ALREADY ON DISK.**
- **W-19:** the redundancy plateau in the gauge-invariant channel is a **Gauss identity** —
  `I(S:F) = H(S)` for every state, coupling and history. Forced; carries no information.
- **W-19:** its only live control lay **entirely in the gauge-variant part**, recorded there as a
  defect of the lane rather than as a result.
- **FT-1** (`LANE_FT_SHAM/`, sealed): across the whole coupling sweep the gauge-invariant channel
  swings **exactly `0.000000`**, while gauge-variant descriptions swing `0.021611` to `0.990639`.
  Invariance checked, not asserted: `Z` commutes with every Gauss operator at `0.000e+00`, `X` fails
  at `1.6e+01`.
- **Attempt one:** `Z_k` moved, but the crossing it motivated adjoined a record slot **carrying no
  gauge action at all** — S3's own flag F6.
- **AND THE CORPUS FLAGGED IT ON DAY ONE AND NEVER READ IT.** **COR-J**, sealed in the S3 audit:
  *the premise "the record must be gauge-invariant" is undeclared, load-bearing, and applied
  asymmetrically — fatal inside the complex, vacuous on the added slots.* **Attempt one built a
  gauge-variant record, noticed the inconsistency, and excused it. Attempt two has been measuring
  the invariant channel and finding nothing there.** This is the program's signature failure —
  a sealed correction, unread, for the whole life of the program.

**WHAT IT WOULD MEAN.** A gauge-variant record lives in the **edge modes** — the degrees of freedom
that must be added to factorize a gauge theory's Hilbert space (Donnelly-Wall). That is **W-04's
located residue**, it is the principal's **boundary**, and it is TERRITORY_MAP region **R-III**.
**Four objects that have been circling each other are one object.**

**THE FALSIFIER, AND IT IS CHEAP.** Exhibit a **gauge-invariant** quantity carrying record structure
that is **not a constraint identity**. Every lane that has measured an invariant channel has had the
opportunity to produce one and none has. **One counterexample kills C-1.**

**FITTING DISCLOSURE, PER THE STANDING GUARD.** C-1 was assembled **after** the measurements, from
findings gathered for other purposes. It is exactly the shape of a fitted story. It is entered as a
CLAIM for that reason — **so that the fitting tests can be pointed at it** rather than at a
conclusion already dressed as a result. **What the registrar got wrong by hedging:** the
`0.000000` appeared in the registrar's own sham output and was reported as a limitation of the test.
**It is the result.**

**NEXT STEP.** W-20's ledger arms are already pointed at this without having been designed for it:
its ARM 1 removes the gauge structure and its ARM 3 varies the boundary's formation. **Add the
falsifier as a standing arm in every subsequent round: measure a gauge-invariant channel and try to
make it carry something that is not forced.**

---

## W-22 — THE FRAME CHALLENGE ON TWO INHERITED BINARIES: **BOTH ARE TWO-POINT SAMPLES, AND WHAT THEY EXCLUDE IS A VALUE GETTING ITS START.**

Commissioned by the principal, 2026-08-17: *"let's question all imported assumptions — variant /
invariant — allow / require — we shouldn't be afraid to ask — could we be looking at a point where
certain values are just getting their start."* First application of `FRAME_CHALLENGE_V002` to
inherited machinery. `LANE_FC_BINARIES/`, sealed.

### **VARIANT / INVARIANT — EXCLUSION CLAUSE FIRES.**

On an **open** carrier — six bulk vertices constrained, one dangling link whose far end is boundary
and carries no Gauss operator — the boundary charge `Q = Gauss(6)` is verified **central** against
every bulk constraint at `0.000e+00`, with `Q^2 = I`, giving exactly **two superselection sectors**.
All twenty single-link operators then sort by two **computed** predicates into **three** categories:

```
 INVARIANT (bulk observables)   10 operators
 VARIANT (genuinely junk)        9 operators
 SECTOR-CHANGING                 1 operator   -- X_9, on the dangling link
```

**`X_9` lies in NEITHER named arm.** It fails to commute with the bulk constraint, so the binary
files it under *variant* and discards it — **and it is the unique operator that moves between
superselection sectors, i.e. that creates or destroys boundary charge.** The classification throws
away the one thing that makes a value.

**AND THAT IS THE PRINCIPAL'S QUESTION IN THE ARITHMETIC.** A superselection sector is a value that
is or is not there, with no superposition between. `X_9` is the operator that starts one. **What
variant/invariant cannot see is precisely a value getting its start.**
*Caveat of record: `X_9` is unique because the construction has one dangling link — the COUNT is a
property of the construction. The three-way SPLIT is not; it follows from `Q` being central.*

### **ALLOW / REQUIRE — FAILS T1 AND T2, AND NO COMPUTATION IS NEEDED.**

**T1, the null option:** both branches presuppose the value **already exists**, to be permitted or
forced. If it **originates** at the surface, neither obtains and the question is malformed there.
**T2, embed:** the modal axis is not even two-valued — **forbid** is missing — so allow/require is a
two-point sample of a three-point axis. **And origination is not on that axis at all**: it is
generative, not modal. The binary samples two of three points on one axis while the live option sits
on a different axis entirely.

**WHAT THIS COSTS A REGISTERED INFERENCE.** The predecessor found alpha **allow-side** — permitted,
forced by nothing — and `FOUNDING_DESIGN §2` read that as the warrant for treating alpha as an
INPUT: *"a process that leaves the coupling's slot open is exactly what a process should look like
when the coupling comes from outside."* **Under the third option that inference does not go
through.** A slot that looks open because nothing forces the value is **indistinguishable** from a
slot where the value is being made, to any test that asks only whether something is forced.
**Allow-side and origination have the same signature under the test that produced the finding.**

### WHAT THIS DOES AND DOES NOT SAY

It does **not** show that any value originates anywhere. It shows that **two classifications this
program inherited cannot represent the possibility**, and that one registered inference depends on
the missing option not existing. **A null under a classification that cannot express the alternative
is not evidence about the alternative** — the same form as the standing correction on classical-shaped
nulls.

**NEXT STEP.** The sector-changing operator is now a named object on a carrier we own. **Ask whether
it is dynamical**: does any Hamiltonian built from the carrier's own data move amplitude between
superselection sectors, or is the boundary charge frozen by construction? A frozen charge is a label;
a charge the dynamics can change is a value with a history. **That is the difference between a
bookkeeping sector and a value getting its start, and it is computable on this carrier.**

---

## ERRATUM AGAINST W-22 — "TWO SUPERSELECTION SECTORS" IS FALSE ON THE PHYSICAL SUBSPACE, AND THE DISCRIMINATOR THAT FOLLOWED IT WAS VOID (registrar error, 2026-08-17)

Found by a diagnostic the registrar printed and nearly read past. Both defects are the same defect.

**E-1. THE CARRIER WAS TOO SMALL TO CARRY THE CLAIM.** W-22 reported `Q^2 = I` and inferred **two**
superselection sectors. On the **physical** subspace there is **one**. With a single dangling link,
every link with both ends in the bulk contributes `Z` twice and cancels, while the dangling link
contributes once — so `prod_bulk G_v = Z_9 = Q` **exactly** (`0.000e+00`), and imposing bulk Gauss
`= +1` **forces** `Q = +1`. Measured: eigenvalues of `Q` on the physical subspace `= [1.0]`.
**W-22's three-way operator split stands** — it rests on `Q` being central, which is independently
verified — **but the sector count does not.**

**E-2. AND THE DISCRIMINATOR BUILT ON IT COULD NOT HAVE FAILED.** The registrar then tested whether
`H` is a function of `Q` alone — the property separating the gravitational structure (where the
Hamiltonian **is** the boundary term) from the electromagnetic one (where charge is a surface term
and energy a bulk density) — and reported **EM-shaped**. **With `Q` constant on the physical
subspace, `H` cannot be a function of it, and the verdict was forced.** The run printed
`distinct eigenvalues of Q on the physical subspace : 1` in its own output. **VOID. The EM-versus-
gravity question is UNTESTED, not answered.**

**E-3. AND THE CORRECTED STRUCTURE IS BETTER THAN THE ONE CLAIMED.** With **two** dangling links
(physical dimension 32): `Q_6` takes **both** values `[-1.0, +1.0]` while the total `Q_6·Q_7` remains
forced at `[1.0]`. **The boundary charge is not free in total — it is free to be DISTRIBUTED, with
only its sum fixed by the bulk.** That is a different and richer object than a global label, and a
single dangling link cannot exhibit it.

**RECORDED WITH IT — THE INERTNESS RESULT STANDS AND IS NOT AFFECTED.** `[H, Q] = 0.000e+00` at
every coupling: the dangling link lies on **no cycle**, so no plaquette term can contain it, and in
**pure** gauge theory nothing in the Hamiltonian can move boundary charge. **The sector is frozen;
it is a label, not a process. Only matter can unfreeze it** — adding a term containing the
sector-changing operator gives `||[H,Q]|| = 4.480e+01`.

**AND A CORRECTION TO THE REGISTRAR'S LANGUAGE, AT THE PRINCIPAL'S DIRECTION.** The registrar wrote
that a negative result would "kill it". **It would not.** Under the charter (R-3) a failed test kills
**one assembly**, never the program — and this one did not even do that. **It killed one carrier that
was too small to show the structure**, which is the same failure as the theta graph at T1: the
question was sound, the construction could not carry it.

**NEXT STEP, AND IT IS NOW CHEAP AND SPECIFIED.** Re-run the EM-versus-gravity discriminator on the
**two-dangling-link** carrier where `Q` genuinely varies: does `H` restricted to the physical
subspace vary **within** a fixed `Q` sector? If it does not, the Hamiltonian is a boundary term and
the structure is gravity-shaped. If it does, energy is a bulk density and the structure is
EM-shaped. **The test is live for the first time, and the carrier exists.**

---

## W-24 — **OUR BOUNDARY WAS NEVER A BOUNDARY. IT WAS A FRINGE — AND A FRINGE CANNOT CARRY ANYTHING.**

Commissioned by the principal, 2026-08-17, after the observation *"lot of pairs"*. `LANE_W24_Z3/`,
sealed, 4 scripts.

### **THE STRUCTURAL FINDING, AND IT EXPLAINS A CLASS OF FAILURES AT ONCE**

**The boundary links of every carrier in this program lie on NO CYCLE.** Measured directly: links
0, 1, 2 on a cycle `True`; links 3 and 4 — the boundary — `False`.

> **No cycle means no flux can thread it, no persistent current can circulate on it, and nothing can
> flow there. By construction, at any group, at any coupling.**

**This is the common cause of results the register has been carrying as separate findings.** The
boundary charge was frozen (`[H,Q] = 0.000e+00`) because nothing in the bulk could drive it. The
chirality could not reach the surface because there was no channel. Every boundary measurement came
back **forced** because a fringe has no degrees of freedom of its own to be otherwise.

**THE BOUNDARY OF A REGION IS A CLOSED CURVE. OURS WAS A SET OF LOOSE ENDS.** That is what makes a
surface a surface, and every carrier here — K1, the theta graph, tri_chain12, Heawood, the open
graphs of the erratum against W-22 — has had dangling ends where it needed a cycle. **This is one
error, not five, and it has one fix.**

### ORIENTATION: WHAT Z_2 STRUCTURALLY CANNOT EXPRESS

**Z_2 forces every charge to be its own inverse**, so the two senses of a circuit are the same
object and the Wilson loop is its own adjoint. **`Im<W> = 0.000000` at every `theta`, structurally,
not numerically.** At **Z_3** the identical term with the identical coefficient gives
`-0.059329`, `-0.151602`, `-0.222120` as `theta` runs `0.4 -> 2.0`. **The ground state acquires a
sense of rotation.** `theta` is dimensionless, periodic, and sets no scale — the first slot of that
kind to appear in this program, and it appeared without being installed.
**AND IT IS CONFINED TO THE BULK:** every boundary observable reads `0.000000` at every `theta`,
for the reason above — the dangling links touch no plaquette.

### AND THE PAIRS ARE OURS, WITH THE SCOPE STATED

Tripling the group changed **nothing** in the measured structure: same three-way operator split
(4 invariant, 3 junk, 1 sector-changing), same Gauss identity at machine zero, same
`I(S:F)/H(S) = 1.000000`. **So the two-valuedness is the registrar's, not the carrier's** (W-15).
**Scope, stated:** every quantity compared there is one a constraint already fixes, so the
comparison could not have separated the groups. **No evidence the pairs come from `Z_2`; no strong
evidence either way.** What Z_3 *does* add is orientation, and that is a different axis.

### CORRECTIONS CARRIED

`-dE_0/dtheta` is **not** a chirality and is **larger at Z_2** (`-0.229`) than at Z_3 (`-0.065`):
`theta` reweights the plaquette in both groups. **`Im<W>` is the orientation-sensitive quantity;
the energy derivative is not.** Recorded because the registrar conflated them.
Five measurements in this stretch were of quantities a constraint already fixes — including
`<psi|i[H,Q]|psi>`, which vanishes in any eigenstate identically. **Standing rule adopted here:
before measuring any quantity, compute whether the constraint determines it. One commutator, first,
every time.**

### **NEXT STEP — ONE FIX FOR THE WHOLE CLASS**

**A carrier whose boundary is a CLOSED CURVE**: an interior region separated from an exterior by a
cycle of links, so that the boundary has flux through it, can carry a persistent current, and is a
surface in the sense this program has been assuming it had. **On that carrier, and only there, the
open questions become askable** — does the boundary carry a current; does the chirality reach it;
does the charge stay correlated with what wrote it; and is there a regime that is *allowed but held*.

**REOPENS IF:** a fringe is shown to carry a flux or a current after all · or the closed-curve
carrier reproduces the same forced results, which would move the cause elsewhere.

---

## W-25 — THE CLOSED-CURVE CARRIER: **THE FIX WORKS. THE BOUNDARY CARRIES CHIRALITY AND IS MORE THAN ITS PIECES. AND THE WHEEL CANNOT DISTINGUISH AREA FROM PERIMETER, WHICH IS THE NEXT CARRIER'S REQUIREMENT.**

Built at the principal's direction after W-24 identified that every prior carrier put its boundary on
dangling links. `LANE_W25_CLOSED_CURVE/`, sealed, 4 scripts.

### THE CARRIER, AND THE TEST EVERY PREVIOUS ONE FAILED

**Wheel `W_n`:** hub = interior, **rim = a closed curve = the boundary**, `n` spokes, `n` interior
triangles. **All rim links lie on cycles** — so a flux can thread the boundary and a current can
circulate on it, which no earlier carrier permitted. Physical dims `16 / 81 / 256` at `Z_2/Z_3/Z_4`.
**DISCRETE STOKES VERIFIED EXACTLY AT EVERY GROUP:** `W_rim = T_0 T_1 T_2 T_3`, residual `0.00e+00`.
**The boundary flux equals the enclosed curvature** — the first relation in this program between a
boundary quantity and a bulk one.

### THE CHIRALITY REACHES THE BOUNDARY

`Im<W_rim>` is `-0.006997 / +0.002180 / -0.011434` at `Z_3` and **exactly `0.000000` at `Z_2` at
every theta, structurally** — the Wilson loop is its own adjoint there, so the two senses of the
circuit are one object. **On every fringe carrier this read zero because the boundary touched no
plaquette. The rim touches `n`.**

### THE BOUNDARY IS MORE THAN ITS PIECES — AND IT GROWS

The four `<T_k>` are **identical** (`+0.23272-0.06043j`), forced by the wheel's `n`-fold symmetry,
**so they cannot cancel by sign.** And `|<W_rim>|` **exceeds** the product of the individual
expectations in every case. Enhancement `|<W_rim>| / |prod_k <T_k>|`, at `theta = 1.0`:

```
   rim n :      3       4       5       6
   Z_2   :   2.17    2.66    3.34    4.23
   Z_3   :   2.13    2.60    3.24    4.09
```

**Monotone growth, ~`1.25^n` — a constant connected correlation per boundary link.**
**AND IT IS THE SAME AT BOTH GROUPS**, while the chirality is zero at one of them. **So the
enhancement is NOT a chirality effect; it is generic plaquette correlation and would appear with no
orientation at all.** Recorded so it is not later attributed to orientation.

### REGISTRAR ERROR CORRECTED — A NEW CLASS

The previous turn claimed `Im<W_rim>` was "20-30x smaller than a single triangle despite Stokes, so
they must nearly cancel." **False, and the reasoning was invalid.** Stokes is an **operator**
identity and says nothing about expectations; comparing a four-operator product to a single operator
is comparing `<x^4>` to `<x>`. **Not a forced measurement this time — INCOMMENSURABLE OBJECTS
COMPARED.** Both hypotheses it generated (screening; resolution floor) are dead: symmetry forbids
cancellation, and exact diagonalisation at dim 81 has no resolution floor.

### **THE NEXT CARRIER'S REQUIREMENT, AND IT IS STRUCTURAL**

**On a wheel the enclosed area and the perimeter are BOTH `n`.** They scale identically, so this
carrier **cannot distinguish an area law from a perimeter law** — and that distinction is the
boundary-versus-bulk question, the one gravitational signature phrased natively in information
language. **Same failure mode as the fringe: the question is sound, the carrier cannot carry it.**

> **NEXT: a carrier where AREA AND PERIMETER SCALE DIFFERENTLY** — a 2-D lattice patch, where a
> region of side `k` has area `~k^2` and perimeter `~k`. Only there can `<W>` be tested for an area
> law against a perimeter law, and only there is the boundary-versus-bulk scaling askable.

**REOPENS IF:** the enhancement is shown to be a finite-size artefact rather than a correlation per
link · or a wheel is exhibited on which area and perimeter can be separated.

---

## W-26 — **THE BOUNDARY TOTAL IS A MIRROR, NOT A MEMORY. THE DISTRIBUTION IS NOT.** — and a relabelling that inverts three earlier readings

Directed by the principal, 2026-08-17: *"It's the boundary."*

### THE RELABELLING, AND IT CHANGES WHAT EARLIER RESULTS SAID

**On a graph, a surface is a SEPARATOR.** Measured on wheels `n = 4,5,6`: removing the **rim** leaves
`1` component and removing the **spokes** gives `2`. **The rim separates nothing. The spokes are the
edge boundary of the region `{hub}`.** The registrar called the rim "the boundary" because it is
drawn as a circle — a picture, not a property of the graph.

**Three consequences.** (i) W-25's "the chirality reaches the boundary" was measured on the **rim**,
which is not the boundary — that result is about the exterior's internal structure and is
**relabelled, not withdrawn**. (ii) The residual order surviving thermalisation (one trit at
`T = 50`) is **on the boundary**, not the interior. (iii) **W-24's requirement was half right**: a
surface must be a separator **and** a cycle. The fringe was neither; the wheel's rim is a cycle that
separates nothing; the wheel's spokes separate but are not a cycle. **No carrier in this program has
had both.**

### "FORCED BY GAUSS" WAS BEING MISREAD, INCLUDING BY ME

The hub's Gauss law fixes the **sum** of the spokes — which is *flux through the boundary equals
charge enclosed*. **That is the physical law, not bookkeeping.** The registrar has been voiding
constraint-determined results as vacuous; this one is the constraint **being** the physics, and
W-19's `I(S:F) = H(S)` is the same statement. **Max `S(spokes) = 4.0000` exactly at `n=5, Z_3`
against `5` for the rim: the trit is real and it is what Gauss says.**

**BUT IT MAKES THE BOUNDARY A MIRROR, AND THIS NEEDS NO MEASUREMENT.** Gauss holds at **every
instant**, so the boundary total can never disagree with the present interior charge and can never
retain one the interior has left. **Perfect fidelity, zero retention. A memory must be able to
disagree with the present; the constraint forbids it.**

### **THE DISTRIBUTION IS UNCONSTRAINED, AND IT RETAINS**

Gauss fixes **one** quantity — the sum of `n` boundary links. **`n-1` boundary degrees of freedom
are unconstrained by the interior.** Every boundary measurement in this program has been of the
total. Measured (`wheel n=4`, `Z_3`, dim 81): two physical states with the **same** boundary total
`0` and **different** distributions `(0,0,0,0)` vs `(0,0,1,2)`:

```
   t        0.0     0.5     1.0     2.0     5.0    20.0   100.0
   boundary TD    1.000   0.895   0.833   0.908   0.725   0.891   0.908
   rim TD (ctrl)  1.000   0.949   0.890   0.975   0.778   0.954   0.970
```

**The boundary distribution stays distinguishable while the total is pinned. The first quantity in
this program that is neither forced nor absent.**

**CAVEAT, LOAD-BEARING:** the rim control behaves the same way, so **nothing decays on this
carrier** — it may simply not thermalise at dimension 81. *"Stays distinguishable"* may be a
statement about a small closed system. **Not established as a boundary property until run on a
carrier that thermalises, or an open one.**

### NEXT

1. **A carrier whose boundary is BOTH a separator AND a cycle** — a 2-D lattice patch, where the
   edge boundary of a block of plaquettes is a closed curve *and* removing it disconnects.
2. **Rerun the distribution test where things decay** — larger, or open (coupled to a bath), so the
   control can fail.
3. **An open system is now required for a further reason** (W-25/AA): the global entropy is exactly
   `0` and stays `0` under unitary evolution. **Nothing can be paid in a closed pure system**, and
   every physical account of record formation involves paying.

**REOPENS IF:** the distribution retention is shown to be non-thermalisation · or a carrier is
exhibited whose boundary is both separator and cycle and behaves differently.

---

## W-27 — THE PLANAR PATCH: **A BOUNDARY THAT IS BOTH A CYCLE AND A SEPARATOR, AND WHERE EM'S TWO HALVES FINALLY MEET**

3x3 planar patch, `Z_2`, 12 links, 4 plaquettes, physical dim 16 (cycle rank 4).
**PERIMETER = 8 links: all degrees `2` (a CYCLE) and removal gives `5` components (a SEPARATOR).**
The registrar had claimed duality forbids one set being both. **It does not, and the patch has the
object** — the wheel's rim was a cycle that separated nothing, the fringe was neither.
**Discrete Stokes exact:** product of the 4 plaquettes = the perimeter loop, `0.00e+00`.

### WHERE EM WAS WHILE WE WERE MISSING THIS — **WE HAD HALF OF IT AT A TIME**

Electric flux is a **cut** quantity (Gauss); magnetic flux is a **cycle** quantity (Wilson). Every
prior carrier could express only one at its boundary: the fringe's dangling links lie on no cycle,
so **no magnetic structure at the boundary at all**; the wheel's rim is a cycle with no cut and its
spokes a cut with no cycle. **So the mirror result (Gauss, electric) and the chirality result
(Wilson, magnetic) were measured on different sets and could never interact.**

### AND THE CONJUGATE PAIR IS NOT WHAT THE REGISTRAR EXPECTED

Electric flux on the **whole perimeter is the IDENTITY** on the physical sector — `nontrivial: False`
— because a closed `Z`-loop is fixed by the Gauss laws it encloses. And `[E, M]` on the **same** set
is `0.000e+00` always: any subset whose `X`-product stays physical is a closed loop, and closed loops
here touch an **even** number of links, so anticommutations pair off.
**THE CONJUGATE PAIR IS A LOOP AND A CUT THAT PIERCES IT AN ODD NUMBER OF TIMES:** `Z` on an odd
subset of the perimeter against the perimeter loop gives `8.000e+00`; even subsets give `0.000e+00`.
**A boundary cannot hold a definite loop flux and a definite odd-piercing cut at once. First
structural limit in this program on what a boundary can record that is not a Gauss identity.**

---

## W-28 — **THE PROCESS, ASSEMBLED AND WORKING: A RECORD SURVIVES THE ENTROPY BEING PAID, IFF IT COMMUTES WITH THE DYNAMICS**

`LANE_W28_PROCESS/`, sealed. Carrier W-27's patch; open system via Lindblad, `gamma = 0.5`, `T = 10`.
**RECORD = the perimeter flux sector.** Write `rho_A` on `W = +1`, `rho_B` on `W = -1`, evolve, read.

```
  phase      bath        ||[H,W]||   S(global)      TD    <W>_A    <W>_B
  magnetic   magnetic     0.00e+00      3.0000  1.0000   1.0000  -1.0000
  magnetic   electric     0.00e+00      3.0000  1.0000   1.0000  -1.0000
  mixed      magnetic     3.20e+01      4.0000  0.0000   0.0000  -0.0000
  mixed      electric     3.20e+01      4.0000  0.0016   0.0008  -0.0008
```

**IN THE MAGNETIC PHASE THE RECORD SURVIVES PERFECTLY WHILE THREE BITS OF ENTROPY ARE PAID.** The
written values hold at `+1.0000` and `-1.0000`; the states stay perfectly distinguishable. **In the
mixed phase, where the record no longer commutes with `H`, it is destroyed completely.** Same
carrier, same bath, same coupling — **one variable: whether the recorded quantity is conserved.**

**THE POINTER CONDITION, MEASURED NOT IMPORTED:** *a record survives dissipation exactly when the
recorded quantity commutes with the dynamics.*

**WHAT DOES NOT HOLD, AND IT WEAKENS THE CLAIM.** In the magnetic phase **the bath choice does not
matter** — magnetic and electric baths both give `TD = 1.0000`. If einselection were doing the work
the electric bath should have damaged it. **So the conservation is doing everything and the
monitoring nothing.** This is a conservation result, not a decoherence result, and the einselection
half of the pointer story is **untested here**.

**AND WHY W-27b FAILED, NOW DIAGNOSED.** That run dephased in `Z` on the cut while `H`'s plaquette
terms rotate states out of the electric basis: Hamiltonian moves the record, bath measures it, and
the pair random-walks the distinction to zero (`TD 0.019` at `gamma = 1`). **Not a construction
failure — the recorded quantity was not conserved.**

**NEXT.** (1) Separate conservation from monitoring: find a bath that damages a conserved record, or
show none can. (2) The record here is a **global** flux sector, not a local one — test whether a
record localised to part of the boundary also survives. (3) The `gamma = 0` control in W-27b drifted
`S` to `0.0035` where it must be exactly `0`; the Heun integrator does not conserve purity and the
small-`gamma` numbers there carry unbounded error.

---

## W-29 — THE WRITE STEP: **WRITABLE AND DURABLE ARE CONJUGATE, AND THEY ARE CONJUGATE BECAUSE THE GEOMETRY IS FROZEN**

`LANE_W29_WRITE/`, sealed. Carrier: W-27's patch. **W-28 measured PERSISTENCE, not formation** — the
value was put in by hand and stayed. **Formation means the record ACQUIRES a value it did not have.**

**W-29, the null and its cause.** Writer = `Z` on a cut link at the interior vertex.
`||[Z_interior, W]|| = 0.000e+00` — **they commute, so nothing can be written.** Separation `0` at
every setting. **The registrar used an operator W-27 had already shown cannot conjugate the loop.**

**W-29b, the right operator, still null.** The conjugate of a loop is a cut that **pierces it an odd
number of times** — `||[Z_S, W]|| = 8.000e+00`. Best separation `0.058`, and only in the **closed**
case; with dissipation `~1e-5`.

> **THE OBSTRUCTION, STATED SHARPLY. W-28: the record survives dissipation IFF it commutes with `H`.
> W-29b: it can be written ONLY by something that does NOT commute with it. So the property that
> makes a record durable is exactly the property that makes it unwritable.** Preparing the writer
> definite leaves the record maximally uncertain, and conservation keeps it there forever.

**W-29c, the dynamics on its own.** *"If the dynamics of the parts force the record creation that's
a process as well"* (the principal). Start **maximally mixed**, nothing written, and let it run:

```
   bath          g2   gamma    T        <W>     |<W>|   S(final)
   plaquette    1.0    0.50  20.0   0.000000  0.000000    4.0000
   electric     1.0    0.50  20.0   0.000000  0.000000    4.0000
   proj +1      0.0    0.50  20.0   0.999909  0.999909    3.0007
   none         1.0    0.00  20.0   0.000000  0.000000    4.0000
```

**`|<W>| = 0.999909` — the dynamics drives the record to a definite sector from nothing.** BUT
**only for the `proj +1` bath, which is a projector onto the answer.** Every physically motivated
bath leaves `<W>` at exactly `0.000000` with entropy pinned at the maximum. **This is dissipative
state preparation: the selection is in the registrar's Lindblad operator, not in the physics.**
**What is missing is specific — a bath with TWO absorbing sectors and a broken tie**, so the system
selects rather than being told. That is spontaneous symmetry breaking, and it is untested.

### THE DESCRIPTION OF THE PROCESS AND ITS TERMS — `PROCESS_DESCRIPTION_V001.md`

**EM: PRESENT** — both Hamiltonian terms **and** the constraint; electric, magnetic and Gauss are
Maxwell's equations. **ALPHA: PRESENT, AND THERE ARE TWO SLOTS** — `g^2`, and `theta` which is
dimensionless, periodic and does nothing at `Z_2`. **GRAVITY: ABSENT, AND THE TEMPTING FILL IS
WRONG** — assigning it to the Gauss constraint counts EM twice, because Gauss is Maxwell's first
equation.

> **WHAT IS MISSING IS THAT THE CARRIER IS STATIC.** The graph is fixed and nothing the field does
> changes it. Every gravitational functional signature reduces to this. **A gravitational term would
> be the carrier responding to the field.**

**AND THAT IS WHY THE WRITE FAILED.** With a frozen geometry the only conserved quantities are the
ones the geometry hands you, and those are precisely the ones nothing can write to.

**NEXT.** (1) A bath with **two** absorbing sectors — does the system select, and does the selection
correlate with anything in the initial state? (2) **A carrier that responds to the field** — the
missing term, and the first construction in this program with a dynamical geometry.

---

## W-30 — **THE W-29 OBSTRUCTION IS NOT A FEATURE OF OUR PATCH. IT IS GENERAL, AND NO VALUE OF THE COUPLING ESCAPES IT.**

`LANE_W30_DYNAMIC_CARRIER/`, sealed. W-29 found the conjugacy on one carrier. **A finding on one
carrier is a property of that carrier until tested elsewhere.**

### W-30a — FOUR CARRIERS, TWO GROUPS, ONE ANSWER

Carriers: the 3×3 patch, a single 2×2 plaquette, a triangle (3-cycle), and the theta graph (two
vertices, three parallel links, **two** independent cycles). Groups `Z_2` and `Z_3`. `R` = rim loop
built as the **product of plaquettes**, so orientation is correct by construction. At `g^2 = 0`:

```
  carrier         N  dim   ||R||  unitarity  ||[H,R]||  ||[L,R]||  max|d<R>/dt|
  3x3 patch       2   16   4.000  0.000e+00  0.000e+00  0.000e+00     1.110e-16
  3x3 patch       3   81   9.000  0.000e+00  0.000e+00  0.000e+00     2.252e-17
  2x2 plaquette   2    2   1.414  0.000e+00  0.000e+00  0.000e+00     0.000e+00
  triangle        3    3   1.732  0.000e+00  0.000e+00  0.000e+00     1.144e-16
  theta graph     3    9   3.000  0.000e+00  0.000e+00  0.000e+00     1.241e-16      (8 rows, all)
```

`R` is **unitary** (defect `0.000e+00`) and **nontrivial** — exactly `N` distinct eigenvalues on
every carrier, so it can label `N` sectors. It is a perfectly good record-bearing observable.
**`d<R>/dt` is zero to machine precision on every carrier, at every group, for every random state.**

> **THE NO-GO.** A perfectly conserved quantity cannot be written, **because that is what conserved
> means.** Its value does not change, so it was never acquired — it always was. And a quantity that
> is not conserved is one the bath can reach. **On a static carrier there is no third option.**

### W-30b — THE COUPLING IS THE DIAL BETWEEN THE HORNS, AND IT DOES NOT REACH A WAY OUT

Exact Lindblad exponential (RK4 agrees to `~1e-14`, CONTROL D — this also **retires the `w27b_open`
Heun defect** for this lane). `LASTS` = time-average of `<R>` over `t ∈ [10,20]`; `OSC` = the same at
`gamma = 0`, separating precession from survival.

```
     g^2   MOVES=||[H,R]||/dim   LASTS(gam=.5)   OSC(gam=0)   LASTS-OSC
    0.00                0.0000        1.000000     1.000000    0.000000
    0.01                0.0400        0.952075     0.998332   -0.046257
    0.03                0.1200        0.646844     0.985428   -0.338584
    0.10                0.4000        0.016774     0.856770   -0.839995
    1.00                4.0000        0.000076     0.211098   -0.211023
   20.00               80.0000        0.240293     0.319244   -0.078951
```

**At `g^2 = 0` the record is untouchable: `<R>` = `1.000000000000` with the bath ON** (CONTROL A).
**The bath cannot damage a conserved record at all.** And `MOVES` is exactly `0` — nothing can write
it. **Switch the coupling on and both change together.** By `g^2 = 0.1` survival is `1.7%`.

**The apparent revival at large `g^2` is not survival.** There `LASTS ≈ OSC` — the same value with
the bath off — so it is the **dephasing residue** (the projection onto the commutant of a
now-dominant electric term), and it is flat at `~0.3`, not rising. The `MOVES×LASTS` product peaks
at the **edge** of the scan only because `MOVES = 4g^2` grows without bound; that is the metric
inflating, not a record persisting.

> **NO VALUE OF THE COUPLING SOLVES IT. THE OBSTRUCTION IS TOTAL ON A STATIC CARRIER.**

### WHAT THIS ESTABLISHES — GRAVITY'S ROLE, DERIVED FROM ITS ABSENCE

The charter asks for the roles of EM, gravity and alpha in record formation. **EM** supplies the
field, the boundary that is both cycle and separator, and the loop that is a candidate record.
**Alpha (`g^2`)** is the dial along the axis of the obstruction — it is what trades writability
against durability, and it lands on that axis without being put there. **And the missing ingredient
is now specified by what it must do:**

> **A record can only form if a quantity can BECOME conserved. On a fixed `H` the conserved
> quantities are fixed for all time, so nothing can become one. The carrier must respond.**

**This is not "gravity would be nice to have." It is: without a responsive carrier there are no
records at all.** Record formation REQUIRES the ingredient we have been calling gravity, and the
requirement is derived from a null, not assumed.

**CAVEAT, STANDING.** The escape not yet tested is **approximate** conservation — einselection uses
pointer states stable on observation timescales, not forever. That is a hierarchy of timescales, and
a timescale ratio is a pure number. **Whether alpha sets that ratio is untested and is the obvious
next question if the dynamical carrier fails.**

---

## W-32 — **THE WINDOW EXISTS. W-30's "NO COUPLING ESCAPES" IS WRONG, AND THE COUPLING SETS THE WIDTH.**

`LANE_W32_TIMESCALES/`, sealed. Opened at the principal's direction: real records are never exactly
conserved — domains flip, crystals anneal, DNA mutates — so the question is not whether `<R>`
survives to a fixed time but **how many times the record can be written before it decays.** That
ratio is dimensionless.

### ERRATUM TO W-30

**W-30b measured survival at a FIXED ABSOLUTE TIME (`T=10`) while the WRITE timescale was itself
changing with `g^2`.** Two moving quantities, one held still. Corrected here by taking both rates
from the Lindbladian spectrum, where no observation window enters.

> **W-30's sentence "no value of the coupling solves it; the obstruction is total on a static
> carrier" IS WITHDRAWN.** The no-go on *exact* conservation (W-30a) stands untouched and is
> unaffected. What fails is the extension of it to approximate records.

### THE MEASUREMENT

`Gamma_R` = slowest decay rate among left-eigenmodes of the Lindbladian **whose overlap with `R`
exceeds `1e-6`** — so it is the record's lifetime, not an unrelated mode's. Overlap is `1.000` at
weak coupling; **at `g^2=0` NO mode carries `R` at all** (`1.3e-16`), confirming exact conservation
there and exposing that W-32's first pass had reported an unrelated mode's rate.

```
  BATH ON THE CUT -- disjoint from the rim, [L,R] = 0
       g^2        omega        Gamma_R        RATIO   d ln(RATIO)/d ln(g2)
   0.00050     0.002000   7.999981e-06     250.0006
   0.00100     0.004000   3.199970e-05     125.0012                 -1.000
   0.00200     0.008000   1.279952e-04      62.5024                 -1.000
   0.00500     0.020000   7.998119e-04      25.0059                 -1.000
   0.01000     0.040000   3.196988e-03      12.5118                 -0.999

  BATH ON THE RIM -- the environment sees the record directly, [L,R] = 8
   0.00050     0.002000   5.999266e+00       0.0003
   0.00500     0.020000   4.992902e+00       0.0040                 +1.001
   0.05000     0.200000   1.022078e+00       0.1957                 +2.166
```

**`omega = 4g^2` (first order). `Gamma_R = 32g^4` (second order). `RATIO = 1/(8g^2)`, slope `-1.000`
across two decades.** The record can be written `250` times over at `g^2 = 0.0005`, and the count
**doubles every time the coupling halves.**

### THE EXPONENT IS PHYSICS, NOT GENERIC COUNTING

The obvious deflation is that `omega ~ g^2` and `Gamma ~ g^4` is just golden-rule order counting.
**It is not, and the control settles it:**

```
  bath on CUT :  d ln(Gamma)/d ln(g2) = +1.996     RATIO ~ 1/g^2   protection DIVERGES as g2 -> 0
  bath on RIM :  d ln(Gamma)/d ln(g2) = -0.310     RATIO ~ g^2     protection VANISHES as g2 -> 0
```

**Same Hamiltonian, same record, same coupling strength — opposite exponents.** The difference is
only **where the environment touches.** When the bath commutes with the record it can reach it only
*through* the `H`-mixing, so decay is one order higher than drive and the record is shielded. When
the bath sees the record directly, `Gamma_R` is flat at `~5` regardless of coupling and there is no
protection at any `g^2`.

> **THE CONDITION FOR A RECORD IS GEOMETRIC. The record lives on the rim; the environment couples to
> the cut. `[L,R] = 0` is the shielding condition, and the W-27 patch — whose perimeter is
> simultaneously a CYCLE and a SEPARATOR — is exactly the structure that supplies it.** That
> construction was built at W-27 and only now does work.

### WHAT THIS DOES TO THE THREE TERMS

**ALPHA GAINS A SECOND, SHARPER ROLE.** Beyond being the dial along the obstruction axis (W-30b),
`1/g^2` **is the number of times a record can be written and re-read before it decays.** A pure
number, measured, not fitted.

**AND THE W-30 CLAIM ABOUT GRAVITY IS WEAKENED AND MUST BE RESTATED.** W-30 concluded "without a
responsive carrier there are no records at all." **That is now false as stated** — approximate
records form and persist on a static carrier, and approximate is what real records are.

**WHAT REMAINS OPEN IS SELECTION, NOT DURABILITY.** W-32 shows a record, once written, persists
`1/(8g^2)` write-times. **W-29c showed nothing writes it spontaneously** — every physically
motivated bath left `<W>` at exactly `0.000000` with entropy pinned at maximum, and only a projector
that already knew the answer broke the tie. **So the live question is no longer "can a record last."
It is "what decides WHICH value it takes."** That is the tie-breaking / symmetry-breaking problem,
and it is where the responsive carrier must now be aimed.

---

## W-33 — **THE CARRIER IS A MEMORY, NOT A RECORDER. IT PRESERVES EXACTLY; IT NEVER AMPLIFIES.**

`LANE_W33_SELECTION/`, sealed.

**STEADY-STATE COUNT — decisive before any dynamics is run, because a Lindbladian with a UNIQUE
steady state cannot select anything from any initial condition.**

```
   g^2      bath   #zero modes
  0.0000     cut         2      DEGENERATE -> a record manifold exists
  0.0010     cut         1      unique                 (next rate 3.200e-05)
  0.0100     cut         1      unique                 (next rate 3.197e-03)
  any        rim         1      unique                 (next rate ~1.0)
  any    all links       1      unique
```

**The record manifold is EXACT only at `g^2 = 0` with a shielded bath.** For `g^2 > 0` it is lifted
— but at rate `32g^4`, so for small coupling the manifold is approximate and long-lived, which is
W-32's window seen from the spectral side.

**WHAT THE STEADY STATE REMEMBERS.** Start from `rho(b) = (I + b R)/dim` and take `t -> infinity`
exactly by projecting onto the zero modes:

```
  bath=cut g2=0.0000   slope d<R>(inf)/d<R>(0) = +1.000000000   PRESERVES EXACTLY
      -0.90->-0.900  -0.50->-0.500  -0.20->-0.200  0.00->0.000  +0.20->+0.200  +0.50->+0.500  +0.90->+0.900
  bath=cut g2=0.0010   slope = -0.000000000                     erases (at t=inf; 1/(8g^2) cycles first)
  bath=rim any g2      slope = +0.000000000                     erases
```

> **THE SLOPE IS EXACTLY `1` OR EXACTLY `0`. IT IS NEVER GREATER THAN `1`, AT ANY SETTING TESTED.
> THE DYNAMICS NEVER BREAKS A TIE. IT KEEPS WHAT IT IS GIVEN AND MANUFACTURES NOTHING.**

**AND THIS REFRAMES W-29c'S NULL.** W-29c started from a maximally mixed state — which carries no
information — and found `<R> = 0.000000`. **That is the correct answer, not a failure: a record of
nothing is nothing.** Reproduced here exactly (`+0.000000000000` at every setting). The construction
was never failing to hold a record; it was being asked to invent one.

## W-34 — **THE PREDICTABILITY SIEVE SELECTS THE BOUNDARY, AND WE NOMINATED NOTHING**

Every prior lane NOMINATED the rim loop and then asked how it fared — which installs the answer.
Here nothing is nominated. The left-eigenmodes of the Liouvillian **are** the observables with
definite decay rates, so the slowest ones **are** the pointer observables. Read them off and ask
what they are.

```
  g2=0.001, bath on CUT          rate        best operator match
        (identity)          2.674e-15        identity
        SLOWEST OBSERVABLE  3.200e-05        RIM LOOP (all 4)      overlap 1.000
        next                5.803e-01        no clean match
        next                9.841e-01        no clean match
```

**CROSS-CHECK — all 16 magnetic operators ranked by their own decay rate, `g^2=0.01`:**

```
    7.157165e-02   RIM LOOP (all 4)          <-- 28x slower than anything else
    1.983944e+00   plaquette (0,)
    1.985041e+00   plaquette (1,)
    2.010041e+00   3-plaquette loop (0,1,3)
    2.029031e+00   2-plaquette loop (0,2)
    3.860385e+00   2-plaquette loop (0,3)
```

> **THE DYNAMICS PICKS THE FULL BOUNDARY, AND ONLY THE FULL BOUNDARY.** Not "bigger is slower" —
> single, double and triple loops are all clustered at `~2.0`. The rim wins by a factor of 28.

**AND THE MECHANISM IS GEOMETRIC, NOT ENERGETIC. The rim loop is the unique gauge-invariant loop
whose support (`PERIM`) is DISJOINT from where the environment couples (`CUT`).** Every other loop
runs through a cut link. **The pointer observable is the one the environment cannot touch.**

**CONFIRMED BY MOVING THE BATH.** With the bath on the RIM instead, no magnetic operator survives at
all — the slow modes become **electric-type (diagonal)**, all at rate `~1.0`. **The pointer basis
follows the environment's coupling.** That is einselection behaving exactly as advertised, and it
means the boundary is not privileged a priori: it is privileged *given where the environment is*.

**THIS RETIRES THE CIRCULARITY.** The rim loop was chosen by the registrar at W-27 and used as the
record ever since. It is now independently re-derived as what this construction actually protects.

---

## W-35 — **THE RECORD FORMS ON EVERY RUN. THE INSTRUMENT WAS BLIND TO IT FROM W-28 TO W-34.**

`LANE_W35_TRAJECTORIES/`, sealed. Raised by a design agent in the W-31 panel and tested here.

**Every lane from W-28 onward measured `<R> = Tr(R rho)` — an ENSEMBLE AVERAGE. A fair coin has mean
zero and every single flip is definite.** So `d<R>/dt = 0` is consistent with every individual run
acquiring a perfectly definite record. Unravel the same Lindbladian and measure the second moment.

```
  HOMODYNE, 600 trajectories, T=15, every start has <R> = 0 EXACTLY
     g^2  gamma      E[<R>]     +-SE    E[<R>^2]   |<R>|>0.9  |<R>|>0.99
   0.000   0.00    0.000000   0.0000    0.000000       0.000       0.000   <- GATE 0
   0.000   0.10    0.003189   0.0324    0.631305       0.432       0.113
   0.000   0.30   -0.014558   0.0397    0.945506       0.922       0.785
   0.000   1.00   -0.019572   0.0408    0.999078       0.998       0.995
   0.100   0.30   -0.001021   0.0258    0.398010       0.082       0.002
   1.000   0.30    0.006214   0.0122    0.090022       0.003       0.000

  GROWTH IN TIME (g2=0, gamma=0.3):  t=0: 0.000  t=1: 0.196  t=3: 0.445
                                     t=6: 0.700  t=10: 0.867  t=15: 0.946  t=25: 0.991
```

> **`E[<R>] = -0.0146 +- 0.0397` (zero, as every previous lane found) WHILE `E[<R>^2] = 0.9455` AND
> 78.5% OF RUNS SIT AT `|<R>| > 0.99`. At `gamma=1.0`, `E[<R>^2] = 0.999078` and 99.5% of runs are
> definite. THE TIE IS BROKEN ON EVERY SINGLE TRAJECTORY. THE VALUE IS A FAIR COIN.**

**GATES.** `gamma=0` gives `E[<R>^2] = 2.7e-29` (machine zero — the integrator invents nothing);
stable across `dt` from `0.008` to `0.001`; and the trajectory ensemble reproduces the exact master
equation (`<R>_exact = -0.00000000`, `<R>_traj = -0.0146`, within one standard error).

### THE SAME LINDBLADIAN, UNRAVELLED THE OTHER WAY, HAS NO RECORD AT ALL

```
  JUMP unravelling, identical generator:  g2=0, gamma=0.3 -> E[<R>^2] = 0.000000
                                          g2=0, gamma=1.0 -> E[<R>^2] = 0.000000
```

**Both unravellings give the same `rho(t)`.** With unitary `L`, jump rates are state-independent
(`gamma||L psi||^2 = gamma` always), so a jump carries **no information** and every trajectory keeps
`<R>` fixed. Homodyne extracts information continuously. **Record formation is therefore not a
property of the master equation. It is a fact about what the environment does with what it learns.**

### ERRATUM — W-29c AND W-33

**W-29c reported that no physically motivated bath selects a sector (`<W> = 0.000000` exactly) and
W-33 reported that the dynamics "preserves but never amplifies" (slope exactly `1` or `0`, never
above `1`). Both numbers are correct and both readings are WITHDRAWN.** They measured the *fairness*
of the coin. The selection they were looking for was happening on every run.

**W-32 and W-34 are NOT affected** — decay rates and pointer selection are properties of the
generator and stand as measured.

### AND IT RESOLVES THE MECHANISM

`[L,R] = 0` was read at W-32 as *shielding* — the environment cannot reach the record. **It is more
than that. `[L,R] = 0` means the environment cannot DISTURB `R`, while `L` and `R` remain CORRELATED
in the state, so the environment LEARNS `R` anyway. That is a quantum non-demolition measurement,
and QND is exactly the condition for a record.** The coupling `g^2` spoils it by making `R`
non-conserved: `E[<R>^2]` falls `0.9455 -> 0.398 -> 0.090` as `g^2` goes `0 -> 0.1 -> 1.0`.

**THE PROCESS, ASSEMBLED FROM WHAT IS MEASURED.** `[H,R] = 0` makes the record durable (W-30a).
`[L,R] = 0` makes it undisturbable while still legible (W-35). Correlation between `L` and `R` makes
the environment learn it. Continuous monitoring collapses each run to a definite value (W-35).
`1/(8g^2)` sets how long it lasts (W-32). And the dynamics selects which observable this happens to
— the full boundary, by a factor of 28 (W-34).

---

## W-36 — **THE RECORD IS NOT OBJECTIVE, AND THE OBSTRUCTION IS LOCALITY**

`LANE_W36_REDUNDANCY/`, sealed. W-35 left record formation depending on how the environment is
read, which is not good enough. Zurek's criterion settles it without choosing an unravelling: a
record is **objective** when many disjoint fragments EACH carry a full copy. That is a property of
the joint state, so the environment is built explicitly and never traced out.

```
  I(R:F) in bits, 6 explicit environment qubits, kappa=8.0, T=16.0, ceiling 1 bit
  |F|                                    0      1      2      3      4      5      6
  A  env on Z at the CUT   (LOCAL)    0.000  0.044  0.100  0.187  0.351  0.658  0.929
  B  env on R itself    (NONLOCAL)    0.000  0.999  1.000  1.000  1.000  1.000  1.000
  C  env on one plaquette  (LOCAL)    0.000  0.037  0.037  0.037  0.037  0.037  0.037
  CONTROL kappa = 0                  -0.000 -0.000 -0.000 -0.000 -0.000 -0.000 -0.000
```

**A — the configuration every earlier lane used — has NO redundancy.** `I(|F|=1)/I(all) = 0.047`:
information rises only as the fragment approaches the whole environment. **One delocalised copy. An
observer holding any part of the environment knows essentially nothing.**

**B is the textbook quantum-Darwinism plateau — `0.999` bits from a SINGLE qubit, flat thereafter.
Every fragment independently holds the whole record. That is objectivity.**

**C reads `ratio 0.999` and is NOT redundancy — the total is `0.037` bits, so every fragment knows
equally nothing.** The ratio test is meaningless without a floor on the total, and it is gated in
`PUBLISHED_CONVENTIONS`.

### THE OBSTRUCTION, STATED

> **`R` IS A PRODUCT OVER 8 RIM LINKS. IT IS NONLOCAL. Redundancy requires the environment to couple
> to the record observable itself, and a LOCAL environment cannot couple to a nonlocal one.**

**And this is the same shape as W-30's obstruction, one level up.** W-30: writable vs durable.
**W-36: legible vs protected.** `[L,R] = 0` is what protects the record (W-32) and it is also what
stops any local fragment from carrying a copy. **The observable that survives is the one nobody can
read.**

**Note that B is not smuggling.** `L = R` is symmetric between the `+1` and `-1` sectors, so it
cannot decide which wins — W-35's coin stays fair — and `R` was selected independently by the W-34
sieve, not nominated here.

### THE NEXT STEP, AND IT IS PHYSICAL

**In gauge theory a nonlocal observable is measured by transporting a probe charge around the loop —
Aharonov–Bohm.** The interaction is local at every instant; the nonlocality is in the PATH, paid for
in TIME proportional to the loop's length. **So the environment CAN read the rim loop, by a local
process extended in time, and case B is the effective description of exactly that.**

**BUILD: a probe charge transported around the rim, and measure whether the record it acquires is
redundantly copied.** If it is, the process closes: the record is written by monitoring, protected
by `[L,R]=0`, selected by the sieve, persists `1/(8g^2)` write-times, and is made objective by
transport. **If the transport time itself destroys the record, that is a new obstruction and the
timescale competition becomes the next quantity to measure.**

---

## W-37 — **A LOCAL PROBE READS THE NONLOCAL RECORD, AND THE READING IS PURELY TOPOLOGICAL**

`LANE_W37_TRANSPORT/`, sealed. W-36's obstruction was that `R` is nonlocal and a local environment
cannot copy it. Gauge theory's own answer is transport.

**EXPLICIT MATTER.** A probe charge hopping the 8 rim vertices, a static anti-charge at the centre.
**The constraint bites and was checked rather than assumed: with the probe alone the total `Z_2`
charge is odd and the physical sector contains `0` states.** Gauss becomes matter-dependent —
`div(s)_v = [probe site] + [centre]` — so **the physical sector MOVES with the probe.** Physical
dim `128 = 8 × 16`. The only interaction is the hop; it touches **one link at a time** and never
mentions `R`.

```
      T   I(R:probe) bits    P(probe back at 0)
   0.00        0.000000                1.0000
   1.00        0.002606                0.0501
   2.00        0.270865                0.1578
   3.00        0.669357                0.0355
  12.00        0.829907                0.4985

  CONTROL A  tau = 0 (no transport)          I = 2.403e-16
  CONTROL B  RING CUT (one hop removed)      I = 0.000000 at T = 4, 8, 12, 20
```

> **`I(R:probe)` reaches `0.83` bits through hops that each touch a single link. CUT THE RING —
> keeping every local interaction and deleting only the closed path — AND IT IS EXACTLY `0.000000`
> AT EVERY TIME. The information is topological. It exists only because a closed path exists.**

**`||[R, H_hop]|| = 0.0e+00`.** The transport **cannot disturb the record.** So the reading is QND,
and **many probes may each read it independently** — which is redundancy, and therefore objectivity.
**W-36's condition 5 is met, by transport.**

`I` oscillates rather than saturating because the dynamics here is coherent and nothing decoheres the
probe; the information sloshes between probe and field. **Locking it in requires decohering the
probe's position, which is untested.**

### THE CLOSING RELATION, AND WHAT IS STILL UNMEASURED IN IT

Readout takes a traversal: `T_read ~ perimeter / tau`. The record decays at `Gamma = 32 g^4` (W-32).
**A region can be read before it forgets only if `32 g^4 · perimeter / tau << 1`** — a relation
between the coupling, the size of the region, and the transport rate.

**THE PERIMETER SCALING IS NOT MEASURED.** One patch, one ring size, so `T_read ∝ perimeter` is an
expectation and not a result. **Rings of several sizes are the next build, and if the scaling holds
the relation above is the program's next pure number.**

## W-37b/c — **THE PERIMETER LAW HOLDS, AND READABILITY DEPENDS ON THE PARITY OF THE LOOP**

```
  bare cycle graphs, tau = 1.0
     n   dim  ||[R,H]||   T_read (I=0.5 bit)   max I     T_read/n
     4     8    0.0e+00          1.25          0.9998      0.312
     5    10    0.0e+00         never          0.0000        --
     6    12    0.0e+00          1.75          0.9827      0.292
     7    14    0.0e+00         never          0.0000        --
     8    16    0.0e+00          2.50          0.9901      0.312
    10    20    0.0e+00          3.00          0.9329      0.300
    12    24    0.0e+00          3.50          0.9338      0.292

  d ln(T_read) / d ln(n) = +0.960        CUT RING, every n: max I <= 4.4e-16, never reaches 0.5
```

> **`T_read/n` IS CONSTANT AT `0.30` ACROSS A FACTOR OF THREE IN RING SIZE. THE PERIMETER LAW IS
> MEASURED, NOT ASSUMED** (W-37 had flagged it as an expectation). And the cut-ring control returns
> `<= 4.4e-16` at every size — **no closed path, no information, at any scale.**

**SO THE CLOSING RELATION IS NOW A MEASURED ONE.** `T_read = 0.30 · perimeter / tau` and
`Gamma = 32 g^4`, so a region can be read before it forgets iff

> **`9.6 · g^4 · perimeter / tau  <<  1`** — a pure number joining the coupling, the SIZE of the
> region, and the transport rate. **A region has a maximum legible size set by the coupling.**

### AND AN UNEXPECTED ONE — ODD LOOPS CARRY NOTHING

`n = 5` and `n = 7` give **exactly** `0.0000`, and TEST 1 confirms it across **every start site and
every time** (`4.4e-16`, `2.2e-16`). An exact zero is a symmetry.

**TEST 3 finds it.** For a ring, `R=+1` is periodic hopping and `R=-1` is antiperiodic. At `n=5` the
periodic spectrum is `[-2, -0.618, -0.618, 1.618, 1.618]` and the antiperiodic is
`[-1.618, -1.618, 0.618, 0.618, 2]` — **the exact negative.** For odd `n` the antiperiodic momenta
ARE the periodic momenta shifted by `pi`, and `cos(k+pi) = -cos(k)`.

> **ON AN ODD LOOP THE FLUX IS ABSORBED INTO A SHIFT OF THE PROBE'S MOMENTUM. THIS PROBE CANNOT SEE
> IT — not because the record is absent, but because the carrier's ARITHMETIC hides it.**

**Stated carefully: this is a fact about a single particle hopping to nearest neighbours. Whether
some other probe can read an odd loop is untested,** and it is a sharp, cheap question.

**A DEFECT, LOGGED.** `w37c` TEST 2 projects a localised start into each sector and that projection
is degenerate at every `n`, so it printed "(a sector is empty)" throughout and measured nothing. It
is kept as written. The result rests on TEST 1 and TEST 3.

---

## ERRATUM (VECTORISATION) — **A REAL BUG IN W-32/33/34, AND IT MOVES NOTHING**

Found by a W-31 adversary. `numpy`'s `reshape(-1)` is **row-major**, so `vec(AXB) = (A ⊗ Bᵀ) vec X`
and the Lindblad generator is `-i(H⊗I - I⊗Hᵀ) + γ Σ (L⊗L* - I⊗I)`. Those lanes used the
**column-major** form `-i(I⊗H - Hᵀ⊗I)` with `kron(L*,L)`.

**Verified against RK4 with a deliberately non-symmetric complex state:** column-major is wrong by
`2.8e-02`; row-major matches to `5.1e-15`.

**All four scripts were patched and re-run. Every registered number is unchanged.** The diffs are
machine-precision only (`1.32e-16 → 2.41e-16`), signs of exact zeros, and reordering among
degenerate eigenvalues. **The reason is structural: the two conventions differ by the swap
permutation, so they are SIMILAR and every eigenvalue is identical** — and W-32's rates, W-34's
sieve ranking and W-33's steady-state counts are all spectral. **W-32's `1/(8g²)`, W-34's 28× margin
and W-33's slope `1.000000000` stand as registered.** W-35's main result used trajectory evolution
and never touched the generator; W-36 and W-37 evolve state vectors.

## W-31 — **ROUTE B: THE RESPONSIVE CARRIER, REFUTED 3/3. THE TOPOLOGY DID NO WORK.**

`LANE_W31_RESPONSIVE_CARRIER/`, sealed. Commissioned as 4 independent designs under distinct lenses,
3 judges, 1 build, 3 adversaries. **The registrar's own hypothesis was withheld from the designers.
The gr-faithful lens found it independently and sharpened it** — from "H depends on the state" to a
topology change: `||[R_E, H_capped]|| = 16/32/64 > 0` (writable while the cap exists) and
`||[R_E, H_punctured]|| = 0.000e+00` (exactly conserved once the hole opens). All three judges
picked it unanimously (`breaks_nogo = 9,9,9`).

**ALL THREE ADVERSARIES REFUTED IT, INDEPENDENTLY, AFTER REPRODUCING THE ARITHMETIC EXACTLY.**

> **ADVERSARY 2 BUILT A TOPOLOGY-FREE TWIN** — no hole, no cap, `b₁ = 0` everywhere, no carrier
> response: two copies of the same capped disk, the second with the writer set to `κ=0` by hand,
> joined by a leak. **It reproduces EVERY headline number to `1e-16`**, spread `0.107789` included.
> Because `ιᵀ H_disk(κ=0) ι = H_annulus + c·I` to `8.9e-16`: **the "punctured annulus" IS the
> zero-spoke-flux sector of the capped disk with the writer switched off.**

**ADVERSARY 3** independently built a 32-dimensional control — no hole, no second Gauss law, no Betti
number — and got the same numbers. **ADVERSARY 1** showed the headline metric is decoupled from what
it claims to measure: the `g²=0` null is forced by a weak symmetry `S` that anticommutes with `R_E`
and leaves all five "unbiased" starts exactly invariant; a record **does** form at `g²=0`
(`±0.145299`), contradicting the build's own reading; and the frozen value decomposes as
`+0.034219` population `+ 0.081116` **coherence** — a continuous readout of the initial relative
phase, so **nothing discrete was recorded at all.**

### WHAT THIS SETTLES

> **THE RESPONSIVE CARRIER CONTRIBUTED EXACTLY NOTHING. The load-bearing content was "the
> destination has no writer, and the transfer commutes with the record" — both hand-set.**

**And it converges with V003 from the opposite direction.** V003 concluded that nothing measured yet
REQUIRES the carrier to respond. Route B was the attempt to build a case that does, and the strongest
design three judges could pick reduces to a hand-set constant. **Two independent routes, same
answer: the gravity line is still empty, and the emptiness is now a result rather than a gap in
effort.**

## W-37d — **THE ODD-LOOP NULL IS ABOUT THE PROBE, NOT THE RECORD. OBJECTIVITY IS PROBE-RELATIVE.**

W-37c registered odd loops as carrying "exactly nothing" and the registrar billed it as a fact about
the carrier. **Tested; it is a fact about the probe.**

**MECHANISM (P1, confirmed).** A `Z_2` flux of `pi` and a sign flip of every hopping are the SAME
operation when `n` is odd, because negating all `n` amplitudes shifts the total flux by `n·pi`.
`spectrum(-H(flux 0)) == spectrum(H(flux pi))` at `n = 5,7,9,11` and NOT at `n = 4,6,8,10`. With
real hopping the position distribution is time-symmetric, so the two sectors become identical **by
position** — which is all the probe reported.

**DECISIVE (P3).** Same odd ring, same record, probe given a complex hopping phase:

```
   n      phase    max I(R:probe) bits
   5     0.0000               0.000000
   5     0.3000               0.922109
   5     1.5708               0.973503
   7     0.0000               0.000000
   7     1.5708               0.874649
```

> **NOTHING ABOUT THE RECORD CHANGED. THE NULL WAS THE PROBE'S.**

**CONSEQUENCE FOR THE PROCESS DESCRIPTION.** W-37 claimed condition 5 (redundant copying →
objectivity) was met. **It is met RELATIVE TO A PROBE.** A record can be present, protected, and
invisible to one probe while fully legible to another. **`V003` §1 condition 5 must be read with
that qualifier**, and "objective" in this program means "objective to probes that can couple to it."

**A FAILED PREDICTION, LOGGED AND NOT BUILT ON.** P2 predicted `Z_3` odd rings would read fine.
`Z_3` returned **exactly `0.000000` at every ring size including EVEN ones**, where `Z_2` gives
`0.999792`. That contradicts the `Z_2` result rather than extending it, so it indicates a defect in
the `Z_3` construction — most likely the partial trace, which matches gauge configurations across
probe positions that satisfy DIFFERENT Gauss laws. **Unresolved. Nothing is inferred from it.**

**ALSO CORRECTED.** `w37c`'s docstring asserts the odd-`n` spectra "coincide as SETS"; its own TEST 3
prints `different` at every `n`, and the true relation is that they are exact NEGATIVES. The register
entry for W-37c stated the negative relation correctly; the code comment is wrong and is superseded here.

---

## W-38 — **THE REGION IS NOT GIVEN. THE ENVIRONMENT DECIDES WHAT COUNTS AS A REGION.**

`LANE_W38_REGION/`, sealed. Opened on the principal's reading: **a region is another way of thinking
about a boundary.** On a graph that is an identity — a region IS a cycle that separates — so "which
region carries the record" and "which boundary is selected" are one question, and W-34 already
answered a special case of it while the registrar noted the general one in passing and moved on.

**15 regions** (subsets of the 4 plaquettes), each with its boundary loop. Sieve run seven times,
with the environment in a different place each time.

```
              bath       winner        rate    runner-up   margin   winner's boundary
                                                                    touching the bath
      CUT (centre) (0, 1, 2, 3)  7.1572e-02         (1,)    27.7x        0 of 8
 one corner plaq 0         (3,)  6.0883e-02         (2,)    16.4x        0 of 4
 one corner plaq 3         (0,)  6.0883e-02         (2,)    16.4x        0 of 4
     single link 0         (3,)  2.7401e-03         (1,)    14.1x        0 of 4
       left column         (3,)  4.5939e-02         (1,)     1.0x        0 of 4   (tie: two regions avoid it)
   RIM (perimeter)         (3,)  1.9812e+00         (0,)     1.0x        2 of 4   (no selection)
         all links         (0,)  3.9455e+00         (3,)     1.0x        4 of 4   (CONTROL: spread only 2.03x)
```

> **THE SURVIVING REGION IS ALWAYS THE ONE WHOSE BOUNDARY IS DISJOINT FROM THE ENVIRONMENT, AND IT
> MOVES WHEN THE ENVIRONMENT MOVES.** Bath at the centre → the WHOLE patch survives. Bath on corner
> plaquette `0` → the OPPOSITE corner `(3)` survives. Bath on corner `3` → corner `(0)` survives.
> Bath on a single link → a region avoiding it. **Same carrier, same Hamiltonian, same field. Only
> the environment's location changed.**

**THE CONTROLS FIRE CORRECTLY AND THEY ARE WHAT MAKE THIS READABLE.** With the bath on **all** links
no region is spared and the spread collapses to `2.03x` — no winner. With the bath on the **rim**,
which touches nearly every boundary, the margin is `1.0x` — no selection. And **"left column"
produces an honest TIE**, because regions `(1)` and `(3)` both have boundaries disjoint from
`[0,4,6,9]`. **When several regions avoid the environment, several regions tie.** The effect is
not "some region always wins"; it is specifically avoidance of the environment.

### WHAT THIS ESTABLISHES

**This is the first result in the program where a GEOMETRIC notion is an OUTPUT rather than an
input.** Every region in this program until now was chosen by the registrar — the 3×3 patch, its
perimeter, the rim loop. Here the carrier offers 15 regions and says nothing about which is real;
**the environment's placement picks one, with a margin of 14–28×.**

**Stated carefully, because the temptation to call this gravity is strong and premature:**

- **WHAT IS MEASURED:** what counts as a record-bearing region is determined by the matter/environment
  content, not fixed in advance. **Content decides geometry** — which is general relativity's central
  move, appearing here for the first time.
- **WHAT IS NOT MEASURED:** the graph is still static. Nothing deforms. What is selected is which
  SUBSET of a fixed complex is a region, not the complex itself. **This is not dynamical geometry
  and must not be reported as such.**

**And it is consistent with the whole night: it happened on a STATIC carrier.** W-31 (refuted 3/3),
V003, and now W-38 all point the same way — **the responsive carrier has not been needed for
anything yet, including for geometry to become an output.**

---

## W-39 — **RECORDS CROWD EACH OTHER OUT. THE CARRIER HOLDS 3, NOT 4, AND PROTECTION DEGRADES WITH EACH ONE.**

`LANE_W39_CAPACITY/`, sealed. Opened on the principal's objection: **dynamical geometry is unlikely
to appear at the level of a SINGLE record — a single record is a test particle, and test particles
never source geometry.** It would emerge where MANY records must share a carrier.

**CAPACITY.** The algebraic bound is `4` and is **FORCED** — it is the cycle rank, i.e. the dimension
of the physical space, and is reported only so it cannot be mistaken for a finding. The geometric
bound — can a set be simultaneously protected, i.e. does a nonempty bath avoid every boundary at
once — is **3**.

> **THE TWO DISAGREE. THE LIMIT IS PACKING, NOT DIMENSION.** `k=4`: **zero** independent sets are
> simultaneously protectable. Example of a pair that provably cannot coexist: regions `(0,3)` and
> `(1,2)`, whose boundaries together cover all 12 links, so **no bath avoids both.**

**AND THE CAPACITY NUMBER UNDERSTATES IT — PROTECTION DEGRADES AS RECORDS ARE ADDED:**

```
   k  |bath|   gamma  gamma*|bath|  worst member  best non-member   margin
   1       8   0.500          4.00    6.7285e-02       2.9460e+00    43.8x
   2       5   0.800          4.00    5.3364e-02       1.0612e-01     2.0x
   3       2   2.000          4.00    5.8497e-02       6.2405e-02     1.1x
```

**THE CONFOUND WAS REAL AND IS CONTROLLED.** The protecting bath necessarily SHRINKS as records are
added (8 → 5 → 2 links), so a weaker environment could explain the collapse by itself. **RUN 2 holds
the total dissipation fixed at `gamma·|bath| = 4.00` and the margin collapses identically: `43.8x →
2.0x → 1.1x`.** The crowding is not the bath weakening. (RUN 3, holding `|bath|` literally constant
at 2, is confounded in the other direction — with so small a bath many regions are protected at once
— and is retained but not read.)

> **AT `k=3` THE MARGIN IS `1.1x`: TWO OF THE THREE RECORDS ARE BARELY DISTINGUISHED FROM
> UNPROTECTED OPERATORS. THE USABLE CAPACITY IS NEARER 2 THAN 3.**

### WHAT THIS DOES TO THE GRAVITY CONCLUSION

**V003 and W-31 concluded that nothing measured REQUIRES a responsive carrier, and the registrar
offered the principal two readings: either records genuinely do not need gravity, or we had not
found the forcing measurement. The principal supplied a third, and it is better than both:
WE HAD NOT BUILT THE STAGE.**

**Every result up to W-38 used exactly ONE record on a passive background.** Nothing there could
have detected backreaction, in the same way a test particle cannot detect that it curves spacetime.

**W-39 is the first measurement in which records constrain EACH OTHER** — they compete for
environment placement, the competition is measured and controlled, and it has a hard limit at 3 and
a practical limit near 2. **That mutual constraint is the precondition for backreaction, and it is
where a responsive carrier could first do work.** Whether it does is untested.

**NEXT.** The carrier's capacity is a property of a FIXED graph. **Ask what happens when the packing
constraint has no solution** — `k=4` is already such a case here. On a static carrier the answer is
that the fourth record simply fails. **A responsive carrier is exactly the thing that could answer
differently, and that is the first question in this program where it could matter.**

---

## W-40 — **REDUNDANCY MEASURED. READING IS FREE; STORING IS NOT.**

`LANE_W40_REDUNDANCY/`, sealed. W-37 claimed condition 5 and **argued** it from `||[R,H_hop]|| = 0`.
W-37e's two-probe attempt returned zero, which was exclusion — hard-core probes never complete a
circuit, and a return trip flips every link twice giving `R² = I`. **Let them pass and measure it.**

```
    n   k   dim        I per probe (bits)          I joint
    4   1     8      0.9333                        0.9333
    4   2    32      0.9333  0.9333                0.9924
    4   3   128      0.9333  0.9333  0.9333        0.9989
    5   3   250      0.7342  0.7342  0.7342        0.9737
    6   3   432      0.8079  0.8079  0.8079        0.9869
```

> **EACH PROBE ALONE HOLDS THE BIT, AND ADDING PROBES DOES NOT COST THE OTHERS ANYTHING — the
> per-probe value is IDENTICAL at `k = 1, 2, 3`, to four decimals.** The joint value climbs toward
> `1` (`0.9333 → 0.9924 → 0.9989`), so the copies are independent samples rather than one shared
> copy. **Condition 5 is measured.**

**WHY THE PER-PROBE VALUE IS EXACTLY UNCHANGED, since an exact identity always deserves suspicion:**
the probes couple to each other only through the gauge field, and what they read — the global flux —
**is conserved (`[R,H] = 0`)**. So each reads the same undisturbed quantity independently. That is
the QND property doing its work, and it is what we set out to verify, not an artifact.

**CONTROLS.** `tau = 0`: `||H|| = 0.000e+00`, nothing moves, nothing is learned. **Real hopping:
`n=4` gives `0.9998`, `n=6` gives `0.9827`, and `n=5` gives EXACTLY `0.0` for every probe** — W-37d's
probe-relativity reproduced here, and it applies per-probe.

### THE ASYMMETRY, AND IT IS THE POINT

> **MANY OBSERVERS CAN READ ONE RECORD WITHOUT INTERFERING (W-40: no per-probe cost at all).
> MANY RECORDS CANNOT SHARE ONE CARRIER WITHOUT DEGRADING EACH OTHER (W-39: margin `43.8x → 2.0x →
> 1.1x`, controlled for bath strength).**
>
> **READING IS FREE. STORING IS NOT.**

The two measurements use the same machinery and differ only in what is multiplied. **Storage is what
has a capacity, and capacity is what could force a carrier to respond.** Observation cannot, and
W-40 is what rules it out rather than leaving it assumed.

**`PROCESS_DESCRIPTION_V003` §1 condition 5 is upgraded from ARGUED to MEASURED**, and keeps W-37d's
qualifier: **objective to probes that can couple to it.**

---

## W-41 — **k=4: THE CARRIER EVICTS. IT DOES NOT SHARE THE DAMAGE.**

`LANE_W41_K4/`, sealed. W-39 established the packing constraint has no solution at `k=4`. Demand it
and watch the failure mode, because the failure mode is the physics.

**A DERIVATION THAT ALSO MAKES THE SCAN CHEAP.** For the adjoint Lindbladian the coherent term
contributes **nothing** to the first-order rate — `Tr(O† i[H,O])` is purely imaginary for Hermitian
`H` — and at `Z_2` a Wilson loop and a link operator either commute or anticommute. So

> **`rate(O) = 2·gamma·|bath ∩ boundary(O)| + O(g⁴)`. The decay rate is literally a COUNT of how many
> bath links sit on the boundary.** W-32, W-38 and W-39 in one line.

**VALIDATED AGAINST THE FULL SPECTRUM before being used:** `|overlap| = 1` → `0.92–0.99`;
`|overlap| = 0` → `0.003–0.06`, the `g⁴` residue.

**THE RESULT.** Of 793 baths, **zero** protect all four — the constraint genuinely has no solution.
And the failure is not shared:

```
  bath [0], confirmed on the full 256x256 spectrum
     region (0,)   rate 9.2242e-01   EVICTED
     region (1,)   rate 3.8571e-02   protected
     region (2,)   rate 3.8571e-02   protected
     region (3,)   rate 2.7401e-03   protected
```

> **THREE RECORDS SURVIVE AT THE `g⁴` RESIDUE AND ONE IS THROWN OUT, A FACTOR OF 24–340x WORSE.
> THE CARRIER HAS A HARD CAPACITY OF 3 AND ENFORCES IT BY EVICTION, NOT BY DEGRADING EVERYONE.**

**AND WHICH ONE DIES IS SET BY GEOMETRY.** Each link lies on 1 or 2 of the four boundaries. A bath
on a **multiplicity-1** link evicts exactly **one** record; on a **multiplicity-2** link it evicts
**two**. **Where the environment sits decides how many records die**, and the count is exact.

### WHAT THIS OPENS

**On a static carrier the fourth record simply fails.** There is no negotiation and no deformation —
the capacity is enforced instantly and cleanly. **This is the first question in the program where a
responsive carrier could give a DIFFERENT answer that would mean something:** instead of evicting,
a carrier that could grow — one more plaquette, one more link — could accommodate the fourth.

**That makes the gravity-shaped mechanism concrete and testable for the first time: CONTENT
EXCEEDING CAPACITY FORCES THE CARRIER TO EXPAND.** The prerequisite measurement is whether capacity
actually grows with carrier size — `4` plaquettes give capacity `3`; what do `6` or `9` give? If
capacity tracks size, "demand exceeds capacity → the carrier grows" is a well-posed dynamics rather
than a wish. **Untested.**

---

## W-42 — **CAPACITY = AREA − 1, EXACTLY. AND IT CORRECTS W-39.**

`LANE_W42_CAPACITY_LAW/`, sealed. Prerequisite for "content exceeding capacity forces the carrier to
expand": capacity must actually depend on size.

W-41's counting formula removes the Hilbert space entirely. The boundary map is **linear over GF(2)**;
a set of records is simultaneously protectable iff **some link lies on none of their boundaries**;
and that is **one linear condition**. So capacity `= max_L dim ker(f_L)`.

```
     patch  verts  links  plaq m  cycle rank  capacity   = m-1
       3x3      9     12       4           4         3    yes
       4x3     12     17       6           6         5    yes
       4x4     16     24       9           9         8    yes
       5x4     20     31      12          12        11    yes
       5x5     25     40      16          16        15    yes
```

**Cross-checked against W-39's explicit brute force at `3x3`: both give `3`.**

> **CAPACITY = m − 1 = AREA − 1**, where `m` is the number of plaquettes, which for a planar patch is
> the area in lattice cells and equals the cycle rank.

### ERRATUM TO W-39

**W-39 reported capacity `3` as a GEOMETRIC bound, contrasted with the FORCED algebraic bound `4`,
and concluded "the limit is packing, not dimension." THAT CONCLUSION IS WITHDRAWN.** `m − 1` is the
kernel dimension of a single linear functional — **it is forced too**, just one less than the space's
dimension rather than equal to it. The registrar drew the forced/not-forced line in the wrong place.

**W-39's other results are unaffected**: the *measured* crowding (margin `43.8x → 2.0x → 1.1x`, with
total dissipation held fixed) is dynamics, not counting, and stands. So does W-41's eviction.

### AND THE HONEST READING, WHICH CUTS AGAINST AN EASY STORY

```
    3x3: area  4  perimeter  8  capacity  3     cap/area 0.750   cap/perimeter 0.375
    4x4: area  9  perimeter 12  capacity  8     cap/area 0.889   cap/perimeter 0.667
    5x5: area 16  perimeter 16  capacity 15     cap/area 0.938   cap/perimeter 0.938
```

> **CAPACITY TRACKS AREA, NOT PERIMETER.** `cap/area → 1` while `cap/perimeter` grows without bound.
> **This is NOT a holographic or boundary-law count and must not be reported as one** — the registrar
> has already conflated two different area laws once in this program (confinement vs Bekenstein) and
> will not do it again.

**WHAT IT BUYS.** The dynamics is now well-posed: **to hold `k` records a carrier needs area `≥ k+1`.**
Below that it evicts (W-41). **"Demand exceeds capacity → the carrier must grow" is a statement with
a number in it**, and the number is one plaquette per record.

---

## CORRESPONDENCE AUDIT — **THE EMPTY GRAVITY LINE IS A PROPERTY OF OUR GRAPH, NOT OF RECORDS**

`GRAVACLE_CORRESPONDENCE_V001.md`, sealed. The principal directed that the program not re-cover
ground already in `10.5281/zenodo.21238968` (Gravacle v337), the guard against fitting being to test
for it afterwards rather than to avoid the source.

**FITTING LINE, VERIFIED BY SEARCH:** before today the project contained **zero** substantive
references to the paper — the only hits are the GitHub org name. **W-27 to W-42 are uncontaminated.
W-43 onward is not, and must be flagged.**

**THE ONE THING THAT CHANGES A CONCLUSION.** The paper's Field-Registration Principle: *EM enters
records through gauge/action phase; gravity enters through metric/proper-time action.* **Our carrier
has gauge phase and a Gauss law, and its links have no length, no metric, no proper time, no clock.**

> **"GRAVITY IS ABSENT FROM THE PROCESS" IS NOT A RESULT ABOUT RECORDS. IT IS A RESULT ABOUT OUR
> GRAPH. We never installed the thing gravity enters through.** V003 and the W-31 refutation both
> reported the empty line as though it were a finding about record formation. **Withdrawn.**

**AND IT DIAGNOSES ROUTE B.** W-31 made the carrier's **topology** dynamical. Gravity is said to
enter through **metric**. **Route B varied the wrong degree of freedom** — which is why three
adversaries found the topology contributed exactly nothing.

**INDEPENDENT CORRESPONDENCES, all produced before reading:** the paper's **Action-Holonomy Sign
Theorem** (the interference sign IS the holonomy of a closed oriented action loop) against W-37's
cut-ring control at exactly `0.000000`; and its **Single-Run Boundary Closure Theorem** (exact
selection is single-run closure, Born capacity is the public ensemble law) against W-35's
`E[<R>] = -0.015 ± 0.040` beside `E[<R>²] = 0.999`. **The second match is precise and it overturned
four of this program's own lanes before the paper was consulted.**

**WHERE THIS PROGRAM SITS IN THE PAPER'S OPEN PROBLEM.** Appendix C names the **accumulation proof**
as unsolved: (1) a local record-to-geometry map, (2) compatibility across overlapping record
patches, (3) the large-record limit. **W-39/41/42 are step 2 with numbers in it.** But our records
carry no geometry, so **capacity constrains how many records fit and says nothing about a metric.
Step 2 has the right shape and no content because step 1 is missing.**

**THE MISSING TERM, CONCRETELY.** Links need a **length / proper-time weight**. Then a transported
probe accumulates a gauge **product round a closed loop** (homotopy-invariant — we have it) and a
**sum of lengths along its path** (not homotopy-invariant — we do not). **Structurally different,
and the difference is measurable: one is blind to path length, the other is not.**

**FITTING RISK FLAGGED IN ADVANCE.** W-37d's complex hopping phase is formally what a proper-time
weight contributes, and it is tempting to claim we already saw gravity. **We did not.** That phase
was **uniform and installed by hand** to break a time-reversal symmetry; a metric weight must **vary
across links and be sourced**. The separating test is uniform versus varying phase, and whether
anything sources the variation.

---

## W-43 — **LOCAL RECORDS ARE OBJECTIVE FOR FREE; THE ONE THE DYNAMICS SELECTS IS NOT**

`LANE_W43_METRIC/`, sealed. **CONTAMINATED LANE — designed after reading Gravacle v337.**

**W-43's chirality test failed twice and both failures are logged rather than hidden.** The measure
was broken (the antipodal site weighted `-n/2` when it is equally `+n/2`, so a symmetric
distribution scored `-0.419` — exactly the "nothing added" baseline). And the concept was wrong: **a
`Z_2` flux cannot break time reversal, because `0` and `pi` are both TR-invariant**, so chirality
could never separate a `Z_2` gauge record from a metric one. **Nothing is inferred from it.**

**W-43b, the measurement that works.** Same environment, same coupling, same machinery as W-36:

```
  GAUGE record  (rim Wilson loop, a product over 8 links)
    |F| : 0      1      2      3      4      5      6
    I   : 0.000  0.044  0.100  0.187  0.351  0.658  0.929      ratio 0.047

  LOCAL record  (a two-level variable at one site)
    I   : 0.000  0.999  1.000  1.000  1.000  1.000  1.000      ratio 0.999

  CONTROL kappa = 0, both:  <= 9.5e-15 at every fragment size
```

### THE HONEST LIMITATION, BEFORE THE RESULT

> **THIS IS NOT A GRAVITY MEASUREMENT.** The "metric record" is a two-level mass at one site with
> `H_sys = 0` and the environment coupled to it **directly**. **The potential it would source never
> enters the dynamics.** So W-43b compares a LOCAL observable against a NONLOCAL one — and that a
> local thing is locally copyable is close to a tautology.

### WHAT IS NOT TAUTOLOGICAL

> **THE RECORD THE DYNAMICS SELECTS IS THE NONLOCAL ONE.** W-34's sieve, nominating nothing, picked
> the full boundary by a factor of **28**. So the carrier protects precisely the record that **cannot
> be made objective**, while the record that is objective for free is **not** the one it protects.

**PROTECTION AND OBJECTIVITY PULL APART, AND THE TWO SIT ON OPPOSITE SIDES.** W-36 named this as
legible-vs-protected; W-43b puts both numbers on one page under identical conditions: `0.047`
against `0.999`. **And the only structural difference is whether the observable lives on a closed
loop or at a point.**

**NEXT, AND IT IS THE REAL TEST.** Make the potential do work: let it source a phase that a
transported probe accumulates, so the metric enters the dynamics rather than being a label the
environment reads off. **Then ask whether THAT is redundantly readable, and whether the sieve still
prefers the loop.** Until then the gravity line has a candidate term and no measurement.

---

## W-45 — **CAPACITY PASSES ALL FOUR OF GRAVITY'S FUNCTIONAL MARKERS, WITH NO METRIC ANYWHERE**

`LANE_W45_FUNCTIONAL/`, sealed. Opened on the principal's standing correction, given twice and
ignored twice by the registrar: **do not expect the full footprint of CLASSICAL gravity at the
record level; it will look different while performing the same function.** *"An early embryo doesn't
look like a human."* The W-44 workflow specifies gravity by metric, proper time and clocks — its
classical form — and therefore imports precisely the assumption we were told to stop importing.

**So test by FUNCTION.** Gravity's signature, stripped of its classical shape, against **capacity**
— a quantity that arose from this program's own measurements (W-39, W-41, W-42) and not from gravity.

```
  F1  UNIVERSAL SOURCING   every record consumes; there is no neutral record
        15 of 15 records consume exactly 1; consumption values observed: [1]         PASS
  F2  NO SCREENING         a record cannot hide behind others and avoid paying
        0 screened cases of 1152 with capacity genuinely available                   PASS
  F3  ONE SIGN             nothing ever frees capacity; there is no negative record
        no record of any size increases what is available to others                  PASS
  F4  ARENA, NOT FORCE     it never appears in H and exerts nothing; it sets what
        is POSSIBLE -- k=1,2,3 possible, k=4 IMPOSSIBLE, no arrangement exists       PASS
```

**F2 FAILED AS FIRST WRITTEN AND THE FAILURE WAS THE TEST.** `108 of 1260` additions appeared to pay
nothing — but in every one of them **capacity was already exhausted**, so there was nothing left to
charge. That is **saturation, not screening.** Gating on capacity `> 0` beforehand gives **zero**
screened cases. Both versions are retained in the lane.

**AND THE CONTRAST IS SHARP.** The `Z_2` charge on the same carrier fails **all four**: it has two
signs, charges annihilate in pairs (`1+1 = 0 mod 2`), and a neutral sector exists (`8` of `16`
configurations are globally neutral). **EM screens. Capacity cannot.**

### WHAT IT IS

> **CAPACITY IS ANOTHER WORD FOR ROOM. And `capacity = area - 1` exactly (W-42), so it is not a
> metaphor for space — IT IS THE AREA, MINUS ONE.**

Everything takes some, nothing makes more, nothing can avoid paying, and it never pushes anything
around — it only decides what can coexist. **That is what space does with respect to matter, derived
here from record dynamics on a pure gauge theory with no metric, no proper time and no clock
installed anywhere.**

**STATED AT ITS PROPER STRENGTH.** This is a functional match, not a metric. Capacity is presently a
**static bookkeeping quantity of a fixed graph** — it has no dynamics of its own, nothing sources a
change in it, and nothing expands. **It is the embryonic form the principal named, and it should be
reported as that and not as gravity.**

**NOT HOLOGRAPHIC, AND THE REGISTRAR WILL NOT CLAIM OTHERWISE.** Capacity tracks the extensive
measure (plaquettes), not the boundary (W-42: `cap/area -> 1` while `cap/perimeter` grows without
bound).

### THE NEXT STEP, AND IT IS NOW MOTIVATED FROM INSIDE

**MAKE CAPACITY DYNAMICAL.** Not "let the graph's topology respond" (Route B, refuted 3/3) and not
"install a metric" (W-44, an imported classical shape). **Let the carrier's ROOM change in response
to demand.** W-41 already measured the alternative: on a fixed carrier, demand beyond capacity is
resolved by **eviction**. So the dichotomy is sharp and it is ours, not borrowed:

> **EITHER THE CARRIER GROWS, OR RECORDS ARE EVICTED. Both are measurable, and only one of them
> looks like an expanding arena.**

---

## W-46 — **STORAGE IS A VOLUME LAW. LEGIBILITY IS A BOUNDARY LAW. BOTH READINGS WERE RIGHT.**

`LANE_W46_HOLOGRAPHY/`, sealed. The principal proposed that gravity and capacity converge exactly at
the Bekenstein/holographic bound. W-42 had measured `capacity = area - 1`, a **volume** law, and the
registrar recorded that as a disagreement. **It was not a disagreement. Two different quantities had
been run together.**

- **STORAGE** — how many independent records a region can HOLD.
- **LEGIBILITY** — how many an observer confined OUTSIDE the region can DISTINGUISH.

**Holography is a claim about what escapes, not about what fits.** Measured, for an `n x n` block of
plaquettes:

```
   |A|  perimeter  STORAGE  LEGIBLE   storage/|A|   legible/perimeter
     1        4        0        1         0.000            0.250
     4        8        3        3         0.750            0.375
     9       12        8        5         0.889            0.417
    16       16       15        7         0.938            0.438
```

> **STORAGE = |A| - 1 = n² - 1 — the BULK.**
> **LEGIBILITY = 2n - 1 = perimeter/2 - 1 — the BOUNDARY.**

`storage/|A| -> 1` while `legible/perimeter -> 1/2`. **Storage scales with area, legibility with
perimeter, on the same regions in the same measurement.**

### WHAT THIS SETTLES

> **A REGION CAN HOLD MORE THAN IT CAN EVER TELL YOU, AND THE GAP GROWS WITH ITS SIZE.** At `n=4`,
> `15` records are storable and `7` are externally distinguishable. The ratio diverges as `n`.

**AND IT IS THE SAME FACT THIS PROGRAM KEPT MEASURING FROM OTHER DIRECTIONS.** W-36: a gauge record
has no redundancy in a local environment (`0.047`). W-43b: `0.047` against `0.999` for a local
observable, identical conditions. W-37: reading requires transport around a CLOSED path, and cutting
the ring gives exactly `0.000000`. **All four are the boundary law seen from different sides.**

**THE CORRECTION IS THE REGISTRAR'S.** W-42 stated "capacity tracks area, not perimeter — this is
NOT a holographic count" and warned against conflating two area laws. **That warning was right about
STORAGE and wrong to close the question**, because the holographic claim was never about storage.

**FORCED-OR-NOT, STATED PLAINLY.** This is a rank computation, so it IS a counting fact: only the
boundary layer of `A` pairs with anything outside, so the rank is the perimeter's. **That is not a
defect — it is the mechanism.** Holography here is the statement that *the outside touches only the
edge*, and the arithmetic says so exactly.

---

## W-47 — **THE COMPOSED LAW: FORM SURVIVES, CONSTANT IS OFF BY ~4x**

`LANE_W47_COMBINED/`, sealed. **The first lane in this program that composes measured relations into
a single prediction and tries to break it.** Every prior lane measured one relation.

**THE COMPOSITION.** EM gives a holonomy on a closed boundary of perimeter `P` (W-27, W-34). Alpha
gives its decay rate `Gamma = 32 g^4` (W-32) and its readout time `T_read = 0.30 P/tau` (W-37b).
Capacity gives the boundary law `P/2 - 1` for what escapes (W-46). A record is exportable only if it
is read before it decays:

> **`X = Gamma · T_read = 9.6 · g⁴ · P / tau  <  1`**
>
> **The falsifiable content is that the surviving fraction depends on `X` ALONE** — three parameters
> must collapse onto one curve.

```
   X band                        n    mean I/I0     sd
   X < 0.5   predicted LEGIBLE   16     0.4826    0.2130
   0.5 - 1.5 transition          15     0.1599    0.1051
   1.5 - 4.0                     16     0.0305    0.0259
   X > 4     predicted ILLEGIBLE 17     0.0036    0.0032

   spread at fixed X:  X=0.37 -> 0.394   X=1.0 -> 0.169   X=2.7 -> 0.022   X=20 -> 0.001
```

**WHAT PASSES.** The surviving fraction falls **130x monotonically** across the `X` bands, and points
at the same `X` from different `(P, tau)` agree ever more closely as `X` grows — absolute spread
`0.394 -> 0.001`. **The composition has the right form: readability is gated by the single product
`Gamma·T_read`, not by `P`, `g` and `tau` separately.**

**WHAT FAILS, AND IT WAS DECLARED IN ADVANCE AS THE WEAKER FAILURE MODE.** Half the readability is
lost at **`X ~ 0.25`**, not at the predicted `X = 1` — **the constant is off by about a factor of 4.**
And the RELATIVE spread does not shrink (`sd/mean` runs `0.44, 0.66, 0.85, 0.89`), so the collapse is
**suggestive, not clean.**

> **VERDICT: the composed law is CONFIRMED IN FORM AND NOT IN CONSTANT.** It is one relation binding
> EM, alpha and the capacity/boundary law, it makes a prediction, and the prediction is about a
> quarter right in magnitude. **That is a partial pass and is registered as one.**

**TWO DEFECTS, BOTH CAUGHT BEFORE READING ANYTHING.** v1's decay channel was `P+ - P-`, which **is**
`R` — W-30a proves such a channel cannot move the record, and indeed `I` was identical to six
decimals across every `g^2`. v2 compared raw `I` across `n` when bare readability differs by `n`
independently of decay. **Both are in the lane conventions; the reported numbers are v3.**

---

## W-48 — **THE DECOHERENCE HALF OF OUR LAW IS TEXTBOOK. THE POWER LAW WAS OURS, NOT NATURE'S.**

`LANE_W48_VS_STANDARD/`, sealed. Run **before** touching any experimental data, on the principal's
own guard: if the composed law is `exp(-Gamma T)` in lattice clothing, fitting it to C70 or Panda
data would be curve-matching a textbook result and calling it confirmation.

```
  I_max   (max over t -- what W-47 reported)      n=48
     EXPONENTIAL  rms log-resid 1.2783
     POWER LAW    rms log-resid 0.6425      <- power law wins by 0.64

  I_fixed (at T_read, NO optimisation)            n=44
     EXPONENTIAL  rms log-resid 1.0229      <- exponential wins by 0.08
     POWER LAW    rms log-resid 1.0991
```

> **THE POWER LAW EXISTS ONLY IN THE OPTIMISED SIGNAL. Taking a max over time of a decaying-but-
> still-rising quantity manufactures it. The un-optimised signal is exponential in `X`, which is
> exactly what standard decoherence predicts.**

**SO ON THIS AXIS OUR COMPOSED LAW ADDS NOTHING.** `X = Gamma·T_read` gating legibility is
`exp(-Gamma T)` with `T` fixed by the loop's perimeter — and that a holonomy is unreadable once the
ring exceeds the coherence length is textbook mesoscopic physics. **Taking W-47 to C70 or Panda data
would have fitted a known result and called it confirmation. It is not done.**

**HONEST ABOUT THE STRENGTH.** Exponential beats power law by only `0.08` in rms log-residual, and
**both fits are poor** (`~1.0` in log-residual is a factor of `e` of scatter). The correct statement
is *consistent with exponential, marginally better than power law, neither fitting well* — **not
"confirmed exponential."**

### WHAT THIS LEAVES, AND IT IS A SHARPENING RATHER THAN A LOSS

**The composed law has two halves and they are not equally novel.**

- **THE ALPHA / DECOHERENCE HALF IS STANDARD.** Decay rate times readout time gating survival. W-48
  says so plainly. **Do not take it to data as though it were new.**
- **THE CAPACITY HALF IS NOT A DECOHERENCE STATEMENT AT ALL.** `storage = area - 1`,
  `legibility = perimeter/2 - 1`, capacity enforced by **eviction**, and capacity satisfying all
  four of gravity's functional markers while EM's charge fails all four. **Standard decoherence says
  nothing whatever about how much a region can hold versus export.**

> **THE NOVEL CONTENT, IF THERE IS ANY, IS ON THE GRAVITY/CAPACITY SIDE — AND IT HAS NEVER BEEN
> TESTED AGAINST ANYTHING.**

**AND THAT CHANGES WHICH LITERATURE IS RELEVANT.** C70 and Panda measure coherence against transit —
the half we now know is standard. **The storage-versus-legibility claim belongs to topological
codes**, where the count of logical operators, their nonlocality, and the readout of nonlocal
observables are the actual physics. That is a different corpus from the one in the paper's registry.

---

## W-44 — **A METRIC THAT GENUINELY DOES WORK BUYS NOTHING. AND IT KILLS W-43b.**

`LANE_W44_METRIC_DYNAMICS/`. **CONTAMINATED LANE, and specified wrongly on purpose-in-hindsight:**
it defines gravity by its CLASSICAL form — metric, proper time, clocks — which is the import the
principal had already flagged twice. **Read under that rule: a classical-shaped null reads two ways.**

Three independent builds (link length, site potential, clock), registrar's expectation withheld,
then three adversaries. **The adversaries verified independently that the metric really does work
this time:** it enters `H` only multiplied by the coupling knob, no jump operator touches it
(`max ||[N_M⊗I, L_k]|| = 0.000e+00`), and coupling-zero reproduces separately built no-metric
carriers to `~1e-14`. **That is precisely where W-43b failed, and it is not repeated.**

### REDUNDANCY — UNANIMOUS NULL, AND IT OVERTURNS W-43b

```
  single-fragment / whole-environment Holevo ratio, same state, same fragments
  build                                 metric    gauge
  link-length, length on a rim link     0.0758   0.0478
  link-length, length on a cut link     0.0385   0.0509
  site-potential, env on cut links      0.0090   0.0046
  site-potential, env at the mass       0.0013   0.0835
  clock                                 0.0135   0.0105
```

> **EVERY VALUE IS FAR BELOW `0.5`, AND THE ORDERING FLIPS WITH PLACEMENT. A metric degree of freedom
> that actually participates in the dynamics acquires NO redundancy, and NO advantage over the gauge
> loop.** Three independent constructions agree.

**W-43b's HEADLINE IS WITHDRAWN.** Its metric record scored `0.999` — a full bit from a single
fragment — **because the environment was coupled directly to the mass operator while `H_sys = 0`.**
The registrar flagged that limitation in the lane conventions and in the register at the time. **The
flag was right and the number was an artifact.** With the metric doing real work it scores `0.0013`
to `0.0758`.

**WHAT SURVIVES OF W-43b:** nothing of the metric side. **W-46 is unaffected** — storage-vs-legibility
is a GF(2) rank computation, not a redundancy measurement.

### SELECTION — THE RIM STILL WINS, BUT THE CONTEST IS TWO OPERATORS

At every reported operating point the slowest operator is still the full-boundary Wilson loop
tensored trivially on the metric (`3.16e-03` clock, `2.94e-03` site, `1.66e-02` link). **But an
adversary counted the bath commutant directly: only `8` of `64` dictionary operators commute with
all four jump operators — `56` are excluded by COUNTING before any dynamics runs.**

**And the winner is not robust.** Sweeping the metric's tunnelling rate `eps`, which the builds
declared unmotivated and never swept:

```
  lam=0.6, g2=0.01:  eps=0.01  RIM 3.164e-03  I(x)sz 4.954e-04   METRIC WINS
                     eps=0.02  RIM 3.164e-03  I(x)sz 1.978e-03   METRIC WINS
                     eps=0.05  RIM 3.164e-03  I(x)sz 1.217e-02   rim wins  3.85x
                     eps=0.15  RIM 3.163e-03  I(x)sz 9.192e-02   rim wins 29.06x  <- reported
```

At `eps=0.02` the slowest non-trivial left-eigenmode of the full `1024x1024` Lindbladian matches
`I⊗sz_M` at overlap `0.975`, so **this is not a dictionary artifact.** And the margin itself is
estimator-dependent: `2.56` at `T=1`, `30.9` at `T=10`, `3.95` at `T=1000`.

> **"THE SIEVE SELECTS THE GAUGE BOUNDARY EVEN WITH A METRIC PRESENT" IS A REPORT ON THE RATIO
> `eps/g²`, NOT A ROBUST FACT.** The winner is stable in `T` but not in `eps`.

### DEFECTS THE ADVERSARIES FOUND

**Site-potential transport stage: REFUTED** — a controlled-phase between the readout register and
the projector onto the very quantity whose Holevo is reported. **Clock section 5: REFUTED twice** —
`np.diag(np.arange(DC)) - (DC-1)/2.0` subtracts from **every matrix element**, not the diagonal
(shipped `<C> = -4.500` where the design requires `0.000`), and the fringe-contrast statistic is
blind: with the bug fixed, contrast is `1.000000` at every `omega` while `S(clock)` rises to `1.61`
bits. **Link-length transport: weakened** — the length register is frozen there, so the reading is a
probe seeing a static classical defect. **All three failures are in the third, UNREQUESTED stage.**

### THE READING, AT ITS PROPER STRENGTH

**Installing a metric — three ways, with the metric verified to participate — changed nothing about
redundancy and does not robustly change what the carrier protects.** Under the principal's standing
rule this reads two ways: either a metric is not what performs gravity's function at the record
level, **or** our carrier is not one where a classical-shaped metric can do anything. **It is not
evidence that gravity is absent, and it is not a baseline.**

**AND IT LEAVES W-45 STANDING AS THE BETTER ROUTE.** Capacity — which required no metric at all —
passes all four functional markers. **The classical-shaped install bought nothing; the
functional identification bought four for four.**

---

## W-49 — **CAPACITY ACQUIRES DYNAMICS. THE CARRIER'S SIZE IS SET BY WHAT IS RECORDED IN IT.**

`LANE_W49_CAPACITY_DYNAMICS/`, sealed. W-45 left capacity passing all four of gravity's functional
markers as **static bookkeeping with no equation of motion**. This gives it one.

### A METHODOLOGICAL FINDING THAT REACHES BACK THROUGH THE PROGRAM

**w49 failed and its controls diagnosed why: `<Nhat> = 0.50000` at every `mu` from `0` to `8`.** The
energy cost did nothing.

> **EVERY BATH IN THIS PROGRAM, FROM W-28 ONWARD, USED UNITARY JUMP OPERATORS. A unitary jump
> operator is unital: it drives the state toward maximally mixed. THAT IS AN INFINITE-TEMPERATURE
> BATH.** It is adequate for the dephasing and pointer questions the program has been asking, **but
> an energy cost cannot register in it, so no energetic question could ever have been asked.**

(A second failure: extracting a steady state as a null eigenvector returns an arbitrary element of a
degenerate manifold, which need not be a state — the `Delta=0` control returned `<Nhat> = -0.208`,
impossible for a projector. Steady states are now obtained by **evolving a physical state**.)

### WITH A THERMAL BATH, AND THE RECORD ACTUALLY CONSERVED

A Davies bath with detailed balance at temperature `T`, coupled to the **structure alone**
(`A = I_gauge ⊗ sigma_x`), so every plaquette flux is exactly conserved and records persist.
`<Nhat>` then tracks Gibbs to `1e-9`, and `T -> infinity` recovers the old `0.5`.

**The record must be conserved or the sectors mix and the test is void.** `g²·ELEC` does **not**
commute with the plaquettes (`||[R2,H]|| = 1.265` at `g2=0.05`), so the first pass leaked and showed
a spurious `4e-4`. At `g2 = 0` the commutator is `0.000e+00`:

```
     mu     T    g2  gate   <N | R2=-1>   <N | R2=+1>    difference
   1.00   0.5  0.05  1.00      0.760505      0.760886     3.811e-04   <- leaking, void
   1.00   0.5  0.00  1.00      0.011863      0.852879     8.410e-01
   2.00   0.5  0.00  1.00      0.005835      0.500000     4.942e-01
   1.00   0.5  0.00  0.50      0.035575      0.500000     4.644e-01
   1.00   0.5  0.00  0.00      0.147121      0.147121     1.943e-16   <- CONTROL
```

> **THE CARRIER IS ESSENTIALLY ABSENT (`0.012`) OR ESSENTIALLY PRESENT (`0.853`) DEPENDING ON A
> SINGLE BIT OF RECORD CONTENT. Remove the structure-content coupling and the difference is exactly
> zero.** Content determines geometry, dynamically, measured.

### AT ITS PROPER STRENGTH

**Nothing in `H` references a record, a boundary or a capacity.** The only structure-content coupling
is the gating `-Nhat ⊗ (W2 + h.c.)` — **which is what it MEANS for the carrier to have that
plaquette**, not an extra assumption. No rule says "grow when full". The correlation is a consequence.

**But this is thermodynamics, not new physics.** A degree of freedom whose energy depends on a
conserved quantity will have a conserved-quantity-dependent equilibrium; that is Boltzmann.
**What it changes is the program's ledger, not the physics literature:** item 14 moves from *static
bookkeeping* to *has an equation of motion*, and this is the first construction here in which the
carrier's structure responds to its content at all.

**AND IT ANSWERS W-41's DICHOTOMY.** *Either the carrier grows, or records are evicted.* **On a
carrier that can pay for growth, it grows** — by `0.84` of a plaquette for one bit of content.
Eviction was the fixed-carrier answer, not the only one.

---

## W-50 — **THE FOUR MARKERS ARE FORCED BY COUNTING. W-45 IS WEAKER THAN IT WAS REPORTED.**

`LANE_W50_NECESSITY/`, sealed. Proof obligation **C**: showing records *can* form this way is not
showing this is *how* they form. The gravity identification rests on capacity satisfying four
functional markers, so strip the structure that produced them.

**Two carriers, same records, same cycle rank, same physical dimension `16`, differing only in
whether record boundaries share links:**

```
                        CONNECTED (3x3 patch)      DISCONNECTED (4 separate squares)
  link multiplicity     [1, 2]  SHARED             [1]  DISJOINT
  capacity              3                          3
  F1 universal          PASS  consumption [1]      PASS  consumption [1, 3]
  F2 no screening       PASS  0 of 1152            PASS  0 of 792
  F3 one sign           PASS                       PASS
  F4 arena              PASS  k=4 impossible       PASS  k=4 impossible
  W-41 eviction         [0,0,0,1] -> 3 kept, 1 out [0,0,0,1] -> 3 kept, 1 out
```

> **ALL FOUR MARKERS SURVIVE INTACT WHEN THE SHARING IS REMOVED, AND SO DOES THE EVICTION PROFILE,
> EXACTLY. The gravity-like character does not depend on the carrier's structure at all.**

### THE CORRECTION, AND IT IS TO THE REGISTRAR'S OWN HEADLINE

**W-45 reported "capacity passes all four of gravity's functional markers" as though it were a
substantive structural finding. It is not.** All four follow from one fact: *independent records
live in a finite-dimensional space and each uses one dimension.*

- **F1** every record consumes — because every independent record uses a dimension
- **F2** no screening — forced by linearity
- **F3** one sign — adding constraints can only shrink a kernel
- **F4** arena — capacity is finite

> **THAT IS LINEAR ALGEBRA, NOT PHYSICS. ANY FINITE RESOURCE PASSES ALL FOUR.** Disk space passes
> all four. **The markers are necessary and nearly vacuous.**

**WHAT REAL CONTENT SURVIVES.** The contrast with EM's charge, which fails all four, is genuine — a
**resource** and a **two-signed conserved charge** are different kinds of object, and gravity is
resource-like where charge is not. **But that is far more modest than "capacity has gravity's
functional signature," and the registrar presented the stronger claim.**

**AND IT NAMES WHAT THE MARKERS CANNOT SEE.** Attraction. The equivalence principle. A field
equation. Any relation between content and a metric. **We have none of these, and the four markers
were never capable of detecting their absence.**

**ONE STRUCTURAL DIFFERENCE DID SHOW.** Consumption values are `[1]` connected and `[1, 3]`
disconnected — a record spanning several components blocks more links. So the carrier's structure is
visible in *how much* is consumed, though not in *whether* the markers pass.

### WHAT THIS DOES TO PROOF OBLIGATION C

**Partially answered, in the deflating direction.** The gravity-like structure is **necessary in the
sense of unavoidable** — no carrier with `m` independent records can lack it. **But its necessity is
trivial: it follows from counting rather than from anything about the carrier, the field, or the
process.** So it does not establish that anything gravity-like is *required for records* in a way
that carries physical content. **Item 14 must be read at this reduced strength.**

---

## MAP ERRATUM — **STEP 3 IMPORTED THE CLASSICAL FOOTPRINT AGAIN**

`MAP_TO_THE_RELATION_V001.md` step 3, as first written, read *"our capacity story is repulsive,
gravity is attractive"* and proposed that finding no attraction would be a **standing objection** to
the gravity identification.

> **THAT MAKES CLASSICAL ATTRACTION THE STANDARD THE RECORD SURFACE MUST MEET.** It is the same
> import the principal has now flagged **three times** — classical-shaped nulls read two ways
> (before W-44), *"an early embryo doesn't look like a human"* (before W-45), and again now.
> **The registrar has made this error at W-44, at W-45's framing, and here.**

**CORRECTED.** The functional content of attraction is **positive feedback**: content makes more
content more likely in the same place. The step now asks that, with all three outcomes read in
advance and **none of them treated as a test gravity must pass**:

- **positive feedback** — content concentrates
- **negative feedback** — already measured (W-39 crowding, W-41 eviction); **NOT a refutation**,
  since crowding may be the record-level form of something that only becomes attraction after
  accumulation
- **neither** — the strongest of the three, since it would mean the resource has no dynamics at all

**Steps 1, 2 and 4 were checked for the same defect.** Step 1 (reconstruct adjacency from records)
and Step 2 (alpha as resolution limit) carry no classical gravitational shape. **Step 4 does head
toward classical geometry, and that is correct** — convergence to classical geometry at large scale
is the expected emergent endpoint, which is a different thing from demanding classical form at the
record level, and it is last in the order for that reason.

---

## W-52 — **SPATIAL STRUCTURE IN RECORD FORMATION IS REAL, CREATED BY ALPHA, AND ITS SIGN OSCILLATES**

`LANE_W52_FEEDBACK/`, sealed. Map step 3 in its corrected form: not *do records attract* (the
classical import) but **does a record make another more likely nearby**.

Records `p0` and `p1` share one link; `p0` and `p3` share none. Bath `[4,9]` is the set of links
avoided by all three, so every comparison runs under the same bath.

```
   g^2    d(neighbour)         d(far)            difference        sigma
  0.00  0.03629 +-0.00305  0.03584 +-0.00313   +0.00045 +-0.00437    0.1
  0.02  0.03072 +-0.00382  0.04565 +-0.00330   -0.01493 +-0.00504    3.0
  0.05  0.09756 +-0.00429  0.05370 +-0.00492   +0.04386 +-0.00653    6.7
  0.10  0.07516 +-0.00522  0.16637 +-0.00591   -0.09121 +-0.00788   11.6
  0.20  0.01712 +-0.00309  0.06358 +-0.00365   -0.04645 +-0.00478    9.7
```

**TWO THINGS ARE ESTABLISHED AND ONE IS REFUSED.**

**ESTABLISHED — the spatial structure is real and it is ALPHA that creates it.** At `g² = 0` the
difference is `0.1 sigma`: **exactly indifferent, as the mechanism requires.** The mechanism was
stated before the run and holds: plaquette operators commute, `||[H(g²=0), W_p1]|| = 0.000e+00`, so
at zero coupling the records are independent degrees of freedom and **no spatial structure is
possible**. Switch the electric term on and `||[H(0.05), W_p1]|| = 0.980` — **it is the only channel
that couples plaquettes, and neighbouring plaquettes couple through the link they share.**

**ESTABLISHED — the effect is large.** Up to `11.6 sigma`, six independent seeds.

**REFUSED — that it is FEEDBACK in either direction. THE SIGN OSCILLATES WITH THE COUPLING:**
negative at `0.02`, positive at `0.05`, negative again at `0.10` and `0.20`.

> **THE REGISTRAR RAN `g² = 0.05` ALONE FIRST AND WOULD HAVE REGISTERED "POSITIVE, SPATIALLY
> STRUCTURED FEEDBACK". It is one point of a sign-oscillating quantity.** The likely cause is the
> same class as two earlier defects in this program: a **fixed sampling time** (`T = 15`) reading a
> coherently precessing quantity — cf. W-32's fixed-`T` survival and W-47's max-over-time.

**AND THE PRE-REGISTERED OUTCOME LIST WAS INCOMPLETE.** The map named three readings in advance —
positive, negative, indifferent. **The measurement returned a fourth: oscillating.** Pre-registering
outcomes is the right discipline and it did not save the reading; **only the sweep did.**

**WHAT IT LEAVES.** Records are **not** indifferent to one another — that possibility is dead at
`11.6 sigma`. **What couples them is alpha, through shared links, and nothing else.** Whether the
coupling concentrates or disperses content is **not answered**, and cannot be until the measurement
is made at something other than a fixed time.

---

## PHASE A — **THREE OF THE FOUR NECESSITY RESULTS ARE NOW THEOREMS, NOT MEASUREMENTS**

`THEOREMS_V001.md` + `LANE_PA_THEOREMS/`, sealed. The program had **measured** four results that are
provable. Measuring a theorem on one lattice is strictly weaker than proving it.

**T1 — durability ⟹ unwritable. PROVED, AND STRONGER THAN WHAT WAS MEASURED.** For any GKSL
generator with **arbitrary** jump operators and `R` **normal**: `[H,R]=0` and `[L_k,R]=0` give
`d⟨R⟩/dt = 0` for every state. **No lattice, no gauge group, no dimension, and no unitarity of the
jumps enters** — the program had only ever measured the unitary-jump case. Verified at the edges
with random operators and exact simultaneous diagonalisation: `≤ 1.2e-15` across `D = 4…12`, with
each hypothesis breaking it when dropped. **And normality is nearly free: if `H` is Hermitian with
non-degenerate spectrum and `[H,R]=0`, then `R` is automatically normal.**

**T2 — reading requires a closed path. PROVED.** An open path's holonomy transforms as
`W → g_a W g_b⁻¹` and admits no gauge-invariant function of the link variables alone; a closed one
transforms by conjugation. **W-37's cut-ring `0.000000` is an instance of the theorem, not evidence
for it.**

**T3 — `capacity = m − 1`. PROVED FOR ARBITRARY COMPLEXES.** `bd` is linear over `GF(2)`, so
protectability via a link `ℓ` is the kernel of ONE linear functional. Verified on the `3×3` patch,
disconnected squares, a **tetrahedron**, a **cube surface**, and six random complexes — **10 of 10**,
with the orphan-link hypothesis confirmed as the one doing the work. **Planarity, dimension, lattice
structure and gauge group play no role.**

**T4 — `legibility = perimeter/2 − 1`. NOT PROVED, and it is the one Phase C depends on.** The
mechanism is clear (only a region's boundary layer pairs with anything outside) but the coefficient
is underived and the class of regions unestablished.

> **WHAT PHASE A BUYS: three of the program's four necessity results are no longer statements about
> a `Z_2` lattice.** T1 in particular is a general fact about open quantum systems. **What it does
> not buy: the carrier is still imported, and T4 — the one with any prospect of a distinguishing
> prediction — is still a measurement on rectangular planar blocks.**

---

## PHASE A / T4 — **W-46's `2n−1` IS WITHDRAWN. THE BULK/BOUNDARY SPLIT SURVIVES AND IS STRONGER.**

Reducing the pairing shows legibility is the **GF(2) rank of the outside–inside plaquette
adjacency**, whose kernel is exactly the region-combinations whose boundary is interior to `A`.

```
    n   |A|=n²   legibility   invisible   (n−2)²
    2       4            4           0        0
    3       9            8           1        1
    4      16           12           4        4
    5      25           16           9        9
```

**`invisible = (n−2)²` exactly — the plaquettes touching no outside plaquette. `legibility = 4(n−1)`.**

**W-46 REPORTED `2n−1 = perimeter/2 − 1`. WITHDRAWN. Its region sat at the lattice CORNER**, so part
of `A`'s boundary faced the lattice edge instead of outside plaquettes. Re-running that geometry
reproduces `3, 5, 7`; the same regions placed in the interior give `4, 8, 12`.

> **THE CONCLUSION IS UNCHANGED AND BETTER FOUNDED: storage scales with AREA, legibility with
> PERIMETER — and the mechanism is now exact. What a region cannot export is precisely its interior.**

**T4 REMAINS OPEN AS A CLOSED FORM.** `legibility = boundary-touching count` is exact for rectangles
and **false in general**: the `plus` pentomino has all five cells touching the outside and legibility
`4`; `3×3`-minus-centre has all eight touching and legibility `8`. The kernel characterisation is
general; the formula is not.

**PHASE A CLOSES AT THREE THEOREMS AND ONE CHARACTERISATION.** T1 (any GKSL generator, arbitrary
jumps, `R` normal), T2 (gauge theory), T3 (arbitrary complexes) are proved. T4 has an exact
mechanism and a shape-dependent coefficient.

---

## PHASE B — **UNIVERSALITY: T1 AND T2 ARE GENERAL. T3 IS ABELIAN-SPECIFIC BY PROOF.**

`LANE_PB_UNIVERSALITY/`, sealed.

**B1 — T1 needs no Markov approximation at all.** Modelling system **and** environment explicitly and
unitarily: if `R` acts on the system, `[H_sys,R]=0` and `[H_int, R⊗I]=0`, then `R⊗I` commutes with the
full `H_tot`, since `H_env` acts on the other factor. **`⟨R⟩` is then exactly conserved with no weak
coupling, no memorylessness and no bath spectral assumption.** Verified with an explicit **finite**
environment (so it recurs and has memory) at strong coupling `3.0`: drift `≤ 6.6e-13` over `t = 0…40`
at `D_S×D_E` up to `5×8`; each hypothesis dropped breaks it. **GKSL was never required — T1 is a
conservation statement.**

**B2/B3 — T3 is field- and dimension-independent.** `capacity = m−1` verified over **GF(2), GF(3),
GF(5)** on plaquette and triangle complexes, and in **three dimensions** with regions as cubes and
boundaries as faces (`2×1×1`, `2×2×1`, `2×2×2`). The proof used only linearity of the boundary map
over a field, and neither the characteristic nor the dimension appears.

**WHERE T3 STOPS, ASSESSED NOT TESTED.** It needs an **abelian** group: a non-abelian holonomy depends
on ordering and base point, so "the product of the plaquettes" is not a linear function of the region
and the kernel argument fails. **Untested and open.** **T2 is group-independent** — its proof
(`W → g_a W g_b⁻¹`) holds for any `G`.

---

## PHASE C — **NO DISTINGUISHING PREDICTION. THE SURVIVING CANDIDATE IS LOCALITY.**

`LANE_PC_PREDICTION/`, sealed. W-48 had already killed the decoherence half of the composed law by
showing the un-optimised signal is `exp(−ΓT)`. **The one surviving candidate was the
storage/legibility split.** The plan's obligation was to establish it predicts something the existing
account does not, **before** touching data.

**The deflation to rule out: an operator supported strictly inside a region commutes with everything
outside it. That is microcausality.** So: is legibility exactly the number of independent records
whose support touches the region's boundary?

```
   shape              |A|   legibility   locality bound   differ?
   square 3x3           9            8                8
   square 4x4          16           12               12
   rect 3x4            12           10               10
   plus pentomino       5            4                4
   3x3 minus centre     8            8                8
   ... 13 shapes tested, differences observed: [0]
```

> **LEGIBILITY IS THE LOCALITY BOUND IN EVERY CASE. THE STORAGE/LEGIBILITY SPLIT IS MICROCAUSALITY
> EXPRESSED IN GAUGE-THEORETIC LANGUAGE.** It predicts nothing the existing account lacks, and it is
> **not** taken to data.

### WHAT THIS MEANS FOR THE PROGRAM, STATED WITHOUT SOFTENING

**Phase D is not reachable.** It was contingent on C producing a prediction that could fail, and C
produced none.

**Every component of the account now reduces to known physics.** The decoherence half is `exp(−ΓT)`
(W-48). The capacity half is locality (C1). Single-run versus ensemble is unravelling-dependence,
standard. W-49's carrier response is Boltzmann. W-52's spatial structure is the electric term coupling
plaquettes that share a link.

> **THE PROGRAM HAS PRODUCED A CORRECT, INTERNALLY VERIFIED, THEOREM-BACKED ACCOUNT OF RECORD
> FORMATION IN LATTICE GAUGE THEORY THAT IS ENTIRELY COMPOSED OF KNOWN PHYSICS. There is no novel
> prediction in it.** That is the ending `PLAN_TO_PROOF_V001.md` named in advance as possible, and it
> is the one that occurred.

**AND THE REASON IS STRUCTURAL, NOT ACCIDENTAL.** The only slot that was ever empty is **gravity**,
and three independent routes to it failed — dynamical topology (refuted 3/3), a classical metric
(three builds, bought nothing), and the functional identification (forced by counting). **An account
built from EM and a coupling alone can only reproduce what EM and a coupling already explain.**

---

## PHASE C ERRATUM — **C1 TESTED LEGIBILITY, NOT CAPACITY. THE VERDICT WAS OVERSTATED.**

The Phase C entry wrote *"the capacity half is locality (C1)"*. **C1 tested no such thing.** It tested
**LEGIBILITY** — how many of a region's records are distinguishable from outside — and found it equals
the locality bound in 13 of 13 shapes. **That is a result about what ESCAPES a region, not about how
many records it can HOLD.** The two are separate claims and the registrar collapsed them.

**WHAT IS ACTUALLY ESTABLISHED, ITEM BY ITEM:**

| claim | status | by |
|---|---|---|
| legibility (what escapes) reduces to locality | **established** | C1, 13 shapes |
| capacity's four gravity-like markers are forced by counting | **established** | W-50 |
| the carrier's response to content is Boltzmann | **established** | W-49 |
| **capacity + boundary formation are not gravity's record-level form** | **NOT ESTABLISHED** | — |

**The last line was never tested and the Phase C verdict implied it.**

### THE PRINCIPAL'S FRAMING, AND WHAT WOULD ACTUALLY TEST IT

> *"we don't expect gravity to appear at the record level looking the same as classical gravity. It
> will likely have other features such as capacity and boundary formation."*

Everything this program has ruled out was ruled out **at a single scale**: one region, one carrier,
one bath placement. **The four markers being forced by counting says they carry no information ABOUT
THE CARRIER. It does not say a large collection of capacity constraints carries no information.**

**THE UNTESTED ROUTE IS ACCUMULATION** — and it is the paper's own Appendix C step 3, the large-record
limit, which this program has never attempted. W-39/41/42 are step 2 (compatibility across
overlapping regions) with numbers in them. **Step 3 asks whether a sufficiently rich collection of
capacity and boundary constraints determines something that is not present in any one of them.**

**Why this is not special pleading.** Every deflation so far — `exp(−ΓT)`, locality, Boltzmann,
counting — is a statement about ONE constraint. **Emergence claims are claims about MANY, and none of
the tests run so far could have detected one.** That is a real gap in the coverage, not a rescue.

**IT IS ALSO FALSIFIABLE.** If a large collection of capacity/boundary constraints determines nothing
beyond what each determines separately, accumulation adds nothing and the negative verdict stands at
every scale. **That is a decidable question and it has not been asked.**

---

## W-51 — **GEOMETRY IS NOT IN THE RECORDS. IT IS IN THE ENVIRONMENT COUPLING.**

`LANE_W51_RECORD_TO_GEOMETRY/`. Map step 1: can the carrier's geometry be reconstructed from records
alone. Three independent methods, expectation withheld, three adversaries. **All three reported
fidelity `1.000` on the true carrier against `~0.5` shuffled. The headline is nonetheless withdrawn.**

### THE RECONSTRUCTION IS AN EXACT IDENTITY, SO NOTHING COULD HAVE FAILED

At `g² = 0` the Hamiltonian is a sum of records and commutes with all of them, so
`Γ(S) = 2γ·|bdy(S)|` exactly. Boundaries are GF(2)-additive, hence
`|bdy(p⊕q)| = |bdy(p)| + |bdy(q)| − 2|bdy(p)∩bdy(q)|`, so **the pair excess IS the shared-link count
by polarisation** — and "shares a link" is by definition that intersection being non-empty. **Two
lines of set algebra, no dynamics.**

**VERIFIED BY EXECUTION, NOT ARGUMENT.** A reconstructor with **no Hamiltonian, no Lindbladian and no
time evolution — just set XOR** — reproduces the lane exactly: block and ring exact, and across 200
count-preserving shuffles it matched **each shuffle's own truth 200/200**, scoring mean `0.5057`
against the original. **Those are the lane's published numbers.**

> **THE MANDATED SHUFFLE CONTROL HAS NO DISCRIMINATING POWER.** A physics-free reconstructor passes it
> with an identical signature. One adversary scored 60 shuffles with and without dynamics:
> `max|difference| = 0.0e+00`.

**Build 1 (spectral) is circular outright** — its input contains the full incidence matrix
(`rank(B) = L`, so `A` follows from one least-squares solve; recovered at `2e-15` by two adversaries
working independently, recovering *which* links, not just how many).

### THE RESULT THAT SURVIVES IS A NULL, AND IT IS THE STRONGEST CLAIM IN THE LANE

> **ADJACENCY IS NOT IN THE RECORD ALGEBRA.** Every record is a product of link operators, all
> commutators are `0.00e+00`, and the multiplication table is `(Z_2)^m` — **identical on block, chain
> and ring, which have three different dual graphs.**
>
> **Geometry enters only through `Z_k` — the electric term and the bath coupling.**

**TWO NON-VACUOUS SURVIVORS.** The **isolation test**: swap the stored incidence for BLOCK while the
operators are RING and fidelity is `1.000` vs RING, `0.667` vs BLOCK, and the mirror image on
reversal — **the answer follows the dynamics and ignores the stored structure entirely.** And the
**`γ` sweep**: fidelity `1.0000` at `γ = 0.5, 0.1, 0.01, 1e-4`, collapsing to `0.5333` at `γ = 0`.

> **REMOVE THE ENVIRONMENT AND NOTHING COMES BACK. THE RECORD SECTOR ON ITS OWN IS GEOMETRY-BLIND.**

### MAP STEP 2 — ALPHA DOES NOT SET THE RESOLUTION

`g²` sets the **validity window of the rate estimator**, not a resolution. It is **not monotone in
`g²` and not monotone in `g²·t*`**: `(g²=1.0, t*=0.2)` fails completely while `(g²=0.5, t*=1.0)` — a
larger product — is exact. Breakdown coincides with the measured coherent leakage rate rising to the
size of the dissipative rates. **The predicted coincidence with the legibility bound does not occur.**

### WHAT THIS DOES TO THE MAP

**Steps 1 and 2 are answered, both negatively.** Geometry is not recoverable from records in any
inferential sense, and the coupling is not a resolution limit. **The three-way relation the map was
built to obtain does not exist by this route.**

**AND IT SHARPENS THE PRINCIPAL'S FRAMING RATHER THAN CONTRADICTING IT.** If boundary formation is
part of gravity's record-level character, **W-51 locates it on the ENVIRONMENT side, not the record
side.** The records carry no geometry at all; what carries it is where the environment couples —
which is also what W-38 measured when the environment's placement selected which region was a region.
**Two independent lanes now say the same thing: geometry lives in the coupling, not in the content.**

---

## W-53 — **THE MIRROR TEST IS VOID, AND THE ASYMMETRY IT EXPOSES IS THE REAL POINT**

`LANE_W53_MIRROR/`, sealed. **Forced-or-not check run BEFORE any dynamics**, on W-51's lesson that a
reconstruction can succeed perfectly and mean nothing.

**VOID.** For a single-link bath `{ℓ}` the protected set is `{S : ℓ ∉ bd(S)} = ker f_ℓ`, and the
family `{ker f_ℓ}` determines every row of the boundary map. Confirmed in code on four carriers:
**the incidence matrix is recovered exactly, by pure set algebra, with no dynamics and no link
labels.** The mirror test is W-51's identity in different clothing. **No dynamics was built.**

### THE ASYMMETRY, WHICH IS NOT VOID

```
  RECORD ALGEBRA (W-51)      identical on block, chain and ring -> GEOMETRY-BLIND
  PROTECTED-SET FAMILY       distinct on all 4 carriers, 6 of 6 pairs -> GEOMETRY-FULL
```

**The same carriers that the record algebra cannot tell apart, the environment-coupling structure
separates completely.** That is W-51's finding stated at its sharpest: **the records carry no
geometry; the coupling carries all of it.**

### WHAT THIS SETTLES ABOUT THE PRINCIPAL'S FRAMING

> *"capacity + boundary formation may well be the signature of gravity at the record level"*

**The first half is where geometry actually lives, and that is now established twice.** But in this
carrier the coupling's geometry is **installed by the registrar**, so what W-38 measured was
**selection among given regions, not formation of them.** Boundary *formation* — the set of possible
boundaries being an output rather than an input — **cannot be tested on a carrier whose incidence is
an input to every quantity we can compute.**

> **EVERY RECONSTRUCTION QUESTION IS CIRCULAR ON THIS CARRIER. That is a structural fact about the
> construction, not a result about records or gravity.**

**So the framing is not refuted and is not testable here.** Testing it needs a carrier in which
adjacency is not given — which is the emergent-geometry problem proper, and is beyond this
construction. **That is the honest boundary of what this program can reach.**

---

## W-54 — **ACCUMULATION ADDS NOTHING. CAPACITY IS ENTIRELY LOCAL.**

`LANE_W54_ACCUMULATION/`, sealed. Road item 20 — the last route this program could decide on its own.
Every prior deflation was obtained at a single scale, so none could have detected a collective effect.

**MADE WELL-POSED FIRST.** On a fixed finite carrier every quantity is an exact function of the
incidence matrix, so emergence in the strong sense cannot arise — that needs a limit. The sharpest
version that **can** fail: **global capacity is `m−1`; how much of it is reachable using only records
supported inside a single part of a partition, and how much requires records that span parts and
belong to none?**

**PREDICTION, STATED IN ADVANCE: deficit `= k−1`, independent of partition shape.**

```
   partition                m    k   global   local-only   deficit   predicted
   9 singletons             9    9        8            8         0          8
   3 rows                   9    3        8            8         0          2
   3 columns                9    3        8            8         0          2
   uneven 5+3+1             9    3        8            8         0          2
   6 singletons             6    6        5            5         0          5
   3 vertical pairs         6    3        5            5         0          2
```

> **THE PREDICTION IS WRONG AND THE RESULT IS A CLEAN NEGATIVE. DEFICIT IS ZERO FOR EVERY PARTITION,
> INCLUDING SINGLETONS.** The full capacity is achievable with **single-plaquette records** — the most
> local objects the carrier has. **No part of a carrier's capacity is collective.**

**Why the prediction was wrong:** the parts are not independent carriers but subsets of one, and
single-plaquette records are already local to singletons. Their independent rank is `m`, and those
avoiding a link on exactly one plaquette give `m−1` directly.

### WHAT THIS CLOSES

**Item 20 is closed, negatively. Accumulation adds nothing on this carrier, and it was the last
question the program could decide by itself.**

Combined with what is already sealed: the decoherence half is `exp(−ΓT)` (W-48); legibility is
locality (C1); the capacity markers are counting (W-50); the carrier's response is Boltzmann (W-49);
geometry is not in the records and every reconstruction question here is circular (W-51, W-53); and
now **capacity has no collective content either.**

> **THE PROGRAM'S HONEST END STATE: a complete, internally verified, three-theorem account of record
> formation in lattice gauge theory, every component of which reduces to known physics, containing no
> distinguishing prediction and no collective content.**

**WHAT REMAINS IS NOT DECIDABLE HERE.** Item 24 — boundary *formation*, the set of possible
boundaries being an output rather than an input — requires a carrier whose adjacency is not installed.
**That is the emergent-geometry problem proper, and no experiment on this construction can reach it.**

---

## W-55 — **ITEM 24: BOUNDARIES ARE NOT DERIVABLE FROM GENERIC DYNAMICS. THEY MUST BE AN INPUT.**

`LANE_W55_FACTORIZATION/`, sealed. Item 24 in its sharpest form: in a bare Hilbert space with no
installed structure, a "boundary" is a **tensor factorisation**. So — can one be an output of the
dynamics rather than an input?

**W-55's optimiser search is VOID and is retained as such.** It plateaued near `0.94` whatever it was
given: at `eps=0` the planted Hamiltonian is exactly local (`1.0000`) and the search reached only
`0.9461`, while at `eps=0.40` it reported `0.936` — **above** the planted truth of `0.875`. The
optimiser, not the physics, set the number.

### THE EXACT QUESTION NEEDS NO OPTIMISER

`H` is exactly local under **some** factorisation iff its spectrum is a **SUMSET** `{a_i + b_j}` —
conjugation preserves the spectrum, so this is a property of the eigenvalues alone.

> **AND IT IS SETTLED BY DIMENSION COUNTING, RIGOROUSLY.** A `d_A × d_B` sumset has `d_A + d_B − 1`
> free parameters while the spectrum has `d_A·d_B` entries. For `4×4`: **7 parameters describing 16
> numbers.** The sumset spectra form a 7-dimensional subvariety of `R^16` — **measure zero. A generic
> Hamiltonian admits NO factorisation making it local.**

```
   planted sumsets           2.3e-16, 7.0e-16, 2.3e-02*     (*one optimiser failure, logged)
   generic random Hermitian  4.4e-02, 4.9e-02, 5.2e-02, 4.6e-02   never near zero, 60 restarts each
   OUR 3x3 patch, H_magnetic 7.7e-17                        EXACTLY a sumset
```

### THE NUMBER THAT ANSWERS ITEM 24

> **OUR OWN CARRIER'S HAMILTONIAN IS EXACTLY A SUMSET — `7.7e-17`. A factorisation exists for it.**
>
> **And it exists because we BUILT it that way:** `H_mag = −Σ_p (W_p + h.c.)` is a sum of **commuting**
> plaquette terms, so its spectrum is a sum of independent contributions by construction.

**THAT IS WHERE THE BOUNDARIES CAME FROM.** Not from the dynamics — from the registrar's choice of a
Hamiltonian assembled out of commuting local pieces. **The moment that choice was made, the set of
boundaries was fixed, and every lane afterwards was reading back an input.**

### ITEM 24, CLOSED

**Boundaries are an output only for Hamiltonians that already carry the structure. For generic
dynamics they are not derivable at all, and must be supplied.** This is a statement about dynamics,
not about our lattice — it is why W-53 found every reconstruction question circular, and it would
have been circular on any carrier built the same way.

**HONEST LIMIT.** One planted control failed at `2.3e-02`, the same order as the generic values, so
the numerics alone separate planted from generic by only ~2×. **The rigorous content is the dimension
count, not the optimisation;** the numbers illustrate it and do not carry it.

---

## SURFACE ASSUMPTION AUDIT — **TWO IMPORTED ASSUMPTIONS. ONE MEASURED TO FAIL, ONE NEVER EXAMINED.**

`SURFACE_ASSUMPTION_AUDIT_V001.md`, sealed. The principal asked whether an imported assumption is the
root cause of not finding a process. **The audit had never been done.** Eight assumptions in the
five-step process, classified.

**A1 — THE HILBERT SPACE FACTORISES. IMPORTED AFTER BEING MEASURED TO FAIL.** The register already
carries it as **IMP-2**: a gauge theory's gauge-invariant algebra does not factorise across a region
boundary. **W-37d broke on this directly.** Yet every Holevo quantity, every partial trace and every
"reduced environment state" in this program presupposes it. **And Gap 2 is the same assumption seen
from the other side** — W-55 asked where factorisations come from and answered: from the modeller.

**A2 — A BACKGROUND TIME PARAMETER. IMPORTED, LOAD-BEARING EVERYWHERE, NEVER EXAMINED ONCE.**
**125 of 125 lanes evolve in `t`. Zero derive it.** A project-wide search for relational or emergent
time returns nothing.

> **GRAVITY IS THE DYNAMICS OF SPACE-TIME STRUCTURE. WITH `t` A FIXED EXTERNAL PARAMETER THERE IS
> NOWHERE FOR GRAVITY TO ACT — AND NONE OF THE THREE FAILED ROUTES TOUCHED IT.** W-31 varied the
> graph; W-44 added lengths, potentials and a clock **read against `t`**; W-45/W-50 varied nothing
> dynamical. **All three left `t` alone.**

**And it matches the paper's own statement of where gravity enters — metric/PROPER-TIME action. We
have no proper time.** One global parameter shared by every part of the carrier, which is precisely
the structure general relativity does not have. **W-44's clock is the sharpest evidence: a clock that
reads the background parameter cannot register a proper-time difference, because there is only one.**

**A8 (Markovian bath) is CLEARED** — Phase B/B1 showed T1 needs no Markov assumption.

**STATUS.** That A2 is imported and unexamined is **established**. That removing it would produce a
process is a **hypothesis, not a result** — and it is falsifiable in the useful direction: build a
carrier with no background time, where evolution is relational, and see whether anything
gravity-shaped has somewhere to act. **If it still does not, A2 was not the obstruction.**

---

## SURFACE AUDIT / A1 — **THE TENSOR PRODUCT WAS THE WRONG FRAMEWORK, AND GAP 2 MAY BE AN ARTIFACT OF IT**

The principal: *"Why would you assume this at the record level?"* — of the step *"to say anything about
a system being monitored by its environment, you first have to cut that space into parts."*

**The tensor product is a POSTULATE ABOUT COMPOSITE SYSTEMS.** It says: given two things, each with a
state space, the pair gets `H_A ⊗ H_B`. **It presupposes that the parts already exist.** Importing it
where parts are the thing to be derived assumes the answer.

### THE FRAMEWORK THAT DOES NOT PRESUPPOSE PARTS

**Algebraic quantum theory.** A subsystem is a **SUBALGEBRA** of observables; its environment is the
**COMMUTANT**. No factorisation is required, and relative entropy is defined for these objects
without one.

> **AND IN THAT FRAMEWORK A REGION'S ALGEBRA IS NOT A FREE CHOICE. It is determined by the field
> content and the constraint: the gauge-invariant operators supported there. THE GAUSS LAW FIXES
> THEM.**

**THIS PROGRAM ALREADY BUILT THAT AND THEN WALKED AWAY FROM IT.** The physical sector was constructed
**from the constraint** — that is algebraic. Then the registrar laid tensor products on top to compute
partial traces, Holevo quantities and redundancy, **while the register carried IMP-2 stating the
algebra does not factorise.**

### WHAT THIS DOES TO GAP 2

> **"Gap 2: supplied, not derived" MAY BE AN ARTIFACT OF THE CHOSEN FRAMEWORK RATHER THAN A FACT
> ABOUT RECORDS.**

**W-55 asked which TENSOR FACTORISATION makes `H` local and answered: none, generically.** It never
asked **which SUBALGEBRAS the constraint singles out.** Those are different questions, and only the
second is the one a gauge theory actually poses.

### WHAT IT COSTS

**Every redundancy result obtained through a partial trace — W-36, W-40, W-43b — was computed in a
framework the system does not have.** The numbers stand as computed; **their interpretation assumed a
split that is not there.** W-37d/W-37e already hit this from the other side and the fix was to abandon
partial traces for classical mutual information — **that fix was applied locally and never propagated.**

**RE-POSED GAP 2:** *given the constraint algebra, is the decomposition into region subalgebras
determined?* **Untested. It is a different question from W-55's and it is the one this carrier can
actually be asked.**

---

## W-56 — **GIVEN A REGION, ITS BOUNDARY DATA IS DERIVED. THE ALGEBRAIC FRAMEWORK NEEDS NO FACTORISATION.**

`LANE_W56_SUBALGEBRA/`, sealed. Road item 25, in the framework that does not presuppose parts.
**NO PARTIAL TRACE IS TAKEN ANYWHERE IN THIS LANE.**

The physical space is `2^4` and every operator in play is a Pauli string on the four effective
qubits, so the question is exact `GF(2)` linear algebra: a plaquette shift is `X_p`; an electric `Z`
on link `ℓ` is the product of `Z_i` over the cycles containing `ℓ`. For a link set `S`, `A(S)` is
generated by `{Z_ℓ : ℓ ∈ S}` and `{W_p : p entirely inside S}`, and its **CENTRE** is
`V ∩ V^⊥` under the symplectic form — **determined by `A(S)` alone, chosen by no one.**

```
   region              inside      dim A(S)   centre generators   |centre|
   one plaquette p0    [0]              4     Z1, Z2                    4
   two adjacent p0,p1  [0,1]            6     Z3, Z2                    4
   two diagonal p0,p3  [0,3]            6     Z1, Z2                    4
   three p0,p1,p2      [0,1,2]          7     Z3                        2
   all four            [0,1,2,3]        8     (identity only)           1
```

> **IN EVERY CASE THE CENTRE IS GENERATED BY THE ELECTRIC CHARGES OF THE CYCLES OUTSIDE THE REGION,
> AND NOTHING ELSE.** Checked explicitly: the centre lives only on the outside cycles for every
> region tested. **It shrinks monotonically as the region grows — `2, 2, 2, 1, 0` generators — and the
> whole algebra is a FACTOR, with trivial centre.**

**This is the Casini–Huerta–Rosabal / Donnelly–Wall structure computed on this program's own carrier
rather than cited.** The registrar's earlier guesses were wrong in both directions: the **magnetic
loop is never central**, and the naive "electric flux summed over boundary links" is central only for
some regions. **The centre was reported rather than guessed, and it is the complement's data.**

### WHAT THIS DOES TO GAP 2 — IT NARROWS IT, IT DOES NOT CLOSE IT

**DERIVED, and this is genuine:** the framework needs **no tensor factorisation at all**; a subsystem
is a subalgebra and its environment the commutant. **Given a region, its boundary data — the centre —
follows from the algebra with nothing chosen.** W-55's negative result was about *tensor
factorisations*, and it does not apply here.

**STILL SUPPLIED:** which links constitute the region. Gap 2 moves from *"which of a continuous family
of factorisations"* to *"which set of links"* — **a far weaker choice, and in a field theory naming a
region of space is a natural act rather than an arbitrary one. But it is still an input.**

**AND THE COST STANDS.** W-36, W-40 and W-43b computed redundancy through partial traces, which this
lane shows are unnecessary and which IMP-2 says are unavailable. **Their numbers were obtained in a
structure the system does not have; the algebraic versions have not been computed.**

---

## W-57 — **REDUNDANCY WITHOUT PARTIAL TRACES: THE RECORD HAS NO PARTIAL LEGIBILITY AT ALL**

`LANE_W57_ALGEBRAIC_REDUNDANCY/`, sealed. Paying the debt from W-56: W-36, W-40 and W-43b computed
"what a fragment knows" through **partial traces**, which presuppose a factorisation IMP-2 says the
system does not have.

**THE ALGEBRAIC QUANTITY NEEDS NO FACTORISATION.** For a subalgebra `A`,
`d_A = max_{a ∈ A, ||a||≤1} |Tr(a ρ_+) − Tr(a ρ_−)| = ||P_A(ρ_+ − ρ_−)||_1`, with `P_A` the
Hilbert-Schmidt conditional expectation. **Only the algebra enters — no factor, no trace-out, no
environment Hilbert space.**

```
   region S                    |S|   dim A      d_A
   one cut link                  1       2   0.000000
   all four cut links            4       8   0.000000
   one perimeter link            1       2   0.000000
   half the perimeter            4      16   0.000000
   PERIMETER MINUS ONE LINK      7      16   0.000000
   the whole perimeter           8      32   1.000000
   everything                   12     256   1.000000
```

> **AN EXACT STEP FUNCTION. Every proper sub-region resolves the record's sectors at `0.000000` —
> INCLUDING seven of the eight perimeter links — and the whole loop resolves them at `1.000000`.
> THERE IS NO PARTIAL LEGIBILITY.**

**This differs from W-36's graded curve** (`0.044, 0.100, 0.187, 0.351, 0.658, 0.929`), and the two
are asking different questions: W-36 measured how much an explicit environment had *learned* through
a coupling; W-57 measures what a region's own algebra *can resolve at all*. **The algebraic answer is
exact where the other was approximate.**

**HONEST LIMIT ON THE STRENGTH.** The sectors are defined by `R` and the states are maximally mixed
within each, so **only `R` itself distinguishes them** — and `R ∈ A(S)` iff its support lies in `S`.
**For this state the result is close to tautological**, and it is the algebraic form of T2 rather than
a new fact. **Its real content is the EXACTNESS: a topological record admits no partial legibility,
not even at 7 links of 8.** With a state carrying correlations, other operators could contribute; that
is untested.

**THE FIRST VERSION FAILED ITS OWN CONTROL** and the definition it exposed is worth keeping: `A(S)`
must be generated by the electric operators on `S` **and by every gauge-invariant Wilson loop whose
SUPPORT lies inside `S`** — not merely by the whole plaquettes inside `S`. Under the narrower
definition `A(PERIM)` does not contain the rim loop at all.

---

## W-58 — **RELATIONAL TIME: THE CONSTRUCTION IS BUILDABLE, THE TEST OF A2 IS NOT SETTLED**

`LANE_W58_RELATIONAL_TIME/`, sealed. Surface audit **A2**: 125 of 125 lanes evolve in an external
parameter and zero derive it. **This is the first lane with no background time anywhere** — a
constraint `H_tot|Ψ⟩ = 0`, time as a correlation between a clock and the rest.

**WHAT IS ESTABLISHED.** The construction works: the constraint is satisfied to `2.7e-16`, and
conditioning on the clock reproduces unitary evolution to `2.6e-15` **from a stationary state with no
external time**. So relational time is realisable on this program's machinery.

**WHAT IS NOT ESTABLISHED, AND THE LANE SAYS SO.** The gravity-relevant case is a **clock whose rate
depends on what is there** — an interaction inside the constraint, making time non-universal. Every
`λ > 0` run is **VOID**: the kernel collapses to dimension 1 and the conditional state is **static**
(`largest variation 0.000`), so there is no history to condition on.

**THREE GATES WERE NEEDED AND THE FIRST TWO WERE WRONG.** The sign (`H_C` generates `+t`, so the
history satisfies `H_C − H_S`); the spectrum (negative `H_S` against non-negative `H_C` leaves only
`n=0`, a static eigenstate). **And the third gate still does not discriminate: participation over
clock readings is `12 of 12` for a single energy eigenstate too, because `|⟨t_k|n⟩|² = 1/d` uniformly
by Fourier duality.** The correct gate is whether the conditional **state** varies with `k`.

> **HONEST STATUS OF A2: UNRESOLVED, WITH A NAMED CAUSE.** A history state needs the clock and system
> spectra to match across many levels, and a generic interaction destroys that matching in finite
> dimensions — the kernel drops from `4` to `1`. **Whether that is a real obstruction or an artifact
> of a `12 × 4` toy is exactly what this construction is too small to say.**

**A2 THEREFORE REMAINS THE ONE UNEXAMINED SURFACE ASSUMPTION.** It has now been *approached* rather
than tested: the timeless framework is buildable, and the state-dependent-rate case — the only one
where gravity could enter — needs a carrier large enough to keep a history alive under interaction.

---

## W-59 — **THE OBSTRUCTIONS COHERE. SIX REDUCE TO FOUR, AND THREE OF THE FOUR ARE NOT DYNAMICAL.**

`LANE_W59_OBSTRUCTION_STRUCTURE/`, sealed. The principal: *"maybe these failures are a feature."*
Every obstruction has the form **"X and Y cannot both be had"** — the shape physics takes when the
content is real. If they are content rather than six accidents they should **cohere**. Decidable, so
decided.

**REDUCTION (a) — W-57 FOLLOWS FROM T2.** Across every subset size `|S| = 0…12`, resolution is an
**exact indicator** of "contains the loop's support", with **zero partial values anywhere**. A
gauge-invariant record is a closed loop (T2); the sectors are distinguished only by it; so a region
resolves them iff it holds the whole loop. **W-57 is T2 plus the state choice, not an independent
obstruction.**

**REDUCTION (b) — W-55 AND W-58 ARE ONE FACT.**

```
   lambda   constraint kernel dim   sumset residual of H_tot
     0.00                       4                  3.022e-16
     0.05                       1                  5.204e-02
     0.15                       1                  4.568e-02
     0.40                       1                  4.297e-02
```

**The kernel collapse and the sumset failure occur together and discontinuously, at the same
coupling.** W-55's "no factorisation" and W-58's "no global history" are both
**SPECTRAL COINCIDENCE IS NON-GENERIC.** One fact, met twice.

### THE STRUCTURE THAT REMAINS

```
   1  T1   a conserved quantity is conserved              DYNAMICAL -- and near-tautological
   2  T2   gauge invariance forces closed loops           KINEMATIC      => implies W-57
   3  T3   capacity = m - 1                               COMBINATORIAL  => implies eviction
   4       spectral coincidence is non-generic            MEASURE-THEORETIC => W-55 and W-58
```

> **SIX OBSTRUCTIONS REDUCE TO FOUR, AND THREE OF THE FOUR ARE NOT DYNAMICAL AT ALL.** Only T1 is,
> and it is close to a tautology about superselection.

**THE HONEST READING, WHICH IS NEITHER THE DEFLATION NOR THE ELEVATION.** The obstructions **do**
cohere — the principal's suspicion is confirmed — but **what they cohere into is structure, not
dynamics.** Record formation in this account is fixed almost entirely by gauge kinematics, counting,
and genericity. **And that is why gravity never entered: gravity would have to be dynamical, and
there is almost no dynamical content in the picture at all.**

**THE ONE SUBSTANTIVE MEMBER IS THE FOURTH.** *The structures records need — a factorisation, a global
history — are NON-GENERIC.* They exist only for special Hamiltonians: sums of commuting local terms,
spectra that match across many levels. **So "a world that has records" is a statement that its
Hamiltonian is special, and the content of the whole account is in WHICH way it is special.** That is
a sharper question than any this program has yet asked, and nothing here answers it.

---

## W-60 — **WHICH HAMILTONIANS ADMIT RECORDS: EXACTLY THE DEGENERATE ONES. AND THAT MEANS EXACT SYMMETRY.**

`LANE_W60_WHICH_HAMILTONIANS/`, sealed. W-59 left the one substantive obstruction — the structures
records need are non-generic — and the content is in **which** way a Hamiltonian must be special.

**THE CRITERION, DERIVED FROM T1 RATHER THAN GUESSED.** A record needs `[H,R] = 0` and must be
non-trivial — not merely a function of the energy, or it carries nothing beyond which level the
system is in. If every eigenvalue of `H` is simple, everything commuting with `H` **is** a function
of `H`. Therefore:

> **A RECORD EXISTS ⟺ THE COMMUTANT OF `H` IS NON-ABELIAN ⟺ `H` HAS A DEGENERATE EIGENVALUE.**

```
                                   multiplicities        dim comm  (predicted)   records beyond f(H)
  GENERIC random Hermitian      [1,1,1,1,1,1,1,1]           8      (8)                    0
  planted [2,2,2,2]                     [2,2,2,2]          16     (16)                   12
  planted [4,4]                             [4,4]          32     (32)                   30
  our 3x3 patch, H_magnetic           [1,4,6,4,1]          70     (70)                   65
  our patch + 0.05 * H_electric  [1,1,2,1,1,3,1,...]        26     (26)                   14
```

**`dim commutant = Σ (multiplicity)²` exactly in every case.**

**RECORDS ARE NON-GENERIC, AND THE REASON IS SPECTRAL: `0 of 400` random Hermitian matrices had ANY
degenerate eigenvalue.**

### THE SYMMETRY LINK, AND IT IS BRUTAL

By Wigner, spectral degeneracy in a physical Hamiltonian comes from **symmetry**. Break it:

```
     eps        multiplicities        dim commutant   records beyond f(H)
   0e+00              [2,2,2,2]                  16                   12
   1e-06      [1,1,1,1,1,1,1,1]                   8                    0
   1e-03      [1,1,1,1,1,1,1,1]                   8                    0
```

> **A SYMMETRY-BREAKING PERTURBATION OF `1e-06` DESTROYS EVERY RECORD. Not gradually — immediately.**

**SO RECORDS REQUIRE EXACT SYMMETRY, NOT APPROXIMATE SYMMETRY.** An approximate symmetry gives
*none*. This is why real records exist at all: the symmetries that carry them — gauge invariance,
particle identity — are **exact**, and exact symmetries are not spoiled by small perturbations. **It
is also why this program's carrier has records: its gauge symmetry is exact.**

### AND A NEW, SHARP ROLE FOR ALPHA

**The electric term breaks the degeneracy.** `H_magnetic` alone carries **65** records; adding *any*
electric term drops it to **14** — and `g² = 0.05` and `g² = 0.5` give the identical `26`-dimensional
commutant. **The reduction is immediate, not gradual.**

> **ALPHA'S ROLE, RESTATED: it is what breaks the degeneracy that records live in. At `g² = 0` the
> carrier holds 65; at any `g² > 0` it holds 14.** That is consistent with every earlier lane — the
> exact records survive only at `g² = 0` — and it says why in one line.

**WHAT THIS ANSWERS AND WHAT IT DOES NOT.** It answers W-59's question: the special Hamiltonians are
the degenerate ones, degeneracy means symmetry, and it must be exact. **It does not say why the
world's Hamiltonian has the exact symmetries it has** — which is now the only question left standing
in this program, and is not one the carrier can be asked.

---

## W-61 — **THE SPACE EMITS THE DEGENERACY. THE PRINCIPAL'S HYPOTHESIS IS CONFIRMED.**

`LANE_W61_TOPOLOGICAL/`, sealed. W-60 left a fatal fragility: records need exact degeneracy, and
SYMMETRY-induced degeneracy dies at `1e-06`. The principal: *"maybe gravity at the record level emits
symmetry."* There is a kind of degeneracy that behaves exactly that way, and W-60 supplies the
contrast that makes the test decisive.

**Same theory, same perturbation, two topologies.**

```
  TORUS 2x2 (genus 1)   unperturbed degeneracy 4
        eps       ground splitting     splitting / gap
    0.0e+00              2.665e-15           6.661e-16
    1.0e-06              4.867e-13           1.217e-13
    1.0e-03              1.282e-06           3.208e-07
    1.0e-01              5.925e-03           1.593e-03

  DISK 3x3 (genus 0)    unperturbed degeneracy 1 -- no splitting possible (control)

  SYMMETRY degeneracy (W-60), same perturbation sizes
    eps = 1e-06   ground splitting  2.003e-06     <- LINEAR in the perturbation
    eps = 1e-03   ground splitting  2.002e-03     <- LINEAR
```

> **AT `eps = 1e-06`: SYMMETRY DEGENERACY SPLITS BY `2.0e-06` — LINEARLY, THE SAME ORDER AS THE
> PERTURBATION. TOPOLOGICAL DEGENERACY SPLITS BY `4.9e-13` — FOUR MILLION TIMES SMALLER.**

**The degeneracy records need does NOT have to be supplied by a symmetry. It can be EMITTED BY THE
TOPOLOGY OF THE SPACE**, and when it is, it is protected in a way symmetry-induced degeneracy is not:
the splitting is suppressed to high order because only a perturbation that WRAPS the space can lift
it. **The disk shows the same theory with no such degeneracy at all — the difference is genus, not
dynamics.**

### WHAT THIS DOES TO THE PROGRAM

**W-60's fragility is resolved and its conclusion is corrected.** *"Records require exact symmetry"*
was too narrow. **Records require exact degeneracy, and TOPOLOGY supplies it more robustly than
symmetry does.**

**AND THIS IS THE FIRST PLACE GRAVITY ENTERS THIS PROGRAM NON-TRIVIALLY AND IN ITS OWN SHAPE.** Not a
metric (W-44: bought nothing), not dynamical topology as a variable (W-31: refuted 3/3), not a
functional resource analogy (W-50: forced by counting). **Here the GENUS OF THE SPACE — a purely
geometric fact, with no symmetry imposed and no metric anywhere — determines whether records can
exist at all, and how well they survive.**

**The principal predicted this shape three times before it appeared:** gravity at the record level
will look different while performing the same function. **The function is supplying the exact
degeneracy records live in. The form is topology, not force, not metric, not curvature.**

**AND IT MEETS HARLOW–OOGURI FROM THE OTHER SIDE.** Quantum gravity forbids exact *global* symmetries,
so a gravitating world cannot use symmetry to protect its records. **Topological degeneracy needs no
symmetry — which is precisely what such a world has left.**

---

## W-62 — **RECORD CREATION. ALL THREE TERMS IN ONE OPERATION, AND THE OLDEST OBSTRUCTION IS RESOLVED.**

`LANE_W62_CREATION/`, sealed. **The logical operators are COMPUTED from the structure, not nominated**
— magnetic ones are cycles that are not boundaries; electric ones are link sets with even overlap
with every plaquette that are not vertex stars. Both by `GF(2)` linear algebra. (The first attempt
guessed them and got `||[W,H]|| = 22.6`.)

```
  TORUS 2x2, physical dim 32, ground-space degeneracy 4, gap 4.0000

  1  the computed logicals commute with H       ||[M,H]|| = 0.00e+00   ||[Z,H]|| = 0.00e+00
  2  and ANTICOMMUTE on the ground space        ||{M,Z}|| = 1.26e-15   ||[M,Z]|| = 4.00
     the record label Z has eigenvalues         [-1, -1, +1, +1]
  3  CONTROL: a CONTRACTIBLE loop does not write            ||[C,Z]|| = 3.01e-17
  4  CONTROL: no LOCAL operator writes          worst single-link Z commutator = 1.59e-16
  5  DISK 3x3: NON-CONTRACTIBLE cycles = 0      same theory, NO record
```

### THE OLDEST OBSTRUCTION IS RESOLVED

W-29/W-30 established that **writable and durable are conjugate** — and it stood for the whole
program. **It was a search for a LOCAL writer for a record only a NON-LOCAL operation can set.**

> **THE RECORD `Z` IS UNTOUCHED BY EVERY LOCAL OPERATOR (`1.6e-16`) AND BY EVERY CONTRACTIBLE LOOP
> (`3.0e-17`), AND IS WRITTEN BY THE NON-CONTRACTIBLE TRANSPORT `M`, WHICH ANTICOMMUTES WITH IT
> (`4.00`). WRITABLE AND DURABLE AT THE SAME TIME.**

T1's no-go applies to operations **commuting** with the record. Transport around a non-contractible
cycle does not commute with it — **and is not local, so noise cannot mimic it.**

### THE THREE TERMS, IN ONE OPERATION

**EM** supplies the gauge field and the holonomy that **is** the record — `Z` on a computed
even-overlap set, with clean `±1` labels on the ground space.

**GRAVITY** supplies the possibility of the operation at all. **On the torus there are non-contractible
cycles; on the disk there are ZERO.** Same theory, same Hamiltonian, same everything — **genus 0 has
no record and no way to write one.** The genus is the difference.

**ALPHA** is what costs the record:

```
     g^2    ground degeneracy    record labels     |{M,Z}|
  0.0000                    4    [-1,-1,+1,+1]    1.26e-15
  0.0001                    3    [-1,+1,+1]       6.02e-08
  0.0100                    1    [+1]             3.94e-23
  0.5000                    1    [+1]             9.97e-32
```

**At `g² = 0` the record has a 4-fold home, clean labels, and a working writer. By `g² = 0.01` the
degeneracy is gone, the label collapses to a single value, and the writer no longer acts.**

> **EM CARRIES THE RECORD. THE GENUS MAKES IT WRITABLE AND PROTECTS IT. ALPHA DESTROYS IT.**
> That is the three-way combination the charter asked for, in one operation, with each role measured
> and each control firing.

---

## W-63 / PROOF_V001 — **THE RESULTS ARE DERIVED, AND THE DERIVATION PREDICTS NUMBERS IT WAS NOT FITTED TO**

`LANE_W63_DERIVATION/` + `PROOF_V001.md`, sealed. Four theorems with proofs, then checked against
what the lanes already measured.

**A — record space dimension `= |H_1| = 2^{2g}`.** Ground states are constant on `B_1`-cosets in
`Z_1`. Derived `4` for the `2×2` and `2×3` tori; **measured `4`.** Disk: `H_1 = 0` ⟹ dimension `1`,
no record; measured **zero** non-contractible cycles.

**B — logicals are `H_1` and `H^1`, and a writer always exists.** `Z(c)M(z) = (−1)^{⟨c,z⟩}M(z)Z(c)`,
and by **Poincaré duality the intersection pairing is non-degenerate**, so every record has an
anticommuting partner. Measured `‖{M,Z}‖ = 1.26e-15`, `‖[M,Z]‖ = 4.00`.

**C — nothing supported on a contractible region acts.** Measured `1.59e-16` and `3.01e-17`.

**D — splitting is `O(ε^d)`, `d` the minimal non-contractible cycle. THE PREDICTION THAT COULD HAVE
FAILED.** Derived `d = 2`; **measured slope `2.000, 2.000, 2.000, 2.000` across two decades**, and
`ε² = 1e-12` against W-61's `4.9e-13`. Symmetry degeneracy has `d = 1` and measured linear.

> **THE THREE ROLES, PROVED: EM supplies the field and the holonomy that IS the record. GENUS supplies
> the record space (A), the writer (B iii), and the protection (C, D). ALPHA is a sum of local terms
> and therefore splits the record space at order `d` and destroys it (D).**

**AND IT RESOLVES W-29/W-30 WITH A PROOF RATHER THAN A WORKAROUND.** Writable and durable are
conjugate **for local operations** — Theorems C and D. B(iii) supplies a **non-local** writer, and C
shows noise cannot mimic it.

**ATTRIBUTION, STATED IN THE PROOF ITSELF.** Theorems A–D **are Kitaev's toric code** and are not
this program's discovery. **What is this program's is the chain making them necessary:** W-60 (a
record exists iff `H` is degenerate) and W-61 (symmetry-sourced degeneracy dies at `1e-06`,
topology-sourced survives by `4×10⁶`), which together force the degeneracy to be topological.

---

## P1 — **THE DEFINITION, AND IT IS NOW THE PROGRAM'S ANCHOR**

`LANE_P1_DEFINITION/` + `CORE_FRAMEWORK_V001.md`, sealed. The program had used "record" in at least
three senses. **One definition, five clauses, and the content is carried by the definition so the
theorems come out clean.**

`R` is a **record** for `(H,{L_k})` if it is **(i)** a bit, **(ii)** durable (`[H,R]=0`, `[L_k,R]=0`),
**(iii)** non-trivial — *not constant on some eigenspace of `H`*, i.e. it distinguishes states of the
**same energy** — **(iv)** writable by some admissible operation, and **(v)** protected: **no**
contractible operation writes it.

**IT DISCRIMINATES.** Toric-code record: **all five pass** (`4.899` non-triviality, `11.314`
protection). Break the degeneracy with a local perturbation: **(iii) collapses to `0.000`.** Take `R`
a function of `H`: **(iii) and (iv) both fail.**

**THREE PROPOSITIONS FALL OUT IMMEDIATELY.** (iii) ⟹ `H` is degenerate — **P2's forward direction is
now one line.** (ii)+(iv) ⟹ the writer is built from neither `H` nor the jumps. **(iv)+(v) ⟹ THE
WRITER IS NON-LOCAL — so W-29/W-30's obstruction is a consequence of the definition rather than an
accident of our carrier.**

**AND THE FRAMEWORK NOW CARRIES THE OBSTRUCTION LIST.** Five solvable (O1 the converse — the one that
decides theorem vs conjecture; O2 the symmetry half; O3 exhaustiveness, to be side-stepped rather
than solved; O4 defining "admissible"; O5 an approximate version of (ii)) and four out of reach and
named as such (lattice-not-spacetime topology; no response to matter; the outcome problem; zero
empirical contact). **Order of attack: O4 → O3 → O2 → O1 → O5.**

---

## ERRATUM — **"TOPOLOGY, NOT SYMMETRY" WAS THE WRONG DICHOTOMY. IT IS A HIGHER-FORM SYMMETRY.**

The principal asked two questions: *why do we assume symmetry?* and *with the number of twins at the
record level, do we have a form of symmetry that goes by another name?* **Both land, and the second
renames the result.**

**ON THE ASSUMPTION.** Statement 2 presupposed symmetry as the candidate source of degeneracy —
standard Wigner lore. **The lore holds one way only.** *Symmetry ⟹ degeneracy* is a theorem;
*degeneracy ⟹ symmetry* is not. **W-61 is a counterexample this program produced itself**, and the
registrar imported the converse anyway.

**ON THE NAME — CONFIRMED IN THE LITERATURE.** Topological order **is** the spontaneous breaking of a
**1-FORM SYMMETRY**. In the toric code the Wilson and 't Hooft loops are **exact 1-form symmetries**,
both commute with `H`, and **the ground states transform non-trivially under the operators on
non-contractible loops — which IS the robust degeneracy.**

> **THE RECORD IS THE ORDER PARAMETER OF A SPONTANEOUSLY BROKEN 1-FORM SYMMETRY.**

### WHAT THIS CORRECTS AND WHAT IT IMPROVES

| was | now |
|---|---|
| statement 2: *symmetry cannot supply the degeneracy* | **ORDINARY (0-form) symmetry cannot** |
| statement 3: *topology can* | **a 1-form symmetry can — and topology is what supplies one** |
| statement 4: *records require genus* | **records require a HIGHER-FORM symmetry; on a manifold that means non-trivial topology** |

**AND IT EXPLAINS THE ROBUSTNESS INSTEAD OF ONLY MEASURING IT.** A 0-form symmetry is generated by
operators acting at points, so a local perturbation couples to it directly and splits the multiplet at
first order. **A 1-form symmetry is generated by EXTENDED (loop) operators, which no local operator
can reach — a perturbation must act along an entire loop.** That is precisely Theorems C and D, and
it is now a *symmetry* statement rather than a topological accident.

**THIS IS A BETTER RESULT, NOT A RETREAT.** "Records require topology" becomes **"records require a
symmetry whose generators are extended"** — which says *why* the protection exists.

### AND IT CREATES A TENSION THAT MUST BE FACED

Harlow–Ooguri forbids **exact global symmetries** in quantum gravity, and the modern statement
**includes higher-form global symmetries**. If records require a 1-form symmetry, and gravity forbids
exact global ones, records would be impossible — which is absurd.

**RESOLUTION, AND IT SHARPENS THE CLAIM.** In the toric code the 1-form symmetry is **EMERGENT** — a
symmetry of the low-energy theory, not an exact microscopic global symmetry. **Emergent symmetries
are not what Harlow–Ooguri forbids.** So:

> **RECORDS REQUIRE AN EMERGENT HIGHER-FORM SYMMETRY.** Exact microscopic symmetry is forbidden by
> gravity and is fatally fragile in any case (W-61); an emergent 1-form symmetry is neither.

**STATUS: this is a re-reading of results already sealed, not a new measurement.** Every number stands
— `slope 2.000`, `4.9e-13` against `2.0e-06`, `2^{2g}`. **What changes is what they are called and why
they hold.** The emergence claim (that the 1-form symmetry here is emergent rather than exact
microscopic) is **asserted from the literature and not yet verified on this carrier.**

---

## O6 — **THE 1-FORM SYMMETRY IS EXACT IN OUR CARRIER, NOT EMERGENT. THE HARLOW–OOGURI TENSION IS LIVE.**

`LANE_O6_EMERGENCE/`, sealed. The emergence claim was asserted from the literature and carries the
whole gravity connection, so it was tested. **It failed.**

```
  1-FORM (toric code, generic local gauge-invariant perturbation)
      eps        ||[W, H+epsV]||   slope      ground splitting   slope
    1.0e-04            0.000e+00                    1.613e-08
    1.0e-03            0.000e+00     --             1.613e-06   2.000
    1.0e-02            0.000e+00     --             1.613e-04   2.000

  0-FORM CONTROL
    1.0e-04            8.517e-04                    1.598e-04
    1.0e-03            8.517e-03   1.000            1.598e-03   1.000
    1.0e-02            8.517e-02   1.000            1.593e-02   0.998
```

**THE CONTROL FIRES CORRECTLY:** a 0-form symmetry is broken at slope `1.000` and its degeneracy
splits at slope `1.000` — **no gap**, exactly as an exact-but-fragile symmetry should behave.

> **BUT THE 1-FORM SYMMETRY IS NOT BROKEN AT ALL: `0.000e+00` AT EVERY PERTURBATION STRENGTH.** It is
> **EXACT**, not emergent — while its degeneracy still splits at order `2`.

**WHY, AND IT IS NOT AN ACCIDENT.** In the gauge-invariant sector the only available local operators
are the electric `Z_k` and the plaquettes. **Both commute with the Wilson-loop generator.** A
single-link shift would not, but it is not gauge-invariant and does not act on the physical space.
**Gauge invariance itself forbids every operator that could break the 1-form symmetry.**

### WHAT THIS DOES TO THE CLAIM

**The proposed resolution of the Harlow–Ooguri tension is withdrawn.** It rested on the 1-form
symmetry being emergent. **In this carrier it is exact — and it is exact precisely because we imposed
gauge invariance.** That is the same "we installed it" defect as A1 and A2.

> **THE TENSION IS LIVE, NOT RESOLVED.** Records require a 1-form symmetry (statements 1–4). Quantum
> gravity forbids exact global symmetries **of every form**. Our carrier supplies an **exact** one.
> **Something must give, and this construction cannot say what.**

**THE THREE LIVE POSSIBILITIES, none decidable here.** (a) The 1-form symmetry of a *gauge* theory is
not "global" in the Harlow–Ooguri sense — the likeliest resolution, and a question about their result
rather than ours. (b) It must be **emergent** in any real realization, which needs the gauge structure
itself to emerge from a non-gauge microscopic model — **not our carrier, where gauge invariance is an
input.** (c) The requirement is weaker than statements 1–4 assert.

**O6 IS NOT CLOSED. It is upgraded from "asserted" to "tested and failed", and the gravity connection
now rests on an open question rather than a citation.**

---

## G1 — **THE RECORD COUNT IS SET BY GENUS, NOT AREA. `capacity = area − 1` NEVER COUNTED RECORDS.**

`LANE_G1_RECORD_COUNT/`, sealed. Two capacity numbers were in the register with different scalings —
`T3: area − 1` (linear in area) and `Thm A: 2^{2g}` (exponential in genus). **Only one can be counting
records under the five-clause definition.** Counted properly: on the **ground space**, and **modulo
vertex stars**, since two link sets differing by a star act identically there.

```
   carrier              area   ground degeneracy   INDEPENDENT records (dim H¹)   T3's area−1
   torus 2x2 (g=1)         4                   4                            2              3
   torus 2x3 (g=1)         6                   4                            2              5
```

> **THE RECORD COUNT IS `2` ON BOTH — IT DOES NOT MOVE WHEN THE AREA GOES FROM 4 TO 6. It equals
> `2g`, exactly as Theorem A predicts, giving a record space of `2^{2g} = 4`.**

**AND T3's OBJECTS DO NOT SURVIVE AS RECORDS.** Of `7` and `31` plaquette-boundary loops, exactly
**1** is independent modulo stars in each case — against T3's counts of `3` and `5`.

> **`capacity = area − 1` IS STILL TRUE AS A STATEMENT ABOUT WHICH PLAQUETTE SUBSETS ARE
> SIMULTANEOUSLY PROTECTABLE FROM A BATH. IT IS NOT A RECORD COUNT.** Those objects fail the
> definition: they act trivially on the ground space, so they are not records under clause (iii).

### WHAT THIS SETTLES ABOUT GRAVITY'S ROLE

**The number of records a world can hold is a TOPOLOGICAL invariant.** It is `2g`. **It does not
depend on the area, the volume, the lattice spacing, the number of degrees of freedom, or any local
geometric quantity.** Double the area and nothing changes; change the genus and everything does.

> **AND THIS IS EXACTLY THE PRINCIPAL'S POINT THAT GRAVITY AT THE RECORD LEVEL LOOKS NOTHING LIKE
> CLASSICAL GRAVITY.** Classical gravity is local, metric, and curvature-driven. **What sets the
> record count here is a GLOBAL, NON-METRIC, TOPOLOGICAL property, and no local measurement can see
> it.** Same function — determining what geometry permits — in a form with no classical resemblance
> whatever.

**TWO MEASUREMENT DEFECTS, BOTH THE SAME CLASS AND BOTH LOGGED.** The first pass checked protection on
the **full Hilbert space**, where a short string maps out of the ground space and so cannot flip
anything — making clause (v) vacuously true for every candidate. The second counted rank in the
**link space** rather than in the quotient `Z¹/B¹`, giving `5` and `7` instead of `2`. **Both are
"counted in the wrong space"; the record lives on the ground space, modulo stars, and nowhere else.**

---

## G2 — **GRAVITY DEFINED, AND AN EXACT BRIDGE TO CURVATURE**

`LANE_G2_GRAVITY_DEF/` + `GRAVITY_DEFINED_V001.md`, sealed.

**DEFINITION: gravity at the record level is `( H₁(Σ), ⟨·,·⟩ )`** — the first homology of the carrier
and its intersection form. The count, the space, the writer and the protection all come from that
pair and nothing else. **No metric, no curvature tensor, no force, no local content.**

**AND THE BRIDGE, WHICH HAD NOT BEEN STATED.** For a closed orientable surface `dim H₁ = 2 − χ`, and
Gauss–Bonnet gives `∫K dA = 2πχ`, so

> **number of independent records `= 2 − (1/2π) ∫ K dA`**

```
   torus (chi=0)         2 − chi = 2      measured degeneracy 4 = 2^2
   sphere (chi=2)        2 − chi = 0      measured degeneracy 1 = 2^0
   disk (boundary)       formula N/A      measured degeneracy 1  (H_1 = 0)
```

> **THE RECORD COUNT IS TOPOLOGICAL, NON-LOCAL AND NON-METRIC — AND IT EQUALS AN INTEGRAL OF THE
> GAUSSIAN CURVATURE.** That is how a count no local measurement can see and the classical
> gravitational quantity turn out to be the same fact.

**FIVE FEATURES OF THE EMERGENCE PICTURE:** the count is an integrated curvature (exact); the
protection order `d` is a **length**; it is global and non-metric; it is a spontaneously broken 1-form
symmetry; and **a simply-connected world has no records at all** — the sphere gives degeneracy `1`.

> **THE SHARPEST STATEMENT THE PROGRAM HAS PRODUCED: a world whose space is a sphere cannot remember
> anything. Not remembers poorly — cannot hold one record.**

**AND THE HONEST LIMIT.** **Content does not change `χ`.** In classical gravity matter curves space;
here nothing records do alters the topology. **We have the half of gravity that says what geometry
permits, and not the half that says how content shapes geometry. Until X2 closes, this is a
correspondence and not an emergence.**

---

## X2 — **χ IS A PARAMETER, NOT AN OBSERVABLE. AND UNDER ALLOW/REQUIRE THAT IS NOT A DEFECT.**

`LANE_X2_BACKREACTION/`, sealed.

**THE STRUCTURAL FACT.** `χ = V − E + F` is a property of the **cell complex**. The Hilbert space is
**built from** that complex. Every operator — unitary, dissipative, any — is a map on that space.
**So `χ` has no eigenvalues, no expectation value and no equation of motion.** Verified: the torus
`2×2` and the cube surface have the **same Hilbert dimension (32)** and different `χ` (`0` vs `2`);
the torus `2×2` and `2×3` differ in **size** but share `χ` — **and share the degeneracy (4)**. The
record count follows `χ` and nothing else, and **nothing inside the theory varies `χ`.**

> **X2 IS NOT A MISSING MEASUREMENT. In any framework with a fixed complex, content CANNOT shape
> geometry, because geometry is not the sort of thing the theory contains.**

### THE PRINCIPAL'S CORRECTION — ALLOW / REQUIRE

The registrar wrote: *"we have the half of gravity that says what geometry permits, and not the half
that says how content shapes geometry — so this is a correspondence, not an emergence."*

**The principal: isn't this the allow/require distinction?** — and it is, and the registrar had it
backwards.

> **"MATTER CURVES SPACE" IS THE CLASSICAL FORM OF GRAVITY. Demanding it AT THE RECORD LEVEL is the
> same import flagged four times before.** At the record level there is no metric to curve. **What
> gravity does there is ALLOW: it says what can exist.** And that is not half a job — **it is the
> whole job at that level.**

**AND X2's RESULT IS EVIDENCE FOR THIS, NOT AGAINST IT.** `χ` is not an observable *at this level*.
Requiring it to respond to content is requiring a level-inappropriate quantity to have dynamics.
**ALLOW is the record-level face of gravity; REQUIRE is its macroscopic face.** Asking for both at
once is a category error — the embryo again.

**THE STATEMENT, CORRECTED:**

> **At the record level gravity ALLOWS. `records = 2 − (1/2π)∫K dA` says exactly what may exist, and
> a sphere permits nothing. That is complete as a record-level statement.** Whether allow becomes
> require at larger scales is a **separate question at a separate level**, and it is the paper's own
> Appendix C step 3.

**AND IT KEEPS A FALSIFIER, so this is not a way of never owing backreaction.** If accumulated
allow-statements never yield anything require-like at any scale, then allow is all there is and the
identification with gravity weakens accordingly. **That is decidable, later, and not here.**

**STATUS CHANGE: X2 moves from "out of reach — the gravity claim is only a correspondence" to
"category error — allow is the record-level face; require belongs to a level this construction does
not reach."**

---

## X2 ERRATUM — **ALLOW IS POTENTIAL AT EVERY LEVEL. THERE IS NO ALLOW→REQUIRE TRANSITION.**

The principal: *"allow is always potential. Why would we expect that to be different at the collective
records level?"*

**The registrar had just written that ALLOW is gravity's record-level face and REQUIRE its macroscopic
face. That is wrong, and the correction is structural.**

> **EINSTEIN'S FIELD EQUATIONS ARE CONSTRAINTS.** In the Hamiltonian formulation they are literally
> that — the Hamiltonian and momentum constraints, `H ≈ 0`, conditions on admissible initial data.
> They do not say what happens; they say which `(geometry, matter)` pairs are **permitted**.
> **"Matter curves space" was never a REQUIRE. It is an ALLOW written in differential form.**

**SO THE CORRECTION IS DOUBLE.** There is no level at which allow becomes require, because require
does not exist at any level. **And the falsifier the registrar attached to X2 — "if accumulated allow
never yields require, the identification weakens" — CAN NEVER FIRE, and is therefore worthless.** It
is withdrawn.

### THE QUESTION THAT REPLACES IT, AND IT IS SHARPER

If gravity is **allow** at every level, the live question is no longer *when does allow become
require* but:

> **IS OUR RECORD-LEVEL ALLOW THE SAME CONSTRAINT AS THE GRAVITATIONAL ONE, SEEN AT A DIFFERENT
> SCALE — OR TWO UNRELATED CONSTRAINTS THAT HAPPEN BOTH TO BE PERMISSIVE?**

**And there is a real structural parallel to test, not merely assert.** Both are **Gauss laws** in the
Dirac sense: conditions on data generated by the theory's own gauge symmetry, with the physical
content appearing as a **boundary term**.

| | our record level | classical gravity |
|---|---|---|
| the constraint | Gauss law at each vertex, `∂s = 0` | Hamiltonian + momentum constraints, `H ≈ 0` |
| generated by | the gauge symmetry | diffeomorphisms |
| physical content is a | **boundary term** — the record is a boundary holonomy | **boundary term** — ADM energy is a surface integral, *because of* the constraint |
| permits | `records = 2 − (1/2π)∫K dA` | which `(g, T)` pairs may exist |

**THE NEW FALSIFIER, and unlike the old one it can fire.** If the record-level constraint and the
gravitational constraint have **different structure** — different generators, or physical content that
is *not* a boundary term on one side — then they are two unrelated permissive statements and the
identification is a coincidence of form. **That is checkable.**

**STATUS: X2's reclassification stands (χ is a parameter, not an observable, and demanding backreaction
imports the classical form). What is withdrawn is the allow→require story layered on top of it, and
the unfalsifiable test that came with it.**

---

## THE IMPORT RULE — **A RESCUE IS ALWAYS DOWNSTREAM OF AN IMPORT**

The principal: *"We won't have to rescue measures if we avoid importing classical gravity measures
into the record level."*

The registrar had responded to the level-migration failure by building a **rescue-detector** into
lane X-6. That treats the symptom. **The rescue was only ever needed because an import was there to
be rescued.** Remove the import and the guard is unnecessary.

### THE IMPORT WAS IN X-6'S OWN FALSIFIER, AND THE REGISTRAR WROTE IT

> *"Different generators, or physical content that is not a boundary term on one side, kills the
> identification."*

This makes **classical gravity's constraint algebra the criterion for whether our object is real.**
A mismatch would read as OUR defect. That is a classical measure applied to the record level as a
test. **It is the same error as demanding backreaction (X-2) and as expecting require (X2 erratum),
in its third costume.**

### THE VECTOR IS THE NAME

**Calling `H₁(Σ)` "gravity" is what lets classical properties in.** Every time the name is used, the
classical field's attributes arrive with it and have to be individually refused — backreaction, an
equation of motion, a require-half, a matching constraint algebra. Each refusal has cost a lane.

**The charter asks for the ROLE of gravity in record formation. It does not ask that classical
gravity be present.** A role-assignment is not a claim of identity, and no property of the classical
field transfers through the name.

### THE RULE, STANDING

> **NO CLASSICAL MEASURE MAY BE APPLIED TO THE RECORD LEVEL AS A CRITERION.**
> A classical quantity may be **computed** and **reported as a relationship**. It may never be the
> **test our object must pass.**
> **TELL:** any falsifier of the form *"our object fails to exhibit ⟨classical feature⟩"* is an
> import and is **void**. A falsifier must be stated in the record level's own terms.

**AND THE OBJECTION THIS RAISES, ANSWERED.** If nothing can falsify "our constraint is gravity's",
that identification is unfalsifiable — the sin corrected hours ago. **The resolution is that the
identification is not claimed.** A claim not made needs no falsifier. What is claimed is the role,
and the role has its own falsifiers already registered (a record on a genus-0 carrier; a local
writer).

### EFFECT ON LANE X-6

- **The COMPUTE half stands.** Measuring our own constraint algebra — commutators, closure,
  structure constants vs functions, the boundary operator, `Z₁/B₁` — imports nothing. It is our
  object described in its own terms, and it is the actual work.
- **The IDENTIFICATION half is WITHDRAWN as an import.** "Is it the same constraint as gravity's"
  is not a charter question.
- What gravity's algebra is remains worth **knowing** and will be recorded as a **relationship**,
  carrying no verdict on our object.
- **The rescue-detector is retired as a permanent fixture.** It was scaffolding for an import.

**CLARIFICATION, same day.** The principal: *"I don't have a problem with using the term 'gravity' as
long as we don't use it as an excuse to import a variety of classical metrics that aren't
applicable."* **The word is restored as a permitted label.** The registrar had over-corrected by
purging it; the purge was never the point. **What survives, and is the whole of the gain: Γ is
defined by R1–R3 and by nothing else, no attribute transfers through the name (D-1, D-2), the
identification with `H₁` is a CANDIDATE and not a definition (G-1 withdrawn → G-5), and uniqueness
is now askable (G-6).** Say "gravity"; never let it do work.

---

## G-7 — **THE CAPACITY LAW IS AN INDEX.** `2 − χ` WAS THE WRONG FORMULA, AND THE DISK SHOWED IT

`LANE_G7_INDEX/g7_index.py` · ranks computed over GF(2) by explicit Gaussian elimination; `∂₁∂₂ = 0`
asserted on every carrier.

> ### `N = dim H₀ + dim H₂ − χ`   —   **holds on all five carriers**
> ### `N = 2 − χ`   —   **FAILS on the disk**

| carrier | V | E | F | χ | H₀ | **H₁** | H₂ | `H₀+H₂−χ` | `2−χ` |
|---|---|---|---|---|---|---|---|---|---|
| torus 2×2 | 4 | 8 | 4 | 0 | 1 | **2** | 1 | **2** ✔ | 2 ✔ |
| torus 2×3 | 6 | 12 | 6 | 0 | 1 | **2** | 1 | **2** ✔ | 2 ✔ |
| torus 3×3 | 9 | 18 | 9 | 0 | 1 | **2** | 1 | **2** ✔ | 2 ✔ |
| tetrahedron (sphere) | 4 | 6 | 4 | 2 | 1 | **0** | 1 | **0** ✔ | 0 ✔ |
| **disk 3×3** | 9 | 12 | 4 | 1 | 1 | **0** | **0** | **0** ✔ | **1 ✘** |

### WHAT THIS CORRECTS

**The disk was registered as a SCOPE CAVEAT — "the relation holds for closed orientable surfaces."
It was never a scope limit.** `2 − χ` is the wrong formula; the index form gets the disk right by the
same mechanism it gets the torus right. **`GRAVITY_DEFINED_V001.md` stated the caveat as if the
carrier were the problem. The formula was the problem.**

### WHERE THE `2` CAME FROM

**`2 = dim H₀ + dim H₂`** — one for **connected**, one for **closed and orientable**. It was never a
constant. On the disk `H₂ = 0`, so the `2` was never there, and the surface law fails by exactly
that `1`.

### WHY THIS MATTERS BEYOND THE ARITHMETIC

**`N` is an INDEX** — an alternating sum of dimensions. `N = 2 − (1/2π)∫K dA` is **Gauss–Bonnet**,
and Gauss–Bonnet is the two-dimensional case of **Euler–Poincaré**. Consequences, in order of weight:

1. **The capacity law needs no geometry.** It is stated for an arbitrary chain complex. Genus,
   curvature and area are special-case vocabulary.
2. **Area-independence stops being an observation and becomes structural.** `χ` is unchanged by local
   refinement of the complex, so `N` cannot move under it. **This is what G1 measured** (2 records at
   area 4 and at area 6) — now with a reason, and confirmed here at a third area.
3. **Curvature enters only through its integral**, which is the same statement seen through the
   surface case.

### THIS DOES NOT DEPEND ON G-6

G-7 is established on **our own carriers**, independently of whether `H₁` is unique. **G-6 decides
whether homology is FORCED by R1–R3; G-7 says that where homology is what carries the record, the
count is an index and not a surface formula.** Both branches of G-6 leave G-7 standing.

**AND THE REGISTRAR'S FRAMING OF G-6 WAS WRONG AND IS CORRECTED.** It was written as if
NOT-UNIQUE were "the bigger result". **UNIQUE is at least as large: it makes R1–R3 force homology,
turns statement 4 from "records ADMIT" into "records REQUIRE", and closes O-3.** The two branches
are large in different directions. Ranking them was the two-valued-object tic, not a finding.

---

## G-4 — **THE RECORD-LEVEL CONSTRAINT, IN ITS OWN TERMS.** `LANE_X6_CONSTRAINT_ALGEBRA`

Stated with no external referent, as **D-1** requires.

> ### The Gauss constraints close into **`Z₂^(NV−1)`** — elementary abelian, exponent 2, with **STRUCTURE CONSTANTS.**

| measured | 2×2 torus | 2×3 torus | meaning |
|---|---|---|---|
| `max ‖[G_v,G_w]‖` over **all** pairs | **0** exact (6 pairs) | **0** exact (15 pairs) | **abelian.** Integer zero in both representations, not a tolerance |
| positive control `‖[σˣ,σᶻ]‖_F` | 32.0000000000 vs closed form 32.0000000000 | — | **a reported zero is a measurement, not a broken norm** |
| `max‖G_v² − I‖` | 0 | 0 | every generator an **involution**; group exponent 2 |
| `∏_all v G_v` | **I** | **I** | one global relation — the generators are **not independent** |
| relation subgroup, **exhaustive** over all `2^NV` words | **2 elements** | **2 elements** | that relation is the **only** one; corank exactly 1 |
| GF(2) incidence rank | 3 (`NV`=4) | 5 (`NV`=6) | `NV−1` — the statement that **the graph is connected**. Scale-free |
| group order, explicit enumeration | 8 = 2³ | 32 = 2⁵ | `Z₂^(NV−1)`, by two independent methods |
| **state-to-state variation in the structure coefficients** | **0** | **0** | **STRUCTURE CONSTANTS.** 48 generic + 48 physical + 48 superposition states, plus the operator identity on every ordered pair |

**The composition law was read off FROM each state, not asserted: on every sampled state the matching
word set was exactly `{e_v + e_w + K}`, the predicted coset, with no state-dependent member.**

### THE CONSTRAINT MAKES A REGION'S TOTAL A SURFACE OPERATOR — AND HIDES THE INTERIOR

| | result |
|---|---|
| `‖P_R − ∏_{l∈∂R} σ_l‖` | **0.000000e+00**, every region, both bases — the bulk constraints cancel **exactly** |
| `support(P_R)`, `\|R\| = 1,4,9,16,25` | 4, 8, 12, 16, 20 — **= 4√\|R\| exactly**, residuals `[0,0,0,0,0]`, fitted exponent **0.500000**: a **PERIMETER law** |
| uncancelled product | `2k² + 2k` — area **plus** perimeter. **The cancellation removes an area's worth of operator content** |
| placement dependence | **min = max in all 14 rows** — the W-46 corner defect is guarded, not merely avoided |
| **hidden interior information** | **`(k−1)²` bits — an AREA — and NONE of it is visible in the boundary operator** |

**So the constraint puts the TOTAL at the boundary while the CONTENT stays an area inside it, invisible
from outside. Boundary support `4k` against hidden interior `(k−1)²`: perimeter against area, diverging
as `k/4`.**

### THE RECORD SPACE AS A QUOTIENT — EXACTLY

| lattice | `dim Z₁` | `dim B₁` | `dim H₁` | |
|---|---|---|---|---|
| torus 2×2 | 5 | 3 | **2** | |
| torus 2×3 | 7 | 5 | **2** | |
| torus 3×3 | 10 | 8 | **2** | |
| | **moves with area** (`F+1`) | **moves with area** (`F−1`) | **CONSTANT** | |

Gauss law ⟺ `ker ∂₁`, exhaustive **match rate 1.0**. Cosets `= 2^{dim H₁}`; every coset has exactly
`2^{dim B₁}` elements. **The record space IS `Z₁/B₁` — the Gauss-law sector modulo plaquettes.**
**Both the numerator and the denominator grow with area; only the quotient does not.**

---

## AND THE WITHDRAWN X-6 QUESTION — **IT WOULD HAVE FAILED. RECORDED SO THE WITHDRAWAL IS NOT AN ESCAPE.**

X-6 was withdrawn as an import (**D-1**) *before* these results returned. Both adversarial roles then
returned the same verdict, and the register states it rather than burying it:

- **prosecution: FIRES.** Ours is a finite abelian *group* with structure constants; gravity's is a Lie
  **algebroid** with structure **functions** (`h^{ab}` in `{H⊥,H⊥}`), and by **Hojman–Kuchař–Teitelboim**
  the hypersurface-deformation algebra plus locality plus `h_ij` **uniquely determines** the ADM
  constraints. Our side has **no analogue of `H⊥` at all**.
- **rescue-detector: FIRES**, and it pre-named the three escapes — the Chern–Simons presentation swap,
  level migration, and the continuum deferral.

**AND THE SPECIFICITY AUDIT KILLED HALF MY ORIGINAL PARALLEL INDEPENDENTLY.** "Physical content appears
as a boundary term" is **generic**: by **Noether's second theorem** *any* local gauge symmetry gives
`Q = ∮k`, off-shell and identically. **Likelihood ratio ≈ 1.** So even had X-6 run as stated, one of its
two legs carried **no evidential weight whatsoever** — I had built a test half of which could not
discriminate anything.

### RECORDED AS A RELATIONSHIP, CARRYING NO VERDICT (permitted by D-1)

| | 3+1 gravity | 2+1 gravity | ours |
|---|---|---|---|
| structure | **functions** (`h^{ab}`) | **constants** in Chern–Simons form | **constants** (measured 0 variation) |
| Lie algebra? | **no** — algebroid | yes, in CS form | yes — abelian group |
| local propagating dof | 2 | **0** | 0 |
| physical space | `C̄/gauge` | `Hom(π₁(Σ),G)/G` | `Hom(π₁(Σ),Z₂) = Z₁/B₁` |

**The last row is the same functor at a different group, and it is logged as an observation with zero
evidential weight for identity. It is not a claim, and nothing in the program rests on it.**

---

## G-10 / G-11 — **THE INDEX SURVIVES OFF MANIFOLDS. THE PROTECTION DOES NOT.** `LANE_G10_NONMANIFOLD`

Eleven carriers: manifolds, a non-orientable surface, a surface with boundary, a pure graph, three
pinch-point complexes, two tori wedged at a point, and **an abstract chain complex with no geometric
realisation at all.** All six self-checks PASS.

| | result |
|---|---|
| **(A) index identity** `dim H₁ = dim H₀ + dim H₂ − χ` | **HOLDS on all 11**, including the abstract complex |
| **(B) surface law** `dim H₁ = 2 − χ` | **FAILS on 6 of 11** — disk, theta graph, all three bouquets, two wedged tori, abstract complex |
| **(C) capacity** — Z₂ gauge degeneracy vs `2^{dim H₁}` | **MATCH on all four tested, INCLUDING the non-manifolds.** Bouquet: 8 = 8. Theta: 4 = 4. Two tori wedged: 16 = 16 |
| **(D) protection** — does `d` grow? | **NO. It does not track the index.** |

### (D) IS THE RESULT, AND IT SEPARATES R1 FROM R3

| family | size | `dim H₁` | **distance `d`** |
|---|---|---|---|
| torus L×L (manifold) | 2, 3, 4 | 2, 2, 2 | **2, 3, 4 — grows** |
| **bouquet of k triangles (pinch)** | 2, 3, 4 | **2, 3, 4 — grows** | **3, 3, 3 — CONSTANT** |

> **The bouquet has UNBOUNDED CAPACITY WITH FIXED PROTECTION.** As many records as you like, every one
> of them destroyable by a **weight-3** operator. The torus is the mirror image: capacity fixed at 2,
> protection growing without limit.

### WHAT THIS DOES TO G-7 — **IT SCOPES IT, AND THE SCOPE IS THE POINT**

**"The capacity law needs no geometry" is TRUE.** Verified on a complex with no geometric realisation.

**"The record needs no geometry" is FALSE.** A record requires **R1 AND R3**. The index delivers R1 on
any chain complex whatsoever. **It says NOTHING about R3.**

> **Γ IS NOT AN INDEX. Γ is an index PLUS a condition that the nontrivial classes have MINIMUM WEIGHT
> GROWING WITH THE CARRIER.** The first half is pure algebra and geometry-free. **The second half is
> where something metric re-enters — and it is the half that does the protecting.**

**The registrar's own next-step framing was therefore half right and half wrong.** "If the law survives
on a non-manifold, needs-no-geometry is a claim" — it survives, and the claim is real **for capacity
only**. The test as posed would have returned a clean PASS and concealed the separation. **It was the
distance column, which the framing did not ask for, that carried the finding.**

### AND IT BEARS ON G-6

**R1 is cheap** — satisfied by graphs, pinch points, and abstract complexes alike. **If uniqueness is
to hold, R3 must be what forces the structure.** G-6 should be read against R3, not R1.

---

## G-6 — **UNIQUENESS IS BROKEN. `H₁(Σ)` IS ONE STRUCTURE SATISFYING R1–R3, NOT THE ONLY ONE.**

Five lenses, each adversarially adjudicated against the five clauses. **One lens (fracton) died on an
API error and did not return — that region of the space is UNSWEPT and is recorded as a coverage gap,
not as a null.**

| survivor | strength | why it is not a surface |
|---|---|---|
| **`H_k` of an ARBITRARY `F₂` chain complex** | **DECISIVE** | the general CSS template; contains members no surface realises |
| **asymptotically good qLDPC** — Panteleev–Kalachev, Leverrier–Zémor, Dinur–Hsieh–Lin–Vidick | **STRONG** | `[[n, Θ(n), Θ(n)]]`. **Not a manifold ANYWHERE**: every vertex link is a `Δ×Δ` grid of `Δ²` squares, and a 2-manifold vertex link is a single cycle. Independently, **Delfosse's bound** `kd² ≤ C(log k)²n` holds for *any* tiling of *any* compact 2-manifold; here `kd² = Θ(n³)` — **exceeded by `Θ(n²/log²n)`** |
| **3D toric code**, `H₁(T³)` | **STRONG** | `[[3L³, 3, L]]`, two distances `L` and `L²`; geometric locality unchanged |
| hypergraph product (Tillich–Zémor) | weak | the toric code *is* the hypergraph product of two repetition codes — closest to the anchor in disguise |

### WHAT DIES AND WHAT SURVIVES

- **DEAD: "records require a SURFACE."** Statement 4's manifold reading is refuted.
- **SURVIVES: "records require non-trivial homology."** Every survivor is `H_k` of an `F₂` complex.
- **BUT NOT ESTABLISHED EITHER:** R1–R3 nowhere require a **CSS** structure. Non-CSS stabiliser codes
  and **non-abelian topological order (Levin–Wen, Fibonacci — writers are Wilson loops, not `F₂`
  chain-complex objects)** are untested. **The general condition is AT MOST this narrow and possibly
  wider.**

### THE CONDITION, AS FAR AS IT IS ESTABLISHED

> **Γ = a length-2 `F₂` chain complex whose `k`-SYSTOLE *and* `k`-COSYSTOLE both exceed the local scale.**

**R3 NEEDS TWO NUMBERS, NOT ONE.** `d_Z` and `d_X` coincide **only in self-dual cases such as the
square-lattice torus** — which is exactly why this program measured a single `d` and derived `d = 2`.
**The single distance was an artefact of the carrier we chose.**

### ERRATUM TO THEOREM B'S ATTRIBUTION — **THE WRITER IS NOT POINCARÉ DUALITY**

`GRAVITY_DEFINED_V001` credited the writer to *"non-degeneracy of the intersection form (Poincaré
duality)"*. **Over-credited.** The pairing `H_k(C) × H^k(C) → F₂` is **perfect for ANY chain complex
over a field** (universal coefficients; `Ext` vanishes over a field). **R2 needs no manifold, no
orientability and no Poincaré duality — it is free linear algebra.** Theorem B's *result* stands;
its stated *source* was too strong.

### AND IT COMPOSES WITH G-11

**G-11 showed R1 is cheap — graphs and pinch points supply capacity freely. G-6 now shows the
homology class is also not unique.** What discriminates is **R3**, and R3 is the systole/cosystole
condition. **The program's centre of gravity moves from "which topology" to "what makes minimum
weight grow."**

---

## D-4 — **ALLOW/REQUIRE IS THE PROGRAM'S TYPE DISCIPLINE, NOT A FACT ABOUT GRAVITY.** F-2 AND F-3 WERE THE SAME ERROR ONE LEVEL DOWN

The principal, on the registrar's *"nothing in the program says how a system comes to have growing
minimum weight"*: **"Isn't this the whole allow/require framework?"**

**It is, and the registrar had walked straight back into it — an hour after registering D-1.**

> **MINIMUM WEIGHT (systole / cosystole) IS A PROPERTY OF THE CARRIER, SO IT IS AN ALLOW.** It says a
> record **may** exist. **Asking what PRODUCES growing minimum weight is asking what produces a
> PERMISSION — the identical category error as demanding backreaction at X-2.**

### THE DISCIPLINE, GENERALISED FROM GRAVITY TO THE WHOLE PROGRAM

| type | what it is | the legitimate question | the category error |
|---|---|---|---|
| **ALLOW** | a permission — what the world's structure **admits**. `records = index`; `systole > local scale`; the Gauss law; Einstein's constraints | **what does it permit, and what is the permitted set?** | *"what produces it?"* |
| **OCCUPANCY** | which of the permitted possibilities **is actually the case** | **what dynamics puts the system HERE rather than elsewhere in the allowed set?** — legitimate, and it is where the arrow lives | — |

**This is not a claim that nothing in physics is a production rule.** Maxwell has evolution equations;
Lindblad dynamics is a production rule. **The discipline is about TYPE-MATCHING: dynamics produces
OCCUPANCIES, never PERMISSIONS.**

### WHAT THIS DOES TO THE RFP, REGISTERED THE SAME DAY IT WAS WRITTEN

| | as written | ruling |
|---|---|---|
| **F-1** arrow | a before with no record, an after with one | **STANDS** — about states, not permissions |
| **F-2** *"the protection TURNS ON"* | min weight goes from `O(1)` to growing | **WITHDRAWN AS WRITTEN.** It asks what produces the systole. **CORRECTED: given a carrier whose systole permits a record, what makes the system occupy a DEFINITE record instead of a mixture?** |
| **F-3** *"the carrier ARISES"* | the complex is not assumed | **RECLASSIFIED, same class as X-2.** It asks what produces the allow. `T-II.5` inherits the reclassification |
| **F-4** dynamics not an act | follows from `(H, {L_k})` | **STANDS** |
| **F-5** measurement | is a measurement the creation of a record? | **COLLAPSES INTO CORRECTED F-2** |

### AND THE COLLAPSE IS A RESULT, NOT A TIDY-UP

> **ONCE FORMATION IS AN OCCUPANCY QUESTION, THE FORMATION QUESTION AND THE MEASUREMENT QUESTION ARE
> THE SAME QUESTION:** *what selects one element of an allowed, exactly degenerate set?*
> **F-5 was never a separate item.** `T-V.3` — "the natural bridge to the measurement problem" — is
> not a bridge to a neighbouring problem. **It is the problem, under the program's own name for it.**

### THE PREDICTION SURVIVES, AND IT WAS ALREADY THE RIGHT SHAPE

The registered advance prediction — *a Davies bath reaches an equal mixture of all `2^{2g}` record
states, which is no record* — **is an OCCUPANCY statement.** It asks what the dynamics puts in the
allowed space, not what makes the space. **It was correctly typed before the requirements around it
were.** It stands unchanged as the RFP's first test.

---

## F-7 FIRST TEST — **THE PREDICTION HOLDS, AND THE REAL RESULT IS STRONGER THAN THE PREDICTION**

`LANE_F7_OCCUPANCY/f7_davies.py`. Toric code, 2×2 torus, `L=8`, dim 256, ground space **4**.
**Logicals COMPUTED from `Z₁/B₁` and `Z¹/B¹`, not nominated** — `‖[Z̄,H₀]‖ = ‖[X̄,H₀]‖ = 0.000e+00`,
`‖{Z̄,X̄}‖ = 0.000e+00`, `Z̄` splits the ground space 2–2.
**DEFECT CAUGHT AND FIXED BEFORE ANY NUMBER WAS READ:** the first build *nominated* the logicals and
self-check reported `‖[Z̄,H₀]‖ = 64` — the identical W-62 defect. Every number below is from the
computed operators.
**BATH POSITIVE CONTROL (the W-49 trap):** the Davies generator reproduces Boltzmann exactly at
`β = 0.5` and `β = 2.0` — `[0.622459, 0.377541]` and `[0.880797, 0.119203]`.

### 1. THE REGISTERED PREDICTION IS CONFIRMED EXACTLY

| β | `‖L(ρ_Gibbs)‖` | `⟨Z̄⟩` | `⟨Z̄₂⟩` | `⟨X̄⟩` | purity on code | `S/ln4` |
|---|---|---|---|---|---|---|
| 0.5 | 7.557e-16 | **0.000000** | 0.000000 | 0.000000 | **0.250000** | **1.000000** |
| 1.0 | 5.913e-16 | **0.000000** | 0.000000 | 0.000000 | **0.250000** | **1.000000** |
| 2.0 | 2.642e-17 | **0.000000** | 0.000000 | 0.000000 | **0.250000** | **1.000000** |
| 5.0 | 4.086e-22 | **0.000000** | 0.000000 | 0.000000 | **0.250000** | **1.000000** |

**Purity `= 1/4` and entropy `= ln 4` exactly: the maximally mixed state on the code space.
THERMAL RELAXATION CANNOT FORM A RECORD.** And a **definite** record decays —
`d⟨Z̄⟩/dt = −1.341e-03` from `⟨Z̄⟩ = +1`.

### 2. AND THE PREDICTION'S *REASON* WAS INCOMPLETE — LIFTING THE DEGENERACY IS NOT ENOUGH

The prediction blamed degeneracy. **Lift it and the record still does not form.**

| perturbation | `‖[pert, X̄]‖` | splitting `ΔE` at `ε=0.2` | `⟨Z̄⟩` | selects? |
|---|---|---|---|---|
| `Σ X_l` | **0.00e+00** | 1.691e-01 | **0.000000** | **no** |
| `Σ Z_l` | 4.53e+01 | 1.691e-01 | **0.211000** | **YES** |

**`Σ X_l` commutes with the WRITER `X̄`, and `X̄` anticommutes with `Z̄` — so any `X̄`-symmetric state
has `⟨Z̄⟩ = 0` IDENTICALLY, at any splitting.** The `Σ Z_l` row is the positive control: the
measurement **can** see selection, so the zeros are a symmetry and not a broken instrument.

> ### **THE CONDITION FOR FORMATION IS NOT "LIFT THE DEGENERACY". IT IS "BREAK THE SYMMETRY GENERATED BY THE WRITER."**

### 3. THE EXCHANGE RATE — **SELECTION IS BOUGHT WITH PROTECTION, AT PARITY**

| `ε` | `ΔE` | `⟨Z̄⟩` | `⟨Z̄⟩/ΔE` |
|---|---|---|---|
| 0.010 | 4.0006e-04 | 0.000500 | **1.2500** |
| 0.020 | 1.6010e-03 | 0.002001 | **1.2500** |
| 0.050 | 1.0037e-02 | 0.012547 | **1.2500** |
| 0.100 | 4.0594e-02 | 0.050742 | **1.2500** |
| 0.200 | 1.6914e-01 | 0.211000 | 1.2475 |

`⟨Z̄⟩ = ½ tanh(βΔE/2)`, with `⟨Z̄⟩/ΔE = β/4` **constant to four figures over three decades.**

| log–log slope in `ε` | |
|---|---|
| splitting `ΔE` | **2.0262** — Theorem D's `ε^d` with derived `d = 2` |
| selection `⟨Z̄⟩` | **2.0210** |

> ### **THE BIAS IN THE RECORD AND THE LOSS OF ITS PROTECTION ARE THE SAME QUANTITY, WITH THE SAME EXPONENT `d`. THERE IS NO `ε` AT WHICH ONE APPEARS WITHOUT THE OTHER.**

### WHAT IS EXCLUDED, AND THE NEXT STEP

**Energy-based dynamics is excluded as the RFP** — not because degeneracy blocks it, but because
**anything that biases the record by an amount unprotects it by the same amount at the same order
`d`. Protection and formability are one quantity with opposite sign.**

**NEXT STEP, CONCRETE.** The escape must be dynamics that is **not** energy-based, i.e. not
detailed-balance. Three candidates, in order of cost:
1. **a driven / non-equilibrium bath** — no Gibbs steady state, so the parity argument does not apply
2. **measurement-induced selection** — which by **D-4** is the *same question*, not a different one
3. **a NON-LOCAL bath coupling** — and note this is exactly what **P-3** says the writer must be

**Test 3 first: it is the only one the program already has a theorem about.**

---

## F-10 — PREDICTION REGISTERED BEFORE THE RUN

**THE QUESTION, POSED SO IT CANNOT BE ANSWERED BY CONSTRUCTION.** Handing a bath a logical operator
and observing that a record forms proves nothing — it assumes the answer. The non-circular question is
a **necessary condition**:

> **With `H = H₀` exactly degenerate and fully protected, what is the MINIMUM WEIGHT of a bath
> coupling that produces `d⟨Z̄⟩/dt ≠ 0` from the maximally mixed code state?**

**PREDICTION.** By **Knill–Laflamme**, any operator `C` with `wt(C) < d` satisfies `P_g C P_g ∝ P_g`,
so it cannot distinguish record states. Therefore:

> ### **NO COUPLING OF WEIGHT `< d` CAN FORM A RECORD, AND THE FORMATION THRESHOLD EQUALS THE DESTRUCTION THRESHOLD. BOTH ARE `d`.**

At `d = 2`: **weight-1 couplings give exactly zero; weight-2 can be non-zero.**

**LIMITATION, STATED IN ADVANCE.** The 2×2 torus is the only carrier of feasible dimension (256), and
it has `d = 2`. **The threshold is therefore tested at ONE value of `d`. The scaling claim is NOT
tested by this run** — 3×3 would need dim 262144.

---

## F-10 RESULT — **THE FORMATION THRESHOLD IS THE CODE DISTANCE. BOTH ARE `d`.**

`LANE_F7_OCCUPANCY/f10b_threshold.py`.
**v1 WAS MIS-DESIGNED AND THE MEASUREMENT CAUGHT IT:** it measured `d⟨Z̄⟩/dt` under a **Davies** bath,
but **F-9 already excludes every detailed-balance bath at any weight** — so the answer was fixed by
the bath class before weight could matter, and it returned `threshold = None`. **A test whose result
is entailed by a prior result is not a test.** v2 separates the necessary condition (bath-independent)
from sufficiency (which must use a non-equilibrium bath by construction).

### A. NECESSARY — Knill–Laflamme, and it cannot inherit F-9's exclusion because no bath appears in it

| weight | # couplings | `max ‖P_g C P_g − (trC/4)P_g‖` | |
|---|---|---|---|
| **1** | 24 | **6.344e-16** | **acts as a SCALAR — cannot form** |
| **2** | 252 | **2.000e+00** | **distinguishes code states** |
| 3 | 1512 | 2.000e+00 | distinguishes code states |

> **MINIMUM WEIGHT WITH ANY CODE-SPACE ACTION = 2 = `d`. THE PRE-REGISTERED PREDICTION IS CONFIRMED.**

### B. SUFFICIENT — a non-equilibrium bath, and it costs NO protection

Single non-Hermitian jump operator `σ⁻ = P₊X̄P₋` (**support 3 qubits**; `‖σ⁻ − σ⁻†‖ = 16.0`, and **a
Hermitian jump operator can only dephase, never select**). `H` is untouched — still `H₀`, still exactly
degenerate.

| `t` | `⟨Z̄⟩` | code-space weight | purity on code |
|---|---|---|---|
| 0.00 | 0.000000 | **1.000000** | 0.250000 |
| 1.00 | 0.635830 | **1.000000** | 0.351070 |
| 4.00 | 0.982412 | **1.000000** | 0.491283 |
| 6.00 | **0.997667** | **1.000000** | 0.498835 |

**THE RECORD FORMS WITHOUT EVER LEAVING THE CODE SPACE AND WITHOUT LIFTING THE DEGENERACY.** Purity
tends to `1/2`, not 1, because selecting one logical qubit leaves the other mixed — as it must on a
4-dimensional code space.

### C. CONTROL — 576 operators `(A + iB)/2` with `A,B` of weight 1: `max |d⟨Z̄⟩/dt| = 5.551e-16`

**No weight-1 jump operator forms a record, Hermitian or not.**

---

### WHAT THIS ESTABLISHES, AND IT REVERSES F-9's VERDICT UNDER ONE CONDITION

**F-9:** under **energy-based** dynamics, selection is bought with protection at parity — same
exponent `d`, no `ε` where one appears without the other.
**F-10:** **drop detailed balance and selection costs NO protection at all** — `⟨Z̄⟩ → 0.9977` with
code-space weight `1.000000` throughout and `H` untouched. **But the coupling must weigh at least `d`.**

> ### **THE RFP HAS TWO REQUIREMENTS, BOTH NECESSARY:**
> ### **(1) NON-EQUILIBRIUM DYNAMICS — no detailed balance. (2) A COUPLING OF WEIGHT ≥ `d`.**
> ### **AND `d` IS THE SAME `d` THAT PROTECTS. A RECORD IS EXACTLY AS HARD TO FORM AS IT IS TO DESTROY.**

Requirement (2) extends **P-3 / Theorem B** from the writer to the *bath*: **whatever forms a record
must couple at least as non-locally as the record is protected.**

### THE OBSTRUCTION THIS CREATES — the program's problem has MOVED, not closed

**A bath coupling of weight ≥ `d` is itself a non-local process.** The question is no longer *how does
a record form* but **WHAT SUPPLIES A NON-LOCAL, NON-EQUILIBRIUM COUPLING?** That is the next
obstruction and it is sharper than what it replaced.

**LIMITATION, AS STATED IN ADVANCE:** `d = 2` only. **The threshold is tested at ONE value of `d`;
the scaling `threshold = d` is NOT tested by this run.**

---

## A-EM CONSOLIDATED — **EM'S ROLE IS LARGER THAN "SUPPLIES THE CARRIER", AND TODAY'S RESULTS SHOW HOW MUCH**

The principal: *"I think we saw in the past how EM has a powerful role in this process."*
**The register under-credited it.** `A-EM` read *"supplies the gauge field and the holonomy that IS
the record"*; `THE_CLAIM` reads *"EM provides the carrier"*. Four measured results say more.

### 1. EM SUPPLIES BOTH BOUNDARY MAPS — THE WHOLE CHAIN COMPLEX, NOT JUST THE FIELD

| the complex | `C₂ →^{∂₂} C₁ →^{∂₁} C₀` | what it is physically |
|---|---|---|
| `∂₁` | **IS the Gauss law** | EM's constraint |
| `∂₂` | **IS the plaquette / field-strength term** | EM's magnetic action |
| `C₁` | the links | where the gauge field lives |

**The carrier supplies the SETS (which cells exist and how they meet). EM supplies the MAPS.**
`H₁ = Z₁/B₁` needs both — measured at match rate **1.0** (G-9).

### 2. THE RECORD SPACE IS THE HOMOLOGY OF EM'S OWN COMPLEX — G-9, MEASURED

`dim Z₁ = 5,7,10` and `dim B₁ = 3,5,8` both move with area; `dim H₁ = 2,2,2` does not.
**Both the Gauss-law sector and the plaquette space are EM structures. The record is what survives
their quotient.**

### 3. **NEW — THE MINIMAL COUPLING THAT CAN FORM A RECORD IS AN EM HOLONOMY.** `f10c_whatformsit.py`

Of 252 weight-2 Paulis, **8 distinguish code states. All 8 commute with every stabiliser — all 8 are
LOGICAL.** And every one is an EM holonomy on a non-contractible cycle:

| | count |
|---|---|
| all-`Z` supported on a **CYCLE** — magnetic Wilson loop | **4** |
| all-`X` supported on a **COCYCLE** — electric Wilson loop | **4** |
| **neither** | **0** |

### 4. SO THREE DIFFERENT THINGS TURN OUT TO BE THE SAME KIND OF OBJECT

> ### **THE RECORD IS AN EM HOLONOMY ON A NON-CONTRACTIBLE CYCLE (Thm B ii).**
> ### **ITS WRITER IS AN EM HOLONOMY ON A NON-CONTRACTIBLE CYCLE (W-62).**
> ### **AND THE MINIMAL THING THAT CAN FORM IT IS AN EM HOLONOMY ON A NON-CONTRACTIBLE CYCLE — 8 of 8, ZERO EXCEPTIONS.**

**The program did not put these three in the same class. They arrived there separately, by three
different measurements, and the third is new today.**

### WHAT THIS DOES TO Γ

**Γ is not an independent field alongside EM.** It is **the statement that EM's own complex has
non-trivial homology.** The carrier decides which cells exist; EM decides the maps; **Γ is a property
of the pair, and of neither alone.**

**CAUTION, STATED:** this does NOT dissolve Γ into EM. The cell structure is not EM's — G-6 already
showed the homology can be that of complexes with no manifold behind them at all, and G-11 showed
protection needs something metric that homology alone does not supply. **Γ remains a distinct
requirement (R1–R3). What changes is that it is a requirement ON EM'S COMPLEX, not a separate
ingredient beside it.**

---

## D-5 / A-EM4 — **AT THE RECORD LEVEL EM HAS NO LOCAL CONTENT. THE FIELD-VALUE PICTURE DOES NOT TRANSFER.**

The principal: *"at the record level EM is a massive object and not just some field measured in other
contexts."* **`LANE_EM_EXTENT/em_extent.py`** — closed forms verified against explicit GF(2) ranks at
`L = 2,3,4,5` (all PASS).

### HOW BIG IS THE EM OBJECT THAT CARRIES ONE RECORD

| `L` | links | `dim Z₁` | `dim H₁` | **record fraction** | `d` (support) | `d`/links |
|---|---|---|---|---|---|---|
| 2 | 8 | 5 | 2 | 4.000000e-01 | 2 | 0.250000 |
| 4 | 32 | 17 | 2 | 1.176471e-01 | 4 | 0.125000 |
| 16 | 512 | 257 | 2 | 7.782101e-03 | 16 | 0.031250 |
| 256 | 131072 | 65537 | 2 | **3.051711e-05** | **256** | 0.001953 |

**THREE THINGS ARE TRUE AT ONCE, AND NO FAMILIAR OBJECT SATISFIES ALL THREE:**

| | |
|---|---|
| **absolute extent `d = L → ∞`** | the object carrying one bit grows **without bound**. It is not a local excitation |
| **record fraction `2/(L²+1) → 0`** | it is a **vanishing fraction** of EM's own gauge-invariant content. It is not "all of EM" either |
| **local content ZERO** | **no local operator reads it** — Thm C, `1.59e-16` |

### THE IMPORT GUARD

> **D-5. MEASURES THAT APPLY TO EM AS A LOCAL FIELD HAVE NO REFERENT AT THE RECORD LEVEL.**
> Field strength at a point, energy density, local flux, a value `E(x)` or `B(x)` — **none of these
> has a record-level meaning.** Using one is an import of the same class as classical gravity's, and
> **D-1 applies to it unchanged.**
> **TELL:** any sentence that assigns EM a value, density or strength **at a place**.

### AND IT CORRECTS A WEAK FRAMING THE PROGRAM HAS BEEN CARRYING

**`THE_CLAIM_V001` says "EM provides the carrier."** A *carrier* suggests a medium that something is
written **on**. **There is no such separation here: the record IS the holonomy.** The object and its
carrier are the same thing, that thing is extended, and **it has no local parts to be written on.**

**Found by the principal's prompt, not by the running import audit** — recorded so the audit's eventual
coverage is not overstated.

---

# IMPORT AUDIT — **FOUR LOAD-BEARING IMPORTS BESIDES CLASSICAL GRAVITY. THREE ARE HIGH AND ALL FOUR HIT ROWS REGISTERED TODAY.**

Six lenses, adversarially adjudicated, each testing not *is this imported* but **would a registered
PROVED row change if it were dropped.** The principal asked the question; the audit answered it against us.

## 1. **THE ENSEMBLE AVERAGE `⟨R⟩ = Tr(Rρ)` USED AS THE TEST FOR FORMATION** — HIGH, and the program had ALREADY CAUGHT IT

**`SURFACE_ASSUMPTION_AUDIT_V001.md:16`** — *"**A4** | "durable" = expectation value constant | imported;
**W-35 showed ensembles are blind to record formation**"* — **and A4 is NOT CLEARED.**
**`REGISTER:2611`** — *"Every lane from W-28 onward measured `⟨R⟩ = Tr(Rρ)` — an ENSEMBLE AVERAGE.
**A fair coin has mean zero and every single flip is definite.**"* W-35 unravelled the same Lindbladian
and found a **definite record on 78.5% of runs.** `REGISTER:2646` closes the escape: *"Both
unravellings give the same `ρ(t)`"* — so purity `1/4` and `S/ln4 = 1` do not rescue the reading either.

**AND THE ENTIRE F-SERIES WAS RUN THROUGH THAT SAME DOOR TODAY.** `grep` of `LANE_F7_OCCUPANCY/` for
`unravel|trajector|single-run|ensemble` returns **ZERO hits.** The audit naming A4 is timestamped
**11:28**; `f7_davies.py` is **14:37**; `f10c` is **14:56**. **Six PROVED rows registered on top of a
named, uncleared assumption within three hours of it being named.**

**WHY IT WAS INVISIBLE, and this is the structural lesson:**
1. **A4 lives in prose, not in the ledger.** It has no row and no D-entry. **The ledger is what gets checked.**
2. **A blind instrument returns exact zeros.** `⟨Z̄⟩ = 0.000000` and `S/ln4 = 1.000000` read as strong
   confirmation. **They are the signature of the blindness.**

## 2. **"MINIMUM WEIGHT MUST GROW WITH THE CARRIER"** — HIGH. **CLAUSE (v) IS BINARY AND SAYS NO SUCH THING**

Clause (v) reads *"NO contractible operation does."* **Binary.** Nothing in the corpus argues that a
record's protection must **grow**. That requirement is imported from **asymptotic good-code-family
theory**, where `d = Θ(n)` is the quality criterion.

**AND IT INVERTS G-11's CONCLUSION.** The bouquet's cycles ARE the generators of `H₁` — they are
**non-contractible**. So a weight-3 operator traversing one is **not a contractible operation**, and
**the bouquet SATISFIES clause (v) as written.** G-11's *numbers* stand (capacity 2,3,4 against `d`
3,3,3). Its *conclusion* — that protection fails there, so Γ needs a growing-weight condition — is the
import.

**G-12's refuter cannot fire:** `"the local scale"` occurs three times in the corpus and **none of them
is a definition.** That is precisely the defect withdrawn at `GRAVITY_DEFINED_V001`: *"it can never
fire… an unfalsifiable test is worthless."*

## 3. **GIBBS STANDING IN FOR "ENERGY-BASED DYNAMICS" AS A CLASS** — HIGH. **THE VERDICT SURVIVES; THE STATED CONTENT DOES NOT**

Re-run on our own carrier. The registered row reproduces exactly (ratio `1.2500`, slopes `2.0262/2.0210`)
— **and the parity is canonical-only.** The constant is `−f'(0)/f(0)/4`:

| occupation `f(ΔE)` | constant | selection slope | splitting slope |
|---|---|---|---|
| Gibbs `β=5` | 1.2500 | 2.0210 | 2.0262 |
| Gibbs `β=1` | 0.2408 | 2.0187 | 2.0262 |
| power law `1/(1+ΔE)³` | 0.6552 | 1.9795 | 2.0262 |
| **Gaussian `exp(−2ΔE²)`** | 0.0050 | **4.0465** | 2.0262 |

**The exponent equality FAILS for the Gaussian, which is equally a function of `H` alone.**
**And `β = 0` is canonical and gives `⟨Z̄⟩ = −0.000000` (spread `1.97e-13`) at splitting `1.691e-01`
— SPLITTING WITHOUT SELECTION, which the register asserts does not exist.**

**WHAT SURVIVES, with its correct warrant:** for **any** occupation that is a function of `H` alone,
exact degeneracy forces flatness on the code space — verified `⟨Z̄⟩ ≤ 1.1e-14` across Gibbs `β=5` and
`β=0.5`, power-law `1/(1+ΔE)⁷`, a non-monotone `0.1+|sin 3ΔE|`, and a **random** function of the
eigenvalue. **The exclusion holds. "The same quantity, same exponent, no `ε` where one appears without
the other" is WITHDRAWN.**

## 4. **DETAILED BALANCE AS A CLASS IN A NECESSITY CLAIM** — MEDIUM, **AND F-13 MAY CONTRADICT ITSELF**

The evidence base is **one Davies generator built from weight-1 site operators.** `grep` for
`weak coupling|Born-Markov|secular|mean force` across the whole corpus returns **nothing relevant.**

**THE SELF-CONTRADICTION, and it is internal:** a strong-coupling thermal environment relaxes to the
**mean-force Gibbs state** `Tr_B[e^{−βH_tot}]/Z`, which depends on the **coupling operators** and not
on `H_S` alone. **For a coupling of weight ≥ `d` — exactly what F-13 clause (2) REQUIRES — that state
is not degeneracy-blind.** So a bath in detailed balance with respect to `H_tot` **meets F-13's own
registered falsifier while satisfying clause (2).**

---

# THE REMAINING WORK — **SIX ROWS ATTACKED, ALL SIX ADVERSARIALLY VERIFIED. O-1 IS SETTLED.**

## O-1 — **THE CONVERSE IS FALSE.** AND THE REPAIRED CONVERSE IS A THEOREM

**REGISTRY HYGIENE, FLAGGED:** P-2 reads *"(ii)+(iv) ⟹ the writer is built from neither `H` nor
`{L_k}`."* **The O-1 row describes P-1's converse, not P-2's.** Recorded, not silently fixed.

### LEMMA 0 — CLAUSE (ii) IS FAR STRONGER THAN IT READS

For `R` Hermitian, `[L,R] = 0 ⟺ [L†,R] = 0`. **So clause (ii) forces `R` into the commutant of the
`*`-ALGEBRA `A = alg{I, H, L_k, L_k†}` — not of the set `{H, L_k}`.**

### THE CONVERSE FAILS ON BOTH GAPS, WITH CONTROLS

| | |
|---|---|
| `H = diag(0,0,1,1)`, **one generic jump** | Hermitian commutant = scalars only **400/400**; **record exists 0/400** |
| **positive control**, same `H`, **diagonal** jumps | **record found 400/400** |
| `H = 0` (maximal degeneracy, the most favourable case there is), `d = 2,3,4,6,8` | `dim A = d²` in **all 10** rows; commutant dim **1**; record **no** in all 10 |
| **codimension** of `{L : [L,R]=0}` | `dim = p²+q²`, **6/6 exact**. Codim `2pq` — **measure zero for every `d ≥ 2`** |
| instability | `‖[L(ε),R]‖/ε = 4.9456` at every `ε` from `1e-8` to `1e-1` — **first order. 0/200 records.** Clause (ii) cannot be rescued by "small enough noise" |

**THE TRAP THAT KILLS THE OBVIOUS REPAIR.** A case with `max‖P_λ L_k P_λ‖ = 0.000e+00` — the noise
identically zero **inside every eigenspace** — and **still no record**, because `P A P` is irreducible.
Control with the return legs deleted: record **YES**, `(ii) = 0.00e+00`. **Second-order excursions out
of the eigenspace and back destroy records, so inspecting `P L P` alone can NEVER prove the converse.**

### THEOREM O1-A
> **A record non-constant on `E_λ` exists ⟺ the compression `P_λ A P_λ` is a PROPER subalgebra of `B(E_λ)`.** 6/6 against brute force.

### THEOREM O1-B — **AND IT REFUTES THE CONJECTURE IN MY OWN BRIEF**

I wrote that flippability was probably free on any degenerate subspace. **False.**
> **`U` with `U†RU = −R` exists ⟺ `p = q` ⟺ `Tr R = 0`.**

Balanced `(2,1,1),(4,2,2),(6,3,3),(8,4,4)`: `‖U†RU+R‖ = 9.6e-16 … 2.5e-15`. Unbalanced: **no flipper**,
and the positive control — **best of 4000 random unitaries each** — never drops below `2.000116`.

> ### **COROLLARY O1-B1: IN AN ODD-DIMENSIONAL HILBERT SPACE, `Tr R` IS ODD, SO NO RECORD IS EVER WRITABLE.**

### THE REPAIRED CONVERSE — **A THEOREM, 210/210 BY EXHAUSTIVE ENUMERATION**
> **A record satisfying (i)–(iv) exists ⟺ the commutant of `alg{I,H,L_k,L_k†}` contains a projection
> that is (H1) non-trivial on some eigenspace of `H` and (H2) trace-balanced.**

---

## O-4 — **"ADMISSIBLE" DEFINED, AND THE UNDEFINED WORD WAS LOAD-BEARING IN CLAUSE (v), NOT (iv)**

> **ADMISSIBLE `U` ≝ a unitary with `[U,H] = 0`.**

Consequences: **clause (iv) becomes exactly `Tr(P_E R) = 0` on every eigenspace of `H`** — agreeing
with O1-B independently. **P-3 survives but its conclusion weakens** to *"no admissible writer fits
inside ONE contractible region."*

> ### **AND THE STING: under the trivial reading "any unitary", THE TORIC CODE FAILS THE PROGRAM'S OWN CLAUSE (v).** The word was never optional.

## O-2 / O-3

**O-2 PROVED under stated hypotheses.** First-order splitting **is exactly** the non-vanishing of
`Φ(V) = PVP − (tr PVP/n)P`; guaranteed at weight 1 for a **connected** 0-form symmetry because its
charge is a sum of local densities. **And the topological vanishing to order `d−1` IS the
Knill–Laflamme condition** — slope `= d` confirmed on **five codes**.
**O-3's registered side-step is REFUTED by two explicit counterexamples.**

## O-5 — the relaxation must be a **spectral width**, never a norm bound

> **Clause (ii) relaxes as a width bound on the cluster carrying the DRESSED record.** The tolerance is
> then **exactly an inverse lifetime**, `T(η) ≥ η/δ` with `δ = c·p^d/Δ^{d−1}`.
> **W-61's four-million-fold separation SURVIVES. Read the naive way — a norm bound on a fixed `R` — it collapses to 0.35.**

## O-7 / O-8 — both gaps swept

- **FRACTONS WIDEN NOTHING.** X-cube, checkerboard **and Haah's cubic code are all length-2 `F₂` chain complexes.**
- **NON-CSS stabiliser codes provably ESCAPE that class.**
- **NON-ABELIAN order FAILS CLAUSE (iv) OUTRIGHT**, on a parity obstruction an `F₂` complex can never trigger.

## O-10 — **CLOSED, AND UPGRADED FROM A MEASUREMENT TO A PROOF**

**Threshold `= d` on all six codes at `d = 1, 2, 3`, including a non-CSS and a degenerate code — and the
equality is now PROVED for every stabiliser code and every coupling, not only Paulis.**
**F-11/F-13 no longer rest on the single `d=2` carrier.**

---

## O-12 CLOSED — **CLAUSE (v) WAS FALSE OF OUR OWN CARRIER. THE WORD FIXES IT.**

**AS PREVIOUSLY WRITTEN, clause (v) carried no admissibility restriction and was FALSE OF THE TORIC
CODE.** A single-edge `X` on `(0,0,H)` satisfies `X†RX = −R` **exactly**.

| | `L=3` | `L=5` |
|---|---|---|
| single-region Paulis that flip `R` (**positive control**) | **1158** | **2.815e15** |
| **ADMISSIBLE** flippers, `[U,H]=0`, over certified-contractible regions | **0** (36 regions) | **0** (300 regions, to 24 edges) |

Exact by `F₂` linear algebra, not sampling — both sets are subspaces, so the count is `0` or exactly
half. **Independently reproduced by a second implementation** (brute-force symplectic enumeration over
all `4^{|T|}` Paulis, no shared code): `1158` and `0`, min admissible weight **3 = d**.

### P-3's STRONG READING IS NOT UNPROVEN. **IT IS FALSE.**

Clause (v) quantifies over **single** regions, never **products**. A (v′) forbidding products would
give *"nothing local can write it"* — **and (v′) is false by the program's own Theorem D**, which says
`d` local terms **do** reach the record. **The gap cannot be closed by strengthening (v).**

**The minimum-weight admissible writer at `L=3` is weight `3 = d`, and it is a PRODUCT of three
single-edge operators each individually INADMISSIBLE (`‖[X_e,H]‖ = 45.255`). The record is written by
an operation that is admissible only AS A WHOLE.** This is the same `d` as F-13's forming coupling.

### DEFECTS IN THE LANE THAT PRODUCED THIS, CAUGHT BY THE VERIFIER

1. **THE REGISTERED FALLBACK WAS A MISCOUNT.** DEF-A′'s published table is arithmetically impossible
   in 3 of 7 rows — it reports **more** admissible unitaries than *all* unitaries. Corrected, DEF-A′
   equals DEF-A except on one row, and it fails the very case its own docstring says it rescues.
   **DEF-A has NO working escape hatch.** The row I registered was wrong.
2. **5 OF THE 108 SELF-CHECKS WERE `check(..., True)` — LITERAL TAUTOLOGIES**, and one of them passed
   the demonstrably wrong table above. **103 real checks, 5 that cannot fail.**
3. My previous entry said the anchor was amended with the definition. **The patch matched nothing and
   silently wrote the file unchanged.** The clauses are in a table; I matched against a plain-text
   form that does not exist in the file. **Amended now, and verified by re-reading.**

> ### **D-8. A CHECK THAT CANNOT FAIL IS NOT A CHECK.** `check(..., True)`, an assertion with no
> ### computed left-hand side, or a control that returns the same value under every input, is
> ### decoration. Here five of them let an arithmetically impossible table through.
> ### **TELL: a self-check whose expected value is a literal.**

---

## O-11 — PREDICTION REGISTERED BEFORE THE RUN

**THE CHARGE.** F-13 clause (1) says the RFP needs dynamics **outside** the detailed-balance class. But
a **strong-coupling** thermal environment does not relax to `e^{−βH_S}`; it relaxes to the **mean-force
Gibbs state** `ρ_MF = Tr_B[e^{−βH_tot}]/Z`, which depends on the **coupling operators**. If `ρ_MF` is
non-flat on the code space for a coupling of weight ≥ `d` — exactly what clause (2) **requires** — then
a **genuinely thermal environment forms a record**, and F-13 contradicts itself.

**THE SYMMETRY THAT DECIDES IT.** `H_tot = H_S + H_B + λ A⊗B` commutes with `X̄` iff `[A,X̄] = 0`, and
`{Z̄,X̄} = 0` forces `⟨Z̄⟩ = 0` whenever it does. **So the coupling must break the writer's symmetry —
which is F-8, reappearing at the level of the total Hamiltonian.**

**THE CLOSED FORM, DERIVED IN ADVANCE.** Take `A = Z̄` (weight `2 = d`), with `H_B` and `B` diagonal.
`Z̄` commutes with `H_S`, so the total blocks by `Z̄ = s = ±1`, and the bath contributes
`Z_B(s) = Σ_j e^{−β(E_j + sλb_j)}`. On the degenerate code space `ρ_MF ∝ Z_B(s)`, hence

> ### `⟨Z̄⟩ = [Z_B(+1) − Z_B(−1)] / [Z_B(+1) + Z_B(−1)]`

**PREDICTIONS:**
1. **`λ → 0` gives `⟨Z̄⟩ → 0`** for every coupling — the weak-coupling limit recovers ordinary Gibbs and
   F-9's exclusion. **This is the control that makes any nonzero a strong-coupling effect.**
2. **A weight-`d` coupling gives `⟨Z̄⟩ ≠ 0` at finite `λ`, rising at order `λ¹`**, matching the closed
   form above. **If so, F-13 clause (1) IS CONTRADICTED: a detailed-balance environment forms a record.**
3. **A weight-1 coupling gives a bias SUPPRESSED as `λ^d`** — nonzero, but at high order, because the
   system must virtually leave the code space. **If so, clause (2) SURVIVES in a scaling form** —
   weight-`d` couplings act at first order, weight-1 only at order `d`.

**WHAT EACH OUTCOME MEANS.** If 2 and 3 both hold, **F-13's clause (1) is wrong as stated and must be
replaced by a statement about coupling weight and order, not about detailed balance at all.** If 2
fails, the charge is dismissed and clause (1) stands.

---

## O-11 RESULT — **F-13 CLAUSE (1) IS CONTRADICTED. A THERMAL ENVIRONMENT FORMS A RECORD.**

`LANE_O11_MEANFORCE`. Toric code 2×2 (dim 256) + a 4-level bath, `β=2`, mean-force state
`ρ_MF = Tr_B[e^{−βH_tot}]/Z`. **This is a genuinely thermal state of the TOTAL — detailed balance with
respect to `H_tot`.**

| `λ` | `⟨Z̄⟩`, coupling `A = Z̄` (weight `2 = d`) | closed form | `A = Z_e` (weight 1) |
|---|---|---|---|
| 0.000 | 0.00000000 | 0.00000000 | 7.197e-15 |
| 0.100 | **−0.15512514** | −0.15512514 | 4.053e-15 |
| 0.400 | **−0.54832339** | −0.54832339 | −2.489e-15 |
| 0.800 | **−0.82457285** | −0.82457285 | −4.504e-15 |

**CLOSED FORM AGREEMENT `7.197e-15`.** `λ→0` control **PASSES** — weak coupling recovers ordinary
Gibbs and F-9's exclusion, so the effect is genuinely strong-coupling. Slope in `λ` = **0.9947**, as
predicted at order 1.

> ### **PREDICTION 2 CONFIRMED. F-13'S CLAUSE (1) IS WRONG: THE RFP DOES NOT NEED NON-EQUILIBRIUM DYNAMICS. THE "NON-EQUILIBRIUM" REQUIREMENT WAS AN ARTEFACT OF THE WEAK-COUPLING (DAVIES) LIMIT, NOT A FACT ABOUT RECORDS.**

### PREDICTION 3 WAS FALSIFIED — **AND IN THE PROGRAM'S FAVOUR**

I predicted weight-1 couplings would bias at order `λ^d`. **They do not bias at all.**

| all 24 weight-1 couplings, `λ = 0.8` | count | `max\|⟨Z̄⟩\|` |
|---|---|---|
| **commute** with the writer `X̄` | 20 | 7.177e-15 |
| **do NOT commute** with `X̄` (`‖[A,X̄]‖ = 32`) | **4** | **5.317e-15** |

Noise floor (no coupling at all): `1.550e-15`.

**THE FOUR THAT BREAK THE WRITER'S SYMMETRY STILL GIVE ZERO.** So **the suppression is
KNILL–LAFLAMME, not symmetry** — and **clause (2) survives in its STRONGEST form: a weight-1 coupling
produces no bias at any coupling strength, not merely a suppressed one.**

### AND A THIRD CONDITION F-13 DID NOT HAVE

| weight-2 coupling | `‖[A,X̄]‖` | `\|⟨Z̄⟩\|` |
|---|---|---|
| `Z̄` | 32.000 | **0.824573** |
| `Z̄₂` | **0.000** | **0.000000** |

**Weight `≥ d` is NECESSARY BUT NOT SUFFICIENT. The coupling must also break the symmetry generated by
the writer** — F-8, reappearing at the level of `H_tot`.

> ### **THE RFP'S REQUIREMENTS, CORRECTED:**
> ### **(1) a coupling of weight ≥ `d`, and (2) that coupling must not commute with the writer.**
> ### **NOTHING ABOUT EQUILIBRIUM. AN ORDINARY THERMAL ENVIRONMENT SUFFICES.**

### THIS DISSOLVES O-9's PREMISE

O-9 asked *"what supplies a non-local, NON-EQUILIBRIUM coupling?"* **The non-equilibrium half is gone.**
What remains is the ordinary physical question **"what supplies a coupling extended over a region at
least as large as `d`?"** — a question about environments, not a demand for exotic dynamics.

### DEFECT CAUGHT IN THE FIRST RUN

The v1 script fitted a log-log slope to the weight-1 column and its **auto-verdict announced "clause (2)
does NOT survive."** That column was **noise** — magnitude `~1e-15` with the sign oscillating — so the
slope `0.2741` was a fit to zero. **No noise floor had been established.** This is **D-8 in a second
costume: a computed verdict is not a check unless the noise floor is measured alongside it.**

---

## F-1 / T-III.6 — **THE ARROW.** PREDICTION AND IMPORT-GUARD REGISTERED BEFORE THE RUN

**WHY THIS DECIDES THE PROGRAM.** Every clause of the anchor is **time-symmetric** — `R=R†`, `R²=I`,
`[H,R]=0`, `[L_k,R]=0`, writable, protected. **Not one mentions time.** Without an arrow we have a
theory of **protected bits**, not of **records**, and the charter's own word is unearned.

### THE DESIGN PROBLEM, AND WHY THE OBVIOUS TEST IS VOID

"Run the formation backwards" does not work as stated. With coupling `A = Z̄`, **`[Z̄, H_tot] = 0`**, so
`⟨Z̄⟩` is a **constant of motion** and unitary evolution never forms anything. The mean-force state is
reached by **relaxation**, and `ρ_MF` is itself **stationary** — an equilibrium state has no arrow.
**Testing reversibility of a stationary state would have measured nothing.**

### THE TEST THAT REPLACES IT

`ρ_MF` blocks by `Z̄ = s`, with bath state `e^{−β(H_B + sλB)}/Z_B(s)` in each block. **Those are
DIFFERENT bath states.** So the bath's state depends on the record's value, and the quantity is the
**Holevo information the bath holds about the record**:

> `χ(Z̄ : B) = S(ρ_B) − Σ_s p_s S(ρ_B^s)`

**AND THE ARROW STATEMENT:** local unitaries **cannot change** `χ`. If the bath holds a copy, **no
system-only operation can unmake it.** Forming needed a coupling; **unforming needs that coupling AND
control of the bath, which the system does not have.** That asymmetry is the candidate arrow.

### **THE IMPORT GUARD — AND IT IS THE POINT OF THE LANE (D-1)**

**If `χ(O:B) > 0` for EVERY observable, this is DECOHERENCE and we have imported einselection.** The
program's concept list already contains einselection and quantum Darwinism. **A general arrow is not
ours.**

> ### **DISCRIMINATOR: does the arrow carry the RECORD'S OWN THRESHOLD?**
> ### **`χ(O:B) > 0` only for observables of weight ≥ `d` ⟹ the arrow is RECORD-LEVEL.**
> ### **`χ(O:B) > 0` for weight-1 observables too ⟹ it is ambient decoherence, and F-1 is NOT ours.**

**PREDICTIONS:**
1. `χ(Z̄:B) > 0` for a weight-`d` coupling, matching a closed form from `Z_B(±1)`.
2. `χ(Z̄:B) = 0` for a weight-1 coupling — **the bath learns nothing about the record.**
3. **Local unitaries leave `χ` exactly invariant** — measured, not asserted.
4. **THE DECIDING ONE:** sweeping observables by weight, `χ` turns on at **weight `= d`** and is **zero
   below it**. If instead low-weight observables also carry `χ`, **the arrow is imported and this lane
   returns a negative result.**

---

## F-1 / T-III.6 RESULT — **THE ARROW IS REAL AND IT CARRIES THE RECORD'S OWN THRESHOLD. IT IS NOT AMBIENT DECOHERENCE.**

`LANE_F1_ARROW`. Toric code 2×2 + 4-level bath, mean-force state, `β=2`, `λ=0.8`.

### 1–2. THE BATH HOLDS INFORMATION ABOUT THE RECORD

| coupling | weight | `‖[A,X̄]‖` | **`χ(Z̄:B)` bits** | closed form |
|---|---|---|---|---|
| `Z̄` (logical) | 2 = `d` | 32.000 | **0.11448276** | **0.11448276** |
| `Z̄₂` (logical) | 2 = `d` | **0.000** | **0.00000000** | |
| `Z_e` (single site) | 1 | 32.000 | **0.00000000** | |
| identity | 0 | 0.000 | 0.00000000 | |

Closed form **exact**. And the same two conditions as F-13/F-15 reappear: **weight ≥ `d` AND
non-commuting with the writer.**

### 3. THE IRREVERSIBILITY, MEASURED

| | |
|---|---|
| covariance instrument check | `9.992e-16` **PASS** |
| **`I(S:B)` under 12 random system-only unitaries** | **`3.686e-14` — EXACTLY INVARIANT** |
| `χ` about the *fixed* label `Z̄` | `1.145e-01` — **moves, and does** |

> **A system-only operation can MOVE which observable the bath knows about. It cannot change `I(S:B)`
> at all. THE CORRELATION IS NOT ERASABLE FROM INSIDE.**

### 4. **THE DECIDING TEST — AND THIS IS THE RESULT**

Sweeping **all** observables by weight in the same state:

| observable weight | # swept | `max χ(O:B)` |
|---|---|---|
| **1** | 24 | **0.00000000** |
| **2 = `d`** | 252 | **0.11448276** |

**AND THE DISCRIMINATION THE IMPORT GUARD WAS BUILT FOR** — from part (c):

| coupling | weight | `I(S:B)` | `χ(Z̄:B)` |
|---|---|---|---|
| `Z_e` | **1** | **0.04549256** | **0.00000000** |
| `Z̄` | 2 = `d` | 0.11448276 | 0.11448276 |

> ### **A WEIGHT-1 COUPLING DOES ENTANGLE THE ENVIRONMENT WITH THE SYSTEM — `I(S:B) = 0.045` — AND TRANSFERS **ZERO BITS ABOUT THE RECORD**.**
> ### **AMBIENT DECOHERENCE IS PRESENT AT WEIGHT 1. THE RECORD'S ARROW IS NOT. IT TURNS ON AT `d`.**

**So the arrow is not einselection wearing our vocabulary. Decoherence and the record's arrow are
separated by a measured threshold, and that threshold is the record's own.**

### THE STATEMENT, IN THE RECORD LEVEL'S OWN TERMS

> **A record is of the past because the environment holds Holevo information about it, and no
> operation the system can perform removes that. Acquiring it requires the environment to couple over
> a region at least as large as `d` — the same `d` that protects it and the same `d` that forms it.**

### WHAT IS **NOT** ESTABLISHED — stated plainly, and it keeps this PARTIAL

1. **This is an equilibrium state, not a dynamical history.** F-1 asked for *"a before with no record
   and an after with one."* **One-wayness is measured; the temporal formation was not simulated.**
2. **The bath is 4 levels.** Redundancy — many environment fragments each holding a copy, which is
   what makes a record *objective* — is **untested**.
3. **One-wayness is necessary for "of the past". Whether it is sufficient is not settled here.**

### DEFECT IN v1, CAUGHT BY ITS OWN CONTROL

v1 reported *"prediction 3 falsified — local unitaries change `χ`."* **It conjugated the observable
the wrong way (`Q†Z̄Q` where covariance needs `QZ̄Q†`), so it measured a rotated observable.** The
corrected covariance check returns `9.992e-16`. **The reported falsification was mine, not nature's.**

---

# THE MODEL — **RECORDS CONSTRUCTED FROM `(H, {L_k})` AND NOTHING ELSE**

`model/record_model.py`. The principal: *"We need a model that can be used to construct records from
first principles without importing values."*

**INPUT: a Hamiltonian and a set of Lindblad operators. NO lattice, NO gauge group, NO temperature, NO
coupling constant, NO code, NO geometry.** Every step is a registered theorem: **C-9** (clause (ii)
puts `R` in the commutant of the `*`-algebra), **C-10** (proper-subalgebra criterion), **C-11 / O-4**
(admissible flipper ⟺ `Tr(P_E R) = 0`), **C-12** (the repaired converse).

### VALIDATION — **12 PASS, 0 FAIL**, each case a registered result re-derived from first principles

| | |
|---|---|
| odd dimension ⟹ no record is ever writable (C-11 corollary) | `C³, C⁵, C⁷` → 0 records |
| O-1 gap (a): degenerate `H` + **one generic jump** kills every record | 0 over 6 draws |
| **positive control**: same `H`, **diagonal** jumps | records in all 6 |
| O-1's **trap**: `max‖P_E L P_E‖ = 0` yet **no record** | 0 records |
| **control**: return legs deleted | records exist |
| gauge carrier handed in as a bare matrix | records found |

## **C-14 — THE RECORD-COUNT LAW, FROM THE CLAUSES ALONE**

> ### `k = min over eigenspaces E of v₂(m_E)` — the **2-adic valuation** of the multiplicities

**22 spectra, 22 PASS, 0 FAIL**, including odd, non-power-of-2 and mixed multiplicities.

**THE DERIVATION IS THE CLAUSES.** A record must be non-trivial (iii) and **trace-balanced on every
eigenspace** (iv = C-11); an independent **family** must split every joint block **evenly**. Each
independent record therefore **halves every eigenspace**, so the family size is bounded by how many
times every multiplicity can be halved.

**AND THE CONTROL SHOWS IT HAS CONTENT.** The naive `floor(log₂ min m_E)` predicts `[3,3] → 1`,
`[6,6] → 2`, `[5,5] → 2`. **Measured: 0, 1, 0.** The count is set by the **valuation**, not the size.

> ### **IT DERIVES THE GAUGE RESULT WITHOUT TOPOLOGY.** The toric code's ground multiplicity is `4`,
> ### so `k = v₂(4) = 2 = 2g`. **The index law G-7 is a CONSEQUENCE on that carrier, not the source
> ### of the count.**

## **C-15 — FOUR OF THE FIVE CLAUSES ARE CARRIER-FREE. THE FIFTH IS NOT.**

Clauses **(i)–(iv) are computable from `(H,{L_k})` alone.** **Clause (v) is not** — it requires a
**locality structure**, which is carrier data and is not derivable from the pair. The model **refuses
to guess it** and raises rather than supplying a default.

**Any claim resting on (v) therefore inherits a carrier.** That is the precise scope boundary of the
whole program, and it is now enforced in code rather than remembered.

## MULTI-RECORD — **PF-7 SUBSTANTIALLY ADVANCED**

| carrier | records | **independent family** | `log₂ dim` | **independently writable** |
|---|---|---|---|---|
| `C⁴` | 3 | **2** | 2 | **2 of 2** |
| `C⁸` | 35 | **3** | 3 | **3 of 3** |
| `C¹⁶` | 6435 | **4** | 4 | **4 of 4** |

**F₂-independence of sign vectors is the WRONG notion** — `k` independent bits need `2^k` joint
eigenspaces. The right criterion is that a new record **splits every existing joint block evenly**,
and under it **every member of the family is independently writable: one record can be flipped without
disturbing any other.**

**DEFECTS CAUGHT DURING THE BUILD, all by the validation:** the writer test was over-strict (asked one
unitary to fix 35 records at once); the XOR basis stored **unreduced** vectors so nothing ever reduced
to zero; and F₂-independence gave `n−2` where the answer is `log₂ n`.

---

## PF-3 — **DEF-A SURVIVES PART A UNIVERSALLY. PART B FOUND AN ERROR IN G-11 INSTEAD.**

### PART A — THE BALANCE LEMMA IS CARRIER-FREE

Tested **through the model**, so no carrier is involved at all: for every spectrum tried
(`[4] [8] [4,4] [2,2] [6,2] [4,2] [2,2,2,2] [8,4] [4,4,4]`), **every record the model builds is
balanced on every eigenspace, and an admissible writer is constructed and verified for every one.**

**POSITIVE CONTROL, and it fires:** an **unbalanced** involution (`Tr R = +2`) has **no** flipper —
best `‖U†RU + R‖` over **4000** random unitaries is **2.0000**, exactly the proved bound.

> **Clause (iv) under DEF-A ⟺ `Tr(P_E R) = 0` is UNIVERSAL, not a fact about the toric code.**

### PART B — **VOID AS A TEST OF DEF-A, AND IT INDICTS G-11 INSTEAD**

On a **bouquet of two triangles** (pinch-point non-manifold, dim 64), contractible regions = forests:

| | |
|---|---|
| any-unitary flippers inside a contractible region (**control**) | **1830** |
| **admissible** flippers inside a contractible region | **171** |

**That reads as DEF-A failing. It is not.** The carrier itself fails clause (v):

| carrier | links | **Z-systole** | **X-cosystole** | **d = min** |
|---|---|---|---|---|
| torus 2×2 | 8 | 2 | 2 | **2** |
| torus 3×3 | 18 | 3 | 3 | **3** |
| **bouquet of 2 triangles** | 6 | 3 | **1** | **1** |
| **bouquet of 3 triangles** | 9 | 3 | **1** | **1** |

## **ERRATUM TO G-11 — ITS DISTANCE COLUMN REPORTED THE SYSTOLE, NOT THE CODE DISTANCE**

**G-11 registered `d = 3,3,3` for the bouquet family. The true distance is `1`.** The bouquet has no
2-cells, so every single-edge `X` is a non-trivial `X`-logical — **cosystole 1**. G-12 had already
stated that **R3 needs two numbers**; G-11's own table was never corrected to use them.

**AND THE CORRECTION STRENGTHENS G-11's POINT.** The bouquet does not have *"unbounded capacity with
fixed protection."* It has **unbounded capacity with NO protection at all.** Capacity and protection
are independent — which is what G-11 was for, now stated correctly.

**PF-3 STATUS: part A closed, part B still owed.** The test needs a **non-manifold carrier with BOTH
distances ≥ 2**; the one chosen was invalid, and the run said so rather than reporting a verdict.

---

## PF-2 — PREDICTION REGISTERED BEFORE THE RUN

F-1 is PARTIAL for two stated reasons: it measured one-wayness on an **equilibrium** state, and
**redundancy** was untested (O-13). Both are addressed dynamically here.

### THE DESIGN POINT THAT MAKES A DYNAMICAL TEST POSSIBLE

With coupling `A = Z̄`, `[Z̄, H_tot] = 0`, so **`⟨Z̄⟩` is a constant of motion** — the record's *value*
never changes under unitary evolution. **That is not an obstacle, because forming a record is not the
record changing value. It is the ENVIRONMENT COMING TO HOLD INFORMATION ABOUT IT.** So the observable
is `χ(Z̄:B)(t)`, which starts at **exactly 0** for a product state and can grow while `⟨Z̄⟩` is fixed.

> **BEFORE = no record information anywhere. AFTER = the environment holds it. That is the history
> F-1 asked for, and it is measurable.**

**PREDICTIONS:**
1. `χ(Z̄:B)(t)` grows from **exactly 0** at `t=0` while `⟨Z̄⟩` stays constant — **the before/after.**
2. **CONTROL: full time reversal returns `χ → 0`.** Unitary evolution is exactly reversible, so if the
   instrument reported irreversibility here it would be manufacturing it. **The arrow must NOT show up
   in the closed dynamics.**
3. **REDUNDANCY (O-13): each bath fragment independently holds `χ > 0`** — many fragments each with a
   copy, which is what makes a record objective instead of merely correlated.
4. **Redundancy carries the record's threshold: a weight-1 coupling gives every fragment ZERO** —
   F-18 extended from the whole bath to its parts.

**WHAT THE ARROW THEN IS, STATED HONESTLY IN ADVANCE:** if 1–3 hold and 2 confirms the closed dynamics
is reversible, the arrow is **RELATIVE, not absolute** — one-way with respect to what the *system* can
do (F-19: `I(S:B)` is invariant under every system-only operation), while the joint evolution remains
reversible. **That is a weaker and more honest claim than "time has a direction", and it is the one
the measurements can support.**

---

## PF-2 RESULT — **THE HISTORY IS REAL, THE CLOSED DYNAMICS IS REVERSIBLE, AND THE RECORD IS REDUNDANT**

`LANE_PF2_DYNAMICAL`. Toric code 2×2 + a **3-qubit** bath, so the bath **has fragments**. Initial
state is a **product**, so `χ = 0` exactly at `t=0`.

### 1. THE BEFORE/AFTER F-1 ASKED FOR

| `t` | `⟨Z̄⟩` | **`χ(Z̄:B)` bits** | `I(S:B)` |
|---|---|---|---|
| 0.00 | −0.000000 | **0.00000000** | −0.00000000 |
| 0.50 | −0.000000 | 0.81447230 | 0.81447230 |
| 1.00 | −0.000000 | **0.97527192** | 0.97527192 |
| 4.00 | −0.000000 | 0.90811968 | 0.90811968 |

> **`⟨Z̄⟩` is EXACTLY CONSTANT throughout — the record's value never changes. What changes is that the
> environment comes to hold it.** Before: no record information anywhere. After: ~1 bit in the bath.
> **That is the history, and forming a record was never the record changing value.**

### 2. THE CONTROL — **AND IT MUST PASS, OR THE RESULT IS MANUFACTURED**

| | |
|---|---|
| `χ` at `t = +4.0` | 0.90811968 |
| `χ` at `t = 0` | **0.00000000** |
| `χ` at `t = −4.0` | **0.90811968** — equal to `t=+4` |

**The closed dynamics is exactly reversible and time-symmetric.** Had the instrument reported
irreversibility here it would have been inventing it.

### 3. REDUNDANCY — **O-13 CLOSED**

| coupling | weight | whole bath | frag {0} | frag {1} | frag {2} |
|---|---|---|---|---|---|
| `Z̄` (logical) | 2 = `d` | **0.90811968** | **0.789366** | 0.048377 | **0.678602** |
| `Z_e` (single site) | 1 | **0.00000000** | 0.000000 | 0.000000 | 0.000000 |

**Fragments independently hold the record — two of three carry most of a bit each.** Separate observers
can each learn it without communicating, which is what makes a record **objective** and not merely
correlated. **And redundancy carries the record's threshold: a weight-1 coupling gives EXACTLY ZERO to
the whole bath AND to every fragment.** F-18 extends from the bath to its parts.

### **THE ARROW, STATED AT THE STRENGTH THE MEASUREMENTS SUPPORT**

> **It is RELATIVE, not absolute.** The joint evolution is exactly reversible (control above). The
> one-wayness is **with respect to what the SYSTEM can do**: `I(S:B)` is invariant under every
> system-only operation (F-19), so nothing the system does removes the environment's copy — and by the
> redundancy above, there are several copies to remove.
> **This is weaker than "time has a direction" and it is what was actually measured.**

### TWO LIMITS, STATED

1. **`χ(t)` is NON-MONOTONIC** — 0.975 at `t=1`, 0.787 at `t=2`, 0.908 at `t=4`. **Partial recurrence,
   because a 3-qubit bath is small.** A macroscopic environment would not recur on any relevant scale,
   but that is asserted here, not measured.
2. **Redundancy is UNEVEN** — 0.789, 0.048, 0.679. The fragments have different energies and acquire
   information at different rates. **Redundancy is present; uniform redundancy is not claimed.**

---

## D-9 / F-20 ERRATUM — **DO NOT GRADE A FINDING AGAINST AN EXTERNAL STANDARD. STATE THE MECHANISM.**

The principal, on the registrar's *"that's weaker than 'time has a direction'"*: **"What does this mean
'weaker'???? We just need to know how it works."**

**"Weaker" compares our result to a yardstick nobody asked for.** The charter asks how records form.
*"Time has a direction"* is a cosmological question the program never posed, and ranking against it is
**D-1 applied to framing instead of to physics** — an imported measure used as a grade.

> **D-9. A RESULT IS DESCRIBED BY ITS MECHANISM, NEVER RANKED AGAINST AN EXTERNAL STANDARD.**
> **TELL:** the words *weaker*, *stronger*, *only*, *merely*, *falls short of*, or any comparison to a
> claim the program did not make.

### F-20 RESTATED — **THE MECHANISM, WITH NOTHING GRADED**

**1. The coupling makes the environment's evolution CONDITIONAL on the record.**
`H_tot = H_S + H_B + λ Z̄ ⊗ ΣX_j`. The bath evolves under `H_B + λΣX_j` when `Z̄ = +1` and under
`H_B − λΣX_j` when `Z̄ = −1`. **Two different bath Hamiltonians, selected by the record.**

**2. The two branches drive the bath to different states. That divergence IS the copy.**
`χ` measures exactly how far apart they are: `0.00000000` at `t=0`, `0.97527192` at `t=1`.

**3. The record's value never changes — it is being READ, not written.**
`[Z̄, H_tot] = 0`, so `⟨Z̄⟩` is exactly constant. **Every bath degree of freedom reads the same bit
and none of them can alter it.**

**4. Several copies form because the coupling touches several bath degrees of freedom.**
Each qubit's evolution is separately conditioned, so each separately diverges: `0.789 / 0.048 / 0.679`
bits. **Redundancy is not an extra property. It is what happens when more than one thing is coupled.**

**5. Only a weight-≥`d` operator can make the environment's evolution conditional at all.**
By Knill–Laflamme a weight-`<d` operator acts as a **scalar** on the code space, so it takes the same
value on both branches, so the bath's Hamiltonian is the **same** either way, so **nothing diverges and
no copy forms** — measured as exactly `0.00000000`, whole bath and every fragment.
**The threshold is `d` because `d` is the point at which an operator can tell the record's two values
apart.**

**6. The system cannot undo it because the system's operators do not act on the environment.**
`I(S:B)` is invariant under every system-only unitary (`3.686e-14`). Undoing the divergence means
running the bath's evolution backwards, which is not an operation the system has.

> ### **THAT IS HOW IT WORKS.** A record forms when an operator large enough to distinguish its values
> ### makes the environment's evolution depend on which value it has, so the environment falls into a
> ### different state for each — in every degree of freedom the coupling reaches, and irreversibly
> ### from the system's side, because the system has no operators there.

---

## PF-5 / O-9 — PREDICTION REGISTERED BEFORE THE RUN

**THE CHARGE.** Formation needs a coupling of weight ≥ `d` (F-13). **Physical environments couple
LOCALLY** — the standard model of an environment is `H_int = Σ_i λ_i A_i ⊗ B_i` with every `A_i` acting
on one site. **If only extended couplings form records, records do not form in nature**, and the whole
process is proved conditional on something the world does not supply.

**THE RESOLUTION I EXPECT, AND IT IS ALREADY IMPLIED BY C-13.** Clause (v) forbids a **single**
contractible operation. It says nothing about **products**, and C-13 recorded that *products of
contractible operations DO reach the record* — that is Theorem D. **A sum of local couplings is not one
weight-1 operator; at order `d` in `λ` its terms act together and reach the record.**

**PREDICTIONS — three couplings, one carrier:**
1. **A SINGLE local term**, `λ Z_e ⊗ X_0`: `χ = 0` at **every** `λ`. Powers of one weight-1 operator
   are `I` or `Z_e`; they never reach the logical. **This is the control.**
2. **A SUM of local terms**, `λ Σ_l Z_l ⊗ X_{l mod 3}`: **`χ > 0`**, suppressed — log-log slope in `λ`
   of order **`2d`** (the amplitude to reach the record is `~λ^d`, and `χ` is second order in it).
3. **A weight-`d` coupling**, `λ Z̄ ⊗ ΣX_j`: `χ > 0` at **first** order, slope ~2.

**IF 1–3 HOLD, PF-5 IS ANSWERED AND O-9's PREMISE DISSOLVES.** The world does not need to supply an
exotic extended coupling. **An ordinary local environment forms records, at order `λ^d`** — so the same
`d` that protects the record, gates its formation, and sets the environment's threshold also **sets how
slowly it forms.** That is one quantity doing four jobs, and it is measurable.

**IF 2 RETURNS ZERO,** local environments genuinely cannot form records, O-9 stands as a real
obstruction, and the process is conditional on an input nothing supplies.

---

## PF-5 / O-9 RESULT — **AN ORDINARY LOCAL ENVIRONMENT DOES FORM RECORDS. THE INPUT IS SUPPLIED.**

`LANE_PF5_LOCALBATH`. Toric code 2×2 + 3-qubit bath, unitary from a product state, `t = 4.0`.
Noise floor `8.882e-16`.

| `λ` | **1. SINGLE local term** | **2. SUM of local terms** | **3. weight-`d` coupling** |
|---|---|---|---|
| 0.020 | 1.221e-15 | 0.00000031 | 0.00224457 |
| 0.100 | 0.000e+00 | 0.00016142 | 0.05127919 |
| 0.400 | 0.000e+00 | 0.01906127 | 0.47151593 |
| **log-log slope in `λ`** | **exactly zero** | **3.8988** *(predicted `2d = 4`)* | **1.9457** *(predicted 2)* |

### THE DISCRIMINATOR IS THE WHOLE POINT

**One local term gives EXACTLY ZERO at every coupling strength.** Powers of a single weight-1 operator
are `I` or that operator — **they never reach the logical, at any order.**
**A SUM of local terms gives `λ^{2d}`.** You need **`d` different local terms acting together**.

> ### **THAT IS C-13 MEASURED DYNAMICALLY.** Clause (v) forbids a *single* contractible operation;
> ### **products of them DO reach the record**, and here is the rate.

### O-9's PREMISE IS DISSOLVED

O-9 asked *"what supplies a coupling extended over a region of size ≥ `d`?"* **Nothing has to.** The
standard model of an environment — `Σ_i λ_i A_i ⊗ B_i`, every term on one site — **forms records
already.** What it costs is **suppression by `λ^{2d}`.**

> ### **AND THE SAME `d` NOW DOES FOUR JOBS, ALL MEASURED:**
> | | |
> |---|---|
> | **protects** the record | splitting `~ ε^d` (Thm D, slope 2.000) |
> | **gates formation** | threshold `= d` (F-11, six codes, `d = 1,2,3`) |
> | **gates what the environment can learn** | `χ` turns on at weight `d` (F-17, F-22) |
> | **sets how slowly a local environment forms it** | `χ ~ λ^{2d}` (here, slope 3.8988) |
>
> **One quantity, four roles. None of them was put in by hand.**

### **AND IT IS A CANDIDATE FOR PF-6 — THE FIRST ONE THE PROGRAM HAS HAD**

`X-4`, `T-VI.3` and `T-VI.4` have stood at **BLOCKED, "none identified"** since they were written.
**`χ ~ λ^{2d}` is quantitative, is about ordinary local environments, and involves only codes and baths
— objects that exist on hardware.** A record of distance `d` is **exponentially slow in `d`** to form.
Registered as the first candidate; **whether it distinguishes this account from any other is not yet
established and PF-6 stays open.**

---

## D-8, THIRD INSTANCE — **IN THE REPRODUCTION HARNESS ITSELF**

The first full-corpus run from a snapshot copy failed, and **both failures are D-8**:

1. **`ROOT` was derived from `$BASH_SOURCE`.** A copy in `/tmp` resolved `ROOT` to `/`, so the run
   `cd`'d to the filesystem root, found no lanes, and reported *"no sealed output — SKIP"* for
   everything. **It looked like a clean run over an empty corpus.** Fixed: `WAC_ROOT` override, and the
   script now **refuses to start** unless it can see `CORE_FRAMEWORK_V001.md`.
2. **THE GRID CHECK ANNOUNCED SUCCESS WITH ITS INPUTS MISSING.** `shasum` failed on both sides, both
   variables were the empty string, `"" = ""` compared true, and the harness printed *"regenerating the
   grid reproduces it byte-for-byte."* **A check that passes when the thing it checks is absent.**
   Fixed: an empty hash is now a failure.

**The verification harness had the exact defect it was built to catch.** Recorded because D-8 has now
fired three times — `check(..., True)` in the O-4 lane, a log-log slope fitted to a `1e-15` column in
O-11, and here.

---

# PF-6 — **ANSWERED NO. NOTHING IN THIS ACCOUNT IS UNPREDICTED BY A RIVAL, AND TWO REGISTERED CLAIMS ARE FALSE.**

Six rival accounts, every claimed difference adversarially adjudicated. **The deflationary lens won.**

## WHAT IS NOT OURS — the attribution, in full

| our result | whose it already is |
|---|---|
| formation threshold `= d` | **Knill–Laflamme** (PRA 55, 900, 1997) + Bravyi–Terhal cleaning lemma. **It is the DEFINITION of `d`** |
| protection `ε^d` | **Bravyi–Hastings–Michalakis**, J. Math. Phys. 51, 093512 (2010) |
| `χ` exactly 0 below `d`, non-zero at `d` | **Cleve–Gottesman–Lo** (1999); and now inside quantum Darwinism itself — **Girard–Cheng–Cao, arXiv:2606.06588, Thm 4** |
| weight-1 entangles but transfers 0 record bits | **information–disturbance**, Schumacher–Nielsen (1996) |
| redundancy across fragments | **quantum Darwinism** (Zurek, Zwolak–Zurek) + GCC Thm 4 |
| `χ ~ λ^{2d}` | `d`-th order degenerate perturbation theory, squared |
| a single local term gives exactly 0 at all orders | **group theory** — powers of one weight-1 Pauli are `I` or itself. **Algebra, not measurement** |
| `I(S:B)` invariant under system-only unitaries | mutual information is invariant under local unitaries. **Arithmetic** |
| clause (v)'s topological restriction | **TQO-1**, Bravyi–Hastings–Michalakis; stated in Kitaev 2003 |

> ### **"ONE QUANTITY, FOUR ROLES" IS ONE THEOREM READ FOUR TIMES. It is not four coincidences, and reporting the convergence is a check that cannot fail. F-24 IS WITHDRAWN.**

## **D-10 — A VERIFICATION WITH NO FAILING BRANCH IS AN INSTRUMENT CHECK, NOT A RESULT**

**`threshold = d` was verified on six codes at three distances — and `threshold = d` IS the definition
of `d`.** The verification had no branch on which it could have come out otherwise. **It confirmed the
instrument, not the account.**
**TELL:** a "verification" whose negation would be a contradiction in terms.

## THREE REGISTERED CLAIMS ARE FALSE OR MISSCOPED

### **F-25 WITHDRAWN — the eleventh withdrawn claim.** The exponent is `2n*`, not `2d`

`n*` = the minimum number of the environment's **available** local terms whose product acts
non-scalar on the code space. On `[[5,1,3]]` with `Z`-only couplings the measured slope is
**9.4619 → 9.8435 → 9.9612 → 9.9966 → 10 = 2n*`**, against `2d = 6`. `[[4,2,2]]` control: 3.9854 → 4.

**THE CAN-FAIL CHECK THAT DECIDES IT:** on the *same* code and estimator, widening the single-site set
from `{Z}` to `{X,Y,Z}` moves the slope to **5.9078 → 5.6933 → 6**, while `{Z}` stays at 10.
**The exponent tracks the COUPLING ALGEBRA, not the code.**

**And our own file closes the escape:** `LANE_PF5_LOCALBATH/pf5_localbath.py:38` uses a `Z`-type,
record-commuting sum and its own docstring calls it *"an ORDINARY LOCAL environment."*

### **C-14 IS FALSE AS STATED.** Verified counterexample

`model/count_law.py` only ever tested the law with an **empty noise set**, so *"from the spectrum
alone"* was never exercised against a non-trivial commutant.

| collective decoherence, `H = J²`, `L = {Jx,Jy,Jz}` | multiplicities | `min v₂(m_E)` | **model `k`** |
|---|---|---|---|
| **n = 3** | `[4,4]` | **2** | **0** |

**C-14 predicts 2. The truth is 0.** And these are **noiseless subsystems built and operated
experimentally** — Kwiat et al. (2000), Kielpinski et al. (2001), Viola et al. (2001).
**C-14 must be restricted to empty `L`, or restated in terms of the minimal projections of `A′`** —
which is what the model actually computes.

### THE PROTECTION LAW IS RESCOPED

`ε^d` holds for a **generic** single-site perturbation — which is what `LANE_O23_SPLITTING` actually
measured (3.0000 on `[[5,1,3]]` and Steane). Under a **`Z`-only** perturbation the slope is
**5.0001 = n\***. **The lane is right; the unqualified verbal form "a local perturbation splits as
`ε^d`" is not.**

### PF-5's EXPONENT NEEDS ITS BATH PREMISE NAMED

`slope(χ)` is **2.0064** at bath purity `q=0` and **3.9665** at `q=0.02`, while the amplitude-level
`slope(D)` holds at **1.9987–1.9992** throughout. **The factor of two is set by how the environment is
prepared. The record-intrinsic exponent is the amplitude exponent.**

## X-4, T-VI.3, T-VI.4 — **THEY DO NOT MOVE**

All three stay **BLOCKED**. **PF-6 is answered NO, and what it gains is an adjudicated reason in place
of silence.** Every arm run so far is closed unitary evolution with a small bath; **the one untested
place where amplitudes and rates need not stand in the squared relation is a genuinely dissipative
bath.**

---

## PF-6 ERRATUM — **THE REGISTRAR APPLIED A TEST THE REGISTER ITSELF REJECTS**

The principal: *"it's expected that we will use conventional physics… What physics has not accomplished
is to describe how those discoveries and observations combine to create records."*

**`STATUS_V001.md` section C already says this, and I ignored it:**

> **"THE TEST APPLIED: *does the assembly answer an open question?* — NOT *can the parts be named?*
> Naming parts does not make an assembly a restatement."**

**PF-6's finding stands: no measurement distinguishes this account from a rival, so X-4, T-VI.3 and
T-VI.4 remain BLOCKED.** That is a real limit on **empirical contact** and nothing here softens it.

**What does NOT follow is the conclusion I drew from it.** I wrote that the result *"materially reduces
what the program can claim as its own."* **It does not.** The charter never asked for a new physical
law. It asks **how EM, gravity and alpha COMBINE to form records** — and every component of a correct
assembly *should* have a named owner. **Finding that each part is known is what a right answer looks
like, not evidence against one.**

> ### **THE CLAIM WAS NEVER "A NEW LAW". IT IS "A PROCESS NOBODY HAS DESCRIBED".**
> ### **PF-6 tested the first and found nothing. It never tested the second.**

**WHAT SURVIVES PF-6 UNTOUCHED:** the assembly itself — that a record is a trace-balanced projection in
the commutant (C-12), written by an operation admissible only as a whole (C-13), carried by an EM
holonomy that is also its writer and its minimal forming coupling (A-EM3), formed when a coupling makes
the environment's evolution conditional on it (F-20), with the environment's copy unremovable from
inside (F-19). **No cited rival assembles these into a formation process; each owns one part.**

**AND THE THREE FALSE CLAIMS STAY FALSE.** F-25, C-14 and the protection scope were genuine errors,
caught by genuine counterexamples, and this erratum does not touch them.

**D-9 fired here and I missed it on myself:** *"materially reduces what the program can claim"* is a
**grade**, not a mechanism.

---

## O-16 — PREDICTION REGISTERED BEFORE THE RUN

**THE ONE UNTESTED ARM.** Every arm so far is **closed unitary evolution with a small bath**, where
information measures are the square of an amplitude by construction. **A genuinely dissipative
(Lindblad) bath is the one place amplitudes and rates need not stand in that relation.**

**THE MECHANISM THAT MAKES ME EXPECT A DIFFERENCE.** For a Pauli jump operator `L = P_i` with
`{P_i, Z̄} = 0`, the Lindblad term gives `Tr(Z̄ · (P_i ρ P_i − ρ)) = −2 Tr(Z̄ρ)` — **first order in the
rate `γ`, with no `d` in it at all.** A single-site jump decays the record immediately, where in the
unitary arm a single local term gave **exactly zero at every order**.

**PREDICTIONS:**
1. **The record's decay exponent under single-site Lindblad jumps is 2 in `λ` (first order in
   `γ = λ²`), INDEPENDENT of `d`.**
2. **The static splitting exponent under the same operator set is `n*`** — as PF-6 established.
3. **Therefore the two exponents DIFFER, and the rival's squared rule does not carry over.**

**IF 1–3 HOLD, THE FINDING IS PHYSICAL AND SHARP:** **distance protects against STATIC perturbation and
does NOT protect against DISSIPATION.** Uncorrected, a distance-`d` code loses its record at the
physical rate — which is why quantum error correction needs an **agent actively correcting**, and this
account has none.

**IF THE EXPONENTS MATCH,** the rival's rule survives the dissipative arm too, O-16 closes negative,
and the account has no arm left in which it differs from perturbation theory.

---

## O-16 RESULT — **THE PREDICTION HOLDS. DISTANCE PROTECTS AGAINST STATIC PERTURBATION AND NOT AGAINST DISSIPATION.**

`LANE_O16_DISSIPATIVE`. Two codes whose self-checks passed; a third was **voided by its own gate**.

| code | coupling set | **decay exponent** (Lindblad) | **splitting exponent** (static) | |
|---|---|---|---|---|
| **[[5,1,3]]** `d=3`, non-CSS | `{Z}` | **0 exactly** | **4.9942** `= n*` | |
| | `{X,Y,Z}` | **2.0000** | **2.9979** `= d` | **DIFFER** |
| **[[7,1,3]]** Steane `d=3`, CSS | `{Z}` | **0 exactly** | 3.0064 | |
| | `{X,Y,Z}` | **2.0000** | **2.9835** `= d` | **DIFFER** |

**`2.0000` on BOTH `d=3` codes — the decay exponent contains no `d` at all**, exactly as the mechanism
predicted: for a jump `L = P_i` with `{P_i, Z̄} = 0`, `Tr(Z̄(P_iρP_i − ρ)) = −2Tr(Z̄ρ)`, first order in `γ`.

> ### **DISTANCE PROTECTS AGAINST STATIC PERTURBATION (`λ^d`) AND DOES NOT PROTECT AGAINST DISSIPATION (`λ²`, independent of `d`).**

### **AND THIS IS NOT OURS EITHER — attribution stated up front (D-10, PF-6)**

**It is standard QEC that an UNCORRECTED code decays at the physical error rate.** `d` bounds what
active correction *can* fix; it protects nothing on its own. A syndrome-extracting, correcting **agent**
is what converts distance into protection.

> ### **THIS ACCOUNT HAS NO AGENT. Nothing in it extracts a syndrome or corrects anything.**
> ### **So the protection the program has been reporting — Theorem D's `ε^d` — is protection against
> ### STATIC PERTURBATION ONLY. Against a real dissipative environment the record decays at `γ`.**

### **O-17 — THE TENSION THIS CREATES, AND IT IS THE SHARPEST OPEN ITEM ON THE BOARD**

| | order in `λ` |
|---|---|
| the environment **learns** the record | `2n*` (PF-5, measured 9.9966 → 10 on `[[5,1,3]]`) |
| the environment **destroys** the record | **2** (here, measured 2.0000) |

> ### **THE RECORD IS DESTROYED AT ORDER 2 AND RECORDED AT ORDER `2n*`. FOR `n* > 1` IT IS ERASED FASTER THAN IT IS WRITTEN.**

The two numbers come from different arms — one unitary-with-small-bath, one Lindblad — so this is a
**tension to resolve, not yet a contradiction**. But it is aimed straight at the formation account:
**an ordinary dissipative environment may destroy a record before it can hold one.**

### THE GATE DID ITS JOB — THIRD NOMINATION ERROR CAUGHT

`[[4,2,2]]`'s arm was **voided by its own self-check**: the nominated `Z̄ = ZZII` and `X̄ = XXII`
**commute** (`‖{Z̄,X̄}‖ = 8.00`), so they are not a conjugate pair and nothing downstream was computed.
**Third time a nominated logical has been caught this session** — W-62's original defect, F-7's first
build, and now this. **In every case the check fired before a number was read.**

---

## O-17 RESOLVED — **THE TWO ARMS RAN ON TWO DIFFERENT `(H,{L_k})` PAIRS, AND ONLY ONE HAS A RECORD**

`LANE_O17_TENSION`, carrier `[[5,1,3]]`.

| environment | `max‖[L_k, Z̄]‖` | clause (ii) | `dim A′` | `dim Herm(A′)` | record possible? |
|---|---|---|---|---|---|
| PF-5's single-site `{Z}` | **0.0000** | **HOLDS** | 2 | 2 | **yes** |
| O-16's single-site `{X,Y,Z}` | **11.3137** | **VIOLATED** | **1** | **1** | **NO — scalars only** |
| bare code, no environment | — | — | 280 | 280 | yes |

> ### **O-16 MEASURED THE DECAY OF AN OBJECT THAT IS NOT A RECORD FOR THAT ENVIRONMENT.**
> ### **The tension was a comparison across coupling classes, not a contradiction in the account.**

**AND THE RESOLUTION WAS ALREADY IN THE ANCHOR.** Clause (ii) is `[L_k, R] = 0`. It says exactly this
— and it says it as a **condition on the environment**, not on the record. **O-1's `400/400` result
(a generic jump set kills every record) is confirmed here on a second carrier by an independent route:
the Hermitian commutant collapses to dimension 1.**

### WHAT THIS COSTS THE ACCOUNT, STATED PLAINLY

**The environment that forms a record must be one for which the record exists** — its couplings must
commute with it. **That is a restriction on the environment, not a free condition, and O-16 showed the
generic environment does not satisfy it.** The formation story therefore requires **structured noise**,
and nothing in the program yet says why the world's noise should be structured that way.
**Registered as O-18.**

### TWO METHOD DEFECTS IN OUR OWN TOOLING

1. **`record_model.py` builds the `*`-algebra when the commutant needs only the generators.**
   **The commutant of a SET equals the commutant of the algebra it generates.** The build is wasted
   work and it is why the first attempt hit the enumeration cap at 32 minimal projections.
2. **Forming the stacked commutator map directly (16384×1024) timed the second attempt out.**
   `M†M` is `1024×1024` and has the same rank. **Fixed; both recorded so the model can be corrected.**

---

## O-18 — PREDICTION REGISTERED BEFORE THE RUN

**THE QUESTION.** A record exists only where the environment's couplings commute with it (C-17), and
the **generic** environment's do not. **Why should the world's noise be the right shape?**

**THE CANDIDATE ANSWER, AND IT IS EM'S OWN.** The structure is not an extra assumption. **A-EM
established that EM supplies both boundary maps of the complex — `∂₁` IS the Gauss law.** An
environment coupling to a gauge field must couple **gauge-invariantly**, i.e. commute with every `A_v`.
**Gauge invariance is not a restriction we impose on the noise. It is what "the environment couples to
the EM field" means.**

**WHAT GAUGE-INVARIANT OPERATORS ARE, ON THIS CARRIER.** A `Z`-type operator commutes with every `A_v`
**iff its support is a CYCLE**. Contractible cycles are products of plaquettes — **stabilisers**.
Non-contractible cycles are **logicals**. There is nothing else.

**PREDICTIONS:**
1. **Gauge-invariant LOCAL noise lies in the stabiliser group and acts TRIVIALLY on the code space.**
2. **A record therefore exists under it and is untouched** — the Hermitian commutant stays > 1.
3. **AND THE SAME FACT PREVENTS FORMATION: `χ = 0` under gauge-invariant local noise.** An operator
   that acts trivially cannot make the environment's evolution conditional on the record (F-22).
4. **PF-5's coupling `Σ_l Z_l` is NOT gauge-invariant term by term** — a single `Z_l` anticommutes with
   the two `A_v` at its endpoints. So the mechanism that formed a record in PF-5 **is unavailable to a
   gauge-invariantly-coupled environment.**

> ### **IF 1–4 HOLD, GAUGE INVARIANCE PROTECTS THE RECORD PERFECTLY AND PREVENTS ITS FORMATION EQUALLY PERFECTLY, AND THAT IS THE REAL SHAPE OF O-18.**

**IF 3 FAILS** — if gauge-invariant local noise does form a record — then EM's own constraint supplies
exactly the structured noise the account needs, and O-18 closes affirmatively.

---

## O-18 RESULT — **GAUGE INVARIANCE AND LOCALITY TOGETHER FORBID FORMATION. ONE MUST BE GIVEN UP.**

`LANE_O18_GAUGENOISE`, toric 2×2. Noise floor `8.882e-16`.

| coupling | gauge-invariant? | local? | **`χ(Z̄:B)` at `λ=0.8`** |
|---|---|---|---|
| **plaquettes** | **yes** | **yes** | **0.00000000** |
| PF-5's `Σ_l Z_l` | **no** (`32.0000`) | yes | 0.21703158 |
| `Z̄` | yes | **no** | 0.90811968 |

> ### **GAUGE-INVARIANT *AND* LOCAL ⟹ NO FORMATION, EXACTLY. To form a record the environment must
> ### give up ONE OF THEM.**

**PF-5's mechanism gives up gauge invariance.** A single `Z_l` fails `‖[Z_l, A_v]‖ = 32.0000`. **The
coupling that formed a record in PF-5 is not one a gauge-invariantly-coupled environment can have.**

### PREDICTION 1 WAS TOO STRONG, AND THE DATA SAYS SO

I predicted gauge-invariant local operators all lie in the stabiliser group. **They do not.**

| weight | Paulis | gauge-invariant | **of those, trivial on the code space** |
|---|---|---|---|
| **1** | 24 | 8 | **8 of 8** |
| **2 = `d`** | 252 | 44 | **36 of 44** — **8 are NOT** |
| 3 | 1512 | 152 | 144 of 152 |
| 4 | 5670 | 662 | 570 of 662 |

**Gauge-invariant operators of weight `< d` are trivial (8 of 8). At weight `≥ d` they can be
LOGICALS** — a minimal non-contractible cycle is gauge-invariant, being a cycle. **On this 2×2 lattice
`d = 2`, so the "non-local" operator has weight 2 and looks local; that is a small-lattice artefact.**

> ### **THE CORRECTED STATEMENT: gauge invariance plus a locality bound BELOW `d` forbids formation.
> ### As the carrier grows, `d` grows, so any FIXED locality bound eventually forbids it.**

### **O-20 — WHAT THIS COSTS, AND IT IS THE SHARPEST THING ON THE BOARD**

**The account's formation story needs an environment that couples to the EM field either
NON-GAUGE-INVARIANTLY or NON-LOCALLY.** A-EM established that EM supplies the Gauss law itself, so a
non-gauge-invariant coupling is **coupling to something that is not the gauge field**.
**Neither option is free, and the program has no argument for either.**

---

## O-20 REFRAMED BY THE PRINCIPAL — **"GRAVITY?"**

The principal, on *"a non-gauge-invariant coupling is coupling to something that is not the gauge
field"*: **"Gravity?"**

**THE TABLE ALREADY SAYS SO AND I READ IT WRONG.** In O-18's run the coupling that formed a record
best — `Z̄`, `χ = 0.90811968` — **IS gauge-invariant** (`‖[Z̄, A_v]‖ = 0.0000`). What it gives up is
**locality**. And `Z̄` is a **non-contractible cycle**: an `H₁` object. **That is Γ.**

**So the dilemma I registered was mis-stated.** It is not "give up gauge invariance or locality." The
plaquette coupling that failed is a **boundary** — an element of `B₁`. The coupling that succeeded is
**not a boundary** — an element of `Z₁ \ B₁`. **Both are gauge-invariant. They differ in HOMOLOGY
CLASS, which is exactly the quotient `Z₁/B₁` the program calls Γ.**

> ### **PREDICTION, REGISTERED BEFORE THE RUN: `χ` IS A FUNCTION OF THE COUPLING'S HOMOLOGY CLASS AND
> ### OF NOTHING ELSE — not of its weight, not of its locality.**
> ### **`χ = 0` for every coupling in `B₁`. `χ > 0` for every coupling in `Z₁ \ B₁`.**

**IF IT HOLDS, O-20 IS ANSWERED IN THE CHARTER'S OWN TERMS:** EM supplies the carrier and the record;
**Γ supplies the channel through which the environment forms it.** The environment is not required to
couple to something that is not the gauge field — **it is required to couple through a non-trivial
homology class, which is the third term's whole content.**

**IF `χ` VARIES WITHIN A CLASS**, or if some boundary forms a record, the reading is wrong and the
dilemma stands as registered.

---

## O-20 ANSWERED — **THE INTERSECTION FORM SELECTS THE CHANNEL. BOTH HALVES OF Γ ARE DOING WORK.**

`LANE_O20_HOMOLOGY`. **My registered prediction — "`χ` depends on the homology class and nothing
else" — is FALSIFIED**, and what replaces it is sharper.

| coupling | in `B₁`? | `\|c ∩ supp X̄\|` | pairing mod 2 | `‖[Z_c, X̄]‖` | **`χ`** |
|---|---|---|---|---|---|
| `[4,6]` | no | 1 | **1** | 32.0000 | **0.90811968** |
| `[0,2]` | no | 1 | **1** | 32.0000 | **0.90811968** |
| `[3,7]` | no | 0 | **0** | 0.0000 | **0.00000000** |
| `[1,5]` | no | 0 | **0** | 0.0000 | **0.00000000** |
| all boundaries | **yes** | — | — | — | **0.00000000** |

**ALL FOUR OF THOSE COUPLINGS ARE NON-BOUNDARIES.** `H₁` alone does not decide it — the class is
non-trivial in every one of them and `χ` still splits. Every coupling is gauge-invariant by
construction (`0.0e+00`).

> ### **`χ > 0` IFF THE COUPLING'S CYCLE PAIRS ODDLY WITH THE RECORD'S CONJUGATE. Four for four.**

### THIS IS Γ'S FULL DEFINITION, AND ONLY NOW IS THE SECOND HALF EARNING ITS PLACE

`GRAVITY_DEFINED_V001` registered Γ as the **pair** `(H₁(Σ), ⟨·,·⟩)`. **Until now every result used
`H₁` — the group — and the intersection form sat there unused.** Here the group is not enough: all
four couplings live in `H₁`, and **the FORM is what selects which of them opens a channel.**

**And the pairing is not Poincaré duality** — G-13 already corrected that. It is the evaluation
pairing, perfect over any field, needing no manifold.

### **O-20 ANSWERED IN THE CHARTER'S TERMS**

The dilemma I registered — *"give up gauge invariance or locality"* — **was mis-stated.** Every
coupling in the table above is gauge-invariant. What distinguishes them is **homological**:

| | |
|---|---|
| **EM** | supplies the complex, the carrier, and the record — which **is** a holonomy |
| **Γ** | supplies **the channel**: a coupling forms a record **iff it pairs non-trivially with the record's conjugate under the intersection form** |
| **alpha** | sets what it costs |

**The environment is NOT required to couple to something that is not the gauge field.** It is required
to couple **through a class that pairs with the record** — and that pairing is the third term's
entire content, both halves of it.

**NAMING DISCIPLINE HOLDS (D-2, and the principal: *"not classical gravity of course"*).** This is Γ,
defined by R1–R3 and by the function it performs. **No attribute of the classical field transfers
through the name.**

---

## PLAN REVISION — **THE PRINCIPAL'S THREE QUESTIONS, ANSWERED AGAINST THE FILES**

*"Have we proven how records are created? Do we have the process model up to date? Have we used real
terms?"* Checked, not recalled.

### 1. **NO — EXISTENCE IS PROVED, FORMATION IS NOT**

| | status |
|---|---|
| record **EXISTENCE** | **PROVED and carrier-free.** C-12, exact criterion, 210/210 exhaustive; re-derived from `(H,{L_k})` alone by the model on nine spectra |
| record **FORMATION** | **described and demonstrated, not proved.** G-16 rests on **one carrier and four couplings** |

`A-PR` says it on its face: *"GENERAL tier PROVED; GAUGE tier proved on ONE carrier family."*
**Only 6 of 78 PROVED rows cite two or more structurally different carriers.** And PF-6 FAILED, with
X-4, T-VI.3 and T-VI.4 all BLOCKED at zero empirical contact.

### 2. **NO — THE MODEL COVERS THE STATIC HALF ONLY**

`model/record_model.py` exposes `records`, `commuting_family`, `independence`, `protection`.

| | in the model? |
|---|---|
| environment · coupling · `χ` | **none of them** |
| the intersection pairing (G-16, today) | **zero mentions**, in the model *or* `MODEL.md` |

**It is a record-EXISTENCE calculator.** Every formation result lives in one-off lane scripts that do
not talk to each other or to the model. **The charter's word is FORMATION, and the model does not
compute it.**

### 3. **MOSTLY — BUT THE MAP WAS NEVER WRITTEN**

The physics vocabulary is standard and used correctly — code distance, Knill–Laflamme,
systole/cosystole, Holevo `χ`, Lindblad, Davies, mean-force Gibbs, Euler–Poincaré. **PF-6 confirmed
every result has a named owner.**
**A layer of program vocabulary sits on top, unmapped:** *record* = a logical operator, *writer* = its
conjugate, *the channel* = coined today, *Γ* = a placeholder for `(H₁, ⟨·,·⟩)`.
**A physicist could not tell which terms are ours and which are theirs — and that is exactly the
confusion that let borrowed results be registered as findings.**

### THE REVISION

- **PF-10 — extend the model to FORMATION.** Until it computes formation, it is not the process model.
- **PF-11 — the glossary.** Every program term to its standard name and owner. PF-6's attribution
  finding turned into a document, so a renaming can never again be mistaken for a discovery.
- **PF-8 RISES TO THE TOP.** Repeatability was written as the final step. **It is the binding
  constraint on the word "proven", and 6 rows of 78 currently meet it.**

---

## O-20, FULL POPULATION — **every boundary at exactly zero; non-boundaries split**

The complete sweep over all 31 cycles of the 2×2 torus finished after the four-sample result was
registered, and corroborates it:

| class | n | `χ` range | spread |
|---|---|---|---|
| **`B₁` (boundary)** | **7** | `[0.00000000, 0.00000000]` | **2.78e-15** |
| **NOT a boundary** | **24** | `[0.00000000, 0.90811968]` | **9.08e-01** |

**Every boundary gives exactly zero. Non-boundaries span the full range.** The script's own verdict
line reads **NOT CONFIRMED** for the prediction as I registered it — correctly — and `o20b` established
what does decide it: **the intersection pairing with the record's conjugate.**

**PROCESS DEFECT, RECORDED:** I sealed `LANE_O20_HOMOLOGY` while its background run was still writing
to the output file, and the gate caught the stale manifest on the next check. **Never seal a file a
background job is still writing.** The gate has now caught: unverifiable lane manifests, three
nominated logicals, two D-8 defects in the harness itself, and this.

---

## H-1 REFRAMED BY THE PRINCIPAL — **EMERGENCE FROM RECORDS, NOT IDENTITY AT THE RECORD LEVEL**

The principal: *"We want to connect Γ with classical gravity via **emergence from records**. We are not
trying to equate Γ and gravity at the record level."*

**THESE ARE DIFFERENT QUESTIONS AND I CONFLATED THEM.**

| | question | verdict |
|---|---|---|
| **X-6, withdrawn** | *is the record-level constraint THE SAME constraint as gravity's?* | an **identity claim at the record level** — an import (D-1), correctly withdrawn |
| **H-1, the real one** | *does classical gravity EMERGE from records?* | **untouched by that withdrawal. It runs the other way.** |

**X-6's failure says nothing about H-1.** Ours being a finite abelian group where gravity's is a Lie
algebroid is a fact about *identity at one level*. **Emergence never claims the two look alike at the
microscopic level — that is what emergence means.** Thermodynamics does not resemble statistical
mechanics; it is what statistical mechanics looks like coarse-grained.

### AND IT IS NOT A D-4 CATEGORY ERROR — CHECKED

D-4 forbids asking what **produces** a permission. **Emergence does not ask that.** It asks whether the
accumulated record-level structure, coarse-grained, **IS** what the classical constraint describes.
That is an **identification between levels of description**, not a production rule. **D-4 permits it.**

### **THIS FORCES A REVISIT OF X-2's RECLASSIFICATION**

X-2 asked whether **content shapes geometry**. I reclassified it as a category error — correct **at the
record level**, where χ is a parameter with no equation of motion. **But that reclassification also
foreclosed the emergence question at the collective level, and it should not have.**

> **"Does record content look like a geometry when accumulated?" is not the record-level question that
> was refused. It is the emergence question, and it has never been asked.**

### **AND H-1 AND H-7 MAY BE THE SAME PROBLEM**

H-7 says the carrier is **assumed** — the complex is handed to us. **If classical gravity emerges from
records, then the carrier's geometry IS a description of record content, and "where does the carrier
come from" is answered by the same result.** Two of the seven hard problems collapse into one.

### WHAT WOULD COUNT AS PROGRESS, STATED SO IT CANNOT BE FUDGED

1. a **collective** quantity built from **many** records — not a property of one
2. shown to obey something **Einstein-constraint-like**
3. **without importing the constraint** — D-1 still binds; the classical form may be *recovered*, never
   *assumed* or used as the test

**WE HAVE ESSENTIALLY NOTHING ON THIS.** The nearest thing is G-2 — `records = 2 − (1/2π)∫K dA` —
which relates a record count to an integrated curvature **on a given carrier**. That is a relation, not
an emergence: the geometry is input on both sides.

---

# **THE CLAIM, STATED — "Γ IS WHERE GRAVITY COMES FROM"**

The principal, 2026-08-19. **This is the program's central claim and it is now stated sharply enough
to be worked against.**

| | | verdict |
|---|---|---|
| Γ **is** gravity at the record level | identity | **withdrawn as an import** (X-6, D-1) |
| Γ **resembles** gravity | correspondence | never claimed; the resemblances are generic |
| **Γ is where gravity COMES FROM** | **origin** | **THE CLAIM** |

Records are the substrate. **Classical gravity is what Γ becomes at scale.** The direction is
Γ → gravity and never gravity → Γ.

## **WHY THE IMPORT DISCIPLINE WAS NEVER HYGIENE**

Every time a classical measure was caught being used as a criterion — backreaction (X-2), allow→require
(X2 erratum), the constraint-algebra falsifier (X-6), EM's local field values (D-5), grading the arrow
against "time has a direction" (D-9) — **the principal caught it, and every catch was protecting this
claim.**

> ### **IF Γ HAD BEEN DEFINED USING ANY FEATURE OF CLASSICAL GRAVITY, "Γ IS WHERE GRAVITY COMES FROM"
> ### WOULD BE CIRCULAR. D-1, D-2, D-4, D-5 AND D-9 ARE NOT TIDINESS. THEY ARE WHAT MAKES THE CLAIM
> ### NON-CIRCULAR, AND THEY HAD TO COME FIRST.**

**And it makes the program's order the only order that works.** Γ was built **from function alone** —
R1 space, R2 writer, R3 protection, and now the channel — with **no gravitational input at any point**.
Only a Γ constructed that way can be shown to *give rise to* gravity rather than to have been shaped by
it.

## WHAT THE CLAIM COMMITS US TO

| | | state |
|---|---|---|
| **1** | Γ exists at the record level with its own content | **DONE.** R1–R3 measured; the channel measured (G-16); count laws; the arrow |
| **2** | **nothing of classical gravity is assumed in defining Γ** | **DONE, and it is the harder half of the two.** Five doctrine rows and eleven withdrawn claims enforce it |
| **3** | classical gravity is **recoverable from accumulated Γ** | **NOTHING. This is T-20 and it is the whole remaining task** |
| **4** | the direction is Γ → gravity, never the reverse | **enforced by D-1** |

## WHAT THE CLAIM FORBIDS, PERMANENTLY

- **any classical gravitational feature used as a criterion for Γ** — it would make the claim circular
- **expecting Γ to look like gravity** — the error caught five times; emergence does not preserve form
- **requiring gravity's equations at the record level** — X-2 and X-6, both closed

## THE HONEST POSITION

**Half of the claim is built and the harder half of THAT half — keeping gravity out — is done.**
**The other half is untouched.** `G-2` relates record count to integrated curvature **on a given
carrier**, with geometry as input on both sides. **That is a relation. It is not an origin.**

---

## T-3 DONE — **O-19 FIXED, AND THE MODEL NOW REACHES dim 256**

`model/record_model.py`, `LANE_T3_MODELREACH`.

| carrier | time | minimal projections | record possible? |
|---|---|---|---|
| toric 2×2, **no noise** | **0.1s** | 256 | yes |
| toric 2×2, **single-site `Z`** | **2.1s** | 32 | yes |
| toric 2×2, **single-site `X,Y,Z`** | **0.2s** | **1** | **NO — scalars only** |

**The last row independently reproduces C-17/O-17 on a SECOND carrier.** That result was measured on
`[[5,1,3]]` by an entirely different route — a Gram matrix of the commutator system. **The model gets
it at dim 256 in a fifth of a second, from `(H,{L_k})` alone.**

### THREE ATTEMPTS, AND THE FIRST TWO FAILED FOR REASONS WORTH KEEPING

1. **Commutant from generators, direct solve.** Correct (O-19 as registered) but `n²×n²`. **OOM at 256.**
2. **Block-diagonal reduction in `H`'s eigenbasis.** Cuts unknowns to `D = Σ m_E²` — **and `D` is large
   PRECISELY WHEN `H` IS DEGENERATE, which is what a record requires (P-1).** Measured: multiplicities
   `[4,48,152,48,4]`, `D = 27744`, a **12.3 GB** Gram matrix. **The reduction helps the case we do not
   care about.**
3. **What works: THE MODEL NEVER NEEDED A BASIS OF `A′`.** `minimal_projections` needs **one generic
   Hermitian element**, and that is a single projection. With no noise the commutant has dimension
   27744 and no sampling scheme could span it — **and nothing in the model ever asked it to.**

**The projection itself:** unitary generators by **twisted averaging** `X → (X + gXg†)/2`; Hermitian
generators — `H` is Hermitian and almost never unitary — by their **exact block projection** in their
own eigenbasis. **Treating `H` as a generic generator is what sent the whole computation into the
`n²×n²` fallback.** The commutant basis remains available as a lazy property and is never on the
critical path.

**`validate_model.py` still passes 12/12 after every step.**

---

## T-4 DONE — **THE MODEL NOW COMPUTES FORMATION**

`model/record_model.py`: `Environment` (a qubit bath at inverse temperature β, with per-qubit probes)
and `RecordModel.formation(record, coupling, env, λ, t)`, returning `χ(record : bath)` after unitary
evolution from a product state. Fragments are supported for redundancy (F-21).

| check | model | target | |
|---|---|---|---|
| F-20, `χ` at `t=1`, coupling `Z̄` | **0.97527192** | 0.97527192 | **MATCH** |
| O-18, plaquettes — gauge-invariant, local | **0.00000000** | 0.00000000 | **MATCH** |
| O-18, `Σ Z_l` — not gauge-invariant, local | **0.21703158** | 0.21703158 | **MATCH** |
| O-18, `Z̄` — gauge-invariant, non-local | **0.90811968** | 0.90811968 | **MATCH** |

**A REAL API DEFECT, CAUGHT BY THE THIRD ROW.** My first `formation` assumed a **product** coupling
`A ⊗ probe`. **The lanes distribute each system term to a SPECIFIC bath qubit** — `Σ_l Z_l ⊗ X_{l mod 3}`
— and the product ansatz silently returned `0.10846460` against `0.21703158`. **Not a tolerance
question: a different physical setup.** `formation` now accepts a product coupling, a **distributed**
list of `(A_i, j)` pairs, or a full interaction operator.

---

## **G-16 IS WRONG AS REGISTERED — NECESSARY, NOT SUFFICIENT**

**G-16 said: `χ > 0` iff the coupling fails to commute with the record's CONJUGATE.** It was validated
on **four weight-2 couplings**, where the distinction cannot arise. **The model, asked the same
question on every cycle of the carrier, found eight counterexamples.**

| coupling | `‖[A, X̄]‖` | component along `Z̄` on the code space | `χ` |
|---|---|---|---|
| `[0,2]`, `[4,6]` | 32.0 | **1.000** | **0.90811968** |
| `[3,7]`, `[1,5]` | 0.0 | 0.000 | 0.00000000 |
| **`[3,4,6,7]`, `[2,3,4,5]`, `[0,3,5,6]` …** | **32.0** | **0.000** | **0.00000000** |

**The last row anticommutes with the writer and gives ZERO.** The reason is exact: `Z̄₂` **commutes**
with `X̄` (measured `0.0`), so **`Z̄·Z̄₂` anticommutes with `X̄`** (measured `32.0`) while being a
**different logical**. The bath learns *that* logical, which in a maximally mixed code space says
nothing about `Z̄`.

> ### **THE CORRECT CRITERION: a coupling opens a channel to a record iff ITS COMPRESSION ONTO THE
> ### CODE SPACE HAS A NON-ZERO COMPONENT ALONG THAT RECORD.** Anticommuting with the writer is
> ### implied by this and does not imply it.

**THIS IS THE SECOND TIME TODAY A ROW REGISTERED AS PROVED WAS VALIDATED ONLY ON THE CASES IT WAS
DERIVED FROM** — the first was F-25's `λ^{2d}`, which PF-6 corrected to `λ^{2n*}`. **Both were caught
by testing outside the fitted set, which is what the model exists for.**

---

## T-5 DONE — **THE CORRECTED CHANNEL CRITERION, 31 OF 31**

`model.channel(record, coupling)`, verified against measured `χ` on **every cycle of the 2×2 torus**:

| | |
|---|---|
| cycles tested | **31** |
| `channel()` predicts a channel opens | **8** |
| **agreement with measured `χ`** | **31 of 31, zero mismatches** |

**The eight that open are exactly the cycles whose compression onto the code space has a non-zero
component along `Z̄`.** The 23 that do not include both the boundaries **and** the non-boundaries that
are other logicals — which the anticommutation form got wrong.

> ### **`channel()` is now the model's answer to "can this environment form this record", and it is
> ### decided entirely by the coupling's action ON THE CODE SPACE — not by its weight, its locality,
> ### its gauge invariance, or its homology class taken alone.**

---

## T-6 DONE — **RECORDS COMPOSE. MEASURED, NOT ASSERTED.** `T-I.4` ANSWERED

`model.channel_map` and `model.formation_independence`, on the toric 2×2 with the family `{Z̄, Z̄₂}`.

### THE DEPENDENCY STRUCTURE

| coupling | serves `Z̄` | serves `Z̄₂` |
|---|---|---|
| `Z̄` | **True** | False |
| `Z̄₂` | False | **True** |
| **`Z̄·Z̄₂`** | **False** | **False** |
| sum of plaquettes | False | False |

**`Z̄·Z̄₂` serves NEITHER** — it is a third logical, and an environment coupling through it forms a
record that is not in the family being tracked. **This is T-5's correction showing up as structure
rather than as an error.**

### CAN ONE BE FORMED WITHOUT DISTURBING THE OTHER?

| coupling | targets | `χ(Z̄)` | `χ(Z̄₂)` | `\|Δ⟨Z̄⟩\|` | `\|Δ⟨Z̄₂⟩\|` | independent |
|---|---|---|---|---|---|---|
| `Z̄` | `Z̄` | **0.90811968** | **0.00000000** | 6.94e-16 | 3.96e-16 | **True** |
| `Z̄₂` | `Z̄₂` | **0.00000000** | **0.90811968** | 8.92e-16 | 1.70e-16 | **True** |

> ### **EACH RECORD IS FORMED WITHOUT THE ENVIRONMENT LEARNING ANYTHING ABOUT THE OTHER, AND WITHOUT
> ### THE OTHER'S VALUE MOVING — both at the `1e-16` floor.**

**`T-I.4` — "do records compose? a theory of one record is not a theory of records" — has been OPEN
since the target document was written. It is now answered for this family, by measurement:
THEY COMPOSE, AND THEY DO NOT INTERFERE.**

**Scope, stated: one carrier, one family of two.** Whether independence survives larger families and
other carriers is T-9's business.

---

## T-7 DONE — **THE FORMATION HALF VALIDATES THROUGH THE MODEL. 17 PASS, 0 FAIL. STAGE B COMPLETE.**

`model/validate_formation.py`. Every number below was first produced by a **one-off lane script** and
is re-derived **through the model**:

| result | checks | |
|---|---|---|
| **F-20** the history | `χ(t=1) = 0.97527192`; `χ(t=0) = 0` exactly | PASS |
| **F-21** redundancy | fragments `0.78936622 / 0.04837713 / 0.67860249`; weight-1 gives 0 | PASS |
| **C-18** gauge invariance + locality | `0.00000000 / 0.21703158 / 0.90811968` | PASS |
| **G-16** the channel criterion | opens for `Z̄`, not for `Z̄₂`, **not for `Z̄·Z̄₂`** — and `χ` really is 0 there | PASS |
| **C-17** clause (ii) on the environment | `Z`-noise admits records; `X,Y,Z`-noise leaves scalars only | PASS |
| **C-19** composition | both form independently; the bath learns `0.00000000` about the other | PASS |

> ### **THE MODEL IS NOW THE PROCESS MODEL, NOT A PARALLEL IMPLEMENTATION. A lane and the model
> ### disagreeing is now a detectable event, and the gate runs the check on every finding.**

**STAGE B IS COMPLETE.** The model computes record **existence** from `(H,{L_k})` alone and record
**formation** from `(H,{L_k},coupling,environment)`, with the dependency structure and composition of
a multi-record family. **Half of the definition of done — "the model so that our proof can be checked
by anyone" — now has a working object behind it.**

---

## T-8 DONE / O-14 CLOSED — **THE SECOND CARRIER, AND A TRAP AVOIDED ON THE WAY**

`LANE_T8_CARRIERS`. PF-3B failed because the bouquet has Z-systole 3 but **X-cosystole 1**, so its
true distance is 1 and it cannot test clause (v) at all. O-14 asked for a **non-manifold with BOTH
distances ≥ 2**.

| candidate | V | E | F | `H₁` | systole | cosystole | `d` | |
|---|---|---|---|---|---|---|---|---|
| torus 2×2 — **incumbent, a manifold** | 4 | 8 | 4 | 2 | 2 | 2 | 2 | |
| bouquet of 2 triangles — PF-3B's | 5 | 6 | 0 | 2 | 3 | **1** | **1** | **disqualified** |
| torus + duplicated plaquette | 4 | 8 | 5 | 2 | 2 | 2 | 2 | **a trap — see below** |
| **torus 2×2 + disk capping a wrap** | 4 | 8 | **5** | **1** | **2** | **2** | **2** | **THE SECOND CARRIER** |
| book, 2 or 3 pages on a spine | | | | **0** | — | — | — | no records at all |

### **THE TRAP, RECORDED BECAUSE I NEARLY TOOK IT**

**"Torus + duplicated plaquette" is non-manifold as a COMPLEX and is NOT a second carrier.** Adding a
face that is already there leaves `rank(∂₂)`, `B₁`, `H₁` **and the entire stabiliser group** unchanged.
**Same code, different drawing.** It would have passed every carrier-independence test by being the
same carrier.

> ### **Only a face that changes the STABILISER GROUP changes the carrier. A complex can be redrawn
> ### as non-manifold without becoming a different quantum system.**

### THE SECOND CARRIER

**Torus 2×2 with a disk capping a non-contractible wrap.** Non-manifold along the capped cycle — those
edges lie in **three** faces. **`H₁ = 1` where the torus has 2**, so it is **`[[8,1,2]]` against the
toric `[[8,2,2]]`** — a genuinely different code — with **both distances 2** and **the same Hilbert
dimension 256**, so everything already computed can be re-run on it at the same cost.

---

## T-13 DONE / O-15 — **RECURRENCE SHRINKS. REDUNDANCY EVENS OUT ONLY FOR EQUIVALENT FRAGMENTS.**

`LANE_T13_BATHSIZE`. The dimension constraint is real — a 7-qubit bath under the toric 2×2 would
need `eigh` on 32768² — so the **system** was shrunk to `[[5,1,3]]` (dim 32, verified logicals) and
the bath grown to 7 qubits.

### RECURRENCE — PREDICTED, AND CONFIRMED

| bath | max `χ` | # decreases in `χ(t)` | **largest dip** |
|---|---|---|---|
| `nq = 3` | 0.968958 | 6 | **0.119752** |
| `nq = 5` | 0.995633 | 5 | **0.081734** |
| `nq = 7` | **0.999502** | **3** | **0.059981** |

**Recurrence shrinks monotonically with bath size and `χ` approaches a full bit.** **It is not
eliminated at `nq = 7` — three decreases remain.** The trend is measured; full monotonicity would need
a bath beyond reach.

### REDUNDANCY — **PREDICTED TO EVEN OUT. IT DID NOT.**

| bath | whole | mean fragment | spread | **relative spread** |
|---|---|---|---|---|
| `nq = 3` | 0.7919 | 0.3994 | 0.4982 | **1.247** |
| `nq = 5` | 0.8934 | 0.3747 | 0.4982 | **1.329** |
| `nq = 7` | 0.9906 | 0.4876 | 0.6782 | **1.391** |

**It gets MORE uneven as the bath grows.** My prediction was wrong.

### THE CONTROL THAT EXPLAINS IT — **`0.0000` EXACTLY**

| bath energies | `nq` | whole | mean fragment | spread | relative spread |
|---|---|---|---|---|---|
| **random** | 3 / 5 / 7 | 0.79 / 0.89 / 0.99 | 0.40 / 0.37 / 0.49 | 0.50 / 0.50 / 0.68 | 1.247 / 1.329 / 1.391 |
| **IDENTICAL** | 3 / 5 / 7 | 0.93 / 0.98 / **1.00** | **0.6287** | **0.0000** | **0.000** |

> ### **REDUNDANCY EVENS OUT EXACTLY WHEN THE FRAGMENTS ARE EQUIVALENT, AND NOT OTHERWISE. The
> ### unevenness was the ENERGIES, not the physics.**

**AND THAT IS A CONDITION ON OBJECTIVITY, NOT A FREE PROPERTY.** Quantum Darwinism's redundancy
plateau assumes many **equivalent** fragments. With inequivalent ones, **different observers get
genuinely different amounts of the record** — `0.657` against `0.159` on the same bath. **Calling a
record OBJECTIVE requires the environment's fragments to be equivalent, and nothing in the account
supplies that.** Registered as **O-21**.

**MODEL DEFECT FIXED ON THE WAY:** `formation()` redid the eigendecomposition for **every** fragment,
which is what made a 7-qubit bath unreachable. Added `evolve()` and `redundancy()` so many readouts —
whole bath, every fragment, several records — share **one** eigendecomposition.

---

## T-9 DONE — **CARRIER INDEPENDENCE. 32 PASS, 0 FAIL ACROSS THREE CARRIERS.**

`LANE_T9_CARRIERINDEP`. Three carriers, chosen so the differences are **structural**, per **D-12** —
only a change to the **stabiliser group** changes the carrier:

| | carrier | code | why it is different |
|---|---|---|---|
| **A** | toric 2×2 | `[[8,2,2]]` | manifold, lattice gauge theory — **the incumbent** |
| **B** | torus + capped wrap | `[[8,1,2]]` | **NON-MANIFOLD**, one logical, same dim 256 |
| **C** | `[[4,2,2]]` | `[[4,2,2]]` | **not a lattice at all**, dim 16 — carries composition, which B cannot test with one logical |

| row | A | B | C |
|---|---|---|---|
| ground-space dim `= 2^{#logicals}` | ✔ | ✔ | ✔ |
| **C-17** `Z`-only noise admits a record | ✔ | ✔ | ✔ |
| **C-17** generic noise leaves scalars only | ✔ | ✔ | ✔ |
| **G-16** `channel(R,R)` opens | ✔ | ✔ | ✔ |
| **G-16** `channel(R, gauge-invariant local)` shut | ✔ | ✔ | ✔ |
| **C-18** `χ` for that coupling `= 0` | ✔ | ✔ | ✔ |
| **F-20** `χ(t=0) = 0` exactly; `χ(t=4) > 0` | ✔ | ✔ | ✔ |
| **F-21** weight-1 coupling gives `0` | ✔ | ✔ | ✔ |
| **C-19** records compose independently | ✔ | *n/a — one logical* | ✔ |

> ### **EVERY CARRIER-DEPENDENT ROW SURVIVES A CARRIER THAT IS NON-MANIFOLD, AND ONE THAT IS NOT A
> ### LATTICE AT ALL. The results were not artefacts of the toric code.**

**H-4 — "one carrier, and the carrier may be the result" — is answered for the formation results.**
What remains single-carrier is now explicit rather than assumed.

---

## T-11 — **"CONTRACTIBLE REGION" IS UNDEFINED, AND THE TWO READINGS DISAGREE**

`LANE_T11_CLAUSEV`. PF-3B could not run because its carrier had `d=1`; T-8 built one that qualifies.
Running clause (v) under DEF-A on both carriers turned up something other than the expected zero.

### THE EDGE-SUBGRAPH READING — clause (v) FAILS on BOTH carriers

| carrier | record | single-region: any-unitary | **single-region: ADMISSIBLE** | scattered: any | scattered: adm |
|---|---|---|---|---|---|
| A toric `[[8,2,2]]` | `Z̄` | 836 | **8** | 32 | 2 |
| **B torus+cap `[[8,1,2]]` NON-MANIFOLD** | `Z̄₂` | 836 | **8** | 32 | 2 |

**Both carriers behave identically — which is itself a carrier-independence result — and both give
EIGHT admissible flippers inside a single connected contractible region.**

**Requiring the region to be CONNECTED does not rescue it.** "Single" excludes 8 scattered forests
carrying 2 of the 10, and 8 admissible flippers remain in genuinely single regions.

### WHY THIS DISAGREES WITH O-4's ZERO

**O-4 measured `0` admissible flippers at `L=3` using CERTIFIED-CONTRACTIBLE PLAQUETTE BLOCKS — disks
of the surface.** This lane used **edge subgraphs with no cycle**. **The anchor says "no admissible
operation on a single contractible region" and does not say which.**

> ### **THIS IS EXACTLY THE DEFECT O-4 FIXED FOR THE WORD "ADMISSIBLE", UNFIXED FOR THE WORDS
> ### "CONTRACTIBLE REGION". An undefined term in the anchor is doing load-bearing work in clause (v)
> ### — the clause that carries the program's whole protection claim.**

**And the likely content of O-4's zero is not contractibility at all.** At `L=3` the code distance is
`3` and the blocks measured were small; here `d = 2` and a connected 3-edge region already exceeds it.
**What O-4 may have measured is that its regions were SMALL RELATIVE TO `d`** — which is
Knill–Laflamme, not topology. **Registered as O-22.**

**The geometric reading is running and will settle whether clause (v) survives under EITHER reading at
this size.** Until it lands, T-11 is **PARTIAL** and no verdict is registered.

---

## T-11 RESOLVED BY THE PRINCIPAL — **"ISN'T THIS ALLOW/REQUIRE?"** IT IS, AND IT DISSOLVES THE QUESTION

The registrar put a **theory decision** to the principal: clause (v) appeared false on our own carrier
under both readings of "contractible region", and the word seemed to need a stipulation the way
"admissible" did at O-4. **The principal asked whether this was allow/require. It was.**

> ### **CLAUSE (v) IS PART OF THE DEFINITION. IT IS NOT A CLAIM THAT CAN BE TRUE OR FALSE.**
> ### **Asking "does clause (v) hold on this carrier" is asking WHETHER THE CARRIER ALLOWS A
> ### PROTECTED RECORD — a capacity question, of exactly the same type as "a sphere allows no
> ### records", which this program has registered for months without ever calling it a defect in
> ### clause (iii).**

### AND THE MEASUREMENT SAYS WHICH CARRIERS ALLOW ONE

| lattice | edges | `d` | region | **region / system** | any-unitary (control) | **ADMISSIBLE** |
|---|---|---|---|---|---|---|
| torus 2×2 | 8 | 2 | 1 plaquette | **0.50** | 512 | **16** |
| torus 2×2 | 8 | 2 | 2 plaquettes | **0.75** | 73728 | **1152** |
| **torus 3×3** | 18 | 3 | 1 plaquette | **0.22** | **768** | **0** |
| torus 3×3 | 18 | 3 | 3 plaquettes | **0.50** | 145358848 | **3120** |

**The discriminator is the FRACTION.** Every row where a region is **half the system or more** admits
a flipper. **The one row where a region is 22% of the system admits none**, against a positive control
of 768. **The 2×2 torus has no room for a region to be local** — one plaquette is already half of it.

> ### **A CARRIER ALLOWS A PROTECTED RECORD WHEN IT IS LARGE ENOUGH THAT A LOCAL REGION IS A SMALL
> ### FRACTION OF IT. The 2×2 torus does not. The 3×3 does. That is a capacity fact about carriers,
> ### not a defect in the anchor.**

**O-22 IS CLOSED.** "Contractible region" needs no stipulation. The two readings did not disagree
about the clause — **they disagreed about which carriers were being asked**, and both agree once the
fraction is held small.

### THE PATTERN, AND IT IS THE REGISTRAR'S

**Every time this program has been framed as facing a defect or a decision — backreaction (X-2),
allow→require (X2), X-6's falsifier, and now clause (v) — the allow/require typing has dissolved it,
and each time the principal saw it first.** The registrar converts permissions into claims and then
finds the claims false. **D-4 exists to catch this and did not fire here because the registrar was
looking at a clause rather than at a carrier.**

> ### **D-4 EXTENDED: THE FIVE CLAUSES ARE PERMISSIONS. A carrier failing one is a fact about the
> ### CARRIER. TELL: any sentence of the form "clause (n) is false", which is a category error —
> ### clauses are not true or false, carriers satisfy them or do not.**

---

## T-10 DONE — **28 PARAMETER SETTINGS, 0 CONCLUSIONS MOVED. STAGE C COMPLETE.**

`LANE_T10_PARAMS`, carrier `[[4,2,2]]`. **The numbers move; the conclusion does not.**

| parameter swept | range | `χ[record]` range | conclusion |
|---|---|---|---|
| **temperature `β`** | 0.2 → 20.0 | 0.057 → **0.99996** | invariant, 6/6 |
| **coupling `λ`** | 0.05 → 3.0 | **0.0042** → 0.979 | invariant, 6/6 |
| **bath size `nq`** | 2 → 6 | 0.906 → 0.989 | invariant, 5/5 |
| **time `t`** | 0.5 → 16.0 | 0.720 → 0.965 | invariant, 6/6 |
| **bath energies** | 5 seeds | 0.730 → 0.965 | invariant, 5/5 |

**`χ[record]` spans more than two orders of magnitude — 0.0042 to 0.99996.** Across all 28 settings:
`χ` for the **gauge-invariant local** coupling stays at the floor (max `4.4e-15`), `χ` for the
**weight-1** coupling stays at the floor (max `4.4e-15`), and **the noise floor at `λ=0` is `0.00e+00`
in 21 of 28 and never above `2.4e-15`.**

> ### **NO CONCLUSION IS CARRIED BY A PARAMETER. The record coupling forms, the gauge-invariant
> ### local one does not, the weight-1 one does not — at every temperature, coupling strength, bath
> ### size, time and set of bath energies tried.**

**STAGE C IS COMPLETE.** Carrier independence (T-9, three carriers, 32 checks), a valid second carrier
(T-8), clause (v) as a capacity statement (T-11), a bath large enough to show the recurrence trend
(T-13), and parameter independence (T-10). **`H-4` — "one carrier, and the carrier may be the result"
— is closed for the formation results, and no free parameter is doing hidden work.**

---

## T-14 DONE — **ALPHA'S EXPONENT IS `n*`, NOT `d`. `d` IS THE SPECIAL CASE.**

`LANE_T14_ALPHA`. PF-6 rescoped Theorem D; this measures both exponents in-house on three carriers,
with `n*` **computed** rather than assumed.

| carrier | `d` | **`n*` (Z-only)** | **GENERIC slope** | **Z-ONLY slope** |
|---|---|---|---|---|
| toric 2×2 `[[8,2,2]]` | 2 | 2 | **2.0211** | **2.0389** |
| **`[[5,1,3]]` non-CSS** | 3 | **5** | **3.0036** | **4.9836** |
| `[[7,1,3]]` Steane | 3 | 3 | **3.0046** | **3.0118** |

**The generic exponent tracks `d`. The Z-only exponent tracks `n*`.** They agree on the two carriers
where `n* = d` and **separate on `[[5,1,3]]`, where `n* = 5` and the measured Z-only slope is 4.9836
against a code distance of 3.**

> ### **ALPHA SPLITS THE RECORD SPACE AT ORDER `n*` — the fewest AVAILABLE local terms whose product
> ### reaches the code space. When the perturbation class is unrestricted every Pauli is available and
> ### `n* = d`; when it is restricted, `n*` can be larger. `d` IS THE SPECIAL CASE, NOT THE LAW.**

**Theorem D's unqualified form — "a local perturbation splits the degeneracy as `ε^d`" — is false on
`[[5,1,3]]` for a record-commuting perturbation, and `n*` subsumes both readings.**

---

## T-22 — **ALPHA STANDS FOR A GENERIC COUPLING STRENGTH HERE, AND T-10 SHOWS ITS VALUE CANNOT MATTER**

`H-2` asked whether alpha has content beyond a name. **It does not, and the honest answer is sharper
than "we have not connected it."**

**T-10 settles it.** Alpha enters this program as the coupling strength `λ`. Over **28 settings
spanning `λ = 0.05` to `3.0`** — a factor of 60 — **no conclusion moved** (`C-21`). Every registered
result is either **exact** (a zero or a non-zero, decided by the channel criterion) or an **exponent**
(`n*`, `d`), and **exponents do not depend on the value of the coupling.**

> ### **NO STRUCTURAL CONCLUSION IN THIS PROGRAM CAN DEPEND ON ALPHA'S VALUE, BECAUSE T-10 PROVED NO
> ### CONCLUSION DEPENDS ON `λ` AT ALL. That is not a gap waiting to be filled — it is a fact about
> ### what kind of results these are.**

### WHAT ALPHA'S VALUE WOULD SET, AND WHY THE PROGRAM CANNOT REACH IT

**Rates and timescales.** `χ ~ λ^{2n*}` (`F-23`) — the value of the coupling sets **how fast** a record
forms, not **whether** it can. **The program has connected that to no physical number**, and doing so
would need a continuum limit from a `Z₂` lattice gauge theory to an actual electromagnetic coupling,
which nothing here supplies. **Claiming otherwise would be an import (D-1).**

### THE ANCHOR IS AMENDED TO SAY SO

> **In this program "alpha" names a GENERIC COUPLING STRENGTH — the magnitude of the local terms that
> do not respect the record's structure. It is NOT the fine structure constant, no result depends on
> its value, and nothing here is dimensionful.**

**`H-2` stands as a stated limitation rather than an open task.** The charter names three terms; **two
have record-level content and the third is a magnitude**, which is what the measurements show it to be.

---

## T-12 / PF-4 DONE — **NO STRUCTURAL CONDITION NARROWER THAN THE CLAUSES IS NECESSARY**

`LANE_T12_NECESSARY`. C-4 read *"records require non-trivial homology of an `F₂` chain complex"*.
**O-8 showed non-CSS stabiliser codes escape that class.** The question was whether **anything**
narrower than the clauses survives.

| system | dim | records | writer verified |
|---|---|---|---|
| random `H`, degenerate pairs, no noise | 4 | 2 | **2/2** |
| random `H`, degenerate pairs, no noise | **6** | 4 | **4/4** |
| random `H`, degenerate pairs, no noise | 8 | 8 | 4/4 |
| random `H` + a diagonal jump | 4 | 2 | **2/2** |
| random `H` + a diagonal jump | **6** | 4 | **4/4** |

**5 of 5 carry a record with a verified admissible writer.** And **two of them are dimension 6**:

| proposed necessary condition | present? |
|---|---|
| tensor factorisation into qubits | **NO — 6 is not a power of 2** |
| a stabiliser group | **NO — there are no Paulis to generate one** |
| an `F₂` chain complex | **NO — there are no cells** |
| non-trivial homology | **NOT DEFINED — there is no complex** |
| a lattice, or any geometry | **NO** |

> ### **THE NECESSARY CONDITION IS C-12, AND IT IS THE CLAUSES RESTATED RATHER THAN ANYTHING NARROWER:
> ### a record satisfying (i)–(iv) exists IFF the commutant of `alg{I,H,L_k,L_k†}` contains a
> ### projection that is non-trivial on some eigenspace and trace-balanced.**

**C-15 already established that (i)–(iv) are carrier-free and that (v) requires a locality structure.
Given one, (v) is a DISTANCE condition — no admissible local operation reaches the record — which is
Knill–Laflamme and is not homological either.**

### WHAT C-4 BECOMES

**Homology is a SUFFICIENT route and one this program has measured extensively. It is not necessary,
and neither is any code-theoretic condition.** `C-4`'s claim that records *require* non-trivial
homology is **withdrawn** — the twelfth withdrawn claim — and replaced by the statement that homology
is one family among others, all of which satisfy C-12.

**STAGE D COMPLETE.**

---

# **T-20's CRITERION, SUPPLIED BY THE PRINCIPAL — RECORD-LEVEL HOLONOMY**

The registrar asked for the **criterion**, not the method: *what would we accept as "gravity emerged"?*
**The principal supplied one, and it is computable.**

> ### **A STABLE, UNIVERSAL, PATH-DEPENDENT MISMATCH AMONG RECORDS THAT CAN BE INTERPRETED AS CURVATURE.**
> ### **Gravity emerging from Γ would look like RECORD-LEVEL HOLONOMY.**

**One record cannot show gravity. Two give relation. Several make PATH COMPARISON possible**, and that
is where geometry can appear: compare `A→B→D` against `A→C→D`. The diagnostic is

> `H_ABCD = (Γ_AB Γ_BD)(Γ_AC Γ_CD)^{-1}`
>
> `H ≈ I` → the record geometry is **flat**. `H ≠ I` **in a structured way** → the record network has
> **curvature**.

**WHY THIS IS ADMISSIBLE UNDER OUR OWN DOCTRINE, CHECKED BEFORE ACCEPTING IT:**

| | |
|---|---|
| **D-1** | the test is whether **our** transport closes. **The Einstein form `R ~ dΓ + ΓΓ` is used to say what a positive result would MEAN, never as the criterion.** This is exactly the line X-6 crossed and this does not |
| **D-4** | it asks whether a structure **exists**, not what **produces** a permission |
| **D-9** | it is stated as a mechanism — transport failing to close — not as a grade |
| **D-11** | it is specified **before** any measurement, on no fitted set |

**THE FURTHER SIGNATURES THE PRINCIPAL NAMES, recorded so they are not lost:** the mismatch must be
**local**, **smooth across neighbouring records**, **universal across record types** (gravity couples to
energy/history, not to a charge), **phase/action-based** rather than a force, **stronger with enclosed
record density**, **consistent with causal ordering**, and **subject to a Bianchi-like closure** — record
curvature cannot appear or disappear arbitrarily. **Geodesic-deviation analogue: neighbouring record
chains focus or defocus together. Visibility analogue: interference fades exactly when the record
network can distinguish the histories.**

> ### **"Gravity emerges when multiple records make path-comparison possible, and the mismatch between
> ### alternative record histories becomes stable, universal, and geometry-like."**

**This is now the standard T-20 is measured against.**

---

## T-20 RESULT — **THE RECORD GEOMETRY IS EXACTLY FLAT. A NULL, AND AN INFORMATIVE ONE.**

`LANE_T20_HOLONOMY`, measured against **H-9**, the principal's criterion, registered before the run.

**Carrier `[[8,3,2]]` — three records, which is the minimum the criterion requires.** Every operator
**computed** by symplectic Gram-Schmidt and verified before use.

| closed loop | `‖H − I‖` | |
|---|---|---|
| `A→B→A→B` | **0.000e+00** | FLAT |
| `A→C→A→C` | **0.000e+00** | FLAT |
| `B→C→B→C` | **0.000e+00** | FLAT |
| **`A→B→D` vs `A→C→D`** — the criterion's own diagram | **0.000e+00** | **FLAT** |

**Writer commutators: `0.000e+00`. The holonomy group generated by the writers is ABELIAN.**

> ### **TRANSPORT AROUND EVERY RECORD LOOP CLOSES EXACTLY. There is no path-dependent mismatch, so by
> ### the criterion there is no record-level curvature on these carriers.**

### WHY, AND WHAT WOULD BE NEEDED

**Our records are logical operators of an ABELIAN stabiliser code and their writers commute**, so
transport is path-independent by construction. **A loop can close up to a SIGN, and a sign is not
curvature — it is the same element of an abelian group.**

> ### **CURVATURE REQUIRES A NON-ABELIAN CONNECTION: transport whose composition depends on order in
> ### a way no relabelling removes. That is exactly the class O-8 flagged as UNTESTED — Levin–Wen and
> ### Fibonacci, where the writers are Wilson loops of a non-abelian theory and G-6 already noted they
> ### fall outside the `F₂` chain-complex class.**

**The null is informative because it converts the claim into a structural question with a known
target:** *does the record structure admit non-abelian transport?* **On every carrier this program has
built, no. The candidate class is named and has never been examined.**

### THREE DEFECTS ON THE WAY, ALL CAUGHT BEFORE A NUMBER WAS READ

1. **v1's formation arm returned `4.409e-01` and `7.867e-01` on BOTH carriers** — identical to four
   digits across dim 256 and dim 16, different codes. **A quantity that cannot tell the carriers apart
   is measuring the bath.** Dropped.
2. **v1's writer arm mixed a NOMINATED `X̄` with a CONSTRUCTED one** and measured their commutator.
   `22.70` was the disagreement between two differently-obtained operators.
3. **v2 compared chains with DIFFERENT endpoints** — `A→B` against `A→C` — and reported **12 spurious
   CURVED while the writer commutators were all zero.** The output contradicted itself, and the
   enumeration was the error: **holonomy is a CLOSED loop.**

**And a fourth, earlier: the `[[8,3,2]]` logicals were NOMINATED and failed verification.** Nominating
logicals has now failed **four times** in this program. `symplectic_logicals()` is now in the model so
it cannot happen again.

### WHAT T-6 DID AND DID NOT MEASURE

**T-6 used TWO records.** By the criterion's own terms — *one gives nothing, two give relation,
several make path comparison possible* — **two is exactly the number that cannot show holonomy: there
is only one route and no loop.** T-6 measured **independence** (forming one does not disturb the
other). **Independence is not flatness**, and the registrar's suggestion that T-6 had already measured
this was wrong.

---

## O-23 — **THE CONNECTION IS NOT DETERMINED BY THE RECORDS. T-20's READING IS OVERTURNED.**

`LANE_O23_CONNECTION`. Before hunting a non-abelian carrier, the prior question: **is the connection
even determined by the record structure?**

**Carrier `H = 0` on `C⁸`, three independent records, all independently writable — the most permissive
case there is.** A writer is fixed only up to a unitary preserving **every** record label.

| writer choice | closed-loop holonomy `‖H − I‖` |
|---|---|
| the canonical permutation of the joint record basis | **2.998e-15 / 2.618e-15 / 2.689e-15 — FLAT** |
| **200 of 200 admissible phase-modified writers** | **up to 5.1694** (`5.0493 / 4.2661 / 5.1694`) |

**Every one of those 200 flips its own record and fixes the others — verified individually. All are
writers by clause (iv). They are not alternatives to the definition; they are what the definition
allows.**

> ### **THE SAME RECORD FAMILY GIVES HOLONOMY `0` FOR ONE ADMISSIBLE WRITER AND `5.169` FOR ANOTHER.
> ### "IS THE RECORD GEOMETRY CURVED" IS NOT WELL-POSED ON THE RECORDS ALONE.**

### WHAT THIS DOES TO T-20

**T-20 measured the minimal-weight Pauli writer and found exactly flat. That was a property of THE
CHOICE, not of the record structure.** T-20's result stands as a measurement and its **interpretation
is withdrawn**: it did not show that record geometry is flat, it showed that **one particular
connection** is.

**And O-23 as registered is the wrong question.** *"Does any record structure admit non-abelian
transport?"* — **every one does, with an admissible choice of writer.** The class O-8 named is not
needed to produce curvature.

> ### **THE QUESTION IS: WHAT DETERMINES THE CONNECTION?**
> **A connection is extra data, exactly as it is in gauge theory — the records fix the fibres, not the
> transport between them. Something physical must pick it, and the program has never asked what.**
> Registered as **O-24**.

### AND A CANDIDATE, BECAUSE THE NULL POINTS AT ONE

**T-20's flat connection was the MINIMAL-WEIGHT writer** — the cheapest operation that flips the
record. **The curved ones were built by multiplying by extra phases, which is more.** If minimality
picks the connection, **the flat one is selected and curvature costs weight** — which is testable on a
carrier where weight is defined.

### A D-8 FAILURE IN THIS LANE, CAUGHT AND FIXED

**v1 combined the records with coefficients `1,2,3`, and `1+2−3 = −1−2+3 = 0`** — the combination is
degenerate, so `eigh` did not return a simultaneous eigenbasis and **no constructed writer verified**.
The script then found **zero** admissible alternatives and **still printed a conclusion from the empty
loop.** Both fixed: powers of two separate the sign patterns, and the script now **refuses to conclude
when no valid case executed**.

---

## O-24 ANSWERED — **MINIMALITY SELECTS THE FLAT CONNECTION. CURVATURE COSTS ONE SITE, AND REQUIRES RECORDS TO OVERLAP.**

`LANE_O24_MINIMALITY`. Three qubits, `H = 0`, records `Z₁ Z₂ Z₃` — weight is defined and every
admissible writer is enumerable.

| writer for `R₀` | weight | `‖[U₀,W₁]‖` | loop `‖H−I‖` | |
|---|---|---|---|---|
| `X₀` — the minimal writer | **1** | 0.000e+00 | **0.000e+00** | FLAT |
| `X₀·S₀` — phase on its **own** site | 1 | 0.000e+00 | 0.000e+00 | FLAT |
| **`X₀·S₁`** — phase on **record 1's** site | **2** | **4.000e+00** | **4.000e+00** | **CURVED** |
| `X₀·S₂` | 2 | 0.000e+00 | 0.000e+00 | FLAT |
| `X₀·S₁·S₂` | 3 | 4.000e+00 | 4.000e+00 | CURVED |

> ### **MINIMUM WEIGHT FLAT: 1. MINIMUM WEIGHT CURVED: 2. CURVATURE COSTS EXACTLY ONE EXTRA SITE.**

### THE MECHANISM IS VISIBLE IN WHICH ONE CURVES

**`X₀·S₁` curves and `X₀·S₂` does not**, at the same weight. The difference is that `S₁` reaches
**record 1's site** — the record the loop is taken against.

> ### **CURVATURE REQUIRES A WRITER THAT REACHES ANOTHER RECORD'S SITE. RECORDS MUST OVERLAP.**

**And minimality selects the flat connection**, because the cheapest writer touches only its own site.
**So T-20's flat result was not an accident of choice after all — it is what minimality picks.** O-23's
finding stands: the connection is not *determined* by the records. **But it is SELECTED, if the physics
uses the cheapest operation that does the job.**

### **AND THIS MEETS A SIGNATURE THE PRINCIPAL NAMED INDEPENDENTLY**

H-9 lists, among the signatures of record-level curvature: **"stronger with enclosed record-density."**

> ### **IF RECORDS ARE PACKED DENSELY ENOUGH THAT MINIMAL WRITERS CANNOT AVOID EACH OTHER, OVERLAP IS
> ### FORCED AND CURVATURE IS NOT A CHOICE.**

**That is a prediction of the account, not an assumption of it, and it is testable: sweep record
density on a fixed carrier and measure whether the minimal-writer holonomy turns on.** Registered as
**O-25**, and it is the sharpest thing on the board — **the first place where the program's own
structure predicts curvature rather than merely permitting it.**

---

## O-25 — **DENSITY CANNOT FORCE CURVATURE. THE PREMISE IS WRONG, AND THE REASON IS STRUCTURAL.**

`LANE_O25_DENSITY`. Every logical **computed** by symplectic Gram-Schmidt and verified before use.

| code | `n` | records | **writer overlap** | `max‖[X_i,X_j]‖` | |
|---|---|---|---|---|---|
| `[[4,2,2]]` | 4 | 2 | 1 | **0.000e+00** | FLAT |
| `[[8,3,2]]` | 8 | 3 | 1 | **0.000e+00** | FLAT |
| **`[[6,4,2]]`** | 6 | **4** | **3** | **0.000e+00** | **FLAT** |
| toric 2×2 | 8 | 5 | 2 | **0.000e+00** | FLAT |

**Writers overlap on up to three sites and still commute exactly.**

> ### **IN A STABILISER CODE THE LOGICAL ALGEBRA IS SYMPLECTIC: conjugate pairs anticommute, EVERY
> ### OTHER PAIR COMMUTES, and SUPPORT HAS NOTHING TO DO WITH IT. Overlap is irrelevant. Density
> ### cannot force curvature, and O-25's premise — mine, not the principal's — is wrong.**

### AND THIS SHARPENS O-24 INTO SOMETHING HARDER

O-24 found curvature from `X₀·S₁`, where `S₁` is a **phase gate — not a Pauli, and not a minimal
writer.** Put together with the table above:

> ### **CURVATURE REQUIRES LEAVING THE STABILISER FORMALISM. MINIMALITY FORBIDS EXACTLY THAT.**
> ### **So the flat connection is not merely selected — for stabiliser records it is FORCED, and no
> ### arrangement, density or overlap of such records can produce record-level curvature.**

**H-9's density signature is therefore unavailable to any stabiliser carrier**, and every carrier this
program has built is one.

### WHAT THIS COSTS THE CLAIM, STATED PLAINLY

**"Γ is where gravity comes from" needs record-level curvature, and stabiliser records cannot have
it.** Either the carriers must leave the stabiliser class — non-abelian topological order (`O-8`), or
records that are not code logicals at all (`C-22` shows those exist) — **or the connection is fixed by
something other than minimality, and `H-11` remains open with no candidate.**

**This is a negative result about the program's whole carrier family, and it was reached by testing a
prediction of the account rather than by an outside objection.**

---

## O-26 ROUTE 2 — **LEAST ACTION SELECTS CURVATURE, 400 OF 400. AND THE NORM IS DOING WORK.**

`LANE_O26_NONCODE`. The principal: *"most record formations in the universe come with gravitational
forces, so these records would have to be pretty common"* — which makes stabiliser codes the special
case, not the norm. **Route 2: records that are not code logicals at all (C-22).**

**THE OBSTACLE, AND WHY IT MATTERS.** O-24's minimality selected the flat connection **by WEIGHT**, and
weight needs a tensor factorisation. **A non-code carrier has none.** So: without weight, does anything
select the connection?

| selector | flat | curved | discriminates? |
|---|---|---|---|
| `‖U − I‖` | **4.0000** | **4.0000** | **NO — identical, selects nothing** |
| **`‖log U‖`** (the action) | **6.2832 = 2π** | **[4.6548, 5.5185]** | **YES — and curvature costs LESS** |

| | |
|---|---|
| admissible alternatives sampled | **400** |
| **with action BELOW the flat connection** | **400 of 400** |
| their holonomy range | **[3.353, 5.367]** — every one **CURVED** |
| correlation(action, holonomy) within the curved family | **+0.0113** — none |

> ### **THE FLAT CONNECTION HAS THE HIGHEST ACTION OF EVERY ADMISSIBLE WRITER TESTED. WEIGHT-MINIMALITY
> ### PICKS FLAT; ACTION-MINIMALITY PICKS CURVED. THEY ARE DIFFERENT SELECTORS AND THEY DISAGREE.**

### **THE CAVEAT, AND IT IS SUBSTANTIAL — STATED BEFORE ANY CLAIM IS DRAWN**

**`‖log U‖ = √(Σθ²)` is MAXIMISED by involutions.** The flat writer is a strict swap with eigenphases
`{0, π}`, and **any** phase perturbation moves eigenvalues off `±1` and reduces `Σθ²`. **So "curvature
costs less action" may be a property of THIS NORM rather than of the physics.**

**And "action" is not yet defined in this program.** A physical action needs a **generating Hamiltonian
and a duration** — `U = exp(−iHt)` with a cost in `H` and `t` — not an operator norm chosen for
convenience. **Until that is defined, this result is suggestive and is not registered as a selector.**
**Registered as O-27.**

### WHAT ROUTE 2 HAS ESTABLISHED

**On a non-code carrier, `‖U−I‖` selects nothing and every admissible alternative is curved.** So
**flatness is not forced outside the stabiliser class** — C-24's necessity was a fact about codes, as
suspected. **What is not yet established is that anything SELECTS curvature**, because the one selector
that discriminates is a norm whose behaviour on involutions may be the whole effect.

**A dim-24 carrier — three 8-fold shells, not a power of two — hit the model's enumeration cap at 24
minimal projections and was not measured.** Recorded rather than skipped silently.

---

## O-27 — **LEAST ACTION SELECTS THE FLAT CONNECTION. O-26's RESULT IS OVERTURNED, AND THE ERROR WAS MINE.**

`LANE_O27_ACTION`. `‖log U‖` is not an arbitrary norm — for `U = exp(−iHt)` it **is** `‖Ht‖`, the
energy–time product in units of `ℏ`. What O-26 got wrong was not the measure but the **comparison**.

| writer | `‖Ht‖_F` | `‖Ht‖_∞` | `Σ\|θ\|` | holonomy |
|---|---|---|---|---|
| canonical flat | 6.2832 | 3.1416 | 12.5664 | 3.00e-15 |
| **MINIMUM-ACTION (`φ = π`)** | **4.4429** | **1.5708** | 12.5664 | **2.882e-15 — FLAT** |
| 300 curved samples | [4.7028, 5.6668] | [2.3325, 3.1054] | 12.5664 | all curved |

**Analytic confirmation:** per 2-cycle the minimum of `Σθ²` is at `φ = π`, giving `π/√2 = 2.2214`
against `π = 3.1416` for the canonical. Over 4 cycles: **`4.4429` against `6.2832`** — matching the
measurement exactly.

> ### **THE CHEAPEST ADMISSIBLE WRITER IS FLAT. Every curved sample costs MORE than it (≥ 4.7028
> ### against 4.4429), under `‖Ht‖_F` and `‖Ht‖_∞` alike. `Σ|θ| = 4π` for every writer and
> ### discriminates nothing.**

### **O-26's ERROR, NAMED**

**I compared curved writers against the CANONICAL flat writer, not against the CHEAPEST one.** The
canonical writer — a strict involution with eigenphases `{0, π}` — is the **most expensive** flat
choice, not the minimum. **"400 of 400 cost less than flat" was true of one flat writer and false of
the flat family.** Sampling could not have found this; **it needed the minimisation to be done.**

### WHERE THAT LEAVES THE SELECTOR QUESTION

| selector | picks |
|---|---|
| **weight** (O-24) | **FLAT** |
| **action** `‖Ht‖_F`, `‖Ht‖_∞` (O-27) | **FLAT** |
| `‖U − I‖` | nothing — identical for all |
| `Σ|θ|` | nothing — `4π` for all |

> ### **EVERY SELECTOR THAT DISCRIMINATES PICKS THE FLAT CONNECTION. Record-level curvature is
> ### AVAILABLE on non-code carriers and is NEVER SELECTED.**

### WHAT SURVIVES, AND WHAT DOES NOT

**Survives:** C-24's flatness is a fact about codes, and outside the stabiliser class curvature is
*available* (O-26). **Does not survive:** the suggestion that anything selects it.

**The claim now needs one of two things, and neither is in hand.** Either a carrier where **flat is
not available at all** — non-abelian transport, where writers genuinely fail to commute (`O-8`,
untested) — or **a selector that is not a minimisation**, and `H-11` has no candidate for one.

**This is a negative reached by overturning my own positive result, by doing the minimisation the
sampling had skipped.**

---

# **ROUTE 1 CLOSED — A FLAT CONNECTION IS ALWAYS AVAILABLE, AND CLAUSE (iv) IS WHY**

`LANE_O8_NONABELIAN`. Before building a non-abelian carrier, the prior question: **can the five
clauses permit a carrier where flat is UNAVAILABLE?**

| carrier | records | block sizes | flat exists | `max‖[U_i,U_j]‖` |
|---|---|---|---|---|
| `C⁸`, blocks of dim 1 | 3 | [1] | **YES** | **0.000e+00** |
| `C¹⁶`, blocks of dim 2 | 3 | [2] | **YES** | **0.000e+00** |
| `C³²`, blocks of dim 4 | 3 | [4] | **YES** | **0.000e+00** |
| `C⁶⁴`, blocks of dim 8 | 3 | [8] | **YES** | **0.000e+00** |
| `C¹⁶`, two 8-fold shells | 3 | [2] | **YES** | **0.000e+00** |

**Blocks of dimension 8 give the writers a 64-dimensional internal freedom to be non-abelian in, and
the flat choice still exists exactly.**

### THE ARGUMENT, AND IT IS THE DEFINITION'S OWN

1. **Clause (iii) puts the record inside a DEGENERATE eigenspace of `H`.**
2. **Admissibility is `[U,H] = 0`, which inside a single eigenspace constrains NOTHING** beyond
   preserving it. A writer may be **any** unitary permuting the joint record blocks.
3. **The blocks have EQUAL dimension — and that is exactly clause (iv)'s trace balance (C-11).**
4. **Equal blocks can be identified position-by-position**, and consistent identifications make the
   writers commute **by construction**. Nothing can obstruct the identification, because step 2 left
   no constraint to obstruct it with.

> ### **THE CLAUSE THAT MAKES A RECORD WRITABLE IS THE CLAUSE THAT MAKES ITS CONNECTION FLATTENABLE.
> ### CURVATURE CAN NEVER BE FORCED BY ANY CARRIER MEETING THE FIVE CLAUSES.**

### WHAT THIS DOES TO THE CLAIM

**Both routes out of O-26 are now closed.**

| route | status |
|---|---|
| **1. a carrier where flat is unavailable** | **CLOSED — flat is always available (this lane)** |
| **2. a selector that picks curvature** | **CLOSED — every selector that discriminates picks flat (C-25)** |

> ### **RECORD-LEVEL CURVATURE IS AVAILABLE ON NON-CODE CARRIERS, IS NEVER FORCED, AND IS NEVER
> ### SELECTED. Under the five clauses as written, Γ does not produce gravity.**

**The principal's criterion (H-9) was decidable, was decided, and the answer is negative.** Not
"undetermined", not "out of reach" — **measured, on carriers up to dimension 64, with the obstruction
identified as a theorem about the definition rather than a limit of the search.**

### THE ONE THING THIS DOES NOT CLOSE

**It closes the question FOR THE FIVE CLAUSES AS WRITTEN.** The argument runs through clause (iv)'s
trace balance and clause (iii)'s degeneracy. **A record notion that dropped or altered either could
still force curvature — and this program has no reason to alter them beyond wanting a different
answer, which is not a reason.** Registered as **H-13**.

---

# **THE PRINCIPAL CATCHES AN IMPORT IN THE NEGATIVE RESULT ITSELF**

*"Are you sure that we aren't again importing metrics to the surface that can't survive there?"*
**Audited, and the answer is no — there is an import, and it is in the object measured.**

## THE IMPORT: **THE WRITER WAS TREATED AS THE CONNECTION**

**H-9 asks for transport BETWEEN records** — *"the local rule telling one record how to relate to
NEARBY records: how phase, orientation, causal order, or local frame is transported FROM ONE RECORD
TO THE NEXT."*

**T-20, O-23, O-24, O-25, O-27 and route 1 all measured `U_i U_j U_i⁻¹ U_j⁻¹`, where `U_i` is the
WRITER — the operation that flips record `i`'s VALUE.**

> ### **FLIPPING ONE RECORD'S VALUE IS NOT TRANSPORTING A FRAME FROM ONE RECORD TO ANOTHER. The
> ### registrar needed something to play the role of "connection", took the writer because it was to
> ### hand, and then proved theorems about writers.**

## WHAT THE THEOREMS ACTUALLY SAY

**C-26's argument runs entirely through clause (iv)'s trace balance and clause (iii)'s degeneracy —
properties of HOW A RECORD IS FLIPPED.** It contains nothing about relations between distinct records.

| | |
|---|---|
| **C-24 / C-25 / C-26 prove** | **a flat set of WRITERS always exists and is always selected** |
| **they do not touch** | **whether transport BETWEEN records is flat** |
| **H-9 asked** | **the second one** |

**THE NEGATIVE STANDS AS A FACT ABOUT WRITERS AND DOES NOT ANSWER THE CRITERION.** Its scope is
narrowed accordingly, and **"under the five clauses Γ does not produce gravity" is WITHDRAWN as
stated** — it was proved of the wrong object.

## THE SAME FAILURE AS T-6, TWICE IN ONE SESSION

**T-6:** a zero appeared (records compose without disturbance) and the registrar read it as flatness.
**Here:** a zero appeared (writers commute) and the registrar read it as no record-level curvature.
**Both times the tell was identical — a zero of the WRONG THING, taken for a zero of the right one.**

> ### **D-14. A ZERO IS ONLY A RESULT IF IT IS A ZERO OF THE OBJECT THE QUESTION NAMES. Before
> ### reporting one, state which object the question asked about and check that it is the one
> ### measured. TELL: a null answering a question whose nouns do not appear in the measurement.**

## WHAT THE RIGHT OBJECT MIGHT BE — A THEORY DECISION, NOT A COMPUTATION

The one inter-record structure this program has that is **ours** rather than borrowed is the
**intersection pairing**, and **G-16 showed it is OPERATIVE** — it decides which couplings open a
channel to which record. **A pairing between record classes has the shape of a connection between
records, where the writer never did.**

| candidate | provenance |
|---|---|
| **the intersection pairing `⟨c_i,c_j⟩` on record classes** | **OURS**, operative (G-16), already measured |
| **the channel structure** — which couplings serve which records | **OURS** (T-6's `channel_map`) |
| **transport along the carrier** — records are cycles; carry a frame between them through the complex | closest to H-9's *"nearby"*; where geometry could genuinely live |

**Whichever is chosen DEFINES what "record geometry" means, so it is put to the principal rather than
picked. Picking wrongly again would only produce another theorem about the wrong object.**

---

# **THE PRINCIPAL FIXES THE CONNECTION — CANDIDATE 3, TRANSPORT ALONG THE CARRIER**

**H-14 is decided, with reasons, and the other two candidates are not discarded but ASSIGNED.**

| candidate | role | why not curvature |
|---|---|---|
| **1. intersection pairing** `⟨c_i,c_j⟩` | **TOPOLOGICAL SOURCE**, `T_μν` | **topologically rigid and metric-blind** — it does not change under continuous deformation, and **curvature must vary across paths** |
| **2. channel_map** | **METRIC / PROPAGATOR**, `g_μν` | it is **adjacency** — the causal graph and transmission capacities. **Curvature is what happens to an internal state MOVING ACROSS that adjacency, not the adjacency** |
| **3. carrier transport** | **CURVATURE**, `G_μν` | **curvature IS the obstruction to integrability**: carry a frame around a closed loop of carrier edges and measure its failure to return |

> ### **`R[carrier frame transport]` ∝ `⟨c_i,c_j⟩` × `channel_map[α]`**
> ### **The three are not competing for one slot. They are the three terms of an emergent field equation.**

**Candidate 3 gives the theory a genuine notion of "nearby", spatial extension, and path-dependent
memory; Candidate 1 ensures curvature is sourced by persistent non-local topological records rather
than by arbitrary background.**

## **AND IT IS ALREADY IN OUR CARRIER**

**D-1 check first: the classical form is used to say WHAT THE OBJECT IS, never as the test.** The test
is whether **our** transport closes. That is the line X-6 crossed and this does not.

**Our carrier is a lattice gauge theory: the gauge field lives ON THE LINKS. A link variable IS a
connection variable, and transport around a face IS the plaquette operator `B_p`.** Regge calculus and
lattice gauge theory are the standard language for exactly this, and per the principal's standing
instruction, **using established physics is expected.**

> ### **SO CARRIER CURVATURE IS ALREADY DEFINED IN THIS PROGRAM AND HAS NEVER BEEN LOOKED AT: it is
> ### the plaquette holonomy, and the code space is the sector where every plaquette is satisfied.**

**The immediate question this raises, and it inverts the expectation:** the code space is defined by
`B_p = +1` for every `p`, which is **exactly zero holonomy around every face.** If records live only
there, then **a record does not source curvature — it requires FLATNESS.** Measured next.

---

## H-15 — **CARRIER CURVATURE AND RECORD CONTENT ARE INDEPENDENT. MEASURED ON THE RIGHT OBJECT.**

`LANE_H15_CARRIER`. The connection is **Candidate 3** as the principal fixed it: transport along the
carrier, which in a lattice gauge theory is the **plaquette holonomy** — link variables are connection
variables and a face's holonomy is `B_p`.

### 1. THE CARRIER IS EXACTLY FLAT WHERE RECORDS LIVE

`⟨B_p⟩ = 1.00000000` on all four faces of the code space.

### 2. RECORDS SURVIVE ON A CURVED CARRIER, UNCHANGED

| sector | dim | curved faces | `Z̄` a record? | `Z̄₂`? |
|---|---|---|---|---|
| flat — the code space | 4 | 0 | **YES** | **YES** |
| two fluxes | 4 | **2** | **YES** | **YES** |
| two fluxes, apart | 4 | **2** | **YES** | **YES** |
| **all four faces curved** | 4 | **4** | **YES** | **YES** |

**Record count is 4 in every sector.** A maximally curved carrier carries the same records as a flat one.

### 3. RECORD CONTENT SOURCES NO CURVATURE

Writing `Z̄`, `Z̄₂`, or both leaves **every** holonomy at `1.00000`.

> ### **CURVATURE AND RECORD CONTENT ARE INDEPENDENT IN BOTH DIRECTIONS ON THIS CARRIER. Records do
> ### not source curvature; curvature does not touch records. THE TRIAD'S PROPORTIONALITY HAS
> ### COEFFICIENT ZERO HERE.**

### A BIANCHI-LIKE CLOSURE IS PRESENT — AND UNCOUPLED

`‖∏_p B_p − I‖ = 0.000e+00`. **Every link lies in exactly two faces, so the number of curved faces
must be EVEN: a single flux is forbidden by the carrier itself.** That is precisely H-9's *"record
curvature cannot appear or disappear arbitrarily; it must be constrained by the surrounding incidence
structure."*

> ### **THE CLOSURE SIGNATURE THE PRINCIPAL NAMED IS THERE. It is a property of the CARRIER's
> ### incidence structure and it is not coupled to record content.**

### A CONSTRUCTION ERROR, RECORDED

v1 tried to flip **one** plaquette and got a sector of **dimension 0**. That was not a null — it was
the constraint above, and the script reported an empty sector rather than the fact producing it.
**Fixed: fluxes are flipped in pairs.**

### WHAT THIS DOES AND DOES NOT SETTLE

**It is the first measurement of the object H-9 actually names**, and on the toric carrier the answer
is independence. **It does NOT close the emergence question**, because the toric code's abelian `Z₂`
gauge field has holonomies in `{±1}` — **a sign, and a sign carries no frame rotation.** A carrier
whose link variables take values in a group with genuine internal structure would give the transport
something to rotate. **That is where H-9's "phase/frame mismatch" could live, and it has not been
tested.** Registered as **O-29**.

---

## O-29 — **THE PROGRAM'S ENTIRE NEGATIVE RECORD ON EMERGENCE WAS MEASURED WHERE THE EFFECT IS ZERO BY CONSTRUCTION.**

`LANE_O29_NONABELIAN`. The principal, mid-run: *"Again we realize that we're trying to find where
gravity emerges from the record surface."* **Emergence means the property belongs to the COLLECTION
and to no single member. Every measurement in this program had been taken on ONE record's
neighbourhood.** The object the question names is **transport BETWEEN records**, which requires at
least two records to exist at all.

### 1. A CARRIER WHERE CURVATURE CAN APPEAR

Every carrier built here has gauge group `Z₂`, whose holonomies are `±1` — **a sign, which cannot
rotate a frame.** And `Z_N` would not have helped: on the minimal torus the plaquette holonomy is the
**group commutator** `g₁g₂g₁⁻¹g₂⁻¹`, trivial for **any** abelian group, `U(1)` included. **Only a
non-abelian group gives non-trivial carrier curvature on a torus.** Smallest is `S₃`, Hilbert space
`|G|^edges = 36`.

| sector | configurations | **record classes** |
|---|---|---|
| **flat** (holonomy `= e`) | 18 | **8** |
| **curved** | 18 | **3** |

Curvature is a **group element**, and **transport disagrees with itself in 18 of 36 configurations.**
Curvature also changes what the carrier can hold, 8 classes against 3 — **the first non-trivial
curvature/record coupling in the program.**

### 2. TRANSPORT BETWEEN RECORDS — WHICH SIGNATURES DISCRIMINATE

A record transported around a record `h` returns conjugated, `g → h g h⁻¹`.

| signature | `Z₂` | `S₃` | discriminates? |
|---|---|---|---|
| record comes back changed | **0 / 4** | **18 / 36** | **YES** |
| order of encirclement matters | **0 / 8** | **54 / 216** | **YES** |
| each added record contributes | **0 / 8** | **108 / 216** | **YES** |
| closure fraction | 2 / 4 | 6 / 36 | no |
| last record determined | `[1]` | `[1]` | no |

> ### **ON AN ABELIAN CARRIER, TRANSPORT BETWEEN RECORDS IS THE IDENTITY. A record taken around
> ### another COMES BACK UNCHANGED, ALWAYS. THAT SINGLE FACT EXPLAINS EVERY NULL THIS PROGRAM HAS
> ### RECORDED ON THE EMERGENCE QUESTION — THEY WERE NOT EVIDENCE AGAINST EMERGENCE, THEY WERE
> ### MEASURED WHERE THE EFFECT IS IDENTICALLY ZERO BY CONSTRUCTION.**

> ### **ON A NON-ABELIAN CARRIER THE RECORD COMES BACK CHANGED, THE ORDER OF ENCIRCLEMENT MATTERS,
> ### AND EACH ADDITIONAL ENCLOSED RECORD CHANGES THE OUTCOME. PATH-DEPENDENT TRANSPORT BETWEEN
> ### RECORDS IS PRESENT — AND IT BELONGS TO THE SET OF RECORDS, NOT TO ANY ONE OF THEM.**

### 3. WHAT DOES **NOT** DISCRIMINATE, AND WHAT IS ABSENT

Closure holds at fraction `1/|G|` on **both** carriers, and "given all but one, the last is
determined" returns `[1]` on **both** — that is the group inverse `z = p⁻¹`, true in any group.
**Neither is an emergence signature; both are properties of being a group at all.**

**A MONOTONE DENSITY LAW IS ABSENT.** Reachable outcomes are bounded by the conjugacy class,
`|class| = 3` on `S₃`, so *"more records → more transport"* **cannot** be seen on a group this small.
**H-4's small-carrier warning, not a null.** Registered as **O-30**.

### ERRATA, LOGGED

- **v1 READ claimed the change GROWS with enclosed records** while its own table showed `3, 3, 3` —
  saturated. The claim contradicted the data printed directly above it.
- **v1 item 4 formed the unordered product of every group element** — not well-defined for a
  non-abelian group, and not a measurement.
- **v2 READ called closure "THE STRONGEST RESULT"** when item 5 returns `[1]` for `Z₂` as well.
  **A signature that gives the same answer on the control discriminates nothing.** `Z₂` is now
  carried as an explicit control column in every row.

---

## O-30 — **A COUNT OF RECORDS IS THE WRONG DENSITY VARIABLE. TRANSPORT MIXES; IT DOES NOT ACCUMULATE.**

`LANE_O30_DENSITY`. H-9 names *"stronger with enclosed record-density."* O-29 read exactly 50% at
every `k`, and that is not a small-carrier artifact — **the product of independent uniform group
elements is uniform in any group**, so uniformly-drawn records can never show a density law. The
enclosed records must be **of one kind** (one conjugacy class), which is also the physically right
condition: mass density is a lot of the **same** stuff.

`T(k)` = fraction of records that come back changed when `k` records of one kind are enclosed.

| carrier | order | `T(1)` | `T(2)` | `T(3)` | `T(4)` | … | subgroup generated | **mixing limit** | time-average |
|---|---|---|---|---|---|---|---|---|---|
| **`Z₂`** (control) | 2 | **0** | **0** | **0** | **0** | 0 | 1 of 2 | 0.0000 | **0.0000 ✓** |
| **`Z₄`** (control) | 4 | **0** | **0** | **0** | **0** | 0 | 1 of 4 | 0.0000 | **0.0000 ✓** |
| **`Z₆`** (control) | 6 | **0** | **0** | **0** | **0** | 0 | 1 of 6 | 0.0000 | **0.0000 ✓** |
| `S₃` | 6 | .6667 | .3333 | .6667 | .3333 | ↔ | 6 of 6 | 0.5000 | **0.5000 ✓** |
| `D₄` | 8 | .5000 | .0000 | .5000 | .0000 | ↔ | **4 of 8** | 0.2500 | **0.2500 ✓** |
| `A₄` | 12 | .7500 | .7500 | .5000 | .7500 | ↺3 | 12 of 12 | 0.6667 | **0.6667 ✓** |
| `S₄` | 24 | .8750 | .6875 | .7812 | .7344 | → | **12 of 24** | 0.7500 | **0.7502 ✓** |
| `S₅` | 120 | .9667 | .9167 | .9507 | .9327 | → | 120 of 120 | 0.9417 | **0.9417 ✓** |

> ### **ON EVERY ABELIAN CONTROL, `T(k) = 0` AT EVERY `k`. NO AMOUNT OF ENCLOSED RECORD DENSITY
> ### PRODUCES ANY TRANSPORT AT ALL — THE DENSITY QUESTION DOES NOT ARISE THERE.**

> ### **ON EVERY NON-ABELIAN CARRIER, `T(k)` DOES NOT GROW. IT CONVERGES TO THE MIXING LIMIT —
> ### PREDICTED EXACTLY AND MATCHED ON 8 OF 8 CARRIERS. THE `k`-TH ENCLOSED RECORD DOES NOT ADD
> ### TRANSPORT; IT RANDOMISES IT.**

### WHY, AND WHY THIS IS NOT A SMALL-CARRIER ARTIFACT

Records of one kind perform a **random walk on the subgroup that kind generates**, and that walk
**mixes**. The limit is therefore a derived number, `1 − |{(a,g) : a ∈ H, g ∈ G, ag = ga}| / (|H||G|)`,
**checked against measurement on all 8 carriers**, at orders from 2 to 120. The walk is **periodic,
not ergodic** — period 2 on `S₃` and `D₄`, period 3 on `A₄` — so the limit is the **time average**;
a two-step mean is the wrong average and was corrected.

**And there is a ceiling.** One kind of record generates only a **subgroup**: `S₄`'s 8-element class
generates `A₄`, order 12 of 24; `D₄`'s 2-element class generates order 4 of 8. **Records of a single
kind cannot reach arbitrary transport at all.**

> ### **H-9's DENSITY SIGNATURE IS ABSENT FROM THE COUNTING OF RECORDS. Gravity's defining feature
> ### is that it GROWS with the amount enclosed; transport between records CONVERGES instead. This
> ### is a proved statement about the counting variable, not a null from a carrier that is too small.**

### WHAT IT LEAVES STANDING

C-30 is untouched: **transport between records exists and is path-dependent on a non-abelian
carrier**, and it belongs to the set of records. What fails is **`count` as the source term.** The
principal's own triad names a different one — `R ∝ ⟨c_i,c_j⟩ × channel_map[α]`, whose source is the
**intersection pairing**, not a count. **That is the next measurement**, registered as **O-31**.

---

## O-31 — **BOTH CANDIDATE SOURCE TERMS ARE TOPOLOGICAL, AND A TOPOLOGICAL QUANTITY CANNOT BE A DENSITY.**

`LANE_O31_PAIRING`. C-32 removed the count. The principal's triad names the **intersection pairing**
instead — `R ~ ⟨c_i,c_j⟩ × channel_map[α]`.

### 0. SELF-CHECK, WHICH FIRED

Every `Z` string meets every star evenly, every `X` string meets every plaquette evenly, and the
pairing matrix over the four records has **determinant 1 mod 2 at every `L`** — genuine logical
operators, non-degenerate symplectic pairing.

### 1. A SCOPE CORRECTION TO C-29

| `L` | links | `⟨Z₁,X₁⟩` | `⟨Z₂,X₂⟩` | `⟨Z₁,X₂⟩` | `⟨Z₂,X₁⟩` | |
|---|---|---|---|---|---|---|
| 2 | 8 | **1** | **1** | 0 | 0 | **ANTICOMMUTE** |
| 3 | 18 | **1** | **1** | 0 | 0 | **ANTICOMMUTE** |
| 4 | 32 | **1** | **1** | 0 | 0 | **ANTICOMMUTE** |
| 5 | 50 | **1** | **1** | 0 | 0 | **ANTICOMMUTE** |
| 6 | 72 | **1** | **1** | 0 | 0 | **ANTICOMMUTE** |

> **THE PAIRING BETWEEN RECORD OPERATORS IS NON-ZERO ON AN ABELIAN CARRIER.** C-29 is narrower than
> it may read — it concerns **conjugation of fluxes only**, and stands. **The intersection pairing
> was present on every `Z₂` carrier the whole time.**

### 2. IT DOES NOT GROW WITH EXTENT

| `L` | 2 | 3 | 4 | 5 | 6 | 8 | 10 | **16** |
|---|---|---|---|---|---|---|---|---|
| carrier length | 2 | 3 | 4 | 5 | 6 | 8 | 10 | **16** |
| **shared links** | **1** | **1** | **1** | **1** | **1** | **1** | **1** | **1** |

**The record carriers get 8× longer and the crossing number does not move.**

### 3. IT DOES NOT GROW WITH RECORD COUNT

| genus `g` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| records `2g` | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 |
| non-zero pairings | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| pairs available | 1 | 6 | 15 | 28 | 45 | 66 | 91 | 120 |
| **fraction interacting** | 1.000 | .3333 | .2000 | .1429 | .1111 | .0909 | .0769 | **.0667** |

Non-zero pairings grow **linearly** while pairs grow **quadratically** — the interacting fraction
**falls toward zero.**

> ### **BOTH CANDIDATE SOURCE TERMS FAIL THE SAME TEST FOR THE SAME REASON: THEY ARE TOPOLOGICAL, AND
> ### A TOPOLOGICAL QUANTITY DOES NOT KNOW HOW MUCH IS ENCLOSED. WHATEVER SUPPLIES GRAVITY'S DENSITY
> ### LAW AT THE RECORD LEVEL IS NEITHER A COUNT NOR AN INTERSECTION NUMBER.**

The principal named this shape already: the pairing is **topologically rigid and metric-blind** — a
source `T_μν`, and a source is not by itself a density law. **The one factor in the triad still
untested is `channel_map[α]` — the metric, and the only factor in the whole construction that carries
a MAGNITUDE rather than an invariant.** Registered as **O-32**.

### ERRATUM, LOGGED

**v1 paired the horizontal `Z` loop with a string on VERTICAL links** — disjoint from it — so every
crossing number printed `0`, and the READ then concluded *"the pairing was never zero here"*,
**contradicting the table directly above it.** The non-degeneracy self-check now in section 0 fires
on exactly this: a set of logicals whose pairing matrix is singular is not a basis, and v1's was
identically zero.

---

## O-32 — **THE DENSITY VARIABLE IS RECORDS PER ENVIRONMENT SITE. THE FIRST MAGNITUDE IN THIS PROGRAM THAT KNOWS HOW MUCH IS ENCLOSED.**

`LANE_O32_MAGNITUDE`. C-32 and C-35 removed the count and the intersection pairing: both topological,
and **a topological quantity does not know how much is enclosed.** Of the principal's triad only
`channel_map[α]` remained, and `channel_map` is **boolean**. The magnitude is one level down — **χ,
what the environment actually holds** — and the untested variable is that **records share an
environment.**

### 1. THE CURVE, WITH ITS CONTROL IN THE SAME TABLE

`m` records placed on **one** bath site; χ read for record 0. Control: identical carrier, every
record on its **own** site.

| `m` on site 0 | records | **χ CROWDED** | χ SPREAD *(control)* | ratio |
|---|---|---|---|---|
| 1 | 1 | 0.789366 | 0.789366 | 1.0000 |
| 2 | 2 | **0.164650** | 0.789366 | 0.2086 |
| 3 | 3 | **0.081033** | 0.789366 | 0.1027 |
| 4 | 4 | **0.081489** | 0.789366 | 0.1032 |

**The control moves by 0.000000 across the whole range.**

### 2. IT IS SHARING, NOT CARRIER SIZE

Spectator records enlarge the carrier without crowding the site:

| spectators | 0 | 1 | 2 |
|---|---|---|---|
| records | 2 | 3 | 4 |
| **χ(record 0)** | **0.164650** | **0.164650** | **0.164650** |

**Unmoved to six decimals.**

### 3. IT IS A CAPACITY CEILING, NOT A WEAK COUPLING

χ time-averaged over 25 times in `[1,13]` — a single snapshot is not interpretable, and at fixed
`t = 4.0` the `λ = 0.6` point read `0.001000`, a **recurrence** of unitary evolution rather than a
coupling effect.

| `λ` | 0.20 | 0.40 | 0.60 | 0.80 | 1.00 | 1.40 |
|---|---|---|---|---|---|---|
| **crowded** | .0698 | .1256 | .1373 | .1364 | .1318 | **.1190** |
| **spread** | .0927 | .2766 | .4354 | .5215 | .5856 | **.6012** |
| **ratio** | .7530 | .4541 | .3153 | .2616 | .2250 | **.1980** |

**Crowded χ saturates near 0.135 and stops while spread χ climbs to 0.60. The suppression
STRENGTHENS with coupling across a 7× range.**

> ### **THE DENSITY VARIABLE IS RECORDS PER ENVIRONMENT SITE. NOT THE NUMBER OF RECORDS — ADDING
> ### RECORDS CHANGES NOTHING. NOT THE SIZE OF THE CARRIER — SPECTATORS CHANGE NOTHING. SHARING IS
> ### THE WHOLE EFFECT.**

> ### **AN ENVIRONMENT SITE HOLDS A BOUNDED AMOUNT ABOUT THE RECORDS WRITTEN ON IT, AND RECORDS
> ### SHARING A SITE SPLIT IT. THIS IS THE FIRST QUANTITY IN THIS PROGRAM THAT KNOWS HOW MUCH IS
> ### ENCLOSED RATHER THAN MERELY WHAT IS WHERE.**

### WHAT IT IS NOT

**A suppression law, not yet a transport law.** Nothing here has been shown to curve anything or to
move a record. What it supplies is the ingredient the topological quantities could not: **a magnitude
that responds to enclosed density.** Joining it to transport is **O-33**.

### ERRATUM, LOGGED

**v1 coupled each record through `X_j`** — the operator that **flips** the record rather than
recording it. **Every χ came back `0.000000`, including the control**, so nothing was measurable.
The program's own `channel()` criterion states the requirement: a coupling opens a channel iff its
compression has a component **along** the record. `channel()` is now asserted as a **precondition**
before any χ is read, so that failure cannot be reported as a result.

---

## O-33a — **THE ABELIAN JOIN: THE PAIRING DOES NOT SIT BESIDE THE MAGNITUDE, IT MODULATES IT.**

`LANE_O33_JOIN`. The principal chose **both joins in parallel, with the non-abelian one as the
necessary theoretical destination.** This is the abelian half. Carrier `[[4,2,2]]`, stabiliser
Hamiltonian so the code space is the ground space, **logicals COMPUTED by `symplectic_logicals`** —
never nominated. χ time-averaged over 25 times in `[1,13]`.

Record `A0` is read. Partners: `A1` **(pairing 0, commutes)** and `B0` **(pairing 1, anticommutes)**.

### (a) DISTURBANCE IS THE PAIRING, AND IT IS SITE-BLIND

partner written on **another** site — so nothing here is crowding:

| `λ` | `A1` spread/alone *(pairing 0)* | `B0` spread/alone *(pairing 1)* |
|---|---|---|
| 0.40 | **1.000000** | 0.854301 |
| 0.80 | **1.000000** | 0.810276 |
| 1.20 | **1.000000** | 0.800345 |

**A commuting partner on another site does nothing, to six decimals, at every coupling. A pairing
partner suppresses the record no matter where it sits.** This is C-34's topological pairing doing
exactly what a topological quantity does: **it says WHO interacts and knows nothing about where.**

### (b) CROWDING IS THE DENSITY, AND IT IS SELECTIVE

what **sharing the site** costs on top of that — crowded/spread:

| `λ` | `A1` crowded/spread *(pairing 0)* | `B0` crowded/spread *(pairing 1)* | difference |
|---|---|---|---|
| 0.40 | **0.4541** | 0.7733 | 0.319174 |
| 0.80 | **0.2616** | 0.6013 | 0.339728 |
| 1.20 | **0.2127** | 0.5389 | 0.326168 |

> ### **SHARING A SITE WITH A COMMUTING PARTNER COSTS FAR MORE THAN SHARING IT WITH A PAIRING
> ### PARTNER — BY ABOUT 0.33 IN RATIO, STABLE ACROSS A 3× RANGE OF COUPLING. TWO RECORDS THAT
> ### ALREADY INTERACT THROUGH THE PAIRING COST EACH OTHER *LESS* WHEN THEY SHARE AN ENVIRONMENT
> ### SITE THAN TWO THAT DO NOT.**

> ### **SO THE TRIAD'S PRODUCT IS REAL IN THE SENSE THAT MATTERS: `⟨c_i,c_j⟩` SELECTS WHO INTERACTS,
> ### THE DENSITY SAYS WHAT A SHARED SITE COSTS, AND THE FIRST CHANGES THE SECOND. THE PAIRING
> ### MODULATES THE MAGNITUDE. MEASURED ON AN ABELIAN CARRIER, WHERE NO FRAME ROTATION EXISTS.**

### WHAT IT IS STILL NOT

**Nothing here transports anything.** The join is between a **source** and a **magnitude**, not yet
between either and C-30's **path-dependent transport** — which exists only on a non-abelian carrier.
That is O-33b and it remains the destination.

### ERRATUM, LOGGED — THE SELF-CHECK FIRED FIRST

`symplectic_logicals` returns a **list of conjugate pairs** `[(X_i,Z_i), …]`, not two lists.
Unpacking it as `Xs, Zs = …` mixed the two pairs, and the symplectic self-check printed
`⟨X1,Z1⟩ = 0` and `⟨Z1,Z2⟩ = 1` and halted before any χ was read. **That is the fifth time this
program has gone wrong on logical operators and the fifth time a self-check caught it before a
number was reported.**

**And a second confound was caught in analysis:** the first ratio panel compared crowded against
**alone**, which conflates two mechanisms — the pairing partner suppresses the record from a
*different* site, so part of that ratio was never crowding. Separating disturbance
(spread/alone) from crowding (crowded/spread) is what made the effect legible; the conflated panel
understated the selectivity as 0.226 where it is 0.340.

---

## AUDIT 1 — **C-36 IS THE HOLEVO BOUND. THE TOOL MADE AN ORDINARY EFFECT LOOK NOVEL.**

`LANE_AUDIT_TOOLS`. The principal, mid-run: *"are we sure that we're using the right tools."* Every
measurement behind C-36 used a bath site of **one qubit**, and a qubit holds one bit — so *"records
sharing a site split its capacity"* may be nothing but that. **The discriminator was never run:
vary the site dimension.**

| `s` qubits/site | site dim | **χ CROWDED** | χ SPREAD | `χ(R0)+χ(R1)` | `≤ s` bits? |
|---|---|---|---|---|---|
| 1 | 2 | **0.133478** | 0.525916 | 0.266957 | **True** |
| 2 | 4 | **0.267223** | 0.731135 | 0.534445 | **True** |
| 3 | 8 | **0.336940** | 0.852175 | 0.673879 | **True** |

> ### **THE CEILING RISES WITH SITE DIMENSION AND THE SUM OVER RECORDS IS BOUNDED BY THE SITE'S BITS
> ### IN EVERY ROW. C-36 IS THE HOLEVO BOUND — CONVENTIONAL PHYSICS, CORRECTLY APPLIED, AND NOT A
> ### DISCOVERY OF THIS PROGRAM. IT IS RESCOPED ACCORDINGLY.**

**One qubit per site is a venue where capacity and density are indistinguishable.** One line of the
experiment — vary the site — separates them immediately, and it was never run. **This is the same
failure as O-29's abelian carriers: a measurement taken where two explanations cannot be told apart,
reported as though it distinguished them.**

### WHAT SURVIVES, AND IT IS THE MORE INTERESTING RESULT

**Pure capacity splitting depends only on HOW MANY records share the site.** O-33a measured a
difference of **0.33** in the crowding cost depending on whether the partner **pairs** with the
record — at **fixed** record count and **fixed** site. **Capacity alone cannot produce that.**
**C-39 is not explained by this audit and stands.** So does C-38: a commuting partner on another
site leaves χ at `1.000000`, which is not a capacity statement at all.

### ROWS CORRECTED

- **C-36** — rescoped: the bounded amount is the site's Holevo capacity; the claim is conventional.
- **C-37** — **WITHDRAWN as stated.** χ per record does vary with records per site, but the variation
  is the Holevo bound, so calling it *"the first quantity in this program that knows how much is
  enclosed"* claimed novelty for a standard result. **What is left of the intent is C-39**, where the
  pairing modulates a cost that capacity alone would leave flat.

---

## AUDIT 2 — **THE `S₃` "RECORDS" ARE NOT RECORDS. I CONFLATED THE RECORD WITH THE EXCITATION.**

`LANE_AUDIT_TOOLS`. O-29 and O-30 called conjugacy classes and gauge classes *"records"* and measured
transport between them. **That identification was imported from lattice gauge theory and never
checked against the five clauses.**

### THE `D(S₃)` CARRIER HAS NO RECORDS AT ALL

Built as an actual Hamiltonian: `H = −(A + B)`, gauge projector rank 11, flatness projector rank 18,
`dim = 36`. **Ground space dimension 8 — matching the 8 gauge classes counted group-theoretically in
O-29, so that identification cross-checks.** But:

| carrier | eigenspace multiplicities | any odd? | per-eigenspace best `\|Tr(P_E R)\|` | worst | **(iv) possible?** |
|---|---|---|---|---|---|
| **`D(S₃)` minimal torus** | **[8, 13, 15]** | **True** | **[0, 1, 1]** | **1** | **NO** |
| `[[4,2,2]]` *(control)* | [4, 8, 4] | False | [0, 0, 0] | 0 | **yes** — 1260 records |

Clause (i) forces `R² = I`, so every eigenvalue of `R` is `±1` and `Tr(P_E R) ≡ dim(E) (mod 2)`.
**An eigenspace of odd dimension can never give zero, so clause (iv) — writability — is
unsatisfiable.**

> ### **NO RECORD EXISTS ON THE MINIMAL-TORUS `D(S₃)` CARRIER. O-29 AND O-30 MEASURED TRANSPORT
> ### BETWEEN OBJECTS THAT ARE NOT RECORDS BY THIS PROGRAM'S DEFINITION.**

### THE CONFLATION, NAMED

**A record is a logical operator. A flux is an excitation.** They are different objects and I used
one word for both. Conjugation `g → hgh⁻¹` transports **fluxes**. The program's records are **Wilson
loops**, and their pairwise structure is the **symplectic pairing** — which C-34 measured and found
**non-zero on abelian carriers.**

**So O-29's headline was too strong.** *"Every null this program recorded on the emergence question
was measured where the effect is zero by construction"* is true of **flux conjugation** and false as
stated of **records**: the pairing between records was never zero on any `Z₂` carrier.

### ROWS RESCOPED

- **C-29** → about **flux conjugation**, not records. The mechanism (conjugation is trivial in an
  abelian group) stands; the word did not.
- **C-30** → about **flux transport** on a non-abelian **group**, not about records on a carrier.
- **C-32, C-33** → statements about **group elements of one conjugacy class**, not about records.
  The mixing-limit arithmetic is unaffected and still matches 8 of 8.
- **O-29's headline claim** → **rescoped**: the venue error is real for flux transport and does not
  extend to records, whose pairing was non-zero throughout.

### WHAT SURVIVES UNTOUCHED — EVERY ROW MEASURED ON GENUINE RECORDS

**C-34** (pairing non-zero on an abelian carrier, symplectic matrix non-degenerate at every `L`),
**C-35** (neither count nor crossing number can supply a density law), **C-38** (a commuting partner
on another site leaves χ at `1.000000`), **C-39** (the pairing modulates the crowding cost by 0.33,
stable across a 3× coupling range). **All four used `[[4,2,2]]` or the toric code, where
`model.records()` returns 1260 and the clauses are met.**

### IT IS A CARRIER DEFECT, NOT A VERDICT ON NON-ABELIAN CARRIERS

The minimal torus has **one vertex and one face**, so the gauge and flatness projectors have almost
nowhere to act — **H-4 again**. Whether a larger `S₃` complex has even multiplicities is a question
about **that carrier**, not about `S₃`. Registered as **O-35**.

---

## O-35 — **THE OBSTRUCTION IS NOT NON-ABELIANNESS. IT IS WHETHER `|G|` IS A POWER OF TWO — AND `D₄` IS A NON-ABELIAN CARRIER WITH RECORDS.**

`LANE_O35_NONABELIAN_CARRIER`. AUDIT 2 found `D(S₃)` has no records. **`S₃` is non-abelian AND has
order 6, which is not a power of two — two explanations that `S₃` alone cannot separate.** The
controls that separate them: **`Z₃`, abelian of order 3**, and **`D₄`, non-abelian of order 8 = 2³**.

| carrier | abelian? | order | `V` | `E` | dim | multiplicities | odd? | **records?** |
|---|---|---|---|---|---|---|---|---|
| `Z₂` 1×2 | abelian | 2 | 2 | 4 | 16 | [4,4,4,4] | False | **yes** |
| **`Z₃`** min | **ABELIAN** | **3** | 1 | 2 | 9 | odd present | **True** | **NO** |
| **`Z₃`** 1×2 | **ABELIAN** | **3** | 2 | 4 | 81 | odd present | **True** | **NO** |
| `Z₄` 1×2 | abelian | 4 | 2 | 4 | 256 | all even | False | **yes** |
| **`D₄`** min | **NON-ABELIAN** | **8 = 2³** | 1 | 2 | 64 | all even | **False** | **yes** |
| `S₃` min | non-abelian | 6 | 1 | 2 | 36 | [8,13,15] | True | **NO** |
| `S₃` 1×2 | non-abelian | 6 | 2 | 4 | 1296 | [8,61,394,833] | True | **NO** |

> ### **AN ABELIAN GROUP FAILS IT (`Z₃`) AND A NON-ABELIAN GROUP PASSES IT (`D₄`). THE OBSTRUCTION IS
> ### THE ORDER OF THE GROUP, NOT ITS COMMUTATIVITY: RECORDS EXIST ON `D(G)` EXACTLY WHEN `|G|` IS A
> ### POWER OF TWO, ACROSS 7 CARRIERS AND TWO CARRIER SIZES.**

**Why.** Clause (i) makes a record a **bit**: `R² = I`, so `Tr(P_E R) ≡ dim(E) (mod 2)` and clause
(iv) needs **every** eigenspace even-dimensional. `|G|^E` is a power of two exactly when `|G|` is.
**A group whose order carries an odd factor produces odd eigenspaces, and no record can be written
on it at all.**

> ### **`D₄` IS A NON-ABELIAN CARRIER WITH RECORDS. IT IS PRECISELY WHAT O-34's JOIN NEEDS AND WHAT
> ### `D(S₃)` COULD NOT SUPPLY.**

### THE CONTROL IS WHAT MADE THIS RIGHT

Run on `S₃` alone, this lane would have registered *"non-abelian carriers cannot have records"* —
**which the `D₄` column shows is false.** That is D-15 doing exactly what it was written for, one
lane after it was written.

---

## O-34 — **TRANSPORT MOVES RECORDS ON A NON-ABELIAN CARRIER. THE FIRST TIME A GENUINE RECORD AND NON-TRIVIAL TRANSPORT HAVE MET ON THE SAME OBJECT.**

`LANE_O34_NONABELIAN_JOIN`. O-35 supplied the carrier `D₄` — **non-abelian** (24 of 64 pairs do not
commute) **and** with all eigenspace multiplicities even, so clause (iv) is satisfiable. **`D(S₃)`
had the first property and not the second; every `Z₂` carrier had the second and not the first.**

`model.records()` cannot enumerate at 64 minimal projections (O-28), so records are **constructed on
the eigenspaces and every clause checked**, never assumed.

### THE MEASUREMENT

| carrier | dim | non-commuting pairs | multiplicities | records verified against (i)–(iv) | **moved by transport** | largest `‖[A_h,R]‖` |
|---|---|---|---|---|---|---|
| `D(Z₂)` *(control)* | 4 | **0 / 4** | [4] | **40 of 40** | **0** | **0.000e+00** |
| **`D(D₄)`** | 64 | **24 / 64** | [22,24,18] | **40 of 40** | **40** | **9.423** |

> ### **EVERY RECORD CONSTRUCTED ON THE NON-ABELIAN CARRIER IS MOVED BY SOME GROUP ELEMENT'S
> ### TRANSPORT. ON THE ABELIAN CONTROL, NONE IS — AND THE COMMUTATOR IS EXACTLY ZERO, BECAUSE
> ### CONJUGATION IN AN ABELIAN GROUP IS THE IDENTITY MAP.**

### A SECOND FINDING ALONG THE WAY

The natural Wilson-loop record `R|g₁,g₂⟩ = χ(g₁)|g₁,g₂⟩` for a linear character **is a record on
`D(Z₂)`** — all four clauses check — and on `D(D₄)` gives `Tr(P_E R) = [6, 0, −6]`, so **it is not a
record there.** **Even multiplicities make clause (iv) possible, not automatic.**

### WHAT IS **NOT** DECIDED, AND WHY IT IS SAID PLAINLY

A random eigenspace splitting commutes with little, so *"40 of 40 moved"* could be sampling rather
than structure. **The decisive question — does a transport-FIXED record exist on `D(D₄)`? — is
OPEN.** `o34b_exists.py` attacks it exactly, through the block structure `(d_i, m_i)` of the gauge
commutant, and **fails its own consistency check** on `D(D₄)`: `Σ d_i·m_i = 20` against a
**18**-dimensional eigenspace, and `26` against a **22**-dimensional one. `commutant()` is
sampling-based and an incomplete basis inflates multiplicities exactly this way.

**On the control the same method is consistent and says a transport-fixed record exists — which
agrees with the direct measurement's `0 of 40` and exact zero. That agreement is what makes it
trustworthy where it is consistent, and its failure elsewhere is why no verdict is read from it.**

### ERRATUM, LOGGED

A first attempt decomposed each eigenspace by the eigenvalues of `Σ_h (A_h + A_hᵀ)` and did a
subset-sum on those dimensions. **It reported NO transport-fixed record on `D(Z₂)` — contradicting
the direct measurement four lines above it.** For an abelian group `A_h` **is** the identity, so the
commutant is everything, but a symmetrised sum of identities has one eigenvalue and the method
returned a single coarse block. **The control caught a method that would have inverted the answer.**

---

## SIGN-DEFINITENESS — **THE TEST IS NOT "DOES IT GROW" BUT "DOES IT FAIL TO CANCEL". THE LEADING RECORD QUANTITY SCREENS.**

`LANE_SIGN_DEFINITE`. The principal proposed searching from the other direction: **find the smallest
appearance of gravity and count down.**

### THE COUNT-DOWN, AS ARITHMETIC

The smallest **source** whose gravitational field has been measured is ~90 mg of gold (Westphal et
al., *Nature*, 2021) — `0.090 / 196.97 × 6.022e23 = 2.752e20` atoms. This program reaches `N ≈ 10`.

> **The gap is 19.4 orders of magnitude and no simulation closes it.** `α_G/α_EM = 5.9e-39 / 7.297e-3
> = 8.09e-37`, twenty orders below the `float64` noise floor. **The strength is unreachable; only the
> FORM is testable.**

Note the asymmetry: gravity's **probe** can be a single quantum system (neutron interferometry,
single-ion redshift over 33 cm). Gravity's **source** needs `~10²⁰`.

### BUT THE COUNT-DOWN EXPLAINS *WHY* THE NUMBER IS THAT LARGE, AND THAT IS TESTABLE AT `N = 10`

**Gravity wins at scale not because it grows faster per pair, but because it does not CANCEL.**
Charge comes in two signs and neutralises in bulk; mass has one sign and adds. **So the record-level
signature of a gravity-role quantity is SIGN-DEFINITENESS** — a form property, scale-free.

### THE LEADING TWO-BODY RECORD QUANTITY IS TWO-SIGNED AND CANCELS *MORE* WITH `N`

| records `k` | 2 | 4 | 6 | 8 |
|---|---|---|---|---|
| integer intersection values | `[-2,0,1,2]` | `[-4…4]` | `[-6…6]` | `[-8…8]` |
| Σ | 2 | 8 | 18 | — |
| Σ\|·\| | 6 | 36 | 106 | — |
| **`\|Σ\| / Σ\|·\|`** | **0.3333** | **0.2222** | **0.1698** | — |

> ### **A QUANTITY THAT CANCELS CANNOT DOMINATE AT `10²⁰` CONSTITUENTS, WHATEVER ITS FORM AND HOWEVER
> ### IT SCALES. THE PAIRING SCREENS.**

### THE MEASUREMENT HAD NEVER BEEN POSSIBLE BEFORE

**Every measurement of the pairing in this program was taken over `F₂`, where the values are `{0,1}`
and the question of sign cannot even be posed.** The signed object is the **integer** intersection
number, and it had not been computed. Registered as **D-19**.

### THIS REFINES C-35 RATHER THAN OVERTURNING IT

C-35 ruled the pairing out as a density because it is **topological** — true, and it is why the
pairing does not grow with a record carrier's extent. But the integer values' **range does widen**
with `k`, from `[-2,2]` to `[-8,8]`. **What kills it is not failure to grow. It is cancellation.**

> ### **THE DISCRIMINATOR: A QUANTITY WITH `|Σ|/Σ|·| = 1` ACCUMULATES WITHOUT BOUND HOWEVER SMALL
> ### EACH TERM IS — WHICH IS EXACTLY HOW A `10⁻³⁶` COUPLING WINS AT `10²⁰` CONSTITUENTS.**

The crowding suppression is the live candidate and its sign is genuinely open — sharing an
environment site could constructively help a record as easily as hurt it. Under measurement.

---

## **ONE STRICTLY EXTENSIVE QUANTITY SURVIVES — AND EVERY LANE THAT MEASURED IT MISFILED IT.**

Three probes on the [[n,n−2,2]] family and on products of [[4,2,2]] blocks, each adversarially
verified, testing whether **any** record-level quantity meets gravity's source standard:
**(a)** strictly extensive — `S(2N)/S(N) → 2`, unbounded; **(b)** additive over disjoint regions;
**(c)** not a count and not topological.

### THE QUANTITY: THE BATH-INDUCED EFFECTIVE POTENTIAL ON THE RECORD REGISTER

`Φ(s) = −(1/β) ln Tr exp(−β H_B(s))`, read as `spread(Φ) = max_s Φ − min_s Φ` or `Var(Φ)`.

**(a) STRICTLY EXTENSIVE AT A FIXED ENVIRONMENT** — bath pinned at 8 sites throughout:

| `N` | 64 | 256 | 1024 | 4096 | 16384 |
|---|---|---|---|---|---|
| `spread(Φ)` | 43.43 | 196.49 | 810.76 | 3268.32 | **13098.72** |
| successive ratio | 2.1707 | 2.0418 | 2.0104 | 2.0026 | **2.0013** |

Closed form `λN = 13107.2` against measured `13098.7`. **And `χ_total` DECAYS over the very same
sweep** (4.17 → 5.68e-03) — so this is **not** the "bath grew with the matter" artifact that
disqualified every other linear candidate.

**(b) EXACTLY ADDITIVE OVER DISJOINT REGIONS** — defect `≤ 9.09e-13`, against a **live** shared-site
control in the same table giving defects of **3.71 / 4.11 / 4.21 / 4.23**. The instrument registers
non-additivity when there is some.

**(c) NOT A COUNT** — at **fixed** `N = 24` it varies **8.5×** (spread) and **72.9×** (Var) as region
content changes, and varies smoothly with `λ` while `N` is pinned.

> ### **THIS IS THE FIRST QUANTITY IN THE PROGRAM TO MEET ALL THREE. One lane measured it and
> ### disqualified it as "the count in different units"; another never built it.**

### THE PRICE, STATED PLAINLY

`spread(Φ)` is non-zero **only where records SHARE a bath site** — and sharing is **exactly where
INDEPENDENT WRITABILITY dies.** Verified at `n = 4`: the two records still satisfy (i)–(iv) against
the full joint Hamiltonian (`max|Tr(P_E R_i)| = 1.48e-15`, `‖[H_tot,R]‖ = 0.0e+00`), yet **no
admissible unitary can flip `R₁` while holding `R₂` fixed** (joint-sector dimension mismatch 3.0000,
against 0.0000 in the separate-site control).

### RULED OUT AT ANY `N`, BY FORM — IMMUNE TO THE LARGE-`N` AND THRESHOLD OBJECTIONS

**1. THE ENTIRE ACCESSIBLE-INFORMATION FAMILY.** `Σᵢ χ(Rᵢ:B) ≤ χ_joint = I(S:B) ≤ S(ρ_B) ≤ log₂ dim(B)`
— **independent of `N`.** Established three times independently: 0 violations across 120 points, max
ratio 0.4963; cap 3 bits with observed maxima 1.2145 and 2.1641; the tighter thermal form
`Σⱼ(1−S(τⱼ)) = 2.5182003436` reproduced to all digits by an independent adversary. **This kills
Holevo χ, joint register χ, redundancy, and every mutual-information variant as gravity's source at
any `N`.** It is the Holevo bound plus a finite bath's entropy — C-36 made exact.

**2. `λ_max` OF ANY RELATION MATRIX FAILS ADDITIVITY.** Disjoint regions give a block-diagonal
matrix, so `λ_max` is a **MAX, not a sum** — measured ratio exactly 0.5000 at five matched sizes.
**No growth rate repairs a maximum.**

**3. TOTAL WRITER WEIGHT IS EXACTLY `2N`.** The minimum admissible writer weight is **exactly 2 for
every record at every even `n`** — brute-forced over the *entire* set `N(S)\S` (60, 1020, 16380
records at `n` = 4, 6, 8, all weights searched over every Pauli), plus 4000 random logical classes at
`n` = 12, 16, 20, 30, and reconfirmed to `n = 32` by a second adversary. **So it is C-35's count in
other units.**

**4. THE RECORD-RECORD SYMPLECTIC RELATION MATRIX IS IDENTICALLY ZERO** — independent records commute,
so the pairing lives between a record and its **writer**, never between two records. The
records+writers positive control registers `k` and `λ_max = 1` in the same table.

### WITHDRAWN UNDER ADVERSARIAL VERIFICATION

- **"No quantity satisfies strict extensivity"** — **FALSE**, refuted by `spread(Φ)` above.
- **A claim that clauses (ii)+(iv) alone forbid a record-configuration energy density in any carrier**
  — refuted by explicit `N = 2` counterexample with `spread(Φ) = 0.877985`. **The correct hypothesis
  is INDEPENDENT writability, not (ii)+(iv).**
- **Two fitted decay exponents** (`−0.4638 ± 0.0212`, `−0.2879 ± 0.0090`) — **withdrawn as laws.**
  Local slopes span 1.4055 and the two exponents drift in *opposite* directions with fitting window.
  Under a defensible noise floor the model selection gives `ΔAICc = 0.04` — **the data cannot
  distinguish linear from logarithmic from saturating.**
- **A `N^1.50` "collective effect"** — arithmetic: `C(N,2) ~ N²/2` pairs times a per-pair coupling
  diluted as `N^{−1/2}` by the central limit theorem.

### THE PREDICTION MADE BEFORE THE DATA LANDED WAS CORRECT

Registrar's prediction, stated in-session before this workflow returned: the crowding suppression's
sign-definiteness is **forced** (a partner's unknown value averages the record's channel — concavity
of Holevo under mixing) and is therefore **capacity-bounded and saturating, not extensive.** Result
**1** above confirms it exactly. **The crowding candidate is dead: sign-definite but bounded.**

---

## O-36 — **DECIDED: A TRANSPORT-FIXED RECORD EXISTS ON `D(D₄)`. C-43's "40 OF 40" MEASURED THE SAMPLING PROCEDURE, NOT AN OBSTRUCTION.**

`LANE_O36_EXACT`. Decided exactly by **character theory**, with the character table **computed** from
the class algebra (Burnside/Dixon) rather than hard-coded, and verified on every carrier against
integrality of `dᵢ` (≤ 4.4e-16), `Σdᵢ² = |G|` (exact), row orthonormality (≤ 2.3e-16), column
orthogonality (≤ 1.8e-15), and the regular character's decomposition (≤ 4.4e-16).

| carrier | dim | abelian | commutant blocks | `Σ dᵢmᵢ = dim E`? | **transport-fixed record?** |
|---|---|---|---|---|---|
| **`D(D₄)`** *(target)* | 64 | no | `1×22 ‖ 1×6⁴ ‖ 1×6³` | 22=22, 24=24, 18=18 ✓ | **EXISTS** |
| `D(Z₂)` *(control)* | 4 | yes | `1×4` | ✓ | EXISTS, `‖[A_h,R]‖ = 0.000e+00` |
| `D(Z₂×Z₂)` | 16 | yes | `1×16` | ✓ | EXISTS |
| `D(Z₄)` | 16 | yes | `1×16` | ✓ | EXISTS |
| `D(Q₈)` | 64 | no | identical to `D₄` | ✓ | EXISTS, `1.9e-14` vs blind control **8.998** |
| **`D(D₈)`** `\|G\|=16` | 256 | no | **`2×12`, `2×36` blocks occur** | 46=46, 84=84, 126=126 ✓ | **EXISTS**, `4.7e-13` vs blind **20.43** |
| **`D(Z₃)`** *(negative control)* | 9 | yes | `1×9` | ✓ | **NO** — dim 9 odd, `0` unreachable |

### THE CORRECTION TO C-43

> ### **AT MATCHED SAMPLE SIZE: 40 OF 40 TRANSPORT-*BLIND* RECORDS MOVE (max `‖[A_h,R]‖ = 9.466`,
> ### REPRODUCING C-43's 9.423) WHILE 0 OF 40 TRANSPORT-*FIXED* RECORDS MOVE (max `1.2e-12`).**

**C-43's measurement is reproduced exactly and its reading was wrong.** Randomly splitting eigenspaces
produces records that are *blind* to transport; it does not show that transport must move a record.
**Transport-fixed records exist, and are constructible.**

**Structural reason:** the gauge action is by **conjugation**, so `Z(D₄)` acts as the identity and the
representation factors through `D₄/Z = Z₂×Z₂` — **abelian**, so every commutant block has `dᵢ = 1` and
every even-dimensional eigenspace reaches trace zero. **`D(D₈)` removes that reason** — `D₈/Z = D₄` is
non-abelian and genuine 2-dimensional blocks appear — **and the verdict survives.**

### WHY THE EARLIER ATTEMPT FAILED, MEASURED

`record_model.commutant()` on `D(D₄)` returns **512** basis elements against the exact dimension
`Σmᵢ² = 22² + 4·6² + 3·6² = 736` — **short by 224, because it is capped at `min(8n, 2000) = 512`
samples.** On `D(Z₂)` it returns 16 = exact, **which is why the failure was invisible on the
control.** A short basis does not merely lose dimensions: fitting a block decomposition to it returns
multiplicities violating `Σdᵢmᵢ = dim E` — **exactly the 20-vs-18 and 26-vs-22 that the consistency
check caught.** Character theory has no such failure mode.

### SCOPE LIMITS, AS STATED BY THE LANE

1. **Clause (v) is NOT tested.** A record here means (i)–(iv) plus transport-fixity.
2. **Transport-fixity is VACUOUS on the ground space** — `A_h` acts as the identity on the `A=1`
   eigenspace, so `[A_h,R]=0` is automatic there. **All the content sits in the excited eigenspaces
   `E=−1` (dim 24) and `E=0` (dim 18)** — and zero is reachable there too, which is what makes the
   verdict non-vacuous.
3. **One geometry** — minimal torus, transport meaning the gauge transformations `A_h`. Ribbon
   operators and larger lattices untested.
4. A group with an eigenspace carrying a single odd-multiplicity block of even `d` would fail; **none
   was found among the six tested.**

### THE HYPOTHESIS THIS KILLS

The registrar's in-session chain — *a record is a bit → a bit carries a 1-dim rep → a 1-dim rep is a
class function → records are transport-invariant, so clause (i) explains every null* — **is refuted
as stated.** Transport-fixed records exist, but so do records transport moves. **Bit-ness does not
force transport-invariance; it merely permits it.** That is allow/require again, and the principal's
framing was the correct one.

---

## **THE `Z[i]` QUANTISATION THEOREM — A GRAVITY-STRENGTH RESIDUAL HAS NO SLOT TO LIVE IN. NOT UNRESOLVED: EXCLUDED.**

Three probes in exact arithmetic (integers, `F₂`, `Z₄`, Gaussian integers, `Fraction` — no floats),
each adversarially verified. The principal's governing objection was that gravity is `~10⁻³⁶` of EM,
twenty orders below the `float64` floor, so its magnitude is unreachable at any `N`.

### P1 — THE QUANTISATION THEOREM

A product of record operators on an abelian stabiliser carrier is a **single signed Pauli** `iᵐW(c)`.
`Tr(Π iᵐW(c))/Tr(Π)` is **exactly 0** if `c ∉ S` and **exactly a fourth root of unity** if `c ∈ S`.
By linearity, every Gaussian-integer-coefficient polynomial in record operators has `Π`-trace ratio
in **`Z[i]`** — and **`Z[i]` contains no element of modulus strictly between 0 and 1.**

> ### **THE INTERVAL `(0,1)` IS EMPTY. SUCH A SCALAR IS EXACTLY ZERO OR HAS MODULUS AT LEAST 1.**
> ### **A `10⁻³⁶` RESIDUAL CANNOT LIVE IN THE RECORD ALGEBRA'S SCALAR INVARIANTS — NOT BECAUSE WE
> ### CANNOT RESOLVE IT, BUT BECAUSE THERE IS NO SLOT.**

Swept **40,000 words and integer-coefficient polynomials per `n`** at `n` = 4, 6, 8, 10, 12, 16, 20:
**minimum non-zero modulus² exactly 1 every time; no value with `0 < |v| < 1` ever found.** Proof
valid at every `n` — an exact argument, not a trend.

On `D(G)` the floor is coarser but still bounded away from zero: exact spectral projectors have
denominator `|G|`, so every exact rational lies in `(1/|G|²)Z` — **the witness `352/9` sits exactly on
that lattice.** Polynomially small in `|G|`, never exponentially small. **Again no `10⁻³⁶` slot.**

### P2 — THE SYMPLECTIC-FORM DETERMINATION THEOREM

Record operators of an abelian stabiliser carrier generate a Pauli group over `F₂^{2k}` with **trivial
quadratic refinement** (`W(a)² = I` for all `a`), and such a group is **determined up to isomorphism
by its symplectic form alone.**

> ### **THEREFORE NO SCALAR INVARIANT OF ANY NUMBER OF RECORDS CARRIES INFORMATION BEYOND THE PAIRWISE
> ### `F₂` PAIRING MATRIX.**

Verified exhaustively: **all 1848 gauge-invariant words of length ≤ 8 in three records** — **ZERO**
separate two triples sharing the same pairwise signature (`n=4`, `n=6` exhaustive over the complete
record group; `n=8` on 299 classes). Every word value in `{+1,−1}`.

### NOTHING THREE-BODY EXISTS — AND THE LANE'S OWN CANDIDATE WAS KILLED BY ITS ADVERSARY

One lane proposed **GAP** — the failure of three pairwise minima to be simultaneously realisable — as
*"the one genuinely three-body object, NOT a function of the six pairwise invariants."*

**It is a function of two-body data, exactly.** A routine handed **only the three two-body tables,
all record identity erased**, reproduces GAP with **0 mismatches in 16,000 triples** at `n` = 6, 8,
10, 12. The lane's own test had grouped by a *lossy* summary; re-run with the non-lossy key it gives
**0 multi-valued groups out of 26,986.**

> **GAP is the ground-state frustration energy of three pairwise couplings on a triangle — the
> antiferromagnetic Ising triangle, the textbook case of something that looks three-body and is
> generated entirely by two-body interactions.** Its apparent growth series (0 → 0.9% → 6.3% →
> 10.4% → 17.9% → 23.7%) is a property of the sampling pool.

### WHERE A RESIDUAL CANNOT HIDE — EXACT ZEROS, NOT BOUNDS

Separation dependence, orientation anisotropy, off-site interaction, and carrier-mediated influence
are **identically zero at every `N` by argument** — Clifford transitivity on the code space,
qubit-permutation invariance, the qubit-wise structure of the symplectic form, clause (ii), and the
absence of bath–bath coupling. **Excluded, not unobserved.**

### **THE VENUE OBJECTION THAT REFRAMES EVERY SEPARATION NULL**

> ### **BOTH CARRIERS HAVE FULL QUBIT-PERMUTATION INVARIANCE, SO THEY CONTAIN NO METRIC STRUCTURE TO
> ### DETECT — BY CONSTRUCTION. Non-record operators show the same flatness to `6.4e-16`. The correct
> ### statement is "these carriers have no geometry", NOT "records have no metric form".**

Registered as **D-22**. **Every separation null in three lanes is downstream of this.**

### THE DECISIVE OPEN QUESTION, PROMOTED OUT OF A CAVEAT

**THE DURABILITY–GEOMETRY EXCLUSION.** On a carrier whose record set generates the full logical
algebra, must every `H` satisfying clause (ii) for **all** records act as a **SCALAR** on the
protected subspace? The argument: *a Hamiltonian term that keeps a record durable commutes with it,
hence is diagonal alongside it, hence contributes only a phase; a term that is not diagonal alongside
it destroys clause (ii).*

- **If it is a theorem:** durability and carrier geometry are **mutually exclusive**, no record-record
  interaction can **ever** depend on separation at any `N`, and **gravity is ruled out as a metric
  relation among records permanently** — immune to both the weakness and threshold objections.
- **If it is false:** **every null in three lanes is a venue artifact** and the separation question
  reopens on the right venue, where the `XX`-bath result already shows a falloff is achievable.

Registered as **O-42**. **It is the only claim anywhere in the workflow that is about RECORDS rather
than about a chosen venue, and every null is downstream of it.**

---

## O-42 — **WRITABILITY REQUIRES ENERGETIC NEUTRALITY. GRAVITY REQUIRES ENERGETIC DISTINCTION. A RECORD CANNOT BE BOTH.**

`LANE_O42_EXCLUSION`. Decided exactly — `F₂` linear algebra and integer Pauli arithmetic. **Every
separation null in three workflows was downstream of this question.**

### 1. THE THEOREM DIRECTION IS SCHUR

The symplectic form on `N(S)/S` is **non-degenerate at every `n`** (rank `2k` = 12, 16, 20 at
`n` = 8, 10, 12), so the records generate the **full logical algebra `M_{2^k}`** — whose commutant is
its **centre, the scalars.**

| carrier | dim | code dim | `H\|code` scalar? | max off-scalar |
|---|---|---|---|---|
| `[[4,2,2]]` | 16 | 4 | **True** | **0.000e+00** |
| `[[6,4,2]]` | 64 | 16 | **True** | **0.000e+00** |
| `[[8,6,2]]` | 256 | 64 | **True** | 1.776e-15 |

> **EVERY RECORD CONFIGURATION HAS THE SAME ENERGY. No configuration can cost more than another, so
> no separation can matter — at any `N`.**

### 2. THE ESCAPE WAS ATTEMPTED, AND IT WORKS — UNTIL CLAUSE (iv)

Restrict to a mutually **commuting** Z-type family and build `H` from those records. Clause (iv) does
not require a writer to be a record, so this is legitimate:

| construction | records commute? | `H\|code` scalar? | **energy spread** | durable? |
|---|---|---|---|---|
| `n=4` Z-family | True | **False** | **1.400000** | True |
| `n=6` Z-family | True | **False** | **3.600000** | True |

**Geometry appears.** And then:

| | max `\|Tr(P_E R₀)\|` | required | **clause (iv)** |
|---|---|---|---|
| `n=4` | **2.000** | 0 | **FAILS** |
| `n=6` | **3.000** | 0 | **FAILS** |

> ### **THE RECORDS STOP BEING RECORDS. They are bits, they are durable, they are non-trivial — and
> ### THEY CANNOT BE WRITTEN.**

### THE STATEMENT THIS EXHIBITS

Clause (iv) requires `Tr(P_E R) = 0` on **every** eigenspace of `H` — the record's value must be
**balanced at every energy**. A record that costs energy to hold one way rather than the other has
`Tr(P_E R) ≠ 0` and **is not writable.**

> ### **WRITABILITY REQUIRES ENERGETIC NEUTRALITY. GRAVITY REQUIRES ENERGETIC DISTINCTION.
> ### A RECORD CANNOT BOTH BE WRITABLE AND CARRY A CONFIGURATION ENERGY.**

**This is why C-47's extensive quantity was bought at the cost of independent writability**, and why
every separation and density null in this program came out zero. **They are all the same fact.**

### SCOPE, STATED PLAINLY

The **theorem direction is proved** for any carrier whose records generate the full logical algebra —
Schur, needing no large `N`, immune to both the weakness and threshold objections. **One escape route
was tried and closed exactly.** It is **not** a proof that every escape fails: a carrier whose durable
records generate a **proper subalgebra** *and* still satisfies clause (iv) has not been ruled out by
construction — only not found here. **That is the open edge**, registered as **O-43**.

---

## O-44 — **WHAT FAILS IS NOT WRITABILITY. IT IS *FREE* WRITABILITY. O-42's EXCLUSION IS AN ARTIFACT OF DEF-A.**

`LANE_O44_ADMISSIBLE`. The principal: *"why did we forbid records from carrying configuration energy?
We shouldn't be assuming anything if we're looking for the truth."*

**We did not forbid it deliberately. It follows from one definition:**

| source | text |
|---|---|
| `CORE_FRAMEWORK_V001.md` line 26 | **`ADMISSIBLE U ≝ a unitary with [U,H] = 0`** — (O-4, **PROVISIONAL**) |
| ledger O-4, evidence | *"PROVISIONAL — one carrier family, and DEF-A has NO working fallback"* |
| ledger O-4, item | *"The second disjunct **'or a physical channel' is UNTESTED**"* |

**The derivation uses it essentially.** Clause (iv) gives an *admissible* `U` with `U†RU = −R`. If
`[U,H] = 0` then `U P_E U† = P_E`, so `Tr(P_E R) = Tr(P_E URU†) = −Tr(P_E R)`, hence `Tr(P_E R) = 0`.
**Remove `[U,H] = 0` and nothing forces it. The O-42 exclusion collapses.**

### MEASURED, WITH WRITERS SEARCHED OVER THE FULL PAULI GROUP — NEVER NOMINATED

| carrier | clause (iv) under DEF-A | **admissible writer** | **physical writer** |
|---|---|---|---|
| `H = −(Xⁿ + Zⁿ)` *(control)* | **HOLDS** | **FOUND**, weight 2, `‖[W,H]‖ = 0.000e+00`, cost **+0.000000** | found, weight 1, cost +2.000000 |
| `H = H_stab − Σcᵢ Rᵢ` | **FAILS** (`\|Tr(P_E R)\| = 3.000`) | **NONE EXISTS** in the Pauli group | **FOUND**, weight 1, cost **+2.600000** |

> ### **WHERE THE CARRIER ASSIGNS A CONFIGURATION ENERGY, NO FREE WRITER EXISTS — BUT A PHYSICAL ONE
> ### DOES, AT WEIGHT 1, COSTING `+2.600000` OF WORK. THE RECORD REMAINS A BIT, REMAINS DURABLE,
> ### REMAINS NON-TRIVIAL, AND REMAINS FLIPPABLE BY AN OPERATOR THE SEARCH ACTUALLY FOUND.**

> ### **WHAT FAILS IS NOT WRITABILITY. WHAT FAILS IS *FREE* WRITABILITY.**

**A unitary commuting with `H` does no work on the state's energy.** So DEF-A amounts to requiring
that **writing be free** — and a free write cannot distinguish energies. **Landauer puts the floor on
a real write at `kT ln 2`, not at zero.**

### WHAT THIS DOES AND DOES NOT DO

**It removes a blocker.** Records can carry a configuration energy provided writing is allowed to cost
work — which is what writing costs in the world. **It does not show that gravity emerges.**

**It reopens O-42**, which appeared to close the question permanently. **And it reopens C-47**, whose
extensive quantity was registered as *"bought at the cost of independent writability"* — a cost that,
under the physical reading, is simply **work done.**

### ERRATUM, LOGGED — THE SIXTH TIME ON THIS EXACT FAILURE

**v1 NOMINATED the writer** as an X-string on sites `0..i`, and its READ then asserted the unmodified
write was free with `‖[W,H]‖ = 0` **while the table directly above it printed `1.600e+01` and a cost
of `+2.000000`.** `X₀` flips `Z₀Z₁` but does not commute with `Zⁿ`. **Writers are now searched over
the full Pauli group.** This is the sixth time this program has gone wrong by nominating a
logical or writer operator instead of computing one.

---

## O-47 — **CONFIGURATION ENERGY *AND* ENERGY-CONSERVING WRITERS, TOGETHER. O-42 APPLIED CLAUSE (iv) TO THE WRONG OBJECT.**

`LANE_O47_BOTH`. The principal: *"Why can't we have configuration energy AND defining a writer as an
energy-conserving symmetry?"* **We can.**

**Clause (iv) constrains EACH RECORD — `Tr(P_E Rᵢ) = 0`. It says nothing whatever about the JOINT
CONFIGURATION.** Two records can each be perfectly balanced at every energy while their **correlation**
is definite at each energy — and the correlation is then exactly what carries the energy.

### THE CONSTRUCTION: `H = Z₁Z₂`

| | `H = Z₁Z₂` | `H = 0` *(control)* |
|---|---|---|
| spectrum | `(−1, 2), (+1, 2)` | `(0, 4)` |
| `R₁ = Z₁`: `Tr(P_E R)` per block | **`[0, 0]`** — clause (iv) **HOLDS** | `[0]` — HOLDS |
| `R₂ = Z₂`: `Tr(P_E R)` per block | **`[0, 0]`** — clause (iv) **HOLDS** | `[0]` — HOLDS |
| clause (iii) | holds for both | holds for both |
| **pair correlation `Z₁Z₂` per block** | **`[−1, +1]` — DEFINITE AND DIFFERENT** | `[0]` — carries nothing |
| admissible writer for `R₁` | **FOUND**, weight 2, `‖[W,H]‖ = 0`, **cost +0.000000**, does **not** change the pair | found, weight 1, free, **does** change the pair |
| admissible writer for `R₂` | **FOUND**, weight 2, `‖[W,H]‖ = 0`, **cost +0.000000** | found, weight 1, free |
| **changing the pair correlation** | best flipper **NOT admissible**, cost **+2.000000** | **admissible**, cost **+0.000000** |

Writers **searched** over the full Pauli group, never nominated.

> ### **EACH RECORD IS INDIVIDUALLY WRITABLE FOR FREE BY AN ENERGY-CONSERVING SYMMETRY. THE PAIR
> ### CORRELATION CARRIES THE ENERGY, AND CHANGING *THAT* COSTS WORK. THE FREE SINGLE-RECORD WRITERS
> ### DO NOT TOUCH IT.**

**The control shows the instrument works:** on `H = 0` the pair correlation is the same on every block,
carries no energy, and the admissible writers — now weight 1 — **do** change it, for free, because
there is no energy to protect.

### WHAT THIS CORRECTS

**O-42's exclusion came from applying clause (iv) to the wrong object.** The configuration energy lives
in the **correlations between records**, which clause (iv) never constrains. **An interaction energy
between records is exactly what a source needs.**

> ### **AND NOTHING WAS IMPORTED TO REACH IT. No reservoir, no temperature, no Landauer bound, no
> ### external agent, and no relaxation of any clause. Only `H`, the records, and the five clauses as
> ### written. O-44's physical-channel rescue is NOT NEEDED — DEF-A can stand exactly as it is.**

This answers the principal's standing question — *"are we importing an assumption and restriction
that is not applicable at the record level?"* — in the strongest possible way: **the resolution
requires no import, and the restriction was never there.**

---

## O-48 — **THE CORRELATION ENERGY IS NOT A SOURCE. AND "ADMISSIBLE ⟹ dE = 0" CLOSES THE ENTIRE ENERGY ROUTE AT ANY `N`.**

Four probes, each adversarially verified. **Verdict: FAILS_SOURCE_FORM.**

### 1. THE QUANTITY THAT ACCUMULATES IS RECORD-BLIND

`S(n) = 2Σ|Jᵢ|` and `Var = Σ Jᵢ²`. **Neither ever touches a record operator.** And the decisive
control: a carrier `H' = ΣJᵢZᵢZᵢ₊₁ + Σhᵢ Zᵢ` with distinct `hᵢ` has an entirely non-degenerate
spectrum — **16/16, 64/64, 256/256, 1024/1024, 4096/4096 distinct energies** — so by P-1 it holds
**ZERO records**, confirmed by the program's own routines (`clause_iii = False`, `max|Tr(P_E Zᵢ)| = 1`).

> ### **ALL FOUR STANDARDS — EXTENSIVE, ADDITIVE, NOT-A-COUNT, SIGN-DEFINITE — PASS IDENTICALLY ON A
> ### CARRIER THAT PROVABLY HOLDS NO RECORDS.** `S(2N)/S(N)` = 3.088, 2.337, 2.133, 1.983; additivity
> defect exactly 0 with a live control at 1.83e12; 200 distinct `S` from 200 draws; C-46 ratio exactly
> 1.000000.

**And `S = 2‖H‖_op` and `Var = Tr(H²)/2ⁿ` exactly** — they are the spectral width and the normalised
Hilbert–Schmidt norm of `H`. **Ordinary spectral norms, not record quantities.**

**Its sign-definiteness is unfalsifiable as tested:** the C-46 ratio is `1.000000` for all-FM,
all-AFM, alternating, random-sign, *and* a coupling set with `Σ Jᵢ` exactly 0 — **because
`S = Σ2|Jᵢ|` takes the absolute value by hand.** No carrier in the family can fail it.

### 2. THE RECORD-DEPENDENT QUANTITY CANCELS, BY CLOSED FORM

`E(s) = Σ Jᵢ sᵢsᵢ₊₁`. Exact mean over configuration space is **exactly 0 as a rational at every `n`**,
and coherence `= mean|E|/Σ|J| = √(2/π)·m^(−1/2)` — verified **digit for digit** against exact-rational
DP to `m = 256` and out-of-sample at `m = 512, 1024, 4096` (`coh·√m = 0.797836` against
`√(2/π) = 0.797885`). **The fraction of configurations cancelling more than half rises to 0.970 by
`n = 20`.**

> **It cancels MORE as records are added — C-46's screening signature, the same shape that
> disqualified the integer intersection pairing. Ruled out BY FORM, immune to both objections.**

### 3. **THE DEFINITIONAL OBSTRUCTION THAT CLOSES THE ENERGY ROUTE ENTIRELY**

> ### **`[U,H] = 0` ⟹ `dE = 0` IDENTICALLY. ON ANY CARRIER, AT ANY `N`, NO ENERGY FUNCTIONAL CAN
> ### RESPOND TO AN ADMISSIBLE WRITE.**

Exhaustive Pauli scan, `n = 2..6`, three carriers: `max|dE|` over all admissible Paulis **exactly 0**;
non-admissible control `1.29e12` to `1.06e13`.

**This demotes O-47's headline from a finding to a tautology.** The writer was free **because every
admissible writer is free, by definition** — not because the construction achieved something.

**And O-47's phrasing is corrected:** the writer flips **all `n` records at once**, and **no admissible
unitary of any kind flips one alone.**

**With a non-existence proof, not a failed search:** no admissible unitary can change any pair
correlation, because each `ZᵢZᵢ₊₁` is a **scalar on every 2-dimensional eigenspace**. **The energy
"carried by the correlation" is carried by conserved charges that no writable operation can touch.**

### 4. A D-18 SELF-CATCH: `n` RECORDS, ONE BIT

Every eigenspace of the fully coupled chain has dimension **exactly 2** at every `n`, and the
program's own `commuting_family` / `independently_writable` return **1 independent record regardless
of `n`.** **The record count is extensive; the record information is not.**

### 5. **CLAUSE (v) TESTED FOR THE FIRST TIME ANYWHERE IN THE PROGRAM — AND IT FAILS ON THE OPEN CHAIN**

An **exact** criterion covering **every** unitary supported on the region (support condition +
Frobenius–König + perfect matching), cross-checked against exhaustive Pauli search on **630** cases
with **zero** disagreements.

**The smallest contractible region whose admissible operations flip a record is exactly `w = n`, at
every `n = 3..14`** — and in 1D the whole chain *is* a contiguous block. Controls fire: cutting one
coupling drops it to the smaller component's size; `H = 0` drops it to 1.

> **On the open chain these are NOT records in the full five-clause sense. Everything in O-42, O-44,
> O-47 and all four O-48 lanes is scoped to clauses (i)–(iv).**

**On a RING under the proper-arc reading, clause (v) HOLDS with distance `n`.** **Which reading is
correct is a convention decision, not a measurement, and it is the principal's to make.** It decides
whether this entire carrier family is admissible at all. Registered as **O-49**.

### 6. THE ONE GENUINE POSITIVE — CRITERION (e)'s FORM, FIRST TIME IN THIS PROGRAM

An **INDUCED** power law: `J_eff(r) → (−1)^(r+1)/(π·r)` on a **gapless** mediator. `t = 0` control
**exactly 0 at every `r`, including `r = 1`**; three independent instruments; amplitude **`1/π =
0.318310` exactly**.

> ### **A POWER-LAW RECORD–RECORD FALLOFF, INDUCED RATHER THAN INSERTED, ON A GAPLESS MEDIATOR. THE
> ### FIRST TIME THIS PROGRAM HAS EXHIBITED CRITERION (e)'s FORM AT ALL** — every previous falloff was
> exponential (C-47's `ξ = 1.1250`). **But it is a pair coupling constant, not a source, and it screens
> at `ln2/lnR`.**

### REFUTED UNDER VERIFICATION

- **Lane A's headline that (a)+(b)+(c)+(d) pass** — refuted as **record-blind** (§1).
- **Lane A's claimed "exact structural obstruction"** that the spread cannot depend on separation in
  *any* variant — **FALSE, tree-only.** On an all-pairs carrier, 300 permutations give **7, 41, 248**
  distinct `S` values against the open-chain control's **1, 1, 1** in the same table. Withdrawn.
- **A transcription error**: Lane A's S4 table as reported is **not its own data** — file and
  recomputation give min 8.648892 / max 12.857377 where the finding reports 9.8688 / 12.0313, and
  wide-family figures that appear nowhere in the output.
- **Lane B's centrepiece** — that clause (iv) forces half filling and the period-2 alternation —
  refuted by explicit counter-carrier.

---

## O-49 — **DECIDED BY THE PRINCIPAL: THE 1D CONVENTION IS A PROXY; THE TORIC CODE IS CANONICAL.**

O-48 tested clause (v) for the first time anywhere in this program and found the reading of
*"contractible"* decisive: on an **open chain** the whole carrier is one contiguous block, so (v)
**FAILS**; on a **ring** under the proper-arc reading it **HOLDS** with distance `n`. That is a
convention, not a measurement.

**The principal, 2026-08-20:**

> *"Adopt Option 3 conceptually, using Option 1 as an explicit low-dimensional convention: For 1D
> rings, state clearly that Clause (v) operates under the standard QEC constraint: locality is bounded
> by proper sub-regions (diam(R)<L). Treat 1D rings as a boundary-constrained proxy and let the Toric
> Code (O-50) serve as the canonical benchmark where Clause (v) is realized purely through manifold
> homology without semantic caveats."*

`CORE_FRAMEWORK_V001.md` amended accordingly and re-read to confirm the patch landed. **Two things
follow, and both are now binding:**

1. **For 1D rings only:** clause (v) operates under the **standard QEC constraint** — locality bounded
   by **proper** sub-regions, `diam(R) < L`. Under that reading (v) holds on the ring with distance
   `n`, matching T-11's no-cycle convention. **This is an explicit stipulation and is labelled as one
   wherever used.**
2. **1D rings are a boundary-constrained PROXY.** **The canonical benchmark is the toric code**, where
   clause (v) is realised purely through **manifold homology** — logical support genuinely
   non-contractible, both distances scaling with `L`, no semantic caveat required. **Any result whose
   truth depends on the 1D convention is scoped to the proxy and must say so; results on the torus are
   not.**

---

## O-38 — **THE COUPLING OPERATOR WAS THE ERROR; THE INSTRUMENT WAS TOO SMALL TO SETTLE IT. LANE B SETTLED IT.**

`LANE_O38_GAPLESS`. The first run coupled each record to `Z`, which in `H_B = Σe·Z + g·ΣXX` is the
**transverse-field direction — the energy operator**, scaling dimension 1, correlations `~r⁻²`. The
**order parameter is `X`**, dimension `1/8`, correlations `~r^(−1/4)`. **The record was coupled to the
short-ranged operator and the falloff was then reported as short-ranged.**

Rerun on `X`, 12 sites:

| | `ξ` with `Z` coupling | **`ξ` with `X` coupling** | power-law exponent |
|---|---|---|---|
| gapped `e=1.0 g=0.1` | 0.1743 | **0.4279** | −9.18 |
| **critical `e=1.0 g=1.0`** | 0.6503 | **5.7063** | **−0.6894** |
| ordered `e=0.1 g=1.0` | 0.1804 | **35.1130** | −0.1116 |

**The range grows 13× and then 80×.** But **`ξ = 5.7` and `ξ = 35` on a 12-site chain exceed or match
the system**, so the fit never observes a decay and **cannot distinguish exponential from power law**
(D-20). **No verdict is drawn from this lane.**

**O-48's Lane B settled the question on a proper instrument** — an induced `J_eff(r) → (−1)^(r+1)/(πr)`,
amplitude `1/π = 0.318310` exactly, `t=0` control exactly zero at every `r`, three independent
instruments agreeing (**C-63**).

**Second erratum:** the "dead-configuration control" returned `0.0087, 0.0017, 0.0004, 0.0001` where
its own description said it must vanish. **The cross term does not require crowding** — the control
behaved correctly and the prediction about it was wrong.

---

## **H-3 ANSWERED. ZERO OF THIRTEEN REAL RECORDS SATISFY THE FIVE CLAUSES AS WRITTEN.**

`LANE_GR1_CENSUS` … `LANE_GR4_DERIVE`. The principal: *"We are not setting out to create a toy. Why
haven't we been grounding every PROOF in the world's records?"* **This is the first time the clauses
have ever been tested against a real record.** Thirteen records, lifetimes `3e7`–`4e17 s`, write
energies eV to MJ.

### THE TALLY

| clause | | result |
|---|---|---|
| **(ii) DURABLE** | **NEVER FAILS** | 12 approximate + 1 exact of 13. **O-5's spectral-width relaxation is vindicated against nature** — width tolerances `ħ/τ` of `1e-41`–`1e-52 J`, **20+ orders below every relevant energy scale** |
| (i) BIT | fails 5/13 | analog records — zircon U-Pb ratio, synapse weight, tree ring, ice core, footprint — have no involution to test |
| **(iii) NON-TRIVIAL** | **fails 9/13** | real records store their value in states of **grossly different energy**: 0.2–1 eV (DNA), 10–26 eV (AgBr), **150 eV (flash)**, **0.5 MeV (mica track)**, **MJ (tree ring)** |
| **(iv) WRITABLE** | **fails 12/13** | under DEF-A every real write dissipates **60× to 3e27× `kT ln2`**. **The world wrote all thirteen — so real records are not writable in the program's sense** |
| **(v) PROTECTED** | **fails 13/13** | every record has an explicit local eraser at finite price: write head `5e-19 J`; **254 nm UV on a flash gate — the commercial EPROM eraser**; a mutagen molecule on DNA; a local anneal on a track |

> ### **ZERO OF THIRTEEN SATISFY ALL FIVE.**

### THE STRUCTURAL THEOREM — WHY, NOT JUST THAT

**Exact (ii) + (iii) are jointly unsatisfiable in generic matter.** A non-degenerate spectrum plus
`[R,H] = 0` forces `R = f(H)`, which clause (iii) forbids. So exact (ii)+(iii) require **symmetry or
engineered degeneracy.**

> ### **THE CORPUS'S CARRIERS PASS BECAUSE THEY WERE BUILT DEGENERATE. THE WORLD'S RECORDS ARE BUILT
> ### METASTABLE. DEGENERACY-PROTECTION AND BARRIER-PROTECTION ARE DIFFERENT MECHANISMS, AND THE
> ### CLAUSES FORMALISE THE WRONG ONE FOR NATURE.**

**And the sharpest single observation in the census:** the one record passing (i)–(iv) exactly — the
**CMB photon's degenerate polarisation doublet**, whose waveplate write genuinely has `dE = 0` and is
admissible — **fails (v) at zero cost. The only object that satisfies the program's writability is the
least protected thing in the census.**

### THE CONSTRUCTIVE HALF — ONE MOVE CURES (iii) AND (iv) TOGETHER

**Draw the boundary around carrier ⊗ local bath.** The clauses were written for the carrier alone.

- **(iii′)** non-constant on the **closed system's energy shell**, width `√(C_v k_B T²)`. A 1 cm³ bath
  gives `~1.6e-9 J (~10 GeV)`, beating the census's worst configuration offset (`0.5 MeV`) by `2e4`.
  **All 13 pass.**
- **(iv′)** admissible = an **energy-conserving dilation unitary** on carrier ⊗ writer ⊗ bath — **O-4's
  untested "or a physical channel" reading.** C-60 survives at the total level, and the cost reappears
  correctly as **free energy, floor `kT ln2 + dE_config`.** **All 13 pass.**
- **(v′)** every single-region flip costs `≥ E_b` with `E_b/kT ≫ 1` — census values 61 (HDD), ~120
  (flash), ~50 (DNA), 220 (zircon), **780 (single-domain magnetite)**. **The corpus's kinematic
  protection is the `E_b → ∞` limit.**
- **(i′)** involution → commuting spectral family, which C-12 already supports.

> ### **AND THIS ANSWERS H-6 AS A BY-PRODUCT: RECORDS ARE MACROSCOPIC BECAUSE THE AMENDED CLAUSES
> ### DEMAND A MACROSCOPIC BATH TO EXPORT THE WRITE ENERGY — NOT BECAUSE THE CARRIER MUST BE BIG.**

### THE FIRST GROUNDED PROOF IS NAMED

**Put the HDD CoCrPt grain through the model as an `(H,{L_k})` two-state macrospin with Arrhenius
jumps** — `K_uV = 61 kT`, `τ = 2e17 s`, splitting 0.007–7 kT, write head `5e-19 J`. **That is a test a
physicist can run against their own data.**

---

## **EXTERNAL REVIEW — "NOT A THEORY, AND NOT PROVEN IN THE SENSE YOU MEANT."**

Four independent hostile reviews, each calibrated for overstatement **in both directions**, plus an
editor verdict. The reviewers read the framework, the ledger, the register, the glossary and ~15 lanes
end to end, and **ran** `reproduce.sh --seals`, `t9_sweep.py`, `validate_model.py` and others.

### THE ANSWER TO THE PRINCIPAL'S QUESTION

> ### **"Is it big?" — "NO — NOT IN THE SENSE YOU ASKED TO CONFIRM."**

The goal sentence fails at every load-bearing word, on the corpus's own rows: **"EM" is a `Z₂` lattice
gauge field** — no `U(1)`, no Maxwell limit, and the repo's `U(1)` strand feeds **zero** ledger rows;
**"gravity" is a lattice's homology pairing** (X-1: *"the topology is a LATTICE's, not spacetime's"*);
**"alpha" is a dimensionless generic coupling** (T-22). PF-6 found no prediction a rival lacks.

### WHAT IS REAL, AND THE REVIEWERS WERE EMPHATIC THAT UNDER-CLAIMING WOULD ALSO FAIL

| | |
|---|---|
| **C-12** | the existence characterization — a five-clause record satisfying (i)–(iv) exists **iff** the commutant of the noise `*`-algebra contains a trace-balanced projection non-trivial on some energy eigenspace; **no writable record in odd dimension**. Constructive proof, 210/210 exhaustive, **reproduced byte-identical by two reviewers**. *"The single result defensible before a hostile committee with no caveats beyond scope."* |
| the exclusion package | C-25/C-26, C-52, C-53, C-48, C-60 as one theorem-grade obstruction. Adversarially verified, exact |
| **C-41** | *"one short proof away from a genuine original theorem"* |
| **C-64** | the clause-(v) decision procedure — *"a publishable-lemma-grade instrument buried inside a lane"* |
| the methodology | *"close to publishable as methodology"* |

**Verdict: note-grade original mathematics at the intersection of noiseless subsystems and the
Zurek/Riedel redundant-records literature. Publishable in a foundations venue.**

### THE WORD: **A FORMAL FRAMEWORK**, NOT A THEORY

> *"A physical theory must make at least one statement that could be false about the world; by the
> corpus's own rows it makes none."*

**Allowed:** *we define*, *we prove (about the defined object)*, *we verify by exact computation*.
**Forbidden until their blocking rows close:** *theory*, *proven process*, *explains*, and the three
nouns **EM**, **gravity**, **alpha**.

### THE COUNTS

Of the 162 rows that carried PROVED: **~14 original theorems (9%)**, ~52 exact computations (32%),
**~41 numerical measurements (25%)** for which `MEASURED` existed and held 2, ~20 standard results
restated (12%), **~34 definitions and decisions (21%)** for which `DEFINED` existed and held 1.
**Proof-grade in spirit: 66/162 = 41%.**

### THREE REGISTRAR ERRORS FROM THIS SESSION, CORRECTED IN PLACE

- **C-63 is the 1D RKKY / Lindhard interaction** — a standard free-fermion result. **The lane's own
  VERIFY directory said so and the ledger row, register and glossary did not.** Registered as "the
  first power-law falloff in the program's history" without a literature check. **Rescoped to
  BORROWED.**
- **C-52's physical conclusion overreached.** The `Z[i]` quantisation binds only for
  **Gaussian-integer** coefficients; **a real `λ·W` escapes it trivially.** "A `10⁻³⁶` residual is
  EXCLUDED" is corrected to: no *integer-combination* invariant can be small.
- **C-60's gloss is circular under DEF-A** — which *defines* admissible as doing no work. Said three
  times; corrected.

### AND A REPRODUCTION FAILURE THAT HAD BEEN REPORTED AS GREEN

**The one-command reproduction does not pass.** 13 scripts DIFFER on re-run; `reproduce_full.log`
ends in `Terminated: 15`; **`LANE_EM_EXTENT/holonomy.txt` is garbled and carries a wrong number**;
stale seals in `LANE_F7_OCCUPANCY` and `model/`; `LANE_O5_ADVERSARIAL` cannot run standalone.

**And T-9 was falsely DONE.** `SINGLE-CARRIER` appears **zero** times in the ledger; ~24 of 162 rows
cite two carriers. **REPLICATE.md's sentence asserting the marking was false of the shipped ledger and
is corrected in place.** T-9 **REOPENED**; PF-8's stale `6 of 78` denominator corrected against 162.

---

## O-51 — **ADOPTED. THE AMENDED DEFINITION, AND THE GOAL'S GROUNDING CLAUSE.**

The principal: *"I just want to proceed with what we need to do to reach the founding goal."* The
grounding clause was already decided three times over — *"not a toy"*, *"ground every PROOF in the
world's records"*, *"any physicist anywhere can run it against their real world data"* — so it is
adopted rather than asked again.

### THE MECHANISM MISMATCH, WHICH IS THE ROOT

> ### **THE WORLD USES ENERGETIC AND KINETIC PROTECTION. THE EXACT CLAUSES ASSUME TOPOLOGICAL
> ### PROTECTION.**

**A small theorem behind it (support-compression, Uhlmann):** any record whose two states differ only
inside a contractible region — **i.e. any locally readable record, which is all of them** — has a
flipper supported on that region. **So (iv) and (v) are co-satisfiable only on non-contractible
supports.** Nature's one non-contractible record, the **superconducting flux quantum**, is still
flipped by a local phase slip over a **0.27 eV** barrier; nature's genuinely (v)-protected quantities
— **Chern number, baryon number at `10⁻¹⁶⁴` suppression** — are **unwritable**.

**And the sting:** at finite `T` the program's canonical carrier has an `O(1)` barrier and a lifetime
**independent of `L`** (Alicki et al. 2009; Bravyi–Terhal 2009 — no passive self-correction below 4D).
**One CoCrPt grain with `K_uV = 60 kT` is a better record than a toric code of any size.**

**The program's own O-16 measured this mismatch from inside before the census confirmed it from
outside.**

### H-3, ANSWERED WITH A NUMBER

**Zero of ~20 real records satisfy the five clauses.** Four independent censuses, each adversarially
checked, **headline upheld every time.** The two nearest residents die on opposite clauses: the **CMB
photon** passes (i)–(iv) and fails (v) at zero cost; **B−L** passes (ii) exactly and fails (iv)
because **nature contains no writer for it.** **That pincer is C-60 observed in nature.**

### WHAT WAS ADOPTED

- **The amended clauses (i′)–(v′)** on **carrier ⊗ local bath**, with declared tolerances. All ~20
  real records pass. `CORE_FRAMEWORK_V001.md` amended and re-read.
- **DEF-A named as the exact corner** — `T→0`, `t_m→∞`, `W=0`, `E_b→∞`. **All 162 FORMAL rows remain
  true theorems about that corner.**
- **The goal's grounding clause**, in `THE_PLAN`: *"…form THE WORLD'S RECORDS — with every PROOF
  grounded in at least one named physical record with real numbers — and the model, so that the proof
  can be checked by anyone AGAINST those records."* **This converts H-3, H-5 and H-6 from open hazards
  into standing acceptance criteria.**

### WHAT THIS OPENS — LARGER THAN WHAT IT COSTS

> ### **THE ENERGY ROUTE TO A GRAVITY SOURCE, CLOSED BY O-48 FOR *FREE WRITES ONLY*, REOPENS UNDER THE
> ### AMENDMENT WITH `dE` = WORK PAID. A MEASURABLE, NON-ZERO, RECORD-BY-RECORD CONFIGURATION ENERGY
> ### IS EXACTLY WHAT A SOURCE TERM NEEDS.**

O-42's headline — *a record cannot be both writable and carry configuration energy* — **is refuted by
flash memory roughly `10¹⁸` times a day.**

### WHAT MUST BE REDONE, PRECISELY BOUNDED — T-28 … T-31

**C-52 and C-53 at finite tolerance** (exclusions proved at tolerance zero do not inherit); **the
O-42-lineage exclusions under `ADMISSIBLE(β,W)`**, with the concrete prediction that the "unwritable"
records become writable at `W` equal to their uphill energy changes — **spreads 1.400000 and
3.600000**; **C-12's existence criterion re-proved for slow manifolds**, its trace-balance hypothesis
being the one corpus theorem genuinely in doubt; and **C-14's count law with asymmetric wells**, which
**collapses to zero records under any splitting** unless width-clustered multiplicities are adopted —
**so the HDD run returns zero unless that is fixed first.**

### THREE ROWS FOUND THE PHYSICS BEFORE THE CENSUS DID

**O-5** (its width bound is the template for (ii′) and never failed against nature), **C-60** (free
writing and durability exclude each other — observed in nature via B−L), **O-16** (found the
protection mismatch from inside). **O-44 is rehabilitated: it is `ADMISSIBLE(β,W)` in embryo, and its
"not needed" disposition reverses.**

---

## T-29 — **THE FIRST RECORD OF THIS PROGRAM THAT EXISTS IN THE WORLD.**

`LANE_T29_HDD`, `model/grounded.py`. A CoCrPt grain in hard-disk media, from published material
constants, taken as an open quantum system `(H,{L_k})` and put through the amended clauses.

`K_u = 2.0e5 J/m³`, `V = 1.26e-24 m³` (a 10.8 nm cube), `T = 300 K`, `f₀ = 1e9 Hz` →
`E_b = 60.8 kT`. Splitting 3 kT; write head `5e-19 J`; local bath `C_v = 1e-3 J/K`.

### THE MODEL RETURNS THE GRAIN'S LIFETIME BY A ROUTE THAT NEVER USES IT

| | |
|---|---|
| from the **record's own Liouvillian mode** | **`τ = 5.6279e16 s = 1.783e9 years`** |
| from the Néel–Arrhenius rates | `τ = 5.6279e16 s` |
| **agreement** | **`2.8e-16` relative** |

### THE AMENDED CLAUSES, ALL PASSING, WITH MARGINS

| clause | measured | requirement | margin |
|---|---|---|---|
| **(i′)** spectral family | commuting to `0.0e+00` | — | exact |
| **(ii′)** durable to `t_m` | `1.777e-17 /s` | `1/t_m = 3.169e-09 /s` **(10-year retention spec, chosen independently)** | **`1.78e8`×** |
| **(iii′)** energy shell | `3.525e-11 J` | `dE_config = 1.243e-20 J` | `2.84e9`× |
| **(iv′)** writable | `W = 5.00e-19 J` | floor `1.530e-20 J` | **`174`× Landauer** |
| **(v′)** protected | `E_b/kT = 60.8` | `≫ 1` | suppression `3.78e-27` |

### THE CONTROL — THE SAME GRAIN UNDER DEF-A

| exact clause | |
|---|---|
| (ii) `[L_k,R] = 0` | **FAIL** — `‖[L_k,R]‖/‖L‖ = 2.0000` |
| (iii) same energy | **FAIL** — `H` non-degenerate, so `[H,R]=0` forces `R = f(H)` |
| (iv) `Tr(P_E R) = 0` | **FAIL** — `max = 1.0000` |
| (v) protected | **FAIL** — the write head, `5e-19 J` |

> ### **THE SAME GRAIN IS A RECORD UNDER THE AMENDED CLAUSES AND IS NOT ONE UNDER THE EXACT CLAUSES.
> ### THE AMENDMENT IS NOT COSMETIC, AND THIS IS THE FIRST TIME IN THE PROGRAM'S LIFE THAT AN OBJECT
> ### IN THE WORLD HAS SATISFIED ITS DEFINITION.**

### WHAT THIS IS NOT

**The retention law is standard physics.** Reproducing it is **grounding, not a distinguishing
prediction.** PF-6 remains FAILED and H-5 remains OPEN. What has changed is that the program now has
**one object whose numbers a physicist can check against their own media.**

### TWO BUGS, LOGGED

**`lifetime()` returned the slowest non-zero Liouvillian mode**, which for a two-level system is the
**coherence** at `(Γ↑+Γ↓)/2` — **not the record**, which is the population difference and relaxes
twice as fast. It gave a lifetime **exactly 2× Néel–Arrhenius.** `spectrum()` now carries the warning
and `lifetime()` requires the record.

**And the READ contradicted its own table**, declaring success beside rows reading `ROUTES DISAGREE`
and `FAIL` — written in advance, the error logged repeatedly today. **The READ is now generated from
the results.** A third: `t_m` had been set to the grain's own lifetime, making clause (ii′) a
tautology; it is now the **independent 10-year retention spec.**

---

## T-30 — **THE `Z[i]` QUANTISATION IS AN ARTIFACT OF EXACTNESS. THE GRAVITY-STRENGTH EXCLUSION DOES NOT INHERIT TO THE WORLD.**

`LANE_T30_TOLERANCE`. C-52 — *a product of record operators is a single signed Pauli, so every
Gaussian-integer polynomial has trace ratio in `Z[i]`, which has no element of modulus in `(0,1)`* —
was the load-bearing exclusion behind two days of negatives. **It was proved at tolerance zero, over
exact signed Paulis in an exact code space: DEF-A's corner, where the censuses found ZERO real
records.**

### THE CONTROL REPRODUCES C-52 EXACTLY

4000 integer-coefficient polynomials on the exact `[[4,2,2]]` carrier: **3296 non-zero, minimum
modulus `1.0000000000`, nothing strictly inside `(0,1)`.**

### THE SAME OPERATION ON A METASTABLE RECORD

| `dE/kT` | 3 | 1 | 0.3 | 0.1 | 0.01 | 1e-4 | **1e-8** |
|---|---|---|---|---|---|---|---|
| **`⟨R⟩_ss`** | 0.905148254 | 0.462117157 | 0.148885034 | 0.049958375 | 0.004999958 | 0.000050000 | **0.000000005** |
| in `Z[i]`? | False | False | False | False | False | False | **False** |

**And the barrier is not the variable.** `E_b/kT` = 60.8 → 30.4 → 15.2 moves `τ` from `1.3e17 s` to
`8.6e-4 s` — **25 orders of magnitude — and leaves `⟨R⟩_ss` at 0.905148254, unchanged.**

> ### **`⟨R⟩_ss = tanh(dE/2kT)`, A CONTINUOUS FUNCTION OF THE SPLITTING. EVERY VALUE IN `(0,1)` IS
> ### REACHABLE, AND ARBITRARILY SMALL ONES BY ARBITRARILY SMALL `dE` — `5.0e-9` DEMONSTRATED,
> ### MATCHING THE CLOSED FORM.**

> ### **THE INTERVAL C-52 CALLS EMPTY IS NOT EMPTY FOR A REAL RECORD. C-52's PHYSICAL CONCLUSION —
> ### THAT A GRAVITY-STRENGTH RESIDUAL HAS NO SLOT — WAS A THEOREM ABOUT DEF-A'S CORNER, NOT ABOUT
> ### THE WORLD. THE EXCLUSION DOES NOT INHERIT.**

### SCOPE, STATED PLAINLY

**This shows nothing forbids a small residual on a real record. It does NOT show one exists.** What it
removes is the argument that appeared to close the question at any `N` — the one the registrar leaned
on hardest over two days. **The gravity question is reopened, not answered.**

### TWO ERRATA, LOGGED

**v1's control summed only non-identity logicals**, every one of which has vanishing normalised trace
on the code space — **all 4000 ratios were exactly 0 and the instrument measured nothing.** C-52's
non-zero values come from terms landing **on** the stabiliser group, so the family must contain
squares and the identity.

**v2 varied only the barrier and reported the interval "populated continuously by the barrier
height" while its own table printed the same value six times.** The value depends on the splitting.
**Both parameters are now swept and the table shows which one moves it.**

---

## T-32 — **ALL FIVE SOURCE STANDARDS ARE MET ON A REAL RECORD. AND THE SIGN-DEFINITENESS COMES FROM THE ACT OF WRITING.**

`LANE_T32_REALSOURCE`. C-70 removed the exclusion that appeared to close this at any `N`. Real records
carry a configuration energy `dE`, and it is measurable. O-48 tested the five standards on a toy chain
where `dE` was two-signed and screened as `m^(−1/2)`. **The toy is not the world.**

CoCrPt grain: `V = 1.26e-24 m³`, `M_s = 4.0e5 A/m`, moment `m = 5.04e-19 A m²`, `E_b = 60.8 kT`.

| standard | result | control in the same table |
|---|---|---|
| **(a) EXTENSIVE** | ratios **exactly 10.0000** per decade, `N` = 10 → 10⁵ | — |
| **(b) ADDITIVE** | defect **exactly 0** over disjoint tracks (`0.0e+00`, `9.9e-32`, `0.0e+00`) | coupled tracks would show a defect |
| **(c) NOT A COUNT** | moves **2.40×** at **fixed `N` = 1000** as `M_s`, `B`, `V` vary | `N` frozen |
| **(d) SIGN-DEFINITE** | **`\|Σ\|/Σ\|·\| = 1.000000` at every `N`** in *written* media | **demagnetised medium screens**, falling as `1/√N`: 0.400, 0.080, 0.0020, 0.0037 |
| **(e) POWER LAW** | dipole falloff, ratio **exactly 8.0000** per doubling → **exponent −3, INDUCED** by magnetostatics | not inserted |

> ### **THE FIRST QUANTITY IN THE PROGRAM TO MEET ALL FIVE, AND IT IS ON AN OBJECT THAT SATISFIES THE
> ### RECORD DEFINITION (C-69).**

### WHY THE TOY FAILED AND THE WORLD DOES NOT

**The demagnetised control reproduces the toy chain's failure exactly** — two-signed terms screening
as `1/√N`, C-46's signature. **What makes the difference is that the medium was WRITTEN.** The write
head aligns every grain, so the terms **add** instead of cancelling.

> ### **ORDERING IS IMPOSED BY THE WRITING PROCESS. The sign-definiteness that every toy candidate
> ### failed is supplied by the act of record formation itself — which is what this program set out
> ### to find.**

### THE LIMIT, SHARPLY

**This is magnetostatics. None of it is new physics.** The exponent is **−3, not gravity's −2**, and a
dipole interaction is not gravitation. **What is established is narrower and still worth having: an
object meeting the record definition carries a quantity with a source's form in all five respects,
and the property every toy candidate lacked comes from writing.**

---

## O-50 — **THE CANDIDATE IS REFUTED. WHAT SURVIVES IS BURNSIDE, AND "MEAN ZERO" IS NOT "CANCELS".**

`LANE_O50_A` … `LANE_O50_D`. **Three of four lanes self-certified the candidate PROVED; all four
adversaries independently returned `theorem_actually_proved = false`.**

### WHAT IS PROVED, EXACTLY

**On the toric code at `L = 2..8` and genus 1..6 (`k = 2..12`), the writer group acts SIMPLY
TRANSITIVELY on record configurations, so the writer-invariant functional space has dimension
EXACTLY 1** — constants only, Burnside-confirmed, re-derived twice from scratch by independent
implementations. **Operator side:** of the `4^k` logical Paulis exactly **one** is fixed by every
writer — the identity. **The complete algebra of write-invariant state functionals is the algebra of
functions of `|⟨P̄⟩|` — record INTEGRITY, never record VALUE.**

**But the hypothesis asserts the generators of the conclusion**, and the lane's own verification
reproduces every torus row from a bare `(Z₂)^k` translation with **zero toric-code input.**

### WHAT IS FALSE

**"Mean zero" ≠ "cancels".** Mean is exactly 0 at every `m`, but `E|F| = √(2m/π)` **grows to 204.26 at
`m = 65536`.** And for `f = (Σsᵢ)²` the record-dependent part is **EXTENSIVE** — typical `|f − m|` is
`0.75m, 0.98m, 0.97m, 0.92m, 0.96m` at `m = 4..20`, not `√m`.

**Two explicit counterexamples to the candidate**, one of them **computed by a lane and omitted from
its own table**: `f = (1+s₁)/2` is non-constant, responsive, mean `1/2`; and
`G = Σ(1+sᵢsⱼ)/(2r_ij)` is responsive **and** strictly positive **and** has mean 6.18 — the forbidden
conjunction.

### THE ONE EXACT OBSTRUCTION LEFT STANDING

**The responsive part of any functional has zero orbit sum and takes both signs.** This follows from
**writes being BIJECTIONS** — not from the five clauses — and **holds on every carrier including one
with no records.**

### CLAUSE (v), VERIFIED BY HOMOLOGY WITH NO CONVENTION

**1480 regions across `L = 3..6`: contractible regions carrying a logical, ZERO; non-contractible,
all of them.** `dim(V(Rg) mod S) = rank χ(V(Rg))` for every region. **This is what O-49's decision
called for — protection through manifold homology, no semantic caveat.** And `Aut(carrier) = 8L²`
exactly, so the carrier is not permutation-symmetric and D-22 is satisfied.

### THE NEXT MEASUREMENT IT NAMES

**Does there exist a durable operator `A` (`[A,H] = 0`) whose EXTENSIVE part is not proportional to
the identity?** `(ΣRᵢ)²` achieves extensivity and responsiveness and fails this — its extensive part
is `m·I`, record-blind. **If that is FORCED, the program has its first genuine form-level exclusion
of a source, immune to both objections. If not, the surviving operator IS the source candidate.**

---

## T-33 — **THE CALCULATION AGREES WITH ANY RECORD SURFACE. TWO LAWS, SIX MECHANISMS, MACHINE PRECISION.**

`LANE_T33_ANYSURFACE`. The principal: *"PROOF means that someone anywhere in the world can prove that
our calculation agrees with **any record surface**."* One named record is an instance, not a proof —
so the `PROVED` bar and `ledger/status.py` were **strengthened**, not relaxed: a row must now carry
`RECORDS VERIFIED:` listing **at least two structurally different mechanisms.**

### LAW 1 — `⟨R⟩_ss = tanh(dE / 2k_BT)`

| record surface | mechanism | `dE/kT` | closed form | from `(H,{L_k})` | abs err |
|---|---|---|---|---|---|
| CoCrPt HDD grain | magnetic anisotropy | 3.00 | 9.0515e-01 | 9.0515e-01 | 1.22e-15 |
| NAND floating gate | trapped charge | 11.60 | 9.9998e-01 | 9.9998e-01 | **0.00e+00** |
| DNA base tautomer | chemical bond | 13.10 | 1.0000e+00 | 1.0000e+00 | 1.11e-16 |
| Fe(II) complex | spin-state transition | 2.10 | 7.8181e-01 | 7.8181e-01 | 5.55e-16 |
| Azobenzene | photoisomerisation | 23.21 | 1.0000e+00 | 1.0000e+00 | **0.00e+00** |
| **Alanine enantiomer** | **parity violation** | **3.87e-12** | **1.9341e-12** | **1.9327e-12** | 1.35e-15 |

### LAW 2 — `τ = exp(E_b/k_BT) / f₀`, from the record's own Liouvillian mode

| surface | `E_b/kT` | closed form (s) | from `(H,{L_k})` (s) | rel err |
|---|---|---|---|---|
| CoCrPt grain | 60.8 | 5.4021e+16 | 5.4021e+16 | 1.48e-16 |
| NAND gate | 61.9 | 2.2852e+11 | 2.2852e+11 | **0.00e+00** |
| DNA tautomer | 48.7 | 1.9477e+05 | 1.9477e+05 | 1.49e-16 |
| Fe(II) | 32.9 | 5.9319e+01 | 5.9319e+01 | 2.40e-16 |
| Azobenzene | 40.6 | 3.9760e-01 | 3.9760e-01 | 1.40e-16 |
| Alanine | 54.2 | 1.6517e+10 | 1.6517e+10 | 2.31e-16 |

> ### **SIX MECHANISMS SHARING NOTHING BUT BEING TWO-STATE RECORDS. `dE` SPANS `6.0e12`. EVERY
> ### ABSOLUTE ERROR AT OR BELOW `1.4e-15` — MACHINE PRECISION. THE CALCULATION IS
> ### MECHANISM-INDEPENDENT.**

### AND IT DECLINES WHERE THE PHYSICS DECLINES

**Zircon U-238** — nuclear decay is **temperature-independent**, so the record is not thermally
activated and neither law applies; `E_b/kT` would be `1.65e8` and the arithmetic declines exactly
where the physics does. **A CMB photon in free flight** — no bath, zero relaxation rates, so the model
returns **no** lifetime and **no** steady-state value rather than a number. **That is what makes the
six passes mean something.**

### THE BAR WAS RAISED AND TWO ROWS FELL BACK

**C-69 and C-70 now meet it** on six mechanisms. **C-71 and C-72 do not** — they are verified on
magnetic media alone and are returned to `FORMAL` until a second mechanism is scored. The named check
is a **written NAND array against an erased one.**

---

## T-28 — **DEF-A IS THE LIMIT OF THE AMENDED DEFINITION. VERIFIED, NOT ASSERTED.**

`LANE_T28_LIMIT`. O-51 named DEF-A as the `T→0, t_m→∞, W=0, E_b→∞` corner. **If that were false, the
162 FORMAL rows would be theorems about something else.**

| carrier | dim | slow modes at `t_m = ∞` | dim commutant, `Σm_E²` | agree |
|---|---|---|---|---|
| `[[4,2,2]]` | 16 | **96** | **96** | ✓ |
| `[[6,4,2]]` | 64 | **1536** | **1536** | ✓ |
| 3-qubit Ising | 8 | **24** | **24** | ✓ |

**Control:** with dissipation the slow set is **monotone in `t_m`** and **strictly smaller** than the
commutant at long `t_m` (1 of 2 at `t_m = 10⁹` and `10³`), so the instrument distinguishes the limit
from the general case. **Clause (ii′) reduces to clause (ii)** — rate and `‖[H,R]‖` both `0.00e+00`.

**Correction that made it work:** durability requires `|λ| ≤ 1/t_m`, **not `|Re λ|`.** With no
dissipation `−i[H,·]` is anti-Hermitian, so every eigenvalue is purely imaginary and a `Re λ` filter
excludes nothing; an observable with `λ = iω` does not decay but **rotates**, so its value oscillates
and it is not durable. The numerical floor also had to be a stated tolerance rather than `1e-300`.

---

## T-31 — **THE DEGENERACY-DEPENDENT CHAIN COLLAPSES UNDER GENERIC ASYMMETRY, AND THE AMENDED DEFINITION ALREADY CARRIES THE FIX.**

`LANE_T31_ASYMMETRY`. `[[4,2,2]]`, `t_m` = 10 years so `δ = ħ/t_m = 3.341e-43 J`.

| run | splitting | multiplicities | **`k`** |
|---|---|---|---|
| EXACT | 0 | `[4, 8, 4]` | **2** |
| **ONE-SITE `Z`** | 1e-3 | `[4, 4, 4, 4]` | **2** |
| **GENERIC** | 1e-6 | `[1,1,2,1,…]` | **0** |
| **GENERIC** | 1e-3 | `[1,1,1,…,1]` | **0** |
| **GENERIC** | 1e-1 | `[1,1,1,…,1]` | **0** |

> **The census was right, and the perturbation must be GENERIC.** A single-site `Z` only *partially*
> lifts the degeneracy — `[4,8,4] → [4,4,4,4]` and `v₂(4)` is still 2, so the count survives. **A
> generic splitting collapses every multiplicity to 1 and `k` falls from 2 to 0.** C-14's count law
> and the W-42/43/44/51 record-to-geometry chain **rest on a symmetry the world does not have.**

**And the fix needs no new machinery.** Clause (ii′) already carries a durability width; eigenvalues
closer than it are indistinguishable to a record that need only last `t_m`. Clustering within a
**stated** tolerance recovers `[4,8,4]` and `k = 2` **exactly** whenever the splitting is inside it —
and correctly leaves the count at 0 when it is not (`1e-1` against a `1e-2` width).

---

## T-40 — **THE FULL-PROJECT MODEL.** And the plan LOCKED, reviewed, with the theory areas surfaced.

The principal, 2026-08-20: *"We need a model to work on that represents the full project."* Built:
`model/project_model.py` — one entry point carrying the five layers: the amended DEFINITION with its
tolerances (O-51), the two PROVED LAWS from the record's own Liouvillian mode (C-69, C-70), the
FORMATION machinery (C-71/C-72, scoped pending the solidity review), the DEF-A CORNER reduction
checked against the exact commutant (C-75), and the ROLES honestly scoped with their open TDs.

**`model/validate_project.py`: 11 PASS, 0 FAIL** — the grain τ (5.6279e16 s), the T-29 clause margins,
both laws on six mechanisms at machine precision, the declines on zircon and the CMB photon, the
corner dims 96/1536/24, and the written/unwritten formation ratios, all reproduced through the one
entry point.

**THE PLAN IS LOCKED** (recorded in its header): appends within the existing phase framework, no
renumbering, no restructuring. Rows T-34–T-40 appended. **`PLAN_REVIEW_V001.md`** carries the
comprehensive review and the seven THEORETICAL DISCUSSION AREAS (TD-1 the world-level Γ claim, TD-2
the three roles restated, TD-3 alpha through the barrier, TD-4 admissible/protection ratification,
TD-5 a prediction of our own, TD-6 what plays the field, TD-7 the CMB/B−L brackets). An adversarial
SOLIDITY REVIEW of the post-amendment corpus is running; C-71/C-72 promotion and the T-34 NAND lane
are gated on its verdict.

---

## SOLIDITY REVIEW — VERDICTS EXECUTED. AND TD-1 DECIDED: **SHARED ORIGIN.**

Four adversarial probes, told to default to refuted. **T-28 fully SOLID.** Both PROVED rows fell;
the machinery beneath them survived.

| item | verdict | action taken |
|---|---|---|
| C-69 | **NOT_SOLID as grounded** | demoted to FORMAL. The stated law contradicted its own number by `2cosh(dE/2kT)` — the computed object is `τ = 1/(g↑+g↓)`; the "not by inserting the Arrhenius rate" clause was false; **no measured datum enters**. The claim *title* survives at full strength |
| C-70 | **NOT_SOLID as grounded** | demoted to FORMAL. An identity of the detailed-balance construction; six "mechanisms" are six parameter sets of one 2×2 model. **Azobenzene withdrawn** (computed 0.398 s vs measured ~1e4–1e6 s — the midpoint-barrier convention) and **alanine withdrawn** (dE ~5 orders above literature PVED, probable J/mol-for-eV misread) |
| T-30 → C-52 | **consequence refuted** | corrected: thermal expectations are a **different functional** from C-52's trace ratio, under which the metastable record stays exactly quantised. "The exclusion does not inherit" is withdrawn; **undecided which functional carries the physical exclusion**. C-52's independent withdrawal ground (real `λ·W`) carries alone |
| T-31 / C-76 | **width-fix refuted** | the "within δ?" column used an ad-hoc `1e-2` tolerance while the same script printed `splitting/δ = 3e36..3e41`; with the actual `δ` the count is 0 everywhere. **Collapse stands; the fix claim is withdrawn — a recovering width must be derived, not chosen** |
| C-71/C-72 | **PROMOTE_AFTER_RESCOPE** | T-34 updated with the required rescope: the encoding-level claim — NAND net charge one-signed for *every* pattern; magnetic remanent moment under **DC-saturation scope, real data tracks screen** (measured: ratio 0.00096 on random data) |
| guards | fixed | `clause_ii` had the `|Re λ|` error live (the same one C-75 corrected in `slow_modes`); `RECORDS VERIFIED: a; a` fooled the dedupe — both fixed; `validate_project` 11 PASS after |

**PROVED rows: 0.** The bar is met by nothing until an external measured number sits beside a model
number — **T-41**, now on the critical path of Phase F.

### TD-1 — DECIDED BY THE PRINCIPAL: **SHARED ORIGIN** (A-GR3)

> *"Shared Origin — but we should keep in mind that measures at the record level might behave
> differently from what we've seen in other contexts. We've been avoiding importing assumptions as
> given so that we can avoid errors that are about our measurements versus being about the record
> surface."*

Registered as **A-GR3**: Γ is the common structure that ALLOWS records and appears at scale as
geometry. **The caveat is binding on T-37**: the Γ-side variable must be defined in the record
surface's own terms — no behavioral assumption imported — with the classical relation as the
recovery target at scale only (D-1). **The fingerprint-variable choice is deliberately left open**:
per the caveat, pre-committing to a variable that behaves like its analogues elsewhere would be the
import the program exists to avoid.

---

## C-77 — **THE EMERGENCE CLAIM, ADOPTED.** T-37 closed.

The principal: *"yes let's adopt this."* The claim, verbatim as adopted:

> **The structure Γ that allows a record — by shaping the boundaries that make a bit non-losable
> (non-contractible support in the corner; basin boundaries in the world) — is the same structure
> whose aggregate at scale appears as geometry. Classical gravity emerges from the boundary-shaping
> terms and is not expected to resemble itself at the record level.**
>
> **First falsifiable increment:** derive, from record-surface boundary structure alone — no
> classical form assumed, every concept earning its place per D-24 — a scale-level relation that
> matches a known gravitational one. **The claim fails** if every such derivation requires assuming
> the classical form, or yields relations incompatible with the known ones.

Registered **CANDIDATE** — assembled and coherent, not yet proved. It rests on A-GR3 (shared origin),
A-GR4 (boundary-shaping mechanism), D-24 (earned concepts), and the principal's binding caveat that
record-level measures may behave unlike their analogues elsewhere. **T-42** carries the derivation
increment, with the first concept to be earned named: **distance** — nothing at the record level has
yet earned a notion of how far apart two records are except boundary-crossing structure.

**C-77 OPENNESS CLAUSE (the principal, same day):** *"we don't want to rule out the possibility that
other terms contribute to gravity emergence. We are ultimately looking to solve gravity emergence."*
Amended into C-77: Γ is the **named** contributor, never asserted as the only one — the original
wording was *"terms like gamma."* A derivation succeeding through additional terms alongside Γ
**satisfies** the claim. The goal is the solution, not Γ-exclusivity.

---

## SOLIDITY REPAIRS EXECUTED; **C-71/C-72 PROMOTED ON THE RESCOPED, ENCODING-LEVEL CLAIM.** T-34 done; T-41 opened with two external anchors.

Per the review's prescriptions, in the lanes with errata noted: **T-34** — image-interaction factor-2
corrected (`U = kq²(1/r − 1/√(r²+4h²))`, `U(40nm)` = 9.7 eV, now inside the known FG-FG interference
ballpark); the unwritten null computed under a **declared ±5e over-erase tolerance**; the ratio-1
result labeled **mechanism-constitutive** (the sign open in design space, fixed once per device);
the screening omission noted. **T-32** — restated **field-free** as remanent moment `M_r = M_s V Σsᵢ`;
random-data and DC-free-coded rows added (**they screen**, as the review measured — the one-signedness
is scoped to DC saturation); the additivity cross-term **computed**, replacing the 1e-3 assertion
(holds ≥ ~60 nm, fails at grain spacing); the r⁻³ **relabeled INSERTED** (quoted magnetostatics;
the induced demonstration is T-34's).

**C-71 and C-72 re-grounded on the promotion text and PROMOTED** — two structurally different
**encodings**, not two parameter sets of one model: occupancy-encoded trapped charge; orientation-
encoded remanent moment. Falsifiers runnable on a flash tester and a VSM. **PROVED rows: 2.**

**Model:** `project_model` moved to the **activation-energy convention** (the midpoint convention
produced the 5–6-order azobenzene contradiction); steady-state guarded against the no-dissipator
arbitrary-vector case; `validate_project` 11 PASS under the corrected convention.

**T-41 (LANE_T41_EXTERNAL), first external contact:** under the corrected convention, **two external
measured anchors sit inside the model's envelopes** — the azobenzene thermal cis lifetime
(measured ~1e4–1e6 s; model envelope over the literature (E_a, f0) spread contains it; the old
convention gave 0.398 s) and the magnetic-media **~10-year design rule at `K_uV/kT = 40`** (model
7.5 years at `f₀ = 1e9`). The corrected alanine input **declines honestly** (predicted excess below
the instrument floor). **Registered debt: exact citation pin-down — knowledge-cited contact, not yet
source-pinned.** T-41 stays DOING.

---

## T-35 REPAIRS — the four named seal corruptions fixed; the O5 lane reproduces; full rerun in flight.

**`LANE_EM_EXTENT/holonomy.txt`** was a corrupted interleaving of two different runs — carrying a
wrong number (`769 classes = 2^dim H_1 = 4`) from an older script version **under a valid seal**, the
exact inversion a seal system must not allow. Resealed from a clean rerun (`768` loops, `4` classes,
`dim H₁ = 2`, internally consistent). **`f7_davies.txt`** and **`pa4_legibility.OUT.txt`** were stale
against post-sealing script edits; resealed to current. **`LANE_O5_ADVERSARIAL`** could not run
standalone (`o5_common` lives in `LANE_O5_APPROXIMATE`); with the path shim added, **all seven
adversarial scripts reproduce their sealed outputs byte-for-byte** — the 6 DIFFERS in the old
reproduction log were purely the missing import, not nondeterminism. **X-2 carries the T-21 note**:
the record-level reclassification stands; the collective question it never touched now lives in
C-77/T-42.

---

## T-42 — **C-77's FIRST INCREMENT: SATISFIED AT FORM LEVEL.** Distance earned; the boundary law derived; owners named; scope honest.

**C-78 — DISTANCE IS EARNED, AND IT IS BOUNDARY-CROSSING COST.** `d_W` = minimal admissible-writer
weight between configurations: a true metric (all axioms, all pairs, **all triples**, exhaustively —
`2²⁴` writers per pair at `L=5`), equal on the torus to **the minimal number of crossings of the `L`
transverse loops**, and to `d_code ×` Hamming **in the basis the metric itself selects**. The crossing
form `J` is *not* a metric (fails triangle, witnesses printed) yet `J mod 2` = symplectic pairing =
channel adjacency: **the geometry-grade distance and the Γ-form are distinct exact structures with a
common crossing origin — the record level not resembling the classical shape, exactly as C-77
expects.** Dimension **earned** as computed content degree (2 corner, 3 world). Attribution corrected
per the verifier: the odd-`n` nonexistence is **BORROWED (Rains, quant-ph/9704043)**.

**C-79 — THE DERIVATION.** From earned boundary structure alone: **interface rank is exactly one
degree below content in both tiers** — `deg IR = deg C − 1`, sub-extensive `IR ~ C^((D−1)/D)` — with
**parameter-free exact forms** `32·capP = (IR2+10)² + 8·(IR2+10) − 160` (every toric `(L,s)` to
`L=12`, 288 qubits, exact `F₂`) and `IFACE³ = 216·CAP²` (every world `n` to 12). **The mechanism is
exact bulk cancellation** — Euler density `1+1−2 = 0` per interior cell, so the source is
boundary-supported; scatter controls with no interior **break the law in both tiers**. 26/26 computed
gates; no classical form in any construction step; all three input probes adversarially not-refuted.

**THE COMPARISON, owners named:** MATCHES IN FORM the **area/entropy-boundary law** (Bekenstein,
Hawking, 't Hooft, Susskind; the stabiliser perimeter instance is **BORROWED** — Hamma–Ionicioiu–
Zanardi, Kitaev–Preskill; **ours** is the Euler bulk-cancellation route, the two-tier degree split,
the earned-dimension instrument, and the parameter-free forms). **Honest scope:** what matches is the
**interface** aggregate — stored record content is **volume** in both tiers; the coefficient is
venue-dependent (32 vs 216), no `1/4G` analogue; Newton falloff and horizon thermodynamics are
**NEITHER-YET**, open targets. The corner tier is **pure Γ**; the world tier runs through a coupling
term, declared under the openness clause — **the cross-tier agreement of the form is itself part of
the finding.**

New obstructions: **O-54** the falloff from Γ (the binding next step — two-region interface rank
against the earned metric), **O-55** no universal coefficient, **O-56** no earned thermodynamic
conjugate pair. **Flagged for the principal, not decided:** whether the mature C-77 requires more
than the interface reading, given stored content is volume.

---

## THE INTERFACE-VS-CONTENT QUESTION — **THE PRINCIPAL: LET THE RECORD SURFACE ANSWER IT.** Decision rule pre-registered.

The flagged question: T-42's area-form match belongs to the **interface aggregate** (boundary-scaling,
the entanglement reading — Bombelli–Koul–Lee–Sorkin, Srednicki), while **stored content is volume**
in both tiers (the strong-holographic content bound — 't Hooft, Susskind, Bousso — is *not*
reproduced). In nature the content bound is enforced by gravitational dynamics (collapse), so the
record surface currently has the profile of **matter before gravity has emerged** — and by
D-24 the content bound may not be imported to the record level; if it is real, it must emerge.

**The principal, 2026-08-20:** *"can't we let the record surface answer this question?"* Adopted as
the method. **THE DECISION RULE, REGISTERED BEFORE THE COMPUTATION (T-43):**

> Compute the **EXTERNALLY CERTIFIABLE CONTENT** of a region — of the volume-many records stored,
> how many can the outside world independently certify or write **through the interface**. Exact in
> the corner (what outside-supported operators can learn/flip), channel-counted in the world model.
>
> - **Boundary-bounded in both tiers** ⟹ the surface has answered: mature C-77 states its area-law
>   claim over *externally certifiable* content — what the world can know about a region, which is
>   what a horizon entropy counts — and the strong content bound is registered as an
>   **emergent-tier target** (the collapse analogue), not a record-level requirement.
> - **Volume-bounded** ⟹ the surface declines to answer; the question returns to the principal.
> - **Mixed/other** ⟹ reported as found; no forcing.

---

## O-54 — **JUDGED: THE HYPOTHESIS HOLDS. NO PURE-Γ FALLOFF EXISTS, AND THE DIVISION OF LABOR IS NOW COMPUTED.** C-77's second increment SATISFIED.

Three probes and a judge, **33/33 gates, 114/114 independent adversarial checks, no fatal
reinsertion anywhere** — every decaying law in every lane is labeled INSERTED at its point of use,
and the verifiers confirmed none was reported as Γ's.

**PURE-Γ TWO-REGION STRUCTURE, THE EXACT TAXONOMY** (toric corner to `L=12`, exact `F₂`; world
access model with the earned axis re-derived from interactions alone):

| character | the law |
|---|---|
| **zero beyond contact** | `I_IR = I_MI = 0` **identically** at every positive earned separation — zero, *not decaying* |
| **contact seams** | `I_IR = 2(s−2)`, `I_MI = s−2`; the `s=2` seam rank-absorbs to exactly zero — contact necessary, not sufficient |
| **topological constants** | winding `w` at every distance; `TEE = −1` exactly *(Kitaev–Preskill, Levin–Wen; instrument Hamma–Ionicioiu–Zanardi)* |
| **the one genuine separation law — GROWING** | **`w_min = d` exactly**: minimal admissible coupling-writer weight equals the earned separation, slope 1, intercept 0, exhaustive to `2²⁵` writers per pair. **Confinement character** *(Wegner 1971, Wilson 1974; Bravyi–Kitaev string distance)* — the opposite of a falloff, and **not gravitational** |

**THE FALLOFF ENTERS ONLY THROUGH THE COUPLING.** An inserted reach-`ℓ` row makes the same corner
pair separation-dependent **exactly at `ℓ = g+3`** — the instrument would have shown a falloff had
one existed. The world block aggregate **inherits** the declared mediator's inserted exponent, with a
measured aggregation correction (`q = 2.10`, analytically confirmed, out-of-sample 0.3–0.8%).

> ### **THE DIVISION OF LABOR — C-77's REFINED SHAPE, NOW COMPUTED RATHER THAN ASSERTED:**
> ### **Γ shapes the boundaries — the boundary-degree law and the two-region character.**
> ### **The coupling supplies reach and the falloff — the LOCUS where Newton-form would have to
> ### live under this claim (locus-match made; no exponent earned).**
> ### **Alpha supplies the costs — unexercised this increment.**

**Register corrections carried:** `dV = g_eff+1` on the torus (the A-lane finding said `g+1`); the
C-lane relay paraphrase was a transcription erratum, sealed output correct. **Taxonomy amendment
bound:** pure-Γ two-region relations include a linearly **growing** law, not only
separation-independent and contact-only ones.

**Named next (T-44):** which falloff exponents a **Γ-constrained** coupling can *reach* — the
weighted-instrument lane, coupling the exact `w_min = d` cost landscape to a declared mediator.
Until it runs, **no falloff exponent is earned.**

---

## T-43 — **THE RULE HAS SPOKEN: MIXED_AS_FOUND.** The surface answered more precisely than the rule asked — and left exactly one choice, which is the principal's.

**The corner tier answered outright, and with an identity nobody ordered:** externally certifiable
content **IS** the stabiliser cut-rank — `CERT = 2·PER − 10 = 8s − 10`, exactly the T-42 interface
law, verified by three independent routes with explicit outside certificates, robust to every honest
re-operationalisation the adversary could build. **The area-form aggregate now has operational
meaning: it counts what the outside world can learn of a region.** Strictly-outside writability is a
computed locality theorem (`WRITE0 = 0`); interface-layer writability is boundary-degree; stored and
hidden content are volume. Bonus exact structure: **thickness protection** — a band's record bit is
certifiable at any width but interface-writable only when thin (1, 2, 1, 0 at widths 1–4+). Scope
honestly: solid regions with interiors; all-interface geometries (comb, scatter) reach volume and the
volume-control fires.

**The world tier split, exactly:** the boundary bounds the certification **RATE** (per-epoch
`= 6n² − 12n + 8`, an exact min-cut, unbeatable by any schedule) — but the certifiable **TOTAL** over
epochs is the whole stored **volume** (`E_min ≤ 3` on the computed range). The lane kept the split
uncollapsed, as briefed. *(Corrections per the verifier: 26/26 gates, not 27/27 — sidecar bookkeeping
error, no number affected; the CAP_depth(1) identity carries no separate weight.)*

**THE RULING (pre-registered rule applied verbatim): MIXED_AS_FOUND.** The rule's phrase "externally
certifiable content" fixed the instruments but **no time convention** — and the corner, a static code
state, has no time axis, so the split is invisible there *by construction*, not settled there. Under
the **simultaneous** reading both tiers are boundary and the rule's first branch fires; under the
**anytime** reading the world certifies its volume and the interface bounds only rates. **The
conditional C-77 sentence and the emergent-tier target (the collapse analogue — a dynamics under
which HIDDEN = STORED − CERT is unstable) are staged, and issue only on the principal's reading.**
The judge's editorial note, carried at zero weight: a horizon entropy is itself a one-time count.

---

## T-45 — **THE PRINCIPAL'S QUESTION ANSWERED: THE CHOICE WAS NEVER THEIRS TO MAKE, AND NEVER OURS. THE SURFACE OWNS THE CLOCK.**

*"If it only surfaces one choice is that mine or just what the surface surfaced?"* — **computed
answer: neither a decree nor a loose end.** The split looked like a convention only because the world
model treated records as immortal. **Clause (ii′)'s own durability tolerance `t_m` supplies the
certification window** — a record must be certified within its own lifetime — and the exact law
`CERT_W(n) = min(n³, W·(6n²−12n+8))` then has **DEF-A's corner as its `W = ∞` limit: the anytime
reading IS the immortal-record idealisation**, the same corner the program already names. For every
finite-lifetime surface, **certifiable content is boundary-bounded at scale**, and the pre-registered
T-43 rule's first branch **fires surface-determinedly**:

> ### **MATURE C-77's AREA-FORM LAW SPEAKS OVER EXTERNALLY CERTIFIABLE CONTENT — what the outside
> ### world can learn of a region within its records' own durability.** (C-83; identity CERT =
> cut-rank from C-81.)

**Honesty clause from the same table:** every terrestrial census device sits far below its crossover
`n* ~ 6W` and certifies its **full volume** within lifetime — the boundary bound binds only at
enormous aggregate scale. *(Editorial, zero weight: invisible at laboratory scale and binding at
scale is the profile an emergent bound should have.)* **O-57 registered** — the collapse analogue,
the staged emergent-tier target.

---

## T-41 DONE — **THE EXTERNAL ANCHORS ARE SOURCE-PINNED.** And two directives registered: D-25 (real-data grounding, tool-enforced) and the proof's architecture.

`LANE_T41_EXTERNAL/CITATIONS.md`: azobenzene **t½ = 1.4 days at 35 °C, ΔH‡ = 0.915 eV** (ACS Cent.
Sci., PMC9951306); **Weller & Moser, IEEE Trans. Magn. 35, 4423 (1999)** — onset `35 ± 2`, `~60` for
10-year; **NAND detrapping `E_a ≈ 1.0 eV`** + JEDEC 1-yr EOL. All three sit inside the model
envelopes; the census's NAND 1.60 eV annotated to the pinned 1.0–1.6 range. Knowledge-cited →
**source-pinned**.

**D-25 (the principal):** the model is grounded in real record data, never the toy category —
world-tier surfaces carry provenance with pinned sources, corner carriers self-declare DEF-A, and
the constructor **refuses** undeclared surfaces once T-46 lands. **And the architecture: THE MODEL
IS THE OVERALL REPRESENTATION OF THE PROOF** — PROOF_V002 becomes the narration of `project_model`,
every proof step a model function with its validator gate and grounding. T-16's text carries it.

---

## T-39 — **THE AUDIT RETURNS NON-EMPTY. PF-6 FAILED IN 2026-08-18; ITS SUCCESSOR REGISTERS THREE SURVIVORS.**

Twelve-plus candidates, three rival advocates each, fairness rule enforced (a rival wins only if its
account *already made* the statement). **The Darwinism advocate claimed nothing whole. The QEC
advocate claimed six. Device physics claimed two.** Combined:

| survivor | the statement | why no rival owns it |
|---|---|---|
| **S-1** | the **durability-clocked certification window**: `CERT_W = min(volume, W·min-cut)`, `W = τ/t_epoch`, crossover `n* ~ 6W` | Darwinism's records are **immortal** — no durability window exists anywhere in its corpus; QEC's memory-time work bounds *storage*, never certification-within-lifetime; engineering takes the rate as a free parameter. *(Provisional on one commissioned literature check.)* |
| **S-2** | **flash alpha-channel discrimination**: one device carries an α-amplified Arrhenius channel (`A ≈ 240`) and an α-flat tunneling channel | stated by neither the varying-constants wing nor the device wing; falsifier = JEDEC retention-bake channel extraction, data exists, no lab needed |
| **S-3** | the thickness profile **1, 2, 1, 0** | corollary grade; the schema is QEC's, the non-monotonic integer instance was never stated |

**Everything else falls to named owners, matching the register's own concessions** — including
alpha's amplification logic, which is **Shlyakhter's move (Oklo, 1976)**, with the rival's own bounds
rendering any record-derived α bound uncompetitive (every predicted shift `< 3e-4` in `ln τ`).

**The creator step, now T-47:** all three rivals share one structural gap — **no account anywhere
owns a surviving-record COUNT law.** C-76 killed `k(t_m)` because its width was *chosen*; the natural
derived clock is the same `W = τ/t_epoch` that survived as S-1. A derived width would make `k(t_m)`
the one wholly program-owned falsifiable count law.

*Audit note: the enumeration agent's API connection dropped mid-relay; the advocates worked from its
sealed lane output, and the recorder's descriptive candidate ids are ruled canonical against
`LANE_T39_A_ENUM`'s sealed list.*

---

## T-46 — **THE UNIVERSAL RECORD MODEL IS BUILT.** Every registered headline from one entry point; D-25 enforced at the gate.

`model/geometry.py` + ten new `ProjectModel` methods + `validate_geometry.py`: **31 gates, every
reproduced number checked against its SEALED lane value**, chained to `validate_project` (**11 → 14
PASS** with the D-25 guard gates, backward compatible). The adversarial checker **re-derived numbers
beyond the gated range** — `s = 9, 10` interface ranks, `n = 11, 12` world rows, the ungated
`WRITE_B` sequence — straight from the sealed OUT files, all equal. Deliberately *not* re-homed: the
lanes' adversarial control batteries, which remain sealed evidence cited from the docstrings.

**The URM's public gate now enforces D-25:** `URM.surface()` **refuses** a world-tier surface without
provenance (the pinned-source registry carries Weller–Moser, the JEDEC/detrapping class, the ACS
azobenzene values) and **refuses** a corner carrier that does not self-declare `DEF-A` — the
idealisation can never silently pose as the world. The refusals are themselves validator gates.

---

## T-47 — **THE COUNT LAW REGISTERS. The width is the carrier's own — derived, two-faced by necessity — and `k(t_m)` is the URM's falsifiable census of surviving records.**

Three probes, three adversarial verifiers (not-refuted, high confidence), drafter verdict
**REGISTER_PARTIAL**. **No smuggled tolerance anywhere** — three independent tokenizer/source
censuses of every numeric literal on every conclusion path; the only `1e-2` strings left are prose
describing C-76's corpse.

> ### **ONE CRITERION — clause (ii′) on the record's own Liouvillian mode — YIELDS BOTH WIDTHS:**
> ### `δ_pop(t_m) = kT·ln(e^{B/kT}/(f₀t_m) − 1)` on the population face, `δ_coh(t_m) = ħ/t_m` on the
> ### coherence face — **two corners of one modulus, 22 orders apart on the same surface. C-76's
> ### error, quantified.**

**The staircase:** `k(t_m) = #{i : dEᵢ ≤ δ_pop,i(t_m)}`, drop times
`t*ᵢ = f₀⁻¹e^{(Bᵢ−dEᵢ)/kT}/(1+e^{−dEᵢ/kT})` — each record dying at its **shallower value's** escape.
Instrument-vs-formula `≤ 6×10⁻¹⁵` across the grid, confirmed by three independent instrument paths;
count discrepancy **0 at all 1201 points**. T-31's binary kill becomes the dated staircase 2→1→0.
**C-14 is recovered exactly as the symmetric corner** (with a derived factor-2 correction to the
commissioning text), and DEF-A as the `t_m → ∞` limit on both faces.

**Ownership, both ways:** Néel/Street–Woolley/Sharrock own the activation window as a *decay* device;
Charap–Lu–He and Weller–Moser own the symmetric corner; Preisach–Néel owns rate-level asymmetry.
**Wholly ours: the width derived from the record definition, the diagonal/coherence unification, the
margin-free integer census stated as a LAW, and the departure term `Σ_dead tanh(dEᵢ/2kT)` — remanence
persists while records die.** Falsifiable today on JEDEC-class MLC bake data and exchange-biased
media grain censuses. **Grade FORMAL; PROVED awaits the external-data run.**

---

## T-44 — **C-77's THIRD INCREMENT, SATISFIED AT FAMILY LEVEL. The critical identity IS the Poisson equation, and the Newton profile lives at exactly one computed design point.**

**The reachable classes (C-87), each located by computation:** exponential below `μ_c` (the
confinement cost `N_min·μ^d`, gated against the true `2²²` Γ-coset); **at `μ_c` exactly — computed
three independent ways — the earned dimension's OWN point-source potential and nothing else**, because
`μ_c = 1/deg` turns the gated resolvent identity into **the venue's discrete Poisson equation**;
divergent above. Computed **linear** in D=1, **marginal/log** in D=2 (brackets containing the exact
Spitzer anchors) — and the two critical kernels occupy **disjoint windows**, so the critical class is
the venue's own, proved by the cross-dimension discriminator. **The D=3 member (`1/d`) is
owner-attributed, not computed** — its probe overflowed and is in re-run (O-58 N1).

**The composition facts (C-88):** superposition is a property of the **admissibility rule** — exact
per-order integer identity under endpoint transparency, strictly subadditive under opacity; the
mediator kernel is positive everywhere so **occupancy can only accumulate and orientation screens**;
shadowing exists only under opacity and equals a **lengthening of earned separation**.

> ### **THE NEWTON COMPOSITION PROFILE — exact superposition, one-signed accumulation, no screening,
> ### no shadowing — IS REACHED AT EXACTLY ONE DESIGN POINT: R1 + OCCUPANCY.** Orientation gives the
> EM-like two-signed screenable profile.

**The judge's verdict on Newton: NEITHER** — writing MATCHES would substitute an owner for a
computation, the move D-24 forbids. **Three pieces stand (O-58):** the D=3 row; **masslessness** —
with the labeled hypothesis that `μ_c = 1/deg` is the *measure-conserving* writer normalization, so
if Γ's writer kernel conserves measure, **masslessness is measure conservation, not tuning**; and
whether the surface enforces the design point.

---

## T-24 — **CLAUSE (v) HOLDS ON THE NON-ABELIAN CARRIER — BY AN EXACT INTEGER OBSTRUCTION WHOSE MECHANISM IS THE GROUP'S OWN NON-ABELIANNESS.** And two readings of "protected" part company.

`LANE_T24_DV`, verifier not-refuted at high confidence with **every verdict-bearing number re-derived
by fresh independent code.** On `D(D₄)` 1×2 (dim 4096): the admissible single-edge algebra on each
contractible region is `span{I, T}` with `T` = right-multiplication by the central `r²`, and
`t_E = Tr(P_E T) = {30, −48, 12, 0, 6}` — **not all zero, so nothing is flippable by any admissible
unitary on any contractible region.** The mechanism: **`r² ∈ [D₄, D₄]` — characters kill it,
conjugation fixes classes.** The abelian `D(Z₂)` control on the **same lattice FAILS** (an admissible
weight-1 flipper exists — the known distance-1 proxy artifact), so the test discriminates; the
non-admissible controls flip exactly. **Minimal-torus vacuity proved from the cell structure**, both
conventions agreeing on every subset. Verifier's correction carried: the Wilson-character diagonals
and the `χ·class` family contain no records here — record constructions go through eigenspace
splittings.

> ### **D-27: "PROTECTED" HAS TWO READINGS AND THEY DIVERGE HERE.** `T` is a weight-1 admissible
> **non-trivial logical operation that flips nothing** — clause (v) as written HOLDS while its
> Knill–Laflamme code-distance renaming FAILS at weight 1. **The KL renaming has not earned its place
> at the record level** — D-24 applied to our own glossary. Protection claims now name their reading.

**O-41 updated:** protection is **transport-blind** at this proxy size — it does not distinguish
transport-fixed from transport-moved records; whether a larger non-abelian lattice separates them is
the live remainder.

---

## T-36 — **THE DIFFERENTIATED RECLASSIFICATION IS APPLIED.** Every FORMAL row now carries its class and owner.

Three range-partitioned classifiers plus a crosschecker (coverage **exact**: 184 FORMAL rows — the
review's "162" was the stamped subset; 22 newer rows included — none missed, none doubled, 12
overlap rows all agreeing; 31-row sample re-verified with 29 verbatim agreements and 2 adjudications).

**Final counts:** THEOREM **41** · EXACT **60** · MEASURED **41** · DEFINED **42**.
**Ownership:** ORIGINAL **104** · BORROWED **23** · ASSEMBLED **57**.

**Applied by the registrar:** every FORMAL row's GROUNDED field now opens with
`[T-36 CLASS: … | OWNER: …]`, existing substantive grounding text preserved; the systemic boilerplate
stamp (which self-refutingly category-mismatched every doctrine row — FLAG-1) replaced on 122 rows;
the **42 DEFINED-class rows moved to DEFINED status** (definitions cannot be true or false; the
world-contact question does not arise for them). THEOREM/EXACT/MEASURED classes stay at FORMAL with
their tags — the status carries the corner-scoped/world-contact axis, the tag carries the epistemic
class. **FLAG-2 fixed:** C-69's GROUNDED no longer carries the "not by inserting the Arrhenius rate"
clause its own evidence declares false; C-70's no longer lists the withdrawn azobenzene/alanine rows
as verified. **Carried for follow-up, not mass-edited:** the quantifier-outruns-computation EXACT
rows the crosschecker flagged (C-49's "every even n" from exhaustion to n=8; O-8's "ALWAYS" from
block dim ≤ 8; O-35's range) — each needs its scope sentence tightened when next touched.

Ledger tally now: **142 FORMAL · 49 DEFINED · 2 PROVED · 2 MEASURED**, with the failure/withdrawal
history intact.

**Housekeeping (post-T-36 commit).** The O-48-B manifest was stale — sealed before the lane's final
re-run; the current `p2d_largest_exact.txt` reproduces byte-for-byte from its script, so the manifest
was regenerated (the file was right, the seal was old). The documentation gate's "no output at all"
check counted only `.txt`; documentation, advocate, and classification lanes carry their sealed
findings as `.md`/`.tsv`, so those now count as output — the refusal on truly-empty lanes is
unchanged.

---

## T-27 — **THE PROCESS DOCUMENT IS CURRENT.** PROCESS_V002 restated as of 2026-08-20, adversarially verified twice.

The 2026-08-19 statement predated the amendment, the world tier, the emergence increments, and the
audit; it also carried a wrong exponent attribution (λ^{2n*} where `F-23` registers `λ^{2d}`) and an
O-11 citation used as support where the row registers an obstruction. The restatement covers the
amended definition (adopted — the ledger's O-51 statement was stale against the register's adoption
entry and was brought current, as was H-3's evidence tail), the corner existence theory, carriers and
clause (v) on both carrier families (C-89 kept at its proxy scope), formation through the two PROVED
encoding laws, the lifetime/steady-state laws and the count law, certifiability and the surface's
clock, cost, the emergence claim at verdict NEITHER, and the audit's three survivors. An adversarial
verifier read every backtick citation against its row: first pass returned 7 SEVERE / 7 MINOR, all
fixed; second pass returned 0 SEVERE, 3 MINOR, all fixed. **Gate: all 66 cited rows live; no
WITHDRAWN or FAILED row cited; the failed O-1 and PF-6 appear only as labeled history; banned-
comparison scan zero matches; the anchor's gravity claim matches the ledger's C-77 shape.** The
anchor itself needed no edit — its ~20 figure is the register's four-census figure, now stated beside
the census set's thirteen wherever the doc uses it.

**Next step (the route stays open):** T-16 will narrate the URM against this document; the document's
one standing debt is inherited from T-9 — the carrier-breadth marks now being applied feed §"WHAT IS
NOT ESTABLISHED" directly.

---

## T-44 LANDS — **THE D=3 CRITICAL ROW IS COMPUTED: THE MEMBER IS 1/d, AND THE PRE-REGISTERED RULE FIRES — NEWTON VERDICT: MATCHES AT MEMBER LEVEL** (C-90; C-77 increment 3 SATISFIED)

The interrupted world lane re-ran to completion (resume from cached probes; the corner and
composition lanes replayed). **LANE_T44_B_WORLD**, on the census access geometry's own deg-6 grain
lattice, earned D=3: `μ_c = 1/6` exact, located three independent ways; **at criticality the class is
a power law with exponent bracket containing 1** on all three rays inside the pre-declared
inverse-distance window, LOG and LIN excluded; `G` finite (D=3 transience the venue's own), Watson's
`1.51639` inside the computed bracket, `d·G(d)` converging onto a coefficient bracket
`[0.476369, 0.487321]` tightening onto Spitzer's `3/(2π) = 0.477465` — owners comparison-only, after
the class was computed. 58/58 gates, exact rationals on the measurement path, proven tails; the
adversarial verifier attacked with an independent Z³ DP, kernel deepening 1400→2800, an m=1000
divergence witness, and a continuum Fourier instrument forbidden to the lane — **not refuted, high
confidence, byte-identical rerun.** Cross-dimension discriminator: one instrument, three venues,
disjoint windows — D=1 linear, D=2 log, D=3 power — and `μ = 1/6` critical on D=3 while subcritical
on D=2.

**The supersession is grounded, not editorial.** The prior judgment's own pre-registered rule — *"a
computed 1/d bracket upgrades the verdict to MATCHES at member level"* (JUDGMENT.txt, N1) — is
applied on its own stated condition. **O-58 N1 CLOSES.** The verdict sentence keeps its load-bearing
conditional structure: unique critical member (computed) + occupancy of criticality (**not** earned)
+ design-point enforcement (**not** earned) — **never a claim that gravity is derived.** The judge's
own lane adds no measurement; every quoted number traces to a sealed artifact.

**Corrections logged by the lanes themselves** (in their D24_AUDIT files, per the register-not-chat
rule): the corner lane's first-run true-ensemble tolerance failed near the (3,7) wrap scale and was
re-derived; the world lane's first D=1 control ran at kernel depth 2000, gate-failed on truncation
precision (not class), corrected to the corner instrument's K=80000 with no threshold changed.

**Register updates:** C-90 appended (FORMAL); C-77 increment 3 SATISFIED with the verdict and its
conditions; C-87 annotated (the D=3 member computed, no longer owner-attributed); O-58 rewritten — N1
closed, **N2 masslessness is the ranked next piece** (μ_c = 1/deg is exactly the measure-conserving
writer normalization; the falsifiable increment: compute from the record surface's OWN writer
ensemble whether the induced per-link amplitude is the measure-conserving one), N3 the design point,
**N4 added: norm selection** (the 1/d law is exact in an emergent Euclidean norm over earned L1
separation — which norm the record's physics selects is open). **Next step named: T-48 appended to
the plan (phase E) — the masslessness increment.** Caveats carried verbatim from the lane: the
exponent is a bracket statement with finite-d drift honestly reported, not a symbolic derivation;
nothing in Γ yet places μ at criticality.

---

## T-9 — **THE CARRIER AUDIT IS APPLIED: EVERY FORMAL, PROVED, AND MEASURED ROW NOW SAYS WHAT CARRIES IT.** The reopened task closes on its own DONE_WHEN, honestly.

Six probes over all 146 rows in scope, defaulting to SINGLE-CARRIER (the external review reopened
this task precisely because two-carrier support was overclaimed); every TWO-CARRIER claim attacked
by an adversarial refuter checking that the cited evidence exists, concerns the row's actual result,
and the carriers are structurally different — same model at another size or parameter set never
counts. **Verdicts: SINGLE-CARRIER 111 · TWO-CARRIER 21 · NOT-CARRIER-SHAPED 14.** Coverage
146/146, no duplicates. Full table with per-row evidence pointers and kept refutation reasons:
`LANE_T9_AUDIT/T9_carrier_audit.tsv`.

**The marks that matter most:** the two PROVED rows — C-71 and C-72 — are **TWO-CARRIER**
(NAND-floating-gate; macrospin-CoCrPt), independently reconfirming the PROOF bar's own requirement.
C-69 and C-70 are marked SINGLE-CARRIER (macrospin): the audit found C-70's six-mechanism table is
six parameter sets of ONE two-state GKSL build — consistent with the solidity review's earlier
demotion, now visible in the ledger. Refuters demoted several claimed second carriers to weakened
spot-checks (e.g. C-88's 2-D lattice is a dimension discriminator, not a second venue for the
screening gates; O-15's bath-size result lives on [[5,1,3]] alone).

**Consequence: T-15 UNBLOCKS** — the three-roles statement can now cite carrier-marked rows, and
T-16's "no step resting on a single carrier unless marked" is enforceable by grep. The marks feed
PROCESS_V002's standing debt directly.

---

## T-15 — **THE THREE ROLES ARE ONE STATEMENT, AND EVERY LOAD-BEARING CLAUSE STANDS ON TWO CARRIERS.** A-PR restated; the proof chain's head is cut.

The restated A-PR (`LANE_T15_ROLES/A_PR_RESTATED.md`, applied to the ledger row): **EM supplies the
complex and the record** — corner: capacity `2^dim H₁` exact on and off manifolds (G-10); world: the
PROVED encoding laws (C-71, C-72). **Γ supplies space, writer, protection and channel** — space:
capacity independent of protection (G-11), records on `D(G)` iff `|G|` a power of two (C-41, O-35);
writer: `d_W` the earned boundary-crossing metric (C-78), no pure-Γ falloff, division of labor
(C-80); protection: the census's metastable barriers with the corner as the `E_b → ∞` limit (C-66,
C-75); channel: conditional-evolution copying (F-20), clause (ii) on the environment (C-17), the
three reachable coupling classes (C-87); emergence in one sentence at C-77's exact current scope.
**Alpha sets the cost** — first-order splitting (O-2), threshold `= d` (F-11, O-10), the world cost
as the barrier in `k(t_m)`'s drop times (C-86), alpha's value through `E_b` explicitly open (T-38).

**Discipline enforced, not asserted:** an adversarial row-fidelity verifier read every citation
against its clause (clean); a mechanical gate confirmed every load-bearing citation carries the T-9
TWO-CARRIER mark and none is WITHDRAWN, FAILED, or PARTIAL (clean, round 1). The corner role rows
A-EM/A-GR/A-AL — all SINGLE-CARRIER by the audit — appear as context only. The old A-PR's PARTIAL
("gauge tier proved on ONE carrier family") is superseded by citation discipline: the statement now
rests only on rows that survived the carrier audit. **T-16 UNBLOCKS** — the proof is next, and its
architecture is fixed: PROOF_V002 is the URM's narration.

---

## T-48 LANDS — **MASSLESSNESS IS MEASURE CONSERVATION: THE CONDITIONAL IS A COMPUTED IDENTITY, AND WHAT REMAINS IS ONE COMPUTABLE BIT** (C-91; O-58 N2 split, residue merged into N3; C-77's occupancy condition PARTIALLY EARNED by the judge's scoping)

Three lanes, three adversarial verifiers with independent machinery (fresh sample points off every
declared grid), a judge adding no measurement — **not refuted anywhere**. The kernel tier: the
unitary writer algebra forces measure conservation for EVERY ensemble weighting — unitarity, not
uniformity, conserves; every conserving kernel is exactly critical, `det(I−K) == 0` beside exact
nonzero controls; conservation does NOT force link-uniformity, and the exact supplement is named —
invariance under the venue's edge-transitive automorphisms, under which `1/deg` is forced
identically. The corner tier earns uniformity from the algebra itself (the elementary writer's
invariant tuple identical on every link) and re-locates `μ_c` in-lane. The world tier fires the
ambiguity guard as commissioned: three honest ensemble constructions, none silently preferred —
**E1 transport is critical at every dE and barrier** (erase-behind releases exactly what write-ahead
costs; `E_b`, `f₀`, `dE` only set the clock); **E2** conserves at every dE, uniform exactly at
`dE = 0`; **E3, the model's own erase channel, is never critical** — the mass gap in closed form,
**`ln(μ_c/μ) = ln(1 + e^{dE/kT}/l)`**, with `f₀` and `E_b` dropping out exactly. The DONE_WHEN
control landed in every lane, and in the world lane it is the physics: bath polarization is bias,
and bias is mass.

**The obstruction, plain (the DONE_WHEN's second branch):** `μ = μ_c` is NOT derived on the physical
surface. Nothing forces the antecedent — K0 and E3 are honest non-conserving constructions, so
whether Γ's GR3 writing conserves measure is a real physical bit, now THE SAME QUESTION as N3's
design point with computed stakes on every branch; and ensemble-weight symmetry is unearned extra
data (the anisotropy frontier, N5). **C-77's "occupancy of criticality" moves to PARTIALLY EARNED,
scoped — issued as the T-48 judge's own call on the computed record; no pre-registered rule governs
N2, so this scoping's ratification sits with the principal** (the verdict sentence is unchanged in
kind: MATCHES at member level, never gravity-derived). D-1 was kept absolutely: Newton appears in no
T-48 lane, comparison included. In-lane corrections are in the lanes' own D24_AUDIT files.

**Next step named: T-49 appended — the conservation bit of GR3 writing** (formulate "one writing
event redistributes writer measure vs creates/destroys it" as a computable property of the writing
tier and decide which honest ensemble Γ enforces), with companions ranked: the anisotropy frontier,
link-indistinguishability forcing the weight measure, E2's decay class at `dE ≠ 0`.

---

## T-16 LANDS — **THE PROOF IS THE MODEL'S NARRATION, AND ITS COMPLETION CRITERION IS A TOOL REFUSAL** (`PROOF_V002.md`; `replicate/check_proof.py`)

The architecture the principal fixed is implemented literally: **`PROOF_V002.md` is the narration of
the Universal Record Model.** Six sections are the URM's six layers — DEFINITION, LAWS, FORMATION,
CORNER, GEOMETRY, ROLES — and every claim is one block carrying five cells: the **model function**
that computes it, the **validator gate** that fires on it, its **grounding** (D-25 provenance, sealed
lane, or pinned external source), its **ledger rows** with their statuses and T-9 carrier marks, and
the **scope** that travels with it. §6 is the document's one comparison section. §7 is the restated
A-PR. §8 is the standing debts, with the full limits statement left where it belongs, at `T-17`.

**The document, in its own printed numbers:** **71 claim blocks · 100 distinct ledger and plan rows
cited · 40 blocks resting on no `TWO-CARRIER` row and saying so in their scope cell · 9 citing a
`PROVED` row · 31 carrying no validator gate · 17 with no model function behind them.** Those counts
are computed from the assembled document at build time and printed in its own front matter, because a
proof that prints its coverage cannot quietly lose it.

**T-16's DONE_WHEN is enforced by `replicate/check_proof.py`, not asserted.** Eleven rules, each
tested against a fixture built to break it and only it: R1 the five fields · R2 every cited ID is a
row in the status ledger or a task in the plan · R3 no `WITHDRAWN`/`FAILED`/`RECLASSIFIED` row is
leaned on · R4 the printed status equals the ledger's — **the stale-proof failure mode this tool
exists for** · R5 the printed carrier mark equals the T-9 audit's verdict, or `UNAUDITED` · R6 a block
resting on no `TWO-CARRIER` row must open its scope cell `SINGLE-CARRIER —` · R7 the model cell names
a `def` that exists under `model/` · R8 the gate cell names a check that actually fires, f-string
check names matched by template · R9 the word `PROVED` in prose requires a `PROVED` row · R10 the D-1
banned-comparison scan, its pattern read from `on_finding.sh` at runtime so there is one copy and not
two, exempting exactly one comparison section · R11 the coverage summary, printed on every run, pass
or fail. The tool exits 2 rather than passing when it cannot read the ledger or the audit: **a gate
that reports PASS because it could not find the record is worse than no gate.**
**Twenty fixtures**: one valid, one per rule built to break that rule and only that rule, three edge
cases (bare IDs, a three-column row, a second comparison section), four plan-citation cases and two
gate-name cases. Every rule fires on its own fixture and on no one else's. Loud-failure paths tested
in a stub root: a missing ledger, a missing audit, an `on_finding.sh` with no pattern line, a missing
`model/`, an audit verdict outside the four marks — all exit 2, none exit 0.

**How it was built, and what the adversaries took out of it.** Six layer probes returned structured
claim tables; six adversarial verifiers, default-refuted with independent machinery, attacked every
field of every block — **40 of 67 blocks refuted**; six correctors landed the corrections, rejected
the verifier findings they could demonstrate were wrong, and added two blocks the verifiers found
missing. Then **four whole-document lenses** — outside-physicist,
overclaim-hunter, coherence-critic, completeness-critic — each reading the entire document, which no
earlier agent had done: **59 findings, 6 of them blocking.** A second correction round landed those.
The blocking one that mattered most was self-inflicted and is worth recording as method: the layer
headers had been written before `check_proof.py` existed, and one of them asserted flatly that the
document's own gate was not in the repository while §0.3 told the reader to run it. **Section headers
now carry no claim that is not also in a block** — the gate parses blocks only, so a substantive
claim in a header is a claim outside the contract.

**Corrections the round forced, and they are the substance of the landing:** the D-15 inversion in
`P-FORM-2` (a zero's own configuration named as its positive control); `P-DEF-1` reporting only passes
while C-69's own DEF-A control — all four exact clauses failing on the same grain — sat in the sealed
source unquoted, and the demotion substance dropped (**the rates ARE the inserted jump strengths; no
measured retention datum enters anywhere**); `P-DEF-2` contradicting itself about which lane its two
positive controls sit in, and compressing the census's declared three-decade latent-image uncertainty
to "about a decade"; `P-DEF-8` leaning on two control rows C-70's demotion note had already withdrawn;
`P-FORM-10`'s margin overstated as four orders where the sealed numbers give 3.4.

**Two placement corrections the registrar required.** `P-ROLES-6` stated the Newton verdict inside
§8; **D-1 permits Newton in the final comparison section only**, so the block was rewritten as what it
actually is — three of the emergence claim's four conditions are not earned — with the comparison left
to §6's single block. `P-ROLES-11` said empirical contact outside the two `PROVED` rows is zero; that
predates `T-41`, and the block now states the contact exactly: the two `PROVED` rows' falsifiers on
standard instruments, plus three pinned external measured values beside the model's own numbers.

### THE ERRATUM — **C-72 MOVES OFF `PROVED`. THE PROGRAM NOW HAS ONE `PROVED` ROW, AND WRITING THE PROOF IS WHAT FOUND IT.**

The outside-physicist lens took the two `PROVED` rows and asked the bar's own question: could a
stranger run this? **C-72's registered PREDICTION — the accumulation ratio `|Σ|/Σ|·|` is "1 for every
data pattern on an occupancy-encoded surface" — is an ALGEBRAIC IDENTITY of scoring an erased cell as
exactly zero charge.** A cell scored zero enters both sums as nothing, so `|−qS|/(qS) = 1` for every
0/1 page whatsoever: a check with no branch on which it could have come out otherwise. **The sealed
lane's own source says so in terms** (`LANE_T34_NAND/t34_nand.py:63-68`: the ratio is 1 IDENTICALLY,
the draws beneath it a consistency check of the premise and not independent evidence). The same model
layer, twelve lines away, gives those same erased cells a signed `±5 e` over-erase residual. **The two
were never combined.** Combine them on the model's own sealed pages and the ratio is
**`0.968134`–`0.979799`, pattern-dependent, not one page at 1** — which is C-72's **own registered
FALSIFIER** ("a ratio that depends on the data pattern"), fired by its own model. Reproduced by the
registrar, by the erratum lane, and by two refuters, all to the last digit.

**What was computed, and survives.** The data-independent floor
`ρ ≥ (Q_p f − Δ(1−f)) / (Q_p f + Δ(1−f))`, valid above `f = Δ/(Q_p+Δ)` — **confirmed and TIGHT**, the
minimum attained exactly when every residual sits at `+Δ` (brute-forced over the `(Σr, Σ|r|)` polytope
at eleven `f`, recovering the closed form to `1e-9`; 20 000 adversarial edge pages, zero violations;
one cell at `Δ + 1e-9` breaks it). **The floor contains no `N`**, while an orientation surface carrying
real data screens as `N^{-1/2}` — so **the two encodings differ in kind and their separation grows as
`√N`**: measured slope `+0.511`, against an all-programmed control at `0.000` and a sampling-noise
surrogate at `-0.0002`, `11×` at `N=10³` → `112×` at `N=10⁵`.

**What does not survive, and it is why the row moves.** A replacement protocol was drafted and then
**REFUTED by two independent refuters, both returning REFUTED with their own machinery.** `ρ` is not
translation-free: mis-setting `V_t,neutral` by under five electrons — 4.8% of the program window,
about `0.19 V` on a `4 V` window — drives `ρ` below the floor, and five electrons the other way
returns `ρ = 1.000000` exactly, **restoring the very tautology the erratum exists to destroy.**
`V_t,neutral` is not a datasheet number, and the proposed text forbade the one reference a `V_t`
histogram does supply. Its falsifier clauses fire on ordinary physics: a fixed-length record in a
growing page screens as `N^{-0.57}`; a 5% error in nominal `Q_p` with an in-spec biased residual puts
a good page below its own floor.

**The ledger, moved:** `C-72` `PROVED → PARTIAL`, `BLOCKED_BY T-50`, its GROUNDED cell rewritten into
WHAT HOLDS and WHAT DOES NOT. **`C-71` stands**, and the reason is specific and now stated in the row:
its claim is about the **SIGN**, read as the shift of a programmed page's `V_t` distribution against
**the same part's own erased population** — a within-part comparison needing no absolute baseline. Its
PREDICTION gains the guard the erratum earned: the sign claim holds for every page whose `|ΣQ|` clears
the surface's declared unwritten tolerance, and a page below it is read as unwritten and carries no
sign claim (net-positive page fraction `0.000` at `f ≥ 0.01`; at `f = 0.005` the page sum `−499 e`
sits an order inside the declared `5000 e`).

**The gate, replaced.** `model/validate_geometry.py`'s `C-71 occupancy: written ratio == 1 for EVERY
pattern` compared against a literal and could not fail (`D-8`). It is **removed**, and six checks
stand in its place — the floor, the discriminator at matched `N`, the widening with `N`, and three
`D-15` controls in different configurations under the identical treatment. **Three of the six flip
under a mutation that makes the occupancy write two-signed** — measured, not asserted, and the
corrector wrote down that it is three and not six when the commissioning brief said six.
**36/36 geometry gates, chain `PASS`.**

**`ledger/status.py` gained a `blocked` command** in the same landing: `PARTIAL`'s own definition in
the closed vocabulary is *"one direction proved, the other open — named in `BLOCKED_BY`"*, and until
now no command could write that column, so the vocabulary's promise was unkeepable through the tool.

**Registrar's slip, logged:** the first `plan.py add` for `T-50` passed a phase number where the phase
NAME belongs and left `ORDER` empty, which made `plan.py` refuse to render. The row was repaired in
place — phase, `ROW`, `ORDER` — with its task text and `DONE_WHEN` unchanged.

---

**A finding the proof surfaced about the ledger itself, registered and not silently repaired:** rows
`X-4`, `T-VI.3` and `T-VI.4` are still `BLOCKED` carrying the texts *"empirical contact is zero"* and
*"no distinguishing prediction is identified"*. Both predate `T-41` (external anchors pinned) and
`C-84` (the distinguishing audit returning three survivors, external checks owed). **The rows are
flagged in `PROOF_V002` §8 and in `REPLICATE.md`; they are not re-audited here.** Their proper home is
`T-26`'s null re-audit, and a task is appended for it.

**`REPLICATE.md` brought current in the same landing** — it is the document an outside physicist reads
first, and three of its passages had gone stale against landings that came after them: the reading
list now carries `PROOF_V002.md` and its gate; the T-9 paragraph now states the audit's real verdicts
(111 / 21 / 14) instead of the pre-audit apology; and "empirical contact is zero" is replaced by what
the contact actually is, with the three stale rows named as stale.

**Next step named.** `T-17` — the limits statement inside the proof — is `T-16`'s successor and is now
unblocked. Beside it the proof states its own standing debt in its front matter, computed rather than
described: **31 of 71 blocks carry no validator gate, and 40 rest on no
`TWO-CARRIER` row.** Both numbers are printed, not described.

**Two seal items found while landing, and neither is resealed to make a gate green.**
`LANE_SCALE_D_THRESHOLD.sha256` was **stale against its own committed content** — every file matches
`HEAD` and none matched the manifest, so the manifest was committed wrong at `e5198cd`. It is
regenerated here, which is a statement about what is in the repository and not a claim that the lane
reproduces; **that lane is still ahead of the in-flight full run and its reproduction is `T-35`'s.**
`LANE_O48_B_SEPARATION/p2d_largest_exact.txt` was rewritten by the in-flight run in its wall-clock
`time s` column alone, every physics figure identical; the committed file is restored rather than the
timings baked into the record. `replicate.sha256` will go stale again while `reproduce_full3.log` is
still being written, and that is the run, not a defect.

---

## THE C-72 RULING — **THE PRINCIPAL SIGNS OPTION A. THE STANDARD HELD, AND THE REPAIR IS DIRECTED.** (`C72_BRIEF_V001.md`; `T-50` rewritten)

**The principal, 2026-08-20, ruling on the `T-16` erratum:** *"Sign the ruling as Option A, register
the defect, and let `T-50` earn the repair. The standard held."*

**`C-72` stands at `PARTIAL`, `BLOCKED_BY T-50`. `C-71` stands at `PROVED`. The program reports one
`PROVED` row.** The ruling was put with its counter-argument attached — that `PARTIAL` understates a
discriminator which is computed, adversarially confirmed and structural — and Option A was taken with
that in view. The brief the ruling was made on is `C72_BRIEF_V001.md`, sealed and committed here so
that what was in front of the principal is part of the record and not a summary of it.

**THE REPAIR IS DIRECTED, AND THE DIRECTION IS THE RULING'S:** *stop trying to rescue an absolute
single-page ratio.* `T-50` is rewritten around a **baseline-free differential observable** — the
contrast between written and unwritten sectors of the **same part in the same read**, whose exponent
in block size separates the encodings. **Three constraints were computed before the task was written,
because each is a way the repair could reproduce the defect in a new costume:**

1. **THE RAW SCALING EXPONENT IS NOT BASELINE-FREE, AND THIS IS THE ONE THAT MATTERS.** A common-mode
   offset of **`0.5 e` per cell — one two-hundredth of the programmed charge — drives the ORIENTATION
   exponent from `0.493` to `0.999`**, making a screening surface indistinguishable from an
   accumulating one. At `2.0 e` it is `1.000`. The **written-minus-unwritten contrast holds at `0.999`
   at every offset tested.** So the contrast and the exponent are **not alternatives**: the contrast is
   what makes the observable baseline-free, the exponent is what makes it untunable, and the repair
   needs the exponent **of** the contrast.
2. **CENTRED VARIANCE DISCRIMINATES NOTHING.** `Var(Q)` scales as `N` for **both** encodings —
   measured `N^0.97` for occupancy against `N^1.00` for orientation. The discriminating statistic is
   `E|Q|` (exponents `1` against `1/2`) or the **uncentred** `⟨Q²⟩` (`2` against `1`).
3. **THE PROGRAMMED DENSITY MUST BE FIXED IN THE OBSERVABLE'S DEFINITION.** A fixed-length record in a
   growing block gives an occupancy surface the orientation exponent — fitted `−0.572`, `−0.889`,
   `−0.878` — which is refuter A's counterexample returning through the new door.

**THE GATE IS A PRECONDITION ON `C-72`'S RETURN, by the ruling.** `T-50`'s `DONE_WHEN` now carries both
halves: the observable **and** a hardened gate. The structural-claim check must fail at rate `1.000`
under an adversarial mutation suite covering at least the two-signed write, a non-zero-mean residual,
and a programmed density falling with `N`; and `control A` is repaired or dropped.

**A CORRECTION TO THIS SESSION'S OWN COMMIT MESSAGE, logged rather than left standing.** `091573f`
says the six replacement checks have "real failing branches." **They do not, uniformly.** Under the
designated two-signed-write mutation the registrar measures **four of six** flipping — `floor`,
`discriminator`, `control A`, `control B` — while **`widens` PASSES**, and `widens` is precisely the
check that gates the structural claim the surviving argument rests on; refuter B measured it failing
on **9 of 50 seeds**, about `0.18` power. `control A`'s equality half cannot fail at any tolerance —
verified passing at `Δ = 1, 5, 20, 50, 90, 99` — because `RHO(1) ≡ 1` and the all-programmed page has
zero erased cells for the treatment to act on; its force comes from its second conjunct alone. The
replacement is a real improvement on an identity that could never fail. **It is not yet a clean gate,
`PROOF_V002`'s own scope cells say so, and `T-50` now owns closing it.**

**`ledger/plan.py` gained `donewhen`** in this landing, for the same reason `status.py` gained
`blocked`: `DONE_WHEN` is what makes "done" checkable rather than a judgement call, and it was
reachable only at `add` — so sharpening a completion criterion meant retyping the task, in a plan
whose whole discipline is that it is retrieved and updated and never retyped.

---

## T-51 IDENTIFIES THE INSTRUMENT — **THE FIELD READING IS THE WRITTEN-VALUE DIFFERENTIAL OF A TEST RECORD'S OWN LAW** (C-92; `FIELD_INSTRUMENT_V001.md`; `LANE_T51_IDENT/`)

**The principal's commission, 2026-08-20:** O-39 said the field side was a missing instrument with no
task for it. The principal directed: *"Let's identify the instrument."* Identified — by a judge panel
over **three designs from deliberately independent starting points** (a fourth, the geometry-response
angle, failed in flight and is owed), each attacked by a D-1/D-24 importer-hunter and a measurability
skeptic. **All six critiques: `VIABLE_WITH_REPAIRS`. No unrepaired D-1 violation found on any path**
— every critique ran a real search for a classical form functioning as requirement or test. The three
designs probe **different channels** — carrier-holonomy response of a test record's spectral law,
bath-mediated induced energy, bath-borne record information in bits — so the verdict is a
**sequence, not a rivalry**.

**FIRST: THE SECOND LUMP.** The surface's only native test object is another record, so the field
reading is `F(D) = Δ(b=−1; D) − Δ(b=+1; D)` — the shift of a weak probe record's own tunneling
splitting with the *value* of distant written content, at earned separation `(d_gen, w_enc)`, through
the program's own priced mediator. **It is literally O-39's named minimum** — a two-lump induced
energy as a function of separation — and it was the only design whose first computation **both** its
critics independently rebuilt from the repository's conventions, reproducing every exploration number
to three significant figures (`F(contact) = −1.99e−3`, `F(far) = +1.94e−4`, onset orders 3.0/3.9
against enclosure costs 3/4, unwritten ≡ source-absent at 6e−15). The artifact structure is the
cleanest achievable: written and unwritten are **two exact sectors of one Hamiltonian**, so the
mediator's furniture cancels in the differential by construction, and a nonzero `F` requires an
enclosure-class amplitude — **content-attributable by algebra, not by control**.

**The audit earned its keep before commissioning:** the sign-constrained coset minimum admits
disconnected representatives the dynamics cancels (computed counterexample at 3×2 — coset minimum 3,
measured onset 4.0), so **`w_enc` is redefined over CONNECTED enclosing strings and gated before the
onset verdict is scored.** The winding-sector sweep is mandatory before any sign of `F` is attributed
to content. Pre-registered rule `V1–V5`, both closures live: **ALL PASS** → the record surface has a
field side in the only sense it has earned, and the two-source composition at 4×4 runs next — **the
mod-2 saturation kill, first, because it is the fastest way the angle dies**; **V1 FALSE** after the
mediator-family sweep → the negative closure is registered, C-80's pure-Γ zero propagates to the
dynamical probe, **the emergence claim is exhibitable-not-provable, and T-17 carries that sentence.**

**Second and third lanes** (commissioned in order, repairs binding, recorded in the lane): THE
HANGING CLOCK — bath-suspended two-level clock reading the exact four-term Casimir-style subtraction;
its own computed design fact: **a degenerate probe is exactly gauged away (contrast ~1e−14), so the
probe must be a clock**; its non-duplicated deliverable is whether an object at separation comes to
*hold record bits* or only an energy response. CERT-SHADOW — the certification deficit of a disjoint
region in **bits**, renamed FORMATION SHADOW until bridged to C-81's `CERT`; **its static arm is a
cheap provable rigidity theorem to take regardless of ranking** — static certifiability has no field
side on stabiliser venues, the certification-currency mirror of C-80's zero-beyond-contact.

**What this does not settle, stated at registration so it cannot be discovered later:** every field
instrument on this surface is **mediated** (C-80), and whose field that is, C-77 must absorb — no
control can decide it; both energy-channel readings are **VALUE, not accumulating AMOUNT** — if the
field side cannot compose, the field side and the source side do not meet the way emergence at scale
needs, which is why the composition kill runs first; all shape-at-scale claims wait on the unbuilt
signed connected kernel, and criticality is O-58's bit, never assumable; metric, connection and
deflection remain unconnected to anything computed; **empirical contact: zero.** An instrument is
identified; **no field has been measured.**

**Next step named: commission `LANE_T51_A`** — the Second Lump's first computation on the toric 3×3,
per the commission in `FIELD_INSTRUMENT_V001.md` §1, after T-35's run completes (compute contention).

**Scope correction to the T-51 registration, on the principal's directive (2026-08-20), and it is
binding on every lane in the sequence:** *"Let's be careful not to be too prescriptive on 'what'
emergence actually is. We're trying to find gravity emerging. The mechanism for accumulation is
whatever it proves to be."* The registration above called the two-source composition computation a
"kill." That framing imported a requirement — that the field side must compose the way the source
side's accumulation standard does — and it is exactly the class of error D-1 exists to catch, one
tier up. Corrected in `FIELD_INSTRUMENT_V001.md` and in C-92's row text: the composition computation
runs first because it is the **most informative**, and **every outcome registers as the surface's own
composition law** — superposition, mod-2 saturation, screening alike. The source side's sign-definite
accumulation standard is not imported as a requirement on the field side. How any measured
composition law relates to classical gravity's is a question for the comparison tier at scale, under
C-77's standing caveat that record-level measures may behave unlike their analogues elsewhere.

---

## T-52 LANDS — **THE CARRIER AUDIT REACHES EVERY ROW, AND THE EMERGENCE CHAIN'S HEAD IS CONFIRMED SINGLE-VENUE** (audit rows C-90 · C-91 · A-PR; the at-registration rule)

The T-9 method applied unchanged to the three post-audit rows, verdicts drafted default-refuted from
repository evidence and spot-verified by the registrar against the cited lane lines:

- **`C-90` — SINGLE-CARRIER (macrospin-CoCrPt).** The D=3 critical result stands entirely on the one
  deg-6 grain venue; the D=1/D=2 venues are a cross-dimension discriminator, the exact C-88 demotion
  pattern, and the adversarial verifier's independent machinery ran on the same carrier. **The
  fragility flagged at the T-16 landing is now a recorded fact, not a suspicion: the Newton-verdict
  chain's head stands on one venue.** Its second carrier is real work owed, not a bookkeeping mark.
- **`C-91` — TWO-CARRIER (spin-chain; toric-2x2; macrospin-CoCrPt).** The headline identity ran with
  full per-venue gates on the C8 ring, the toric family, and the grain venue — with the scope kept
  that the corner tier's algebra-earned uniformity is toric-family only and the world tier's
  E1-criticality and mass-gap closed form are grain-lattice only.
- **`A-PR` — NOT-CARRIER-SHAPED** (role-assembly, the C-85/G-13 precedent class), all seventeen
  load-bearing citations verified TWO-CARRIER in the sealed table. **And the refuter surfaced a real
  breach:** C-72, load-bearing in the EM-world clause, moved to PARTIAL *after* T-15 landed —
  breaching the restatement's own live-non-PARTIAL gate. Recorded on the A-PR row; until T-50 lands,
  the EM-world clause rests on C-71 alone; the disposition travels with T-50.

**The rule that stops the debt re-accumulating** is now in `LANE_T9_AUDIT/METHOD.md`: a newly
registered `FORMAL`/`PROVED`/`MEASURED` row is audited **at registration**, in the same landing.
`check_proof.py` R5 enforced the propagation mechanically — five blocks failed the moment the
verdicts landed, and the proof was rebuilt under the new marks (its no-TWO-CARRIER count improving
40 → 38 because C-91's mark is now real). Zero `UNAUDITED` remains in the audit's scope. T-52's
DONE_WHEN is met. **Next step named: C-90's second venue** — a structurally different D=3 carrier
for the critical member — folds into the T-49/O-58 queue where that computation naturally lives.

---

## THE OWED FOURTH DESIGN LANDS AS A THEOREM — **THE EARNED METRIC IS CONTENT-RIGID ON STABILISER VENUES, AND THE FIELD CAN ONLY LIVE ONE TIER DOWN** (C-93; `LANE_T51_IDENT/FOURTH_*`)

The geometry-response angle, which failed in flight during the T-51 round, is delivered — and its
honest branch fired: **not an instrument, a rigidity theorem**, exactly the outcome the commission
named as a result rather than a failure. Three size-free mechanisms, 22/22 gates, **every
load-bearing number reproduced by the critic's independently written machinery** (own F₂ kit,
enumeration, partial trace), verdict RIGIDITY_CONFIRMED with six repairs adopted, none touching a
number: writers translate labels state-independently (`d_W` exactly content-blind, per-pair at
L=2,3,4); the writer-class landscape is defined by pairings against operators, never states; and a
region's reduced state responds to a distant write **iff** it supports an enclosure detector under
the winding-preserving representative convention (unrestricted the iff fails 45/495; restricted,
0/495 exhaustively at 3×2).

**Why this strengthens rather than weakens the instrument:** the integer tier carrying no field is
what forces the field reading into the real-valued amplitude over the rigid classes — which is
literally the Second Lump's `F`, with the onset locked to **connected `w_enc`** placement by
placement (3.995→4, 2.980→3, 4.988→5, 3.980→4, and the critic's off-script fifth placement
4.987→5). The lane also found a **second counterexample to the unconnected spec at the commissioned
3×3 venue itself** (old-spec 4, connected 5, onset 4.99): `LANE_T51_A`'s V3 scores against connected
`w_enc` per placement, and its brief now carries the cross-check. The winding annex independently
confirms V5's necessity — the sign is winding-sector-resolved.

**The responsive-venue statement, delivered:** all three rigidity mechanisms require stabiliser
exactness; none survives real-valued costs. The metastable/world tier is where the metric itself
could respond, measurable in C-91's own currency — **does one written record shift `dE` for an
adjacent write in the E1/E2/E3 writing tier?** ("bias is mass.") That computation naturally joins the
T-49/O-58 queue. C-93 registered FORMAL and **audited at registration per the T-52 rule**:
SINGLE-CARRIER (toric family), the second carrier absent by construction — the theorem is *about*
stabiliser venues, and the metastable tier where it may fail is the responsive-venue question, not a
second venue for this result.

---

## THE C-86 EXTERNAL RUN — **THE FIRST GENUINELY EXTERNAL COMPARISON TABLE, AND THE HONEST VERDICT IS NOT-YET-COMPARABLE. PROMOTION DOES NOT FIRE.** (`LANE_C86_EXTERNAL/`; C-86 stays `FORMAL`)

The run C-86 has owed since registration: published data hunted on both arms, pinned house-style,
the model side computed with closed forms evaluated (never re-derived), and the whole thing attacked
by a refuter who **re-fetched nine sources first-hand** — Cai '17 (Table 5 extracted from the PDF
itself), the ETH HPCA '15 data, HotStorage '21, Malavena JEDS '23, JEDEC's own committee deck,
Wernsdorfer's nanomagnet review, Funatsu's superparamagnetic-MTJ telegraph paper and its Zenodo
deposit. Both lane instruments reproduce byte-identical.

**The table's verdicts, refuter-checked row by row:** five AGREES rows — drift ordering strictly
decreasing in level with exactly one sign crossing, the extreme-pair identification, magnitude
monotonicity, the bake-underestimates-aging sign, the nonmonotonic fresh-3D structure — **all
ordinal/sign-level, and all sitting in conceded territory** (Néel/Street-Woolley/Sharrock, MLC
margin engineering own them too); every absolute row **NOT-COMPARABLE**, blocked not by physics but
by **vendor-held calibration**: the volts→eV constant, `f0`, and even the retention temperature are
withheld or unstated in the public record. **No row meets the promotion standard. No row falsifies**
(the one broken premise — a second opposite-sign channel on fresh 3D NAND — is a scope finding, and
the two-way-null rule applies). `FORMAL` stands.

**Corrections the refuter sustained against the lane's own pinning, registered here:** a
transcription row-slip (Table 5's P6/P7 one-day sigmas are 9.5/9.1, not 9.3/8.5 — the corrected
range is 9.1–12.8, and the corrected row now equals Table 4's 2,000 P/E row in mean AND sigma,
*strengthening* the identification); the N-7 retention temperature is nowhere stated in its paper and
was imported from a different one; the `f0`-exclusion claim ("the textbook 1e12–1e13 Hz decade is
excluded") holds only CONDITIONAL on the class mapping, `Ea = B`, and `T = 20 °C`, and dissolves
under the mixture reading at `dE ≳ 0.06 eV`; and the Funatsu Zenodo deposit is **RESTRICTED**, not
open — "raw data public" was wrong on access and unverified on content.

**Next steps named, in order of promise:** (1) **the SMTJ dwell-time route** — Funatsu's
superparamagnetic MTJ is a real two-state record with separately published `τ_P`/`τ_AP` and
Poisson-verified telegraph statistics, the exact object of C-69/C-70; an access request for Zenodo
6767828 plus a content-depth check must precede any grounding run, **and filing that request is the
principal's action, not the registrar's**; (2) the in-house read-retry census — the only located
route to margin-free absolute staircase positions; (3) the integer survivor census on one magnetic
sample is lab work, not literature work, and no located publication carries it. **The departure term
— the count law's wholly-owned content — remains touched by nothing located.**

---

## T-50 PARTIAL LANDING — **THE GATE HALF IS DONE AND INSTALLED; THE OBSERVABLE HALF STAYS OPEN, AND "NO RUNNABLE FORM" IS NOT THE VERDICT** (`LANE_T50/`; the hardened gate live in `model/validate_geometry.py`)

**GATE HALF (`DONE_WHEN` (b)): DONE, judge-verified, registrar-verified.** The hardened C-71/C-72
formation gate is sealed at `LANE_T50/GATE/` (block `633afb2e…`, harness `24bf34cf…`, matrix
`6931f774…`, declared seed 20260821) and **installed**: `model/validate_geometry.py` now executes it
in place of the six erratum-era checks — 33/33, chain PASS. **Every structural check fails at rate
1.000 under its designated mutation**, deterministic over 50 seeds: S1, the widens successor, at
1.000 under the two-signed write where the old check measured 0.18; the non-zero-mean residual
covered in three placements with **constraint-1 invariance MEASURED** (decision checks 0.000 under
common-mode rows while the raw shadow exponent flips at 1.000); density-falling-with-N at 1.000;
control A **dropped** (unfailable at any tolerance, verified `Δ = 1..99`) and its slot repaired as
A2 at power 1.000. No literal expected value sits on any decision path — every decision compares one
quantity measured in the run against another measured in the same run. The registrar re-ran the
harness independently: bit-identical to the sealed matrix. The proof's six stale gate cells were
caught by its own R8 and repointed at the block.

**OBSERVABLE HALF (`DONE_WHEN` (a)): OPEN.** Both designs on the ruled baseline-free differential
were **REFUTED by independent refuters** — Design One by the median-vs-mean density-shape confound
(a legal skew-density pattern fires its registered falsifier 30/30 **on correct physics** — the
constraint-3 confound in a new costume) and by instrument reality (every named stray-field reader
has zero response at k=0, so its DC positive control cannot pass its own guard); Design Two by a
blank control page and a zero-mean written-track bow, both firing on healthy physics. **And the
judge's most important finding cuts the other way: "the occupancy law has no runnable form" is NOT
the honest verdict** — both refuters' own rebuilds keep the same-read contrast-exponent CORE (it
honours all three ruling constraints, measured), and both name bounded repairs. **Next step named:
DESIGN ONE V002 with the eight merged closures** (`LANE_T50/JUDGMENT.txt` §2), re-faced by both
refuters before anything enters C-72. The judge's caveats carried: when V002 lands, the mutation
suite gains a median-vs-mean density-skew member and a fixed-pattern member.

**C-72's GROUNDED cell rewritten to the judged text** — the contrast-exponent quantity, what holds
with its adversarial confirmations, the hardened gate, the two refuted protocols by name, and the
open repair. **C-72 stays `PARTIAL`, `BLOCKED_BY T-50`. The program still has one `PROVED` row.**

---

## THE T-35 FIX PASS LANDS — **EVERY DIFFERS IS CLASSIFIED, EVERY SEAL IS HONEST, AND THE DATED-RECORD CLASS IS NOW A HARNESS MECHANISM, NOT A JUDGMENT CALL** (39 lanes; the clean zero-DIFFERS run launches from this commit)

The full reproduction run (`reproduce_full3.log`, 943 lines) ended with 58 DIFFERS. One agent per
lane classified and repaired each under the established pattern — presentation normalized
harness-side, real fixes byte-identical twice then resealed, physics never touched to make a diff
pass. The classes, and what was done:

**TIMING (the majority)** — trailing wall-clock lines in seven formats, all now absorbed by the
anchored `norm()` (each rule end-of-line-anchored after the first draft matched `(2s)` inside a
probability expression — a physics line). No file changed.

**DATED RECORDS (13 seals) — the new mechanism.** Eleven corpus-audit scripts grep the repository's
own documents, so their sealed outputs are audits of the corpus *as of their sealing date* — they can
never byte-match a fresh run against a grown corpus, by design. Two more are deliberate lane records:
`o7_writer_shape`'s seal carries the discard-verdict annotation the script never prints (deleting it
would destroy the lane's own negative finding), and `pf3_admissible`'s seal is the stdout-only
capture of the probe whose crash IS the dated finding. `replicate/dated_records.txt` now lists all
thirteen with reasons; `reproduce.sh` prints `DATED-RECORD (reason)` for each on every run — counted
separately, never as DIFFERS, never silently. Adding a line to that list is a registrar act.

**STALE SEALS FROM PAST FIX COMMITS (8 outputs resealed, each attribution exact from git):**
`w35_unravel` — the vectorisation-erratum commit fixed `exact_rho` and updated the script's hash but
left the OUT pre-fix; the resealed control value `⟨R⟩_exact = −0.00042139` is the erratum's own
corrected physics. `w58_pagewootters` — the ladder-fix landed in the script, its seal never
refreshed; the resealed kernel dimension 4 is exactly what the register's W-58 entry already
describes (the sealed 1 was the pre-fix failure mode). `w58b_ratedepends` — same event, the gate
line. `w30b_alpha_axis` — the seal came from a `steps=200000` variant never committed; resealed to
the committed script's 20k output (RK4-vs-expm agreement 4.5e−12, the control's purpose intact).
`S_07_onset` — the seal carried a rank-2 block from an uncommitted longer variant, cited nowhere;
resealed to the committed script. `RL5` — additive commentary printed by the committed script,
sealed from a run just before the print was added. `s5_D_decide` — the seal was TRUNCATED mid-file;
the resealed output adds the D5 charge-vs-multiplicity block, cited nowhere, deterministic twice.
`t13_bathsize` — truncated before the heavy nq=7 block (per-fragment eigh at 4096², the exact cost
`record_model.py` documents); the unbounded rerun reproduces the sealed 28 lines byte-for-byte and
appends the two nq=7 lines, whose relative spread 1.391 matches F-28's registered sequence.

**THE GARBLED SEAL REPAIRED:** `w56_center.OUT.txt` was **0 bytes** — no run had ever completed,
because `svd(full_matrices=True)` materialized a 68.7 GB U at case 4. The identity-preserving fix
(`full_matrices=False`; rows ≥ columns always on this path, so the reduced factors equal the full
ones and the m<n guard never fires) makes the script complete in seconds, deterministic twice, and
its six case lines agree with the sibling `w56b_symplectic` — the sealed source of every registered
W-56 number — on every comparable quantity. No registered number ever traced to the broken script.

**NONDETERMINISM FIXED (script edits, minimal, byte-identical twice):** ten scripts across
O-36 (a deterministic numpy `ComplexWarning` on stderr — `.real` moved before `float()`, value
bit-identical), O-6, R_SCHEDULE_REFUTER (sealed output updated under the fix pattern), SCALE_A,
SCALE_B, SCALE_D, W08_M2, W13_RULING, W17_R4, W10_C. Each edit is one seed or one ordering, with the
reason as a comment.

**HEAVY, NO ACTION:** `b4_reach` (sealed elapsed 5518s; every residual line is a timing form the
new norm absorbs — the clean run decides). **`LANE_T44_B_WORLD` — C-90's sealed evidence — was
presentation-only.** All inner `SEALS.sha256` and outer manifests for the eighteen touched lanes
resealed; the O48 stray `.norm` debris swept.

**DWELL-DATA SEARCH LANDED IN THE SAME ARC** (`LANE_DWELL_SEARCH/`, sealed): three arms and an
access refuter who re-fetched every top candidate this session. **The single best target for the
record laws' first real-instrument contact: Saira et al., PRL 109, 180601** — both directional rates
at three known temperatures, with `dE` sourced twice inside the paper (detailed-balance 1.94±0.05 K
against Jarzynski 1.91±0.03 K) — **the in-source cross-check that breaks the C-70 circle.** Woodside
PNAS 2006 runs second: its 20-hairpin SI table was RETRIEVED outright (T = 23±0.5 °C verified,
transcribed to `WOODSIDE_TABLE1_RETRIEVED.md`). Funatsu's Zenodo deposit re-confirmed RESTRICTED
(third check); nothing located forces that request as the first move. Refuter corrections carried:
Lyons demoted (temperature absent from the paper; dE≈0 by construction), two citation errata on the
hygiene-grade Zenodo set, one figure-caption conflict flagged as a digitization hazard.
**Next steps named: the clean zero-DIFFERS run (T-35's DONE_WHEN), then LANE_T51_A + T-17; the
Saira grounding lane queued on the principal's word.**

---

## T-17 LANDS — **THE PROOF STATES ITS OWN LIMITS, IN THE PROOF** (`PROOF_V002.md` §9, seven blocks)

The limits section is §9, gate-passing like every other section: the three `BLOCKED` rows named
verbatim **with their own staleness stated** (their texts predate T-41, C-84 and C-71's promotion,
and their re-audit is T-26's — cited as they stand, not silently repaired); the empirical status
exactly (one `PROVED` row on modelled surfaces, falsifier unrun by anyone; three pinned anchors; one
external run whose honest verdict was NOT-YET-COMPARABLE; C-72 `PARTIAL` with no runnable prediction
and no-runnable-form not established either); the formal wall (145 of 270 rows are mathematics about
a definition the program wrote — H-3's question is now T-53, and until it lands every FORMAL result
is conditional on that definition); the emergence claim's unearned conditions in one list, O-55/56/57
beside them, the field side identified-not-measured, the chain's head single-venue; carrier breadth
measured (113/22/15); the relocated problems stated as relocated, never solved (F-7, X-3, O-21,
O-53); and the document's own blind spots (31 ungated blocks, 13 dated-record seals, T-35 and T-18
the two checks still owed). **T-17's DONE_WHEN was sharpened first** — its 2026-08-19 text said
"says plainly that this is a mathematical result with no empirical contact," which is no longer what
the record carries; the criterion now requires stating the empirical status *exactly as the record
carries it*, which is both stricter and true. T-17 `DONE`. **T-18 is the last task of phase F.**

---

## THE URM BUILD-OUT AUDIT — **THE PLAN DID NOT COVER THE MODEL'S OWN GAPS; NOW IT DOES** (T-54, T-55 appended)

The principal asked whether the plan carries ALL tasks needed to build the URM out fully — the world
model, complete picture, rooted in the world. **It did not.** The physics tasks were all present;
the MODEL-HOMING debts — recorded in the proof's own cells but tasked nowhere — were: 24 blocks with
no model function and 38 with no gate; the arrow/redundancy family owed a layer (§3's own header);
the count law, the reachable classes, and the E1/E2/E3 writing-tier ensembles living only in sealed
lanes (`C-86` and `C-87` appear nowhere in `model/`, and `C-93`'s responsive-venue computation needs
`C-91`'s ensembles homed); the field instrument's fold-in unscheduled; and **P-DEF-7's integrity
finding** — the D-25 provenance gate is real, tested, and bypassed by the program's own validators,
so not one number in the proof actually passed through it.

**Appended, phase B (the model phase, appends-only per the lock):** `T-54` — home the five unhomed
families by the T-46 pattern, DONE_WHEN checkable against the proof's own computed front-matter
counts; `T-55` — make D-25 unbypassable (no direct `RecordSurface()` outside the model, grep-checkable)
and put at least one pinned external measured value beside a model number in a gated check with a
stated tolerance, replacing the substring test. Plan now 44/55.

---

## THE CLAIMS GRID — **THE HEADLINE CLAIMS, THEIR STAGE, AND THEIR ANCHORS' LIVE STATUSES, BESIDE THE MODEL** (`THE_CLAIMS_V001.md`; `ledger/claims.tsv` + `claims.py`)

**Commissioned by the principal, 2026-08-21:** a status grid of the main claims the program works to
prove — the final deliverable being **the URM with the ability to prove each of them.** Built in the
house pattern: the TSV is truth, the grid is generated, rows append and never renumber — and two
disciplines make it safe at this altitude. **Anchor statuses are read LIVE from the status ledger at
render time**, so the claims grid cannot silently go stale against the record (C-72's demotion, for
instance, shows in G-B's anchor line on every render without anyone editing the grid). And **the
tool refuses `PROVED-AT-BAR` unless every anchor row is `PROVED`** — the principal's bar held at
claim level exactly as `status.py` holds it at row level. Six claims: THE DEFINITION
(`GROUNDED-NOT-EARNED`), RECORD FORMATION (`WORLD-CONTACT-PARTIAL` — the only claim with a `PROVED`
anchor), THE RECORD LAWS (`FORMAL-COMPLETE`), GRAVITY EMERGENCE (`MEMBER-LEVEL-MATCH`), THE THREE
ROLES (`STATED-ON-TWO-CARRIERS`), THE PROOF ITSELF (`IN-CONSTRUCTION`). Stage vocabulary closed;
stage moves are registrar acts with register entries; the grid is a VIEW of the ledger and plan,
never a second source of truth. Wired into `on_finding.sh` beside the status and plan grids
(byte-for-byte regeneration + the refusal must hold). This grid is not the ROAD list and does not
replace it — it is the claim-level companion the ROAD's tasks serve.

---

## T-50 V002 — **REFUTED BY BOTH REFUTERS; THE JUDGE RULES ONE MORE NAMED REPAIR, AND THE TERMINAL BOUNDARY IS REGISTERED HERE, BEFORE V003 RUNS** (`LANE_T50/V002/`, sealed)

Design One V002 carried the eight closures and fell to **one family plus one**: B-K1 and A-K2 are the
V001 density-shape confound returned through two gaps the new C1 condition left open — it bounded the
ABSOLUTE density-median slope where the exponent confound is RELATIVE (`slope/(medf·ln10)`), and its
window started at N=64 while the fit started at the guard point — enabled by B-K2, the one-sided
point certificate. A-K1: orientation falsifier (c) fires at rate 1.000 on ordinarily biased data the
prediction makes no claim about — healthy physics firing a falsifier, the automatic-REFUTED trigger.
**Judge-verified as facts of the sealed pipeline text itself** (line numbers in the judgment), and
both refuters killed through the lane's own sealed instruments.

**The branch was scored, not waved off.** Four refuted protocol texts now stand. "No runnable form"
is NOT taken, for measured reasons: each kill has a **named identity-level repair** (the decisive
one: `beta_WU − 1` EQUALS the relative trend of `medf` over the fit's own window, so bounding that
quantity bounds the confound itself, not a corner of it); the kept core contradicted the no-form
statement for the **third consecutive judgment** (independent rebuild from the registered text alone
`beta_WU +0.9997`; 877/877 certified honest reads, worst `+0.9902`, **zero false occupancy fires in
any round including under the kills**); and **the orientation half survived whole** — polar Kerr at
k=0 sound, the design's own named worst risk caught by the read's own DC-free voider at every gain.

**THE TERMINAL BOUNDARY, registered so the next judgment inherits a closed choice:** if V003 falls
to **another D1-family kill**, the outcome is the **fallback rescope** — the falsifier-grade 2-SE
claim, which has never fired falsely in any round, becomes the registered prediction, with the point
band scoped or withdrawn — **and never "no runnable form."** The judge's §8 flag stands for the
principal's eventual ruling: whether that fallback is an acceptable landing zone need not be decided
now; proceeding with V003 requires no ruling under the standing T-50 commission. C-72 does not
return to `PROVED`; the DONE_WHEN's conjunction fails on half (a) regardless of the landed half (b).

---

## T-35 / B4 CORRECTION — **THE OLD “HEAVY, NO ACTION” CLASSIFICATION IS SUPERSEDED; THE FLOAT64-FLOOR DIFF IS REPAIRED, BUT T-35 IS NOT COMPLETE**

The `b4_reach` sentence above under **HEAVY, NO ACTION** is superseded. The r4 diff was not timing:
it comprised the **seven** n=8/n=12 comparison rows and the **one** worst-difference line
(`LANE_EXACT_B_RESIDUAL/b4_reach.txt:56–68`). The old run's worst raw difference was
`1.371e-14`; r4's was `9.243e-15`. Every one of the seven differences was at most the now-declared
`1.0e-12` numerical tolerance, and every pair is equal at the twelve decimals the lane reports.
Those last float64-floor digits are BLAS-dependent consistency noise, not a changed result.

The bounded repair stores the n=10 sidecar at twelve decimals and writes exactly one terminal LF
(`LANE_EXACT_B_RESIDUAL/b4_reach.py:36–48`); the n=12 table reports twelve decimals and makes the
tolerance decision explicit (`LANE_EXACT_B_RESIDUAL/b4_reach.py:65–81`). **No registered number
changed.** The downstream `b9_synthesis.py` reproduction was byte-identical in r4
(`replicate/reproduce_full4_overlap_invalid.log:69–77`), so no downstream synthesis or ruling is
altered.

**CUSTODY CORRECTION, DISCOVERED AFTER THE RUN:** two reproduction processes overlapped while
writing the same `reproduce_full4.log`. That byte stream is preserved as
`replicate/reproduce_full4_overlap_invalid.log`, but it is **invalid as T-35 evidence**. No clean
zero-DIFFERS reproduction, and therefore **no T-35 completion, is claimed here**. This entry lands
only the bounded B4 reproducibility repair and preserves the invalid log rather than laundering it
into a completion record.

**SECOND CUSTODY CORRECTION:** after that overlap was discovered, an old session launched another
snapshot harness at 13:08 with `WAC_ROOT` pointed at the **live repository**, while this B4 repair
and T-54 work were changing that tree. It was terminated incomplete and its 2,270-byte log is
preserved, not deleted, as `replicate/reproduce_full5_live_tree_invalid.log`. Because its input tree
was not fixed and the run did not finish, this second attempt is also **invalid as T-35 evidence**
and changes none of the no-completion ruling above.

A bounded post-repair rerun of `b9_synthesis.py` is independently byte-identical to its sealed
7,563-byte output. That light check confirms the downstream result without promoting either invalid
full-run log into T-35 evidence.

---

## T-54 / T-55 BOUNDED URM LANDING — **FOUR NON-FIELD FAMILIES ARE HOMED, THE LIVE MODEL-TREE D-25 BYPASS IS CLOSED, T-55 IS DONE; T-54 STAYS DOING AND T-51 IS EXCLUDED** (`LANE_T54_VERIFY/`)

**JUDGMENT BOUNDARY.** The no-new-measurement judge accepts this bounded landing. No sealed lane
program was rerun by the judge, no new scientific value was added, and no T-51 result is admitted.
`LANE_T51_A`'s V1–V5 rule remains unscored by an admissible verifier and judge; its field instrument
is neither registered nor folded into the URM here. This entry lands the four commissioned
**non-field** families and the D-25 integration only.

**THE TERMINAL STACK, EXACTLY.** `model/validate_urm.py` is the continuous entry point: arrow
27/27, count law 40/40, reachable classes 52/52, and writing 57/57, hence 176/176 family gates;
then geometry 33/33 and project/D-25 24/24, hence **233/233** with zero failure. Verifier A confirms
arrow 9/9, count law 11/11 and D-25 10/10; verifier B confirms classes/writing 26/26; the independent
integration verifier confirms 25/25 predicates. The assembled post-ledger proof is
`adc6ccecbff5ecd39c73fd843ae4d441759c87152737d1b4b13e2872b8508f21`: R1–R10 pass, with R11 at
83 blocks / 115 distinct rows / 48 resting on no TWO-CARRIER row / 10 blocks carrying the program's
**one** PROVED row. Ten blocks citing PROVED does not mean ten PROVED rows: C-71 remains the only one.

**THE DEFAULT-REFUTED PATH IS PART OF THE RESULT, NOT ERASED BY THE GREEN ENDPOINT.**

1. **Arrow began REFUTED, 13/15.** A custom two-dimensional `RecordModel` with its record omitted
   silently selected the sealed 256-dimensional toric record and died in an accidental NumPy shape
   broadcast; `ProjectModel.arrow_observation` also did not expose or forward `model=`. Omitted and
   dimension-mismatched records now refuse intentionally, the matching-record neighbor computes,
   and the integrated delegate forwards the custom model. The full repaired family is 27/27.

2. **Count law began REFUTED, 15/17.** `census` accepted both a raw unprovenanced world
   `RecordSurface` and a false corner declaration whose provenance was not exact `DEF-A`. The
   observation entry and every public surface-consuming path exercised by the verifier now recheck
   provenance, including after mutation; valid world and exact-corner neighbors compute. The full
   repaired family is 40/40.

3. **D-25 was captured REFUTED, 9/10.** The builder scan and an independent AST walker found the
   same five direct `validate_project.py` sites. They now enter through `URM.surface` or
   `URM.corner`, and the recursive live-model scan returns zero `RecordSurface` binding/reference
   outside `project_model.py`. The full project/D-25 validator is 24/24 and the D-25 family is 10/10.

4. **Classes and writing required scientific-API repair before final verification.** Classes now
   refuses negative coupling price and non-positive/non-integer venue multiplicity beside valid
   computed neighbors. E1, E2 and both E3 counting rules now refuse signed or overfull probability
   domains; unit-sum signed kernels are no longer called stochastic/conserving/critical; an extreme
   Boltzmann underflow declines as `None` instead of reaching `Fraction(1,0)`. The negative and
   boundary controls execute. Their final suites are 52/52 and 57/57.

5. **Verifier A's two refuted race captures remain in custody.** The first read a tree changing
   from 26/39 to 27/40 while retaining stale expected counts, and its F-17 parser rejected a valid
   sealed row whose trailing argmax field contained spaces. The second correctly preserved the
   initial 13/15 and 15/17 defects, but D-25 integrated during the run and invalidated its stale
   five-offender expectations; its off-grid count-law probe also chose a no-crossing point and took
   a logarithm outside the domain. Parser, snapshot custody, expected counts, D-25 expectation and
   probe were repaired, then the complete verifier reran. These are recorded verifier/race errors
   where stated, not retroactive API findings.

6. **Verifier B first returned 25/26.** A repeated-key parser selected the M=1400 E4 row instead
   of the M=2800 E6 row. It was narrowed and the whole verifier reran to 26/26. The same audit caught
   a real integration-paste defect: `writing_kernel_verdict` divided by `(1-c)` at `c=1`, admitted
   `c` outside `[0,1]`, and could label a nonconserving kernel critical. The integrated method now
   refuses the outside domain and returns the conserving critical no-move endpoint with zero link
   amplitude and `per_crossing=None`.

7. **Integration first returned REFUTED, 22/24.** I15 treated the deliberate
   `(VenueGraph, cells, idx)` return as a `VenueGraph`; I24 correctly refused while verifier A's
   terminal artifacts were absent. Tuple comparison and dependency custody were repaired. The
   final integration rerun is 25/25 and binds the one captured 233-gate umbrella execution.

8. **The proof cutover was twice semantically REFUTED despite a mechanical green gate.** The first
   assembled version retained pre-T54 claims that C-86/C-87 were absent, D-25 was bypassed and old
   geometry/project counts were live; the second still said “the two PROVED rows” against the
   exactly-one invariant. Both were repaired at `proofsrc/`, reassembled and rechecked. After the
   ledger cutover, the semantic reviewer caught one further claims-grid error — the nonexistent
   `.reachable_classes` plural instead of live `ProjectModel.reachable_class` — which was repaired
   through the new field-aware `ledger/claims.py urm` command, not by hand-editing the TSV. The
   post-ledger semantic verdict is 12/12 CONFIRMED.

**D-25 / T-55, WITH THE RESIDUAL TRAVELLING.** The pinned azobenzene gate puts measured
`t1/2 = 1.2e5 s` beside model `t1/2 = 4.170e4 s`: -0.46 decades, inside the declared one-decade
tolerance. The historically wrong midpoint convention is the power control and fails the same gate
at -5.37 decades. This is **same-source order-of-magnitude consistency** using source-supplied
`dH` and `dS`, not a parameter-free prediction; Weller-Moser and NAND remain pinned anchors and
historical comparisons, not equivalent integrated predictions. D-25 is model-tree integrity and
construction hygiene, **not authentication or a security boundary**: Python metadata remains
mutable/fabricable, callers outside the scanned tree can instantiate the exported class, and sealed
legacy lanes remain outside the scan. Consumption refusals close the tested raw/false/mutated paths;
they do not turn provenance text into cryptographic identity.

**LEDGER AND TASK DISPOSITION.** C-85 was narrowed from the false “every registered headline”
breadth and old 31/14 counts to the bounded 176 + 33 + 24 = 233 stack, with T-51, full-corpus
reproduction and T-35 explicitly excluded. D-25 now states its live gates and residual. C-91's
world-tier denominator remains the corrected **36 gates**, not the earlier erroneous 42. G-C now
maps the homed count law to `.census`; G-D maps classes to singular `.reachable_class` and keeps
T-51/T-49 open; G-F drops completed T-55 from NEXT while retaining T-35, T-18 and T-54. The claims
tool gained narrow `next` and `urm` commands so those updates obey the retrieve-and-update rule.
No claim status moves. **T-55 moves TODO → DONE. T-54 remains DOING. T-51 remains TODO.**

**THE CONTINUOUS URM RULE NOW EXECUTES.** New features do not merely accumulate beside the model:
a new surface or corner enters through the URM declaration/refusal doors; a new law enters through
a `ProjectModel` method and family gate; a new external number enters only as a pinned comparison
with a stated tolerance and power/control semantics. `validate_urm.py` composes those obligations
before the geometry/project chains, and `replicate/on_finding.sh` invokes that umbrella on every
landing. The final commit remains contingent on both required landing gates; no failure may be
narrated past.

---

## T-51 QUARANTINE CORRECTION — **THE OLD ALL-PASS IS INADMISSIBLE; THE CORRECTION LANDS, SCIENTIFIC REGISTRATION DOES NOT** (`LANE_T51_REPAIR/`, sealed correction subset)

**CUSTODY BOUNDARY.** `LANE_T51_A.sha256` remains unchanged at
`15a4d1a83fe92b4282746a35b996c179013a94c942e12e609f7322429bfca1a8`; the sealed builder is input
and was not rerun. The tracked `LANE_T51_A/VERIFY/v1_adversarial_rebuild.py` remains an obsolete,
unexecuted fragment sealed with that historical builder package, not an admissible verifier. The
untracked, final-looking `LANE_T51_A/VERIFY_CODEX/**` and `JUDGMENT_CODEX.txt` drafts were not
promoted at those paths. Exact byte copies are preserved under
`LANE_T51_REPAIR/QUARANTINED_DRAFTS/ORIGINAL_LAYOUT/`, with the old nested seals retained as
integrity evidence only and an explicit instruction that none of the copies may be executed or
registered. The originals were neither modified nor removed and remain excluded from this landing.

**THE TWO OLD VERIFIER DEFECTS ARE NOW PART OF THE RECORD.** The drafted C verdict consumed only
`lambda=0.037` at near/far even though its raw artifact also contained `0.071` and the fresh
placement. The drafted E scan walked only the top level of `LANE_T51_A`, omitted nested artifacts,
returned a literal `violation_count=0`, and made its verdict depend on that literal. Therefore the
old A–E all-clear and the judgment built on it never met the default-refuted commission.

**WHAT THE QUARANTINE AUDIT DOES — AND DOES NOT DO.** The clean-clone-replayable correction audit
hashes 26 frozen inputs with zero mismatch, cross-checks the builder, archived-verifier and
quarantine-copy manifests, consumes all six C cells (near/far/fresh × `0.037/0.071`), and runs E on
a closed 23-file claim corpus with three firing positive controls and zero unexculpated decision
hits. Its overall result remains `REFUTED`, with scientific disposition **PARTIAL POSITIVE / NUMERIC
SUPPORT ONLY / REPAIR REQUIRED**. A/B/D re-adjudicate the archived verifier's stored records, C
repairs the predicate over archived raw `F` rows, and V1 reads the builder table and floor. Those
operations are useful correction evidence, but they are not a fresh independent-own-machinery
scientific rebuild. Component `NOT_REFUTED` labels must not be promoted into V1–V5 scores.

**THE NO-MEASUREMENT JUDGMENT.** The quarantine correction is **ACCEPTED FOR LANDING**; historical
scientific terminal registration is **REJECTED**; the required independent-own-machinery verifier
standard is **NOT MET**. Scoring from `FIELD_INSTRUMENT_V001.md` section 1 is therefore:

1. **V1:** numerically supported only; pending admissible independent verification; no score.
2. **V2:** **UNSCOREABLE**, never FALSE. FIELD defines the reading as `F(D)`, while the builder
   scored onset `k`, introduced `TOL_SWAP=0.25` after FIELD, and replaced the singleton commissioned
   connected-`w_enc=5` far class with a connected-`w_enc=4` pair.
3. **V3:** numerically supported only; pending admissible independent verification; no score.
4. **V4:** qualified descriptive comparison only. The stored back-action is below `1e-3`, but that
   budget was selected after a same-family magnitude survey and placed above the observed scale; it
   is not a prospective Boolean available to the conjunction.
5. **V5:** numerically supported only; pending admissible independent verification; no score; the
   far sign remains relative to the sealed winding representatives.

Neither registered route fires: ALL PASS cannot fire, and V1 has not scored FALSE, so the
mediator-family negative route cannot fire. **PARTIAL POSITIVE / REPAIR REQUIRED is an
administrative disposition, not a third terminal branch.** The drafted C-94 row, drafted C-77
increment and drafted T-51 completion are rejected.

**THE CORRECTION TRAIL IS PRESERVED, NOT CLEANED AWAY.** The quarantine audit first misclassified a
wrapped explicit no-failure sentence because its scan window omitted preceding context; the window
was made bidirectional and all positive controls still fired. It then exposed two parser defects:
Markdown markup blocked exact quote matching, and `TOL_BACK` was sought in the wrong frozen file;
both were corrected without changing a scientific value. Pre-landing replay review then found the
audit depended on untracked final-looking paths; byte copies were placed in the quarantined custody
tree, all references were repointed, and two final runs were byte-identical. The judge's first
custody check requested the manifest at the wrong directory and its first quote checker assumed a
wrapped clause occupied one line; both checks were corrected. Final pre-seal review also corrected
the judge audit's description of `d_gen`: FIELD explicitly treats both `d_gen` and connected
`w_enc` as earned quantities. Every correction is in the two D24 audits; none changes the judgment.

**LEDGER, PLAN, AND URM DISPOSITION.** No ledger or claims row moves. No C-94 or T-9 registration
row is added. `T-51` remains `TODO` and open; `T-54` remains `DOING`; no field result enters the
URM, proof, or claims grid. The continuous URM rule is being applied here precisely by refusing to
home an invalid result. A future field law may enter only after a complete prospective instrument,
fresh measurement, independent default-refuted verification, and a no-measurement judgment.

**NEXT BOUNDARY.** Prospective design work remains unsealed and outside this correction landing.
Before even a geometry selector runs, one coherent fresh rule, all builder/scorer/checker sources,
the independent budget, verifier briefs, immutable pre-execution audit declaration, and design
judge packet must be sealed and pushed. The historical exposed rows may inform a declared design;
they may never score their own repair.

## 2026-09-15 — exact L12 closure, finite relational continuation, and L14 seam

**EXACT L12 CUSTODY.** The target and independent hostile L12 histories now agree on all
`1156/1156` declared comparisons. The strict common-lineage support is
`0.11570852222694002` on the target and `0.11570852222694036` on the hostile
reconstruction; the target value is retained as the conservative governing finite diagnostic.
The authority is `AUDIT_R_L12_NUMERICAL_REPAIR_V003/EXACT_ADJUDICATION_V003R1.json` together
with its execution-custody record. This supersedes the September 9 statement that no L12
numerical computation existed; the earlier obstruction remains preserved as history.

**FINITE STAGE-6 DECISION.** The authenticated sector manifest and Stage-6R2 adjudication close
the declared L4--L12 endpoint as `AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12`. The result is a
finite-sector rejection, not a general no-go theorem for `z=1`, a continuum, emergence, or
gravity. The record-flow and Stage-6R3 packets are supplemental diagnostics and do not override
the governing Stage-6R2 gate.

**COMMON-LINEAGE PROGRESSION.** Under the declared deterministic extraction, support is strictly
increasing: L08 `0.0244800482`, L10 `0.0687369678`, and conservative L12
`0.11570852222694002`. L08 and L10 are rigorous diagnostics from the authenticated target cache;
L12 also has an independent hostile reconstruction. This difference is a gate classification,
not doubt about the cache. No monotone-continuation, asymptotic-extrapolation, or L14-value theorem
is claimed from three points.

**L14 BOUNDARY.** The authoritative implementation is
`DEVELOPMENT_R_L14_TARGETED_SCOUT_V003`, with source authority recorded per branch. Initial Target
R5 and untouched Hostile R5 use `KERNEL_BINDINGS_RELEASE_V003R3.json` and
`L14_SOURCE_BUNDLE_MANIFEST_V003R5.json`; the fresh Target R6 restart uses
`KERNEL_BINDINGS_RELEASE_V003R6.json` and `L14_SOURCE_BUNDLE_MANIFEST_V003R6.json`. Target R5 ended
at q10 when numerical Krylov-capacity exhaustion produced a non-finite residual diagnostic and
strict JSON correctly refused publication. `EXACT_KERNEL_AUDIT_V003R6.json` classifies that event as
a numerical-capacity obstruction surfaced by strict JSON, not AWS hardware failure or an L14
physics result. A target-only R6 capacity repair preserved the physics contract, after which a fresh
Target R6 restart was authorized and initiated from a new checkpoint root without checkpoint
migration; failed R5 evidence was preserved and Hostile R5 was untouched. This is durable attempt
history, not an assertion about process state at read time. The scientific value remains
exactly `PENDING_AUTHENTICATED_RESULT`. The owner-once authenticated Phase-1 merge must first
preserve the original numerical predicates and satisfy the q5, q6-core, contiguous-cell, and
optimistic unopened-q8/q9 reachability conditions. A Phase-2 pass authorizes only Phase 3 q8/q9.
L14 progression admission additionally requires authenticated Phase-3 target/hostile evidence and
the distinct final finite-scout decision: lower independently computed branch mass per actually
passing sector, deduplicated by q identity, must sum to at least `0.50`. The finite-scout gate is not
an exact or asymptotic `z=1` emergence theorem. Until both decisions and the complete authenticated
branch evidence exist, the pending marker cannot move. The declared q-domain remains whole; no
q10--q14 truncation or denominator-changing shortcut is admitted. Runtime advisory limits are
operational notices rather than scientific stop conditions.

**URM AND RELEASE DISPOSITION.** Rows `URFT-1`, `A-AL2`, `GFT-1`, and `RA-1`--`RA-4` register the
current foundational, alpha, conditional-gravity, and finite-relational state. Tasks `T-56`--`T-58`
hold L14 closure, source reconciliation, and publication/deposit. The generated ledgers and proof
are rebuilt from their sources. Git commit, push, release tag, and Zenodo deposit remain separately
unauthorized; the preparation capsule keeps L14, aggregate validation, license, citation, and DOI
inputs fail-closed.

## 2026-09-16 — exact majority record block, governing block Gate, and L14 closure

**STRUCTURAL THEOREM.** The fixed `A009--A016` envelope is now controlled by
`L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md` and the independent
`AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md` verdict `PASS`.
At each authenticated size `L in {4,6,8,10,12}`, exact bounded record roles are
proved and the deduplicated block mass exceeds one half. The masses are
respectively `0.7260206189754993`, `0.5846615608350367`,
`0.7373965730354166`, `0.6500987927669427`, and
`0.56956498393327842`. This theorem is bounded to the five authenticated
sizes; it does not silently assert an all-`L` continuation.

**PURE FINITE VISIBILITY.** The proof path in
`DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001` reads the Hamiltonian/probe
rows directly and imports no legacy adjudication verdict. The 40 atom/size
assignments reduce to 13 unique `(L,q)` sectors. Every sector has positive
finite visibility; the minimum observed `R_low` is
`0.4280947078156539`, the minimum lowest-pole weight is `0.5`, and the
independent Target/Blind higher-size calculations agree within their pinned
tolerance.

**GOVERNING GATE ADOPTION.** By principal decision, recorded in
`ARGER_GATE_ADOPTION_2026-09-16.md`, ARGER-GATE-1 is the governing UNT finite
ARGER Gate. Exact bounded membership, deduplicated mass above `0.50`, and
positive finite visibility across the complete finite record domain constitute
the finite GFT `z=1` standard. The `A009--A016` domain passes. ARGER remains the
record-formation process; the record block is the theorem's evaluation domain,
not an additional mechanism.

**DYNAMICAL-EXPONENT TYPE.** The same-model LL-P theorem separately supports
dynamical exponent `z=1` throughout the declared density interval under its
explicit physical premise. A premise-free repository-internal uniform all-`L`
theorem remains a stronger open result. It is not a condition of the adopted
finite Gate.

**L14 TERMINAL DISPOSITION.** The L14 attempt ended before final authenticated
Target/Hostile outputs. Compact sanitized event custody was retained, no L14
number or physical verdict is inferred, and the disposition is
`INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT` in
`L14_RUN_DISPOSITION_2026-09-16.md`. This supersedes the former pending marker.
L14 is neither a prerequisite nor an input to the L4--L12 block theorem or
Gate. Task `T-56` is therefore complete as a clean attempt closure, not as a
completed L14 computation.

**URM AND RELEASE DISPOSITION.** Rows `RA-5`--`RA-8` register the theorem,
finite visibility, adopted finite Gate, and conditional dynamical theorem;
`RA-4` now carries the terminal L14 disposition. Task `T-57` continues the
URM, proof-guide, generated-ledger, Git-preparation, and Zenodo reconciliation.
No commit, push, tag, GitHub release, Zenodo deposit, or publication act is
authorized by this register entry.

## 2026-09-17 — completed-proof table and G-F process classification

**PUBLICATION TABLE.** The Universal Network Theory Major Proof Index now
reserves its principal proof table for exact theorems, exact conditional
theorems with named premises, and authenticated finite results. Adopted
definitions, broad partial research programs, superseded routes, incomplete
attempts, and publication administration remain documented, but they are not
presented as completed proof entries.

**G-F CLASSIFICATION.** Canonical row `G-F` is renamed from `THE PROOF ITSELF`
to `URM INTEGRATION AND REPRODUCTION`. Its `IN-CONSTRUCTION` label is retained
as a process/release status for broader URM homing, whole-history external
reproduction, and publication. It does not qualify or reopen the completed
scientific status carried by `G-G` and `G-H`. The focused relational closure
and preparation capsule pass locally; Git publication and Zenodo deposit remain
separate human-authorized acts.

**TABLE SCOPE REPAIR.** The publication proof tables and release claim map are
limited to completed exact results, authenticated finite results, and exact
conditional theorems with their premises stated. The former broad Record
Formation table entry is narrowed to the completed L4 intrinsic-admission
theorem: target `10/10`, independent reconstruction `12/12`, and final
hash-pinned hostile verifier `50/50`. The unfinished T-50 family is not cited
as though it were a completed independent check. Definition rows, partial
families, microscopic-progress interfaces, failed attempts, and release
administration are kept in program-status prose or canonical ledgers rather
than presented as proof-table entries.

**HISTORY.** No sealed theorem, dated audit, historical handoff, or prior
register entry is rewritten by this classification repair.

## 2026-09-18 — L14 publication prominence correction

**PUBLICATION FRAMING.** L14 is removed from the Major Proof Index header,
opening conclusion, proof route, release summary, and other headline
positions. Because the attempted extension produced no authenticated result
and supplies no proof premise, the publication-facing Index and READMEs retain
only one subordinate historical note. The dated terminal-disposition artifact
and chronological Git custody remain unchanged.

## 2026-09-18 — single ARGER Gate terminology and finite-size notation

**SINGLE GATE.** Current theory, URM, and publication prose now names **the
ARGER Gate** or `GATE`. The former `ARGER-GATE-1` wording was a versioned
implementation identifier, not evidence of a numbered family of gates. ARGER
remains the complete record-formation process `ALLOW -> REQUIRE -> GATE -> EM
-> RECORD`; `GATE` is its one classification stage. The scientific result is
that the authenticated `A009--A016` record block passes that Gate and thereby
receives the finite GFT `z=1` classification. The criterion, its evidence
domain, and its resulting classification are no longer conflated in the
publication layer.

**FINITE-SIZE NOTATION.** Publication-facing documents now define `L` before
using the finite ladder. In the relational family, `L` is the even size and
one-pass horizon of an independently constructed owner-once periodic-prism
parent: `L` active genesis cells, `2L` carrier sites, `3L` transport edges, and
`L` fresh admissions before revisit. Event-prefix depth `n` and retained-
carrier/spent-lineage rank `q` are distinct. The 13 selected `(L,q)` visibility
rows span five independently constructed parents; they are not 13 sectors in
one `L = 12` system.

**PROVENANCE.** Sealed 2026-09-16 theorem, audit, evidence, and executable
artifacts retain their original bytes and archival machine identifiers. Those
identifiers refer to this same single Gate and do not create additional theory
objects. Generated current proof and status surfaces were rebuilt from their
corrected sources.

## 2026-09-19 — Universal Network Theory closure composition

**MASTER THEOREM.** `UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md` now
states the exact type-preserving composition of the completed Record Formation
Theory and Gravity Formation Theory results. It introduces no additional
physical axiom. Universal RFT coverage, the governing-domain alpha requirement, the
finite GFT `z=1` Gate classification, record-conditioned geometry, and the
conditional macroscopic Einstein response retain their controlling domains,
premises, and proof types.

**PUBLICATION AND URM.** The Major Proof Index, release navigation, claim map,
and URM integration now expose the master theorem as the controlling UNT
composition. The finite `A009--A016` result remains the microscopic Gate
theorem; RGRL and `WTC-H1` through `WTC-H5` remain the separately typed basis
of the conditional macroscopic response theorem.

**CITATION AUDIT.** The publication bibliography now contains only sources
actively invoked as a load-bearing premise, technical or empirical anchor, or
specific boundary comparison for a completed result. Passive background
citations were removed and the retained references were renumbered
contiguously.

**PROVENANCE.** Dated, sealed, audited, and evidentiary artifacts retain their
original bytes. This entry changes current navigation, composition, and
publication custody only.

## 2026-09-25 — L10/L12 owner-once joint lineage--carrier witness recognized

**FINITE COMPUTATIONAL RESULT.** The exact Target and independently
implemented Hostile branches reproduce the same held-out values at the common
reported precision:

```text
L10  D_L = -0.00031184885937284
L12  D_L = -0.00003236588485224
T_10:12 = 32365.88485223031
```

Every branch-internal numerical and null control passes. The agreement is
valid finite computational evidence of a nonzero **two-sided** owner-once
lineage--carrier association through `L = 12`. It does not establish that the
association keeps one sign, stays above a positive floor, or survives at all
larger sizes.

The live recognition authority is
`DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_RECOGNITION_V001`:
its independent reconciliation validator passes `50/50`, its mutation and
determinism tests pass `8/8`, and its machine-readable result carries the same
three-way disposition used here.

**FROZEN SECONDARY CRITERION.** The post-computation, pre-unblinding secondary
freeze set the signed no-decline floor to
`f = D_8 = 0.001963064475535806`. Both held-out values are negative and their
magnitudes are below the floor. The signed positive no-decline criterion
therefore fails decisively; this is neither a narrow miss nor evidence for a
positive scale-stable limit. The result instead shows a sign reversal and a
substantial magnitude decline across the held-out sizes. It does not by itself
choose among decay, oscillation, or another finite-size mechanism.

**DISCLOSED PROCEDURAL DEVIATION.** Target release preceded Hostile release by
`10,748 s`, exceeding the frozen legacy `60 s` concurrent-release rule. The
result is therefore not called a pristine strict-protocol held-out pass. The
timing deviation is not a failure of the equations, numerical controls, or
independent agreement. Target was launched on September 23 at `07:45:33` and
Hostile at `10:44:41`; Hostile did not publish its final output until September
24 at `21:36:49`, and Target did not publish its final output until September
25 at `09:13:29`. Neither final value existed when either branch was launched,
Target was already deterministically running before Hostile began, and the
Hostile value remained unopened by the interpreting workflow until Target
finished. No value-contamination path is evidenced.

**LIVE PROTOCOL POLICY — NOT A RETROACTIVE FREEZE CHANGE.** The `60 s` rule was
introduced as a conservative anti-contamination and blinding safeguard: close
launch times make it harder to adapt one branch after learning the other's
value. It is not a scientific premise, an equation of the model, or a
numerical acceptance condition, and arbitrary simultaneity is not the property
the experiment actually needs. Future protocols should directly gate the
scientific safeguards: source and parameter freeze before release, branch
isolation, prohibition on cross-branch value access, atomic final publication,
and a recorded unblinding barrier. A wall-clock launch-skew limit should be
used only when it has a separately stated operational purpose. The historical
freeze remains unchanged.

**TYPE BOUNDARY.** This result changes no sealed theorem or historical
artifact. It is not a premise of the finite ARGER Gate and does not promote
finite Gate `z=1`, conditional dynamical `z=1`, RGRL/WTC response, alpha,
record curvature, geometry, spacetime, or gravity. It supplies one new exact
finite computational fact and one falsified stronger persistence prediction.

## 2026-09-25 — L8 formation-order Ollivier--Ricci test returns controlled null

**FROZEN QUESTION.** Before opening any curvature or association output, the
analysis fixed the L8 graph as the unweighted path `0--1--...--7`, the
transitive reduction of the first owner-once formation order with direction
forgotten for metric transport. It fixed Ollivier--Ricci idleness `1/2`,
incident-edge-mean node curvature, terminal spent-lineage concentration,
Spearman correlation, every one of the `8!` record-label permutations, and
the positive criterion `rho >= 0.5` with `p_plus <= 0.05`.

**RESULT.** The authenticated read-only reconstruction returns

```text
rho = 0.1543033499620919
p_plus = 14592 / 40320 = 0.3619047619047619
p_minus = 26496 / 40320 = 0.6571428571428571
```

Neither registered direction passes. The exact disposition is
`NO_RESOLVED_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8`. The null is a
valid measured outcome and is retained unchanged; it is not converted into a
validator failure.

**SCOPE.** This result rejects a resolved association only on the frozen
unweighted formation-order path at L8. It does not rule out richer lineage
graphs whose native relation is earned prospectively from unchanged dynamics
without reusing the record-concentration response. The path is a finite
chronology diagnostic, not emergent space. No geometry, spacetime Ricci
curvature, RGRL/WTC response, Einstein dynamics, gravity, or numerical `G`
follows.

**LIVE INTEGRATION.** Row `RA-10`, generated proof block `P-CURRENT-8`, and
the non-load-bearing hash-pinned `lineage_order_curvature_certificate` expose
the controlled null without changing the ARGER Gate or any sealed historical
theorem. The autonomous lineage-sensitive continuation is a separate test and
is not adjudicated by this result.

## 2026-09-25 — L4 autonomous lineage-sensitive continuation recognized

**FROZEN TEST.** At the authenticated L4 terminal checkpoint, the test formed
the symmetrically sharp-sector-dephased retained joint state and a same-sector
quantum-product comparator preserving the complete separate lineage and
carrier marginals and each sector weight. Both arms received the same fixed
event-zero lineage-reading revisit and the same carrier transport. The primary
observable was the post-transport carrier trace distance.

**INDEPENDENT RESULT.** The target returns
`Delta_C=0.14761185701902999`; an independently written implementation that
imports neither the target continuation nor the historical parent returns
`0.14761185701903007`. With `tau=1e-10`, the independent statistic is
`T_dyn=1476118570.1903007`. The initial carrier-marginal residual is
`6.938893903907228e-18`, the maximum registered target/independent difference
is `1.1102230246251565e-16`, and the independent no-`@` contraction route
captures zero warnings. The original target warning stream is therefore not a
premise of acceptance.

**CONTROL AND DIAGNOSTIC.** Trace distance is invariant under the common
carrier-only transport, so that invariance is a control rather than separate
evidence. The fixed occupation profile is transport-sensitive: it is at
roundoff immediately after admission and reaches RMS
`0.006009875541368592` after transport.

**DISPOSITION AND CEILING.** Register
`RESOLVED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION` for this one fixed L4
mechanism. It establishes neither a second size nor persistence, scaling,
curvature, emergent geometry, a continuum, RGRL/WTC response, alpha, Einstein
dynamics, gravity, or numerical `G`. Row `RA-11`, generated proof block
`P-CURRENT-9`, and the non-load-bearing hash-pinned
`owner_once_autonomous_continuation_certificate` carry the live result without
changing the finite ARGER Gate or any sealed historical theorem.
