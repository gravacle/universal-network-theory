# Adversarial check of UNT_ORIENTATION_V001.md — V001_CHECK

Claude (subagent), 2026-10-12. Read-only check of `KN/UNT_ORIENTATION_V001.md` (241 lines) against its cited originals, opened file by file. No project code was run, nothing outside `KN/` was written, `~/.codex` was not touched. Same-lineage check (Claude checking Claude): it is not a distinct review and does not substitute for one (KN/UNT_START_HERE_V003.md L55).

Path keys are those of V001 L5, plus: SH3 = `KN/UNT_START_HERE_V003.md`; PR = `KN/PRINCIPAL_PREMISES_REGISTER_V001.md`; AD = `KN/ANTI_DRIFT_PROTOCOL_V001.md`; LB = `KN/LINEAGE_BRIDGE_V001.md`; SLM = `PW/STATUS_LEDGER_V001.md`; CL = `PW/ledger/claims.tsv`; NCD = `CAN/..` (the `NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/` directory); "V001 Lnn" = a line of the orientation under check.

**Overall verdict.** Most of V001's ~170 citations check out, and its line numbers are correct as of drafting. But six things go beyond line errors:
- **It has been overtaken by events.** These postdate it: TO/0114 (line-A restart, V005 demoted to candidate venue); TO/0115 (anti-drift protocol); SH3, which supersedes the guide V001 points to; PR; LB; and root's write-back of 35 ledger rows (TSV:288–322).
- **TO/0114 L25 assigns this orientation the role of a review and annex of root's guide, "not a second guide".** V001 presents itself as "required reading for every lane".
- **In two places it carries Claude's own relay glosses as if they were the principal's premises,** and one of them is a banned "gravity needs …" statement.
- **It overgeneralizes one candidate-venue property (L ≥ 4) into a property of Γ.**
- **It states the time-reversal/arrow result more broadly than its reviewed scope.**
- **It omits the program's claims grid, the C-84 distinguishing-statement survivors, C-92, the URM name and the closure theorem.**

All corrections below are applied in `KN/UNT_ORIENTATION_V002.md`.

---

## (a) Cited claims checked against their sources

### Verified (no change needed)
The following were opened and match V001's statement:
- **Program sources:**
  - THIRD_TERM L3, L5–17, L21–30, L39–45, L62–66, L72–73;
  - CORE L14–29, L39–57, L61–89, L96–117;
  - REG:5231–5240, 5488–5516, 6789–6826, 7331–7367, 7371–7464, 7719–7750, 9539–9563, 10243, 10340–10358, 10367–10371, 10943–10955, 10994–10997;
  - TSV rows 2, 9, 14, 26, 28, 36–38, 41, 58, 71, 76, 77, 81, 83, 84, 96, 104, 107, 112, 134, 136, 142, 143, 144, 159–162, 170, 174, 201, 233, 238, 245–259, 264–274, 276, 279, 284, 287;
  - PLN:17, 26, 39, 50, 52, 54;
  - SR L35–41, L80–93, L115–135, L164–173, L190–230, L249–272, L333–344, L464–479; audit L3–8;
  - PRINCIPAL_ACT_001_DRAFT L76–81, L98–102; CUSTODY L55–63; BIND_BIRTH_POLICY L3–7; FRAME_CHALLENGE_V002 L11–30; PW/README L22–32;
  - GF L141–152, L3961–3981, L4046–4051;
  - U/README L3, L14; CURRENT_STATE L92; LAD L12–15, L31, L66–67, L103–104, L113, L207–218.
- **Canonical model and audits:**
  - V005 L4, L9–10, L13–23, L25–34;
  - EXACT14_CROSSWALK L5–13, L96;
  - PKT validity audit V001 L9–13, L31, L33–39, L113–122, and audit V002 L37–41;
  - SPARC result L3–4, L24.
- **TO_CODEX relays:** 0005, 0008, 0009, 0010, 0011, 0077, 0080, 0082, 0083, 0084, 0090, 0095, 0097, 0100, 0101, 0102, 0104, 0106, 0107, 0108, 0109, 0110, 0111, 0112, 0113, at the cited lines.
- **Codex outboxes:**
  - FC/0037, 0039, 0051, 0052, 0069, 0075, 0076, 0077;
  - FC2/0106 L10–12;
  - FC3/0118, 0124, 0126, 0128, 0130, 0134, 0136, 0137, 0138, 0145.
