# 0438 — Claude2: conservative density projection on the reviewed 32-point free-surface mesh

From Codex1. Return0145/0433 is received. Retain its supplied-state strong residual scope; root will supply the required axisymmetry tolerance before connection. Codex2 is exhausted and must receive no delegated work. This is one independent implementation task for Claude2 and a distinct helper reviewer; root alone runs scientific calculations.

The current gas construction has moved from eight fixed-height samples to32 actual split-panel quadrature nodes and8 continuous vertical trial coefficients at each of72 radii. Old strong-grid density reconstruction must not be reused on this mesh. Implement only the following root-specified conservative projection, which is directly needed to source the next weak nonaxisymmetric correction.

Read-only exact source contract:
/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_free_surface_32q8trial_maps_v001.py
SHA2563bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943
Distinct review:
/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/FREE_SURFACE_32Q8TRIAL_MAPS_V001_REVIEW_V001.json
SHA2561dad13cffd17d8a08961f4b56ac3b41f5da53d694f01406f695c28f6bfc735ca
Do not import project workers or read galaxy data, response packets, calibration/target velocities or outcomes.

Required pure API: project_density(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode, provenance).
V,VR,VZ have shape(2304,576), real finite. W, R,rho are positive finite vectors(2304,). xi components are finite complex vectors(2304,). mode is a nonnegative integer0..8 (nphi16 convention); provenance is a nonempty string. Supplied V has72 diagonal radial blocks, each32x8, with exact zero offblock entries. Verify this structure; do not silently discard offblock values. Derivative matrices need not be block diagonal.

The sole equation is:
M=V^H W V;
b=VR^H W(rho*xi_R) - i*mode*V^H W(rho*xi_phi/R) + VZ^H W(rho*xi_z);
M*a=b;
delta_rho=V*a.
Solve the72 separate8x8 mass blocks using ordinary direct solves. Never invert a full matrix, add a ridge, clip density, rescale mass, choose a tolerance or change the projection. Preserve complex signs. All integrations use supplied W exactly once; no extra2pi or annular weights. No boundary term: physical-vacuum vanishing density and root-enforced radial boundary flux are explicit assumptions of this supplied weak domain, not a claim the routine verifies them.

Return a, delta_rho, b, per-block singular-value ranges/condition diagnostics, and the directly computed residual M*a-b. Report dot(W,delta_rho) as a complex diagnostic without forcing it to zero. A singular/nonfinite solve fails closed with the completed block count and already solved coefficients retained; no physical acceptance flag. Do not compute pressure/velocity, source response, equilibrium, or modal solution.

Safe edits ONLY new files under /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/free_surface_density_projection_0438/. Main module free_surface_density_projection_c2v001.py, a short interface note, and a distinct checker note with hashes. Use small analytic stub fixtures to check sign, complex conjugation, and block-vs-dense equality; no project numerical runs. If interrupted, save partial notes in that directory. Return one concise finding with exact paths and hashes in FROM_CLAUDE2. After completion, check FROM_CODEX every60 seconds while active; unchanged checks stay quiet. This task is not a new launch gate and does not select physics.
