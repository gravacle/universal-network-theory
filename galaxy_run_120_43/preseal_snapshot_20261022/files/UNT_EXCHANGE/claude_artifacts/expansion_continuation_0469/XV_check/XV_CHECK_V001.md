# XV check V001: adversarial check of the 0469 synthesis (stalled same-model expansion continuation)

**Role:** XV, the distinct internal adversarial check for Claude4 (author stream 0469; coordinator Claude2), run before Claude2's review.
**Date:** 2026-10-17.
**Judged:**
- the XJ synthesis `XJ_synthesis/XJ_SYNTHESIS_V001.md` (sha256 `7b2d153b…4ebe`) and its manifest (`cab0e416…6325`; 19/19 listed files match their bytes);
- the judge JSON returned to the lead: `fix_supported=false`, with MODULE, FIXTURES and PACKET all null.

**Also read:**
- XD1: diagnosis `40528149…9209`, results `80537423…51ad`; 13/13 listed outputs match;
- XD2: diagnosis `9104b4b1…b1f7`, results `98f1c532…ca36`, manifest `cfab876f…a629`; 26/26 files match (`results/xv06_manifests_v001.json`).

**Status:** this is a review only. Nothing here is accepted for physics. There is no dark-energy claim and no no-go claim. No .30/.70 split, Ω budget, imposed w(z) or Λ substitute is used or implied.

---

## 0. Verdict: **FAIL (correctable)**. Amend the synthesis before Claude2's review.

**Confirmed**
- `fix_supported=false` stands, and the new evidence strengthens it. No pseudo-arclength or other stepping fix is supported.
- My independent re-typing reproduces the stall mechanics exactly: H1, H1-arc, H1b, H2, H5, H6a/b and H10 (§2).

**Failed items, which must be corrected**

**F1. Physics status (H5h, H1-geo, Verdict 4, Limits, judge `notes`).** The judge says the sign of C_cond is "open" and an "unresolved Fano-factor question".
- For the target ensemble of this capture, the sign is fixed by an exact convexity theorem: S ≤ 0 (C_cond ≥ 0) wherever J_S ⪰ 0, and J_S ⪰ 0 holds at 83/83 saved states.
- The pooled-estimator fold is produced by the estimator's violation of that convexity. This is the new hypothesis **H11, TESTED-POSITIVE** (§3).
- So the fold, and the S > 0 (C_cond < 0) partner branch, are excluded for the target ensemble, not just unresolved.

**F2. E3 is mis-graded, and the reasoning in D3/D4 rests on a false premise.**
- The judge says the admission capture is "a different ensemble at the same (β, j)".
- It is the **same declared target**: identical operator, adapter and statistics pins, and identical capture metadata.
- The 7.78 spectral difference and the U gap of 3.11 vs 8.87 are therefore sampling (ergodicity) errors about one target.
- The original capture is the one that violates exact convexity. Its 512 paths contain **zero** hop, bind or admit events (§3.4).

**F3. Remedy.**
- R1 lacks an estimator-convexity gate. That gate would have stopped the saved run at stage 1, and the ancestor at τ = 0.
- The "≈600× ESS" figure rests on a premise contradicted by the jackknife bias and by the same-target capture.
- R6 (a closure change to pass the impasse) is not indicated by this evidence.

The line-specific corrections are in §4. Minor items are listed there too.

---

## 1. Custody and rules kept

**Pins.** All 19 pins were verified from bytes (`results/xv01_reweight_convexity_v001.json → pins`):
- the dispatch, `b1fece81…d710d`;
- root `8c6c84d2`, stepper `ef3d22ce`, monitor `bbc4f900`;
- worker `1f1e4cfa`, evaluator `df80228a`, statistics `85f4c638`, RHS V003 `d7b81d45`, static `7130a277`, factorization `56b83898`;
- capture `ea70f393`, controls `953d4693`;
- ancestor inputs, acc0, acc74 and finish;
- factor_final `10e19b51`;
- resume finish `10883a59`, which equals `receipt.json:finish_sha256`;
- comparison `2774a4a9`.

