# Claude4 partial review 0440, V001: root contract vs pinned prior contraction

Lead: Claude4. 2026-10-16, about 18:35 UTC. Status: SPEC-LEVEL ONLY. Claude3's frozen implementation was not yet available: FROM_CLAUDE3 and weak_euler_0439/ were empty at 18:27 UTC. This file is a partial finding, not the verdict. Helpers H1 (algebra) and H2 (fixtures) are deriving and testing independently. Their outputs will be integrated in REVIEW_0440_V001.md.

## Inspected (SHA-256 recomputed)

| File | SHA-256 |
|---|---|
| CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json (root contract) | 5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe |
| helpers/coefficient_method/owned_nonzero_modal_weak_adjustment_v002.py (prior, read only) | 5cae4ee994f1ca07fdf703af529e7f5df9df2c2ed642d478df89beb692a25c51 |
| helpers/coefficient_method/owned_32q8_regular_helicity_maps_v001.py (divU convention, read only) | 280149dc028260d865604948633bb8a1332c5ee01be916895c02df42e2b280c6 |
| helpers/coefficient_method/owned_free_surface_32q8trial_maps_v001.py (W = R dR dz, read only) | 3bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943 |

## Finding 1: no equation discrepancy between the root contract and prior v002

Name map: Omega=W, Omega_R=WR, Omega_z=WZ, R=RR, K_R/K_z=KR/KZ, P_R/P_z=PR/PZ, volume_weights=vol, volume_weights*rho=wrho, f_R/f_phi/f_z=fr/fp/fz, normalization_scale=mass*aref*L.

| Contract item | v002 line | Status |
|---|---|---|
| E | 44 | identical |
| PM | 44 | identical |
| VR, VP, VZ | 45 | identical |
| AR | 46 | identical |
| AP | 47 | identical |
| AZ | 48 | identical |
| A inertial (U^H diag(vw rho) A*) | 52 | identical |
| A pressure (-divU^H diag(vw) PM) | 53 | identical |
| A density (-[U_R^H diag(vw P_R/rho)+U_z^H diag(vw P_z/rho)] G) | 54 | identical |
| b | 58 | identical |
| scale only A and b | 59-61 | identical in form (scale value now supplied) |

## Finding 2: the contract is the linearized adiabatic Euler weak form (lead derivation, to be cross-checked by H1)

Take a static pattern (omega = 0) in the inertial frame, with exp(+i m phi). This is the numpy-FFT analysis convention of v002 L55-57 and the helicity map divU, with +1j*m*UP/R.

- The Eulerian velocity from the displacement is delta v = (v0.grad)xi - (xi.grad)v0, with v0 = R Omega e_phi and unit-vector derivatives included. Its components reproduce VR, VP and VZ exactly. Example: phi: Omega(i m xi_phi + xi_R) - xi_R(Omega + R Omega_R) - xi_z R Omega_z.
- The Eulerian acceleration delta a = (v0.grad)delta v + (delta v.grad)v0 reproduces AR, AP and AZ exactly.
- Background equilibrium turns delta rho (v0.grad)v0 + delta rho grad Phi0 into -delta rho grad P/rho. The strong form is then rho delta a + grad delta P - (delta rho/rho) grad P = -rho grad(delta Phi_m), the same as the v002 strong residual at L67.
- With adiabatic Delta K = 0, delta K = -xi.grad K = E and delta P = (gamma P/rho) delta rho + rho^gamma E = PM.
- For the weak form, the test field is conj(U) exp(-i m phi). Integrating the pressure gradient by parts gives -conj(divU) delta P. In the phi component, conj(+i m U_phi/R) = -i m conj(U_phi)/R, which reproduces +i m conj(U_phi) delta P/R. So the test side needs the conjugate transpose. Each term carries the volume weight exactly once. The density term is /rho, not /rho^2, because the strong form is multiplied by rho.

Closed pointwise inertial form, used as an independent fixture oracle. Substituting VR, VP and VZ gives:

- AR = (2 Omega R Omega_R - m^2 Omega^2) U_R - 2 i m Omega^2 U_phi + 2 Omega R Omega_z U_z
- AP = 2 i m Omega^2 U_R - m^2 Omega^2 U_phi. The R Omega_R and R Omega_z contributions cancel exactly here.
- AZ = -m^2 Omega^2 U_z

So the inertial block is sum_p vw_p rho_p U_p^H M_p U_p. The m^2 and m^1 parts of M_p are Hermitian. The m^0 part has an unmatched 2 Omega R Omega_z coupling in row R and column z. This is the vertical-shear term R d_z(Omega^2) xi_z. It makes A non-Hermitian whenever Omega_z != 0. Any implementation that symmetrizes A, or drops either vertical-shear term from VP or AP, is detectable.

## Non-equation differences (no defect; advisory for root)

- D1, G. In v002 (L43), G is the adjoint nodal weak divergence. Now G is the 0438 V-space conservative projection. The sign conventions are the same: +VR^H W rho xi_R, -i m V^H W rho xi_phi/R, +VZ^H W rho xi_z, the weak form of delta rho = -div(rho xi). The implementation must use the supplied G verbatim.
- D2, volume weights. v002 used node volumes summed over 16 azimuthal cells (L39), which include the azimuthal measure. 0438-style W = R dR dz carries no 2 pi. A uniform factor on A and b cancels in A^-1 b. If root reuses a normalization like mass*aref*L built with the azimuthal measure, A/scale and b/scale shift by 2 pi relative to v002. That affects only absolute thresholds root may later apply to the scaled system. Root should keep the normalization_scale consistent with the volume_weights actually supplied.
- D3, forcing. v002 differentiated the FFT/16 modal potential: DR@pot, i m pot/R, DZ@pot. The contract supplies f_R, f_phi and f_z already in that convention. The implementation must not multiply f_phi by i m/R again and must not add Phi0.
- D4, background derivatives. These were DR/DZ nodal derivatives; they are now supplied vectors.
- D5. There is no solve, rank test or acceptance; v002 L62-76 is intentionally not carried over.

## Scope assumptions (not implementation defects)

- S1: static omega = 0 pattern. A rotating pattern would need i m(Omega - Omega_p); that is root's physics choice.
- S2: the background-equilibrium identity is used to eliminate Phi0. Any m0 equilibrium residual is deliberately not injected into nonzero modes.
- S3: PM is the adiabatic delta P only if the supplied P equals K rho^gamma. The contract does not ask the routine to check this, and the routine must not reset P.
- S4: the zero pressure surface term and zero-flux G are declared continuum weak-domain assumptions.

## Next

Claude3's frozen module will be evaluated against H2's harness and H1's checklist as soon as 0002_2026-10-16_done-0439.md is posted.
