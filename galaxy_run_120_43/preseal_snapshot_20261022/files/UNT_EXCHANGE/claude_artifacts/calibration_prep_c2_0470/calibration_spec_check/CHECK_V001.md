# CHECK_V001: independent check of calibration_spec (DDO154 calibration coordinate spec, draft C2V001)

**Verdict: PASS_WITH_CORRECTIONS.**

The derivations are correct. The binding decisions A1 and A2 are respected, nothing was launched, no NGC3198 data was touched, and no scipy was used.

The defects are omissions and underspecified rules, not wrong numbers. Four of them (D1–D4) would let the 120/43 run either silently condition the NGC3198 band, or stall and fill the disk partway through calibration. D1–D7 must be fixed in the spec before the first W1 calibration call. D8–D21 must be fixed before freeze.

## Scope and method

- **Checked:**
  - `calibration_spec/build_calibration_spec_c2v001.py` (`f2e1fd7b…`)
  - `DDO154_CALIBRATION_COORDINATE_SPEC_DRAFT_C2V001.json` (`a7709bd2…`)
  - `SPEC_VALIDATION_C2V001.json` (`ee7e6742…`)
  - All three match `HASHES_C2V001.txt`. I did not write any of them.
- **How I checked:**
  - Read-only, synthetic-only.
  - Runtime: codex python3 `-I -B`, numpy 2.3.5, one thread.
  - Every forward function in my fixtures is a toy I wrote. None of them is the project forward.
- **Not opened:**
  - No NGC3198 file.
  - Nothing in the 0466 driver folder was edited. Its driver (`75b0c08a…`, unchanged since the spec read it) and `INTERFACE_C2_0466_V001.md` (`10d1db3c…` at my read, still being written) were read only.
- **Line references:**
  - `B:n` is a line of the builder. JSON paths name spec fields.
  - `ENG:n` is a line of `calibration_freeze_0462/calibration_region_engine_c3v001.py`.
  - `DRV:n` is a line of the 0466 driver.
  - `IF66 §n` is a section of the 0466 interface.
  - Other source abbreviations are the spec's own.

## 1. What I re-derived (all CONFIRMED)