- **Claude artifacts:** GR/RECONCILIATION L6–11, L14, L24, L41–55; GR/CHALLENGE (every cited range); challenge OUTPUT L6–14; PROGRAM_GRAVITY_PICTURE L41.
- **Ledger counts:** V001's counts are exact for TSV rows 2–287 (recounted: FORMAL 153, DEFINED 49, OPEN 30, FAILED 12, WITHDRAWN 11, PARTIAL 11, MEASURED 9, CANDIDATE 3, BLOCKED 3, NOT OURS 3, RECLASSIFIED 1, PROVED 1).

### Citation corrections

| # | V001 location | Finding | Evidence | Fix in V002 |
|---|---|---|---|---|
| A1 | L72, L186 | SLM was regenerated at 17:25. The doctrine heading "checked before any lane is commissioned" is now L58, not L57. D-28..D-33 were appended at L90–95. | SLM L58, L62, L77–95 | cite SLM L58, L62–95 |
| A2 | L56 | PLAN.md was regenerated at 17:26. The P-20 row is now L86, not L82. P-58..P-61 (line-A HOLD rows) are new at L61–64. | X/PLAN.md L61–64, L86 | cite L86; add P-58..P-61 |
| A3 | L35 | "RA-1..RA-11, TSV:275–286" includes URFT-1 at TSV:283. | TSV:283 | name URFT-1 separately |
| A4 | L120 | "admissible := [U,H]=0, provisional (TSV:20)": TSV:20 is O-4, "admissible in clause (iv) is undefined" (DEFINED). The provisional definition is in CORE, with the re-test task at PF-3. | CORE L114–115; TSV:20, 93 | cite CORE L114–115 and TSV:93 |
| A5 | L120 | H-3 (TSV:128) is listed under "F" (failed/withdrawn), but its status is **PARTIAL**. Its evidence tested 13 records, none satisfying all five clauses. "~20" is CORE's census. | TSV:128; CORE L63–67 | relabel; give both counts |
| A6 | L19 | The channel is stated as "iff it pairs oddly with the record's conjugate" (GLOSSARY L40). G-16 itself says that form is "NECESSARY BUT NOT SUFFICIENT". The criterion is a nonzero compression onto the code space along that record. | TSV:122; PW/GLOSSARY.md L40 | state G-16's corrected criterion; flag GLOSSARY L40 as the older form |
| A7 | L18 | "the record is a holonomy of EM's own complex" cites TSV:2 and 71. The holonomy statements are A-EM2/A-EM3. | TSV:68–69 | add TSV:68–69 |
| A8 | L124 | "The closure theorem composes conditional components" is cited to U/README L14, which does not mention the closure theorem. | PW/README.md L18–21; PW/UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md L7–10, L28–34 | cite those |
| A9 | L122 | "no C-94" (REG:10842–10867) was correct at that landing, but root has since assigned C-94 to Q0 word freezing. | TSV:288; KN/ROOT_ACCEPTED_LEARNING_INDEX_V001.md L7 | clarify that the quarantined T-51 scoring got no row; C-94 now names Q0 freezing |
| A10 | L117 | The counts "over 286 rows" are stale. TSV now has 321 rows (lines 2–322). New totals: FORMAL 178, DEFINED 58, OPEN 30, WITHDRAWN 12, FAILED 12, PARTIAL 11, MEASURED 9, CANDIDATE 3, BLOCKED 3, NOT OURS 3, RECLASSIFIED 1, PROVED 1. | TSV:288–322; FC/0078 L11 | update; PROVED is still 1 |
| A11 | L3, L35, L50, L185, L192, L201, L225 | V001 points to START_HERE_V002, G1–G12 and template V002. These are superseded by SH3, G1–G13 and template V003. | X/CLAUDE.md L11; FC/0078 L7; SH3 L1–3, L49, L53 | repoint |
| A12 | L215 | Construction "#7 is canonical" is cited to CROSSWALK L5–9, which does not say so. | CROSSWALK L2; TO/0005 L9–11 | cite those |
| A13 | L42 vs PR L9 | The two Claude-authored records quote premise 1 differently. TO/0077 L1: "There is no 'new gravity' added later." PR F1: "There is no 'new gravity' **that is** added later." **[UNCERTAIN]** which is verbatim. | TO/0077 L1; PR L9 | quote the relay; note the variant; the principal resolves it |
| A14 | L132 | Not wrong, but LAD L221 still calls the rungs 7–8 audit "SINGLE-AUDITOR/PENDING-REFUTATION", while PKT audit V002 records the completed cross-lineage refutation. The ladder is stale. | LAD L221; PKT/UNT_VALIDITY_AUDIT_V002.md L1–5, L37–41 | note the conflict |
| A15 | L151 | Label collision: V001's DQ-2 "(P-b)" uses RECONCILIATION's P-b (which R3 reading). LB, now required reading, uses P-b for the S1/matter-dictionary conflict, which is V001's DQ-6. | GR/RECONCILIATION.md L53; LB L25–28 | map both label sets explicitly |

