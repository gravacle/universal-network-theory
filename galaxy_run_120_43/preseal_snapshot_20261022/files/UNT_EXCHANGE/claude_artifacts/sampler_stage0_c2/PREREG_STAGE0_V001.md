# PREREG_STAGE0_V001 — P-96 stage 0: L=4 control, 8 chains from distinct born graphs, x/y/z-polarized starts

Claude2 workflow lane, 2026-10-18 (UTC, written before any stage-0 sampler output existed: no smoke run, no worker successor, no start state had been built when this file was sealed). Mandate: A29 workstream 2 and A20/A19 in `ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md` (open; cited by name, not pinned). Frozen pins used: V002 addendum `17c26616…`, V003 addendum `5bef6552…` (A12/P-96 row at V003:96).

Groundwork read (sha256 from bytes): RD2 capture plan `698d743a…` (stage 0 at §8), CHECK_RD_V001 `ab1ed1b1…`, REACH_GROUNDWORK_INDEX_V001 `4adffde2…`, RD5 rotated-start rule in `FROM_CLAUDE4/0036`, BIRTHK_PILOT_EVALUATION_V001 (mixing rule, worker/recipe pins).

Grades: DECLARED-PREMISE / HYPOTHESIS / FORMAL-RESULT / TESTED-POSITIVE / TESTED-NEGATIVE / UNTESTED (+deciding test). Every outcome below registers; none is a target. Nothing here prescribes what the sampler or the response must look like.

## 0. What stage 0 is for (DECLARED-PREMISE)

Stage 0 measures, on the current BIRTHK kernel at L=4, whether chains started from 8 distinct born graphs with starts polarized along x, y and z agree with each other under the pre-registered mixing rule, and what the start-balanced coefficient grid and its between-graph spread are. It decides whether stage 1 (L=6 pilot) is proposable, and supplies a start-balanced sensitivity grid for the NGC3198 outer rows (A18 plug). It does not touch the tail question (A20: FORMAL under the static isothermal typing; UT-1 owns it).

## 1. Design (DECLARED-PREMISE)

