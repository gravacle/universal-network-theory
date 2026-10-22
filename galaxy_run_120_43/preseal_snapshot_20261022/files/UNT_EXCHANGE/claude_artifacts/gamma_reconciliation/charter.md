# Γ charter notes: what the third term is, and what T-20 actually says

Read-only extraction, 2026-10-12. Worktree HEAD `b4d9311c` (2026-10-11), with the cited files clean.
`THIRD_TERM_V001.md` sha256 begins `81605d2b9d62282b`, which matches the hash pinned in
`UNT_AUTHENTICATED_PROGRAM_REVIEW_2026-09-27_V001/FOUNDATIONAL_SEEDED_ROW_REVIEW_2026-09-27.md:131`.
All paths are relative to `/Users/bgm/Research/Universal Network Theory/program-worktree/` unless
stated otherwise. `REG` = `REGISTER_V001.md` and `SL` = `ledger/status_ledger.tsv` (line = row).

---

## 0. Short answer

- **Γ is defined only by its function, R1–R3.** The word "gravity" is a permitted label that does
  no work. No classical quantity may be a test Γ has to pass (D-1).
- **`(H₁(Σ), ⟨·,·⟩)` is one candidate and not the only one.** Σ is a cell-complex surface carrying
  a Z₂ gauge field, which is Kitaev's toric code. Uniqueness has since **FAILED** (G-6). Survivors
  are the `H_k` of any F₂ chain complex whose systole and cosystole both grow.
- **The charter is stale on two points.** It still says uniqueness is open, and it says T-20 is
  "untouched". In fact T-20 was marked DONE on 2026-08-19 with a flat-holonomy null, its reading
  was overturned by O-23, and field recovery moved to **C-77** (status CANDIDATE).
- **R3 as written excludes any record that a local operation writes.** In canonical V005, the
  per-vertex q_v bits are written by the local Bind term. If the brief's description of V005 is
  right, q_v cannot be Γ records. On V005, the charter-native Γ candidate is the ice manifold's
  winding/flux sectors. See §7.

---

## 1. What Γ is (THIRD_TERM_V001.md)

| point | text | lines |
|---|---|---|
| "gravity" is permitted as a label | principal, 2026-08-18: fine to say "gravity" provided it is not used to import classical metrics | 5–7 |
| inference from the label is forbidden | "Γ IS DEFINED ONLY BY THE FUNCTION IT PERFORMS (R1–R3)… no classical quantity may serve as a *test Γ must pass* (D-1)… zero evidential weight" | 9–17 |
| Γ is whatever satisfies all three roles | R1–R3 table | 21–30 |
| theorems are about R1–R3, not about the name | — | 34–37 |
| H₁ is a CANDIDATE, not a definition | "satisfies R1, R2 and R3 — that is Theorems A, B and C… verified (G1, G2, W-62)" | 39–45 |
| uniqueness question | "Is `H₁(Σ)` the ONLY structure satisfying R1–R3?" (stale, see §4.4) | 47–60 |
| THE CLAIM | "gravity COMES FROM Γ". Identity is withdrawn (X-6); resemblance is generic; "classical gravity is what Γ becomes at scale" | 62–66 |
| why the definition is function-only | a Γ shaped by any feature of classical gravity would make the claim circular. "The import discipline (D-1, D-2, D-4, D-5, D-9)… had to come first" | 68–70 |
| state | "recovery of classical gravity from accumulated Γ is untouched — plan task T-20" (stale, see §4.4) | 72–73 |
| renaming | allowed only after R1–R3 are solved, and only if the solution earns it | 75–78 |

`GRAVITY_DEFINED_V001.md` is superseded (lines 1–2). It made `(H₁, ⟨·,·⟩)` the definition (8–9),
which meant nothing could fail it. Its "bridge" `records = 2 − (1/2π)∫K dA` (29–31) was later
corrected to an index law (G-7, `REG:4990`). The surface law fails off closed surfaces. Its closing
section, "Γ's role is ALLOW at every level" (75–77), was superseded on 2026-09-06 (§6).

---

## 2. What R1–R3 require

