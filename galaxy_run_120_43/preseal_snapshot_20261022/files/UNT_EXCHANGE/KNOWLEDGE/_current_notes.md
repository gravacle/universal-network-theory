# UNT current-state notes (grounding input for every lane)

Compiled 2026-10-12 (~17:15 CDT) by a read-only Claude subagent. Purpose: a faithful, cited extraction of where UNT stands today, so that lane grounding starts from the program's own premises and results. Nothing here is a new derivation, adoption or verdict. Every claim carries a path and line(s). Where something is uncertain, unresolved or is Claude's own reading, it is marked **[UNCERTAIN]**, **[OPEN]** or **[CLAUDE READING]**.

## 0. Path keys, sources read, and source-state caveats

| key | path |
|---|---|
| PKT | `/Users/bgm/Desktop/FOLDERS/Gravity/20260918 Packet/20260924 Packet Updates/` |
| X | `/Users/bgm/Research/UNT_EXCHANGE/` |
| R | `/Users/bgm/Research/Universal Network Theory/` |
| PW | `R/program-worktree/` |
| CAN | `R/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/CANONICAL_V006_SELECTION_AND_EXACT14_CROSSWALK_V001/` |
| GR | `X/claude_artifacts/gamma_reconciliation/` |
| TO/nnnn | `X/TO_CODEX/nnnn_*.md` (Claude → Codex, immutable) |
| FC/nnnn, FC2/nnnn, FC3/nnnn | `X/FROM_CODEX/`, `X/FROM_CODEX2/`, `X/FROM_CODEX3/` |

