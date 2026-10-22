# UNT orientation — required reading for every lane — V001

Claude, 2026-10-12. Documentary orientation written under the principal's instruction to ground every lane in the whole program ("We are working to prove this theory"; see §2.1). **This file is a navigation aid. The cited originals govern.** It has not yet had a distinct review; until it does, treat it as KN/UNT_START_HERE_V002.md L18 treats Claude's maps. It does **not** replace the G1–G12 grounding receipt (KN/UNT_START_HERE_V002.md L22–41; KN/GROUNDING_RECEIPT_TEMPLATE_V002.json). Read this first, then the originals, then answer §9 in your acknowledgment alongside that receipt. Science is PAUSED (X/STANDING_ORDER.md L1; TO/0112 L7–12).

**Path keys.** U = `/Users/bgm/Research/Universal Network Theory/` · PW = `U/program-worktree/` · REG = `PW/REGISTER_V001.md` · TSV = `PW/ledger/status_ledger.tsv` (line n; line 1 is the header) · PLN = `PW/ledger/plan.tsv` · CORE = `PW/CORE_FRAMEWORK_V001.md` · TT = `PW/THIRD_TERM_V001.md` · SR = `PW/DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/FORMAL_SCOPE_THEOREM.md` · GF = `PW/GRAVITY_FORMATION_CURRENT_PICTURE_V001.md` · LAD = `U/LADDER.md` · CAN = `U/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/CANONICAL_V006_SELECTION_AND_EXACT14_CROSSWALK_V001/` · V005 = `CAN/CANONICAL_MODEL_7_PROPOSAL_V005.txt` · X = `/Users/bgm/Research/UNT_EXCHANGE/` · TO/nnnn, FC/nnnn, FC2/nnnn, FC3/nnnn = `X/TO_CODEX/`, `X/FROM_CODEX/`, `X/FROM_CODEX2/`, `X/FROM_CODEX3/` message nnnn · GR = `X/claude_artifacts/gamma_reconciliation/` · PKT = `/Users/bgm/Desktop/FOLDERS/Gravity/20260918 Packet/20260924 Packet Updates/` · KN = `X/KNOWLEDGE/`. Longer cited extractions: KN/_foundations_notes.md, KN/_results_notes.md, KN/_current_notes.md.

Markers: **[UNCERTAIN]** = sources disagree or the point is unresolved; **[CLAUDE READING]** = Claude's own reading, not yet distinctly reviewed.

---

## 1. What UNT is and what it claims (in its own terms)

