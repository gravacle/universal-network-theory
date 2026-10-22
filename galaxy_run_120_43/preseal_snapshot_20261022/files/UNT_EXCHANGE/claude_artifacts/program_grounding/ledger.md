# The program's gravity line, as its own ledger records it

Claude, 2026-10-12. Read-only reconstruction. No project code was run and nothing outside this folder was written.

**Sources, all under `/Users/bgm/Research/Universal Network Theory/program-worktree/`:**
- `ledger/status_ledger.tsv`, all 286 rows, with every gravity, Γ, T-20, G-\*, C-7x to C-9x, emergence and accumulation row read in full;
- `ledger/plan.tsv`, all 58 tasks;
- `ledger/claims.tsv`;
- `REGISTER_V001.md` at the lines cited;
- `THIRD_TERM_V001.md` and `CORE_FRAMEWORK_V001.md`;
- dates from `git log` on those files (hashes cited).

**Citation keys.** `SL:n` is physical line n of `ledger/status_ledger.tsv`, where line 1 is the header. `PL:n` is line n of `ledger/plan.tsv`, `CL:n` is line n of `ledger/claims.tsv`, `REG:n` is a line of `REGISTER_V001.md`, `TT:n` is a line of `THIRD_TERM_V001.md` and `CF:n` is a line of `CORE_FRAMEWORK_V001.md`.

---

## 0. Bottom line

1. **The ledger holds two gravity lines, and nothing in the record joins them.**
   - **The Γ line** ran 2026-08-18 to 08-21. It goes: the charter's Γ, defined by function R1–R3, then T-20's record-level holonomy test, then the C-77 boundary-shaping claim, then the increments C-78 to C-93. All of it is in the REGISTER and the ledger.
   - **The Gravity Formation line** (GFT, RGRL, the ARGER Gate, finite relational accumulation L4–L12) was built 08-27 to 09-25, mostly in `GRAVITY_*` documents. Between 08-22 and 09-14, 80 commits landed and only one of them touched the REGISTER or the ledger (`4b335b7f`, 09-06, the ALLOW/REQUIRE scope repair). This line entered the ledger on 09-15/09-19 as `GFT-1` and `RA-1`…`RA-8` (SL:274–282); `RA-9`…`RA-11` (SL:284–286) followed on 09-25.
2. **On 2026-09-19 the word "emergence" moved off the Γ line** (commit `48b59062`). Four labels changed:
   - C-77 "THE EMERGENCE CLAIM" became "THE CLASSICAL/CONTINUUM FIELD-RECOVERY CLAIM" (SL:248).
   - H-1 "IS GAMMA WHERE GRAVITY COMES FROM?" became "DOES GAMMA YIELD THE CLASSICAL/CONTINUUM GRAVITY FIELD?" (SL:126).
   - Plan phase E "DOES GRAVITY EMERGE?" became "DOES A CLASSICAL/CONTINUUM GRAVITY FIELD EMERGE?" (PL:17 onward).
   - Claim G-D "GRAVITY EMERGENCE" became "CLASSICAL/CONTINUUM FIELD-SIDE RECOVERY … separate from the established finite ARGER Gate formation result" (CL:5).
   
   A new claim, G-G "GRAVITY FORMATION THEORY", was added at FORMAL-COMPLETE (CL:8).
3. **The GFT line cites no Γ-line row, and its "gamma" is a different object.** No C-77…C-93, T-20, H-9 or O-58 citation appears in its controlling documents (§6). There, "gamma" is the distinguishability γ_Q (squared fidelity). The charter's Γ is the R1–R3 structure.
4. **T-20 is DONE on a null whose interpretation was withdrawn the same day** (2026-08-19). Its question was handed to C-77 by T-21's note on X-2 (SL:24; PL:18). C-77's own row (SL:248) does not mention T-20 or H-9.
5. **The Γ line today:**
   - C-77 is CANDIDATE, and its three derivation increments are SATISFIED.
   - The Newton comparison stands at "MATCHES AT MEMBER LEVEL". It rests on one venue: C-90 is SINGLE-CARRIER (REG:10367-10371).
   - Masslessness reduces to one uncomputed bit (T-49, TODO).
   - The field readout is open (T-51, TODO; its first attempt was quarantined).
   - O-55, O-56 and O-57 are open and no plan task covers them.
6. **DS-1 (SL:287), the dark-sector row that today's V005 lanes live under, is attached to neither line.** It cites none of C-77…C-93, GFT-1 or RA-\*, and no plan task names it.

