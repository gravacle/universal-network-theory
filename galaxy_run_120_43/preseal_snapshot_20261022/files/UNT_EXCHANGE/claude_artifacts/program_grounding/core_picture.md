# Core picture: framework definitions and the gravity-emergence account (read-only extraction)

Date: 2026-10-12. Every statement below is taken from the program files and cites them by path and
line. Nothing in the program tree was executed or modified. No classical gravitational form is used
here as a test; where a program file compares to one, this summary says so and quotes the file's own
label for it.

Path abbreviations:

- `PW` = `/Users/bgm/Research/Universal Network Theory/program-worktree`
- `CF` = `PW/CORE_FRAMEWORK_V001.md` (219 lines)
- `TT` = `PW/THIRD_TERM_V001.md` (78 lines)
- `GF` = `PW/GRAVITY_FORMATION_CURRENT_PICTURE_V001.md` (4382 lines)
- `RG` = `PW/REGISTER_V001.md` (11220 lines)
- `SL:n` = line n of `PW/ledger/status_ledger.tsv` (header is line 1; columns ID, AREA, ITEM, STATUS, EVIDENCE, BLOCKED_BY, REFUTED_BY, GROUNDED)
- `SLMD:n` = line n of `PW/STATUS_LEDGER_V001.md` (generated from the TSV)
- `PL:n` = line n of `PW/ledger/plan.tsv`
- `AR/` = `PW/DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/`

---

## 0. The grounding fact that matters most

The program tree holds **two gravity lineages**, and its largest "current picture" document does not
cite the third-term Γ at all.

1. **The Γ / C-77 lineage (third term, boundary structure).** This is `CF` + `TT` + register entries
   C-77…C-93 + plan tasks T-20, T-42…T-51. Most of it dates to 2026-08-18…08-21. Here Γ is the
   third term defined by function (R1–R3, `TT:21-31`). The emergence claim is that Γ's
   **boundary-shaping aggregate at scale** appears as geometry (C-77, `RG:9543-9546`).
2. **The RFT/MGFT/F3 lineage (`GF`).** `GF` is V001, dated 2026-08-27 (`GF:3-5`), and later entries
   were appended into late September (`GF:1289-1392`). Its "gamma" is a lower-case **γ**, a
   fidelity/distinguishability quantity: `γ_Q`, `γ_IF`, `γ_state`, with `I_γ = −log γ_Q`
   (`GF:1527-1542`). The capital Γ appears only as an unconstructed "physical record-sealing rate"
   (`GF:1647-1652`) and as `Γ_IR` (`GF:1987`).

A grep of `GF` finds **zero** occurrences of `C-7x`, `C-8x`, `C-9x`, `A-GR`, `THIRD`, `R1`,
`boundary-shaping`, `DEF-A`, `O-51`, `D-1`, `D-24`, `T-49`, `T-51`, `O-58`, `mu_c`, and
`interface rank`. It finds one "Poisson" (run 2026-10-12 against the files as they stand). The two
lineages do share the ALLOW/REQUIRE vocabulary (`GF:210, 271, 425, 2338-2341`) and the principle
that no classical field sits on a single record (`CF:14-16`; `GF:3961-3981`).

A lane "grounded in the previous work" therefore has to name which lineage it continues. Sections
5 and 6 list what each lineage says must be computed next.

---

## 1. CORE_FRAMEWORK_V001: the anchor

`CF:3-4`: "THIS IS THE PROGRAM'S ANCHOR"; it is amended only by a registered erratum.

### 1.1 What the record level is NOT measured against (`CF:8-33`)
- The principal (`CF:10-12`) wants to connect Γ with classical gravity via emergence from records,
  **not** to equate Γ and gravity at the record level. "Γ is where gravity comes from."
- `CF:14-16`: classical gravity is not expected at the record level and is never the test. The
  claim is emergence at scale, so the record level should NOT resemble the emergent form.