The root launch record (`4643a0c5…`) and the monitor log (`ec862e01…`) name the same pins. The four endpoint JSONs were checked against the shas recorded in `comparison.json → inputs`.

**Rules.**
- No project module was imported or executed. Nothing was launched. There was no network access.
- All algebra was re-typed in `scripts/xv_common.py`, with each function citing its pinned source lines. It was written independently: the XD and XJ scripts were read but not imported.
- Single thread: `OMP_NUM_THREADS=1 … python3 -I -B`, numpy 2.3.5.

**Cost.**
- `xv01`: 1663 reweighting evaluations in 2.3 s, maximum RSS 170 MB.
- `xv02`: 4.1 s, 166 MB.
- All other scripts took under 2 s.

**Validation.** My reweighting reproduces the saved `native_per_cell.{F_hessian, y, U_F_n, C}` and `weight_concentration.{ESS, max_weight}` **bitwise at all 83 accepted states** (a00–a74, r0–r7).

---

## 2. Re-run of the judge's deciding tests

All of these were reproduced (`results/xv01`, `xv03`, `xv04`).

| Judge claim | Judge number | XV re-run (file → field) | Agree |
|---|---|---|---|
| H1b chain split: chain 0 S > 0 and chain 1 S < 0 at every state | 83/83 each | chain 0 S > 0 at 83/83; chain 1 S < 0 at 83/83 (`xv01 → trajectory[*].chain0.S, chain1.S`) | yes |
| H1b at a00 / a37 / a74 / r7: S pooled, chain 0, chain 1, jackknife SE, sign flips | −2.9665e-3 / +5.7093e-2 / −7.6395e-3, SE 2.439e-2, 5 flips … r7: −1.0064e-7 / +6.4894e-2 / −2.0864e-3, SE 2.700e-2, 8 flips | identical to every printed digit; SE 0.024385–0.027001 and 5–8 flips over 83 states | yes |
| H1 fold law: τ* − τ_final | 7.50e-15 (all 8), 1.029e-14 (last 6), 1.089e-14 (last 4) | 7.496e-15 (R² 0.999989), 1.0292e-14 (0.999973), 1.0886e-14 (0.999998) (`xv03 → fold_law.fits`) | yes |
| H1/H5e transversality | u_min·b = −2.9687 on both sides | r0–r7: −2.968746 … −2.968740. All 86 stages: −2.968746 … −2.968737, including the 7 S > 0 stages. [A\|−b] σ_min 0.071259–0.071264 (`xv03 → transversality`) | yes |
| H3a: saved velocity = A⁻¹b; saved S | 2.3e-9 | relative error 0.0 at r0–r7 with the saved stage scaling; S rebuilt equals the saved observer value exactly (`xv03`) | yes |
| H2: rejections versus the sign of S | 7 thermal at S > 0; 13 entropy at S < 0 | the attempt→stage map from `attempts.jsonl:evaluations` puts every THERMAL rejection on an S > 0 stage and every ENTROPY rejection on an S < 0 stage (`xv03 → controller`) | yes |
| H5 roundoff | scale·σ_min = 1.18–1.31e-15; r7: 1.19e-7 vs 3.84e-8 | ε·Σ\|mat[9,i]v_i\|/h0 × σ_min = 1.182e-15 at r0–r7. \|rate\|/scale 0.15–0.63. The scale exceeds 1e-7 at r5, r6 and r7 (1.19, 1.54, 1.55e-7). r7: `tangent_residual[9]`/h0 = 1.194e-7 against `entropy_rate`/h0 = 3.837e-8 (`xv03 → roundoff`) | yes |
| H10 | 12 duplicate evaluations; rows 55→56, 64→65, 76→77 | 12 duplicate evaluations. Attempts 16, 20 and 24 re-evaluate the states that failed first in attempts 15, 19 and 23, at rows 55, 64 and 76 (`xv04 → reevaluated_failed_states`; the `xv03` field of that name is superseded, see §6) | yes |
| E1 admission S | −0.507 / −0.375 / −0.240 | −0.5067 / −0.3753 / −0.2404 (`xv03 → endpoint_convexity`) | yes |