---

## 1. Chronology

| date (commit) | event | where |
|---|---|---|
| 08-18 (`6a23c591`, `e870ffa3`) | The status ledger and CORE_FRAMEWORK are created. The record level is never tested against classical gravity: no `r⁻²`, `1/r`, G, metric or Einstein equations; source standards are about accumulation only, and **a falloff exponent is not among them** | CF:8-28 |
| 08-18 | **The charter.** Γ is defined only by function: R1 space, R2 non-local writer, R3 protection. H₁(Σ) is demoted from definition to candidate (G-1 WITHDRAWN, G-5 FORMAL) | TT:11-45; SL:14, SL:40 |
| 08-18 (`f722a604`) | **G-6 FAILED: Γ is not unique.** qLDPC codes, 3D toric codes and arbitrary F₂ complexes also satisfy R1–R3. The charter's stated consequence: "topology is sufficient but not necessary … any eventual identification of Γ with anything gravitational is much weaker" | SL:41; TT:56-58 |
| 08-18 | X-6 ("is the record constraint the same as gravity's?") WITHDRAWN as an import; D-1, D-2 and D-3 adopted | SL:28, SL:36-38 |
| 08-19 (`f9ba791a`) | **The claim stated: "Γ is where gravity COMES FROM."** Classical gravity is what Γ becomes at scale, and the direction is Γ → gravity. The progress table marks recovery as "NOTHING. This is T-20 and it is the whole remaining task" | REG:6789-6827; REG:6738-6787 (H-1 reframed as emergence) |
| 08-19 (`bcf9199a`) | **T-20's criterion (the principal): H-9, record-level holonomy.** H_ABCD = (Γ_AB Γ_BD)(Γ_AC Γ_CD)⁻¹. Signatures: local, smooth, universal, phase-based, stronger with enclosed record density, Bianchi-like closure | SL:144; REG:7331-7367 |
| 08-19 (`9df305d5`) | **T-20 run on [[8,3,2]]: every loop gives ‖H−I‖ = 0, exactly flat. T-20 marked DONE** | REG:7371-7395; PL:17 |
| 08-19 (`37b2188f`) | O-23: on the same records, admissible writers give holonomy anywhere from 0 to 5.169. **"T-20's … interpretation is withdrawn."** H-11 opens: "what determines the connection?" | SL:145-147; REG:7450-7455 |
| 08-19 | O-24: minimality picks the flat connection (SL:148). O-25 FAILED: density cannot force curvature (SL:150). C-24/C-25/C-26: a flat set of writers is always available and always selected (SL:151, 156, 157). "Under the five clauses as written, Γ does not produce gravity" is stated | REG:7665-7704 |
| 08-19 | **The principal finds an import in the negative result: the measured object was the WRITER, not transport between records.** The negative claim is "WITHDRAWN as stated"; D-14 says a zero counts only if it is a zero of the object the question names | REG:7719-7760; SL:159 |
| 08-19 (`55e54ae0`) | H-14 decided: the connection is transport along the carrier. The triad R[carrier transport] ∝ ⟨c_i,c_j⟩ × channel_map[α] | SL:160; REG:7780-7790 |
| 08-19 (`210081c7`) | H-15/C-27: carrier curvature and record content are independent in both directions; the triad coefficient is 0 on the toric code. C-28: a Bianchi-like closure is present but uncoupled from records. O-29: the abelian carrier has nothing to rotate | SL:161-164; REG:7816-7870 |
| 08-19/20 | Non-abelian and density probes: C-29…C-44 (several rescoped by audit, C-37 WITHDRAWN). O-33 (open) leaves the density-to-transport join unbuilt; O-34 is PARTIAL | SL:165-191 |
| 08-20 (`a4fc4a9d`, `fb02980b`) | **The source-side standards:**<br>• C-45/C-46: the test is fail-to-cancel; the integer pairing cancels.<br>• C-47: the bath-induced Φ is extensive, additive and not a count.<br>• C-48: the whole accessible-information family is bounded independently of N.<br>• O-37: no record quantity is both sign-definite and unbounded.<br>• O-38/C-63: falloff (the induced 1/(πr) is BORROWED, RKKY). O-39 opens: "no lane has measured a field" | SL:192-201, SL:224 |
| 08-20 (`8eabd7ee` → `1580b00a`) | C-52 (Z[i] quantisation; its physical conclusion withdrawn). The durability–geometry exclusion O-42 FAILED, overturned by O-47/C-58/C-59. O-48 FAILED: the correlation energy is not a source (C-60/C-61/C-62) | SL:207-229 |
| 08-20 (`653493e9`, `5f7d50d8`) | H-3: 0 of 13 real records satisfy the five clauses. The amended clauses (i′)–(v′) are adopted (O-51). O-52 opens: the energy route to a source reopens under the amendment | SL:128, SL:233, SL:235 |
| 08-20 | First world records:<br>• C-69 and C-70 (FORMAL).<br>• **C-71, the only PROVED row**: the accumulated quantity of a written surface (NAND page, DC-saturated media).<br>• C-72 (PARTIAL): sign-definiteness is supplied by the write mechanism | SL:236-239 |
| 08-20 (`136d668f`, `3fa63272`) | **TD-1 → A-GR3: shared origin.** Γ is the common structure that ALLOWS records and appears at scale as geometry.<br>**D-24:** every classical concept must earn its place.<br>**A-GR4:** gravity emerges from terms that SHAPE GEOMETRY AND BOUNDARIES | SL:245-247; REG:9506-9537 |
| 08-20 (`5b197ad2`) | **C-77 adopted** ("yes let's adopt this"). T-37 DONE. First increment: derive a known gravitational relation from boundary structure alone. Failure clause and openness clause added (Γ is named as a contributor, not as the only one) | REG:9539-9563; SL:248; PL:38 |
| 08-20 (`04819fea`) | **T-21 DONE: a note on X-2.** "THE COLLECTIVE-LEVEL QUESTION … REMAINS OPEN and now lives in C-77's derivation increment (T-42)" | SL:24; PL:18 |
| 08-20 | The C-77 increments:<br>• C-78: distance = boundary-crossing cost.<br>• C-79: the boundary-degree law (increment 1).<br>• O-54/C-80: there is no pure-Γ falloff; falloff enters only through the coupling (increment 2).<br>• C-81/C-82/C-83: certifiability is the interface; the surface owns the clock.<br>• O-55, O-56 and O-57 opened | SL:249-258 |
| 08-20 (`e8f61d7c`, `14b26514`) | C-87: Γ-priced couplings reach exactly three classes; the critical class is the venue's discrete Poisson equation. C-88: the Newton composition profile appears only at R1 + occupancy. O-58 lists N1–N5. **C-90: the D=3 critical member is 1/d; NEWTON VERDICT: MATCHES AT MEMBER LEVEL** (increment 3) | SL:264-266, SL:269 |
| 08-20 (`d41cfe07`) | C-91: masslessness = measure conservation, a computed identity. The residue is one computable bit, which becomes **T-49 (TODO)** | SL:270; PL:50 |
| 08-20 (`3f6fbb7f`) | C-92: the field-side instrument is identified (the "Second Lump", F(D)), with pre-registered rule V1–V5 | SL:271 |
| 08-21 (`9f4e421a`, `609755bc`) | C-93: the earned metric is content-rigid on stabiliser venues, so a field can live only one tier down. Named next step: "does one written record shift dE for an adjacent write in the E1/E2/E3 writing tier?" T-52: C-90 is SINGLE-CARRIER, and its second venue is owed | SL:272; REG:10362-10388 |
| 08-21 (`0d7de834`) | **The T-51 ALL-PASS is quarantined as inadmissible.** The drafted C-94 row, C-77 increment and T-51 completion are rejected. T-51 stays TODO | REG:10797-10868 |
| 08-22 → 09-14 | 80 commits, in `GRAVITY_*`, `DEVELOPMENT_R_*` and `AUDIT_*`:<br>• RGRL adopted as a working postulate (08-27).<br>• Record-first closure (08-29).<br>• Gate A, then L4–L12 relational accumulation (09-05/06).<br>The only REGISTER or ledger touch is `4b335b7f` (09-06), which rescopes G-3, D-4, T-II.5, F-3, H-7 and H-8 | git log; SL:16, 33, 54, 58, 132, 133 |
| 09-15/16 | URFT-1, A-AL2, **GFT-1** (conditional), RA-1…RA-8. The ARGER Gate is adopted, and the finite `z=1` classification holds at L = 4…12 | SL:273-283; REG:10869-10970 |
| 09-19 (`48b59062`) | **Relabel** (§0 item 2). G-G is added at FORMAL-COMPLETE and G-D is narrowed to field-side recovery | CL:5, CL:8; SL:126, 133, 248 |
| 09-25 (`f5973628`) | RA-9: a two-sided association; the signed persistence prediction FAILS. RA-10: Ollivier–Ricci controlled null. RA-11: one L4 mechanism. Each explicitly supplies no geometry or gravity | SL:284-286 |
| 09-30 / 10-08 (`fc70e2e2`) | DS-1: dark-sector candidate. All eleven Stage 1–3 obligations are open | SL:287; REG:11200-11220 |

