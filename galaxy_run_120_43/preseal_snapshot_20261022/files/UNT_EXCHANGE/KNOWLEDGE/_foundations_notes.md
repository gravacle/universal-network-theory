# UNT foundations notes: what every lane must know before it starts

Prepared 2026-10-12 by a Claude subagent (read-only extraction; no program file was modified and no project code was executed).
Purpose: ground every lane in the program's own charter, definitions, principles and forbidden moves, in UNT's own terms.
These are NOTES with pointers. The cited files are the authority. Where a source is historical, superseded or in conflict with another, that is marked.

## Path legend

| key | absolute path |
|---|---|
| `U/` | `/Users/bgm/Research/Universal Network Theory/` |
| `PW/` | `/Users/bgm/Research/Universal Network Theory/program-worktree/` |
| `REG` | `PW/REGISTER_V001.md` (question-indexed, append-only register) |
| `TSV` | `PW/ledger/status_ledger.tsv` (the status ledger's source of truth) |
| `SL` | `PW/STATUS_LEDGER_V001.md` (generated view of TSV; `SL:1-6` says so) |
| `PLAN` | `PW/ledger/plan.tsv` (program task list, T-rows) |
| `SR/` | `PW/DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/` |
| `SRA/` | `PW/AUDIT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/` |
| `C7/` | `U/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/CANONICAL_V006_SELECTION_AND_EXACT14_CROSSWALK_V001/` |
| `X/` | `/Users/bgm/Research/UNT_EXCHANGE/` |
| `TO/` | `X/TO_CODEX/` (Claude's numbered messages; principal statements there are RELAYED by Claude, with the principal's words in quotes) |

Citation form: `file:line` or `file:start-end`. `U/CURRENT_STATE.md` is a live append log; its line numbers are as read on 2026-10-12 (~22:00 UTC) and may shift.

---

## 0. Quick card (read this if nothing else)

1. **The charter (principal's words):** find the process responsible for record formation, and explain the roles of EM, gravity and alpha in that process; log what fails and invent a next step. `PW/PRINCIPAL_ACT_001_DRAFT.md:79-81`; `PW/HANDOFF_2026-08-17.md:16-19`.
2. **Gravity's third term is Γ, defined only by function (R1 SPACE, R2 WRITER, R3 PROTECTION).** "Gravity" is a permitted label with zero evidential weight; inference from the label is forbidden. `PW/THIRD_TERM_V001.md:5-27`.
3. **The central claim is ORIGIN:** "Γ is where gravity comes from." Not identity at the record level (withdrawn as an import), not resemblance. Classical gravity is what Γ becomes at scale; the direction is Γ → gravity, never the reverse. `PW/THIRD_TERM_V001.md:62-70`; `REG:6789-6826`.
4. **Classical gravity is never the test at the record level.** No r⁻², 1/r, G, metric, geodesic, Einstein equations, or "gravity needs…" criterion there (`PW/CORE_FRAMEWORK_V001.md:14-21`). A classical-shaped null reads two ways (`PW/CORE_FRAMEWORK_V001.md:28-29`).
5. **Records are defined (DEF-A exact corner; O-51 amended clauses on carrier ⊗ local bath).** All ~20 real records pass the amended clauses; zero pass DEF-A. `PW/CORE_FRAMEWORK_V001.md:61-106`.
6. **ALLOW / REQUIRE / SELECT is the type discipline.** Within a frozen parent, dynamics changes occupancy, never permissions; effective permissions can change only in an enlarged parent that owns the change. `SR/FORMAL_SCOPE_THEOREM.md:113-186, 464-479`.
7. **Import discipline D-1…D-14 (and D-15…D-27) binds every packet.** Table in §7 below. `SL:62-89`; `TSV`.
8. **Current principal premises (2026-10-12, relayed):** records all the way down; the universe is made of Records; no empty space (S1); gravity is collective emergence, never a single-Record verdict; no classical imports in the native chain; build on prior program results; new science PAUSED until the framing is agreed. `TO/0077`, `0080`, `0082`, `0083`, `0084`, `0100`, `0109`, `0110`, `0111`, `0112`.
9. **PROOF means** a measurable quantity in units, a predicted value, a falsifier, and at least two structurally different real record surfaces. Results about the clauses alone are FORMAL. `PW/CORE_FRAMEWORK_V001.md:37-57`.
10. **No route closes without a next step named.** `PW/PRINCIPAL_ACT_001_DRAFT.md:98-102`.

---

## 1. The charter and its three terms

**Charter, standing (R-3, affirmed 2026-08-17):** "Find the process responsible for record formation, and explain the roles of EM, gravity and alpha in that process. We will find things that don't work. Log them, and invent a next step, so that we ultimately find the process responsible for record formation." `PW/PRINCIPAL_ACT_001_DRAFT.md:76-81`. Same wording, slightly varied, at `PW/HANDOFF_2026-08-17.md:16-19`, `PW/RECORD_FORMATION_V001.md:14-17`, `PW/TERRITORY_MAP_V001.md:8`.

- The founding target ("What relationship, if any, holds between gravitational structure, electromagnetic structure, and alpha, in the process by which quantum cells form and records come into being?") and the alpha-as-input reframe are recorded as the principal's standing intent. `PW/FOUNDING_DESIGN_V001.md:11-33`; `PW/PRINCIPAL_ACT_001_DRAFT.md:83-89`.
- **"The program is the goal, not the artifact."** A failed construction closes an attempt, never the program. `PW/PRINCIPAL_ACT_001_DRAFT.md:36-39, 65-67`; `PW/HANDOFF_2026-08-17.md:21-23`; `REG:2030-2034`.
- **Standing rule:** a negative result is entered with what was attempted, what it established, why it failed, and the next step it forces. `PW/PRINCIPAL_ACT_001_DRAFT.md:98-102`.
- The charter word is FORMATION (chosen 2026-08-18 over "build", "closure", "onset"). `PW/RECORD_FORMATION_V001.md:14`. That file is now a historical charter; its current pointer is `PW/PROOF_V002.md` FORMATION section. `PW/RECORD_FORMATION_V001.md:3-12`.

**The three terms (roles as currently registered):**

| term | registered role | status / cite |
|---|---|---|
| **EM** | Supplies both boundary maps of the chain complex: d₁ is the Gauss law, d₂ the plaquette/field-strength term; the record space is the homology of EM's own complex; the record is a holonomy of that field. | A-EM FORMAL, `SL:95`, `TSV:2`. A-EM2/A-EM3 (minimal forming coupling, record, writer all EM holonomies), `SL:99-100`. A-EM4/D-5: the record-carrying EM object is neither local nor the whole system, local content exactly zero, `SL:101`, `REG:5488-5516`. Principal: "at the record level EM is a massive object and not just some field measured in other contexts" `REG:5490-5491`. |
| **Gravity = Γ** | Supplies the record space (R1), the non-local writer (R2), the protection (R3), and the channel (which couplings form a record, via the intersection pairing). Claimed to be where gravity comes from at scale. | A-GR FORMAL `SL:96`; A-GR2 DEFINED `SL:102`; A-GR3 shared origin `SL:103`; A-GR4 boundary-shaping `SL:104`; `PW/THIRD_TERM_V001.md` whole. |
| **alpha** | Two explicitly separated uses. (a) Historical generic perturbation magnitude λ: a sum of local terms that splits the record space at order n* (the fewest available local terms whose product reaches the code space); not the fine-structure constant. (b) Physical fine-structure alpha: exact construction-scoped ALLOW interval; REQUIRE for same-sector ACTVIS records under SAI1-SAI8; SELECT separate and open. | A-AL `SL:97`; A-PR `SL:98`; A-AL2 FORMAL `SL:105`, `TSV:273`; `PW/CORE_FRAMEWORK_V001.md:108-112`; `PW/ALPHA_PROGRAM_PROVENANCE_2026-09-15.md:8-43`. |

**Alpha custody rule (founding):** "Alpha may constrain STRUCTURE. Alpha may not SELECT structure." Legitimate: requiring a slot for a free dimensionless coupling of this type. Barred: choosing a construction because it lands on a known value; inserting a measured number and reading off what follows. `PW/CUSTODY_V001.md:55-68`.

---

## 2. What UNT claims, layer by layer (with status)

### 2.1 The central claim: Γ is where gravity comes from
- Stated by the principal 2026-08-19. Identity at record level: withdrawn as an import (X-6, D-1). Resemblance: never claimed. Origin: THE CLAIM. "Records are the substrate. Classical gravity is what Γ becomes at scale. The direction is Γ → gravity and never gravity → Γ." `REG:6789-6801`; `PW/THIRD_TERM_V001.md:62-70`.
- Why Γ must be defined by function alone: a Γ shaped by any feature of classical gravity could not be shown to give rise to it; the claim would be circular. D-1, D-2, D-4, D-5, D-9 "are what makes the claim non-circular." `PW/THIRD_TERM_V001.md:68-70`; `REG:6809-6812`.
- Commitments: (1) Γ exists at record level with its own content, DONE; (2) nothing of classical gravity assumed in defining Γ, DONE; (3) classical gravity recoverable from accumulated Γ, T-20 (see §5 and §10 for status); (4) direction Γ → gravity, enforced by D-1. `REG:6819-6826`.
- Permanently forbidden by the claim: any classical gravitational feature as a criterion for Γ; expecting Γ to look like gravity; requiring gravity's equations at the record level. `REG:6828-6832`.
- Principal's earlier framing: "We want to connect Γ with classical gravity via emergence from records. We are NOT trying to equate Γ and gravity at the record level." `PW/CORE_FRAMEWORK_V001.md:10-12`; `REG:6740-6741`.

### 2.2 The adopted emergence claim (C-77) and its shape
- **C-77 (adopted by the principal: "yes let's adopt this"):** the structure Γ that allows a record, by shaping the boundaries that make a bit non-losable (non-contractible support in the corner; basin boundaries in the world), is the same structure whose aggregate at scale appears as geometry; classical gravity emerges from the boundary-shaping terms and is not expected to resemble itself at the record level. First falsifiable increment: derive from record-surface boundary structure alone, no classical form assumed, a scale-level relation matching a known gravitational one. Fails if every derivation needs the classical form or yields incompatible relations. Status CANDIDATE. `REG:9539-9557`; `TSV:248`; `SL:187`.
- **Openness clause (principal):** "we don't want to rule out the possibility that other terms contribute to gravity emergence. We are ultimately looking to solve gravity emergence." Γ is the named contributor, never asserted as the only one. `REG:9559-9563`.
- **A-GR3 shared origin** (principal, TD-1): Γ is the common structure that ALLOWS records on a frozen parent and is proposed to appear at scale as geometry; record-level measures may differ from macroscopic ones; the classical relation is a recovery target at scale only (D-1). `SL:103`; `TSV:245`.
- **A-GR4 mechanism shape** (principal): "We don't expect classical gravity to look the same at the record level. We expect it will emerge from terms like Gamma that SHAPE GEOMETRY AND BOUNDARIES." `SL:104`; `TSV:247`.
- **The principal's emergence criterion (H-9, supplied for T-20):** "a stable, universal, path-dependent mismatch among records that can be interpreted as curvature"; "One record cannot show gravity. Two give relation. Several make PATH COMPARISON possible." Diagnostic H_ABCD = (Γ_AB Γ_BD)(Γ_AC Γ_CD)⁻¹. Further signatures named by the principal: local, smooth across neighbouring records, universal across record types, phase/action-based rather than a force, stronger with enclosed record density, consistent with causal ordering, Bianchi-like closure. The Einstein form says what a positive result would MEAN and is never the criterion. `REG:7330-7367`; `SL:33`.

### 2.3 The roles statement (A-PR / claims grid G-E)
"EM supplies the complex and the record. Gamma supplies space, writer, protection, and channel. Alpha has two explicitly separated uses…" with the physical-alpha ALLOW/REQUIRE/SELECT ladder; every constituent result keeps its own tier. `SL:98`; `PW/THE_CLAIMS_V001.md:16`. The claims grid G-A…G-I with live stages is at `PW/THE_CLAIMS_V001.md:10-20` (G-D classical/continuum field-side recovery = MEMBER-LEVEL-MATCH, direct field readout open, `:15`).

### 2.4 The UNT Closure Theorem (typed composition, conditional components)
- `PW/UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md` (2026-09-19). UNT "places quantum-scale record formation and macroscopic gravity within a single computable topological framework" (`:17-18`). Record-formation dependency order: `ALLOW -> REQUIRE -> GATE -> ELECTROMAGNETISM -> RECORD` (`:24-26`).
- Components and their types (`:247-267`): AURFT Coverage-U (exact inside adopted U-DCL axiom); alpha ALLOW (exact construction) and REQUIRE (conditional inheritance with empirical anchor); finite L4-L12 record envelope (exact + authenticated arithmetic); finite ARGER Gate (adopted classification); dynamical z=1 (conditional on LL-P); record-conditioned geometry (exact inside adopted RGRL); macroscopic Einstein-Hilbert response (conditional on RGRL and WTC-H1…H5, coefficient calibrated by G_obs, `:167-187`).
- "No implication from a finite ARGER Gate pass to satisfaction of RGRL or WTC-H1 through WTC-H5 is claimed." `:255-256`.
- **Qualifiers the lanes must carry with it:**
  - Root README: these results "do not establish an unconditional native gravity theory or derive the numerical fine-structure constant." `U/README.md:14`.
  - Reviewer ladder: "ARGER pass — ADOPT gate membership / CERT implementation; UNINFORMATIVE as physical criticality evidence." `U/LADDER.md:31` (full audited-label table `U/LADDER.md:24-34`).
  - Adoption-log audit: the ARGER Gate was adopted "by principal decision" one day after the authenticated relational z=1 test was rejected; flagged post_failure_fix / criterion_after_results; clauses (1) and (3) "cannot fail"; the closure theorem does not disclose the rejection. `U/ADOPTION_LOG.md:126`. (Historical reviewer assessment, copied verbatim; `U/ADOPTION_LOG.md:5-12` says copying it does not newly adopt anything.)
  - GFT-1 ceilings: RGRL's empirical confirmation, microscopic F3 derivation, strict induced origin and parameter-free G remain open. `TSV:274`.
  - The principal (2026-10-12, relayed): "z=1 method … was actually the correct way to approach that metric" (exact response sum-rule method), while the audit objections (roundoff in preregistered 1/L tests; ARGER passes by construction; S(k) small-k input taken from an external Luttinger premise) stand separately. `TO/0108:1-18`.

### 2.5 Current principal premises (2026-10-12, relayed by Claude in TO_CODEX)
These are the principal's most recent stated premises. Each is quoted from the relay header; the bullets give the operational consequence written in the same message.

| premise | principal's words (as relayed) | consequence registered | cite |
|---|---|---|---|
| Records all the way down | "UNT basically says gravity starts at the record level. There is no 'new gravity' added later. It's records all the way down. It just emerges." GR was assumed only as scaffolding where classical gravity could not emerge. | No separate gravity source law; Records are the source; an added bond-angle operator (P-31) is a diagnostic, not the verdict. | `TO/0077:1, 7-12` |
| Universe made of Records | "There are records all the way across the universe. The universe is made of records. Why is this a mystery?" | Matter and space are both made of Records; gravity needs a difference (gradient) relative to a Record-filled background; blank-start runs are controls only. | `TO/0080:1, 7-15` |
| S1: no empty space | "There is no 'empty space' in UNT." | Blank-Record states are mathematical controls and limits only; physical comparisons are between Record-filled backgrounds. S1 is registered as a declared state premise of the canonical model; it fixes no numbers. | `TO/0082:1, 7-13`; `TO/0083:9-11`; `C7/CANONICAL_MODEL_7_PROPOSAL_V005.txt:25-32` |
| Derive the background | "We want to derive this" | The Record-filled background (density, pattern, correlations) is to be derived from the dynamics (P-49), declared only if derivation is proved impossible and then referred to the principal. | `TO/0084:1-12` |
| No classical imports | "We need to be careful here not to import classical machinery into the analysis." | Native verdict from the canonical model's own dynamics; classical constructs only as labelled conditional diagnostics; CLASSICAL-IMPORT LEDGER in every packet; any load-bearing import is a declaration to the principal. | `TO/0100:1-25`; audit results `TO/0102:1-15` |
| Gravity is collective emergence | "I never would have assumed that you could get gravity from individual records. This has always been about emergence and collective behavior." | Single-carrier/single-Record results are constraints on the parts, never gravity verdicts. | `TO/0109:1, 7` |
| Build on previous learning | "The whole point of doing a project like this is to build on previous learning." / "If we have to start from scratch every time … we end up repeating work." | PRIOR-WORK LEDGER mandatory in every packet and task (REGISTER C/X/D entries, status rows, theorems, with path and line); accepted results written back to REG and TSV. | `TO/0110:1, 15`; `TO/0111:1, 6-21` |
| Pause new science | "This program is too much of a departure from standard physics to just throw work at agents." | New science paused until a framing in UNT's own terms is agreed (charter, ALLOW/REQUIRE, Γ by function, collective emergence, Records all the way down). A standard-physics default "is a framing error, not a neutral starting point." | `TO/0112:1-14` |
| Canonical rule set (declared premise) | (decision) canonical UNT = literal V006 H_complete #7 + owner-once admission-resource extension | Declared premise, not a derivation; admission and Bind are joined deliberately, not identified. | `TO/0005:9-24` |

### 2.6 The current empirical objective
"The current objective is one physically normalized law connecting measured galaxy dynamics and expansion without imported dark-sector energy budgets." `U/README.md:3`. Clean native 120-chunk and regenerated 43-point NGC 3198 comparison unstarted; physical normalization, causal source preparation, common matter/light response and gravitational/expansion admission open; superiority not established. `U/README.md:14-18`; `U/CURRENT_STATE.md:5, 11`. Full goal includes lensing, growth, mergers, BBN/early universe/CMB, thermal origin, fair joint comparisons. `U/UNT_FRESH_CHAT_HANDOFF_2026-10-12_V001.md:37`.

---

## 3. Primitive objects: terms and their (several) meanings

Many UNT words have more than one registered sense. A lane must say which sense it uses. Conflation is a recurring failure (D-14, D-18, D-27).

### 3.1 Record
| sense | definition | cite |
|---|---|---|
| DEF-A record (exact corner) | Operator R on an open system (H,{L_k}) meeting clauses (i)-(v) (§4). Standard name: a logical operator of a QEC code plus clause conditions (RENAMING). | `PW/CORE_FRAMEWORK_V001.md:96-106`; `PW/GLOSSARY.md:21` |
| O-51 amended record (the world's records) | Same clauses restated on CARRIER ⊗ LOCAL BATH with declared tolerances (T, t_m, δ, t_w, Δ, W, N_r). | `PW/CORE_FRAMEWORK_V001.md:73-84`; `REG:9119-9187`; `TSV:233` |
| UNT forward noun | "Record names a retained network state or its topological mass/data content." Record is the static noun; Bind and Birth name actions. | `PW/nomenclature/BIND_BIRTH_POLICY.md:3-7`; `U/LADDER.md:50` |
| Canonical #7 native Record q_v | Binary one-content Record bit at each site of the graph; written/rotated by Bind; distinct from the Spent cell label P_S (N_spent and N_q are distinct censuses, neither asserted monotone). | `C7/CANONICAL_MODEL_7_PROPOSAL_V001.txt:10-21`; `C7/CANONICAL_MODEL_7_PROPOSAL_V003.txt:4, 17` |
| Not a record | A flux is an excitation, not a logical operator; check the five clauses before calling anything a record (D-18). | `SL:80` |
| OPEN conflict | Whether V005's local q Records (written/erased by the local Bind term) are the charter's "records": on their face they fail R2/R3. Principal's call. | `TO/0106:13, 19` |

### 3.2 Carrier, bath, parent, fiber
- **Carrier:** the physical system (lattice, code, chain complex); RENAMING. `PW/GLOSSARY.md:41`. Canonical benchmark is the toric code; 1D rings are a boundary-constrained proxy (D-23). `PW/CORE_FRAMEWORK_V001.md:126-141`.
- **Carrier ⊗ local bath:** where the amended clauses live; records are macroscopic because the bath must export the write energy (answers H-6). `PW/CORE_FRAMEWORK_V001.md:73-74, 91-92`.
- **Parent specification P:** all data held fixed while a dynamical question is asked (carrier, topology, couplings, boundary conditions, controller, state-space representation). `SR/FORMAL_SCOPE_THEOREM.md:35-41`.
- **Enlarged parent / carrier fiber:** direct sum over carrier labels c with off-diagonal fiber maps; a block-diagonal dynamics does not establish carrier formation. `SR/FORMAL_SCOPE_THEOREM.md:249-272`.
- **Canonical #7 "carrier" p_v:** a hard-core binary carrier at each site, distinct from Record q_v and from the I/R/S resource cell. `C7/CANONICAL_MODEL_7_PROPOSAL_V003.txt:4`; S1 does not identify p with q `C7/CANONICAL_MODEL_7_PROPOSAL_V005.txt:32`.

### 3.3 Network / graph
- UNT "investigates whether causal Records and the Bind and Birth actions can provide a common physical account of matter, gravity and cosmic evolution." `U/README.md:3`.
- Canonical #7 network: the literal V006 old periodic q4 (diamond) graph plus a supplied one-Born four-cut/two-star graph; every edge carries an incidence bit n_e; d_v = Σ_{e at v} n_e. `C7/CANONICAL_MODEL_7_PROPOSAL_V003.txt:4`; H_complete is combinatorial with no native coframe or bond-length dependence `C7/CANONICAL_MODEL_7_PROPOSAL_V001.txt:44-49`.
- Finite relational family: L = even size and one-pass horizon of an owner-once periodic-prism parent (L active cells, 2L carrier sites, 3L transport edges, L fresh admissions); separate sizes, not a growing run or a continuum coordinate. `PW/GLOSSARY.md:97`; `PW/README.md:34-38`.
- Principal: the Record network fills the universe (`TO/0080:7`); geometry/range questions are decided on graph distance, not 3D shells (`TO/0102:15`).

### 3.4 Bind, Birth, admission (actions)
| term | meaning | cite |
|---|---|---|
| **Bind (Bind Operator)** | "the action that locks phase space to maintain Records". In canonical #7: g Σ_v p_v X_(r,v); rotates q (even at a spent site); conserves N_c; commutes with P_S. | `PW/nomenclature/BIND_BIRTH_POLICY.md:4`; `C7/CANONICAL_MODEL_7_PROPOSAL_V003.txt:5-7, 17` |
| **Birth (Birth Operator)** | "graph splicing that adds Volume". Canonical: finite four-cut/two-star map T = F_q4 P_(S=2) ⊗ J_blank (norm 1); new Records blank, no carrier at insertion; its adjoint (un-Birth) is real and never omitted; no indefinitely iterated Birth rule is supplied. | `PW/nomenclature/BIND_BIRTH_POLICY.md:5`; `C7/CANONICAL_MODEL_7_PROPOSAL_V001.txt:25-33`; `C7/CANONICAL_MODEL_7_PROPOSAL_V003.txt:15` |
| Renaming caution | Changing names "does not supply a missing physical vertex, validate a model, or alter a scientific result." | `PW/nomenclature/BIND_BIRTH_POLICY.md:5-7` |
| **Intrinsic admission** (relational line) | Finite owner-once transition on an allowed loaded-cell/blank-target pair (w,r), with depleted bandwidth and sealed lineage retained; "its configuration predicate does not itself generate motion". OURS. | `PW/GLOSSARY.md:73`; rung 1 `U/LADDER.md:39-41` |
| **Canonical admission** (#7 + admission) | A_v⁺ = \|S,x⟩⟨R,B\| ⊗ I_q on a per-site cell span{I,R,S} (Ready/Spent); Hermitian with reverse (un-writing allowed); conserves Q = N_c + N_ready and M = N_ready + N_spent; does not itself write q. No permanence is imposed. | `C7/CANONICAL_MODEL_7_PROPOSAL_V003.txt:8-19` |
| Bind ≠ admission | Admission changes N_c (conserving N_c + N_ready); Bind conserves N_c; no full-domain equivalence follows; the principal's sign-off joins them deliberately rather than identifying them. | `C7/CANONICAL_MODEL_7_PROPOSAL_V001.txt:56-60`; `TO/0005:16-22` |
| **Admissibility predicate** (type theory) | A_P : X_P → {0,1}; admissible set; a projector only after a representation is supplied. Unrelated to the admission operator above. | `SR/FORMAL_SCOPE_THEOREM.md:35-64` |
| **Admissible U** (DEF-A) | A unitary with [U,H]=0 (O-4, PROVISIONAL, one carrier family). Equivalent, given (i)+(ii), to Tr(P_E R)=0 on every eigenspace. | `PW/CORE_FRAMEWORK_V001.md:114-117`; `PW/GLOSSARY.md:27` |
| **Admissible (O-51 (iv′))** | Writable by an energy-conserving dilation unitary on carrier ⊗ writer ⊗ bath; cost reappears as free energy, floor kT ln2 + ΔE_config. | `PW/CORE_FRAMEWORK_V001.md:81` |

### 3.5 Writer, protection, contractible, channel
- **Writer:** the conjugate logical operator (RENAMING). `PW/GLOSSARY.md:29`. P-2: built from neither H nor {L_k}. P-3: no admissible writer fits inside one contractible region; the strong reading "nothing local can write it" is FALSE (Theorem D: d local terms do reach the record; minimum-weight admissible writer at L=3 is a product of three individually inadmissible single-edge operators). `PW/CORE_FRAMEWORK_V001.md:163-182`.
- **Protected (clause v):** no admissible operation on a single contractible region flips R. The word "admissible" is load-bearing (erratum: without it (v) is false of the toric code). `PW/CORE_FRAMEWORK_V001.md:106, 119-124`. Two readings (flip-immunity vs Knill-Laflamme code distance) diverge on non-abelian carriers; claims must name their reading (D-27). `SL:89`.
- **Channel (G-16, OURS):** a coupling forms a record iff it pairs oddly with the record's conjugate. `PW/GLOSSARY.md:40`.

### 3.6 Γ and R1-R3
See §5. Γ is OURS, "a deliberate placeholder for (H₁(Σ), ⟨·,·⟩), defined by function (R1-R3). Introduced to keep classical gravity out of its definition." `PW/GLOSSARY.md:36`.

### 3.7 Alpha (three distinct objects; never interchange)
1. Generic perturbation magnitude λ (DEF-A corner): "It is NOT the fine structure constant"; sets formation rate χ ~ λ^{2n*}. `PW/CORE_FRAMEWORK_V001.md:108-112`; RENAMING `PW/GLOSSARY.md:53`.
2. Physical fine-structure alpha: constitutive identity data of an electromagnetic parent ("A different alpha is a different parent"); ALLOW interval I_χ ∩ ((−ln(1−δ))/(4πB²), ∞); REQUIRE inheritance for ACTVIS same-sector records; SELECT open. `PW/ALPHA_PROGRAM_PROVENANCE_2026-09-15.md:10-43`; `PW/GLOSSARY.md:54`; `SL:105`.
3. Formation-activity coefficient a_v^adm: "Exact formation-activity coefficient a_v^adm is NOT electromagnetic fine-structure alpha." `U/CURRENT_STATE.md:92`.
- Also: the L12 majority margin 0.0696… interpreted as an alpha write cost / binding energy is a HYPOTHESIS. `PW/README.md:103-105`.

### 3.8 ARGER, gate, occupancy, lineage
- **ARGER process:** `ALLOW -> REQUIRE -> GATE -> EM -> RECORD`. The finite ARGER Gate is applied at the GATE step; the finite record block is the evidence domain, not part of ARGER's identity. `PW/README.md:22-32`; `PW/GLOSSARY.md:90`.
- **Occupancy:** the actual state inside the admissible set; occupying one allowed alternative does not forbid the others. `SR/FORMAL_SCOPE_THEOREM.md:80-93`.
- **Lineage:** retained ancestry/provenance coordinate (spent-genesis subset S, preserved injectively). `PW/GLOSSARY.md:74`.
- **URM (Universal Record Model):** the program's model; "Universal" is operational and "a TITLE, not a claim". `PW/GLOSSARY.md:127-135`; D-26 `SL:88`.

---

## 4. DEF-A, O-51 and what "proof" means

### 4.1 DEF-A, the exact corner (`PW/CORE_FRAMEWORK_V001.md:96-106`)
Given H and jump operators {L_k}, R is a RECORD if:
| clause | condition | meaning |
|---|---|---|
| (i) | R = R†, R² = I | a bit |
| (ii) | [H,R] = 0 and [L_k,R] = 0 ∀k | durable |
| (iii) | R not constant on some eigenspace of H | distinguishes states of the same energy (not a function of H) |
| (iv) | some admissible U has U†RU = −R | writable |
| (v) | no admissible operation on a single contractible region does | protected |

- Why (iii): if R = f(H), knowing the energy tells you the record. `:143-146`. Why (iv)+(v): the writable/durable tension made explicit. `:148-150`.
- P-1 (iii) ⟹ H degenerate; P-2 writer built from neither H nor {L_k}; P-3 no admissible writer inside one contractible region. `:163-182`.
- "What is actually ours": clause (iii); admissible := [U,H]=0; Γ as functional placeholder and the discipline that kept gravity out; the channel criterion; n*; the assembly. `PW/GLOSSARY.md:113-122`.

### 4.2 O-51, the amended definition grounded in the world's records (adopted 2026-08-20)
- Why: ~20 real records (HDD/FePt/CoCrPt, tape, flash, MRAM, AgBr, DNA, synapse, zircon, mica fission track, ice core, lava TRM, CMB photon polarisation, SC flux quantum, B−L): ZERO satisfy DEF-A. "THE WORLD USES ENERGETIC AND KINETIC PROTECTION. THE EXACT CLAUSES ASSUME TOPOLOGICAL PROTECTION." `PW/CORE_FRAMEWORK_V001.md:61-71`; `REG:9126-9150`.
- The one move: clauses restated on CARRIER ⊗ LOCAL BATH with declared tolerances. `PW/CORE_FRAMEWORK_V001.md:73-74`.

| | amended clause | cite |
|---|---|---|
| (i′) | commuting spectral family {P_a}, not necessarily an involution | `PW/CORE_FRAMEWORK_V001.md:78` |
| (ii′) | durable to t_m (O-5 width bound δ = ħ/t_m) | `:79` |
| (iii′) | non-constant on the closed system's energy shell, width √(C_v k_B T²) ≥ ΔE_config | `:80` |
| (iv′) | writable by an energy-conserving dilation unitary on carrier ⊗ writer ⊗ bath; cost = free energy, floor kT ln2 + ΔE_config | `:81` |
| (v′) | every single-region flip costs ≥ E_b, E_b/kT ≫ 1 | `:82` |

- ALL ~20 real records pass. DEF-A is retained and renamed as the T→0, t_m→∞, W=0, E_b→∞ corner; every FORMAL row stays a true theorem about that corner, "which has approximately zero residents there." `PW/CORE_FRAMEWORK_V001.md:84-89`.
- The goal's grounding clause converts H-3, H-5, H-6 into standing acceptance criteria: every PROOF grounded in at least one named physical record with real numbers. `REG:9152-9161`; `TSV:233`.
- It reopens the energy route to a gravity source: dE = work paid is "a measurable, non-zero, record-by-record configuration energy" which "is exactly what a source term needs." `REG:9163-9172`.
- First world record satisfying the definition: CoCrPt HDD grain (T-29), all amended clauses pass with margins; the same grain fails every DEF-A clause. Reproducing the retention law "is grounding, not a distinguishing prediction." `REG:9191-9235`.

### 4.3 PROOF, FORMAL, and the H-3 hazard
- Principal: "The PROOF must be something that any physicist anywhere in the world can run against their real world data and confirm that it works as asserted." `PW/CORE_FRAMEWORK_V001.md:39-43`.
- A row is PROVED only with (1) measurable quantity in units, (2) predicted value/relation, (3) falsifier, (4) RECORDS VERIFIED on at least two structurally different real record surfaces (different mechanism, not different parameters); enforced by `ledger/status.py`. `PW/CORE_FRAMEWORK_V001.md:48-53`.
- Results about the five clauses are FORMAL, "real mathematics", not claims about the world. "H-3: the five clauses are ours, and nothing says the world's records meet them." `PW/CORE_FRAMEWORK_V001.md:55-57`. H-3 remains PARTIAL on "why THIS definition". `SL:27`.
- Out of reach, named so they are not mistaken for oversights: X1 topology is a lattice's, not spacetime's; X2 record-level matter response (withdrawn row; D-1); X3 outcome problem; X4 empirical contact. `PW/CORE_FRAMEWORK_V001.md:209-216`.

---

## 5. Γ (the third term): R1-R3, the candidate, uniqueness, and T-20

**R1-R3** (`PW/THIRD_TERM_V001.md:21-30`):
| | requirement | source |
|---|---|---|
| R1 SPACE | supplies a set of states a record can occupy, of size > 1, distinguishing states of the SAME energy | clause (iii) |
| R2 WRITER | supplies an operation that flips the record, which no local operation can mimic | clauses (iv)+(v), P-3 |
| R3 PROTECTION | ensures no local operation writes or destroys it | clause (v) |
"Stated in the record level's own terms and mention nothing external." `:29-30`.

- **Γ IS WHATEVER SATISFIES ALL THREE.** Theorems A-D are statements about whatever satisfies R1-R3, independent of the name. `PW/THIRD_TERM_V001.md:21, 34-37`.
- **H₁(Σ) with the intersection form is a CANDIDATE, not a definition** (it satisfies R1-R3 by Theorems A, B, C). `GRAVITY_DEFINED_V001.md` is SUPERSEDED because it made the identification a definition "so nothing could fail it". `PW/THIRD_TERM_V001.md:39-45`; `PW/GRAVITY_DEFINED_V001.md:1-2`.
- **Uniqueness question** posed as open in THIRD_TERM (`:47-60`); later answered by **G-6: "UNIQUENESS IS BROKEN"**: H₁(Σ) is one structure satisfying R1-R3, not the only one. "Records require a SURFACE" is dead; "records require non-trivial homology" survives; CSS structure not required by R1-R3; non-CSS and non-abelian orders untested; fracton lens unswept (coverage gap). Established condition: Γ = a length-2 F₂ chain complex whose k-systole and k-cosystole both exceed the local scale (R3 needs two numbers). `REG:5173-5200`. Per THIRD_TERM's own fork (`:56-58`), non-uniqueness weakens statement 4 from "records require" to "records admit".
- **When Γ may be renamed:** only after R1-R3 are solved, and only if the solution earns it. `PW/THIRD_TERM_V001.md:75-78`.
- **T-20 (recovering classical gravity from accumulated Γ):** THIRD_TERM records "untouched — plan task T-20" (`:72-73`); GLOSSARY repeats it (`PW/GLOSSARY.md:124-125`). Later history: T-20 ran against H-9 and found the record geometry exactly flat on [[8,3,2]] (`REG:7371-7400`); O-23 then showed the connection is not determined by the records (holonomy 0 to 5.169 across admissible writers), so T-20's interpretation was withdrawn and the question became "what determines the connection?" (`REG:7430-7464`); O-24: minimality selects the flat connection (`REG:7483`). `PLAN:17` marks T-20 DONE (task executed, criterion as stated in its DONE_WHEN). C-77's increments (C-79, C-80, C-87/C-88, C-90, C-91) give a member-level Newton match with load-bearing caveats (enforcement and norm unearned) and C-77 stays CANDIDATE (`TSV:248`). The principal's relay says "T-20 is DONE and reread into C-77" (`TO/0110:11`). See §10 item 1.
- Program results the principal's grounding message lists as the program's own gravity line: C-77 (Γ responds to Record boundaries), C-78 (distance = boundary-crossing cost, a true metric on record venues, `TSV:249`), C-80 (no pure-Γ falloff; falloff enters only through the coupling; division of labour Γ / coupling / alpha, `TSV:254`), C-90/C-91 (Γ-priced kernel; D=3 critical member 1/d; occupancy = measure conservation, one undischarged bit, `TSV:269-270`). `TO/0110:7-12`.
- Γ-first question now pending: P-54 Γ census of V005 structures with exact R1/R2/R3 verdicts; the ice winding/flux class is named as collective by nature. `TO/0106:15-19`; `TO/0109:13`.

---

## 6. ALLOW / REQUIRE / SELECT (the type discipline)

### 6.1 Origin (D-4, 2026-08-19)
Principal: "Isn't this the whole allow/require framework?" Minimum weight (systole/cosystole) is a property of the carrier, so it is an ALLOW; asking what PRODUCES a permission is the category error. "Dynamics produces OCCUPANCIES, never PERMISSIONS." F-2 withdrawn as written (corrected to the occupancy question); F-3 reclassified; formation and measurement collapse into one question: what selects one element of an allowed, exactly degenerate set? `REG:5220-5262`. Emergence (an identification between levels of description) is not a D-4 error. `REG:6755-6759`.

### 6.2 The scope repair (governing since the hostile audit passed)
- Verdict: `PASS_HOSTILE_ALLOW_REQUIRE_SCOPE_REPAIR_V001`, mechanical 300/300, hostile semantic screen 102/102. `SRA/INDEPENDENT_HOSTILE_AUDIT.md:3-8, 94-105`. Promotion rule: governing only with both records. `SR/RESULT.md:56-62`.
- **Five typed objects that may not be interchanged:** admissibility predicate; its characteristic projector (after a representation is chosen); constraint generators; occupied state; dynamical or coarse-graining map. `SR/FORMAL_SCOPE_THEOREM.md:17-26`.
- **Definitions** (`SR/FORMAL_SCOPE_THEOREM.md:115-162`): attainable set S_P(v) = {v(x): x ∈ A_P}. ALLOW_P(v=a) ⟺ a ∈ S_P(v). REQUIRE_P(φ) ⟺ ∀x ∈ A_P, φ(x); numerically, S_P(v) = {a*} (singleton). SELECT_{P,D,μ0}(v=a) ⟺ a declared trajectory or limiting law selects the v=a occupancy (what "selects" means must be declared). FORBID_P(v=a) ⟺ a ∉ S_P(v). Origination is not a fourth modal value; it is historical and needs a declared dynamical parent. "The bare fact that one state is actual is occupancy, not a dynamical selection theorem."
- **Logical relations** (`:164-173`): REQUIRE ⟹ ALLOW (nonempty A_P); ALLOW ⇏ REQUIRE; admissibility-preserving SELECT ⟹ ALLOW; SELECT ⇏ REQUIRE; REQUIRE supplies no parent-selection mechanism.
- Host-sector REQUIRE "is not a production operator. It is a universal conditional statement inside a parent whose sector is already fixed." `:184-186`.
- **Frozen-parent theorem 4.1:** admissibility-preserving dynamics changes occupancy, correlations, reachable subsets and stationary measures without changing the parent's admissible space. `:190-218`. Corollary 4.2 (scoped D-4): within a frozen parent, asking D_P to construct A_P is circular; legitimate questions are which occupancy is reached, what invariant/attracting subsets exist, what selects among them. `:220-230`. Example 4.3: selection without changed permission. `:232-247`.
- **Enlarged-parent theorem 5.2 and Example 5.3:** with an owned off-diagonal fiber map preserving global admissibility, a history can move occupancy into another fiber whose effective predicate differs, while the global predicate is fixed. "Not evidence that the record program's physical parent contains the required fiber variable or coupling." `:274-331`.
- **Corollary 5.4, formation is a lawful enlarged-parent question** only when given: (1) a larger state space with distinguishable carrier fibers; (2) an admissible global subspace; (3) an owned off-diagonal transition; (4) a before/after occupancy criterion; (5) complete conservation and boundary accounting. "Absent these objects, carrier formation remains open rather than prohibited." `:333-344`.
- **Projectors vs generators:** common-basis characteristic projectors commute exactly (Boolean null control, no spacetime meaning); the same admissible subspace admits non-commuting constraint generators; noncommutation comes from supplied representation data, not from the words ALLOW/REQUIRE. `:346-409`. A scaling exponent cannot be injected into an exact zero to create an anomaly; unconstructed generators have an undefined anomaly, not zero. `:436-444`.
- **Repaired scope rule (§8):** "Within a frozen parent, internal dynamics changes occupancy inside the parent's admissible space; it does not change the definition of that parent's permissions. Effective permissions may change along a history only when an enlarged parent, external parent family, or explicitly declared coarse-graining map contains and owns the variables responsible for the change." `:464-479`.
- **Dispositions** (`SR/RESULT.md:26-44`; `SR/ERRATUM_2026-09-06.md:38-51`): D-1 PRESERVE; D-4 NARROW (frozen parent/fixed fiber); X-2 and T-21 PRESERVE (collective emergence open); G-3 SUPERSEDE (all-level/no-REQUIRE wording retired; only fixed-parent Γ capacity remains, `TSV:16`); F-3, T-II.5, H-7 REOPEN_CONDITIONALLY (`TSV:54, 33`; `SL:31`); A-GR3 NARROW; A-GR4, C-77, H-1 PRESERVE; H-8 SUPERSEDE.
- **ADM correction:** the earlier claim that Einstein's equations are wholly constraints on admissible data was overstated (3+1 has constraints plus evolution equations); "This correction is a scope repair only; it imports no Einstein … structure into the microscopic record parent." `SR/ERRATUM_2026-09-06.md:11-19`.
- **Explicit non-claims:** no Poincaré/Virasoro closure, continuum limit, Ward identity, gravity, or proof of emergence. `SR/RESULT.md:53-54`; open list `SR/FORMAL_SCOPE_THEOREM.md:508-516`.
- **The alpha ladder is the worked instance:** finite recordhood can ALLOW a non-singleton set; embedding in one realized sector REQUIREs same-sector inheritance; a complete-universe singleton is a separate theorem; SELECT_parent may not exist. `SR/FORMAL_SCOPE_THEOREM.md:175-182`; `PW/ALPHA_PROGRAM_PROVENANCE_2026-09-15.md:39-43`.
- Principal's current ask: frame UNT in its own terms including ALLOW/REQUIRE. `TO/0112:12`.

---

## 7. The import discipline: D-1 … D-14 (standing doctrine, checked before any lane is commissioned)

`SL:59-60` header: "STANDING DOCTRINE — checked before any lane is commissioned". Text below is condensed from the ledger rows; read the row before relying on the paraphrase.

| ID | rule (condensed) | TELL / would be refuted by | origin | status | cite |
|---|---|---|---|---|---|
| **D-1** | No classical measure may be applied to the record level as a criterion. A classical quantity may be computed and reported as a relationship; it may never be the test our object must pass. | A falsifier of the form "our object fails to exhibit ⟨classical feature⟩" is void on sight. | X-2 backreaction, X2 allow→require, X-6 falsifier | DEFINED; PRESERVED by scope repair | `TSV:36`; `SL:62`; `REG:4955-4962`; `SR/RESULT.md:30` |
| **D-2** | The name is the import vector, but the fix is the discipline, not the word. "Gravity" is a permitted LABEL for Γ; inference from the label is forbidden; no attribute transfers through a name. | A property of our object justifiable only by the name. | X-2, X2 erratum, X-6 | DEFINED | `TSV:37`; `SL:63`; `REG:4945-4949, 4980-4987`; `PW/THIRD_TERM_V001.md:5-17` |
| **D-3** | A rescue is always downstream of an import. Remove the import, not the symptom. | A rescue with no import upstream. | X-6 rescue-detector | DEFINED | `TSV:38`; `SL:64` |
| **D-4** | ALLOW/REQUIRE/SELECT is a type discipline. Within a frozen parent/fixed fiber, admissibility-preserving dynamics changes occupancies and does not redefine permissions; an enlarged parent with owned inter-fiber transitions is conditional/open; SELECT is separate. | An admissibility-preserving internal map on one fixed parent that redefines that parent's admissible set. | F-2/F-3 (2026-08-19); scoped 2026-09-06 | DEFINED (NARROWED) | `TSV:58`; `SL:66`; `REG:5220-5262`; §6 |
| **D-5** | At the record level EM has no local content: field strength at a point, energy density, local flux, E(x) have no record-level referent. D-1 applies unchanged. | Any sentence assigning EM a value or density AT A PLACE; refuted by a local operator that reads the record. | LANE_EM_EXTENT; Thm C 1.59e-16 | DEFINED | `TSV:71`; `SL:67`; `REG:5488-5516` |
| **D-6** | The ensemble instrument ⟨R⟩ = Tr(Rρ) is blind to record formation; negative verdicts from ⟨R⟩ are void without a single-run warrant. | Any exclusion warranted by an expectation value or code-space entropy. | W-35 unravelling (definite record on 78.5% of runs, same ρ(t)) | DEFINED | `TSV:76`; `SL:68` |
| **D-7** | A caught assumption that lives only in prose will be re-made; every uncleared assumption gets a ledger row. | — | A4 in SURFACE_ASSUMPTION_AUDIT | DEFINED | `TSV:77`; `SL:69` |
| **D-8** | A check that cannot fail is not a check; a computed verdict is not a check unless the noise floor is measured beside it. | An expected value that is a literal; a fit with no noise floor. | O-4 lane (5 tautologies of 108); 1e-15 slope fit | DEFINED | `TSV:84`; `SL:70`; `REG:5725` |
| **D-9** | A result is described by its mechanism, never ranked against an external standard (D-1 applied to framing). | The words weaker, stronger, only, merely, falls short of, or comparison to a claim the program never made. | Principal: "What does this mean 'weaker'???? We just need to know how it works." | DEFINED | `TSV:107`; `SL:71`; `REG:6149-6160` |
| **D-10** | A verification with no failing branch is an instrument check, not a result. | A verification whose negation would be a contradiction in terms ("threshold = d"). | PF-6; F-24 withdrawn | DEFINED | `TSV:112`; `SL:72`; `REG:6312` |
| **D-11** | A criterion validated only on the cases it was derived from is not validated. | A criterion whose test set is the set that suggested it. | G-16 fitted on weight-2, failed on weight-4; F-25 λ^2d → λ^2n* | DEFINED | `TSV:134`; `SL:73` |
| **D-12** | A complex redrawn as non-manifold need not be a different quantum system; only a face that changes the stabiliser group changes the carrier. | A "second carrier" whose stabiliser group is not checked against the first. | T-8 duplicated plaquette | DEFINED | `TSV:136`; `SL:74` |
| **D-13** | Alpha names a magnitude, not a constant (generic coupling; connecting it to the fine-structure constant would be an import). | — | T-10 | **WITHDRAWN** 2026-09-15: superseded by the two-alpha vocabulary split and A-AL2 (physical alpha connected conditionally via same-sector inheritance; numerical selection open). The generic corner magnitude remains non-numerical. | `TSV:142`; `SL:75` |
| **D-14** | A zero is only a result if it is a zero of the object the question names. State which object the question asked about and check it is the one measured. | A null answering a question whose nouns do not appear in the measurement. | T-6 composition zero read as flatness; writer-commutator zero read as no curvature | DEFINED | `TSV:159`; `SL:76`; `REG:7758-7760` |

**D-15 … D-27 (also standing; one line each, read the row):** D-15 carry the control in the same table (`SL:77`); D-16 separate site-blind from site-bound before reading a suppression (`SL:78`); D-17 vary the venue's own scale before calling an effect new (`SL:79`); D-18 a record is a logical operator, a flux is an excitation (`SL:80`); D-19 F₂ cannot pose the question of sign; compute over the integers when accumulation vs cancellation matters (`SL:81`); D-20 a short-range fit does not establish an asymptotic law; prefer out-of-sample prediction; report when the data cannot decide (`SL:82`); D-21 sampling-capped commutants silently return short bases (`SL:83`); D-22 a permutation-symmetric carrier contains no geometry to detect; separation nulls there mean "these carriers have no geometry" (`SL:84`); D-23 results depending on a low-dimensional convention are scoped to the proxy (`SL:85`); **D-24 each classical concept must earn its place** (energy, entropy, distance, field, exponent; a concept appears in no claim, test or READ until the record surface exhibits it unassumed; no falloff exponent has been earned) (`SL:86`); **D-25 the model is grounded in real record data, never the toy category** (`SL:87`); D-26 the model is named URM, a title not a claim (`SL:88`); D-27 two readings of "protected" diverge on non-abelian carriers; name the reading (`SL:89`).

Also binding: X-6 withdrawn (identity question is an import, `TSV:28`); X-2 record-level reclassification stands, the collective question is open (`TSV:24`); F-0 the program had no formation step (`SL:65`).

---

## 8. Forbidden moves (consolidated; each tied to its source)

1. **Inferring anything about Γ from the word "gravity"**, or demanding of Γ anything because gravity has it. `PW/THIRD_TERM_V001.md:9-17`; D-2.
2. **Using a classical quantity as a test the record level must pass**, including the banned comparisons: inverse-square / r⁻², 1/r potential, G, a metric, a geodesic, the Einstein equations, "gravity needs …", or "the record-level quantity should be shaped like gravity". `PW/CORE_FRAMEWORK_V001.md:14-21`; D-1.
3. **Requiring a falloff exponent** of a record-level source (the exponent belongs to the emergent description). `PW/CORE_FRAMEWORK_V001.md:23-26`; D-24 (no exponent earned).
4. **Reading a classical-shaped null as a loss.** It reads two ways (different-shape hypothesis, or no gravity present); same-function/different-shape is an assumption with no falsifier yet, never a baseline. `PW/CORE_FRAMEWORK_V001.md:28-29`.
5. **Claiming identity of Γ and gravity at the record level** (X-6, withdrawn as an import), or treating H₁(Σ) as the definition of Γ. `REG:6747-6748`; `PW/THIRD_TERM_V001.md:39-45`.
6. **Asking a frozen parent's dynamics to produce its own permissions** (scoped D-4); treating occupancy as selection; treating host-sector REQUIRE as a production operator; asserting carrier formation without the five Corollary 5.4 objects. `SR/FORMAL_SCOPE_THEOREM.md:158-162, 184-186, 220-230, 333-344`.
7. **Reading Boolean projector commutation as spacetime/Poincaré/Virasoro closure**, or rescaling an exact finite zero into an anomaly. `SR/FORMAL_SCOPE_THEOREM.md:423-444`.
8. **Assigning EM a value, density or strength at a place** at the record level. D-5.
9. **Excluding formation from an ensemble average** without a single-run warrant. D-6.
10. **Checks that cannot fail; verdicts without a noise floor; verifications with no failing branch; criteria tested only on their fitting set; nulls of the wrong object.** D-8, D-10, D-11, D-14.
11. **Grading a result against an external standard** ("weaker", "only", "merely"). D-9.
12. **Letting alpha select structure** (choosing a construction because it lands on a known value; inserting a measured number and reading off consequences). `PW/CUSTODY_V001.md:57-63`. Also: calling any of the three alphas by another's name (§3.7).
13. **Using a concept at the record level before it has earned its place.** D-24. **Working in the toy category.** D-25.
14. **(Current, principal 2026-10-12) Load-bearing classical machinery in the native chain:** Coulomb/Gaussian Maxwell phase, Gauss-law fields and 1/r² profiles; Debye/RPA screening; Poisson and Einstein equations; Newtonian orbits (v² = r·g); a Euclidean embedding or continuum chart; thermal/Gibbs states; QSI/QMC phase evidence; elasticity and displacement fields. These may appear only as labelled conditional diagnostics; any load-bearing use is a declaration to the principal. `TO/0100:7-19`. Retired framings: the one-metric / 3+1 template as geometry criterion; SPARC Newtonian velocity templates as the baryonic source; "kernel → potential → additive correction" orbit stage; Maxwell-derived light; 3D-shell range tests. `TO/0102:10-15`.
15. **Treating a blank-Record state as a physical region** ("empty space"). `TO/0082:7-9`; S1.
16. **Reporting a single-carrier or single-Record result as a gravity verdict.** `TO/0109:7`.
17. **Adding a separate gravity source law** and treating its response as the gravity verdict. `TO/0077:8`.
18. **Starting a term from scratch** (from the Hamiltonian) without a prior-work ledger citing REG/TSV results that the work builds on, ports, contradicts or supersedes. `TO/0110:15`; `TO/0111:6-8`.
19. **Defaulting to standard-physics framings** ("single-object footprints, fields falling with distance, Coulomb/Maxwell channels, metric pass tests, Newtonian inputs"); the principal calls this a framing error. `TO/0112:14`.
20. **Closing a route without naming the next step it forces.** `PW/PRINCIPAL_ACT_001_DRAFT.md:98-102`.
21. **Quietly adopting** a premise, dictionary or value (e.g. matter-Record identity in #7, a background density). Register mismatches; a declaration goes to the principal. `TO/0080:15`; `TO/0083:11`; `TO/0084:4`; `C7/CANONICAL_MODEL_7_PROPOSAL_V005.txt:32`.

---

## 9. What IS allowed or required (the positive principles)

- **Requirements on a record-level source are about accumulation, not shape:** extensive, additive over disjoint regions, not a mere count, sign-definite so it accumulates rather than screens. `PW/CORE_FRAMEWORK_V001.md:23-25`. (D-24 notes additivity was earned by an exact-zero defect and sign-definiteness by the act of writing, `SL:86`.)
- **A classical quantity may be computed and reported as a relationship** carrying no verdict, and the classical form may be used to say what a positive result would MEAN, never as the criterion. `TSV:36`; `REG:4955-4962, 7351`.
- **Emergence as identification between levels of description is permitted** (it does not ask what produces a permission). `REG:6755-6759`. Progress on emergence = a collective quantity built from many records, shown to obey something constraint-like, without importing the constraint. `REG:6776-6782`; `PLAN:17`.
- **Every outcome registers**, including "no profile", "no difference beyond contact", or non-classical forms. `TO/0077:10`; `TO/0080:9`; `TO/0100:25`.
- **Record-filled backgrounds and differences:** gravity needs a difference relative to the same Record-filled background (with-matter minus sham). `TO/0080:9-13`.
- **Collective, many-body, finite-density, coarse-grained quantities are the target.** `TO/0109:7-12`; principal H-9: "Several make PATH COMPARISON possible" `REG:7339-7340`.
- **Build-and-audit:** every build paired with a default-refute audit; same-lineage pairing is adversarial in prompt only; findings graded adversarially-checked unless independent lineage exists. `PW/CUSTODY_V001.md:44-53`. Exchange rule: never consume an unreviewed output; never self-review; cross-lineage review preferred. `X/README.md` "Additional agents" item 4.
- **Pointer rule:** no term enters a governing clause without a digest, `file:line` or named ruling. `PW/CUSTODY_V001.md:7-19`; `REG:13-14`.
- **Progress metric:** constructions completed, never questions closed. `PW/CUSTODY_V001.md:70-73`.
- **Frame challenge on route decisions:** run the NULL OPTION first (does either branch obtain?); embedding test needs exclusion, relevance, provenance. Adopted by R-2. `PW/FRAME_CHALLENGE_V002.md:11-30`; `PW/PRINCIPAL_ACT_001_DRAFT.md:69-74`.
- **Prior-work ledger in every packet; write accepted results back to REG and TSV** (root owns those writes). `TO/0110:15`; `TO/0111:6-21`.

---

## 10. Discrepancies and uncertainties found (registered here, not resolved)

1. **T-20 status reads differently by date.** `PW/THIRD_TERM_V001.md:72-73` and `PW/GLOSSARY.md:124-125` say recovery of classical gravity from accumulated Γ is "untouched"; `PLAN:17` marks T-20 DONE; `REG:7371-7464` shows it ran (flat null) and its interpretation was withdrawn by O-23; `TO/0110:11` says it was "reread into C-77"; C-77 remains CANDIDATE with a member-level match only (`TSV:248`). Safe reading: the T-20 task was executed; the claim "classical gravity is recovered from accumulated Γ" is NOT established. Lanes should cite C-77's current row, not either summary alone.
2. **Γ uniqueness:** THIRD_TERM poses it as the sharpest open question (`:47-60`); G-6 later records "UNIQUENESS IS BROKEN" (`REG:5173-5200`). Lanes should treat Γ as not unique (topology sufficient, not shown necessary), with the non-abelian/non-CSS/fracton regions untested.
3. **"Closed" theory vs conditional premises.** The closure theorem's "closed … by exact typed composition" (`PW/UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md:289-299`) depends on adopted U-DCL, ARGER Gate, LL-P, RGRL and WTC-H1…H5 (with G calibrated to G_obs). Root README, LADDER and ADOPTION_LOG qualify it (§2.4). Do not cite UNT-CLOSURE as a native derivation of gravity.
4. **Which object is "the record" for gravity.** Charter records (DEF-A/O-51, R2/R3 non-local writer and protection) vs canonical V005 local q Records written and erased by local Bind. Registered as a possible premise conflict; principal's call. `TO/0106:13, 19`.
5. **S1 vs the canonical rules.** S1 (no empty space) is a declared state premise; the canonical generator still admits blank states and inserts blank q/I factors at Birth; "matter and space are made of Records" does not identify p with q. Open checks. `C7/CANONICAL_MODEL_7_PROPOSAL_V005.txt:28-32`.
6. **Document force.** `PW/PRINCIPAL_ACT_001_DRAFT.md:1-4` is headed "DRAFT, UNAFFIRMED", while its table records R-1…R-4 as AFFIRMED by session instruction (`:26-31, 130-140`), explicitly not a cryptographic act (`:11-16`). `PW/FOUNDING_DESIGN_V001.md:3` reads "PROPOSED, NOT ADOPTED", but §1 target and §2 alpha-as-input survive as the principal's standing intent under R-3 (`PRINCIPAL_ACT:83-89`); its §3-§5 are logged as attempt one with no force (`:91-96`). `PW/FRAME_CHALLENGE_V002.md:3` likewise reads "PROPOSED, NOT ADOPTED" but is adopted by R-2 (`PRINCIPAL_ACT:69-72`).
7. **Historical claim wording.** `PW/THE_CLAIM_V001.md:28-33` ("GRAVITY — as the topology of the space — supplies …") and `PW/CORE_FRAMEWORK_V001.md:186-193` ("A quantum record is a topologically protected degeneracy of a gauge field …") predate the function-only Γ, the identity withdrawal and O-51; THE_CLAIM is marked superseded for the process description (`:1-2`). Read them as the DEF-A-corner, historical form of the claim.
8. **"Admissible/admission" names at least five different objects** (§3.4). The canonical admission operator is unrelated to the type-theoretic admissibility predicate and to DEF-A's admissible unitary.
9. **"Alpha" names three different objects** (§3.7). The formation-activity coefficient a_v^adm is explicitly not EM alpha.
10. **Source layer of the current premises.** The 2026-10-12 premises in §2.5 are Claude's relays in TO_CODEX, quoting the principal; some are registered into program artifacts (S1 in `C7/CANONICAL_MODEL_7_PROPOSAL_V005.txt:25-34`), others are scheduled for write-back to REG/TSV (`TO/0111:18`). I did not find them in REG/TSV as of this reading.
11. **Generated vs source ledger.** `SL` (generated) and `TSV` (truth) matched for every row checked here (D-1, D-4, D-5, D-13, D-14, O-51); `SL` was last generated 2026-09-30. Treat TSV as authoritative.
12. **The legacy alias path** `/Users/bgm/Documents/ChatGPT/Universal Network Theory` appears in older artifacts; the canonical root is `/Users/bgm/Research/Universal Network Theory`. `U/CURRENT_STATE.md:13`; `U/UNT_FRESH_CHAT_HANDOFF_2026-10-12_V001.md:5-6`.

---

## 11. Sources read for these notes

Read in full: `PW/THIRD_TERM_V001.md` (78 lines); `PW/CORE_FRAMEWORK_V001.md` (219); `PW/GLOSSARY.md` (142); `PW/README.md` (162); `PW/FOUNDING_DESIGN_V001.md` (133); `PW/CUSTODY_V001.md` (86); `PW/INHERITED_FROM_THE_PREDECESSOR.md` (34); `PW/FRAME_CHALLENGE_V002.md` (51); `PW/THE_CLAIM_V001.md` (94); `PW/THE_CLAIMS_V001.md` (37); `PW/UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md` (299); `PW/nomenclature/BIND_BIRTH_POLICY.md` (55); `SR/RESULT.md`, `SR/FORMAL_SCOPE_THEOREM.md`, `SR/ERRATUM_2026-09-06.md`; `U/README.md`; `U/UNT_FRESH_CHAT_HANDOFF_2026-10-12_V001.md`; `C7/CANONICAL_MODEL_7_PROPOSAL_V001…V005.txt`; `TO/0005, 0027, 0077, 0080, 0082, 0083, 0084, 0100, 0102, 0106, 0108, 0109, 0110, 0111, 0112`; `X/README.md`, `X/STANDING_ORDER.md`.

Read in part: `PW/PRINCIPAL_ACT_001_DRAFT.md:1-140`; `PW/HANDOFF_2026-08-17.md:1-60`; `PW/RECORD_FORMATION_V001.md:1-56`; `PW/ALPHA_PROGRAM_PROVENANCE_2026-09-15.md:1-140`; `PW/GRAVITY_DEFINED_V001.md:1-25`; `SL:1-105` plus rows 187, 207, 225, 292, 306, 310; `TSV` rows cited; `PLAN` rows 17, 18, 43; `REG` sections at 1-60, 2028-2036, 2423-2440, 4945-5000, 5173-5200, 5218-5262, 5488-5520, 6149-6165, 6740-6845, 7325-7470, 7750-7775, 9119-9240, 9539-9590; `SRA/INDEPENDENT_HOSTILE_AUDIT.md` verdict lines, `SRA/MECHANICAL_AUDIT_RESULT.json`; `U/CURRENT_STATE.md` lines 1-140, 252-256, 375-405 and a keyword sweep; `U/LADDER.md:1-120`; `U/ADOPTION_LOG.md:1-20, 126`.

Not read (out of scope for this pass; other lanes should consult as needed): `PW/PROOF_V001.md`, `PW/PROOF_V002.md`, `PW/THE_ROAD_V001.md`, `PW/STATUS_V001.md`, `PW/PLAN_TO_PROOF_V001.md`, `PW/TERRITORY_MAP_V001.md` beyond line 8, the RGRL/WTC gravity theorem files, `PW/LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/`, `PW/LANE_RFT_AXIOMATIC_URFT_CLOSURE_V001/`, `U/FRONTIER_INDEX.md`, the dark-sector frontier/ledger series, `X/PLAN.md`, `X/STATUS.md`, FROM_CODEX outboxes, and `X/claude_artifacts/program_grounding/`.