- Banned comparisons at the record level (`CF:18-21`): an inverse-square law, `r⁻²`, a `1/r`
  potential, `G`, a metric, a geodesic, the Einstein equations, "gravity needs …", and "the
  record-level quantity should be shaped like gravity".
- What a record-level **source** may be required to be (`CF:23-26`): extensive, additive over
  disjoint regions, not a mere count, and **sign-definite so it accumulates rather than screens**.
  "A falloff EXPONENT IS NOT AMONG THEM."
- A classical-shaped null reads two ways (`CF:28-29`): the different-shape hypothesis, or no
  gravity present.
- `replicate/on_finding.sh` scans findings for banned comparisons (`CF:31-33`).

### 1.2 What "PROOF" means (`CF:37-57`)
- A row is `PROVED` only if it names (1) a measurable quantity with units, (2) the predicted value
  or relation, (3) a falsifier, and (4) `RECORDS VERIFIED:` on at least **two structurally
  different** real record surfaces. "Different MECHANISM, not different parameters"
  (`CF:48-53`); `ledger/status.py` enforces this.
- A result about the five clauses is `FORMAL`, not `PROVED` (`CF:55-57`; H-3).

### 1.3 O-51: the amended definition with finite tolerance (`CF:61-94`; SL:233)
- Why it changed: about 20 real records were tested (HDD, flash, MRAM, DNA, zircon, ice core, and
  others), and **zero satisfy the exact clauses**. The exact clauses describe a passive
  self-correcting quantum memory (`CF:63-67`). The world uses **energetic/kinetic** protection;
  the exact clauses assume **topological** protection (`CF:69-71`).
- The one move: the clauses are restated from the **carrier alone** onto **carrier ⊗ local bath**,
  with declared tolerances `(T, t_m, δ, t_w, Δ, W, N_r)` (`CF:73-74`).
- The amended clauses (`CF:76-82`):
  - (i′) a commuting spectral family `{P_a}`.
  - (ii′) durable to `t_m`, with width `δ = ħ/t_m`.
  - (iii′) non-constant on the closed system's energy shell, of width `√(C_v k_B T²)`.
  - (iv′) writable by an energy-conserving **dilation unitary** on carrier ⊗ writer ⊗ bath. The
    cost is free energy, with floor `kT ln2 + ΔE_config`.
  - (v′) every single-region flip costs `≥ E_b`, with `E_b/kT ≫ 1`.
- All ~20 records pass (`CF:84`).
- **DEF-A is the exact corner** `T→0, t_m→∞, W=0, E_b→∞` (`CF:86-89`). All FORMAL rows remain
  theorems about that corner, and the world has "approximately zero residents there".
- The H-6 by-product: records are macroscopic because a macroscopic bath must export the write
  energy (`CF:91-92`).
- SL:233 adds that O-51 converts H-3, H-5, and H-6 into standing acceptance criteria.

### 1.4 DEF-A: the exact corner (`CF:96-150`)
- `R` is a record if (`CF:98-106`):
  - (i) `R=R†, R²=I`
  - (ii) `[H,R]=0` and `[L_k,R]=0`
  - (iii) `R` is non-constant on some eigenspace of `H`
  - (iv) some **admissible** `U` has `U†RU=−R`
  - (v) no admissible operation on a **single** contractible region does so
- "Alpha" in this file is a generic coupling magnitude, not the fine-structure constant
  (`CF:108-112`).
- Admissible `U` ≝ `[U,H]=0` (O-4, provisional). (iv) ⟺ `Tr(P_E R)=0` on every eigenspace
  (`CF:114-117`).
- Erratum to (v) (`CF:119-124`): without "admissible", (v) is false on the toric code. With it,
  (v) holds exactly.
- The "contractible" convention (`CF:126-141`): 1D rings use the proper-subregion convention and
  are a boundary-constrained proxy. **The toric code is the canonical benchmark**, where (v) is
  manifold homology.
- `CF:152-159` verifies that the definition discriminates.