The roles are stated in the record level's own terms (`THIRD_TERM:23–27`). Each one points to
clauses of the anchor definition DEF-A (`CORE_FRAMEWORK_V001.md:98–106`). The record definition
there reads: `R` is a record iff
(i) `R=R†, R²=I`;
(ii) `[H,R]=0` and `[L_k,R]=0` for every `k`;
(iii) `R` is not constant on some eigenspace of `H`;
(iv) some **admissible** `U` (`[U,H]=0`, line 114) has `U†RU=−R`;
(v) **no admissible** operation on a **single contractible region** does.

| role | requirement | source clauses | precise content |
|---|---|---|---|
| **R1 SPACE** | a set of states a record can occupy, of size > 1, that distinguishes states of the **same energy** | (iii) | a degenerate eigenspace of `H`. P-1: (iii) ⟹ `H` is degenerate (`CORE_FRAMEWORK:165–166`) |
| **R2 WRITER** | an operation that flips the record, **which no local operation can mimic** | (iv)+(v), P-3 | P-3: no admissible writer fits inside one contractible region (`CORE_FRAMEWORK:171`). The strong reading "nothing local can write it" is **false**, because products of `d` local terms do reach the record (Thm D, lines 173–177). The minimal writer at L=3 is `XXX`, a product of three single-edge operators that are each inadmissible (179–181) |
| **R3 PROTECTION** | **no local operation** writes or destroys it | (v) | flip-immunity under admissible single-region operations. Before the erratum adding "admissible", (v) was false for the toric code (119–124) |

**Qualifications registered after the charter was written:**

- **R1 is cheap and R3 discriminates.** G-10/G-11 (`REG:5126`, `SL:46`): capacity and protection
  are independent. A bouquet of triangles has `dim H₁` = 2, 3, 4 with true `d = 1`. A torus has
  `dim H₁ = 2` with `d = L`. R3 needs **two** numbers: `d = min(systole, cosystole)` (`REG:5195–5201`).
- **R2 needs no manifold.** G-13 (`SL:48`, `REG:5203`): the evaluation pairing `H_k × H^k → F₂` is
  perfect for any complex over a field. Theorem B's attribution to "Poincaré duality" is
  over-credited.
- **R3 is stated for the exact DEF-A corner.** O-51 (adopted 2026-08-20, after the charter; `SL:233`;
  `CORE_FRAMEWORK:73–89`) amended the clauses for real records to carrier ⊗ bath. Under the
  amendment, **(v′)** means every single-region flip costs `≥ E_b` with `E_b/kT ≫ 1`, which is
  energetic or kinetic protection. A-GR4 (`SL:247`) and C-77 (`REG:9543`) describe protection as
  "non-contractible support in the corner; **basin boundaries** in the world".
  **The charter never says whether R3 is (v) or (v′).** That ambiguity decides whether locally
  written records can count (§7).
- D-27 (`SL:268`): on non-abelian carriers, "protected" as flip-immunity and as code distance give
  different answers, so a claim of protection has to say which reading it uses.

---

## 3. The candidate `(H₁(Σ), ⟨·,·⟩)`, and what Σ is

**Σ** (`PROOF_V001.md:8–15`) is a **closed orientable surface with a cell decomposition**, with
vertices V, edges E, faces F and genus g. On it:

- A Z₂ gauge field puts `s_e ∈ Z₂` on each edge.
- The physical Hilbert space is `span{|s⟩ : s ∈ Z₁}`, the **Gauss-law sector** (`∂₁s = 0`).
- `M(z)|s⟩=|s+z⟩` and `Z(c)|s⟩=(−1)^{⟨c,s⟩}|s⟩`.
- `H = −Σ_p M(∂p)`. This is Kitaev's toric code, credited as such (`PROOF_V001:104–106`).
- Carriers actually measured: the 2×2 and 2×3 tori, the tetrahedron (a sphere) and a 3×3 disk
  (`GRAVITY_DEFINED:35–40`). Later work added an L×L torus up to L=12 and off-manifold complexes.
- **This Σ is a lattice's topology, not spacetime's** (`CORE_FRAMEWORK:213`, X1). Σ is a fixed
  input, and χ is a construction parameter with no equation of motion (X-2, `REG:4829`, `SL:24`).

