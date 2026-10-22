# REVIEW 0407: estimator and spec fidelity, V001

- **Role:** distinct reviewer, not the author. I did not write the module or the conventions note.
- **Method:** static text review and hand algebra only. Nothing was imported, executed, sampled or run. The only code run was `python3 -I -B` `ast.parse`/`compile` on the file text, from my own scratch directory. No `__pycache__` was written into this directory.
- **Date:** 2026-10-16.

## Verdict: PASS_WITH_NOTES (no blocking issue)

Every estimator, sign, normalization and source derivative I checked by hand is correct. The sampler implements the SPEC's sections 2–3 move exactly. Every interface mismatch with the actual operator text fails closed with status `failed`; none produces wrong numbers. No hard rule is violated. The notes below are things to reconcile or fix before launch. N1–N3 matter most.

## Hashes (computed from bytes)

| File | sha256 |
|---|---|
| owned_collective_worldline_static_response_v001.py (reviewed, 83799 B) | 0552b71c88547bf0d0795976d2d3c333d8c38388831c8dc5499cb8ddd909eb8f |
| CONVENTIONS_0407_V001.md (reviewed, 6489 B) | 7787d6a54ac1dbdf9e5374b215a4df2c399dde5a7e5f932815816614cd76f182 |
| Task 0407 | f3f60cebd42db1120b2193968404644a1890cf2f5e48563c2d94544a4bd33fc3 (match) |
| SPEC (worldline proposal V001) | 915e8a43607bb93885b00c888a144d9f18fdbea0fccee046f9dab41523a80ec3 (match) |
| Operator addendum | 7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39 (match) |
| Operator contract | fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642 (match) |
| 0406 | a465d9e3f703f2a2f19d383446c6a2bf6486e5f6be9fdf5996fc96dfb4693d50 (match) |
| Register spec | 032a564bd018b7302bd60de633f8e3c9d2f91f8c079f16b62548bce0e4e53d94 (match) |
| Proper-time V002 | 494d0124c1cd49841760dfc49673d696eab3486d75b31fda708679fa5cacb78a (match) |
| Partial Legendre | d81d48e8407f5576305dbbb50a275f163401bbb91f67b5938dc9736ec8b21663 (match) |
| Kubo / zero mode | a7d048c11a826d6d2627afd3f5324458a0350bc6abbd58bd8ab8d6c39d7eedf7 (match) |
| Assembly | lines 300–327 only |
| Operator text, read for name alignment only (concurrent; may change) | 27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6 |
| Style reference scalar_metric_particular_solve_v002.py | ef767fd79f60852e23ec0de29b04737cf4acfacca3461d83f5b3d01413abaecf |

## 1. Hand algebra: H_c, rates and source derivatives

Positive gauge (L670–692; assembly 300–327). The assembly gives the gauge as D = (−1)^{Σq}(−e^{i arg κ})^{N_S} e^{iθN} with e^{−iθ}ε = −|ε|. That makes e^{iθ} = −e^{i arg ε}, so the module's s_b = −e^{iφ_birth} is the same gauge. The element transforms as conj(G(y)) h G(x). By kind:
- A rise of +1 gives conj(s), a fall of −1 gives s, and a parity flip gives −1. All correct.
- Against the operator's amplitudes:
  - flip: −h → −h
  - hop: −t (θ = 0) → −t
  - bind: +g with a q flip → −g
  - admit: κ, N_S+1 → −e^{−iφ}|κ|e^{iφ} = −|κ|
  - admit_rev: conj κ → −|κ|
  - birth: ε, N+1, newborns R with p = q = 0 → −|ε|
  - birth_rev: conj ε → −|ε|

  The per-kind increment table (L657–667) therefore matches the operator semantics (contract §3, operator docstring).
- The check |gauged + |h|| ≤ tol·|h| is enforced on every enumerated primitive (L807–817), so a wrong increment assumption ends as `unsupported`. It cannot silently flip a sign.
- Gauge increments must net to zero on the initial path (L1255), and every regrown segment must match the increments of the segment it replaces (L1188). Hence every sampled closed path has ∏ gauge factors = 1, and its true weight equals exp(−∫D)∏W.

