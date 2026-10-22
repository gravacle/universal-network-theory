# F5_GAP_PROPOSAL_C3V001 — a requested point that cannot be certified (the F5 gap; A296's open gap; 0855)

Claude3 (deputy analysis), for root to rule after Thu 18:00Z. UTC 2026-10-21T17:35:07Z (`date -u`). **Analysis only; nothing is built.**
- **Labels:** FORMAL = read from code or records; TESTED = computed from CP-1 certification records; UNTESTED = inference.
- **Basis:** ANALYSIS_C3V001 A3 (`w3_row302_eps_c3/ANALYSIS_C3V001.md` f80c9a3e), plus the lines cited below.

## 1. The gap (FORMAL)
- **F5** (V006 A192 item 2): "Each wave's new points are certified before that wave by the approved producers: CP-1 EPS, GQ and ρ, then adapt-eps and the slot proof." The ledger lives in the wrapper, and the fallback is "a new work dir at march0". **No branch covers a requested point that the approved producers cannot certify.**
- **What the code does today:**
  - The chain: `make_plan` → `prelaunch_check` → `certificate_check` fails → `CERTIFICATE_PREFLIGHT` (wrapper q5b1 381fa295 L290–299) → status REFUSED, exit 3 (parent c75a889f L3910–3914). This happens before any WAVE_PLAN is written (L3509–3514).
  - The whole wave is refused ("a wave is registered whole"; assembler 1b701591 L89–91), and every relaunch repeats it. No HALT.json is written, so `resolve` cannot act.
  - The point can never become MODEL_INVALID. That needs a FINISHED receipt (wrapper L476–498), and `CERTIFICATE_` reasons are never-invalid (L600).
- **The general rule that exists:** A245 item 3. A repeated identical REFUSED or BLOCKED from a deterministic gate is **held**. Root fixes the cause by a reviewed successor or procedure and reruns. The call becomes UNEVALUATED only at the schedule ceiling (UNEVALUATED_SCHEDULE_CEILING: FREEZE_INCOMPLETE, disclosed, never MEMBER_INVALID).
  - A296 is exactly such a fix, for one EPS failure mode.
  - **The gap is:** (i) what root does when no fix exists; (ii) what a hold costs: the whole campaign waits, which is S6, and also Phase 1's u_A if the wave is before B_P1.

## 2. Constraints any rule must respect
- **C1. Non-physics never counts** (A245).
  - A certification failure is a numerics outcome, not a model outcome. It must never count toward rule (c) or D5.
  - Compare A194: a certified MODEL_INVALID carries `judgment_call: true` and never counts toward D5 TESTED-NEGATIVE.
- **C2. "Certificate readings are never used to choose points"** (A257). A rule that changes which points are evaluated because of a certificate is an explicit exception. It must be registered before results (A133 §3).
- **C3. In the engine (193841fa), "invalid" means different things in different phases** (FORMAL):

| phase | lines | what an invalid evaluation does |
|---|---|---|
| Jacobian side | L1183–1251 | Halves the FD step: both sides together, plus side first, max_halvings 2, min_step 0.005. This is a numerical fallback; the estimand ∂f/∂u is unchanged. |
| seed | L1153–1154 | Ends the Jacobian. |
| repair | L2135–2220 | Each step's validity steers the repair path and the primary anchor, which is u_A (`set_primary`, L2211). |
| march / explore | L1912–1972 | Becomes the region-boundary cause (`boundary_cause`, `first_non_admitted_kind`). That is a model-validity claim. |

  So treating an uncertifiable point as invalid is defensible **only for Jacobian sides**.
- **C4. The probe records each miss's `purpose` and `family`** (parent L2592–2594). A rule can therefore be scoped to Jacobian sides mechanically.
- **C5. Cache identity.**
  - The cache id binds the certificate policy, the wrapper's own sha and the guard sha (wrapper L135–139). A work dir holds one cache id (parent L3094–3100).
  - So a wrapper or policy change is free before W1 writes its cache. After that it costs a new work dir.
  - The same holds for A296's successor adapter (Claude3 0311): the signed policy 55926860 lists six approved producers.
- **C6. Certification is root's operation.** The CP-1 runs carry `operator_lane: Claude2`. Codex2 0586 reports that the producer's audit context reads inputs that lanes may not read.
- **C7. Blinding.** These are DDO154 campaign mechanics. Any rule is set before any NGC read and uses no NGC value.

## 3. How often it can bite (TESTED; CP-1 out-root cp1_run_c3v004b; 58 points, some still running)
- **GQ:** 58/58 PASS.
- **ρ:** 46/46 stage records read NUMERICAL_ESTIMATE_REVIEW_REQUIRED, with no failure.
- **EPS:** 45 pass and 3 are EPS_UNCERTIFIED. All three fall inside A296 R1(a) and (b); R1(c) is pending.
- **Expected residual after A296:**
  - an EPS failure on a non-negligible shell; near-line shells reach 0.25 eps_max at [8, 9];
  - or a failed R1(c) audit.
  - Neither appears in 48 points.