| theorem (`PROOF_V001.md`) | statement | role filled | verification |
|---|---|---|---|
| **A** (19–26) | ground space dimension `= \|H₁\| = 2^{2g}` | R1 | 2×2 and 2×3 tori: 4 predicted, 4 measured. Disk: 1, so no record |
| **B** (30–43) | logicals are `H₁` and `H¹`. Z(c) and M(z) anticommute when `⟨c,z⟩=1`. A writer exists for every record | R2 | W-62: `‖{M,Z}‖=1.26e-15`, `‖[M,Z]‖=4.00`, labels `[−1,−1,+1,+1]` (`LANE_W62_CREATION/w62b_logicals.OUT.txt`) |
| **C** (47–61) | an operator supported on a contractible region acts as `∝P` | R3 | worst single-link commutator `1.59e-16`; contractible loops `3.01e-17` |
| **D** (65–78) | splitting is `O(ε^d)` with `d` = minimal non-contractible cycle | R3 order; alpha destroys | slope 2.000 measured across two decades (derived d=2); symmetry degeneracy is linear |
| **G1** (`REG:4749`) | independent records = `2g` = 2 at area 4 and at area 6. T3's `area−1` objects are not records | R1 count | `LANE_G1_RECORD_COUNT/g1b_groundspace.OUT.txt` |
| **G2** (`REG:4792`) | `2^{2−χ}` matches degeneracy on the tori (4) and the sphere (1) | R1 | `LANE_G2_GRAVITY_DEF/g2_gaussbonnet.OUT.txt` |

**Mapping to the record language.** Record = holonomy label `Z(c)` with `c ∈ Z¹∖B¹`.
Writer = non-contractible transport `M(z)` with `z ∈ Z₁∖B₁`. Record space = `Z₁/B₁`, "the
Gauss-law sector modulo plaquettes" (G-4, `REG:5045`).

`SL:40` (G-5) carries the candidacy as FORMAL and SINGLE-CARRIER (toric 2×2). Its falsifier is
"a structure satisfying R1–R3 that H₁ fails to describe". **That falsifier fired** (§4.4, G-6).

A-GR (`SL:3`) gives the role's own falsifiers: **"a record on a genus-0 carrier; a local writer."**

---

## 4. "Accumulated Γ" and T-20

### 4.1 What T-20 is

`ledger/plan.tsv:17` (rendered at `THE_PLAN_V001.md:83`):

> DOES CLASSICAL GRAVITY EMERGE FROM RECORDS? Build a COLLECTIVE quantity from MANY records and ask
> whether it obeys anything Einstein-constraint-like — without importing the constraint (D-1 binds:
> the classical form may be recovered, never assumed or used as the test).
> DONE_WHEN: a many-record collective quantity is defined, computed, and either shown to satisfy a
> constraint of the right type or shown not to — with the classical form never used as a criterion.
> STATUS: **DONE**. Depends on T-6, T-9, T-13. Critical path.

### 4.2 What "accumulated Γ" means

