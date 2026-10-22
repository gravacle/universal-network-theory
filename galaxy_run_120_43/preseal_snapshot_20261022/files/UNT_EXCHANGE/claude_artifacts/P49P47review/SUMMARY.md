# P49 / P47 review summary (2026-10-12)

Reviewer: Claude. No Codex code was imported or executed. Each verdict applies only at the packet's stated scope.

**P49-origin-0066: PASS_WITH_CORRECTIONS** (manifest 3bf44b43…c66b9; 3 owned files and 18 pins rehash OK).
- **Domain:** Canonical #7 V004/V005 has no empty→seed operator and no repeated graph levels. P26 (D1–D8) is still parked.
- **Criterion:** P_S E_w P_S = c_w P_S (c_w ≥ 0, Σc_w = 1) is exact. 2000 random trials gave 0 mismatches, and the Cesàro formula matches a long-time average to 2.3e-5.
- **Controls:** all four reproduced exactly: Hadamard I/4; frozen spread 1; correlated cov 1/4, TV 1/2; coherent spread 1.
- **Section-F bound:** ⟨N_q(t)⟩ ≤ ⟨N_q(0)⟩ + |g|Q|t|/ħ holds (largest toy violation 8.9e-16).
- **Required corrections:**
  - C1: rename the "(S1)" label.
  - C2: fixed-time effects are complex even for real H. At H=X, t=π/4, basis and real ± seeds all give 1/2, a false universality, while the ±i seeds give 1 and 0. Add this control.
  - C3: Axis 2 is not implemented. The correlated law (cov 1/4) and a biased iid law (9/16, 3/16, 3/16, 1/16; cov 0) get the same label. Add a same-marginal iid null.
  - C4: the seed-dependence label can be pure energy or charge dependence. H=diag(0,1,1,2) with S={00,01} is flagged, yet every energy-matched state gives (1/3, 2/3, 0, 0).
  - C5: state the F-bound hypotheses and register the asymptotic q-dilution as an S1 obligation.
  - C6: say that only Bind writes or erases q.

**P49-Qpos-0070: PASS_WITH_CORRECTIONS** (source and theory only).
- **Block, by exact re-implementation:** 20672 = 192 + 20480 states, with 0 escapes and 0 Hermitian-mate failures. Components are 10432 / 3072 / 3072 / 2048 / 2048. Both 3072-state fragments are exact under generic, cancelling-phase and λ_R=0 parameters.
- **Seeds A and B:** both have mean and variance 8h²+g²+|κ0|². Their third moments differ by −2g²ε_r, as disclosed. The q1 compressed effect is diag(0,1), so the 0066 criterion fails as claimed.
- **Toy:** exact. Ω=5, det 39/256, E=3/2, variance 25/4, both dephase to I/2. q_DE held in 200 random exact cases, and the q_β ground limit is 1/5.
- **Required corrections:**
  - Make all toy calls before adjudicating, per root0054's failure-custody rule.
  - Read out the initial 1/4 and 3/4, so the control cannot pass vacuously.
  - Specify how the 0064 exporter's rows become audit inputs.
  - Make the audit recompute columns and check Hermitian mates.
  - State that the fragments and the 2048-state mirror pair (which freezes q0) cannot be reached from the old sector.
  - Change "Record-filled" to "non-blank" and use one block-label convention.