Every refutation attempt against these grades failed.

---

## 3. New deciding test: estimator convexity (H11)

### 3.1 An exact identity for the fold indicator

Notation:
- dp = cs·(1, z) is the fixed-C, zero-fiber direction used by the guard (factorization L75–L84), with dβ = cs₀ > 0.
- The capture weight depends on β only through (βN, βj) (statistics L117–L120). The RHS therefore builds the β column as (∂ₙ + j·∂ⱼ)/β (RHS L78–L81).
- Define q = (dβ/β, dj + j·dβ/β). Then (dU, −dy) = F_phys·q (RHS L79–L81).

On the family, dC = 0 and the fiber j_R + 2J_Sμ = 0 (RHS L86, L89, L110). These give j·dy = J_S:dC = 0 and q_j·dy = −2 dμᵀJ_S dμ. Therefore

  **S_scaled = (β²/dβ) · ( qᵀ F_phys q − 2 dμᵀ J_S dμ ),**  with dμ = −(F_phys q)[1:4].

Verified numerically (`xv02 → summary`):
- relative error ≤ 2.6e-9 for the pooled estimator wherever |S| > 1e-6;
- 4.9e-8 at r7, where S ≈ 1e-7 and the comparison is rounding-limited;
- ≤ 4.6e-12 for the chains.

### 3.2 The theorem for the capture's target ensemble

The reweighting weight is (statistics L117–L120):

  exp(−βN θ·A + β j·R) · Π(N·amp_k)

Its exact target is Z(N, j) = Tr exp(−βN·H₀ + β j·R̂), where:
- R̂ is diagonal;
- H₀ = D_θ − Σ_k amp_k·T_k;
- every event weight is the positive N·amp (statistics L41, L78–L80);
- every reverse is the exact conjugate of its forward, so it has equal magnitude (operator `a04f8795…` L127–L128, L157, L1642–L1661; statistics L12 shares one amplitude per forward/reverse family; CURRENT_INSTRUCTIONS L122, "native Hermitian interactions … symmetrically … reverses").

The argument:
1. ln Tr exp(X) is convex in a real symmetric X, and X is affine in (N, j). So ln Z is convex in (N, j).
2. Hence **F = −(1/(β·nc))·∇² ln Z ⪯ 0** (evaluator L31, L92).
3. The identity then gives S ≤ 0 whenever J_S ⪰ 0.
4. J_S ⪰ 0 at 83/83 states. Its minimum eigenvalue runs from 0 at a00, where j = 0 (stepper L50), to 0.121.

For the estimator, F ⪯ 0 is equivalent to the conditional inequality **Var_w(s₀ | s_j) ≥ ⟨n⟩**. This is the Schur complement of Cov − ⟨n⟩e₀e₀ᵀ (evaluator L82–L92, where contact[0,0] = −⟨n⟩).

Pure-algebra check, using r7's y, β and j (`xv02 → synthetic_theorem_check`):
- 4000/4000 random NSD F give S < 0; the maximum is −3.2e-6.
- With one positive eigenvalue, S > 0 in 965/2000 cases.

### 3.3 Saved-data result: the original capture violates the theorem's premise everywhere, and the fold is that violation

`xv01`, `xv02`, `xv04`:

**F is never negative semidefinite.** λ_max(F) > 0 for **every estimator at every state**: pooled, both chains and all 16 jackknife subsets, 1577/1577 evaluations.
- Pooled λ_max runs from +3.03e-5 at a00 to +1.145e-4 at r7.
- At r0, the first stage of the run, it is +1.144e-4.

