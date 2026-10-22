# Root decisions A1 and A2 — 2026-10-17 (Claude2, coordinator and launch owner)

Authority:
- the principal's delegation of "ALL reasonable theory decisions" through completion of the galaxy run (CURRENT_INSTRUCTIONS);
- "proceed as quickly as possible… begin the Galaxy Run 120/43" (2026-10-17).

Evidence is in `CRITICAL_PATH_EVALUATION_2026-10-17_V001/` (this folder):

| File | SHA256 | Review |
|---|---|---|
| `sampler_eval/SAMPLER_EVALUATION_V001.json` | `c2bcd088…` | `sampler_eval/review/REVIEW_V001.md` (`69f7f174…`), PASS_WITH_CORRECTIONS |
| `forward_route/FORWARD_ROUTE_ASSESSMENT_V001.json` | `b018cdfb…` | `forward_route/review/REVIEW_V001.md` (`f714bf23…`), PASS_WITH_CORRECTIONS |

Both reviewers' corrections are binding and supersede the original text where they conflict.

## A2 — response coefficients fed to the galaxy kernel

**Decision:** replace the V004 provisional grid with the 4-chain pooled point as the best-available provisional coefficients.
- V004 grid: `PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz`, `fe5a2f06…`.
- 4-chain pooled point: `CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz`, `2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7`. It is built from the admission and current-graph cycle captures and was independently reproduced by the reviewer to 1.55e-14.

**Why:**
- V004 came from 64+256 sweeps and retains the seed's polarisation:
  - background M diagonal (0.613, 1.462, 0.630) against (0.879, 0.937, 0.909);
  - k=0 S11 −6.47 against −0.18;
  - k=0 R response about −1e-4 against 0.025–0.094.
- Unbiased distances: V004 against the cycle run is 1.418; admission against cycle is 0.752.

**Status:** PROVISIONAL.
- Mixing failed in every run, the Birth census is not stationary, and errors are withheld.
- The V004-versus-pooled difference and the single-chain spreads are carried as **sensitivity, not error bars**.
- This choice does not accept the coefficients as physical (`coefficients_accepted_for_galaxy` stays false).

**Next sampling remedy (D2):** an occupancy-guided long alternating-loop whole-path move, run as a pilot that saves the canonical reference key on every durable row.
- Its deciding test is the same all-36 and background mixing criterion, plus stationarity of the Birth census and U.
- A quasi-conserved sector remains UNTESTED. The exactly conserved sector is excluded (FORMAL-RESULT).

## A1 — galaxy state used for calibration and prediction

**Decision:** use the stationary axisymmetric (m=0) member as the counted working state for DDO154 calibration and NGC3198 prediction. This is the route-B chain: free-surface polytropic columns with observed Σ, pressure-balanced m=0 rotation and fixed axisymmetric stars. It is driven by the m=0 projection of the **unmodified** anisotropic kernel.

**Counted assumptions** (each carried with its sensitivity):
1. **A1-state.** Stationary circular streaming and m=0 equilibrium; CI:75's averaged-source permission does not supply these, so they are counted here.
2. **A1-response.** The kernel is unmodified; only its m=0 projection drives the state. The stored m≥1 residual is kept.
3. **A1-orientation.** Disk axis = chart z, a counted choice with no orientation law. The tilt family is UNTESTED; its deciding test is to rerun with the disk axis along each C̄ principal axis and along [111].
4. **A1-m≥1.** The m≥1 forcing is carried as a stated sensitivity.
   - Its gas response is **not** assumed small: the evaluated linear m=1..6 response was non-perturbative (19.26% folded mass) and the reviewer refuted the ε² bound.
   - That response is UNTESTED with artifact-free forcing and the A2 coefficients. Its deciding test is D3.
   - Part of the anisotropy is attributable to the failed-mixing V004 point, which A2 replaces.
5. **A1-numerics.** The m=4/m=8 components from Cartesian cube corners and 8-azimuth columns are numerical and are not physical forcing.
   - Truncation shape and k_max convergence must be settled **before** calibration: the cube-to-sphere change moves the inner m=0 force by up to 18.8%.
   - Deciding test: extend k_max to 3–4 /kpc at a fixed source under the reviewed route-B driver, compare the 12 rows, and adopt the converged truncation.

**Not adopted:**
- an isotropic or symmetrized kernel;
- any orientation-averaged physics;
- any claim that the m≥1 effect is negligible.

**Reversal condition:** if D3 shows that the artifact-free m≥1 response materially changes the m=0 rows, A1 is revised and the non-axisymmetric flow becomes critical path.
