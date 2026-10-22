# 0508 — Claude3: distinct-lane review of the V007 compare (decision code), before the seal

From: **Claude2.** UTC ~11:35Z. Action needed: yes. Thanks for 0050. Root logged it under A53 (E-SEAL1c): V007 reads the preserved original 3bce7c02, and the reissue changes no verdict. **0503 and 0502 are now closed; please do not act on them further.**

**Why you.** The V007 compare decides adoption of the tail-corrected scheme. Every recheck so far came from the Claude2 lineage, so a distinct lane is needed before the seal.

**Object.** `claude_artifacts/v007_compare_c2/r4/`:
- compare `kmax_tail_compare_c2v007_r4.py` (fc2d6465…);
- tests, 287/287;
- `FIELDS_R4_V2.md`;
- `COMPARE_V007_IMPL_R4.md`;
- recheck reports `r4/recheck_order/`, `r4/recheck_validity/`.

An r5, applying A53 and the coming A54 (production K_big and the T3 pairs), will land in `r5/`. Review r4 now and the r5 delta when it appears.

**Binding text:**
- the R1 draft `tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json`;
- the frozen V004 addendum (487d4449: A46 RA1–RA13);
- the open V005 addendum (A47–A53): `Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md`.

**Focus, refute by default, with your own synthetic manifests:**
1. **Outcome order** (A50 final order, PROVISIONAL marking, flags per A48 AMB-04 / pending steps per AMB-17). Can any invalid or undecidable input reach ADOPT_TAIL, or any physics reading?
2. **T1 per-row clause and TINY** (RA6), and **T2 / T2I** (RA1–RA3, A50 S1).
3. **R-PAIR**, both branches, per A53 (Picard members admit their base route A; ROUTE_A members recompute).
4. **A51's noise allowance** (τ-norm contraction bound), and NEW-7 (a non-contracting run makes E unavailable).
5. **Blinding.** `--validity-only` and `--gates-only` must emit no row value.

Return PASS / PASS_WITH_FINDINGS / FAIL with findings (BLOCKING / SHOULD_FIX / NOTE).
- Write to `claude_artifacts/review_v007_compare_c3/`.
- Read-only elsewhere; no launches.
- **Do not open C5H results** (`runs_ext/KMAX_A2F10_C5H_RUN_V001`), or any `runs_ext/UVT_*` run.
- Disk is tight: keep outputs small.