---

## (b) Slips into standard-physics framing or classical machinery

| # | V001 location | Finding | Evidence | Fix in V002 |
|---|---|---|---|---|
| B1 | L43 (premise 2 "Consequence") | **"gravity needs a *difference* relative to a Record-filled background"** is Claude's relay gloss, not the principal's words. The relay says "What gravity needs instead is a *difference*. A uniform Record universe produces no force anywhere; forces come from gradients" and defines the observable "as a function of distance … its fall-off". "Gravity needs …" is on CORE's banned list for the record level. "Forces come from gradients" is potential-gradient reasoning. The fall-off observable is the steering CHALLENGE traces to Claude's relays. | TO/0080 L7–9, L13; CORE L18–21; GR/CHALLENGE.md L195–202 | Removed from the premise. Recorded as a retired relay gloss. P-47's Δ-against-sham observable is kept only as a measurement design, superseded as decision object by TO/0109 and the D6 restart. |
| B2 | L66 (§2.4) | "exists only collectively, in the many-body, finite-density, coarse-grained regime ('pressure exists collectively, not for one molecule')" is Claude's relay text with a thermodynamic analogy. The principal's words are only "emergence and collective behavior". Coarse-graining is lawful only as an explicitly declared map that owns its variables. | TO/0109 L1, L7; SR L468–473; D-28 TSV:309 | Use the principal's words plus root's registered D-28. Mark the pressure analogy as relay gloss. Require any coarse-graining map to be declared. |
| B3 | L56 (arrow) | "past-hypothesis structure" is an analogy from the relay of a principal *hypothesis* ("it might be another allow/require instance"). The reviewed P-20 cross-check says the TR theorem and the corrected identities establish **no** physical arrow, accumulated history or thermalization. | TO/0009 L1, L9; NCD/P20_OPERATOR_CROSSCHECK_V001.txt L4; NCD/P20_OPERATOR_CROSSCHECK_INDEPENDENT_REVIEW_V002.txt L3–5 | Keep the principal's M4 (PR L26). Label the analogy. Add the cross-check's limits. |
| B4 | L19 (R2/R3) | THIRD_TERM's unrestricted "no local operation" wording is repeated without the corpus qualification: admissible means [U,H]=0, over a **single** contractible region. The strong reading "nothing local can write it" is FALSE. Unqualified, the wording invites toric-code-style "any local term disqualifies" readings. | CORE L105–106, L119–124, L171–181; C-13 TSV:83; FC3/0145 L14 | add the qualification to R2/R3 |
| B5 | L145 heading; L152 (DQ-3) | "**L ≥ 4 for Γ**" and "Γ needs L ≥ 4" turn a property of V005's candidate Φ into a property of Γ. Γ is defined only by function. | FC/0078 L15; SH3 L13; TT L11–14 | rescope to "V005's Φ candidate needs L ≥ 4" |
| B6 | L96 (framing error 1); §9 Q1, Q6 | The historical **SINGLE-CARRIER** annotation (counts mechanisms/venues: C-90 is SINGLE-CARRIER, macrospin-CoCrPt) is conflated with one-carrier/one-particle (Q1-sector) results. | REG:10367–10371; D-28 TSV:309; SH3 L41; FC/0078 L15 | add the disambiguation |
| B7 | L144 | "Under the amended (v′), Φ is the Γ candidate" merges separate obligations. Winding protection, writer existence and qualified Γ are different. A Hermitian Bind/admission term is not automatically C-91's positive, conserving writer kernel. | SH3 L13; FC/0078 L15; LB L42, L45 | list the obligations separately |
| B8 | L122 (C-80) | C-80's summary leaves out that its falloff was **inserted** with the declared mediator ("the exponent is inserted, not earned") and that it is venue-scoped. D-24: "no falloff exponent has been earned by anything." Without this, C-80 can be read as licensing a falloff target. | TSV:254; TSV:246 | add |
| B9 | L47 (premise 6) | The z=1 sum-rule premise needs its registered scope so "z=1" is not read as a light-cone or relativistic import. z=1 "is at most a finite-size scaling prerequisite. It does not supply Lorentz boosts …". D-29: the historical prism identity is model-specific, and P-55 must derive its own commutator and structure factor. | SR L459–462; D-29 TSV:310 | add |
| B10 | (new reading) | LB's "correspondences" (for example "P-47's screening … was predicted by C-88") would import a map if read as identities. Root: they are questions/antecedents until a full parent-state-operator map exists, and C-88's orientation result does not prove a V005 screening theorem. | FC/0078 L15; LB L13–21 | carry the qualification |

