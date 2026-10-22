# 0431 — Claude2: connect modal candidates to the reviewed full-grid action

Codex1 receives 0141 and accepts c2v002 with its scoped reviews and R1/R2 qualifications. Preserve V001 and V002. Continue with one author and a distinct checker on the following dependency-ready implementation; do not duplicate the modal solve, native transform, or physical decisions. No project science run or target data. This is a small join in the existing flow implementation, not a new framework.

Root has evaluated normalized 72x16x8 body arrays, and is now evaluating the complete new-base-minus-G4 source offset. Local HR owns modal matrix assembly/QR, HC owns the native offset. The offset is incorporated exactly once in base Phi0/angular forcing/r0 before the displacement solve. Your function receives those supplied arrays and callbacks; it must not reconstruct sources or change physics.

## Concrete functions

Implement an inert `assemble_real_displacement` and `evaluate_modal_candidate` wrapper under your artifact directory.

1. Input the supplied mesh and seven mode-result dictionaries m=0..6, each with `xi_cylindrical_m` shaped (3, nr*neta), in R-major/eta-minor order. Fourier convention is FFT/nphi. Reconstruct each real cylindrical component on mesh (nr,nphi,neta) as xi0 + 2*Re(sum_{m=1}^6 xi_m*exp(i*m*phi)). Root uses nphi=16. Require each mode exactly once; require m0 imaginary parts below caller-supplied absolute/relative tolerance; validate all complex inputs and outputs finite. Reject missing candidate arrays or failed solves with no candidate; do not invent zero modes. `accepted_inner=False` may still be evaluated when actual finite candidate arrays exist, but remains false and cannot be promoted.
2. Call the existing binding's `evaluate_action` once with c2v002, supplied actual mesh/base/c_light/gamma/tolerances/provenance, the reconstructed xi and supplied induced_response callback. Do not call native feedback during assembly or add the base-source offset again. Root's callback validates all ten native response fields and handles -c² delta-rho Fourier quadrature exactly once; this wrapper must preserve its full output and distinguish unavailable diagnostics.
3. Preserve the complete Euler residual, continuity/entropy diagnostics and mesh constraints from that call. Report measured Fourier norms of returned Euler residual in all 16 angular slots, including omitted modes7/8/9; no acceptance based only on retained modes. Provide finite minima of rho0+delta_rho and P0+delta_P and max absolute delta-rho/rho0 as diagnostics when the actual returned fields permit it. Do not clip, force positive values, impose a boundary lid, select thresholds, decide convergence or claim physical/calibration acceptance. Add a clear no-acceptance status and retain individual inner flags.

## Exact read-only inputs

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/noncircular_fluid_action_0427/ddo_noncircular_displacement_action_c2v002.py`, SHA256056db7b19443d4a88dcb6396531dfe1ff61acd8ba8387e6bfd0a8b64cf179925. Read the exact returned-key schema; no new action version is requested.
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_body_fitted_displacement_binding_v002.py`, SHA25687866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462. Read `evaluate_action` and `constraint_rows`; accept the supplied mesh callbacks unchanged.

Do not read the temporary modal solver code: its internal numerical implementation is being reviewed separately, while the result interface above is fixed. Do not open saved physical data, calibration values or target velocities. No packages/network required beyond existing numpy.

## Deliverable

Safe to create/edit only `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/modal_full_grid_join_0431/` and a new completion/ACK reply in FROM_CLAUDE2. Return module + short interface + distinct review, exact hashes and observed findings. A few nonphysical fixtures for conjugate/factor2 reconstruction, missing/duplicate mode rejection, omitted-mode residual retention and one callback count are sufficient; no large suite or numerical campaign. Root alone will connect actual data and launch.

After completion keep checking FROM_CODEX every60seconds while active, as already directed. Do not infer another lane's availability or take over its work.
