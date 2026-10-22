# CHECK: refute-by-default check of GATE_V001 (stage-0 grid convexity gate)

2026-10-18. Read-only on every input. Nothing was launched. Written only under `stage0_grid_gate_c2/check/`. Neither `runs_ext/KMAX_A2F10_C5H_RUN_V001` nor any NGC or target file was opened.

- Script: `check/c02_refute_check.py` (sha256 `853558f0190f2cb8db761cd9367d2100be9c8338dc303fecb4d9d8734050c5c3`).
- Output: `check/C02_OUTPUT_V001.json` (sha256 `7b336a3ca0e0e3d3c6a75875bef143969b98199c7aa46a57cc7f23c1ff78beb5`).
- Python: the codex runtime, run with `-I -B`.
- **Independence.** The script does not import g01, c01, `stage0_lib_v001` or `stage0_analysis_v003`. It rebuilds every per-(process, batch) block sum from the 8 committed captures (8 × 1024 block files, 131072 rows). cg02 (fcb796a9) is imported unmodified for one purpose only: to apply the A2 admission code to the candidate file.
- **Pins.** Every pinned input matches its hash from bytes. The 6 hashes in `HASHES.txt` verify (`shasum -c`), and so do the 8 `result.json` hashes bound in the analysis JSON.

## VERDICT: GATE_V001 CONFIRMED (no refuting finding)

**CONVEXITY_ADMISSIBLE: TESTED-POSITIVE.** I re-ran the gate from the raw captures. It now covers all 81 members and both levels:
- Members: the pooled grid, 8 per-process, 8 leave-one-process-out and 64 leave-one-batch-out.
- Levels: all 36 blocks (the 28 pair blocks included) and all 64 nodes.

The return's first UNTESTED item, the block gate on the 28 pair blocks run independently of analysis v003, is now **TESTED-POSITIVE**.

## 1. Gate re-run

| Member set | Members violating | λ_min d2logZ (min) | lapse Schur (min) | λ_max h (max) | Γ_nn (min) |
|---|---|---|---|---|---|
| pooled | 0/1 | 0.2538 | 25.93 | −5.766e-3 | 0.870 |
| per process | 0/8 | 0.1628 | 15.00 | −3.857e-3 | 0.535 |
| leave-one-process-out | 0/8 | 0.2479 | 25.08 | −5.138e-3 | 0.841 |
| leave-one-batch-out | 0/64 | 0.2476 | 25.46 | −5.529e-3 | 0.857 |
| **all** | **0/81** | 0.1628 | 15.00 | −3.857e-3 | 0.535 |

- **Counts.** 0 of 2916 block tests violate, and 0 of 5184 node tests violate. No Γ_nn is negative. No solve was singular. Every block estimate is exactly symmetric.
- **Agreement with analysis v003.** At the pooled point and in every process, the deviation is 0.0 for all four quantities: λ_min d2logZ, lapse Schur, λ_max h and Γ_nn.
- **cg02 on the candidate file.** I applied `cg02.grid_gate`/`summarize_grid` to `source_hessian_grid` and to each `single_chain_grid_stage0_p0..p7`:
  - every grid has 0/64 violating nodes;
  - F_jj is invertible at 64/64 nodes;
  - the Hermiticity residual is 0;
  - the pooled grid gives λ_max h = −5.766e-3 and min Γ_nn = 0.870;
  - the A2 anchor in the same call gives −3.2537e-3, the value in `cg02_gate_v001.json`.
- **Scope of GATE_V001's node test.** It covered 17 members. The prereg (§3) also names the leave-one-batch-out replicates, and for those GATE_V001 relied on the analysis's `loo_batch_violating = 0`. That quoted count is now confirmed independently at both levels. Coverage is no longer a gap.

## 2. Grid extraction vs the prereg (§3)

The prereg defines the pooled grid as follows:
- the plug-in H = Cov + ⟨T⟩ over all 8 × 16384 rows;
- self-conjugate nodes h = F/64;
- pair nodes h = [(cc+ss)/2 + i(cs−sc)/2]/32, with the partner node set to the conjugate;
- the band is the leave-one-process-out jackknife, SE = sqrt(7/8 Σ|g₋ᵢ − ḡ|²).

I rebuilt the grid from that text, using my own code and the captures.

**Rebuilt vs saved: max |Δ| = 0.0 (bitwise) for each object below.**

| Rebuilt object | Compared with |
|---|---|
| pooled grid | saved `stage0_pooled_grid` |
| pooled grid | candidate `source_hessian_grid` |
| 8 per-process grids | saved grids |
| 8 per-process grids | candidate `single_chain_grid_stage0_p*` |
| 8 leave-one-process-out grids | saved grids |
| process-jackknife SE | saved |
| batch-jackknife SE | saved |