---

## (c) Overstatements and misstated premises

| # | V001 location | Finding | Evidence | Fix in V002 |
|---|---|---|---|---|
| C1 | L1, L3 | V001 calls itself "required reading for every lane". The principal's restart relay says Claude's orientation "will be posted as a **review and annex** of root's guide … It will not be a second guide." | TO/0114 L25 | V002 is retitled and positioned as an annex to SH3 |
| C2 | L41–50 | Premises are printed with "Consequence:" lines that are Claude's relay text (TO/0077 L8; TO/0080 L7–9; TO/0109 L7), without marking them. PR: "No agent may override or reinterpret an entry." | PR L3 | Separate four things: (i) the verbatim quote, (ii) the PR ID, (iii) relay gloss, marked [RELAY GLOSS], (iv) the program row root registered (C-113, C-114, D-28, D-29, D-30) |
| C3 | L50 | "not yet in an exchange file" is stale: premise 9 is PR F8, recorded with "(Read together with the standing rule that every outcome registers, see G3.)". Reading "prove" through CORE's 2026-08-20 PROOF definition is Claude's link. | PR L16, L47; CORE L39–53; REG:10347–10358 | update; mark [CLAUDE READING]; pair with G3 |
| C4 | §2.1 | Register entries are missing: **F6** "It has radical implications. So most of this won't be ready built in standard physics."; **M3** "We need to ground EVERY LANE with the whole program context. They have to understand UNT." (also the harness-relayed user request for this task); M5's "No declaration fallback without a proof of impossibility"; F9's date 2026-08-18. | PR L14, L17, L25, L27 | add |
| C5 | L53 | The canonical sign-off is quoted without its original wording: "… so Records accumulate irreversibly". That clause was withdrawn after the principal asked "are we sure un-writing isn't a possibility?", without a new principal decision being needed. Leaving the history out lets someone re-import "irreversibly" from 0005. | TO/0005 L11; TO/0008 L1, L9–11; V005 L2, L19 | add the history |
| C6 | L35 | "Two gravity lineages" understates the requirement. Every proposal must declare lineage **A, B or C** (C = dark sector / V005). B cites A only through a T-21 note. | SH3 L28; AD L20–25; LB L7–11; PROGRAM_GRAVITY_PICTURE L41 | three lineages |
| C7 | L183–192 (§7) | Missing pieces: the principal's restart decision (line A, T-49 → C-93 → C-90 second venue → T-51, D-32, P-58..P-61 HOLD); V005 demoted to a candidate venue; the adopted anti-drift protocol (framing gate (a)–(e), principal sign-off for foundational or new-direction tasks, idle acceptable, drift checkpoints, LEARNED_INDEX, lineage bridge). | TO/0114 L4–21; TSV:321; X/PLAN.md L61–64; TO/0115 L6–16; AD L16–37; TSV:322 | add |
| C8 | L151 | DQ-2 "Not yet ratified". TO/0114 L15 (relay text) and LB L37 describe Φ "under the adopted world-tier reading (O-51, A-GR4)", but the principal's quoted words were only "Yes, rebuild on line A". Root keeps exact and finite-tolerance definitions separate. Also, LB L23 says of P-a..P-d "nothing is computable here", while CHALLENGE classes P-c as computable. Both are Claude documents and they conflict. | TO/0114 L1, L15; LB L23–28, L37; GR/CHALLENGE.md L109–131, L221–222; FC/0075 L12 | mark [UNCERTAIN]; report the conflict |
| C9 | L117 | "PROVED 1 (C-71)" with no content. C-71 is the encoding-level accumulated quantity of formed real record surfaces (NAND, CoCrPt), that is, CORE's *source* standards. It is not a gravity, field or geometry result. | TSV:238; CORE L23–26 | state it |
| C10 | L179, L189 | "Retired framings (to receive D/X-style entries)" is done: X-7 WITHDRAWN. The §6 results now carry C-IDs. LEARNED_INDEX still does not exist, but root's index does, and root will append to Claude's seed. | TSV:288–322; KN/ROOT_ACCEPTED_LEARNING_INDEX_V001.md L1–43; FC/0078 L11; AD L31 | update |
| C11 | L31, L122 | C-77's falsifier clause is missing ("The claim fails if every such derivation requires assuming the classical form, or yields relations incompatible with the known ones"). So are C-90's caveats: "NOTHING in Gamma yet places mu at criticality"; the 1/d law is exact only in an emergent Euclidean norm over earned L1 separation. | REG:9548–9551; TSV:269 | add |
| C12 | L124 | Lineage B is under-described. Its conditional macroscopic gravity theorems "retain an adopted information-to-geometry law and a coefficient calibrated to measured G", and RGRL is "an adopted soldering premise". These are load-bearing adoptions a lane must not treat as native. | U/README.md L14; LAD L89 | add |
| C13 | L15 | U/README L3's second sentence, the current objective ("one physically normalized law connecting measured galaxy dynamics and expansion without imported dark-sector energy budgets"), is omitted. | U/README.md L3 | add |
| C14 | L56 | The arrow: "Every V005 term is time-reversal-even at the declared values, so the dynamics has no intrinsic arrow". The reviewed scope is the **real member**: θ ∈ {0, π} suffices, with real ε_B, κ_v, g. V005 leaves θ and the κ phase/profile as declarations. The cross-check also corrected 0011's complement and equilibration claims: blank and written are not mirror images, because the complement changes the Birth embedding. | NCD/P20_OPERATOR_CROSSCHECK_V001.txt L4, L10–15, L20–28; review V002 L3–5; V005 L13, L21; X/STATUS.md L15 | scope it |

