# Claude2: implement resumable coupled gas execution

From Codex1, principal-authorized support assignment. Posted 2026-10-16T13:06:44.881279+00:00. Principal reports Claude Code capacity restored and explicitly authorizes assignment. Acknowledge in FROM_CLAUDE2 before claiming active work. Codex3 handoff remains prepared/unacknowledged; Codex1 is coordinating here.

Read CURRENT_INSTRUCTIONS.md and this task. Do not duplicate completed pair/all-k/reweight capture or W2 work from0421. Use your helpers for one implementation author and a distinct reviewer. Root retains physics, calibration and numerical launch/acceptance.

## Concrete task

Implement actual restart at a completed HI-column boundary for the current coupled source iteration. The principal requests retaining state across timeouts and continuing the inward-response candidate. Existing progress files are evidence only, not a complete restart. Keep the current physical equations and exact finite Fourier reduction unchanged.

Base directory: /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13. Current files:
- helpers/recovered_packet_audit/coupled_hi_fourier_source_iteration_v005.py SHA d35c55bdd588f80661b568629482cbe54b50b5e0626dc0e370cd9a63f278188f
- helpers/recovered_packet_audit/ddo12_coupled_trial_root_driver_v009.py SHA 9629d8b4e1ac9fed9bf7b1e6e39657a73d9e57e81d293a33b31dd26df27a4812
- helpers/recovered_packet_audit/owned_fixed_xy_fourier_line_v001.py SHA 5c0ab4f6dcd14b79d5ec012f3eee6f58704b8e2982657ac58862b94b9429dfb4
- helpers/response_packet_audit/DDO_FIXED_XY_LINE_DRIVER_V009_DISTINCT_REVIEW_V001.json SHA 2d98ebfca74e873979c953b7a2a34e95189af050e094bdb80e24ab8865434ca6
- CODEX1/DDO154_FIRST_DIMENSIONAL_TRIAL_LAUNCH_V008.json SHA 80a48093d5de741fbe92694ec998afc24e5f59b33a797c97ba2c23eca3851594
- CODEX1/DDO154_FIRST_DIMENSIONAL_TRIAL_RUN_V008/result.json SHA 8208dee8a0b148587052397bca0b8d06b657dc26d416b5d6a3850abe2715232a

V008 completed in15.7195s,292864000B combined; iteration0 completed395of576columns then upper root not bracketed by32kpc at column395. Scientific status FAILED_SOURCE_PREPARATION. This is not an unbounded-gas proof. The earlier V007180s limit preserved no completedresult; exactline optimization resolved that bottleneck. Root/local HR is independently resolving vertical field integration. Do not change vertical profile, source/EH sign, gas boundary, parameters, force balance or search limits. No arbitrary strain taper or Birth ceiling.

Required restart evidence: actual iteration index, current gas Fourier iterate (do not reconstruct by subtraction if this changes arithmetic), fixed/current source, prepared waves, prior iteration history, ordered COMPLETE completed-column solutions including source quadrature, next column index; exact input identity for coefficients, source arrays, physical parameters, boundary prescription, full column roster, numerical controls and code pins. Reconstruct integrated gas positions/J in original order, rebuild exactline cache and continue. Form updated gas and apply relaxation exactly once after all columns complete. Reject stale/mismatched inputs. A changed Fourier/source grid invalidates saved columns.

Prefer a small optional checkpoint/resume interface in the existing solver/driver. Save completed column records incrementally rather than rewriting the full solution after each column. Preserve interrupted or invalid files and identify failures; no silent success or physics fallback. Do not create a generic job framework. New versioned code under your claude_artifacts area; do not overwrite local author files. Return exact pins, changed lines, assumptions and distinct review.

Do not run scientific workers, reread held-out NGC3198 velocities or validation outcomes, refit constants, create a replacement physical state, access cloud or restart old0351/0360 jobs. Static checks and narrowly scoped nonphysical restart-contract tests may be performed; clearly distinguish them from scientific execution. After completion, check FROM_CODEX every60seconds while active, keep unchanged checks quiet, and report actual blockers/returns.
