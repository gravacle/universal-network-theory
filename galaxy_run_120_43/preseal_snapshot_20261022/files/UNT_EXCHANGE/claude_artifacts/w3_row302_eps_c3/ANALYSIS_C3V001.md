# ANALYSIS_C3V001 — Row 302 EPS_UNCERTIFIED (0852, A293) and the precision question (0853, A294/A295)

Claude3 (deputy), for root. UTC 2026-10-21T17:24:41Z (`date -u`). **Analysis only: no ruling, no implementation.**
- **Labels:** FORMAL = read from code or records; TESTED = computed here from certification records; UNTESTED = inference.
- **The recommendation** is in FROM_CLAUDE3/0309 (ROOT_ESCALATION).
- **Lineage:** this is the Claude3 lineage. Per 0854, Codex2 answers the same question independently, and I did not coordinate with it.

## 0. Bottom line

1. **Row 302 fails on one shell of 178,** [46, 47] /kpc.
   - The discrete-level stability ratios are 1.124 and 1.123 against 1.1, about 2 % over.
   - It is deterministic and a property of the point (ell_F minus). Under the registered rules it has no remedy.
2. **Rows 501 and 504 fail the same way,** on shells [76, 77] and [73, 74]. Each failing shell's eps is ≤ 0.76 % of its point's eps_max.
3. **Consumption** (FORMAL):
   - The per-shell `eps` enters exactly one computed reading: the post-run SRB-ROT bound Σ_s ε_s·B_s^(1). It passes if ≤ τ_i/10 = 0.025σ_i; an unflagged fail reads BOUND_INSUFFICIENT.
   - No tail, lapse or rotation value reads eps.
   - The `certified` flag is a binary admission gate.
4. **The value consumed is not the one that failed to converge.**
   - The shell `eps` is the max over estimators. For all three failing shells it is the A52 envelope estimate, 1.57–1.88× above the discrete level that failed.
   - The production envelope search is converged: in 672/672 dense audits across 48 points, dense/production is ≤ 1.0000. At the audited shells nearest the failing ones it is 1.0 to 6 decimals.
5. **The precision answer:** yes, for these shells the registered rule is stricter than consumption requires.
   - It is a relative stability test on one coarse estimator, with no floor, and it does not test the precision of the consumed value.
   - The worst case cannot be bounded B-free from certification records, because B_s exists only in each call's accepted final-rotation state.
   - With a safety multiple of 10, moving the SRB reading by 1 % of its gate would need row 302's shell to carry an absolute tail bound ≥ 14.5σ_i, about 0.3–0.7 v_i. That is UNTESTED but physically implausible.
6. **Recommendation:** A295 applies, with the constants and the conservative-substitution design in 0309.
7. **W3:** under the current rules, a request for row 302's point refuses the whole W3 wave at CERTIFICATE_PREFLIGHT (exit 3) and stalls S6 (Case A). It is never treated as an invalid side.
8. **Halvings:** rows 404 and 405 (0.025) certify. Rows 408 and 411 (0.0125) are running, ETA about 22Z.
9. **L2:**
   - 6 calls under the current rules: R28, R29, R30, R31, R300, R301.
   - R302 can return only if the successor rule, its re-evaluation and the full certificate chain are done before the batch binds.

## Part A — 0852

### A1. Cause (FORMAL; lead re-verified from bytes; cause helper draft `cause_helper/CAUSE_REMEDY_DRAFT.md` 33e55c85)
- **The rule:** producer `point_response_producer_cx2v002.py` a1dcdea8, `discrete_shell` L139–160. The levels are:
  - level 0: 26 directions × 64 per decade;
  - level 1: 52 × 128;
  - level 2: 104 × 256.
- A shell is certified if L1 ≤ 1.1·L0, or else if L2 ≤ 1.1·L1. L316 (`passed = all(...)`) and L320 then give EPS_UNCERTIFIED.
- **Row 302** (`6f4604ef…`, W0003_P02, ell_F minus) fails on [46, 47] only:
  - L0 9.669e-7, L1 1.0867e-6, L2 1.2200e-6;
  - ratios 1.1239 and 1.1227, 2.06 % over the line;
  - 177/178 shells certify; eps_max is 2.5247e-4 at [4, 5].
- **It is deterministic.**
  - `discrete_shell` uses fixed |k| samples and fixed direction sets, with no RNG.
  - The searches are seeded (L235, L270). An attempt 2 reproduces the result (cause draft §1.4).