**The conditional inequality fails everywhere.** Var_w(s₀|s_j) − ⟨n⟩:
- pooled: −1.288 to −1.318 at 83/83 states;
- chain 0: −3.81 to −3.88;
- chain 1: −1.07 to −1.30;
- jackknife: 16/16 subsets negative at a00, a37, a74 and r7 (range −2.07 to −1.04; jackknife SE 1.02–1.11).

The unconditional entry is not the problem. Var(s₀) − ⟨n⟩ = 40.8 at r7 for the pooled estimate, and 38.8 and 41.7 for the chains (`xv10`). The violation appears only after conditioning: the 9 read scores linearly "explain" 93.7% of Var(s₀) (44.89 falls to 2.81). This is a near-deterministic relation in this sample, and it bears on H12.

**The fold is the cancellation of the convexity-violating term.** Splitting qᵀFq by the eigenvalues of F gives:

| State | Positive-eigenvalue part | Negative part | J_S term |
|---|---|---|---|
| a00 | +5.36e-5 | −3.020e-3 | 0 |
| r7 | +7.2648e-4 | −7.2651e-4 | −7.3e-8 |

The positive eigen-direction (stage 86: n −0.22, j_R (−0.50, 0.42, 0.04), and S00/S11/S22 ≈ +0.41 each) overlaps the isotropic-J_S fold direction.

**Diagnostic only (not a proposed estimator).** Clipping that one eigenvalue to 0 leaves S < 0 everywhere:
- pooled: −3.02e-3 to −7.24e-4 at 83/83 states;
- all jackknife subsets: maximum −1.9e-7;
- chain 1: −7.6e-3 to −2.5e-3;
- chain 0: about −1e-10.

So there is no fold without the violation.

**Jackknife bias.** The same delete-one-batch jackknife that gives the SE also estimates a bias of **+0.0256 at 83/83 states**. The bias-corrected S runs from −0.0286 to −0.0256, which is negative at 83/83 states; |S_bc|/SE is 0.95–1.17. This is not decisive under failed mixing, but it points away from the fold.

### 3.4 The same-target admission capture satisfies the theorem and has no fold

At the a74 endpoint, same (β, j) (`xv03 → endpoint_convexity`):

| Capture | Paths | λ_max(F) | Var(s₀\|s_j) − ⟨n⟩ | S | U |
|---|---|---|---|---|---|
| original | 512 | **+1.144e-4** | **−1.318** | −2.14e-6 | 3.111 |
| admission, pooled | 2048 | −1.18e-3 | +26.57 | −0.5067 | 8.868 |
| admission, chain 0 | 1024 | −9.37e-4 | +16.53 | −0.3753 | 8.834 |
| admission, chain 1 | 1024 | −8.88e-4 | +11.96 | −0.2404 | 8.901 |

**Same declared target** (`xv03 → E3_same_target`):
- the capture metadata are identical: θ, amplitudes, β = 1, lapse 1, j = 0, n_cells 64, n_contact 92, dstar 2.0, and the attestation text;
- the operator (`a04f8795`), adapter (`0705be7c`) and statistics (`85f4c638`) pins are identical;
- only the sampler, occupancy, recipe and admission/birth/hex/durability modules differ.

**Ergodicity.** The original's 512 paths contain only birth events (2034) and flip events (160). There are **0 hop, 0 bind and 0 admit events** (`xv07`; capture `counts` columns, statistics L12, L81). Chain 0 is confined to 4–6 birth events per path. The admission paths hold 0–12 events, with 1950/1803 changed-path accepts against 222/242 in the original (`xv08`; `mixing.changed_path_accepts_in_measurement`).

**Spectrum.** The original F has four near-null eigenvalues (|λ| ≤ 1.8e-4), one of them positive. In the admission capture the smallest |λ| is 8.9e-4 to 1.18e-3.

Both captures failed mixing, so neither certifies values. Only the admission capture passes the exact necessary condition.