---

## 2. What T-20's completion means, and where the "reread into C-77" actually is

- **The DONE_WHEN (PL:17):** "a many-record collective quantity is defined, computed, and either shown to satisfy a constraint of the right type or shown not to". It was marked DONE at `9df305d5` on the [[8,3,2]] flat null. The task's ROW column is empty, so T-20 was never linked to a ledger row.
- **The same day, the result lost its reading twice:**
  1. O-23 showed that the connection is not fixed by the records ("T-20's result stands as a measurement and its interpretation is withdrawn", REG:7453-7455; also SL:145).
  2. The import catch showed that T-20, O-23, O-24, O-25, O-27 and route 1 all measured writers, not transport between records, which is the object H-9 names (REG:7728-7750).
  
  Under D-14 (SL:159), T-20 is a zero of the wrong object. The plan row was never reopened.
- **The handoff to C-77 is T-21, not C-77's own text.** T-21's DONE_WHEN reads "the collective one (open, = T-20)" (PL:18). The note it placed on X-2 reads "now lives in C-77's derivation increment (T-42)" (SL:24). H-8 repeats the routing: "remains open under H-1/C-77" (SL:133). **SL:248 (C-77) never names T-20 or H-9.** Cite SL:24 and PL:18 for the reread; this corrects the citation in `TO_CODEX/0110` and `gamma_reconciliation/RECONCILIATION.md`, which point to SL:248.
- **The handoff also changed the criterion:**
  - T-20 was judged against H-9: a stable, universal, path-dependent mismatch among records.
  - C-77 is judged against "derive, from record-surface boundary structure alone … a scale-level relation that matches a known gravitational one", with a failure clause (REG:9548-9552).
  
  H-9 stays DEFINED (SL:144) and has not been re-measured on the C-77 machinery. The holonomy branch's open rows are H-11 (SL:147), O-26 (reopened, SL:152), O-33 (SL:178), O-34 PARTIAL (SL:181) and O-41 (SL:206). No plan task names H-11, O-26 or O-33.
