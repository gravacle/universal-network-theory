# UNT results notes — what the program has established, adopted, failed, and left open

Extracted 2026-10-12 by a read-only registrar subagent. **These notes are a map, not an authority.**
The sources below are the authority; every claim here carries a citation so a lane can check it.
Nothing in the program workspace was modified and no project code was executed.

## Sources and citation keys

| Key | Absolute path |
|---|---|
| `L:n` | `/Users/bgm/Research/Universal Network Theory/program-worktree/ledger/status_ledger.tsv`, line n (line 1 is the header; 286 rows) |
| `P:n` | `/Users/bgm/Research/Universal Network Theory/program-worktree/ledger/plan.tsv`, line n (the task named `plan.tsv` lives in `ledger/`, not the worktree root) |
| `CG:n` | `/Users/bgm/Research/Universal Network Theory/program-worktree/ledger/claims.tsv`, line n (the headline claims grid) |
| `SV:n` | `/Users/bgm/Research/Universal Network Theory/program-worktree/ledger/STATUS_VOCAB.tsv`, line n |
| `R:a-b` | `/Users/bgm/Research/Universal Network Theory/program-worktree/REGISTER_V001.md`, lines a-b (11,220 lines, append-only) |
| `LAD:a-b` | `/Users/bgm/Research/Universal Network Theory/LADDER.md` (navigation map promoted 2026-10-11) |
| `AL:a-b` | `/Users/bgm/Research/Universal Network Theory/ADOPTION_LOG.md` (see the caution below) |
| `CS:a-b` | `/Users/bgm/Research/Universal Network Theory/CURRENT_STATE.md` (the current-authority pointer named by LAD:3) |
| `SP:a-b` | `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/SPARC_EFFECTIVE_TRANSFER_V001_RESULT.md` |

**Caution on `AL`.** ADOPTION_LOG.md's historical section is *a reviewer's imported assessment*, copied verbatim.
The log itself says that copying it "does not newly adopt a rule, convert a conditional result into an
unconditional claim, or independently reverify every cited artifact" (AL:5-12). Its categories, such as
"criterion_after_results" and "post_failure_fix", are that reviewer's judgments, not the program's verdicts.
LAD:221 adds that the rung 7-8 audit is single-auditor and still pending refutation. Below, every `AL` item is
labelled **[reviewer]**.