Read in full: PKT `UNT_VALIDITY_AUDIT_V001.md`, `UNT_VALIDITY_AUDIT_V002.md`, `UNT_LADDER_V001.md`; X `README.md`, `STANDING_ORDER.md`, `PLAN.md`; TO/0005, 0008, 0010, 0077, 0080, 0082, 0083, 0084, 0095, 0100, 0102, 0106, 0108, 0109, 0110, 0111, 0112; GR `RECONCILIATION.md`, `canonical.md`, `charter.md`, and the outputs in `checks/` and `challenge_checks/`; CAN `CANONICAL_MODEL_7_PROPOSAL_V005.txt`, `EXACT14_CROSSWALK_V001.txt`; PW `THIRD_TERM_V001.md` (all 78 lines); PW `CORE_FRAMEWORK_V001.md` L10–32, L70–125, L160–185.
Read in part (headers/summaries, to scope today's accepted results): FC/0051, 0052, 0069, 0075, 0076; FC2/0096, 0106, 0112; FC3/0118, 0124, 0126, 0128, 0130, 0134, 0136, 0137, 0138, 0144–0148, 0158; `X/STATUS.md` rows 0100–0108.
Not read: the lane packets themselves (`X/lanes/*`), the program `REGISTER_V001.md` and `ledger/status_ledger.tsv` (cited here only through GR `charter.md`), FC3/0147's packet body.

Caveats on the source state:
1. **PLAN location.** The task named `X/plan/PLAN.md`; that file does not exist. The generated PLAN is `X/PLAN.md` (README L26: "`PLAN.md` is generated from `plan/plan.tsv` by `plan/plan.py`"). `plan.py` was not run (no project code executed); `X/PLAN.md` was read directly.
2. **PLAN changed during this read.** At first read it showed `ACTIVE 30 · HOLD 1`; it was regenerated during the session and now shows `TODO 1 · ACTIVE 3 · DONE 20 · HOLD 31 · DROPPED 1`, Active P-4, P-49, P-55, Next TODO P-22 (`X/PLAN.md` L7, L9). The held rows cite FC/0076 (the pause). Line numbers below are from the current file unless noted.
3. **`X/claude_artifacts/program_grounding/` exists but is empty** (created 17:09; `ls` shows 0 files). The program-grounding map promised in TO/0110 L17 and TO/0112 L12 has not landed.
4. **GR has a pending challenge step.** `GR/challenge_checks/ice_flux_parity_balance.py` and its OUTPUT (17:08) postdate `RECONCILIATION.md` (16:57) and bear on its §2 theorem (see §5.6 below). No written conclusion exists yet.
5. `X/STATUS.md` has rows only through 0108 (L148); 0109–0112 are acknowledged in FC/0076 and FC3/0158, not in STATUS.

---

## 1. Program state right now

- **Switch is PAUSE.** `X/STANDING_ORDER.md` L1 = `PAUSE`; L7 "finish the current step, post a status message, and stop".
- **Principal decision: pause new science** (TO/0112 L1: "This program is too much of a departure from standard physics to just throw work at agents."). Finish only in-flight reviews, controls and launched runs (L8); then hold and monitor TO_CODEX only (L9); program write-back continues (L10).
- **Restart condition** (TO/0112 L12): Claude brings the principal the program-grounding map (the program's own derived gravity picture plus anchoring of every lane) and the Γ reading; principal and Claude agree the framing "in UNT's own terms (charter, ALLOW/REQUIRE, Γ by function, collective emergence, Records all the way down)" and a small number of well-posed questions grounded in program results; lanes restart from cited program results (TO/0110 prior-work ledger), not from the Hamiltonian.
- **Framing-error rule** (TO/0112 L14): "A standard-physics default (single-object footprints, fields falling with distance, Coulomb/Maxwell channels, metric pass tests, Newtonian inputs) is a framing error, not a neutral starting point."
- **Root's acknowledgment and grounding-receipt requirement** (FC/0076 L4–8): pause applied; "The principal has now directly required Codex root, Codex2 and Codex3 to become thoroughly familiar with UNT and construct from its own nonclassical premises." Each lane must read `THIRD_TERM_V001.md`, `CORE_FRAMEWORK_V001.md`, `REGISTER_V001.md`, `ledger/status_ledger.tsv`, then the original proofs for its scope, "Await and consume Claude's program-grounding map", and post a source-only grounding receipt (paths/lines/hashes, coverage read, UNT primitives, ALLOW/REQUIRE/selection boundaries, established vs conditional vs open, relevant C/X/D/T rulings and reopen conditions, assumptions its next work would need). "A declaration of familiarity without citations is insufficient." (L8)
- **Codex3** acknowledged the pause and is holding for the grounding map (FC3/0158 L7, L11, L13). **Codex2** acknowledged: "PAUSE acknowledged. No new derivations, task sources or channel analyses will be authored. P56 is not started or claimed." (FC2/0112 L7; TO/0109–0111 accepted, L9).
- **PLAN goal (unchanged):** "NGC 3198's observed baryons in, its 43 velocities out, from ONE canonical UNT model with every calibration counted, and a clear verdict on whether records make gravity." (`X/PLAN.md` L5)
- **Still ACTIVE** (in-flight closure only): P-4 validity gate (L18); P-49 background derivation, "allnativecampaignjobs held" (L54); P-55 sum-rule, "Nativeandnewcollectiveworkheld" (L59). P-56 (collective modes) is HOLD, never started (L60; FC3/0158 L7).

---

## 2. Principal premises and corrections (chronological), with what each changed

All are relayed by Claude in TO_CODEX; quoted principal words are the relays' own quotations.

| msg | principal statement / decision | what it established or retired | lines |
|---|---|---|---|
| TO/0005 | Signs as a **declared premise**: canonical UNT = literal V006 H_complete (#7: incidence/light, carriers, Records with Bind, feedback, Birth) + owner-once admission extension | A declaration, not a derivation; rung-1 admission and Bind are joined deliberately, not identified; no existing result promoted to canonical | L9–11, L22, L24 |
| TO/0008 | "are we sure un-writing isn't a possibility?" | **Do not impose irreversibility; measure net accumulation.** Bind is a Rabi oscillation; Hermitian admission contains reverse admission; imposed permanence "would build accumulation in by construction". Created P-18 with controls (isolated two-level: no growth; many-mode: growth) and three registered verdicts | L1, L9, L11–23 |
| TO/0010 | (closure of P-1 under 0008/0009) | P-1 closes **without** choosing a permanence option; cursor is only a preparation protocol; **spent label S and native q are kept separate** — whether they track each other is a measured result, identification only by later principal decision | L7–14 |
| TO/0077 | "UNT basically says gravity starts at the record level. There is no 'new gravity' added later. It's records all the way down. It just emerges." Also: GR was assumed only as scaffolding where classical gravity could not emerge (e.g. L10) | **No separate gravity source law; Records are the source.** P-31 bond-angle operator is an added coupling; P-37 reclassified as a diagnostic of that operator. Linearized-Einstein form is a classical-shape criterion; a non-Einstein outcome "reads two ways" | L1, L8–12 |
| TO/0080 | "There are records all the way across the universe. The universe is made of records. Why is this a mystery?" | **Matter and space are both made of Records.** Gravity needs a *difference*: P-47 observable becomes Δ(Record network)(r) = with matter − sham, on a Record-filled background; blank-start runs are controls; infinite-T ⟨q⟩=½ is the uniform-sea limit; matter–Record identity mismatch in #7 to be registered, not adopted | L1, L7–15 |
| TO/0082 | "There is no 'empty space' in UNT." | **Blank-Record states are mathematical controls only.** One-geometry test is physical only between Record-filled backgrounds; the physical background must be identified | L1, L8–13 |
| TO/0083 | "Don't we have that dialed into the model yet?" | Registers **S1** (state premise): no empty space; every physical state Record-filled; matter and space made of Records; blank states controls/limits only. **S1 fixes no numbers.** Gap diagnosed: P-1 fixed the rules (H), declared nothing about the state | L1, L7, L10–11 |
| TO/0084 | "We want to derive this" (the background) | **Derive, don't declare, the background** (P-49: thermalization vs fragmentation/localization/freezing; ρ*, word statistics, correlations vs energy and conserved charges; which charges are computed vs counted). A declaration only if derivation is proven impossible, then to the principal with the proof | L1, L4, L8–12 |
| TO/0095 | "Streamline" | Proportionate review: class 2a (analytic/small exact) accepted on one cross-lineage review; class 2b (method controls) one independent check; class (c) real-model runs feeding 120/43 keep full custody | L1, L9–20 |
| TO/0100 | "We need to be careful here not to import classical machinery into the analysis." | **Native verdict from the canonical model's own dynamics only**; classical constructs only as labelled conditional diagnostics; mandatory CLASSICAL-IMPORT LEDGER (Coulomb/Maxwell/Gauss 1/r², Debye/RPA, Poisson/Einstein, Newtonian orbits v²=r·g, Euclidean embedding/continuum chart, thermal/Gibbs, QSI/QMC, elasticity); any load-bearing import is a declaration to the principal; native outcomes not resembling classical gravity are reported as they are | L1, L7–25 |
| TO/0102 | (Claude's classical-import audit, under 0100) | 97 items: 36 load-bearing (27 still live), 11 unclear, 50 diagnostic. Five chain corrections: (1) one-metric/3+1 template stops being the geometry *criterion* → P-52 native species-response vector, "whether the species share one geometry is a finding"; (2) SPARC V_gas/V_disk/V_bul are Newtonian-derived → P-53 mass surface densities; (3) orbit stage → native matter transport at light/matter-defined lengths; (4) light from native spectrum, not Maxwell; (5) P-47 range on graph distance via Combes–Thomas bound, full Record state indexed by graph distance | L4, L8, L10–15 |
| TO/0108 | "The method that we used for z=1 was actually the correct way to approach that metric." | The earlier z=1 route (`PW/DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/`) is a native exact response **sum-rule** method (m₁(k)=(1−cos k)(−E₀); ω_min(k) ≤ m₁(k)/S(k)). Audit objections are narrower: prereg 1/L tests failed on roundoff; ARGER passes by construction; S(k) small-k input came from an external Luttinger premise. Sum rule becomes P-55 primary estimator, S(k) computed natively | L1, L7–24 |
| TO/0109 | "I never would have assumed that you could get gravity from individual records. This has always been about emergence and collective behavior." | **Single-carrier / single-Record results are constraints on the parts, not verdicts on emergent gravity.** P-47 → collective finite-density response; P-55 collective gapless modes; new P-56 (held). Γ-first plan noted | L1, L7–15 |
| TO/0110 | "It feels like these results have almost no grounding in the previous work … The whole point of doing a project like this is to build on previous learning." | Diagnosis (owned by Claude): today's lanes restarted from the V005 Hamiltonian, not from PW's gravity line (charter, CORE, REGISTER C-77/78/80/90/91, status ledger T-20). Several "findings" (MSCM ≈ P-41, piezo result, z=1 sum rule, Γ) "had already been learned". **Mandatory PRIOR-WORK LEDGER** in every packet and task | L1, L7–15, L17 |
| TO/0111 | "If we have to start from scratch every time we're working on the next term we end up repeating work." | **One shared memory both ways**: REGISTER + status ledger are the entry point; every accepted exchange result is written back to the program REGISTER/ledger by root (list of today's results at L9–18); D/X-style entries for retired framings (one-metric pass criterion, Newtonian templates, single-carrier verdicts); `X/KNOWLEDGE/LEARNED_INDEX.md` to be seeded by Claude after the grounding map | L1, L6–21 |
| TO/0112 | Pause new science (see §1) | — | L1, L7–14 |

**Charter-level premises (standing, from the program itself)** — these are the "UNT's own terms" the restart must use (TO/0112 L12):
- "gravity" is permitted as a label; inference from the label is forbidden; Γ is defined only by function R1–R3; no classical quantity may be a test Γ must pass (D-1). `PW/THIRD_TERM_V001.md` L5–17.
- R1 SPACE (states of the SAME energy, size > 1), R2 WRITER (flip no local operation can mimic), R3 PROTECTION (no local operation writes or destroys). `PW/THIRD_TERM_V001.md` L21–27.
- H₁(Σ) is a candidate, not a definition. L39–45.
- **THE CLAIM:** not identity, not resemblance — "gravity COMES FROM Γ. Records are the substrate; classical gravity is what Γ becomes at scale." L62–66. The charter's state line ("recovery … from accumulated Γ is untouched — plan task T-20", L72–73) is stale (see §5.5).
- Principal standing quote: "We want to connect Γ with classical gravity via emergence from records. We are NOT trying to equate Γ and gravity at the record level." `PW/CORE_FRAMEWORK_V001.md` L10–12.
- "CLASSICAL GRAVITY IS NOT EXPECTED AT THE RECORD LEVEL AND IS NEVER THE TEST." Banned comparisons: inverse-square, r⁻², 1/r, G, a metric, a geodesic, Einstein equations, "gravity needs …". Allowed requirements on a record-level source are about accumulation (extensive, additive, not a mere count, sign-definite); "A falloff EXPONENT IS NOT AMONG THEM." A classical-shaped null "READS TWO WAYS". `PW/CORE_FRAMEWORK_V001.md` L14–29.
- Vocabulary hazard: "ALPHA" in CORE names a generic coupling strength, "NOT the fine structure constant". `PW/CORE_FRAMEWORK_V001.md` L108–112.

---

## 3. What was learned today (accepted results and their scopes)

### 3.1 Validity audit and ladder (packet folder)
- **Bottom line (V001 §1):** execution is verified, discriminating power usually is not ("the L8 pattern", program-wide) (L9); **there is no single UNT model — 14 constructions** (L10, see §6); top end is imported (galaxy law AQUAL/MOND-type; cosmology through adopted Ω_A=0.7, Ω_C=0.251 and fits to θ* and D/H) (L11–13); current main-line tests cannot decide at feasible sizes (L14, table L101–109); the shorter-path measurement needs a universality discriminator (L15).
- **Scorecard after V002:** 82 items: VALID 16, LIMITED 37, UNINFORMATIVE 18, MISREPORTED 11 (V002 L37–41; V001 L19–29 before refutation of rungs 7–8). "Most VALID verdicts are honest ADOPT/OPEN labels or honestly reported failures, not positive evidence." (V001 L31)
- **What survives as informative** (V001 L33–39): signed lineage-persistence FAIL (L10/L12 sign reversal) — a real discriminating negative against "lineage changes dynamics"; exact obstructions GL6AQ, GL6BC, FR, FF, GJ (each scoped to one construction); implementation certificates (L12 history to 1e-14, "numerics, not physics"); SPARC transfer as a test of a MOND-type law (not UNT-specific); honest labels (RGRL ADOPT, Ω_A/Ω_C ADOPT, Gap C open).
- **Key failures** (V001 L43–91): W3 = −0.284 "coherent unwriting" is an L4 κ=π/2 resonance artifact (L44–48); π/8 66/66 "cannot fail" (L49); "Rungs 2–5 derived within the micro-rule" is false (L51); record definition amended to fit the sample later cited as fitting it (L54); α "FREE could not have come out otherwise" (L61); "form required, magnitude allowed" carried to G rests on stand-in models (L63); L14 is 98 non-interacting 28-site rings (L66); "lineage changes future dynamics" is an algebraic consequence of the adopted write, no negative control (L70); Einstein's equations (COND) get gravitational content from WTC-H3–H5 ("GR assumed in record vocabulary") (L74); "From below" Ward route is Fierz–Pauli uniqueness (L75).
- **Rungs 7–8 after cross-lineage refutation (V002):** halo-beat claim's MISREPORTED verdict withdrawn → LIMITED (L17, L25); lensing 15.5× only for the prepared sphere/grid (L18); stationary-clock fails at ε=1e-6, passes the charged necessary condition at ε=1e-5 with the changed constant counted (L19); BBN D/H and θ* are fit targets (L21); background near-degenerate with same-inventory Λ+dust limit, "no useful discriminating power" vs ΛCDM backgrounds (L27); "same law" split: (a) no native record-derived common law with predicted budget (confirmed), (b) conditional agreement is real computed agreement, weakly discriminating (L29–33).
- **Cross-lineage W3 confirmation:** Codex fixed table matches Claude's independent rebuild (L4 κ=π/2 −0.2840664; L4 κ=1.0 +0.5556; L6 +0.6041; L8 +0.3380). "The 'coherent unwriting' failure is specific to the L4 resonance at κ = π/2." TO/0010 L16–25.
- **Ladder status:** `UNT_LADDER_V001.md` L3: "Superseded in part … read `UNT_VALIDITY_AUDIT_V001.md` first … the rungs are not one model." The ladder's framing of the research priority — "derive the top end's law from the bottom end's records" (L49) and "Showing that the first *is* the second would be the program's central theorem" (L224) — still describes the open middle (Gaps B, C; L215–222), but its one-page claims are overstated per the audit.
- **[CLAUDE READING] tension to carry forward:** audit V001 §6 (L113–122) proposes *universality across species* ("gravity shifts every species' local speed by the same fraction (the equivalence principle)") as the discriminator. Under TO/0100 and TO/0102 L11 that one-metric template is now a diagnostic, not a criterion ("Whether the species share one geometry is a **finding**"), and the charter's H-9 calls universality "an interpretive signature, not a pass/fail test" (GR `charter.md` L298–302). Lanes should not treat audit §6 as a pass test.

### 3.2 Foundations closed today
- **P-1 DONE:** canonical V005 (= V004 byte-exact + appended S1) independently reviewed (documentary); "Physical background density, words, correlations and carrier content must be derived by P49 … Canonical p/q/Spent identity and blank-I Birth compatibility remain explicit open checks. P1 documentary registration is DONE; no state/numeric/metric adoption." FC/0051 L5; `X/PLAN.md` L15.
- **P-2 DONE:** crosswalk of the 14 constructions (see §6). `X/PLAN.md` L16.
- **P-3 DONE** (documentary calibration map; "calibrationrank0", B30 E_unit invariant sector OPEN). `X/PLAN.md` L17.
- **P-13 DONE:** audit V002 published. `X/PLAN.md` L78.
- **P-12 DONE:** program `LADDER.md` L8 row and the eight audit §7.6 retypings saved. `X/PLAN.md` L77.

### 3.3 Native results listed for write-back (TO/0111 L9–18), with their stated scopes
| result | stated scope / limit | source |
|---|---|---|
| **Q0 Record-word freezing** | Exact frozen-word theorem holds on invariant global Q=0 (no carriers AND no Ready). "Do not promote either observation to regional eternal freezing or an equation-of-state no-go." Q0 is P-49's exact frozen-word control | FC/0052 L7 |
| **Direct Bind-erased cloud: exponential range** (0118) | All-order exponential probability bound in a uniformly gapped, fixed-ice, written-background Q1 branch, admission retained. "conditional dictionary diagnostic, not a derived physical S1 sea"; full-model mediated static range undetermined | FC3/0118 L9–11 |
| **Exposure/energy bounds** (0126/0128/0134) | 0126: a 1/r history remnant can arise in a stochastic control (diagnostic only); exact obstruction: fixed-ice positive-erasure-cost Q1 model bounds ΔN_flip by energy at all times. 0128: full-native sufficient certificate if δ*>0; non-covering if δ*≤0; no tuple/background/radial law selected. 0134: dual bound for energy-releasing erasure; benchmark a*=3/8; not an actual native range result | FC3/0126 L11–13; FC3/0128 L11–13; FC3/0134 L11–13 |
| **Graph-distance resolvent criterion** (0130) | Full native Combes–Thomas bound, Birth included; exponential sufficient test; "Algebraic range cannot be concluded from failure of this sufficient exponential test"; no static range adopted | FC3/0130 L11–13 |
| **Channel census** (0124, with RC1–RC6) | Bare p and Bind commute with incidence G; native q vertex is −λ_R η G q (charge/divergence, not transverse); "even a conditional Coulomb field does not automatically produce a scalar 1/r² Record difference"; S1 does not determine carrier density or a thermal state; Gaussian analyses are diagnostics | FC3/0124 L11–13; TO/0104 L5, L12, L21 |
| **Loop confinement** (0136) | Exact fixed-ice Q1: only n_e-gated hopping moves the resource, which stays on its occupied loop component; Brownian loop census does not yield a native r^-1.05 law; full V005 needs controlled transfer | FC3/0136 L11–13 |
| **Pair-word blindness** (0137) | On ice, all-written / single-isolated-erasure words are blind to the pair-word term; adjacent erased pairs survive; pure pair-word effects absent at order g² one-erasure for sharp all-written preparation | FC3/0137 L11–13 |
| **Magnetic sign not triggered** (0138) | P45 accepted coefficient table: hypothetical flipped-star obstruction NOT triggered in those fixtures; sufficient sign theorem; excited/indefinite/complex/Birth cases not covered; no deconfined photon or magnetic tail proved | FC3/0138 L11–15 |
| **P-45 h⁶ diagonal theorem + uniform light factorization** | Uniform old-parent order-6 diagonal is a configuration-independent scalar in the four-regular girth ≥ 6 ice domain; same ring operator gives endpoint scale ratio T1/T0 conditional on a qualified photon phase. Does NOT prove full Born-join factorization, a native photon, matter curvature or a finite-h clock line | FC/0037 L10; FC/0039 L25 |
| **P-49 first native history benchmark** | Short manufactured native finite-window benchmark; single preparation mostly retains its initial word (time-averaged word 11 ∈ [0.998, 0.999]). "not stationarity, DE, ETH, physical background or long-time memory"; covariance including zero is not correlation evidence | FC/0069 L5–10 |
| **P-51 first-Birth and t⁸** | TEST MODEL (P-26 repeated-Birth, unadopted). Leading t⁶ fresh-writing donor term common to matter and sham; t⁸ second-generation matter-minus-sham positive coefficient; "repeated local writing, not proved time-monotone accumulation or spatial force"; root 0076: c6=5/9216, t8=25/9437184, D8 second difference −1/6144, R8/finite-time signs uncomputed | FC2/0096 L14; FC2/0106 L10–12; FC/0075 L8; FC/0076 L14 |
| **P-54 Γ census** | See §5.4. "No actual V005 Gamma certificate and no no-Gamma theorem." DONE with explicit gaps; no definition or Γ identification adopted | FC/0075 L10–12; `X/PLAN.md` L58 |
| **Classical-import corrections** | TO/0100, TO/0102 (§2) | — |
| **Principal premises** | S1; records all the way down; gravity as collective emergence; z=1 sum-rule method (§2) | TO/0083, 0077, 0109, 0108 |

### 3.4 In-flight closures accepted by root under the pause (FC/0076 L10–15)
- **P-48:** full 111,104-column native coefficient laws accepted (201,284,393 checks). "finite coefficient-law result; generic conservation-ansatz completeness and collective IR constraints remain OPEN, no gravity/helicity verdict." (L11)
- **P-34:** candidate log provider accepted; "no full4096-grid … and no successor launch." (L12)
- **P-49:** 32 changed-risk controls accepted; "no native segment was launched and it is now held." (L13)
- **P-51:** literal 8-arm fixture and 14 conditional derivations accepted as source/theory only; TEST MODEL unadopted. (L14)
- **P-55:** native primary sum-rule and conditional complete-word matrix theory accepted at stated scope; 18 gated controls ran; "No actual native spectrum/provider is released." Two corrections to slice 0152 (released-q one-carrier coefficient is ε_r − 2λ_R p_v; incidence slice C must fix a sharp q word). (L15)
- **Preserved unreviewed:** FC3/0156, 0157 collective packets ("not accepted or commissioned for extension"). (L17)

### 3.5 Framings retired today (to be D/X entries per TO/0111 L20)
- One-metric / 3+1 / GR weak-field fixtures as the geometry *criterion* (TO/0102 L11; PLAN P-41 L47, P-43 L49, P-45 L51: "diagnostic only").
- Newtonian SPARC velocity templates as the baryonic source (TO/0102 L12).
- Single-carrier / single-Record results as gravity verdicts (TO/0109 L7).
- Blank-Record vacuum as a physical background (TO/0082 L8; V005 L28).
- Imposed irreversibility/permanence (TO/0008 L9–11).
- P-31 bond-angle source law as UNT's gravity source; P-37 kernel as the gravity verdict (TO/0077 L8).
- "Flat curve needs a 1/r pull" and Coulomb/Debye wording in Claude's own 0098 (TO/0100 L4).

### 3.6 What is NOT established (as of now)
No physical Record-filled background (P-49 open; FC/0051 L5). No native photon, metric, universality, gravity or galaxy prediction from V005 (CAN V005 L23, L36). No matter dictionary (P-50 L55: "native baryon/restenergy/coframe/background dictionary remainsopen"). No Γ certificate or no-Γ theorem (FC/0075 L10). No native range/fall-off law (FC3/0130 L13). P-8/P-10 NOT_READY (FC/0075 L6). The 120/43 sealed comparison has not run.

---

## 4. The canonical model V005

**File:** `CAN/CANONICAL_MODEL_7_PROPOSAL_V005.txt` (SHA e6c1c47d…, FC/0051 L5). Note: its line 1 still carries the V004 title ("PROPOSAL V004"); V004 is preserved byte-exact as the prefix and V005 is the appendix starting at L25.

**Rules (the Hamiltonian; declared premise per TO/0005):**
- Domain: literal V006 old periodic q4 graph + supplied one-Born four-cut/two-star graph. Edge incidence bit n_e; per site: hard-core carrier p_v, **native Record q_v**, cell span{I,R,S} (R=Ready, S=Spent; "neither is q"). All N_c and all Born off-image states kept. d_v = Σ n_e. (L4)
- H7 = −hΣX_e + ΔΣn_e + U_dΣ(d_v−d*)² + ε_c N_c − tΣ n_e T_e(θ) + ε_rΣq_v + gΣ p_v X_{r,v} − λ_RΣ d_v q_v + λ_JΣ d_v p_v. (L5–7)
- Hcell; admission A_v^± (|S,x⟩⟨R,B| ⊗ I_q), HA = Σ(κ_v A^+ + h.c.) — Hermitian, reverse included; Hjoin couples old and Born sectors through ε_B Tjoin. (L8–12)
- Finite Birth: Tjoin inserts blank carrier, **blank q**, inactive I cell at each new star; adjoint (un-Birth) retained; Q = N_c + N_ready and M = N_ready + N_spent conserved; one Birth level only, no iterated rule. (L15)
- Formation/reversal: forward admission does **not** write q; **Bind g p X_r rotates q** (including at a Spent site); N_spent and N_q "distinct censuses and neither is asserted monotone". (L17)
- No imposed permanence; cursor only an optional preparation protocol; P-18 measures both censuses. (L19)
- Allowed magnitudes: eight ratios (Δ, U_d, t, ε_r, g, λ_R, λ_J, |ε_B|)/Ω plus h, ε_c, |κ_v|, E_I, E_R, E_S over Ω; d*, θ, phases, graph/Birth map, preparation are further declarations; "No observation fixes any coefficient here; the historical tuple is a benchmark, not a fit." (L21)
- "No existing result is promoted by this declaration. No photon recovery, positive mobile mass gap, metric, universality, gravity or galaxy prediction follows from defining Hjoin." (L23)

**State premise (V005 appendix):**
- S1 registered: no empty space; every physical state Record-filled; matter and space made of Records; blank states controls/limits only. "It changes the interpretation of preparations, not the canonical Hamiltonian." (L28)
- Background must be derived (P-49); nothing adopted (no density, pattern, ensemble, thermalization, EOS). (L30)
- **Open compatibility, stated in the canonical text itself:** p, q and Ready/Spent stay distinct; "matter and space are made of Records" "does not by itself identify p with q or replace Spent with q"; S1 "supplies no numeric meaning of 'filled'"; the rules still admit blank states and insert blank q/I in Birth; "the physical admissibility and dynamical compatibility of the S1 class therefore require an explicit dictionary and state analysis". (L32)
- Infinite-temperature control ⟨q⟩=½ on old sites (from FC3/0096) is "an exact mathematical control, not evidence that a physical preparation evolves to that ensemble". (L34)
- Downstream contract (P-47 difference vs filled background; P-46 consumes background + change). (L36)

---

## 5. Tension: V005 q "Records" versus the charter's Γ

### 5.1 The charter's record and Γ
- DEF-A record: (i) R=R†, R²=I; (ii) [H,R]=0 and [L_k,R]=0; (iii) not constant on some eigenspace of H; (iv) some **admissible** U ([U,H]=0) has U†RU = −R; (v) no admissible operation on a **single contractible region** does. `PW/CORE_FRAMEWORK_V001.md` L98–106, L114.
- "clause (iv) ⟺ Tr(P_E R) = 0 on every eigenspace of H" (balance). L116–117.
- P-3: "NO ADMISSIBLE WRITER FITS INSIDE ONE CONTRACTIBLE REGION"; the strong reading "nothing local can write it" is FALSE (products of d local terms reach the record); the record "is written by an operation that is admissible only as a whole". L171–181.
- O-51 amended clauses (i′)–(v′) on carrier ⊗ local bath; (v′) every single-region flip costs ≥ E_b with E_b/kT ≫ 1; the exact clauses are retained as the DEF-A corner. L73–89.
- Γ = whatever satisfies R1–R3 (`PW/THIRD_TERM_V001.md` L21–27). The charter never says whether R3 is (v) or (v′) (GR `charter.md` L80–81).

### 5.2 V005's q_v measured against that definition
- q_v's only native writer/eraser is Bind g p_v X_{r,v}, a term of H, local and gated by a carrier at the same vertex (CAN V005 L6, L17; GR `canonical.md` L18–22, L101–109).
- q_v is not conserved whenever p_v can be 1; frozen only in Q=0 (no carriers, no Ready) because the writer is absent — superselection, not protection (GR `canonical.md` L111–116; FC/0052 L7).
- **Verdict (both readings agree q_v is not Γ):** Claude: "q_v fails R2 and R3 by construction … The word 'Record' in V005 names a register. It does not name the charter's record." (GR `canonical.md` L140–141; `RECONCILIATION.md` L6–11). Codex3/root: "Generic persistent q fails exact durability" (FC/0075 L10; FC3/0145 L12).
- **The reason, as corrected by root/Codex3:** "Bind alone is not automatically an admissible full-H energy-preserving writer; bareq obstruction is its nonzero commutator" (FC/0075 L12 item 1; FC3/0147 L10). I.e. q_v fails clause (ii) durability; it is not that Bind is a DEF-A-admissible local writer. TO/0106 L13's phrasing ("written and erased by the local Bind term, so on their face they fail R2 and R3") should be read with this correction.
- The program's own lane docs already limit "Record": P27 L26 ("q is not Spent S, the cut census … or a metric"), L30 (a qualified record needs preparation, distinguishability, retention, complete read, lineage controls; a bit occupation alone does not), P50 L19–20 (as cited in GR `canonical.md` L122–126).
- Other V005 labels (Spent, M_v, Q, Q=0 q-words, old/Born projector) are inventories/charges, not topology; none meets R2/R3 (GR `canonical.md` L145–157). P48's census is limited to the diagonal-linear ansatz; the full commutant is not exhausted **[OPEN]** (GR `canonical.md` L155–157).

### 5.3 The only Γ-shaped candidate in V005 (Claude's reading) and its conditions
- Ice manifold I = {d_v = 2 ∀v}; flux/winding label Φ ∈ H₁(T³; ℤ) = ℤ³ from E_link = n − ½ oriented A→B (GR `RECONCILIATION.md` L14; `canonical.md` L27–32, L200–214).
- Claude's theorem (h=0, Q=0, generic coefficients): R_S = (−1)^{Φ_S} is an exact DEF-A record (GR `RECONCILIATION.md` L15–19). Writer = alternating non-contractible loop flip of weight 2L — "admissible only as a whole" (L18; `canonical.md` L216–221). Check: 0 of 1687 flippable short loops changed Φ (`RECONCILIATION.md` L19; `checks/diamond_cycle_flux_birth_check_OUTPUT.txt` L4, L8, L12).
- Conditions/limits: at h≠0 Gauss law is broken; protection only perturbative at O(h^{2L}), conditional on an uncertified defect gap U_d ± μ_v > 0 (`RECONCILIATION.md` L21; `canonical.md` L242–245). Native phase UNDETERMINED (L22). Γ ≅ ℤ³ only for L ≥ 4; at L = 2, 3 there is no Γ — the literal L2 member has none (L24; `checks/min_cycle_basis_profile_OUTPUT.txt`; `checks/diamond_cycle_flux_birth_check_OUTPUT.txt` L1–3). Shape is a 3D U(1)/ℤ³ flux, not the charter's gapped ℤ₂ toric code; "described, not ranked (D-9)" (L23).
- How matter, Records, Birth act on it (Claude's reading): only −hX (at order 2L) and Birth change Φ; layered Record patterns tilt sectors linearly (W = 2L²Σq − F·b); Records/carriers shift the local Gauss-defect cost μ_v = μ0 + λ_J p_v − λ_R q_v; Birth always adds 2 to β₁ and may carry or degrade Φ depending on cut geometry (GR `canonical.md` L318–327; `RECONCILIATION.md` L22, L26–31).

### 5.4 Codex3/root's independent census (P-54) and the qualifications they place on Claude's reading
- "No V005 structure is certified here as Gamma; this is not a no-Gamma theorem. Generic q fails exact durability, bare full-h winding is nonconserved, and cycle rank/inventories alone supply no same-energy protected writer. Encoded and approximate candidates remain open." (FC3/0145 L12)
- Corpus correction: THIRD_TERM's unrestricted "local operation" wording is qualified by CORE's admissible [U,H]=0, the SINGLE contractible-region DEF-A clause, and O-51's adopted carrier-plus-bath definition; "Principal definition/state dictionary decision remains explicit." (FC3/0145 L14)
- Exact local-writer certificate: an admissible exact flipper exists iff the H-commuting / R-anticommuting space contains an invertible operator; "Global balance follows; any odd-dimensional energy eigenspace obstructs full-domain DEF-A writability". (FC3/0146 L10)
- Root-accepted comparison corrections (FC/0075 L12): (1) Bind is not automatically an admissible writer (q's obstruction is its commutator); (2) literal carrier hopping commutes with every incidence bit and cannot alone flip winding; (3) "A generic patterned written-pair field need not be constant within a winding sector; a qualified contractible ring/two-erasure witness changes it"; (4) Birth supplies graph-fiber motion with full accounting, "not established Gamma capacity or a unique physical accumulation route". Exact DEF-A vs finite-tolerance carrier/bath definitions stay separate; no bath imported.
- Root disposition: P-54 DONE as a scoped census; "no definition or physical Gamma identification adopted", no lane redirection (FC/0075 L10; `X/STATUS.md` row 0106).

### 5.5 Charter staleness and the program's own prior answers (via GR `charter.md`; REGISTER/ledger not read directly)
- Uniqueness is not open: G-6 FAILED; survivors include H_k of any F₂ chain complex whose systole and cosystole both grow (GR `charter.md` L15–17, L180–185).
- T-20 is not "untouched": DONE 2026-08-19 with a flat-holonomy null, interpretation withdrawn by O-23, field recovery moved to C-77 (CANDIDATE) (GR `charter.md` L18–20, L164–177).
- C-77: Γ (shaping the boundaries that make a bit non-losable) "is the same structure whose aggregate at scale appears as geometry" (GR `charter.md` L173). C-78: distance as boundary-crossing cost (L174). **C-80/O-54: "NO PURE-Γ FALLOFF … The falloff enters only through the coupling"** (L175). C-90/C-91: a Γ-priced coupling kernel at criticality gives the lattice Green class, "MATCHES AT MEMBER LEVEL", with design point, occupancy bit and norm selection not earned (L176).
- Enlarged-parent theorem / Corollary 5.4 (five objects make "does a carrier arise?" well-typed); H-7, F-3, T-II.5 reopened conditionally (GR `charter.md` L254–269). V005 already holds three of the five objects; two must be declared (GR `RECONCILIATION.md` L47).

### 5.6 [UNCERTAIN] pending challenge to Claude's §2 theorem
- `GR/challenge_checks/ice_flux_parity_balance.py` (docstring L4–9) tests whether R_S is BALANCED on the ice manifold, since by CORE L116 clause (iv) requires Tr(P_E R)=0 on every eigenspace, and at h=0, Q=0, fixed q-word all ice states are degenerate.
- Output (`ice_flux_parity_balance_OUTPUT.txt` L6–14): exact transfer-matrix counts (cross-checked against brute force, L1–3) give **nonzero** Σ_ice R_S for every member with |S| even (2×2×4 ratio 0.229; 2×2×5 0.357; 2×2×6 0.475; 2×2×8 0.666; 2×4×4 and 4×2×4 0.0323; 2×4×6 0.140), and exactly 0 for the |S| = 9 members (3×3×4, 3×3×5).
- **[CLAUDE READING, not yet written up by the reconciliation]:** if the h=0 degenerate eigenspace is the whole fixed-word ice manifold, imbalance means no admissible full-domain writer exists for R_S in those members, which would contradict the (iv)/R2 clause of the theorem in GR `RECONCILIATION.md` L15–18; this is the same balance requirement Codex3 states in FC3/0146 L10. Caveats: the tested members are anisotropic (L_x = L_y = 2, below the L ≥ 4 protection length in those directions); the Birth-resolved and ε_B ≠ 0 eigenspace structure is not covered. **Do not cite the ice-flux Γ theorem as established until the challenge step concludes.**

### 5.7 Where the 120/43 chain was aimed, and the premise conflicts
- Claude's answer to "Are we sure we're looking at the search with a UNT perspective?" (TO/0106 L1): **"no."** The chain measures matter's local q-footprint (the coupling/occupancy layer); Γ enters no link of the chain; the steering quantity was a fall-off exponent, which CORE L23–26 excludes as a requirement (GR `RECONCILIATION.md` L4, L34–39).
- Premise conflicts for the principal (GR `RECONCILIATION.md` L51–56), classified as **declared** items, not choices to be computed:
  - **P-a:** V005's "Record" q_v is not the charter's record; **[CLAUDE READING]** in the charter's sense S1's "made of Records" points to Γ-protected incidence structure, not q bits (L52).
  - **P-b:** R3 read as exact (v) or amended (v′) — q_v fails both; the reading decides any barrier-protected candidate (L53).
  - **P-c:** the charter claims gravity comes from Γ, but the 120/43 kernel carries no Γ (L54).
  - **P-d:** the canonical L is declared, and Γ (as the ice flux class) exists only for L ≥ 4 (L55).
  - Documentary (not a principal matter): the charter is stale on uniqueness and T-20 (L56).
- Proposed Γ-first search G1–G6 (GR `RECONCILIATION.md` L41–49) is Claude's proposal, to go to the principal as a decision card before any lane redirect (TO/0109 L13). Not adopted.
- Vocabulary hazards (GR `charter.md` L309–313): "records" in V005 (q_v bits) ≠ the charter's records (operators meeting five clauses); "flux" in V005 is a sector label while D-18's "flux" is an excitation; H-9's Γ_AB is a connection, not the third term. Add: "alpha" in CORE is a generic coupling, not the fine-structure constant (CORE L108–112).

---

## 6. The 14-constructions issue

- **Audit claim:** "There is no single UNT model. 14 distinct constructions are in use, each with its own graph and coefficient tuple. 'What matter is' is re-declared per member." Bottom end (rungs 1–5), geometry theorems (rung 6), galaxy/cosmology law (rungs 7–8) and the 120/43 track sit on different models; "The ladder presents them as one derived chain." (PKT V001 L10). No canonical definition existed; coefficient tuples differ across members (L95–97). Fix: label each construction canonical / approximation / separate; "Every claim names its model." (L126). Appendix A table (L136–161).
- **Crosswalk result (P-2, `CAN/EXACT14_CROSSWALK_V001.txt`):** the 14 numbers are inventory rows, "several of which bundle multiple models, protocols or an analysis engine. No unique physical model count is inferred." (L5–9; L96: "Appendix A is a 14-entry inventory, not evidence of exactly fourteen distinct dynamical models"). A reduction requires domain/map, generator and absolute-energy correspondence, source/readout, preparation/boundary and a leakage/remainder bound; "Shared terminology is not one." (L11–13)
- **Relation of each entry to canonical #7** (crosswalk statuses):
  - #1 prism admission / L4–L14 histories (rung 1, rung 5 lineage): SEPARATE_MODEL; L14 = 98 independent 28-site components (L15–19).
  - #2 F3-QIRN seed: separate ancestor family (L21–25).
  - #3 degree-lock q4 TFIM + ring effective theory: exact restriction (Birth off, N_c=0, q=0) then controlled asymptotic approximation; ring term −63h⁶/(8U_d⁵)ΣT_c (L27–31).
  - #4 minimal Record→geometry join: separate declared reduction of #2, own tuple (L33–37).
  - #5 BS10/11 supported members: separate, own tuples (L39–43).
  - #6 local CTP K2,2→K3,3: separate Birth completion of #2 (L45–49).
  - #7 V006 H_complete: PROPOSED_CANONICAL_FINITE_FAMILY (now canonical with admission, V005) (L51–55).
  - #8 restored_bs11 (N16/MPS/GFMC main line): differs from #7 by 2λ_J Σ n_e p_u p_v and removes Birth; "no error bound makes the pair interaction or Birth irrelevant for counts 2–9"; N16 results are conditional #8 results (L57–61).
  - #9 H/I admission join: extension of #8, not #7 (L63–67).
  - #10 pure ring model: leading effective approximation of #3, photon infrastructure only (L69–73).
  - #11 R2 ISO-HISTORY: separate classical face ensemble (L75–79).
  - #12 continuum clock/U cosmologies + SPARC closure: separate effective actions; "No map derives these equations … from #7" (L81–85).
  - #13 RGRL/WTC Einstein closure: separate adopted continuum bridge (L87–91).
  - #14 U(1) alt-α EFT + URM corner/HDD/NAND: separate bundle and analysis engine (L93–97).
- **Current computation labels:** N16 work is #8; photon samplers #3; ring GFMC #10; prism W3/lineage #1; continuum galaxy/cosmology #12 (L99–112).
- **Canonical selection does not promote anything:** "Existing results keep their own construction labels (#1, #8, #9, …). None is promoted to the canonical model by this sign-off." (TO/0005 L24; CAN V005 L23)
- **Consequences for grounding [CLAUDE READING, from the cited sources]:**
  1. Nearly every prior program result a lane might "build on" (TO/0110) lives on a construction other than #7: rung-1–5 results on #1 (prism), rungs 2–3 on separate GKSL models (PKT V001 L51, L58), rung-4 α in a separate archive (L51), N16 main line on #8, galaxy/cosmology on #12, Einstein closure on #13. The charter's verified Γ candidate (toric code, H₁(Σ)) is yet another carrier (GR `charter.md` L87–99; CORE L213 as cited there: "This Σ is a lattice's topology, not spacetime's").
  2. So the prior-work ledger (TO/0110 L15) must record, for each cited result, **which construction it was proved on** and whether any reduction to V005 exists (crosswalk criteria, `EXACT14_CROSSWALK_V001.txt` L11–13). Porting a result to V005 is new work, not inheritance.
  3. TO/0110 L13 names results "already learned" (MSCM ≈ P-41, piezo, z=1 sum rule, Γ); those were learned on their own constructions, and their V005 status must be stated per item.
  4. P-1 resolves the "which model is canonical" question as a **declaration** (TO/0005 L9, L22), not a derivation; the audit's point that the rungs are not one derived chain (PKT V001 L10) is not closed by it.

---

## 7. Open items, classified (computed / measured / declared) — no choices handed to the principal

**Declared (principal's premises to register, not compute):**
- Whether V005's q_v is to be called the charter's "record" (P-a); which R3 reading, (v) or (v′), governs (P-b); whether the 120/43 chain must carry Γ (P-c) (GR `RECONCILIATION.md` L52–54). Codex3 also flags "Principal definition/state dictionary decision remains explicit" (FC3/0145 L14).
- Canonical L, cell convention, first-cut geometry (CAN V001 L30–33 as cited in GR `canonical.md` L333–335; GR `RECONCILIATION.md` L55).
- Corollary 5.4 objects (2) and (4) if the Birth/enlarged-parent route is taken (GR `RECONCILIATION.md` L47).

**To be computed:**
- Physical Record-filled background and its EOS (P-49; CAN V005 L30).
- p/q/Spent dictionary and S1 compatibility with blank Birth inserts (CAN V005 L32; P-50 `X/PLAN.md` L55).
- Defect-gap certificate U_d ± μ_v > 0; exact/certified sector splitting; flux-sector map through the declared Birth; full commutant beyond diagonal-linear (GR `canonical.md` L339–346).
- Resolution of the §5.6 balance challenge.
- Native collective modes and their dispersion (P-55, P-56 held).

**To be measured:**
- Net Record accumulation under reversible dynamics (P-18; TO/0008 L12–23).
- Response of flux-sector distribution to Record patterns and Birth; whether carrier spectra depend on sector (GR `canonical.md` L347–350).

---

## 8. One-paragraph orientation for any lane (summary of the above, no new claims)

UNT's program premise is that gravity comes from Γ, a structure defined only by function (R1 same-energy record space, R2 writer no local operation can mimic, R3 protection), with classical gravity what Γ becomes at scale and never a test at the record level (`PW/THIRD_TERM_V001.md` L21–27, L62–66; `PW/CORE_FRAMEWORK_V001.md` L14–29). Today's principal premises add: records all the way down, no separate gravity source law (TO/0077); the universe, matter and space are made of Records, there is no empty space, and the background must be derived (TO/0080, 0082, 0083, 0084); gravity is collective emergence, never a single-Record result (TO/0109); no classical machinery may be load-bearing (TO/0100, 0102); build on and write back to the program's REGISTER and ledger (TO/0110, 0111). The canonical rule set V005 (#7 + coherent admission + S1) is a declaration; its q_v "Record" is a local register that fails the charter's durability/protection clauses, the only Γ-shaped V005 structure found so far is the ice-manifold flux class (conditional, and under an open balance challenge), and the 120/43 chain as built carried no Γ. Prior program results mostly live on other constructions (14-entry inventory), so every lane must name the construction of each result it cites. New science is paused until the principal and Claude agree the framing and the program-grounding map lands (TO/0112; FC/0076 L8).