- **The charter is stale here.** It still says recovery is "untouched — plan task T-20" (TT:72-73).
- **Correct paraphrases of the C-77 line**, for anyone citing it:
  - **C-77** (REG:9543-9546): "The structure Γ that allows a record — by shaping the boundaries that make a bit non-losable … — is the same structure whose aggregate at scale appears as geometry. Classical gravity emerges from the boundary-shaping terms and is not expected to resemble itself at the record level." The paraphrase "Γ responds to Record boundaries" is a gloss and not the registered text.
  - **C-78** (SL:249): "literally boundary-crossing cost", exact on the torus.
  - **C-80** (SL:254): "NO PURE-GAMMA FALLOFF EXISTS … THE FALLOFF ENTERS ONLY THROUGH THE DECLARED COUPLING TERM … the exponent is inserted, not earned."
  - **The Γ-priced kernel** is C-87's G_μ(d) (SL:264). C-90 computes its D=3 member (SL:269), and C-91 supplies the criticality-equals-conservation identity (SL:270).

---

## 3. Current status: the Γ line

**Computed (FORMAL; mostly EXACT)**
- **Γ-only structure:**
  - G-5: H₁ satisfies R1–R3 as a candidate.
  - G-8: the constraint puts the total at the boundary (perimeter).
  - G-9: record space = Z₁/B₁.
  - G-10: capacity survives off manifolds.
  - C-74: clause (v) holds by homology on the toric code.
  - (SL:40, 43-45, 241)
- **The C-77 increments:**
  - C-78: distance.
  - C-79: boundary-degree law (registered CANDIDATE).
  - C-80: there is no pure-Γ falloff. Pure-Γ two-region structure is zero beyond contact, contact laws, topological constants, switches, or w_min = d (confinement).
  - C-81/C-82/C-83: the certifiability interface and the durability clock.
  - C-87: three reachable classes.
  - C-88: the Newton composition profile exists only at R1 + occupancy.
  - C-90: 1/d at D=3 on one venue.
  - C-91: masslessness ⇔ measure conservation; the mass gap has a closed form under E3.
  - C-93: content-rigid metric, so the field must live in real-valued amplitudes.
  - (SL:249-257, 264-265, 269-270, 272)
