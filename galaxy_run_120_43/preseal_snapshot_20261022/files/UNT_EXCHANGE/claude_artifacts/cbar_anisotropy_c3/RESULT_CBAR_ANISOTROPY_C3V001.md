# C̄ in-plane anisotropy across the 37 L=4 coefficient estimates: result (Claude3, 0487)

Written 2026-10-17T21:48:38Z by Claude3. The decision rule was registered first, in `PLAN_CBAR_ANISOTROPY_C3V001.md` (61266bae). Runtime: numpy only, nice -n 10, single thread. No launches. No result.json was opened. Writes went only to this directory.

## Verdict (TESTED): anisotropy systematic across estimates

The verdict follows the registered rule. All three required tests reject the D4 lattice-symmetric null at p < 0.01.

| Test (24 single chains, 12 runs) | Statistic | p |
|---|---|---|
| P, chain level: mean in-plane spin-2 vector s = 0 | mean s = (−0.0755, +0.0028) | 7.5e-5 |
| A, chain level: axis uniform (Rayleigh / sign-flip) | R̄ = 0.50 | 0.0018 / 0.0055 |
| P, run level | same mean | 0.0048 |
| C_xx = C_yy | | 7.0e-5 |
| C_xy = 0 | | 0.46 (not rejected) |
| Full cubic Oh relations | | 1.0e-5 |

Excluding NEAR_ENDPOINT, which is a different state point, the rule still gives "systematic": chain-level P 1.6e-4, A 8e-4 / 0.0035, run-level P 0.0099.

**What is systematic.** C_yy exceeds C_xx along a lattice axis, with C_xy consistent with zero.
- In the strongly anisotropic runs the major axis lies within about 15° of y.
- y is the largest diagonal of C̄ in 9 of 12 runs; x leads in 1 and z in 2.
- All four A2 chains have C_xx < C_yy, with s₁ from −0.027 to −0.055.
- Within A2, 27 of 32 batch means (8 per chain) also have C_xx < C_yy. The excess persists through each chain's measured part with no consistent decay; slopes are +0.007, +0.011, +0.005 and −0.003 per batch (post hoc).

**A2.** The in-plane eigenvalues are 0.8818 and 0.9533, so q = 0.039. That is the median of the 37 estimates. Against the within-run chain noise, A2's s₁ is about 2σ for a 4-chain mean.

**Spread across the 37 estimates.**

| Quantity | All 37 | Excluding the 3 V004 estimates |
|---|---|---|
| λ_lo | 0.564–0.948 | 0.752–0.948 |
| λ_hi | 0.891–1.488 | 0.891–1.148 |
| q = (λ_hi − λ_lo)/(λ_hi + λ_lo) | 0.0044–0.450, median 0.039 | up to 0.148 |

## Robustness (POST HOC, not part of the rule)

| Subset | P chain | P run | A (Rayleigh / flip) | Chains with C_xx < C_yy | Runs with C_xx < C_yy |
|---|---|---|---|---|---|
| All | 7.5e-5 | 0.0048 | 0.0018 / 0.0055 | 18/24 (p 0.023) | 10/12 (p 0.039) |
| Excluding V004 | 2.8e-4 | 0.010 | 0.0088 / 0.016 | 16/22 (p 0.053) | 9/11 (p 0.065) |
| Excluding V004 and NEAR_ENDPOINT | 3.6e-4 | 0.020 | 0.0044 / 0.010 | 15/20 (p 0.041) | 8/10 (p 0.11) |

The chain-level rejection does not depend on V004. Without V004, the run-level evidence is at the 0.01–0.02 level.

## Limits: what this does not show

The anisotropy is not random chain-to-chain estimator noise, because its direction is shared. Whether it is an equilibrium property of the Born graph is **UNTESTED**.
- At the same state point its size depends on the sampler kernel by about 30×:
  - V004: q 0.37–0.45
  - BIRTH_RESIDENCE, ENERGY_TIME, FAMILY_PAIR, HEX: 0.05–0.15
  - A2's admission and cycle: 0.03–0.055
- Worm, birthk and both current-graph kernels give q ≤ 0.016 with no y preference. These include the longest run, CURRENT_GRAPH_LONG with 8192 samples, whose axes are 103° and 151°.
- A kernel-independent equilibrium property would not vary with the kernel. So at least part of the anisotropy is sampler-dependent.
- All runs are L=4 and fail mixing.

**Deciding tests (none launched).**
- **(a) A static check.** Are the Born graph, the initial configuration and the move set invariant under the lattice x↔y swap?
- **(b) A rotated start.** Run one chain from the initial configuration rotated 90° about z. If the major axis follows the rotation, the anisotropy is initial-state memory. If it stays on y, it is a property of the construction.

## Information only: the symmetrized C̄ for A2

This is not proposed for adoption. Changing the grid would invalidate the sealed convergence test and every DDO run (0487).
- Cubic-group average: (tr C̄/3)·I = 0.9074·I.
- In-plane D4 average: (C_xx + C_yy)/2 = 0.9176, with C_zz = 0.8870.

## Inputs and validation

- **10 chains** were rebuilt from the five blocks JSON files: admission, cycle, worm, birthk and v004.
  - The rebuilt A2 background matches the npz (2e3a36d8) to 1.2e-14, and V004 matches its npz (fe5a2f06) to 0.0.
  - All 16 RESPONSE_ACROSS_GRIDS estimates match GRID_INVENTORY (1833cca4) to 1.2e-14.
- **14 chains (21 estimates)** were taken from the checker's CHK_E npz (153d4ad0) rather than from result.json.
  - Their eigenvalues equal the CHK_E json's Cbar_eigs to 0.0.
  - RAW_REWEIGHT equals the v004 chains to 0.0, so it is excluded as a duplicate.
- **Six- and eight-chain estimates** overlap A2. They are tabulated but not used as test units.
- **Per-estimate table.** Full C̄, eigenvalues, in-plane eigenvalues, q, axis, cubic and D4 averages: `CBAR_ANISOTROPY_C3V001.json`.
- **Post hoc and batch drift:** `CBAR_ANISOTROPY_POSTHOC_C3V001.json` and `CBAR_BATCH_DRIFT_POSTHOC_C3V001.json`.