Rates and energy, with n = N − 1 and w̄ the endpoint-averaged per-cell weights:
- W_X = |h_X|(1 + Σ n_α w̄_αX) (L819, L832).
- D = Σ_d v_d(1 + Σ n w_d) − Σ j O − λA, with A = Σ a·O (L882, L945–947).

Under the checked partition Σ w̄ = 1, 1 + Σ n w̄ = Σ N w̄. That is V002's mean of the support-weighted N at both endpoints, and it equals the contract §5 E_α element. Correct.

| Coordinate u_a | D_a | W_a / W | D_ab, W_ab | Code |
|---|---|---|---|---|
| ("lapse", α), i.e. n_α (= N_α) | Σ_d v_d w_dα | w̄_αX / mult | 0 | L883–885, L953, L975 |
| ("source", ℓ), i.e. j_ℓ | −O_ℓ(x) | 0 | 0 | L955 |
| ("volume_multiplier",), i.e. λ | −A(x) | 0 | 0 | L957 |

All of these follow directly from H_c = H[N] − j·O − λA, and all are correct. The second derivatives are exactly zero because every coordinate is affine. Nonlinear coordinates such as g00 are left to the caller's chain rule, which needs both returned orders (L5). That matches contract §7 and V002's coordinate contacts.

## 2. Estimators (SPEC §4)

The path weight is π = exp(−∫D)∏W, with labelled primitive marks. Hence:
- **Score:** S_a = ∂_a log π = −∫D_a + Σ_events W_a/W. In code, `score = −einsum(dur, Da) + Σρ` (L1286). Correct.
- **Contact:** T_ab = −∫D_ab + Σ[W_ab/W − W_aW_b/W²], which here is −Σ ρ_aρ_b (L1287). Correct.
- **Derivatives of log Z:** ∂_a log Z = ⟨S_a⟩ and ∂_ab log Z = Cov(S_a,S_b) + ⟨T_ab⟩ (L1330–1334). Correct.
- **Free-energy derivatives:** F_u = −⟨S⟩/β and F_uu = −(Cov + ⟨T⟩)/β (L1889–1890). Both signs and the β factors are correct. Absolute F is returned as None and honestly labelled (L4).
- **Mean checks:**
  - j source: ⟨S_j⟩ = ⟨∫O⟩ = β⟨O⟩, so F_j = −⟨O⟩.
  - Lapse: F_n = ⟨E_α⟩, the full diagonal plus offdiagonal energy (Hellmann–Feynman through the event term).
  - Uniform lapse: F_nn = −β Var H, which matches the Kubo note's re-prepared-equilibrium −β Var(H).
- **Read means and responses:**
  - The time-average R̄_r = (1/β)Σ_seg dur·O_r(seg) is exact on piecewise-constant paths (L1279, L1305).
  - d⟨O_r⟩/du_a = Cov(S_a, R̄_r) (L1335) is correct, because R̄ does not depend on u (reads are fixed).
  - Consistency check: Var(R̄) = χ^iso/β, so making a read a source coordinate gives β²Var(R̄) = ∂²log Z/∂j², as L8 says.
- **Zero-rate source opening:** a primitive with amplitude ≠ 0 and mult == 0 records ("lapse", α) for each α with w ≠ 0 (L827–831). That direction is dropped from every output and marked unsupported (L1860–1869). No division occurs, since ρ = w/mult only when mult > 0, and mult < 0 is `unsupported`.
  - For affine coordinates this detection is complete: j and λ are diagonal and cannot open a rate, and an amplitude-0 record has W_a = 0.
  - Other directions remain valid, because a W = 0 mark contributes nothing at the evaluation point.
- **One ensemble:** all columns (S, T, read means, Cov(S, R̄)) come from the same measured paths (`_analyze` L1383–1512). The joint covariance comes from the same replicates.

## 3. Sampler (SPEC §§2–3)