### 1.5 Propositions and the claim (`CF:163-193`)
- P-1: (iii) ⟹ `H` is degenerate.
- P-2: the writer is built from neither `H` nor `{L_k}`.
- P-3: no admissible writer fits inside one contractible region. The minimum admissible writer is
  a product of `d` individually inadmissible single-edge operators, "admissible only as a whole"
  (`CF:171-182`).
- The claim (`CF:188-190`): a quantum record is a topologically protected degeneracy of a gauge
  field.
- Obstructions O1–O5 and X1–X4 are at `CF:197-219`. X2 (`CF:214`): matter-response at the record
  level was withdrawn as a D-1 import. The live collective questions are `H-1`/`C-77` and the
  conditional `F-3`/`T-II.5`/`H-7`.

---

## 2. THIRD_TERM_V001: Γ by function

- "Gravity" is permitted as a **label** for Γ. Inference from the label is forbidden
  (`TT:5-14`, D-2).
- **Γ is whatever satisfies all three requirements** (`TT:21-31`):
  - **R1 SPACE**: a set of record states of size > 1 that distinguishes states of the same energy
    (clause iii).
  - **R2 WRITER**: a flip that no local operation can mimic (clauses iv+v, P-3).
  - **R3 PROTECTION**: no local operation writes or destroys the record (clause v).
- `(H₁(Σ), ⟨·,·⟩)` is a **candidate**, not a definition (`TT:39-45`; Thms A–C).
- Uniqueness (`TT:47-60`) is **FAILED** at SL:41 (G-6). The breaking examples are qLDPC, the 3D
  toric code, and arbitrary F₂ complexes. So by `TT:56-58`, topology is sufficient but not
  necessary: "records admit", not "records require".
- The claim (`TT:62-70`): not that Γ **is** gravity at the record level (X-6 withdrawn), and not
  that it resembles gravity, but that "gravity COMES FROM Γ". Classical gravity is what Γ becomes
  at scale.
- `TT:72-73`: "The recovery of classical gravity from accumulated Γ is untouched — plan task T-20."
  That sentence was later overtaken by T-20 DONE (PL:17) and by the T-21 note on X-2 (SL:24;
  `RG:9606-9608`): "the collective question it never touched now lives in C-77/T-42."

---

## 3. ALLOW / REQUIRE / SELECT

- The governing definitions (`AR/ERRATUM_2026-09-06.md:23-28`):
  - `ALLOW_P(v=a)` = membership in the attainable set of a declared parent.
  - `REQUIRE_P(φ)` = a universal statement over that parent's nonempty admissible set. For a
    numerical value it is a singleton theorem.
  - `SELECT_{P,D,μ0}(v=a)` = a separately supplied dynamical explanation of which allowed
    occupancy becomes actual.
  - "None of these English labels creates an operator."
- Frozen parent vs enlarged parent (`AR/ERRATUM_2026-09-06.md:30-36`; `AR/RESULT.md:10-18`):
  - On a frozen parent, admissibility-preserving dynamics changes **occupancy**, not permissions.
  - An enlarged parent with dynamical carrier labels and owned inter-fiber transitions can change a
    subsystem's effective fiber.
  - That route is a logical reopening only; no physical enlarged parent is constructed.
- Superseded wording (`AR/ERRATUM_2026-09-06.md:5-9`): "every level only ALLOW / REQUIRE at no
  level / Einstein's equations are wholly constraints". The ADM overclaim was corrected with an
  external source (`:11-19`).
- D-4 (SL:58) is narrowed to the frozen parent. G-3 (SL:16) keeps only the frozen-parent "Γ
  supplies an ALLOW/capacity predicate". F-3 (SL:54) and H-7 (SL:132) reopen conditionally, and
  only once a complete enlarged physical parent exists.
- The alpha ladder (SL:273, A-AL2) is the repository precedent for the three levels.
- ARGER is named as the full process `ALLOW -> REQUIRE -> GATE -> EM -> RECORD` (`RG:11016-11019`;
  SL:281).