| Item | Value |
|---|---|
| Kernel | BIRTHK mixture unchanged: recipe `owned_L4_worm_birthk_recipe_v004.py` (997f4d1f), family recipe 86c2ee53, sampler v006 896cadbb (base v004 7d079892), operator a04f8795, adapter 0705be7c, occupancy dedc9328, statistics 85f4c638, Birth c2v002 6c14cb85, worm c2v001 9fef6042, admission c3v001 5b19e90e, durability v002 c0646a93. Fixed mixture .25 occupancy / .10 worm / .20 Birth / .20 admission / .25 base. TRIAL, beta = 1, L = 4 unchanged |
| Chains | 8, **one chain per process** (k = 0..7) |
| Born graphs | B_k = saturated born graph from the registered adapter seed by the RD2 s1 protocol (`RD2_capture_plan/scripts/s1_states_v001.py:112-133`): stream `SeedSequence(2026101810).spawn(8)[k]`; per pass an RNG-permuted owner order; for each owner the native Birth records (`palette_channels`, kind `birth`, owner_id[0] `birth`, nonzero amplitude), one drawn uniformly; repeated until no owner has a Birth mark |
| Start rotation g_k | axis y: identity e; axis x: c3 = cell (c0,c1,c2)→(c1,c2,c0), Cartesian (x,y,z)→(y,z,x); axis z: c3∘c3. Maps as in `RD5_cbar_anisotropy/rd5_common_v001.py:32-65` (TESTED equivariances of born graph, Hamiltonian and kernel rules: A19). FORMAL: c3 maps the seed's C̄ = diag(0,3,0) to diag(3,0,0) (M C̄ Mᵀ) |
| Axis per chain | k: 0 y, 1 x, 2 z, 3 y, 4 x, 5 z, 6 x, 7 y (3 x, 3 y, 2 z: in-plane balanced; never all y) |
| Start state x0_k | g_k(B_k) as a labelled mapping; its canonical key and key-text sha256 (durability `key_text_sha256`) are pinned in the starts manifest; initial path `{'x0': x0_k, 'events': []}` |
| Chain RNG | `np.random.default_rng(SeedSequence(2026101811).spawn(8)[k])` |
| Schedule | burn-in 2048 sweeps, 16384 measurement sweeps, 5 moves/sweep; batches_per_chain 8 → batch length 2048 |
| Caps per process | max_sweeps 18432; max_events_per_path 10000 (unchanged); max_total_events 21,600,000 and max_channel_enumerations 14,400,000 (v004's time-proportional caps ×4.5 = 18432/4096); soft and hard wall/RSS/output caps set from the measured smoke numbers in the launch package |
| Durable capture | durability v002 unchanged (16-row atomic blocks: scores, all-k contacts, background, features, reference key, census, U). The worker's result.json keeps every analysis output and drops only the per-row series already in the committed capture |
| Preconditions (checked before launch, else no launch) | (i) every x0_k decodes, re-keys to its pinned key, and is admitted by the sampler (smoke); (ii) pairwise shared present edges between the 8 starts < 50% of the smaller present-edge count; (iii) g_k(B_k) ≠ g_j(B_j) for k ≠ j; (iv) the successor worker reproduces the pinned worker v004 bitwise at the original seed/start (identity test) |

## 2. Mixing rule (numeric; applied by an external evaluator over the 8 processes)

With one chain per process every process's own sampler analysis is `unassessable` (S4:3844, FORMAL). The rule is computed offline from the committed rows of all 8 processes, with the program's estimators transcribed exactly (S4 `_rhat` :3746-3759, `_sokal_tau` c = 5 :3722-3743, `_analyze` column set and statuses :3762-3860, `_allk_analyze` block projection :4274-4444). The evaluator must reproduce the sampler's own Rhat and τ on an existing 2-chain capture (BIRTHK) to ≤ 1e-10 before it is used (check A0).

**Columns.** As S4: for each of the 36 all-k blocks, its d score columns, its contact upper triangle (structurally zero non-NN entries are `exact_invariant`, other constant columns `unassessable`), and events_per_path; the background's 9 read columns and events_per_path. A chain with zero changed-path accepts in measurement fails the rule (S4 L28).

**R-LIT, the literal two-part rule (P-96 as written).** Every assessed column has Rhat ≤ 1.1 over the 8 chains, and in every chain blen/τ̂ ≥ 5, i.e. τ̂ ≤ 409.6 sweeps (blen = 2048). Any `unassessable` column makes R-LIT unassessable.

**R-MA, the multiplicity-aware rule.** Same columns, same Rhat leg (Rhat ≤ 1.1 for every column). τ leg: for each column the pooled-ACF τ̃ (ρ̄(t) = mean over the 8 chains of each chain's own normalized autocovariance; Sokal window c = 5 applied to ρ̄) satisfies τ̃ ≤ 409.6, and every per-chain τ̂ ≤ 819.2 (a 2× guard against a single grossly slow chain). Reason (FORMAL + TESTED in RD2/RD3): with 778 columns × 8 chains the maximum of ~6,000 noisy per-chain τ̂ fails the nominal threshold for a perfectly mixed sampler unless τ ≲ blen/20; the Rhat leg at 8 chains and n = 16384 has no such problem. R-MA changes only the τ estimator's noise, not the threshold or the estimand. Its size and power are measured on synthetic AR(1) data before launch (check P0-b) and reported with the outcome; the rule does not change with that result.

**Census/U two-part rule (delta spec V004:197).** Series `time_mean_active_slots` and `time_mean_U` (durability v002 fields): Rhat ≤ 1.1 over 8 chains; τ̂ ≤ 409.6 in every chain; and **flat quarter means**: for every chain c and series x, with the measured series cut into 4 contiguous quarters of 4096 rows, Q_j the quarter means, x̄_c the chain mean, τ̂_c the chain's Sokal τ and s²_c its variance,

  max_j |Q_j − x̄_c| ≤ 2.91 · SE_Q,c,  SE_Q,c = sqrt(2 τ̂_c s²_c / 4096).

2.91 = 3.36·sqrt(3/4): Bonferroni over 2 series × 8 chains × 4 quarters = 64 tests at family-wise 0.05 (two-sided z = 3.36), times the sd of a quarter's deviation from the 4-quarter mean. An unassessable τ̂ fails flatness. Its size and power are measured before launch on synthetic AR(1) data (check P0-a, below). Reported with no decision weight: the RD2 proposal (|Q_j − x̄| ≤ 2 batch SE) and degree-1/degree-3 counts.

**Pre-launch synthetic checks (registered now; results reported, rules fixed).**
- P0-a: family-wise false-failure rate of the flat-quarter rule over 16 stationary AR(1) (series, chain) units at τ ∈ {10, 50, 100, 200}, n = 16384; power against a linear drift whose half-to-half mean difference is 0.5 and 1.72 sd (1.72 = BIRTHK chain-0 U drift).
- P0-b: P(all 778 columns pass) under stationary independent AR(1) chains (8 × 16384) at τ ∈ {50, 100, 150, 200, 300} for R-LIT and R-MA.

## 3. Coefficient-grid estimator (registered)

- Per (process k, batch b of 8, block): plug-in sums of the block score vector (Mandel √2 once, profile-major as S4 LK3) and its NN contact rows. H = Cov + ⟨T⟩ exactly as v004 `_estimate` (:3707-3716); F = −H/β.
- Grid h(k) as in `BIRTHK_PILOT_EVALUATION/scripts/b7_gate_coeff.py` `grid_arr`: self-conjugate h = F/64; pairs h = [(cc+ss)/2 + i(cs−sc)/2]/32; partner = conjugate.
- **Point estimate:** pooled over all 8 × 16384 rows (= S4's pooled estimator: mean within-chain H plus between-chain covariance of chain means).
- **Error (primary):** leave-one-process-out jackknife over the 8 processes, SE = sqrt(7/8 Σ (g₋ᵢ − ḡ)²) per grid entry. It is a between-graph band and is reported whatever the mixing outcome. The 64-batch leave-one-batch-out jackknife (S4 L13) is reported as an error only if R-LIT passes; otherwise it is withheld, as S4 withholds it.
- **Convexity gate:** CONVEXITY_GATE_V001 as implemented in b7 (pooled blocks and nodes, every process, every leave-one-process-out and leave-one-batch-out replicate; 1e-10 relative roundoff).
- **k = 0 lapse:** h_NN(0) = −(Var S_N(0) + ⟨T_NN(0)⟩)/64 pooled, per process, with the jackknife SE; ρ = Var S_N(0)/|⟨T_NN(0)⟩|. Sign T(0) < 0 is FORMAL under the current typing (RD3-2) and carries no decision weight.
- **Descriptive distances** (relative Frobenius, b7 `rel`): stage-0 pooled vs A2 (2e3a36d8) and vs the BIRTHK pooled grid; leave-one-process-out spread.

## 4. Anisotropy statistic (A18/A19)

For any set of chains, C̄ = M − μ̄μ̄ᵀ from the mean background row /64 (labels R0..R2, S00, S11, S22, S12, S02, S01; b7 `bgC`, Claude3 `moments`). s = (C_xx − C_yy, 2C_xy)/(C_xx + C_yy); q = |s| (the in-plane anisotropy); major axis angle from x.
- Reported per process (8 values of s, q, axis) and pooled (equal-weight mean of the 8 process mean rows).
- **Start-memory test.** For process k with start axis a_k: u_k = (C_aa − (C_bb + C_cc)/2)/(tr C̄/3). Ū = mean u_k. Exact randomization p over all 3⁸ = 6561 reassignments of the 8 start axes (valid under the null that each chain's C̄ law is c3-invariant, which the TESTED equivariance makes the no-memory null). Also m = number of processes whose largest C̄ diagonal is their start axis; null Binomial(8, 1/3), P(m ≥ 6) = 129/6561 = 0.0197.
  - START_MEMORY_DETECTED if p ≤ 0.05 or m ≥ 6; else NO_MEMORY_DETECTED. Reported: the in-plane contrast D = mean s₁(x-starts) − mean s₁(y-starts).
- **Pooled isotropy.** WITHIN_REFERENCE if q_pooled ≤ 0.016 (A18 better-mixed-kernel level); else EXCEEDS_REFERENCE, with z = |s₁,pooled| / SE_jackknife-by-process. EXCEEDS_REFERENCE with z ≥ 3 in a start-balanced design reads as an x↔y-breaking element other than the start (A19 found none beyond the read-out tie-break, s₁ +0.006 ± 0.005) and must be located before stage 1.

## 5. Wiring measures (RD2 §8 (i), review C3)

From the reference keys (field 1 = present edgeset, field 0 = active slots; layout of BIRTHK `review/q4_keys.py`):
- edge marginals p_k(e) per process and per quarter (all rows); between-process cosine overlap ω_ij = Σ p_i p_j / sqrt(Σ p_i² Σ p_j²) (28 pairs), and within-process ω_self between first and second half; ρ_w = mean ω_between(Q4) / mean ω_self.
  - WIRING_MIXED if ρ_w ≥ 0.9; WIRING_CHAIN_SPECIFIC if ρ_w ≤ 0.5; else WIRING_PARTIAL. The trend mean ω_between(Q4) − mean ω_between(Q1) is reported.
- Owners ever toggled (cumulative by quarter), edges present on every row, per process.

## 6. Outcomes and what each means (all register)

| Outcome | Condition | P-96 | P-76 / NGC outer-row sensitivity grid (A18 plug) |
|---|---|---|---|
| **S0-PASS-LIT** | R-LIT passes and census/U passes | TESTED-POSITIVE that the two-part rule can pass with distinct born graphs at L=4; stage 1 (L=6 pilot, RD2 §8) becomes proposable to root, its length set from the stage-0 τ̃ scaled per RD2 §7 | Stage-0 pooled grid (if convexity-admissible) with the 64-batch jackknife errors becomes the candidate for the next freeze (root decision; A2 stays PROVISIONAL until root rules) and is offered now as the NGC outer-row sensitivity grid |
| **S0-PASS-MA** | R-LIT fails only on τ entries, R-MA and census/U pass | Mixed at this length under the multiplicity-aware rule; the literal rule's joint τ leg is the binding constraint (P0-b gives its size). Root decides whether P-96 adopts R-MA or lengthens; stage 1 proposable either way, with the length from τ̃ | As S0-PASS-LIT, but errors are the process jackknife (batch errors withheld per S4) |
| **S0-FAIL-RHAT** | some column Rhat > 1.1 | TESTED-NEGATIVE: distinct born graphs disagree at 16384 sweeps. Read with §5: WIRING_CHAIN_SPECIFIC → frozen-wiring reading; P-96 needs a root decision (a rewiring move, or a graph-ensemble estimand whose error is the between-graph spread; the latter changes the estimand and is a counted approximation) before any L=6 capture. WIRING_PARTIAL/MIXED → slow but moving; the stage-0 τ̃ sets a longer length | Stage-0 grid is a start-balanced, graph-ensemble sensitivity grid only (process-jackknife band), never a replacement; offered for the NGC outer rows if convexity-admissible |
| **S0-FAIL-TAU** | all Rhat ≤ 1.1, R-MA τ leg fails | Consistent but slow; τ̃_max measured; P-96 length rescaled; stage 1 proposable only with the rescaled length | As S0-FAIL-RHAT |
| **S0-FAIL-CENSUS** | census/U fails (Rhat, τ or flat quarters) while the block rule passes | Burn-in or drift not settled; block results carry a drift caveat; P-96 needs longer burn-in | As S0-FAIL-RHAT; the k=0 lapse reading below is not made |
| **INCOMPLETE_n/8** | fewer than 8 processes complete | No rule verdict; the n complete processes are analysed descriptively | Descriptive only |

Additional registered readings (each also registers whatever the outcome):
- **Anisotropy (A18/A19).** START_MEMORY_DETECTED supports A19's start-memory reading for this kernel (A2's anisotropy then rests on start memory plus the read-out tie-break, FORMAL argument in 0036); NO_MEMORY_DETECTED at this kernel's level is consistent with q ≤ 0.016 (A18) and says nothing about V004 or A2 by itself. EXCEEDS_REFERENCE as §4.
- **k = 0 lapse drift (BIRTHK §7 PLAUSIBLE/UNTESTED).** Only if census/U passes in every process: |h_NN(0)| stage-0 vs A2's 3.551. Supported (drift inflated A2's magnitude) if |h_S0| < 3.551 − 2 SE; contradicted if |h_S0| > 3.551 + 2 SE; else INCONCLUSIVE.
- **Frozen owners (RD1).** Owners ever toggled and edges always present per process are reported against the BIRTHK values (22/18 and 385/460); no threshold.

## 7. What is not claimed

- No mixing at L ≥ 6 is implied by any stage-0 outcome (UNTESTED; deciding test stage 1).
- The tail (1/r) is not addressed (A20 FORMAL; UT-1).
- No grid switch happens through this file; any switch is a root decision (A18).
- No NGC3198 observed or target velocity is read by any stage-0 script.