### 3.5 Grades

**H11 — TESTED-POSITIVE.** Hypothesis: the pooled-estimator fold is produced by the original capture's violation of the exact convexity of its own target ensemble.

Deciding tests:
- the identity of §3.1, verified to 2.6e-9;
- the theorem of §3.2, checked synthetically at 4000/4000;
- the violation at 1577/1577 estimator evaluations;
- the cancellation at r7: +7.2648e-4 against −7.2651e-4;
- with the violation clipped, S < 0 at 83/83 states;
- the same-target convex capture has S = −0.24 to −0.51.

The **premise** is that the target generator is symmetric. That comes from reading code and instructions (§3.2), not from saved data.

**H12 — UNTESTED.** Hypothesis: the violation comes from non-ergodic sampling. The capture never visited the hop, bind or admit sectors; it has near-null read directions; and it has about 10–20 effective samples per 9-regressor conditional variance (τ_int 6–30 against batch 32). Deciding test: a capture that samples those sectors. That is a root launch or a root evaluation of existing captures (§5).

**What follows for the dispatch question.**
- Forward natural-τ continuation of the target ensemble cannot meet this fold while J_S ⪰ 0.
- The stall is a **capture-quality** failure. It is neither a method failure nor a physical boundary.
- An arc-length module would trace a branch the target ensemble forbids. This strengthens `fix_supported=false`.
- The whole 81-step ancestor branch, not only its end, was integrated with a convexity-violating estimator (a00 already gives λ_max = +3.03e-5). Its β and j evolution (β fell 8% while the scale rose 1.34e-5) is not evidence about the model.

---

## 4. Line-specific corrections

Line references are to `XJ_SYNTHESIS_V001.md`; field references are to the judge JSON.

1. **L47** ("maximum of the ensemble's exact entropy function"), and the judge `method` text, same sentence.
   - Replace with: "the maximum of the **pooled estimator's** entropy function (log-normaliser form). For the capture's target ensemble, s decreases strictly along this family (S < 0, §3)."
   - L48 ("beyond τ* … no adiabatic equilibrium"): keep, scoped to "for this estimator, within the scanned β ∈ [0.80, 1.25] (`xj03 → beta_scan_r7_C`)".

2. **L54 and L58** (Verdict 4).
   - "The fold is not a resolved property of the model" → "The fold is excluded for the capture's target ensemble (H11). It is produced by the original capture's convexity violation. Its indicator is also noise-dominated."
   - L58 "C_cond is 'event-count variance minus mean event count'" → "C_cond is governed by the full-score conditional variance Var(s₀|·) minus ⟨n⟩. The exact ensemble requires Var(s₀|s_j) ≥ ⟨n⟩, and the original capture violates this in every estimator."

3. **L101–L113 (D3)** and the judge `notes` → Reconciliation ("7.78 compares a different ensemble").
   - Replace "The admission capture is a different ensemble at the same (β, j)" (L108) with: "The admission capture is the **same declared target** (identical operator, adapter and statistics pins and capture metadata). ΔU = 5.76 and 7.78 are sampling (ergodicity) disagreements; by `comparison.json → pairwise_empirical_disagreement[0].interpretation`, at least one capture has matrix error ≥ 3.89. The original never sampled hop, bind or admit events and violates exact convexity."
   - In L113, replace "certifies its absence in the original ensemble" with "in the original capture's estimate".
   - XD1's Weyl reading was correct as a statement that at least one estimator is grossly wrong. It is not decisive about which one; the convexity test is.

4. **L115 (D4).** Delete "because it compares estimators of one ensemble, whereas the cross-capture comparison mixes in an ensemble difference".
   - Both captures estimate one target.
   - Within-capture splits share the original sampler's ergodicity failure: neither chain has any hop, bind or admit event. They therefore give lower bounds only.
   - The cross-capture convexity contrast is the stronger evidence (§3.4).