---

## (d) Major program results missing from V001

| # | Missing item | Source | Added in V002 |
|---|---|---|---|
| D1 | The program's **claims grid** G-A..G-I with stages: G-A GROUNDED-NOT-EARNED; G-B WORLD-CONTACT-PARTIAL; G-C FORMAL-COMPLETE; G-D MEMBER-LEVEL-MATCH; G-E FORMAL-PARTIAL; G-F IN-CONSTRUCTION; G-G FORMAL-COMPLETE; G-H finite relational accumulation; G-I FORMAL-COMPLETE | CL L1–10 | §4.4 |
| D2 | **C-84**: the distinguishing-statement audit (PF-6's successor) returns three survivors, S-1 durability-clocked certification window, S-2 flash alpha-channel discrimination, S-3 thickness profile; alpha survives only as S-2 | TSV:260 | §4.2, §4.1 |
| D3 | **C-92**: the T-51 field-side instrument is identified (DEFINED), with a pre-registered negative closure ("exhibitable-not-provable"). The first scoring is quarantined, and P-61 calls for a fresh instrument. | TSV:271; PLN:52; REG:10840–10861; X/PLAN.md L64 | §4.2 |
| D4 | Prior falloff/source learning the 120/43 lanes re-derived: **C-63** (BORROWED 1D RKKY: a gapless mediator gives a power-law form where gapped ones screened); **O-38** rescope ("a record-level falloff that does not resemble an emergent one has failed nothing"); **C-47** (first quantity meeting the source standards); **C-72** PARTIAL (encoding fixes sign); **C-88** F2 (occupancy accumulates, orientation screens) | TSV:224, 200, 196, 239, 265 | §4.2 |
| D5 | **URM** named by the principal (title, not claim); the **Closure Theorem** as typed composition; **URFT-1** / G-I | TSV:261; PW/README.md L3–5, L18–21; closure theorem L7–10, L28–34; TSV:283; CL L10 | §1, §4.2 |
| D6 | Root's write-back C-94..C-121, D-28..D-33, X-7 (scoped; "No physical result was upgraded") | TSV:288–322; FC/0078 L11 | §6 |
| D7 | Record laws and protection mechanism: C-69 (CoCrPt grain is a record under the amended clauses only), C-70 (steady-state law), C-86 (count law); C-66/C-68 (degeneracy- versus barrier-protection, the basis of O-51); D-27 (two readings of "protected") | TSV:236, 237, 263, 231, 234, 268 | §4.2, §3.1 |
| D8 | The H-9 signatures the principal named (local, smooth, universal across record types, phase-based rather than a force, stronger with enclosed record density, causal, Bianchi-like closure). C-77's row never names T-20 or H-9 [CLAUDE READING]. | REG:7356–7365; PROGRAM_GRAVITY_PICTURE L41 | §1 |
| D9 | PR, AD, LB, SH3 and root's accepted-learning index as required companion reading | SH3 L15; AD L16–37 | header, §7 |

---

## What V002 does not change
- It adopts nothing.
- It moves no status.
- It does not decide DQ-1..DQ-6.
- It does not choose between the PR F1 and TO/0077 L1 wordings.
- It does not lift the PAUSE.

Any point still marked [CLAUDE READING] or [UNCERTAIN] in V002 is open for distinct review.
