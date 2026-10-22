# 0436 — Codex2: free-surface column derivative and rotation identity

Codex1 integrates0410 PASS_SCOPED: combined field is G4+offset once and potential is c² times mean log lapse. The three failed outer columns now solved their fixed-K/fixed-Sigma free surfaces, with mass relative residuals below7.5e-9. The principal explicitly requests your next small task.

Specific question: verify the following exact hydrostatic-to-rotation identities before their use in motion evaluation. Let P=K(R)rho^gamma, gamma=5/3, h=gamma K rho^(gamma−1)/(gamma−1)=C(R)−Phi(R,z)>0 inside its connected support. Let rho vanish at the two moving free surfaces, and Sigma(R)=integral rho dz. Phi is the actual azimuthally averaged native c²lnN. Proposed identities, all derivatives at fixed physical z:

1. (partial_R P)/rho=partial_R h−(h/gamma) partial_R lnK.
2. R Omega²=C'(R)−(h/gamma) partial_R lnK.
3. C'=[(gamma−1)Sigma' +(K'/K)Sigma + integral (rho/h) partial_R Phi dz] / integral (rho/h) dz.

Derive or correct all three as one short linked calculation. Check Leibniz moving-endpoint terms, integrability of rho/h at a simple h=0 surface for gamma5/3, signs and dimensions. If only a midplane difference is available, Hc=C−Phi(R,0), so be explicit that C'=Hc'+partial_R Phi(R,0); dropping the latter is prohibited. Negative Omega² must remain a failed stationary branch, never clipped. This is a declared effective hydrostatic/Euler branch, not a claim that classical equations were independently derived here.

Exact implementation context: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_fixed_K_free_surface_column_v001.py`, SHA256 `54e56f7b53d8ad705875f30b4ddfb029484585fb9343363dab2ab5a2f93bb0d5`. Read only its enthalpy/rho/P/mass definitions if needed. Exact evaluated evidence is `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/DDO154_OUTER_FREE_SURFACE_RUN_V001/columns/finish.json`; do not read arrays, target velocities or broad background. Local HC handles successor implementation; HP reviewed the boundary solver. This algebraic radial-derivative question is distinct.

Return <=350 words, PASS_SCOPED or precise correction plus any non-simple-boundary qualification, to `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0411_2026-10-16_free_surface_rotation_identity.md`. No helpers, numerical runs/imports, live-code edits, general planning or new physical choices. Only that return and partial notes under `/Users/bgm/Research/UNT_EXCHANGE/codex2_artifacts/0436_rotation_identity/` are safe to edit. Preserve partial findings if usage expires; report exhaustion when observed. No new approval gate.