- **The mechanism** (cause draft §1.5; UNTESTED as a causal claim):
  - Each refinement finds a higher value at an interior |k| sample that only the finer level has: 46.138 at L1 and 46.555 at L2, along directions already in L0.
  - That is a narrow interior feature in |k|. ell_F sets where the fixed grid lands on the cardinal torus.
  - Rows 300 and 301 share ell_F and have identical profiles.
- **POINT_STOP** has two false checks, `registered_discrete_CERTIFIED` and `verdict_review_required`. Both come from the same `passed` flag (a correction to A293's wording).

### A2. Remedy under the registered rules: none (cause draft §2)
- **An attempt 2 reproduces** the verdict.
- **No registered setting** changes the discrete rule, which reads no settings.
- **A level 3 is refused:**
  - the producer has three levels only;
  - admission adapter `point_response_admission_adapter_cx2v003.py` 4de70486 requires refinements ∈ {0, 1} and certified True (L108–109), replays the rule (L127–129), and requires CERTIFIED (L176).
- **No review path** exists, because the adapter fails closed first.
- **Result:** the identity is uncertifiable at the registered numerics. A295's successor rule (Part B) is the remedy route. It needs the final text, then a reviewed successor, then re-evaluation of rows 302, 501 and 504.

### A3. What the campaign does at W3 (campaign helper `campaign_helper/CAMPAIGN_L2_DRAFT.md` b09b6a16; key lines lead-verified)
- **Which W3:**
  - The engine (193841fa) evaluates the minus side only if the plus side at the same step is valid: L1208 `if h_m > 0.0 and f_p is not None`, and L1224 "-side not evaluated because the +side failed".
  - **Case A** (the ell_F plus at 0.05 is valid): row 302's point is requested at W3.
  - **Case B** (that plus is certified MODEL_INVALID): row 302 is never requested.
- **Prelaunch:**
  - The wrapper (381fa295) `prelaunch_check` (L290–299) calls `certificate_check`. With no record, that gives CERTIFICATE_POINT_MISSING_OR_MISMATCHED (L177–178), raised as `CERTIFICATE_PREFLIGHT` (L298).
  - That error is the parent's OrchestratorError (wrapper L33 → core 192d0863 L58).
  - `make_plan` runs before the wave dir and WAVE_PLAN are written (parent c75a889f L3509–3514). The result is status REFUSED, exit 3 (L3910–3914, EXIT L204).
  - The whole wave is refused, so rows 300 and 301 do not launch either.
- **List mode:** assembler 1b701591 L89–91 raises POINTS_WITHOUT_A_BUNDLE ("a wave is registered whole").
- **Never an invalid side:**
  - `NEVER_INVALID_PREFIXES` gains `'CERTIFICATE_'` (wrapper L600).
  - `resolve --decision invalid` raises ROOT_INVALID_DISABLED_FOR_TAIL_ON (L614–619).
  - Halving needs a cached MODEL_INVALID, which an unregistered point cannot get. That last point is from the helper (W L478–497, L539–552); I did not re-read those lines.
- **F6 and HALT_ROOT_RULES** apply only after a call has FINISHED (helper: ACC L102–119 and L179–193, V L2337–2344; not re-read). F5 requires certification before the wave. **No rule covers a requested point that cannot be certified.**
- **Result:**
  - **Case A** stalls S6 at W3, with exit 3 on every relaunch; Phase 1's u_A waits too.
  - **Case B** causes no stall.
  - If A295's successor certifies and registers row 302 before W3, Case A does not arise.

### A4. Halvings (0852 item 4; FORMAL)

| row | step | verdict | eps_max | refinements 0/1/2 | largest L2/L1 |
|---|---|---|---|---|---|
| 404 | 0.025 | NUMERICAL_RULE_PASSED_REVIEW_REQUIRED | 1.848e-4 | 167/11/0 | 1.071 |
| 405 | 0.025 | NUMERICAL_RULE_PASSED_REVIEW_REQUIRED | 2.275e-4 | 173/5/0 | 1.000 |

- **Both 0.025 halvings certify,** with no uncertified shell and no POINT_STOP. I did not map plus/minus to rows; the conclusion holds either way.
- **Rows 408 and 411 (0.0125)** are running: row 408 started at 16:49:07Z, row 411 at about 16:58Z. At row 404's pace (4 h 56 min) both are due at about 22Z. I'll post a follow-up when they land.

### A5. L2 composition (campaign helper; root's provisional A293: 6 calls)
- **Under the current rules: 6 calls,** R28, R29, R30, R31, R300, R301.
  - Row 302 cannot be a direct call, because it has no certified final spec.
  - The halving points depend on readings from the same batch, so they are hedges, not replacements.
- **If R302 returns:** that requires root to adopt A295's final text and the successor to re-certify row 302, with its bundle, ρ, slot proof and unit 2 final spec, before the batch binds. R302 can then come back as the 7th call, in the reviewed 7-call/580 GiB shape.
- **Otherwise 6 calls.** The optional 7th-slot hedge, the ell_F plus at 0.025, is root's call under A258.
- **R300 and R301 still need:**
  - EPS reviews by an approved signer (A202/A205; Claude3 is not one);
  - adapt-eps, ρ and slot proof;
  - a cx2v002 bundle;
  - unit 2 final specs. Unit 2 is FAIL until Codex3's fix lands (0298).

### A6. Rows 501 and 504 (FORMAL; posted in 0308)
- Each has one failing high-k shell and a POINT_STOP:
  - **row 501, [76, 77]:** levels 1.8416e-7 / 2.0515e-7 / 2.2613e-7, ratios 1.114 / 1.102, eps/eps_max 2.8e-3;
  - **row 504, [73, 74]:** levels 4.9485e-7 / 5.5132e-7 / 6.1822e-7, ratios 1.114 / 1.121, eps/eps_max 3.0e-3.
- Root's 0854 counts them as 2 of the 5 global hedge points so far.

## Part B — 0853 (A294/A295)

### B1. How `uv_tail.eps_certificate` is consumed (FORMAL from code; DDO driver b5cc62af)
1. **In the call, custody only.**
   - The driver pins {path, sha256} (L1076–1086, `verify_pin`) and forwards them in `route_a_argv` (L1104).
   - The RO1 route A worker (fbe9ae79 L78–84) and the lapse library `owned_uv_tail_lapse_v002.py` (2026f2b6 L664–673, UV_TAIL_CERTIFICATE_MISMATCH) re-check the sha. The state record stores the pin (L687).
   - Every stage writes `srb_rot = 'NOT_EVALUATED_IN_STAGE: SRB-ROT is a gate on the C4T rows (sec 1.5)'` (route B binding 1e27430c L215–216).
2. **No computed tail, lapse or rotation value reads eps.** In the library, only `_eps_per_shell` (L830–844) reads the certificate's `shells`, and only `field_bound` (L847–857) and `srb_rot` (L860–871) use that.
3. **The one computed reading** is at acceptance.
   - The chain: `h3_accept_call_c2v004` eb895263 → deps `srb_adapter` (L88) → `srb_rot_adapter_c3v003` 08e9ac0a.
   - Its `format_eps` (L265–291) feeds each shell's `eps` over [4, 182] into the library's `srb_rot` on the call's accepted final-rotation state. That `eps` is the max over estimators; guard v003 5f1e49e6 L139 requires eps ≥ eps_envelope.
   - The bound: |δv_c(R)| ≤ R c² Σ_s ε_s B_s^(1) / (2 N_min v_c(R)), and a row's bound is the max over the row's columns.
   - It passes iff the bound is ≤ τ_i/10, with τ_i = 0.25σ_i from the prereg V005 row contract.
   - An unflagged fail reads BOUND_INSUFFICIENT, which F6 makes a certified MODEL_INVALID (ACC L97, adapter L80).
   - **It is per shell, not eps_max:** each ε_s multiplies its own weight B_s^(1), a magnitude integral of the call's tail source over D ∩ shell s.
4. **The binary gates:**
   - producer `certified` and verdict;
   - admission adapter 4de70486, which re-applies the 1.1× rule (L108–129, L176);
   - the EPS slot proof, TESTED PASS;
   - the bundle;
   - the W plan's `certificate_check` (CERTIFICATE_PREFLIGHT), and SRB adapter L420–426 (EPS_PROOF_NOT_TESTED_PASS_FOR_THIS_SLOT).
5. **Not consumed in this campaign:** RB-FP, the ε_max-based full-chain bound of design V002 §1.5. The SRB adapter says the RB-FP screen "is never a gate", and A134 Q10 gives no bare EPS magnitude gate.
6. **Not analysed by Claude3:** the NGC driver cx3r008. 0853 scoped the DDO driver, and 0854 gives cx3r008 to Codex2.

**Worst-case effect of an under-converged shell s\*.**
- **The size of the effect:** Δ(row bound)_i = C_i (ε_true − ε_s\*) B_s\*^(1), with C_i = R c²/(2 N_min v_c). If ε_true ≤ M·ε_s\*, then Δ_i ≤ (M − 1)·c_{s\*,i}, where c_{s\*,i} is the shell's own current term.
- **Why there is no B-free bound:** c_{s\*,i} needs B_s\*, which exists only in the call's accepted final-rotation TailState at acceptance. No certification record carries it.
- **The evidence on M_true (TESTED):**
  - The consumed ε is the envelope estimate. It is ≥ the actual dense/local search, which is ≥ the discrete levels: for row 302, 1.909e-6 ≥ 1.724e-6 ≥ 1.220e-6.
  - The production envelope agrees with the producer's own dense audit (20³ torus × 400 directions × 5 radii, 16 starts) at 672/672 audited shells, max dense/production 1.0000.
  - At shells 32, 45, 63, 64 and 100 of rows 302, 501 and 504, every audit is 1.0 to 6 decimals.
  - The failing shells themselves are not in AUDIT_LO (L31), so convergence there is UNTESTED; the adjacent shells are TESTED.
- **The threshold scale** (M = 10; a 1 % move of the gate τ_i/10 = 0.025σ_i):
  - It needs C_i B_s\*^(1) ≥ 2.5e-4σ_i / (9 ε_s\*): 14.5σ_i for row 302, 69σ_i for row 501, 24σ_i for row 504.
  - With σ_i = 2–5 % of v_i, row 302 needs ≥ 0.29–0.73 v_i. One unit shell at |k| = 46 /kpc (λ ≈ 137 pc) would have to carry a tail bound comparable to the rotation speed. That is UNTESTED but physically implausible.
  - Where audited (M_true − 1 ≤ 5e-5), the threshold rises by more than 10⁵.
- **Margins for row 302,** assuming C_i B_s\*^(1) ≤ v_i (UNTESTED) and M = 10:

| against | value | margin |
|---|---|---|
| observational budget σ = 2–5 % of v | Δ ≤ 1.7e-5 v_i | 1,200–2,900× |
| A133's τ_i = 0.25σ_i | same | 290–730× |
| the SRB gate τ_i/10 | same | 29–73× |
| the discrete step |L2 − L1| = 1.33e-7 itself, which is not consumed (σ, τ, τ/10 at σ = 2 %) | 1.33e-7 v_i | about 1.5e5×, 3.7e4×, 3.7e3× |

- **Reading:** A295's principle holds for these shells, either on the physical bound or, without relying on it, under the conservative substitution in 0309 R2. That substitution makes the per-call SRB gate carry the worst case with the exact B_s, so for any true sup ≤ M·ε_s\* a false PASS is impossible.

### B2. Where the 1.1× rule was registered, and why
- **Text of record:** `tail_scheme_design_c2/v002/TAIL_SCHEME_DESIGN_V002.md` cdb16d1c §1.5, L235–238: "ε certificate EPS (an estimate, not a proven sup) … Refine (128 per decade, 26 + 26 directions) and require ε_s(refined) ≤ 1.1·ε_s(base). After two failed refinements the certificate is EPS_UNCERTIFIED, which blocks all T runs."
- **First implementation:** `tail_scheme_impl_c2/certificates_v001/CERTIFICATES_V001.md` 5fdc9f01 L53–57, under "Registered rule (as written)". It added the 104-direction × 256-per-decade second level.
- **Rationale:**
  - It is design V002's response to review finding K6, "RB not a row bound; ε sampled" (MODERATE, L94): "ε_cert is a refined sample, labelled an estimate".
  - V001 (3b61201d L216) had only a single sample of 13 directions × 64 per decade.
  - The 1.1 factor is a sampling-stability tolerance. No precision target or error-budget derivation is stated for it.
- **It was written for a different setting.** At the time, one galaxy-wide certificate (DDO 2–363 and NGC 2–46 /kpc) gated "all T runs". The CP-1 per-point certificates reuse the rule unchanged.
- **The under-sampling was known from the start:**
  - CERTIFICATES_V001 L58–60: "The rule's sampling under-estimates the per-shell sup (TESTED)", by up to 1.29×.
  - V005 c01b3c51 A52 item 5 (L219): above about 15 /kpc, per-shell ε is under-sampled by 18–28 %, while ε_max is converged.
  - That led to the envelope successor: each shell's `eps` is the max of the actual, discrete, envelope and dense-audit estimates (producer L304–305; `shell_value_rule` L326).
- **Since then,** the 1.1× rule judges only the discrete estimator, while consumption uses the larger, converged envelope value.

### B3. Is a uniform amendment justified? (recommendation and constants in 0309)
- **Yes.**
  - The rule is relative with no floor.
  - Its failure concerns an estimator that is not consumed.
  - The failing shells are negligible within their certificates. For lo ≥ 20, eps(k) ≈ 0.80·eps_max·(4.5/(lo + 0.5))² (TESTED, p10–p90 0.79–0.81), so "≤ 1 % of eps_max" means |k| ≳ 40 /kpc.
  - It only adds passes: a certified point has no shell with two refinements, so no certified point changes. Genesis has 0 such shells (TESTED).
- **The proposal (0309 R1–R2):**
  - safety multiple M = 10 and fraction f = 0.1, that is M·ε_s ≤ 0.1·eps_max, equivalently ε_s ≤ 1 % of eps_max;
  - an absolute step floor |L2 − L1| ≤ 1e-6;
  - a dense envelope audit on the accepted shell, with audit/production ≤ 1.05;
  - conservative substitution, ε := M·ε_s, in the successor record.
- **Margins on the three failing rows:**

| row | shell | ε_s/eps_max | margin at 1 % | margin at 2 % | step L2 − L1 | margin at 1e-6 |
|---|---|---|---|---|---|---|
| 302 | [46, 47] | 7.56e-3 | 1.32× | 2.64× | 1.333e-7 | 7.5× |
| 501 | [76, 77] | 2.77e-3 | 3.61× | 7.22× | 2.098e-8 | 47.7× |
| 504 | [73, 74] | 3.00e-3 | 3.33× | 6.66× | 6.690e-8 | 14.9× |

- **Context (TESTED):**
  - Of the 335 shells that needed a refinement, 247 meet (1 %, 1e-6) and 283 meet (2 %, 1e-6).
  - The largest step over all refined shells is 4.6e-7, and the largest step/eps_max is 1.8e-3.
  - Across the 48 points, eps_max ranges from 2.6e-6 to 1.6e-2, always at [4, 5]. A purely absolute ε floor would therefore act very differently from point to point. That is why the floor goes on the step, while the relative criterion carries the negligibility.
- **Not covered:** a failing shell above 1 % of eps_max stays EPS_UNCERTIFIED, and root rules. That case exists in principle: shells near the line reach eps/eps_max 0.25, at shell [8, 9].

### B4. Census (0853 item 4; certification records only; interim, 48 of 58 points)
- **Files:** `census_c3v001/census_c3v001.py` bb8ec3cb and `census_c3v001/EPS_REFINEMENT_CENSUS_C3V001_INTERIM_48of58.json` 5a0d3799, which lists every input sha256.
- **The 31 genesis points (5,518 shells):**
  - refinements 0/1/2 = 5,311 / 207 / 0;
  - decisive ratio ≤ 1.00: 5,082; in (1.00, 1.05]: 325; in (1.05, 1.10]: 111; above 1.10: 0;
  - the largest certified ratio is 1.0946.
- **The list points so far (17 of 27; 3,026 shells):**
  - refinements 2,898 / 125 / 3;
  - in (1.05, 1.10]: 62; in (1.10, 1.15]: 3, which are the three failures;
  - the largest certified ratio is 1.0992.
- **The shells near the line:**
  - 176 shells have a decisive ratio in (1.05, 1.15];
  - counting every refined shell as well, the near-line or refined set holds 507 shells;
  - their eps/eps_max is p10 1.1e-3, p50 3.5e-3, p90 8.2e-2, max 0.25.
- **The estimator gap:** the reported eps sits above the discrete max by a median 1.76×, p99 2.24× and max 2.34× (genesis); the list max is 2.28×.
- **How often it bites:** about 4 % of shells need a refinement, and about 1 % of those fail. That is 3 of 48 points (6 %), all of them list points.
- **Pending:** rows 408–411 and 506–511. I'll post the final census when they land.

### B5. Blinding (0853 item 5)
- **This is DDO154 only.**
  - The CP-1 points carry distance_Mpc 4.04 (POINT_START).
  - The producer takes "the actual DDO154 forward-call spec" (docstring L7).
  - My evidence is DDO154 CP-1 certification records, code, design text, V005 A52, and V006 A133 and A293–A295 (by heading).
- **No NGC value was read.** I did not open the NGC EPS certificate (`certificates_ngc_k32`), any run output, or V007_POSTSEAL_RECORDS.
- **Disclosure:**
  - While tracing the driver's RO1_ROUTE_A table, I hashed and grepped the eps-certificate flag lines of the two `ngc43_*` RO1 worker code files (b6c4586d, ee0510df). That is code, not data, and no conclusion uses it.
  - V005's A sections mention NGC coverage numbers; I used none of them.
- **The amendment only adds passes,** so no certificate that already passes, DDO or NGC, can change. Whether its scope extends beyond CP-1 is root's call.
- **Conclusion:** ruling now, before any NGC value is read, is clean.

### B6. Sites a successor would touch (for the build after the final text; nothing is implemented)
- **Producer** a1dcdea8: `discrete_shell` and `produce_eps` (L139–160, L304–305, L316–320). Alternatively, a re-evaluation tool over the existing records plus the dense audit (0854 item b).
- **Admission adapter** 4de70486: L108–129 and L176.
- **POINT_STOP's two checks.**
- **No change needed:**
  - SRB adapter c3v003, which reads `eps` as given;
  - guard v003 L139, which still holds because ε := M·ε_s ≥ eps_envelope.
- **For rows 302, 501 and 504:** the registry and bundle chain (A257 rebind, ρ, slot proof, bundle, unit 2).

## Part C — open root items
1. **0309 R1–R4:** A295's final text and constants.
2. **From 0852, under the current rules** (campaign helper Q1–Q5):
   - the Case A W3 route;
   - whether an uncertifiable requested point is an invalid side;
   - how D5 counts it;
   - L2 at 6 or 7 calls, and the hedge;
   - the timing against the batch binding at H11 end.
   - **The open gap:** F5 has no branch for a requested point that cannot be certified. A295 makes the "registered remedy" route available.
3. **Mapping:** plus/minus to rows 404, 405, 408 and 411, and the roles of rows 501 and 504.

## Provenance (sha256 from bytes)
- producer a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231; admission adapter 4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372; guard 5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f
- lapse library 2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54; SRB adapter 08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a; DDO driver b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6; route B binding 1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329; RO1 worker fbe9ae79 (`ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002_r5.py`)
- design V002 cdb16d1c42da39cf8eabe253b7192f4f391d19adfdd026e57a6971837a6aa944; design V001 3b61201d82e95c0cb653e375bafe23955fcfb5abe3ca0b6fbf35beb5add47094; CERTIFICATES_V001 5fdc9f01add40cd8df78467732166fda5ef050d6e76198a449969568b7e9c645
- acceptance step eb895263c8458696b265b30dc5dee771dcb89649e5b490c893bb613281c7bf19; deps template 48ec0e010cd4228f6b3a7eab78940e956465af32d3d3e796efb41f4a7ca3bfa5
- wrapper 381fa2957edabf18032afba9a8ff026744f6cc1d933efb5f3d30f289ea9decb9; core 192d086348fed9307da99732c0ef146bb336a3d605afc1e9e56b6ce959ad1a73; parent c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d; engine 193841fa1f1d078f7fc981fdba78cf3d736b50ee17e019f0cf94aae94e3a63a6; assembler 1b701591714c11856d525631f946d19a64f76f28041da21c6e9f1a62863b0e88
- V005 c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1 (A52); V006 ea88b1809e9f630c07844fd66e88bce2950d4def4fb605dff8ce9a01b655a581 (A133, A293–A295 by heading); A133 text cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17
- helper drafts: cause 33e55c858ae79ca3a687e48845cc59cf6d7050cad56ff0c226135121507fbcbd; campaign b09b6a162a05dfb7c15824cc34044f1555cd3780e0ff2a3b0944d9bd0b9100e3
- census script bb8ec3cbf0e34691be10691169cb916c23c17faa16885532b1818532a63702bc; census interim 5a0d3799f179b9aec3105fbfcf21b46edfa460683cb5d0b5186a9a3999af5284 (it lists the sha256 of all 48 EPS_NUMERIC inputs)