- A-GR3 (SL:245): Γ is the common structure that **ALLOWS** records on a frozen parent and is
  proposed to appear at scale as geometry. The classical relation is a recovery target at scale
  only (D-1).

---

## 4. Doctrine rules D-1 … D-14 (SL rows; display at `SLMD:62-76`)

| ID | SL | rule (abridged, verbatim where quoted) |
|---|---|---|
| D-1 | 36 | "NO CLASSICAL MEASURE MAY BE APPLIED TO THE RECORD LEVEL AS A CRITERION." A classical quantity may be computed and reported as a relationship, never the test. A falsifier of the form "our object fails to exhibit <classical feature>" is void. |
| D-2 | 37 | The name is the import vector. "Gravity" is a label; no attribute transfers through the name. |
| D-3 | 38 | A rescue is always downstream of an import. Remove the import, not the symptom. |
| D-4 | 58 | ALLOW/REQUIRE/SELECT is a type discipline, scoped to the frozen parent/fixed fiber (see §3). |
| D-5 | 71 | At the record level EM has no local content (no field strength at a point). |
| D-6 | 76 | The ensemble instrument is blind to record formation. `<R>=Tr(Rρ)`-based negatives are void without a single-run warrant (W-35: 78.5% definite runs, same ρ(t)). |
| D-7 | 77 | An assumption that lives only in prose will be re-made, so every uncleared assumption gets a row. |
| D-8 | 84 | A check that cannot fail is not a check. A computed verdict needs its noise floor measured alongside it. |
| D-9 | 107 | Describe results by mechanism, never ranked against an external standard (tells: "weaker", "only", "merely"). |
| D-10 | 112 | A verification with no failing branch is an instrument check, not a result. |
| D-11 | 134 | A criterion validated only on the cases it was derived from is not validated. |
| D-12 | 136 | A redrawn complex is not a new carrier unless the stabiliser group changes. |
| D-13 | 142 | WITHDRAWN (alpha as magnitude), superseded by A-AL2. |
| D-14 | 159 | "A ZERO IS ONLY A RESULT IF IT IS A ZERO OF THE OBJECT THE QUESTION NAMES." |

Later rules that bind any gravity lane:
- D-22 (SL:210): a permutation-symmetric carrier contains no geometry to detect, so verify that
  the carrier admits a separation before reading a separation null.