**Status vocabulary (the ledger's own definitions, SV:2-14).**
- **PROVED** means a test that any physicist can run against *their own real-world data*, naming the quantity, the predicted value and the falsifier (the principal, 2026-08-20; SV:2).
- **FORMAL** means established about the program's *own stipulated definition* (a theorem, an exact computation or a sweep) with *no contact with any real record*. It is real mathematics, but it is not PROVED in this sense (SV:14).
- **DEFINED** marks a construction or decision that cannot be true or false (SV:6).
- **MEASURED** marks something numerically established across a sweep, without proof (SV:4).
- The other words are PARTIAL, CANDIDATE, OPEN, BLOCKED, FAILED, WITHDRAWN, RECLASSIFIED and NOT OURS (SV:5-13).
- Since T-36, the GROUNDED cell of each FORMAL row has also carried a CLASS (THEOREM, EXACT, MEASURED or DEFINED) and an OWNER (ORIGINAL, BORROWED or ASSEMBLED) (R:9905-9927).
- Since T-9 and T-52, each row has also carried a carrier mark (SINGLE-CARRIER, TWO-CARRIER or NOT-CARRIER-SHAPED) (R:10002-10022, R:10362-10388).

LADDER uses a different word set: EXACT, COND, CERT, ADOPT, FORMAL, OPEN and FAIL (LAD:12-15). LAD:15 notes that "CERT does not silently promote a supplied premise to a native physical result."

---

## 0. The principal's stated premises (carry these into every lane)

These are the program's standing commitments as the register records them. They are not standard-physics framings, so do not substitute any.

1. **The central claim is about origin, not identity: "Γ IS WHERE GRAVITY COMES FROM."** The register rules out identity ("Γ *is* gravity at the record level", withdrawn as an import) and resemblance ("never claimed"). It keeps origin: "Records are the substrate. **Classical gravity is what Γ becomes at scale.** The direction is Γ → gravity and never gravity → Γ" (R:6789-6801). A-GR2 states the same thing (L:123).
2. **Emergence comes from records. It is not identity at the record level.** The principal: *"We want to connect Γ with classical gravity via emergence from records. We are not trying to equate Γ and gravity at the record level."* (R:6738-6753). Emergence "never claims the two look alike at the microscopic level" (R:6750-6753).
3. **The shape is shared origin (A-GR3, TD-1).** Γ is the common structure that ALLOWS records and is proposed to appear at scale as geometry. The binding caveat: "measures at the record level might behave differently from what we've seen in other contexts" (R:9523-9535; L:245).
4. **The mechanism shape is A-GR4.** *"We don't expect classical gravity to look the same at the record level. We expect it will emerge from terms like Gamma that SHAPE GEOMETRY AND BOUNDARIES."* (L:247).
5. **C-77, as adopted, with its openness clause.** "The structure Γ that allows a record ... is the same structure whose aggregate at scale appears as geometry. Classical gravity emerges from the boundary-shaping terms and is not expected to resemble itself at the record level" (R:9541-9551). Openness clause: Γ is the *named* contributor and is never asserted to be the only one. "A derivation succeeding through additional terms alongside Γ **satisfies** the claim. The goal is the solution, not Γ-exclusivity" (R:9559-9563).
6. **Accumulation is whatever it proves to be.** *"Let's be careful not to be too prescriptive on 'what' emergence actually is ... The mechanism for accumulation is whatever it proves to be."* The register says this is binding on every lane, and every outcome of a composition measurement registers as the surface's own law (R:10347-10358).
7. **The import doctrine is what makes the claim non-circular** (R:6803-6817):
   - **D-1:** no classical measure may be applied to the record level as a criterion (L:36).
   - **D-2:** "gravity" is a label; no inference may be drawn from the label (L:37).
   - **D-3:** a rescue is always downstream of an import (L:38).
   - **D-9:** describe a result by its mechanism; never rank it against an external standard (L:107).
   - **D-14:** a zero is a result only if it is a zero of the object the question names (L:159).
   - **D-24:** each classical concept must earn its place (L:246).
   - The import rule itself is at R:4926-4989.
8. **D-25: grounding in real record data, never the toy category.** The principal: *"We are not setting out to create a toy"* (R:8993-8994; L:259). PROOF means "someone anywhere in the world can prove that our calculation agrees with **any record surface**" (R:9390-9393).
9. **ALLOW / REQUIRE / SELECT is a type discipline (D-4, L:58).**
   - Dynamics produces *occupancies*; it never produces *permissions* (R:5231-5240).
   - The older wording "require does not exist at any level" (the X2 erratum, R:4878-4895) and "all Einstein equations are constraints" were **superseded** by DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001. The scoped replacement is G-3 (L:16): inside a frozen parent, Γ supplies an ALLOW/capacity predicate. That does not exclude domain-relative REQUIRE, or a complete enlarged parent whose dynamics changes the occupied fiber.
10. **ARGER is the record-formation process: ALLOW → REQUIRE → GATE → EM → RECORD.** GATE is its single classification stage (R:11016-11019; L:281).
11. **Nomenclature (2026-10-09).** *Record* names retained state or content. *Bind* names the action that maintains Records. *Birth* names the graph splicing that adds Volume (AL:259). This is terminology only.
12. **Vocabulary limits recorded from the external review.** The review called the work "A FORMAL FRAMEWORK, NOT A THEORY". It allowed "we define / we prove (about the defined object) / we verify by exact computation", and forbade *theory*, *proven process*, *explains*, EM, gravity and alpha "until their blocking rows close" (R:9079-9086). D-26 says the review's vocabulary rules "still govern what the URM is said to establish" (L:261). **Uncertain:** later entries use the names "Universal Network Theory" and "Gravity Formation Theory" (R:11040-11064). These notes do not decide how the two fit together.

---

## 1. Program-wide scoreboard

**Ledger totals over 286 rows** (counted from L:2-287):

| Status | Rows |
|---|---|
| FORMAL | 153 |
| DEFINED | 49 |
| OPEN | 30 |
| FAILED | 12 |
| WITHDRAWN | 11 |
| PARTIAL | 11 |
| MEASURED | 9 |
| CANDIDATE | 3 |
| BLOCKED | 3 |
| NOT OURS | 3 |
| RECLASSIFIED | 1 |
| **PROVED** | **1** |

**There is exactly one PROVED row: C-71** (L:238). The program says so itself: "The program reports one PROVED row" (R:10243), and "one PROVED row on modelled surfaces with its falsifier unrun" (T-17 DONE_WHEN, P:21). **[reviewer]** AL:94 notes that C-71's EVIDENCE cell still carries the older "VERIFIED ON ONE MECHANISM ONLY ... this is FORMAL" text. That text is visible in L:238.

**Headline claims grid** (CG:2-10):

| Claim | Stage |
|---|---|
| G-A Definition | GROUNDED-NOT-EARNED |
| G-B Record formation | WORLD-CONTACT-PARTIAL |
| G-C Record laws | FORMAL-COMPLETE |
| G-D Classical/continuum field-side recovery | MEMBER-LEVEL-MATCH (direct field readout open) |
| G-E Three roles | FORMAL-PARTIAL |
| G-F URM integration | IN-CONSTRUCTION (a process status) |
| G-G Gravity Formation Theory | FORMAL-COMPLETE |
| G-H Finite relational accumulation | FORMAL-COMPLETE |
| G-I Foundational record closure | FORMAL-COMPLETE |

**The plan** (`ledger/plan.tsv`, 58 tasks): 46 DONE, 8 TODO, 2 DOING, 2 BLOCKED.
- **TODO:** T-25 what "admissible" means (P:26); T-26 re-audit every null against the venue rule (P:27); T-35 reproduction debt (P:36); T-38 alpha through the barrier (P:39); **T-49 the conservation bit of GR3 writing** (P:50); **T-50 the baseline-free observable for C-72** (P:51); **T-51 the field-side instrument** (P:52); T-53 why this definition (P:54).
- **DOING:** T-19 the gate stays green (P:23); T-54 home the unhomed machinery in the URM (P:55).
- **BLOCKED:** T-18 external reproduction (P:22); T-58 publish and deposit (P:59).

**Empirical contact and prediction.**
- X-4 is BLOCKED: "empirical contact is zero and no distinguishing prediction is identified" (L:26). T-VI.3 and T-VI.4 are BLOCKED (L:34-35).
- PF-6 FAILED: every measured result was already predicted by a rival (L:96).
- Its successor audit, C-84, returned **three survivors** (DEFINED; L:260; R:9781-9804):
  - **S-1:** the durability-clocked certification window.
  - **S-2:** flash alpha-channel discrimination.
  - **S-3:** the thickness profile 1,2,1,0.

**The LADDER's current inference labels for audited headline claims** (LAD:24-34):

| Audited claim | Label |
|---|---|
| pi/8 covariance transfer | UNINFORMATIVE as an independent physical prediction |
| W3 coherent-unwriting obstruction | LIMITED historical case |
| Lineage changes future dynamics | COND |
| Strict common-lineage rise | UNINFORMATIVE without a discriminating null |
| Preregistered z=1 failure | UNINFORMATIVE about z=1 until a known z=1 positive control passes the same test |
| ARGER pass | ADOPT membership / CERT implementation; UNINFORMATIVE as physical criticality evidence |
| Alpha FREE | LIMITED / underpowered |
| Outer-radius halo win | LIMITED / PROVISIONAL |
| L8 chronology-path curvature | UNINFORMATIVE for emergent geometry or gravity |

**All eleven program lanes are OPEN** (LAD:207-218): native source/clock/ruler/volume/formation; shared spatial state; galaxies; expansion and ruler; lensing; structure/growth/stability; mergers; BBN and recombination; CMB; the separate network thermal-origin hypothesis; and independent synthesis.

**The current bridge target.** It is "one physically normalized action and causal state connecting record dynamics, material gravity and cosmic evolution. The clean native120 and new43 remain unstarted ... their connection and physical normalization remain the open middle" (LAD:5-9). As of 2026-10-11 and 2026-10-12, "No candidate has passed all four physical screens" (CS:9). A mandatory member-identity hold (CS:129-137) found the PackedNative restored_bs11 member identical to the old rejected primitive. Physical size ladders are HELD.

---

## 2. Area: RECORDS (definition, existence, formation, record laws)

### 2a. Derived or established

**Corner tier: the exact five-clause definition DEF-A, all FORMAL.** These are theorems about the stipulated object.
- **C-12, the existence characterization.** A record satisfying (i)-(iv) exists **iff** the commutant of alg{I,H,L_k,L_k†} contains a projection that is non-trivial on some eigenspace of H and trace-balanced. Verified 210/210 exhaustively (L:81). The external review called it "the single result defensible before a hostile committee with no caveats beyond scope" (R:9070). Its supporting lemmas:
  - C-9, Lemma 0 (L:78).
  - C-10, Theorem O1-A (L:79).
  - C-11, Theorem O1-B: in an odd-dimensional Hilbert space no record is ever writable (L:80).
  - C-16, the carrier-free Balance Lemma (L:102).
  - The naive converse is FALSE (O-1, L:17).
- **C-4 and C-22: no structural condition narrower than the clauses is necessary.** Records with verified writers exist in dimension 6 with no qubits, no stabiliser group, no cells and **no homology** (5 of 5). Homology of an F2 complex is *sufficient, not necessary* (L:9, L:143).
- **Degeneracy and symmetry.**
  - C-1: records require exact degeneracy (L:6).
  - C-2: 0-form symmetry splits linearly (MEASURED, L:7).
  - C-3: a 1-form symmetry splits only at order d (L:8).
  - O-6: the 1-form symmetry is exact in the carrier (FAILED as an "emergent?" question, L:22).
- **Count, writer and protection on the toric carrier.**
  - C-5: 2^2g records, independent of area (BORROWED from Kitaev, L:10).
  - C-6: a writer always exists and is never local (L:11).
  - C-7: nothing local writes or destroys a record (L:12).
  - C-13: the corrected P-3, "no admissible writer fits inside one contractible region"; the strong reading is FALSE (L:83).
- **C-15: four clauses are carrier-free.** Clause (v) needs locality data, which belongs to the carrier (L:100).
- **Clause (v).**
  - C-64 gives an exact decision procedure; (v) FAILS on the open chain (L:225). The review judged it "publishable-lemma-grade" (R:9073).
  - C-74: (v) holds on the toric code by manifold homology over 1480 regions with no convention needed (L:241).
  - C-89: (v) holds on the D(D4) proxy through a genuinely non-abelian integer obstruction (L:267).
- **C-41: records exist on D(G) exactly when |G| is a power of two.** The obstruction is the group's order, not its commutativity (L:187). The review called it "one short proof away from a genuine original theorem" (R:9072).
- **Formation, corner tier.**
  - **The threshold equals d.** F-11 confirmed it at d=2; O-10 says it is "now PROVED for every stabiliser code and every coupling" (L:63, L:67). F-22 explains why, via Knill-Laflamme (L:108).
  - **F-13 names two requirements:** a coupling of weight ≥ d, and that coupling must not commute with the writer. An ordinary thermal environment suffices (L:65).
  - **F-20, the mechanism:** the environment's evolution is conditional on the record value. "The record is READ, not written" (L:104).
  - **The arrow:**
    - F-17: the arrow carries the threshold (L:87).
    - F-18: the arrow is not ambient decoherence (L:88).
    - F-19: irreversibility is relative to system-only operations (L:89).
    - T-III.6: the arrow is relative (L:29).
  - **Redundancy:** F-21 (L:105); PF-2 closes the dynamical before/after and redundancy (L:92).
  - **The channel:** G-16, a coupling opens a channel iff its code-space compression has a component along the record (L:122). C-17: clause (ii) is a condition on the environment (L:117). C-18: gauge invariance plus locality forbid formation (L:120).
  - **Records compose:** C-19 (L:135); T-I.4 (L:31).
  - **PF-5:** an ordinary local environment forms records at order λ^(2d) (L:95). The F-23 refinement says the exponent is 2n*, not 2d (PARTIAL, L:109).
  - **A-EM2 and A-EM3:** the minimal forming coupling, the record and the writer are all EM holonomies (L:68-69).
  - **F-26: distance protects against static perturbation, not dissipation.** The row concedes this is NOT OURS, standard QEC (L:114).

**World tier: real records.**
- **H-3 answered with a number.** Zero of 13 real records (zero of about 20 across four censuses) satisfy the five exact clauses (L:128; R:8991-9008). Exact (ii) and (iii) together are "jointly unsatisfiable in generic matter" (R:9010-9014; C-66, L:231).
  - C-67: the one record satisfying (i)-(iv) exactly, the CMB photon's polarisation, is the least protected object (L:232).
  - C-68: the world uses energetic and kinetic protection, while the exact clauses assume topological protection (L:234).
- **C-69: a CoCrPt HDD grain is a record under the amended clauses and not under the exact ones.** FORMAL; the law is BORROWED from Néel/Brown and is "reproduced not predicted" (L:236; R:9191-9246).
- **C-70: ⟨R⟩_ss = tanh(dE/2kT).** It is an exact identity of any two-state detailed-balance GKSL record. FORMAL, BORROWED, demoted from PROVED (L:237). The azobenzene and alanine rows were withdrawn.
- **C-71 is PROVED, on the encoding-level accumulated quantity of a formed record surface** (L:238):
  - On a NAND page, occupancy-encoded net trapped charge is one-signed for every data pattern.
  - A DC-saturated CoCrPt track carries remanent moment, but only under DC saturation; real data tracks screen (measured ratio 0.00096).
  - Falsifier: a programmed NAND page whose net charge carries the erase carrier's sign or depends on the data pattern (a Vt shift); or a DC-saturated medium with no remanent moment above the AC-erased background (VSM).
  - TWO-CARRIER: NAND floating gate and macrospin CoCrPt.
- **C-75: DEF-A is the limit of the amended definition, verified rather than asserted** (96/96, 1536/1536, 24/24; L:243; R:9437-9455).
- **C-86: the surviving-record count law k(t_m).** FORMAL, ownership PARTIAL (L:263; R:9824-9848).
  - The width is derived from clause (ii') on the record's own Liouvillian mode.
  - The departure term Σ_dead tanh(dE_i/2kT) is "wholly owned".
  - **External run, NOT-YET-COMPARABLE:** five ordinal/sign rows AGREE, all in conceded territory, and every absolute row is blocked by vendor-held calibration. Promotion does not fire (R:10425-10460).
- **C-73: the only exact obstruction is that writes are bijections.** Responsive parts have zero orbit sum and both signs. Mean zero does not mean cancellation (L:240).
- **URFT-1: Universal Coverage-U is an exact theorem inside the adopted U-DCL physical axiom system.** Outcome selection, Born probabilities, collapse, gravity and numerical alpha stay separately typed (L:283; CG:10).
- **C-84: three distinguishing survivors**, listed in §1 (L:260).
- **C-85: the URM entry point is built and adversarially confirmed for its declared machinery, not for every headline.** The current aggregate exits 1, failing only on two zero-weight replay contracts (L:262).

### 2b. Adopted (definitions, decisions, premises)
- **DEF-A, the five clauses.** H-3 is PARTIAL: "THE DEFINITION IS WRITTEN, NOT DERIVED ... why THIS definition remains the open question" (L:128).
- **"Admissible := [U,H]=0" (O-4, DEFINED, L:20).** It is PROVISIONAL; T-25 is TODO (P:26).
- **O-12:** "admissible" inserted into clause (v) (L:82).
- **O-49 (the principal's decision):** for 1D rings only, clause (v) uses proper sub-regions. The toric code is the canonical benchmark (L:227). D-23 governs proxy scoping (L:230).
- **O-51, the amended clauses (i')-(v') on carrier ⊗ local bath, adopted 2026-08-20** (L:233; R:9119-9187).
  - (iv') admissible becomes an energy-conserving dilation, with the cost reappearing as free energy ≥ kT ln2 + dE_config.
  - (v') protected means every single-region flip costs ≥ E_b with E_b/kT ≫ 1.
  - DEF-A is named the exact corner T→0, t_m→∞, W=0, E_b→∞.
  - The grounding clause converts H-3, H-5 and H-6 into standing acceptance criteria.
- **H-6 answered conditionally:** records are macroscopic because the amended clauses demand a macroscopic bath (L:131).
- **The PROVED bar was raised twice before rows were scored:**
  - PROVED requires a measurable quantity, a prediction and a falsifier (SV:2).
  - Then RECORDS VERIFIED must name at least two structurally different mechanisms (R:9388-9393).
- **The C-72 ruling (Option A, the principal):** C-72 stays PARTIAL, blocked by T-50; "stop trying to rescue an absolute single-page ratio" (R:10238-10288).
- **U-DCL physical axiom**, adopted 2026-08-25 (L:283) **[reviewer, AL:97: "adopted_postulate · low"]**.
- **[reviewer] Rung 2-3 adoption notes** (AL:85-110). The reviewer flags:
  - the 1 cm³ bath size in (iii'), which the tree-ring census row would fail by about 6e14× (AL:91);
  - the inserted Arrhenius rates, which make C-69 and C-70 identities (AL:103);
  - the D-25 azobenzene gate as an Eyring round trip (AL:106);
  - the C-71/C-72 promotion as criterion_after_results (AL:94).

### 2c. Failed or withdrawn
- O-1: the naive converse is false (L:17). O-3: the exhaustiveness side-step is refuted (L:19).
- PF-6: no distinguishing prediction (FAILED, L:96).
- F-24 "one quantity, four roles" is WITHDRAWN as a check that cannot fail (L:110). F-25 λ^(2d) is WITHDRAWN; the exponent is 2n* (L:111).
- The C-14 count law collapses under generic asymmetry (C-76, L:244). The T-31 width fix was refuted and withdrawn (R:9516). C-14 now survives only as a corner of C-86 (PARTIAL, L:99).
- C-69 and C-70 were demoted from PROVED. PROVED rows briefly fell to 0 (R:9506-9520).
- C-72 was demoted to PARTIAL. Both T-50 designs were refuted, but "no runnable form" is NOT the verdict (L:239; R:10464-10495).
- The real-world records fail DEF-A (H-3, L:128).

### 2d. Open
- **Why this definition?** T-53 TODO (P:54); H-3 PARTIAL.
- **What admissible means:** T-25 TODO (P:26); the physical-channel reading O-45 (L:216).
- **The C-72 observable:** T-50 TODO (P:51).
- **External data for C-86 and C-69/C-70.** The SMTJ dwell-time route needs an access request, and filing it "is the principal's action" (R:10453-10457).
- **Objectivity:** O-21, which needs equivalent fragments (L:138).
- **Measurement as record creation:** T-V.3 (L:30) and F-7 (L:59). D-4 says formation and measurement are the same question (R:5252-5257).
- **The classical limit:** T-V.4 (L:32).
- **Formation as dynamics:** F-4 (L:55).
- **The necessary condition:** PF-4 (L:94).
- **Reproducibility:** PF-8 (L:98), T-35 (P:36), T-18 (P:22).
- **[reviewer] Background time t:** "125 of 125 lanes evolve in t. Zero derive it" (AL:79). This applies to every rung.

---

## 3. Area: ADMISSION (the microscopic owner-once rule)

**Established**
- **The L4 intrinsic-admission theorem:** target 10/10, independent reconstruction 12/12, final hash-pinned hostile verifier 50/50 (R:10994-10997).
- **"A concrete admission mechanism exists inside its declared prism parent."** It does *not* automatically provide the same-parent physical q4 carrier/EM/geometry registration (LAD:41).
- **The coherent same-port writer:** the third-write decrease W3 = −0.2840663550582732, exact for the historical L4 case at κ=π/2. It is LIMITED to that declared history; "the broader generic obstruction is not established" (LAD:40).
- **pi/8, 66/66 covariance transfer:** "verifies the stated algebraic admission identity and its implementation; it is UNINFORMATIVE as an independent physical prediction" (LAD:40).

**Adopted**
- **Owner-once prism admission is "an adopted microscopic rule"** (LAD:40).
- **[reviewer] Items AL:74-79:**
  - write angle Φ=π/4 (a definition);
  - transport dwell κ=π/2 (hand-set, with no κ sweep);
  - the intrinsic admission parent (post-failure);
  - the one-pass cursor (post-failure, high risk), where "Nonnegative accumulation is guaranteed by stopping, not proved";
  - the genesis initial condition (hand-set).
- **LAD:167-172:** "The actual prism admission mechanism transfers a declared resource; a matched physical q4 admission/source map is not owned merely because the same word carrier is used."

**Failed:** coherent unwriting is retained as a failure (LAD:175).

**Open**
- The fixed L4/L6/L8 and κ=1/π/2 recheck has not been executed (LAD:40).
- A self-replenishing autonomous genesis law **[reviewer, AL:77-78]**.

---

## 4. Area: ALPHA

There are **two alphas**, and they must not be conflated (A-PR, L:5; H-2 superseded, L:127):

1. **Generic perturbation "alpha" in the DEF-A corner.**
   - A-AL: a sum of local terms that splits the record space at order n* (L:4). C-8 (L:13). T-14 measured both exponents on three carriers.
   - T-22 DONE: "alpha" there names a generic coupling (P:16).
   - D-13, "alpha names a magnitude, not a constant", was WITHDRAWN and superseded by the two-alpha split (L:142).
2. **Physical fine-structure α, row A-AL2 (FORMAL, L:273).**
   - **ALLOW:** an exact construction-scoped admitted interval, I_χ ∩ ((−ln(1−δ))/(4πB²), ∞).
   - **REQUIRE:** for same-sector ACTVIS records under SAI1-SAI8, with independently established governing-domain ancestry, records inherit that domain's empirically anchored α and RG trajectory "as constitutive identity; changing alpha defines a different governing domain."
   - **SELECT** is separate and open.
   - The row is NOT-CARRIER-SHAPED. 1/137 is not derived (L:127).

**Established**
- The A-AL2 typing theorem (L:273). A-PR includes it (L:5).
- C-84 S-2: one flash device carries an α-amplified Arrhenius channel (A ≈ 240) and an α-flat tunneling channel. This is a falsifiable mechanism discrimination (L:260).

**Failed or withdrawn**
- "The prior forced-alpha claim was withdrawn" (LAD:66).
- The historical "alpha FREE" verdict is LIMITED and underpowered (LAD:32, LAD:66).
- The amplification logic belongs to Shlyakhter/Damour-Dyson (Oklo), and record-derived α bounds are uncompetitive (every predicted shift is < 3e-4 in ln τ) (L:260; R:9793-9795).

**Adopted:** **[reviewer, AL:116-120]**
- the SAI1-SAI8 premises (imported, low);
- the empirical α anchor (calibrated to data);
- the cavity witness parameters e1=3/10, e2=3/5 (hand-set);
- "form required, magnitude allowed" (an unproved bridge framing, medium).

**Open**
- **T-38:** how α's value enters the record laws through the barrier (TODO, P:39).
- **LAD:67:** "Neither local alpha nor Poincare generator counts select a 3/7 partition, absolute length/volume or cosmic energy share. Such a proposed partition stays a supplied premise until an actual action selects it."
- **[reviewer] AL:116:** emergence of compact U(1) and the EM action from record formation is open.

---

## 5. Area: FINITE UNIVERSE (finite relational accumulation, the ARGER Gate, lineage)

The relational family is defined at R:11024-11032:
- L is the even size and one-pass horizon of an owner-once periodic-prism parent;
- the parent has L genesis cells, 2L carrier sites and 3L transport edges;
- the 13 (L,q) visibility rows span five independently constructed parents.

**Established (FORMAL or MEASURED, all on one carrier family, "finite-relational-accumulation")**
- **RA-1, the exact L12 custody.** Target and Hostile agree on 1156/1156 comparisons. Strict common-lineage support is 0.11570852222694002 (L:275; R:10871-10877).
- **RA-5, the exact L4-L12 extendible record-block theorem.** Deduplicated masses are 0.7260, 0.5847, 0.7374, 0.6501 and 0.5696, each > 0.50, bounded to five sizes (L:279; R:10924-10932).
- **RA-6:** all 13 (L,q) sectors have positive finite probe visibility; the minimum R_low is 0.4280947 (L:280).
- **RA-7:** under the *adopted* ARGER Gate, RA-5 plus RA-6 establish the finite GFT z=1 phase at L=4..12 (L:281).
- **RA-8:** under the explicitly pinned Luttinger premise LL-P, z=1 holds throughout the density interval. It is a supplementary conditional theorem (L:282).
- **RA-9:** Target and Hostile both reproduce a nonzero *two-sided* lineage-carrier association through L12. The signed positive no-decline prediction **fails decisively**: the sign reverses and the magnitude declines (L:284; R:11066-11127). A 10,748 s release skew is disclosed.
- **RA-11:** one fixed L4 lineage-sensitive carrier continuation mechanism, Δ_C = 0.147611857. There is no size persistence, scaling or geometry (L:286; R:11166-11198).
- **RA-3:** a strictly increasing common-lineage support diagnostic at L08, L10 and L12 (L:277). No monotone-continuation theorem is claimed (R:10885-10890).
- **The claims grid G-H is FORMAL-COMPLETE** (CG:9). G-G is FORMAL-COMPLETE (CG:8).
- **LAD:76:** formation/state and full phase/current mechanisms have reusable owned finite evidence. The M10-to-M12 occupation-cutoff checks pass; the M4/M6 and M8/M10 failures remain (LAD:145-149). "Occupation cutoff is not physical universe expansion."

**Adopted**
- **The ARGER Gate as the governing finite GFT z=1 standard**, by principal decision on 2026-09-16 (R:10943-10949). Its criterion is exact bounded membership, deduplicated mass > 0.50 and positive visibility.
- **[reviewer] AL:126-145 flags most rung-5 items as criterion_after_results.** For example: the Gate was adopted one day after the Stage-6R2 rejection; the A009-A016 band was selected after results; clauses (1) and (3) "cannot fail"; the "z=1" label is not a derived dispersion.
- **The program's own label** is "ARGER pass: ADOPT gate membership / CERT implementation; UNINFORMATIVE as physical criticality evidence" (LAD:31). LAD:75 adds that ARGER passes "certify membership in an adopted finite gate, not physical criticality or z=1."

**Failed or negative**
- **RA-2, the historical Stage-6:** AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12 for its own classifier. This is a finite-sector rejection, "not a general no-go theorem for z=1, a continuum, emergence, or gravity" (L:276; R:10879-10883).
- **RA-10:** the L8 Ollivier-Ricci controlled null, ρ = 0.154 and p+ = 0.362 (L:285; R:11129-11164). LAD:34 calls it UNINFORMATIVE for emergent geometry.
- **RA-9:** the signed-persistence prediction failed (L:284).
- The retained failures listed at LAD:175-179 include the criticality and z=1 preregistration, signed-persistence reversal, and the stationary-clock failures.

**Open**
- **RA-4:** L14 is INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT. It is not a premise (L:278).
- A premise-free uniform all-L z=1 theorem "remains a stronger open result" (R:10951-10955).
- LAD:30: the preregistered z=1 test needs a known z=1 positive control.
- LAD:29: common-lineage rise needs a discriminating ordinary-history null.
- LAD:28: lineage-changes-dynamics has an incomplete independent discriminator.

---

## 6. Area: GEOMETRY / Γ / GRAVITY EMERGENCE (emphasis)

### 6.1 Γ defined by function

- **Γ is defined only by function** (A-GR, L:3; G-5, L:40):
  - **R1** supplies record space (2^2g);
  - **R2** supplies the writer, which is non-local;
  - **R3** supplies protection.
- **G-1** defined the third term as (H_1(Σ), intersection pairing) and is WITHDRAWN as a definition (L:14). **G-5** demotes that object to a candidate that satisfies R1-R3 (L:40).
- **G-6 is FAILED: "IS THE THIRD TERM UNIQUE?" Uniqueness was tested and broken** (L:41; R:5173-5216).
  - **Survivors:** H_k of an *arbitrary* F2 chain complex (DECISIVE); asymptotically good qLDPC, which is "Not a manifold ANYWHERE" and exceeds Delfosse's surface bound by Θ(n²/log²n) (STRONG); the 3D toric code (STRONG).
  - **What died:** "records require a SURFACE". What survived *at that time* was "records require non-trivial homology". **Later, C-4 and C-22 withdrew even that** (L:9, L:143).
  - R3 needs two numbers (systole and cosystole). "The single distance was an artefact of the carrier we chose" (R:5199-5201).
  - The erratum G-13 says the writer is not Poincaré duality: the evaluation pairing is perfect over any field (L:48).
  - The fracton coverage gap O-7 was later swept: fractons widen nothing (L:49).
  - **D-4 then ruled** that asking what *produces* growing minimum weight is asking what produces a permission, which is a category error. F-2 was withdrawn and F-7 became the occupancy question (R:5220-5264).
- **The Γ capacity facts:**
  - G-7, the capacity law as an index N = dim H0 + dim H2 − χ (PARTIAL, L:42);
  - G-8, the constraint puts the total at the boundary (perimeter law) (L:43);
  - G-9, the record space is Z1/B1 (L:44);
  - G-10, capacity survives off manifolds (L:45);
  - G-11, capacity and protection are independent (L:46);
  - G-14, Γ is a requirement on EM's complex (DEFINED, L:70);
  - G-15, the condition is restated in clause (v)'s binary terms, with no growth requirement (DEFINED, L:75);
  - G-12 is WITHDRAWN (L:47).
- **G-2:** records = 2 − (1/2π)∫K dA on closed orientable carriers (PARTIAL, L:15). The register says plainly: "That is a relation, not an emergence: the geometry is input on both sides" (R:6783-6785).
- **X-rows:**
  - X-1 "the topology is a LATTICE's" is NOT OURS (L:23).
  - X-2: χ is a parameter. It was RECLASSIFIED at the record level, and the collective-level question was explicitly left open and moved to C-77 (L:24).
  - X-6, "is the record-level constraint gravity's?", is WITHDRAWN as an import (L:28).
  - X-3 and X-5 are NOT OURS (L:25, L:27).
  - X-4 is BLOCKED (L:26).

### 6.2 The channel: the second half of Γ at work
- **O-20 answered:** χ > 0 iff the coupling's cycle pairs oddly with the record's conjugate (four for four). Every boundary gives exactly 0 (7/7), and non-boundaries split (R:6619-6665, R:6717-6729).
- **A-GR2 (DEFINED):** "Gamma supplies the channel ... classical gravity is what Gamma becomes at scale" (L:123).

### 6.3 T-20 and the holonomy route (record-level curvature)
- **T-20:** "DOES CLASSICAL GRAVITY EMERGE FROM RECORDS?" It was DONE against its DONE_WHEN: a many-record collective quantity defined, computed, and shown either to satisfy a constraint of the right type or not, with the classical form never used as a criterion (P:17).
- **H-9, the principal's T-20 criterion (DEFINED, L:144; R:7331-7367).** Gravity emerging from Γ would look like **record-level holonomy**: H_ABCD = (Γ_AB Γ_BD)(Γ_AC Γ_CD)^-1. The criterion was supplied before any measurement. The further signatures the principal named:
  - the mismatch is local and smooth;
  - it is universal across record types;
  - it is phase- or action-based;
  - it is stronger with enclosed record density;
  - it is causal;
  - it obeys a Bianchi-like closure;
  - there are geodesic-deviation and visibility analogues.
- **The T-20 result: exactly flat on [[8,3,2]]** (R:7371-7403). The writers commute, so the holonomy group is abelian.
- **O-23 overturned the interpretation.** The connection is *not determined by the records*. The same family gives holonomy 0 for one admissible writer and up to 5.169 for another (200 of 200 admissible). The T-20 measurement stands; "its interpretation is withdrawn" (R:7430-7464; H-10 PARTIAL, L:145; O-23 FAILED as a question, L:146; H-11 OPEN, L:147).
- **Minimality and least action select flat writers:** O-24 (L:148), C-23 (L:149), C-24 (L:151), C-25 (L:156), C-26 (L:157). O-25 "density forces curvature" FAILED (L:150). H-12 FAILED (L:153).
- **The principal caught an import in the negative result itself: "THE WRITER WAS TREATED AS THE CONNECTION."** C-24, C-25 and C-26 are facts about *writers*. They do not touch transport *between* records, which is what H-9 asked about. "**under the five clauses Γ does not produce gravity** is WITHDRAWN as stated" (R:7719-7750). D-14 records the lesson (L:159). H-13 stays OPEN (L:158).
- **The principal fixed the connection as Candidate 3, transport along the carrier** (H-14, DEFINED, L:160; R:7780-7812):
  - the intersection pairing plays the topological source, T_μν;
  - channel_map plays the metric/propagator, g_μν;
  - carrier frame transport plays the curvature, G_μν;
  - "R[carrier transport] ∝ ⟨c_i,c_j⟩ × channel_map[α]".
  - The GR symbols are labels only.
- **H-15 and C-27, measured on the right object:** on the toric carrier, carrier curvature (plaquette holonomy) and record content are **independent in both directions**. "THE TRIAD'S PROPORTIONALITY HAS COEFFICIENT ZERO HERE" (L:161-162; R:7816-7868). **C-28:** a Bianchi-like closure is present in the carrier, but it is not coupled to content (L:163).
- **O-29: the abelian carrier has nothing to rotate.** "Every prior null on the emergence question was measured where the effect is zero by construction" (L:164; R:7872).
- **The move to non-abelian carriers:**
  - C-30: S_3 flux transport is path dependent (on group elements, not records) (L:166).
  - C-40: D(S_3) has no records (L:184).
  - C-41 and C-42: D_4 is a non-abelian carrier that has records (L:187-188).
  - C-43 and O-36: transport moves *randomly constructed* records; transport-fixed records exist (L:189, L:191).
  - C-51: both kinds coexist on the same carrier (L:204).
  - O-34 is PARTIAL (L:181). O-41 is OPEN: protection is transport-blind at proxy size (L:206).
- **Count is the wrong density variable:**
  - C-32 (mixing limit, L:170);
  - C-35 (count and intersection number are topological) (L:174);
  - O-30 and O-31 (L:168, L:172).

### 6.4 The source side: density, sign, accumulation
- **C-46 sets the discriminator (DEFINED):** the test for a gravity-role quantity "is not whether it grows but whether it fails to cancel" (L:193). D-19 says to compute sign over the integers, not F2 (L:194).
- **The integer intersection pairing is two-signed and cancels more** as records are added (C-45, L:192).
- **The crowding suppression is sign-definite but BOUNDED.** The whole accessible-information family is bounded by log2 dim(B), independent of N (C-48 THEOREM, BORROWED Holevo, L:197; O-37 resolved, L:195). C-36 is the Holevo bound (L:176). C-37 is WITHDRAWN (L:177).
- **C-47:** the bath-induced effective potential is strictly extensive, additive and not a count; it is the first quantity to meet the source standard (MEASURED class, L:196). **O-40 (OPEN):** it is bought at the cost of independent writability (L:202).
- **Correlation energy:**
  - C-58 and C-59: the configuration energy lives in correlations between records (L:217-218).
  - O-48 FAILED: the correlation energy is "NOT A SOURCE ... BY FORM" (L:219). C-61 shows it is record-blind (L:222). C-62 shows it cancels by an exact closed form (L:223).
  - C-60: admissible implies dE=0, which is circular under DEF-A (L:221).
  - C-63: an induced 1/(πr) falloff on a gapless mediator, BORROWED (1D RKKY/Lindhard) (L:224).
  - O-38: the earlier falloff demand was rescoped as an import (L:200).
- **O-42, the durability-geometry exclusion, FAILED, overturned by O-47** (L:211). C-56, the Schur direction, stands (L:213). **O-43 is OPEN:** is the exclusion complete for proper-subalgebra carriers? (L:214).
- **C-52, the Z[i] quantisation theorem, is true of DEF-A's corner.** Its physical conclusion is withdrawn twice over (L:207). C-70 and T-30 show that thermal expectations are unquantised. The solidity review corrected this: which functional carries the physical exclusion is **UNDECIDED** (L:237; R:9515).
- **O-50 FAILED, the candidate refuted.** What survives is Burnside, and "mean zero" is not "cancels" (L:228; R:9338-9384). **O-53 is OPEN:** does a durable operator exist whose extensive part is not proportional to the identity? (L:242).
- **The world tier, T-32: all five source standards are met on a real record** (R:9300-9334):
  - extensive;
  - additive;
  - not a count;
  - **sign-definite, "supplied by the act of record formation itself"**;
  - power law with exponent −3. The limit is stated sharply: "This is magnetostatics ... exponent is −3, not gravity's −2."
  - This became C-71 (PROVED) and C-72 (PARTIAL) (L:238-239). C-72's kernel: occupancy-encoded surfaces accumulate for every pattern, while orientation-encoded surfaces screen for real data.
- **O-52 (OPEN):** the energy route to a gravity source reopens under the amendment, because under (iv') writes pay work (L:235).

### 6.5 The C-77 emergence claim and its increments (rows C-77 to C-93)
- **C-77, CANDIDATE (L:248):** the classical/continuum field-recovery claim, adopted 2026-08-20 (R:9539-9563). Increments:
  - **Increment 1 SATISFIED at form level (C-79).**
  - **Increment 2 SATISFIED (C-80).**
  - **Interface-vs-content resolved surface-determinedly (C-81, C-82, C-83).**
  - **Increment 3 SATISFIED at family level (C-87, C-88), with C-90 closing the D=3 member.**
  - The verdict: **"NEWTON VERDICT: MATCHES AT MEMBER LEVEL"**, which supersedes NEITHER. It is "Never a claim that continuum or Einstein gravity is empirically derived."
  - The conditional structure stays load-bearing:
    - unique critical member: computed;
    - occupancy of criticality: PARTIALLY EARNED (C-91; the judge's call, with ratification by the principal not recorded, R:10071-10074);
    - design-point enforcement: NOT earned (O-58 N3);
    - norm selection: open (O-58 N4).
  - Also remaining: the universal coefficient (O-55), the thermodynamic pair (O-56) and the collapse analogue (O-57).
- **C-78, FORMAL: distance is earned on the record surface, and it is literally boundary-crossing cost** (L:249).
  - d_W is the minimum admissible-writer weight; it is a true metric, checked exhaustively (2^24 writers per pair at L=5).
  - "THE METRIC AND THE GAMMA-FORM ARE DISTINCT" exact structures with a common crossing origin.
  - Dimension is earned as computed content degree: 2 for the corner, 3 for the world.
- **C-79, CANDIDATE: increment 1** (L:250; R:9612-9645).
  - deg IR = deg C − 1 in both tiers. The parameter-free forms are 32·capP = (IR2+10)² + 8(IR2+10) − 160 and IFACE³ = 216·CAP².
  - The mechanism is exact bulk cancellation, with Euler density per interior cell 1+1−2 = 0.
  - It MATCHES IN FORM the area/entropy-boundary law, with owners named (the stabiliser perimeter instance is BORROWED from HIZ and Kitaev-Preskill).
  - Scope: what matches is the *interface* aggregate. Stored content is volume. The coefficient depends on the venue (32 vs 216).
- **C-80, FORMAL: no pure-Γ falloff exists; the division of labor is computed** (L:254; R:9674-9708).
  - Pure-Γ two-region relations are exactly: zero beyond contact; contact seams; topological constants (TEE −1); switches; and one GROWING law, **w_min = d** (confinement character, "NOT gravitational").
  - **Γ shapes the boundaries. The coupling supplies reach and falloff, which is the LOCUS where a Newton form would have to live; the exponent is inserted, not earned. Alpha supplies the costs.**
- **C-81, FORMAL:** certifiability is the interface. CERT equals the stabiliser cut-rank; HIDDEN = STORED − CERT is volume. It also introduces thickness protection 1,2,1,0 (L:255).
- **C-82, FORMAL:** in the world tier, the boundary bounds the certification **rate** (6n²−12n+8, an exact min-cut), not the total (L:256).
- **C-83, FORMAL: "THE SURFACE OWNS THE CLOCK."** CERT_W(n) = min(n³, W·(6n²−12n+8)) with W = τ/t_epoch (L:257; R:9742-9761).
  - Certifiable content is boundary-bounded at scale for any finite-lifetime surface. W=∞ is DEF-A's corner.
  - The honesty clause: terrestrial devices certify their full volume within their lifetime.
- **C-84 S-1** is the related distinguishing survivor (L:260).
- **C-86:** the count law, covered in §2 (L:263).
- **C-87, FORMAL: the reachable-class statement** (L:264; R:9852-9861). A Γ-constrained coupling reaches exactly three classes:
  - exponential below μ_c;
  - at μ_c = 1/deg, the earned dimension's own point-source potential, because "the gated resolvent identity at criticality IS the venue's discrete Poisson equation". It is computed as linear in D=1 and log in D=2, and as 1/d in D=3 (via C-90);
  - divergent above μ_c.
- **C-88, FORMAL: the Newton composition profile exists at exactly one design point, R1 (endpoint-transparent admissibility) plus OCCUPANCY encoding** (L:265).
  - The profile is exact superposition, one-signed accumulation, no screening and no shadowing.
  - Orientation encoding gives the EM-like two-signed, screenable profile.
  - Whether the surface enforces R1 + occupancy is UNDECIDED (O-58 N3).
- **C-89:** clause (v) on D(D4), covered in §2 (L:267). D-27 records that two readings of "protected" diverge (L:268).
- **C-90, FORMAL: the D=3 critical member is 1/d** (L:269; R:9961-9998).
  - The venue is the census access geometry's deg-6 grain lattice, with μ_c = 1/6 exact.
  - The exponent bracket contains 1, and the coefficient bracket tightens onto 3/(2π). The owners (Spitzer, Watson) were consulted for comparison only, after the class was computed.
  - Caveats kept: the exponent is a bracket statement, not a symbolic derivation; the 1/d is exact in an emergent Euclidean norm over earned L1 separation; "NOTHING in Gamma yet places mu at criticality".
  - **SINGLE-CARRIER: "the Newton-verdict chain's head stands on one venue"** (R:10367-10371).
- **C-91, FORMAL: MASSLESSNESS IS MEASURE CONSERVATION** (L:270; R:10049-10080).
  - The unitary writer algebra conserves measure for every ensemble weighting, and every conserving kernel is exactly critical.
  - World tier: E1 transport is critical at every dE. E2 trail-with-retreat conserves, but is uniform only at dE=0. E3 trail-with-decay is never critical; its mass gap is ln(μ_c/μ) = ln(1 + e^{dE/kT}/l). "Bias is mass."
  - **The obstruction, plainly:** μ = μ_c is NOT derived on the physical surface. Which ensemble GR3 writing enforces is **one computable bit (T-49, TODO, P:50)**.
  - The anisotropy frontier N5 is uncomputed.
  - TWO-CARRIER (R:10372-10375).
- **C-92, DEFINED: the field-side instrument is identified** (L:271; R:10292-10358).
  - **"The Second Lump"**, F(D) = Δ(b=−1;D) − Δ(b=+1;D): the written-value differential of a probe record's own law at earned separation. It is literally O-39's named minimum.
  - Pre-registered rule V1-V5. If V1 is FALSE, the field-recovery claim is registered "exhibitable-not-provable".
  - "An instrument is identified; **no field has been measured**" (R:10340-10342).
- **C-93, FORMAL: the earned metric is content-rigid on stabiliser venues** (L:272; R:10392-10421).
  - "THE INTEGER TIER CARRIES NO FIELD, AND THE RESPONSE LIVES ONE TIER DOWN."
  - The named next step is the responsive venue: "does one written record shift dE for an adjacent write in the E1/E2/E3 writing tier? (bias is mass)".
- **Rows "C-94" and "C-95" do not exist.** A drafted C-94 row, a drafted C-77 increment and a drafted T-51 completion were **rejected** at the T-51 quarantine correction. The old all-pass is inadmissible; V2 is UNSCOREABLE; the disposition is PARTIAL POSITIVE / REPAIR REQUIRED, which is administrative, not a terminal branch. No field result enters the URM (R:10797-10867).
- **The classical/continuum field-recovery claim (H-1 PARTIAL, L:126).** It "is not answered". **H-8:** X-2 does not foreclose accumulated or enlarged-parent emergence (L:133). **H-7 (OPEN):** a conditional carrier-formation form (L:132).

### 6.6 Conditional gravity formation and the macroscopic bridge
- **GFT-1, FORMAL:** record-first Gravity Formation Theory "closes an exact implication under adopted RGRL and WTC-H1-H5". RGRL's empirical confirmation, the microscopic F3 derivation, the strict induced origin and a parameter-free numerical G **remain open**. No graviton premise is required (L:274; CG:8).
- **The UNT master closure theorem (2026-09-19)** is an exact, type-preserving composition with no added axiom. Each component keeps its own domain and premises (R:11040-11064).
- **LADDER rung 6** (LAD:88-100):
  - "RGRL is an adopted soldering premise; conditional Einstein closure and Ward/response theorems keep their stated ceilings. Minimal record-to-link response is not itself a physical metric."
  - Same-parent physical current/stress, ruler/Birth volume and complete causal state still require an admitted effective member.
  - "Rank/alpha/dimensionless response cannot silently fix the physical ruler or stress normalization."
  - Gap B (5→6), the full native normalized metric bridge, is OPEN (LAD:132-134).
- **[reviewer] AL:151-173:**
  - RGRL is an adopted bridge (high);
  - D=4 comes via MARGINAL-ALPHA;
  - G_obs is calibrated to data;
  - WTC-H3's Lovelock premises are a strong structural hypothesis;
  - Λ_eff's C_0^eff is unfixed;
  - the GL6CR Ward null is an imposed target condition;
  - in the minimal join, λ_R is set by hand and the sign reverses at s=2 (AL:166);
  - μ_c = 1/deg with R1 + occupancy is hand-set (AL:171).

### 6.7 What is open in the gravity/Γ area (the work queue)
- **T-49 (TODO):** the conservation bit of GR3 writing (P:50). It decides masslessness and the design point (O-58 N2/N3, L:266).
- **T-51 (TODO):** a field-side observable with an unwritten positive control and a falsifier (P:52).
- **O-39 (OPEN):** "EVERY LANE HAS MEASURED SOURCES; NONE HAS MEASURED A FIELD" (L:201).
- **O-58 N3, N4, N5:** the design point, norm selection, and the anisotropy frontier (L:266).
- **C-90's second D=3 venue** is owed (R:10387-10388).
- **The responsive-venue question** (C-93, L:272).
- **O-55:** no universal coefficient, nothing yet playing the role of 1/4G (L:252).
- **O-56:** no earned thermodynamic conjugate pair (L:253).
- **O-57:** the emergent content bound, the collapse analogue (L:258).
- **O-53:** the extensive durable operator (L:242). **O-43:** completeness of the exclusion (L:214). **O-40:** source vs independent writability (L:202). **O-52:** the energy route under (iv') (L:235).
- **O-41:** transport-fixed vs transport-moved on a larger non-abelian lattice (L:206).
- **O-26** (L:152), **O-33** (L:178), **H-11** (L:147), **H-13** (L:158).
- **T-26 (TODO):** re-audit every registered null against the venue rule. Each null must cite a positive control, or be rescoped to absence within range or absence in this venue (P:27; D-15 L:169, D-17 L:183, D-22 L:210).

---

## 7. Area: GALAXIES

**Established (CERT, real data, effective level)**
- **The held-out SPARC effective transfer.**
  - a0 was calibrated on 51 galaxies and predicts 100 others. Evaluation log-acceleration RMS is .201573 dex, against .201590 for the empirical RAR and .569 for baryons only.
  - It improves on baryons-only in 93/100 galaxies and on RAR in 49/100.
  - **"There is no resolved advantage over RAR"** (SP:1-25).
  - "This is useful effective-model evidence, not established UNT superiority" (SP:3-4). It "does not ... demonstrate that the network forms this response" (SP:38-40).
  - LAD:103 says it "ties the MOND-like RAR rather than proving superiority."
- **The historical NGC3198 curve:** 13/43 within quoted errors, 30/43 outside, RMS 9.849457 km/s, MAPE 9.404% (LAD:103).

**Adopted (mostly calibrated or imported). [reviewer] AL:179-199 lists them:**
- a0 calibrated to SPARC;
- saturation ratio r;
- endpoint matching;
- quartic mode potential;
- the h(g)=g linear source (post-failure);
- ℓ = 100 pc (a disclosed selection);
- the S_cross action switch;
- the NGC3198 EXP24 stellar-source switch, which came after χ² = 1395.93;
- imported astrophysical conventions such as M/L = .5.

**Failed or limited**
- "Outer-radius halo win: LIMITED / PROVISIONAL" (LAD:33).
- The imported-budget old assembly is terminal at 89/120 chunks and 267/360 units (LAD:104).
- The historical 43 misses are retained (LAD:175-179).

**Open**
- A clean native120 and a changed-metric all-43 prediction remain **unstarted** (LAD:104; CS:5).
- Gap C (6→7) is OPEN: "Additional effective clock/material response not yet derived/admitted as the same native physical law" (LAD:136-138).
- The all-43 report format is fixed at LAD:202-205.
- The galaxies lane is OPEN (LAD:210).

---

## 8. Area: COSMOLOGY / EXPANSION / DARK SECTOR

**Established**
- **DS-1, CANDIDATE:** the shared dark-sector candidate specification. "All eleven Stage 1-3 obligations remain open" (L:287; R:11200-11220).
- **"The earlier BBN/ruler/BAO/supernova chain is retained as conditional calibrated evidence, including exposed calibration data and adopted Omega_A=.7/Omega_C~.251. It is not a budget-free native prediction"** (LAD:113).

**Adopted.** **[reviewer] AL:205-231** lists rung-8 items:
- Ω_A = 0.7 (hand-set, high);
- the constant vacuum amplitude A, added after an expansion failure ("Functionally Λ with a free amplitude");
- Ω_C and d0;
- flatness;
- Hunit fit jointly to D/H and θ, so "D/H and θ* are calibrations";
- ω_b fitted after D/H came out 10.46% low;
- rG = 0.98 imported;
- the AeST action architecture imported;
- the EPS values selected post-failure.
- AL:228 flags a tension between the BBN/recombination checks and the stated no-Big-Bang premise.

**Retired from the clean path.** "Retired cosmic budgets, chosen 30/70 or ln2 shares and old phase/preparation are not initial inputs to the clean path" (LAD:114, LAD:182-189; AL:30).

**Failed**
- "Lack of early acceleration and unqualified cosmic transfer remain recorded" (LAD:113).
- **[reviewer]** Both early-transfer reports failed (375/527 and 499/527), so the 6.33 GN figure is unqualified (AL:227, AL:230).

**Open**
- Shared native expansion, lensing/growth/mergers, the early universe, the CMB, thermal origin, and joint comparisons are all OPEN (LAD:114, LAD:207-218).
- The 7→8 link (one normalized law plus joint evidence) is OPEN (LAD:140-142).
- The cosmological-term slot C_0^eff is unfixed **[reviewer, AL:161]**.
- The separate network thermal-origin hypothesis exists as a file (`/Users/bgm/Research/Universal Network Theory/UNT_CMB_NETWORK_THERMAL_HYPOTHESIS_V001.md`). **It was not read for these notes.**

---

## 9. Process and reproduction state (short)
- **T-9 carrier audit** (R:10002-10018): SINGLE-CARRIER 111, TWO-CARRIER 21, NOT-CARRIER-SHAPED 14. T-52 extended the audit at registration (R:10362-10388).
- **T-36 classes** (R:9911-9912): THEOREM 41, EXACT 60, MEASURED 41, DEFINED 42; ORIGINAL 104, BORROWED 23, ASSEMBLED 57.
- **The external review counted 162 PROVED-stamped rows** as about 9% original theorems, 32% exact computations, 25% numerical, 12% standard restatements and 21% definitions (R:9088-9093).
- **Reproduction is not green:**
  - T-35 is TODO (P:36);
  - the T-35 fix pass classified 58 DIFFERS (R:10499-10507);
  - T-18 is BLOCKED (P:22);
  - the URM aggregate exits 1, failing only on zero-weight replay contracts (L:262).
- **Publication and deposit are human-authorized acts** (T-58 BLOCKED, P:59; R:10915-10920).

---

## 10. Uncertainties in these notes
- **The task's emphasis range "C-70..C-95" overshoots.** The ledger ends at C-93 (L:272). C-94 exists only as a rejected draft (R:10842-10843, R:10857).
- **The ledger's EVIDENCE and GROUNDED cells sometimes disagree within one row.** For example, C-71's EVIDENCE carries pre-promotion text (L:238). The STATUS column and the most recent register entry are taken as current here.
- **The reviewer categories in ADOPTION_LOG.md are not program verdicts**, and the rung 7-8 audit is pending refutation (AL:5-12; LAD:221).
- **"z=1" in the finite-Gate sense is a gate classification, not a derived dispersion exponent.** This rests on the reviewer reading at AL:127, which points to GLOSSARY.md; GLOSSARY.md was not read here. LAD:30-31 and LAD:75 support the cautious reading.
- **CURRENT_STATE.md is a rapidly changing execution log** (entries through 2026-10-12T16:23Z). Only its top-level status (CS:5-9) and the member-identity hold (CS:129-137) were used. Lane-specific frontier files (FRONTIER_UPDATE_V3xx, the outstanding-test ledgers) were not read.
- **These notes do not decide whether the external review's vocabulary rule is still in force** (see §0 item 12).