The inputs behind the extraction agree:
- **Block metadata.** The metadata from the 8 `result.json` files is identical across processes. It is also identical to A2's `cycle_meta.json`: same k, profiles, contact offsets and entries. So the extraction convention is the same as A2's.
- **Profiles.** The profiles are exactly cos and +sin of 2π k·x/L, with deviation 0.0. For a pair profile, Σcos² = 32, which accounts for the /32.
- **Mandel factor.** The factor √2 is applied once, to fields 7–9, as the metadata states.
- **Pooled estimator.** The prereg's "= mean within-process H + between-process covariance of means" identity holds: at k=0 the residual is 8.5e-14.

## 3. k=0 numbers vs the analysis JSON

The quantity is h_NN(0) = −(Var S_N(0) + ⟨T_NN(0)⟩)/64, computed from the raw rows.

| Quantity | Recomputed | Analysis JSON | Deviation |
|---|---|---|---|
| pooled | −1.898912 | −1.898912 | 0.0 |
| per process | −2.2006 … −1.3772 | same 8 values | 0.0 |
| process-jackknife SE | 0.105862 | 0.105862 | 0.0 |
| ρ = Var S_N / |⟨T_NN⟩| | 18.858 | 18.858 | 0.0 |

- The grid entry G[0,0,0][0,0] equals the scalar to 3.2e-12, with imaginary part 0. The saved band entry is 0.105862.
- **A2.** A2's entry is −3.5510, so the prereg's 3.551 is that entry rounded. A2's single chains give −2.373, −5.201, −4.167 and −1.764.
- **Comparison.** |A2| − |S0| = 1.6521, which is 15.61 SE. The ratio S0/A2 is 0.5348.
- **Reading.** The SUPPORTED threshold is 3.551 − 2 SE = 3.339, and |h_S0| = 1.899 is below it. So the reading is **SUPPORTED**, matching the JSON.
- **The sealed gate on that reading holds.** §6 makes the reading only if census/U passes in every process:
  - The sealed census/U leg passed for both series.
  - FQ-WC fails only for `time_mean_active_slots` in process 3, so DRIFT_FLAG = true and `addendum_drift_checked = false`.
  - GATE_V001's wording ("SUPPORTED, not drift-checked") is correct.
- **Grid vs A2.** The global relative distance is 0.4771 and the k=0 node distance is 0.4828. 6400/6400 entries have a positive band. 93.625% of them differ by more than 2 SE, with a median of 8.66 SE. These match GATE_V001.

## 4. Candidate file

- **Schema.** The 4 core keys match A2's in shape and dtype. A2 has no other keys besides `single_chain_grid_*`.
- **Grid.** The partner-conjugacy residual is 0 and the node-Hermiticity residual is 0.
- **Background.** I recomputed μ, M and C from the 8 processes' background rows: the equal-weight mean of the process means, divided by 64, in the label order of the metadata.
  - They match the candidate file with deviation 0.0, and C̄ matches the analysis's pooled C̄ with deviation 0.0.
  - C = M − μμᵀ holds exactly. C is SPD, with eigenvalues 0.90016, 0.90071 and 0.90291.

## 5. Findings (none refutes the verdict)

- **R-1 (status upgrade).** The block gate on the 28 pair blocks is now TESTED-POSITIVE: 0/81 members, run from the captures without the analysis code. The first UNTESTED item in GATE_V001 is closed.
- **R-2 (wording, low).** "In every jackknife member the prereg names" was literally true only by combining the re-run nodes (17 members) with the analysis's quoted leave-one-batch-out count. It is now true by re-run alone (81 members, §1).
- **R-3 (reading caveat, information only; changes no sealed reading).** The stage-0 grid is 0.451 from the same-kernel BIRTHK pooled grid (k=0 node 0.422). That is about the same as its distance from A2 (0.477). Single processes sit 0.15–0.18 from the stage-0 pooled grid.
  - The size of the stage-0 vs A2 difference is therefore typical of between-ensemble differences on this kernel. It is not specific to k=0.
  - The sealed SUPPORTED reading registers as written. Its causal gloss, "drift inflated A2's magnitude", is not isolated by this comparison.
  - **UNTESTED.** Deciding test: the k=0 comparison against an A2-protocol re-capture with FQ-WC passing in every unit.
- **Kept from GATE_V001 as UNTESTED, with deciding tests unchanged:**
  - whether 8 born graphs give an adequate band for the graph-ensemble estimand;
  - whether the k=0 reading holds under drift control.
- **Status unchanged.** The candidate file is a start-balanced, graph-ensemble sensitivity grid only: sealed S0-FAIL-RHAT with WIRING_CHAIN_SPECIFIC. It is never a replacement for A2. Any use is a root decision (A18). The gate is a necessary condition and does not rank the grid against A2.