**The charter (principal's words, affirmed 2026-08-17):** "Find the process responsible for record formation, and explain the roles of EM, gravity and alpha in that process. We will find things that don't work. Log them, and invent a next step, so that we ultimately find the process responsible for record formation." PW/PRINCIPAL_ACT_001_DRAFT.md L76–81. No route closes without its next step named (same file L98–102).

**UNT's stated scope:** UNT "investigates whether causal Records and the Bind and Birth actions can provide a common physical account of matter, gravity and cosmic evolution" (U/README.md L3). The exchange PLAN's goal: "NGC 3198's observed baryons in, its 43 velocities out, from ONE canonical UNT model with every calibration counted, and a clear verdict on whether records make gravity" (X/PLAN.md L5).

**The three terms of the charter** (TT L3):
- **EM** supplies the chain complex and the record: d₁ is the Gauss law, d₂ the field-strength term; the record is a holonomy of EM's own complex; at the record level EM has no local content (D-5) (TSV:2, 71; REG:5488–5516).
- **Γ, the third term.** "Gravity" is a permitted label for Γ that does no work: "Γ IS DEFINED ONLY BY THE FUNCTION IT PERFORMS" (TT L5–17). Γ is whatever satisfies R1 SPACE (more than one record state, distinguishing states of the same energy), R2 WRITER (an operation that flips the record which no local operation can mimic), R3 PROTECTION (no local operation writes or destroys it) (TT L21–30). (H₁(Σ), intersection form) is a candidate that satisfies R1–R3, not a definition (TT L39–45). Γ also supplies the channel: a coupling forms a record iff it pairs oddly with the record's conjugate (PW/GLOSSARY.md L40; TSV:123).
- **Alpha** names three separate objects that must never be interchanged: (a) the generic perturbation magnitude λ of the DEF-A corner, "NOT the fine structure constant" (CORE L108–112); (b) physical fine-structure α, typed ALLOW (construction-scoped interval) / REQUIRE (same-sector inheritance under SAI1–SAI8) / SELECT (open) (TSV:273); (c) the formation-activity coefficient a_v^adm, which "is NOT electromagnetic fine-structure alpha" (U/CURRENT_STATE.md L92). Custody rule: "Alpha may constrain STRUCTURE. Alpha may not SELECT structure." (PW/CUSTODY_V001.md L55–63).

**Records.** "Record" has several registered senses; name yours every time:
- **DEF-A record (exact corner):** an operator R with (i) R=R†, R²=I; (ii) [H,R]=0 and [L_k,R]=0; (iii) R not constant on some eigenspace of H; (iv) some admissible U ([U,H]=0) has U†RU=−R; (v) no admissible operation on a single contractible region does (CORE L96–106, L114–117).
- **O-51 amended record (the world's records, ADOPTED):** the same clauses on carrier ⊗ local bath with declared tolerances; (v′) every single-region flip costs ≥ E_b with E_b/kT ≫ 1. All ~20 real records surveyed pass; zero pass DEF-A, which is retained as the T→0, t_m→∞, W=0, E_b→∞ corner (CORE L61–89; TSV:233).
- **Nomenclature:** "Record" names retained network state or content; Bind and Birth name actions (PW/nomenclature/BIND_BIRTH_POLICY.md L3–7).
- **V005's q_v:** a binary Record register at each site, rotated by Bind (V005 L4, L17). Whether this is the charter's record is an open declared item (§5).

**The network and its actions (canonical V005, §5).** A finite graph whose edges carry incidence bits n_e and whose sites carry a carrier p_v, a Record q_v and a resource cell {I, Ready, Spent} (V005 L4). **Bind** g p_v X_{r,v} rotates q (V005 L17). **Admission** A_v⁺ = |S,x⟩⟨R,B| ⊗ I_q moves Ready to Spent without writing q, and its reverse is kept (V005 L9–10, L17). **Birth** is a finite graph splice that inserts blank carrier, blank q and inactive cells at new stars; its adjoint, un-Birth, is real (V005 L15).

**The central claim: origin.** "Γ IS WHERE GRAVITY COMES FROM": not identity at the record level (withdrawn as an import, X-6), not resemblance; "Records are the substrate. Classical gravity is what Γ becomes at scale. The direction is Γ → gravity and never gravity → Γ." (REG:6789–6801; TT L62–66). Defining Γ by function alone is what keeps the claim non-circular (REG:6803–6817). Commitment 3, "classical gravity is recoverable from accumulated Γ", was recorded as the whole remaining task, T-20 (REG:6819–6826).
- **C-77, adopted ("yes let's adopt this"), status CANDIDATE:** "The structure Γ that allows a record — by shaping the boundaries that make a bit non-losable (non-contractible support in the corner; basin boundaries in the world) — is the same structure whose aggregate at scale appears as geometry. Classical gravity emerges from the boundary-shaping terms and is not expected to resemble itself at the record level." Openness clause: Γ is the named contributor, never asserted to be the only one; "A derivation succeeding through additional terms alongside Γ satisfies the claim." (REG:9539–9563; TSV:248).
- **A-GR3 shared origin** and **A-GR4 mechanism shape** ("We don't expect classical gravity to look the same at the record level. We expect it will emerge from terms like Gamma that SHAPE GEOMETRY AND BOUNDARIES.") (TSV:245, 247).
- **H-9, the principal's emergence criterion:** "A STABLE, UNIVERSAL, PATH-DEPENDENT MISMATCH AMONG RECORDS THAT CAN BE INTERPRETED AS CURVATURE"; "One record cannot show gravity. Two give relation. Several make PATH COMPARISON possible." The Einstein form says what a positive result would mean and is never the criterion (REG:7330–7367; TSV:144).

**Two gravity lineages exist in the program.** Lineage A is Γ / C-77 through C-93 (TSV:248–272). Lineage B is record-first Gravity Formation (GF; GFT-1, TSV:274; RA-1..RA-11, TSV:275–286; DS-1, TSV:287): by its own text "an architecture, not yet a complete gravity derivation" that "does not place a classical gravitational field on the first record" (GF L3961–3981); its collective variable is "active retained-memory topology, not raw record number" (GF L4046–4051). **[CLAUDE READING]** The two lineages do not cite each other (X/claude_artifacts/program_grounding/PROGRAM_GRAVITY_PICTURE.md L41). Every proposal names which lineage it extends and whether any bridge is proved (KN/UNT_START_HERE_V002.md L18).

---

## 2. Core principles and premises

### 2.1 The principal's premises of 2026-10-12 (verbatim from the relays)
1. "UNT basically says gravity starts at the record level. There is no 'new gravity' added later. It's records all the way down. It just emerges." Consequence: no separate gravity source law; Records are the source (TO/0077 L1, L8).
2. "There are records all the way across the universe. The universe is made of records. Why is this a mystery?" Consequence: matter and space are both made of Records; gravity needs a *difference* relative to a Record-filled background (TO/0080 L1, L7–9).
3. "There is no 'empty space' in UNT." Registered as state premise S1; blank-Record states are mathematical controls and limits only (TO/0082 L1, L8; TO/0083 L9–11; V005 L28). Related: "We want to derive this", i.e. the background is derived, not declared (TO/0084 L1–4; V005 L30).
4. "I never would have assumed that you could get gravity from individual records. This has always been about emergence and collective behavior." Consequence: single-carrier and single-Record results are constraints on the parts, never gravity verdicts (TO/0109 L1, L7).
5. "We need to be careful here not to import classical machinery into the analysis." (TO/0100 L1; rule L7–19).
6. "The method that we used for z=1 was actually the correct way to approach that metric." The exact response sum-rule route (m₁(k) from the double commutator; ω_min(k) ≤ m₁(k)/S(k)) is the primary estimator; the audit objections (roundoff in preregistered 1/L tests, ARGER passes by construction, external Luttinger input for S(k)) are separate from the method (TO/0108 L1, L7–18).
7. "The whole point of doing a project like this is to build on previous learning." and "If we have to start from scratch every time we're working on the next term we end up repeating work." (TO/0110 L1; TO/0111 L1).
8. "This program is too much of a departure from standard physics to just throw work at agents." (TO/0112 L1).
9. "We are working to prove this theory." (principal, 2026-10-12, in the instruction that commissioned this orientation; not yet in an exchange file). Also: "We need to make sure that every model working on this program is thoroughly versed in UNT." (KN/UNT_START_HERE_V002.md L5). "Prove" carries the program's own meaning (§4.1): a test any physicist can run on real record data (CORE L39–53).

### 2.2 Earlier standing principal decisions
- **Canonical rule set** = literal V006 H_complete #7 plus the owner-once admission extension, signed as a **declared premise, not a derivation**; admission and Bind are joined deliberately, not identified; no existing result is promoted by it (TO/0005 L9–11, L22–24). V005 adds S1 (V005 L25–28; FC/0051 L5).
- **No imposed permanence.** Bind is a Rabi oscillation and Hermitian admission contains its reverse; imposing permanence "would build accumulation in by construction" (TO/0008 L9–11; TO/0010 L7–12; V005 L19).
- **Records accumulate is measured, not imposed** (P-18; TO/0008 L12–23). S and q are separate censuses; whether they track each other is a measured result (TO/0010 L13–14).
- **The arrow comes from preparation.** Every V005 term is time-reversal-even at the declared values, so the dynamics has no intrinsic arrow; the arrow is ALLOW-side, set by the preparation (past-hypothesis structure) (TO/0009 L9; TO/0011 L21–24; X/PLAN.md L82).
- **P-26 repeated Birth is parked, unadopted.** P-51 tests it as a labelled TEST MODEL feeding a decision card (X/PLAN.md L34, L56; TO/0101 L4, L22).
- **The label does no work:** "I don't have a problem with using the term 'gravity' as long as we don't use it as an excuse to import a variety of classical metrics that aren't applicable." (TT L5–7, L16–17; D-2, TSV:37).
- **Accumulation is whatever it proves to be:** "Let's be careful not to be too prescriptive on 'what' emergence actually is. ... The mechanism for accumulation is whatever it proves to be." Binding on every lane; every outcome registers as the surface's own law (REG:10347–10358).
- **What may be asked of a record-level source:** extensive, additive over disjoint regions, not a mere count, sign-definite so it accumulates. "A falloff EXPONENT IS NOT AMONG THEM." (CORE L23–26).

### 2.3 ALLOW / REQUIRE / SELECT (the type discipline)
On a declared parent P with admissible set A_P and reporting map v: ALLOW_P(v=a) ⟺ a is attained on A_P; REQUIRE_P(φ) ⟺ φ holds on all of A_P; SELECT ⟺ a declared trajectory or limiting law selects the v=a occupancy (SR L115–135). REQUIRE ⟹ ALLOW; ALLOW ⇏ REQUIRE; SELECT ⇏ REQUIRE (SR L164–173). Origin: "Dynamics produces OCCUPANCIES, never PERMISSIONS" (REG:5231–5240; D-4, TSV:58). **Repaired rule:** "Within a frozen parent, internal dynamics changes occupancy inside the parent's admissible space; it does not change the definition of that parent's permissions. Effective permissions may change along a history only when an enlarged parent, external parent family, or explicitly declared coarse-graining map contains and owns the variables responsible for the change." (SR L464–479). Formation in an enlarged parent is well-typed only given five objects: distinguishable carrier fibers, an admissible global subspace, an owned off-diagonal transition, a before/after occupancy criterion, and complete conservation and boundary accounting (SR L333–344). Hostile audit PASS 300/300 and 102/102 (PW/AUDIT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/INDEPENDENT_HOSTILE_AUDIT.md L3–8).

### 2.4 Gravity as collective emergence from accumulated Γ
Put together, the sources say: gravity starts in Records and is not added later (TO/0077 L1); it is what Γ becomes at scale (TT L66; REG:6798–6801), via the aggregate of the boundary-shaping structure (C-77, REG:9541–9551), possibly with other contributing terms (REG:9559–9563); it exists only collectively, in the many-body, finite-density, coarse-grained regime ("pressure exists collectively, not for one molecule", TO/0109 L7); and its emergent form is not expected at the record level (CORE L14–16). **[UNCERTAIN]** Whether the Records of premise 1 are the charter's Γ-carrying records or V005's q registers is open (§5.3, DQ-1).

---

## 3. Forbidden moves and import discipline

### 3.1 Standing doctrine D-1..D-14 ("checked before any lane is commissioned", PW/STATUS_LEDGER_V001.md L57)
| ID | rule (condensed; read the row) | TSV |
|---|---|---|
| D-1 | No classical measure may be applied to the record level as a criterion; a classical quantity may be computed and reported as a relationship, never as the test our object must pass | 36 |
| D-2 | "Gravity" is a permitted label; inference from the label is forbidden | 37 |
| D-3 | A rescue is always downstream of an import: remove the import, not the symptom | 38 |
| D-4 | ALLOW/REQUIRE/SELECT is a type discipline; frozen-parent dynamics changes occupancies, not permissions (scoped by SR) | 58 |
| D-5 | At the record level EM has no local content (no field value or density at a place) | 71 |
| D-6 | The ensemble average ⟨R⟩ is blind to record formation; no exclusion from it without a single-run warrant | 76 |
| D-7 | A caught assumption that lives only in prose will be re-made; every uncleared assumption gets a ledger row | 77 |
| D-8 | A check that cannot fail is not a check; a verdict needs its noise floor measured beside it | 84 |
| D-9 | Describe a result by its mechanism; never rank it ("weaker", "only", "merely") against an external standard | 107 |
| D-10 | A verification with no failing branch is an instrument check, not a result | 112 |
| D-11 | A criterion validated only on the cases it was derived from is not validated | 134 |
| D-12 | Redrawing a complex as non-manifold need not change the quantum system | 136 |
| D-13 | WITHDRAWN 2026-09-15; superseded by the two-alpha split and A-AL2 | 142 |
| D-14 | A zero is a result only if it is a zero of the object the question names | 159 |

Also standing: D-15..D-27 (PW/STATUS_LEDGER_V001.md L77–89), notably **D-24 each classical concept must earn its place** (no falloff exponent has been earned) and **D-25 grounded in real record data, never the toy category** (TSV:246, 259).

### 3.2 No classical machinery as a criterion or load-bearing step (TO/0100 L7–19; TO/0102 L10–15)
Native verdicts come from the canonical model's own dynamics. These appear only as **labelled conditional diagnostics**, recorded in a CLASSICAL-IMPORT LEDGER in every packet; any load-bearing use is a declaration to the principal: Coulomb/Gaussian Maxwell phase, Gauss-law fields, 1/r² profiles; Debye/RPA screening; Poisson and Einstein equations; Newtonian orbits (v²=r·g); Euclidean embedding or continuum chart; thermal/Gibbs states; QSI/QMC phase evidence; elasticity and displacement fields. Exact mathematical and numerical tools do not by themselves supply a physical premise (FC/0076 L8). Banned record-level comparisons: inverse-square, r⁻², 1/r, G, a metric, a geodesic, the Einstein equations, "gravity needs …" (CORE L18–21). A classical-shaped null "READS TWO WAYS" (CORE L28–29).

### 3.3 Standard-physics defaults that are framing errors (TO/0112 L14: "a framing error, not a neutral starting point")
1. Single-object footprints as the decision object; a single-carrier result read as a gravity verdict (TO/0109 L4, L7).
2. Fields falling with distance; a falloff exponent as target, pass test or lane-steering quantity (CORE L23–26; GR/CHALLENGE.md L195–202).
3. Coulomb/Maxwell channels; light from Maxwell instead of the native spectrum (TO/0102 L14).
4. Metric pass tests; one-metric/3+1 template as geometry criterion — whether species share one geometry is a finding (TO/0102 L11).
5. Newtonian inputs: SPARC V_gas/V_disk/V_bul templates as baryonic source; "kernel → potential → additive correction" orbits (TO/0102 L12–13).
6. Empty space: a blank-Record vacuum as a physical region (TO/0082 L8; V005 L28).
7. A separate gravity source law added to the model (TO/0077 L8).
8. Imposed irreversibility or permanence (TO/0008 L9–11).
9. Assuming a thermal/Gibbs or equilibrated background instead of deriving it (TO/0100 L15; TO/0084 L8–12; V005 L30).
10. Graph distance replaced by 3D shells or an embedding (TO/0102 L15).
11. Identity of Γ and gravity at the record level; H₁(Σ) treated as the definition of Γ (TSV:28; TT L39–45).
12. "Alpha" read as the fine-structure constant where the source means λ or a_v^adm (CORE L108–112; U/CURRENT_STATE.md L92).
13. Asking a frozen parent's dynamics to produce its own permissions (D-4; SR L220–230).
14. Treating Records as counts: record density as the gravity variable (count is the wrong density variable, TSV:170, 174; GF L4046–4051).
15. Starting from the Hamiltonian without a prior-work ledger (TO/0110 L15; TO/0111 L7).

---

## 4. What the program has established (the prior learning every lane builds on)

### 4.1 Status vocabulary and scoreboard
PROVED = a quantity in units, a predicted value, a falsifier, and at least two structurally different real record surfaces; enforced by `ledger/status.py` (CORE L48–53). FORMAL = real mathematics about the program's own stipulated definition, with no real-record contact (CORE L55–57; PW/ledger/STATUS_VOCAB.tsv L14). DEFINED, MEASURED, CANDIDATE, PARTIAL, OPEN, FAILED, WITHDRAWN are the ledger's other words (STATUS_VOCAB.tsv L2–14). LADDER adds EXACT/COND/CERT/ADOPT (LAD L12–15). Ledger counts over 286 rows: FORMAL 153, DEFINED 49, OPEN 30, FAILED 12, WITHDRAWN 11, PARTIAL 11, MEASURED 9, CANDIDATE 3, BLOCKED 3, NOT OURS 3, RECLASSIFIED 1, **PROVED 1 (C-71)** (TSV:2–287; REG:10243). Empirical contact: X-4 BLOCKED, "empirical contact is zero" (TSV:26). Proving UNT in the program's sense is therefore the open work.

### 4.2 By area (D = derived, A = adopted, F = failed/withdrawn, O = open)
**Records.** D: existence iff a trace-balanced commutant projection (C-12, TSV:81); homology sufficient, not necessary (C-4, C-22, TSV:9, 143); no admissible writer fits in one contractible region, and the strong reading "nothing local can write it" is false (C-13, TSV:83); "the record is READ, not written" (F-20, TSV:104); C-71 PROVED on NAND and CoCrPt (TSV:238). A: DEF-A as the corner; O-51 (TSV:233); admissible := [U,H]=0, provisional (TSV:20). F: zero of ~20 real records meet DEF-A (H-3, TSV:128); PF-6 no distinguishing prediction (TSV:96). O: why this definition (T-53, PLN:54); what admissible means (T-25, PLN:26).

**Γ and geometry (lineage A).** D: C-78 distance is boundary-crossing cost, a true metric (TSV:249); C-79 boundary-degree law matches the area law in form, CANDIDATE (TSV:250); **C-80 no pure-Γ falloff: Γ shapes boundaries, the coupling supplies reach and falloff, alpha supplies costs** (TSV:254); C-83 "the surface owns the clock" (TSV:257); C-87/C-88 three reachable classes and one design point (R1 + occupancy) for the Newton profile (TSV:264–265); C-90 D=3 critical member is 1/d on a single venue (TSV:269; REG:10367–10371); C-91 masslessness = measure conservation, residue one bit (TSV:270); C-93 the integer tier carries no field (TSV:272); carrier curvature and record content independent on the toric carrier (H-15/C-27, TSV:161–162). A: C-77 CANDIDATE, "NEWTON VERDICT: MATCHES AT MEMBER LEVEL ... never a claim that continuum or Einstein gravity is empirically derived" (TSV:248); connection = carrier transport (H-14, TSV:160). F: **G-6 uniqueness broken** (TSV:41); H₁ as definition withdrawn (G-1, TSV:14); T-20 measured flat, interpretation withdrawn by O-23, connection not fixed by records (REG:7371–7464); "under the five clauses Γ does not produce gravity" withdrawn as proved of the wrong object (REG:7719–7750); first T-51 field scoring quarantined, no C-94 (REG:10842–10867). O: T-49 conservation bit (PLN:50); T-51 field instrument, "no field has been measured" (PLN:52; REG:10340–10342); O-39 (TSV:201); O-55/56/57 (TSV:252, 253, 258); O-58 N3–N5 design point, norm, anisotropy (TSV:266). **[UNCERTAIN]** TT L72–73 still reads "untouched — plan task T-20" while PLN:17 marks T-20 DONE; cite C-77's row, not either summary.

**Gravity formation (lineage B).** A/D: GFT-1 FORMAL as a conditional implication under adopted RGRL and WTC-H1–H5; empirical RGRL, microscopic F3, strict origin and numerical G open (TSV:274). The closure theorem composes conditional components; "These results do not establish an unconditional native gravity theory or derive the numerical fine-structure constant." (U/README.md L14).

**Admission and finite universe.** D: L4 intrinsic-admission theorem (REG:10994–10997); RA-5 L4–L12 record-block theorem (TSV:279). A: ARGER Gate by principal decision (REG:10943–10949); LADDER label "ADOPT gate membership / CERT implementation; UNINFORMATIVE as physical criticality evidence" (LAD L31). F: RA-2 Stage-6 z=1 rejected for its own classifier (TSV:276); RA-9 signed persistence failed (TSV:284); W3 = −0.284 "coherent unwriting" is specific to the L4 κ=π/2 resonance (TO/0010 L16–25). O: premise-free all-L z=1 (REG:10951–10955); sum-rule port to V005 (TO/0108 L20–24).

**Alpha.** D: A-AL2 typing (TSV:273). F: forced alpha withdrawn; alpha FREE LIMITED (LAD L66). O: T-38 (PLN:39); no 3/7 partition selected (LAD L67).

**Galaxies and cosmology.** SPARC transfer: "There is no resolved advantage over RAR"; "useful effective-model evidence, not established UNT superiority" (U/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/SPARC_EFFECTIVE_TRANSFER_V001_RESULT.md L3–4, L24). Historical NGC 3198: 13/43 within errors (LAD L103). Cosmology chain uses adopted Ω_A=.7 / Ω_C≈.251, "not a budget-free native prediction" (LAD L113). Clean native120 and new43 unstarted (LAD L104). All eleven program lanes OPEN (LAD L207–218).

### 4.3 Validity audit verdicts (PKT)
Bottom line: "Execution is verified; discriminating power usually isn't"; "There is no single UNT model"; the top end is imported (UNT_VALIDITY_AUDIT_V001.md L9–13). Scorecard after cross-lineage refutation: 82 items, VALID 16, LIMITED 37, UNINFORMATIVE 18, MISREPORTED 11 (UNT_VALIDITY_AUDIT_V002.md L37–41); "Most VALID verdicts are honest ADOPT/OPEN labels or honestly reported failures, not positive evidence" (V001 L31). Survivors: the signed lineage-persistence FAIL, the scoped exact obstructions, implementation certificates (numerics, not physics), SPARC as a test of a MOND-type law (V001 L33–39). The "14 constructions" are a 14-entry inventory, not 14 dynamical models; reduction needs a stated map and bounds; "Shared terminology is not one" (CAN/EXACT14_CROSSWALK_V001.txt L5–13, L96). **Every cited prior result must carry its construction label**; porting one to V005 is new work (TO/0005 L24; V005 L23). **[CLAUDE READING]** Audit V001 §6's universality discriminator (L113–122) must not be used as a pass test under TO/0102 L11.

---

## 5. The canonical model V005 and its tensions with the charter

### 5.1 What V005 is
Rules (V005 L4–23): domain = literal V006 periodic q4 graph plus one supplied Born graph; H7 + H_cell + Hermitian admission + Hjoin (Birth through ε_B Tjoin and its adjoint); Q = N_c + N_ready and M = N_ready + N_spent conserved; Bind rotates q, admission does not write q; neither census is asserted monotone; no imposed permanence; magnitudes declared, "the historical tuple is a benchmark, not a fit"; "No existing result is promoted ... No photon recovery, positive mobile mass gap, metric, universality, gravity or galaxy prediction follows". State premise S1 and "derive the background" (V005 L28–30). Open checks stated in V005 itself: p, q and Ready/Spent stay distinct; "matter and space are made of Records" does not identify p with q; S1 "supplies no numeric meaning of 'filled'"; Birth still inserts blank q (V005 L32). ⟨q⟩=½ at infinite temperature is a control only (V005 L34).

### 5.2 Known tensions
- **q Records vs Γ.** q_v's only writer/eraser is Bind, a local term of H; generic q "fails exact durability" (FC3/0145 L12; FC/0075 L10–12). Root's correction: "Bind alone is not automatically an admissible full-H energy-preserving writer; bareq obstruction is its nonzero commutator" (FC/0075 L12). Both readings agree q_v is not Γ (GR/RECONCILIATION.md L6–11; GR/CHALLENGE.md L231–232). P-54: "No actual V005 Gamma certificate and no no-Gamma theorem" (FC/0075 L10).
- **The only Γ-shaped V005 object is conditional.** The ice-manifold flux class Φ ∈ ℤ³ (GR/RECONCILIATION.md L14). **[CLAUDE READING, same-lineage challenge, not yet cross-reviewed]** The reconciliation's exact DEF-A "THEOREM" is false as stated: R_S is unbalanced on the ice manifold whenever the cross-section has an even number of edges, and at the declared h=1/5 the −hX_e term breaks durability; "exact DEF-A shows no Γ in V005" (GR/CHALLENGE.md L16–21, L56–90, L251–258; GR/challenge_checks/ice_flux_parity_balance_OUTPUT.txt L6–14). Under the amended (v′), Φ is the Γ candidate; contractible moves cannot change it; its barrier is ≈ 2U_d − |λ_J Σp − λ_R Σq| on the card's degree-lock ray, so Records and matter lower it (CHALLENGE L119–131, L259–265). Charter Σ (faced 2-surface, imposed Z₂ Gauss sector, plaquette H) is not V005's graph; Theorems A–D do not transfer (CHALLENGE L136–150).
- **L ≥ 4 for Γ.** Φ's protected classes exist only for L ≥ 4; the literal L2 member has none (GR/RECONCILIATION.md L24; GR/CHALLENGE.md L184).
- **One-level Birth.** V005 has one Born level and "no indefinitely iterated Birth rule" (V005 L15); "no empty→seed operator and no repeated graph levels", so a growth history from an origin cannot run inside #7 as signed (TO/0090 L9). One Birth level caps accumulation; Birth can change which Φ classes are protected (3→2 at L=4 under illustrative labels) (GR/RECONCILIATION.md L48; GR/CHALLENGE.md L172–184).
- **Where the 120/43 chain was aimed.** It measured matter's q-footprint and steered lanes by falloff shape; that steering came from Claude's own relays (TO/0097 L19; TO/0104 L24; TO/0107 L9) and is what CORE L14–26 and D-1 forbid as a record-level test (GR/CHALLENGE.md L195–202). Measuring the coupling is legitimate (C-80); what is missing is the Γ side that prices it (CHALLENGE L190–194).

### 5.3 Open declared items for the principal (not computable; registered, not chosen by lanes)
- **DQ-1 (P-a):** Is V005's q_v the charter's "record", and what does S1's "made of Records" refer to? (GR/RECONCILIATION.md L52; TO/0106 L19; FC3/0145 L14 "Principal definition/state dictionary decision remains explicit").
- **DQ-2 (P-b):** Which protection reading governs V005: exact (v) or amended (v′)? **[CLAUDE READING]** CHALLENGE L109–131 argues the corpus already settles (v′) through O-51 (TSV:233) and A-GR4 (TSV:247); root keeps exact DEF-A and finite-tolerance definitions explicitly separate (FC/0075 L12). Not yet ratified.
- **DQ-3 (P-d):** the canonical L and cut geometry are declared, and Γ needs L ≥ 4 (GR/RECONCILIATION.md L55).
- **DQ-4:** repeated Birth (P-26) adoption, after P-51 evidence (TO/0101 L22).
- **DQ-5:** Corollary 5.4 objects (2) and (4), if the enlarged-parent formation route is taken (GR/RECONCILIATION.md L47; SR L333–344).
- **DQ-6:** any residue of the matter dictionary ("what in #7 plays matter made of Records") that derivation cannot fix (TO/0080 L15; V005 L32).
- Computable, so not principal items: whether the 120/43 kernel carries Γ (CHALLENGE L221–222); the background (P-49); Φ's barrier certificate.
- The Γ-first search (GR/RECONCILIATION.md L41–49) and the restart framing are agreed with the principal before any lane restarts (TO/0109 L13; TO/0112 L12).

---

## 6. Today's accepted results (with their scopes) and retired framings

None of these is a native gravity, metric, background or galaxy result.
| result | scope as accepted | source |
|---|---|---|
| Q0 Record-word freezing | exact on invariant global Q=0 only; not regional freezing or an EOS no-go | FC/0052 L7 |
| Bind-erased cloud exponential bound | fixed-ice, gapped, written-background Q1 branch; "conditional dictionary diagnostic"; full-model range undetermined | FC3/0118 L9–11 |
| graph-distance resolvent (Combes–Thomas) | sufficient exponential test only; "Algebraic range cannot be concluded from failure"; weak in practice | FC3/0130 L11–13; TO/0113 L12 |
| exposure/energy bounds 0126/0128/0134 | diagnostics and conditional certificates; 0128 PASS_WITH_CORRECTIONS (uniform bound on \|g\|Q required) | FC3/0126, 0128, 0134 L11–13; TO/0113 L8–11 |
| channel census, loop confinement, pair-word blindness, magnetic sign | each scoped to its fixture; no native r⁻¹·⁰⁵ law; no deconfined photon proved | FC3/0124, 0136, 0137, 0138 L11–15 |
| P-45 h⁶ diagonal theorem | four-regular girth ≥ 6 ice domain; no photon, curvature or clock line | FC/0037 L10; FC/0039 L25 |
| P-48 coefficient laws | finite coefficient-law result; "no gravity/helicity verdict" | FC/0076 L11 |
| P-49 benchmark and controls | "not stationarity, DE, ETH, physical background or long-time memory"; held | FC/0069 L5–10; FC/0076 L13; FC/0077 L13 |
| P-51 first-Birth, t⁸ | TEST MODEL, unadopted; "repeated local writing, not proved time-monotone accumulation or spatial force" | FC2/0106 L10–12; FC/0076 L14 |
| P-54 Γ census | no Γ certificate, no no-Γ theorem | FC/0075 L10 |
| P-55 sum-rule theory and controls | method controls only; no native spectrum released | FC/0076 L15; FC/0077 L13 |
| validity audit V002; P-1 V005+S1; P-2 crosswalk | documentary | PKT/UNT_VALIDITY_AUDIT_V002.md; X/PLAN.md L15–16 |

**Retired framings** (to receive D/X-style entries, TO/0111 L20; FC/0076 L19): one-metric/3+1/GR weak-field fixtures as geometry criterion (TO/0102 L11); Newtonian SPARC templates as source (TO/0102 L12); single-carrier/single-Record verdicts (TO/0109 L7); blank-Record vacuum as physical background (TO/0082 L8); imposed permanence (TO/0008 L9); P-31 bond-angle source law and P-37 kernel as the gravity verdict (TO/0077 L8); "flat curve needs a 1/r pull" and Coulomb/Debye wording (TO/0100 L4).

---

## 7. How to work

1. **Pause.** Switch is PAUSE: finish the current step, post status, stop (X/STANDING_ORDER.md L1, L7). Only in-flight reviews, controls and write-back continue (TO/0112 L8–10). Grounding does not authorize science (KN/UNT_START_HERE_V002.md L7).
2. **Framing before dispatch.** No lane restarts until the principal and Claude agree the framing in UNT's own terms and a small set of well-posed questions grounded in program results (TO/0112 L12). Before any task is commissioned, check it against D-1..D-14 (PW/STATUS_LEDGER_V001.md L57) and the 0100 import list; run the null option first on route decisions (PW/FRAME_CHALLENGE_V002.md L11–30).
3. **Prior-work ledger (mandatory, TO/0110 L15).** Every packet and PLAN task lists the program results it **builds on, ports, contradicts or supersedes**: REG C-/X-/D-entries, TSV rows, theorems, lane files, with path and line. Add for each: its construction label (#1..#14) and whether a reduction to V005 exists (CAN/EXACT14_CROSSWALK_V001.txt L11–13); its status word; which lineage (A or B). A packet that cites nothing says why it is new. Reviewers check this ledger.
4. **Classical-import ledger** in every packet: each construct and its role, diagnostic or load-bearing (TO/0100 L9–19).
5. **Write-back (TO/0111 L6–21).** REG and TSV are the entry point. Root alone appends accepted results there with scope, status and reopen condition (FC/0076 L19). KN/LEARNED_INDEX.md is to be seeded after the grounding map (TO/0111 L21); it does not exist yet.
6. **Every outcome registers**, including "no profile", "no difference beyond contact" and non-classical forms; a native result is reported as it is (TO/0077 L9; TO/0080 L9; TO/0100 L25; REG:10347–10358). Describe by mechanism (D-9). Name the next step any failure forces (PW/PRINCIPAL_ACT_001_DRAFT.md L98–102).
7. **Review classes (TO/0095 L11–19).** Class 2a (analytic or small exact): one distinct cross-lineage review naming what it recomputed. Class 2b (method controls): one independent check against independently computed values. Class (c) (real-model runs feeding 120/43): full custody. Always: no self-review, never consume an unreviewed output, cross-lineage preferred, Codex root is sole numerical launcher (X/README.md L33–34; X/STANDING_ORDER.md L16–19).
8. **Grounding receipt.** Post an immutable receipt answering G1–G12 with path/line evidence, reading coverage and gaps; a different reviewer checks it; no self-certification (KN/UNT_START_HERE_V002.md L22–47; FC/0077 L7).

---

## 8. Glossary (program meanings; the cited source governs)

| term | meaning | source |
|---|---|---|
| Γ | the third term, defined only by R1–R3; "gravity" is its label | TT L5–30 |
| γ_Q, γ_IF, γ_state | lower-case lineage-B quantities (complete-query, influence, squared Uhlmann fidelity); not Γ unless a separate warrant identifies them | KN/UNT_START_HERE_V002.md L27; GF L141–152 |
| R1 / R2 / R3 | SPACE / WRITER / PROTECTION | TT L25–27 |
| DEF-A / O-51 | exact five-clause corner / amended clauses on carrier ⊗ bath (ADOPTED) | CORE L61–106 |
| admissible | at least five distinct senses: [U,H]=0 (DEF-A); dilation-writable (iv′); predicate A_P (SR); canonical admission operator; channel | KN/_foundations_notes.md §3.4 |
| writer | the conjugate operation that flips a record | PW/GLOSSARY.md L29 |
| Bind / Birth / un-Birth | q-rotating action / finite graph splice / its real adjoint | V005 L15–17 |
| admission, Ready, Spent | A_v± on cell {I,R,S}; R=Ready, S=Spent, "neither is q" | V005 L4, L9 |
| p_v, q_v, n_e | carrier, native Record register, edge incidence bit | V005 L4 |
| Q, M | N_c+N_ready, N_ready+N_spent (conserved) | V005 L15 |
| S1 | no empty space; physical states Record-filled; fixes no numbers | V005 L28–32 |
| parent / enlarged parent | data held fixed for a question / direct sum over carrier fibers with owned transitions | SR L35–41, L249–272 |
| occupancy | the actual state inside the admissible set | SR L80–93 |
| ARGER | ALLOW → REQUIRE → GATE → EM → RECORD | PW/README.md L22–32 |
| Φ (ice flux class) | winding label in ℤ³ on d_v=2 states; V005's only Γ-shaped candidate, conditional | GR/RECONCILIATION.md L14; GR/CHALLENGE.md L259 |
| construction #1..#14 | inventory rows; #7 is canonical; results keep their labels | CAN/EXACT14_CROSSWALK_V001.txt L5–9 |
| venue / member | the carrier on which a result was computed / one size or tuple of a family | REG:10367–10371 |
| 120/43 | native 120-chunk and NGC 3198 43-velocity comparison | X/PLAN.md L5; LAD L104 |
| class 2a / 2b / (c) | review classes | TO/0095 L11–18 |
| C-, D-, O-, X-, H-, G-, T-, P- | REG claims, doctrine, obstructions, out-of-reach, hard questions, Γ rows, program tasks, exchange PLAN tasks | TSV; PLN; X/PLAN.md |

---

## 9. Comprehension check (answer all eight in your acknowledgment, with path:line evidence)

Answer in your own words, cite originals (not this file), and post with your G1–G12 receipt. Reviewer flags name the framing error each question is built to catch.

**Q1.** A lane finds that the Record difference around a single carrier on a Record-filled background decays exponentially in graph distance. What does this establish, what does it not establish, and how is it registered? *Flag:* reading it as "UNT fails to produce gravity" or "we need a slower falloff" (TO/0109 L7; CORE L23–29; C-80, TSV:254; D-14).

**Q2.** Define Γ. Is H₁(Σ) Γ? Is V005's q_v Γ? Is lineage B's γ_Q Γ? Is the CORE "alpha" the fine-structure constant? *Flag:* defining Γ by any gravitational feature, or equating objects by shared names (TT L5–45; TSV:41; FC/0075 L10–12; KN/UNT_START_HERE_V002.md L27; CORE L108–112).

**Q3.** Your computation needs a background state. What may you use, what is a blank-Record state for, and may you assume a thermal state? *Flag:* empty space as physical; Gibbs/thermal assumed; ⟨q⟩=½ read as the physical sea (TO/0082 L8–10; TO/0084; V005 L28–34; TO/0100 L15).

**Q4.** Does V005 make Records accumulate? Where does the arrow come from? What would oscillation without net growth in P-18 mean? *Flag:* imposing irreversibility, or treating accumulation as required by the dynamics (TO/0008; TO/0009 L9–18; TO/0011 L21–24; V005 L17–19).

**Q5.** A lane proposes to show that the dynamics produces the record space or its protection on the fixed canonical parent. What is wrong, and what is the lawful version? *Flag:* asking a frozen parent to make its permissions (D-4; SR L190–230, L333–344, L464–479).

**Q6.** Is C-90's 1/d member a derivation of Newtonian gravity? Name its status, venue, and what remains unearned. *Flag:* treating a member-level match as a derivation, or ranking it with "only" or "weaker" (TSV:248, 266, 269–270; REG:10367–10371; D-9).

**Q7.** For each, say whether it may appear in your packet and in what role: Poisson equation, Gibbs state, Euclidean embedding, Maxwell light, linearized Einstein form, SPARC V_disk templates, a 1/r² profile, "one metric for all species". *Flag:* any of these as load-bearing without a declaration to the principal (TO/0100 L7–19; TO/0102 L11–15).

**Q8.** What does "prove this theory" mean in this program, what is the current proof status, and what do the ARGER pass, the SPARC tie and the closure theorem each establish? Name the prior results your next task builds on, with construction labels. *Flag:* treating FORMAL, ADOPT or CERT as PROVED, or a fresh start from the Hamiltonian (CORE L39–57; TSV:238; LAD L31, L103; U/README.md L14; TO/0110 L15).