- D-23 (SL:230): low-dimensional conventions scope results to the proxy.
- D-24 (SL:246): each classical concept must **earn** its place (distance was earned at C-78; "no
  falloff exponent has been earned by anything").
- D-25 (SL:259): grounded in real record data, never the toy category.

---

## 5. Lineage A: how classical gravity is to emerge from accumulated Γ (C-77 line)

### 5.1 The adopted claim
- A-GR2 (SL:123): "classical gravity is what Gamma becomes at scale". EM supplies the
  complex/carrier/record, Γ decides which couplings form one, and alpha sets the cost.
- A-GR4 (SL:247): "emerge from terms like Gamma that SHAPE GEOMETRY AND BOUNDARIES". In the corner,
  Γ is boundary structure (`Z_1/B_1`, G-9 SL:44; total at the boundary, G-8 SL:43). In the world,
  protection is basin boundaries `E_b`. The Γ-side variable is a **boundary-structure measure** in
  the record surface's own terms.
- **C-77, adopted** (`RG:9541-9551`; SL:248 CANDIDATE): "The structure Γ that allows a record — by
  shaping the boundaries that make a bit non-losable … — is the same structure whose aggregate at
  scale appears as geometry."
  - Fail condition: every derivation requires assuming the classical form, or yields incompatible
    relations.
  - **Openness clause** (`RG:9559-9563`): Γ is the named contributor, not the only one. A
    derivation that succeeds through additional terms satisfies the claim.

### 5.2 The increments and their constructions (all FORMAL unless stated)

| step | construction / quantity | result | cite |
|---|---|---|---|
| Distance (C-78) | `d_W(s,s')` = minimal weight of an admissible operation from configuration s to s' | A true metric. On the torus it equals the minimal crossings of the transverse loops. The crossing form `J` is not a metric, but `J mod 2` = symplectic pairing = channel adjacency. Dimension is earned as content degree (2 corner, 3 world). | SL:249; `RG:9614-9622` |
| Boundary-degree law (C-79, CANDIDATE) | interface rank `IR` vs content `C` | `deg IR = deg C − 1` in both tiers, with parameter-free forms `32·capP=(IR2+10)²+8(IR2+10)−160` and `IFACE³=216·CAP²`. Mechanism: Euler bulk cancellation `1+1−2=0`. Stored content is **volume**; the coefficient depends on venue (32 vs 216). | SL:250; `RG:9624-9640` |
| Pure-Γ two-region relations (C-80) | `I_IR`, `I_MI` vs earned separation | **Zero beyond contact** (not decaying), plus contact seams, topological constants, and one growing law `w_min = d` (confinement). "THE FALLOFF ENTERS ONLY THROUGH THE DECLARED COUPLING TERM." Division of labor: Γ = boundaries, coupling = reach/falloff, alpha = costs. | SL:254; `RG:9674-9708` |
| Certifiability (C-81/82/83) | externally certifiable content `CERT` | Corner: `CERT = 8s−10` = cut-rank (boundary degree); `HIDDEN = STORED − CERT` is volume. World: `CERT_W(n)=min(n³, W·(6n²−12n+8))`, with `W = τ/t_epoch` fixed by `t_m`. Boundary-bounded at scale; `W=∞` is the DEF-A corner. | SL:255-257; rule at `RG:9658-9670` |
| **Γ-priced kernel** (C-87) | `G_μ(d) = Σ_{admissible strings} μ^{weight}`, strings priced by Γ at `w_min = d` | Three classes: exponential (`μ<μ_c`, leading `N_min μ^d`); critical at `μ_c = 1/deg`, where "the gated resolvent identity at criticality IS the venue's discrete Poisson equation"; divergent above. | SL:264; `RG:9854-9861` |
| Composition (C-88) | admissibility rule R1 (endpoint-transparent) vs R2 (opaque); encoding occupancy vs orientation | Superposition is a property of the admissibility rule. The mediator kernel is positive, so **occupancy accumulates and orientation screens**. The one-signed, unscreened, unshadowed profile occurs only at **R1 + occupancy**. Whether the surface enforces that point is open (N3). | SL:265; `RG:9863-9870` |
| D=3 member (C-90) | the same kernel on the census grain lattice (deg 6) | `μ_c = 1/6` exact; at criticality a power law with exponent bracket containing 1, and `d·G(d) → [0.476,0.487]`. Owner comparison (Watson, 3/(2π)) is made "after class". **SINGLE-CARRIER** (`RG:10367-10371`). Norm selection is open. "NOTHING in Gamma yet places μ at criticality." | SL:269 |
| Masslessness (C-91) | invariant kernel `K = cI + tA`; ensembles E1/E2/E3 | Measure conservation ⟺ criticality (`det(I−K)=0`). E1 transport is critical at every dE. E3 trail-with-decay is never critical, with mass gap `ln(μ_c/μ) = ln(1 + e^{dE/kT}/l)`. "Bias is mass." The antecedent (does GR3 writing conserve measure?) is **one computable bit, not discharged**. | SL:270; `RG:10052-10080` |
| Field side (C-92, DEFINED) | Second Lump: `F(D) = Δ(b=−1;D) − Δ(b=+1;D)`, the written-value differential of a probe record's own splitting at earned separation `(d_gen, connected w_enc)` | Instrument identified; **no field measured**. The principal's correction (`RG:10347-10358`): "The mechanism for accumulation is whatever it proves to be". Composition runs first, and every outcome registers as the surface's own law. | SL:271; `RG:10292-10358` |
| Rigidity (C-93) | `d_W` and the class landscape on stabiliser venues | The integer tier carries no field; the response "lives one tier down". **Named responsive venue**: "does one written record shift dE for an adjacent write in the E1/E2/E3 writing tier?" | SL:272; `RG:10392-10421` |
| T-51 status | the C-92 first computation `LANE_T51_A` | The quarantine correction makes the old all-pass inadmissible. V1–V5 are unscored, so neither terminal branch fires. **T-51 remains TODO.** A future field law needs a fresh prospective instrument and independent verification. | `RG:10797-10867`; PL:52 |

The C-77 row (SL:248) states its verdict as "NEWTON VERDICT: MATCHES AT MEMBER LEVEL … Never a claim
that continuum or Einstein gravity is empirically derived." Under D-1 the comparison is reported as a
relationship after computation ("comparison only after class", SL:269), not used as a test.

### 5.3 Holonomy branch (H-9 / T-20)
- H-9 (SL:144) defines the criterion as record-level holonomy, `H_ABCD = (G_AB G_BD)(G_AC G_CD)^-1`.
- The T-20 run found exactly flat holonomy on abelian carriers (`RG:7371-7403`).
- O-23 (`RG:7430-7464`; SL:146 FAILED) then showed the connection is **not determined by the
  records**: admissible writers give holonomy 0 or 5.17 on the same record family. The open
  question is "WHAT DETERMINES THE CONNECTION?", carried as O-24 (SL:148; minimality as a candidate).

### 5.4 What lineage A says must still be computed
1. **T-49** (PL:50, TODO): the conservation bit of one GR3 writing event, i.e. which ensemble
   (E1/E2/E3) Γ's actual writing enforces. Deciding it decides masslessness. Companions: the
   anisotropy frontier (N5), link indistinguishability forcing a symmetric weight measure, and E2's
   decay class at dE ≠ 0.
2. **The C-93 responsive venue** (SL:272): the dE shift of an adjacent write caused by one written
   record, on the metastable/world tier.
3. **T-51** (PL:52): the field-side observable `F(D)` against an unwritten control, done with
   fresh prospective design and independent verification (`RG:10863-10867`).
4. **A second D=3 venue for C-90** (`RG:10387-10388`).
5. **O-58 N3/N4/N5** (SL:266): the design point (R1 + occupancy), the norm selection, and the
   anisotropy frontier.
6. **O-55** (SL:252), universal coefficient; **O-56** (SL:253), an earned thermodynamic conjugate
   pair; **O-57** (SL:258), the emergent content bound or "collapse analogue": HIDDEN content made
   unstable by a dynamics that must *emerge*, not be imposed.
7. **O-52** (SL:235): the energy route to a source reopened under (iv′), "dE is measurable, non-zero
   and record-by-record". **O-53** (SL:242): an extensive durable operator whose
   configuration-dependent part does not cancel.
8. **T-50** (PL:51): a baseline-free observable for the occupancy law (C-72 is PARTIAL, SL:239).

---

## 6. Lineage B: GRAVITY_FORMATION_CURRENT_PICTURE_V001 (γ, collective phase, scale)

### 6.1 What "gamma" means there
- There are three noninterchangeable objects (`GF:1527-1542`):
  - `γ_Q`, complete-query record gamma, with the seed `D_TV ≥ B_rec > 0 ⟹ I_γ = −log γ_Q > 0`.
  - `γ_IF`, influence gamma, used in the KMS response theorem.
  - `γ_state`, squared Uhlmann fidelity, which gives QFI.
- `γ_state` gives an information semimetric (`GF:1544-1556`). There is "no universal map
  γ ↦ g_μν, causal order, or gravity dynamics" (`GF:1588-1598`).
- Γ, the sealing rate, "must be constructed from a declared process … accumulated fragment/channel
  flux". Γ, γ, and the entropies remain distinct typed objects (`GF:1641-1652`).
- Nonlinear boundary: `Im W = −(ħ/2) log γ`. Gamma fixes the influence magnitude, not the phase,
  and "gamma alone cannot be promoted into nonlinear Einstein dynamics" (`GF:982-997, 4252-4261`).

### 6.2 The emergence account (collective / scale)
- **The formation chain** (`GF:109-123`): qualified record episode `H` with `I_γ(H) > 0` →
  `K_⋆[H]` → coarse-grainings `Π_n K_⋆[H]` → predictive IR autonomy → operational front/order →
  `(I_H^+, μ_H^vol)` → conformal class `[g_H^eff]` → `g_H^eff` → universal gravitational dynamics.
  Each arrow carries a distinct proof obligation (`GF:173-182`).
- **What it is not** (`GF:3961-3969`): "does not say that microscopic records contain little pieces
  of curvature." The mechanism is record-associated substrate dynamics establishing a **stable
  collective phase**. A protected long-wavelength tensor excitation of that phase is the candidate
  metric channel; complete stress-energy sources it; the retarded field acts back through the same
  CTP effective action. "It is an architecture, not yet a complete gravity derivation."
- **Seed plus ancestry** (`GF:3971-3981`): the first record carries `I_γ > 0`. Classical geometry
  and gravity "arise only after collective gluing, same-sector ancestry, physical soldering,
  compatible connection selection, refinement, and the universal stress/response gates."
- **Adopted meaning of Gravity Emergence** (`GF:1067-1078`): memory-lineage processes in one
  complete parent establish a stable relational phase whose macroscopic self-consistent long-wave
  response is gravity. The constitutive discriminator is **intact vs whole-lineage BREAK at matched
  energy, stress, EM, occupancy, heat, support, boundary export, and read sensitivity**.
- **Curvature** (`GF:1934-1952`): "not 'record curvature grows until it becomes gravity'". Instead,
  one parent develops causal order plus physical volume whose continuum description is metric, and
  then universal metric dynamics.
- Adopted construction: `F3_grav + E-EMERGENTSPACE`, non-temporal micro-to-IR (2026-08-26,
  `GF:1043-1048`). Named composite target: **RGTSC**, with its contract at `GF:1062-1065` and
  `GF:1105-1116`.
- **The collective-onset layer, derived** (`GF:3989-4051`):
  - Feedback boundary `4U_d χ_0^R(0) = 1` (`GF:184-198`).
  - Degree plateaus `−2U_d < Δ − 2λ_R x < 2U_d`.
  - The TFIM phase `Δ_coll = |2h − U_d|` (`GF:200-211`).
  - Record-patterned ring stiffness `J_□(r) = h⁴ Σ_{π∈S4} 1/(Δ(S1)Δ(S2)Δ(S3))` (`GF:254-269`).
  - Record-occupation-dependent 2D Ising mediation (`GF:291-304`) and phase straddling
    (`GF:306-321`).
  - KEEP reaches the ordered phase and BREAK reaches the blank phase (`GF:323-334`).
  - The collective variable is named at `GF:4049-4051`: **"the current collective variable is
    active retained-memory topology, not raw record number"**. Equal-count placements give
    different responses (`GF:1226`).
- **Downward direction** (`GF:4053-4060`): in the sealed static hold the retarded back-kernels are
  exactly zero. Autonomous support, a back-propagation limit, emergent space, and gravity remain
  open.
- **Not earned** (`GF:4173-4184`): no stable local second pole, derived connected-support phase,
  distance/dimension, common chart, or common-cone/gap-ratio pass.

### 6.3 Latest finite results in lineage B (`GF:1289-1392`; `RG:11066-11198`)
- **RA-9**: the joint lineage–carrier association is nonzero and two-sided through L12
  (`D_10 = −3.12e-4`, `D_12 = −3.24e-5`). The **positive no-decline prediction FAILS**: the sign
  reverses and the magnitude falls, with normalized `η_12 ≈ 0.014%` (`GF:1308-1319`).
- **RA-10**: an L8 Ollivier–Ricci formation-order curvature test gives a controlled null,
  `ρ = 0.154`, `p₊ = 0.362` (`GF:1339-1366`).
- **RA-11**: at L4, retained joint lineage information changes later carrier state,
  `Δ_C = 0.1476` (`GF:1368-1392`). There is one size only, and no persistence or geometry.
- GFT-1 (SL:274) is a conditional closure under adopted RGRL + WTC-H1-H5. RA-7 (SL:281) is the
  finite `z=1` Gate classification at L = 4…12.

### 6.4 What lineage B says must be computed
1. **The G2 same-ancestry pole test** (`GF:4349-4370`): `Δ_L(k)/|k| → c_T > 0`, `rank P_pole = 2`,
   `Z_pole^canon ↛ 0`. If it passes, G3 tests longitudinal decoupling (universal coupling to total
   momentum), then G4/G5 test self-coupling and static exchange.
2. **The missing linear `E` strain source derivative** (`GF:3740-3747, 3749-3756`): find an
   inherited observable that supplies it with the source-off parent unchanged. DPAR is a
   conditional local completion, not an inheritance (`GF:3757-3785`).
3. **Target 4** (`GF:3135-3161`): `GSGB-JOIN` across one authenticated scale family, physical
   `G-SOLDER`, the scale lock `ℓ_F² f = 4a²/3`, torsion-free connection selection, and controlled
   refinement. The endpoint is one same-world chain "with no inserted geometry or routing"
   (`GF:166-171, 3983-3987`).
4. **The complete same-parent `Δ_sw Γ_eff` with graph entropy**, where "no target exponent or `1/r`
   reward may be inserted" (`GF:1150`). Also needed: a physical capacity/formation law, and the
   UCAIC premise, which is not derived (`GF:4111-4116`).
5. **Target 7** (`GF:3448-3464`): derive the U(1)/coupling objects before any number.
6. **DS-1** (SL:287; `RG:11200-11220`): the shared dark-sector candidate.
   - "The next scientific priority is one specified physical coupling and autonomous formation law
     with complete energy/work accounting."
   - The density hypothesis "cannot be supplied merely by increasing identical retained mode
     counts" (`RG:11216-11219`).
   - DS-1 points to `../UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/`.

---

## 7. Where the two lineages already speak to each other (and where they do not)

- **Collective, not per-record.** Both lineages say this:
  - A: `CF:14-16` and the C-80 zero beyond contact for pure Γ.
  - B: `GF:3961-3981`, `GF:1949-1952`.
  - Both match the principal's standing position.
- **Accumulation.**
  - A: requires the source to be sign-definite and accumulating (`CF:23-26`). It computed that
    occupancy accumulates and orientation screens (C-88), and that `μ = μ_c` ⟺ measure-conserving
    writing (C-91).
  - B: names active retained-memory **topology** as the collective variable, "not raw record
    number" (`GF:4049-4051`). Equal-count placements differ (`GF:1226`).
  - Neither file connects B's topology variable to A's occupancy/criticality bit.
- **Where scale enters.**
  - A: falloff and reach live in the **coupling** (C-80). Γ supplies boundaries and the critical
    class at `μ_c = 1/deg`.
  - B: scale enters through the collective phase, a protected tensor pole, and calibrated volume.
  - B never cites `μ_c`, the Γ-priced kernel, or the boundary-degree law.
- **Classical forms inside the documents.**
  - A uses Newton and area-law only as post-computation comparisons, with owners named (SL:250,
    SL:269).
  - B states one conditional IR filter that uses the empirical `1/r`: "Under separately earned
    standard diffusion, `1/r` requires `D=d_s=3`" (`GF:428-430`, `GF:1149`). B labels it a
    necessary filter on support at the IR tier, not a record-level criterion, and the next row
    (`GF:1150`) forbids inserting `1/r` as a reward.
  - Readers checking D-1 compliance should know this sentence exists.
- **Checks any new lane must carry, from the doctrine rows:**
  - D-6: no ensemble-average negatives.
  - D-14: a null must be a null of the named object.
  - D-15 (SL:169): carry the control in the same table.
  - D-22: verify the carrier admits a separation before reading separation-dependence.
  - D-24: earn every concept, including distance.
  - D-25: real record surfaces, not toys.