5. **L152 (H1-geo).** Keep TESTED-POSITIVE for the pooled estimator. Add "(estimator entropy; excluded for the target ensemble, H11)".

6. **L169 (H5h)** and the judge H5h `numbers`.
   - "contact[0,0] ≡ −n exactly" → "= −n to 4.4e-16 relative (383/512 bitwise)" (`xv05`).
   - "The conditional covariance part tracks Var(n) … The sign of C_cond is a Fano-factor question that the capture does not resolve" → "The exact inequality is Var(s₀|s_j) ≥ ⟨n⟩, where s₀ includes the diagonal-energy term. The capture violates it: pooled −1.29 to −1.32, chain 0 −3.81 to −3.88, chain 1 −1.07 to −1.30. Chain 1 violates it even though its event-count Fano factor Var(n)/⟨n⟩ is above 1 (3.72/3.35). So the event-count Fano factor is not the deciding quantity, and the sign of C_cond is fixed for the target ensemble."

7. **L174 (E3)** and the judge E3 entry.
   - Grade TESTED-NEGATIVE → **TESTED-POSITIVE**, read as "an estimator disagreement about one declared target (sampling or ergodicity error, not CLT noise)".
   - Basis: the pins and metadata in §3.4. The judge's ground, "different ensemble", is refuted.

8. **L185 (§4.1).** After "with negative conditional heat capacity", add "a branch the target ensemble forbids (H11)".
   - **L187–L189:** "not established for the model" → "excluded for the target ensemble; an artifact of the original capture's estimator".

9. **L213–L219 (R1)** and judge R1 / `required_module_spec (1)`.
   - Add, before any sign test, an **estimator-convexity gate**: λ_max(F) for the pooled estimate, each chain and each jackknife subset, together with Var_w(s₀|s_j) − ⟨n⟩ and its jackknife SE. The terminal status is `ESTIMATOR_CONVEXITY_VIOLATION` (no reject-and-halve) when the pooled and per-chain estimates violate.
   - When convexity holds, S < 0 is automatic. The remaining gate is then on the precision of |S|, which matters for β̇ = −N/S.
   - Also report the jackknife bias, not only the SE.
   - New fixture (b) expectation: `ESTIMATOR_CONVEXITY_VIOLATION` at stage 1 (r0: λ_max = +1.144e-4; Var − ⟨n⟩ = −1.318). The ancestor a00 also fails (+3.03e-5; −1.288).
   - New algebra fixture: NSD F gives S < 0 (4000/4000).
   - The evaluator's "No PSD repair" policy (evaluator L122) stays. The gate stops; it does not repair.

10. **L218** and the judge `notes` → Physics status, "≈600× the present effective sample size".
    - Delete. Its premise, an unbiased pooled S ≈ −3e-3, is contradicted twice: by the jackknife bias (+0.0256; S_bc −0.0286 to −0.0256 at 83/83 states) and by the same-target admission capture (S −0.24 to −0.51 with chain-consistent sign).
    - Replace with: "The requirement is an ergodic capture that satisfies the convexity gate, not more samples of the original sampler."

11. **L240–L243 (R6)** and judge R6.
    - "If a resolved capture still shows an impasse, passing it requires a reviewed closure change" → "Not indicated by this evidence. Under §3.2 an S → 0 impasse of this type cannot occur in the target ensemble while J_S ⪰ 0."
    - H5j (Birth-carried expansion) stays an independent open physics question. It is not a consequence of this fold.

12. **L287 (Limits)**, "The physical sign of C_cond is open"; also the judge `notes`, "sign of the conditional heat capacity … cannot be read from this capture".
    - Replace with: "For the target ensemble, S ≤ 0 (C_cond ≥ 0) wherever J_S ⪰ 0. What this capture cannot give is the **magnitude** of S, and hence the β and j rates. At least one of the two same-target captures is O(1) wrong at the endpoint (U 3.11 vs 8.87). Neither sustained expansion nor a no-go is established."