The charter has **no operational definition**. The phrase appears only at `THIRD_TERM:73`,
`GLOSSARY.md:125` and `REG:6825`. The nearest operational text is `REG:6776–6787` ("WHAT WOULD
COUNT AS PROGRESS"), which needs three things:

1. a **collective** quantity built from **many** records, not a property of one record;
2. shown to obey something **Einstein-constraint-like**;
3. without importing that constraint.

The same passage says G-2 is "a relation, not an emergence: the geometry is input on both sides".
Its context: H-1 was reframed as emergence, not identity (`REG:6738`). The register adds that
"H-1 and H-7 may be the same problem": if gravity emerges from records, "the carrier's geometry IS a
description of record content", and that would also answer where the carrier comes from
(`REG:6770–6774`).

### 4.3 The criterion actually used: H-9 (`SL:144`; `REG:7331–7369`)

The principal supplied it before the run: **record-level holonomy**, meaning "a stable, universal,
path-dependent mismatch among records". The diagnostic is
`H_ABCD = (Γ_AB Γ_BD)(Γ_AC Γ_CD)⁻¹` over at least 3 records.

- It is admissible under D-1 because the Einstein form only says what a positive result would
  *mean*; it is never the criterion.
- Further signatures named (`REG:7356`): local; smooth across neighbouring records; **universal
  across record types**; phase/action-based rather than a force; stronger with enclosed record
  density; consistent with causal order; Bianchi-like closure.
- **Vocabulary collision:** `Γ_AB` here is the **transport/connection between records**, not the
  third term Γ.

### 4.4 What happened, from the ledger and git history (not the charter)

| step | result | where |
|---|---|---|
| T-20 run (2026-08-19 17:48, commit `9df305d5`, the same commit that set plan.tsv T-20 → DONE) | on `[[8,3,2]]`, every loop has `‖H−I‖ = 0.000e+00` and the writers commute: **flat** | `REG:7371`; `LANE_T20_HOLONOMY/t20c_final.txt` |
| O-23 | **interpretation withdrawn**. The connection is not determined by the records: 200/200 admissible phase-modified writers give holonomy up to 5.169. "Is the record geometry curved" is not well-posed on the records alone | `REG:7430–7470`; `SL:146` (O-23 FAILED as a question) |
| O-24 / O-25 / C-24–C-26 | minimality selects the flat connection. Density cannot force curvature (stabiliser logical algebra is symplectic). A flat writer set is always available, and clause (iv) is why | `REG:7483`, `7524`, `7665`; `SL:148,151,156,157` |
| H-1 | **PARTIAL**: "the record-level question is answered negatively for the five clauses as written… a theorem about the definition" | `SL:126` |
| T-21 | X-2's record-level reclassification stands; the collective question stays open | `SL:24` |
| **C-77** (adopted 2026-08-20) | "the structure Γ that allows a record — by shaping the boundaries that make a bit non-losable… — is the same structure whose aggregate at scale appears as geometry". Openness clause: other terms may contribute | `REG:9539–9563`; `SL:248` |
| C-78 / C-79 | distance earned as boundary-crossing cost; interface rank one degree below content | `SL:249`; `REG:9612` |
| **C-80 / O-54** | **NO PURE-Γ FALLOFF.** Pure-Γ two-region structure is: zero beyond contact; contact seams; topological constants (**winding w at every distance**); homological switches; one **growing** law, `w_min = d` (confinement). "The falloff enters only through the coupling" | `REG:9674–9700`; `SL:254` |
| C-90 / C-91 | a Γ-priced coupling kernel at criticality gives the lattice Poisson/Green class, `1/d` in D=3. Masslessness is measure conservation. "NEWTON VERDICT: MATCHES AT MEMBER LEVEL", with design point, occupancy bit and norm selection not earned | `SL:269–270`, `SL:248` |
| current | C-77 is **CANDIDATE**: "Never a claim that continuum or Einstein gravity is empirically derived." O-55 (coefficient), O-56 (thermo pair) and O-57 (collapse) remain | `SL:248` |

**Stale charter statements:**
- `THIRD_TERM:47–60`: uniqueness is not open. **G-6 FAILED** (`SL:41`, `REG:5173–5218`).
  Survivors: `H_k` of an arbitrary F₂ complex, qLDPC, and the 3D toric code. "Records require a
  SURFACE" is dead. "Records require non-trivial homology" survives, but non-CSS and non-abelian
  structures are untested. The condition as far as it is established:
  **"Γ = a length-2 F₂ chain complex whose k-systole and k-cosystole both exceed the local scale."**
  O-3 (exhaustiveness) is also FAILED (`SL:19`).
- `THIRD_TERM:72–73` and `GLOSSARY:124–125`: T-20 is not "untouched". It is DONE (null), its reading
  is withdrawn, and C-77 now carries the question.

---

## 5. Import discipline: D-1 to D-9 (`SL` rows; all DEFINED doctrine)

| rule | content (condensed from the row) | TELL / falsifier | SL line |
|---|---|---|---|
| **D-1** | **No classical measure may be applied to the record level as a criterion.** It may be computed and reported as a relationship, but never be the test | any falsifier of the form "our object fails to exhibit ⟨classical feature⟩" is void on sight | 36 |
| **D-2** | the name is the import vector. "Gravity" is a permitted label; inference from the label is forbidden; no attribute transfers through a name | a property justified only by the name | 37 |
| **D-3** | a rescue is always downstream of an import. Remove the import, not the symptom | — | 38 |
| **D-4** (narrowed 2026-09-06) | ALLOW/REQUIRE/SELECT is a type discipline. **Within a frozen parent or fixed fiber**, internal dynamics changes occupancy and does not redefine permissions. An enlarged parent may carry dynamical carrier labels (conditional/open) | an admissibility-preserving map that redefines its own parent's admissible set | 58 |
| **D-5** | at the record level EM has no local content: no field value or density at a place | a local operator that reads the record | 71 |
| D-6 | the ensemble instrument `⟨R⟩` cannot see record formation. Negative verdicts from `⟨R⟩` are void without a single-run warrant | — | 76 |
| D-7 | a caught assumption that lives only in prose will be made again. Every uncleared assumption gets a ledger row | — | 77 |
| D-8 | a check that cannot fail is not a check. A computed verdict needs its noise floor beside it | literal expected values; fits with no floor | 84 |
| **D-9** | a result is described by its mechanism and never ranked against an external standard ("weaker", "only", "falls short of"…). This is D-1 applied to framing | — | 107 |

- The charter names **D-1, D-2, D-4, D-5 and D-9** as the import core (`THIRD_TERM:69–70`;
  `REG:6811`).
- The origin rule is at `REG:4955–4962` (THE RULE, STANDING). The "vector is the name" diagnosis is
  at `REG:4945`.
- **Allied rules that bear on the current search:**
  - D-14 (`SL:159`): a zero is a result only if it is a zero of the object the question names.
  - D-18 (`SL:185`): a record is a logical operator; a flux is an excitation.
  - D-19 (`SL:194`): F₂ cannot pose sign questions, so use integers.
  - D-22 (`SL:210`): a permutation-symmetric carrier has no geometry to detect.
  - D-24 (`SL:246`): each classical concept must earn its place, and no falloff exponent has been
    earned.

**Standing ban list** (`CORE_FRAMEWORK_V001.md:14–29`). These are banned as record-level
comparisons: inverse-square, `r⁻²`, `1/r`, `G`, a metric, **a geodesic**, the Einstein equations,
and "the record-level quantity should be shaped like gravity".

What may be required of a record-level source is all about accumulation: extensive, additive over
disjoint regions, not a mere count, and sign-definite. **"A falloff EXPONENT IS NOT AMONG THEM."**
A null with classical shape can be read two ways (different shape, or no gravity present).

**What D-1 permits:**
- computing a classical quantity and reporting it as a relationship;
- using the classical form to say what a positive result would *mean* (H-9);
- treating the classical relation as a "recovery target at scale only" (`REG:9533`);
- Newton "in the final comparison section only" (`REG:10141`).

The fingerprint variable on the Γ side was "deliberately left open" (`REG:9533–9535`).

---

## 6. ALLOW / REQUIRE / SELECT after the scope repair (2026-09-06)

Sources: `DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/{RESULT.md, ERRATUM_2026-09-06.md, FORMAL_SCOPE_THEOREM.md}`.
Audit: `AUDIT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/INDEPENDENT_HOSTILE_AUDIT.md` gives
`PASS_HOSTILE_ALLOW_REQUIRE_SCOPE_REPAIR_V001`, with 300/300 mechanical and 102/102 semantic checks.

**Definitions** (ERRATUM 23–28):
- `ALLOW_P(v=a)` is membership in a declared parent's attainable set.
- `REQUIRE_P(φ)` is a universal statement over that parent's nonempty admissible set.
- `SELECT` is a separate dynamical account of which allowed occupancy becomes actual.
- These labels do not create operators.

**Superseded** (ERRATUM 5–19): the claims "every level is only ALLOW", "REQUIRE exists at no level"
and "Einstein's equations are wholly constraints". The ADM split also has evolution equations
(Gourgoulhon, gr-qc/0703035).

**Frozen-parent theorem** (FORMAL_SCOPE 4.1): occupancy evolves, and the frozen admissible set
does not.

**Enlarged-parent theorem** (FORMAL_SCOPE 5.2, lines 274–298): if the parent is
`⊕_c H_c` with an owned off-diagonal inter-fiber map `V_{c'c}` that is nonzero on `K_c` and maps
`K_c → K_{c'}`, then a history can move support to a different **effective carrier fiber** while
the global admissible set stays fixed.

**Corollary 5.4** (333–344): "does a carrier arise?" becomes well-typed once five objects are
given: (1) a larger state space with distinguishable carrier fibers, (2) an admissible global
subspace, (3) an owned inter-fiber transition, (4) a before/after occupancy criterion, and
(5) full conservation and boundary accounting.

**Dispositions** (RESULT 28–44):
- D-1 PRESERVE; D-4 NARROW; X-2 and T-21 PRESERVE.
- G-3 SUPERSEDE: only fixed-parent capacity is kept (`SL:16`).
- **F-3, T-II.5 and H-7 REOPEN_CONDITIONALLY** (`SL:54,33,132`). H-7: "record accumulation may
  select or change an effective carrier fiber", with the parent, transition, conservation and
  accounting to be exhibited.
- C-77 and H-1 PRESERVE (open).

---

## 7. Bearing on the current V005 search: is it UNT-native?

These points depend on the brief's description of V005. **None of them was checked against the
V005 source in this step.** They are the specific places where the charter and the current framing
meet.

1. **q_v are not Γ records under the charter's R2/R3.** The brief says q_v bits are written and
   erased by the local Bind term `g p X_r` at the carrier site. That is a local writer, which is
   exactly A-GR's falsifier (`SL:3`) and P-3's exclusion. At most, q_v could be world-tier records
   under (v′) energetic protection, or occupancy. A "footprint of matter on local q" is then a
   coupling- or occupancy-level observable. C-80 places reach and falloff in the coupling, not in Γ.
2. **On V005, the charter-native Γ candidate is the ice manifold's winding/flux sectors.** The ice
   rule is a Gauss law, and winding sectors are `H₁`-type classes, over Z rather than F₂ (D-19). For
   R1–R3 they would need to be:
   - **same-energy** (R1): check whether the degree energy and Bind keep the sectors degenerate;
   - **flipped only by non-contractible transport** (R2): carriers moving around a non-contractible
     occupied ice loop;
   - **untouched by local moves** (R3).
   This is the mapping to test, not something established.
3. **Codex2's result has Γ's own shape and is not a null.** The written–written edge field is
   constant within a fixed winding flux but biases flux sectors. That matches C-80's pure-Γ
   taxonomy: separation-independent topological constants ("winding w at every distance") and
   homological switches, with no pure-Γ falloff. Under D-14 and `CORE_FRAMEWORK:28–29`, a lack of
   distance falloff in q is not a null for Γ.
4. **Several current criteria import classical form if they are used as tests.** These are:
   falloff with distance (the exponent is explicitly not a requirement); orbits (geodesic/force
   shape); and any `1/r` or `r⁻²` target. Under D-1 they may only be reported as relationships, or
   used in a final comparison at scale. Species response is ambiguous: H-9's signature is
   *universality* across record types, and it is an interpretive signature, not a pass/fail test.
5. **Birth is the UNT-native route to "accumulated Γ".** If Birth changes the cycle space and the
   flux sectors, V005 is an **enlarged parent with a dynamical carrier label** (Corollary 5.4). That
   is the conditionally reopened H-7/F-3/T-II.5 question: does record accumulation change the
   effective carrier fiber, meaning Γ's own record space? It is the one place the charter lets
   "content shapes carrier" be asked without making it a classical requirement (`REG:6770–6774`).
   It needs the five Corollary 5.4 objects to be exhibited.
6. **Vocabulary hazards:**
   - "records" in V005 (q_v bits) are not the charter's records (operators satisfying the five
     clauses).
   - "flux" in V005 is a sector label, while D-18's "flux" is an excitation.
   - H-9's `Γ_AB` is a connection, not the third term.