- **The source side:**
  - C-47: extensive Φ.
  - C-48: bound on accessible information.
  - C-71 PROVED: the accumulated quantity, with its sign fixed by the write.
  - C-72 PARTIAL, blocked by T-50.
  - (SL:196-197, 238-239)
- **C-77 itself:** CANDIDATE. "Never a claim that continuum or Einstein gravity is empirically derived" (SL:248).

**Failed or withdrawn on this line**
- Uniqueness: G-6 FAILED (SL:41).
- Withdrawn identity and definition rows: G-1, G-12 and X-6 (SL:14, 47, 28).
- The holonomy branch: O-23 FAILED, O-25 FAILED and H-12 FAILED (SL:146, 150, 153). The general negative "Γ does not produce gravity" is withdrawn (REG:7749).
- The energy route: O-42 FAILED and O-48 FAILED (SL:211, 219). O-50 FAILED (SL:228).
- Source claims: C-37 and C-55 WITHDRAWN (SL:177, 212). C-52's physical conclusion is withdrawn (SL:207).

**Open, with a plan task**

| row | content | task |
|---|---|---|
| O-58 N2/N3 (SL:266) | Does one GR3 writing event conserve writer measure (E1 transport / E2 trail-with-retreat / E3 trail-with-decay)? The answer decides masslessness | T-49 TODO (PL:50) |
| O-39 / C-92 (SL:201, 271) | Field-side readout. Its first scoring was quarantined; a fresh sealed instrument is required (REG:10858-10868) | T-51 TODO (PL:52) |
| C-72 (SL:239) | A baseline-free observable for the occupancy law | T-50 TODO (PL:51) |
| O-4/O-45 (SL:20, 216) | What "admissible" means | T-25 TODO (PL:26) |
| D-15/D-17/D-22 | Re-audit every null against the venue rule | T-26 TODO (PL:27) |
| H-3 (SL:128) | Why this definition | T-53 TODO (PL:54) |

**Open, with no plan task in the ROW column**
- O-58 N4: norm selection. N5: the anisotropy frontier (SL:266).
- C-90's second D=3 venue (REG:10387-10388). It is said to fold into T-49 but is not in T-49's DONE_WHEN.
- O-55: no universal coefficient (SL:252).
- O-56: no earned thermodynamic pair (SL:253).
- O-57: the collapse analogue (SL:258).
- O-52: the energy route reopened under the amendment (SL:235).
- O-53: the extensive durable operator (SL:242).
- O-43: completeness of the exclusion (SL:214).
- O-40 (SL:202).
- H-11 (SL:147), H-13 (SL:158), O-26 (SL:152) and O-33 (SL:178).
- H-7, the carrier-formation form of H-1 (SL:132), and T-II.5 (SL:33).
- T-V.4, the classical limit (SL:32).

**Blocked:** X-4, T-VI.3 and T-VI.4, because empirical contact is zero (SL:26, 34, 35).

---

## 4. Current status: the GFT/ARGER line

- **GFT-1, FORMAL (SL:274).** An exact implication under the adopted RGRL and WTC-H1–H5. Four items remain open: RGRL's empirical confirmation, the microscopic F3 derivation, the strict induced origin, and a parameter-free numerical G. RGRL is a principal-adopted working postulate (`GRAVITY_RGRL_ADOPTION_V001.md:1-30`). Its final target is the Einstein–Hilbert response, stated as a recovery target at scale (`GRAVITY_FORMATION_CURRENT_PICTURE_V001.md:167-171`).
- **RA-5/RA-6/RA-7, FORMAL/MEASURED (SL:279-281).** At L = 4, 6, 8, 10 and 12, the finite record block has bounded membership, deduplicated mass > 0.5 and positive probe visibility, so it passes the ARGER Gate and receives the finite `z=1` classification.
  - RA-8 adds a conditional `z=1` under the LL-P premise (SL:282).
  - L14 produced no result (RA-4, SL:278).