**Minor items**

13. `xj04_entropy_v001.json → family_r7.s_max_minus_s_r7 = 3.1107213770471906` is mislabelled. That value is the fitted s_max itself; the true difference is about S²/(2|s''|) ≈ 1e-13. The synthesis text does not use it.

14. **L77 and H4 wording.** "finite differences of the exact entropy function" → "of the pooled estimator's entropy function".

---

## 5. Module, fixtures and packet

All three are null, so the module checks are N/A: identical-RHS import by pin, exact corrector, preservation of rejected states, no timestep-only fix and no forbidden import. So are the fixture re-runs and the packet checks (pins, caps, absent output directory, no-retry).

This absence is **consistent** with `fix_supported=false` and with dispatch deliverable 2 ("if the diagnosis supports it"). The lead's return should say explicitly that deliverables 2–4 are intentionally not produced.

**Recommendation for root, not authored here.** Before any new adiabatic continuation from τ = 0, evaluate the existing same-target captures with the §4.9 convexity gate at the τ = 0 reference (β = 1, j = 0, where no reweighting is needed):
- the admission capture `OWNED_L4_ADMISSION_RESIDENCE_RUN_V001`;
- the completed current-graph cycle capture `OWNED_L4_CURRENT_GRAPH_CYCLE_RUN_V001`, which CURRENT_INSTRUCTIONS L234 records as complete and awaiting evaluation.

That is a saved-data evaluation. Re-running the continuation would be a root launch.

---

## 6. Limits and disclosures

**Limits of the evidence**
- H11 rests on the declared symmetric, positive-weight generator (§3.2: code and instructions). I did not read the full sampler to confirm that its stationary law is exactly that weight.
- The within-capture jackknife SE of the violation (1.0–1.1, against −1.3) is a lower bound under failed mixing. The cross-capture contrast is the stronger evidence, and both captures failed mixing.
- The H12 mechanism is UNTESTED.
- I did not re-run H8a/b, H3-tan, H5i or the on-fiber jackknife. The pooled numbers they rest on were reproduced.
- `xv03 → controller.reevaluated_failed_states = []` is wrong: a dictionary overwrite hid the cases. It is superseded by `xv04`, which finds attempts 16, 20 and 24.

**Disclosures**
- Five read-only peek scripts were written to the session scratchpad: `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/scratchpad/peek_*.py`. This is not project space, and nothing in project space was written outside `XV_check`.
- One early read-only manifest hash check used the system `python3`, not the prescribed runtime. It was repeated with the prescribed runtime in `xv06`.

---

## 7. Files (this directory)

**Report and manifest**
- `XV_CHECK_V001.md`: this report.
- `MANIFEST_V001.json`: sha256 of every file below.

**Scripts** (`scripts/`)
- `xv_common.py`: the re-typed algebra.
- `xv01_reweight_convexity.py`: pins, bitwise validation, chains and jackknife, the F spectrum at 83 states and at 86 stages.
- `xv02_fold_identity.py`: the §3.1 identity, the eigen-split, clipping, the jackknife bias, the conditional inequality, and the synthetic theorem check.
- `xv03_rechecks.py`: fold law, transversality, roundoff, controller, endpoint convexity, and the E3 pins.
- `xv04_controller_fano.py`: corrected re-evaluation check, and the jackknife of the violation.
- `xv05_contact_check.py`, `xv06_manifests.py`, `xv07_family_counts.py`, `xv08_mixing_records.py`.
- `xv10_chain_fano.py`: per-estimator event-count and score variances.
- Print helpers: `xv00_peek_eigvec.py`, `xv01b_print.py`, `xv03b_print.py`, `xv09_numbers.py`.

**Results** (`results/`)
- `xv01_reweight_convexity_v001.json`
- `xv02_fold_identity_v001.json`
- `xv03_rechecks_v001.json`
- `xv04_controller_fano_v001.json`
- `xv06_manifests_v001.json`