- **Interval regrowth:** the module rotates to a uniform origin and regrows [0, L) from the fixed initial state for exactly L with an unconditioned CTMC: holding Exp(r) (L1114), mark chosen with probability W/r (L1093). It rejects on key mismatch (L1185) and accepts with min(1, exp{∫new(r−D) − ∫old(r−D)}) in log form (L1195–1199).
  - The proposal density exp(−∫r)∏W cancels the rate products exactly.
  - The selection density (origin uniform; whole circle with probability p_whole; length U·f·β from caller components, at least one with f = 1) does not depend on the path or the sources, so it is symmetric.
  - Splicing is correct: the new segments plus old segments m+1 onward, events evs + old[m:], and the final new segment shares a key with old segment m (L1202–1206). The whole-circle case (m = k) is also correct.
- **Rotation:** the rotation move (L1058–1075) re-indexes segments as [s] + [s+1:] + [1:s+1] with the times shifted. It preserves the closed path and is accepted with probability one.
- **Other SPEC prohibitions:** there is no Born-count restriction, no forward-only tree and no basis enumeration.
- **Reverse completeness:** at each sampled event the summed same-kind forward rate x→y must equal the summed reverse-kind rate y→x (L1004–1030).
- **Caps:** every cap raises `incomplete` (L777, L1121, L1127, L1223, L1818) and returns diagnostics only. No path is rejected because of a cap.
- **Time conventions:** imaginary time and sweeps are never called physical time.

## 4. Errors and mixing (SPEC §7)

- **Jackknife:** batches are leave-one-out from all chains pooled. The variance is (J−1)/J Σ(y_i − ȳ)², and the joint covariance has the same form (L1480–1493). Both are correct delete-one-block formulas.
- **Between-chain error:** the variance of the per-chain estimates divided by C (L1494–1495).
- **Autocorrelation:** Sokal τ_int = ½ + Σρ, with the first window M ≥ c·τ(M) (L1343–1364). Correct.
- **R-hat:** the Gelman–Rubin formula is correct (L1367–1380).
- **Mixing gate:**
  - Mixing is `failed` if any non-constant primary column has R-hat above the caller's maximum, any chain has batch length below ratio·τ, or any chain made zero accepted regrowths during measurement.
  - It is `unassessable` if there are fewer than 2 chains or any τ or R-hat cannot be assessed.
  - Errors are returned only when mixing is `passed`. The per-chain batch standard errors in the mixing report are explicitly labelled as not a band.
- **Labelling:** the module calls these statistical/assessed estimates, not a mixing-time bound (L13).

## 5. Conventions note and scope

- The CONVENTIONS note matches the code on signs, outputs, gating, cost and what is not implemented.
- **Legendre:** F + j·Q has QQ Hessian +χ⁻¹, with F_jj = −χ_OO, F_nn = −χ_EE and F_nj = +χ_EO. These are correct for F = −log Z/β. Real-time W/Γ signs (V002 / partial-Legendre Γ_QQ = −χ⁻¹) are explicitly not imported.
- **Scope:** the note gives SPEC §6 scope: static isothermal native functional, not fixed-preparation retarded response (χ_HH^iso = β Var H against retarded 0), not the metric propagator, and no EH matching, c_star, scales, normalization or fits.
- **implicit_closure:** checked first (L1658). Anything other than None returns `unsupported` with the SPEC §5 contract retained.
- **Storage:** L3 honestly records the storage deviation from the SPEC's O(V0 + events).

## 6. Assumed API against the actual operator text (sha 27ad1762…, concurrent)

All differences below fail closed with `failed`. None yields wrong numbers. They are for the final checker to reconcile.
- **D1.** `primitive_channels` also returns the `kind='diag'` records (target_state None).
  - The 0407 module rejects them as "unknown kind" (L799).
  - Reconcile by filtering out `diag` there, because it also comes from `diagonal_terms`. Do not count it twice.
- **D2.** Per-cell weights are `energy_weights`, a dense tuple in `context.energy_cells` order. 0407 expects `weights` as a mapping {cell: w}.
  - Zip it with `energy_cells`.
  - `lapse_factors` must then cover every energy cell, because 0407 requires a factor even for cells with zero weight (L736).