- **RA-9, RA-10 and RA-11 (SL:284-286).** RA-9's signed persistence prediction FAILED (the sign reverses and the magnitude declines). RA-10 is a curvature null. RA-11 is one L4 mechanism. **Each row states that it supplies no geometry, curvature or gravity.**
- **Claims grid.** G-G and G-H are FORMAL-COMPLETE (CL:8, CL:9). G-D, the Γ line, is MEMBER-LEVEL-MATCH, with NEXT = T-51, T-49 (CL:5).
- **No plan task carries GFT-1's open items** (no ROW = GFT-1 anywhere in plan.tsv). T-57 is DONE (PL:58) and T-58 is BLOCKED (PL:59).

---

## 5. Where the two lines touch

- **ALLOW is the only shared joint, and only by definition.**
  - G-3: "Gamma supplies an ALLOW/capacity predicate" (SL:16).
  - A-GR3: "Γ is the common structure that ALLOWS records" (SL:245).
  - ARGER's first stage is "`ALLOW` | topological capacity" (`UNIVERSAL_NETWORK_THEORY_ARCHITECTURE_V001.md:54,63`), and that document never names Γ.
  
  So Γ sits at ARGER's ALLOW stage by definition, but no ledger row registers that link or uses it.
- **No citations cross.** `GRAVITY_FORMATION_CURRENT_PICTURE_V001.md`, `GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md`, `GRAVITY_FORMATION_THEORY_CLOSURE_V001.md`, `GRAVITY_RGRL_ADOPTION_V001.md` and `UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md` contain no C-77…C-93, O-58, T-49, T-51, H-9 or A-GR\* citation. The three "T-20" grep hits in the current picture (lines 1261, 3620 and 3872) are the string "HUST-2018".
- **One letter, two objects.** In the GFT line, "gamma" is the distinguishability γ_Q ≤ 1 − B_rec², with I_γ = −log γ_Q, which yields "Fisher/Bures information geometry" (`GRAVITY_FORMATION_CURRENT_PICTURE_V001.md:143-149, 173-175`). Γ in the charter is whatever satisfies R1–R3 (TT:21-27).
- **DS-1 is attached to neither line.** It cites the dark-sector checkpoint only (SL:287). Its BLOCKED_BY list is "physical dictionary, formation, shared energy closure, joint predictive tests".

---

## 6. Record inconsistencies, for the registrar (data only)

1. T-20 is DONE (PL:17) while T-21 declares its question open "= T-20" (PL:18), and the interpretation of T-20's result is withdrawn (REG:7453-7455).
2. THIRD_TERM still says recovery is "untouched — plan task T-20" (TT:72-73). It also predates G-6's FAILED verdict, whose consequence it states only conditionally (TT:56-58).
3. The 09-19 relabel narrowed C-77, H-1, H-8, phase E and G-D (`48b59062`), and no REGISTER entry explains the narrowing. The 2026-09-19 entry (REG:11040-11064) covers the closure composition only.
4. C-90 carries no T-9 carrier mark in its own GROUNDED cell (SL:269), but REG:10367 records it as SINGLE-CARRIER (macrospin-CoCrPt).
5. A-PR's EM-world clause rests on C-71 alone until T-50 lands (REG:10376-10380), because C-72 is PARTIAL (SL:239).

---

## 7. Where the ledger itself says the Γ line resumes

Each item is classified computed, measured or declared, per the program's own rows.

- **Computed:**
  - **T-49's bit** (PL:50): is one GR3 writing event measure-conserving on the surface's own writing tier (E1, E2 or E3)? By C-91's identity, the answer decides masslessness (SL:270).
  - **C-93's named step** (SL:272): does one written record shift dE for an adjacent write in the E1/E2/E3 tier ("bias is mass")?
  - **C-90's second D=3 venue** (REG:10387-10388).
- **Measured:** T-51's field reading F(D), on a freshly sealed instrument with an independent default-refuted verifier (REG:10858-10868).
- **Declared (principal):**
  - which object "gravity emergence" names after the 09-19 relabel (CL:5 against CL:8);
  - whether H-9 or C-77's increment criterion governs the collective question (SL:144 against REG:9548-9552);
  - DS-1's attachment to either line.
- **For lanes in the V005 Hamiltonian**, the C-77 line's own premises apply unchanged:
  - pure Γ supplies no falloff (C-80);
  - distance is boundary-crossing cost (C-78);
  - criticality ⇔ measure conservation of the writing (C-91).
  
  A V005 kernel priced by Bind and not by Γ sits in C-80's "coupling term". C-80 assigns falloff to that term, with the exponent inserted, not earned (SL:254).
