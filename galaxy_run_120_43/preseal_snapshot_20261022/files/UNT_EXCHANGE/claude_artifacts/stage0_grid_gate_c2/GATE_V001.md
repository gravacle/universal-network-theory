# GATE_V001: estimator-convexity gate on the stage-0 grid

Claude2, 2026-10-18. Read-only. Nothing was launched. The gate was evaluated on saved grids only, and nothing was repaired. Every number below comes from `GATE_V001.json`, written by `scripts/g01_stage0_grid_gate.py`. Hashes are in `HASHES.txt`.

## Verdict

**CONVEXITY_ADMISSIBLE: TESTED-POSITIVE.** The registered stage-0 grid passes the CONVEXITY_GATE_V001 admission rule at the pooled point and in every jackknife member the prereg names.

- **Node test, re-run here.** This is `cg02_gate.grid_gate` (fcb796a9), the code that admitted A2, imported unmodified.
  - It was run on 17 saved grids: the pooled grid, the 8 per-process grids and the 8 leave-one-process-out grids.
  - **0 of 17 members violate, and 0 of 1088 nodes violate.**
  - Max λ_max(h) over all members is −3.86e-3. On the pooled grid it is −5.77e-3; A2's is −3.25e-3.
  - Min Γ_nn over all members is 0.535. On the pooled grid it is 0.870; A2's is 0.557.
  - At every node of every member, F_jj is invertible and Γ_nn > 0.
- **Anchor.** The same call on the A2 npz reproduces the A2 admission's saved-grid summaries exactly, for the pooled grid and its 4 single chains (`cg02_gate_v001.json`).
- **Block test.** Quoted from the analysis. It was not re-run here, because pair blocks cannot be recovered from h.
  - STAGE0_ANALYSIS_V003 (b7 transcription) reports:
    - pooled: 0/36 blocks violate, min λ(d2logZ) 0.254, min lapse Schur 25.9 (A2: 0.0645 and 10.97);
    - processes: 0/8 violate, min lapse Schur 15.0–20.8;
    - leave-one-process-out replicates: 0/8;
    - leave-one-batch-out replicates: 0/64.
  - The 8 self-conjugate blocks were rebuilt exactly from the grid (H = −64h): 0 violations across all 17 members, min lapse Schur 34.2.
- **Independent check.** `check/c01` does not import cg02. It gives the same counts and extremes, with deviation 0.0, and returns PASS.
- **Scope of the pass (from CONVEXITY_GATE_V001 §3).** The gate is a necessary condition only. It does not validate the grid and does not rank it against A2.

## k=0 entry and band vs A2

| | h_NN(0) | band |
|---|---|---|
| Stage-0 pooled (8 processes, 131072 rows) | **−1.899** | ±0.106 (process jackknife) |
| Stage-0 per process | −2.201 … −1.377 | |
| A2 pooled | **−3.551** | no band (the A2 file carries no jackknife) |
| A2 single chains | −5.201 … −1.764 | |

- The difference is |A2| − |S0| = 1.652, which is 15.6 stage-0 SE. The ratio S0/A2 is 0.535.
- Under the sealed rule (|h_S0| < 3.551 − 2 SE) the reading is **SUPPORTED**. This matches the analysis.
- The reading is **not drift-checked**:
  - ADDENDUM_V001 A3: FQ-WC fails in process 3, series `time_mean_active_slots`, so DRIFT_FLAG = true.
  - The sealed census/U leg passed.
- The A2 single-chain range (−5.20 to −1.76) contains the stage-0 value. The rule tests against A2's point estimate only.
- Whole k=0 node vs A2: relative Frobenius distance 0.483.
- Whole grid vs A2:
  - global distance 0.477;
  - 93.6% of the 6400 entries differ from A2 by more than 2 band-SE, with a median of 8.7 SE.
  - So the stage-0 grid and A2 are not compatible within the stage-0 process band.

## Coefficient-file format

**Yes. The grid can be expressed in the 2e3a36d8 schema.**

- **Core keys.** All 4 core keys have the same shape and dtype as A2:
  - `source_hessian_grid` (4,4,4,10,10) c128, `background_mu` (3), `background_M` (3,3), `background_C` (3,3).
  - The consumer `ddo_body_source_offset_root_v003` (c5faed57) reads `source_hessian_grid`, `background_mu` and `background_C` (from its source text; it was not run).
- **Extra keys.** The file adds `single_chain_grid_stage0_p0…p7`, following A2's `single_chain_grid_*` pattern.
- **Grid.** `source_hessian_grid` is bit-identical to the saved `stage0_pooled_grid`. Partner-conjugacy residual is 0, and every value is finite.
- **Background.** Computed with A2's own `moments()` from the 8 processes' committed-capture background rows.
  - It equals the analysis's pooled C̄ and its per-process C̄ to 0.0.
  - C is SPD, with eigenvalues 0.9002, 0.9007, 0.9029 (A2: 0.882, 0.887, 0.954).
- **Target-free.** No galaxy or target file was read.
- **File.** `candidate/STAGE0_POOLED8_CANDIDATE_GRID_V001.npz`, sha256 `bdb9016c97685d72de8fb93d43cb6ce5baff42b64e59f99af14fb310c8317ca5`.
- **Status.** The file is **not registered and not used.** The sealed outcome is S0-FAIL-RHAT with WIRING_CHAIN_SPECIFIC. Under that row, this is a start-balanced, graph-ensemble sensitivity grid only, with the process-jackknife band. It is never a replacement for A2. It is offered for the NGC outer rows, now convexity-admissible. Any use is a root decision (A18).

## UNTESTED, each with its deciding test

- **Block gate on the 28 pair blocks, independently of analysis v003.** Deciding test: re-run cg02's `block_gate` on per-(process, batch) sums from the 8 captures.
- **Whether the band covers the graph-ensemble estimand.** The process jackknife has only 8 born graphs, and wiring is chain-specific. Deciding test: more born graphs, or a rewiring move (P-96 root decision).
- **Whether the k=0 drift reading survives drift control.** Deciding test: the reading with FQ-WC passing in every unit.