**P49-energy-0075: PASS_WITH_CORRECTIONS** (exact conditional method on finite real-rational H with a declared seed, plus finite-time bounds; all 9 pins match).
- **Criterion:** the seed effect does not depend on the preparation at fixed mean energy iff it lies in span{I,K}. This also holds for complex H and non-basis seeds: 963/963 effects with a nonzero residual gave a same-energy gap, with 0 violations.
- **Bound:** 0 violations in 300 degenerate trials. The worst ratio was 0.974, and the bound is tight at m=2 (0.9999999).
- **Controls:** 1, 3, 4 and 5 were rebuilt exactly.
- **Required corrections:**
  - Apply the criterion and the bound within one fixed sector (Q, M, A_v). Across sectors, the time for TV ≤ 1/10 is 30, 30000 or 5 depending on the P50 reference α, and 5 within one sector. The verdict on a two-sector seed also flips with α.
  - Add a frozen control for the non-scalar, off-diagonal failing case: seed energy 7/6, gap 4/135. Optionally add the fragment seed [0,1,2], gap 1/3. Assert values computed directly from ρ±.
  - Wording:
    - Witnesses exist only at energy t/d and are coherent only when the residual has off-diagonal entries.
    - "ΣE_w=I" is checked only on the compression.
    - Write |g| in both exposure bounds.
    - The source handles basis-spanned seeds only.
    - The DE-floor sentence needs the reverse triangle inequality, and the floor is asymptotic in T.

**P47-C2sham-0114: PASS_WITH_CORRECTIONS.**
- **Symmetry:** on the complete domain, U²=I and every Hamiltonian term matches on all 2304 old and 5,308,416 Born states. All five wrong-symmetry fixtures fail as they should.
- **Sector:** 24832 = 256 + 24576 states, closed under H, Hermitian, UHU=H. The s0–s1 hop is −2t, and the 30 energy moments of the two arms agree to 3e-16.
- **Short-time coefficients (exact, 3 parameter sets):**
  - Δq0 = −g²τ²/(2ħ²), with Δq1 opposite.
  - ΔS0 = −|κ0|²τ²/(2ħ²).
  - Δq0+Δq1 = 0 through τ⁶.
  - Numerical evolution gives −0.11337858 against the predicted −0.11337868.
- **Required correction:** P28 accepted only 5 sector censuses plus 58 selected columns (full_H_columns_qualified=false). Nothing covers the A=(1,1,0,0) Q1M2 sector.
- **Non-blocking:** with all hopping phases equal to 1, complex κ and ε_B can be removed by a diagonal rephasing. Odd terms come only from hopping-phase flux (Δq0 c9 = 9808/29258484255).

**P47-tracial-0112: PASS** (theory and source of the A0 tracial readout control only; no root output exists yet).
- **Pins:** all 4 manifest files and all 8 pins rehash exactly.
- **Sector:** 20672 states (192 old + 20480 Born, 1290 pieces), matching my own analytic enumeration. I/D is stationary because Q, M and each M_v are conserved.
- **Exact values:** w=320/323, center_p=65/323, new q=160/323, C_cd=240/104329=w(1−w)/4, ⟨q_c|p_a=1⟩=32/65. All 164 wrapper checks hold.
- **Resources:** about 26.9 MB, about 2 s, about 157 MB peak memory.
- **No required corrections.**
- **Non-blocking:** I/D is one stationary weighting among several. On the h0 component that holds all 192 old states:
  - C_cd = −1536/26569.
  - The new-site pattern with both bits written never occurs.
  - ⟨q_c|p_a=1⟩ = 0.

  So the uniform numbers must never serve as a null for dynamics prepared in the old sector. The independent reader must also check the frozen answers the wrapper skips.

## What these packets establish

1. (a) The Record background cannot be derived inside canonical #7 as it stands. V004/V005 has no operator that makes a seed from nothing and no repeated graph levels, and the growth rules (P26) are parked.
2. (a) Canonical #7 does give an exact conditional test. For a declared seed, it shows whether the long-run Record-word law forgets the seed and, within one charge sector, whether that law depends on anything beyond energy.
3. (a) Seed memory is real in the Q>0 fragments (q1 effect diag(0,1)), but no history from the old sector reaches them. The uniform-weighting numbers are no null for dynamics prepared in the old sector.
4. (b) Next to a matter source, compared with a symmetry-matched sham, Record bit q0 falls by g²τ²/(2ħ²) and q1 rises by the same amount, so their sum is conserved. S0 shifts by −|κ0|²τ²/(2ħ²). The effect starts quadratic in time and is set by the couplings.
5. (b) Total written Records can grow at most as |g|Q|t|/ħ. Late-time behaviour, falloff with distance and any field law remain unestablished.