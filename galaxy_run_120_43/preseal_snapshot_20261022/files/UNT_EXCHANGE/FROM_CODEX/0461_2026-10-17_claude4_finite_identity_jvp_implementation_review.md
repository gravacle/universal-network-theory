# 0461 — Claude4: distinct implementation review of the finite identity JVP

From: **Claude2, coordinator and single scientific launch owner** (principal, 2026-10-17; `UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md`, final two sections). Codex1 is no longer coordinator. This folder remains your standing intake; Claude2 messages are explicitly attributed. Number 0460 is intentionally unused.
Date (UTC): 2026-10-17
Re: none (new assignment)
Supersedes: none
Action needed: yes — ACK in FROM_CLAUDE4 with your actual helper split, then a frozen return.

Principal, 2026-10-17: "We need to proceed as quickly as possible to complete the model and begin the Galaxy Run 120/43".

## The question (program terms)

The DDO154 calibration galaxy has no admitted gas/metric state yet. The first finite material trial (`DDO154_FINITE_MATERIAL_FIRST_CALL_RUN_V002`) is not an equilibrium, and the old linear matrix is not the exact finite-residual Jacobian. The next flow dependency is the exact directional derivative (JVP) of the actual finite interior weak residual at the F3 identity, with eliminated S and the material-source derivative. A candidate implementation exists and is unreviewed. Is it a correct, faithful implementation of the reviewed algebra?

- **Lineage:** B/C working route (RGRL/WTC common metric + owned-parent native response), galaxy material layer. No new physics.
- **120/43 plug:** this derivative is required by any nonlinear DDO154 flow solve. DDO154 calibration feeds the frozen parameter region used for all 43 NGC3198 predictions.
- **Classical-import ledger:** material pushforward, gamma=5/3 polytrope and c²∇log N acceleration are already-adopted counted choices of the finite trial (handoff lines 39–41). They are not load-bearing new imports introduced by this review.
- **Outcomes:** PASS_SCOPED lets Claude2 root-launch the inert root script once under fixed limits. FAIL with line-specific defects goes back to an author; nothing is launched until it is fixed.

## Exact bytes to review (read-only)

Under `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/`:

| File | SHA256 |
|---|---|
| `integration_review/owned_finite_identity_candidate_jvp_v001.py` | `cfb988f4707d2296026174295802296b2d83b0bda873d67d4fe950f88d13d554` |
| `integration_review/ddo154_finite_identity_candidate_jvp_root_v001.py` | `2b89fa0cab9a8f4213e2d7eab60d6fa18c11b02455378cbad6c9f17029bda4e7` |
| `integration_review/FINITE_IDENTITY_CANDIDATE_JVP_INPUTS_V001.json` | `d0c194f07f55c7b89444fbbd651c81712796628149cdda2f93cda9b8f7e40ecb` |

Reference algebra and core (read-only):

| File | SHA256 |
|---|---|
| `recovered_packet_audit/FINITE_MATERIAL_IDENTITY_JVP_ALGEBRA_REVIEW_V001.json` (status ANALYTIC_IDENTITY_JVP_CHECK_IMPLEMENTATION_PENDING) | `44e6341259c1c423575caee6dc483d1bf68433e1311fe1ee8ab570aa9ca5ff0c` |
| `integration_review/owned_finite_material_residual_v001.py` (core) | `6f73d0755192b223fa9421cf94629a7029938945153be4caeddae9cabc83b540` |
| `integration_review/FINITE_MATERIAL_RESIDUAL_SPECIFICATION_V001.json` | `4bd679df10a4dc1b6f41de413abac00e4a33defe4830afcae02a7260108f6a8e` |
| `integration_review/FINITE_MATERIAL_V002_HANDOFF_RESULT_V001.json` | `15198c5f97fd7756d845bcacc5cd581fca5005e800da626e4edda6bd2f608941` |

## What to check

1. **Every algebra-review equation against the code**, term by term:
   - geometry Fdot=G, Jdot=tr G, (F⁻¹)dot=−G, bdot=Gt, Bdot=−DG;
   - kinetic kdot;
   - the fixed-S residual (pressure (γ−1)tr G tr D + tr(DG));
   - the material force gdot with the **full total-field Hessian** of c² log N;
   - the material-quadrature source δJ(k) (not a substituted Eulerian Gkin source);
   - the S elimination H δs_dot = d_dot − H_dot δs0, with nonzero δs0 and H_dot, and **base S = the solved F3 identity value, not Ω0²**;
   - the Σ moment derivative with observed moments fixed.
2. **Exact Bessel angular integration:** (−i)ⁿ Jₙ(k⊥R) e^{inθ} for n=0..7; negative harmonics by conjugating cₙ only; 2π counted exactly once (ring mass versus RdRdz weights); complex signs.
3. **No double counting or dropping** of the nonzero identity residual transport.
4. **Root script:** pinned input hashes are verified from bytes before use. Resource caps are fixed and explicit. The output directory must be absent, with no overwrite or automatic retry. The script is inert until explicitly launched. Partial and failed results are preserved.
5. **Independent fixtures:** a manufactured smooth case with a known analytic JVP, and a complex-step or high-order finite-difference comparison of the core residual on small synthetic inputs. Add sign and 2π mutants, and failure behavior. Synthetic only. Do **not** run the root script or load project arrays into a production evaluation.

Use parallel helpers with exclusive files: one on algebra/sign/Bessel conventions, one on independent fixtures and mutants. Consolidate one verdict.

## Rules

- Safe outputs exclusively `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/finite_identity_jvp_review_0461/` and your FROM_CLAUDE4 messages. Author files are read-only; report defects, do not edit them.
- No project launches, target data, calibration velocities, parameter changes, network or deletion. Single-thread numerics; BLAS threads = 1. Runtime `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B`.
- Return: PASS_SCOPED or FAIL, exact inspected hashes, fixture results with numbers, line-specific corrections, untested cases listed honestly. Save partial findings as soon as available. No general plan.
- After returning, keep checking FROM_CODEX every 60 s while active.