| Claim | Check |
|---|---|
| 30 input pins | All verify from bytes (k01). Driver 0466 hash now equals hash at read. |
| Reproducibility | Builder rerun from a copy gives an identical spec except `created_utc`. The validation file is byte-identical, `ee7e6742…` (`rerun/`). |
| Native literals | Cycle and admission `trial` dicts are identical: 19 literals, sampler beta 1.0 for both. The spec's `native_*` values equal them (k02). |
| γ/Eref anchor and box | Anchor 2.008512630003547e-17 is exactly 10 × V008 (1.8566e41 / 9.2435e58). Box ×[0.1, 10]. |
| Gamma scans | Outward counts on fixed V006: 66, 96, 96, 62, 0, 0, 0, 0 at 2e-22 … 2e-15. Current V008 source: 0 and 0. V008 trial failed with FREE_BOUNDARY_NOT_BRACKETED. |
| 1/γ exponent | Exponent range [−0.99789, −0.98210] over 96 nodes. The nodes are paired by identical `R_m`/`phi`/`query_index`, and all diagnostics are positive (inward). |
| s box | obs/pred v² = 0.8669 to 1.4197 (region rows against FR-MD:131). The cube-to-sphere shift is −9.89% / +1.78% in speed. |
| Distance | u_D(4.04) = 0.45581. ln-box width 0.032236. |
| ℓ_F | ℓ_F = 3.2100 kpc. Period span 1.04 to 4.16 (review row 7's 2.08). 17.3 nodes per period at the ×2 edge. |
| Cost | 20 receipts, hashes OK, sum 6844.8 s (1.90 h). Equal to IF66 §12's measured 6845 s. |
| Citations | Region:109-124, calibration input:141/154/621/1141/1142/1147-1150/1158, binding V003:24-30/72-84/89/91/99-104/108/129-134 and actual_heights (R_d 0.3584 / 0.2639), LIVE:29/37/41/47/51/53/67/78-80, seed V002:11/71-72/88, C178 coordinate names at 486-620, ASM:1643, DRV:409-413 (geometry refusal), DRV:543-571 (s·Eref, s·γ) and DRV:85 (default grid = V004). Each matches its source text. |
| Binding decisions | A1 is respected: m=0 route B, kernel unmodified, orientation counted with tilt UNTESTED, m≥1 not assumed small (CA-04 cites the 19.26% folded mass from review row 35), truncation settled before calibration (PC-1). A2 is respected: grid `2e3a36d8…` bound by PC-2, PROVISIONAL, not accepted. Both reviews' corrections are reflected: row 7's 2.08, rows 10, 15, 20, 30, 35, 37. |
| Process | No scipy, subprocess or NGC reference in the builder. The engine was run only on a toy. DI-1…DI-6 are declared before any calibration call. |

## 2. Adversarial fixtures (synthetic; with the spec's engine parameters and the frozen 0462 engine)

| Fixture | Result |
|---|---|
| Spec's own sizing toy (rerun) | COMPLETE, 76 calls: seed 1, jacobian 10, repair 1, march 28, bisection 24, design 12. Reproduced. |
| k03 F1: saved V004 anchor, common factor only | No admission window. Row 06 needs a factor ≥ 0.99978 and row 11 needs ≤ 0.97045. TESTED-NEGATIVE (arithmetic on saved rows): admission needs non-uniform shape changes from ℓ_F, A2 or truncation. |
| k04 G1: repairable anchor (obs + 0.5·(V004 − obs)) | COMPLETE, 41 calls. **All 18 admitted points have the anchor's projection on every near-null direction to ≤1.1e-16.** |
| k04 G2: G1 + 0.0095 km/s per-call noise | The engine identifies a noise direction (s₃ = 1.51 ≥ tol·s_max = 1.077), where DI-4's own threshold would be 1.645. It marches it, and 5 of 6 sides hit box faces. |
| k04 G4: G1 + 20% calls BLOCKED (mimics ROUTE_A_ITERATION_NOT_4) | COMPLETE, 46 calls, 10 invalid, 6 extra Jacobian halvings. **2 of 4 region boundaries are set by a blocked call, not by a rectangle miss.** |
| k04 G5 + k05(a): weak response | Engine returns NO_ADMITTED_POINT after 3 repairs (14 calls). But a common factor in [0.9931, 0.9966] is admitted, e.g. s = 1.042, u_s = 0.530, inside the box. **False empty** (TESTED-POSITIVE on the toy; UNTESTED on the real forward). |
| k05(b): all 5 directions identified, long extents | COMPLETE, 72 calls with 0 bisections, so all 10 sides end at box faces. The analytic worst case with halvings is 116–136 calls, against a budget of 120. |

## 3. Defects (line-specific)

### Must be fixed before the first calibration call

**D1 (major). Near-null directions are pinned in the frozen envelope, not "carried".**

*Where:* B:226-230, `coordinate_metadata.gamma_over_Eref.identifiability_indicator`: "a near-null direction is carried, never pinned". B:304 / DI-1.

*Problem:*
- The engine repairs, marches and designs only along identified directions (ENG:1114-1119, 1165-1168, 1247-1251).
- So every admitted point, and every Module-2 representative, sits at the anchor's projection on each near-null direction (G1: ≤1.1e-16).
- The spec itself expects the d ln s = −d ln(γ/Eref) direction to be near-null. If it is, the 43-point band silently conditions on the anchor's Eref/γ split. That split is the seed-V002 choice of the "ratio 10" decade, made under V004.

*Correction:* declare before W1 how each near-null direction that involves a shared theory coordinate enters the freeze. For example: points along it to the box faces, verified admitted on DDO154, then evaluated on NGC3198 and reported. Otherwise the headline must be labelled conditional on the anchor projection. Replace "never pinned".

**D2 (major). Missing precondition: the route-A iteration-4 blocker.**

*Where:* B:407-415, `preconditions_before_freeze`.

*Problem:*
- The driver refuses any call whose route-A fixed point converges at an iteration other than 4: DRV:685-703, `Blocked('ROUTE_A_ITERATION_NOT_4…')`, IF66 §11 item 1.
- Every change of s, γ/Eref or ℓ_F reruns route A (DRV:543-571; IF66 §2, "each needs the whole chain").
- G4 shows what invalid calls do: they force Jacobian halvings and set region boundaries.

*Correction:* add PC-9, a reviewed successor that accepts the converged route-A iteration, with a test that it reproduces the saved chain.

**D3 (major). No disk budget.**

*Where:* B:317-337, `evaluation_budget_proposal`.

*Problem:*
- The saved chain occupies 5.67 GiB per call (measured `du` of the 20 runs; route A alone is 3.49 GiB).
- About 330 GiB was free at check time, which holds about 58 calls.
- Tier 1 alone needs about 140–240 calls.

*Correction:* add a retention rule (what is kept per call, and what is pruned after the 12 speeds and custody records are hashed) and a disk line in the budget.

**D4 (major). DI-4 cannot be implemented inside the frozen `run_calibration_region`.**

*Where:* B:311-314 and B:420 (DI-4); B:389 (freeze gate).

*Problem:*
- The engine decides identification by `s_i ≥ tol·s_max` alone (ENG:889-895), inside the orchestrated call.
- G2 shows the engine marching a direction that DI-4 would call near-null.
- `s_max` is dominated by the box widths (the ×100 γ/Eref box). Which directions count as identified therefore depends on computational box widths, and only the absolute noise criterion is box-independent.

*Correction:* fix before W1 a formula, for example `null_tolerance_eff = max(1e-3, s_noise/s_max)` with `s_noise` from PC-7. Apply it through `finite_difference_jacobian` → `identifiability_report` → `explore_region`, and restate the freeze gate for that path.

Two smaller notes on the threshold:
- 0.0095 km/s is a Picard increment, not measured call-to-call noise. PC-7 is the right place to measure it.
- The i.i.d. largest-singular-value estimate is about 3.8, against the spec formula's 1.645.

**D5 (moderate-major). No pre-declared rule for engine outcomes other than COMPLETE.**

*Where:* B:388-389, B:416-422.

*Problem:*
- There is no rule for NO_ADMITTED_POINT, BUDGET_EXHAUSTED, SEED_INVALID or ANCHOR_INVALID.
- The 3-step centre-targeting repair can return NO_ADMITTED_POINT while admitted points exist in the box (G5 / k05a).
- F1 shows the saved anchor shape is not repairable by common factors alone.

*Correction:* declare that NO_ADMITTED_POINT is REPAIR_FAILED with emptiness UNTESTED. Pre-declare its deciding test (a fixed restart rule) and the condition under which an empty region is registered TESTED-NEGATIVE. Do not widen rectangles. Also declare the exhaustion rule: rerun with a larger budget, replaying from the θ-keyed cache with zero new calls for points already evaluated.

**D6 (moderate). Boundaries set by failed solves are not distinguished from rectangle misses.**

*Where:* B:224 ("invalid evaluations … are logged") and B:404-406.

*Problem:* the engine treats an invalid evaluation as a rejection (ENG:1197-1204). In G4, 2 of 4 boundaries are solver or blocker limits.

*Correction:* declare a VALIDITY_LIMITED flag for every side whose first rejection is invalid, and carry it into the freeze notes.

**D7 (moderate). The edge rule covers only nuisance coordinates.**

*Where:* B:419, DI-3.

*Problem:* free coordinates s, γ/Eref and ℓ_F hitting box faces have no rule. In k05(b) all 10 sides end at faces; in G2, 5 of 6.

*Correction:* extend DI-3, or a sibling rule, to free coordinates, with a pre-declared widening that is reported, never silent.

### Must be fixed before freeze

**D8 (moderate). Tier-2 branches and the union rule are underspecified.**

*Where:* B:298-301 (DI-2), B:304 (DI-1), B:389.

*Problems:*
- It is unspecified what a non-promoted tier-2 branch contributes to the 43-point union: one verified point, or the BR-A hull shifted linearly.
- The freeze gate (`run_calibration_region.status == COMPLETE`) can never be met by a tier-2 branch.
- The linearised repair is new code outside the frozen engine and needs review.
- DI-1 has no headline rule for a union of branches: Module 2's `central` is the median of a single point set.

**D9 (moderate). The A2 sensitivity is not operationalized.**

*Where:* B:302-303, B:430-435.

*Problem:* ROOT_DECISIONS:31 says the V004-versus-pooled difference and the single-chain spreads "are carried as sensitivity". The spec has no evaluation that carries them. The A2 npz holds `single_chain_grid_*` but no per-chain backgrounds.

*Correction:* define the sensitivity evaluation, for example at the BR-A admitted representatives, and how per-chain grids become driver-acceptable npz files.

**D10 (moderate). PC-1 and the truncation item ignore that route A cannot be masked.**

*Where:* B:404 and B:408 (PC-1).

*Problem:* IF66 §5 says "Route A is not masked… stays cube-truncated", and §11 item 4 marks the full-chain mask UNSUPPORTED. So the converged truncation can be adopted for the route-B field only.

*Correction:* PC-1 must require a route-A extension, or count the residual cube truncation of K0, body and roots.

**D11 (minor-moderate). Stale cost wording.**

*Where:* B:209, B:218, B:233 ("no kernel rebuild", "one kernel rebuild (≤124 s)"); B:337 (speed lever 3).

*Problem:* the 0466 driver reruns the whole chain (1.9 h) for each change and does not exploit the 1/s shortcut (IF66 §2, §11 item 6). The budget at B:317-334 already uses the whole chain, so this is an internal inconsistency only.

**D12 (minor-moderate). The PC-4 rule is circular.**

*Where:* B:411.

*Problem:*
- The rescan at {0.1, 1, 10}× the anchor evaluates exactly the current edges, so "move the edges to the nearest evaluated ratios" cannot move them.
- "The same rule" is undefined: the lower edge failed on the current source but was all-inward on the fixed V006 source.
- Re-deriving the anchor ratio under A2 is unspecified, and through D1 it matters.

**D13 (minor-moderate). The ℓ_F box rationale assumes 72 nodes at kmax 2/kpc.**

*Where:* B:234-237.

*Problem:* PC-1 targets kmax 3–4/kpc. At kmax 4, the ×2 edge gives about 8.3 periods and about 8.7 nodes per period on 72 nodes, not ≥17. C̄ also changes under A2.

*Correction:* re-derive the box after PC-1.

**D14 (minor). Fixed native ratios are described as "preserved".**

*Where:* B:364 (CA-25), "unconstrained directions are preserved".

*Problem:* the 11 native ratios and b are fixed at one point, not explored, and the engine pins near-null directions (D1).

*Correction:* reword. Add to B:430-435 "native ratios/b variation: UNTESTED; deciding test: native re-sampling at alternative points".

**D15 (minor). NGC wording is too strong.**

*Where:* B:383, "no NGC3198 file (target or source) is read".

*Problem:* the builder parses binding V003, which holds NGC3198 source descriptions (lines 24, 51-67, 84, 87), and it hashes LIVE. No NGC3198 velocity is read and no NGC value is used; `bind` at B:126 is never used.

*Correction:* reword to "no NGC3198 target file read; no NGC3198 value used".

**D16 (minor). The custody claim is overstated.**

*Where:* B:2-3, "every input is SHA256-verified from bytes".

*Problem:* the claim does not hold for:
- the 20 `receipt.json` files (B:100-113; hashes are recorded, not verified);
- the 10 gamma-scan `input.json` files, which supply the Eref denominators (B:150; not hashed at all);
- `points.jsonl` (B:162; recorded only).

*Correction:* pin them. My hashes for the 10 `input.json` files:

| Run / candidate | sha256 prefix |
|---|---|
| FIXED_V001 c0 | 2cd5bbb4 |
| FIXED_V001 c1 | 5bd0732e |
| FIXED_V001 c2 | b68bd4f9 |
| FIXED_V001 c3 | a6ad74d8 |
| FIXED_V002 c0 | fb1f4d61 |
| FIXED_V002 c1 | b45353c5 |
| FIXED_V002 c2 | 55a32a57 |
| FIXED_V002 c3 | ccf9766c |
| CURRENT c0 | 6036f3ea |
| CURRENT c1 | 98541dad |

**D17 (minor). Validation toy mislabelled.**

*Where:* B:455-457 and B:481.

*Problem:* the toy's null is u_s + u_r, which is d ln r/d ln s = −3.32. It is not "ln s + ln γ-ratio". Sizing is unaffected.

**D18 (minor). The s-box rationale arithmetic is loose.**

*Where:* B:210-214.

*Problems:*
- The margins are about 1.14 on the low-s side (row 01 with the −18.8% force shift) and about 1.7 on the high side, not "~1.4 per side".
- The cube-to-sphere shift is not a bound. Review row 30 finds no in-domain plateau; row 01 moves −28.4% at 1.8/kpc and −40.5% at 1.5/kpc (iso).

**D19 (minor). Tier-2 coverage is incomplete.**

*Where:* B:293-297.

*Problem:* tier 2 is one-at-a-time around BR-A only. Two things stay UNTESTED and should be listed: BR-K1 crossed with {ML, He, Γ, h*, photometry}, and interactions between branches.

**D20 (minor). PC-6 names no provenance source.**

*Where:* B:257-259, B:413.

*Problem:* the A2 npz carries no trial dict (its keys are `background_*`, `source_hessian_grid`, `single_chain_grid_*`).

*Correction:* name the provenance: cycle and admission `result.json`, pins `6377a9bc…` and `3c82d2be…`.

**D21 (scope note). The freeze-stage NGC3198 evaluations are not budgeted.**

*Where:* B:304.

*Problem:* the count of representatives × branches is not budgeted, and `forward_ngc` does not exist yet (IF66 §11 item 3). This is outside B1, but DI-1 commits the run to it.

## 4. Classification of the open items the spec raises

| Status | Items |
|---|---|
| UNTESTED, deciding test named | ℓ_F response; native/EH split under A2; converged truncation (P-88); artifact-free m≥1 (D3); tilt family. Add native/b variation (D14), BR-K1 tier-2 (D19), A2 coefficient sensitivity (D9). |
| TESTED-NEGATIVE (arithmetic) | Admission of the saved V004 anchor shape by any common factor (F1). |
| DECLARED (freeze owner, before W1) | D1, D4, D5, D6, D7 rules. |
| Measured preconditions | PC-7 noise floor, PC-3 re-anchor, PC-4 rescan; plus PC-9 (D2) and the D3 retention rule. |

## Files (checker subfolder; hashes from bytes)

| File | SHA256 |
|---|---|
| `k01_pins.py` | fc383fe4138c86135288ca046bd83e8aad8c0530a359ba84fc3cf3c91c8c4c84 |
| `k02_sources.py` | bd1602ca665af5138fffded61852aa0351557ede628fd8b7b031e7f8420239d8 |
| `k03_adversarial.py` | 239bcb6eebf4414a80f8c19f0d499e6d34ef354272ed324b5c6b5dd8082ff97a |
| `k04_admissible_toys.py` | 6a2ec3f6a7f76d194f830be3af1f13a998b162fcd296ad3a969385a707d76f5a |
| `k05_false_empty_and_budget.py` | 76093081b14eb0c2ab431b32d1f8c20971c4778451276387062179ff21c19a2d |
| `K01_OUTPUT_V001.json` | 4401ff3c187391c93031af604bf5e230615c0a37b73da7485626a93758d10d6a |
| `K02_OUTPUT_V001.json` | 5e4ba101e6e3269ec7c9d6dfcee8e3d51c91f84233dfd18940abdfaec24127b2 |
| `K03_RESULTS_V001.json` | d795191bc9cddebfeadd21659c5cef8651889da914f26f49bffb44a34fa5aefa |
| `K04_RESULTS_V001.json` | 969ed5e9126d980394cafc57b701f42b6e89d8af712a9ca2d4c247357b6c17c0 |
| `K05_RESULTS_V001.json` | d50c44ab12e56bc368e16ac1a2270cfee3c7f9108c114f7cac6967f8006624a2 |
| `rerun/DDO154_CALIBRATION_COORDINATE_SPEC_DRAFT_C2V001.json` | f2625cce3f66d8db2a20c3ea77c9f648949d7577fe642e863588543f94bce95b (differs only in `created_utc`) |
| `rerun/SPEC_VALIDATION_C2V001.json` | ee7e6742322056350491507787feafed9dea636da978151cb9d96425e54c9bd7 (identical to the original) |