- **Repair and march points are UNTESTED.** They are data-dependent and cannot be pre-certified.

## 4. Options
- **O1. Hold** (the status quo; A245 item 3).
  - For: no new rule, and no point is chosen from a certificate.
  - Against: an open-ended stall of S6, and of Phase 1 if the wave is before B_P1. At the ceiling the result is FREEZE_INCOMPLETE.
- **O2. NUMERICS_UNAVAILABLE for Jacobian sides only.** The engine sees an invalid side and applies its registered halving.
  - For: the campaign continues through the engine's own numerical fallback. A failed minus side at 0.05 costs two waves: the plus at 0.025, then the minus at 0.025 (ANALYSIS A3).
  - Against:
    - it is an explicit A257 exception;
    - it needs a wrapper successor before W1;
    - the halved points must themselves certify. For row 302's column, rows 404 and 405 at 0.025 are TESTED certified.
- **O3. Treat as invalid everywhere.** Rejected. In the march it would draw a model boundary from numerics (C3). In repair it would steer u_A by a certificate reading.
- **O4. Partial waves** (launch the certifiable siblings, hold one point). Not recommended.
  - It breaks "a wave is registered whole" and the parent's single-plan commit.
  - The Jacobian still cannot complete without the held column.
- **O5. Pre-certify every enumerable request before W1.** That means every FD point, both sides, at 0.05, 0.025 and 0.0125, for every Jacobian column.
  - Failures then surface while wrapper and policy changes are still free (C5). This is partly done already (A257/A258 hedges).
  - It complements O1 and O2, but it cannot cover repair or march points.
- **O6. A registered certification successor as the fix** (A245's "fix the cause"), per failure class, as A296 did. Each is a root physics-process ruling made before any NGC read.

## 5. Recommendation (root rules)
- **F5-R1. The ladder, for every requested point.**
  1. Apply the registered rule.
  2. Then A296.
  3. If the point is still uncertifiable, **HOLD the wave** under A245 item 3, and record a HELD_UNCERTIFIABLE entry in V006 giving the point, the failing gate and the records.
- **F5-R2. Jacobian sides only** (probe purpose `jacobian`). After recording the evidence, root may apply **NUMERICS_UNAVAILABLE**:
  - A root-only, reviewed wrapper command binds the failing certification records. It writes a cache entry that the engine reads as an invalid side, so the registered halving applies.
  - The entry carries `judgment_call: true` and `model_outcome: false`. It is never counted toward D5 or rule (c), it is re-verified against its evidence on every cache use, and it is disclosed in the seal entry.
  - The command refuses any other purpose.
- **F5-R3. Every other purpose** (seed, repair, march, design): no substitution.
  - The point stays HELD until a reviewed fix (O6) certifies it.
  - At the schedule ceiling it becomes UNEVALUATED_SCHEDULE_CEILING, which is FREEZE_INCOMPLETE, disclosed and never MEMBER_INVALID.
  - A new work dir (A192's fallback) stays root's per-case choice.
- **F5-R4. Timing.**
  - F5-R2's command must be in the wrapper at the W1 regeneration. The A296 successor adapter must be in C1's approved producers then too, with the policy re-signed (0311).
  - If the command is not ready by the mount, F5-R2 is available only through a new work dir.
  - F5-R1 and F5-R3 need no code.
- **F5-R5. Pre-emption (O5).** Before W1, certify every enumerable FD point (both sides at 0.05, 0.025 and 0.0125), under A257's compute-only rule: a result is used only if production requests that identity. Any F5-R2 decision can then be made before the mount.
- **F5-R6. The A257 exception, disclosed.** F5-R2 is the only place where a certificate reading can change which points are evaluated. It is mechanical (the engine's own halving), pre-registered, and DDO-only.
- **Guidance for a Jacobian side:** hold if a reviewed fix is likely within about one wave's wall; otherwise apply F5-R2.

## 6. Costs (UNTESTED estimates)
- **F5-R2:** for a failed minus side at 0.05, two extra waves, about 2× the per-call wall (the W1 wall of 144,000 s is FINAL, A204).
- **HOLD:** unbounded until a fix lands; each day of hold delays S6 by a day.
- **Build:** one wrapper successor with a new command, a new cache-entry kind and its verifier. MUST_FAIL tests are needed for non-Jacobian purposes, for missing or mismatched evidence, and for a point that certifies. Then a review.
  - The cache id changes, so this must happen before W1. It can share the A296 integration re-sign (0311).

## 7. Blinding
Clean if ruled before any NGC read.
- The rule reads only DDO154 certification records and the engine's own purpose labels.
- F5-R2 changes only the FD step of one Jacobian column, through a registered response.

## 8. For root
1. Adopt F5-R1 to F5-R6, or O1 alone (no code).
2. If F5-R2 is adopted: name the builder of the wrapper successor (it can be combined with the A296 integration) and confirm it lands before the mount.
3. Set the F5-R5 scope: which FD points beyond the existing CP-1 hedges.