- **D3.** `diagonal_terms` records carry `amplitude` (complex) and `energy_weights`, not `value` and `weights`.
- **D4.** `read_rows` returns {labels, values, presence} arrays, not a list of records. 0407 fails with "read_rows did not return a list" (L893).
- **D5. Compatible:** `validate_owned_model`, which returns {ok, stage_reached, failures, context}.
- **D6. Compatible:** `canonical_state_key`, a tuple of ints that compares with `==` to a bool and is hashable.
- **D7. Compatible:** the kind tokens.
- **D8. Compatible:** the amplitudes are H matrix elements with the conventions in §1.
- **D9. Compatible:** forward and reverse Birth `changed_support` are equal as sets (cut + child + newborn + donors), so the signature filter works.
- **D10. Compatible:** every reverse reconnection is its own record.
- **D11. Compatible:** coincident destinations stay separate.

## 7. Hard rules (static AST, run from scratch)

- **Imports:** only `bisect`, `math`, `collections.abc.Mapping` and `numpy`.
- **Forbidden calls:** none present.
  - No `@` operator.
  - No dot, matmul, vdot, inner, tensordot or outer.
  - Every `einsum` passes `optimize=False`.
  - No print, open, eval or exec.
  - No threads, os, sys or subprocess.
  - No global or nonlocal.
- **Module level:** only the docstring, the imports, the `LIMITATIONS` string, the `_Stop` class and function definitions.
- **Public function:** one public function with 22 keyword-only parameters and no defaults. No helper has a default either.
- **Compile:** `compile` of the text succeeds.

## Notes (non-blocking; ranked)

- **N1 (fix at reconciliation).** L2 says the model-level member check is "delegated to validate_owned_model". The actual operator does not perform it.
  - Its `_admit_model` accepts any real h, t, g, any θ, per-vertex complex κ and per-owner complex ε.
  - The member is therefore certified only on primitives enumerated at visited states.
  - Example: a nonzero θ, or a negative or zero t, h or g, on an edge or vertex never enumerated (such as a rarely born child edge) would let a run finish `ok` for the positive |h| model rather than the caller's model.
  - Add a model-level check before launch, either in an operator `validate_member` or in a reconciler wrapper: h, t, g > 0 real; θ ≡ 0 on every edge key that can occur, including newborn and child edges; common arg κ; common arg ε.
- **N2 (fix at reconciliation).** A referenced label (source, A coefficient, tracked or coordinate) never seen in any read only raises a flag (L1903). `ok` can still be True.
  - The actual operator lists every read label at every state, with value 0 when absent.
  - A label it never returns is therefore a caller typo, and it silently gives a zero derivative.
  - With that operator, fail closed: check the referenced labels against `context.read_labels` plus the extra-read labels.
- **N3 (record).** The SPEC wants O(V0 + events) storage; this module stores one state and key per dwell (L3).
  - With the operator's 7-int bitset keys this is O(events · V0/word), which is practical but a documented deviation.
  - The per-event work is O(V) operator calls (`primitive_channels`, `diagonal_terms`, `read_rows`, key), which fits the SPEC's stated worst case.
  - The reverse-check fallback can cost O(V) key computations per event and is counted.
- **N4 (scope).** The returned quantities are:
  - first derivatives of read means;
  - the joint statistical covariance;
  - log Z Hessians, which include read–read susceptibilities once reads are made source coordinates.

  It does not return d²⟨O⟩/du², which the register spec uses for second-order δC (and which would amount to third derivatives of log Z). C = M − μμᵀ and the first-order δC = δM − δμ μᵀ − μ δμᵀ can be assembled by the caller from the outputs. The 0407 brief does not require more, but the reading "their covariance = C" should be confirmed by the checker.
- **N5 (stale text).** L8 says coarse R and S are available only through `extra_diagonal_reads`. The actual operator's `read_rows` already includes coarse R_α and S_α with the current-state 1/m_α. This is harmless; update the text.
- **N6 (statistics).** Cov uses 1/n normalization (an O(1/n) bias, partly corrected by the jackknife). Products S_aS_b are not mixing-gated separately (L13). The pooled-batch jackknife relies on the mixing gate, which is enforced. All of this is acceptable as labelled.
- **N7 (minor).** The `_admit_tolerances` error message duplicates on a non-real input. The float roulette fallback `channels[-1]` (L1100) has an O(ulp) effect and is negligible.
- **N8 (record).** The extra inputs `gauge_phases`, `numerical_tolerances` and `error_parameters` are justified, since the module must not choose values. `gauge_phases` is cross-checked on every primitive.
