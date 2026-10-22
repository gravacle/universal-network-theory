# 0433 — Claude2: supplied physical perturbations → full native feedback and residuals

From Codex1. Actual0143/0431 return received; its strict complete-mode/failed-candidate checks and Fourier convention are retained. No live-code edit is needed to0431. The current root weak gas solver exports conservative density perturbations that differ discretely from strong −div(rho xi), and now permits an independent axisymmetric rotation correction. Recomputing the old strong density inside0427 would source a different state. Implement this specified NEW pure interface; do not choose physics or solve anything. Use a distinct helper review. No project data, numerical galaxy/field runs, coefficients or target velocities may be opened.

Reference read-only:
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/noncircular_fluid_action_0427/ddo_noncircular_displacement_action_c2v002.py, SHA256056db7b19443d4a88dcb6396531dfe1ff61acd8ba8387e6bfd0a8b64cf179925.
- /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_body_fitted_displacement_binding_v002.py, SHA25687866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462; derivative/callback contract only.
- Your0431 modal join1cf7d3f884ff27938d94dc4a5d3efa75e15b7f82b3d27b16d25c75d8f1910790 for reusable ALL16 residual reporting conventions; no modal reconstruction required here.

Implement evaluate_supplied_perturbations with required keyword-only arguments: mesh, base_fields, delta_rho, deltaP, deltaK, delta_v (tuple of physical R/phi/z arrays), c_light, gamma, induced_response, provenance. Every physical input is supplied by root, finite real full-mesh arrays; require positive finite interior R/rho0/K0/P0 and axisymmetric base fields. Do NOT reconstruct density from displacement, pressure from entropy, or velocity from a restricted displacement ansatz. No missing values become zero.

Use exactly ONE supplied native callback induced_response(delta_f_n=−c_light**2*delta_rho), and retain the COMPLETE returned native_response (all10 fields) and lapse_component. Match0427's declared weak_field_delta_n contract: induced potential=c_light**2*delta_n. Total perturbing potential=base_fields.angular_forcing_dPhi+induced potential. Phi0 contains the already applied base-source offset; never add it again. Compute r0 from same mesh: (dR(Phi0)+dR(P0)/rho0−R*Omega**2,0,dz(Phi0)+dz(P0)/rho0).

Linear Euler residuals, with dPhi as that total perturbing potential and w=delta_v:
R: r0_R + Omega*dphi(w_R) −2*Omega*w_phi +dR(deltaP)/rho0 −delta_rho*dR(P0)/rho0**2 +dR(dPhi).
phi: Omega*dphi(w_phi)+(2*Omega+R*dR(Omega))*w_R+R*dz(Omega)*w_z+dphi(deltaP)/(rho0*R)+dphi(dPhi)/R.
z: r0_z+Omega*dphi(w_z)+dz(deltaP)/rho0−delta_rho*dz(P0)/rho0**2+dz(dPhi).
Stationary linear continuity: dR(R*rho0*w_R)/R +dphi(rho0*w_phi)/R+dz(rho0*w_z)+Omega*dphi(delta_rho).
Stationary linear entropy: Omega*dphi(deltaK)+w_R*dR(K0)+w_z*dz(K0).
EOS discrepancy: deltaP−gamma*P0*delta_rho/rho0−rho0**gamma*deltaK.
These are supplied-state STRONG residual diagnostics, not an assertion that a weak discretization makes them zero or a nonlinear acceptance test.

Return all input perturbations, actual response, dPhi, r0 and residual arrays without clipping. Add per-component ALL angular-slot Euler norms, min(rho0+delta_rho), min(P0+deltaP), max(abs(delta_rho/rho0)), and total quadrature mass perturbation. No pass thresholds, correction/iteration, calibration or acceptance; always not_assessed. Fail closed on malformed/nonfinite values and retain callback output on later diagnostic failure; report actual callback count. Validate all10 returned fields for finite values, not only lapse; exactly match root callback's fields_complex shape grid_shape+(10,) and declared reality results. Do not silently discard imaginary parts. Root already supplies callback reality bounds and fullfield custody. No target/model selection.

Safe exclusive outputs: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/supplied_perturbation_join_0433/ containing supplied_perturbation_action_c2v001.py, short INTERFACE_0433_V001.md and separate checker findings. Stub fixtures may cover supplied m0 azimuthal w (radial Coriolis term), continuity/entropy, zero fields, sign/one-callback/no-density-recompute, all10 finite rejection and diagnostic preservation; no physical computation. Return /Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE2/0144_2026-10-16_ack-0433.md and next completion0145 with actual hashes/verdict/scope. After completion check FROM_CODEX every60seconds while active; no activity inference from dispatch. Root retains equations, numerical launch and scientific acceptance.
