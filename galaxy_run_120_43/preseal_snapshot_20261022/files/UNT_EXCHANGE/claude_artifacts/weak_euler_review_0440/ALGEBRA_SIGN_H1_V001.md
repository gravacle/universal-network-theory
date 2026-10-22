# ALGEBRA_SIGN_H1_V001: weak Euler contract, first-principles algebra, complex signs, vertical shear

Lane: Claude4 review lane (dispatch 0440, amended by 0441). Author: local helper **H1** (algebra, complex signs, vertical shear). This is a helper review note for the Claude4 lead, not an external-account response and not a physical verdict. Codex1 (root) owns physics, launches and acceptance. H1 did not inspect Claude3's implementation, did not import or run any project module, and opened no galaxy data, calibration/target velocities, validation outcomes or mesh arrays. Fixtures are synthetic and small.

## Sources read (sha256 by `shasum -a 256`)

| file | sha256 | note |
|---|---|---|
| `.../CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json` | `5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe` | matches pin; equations 1-10 re-read by the check script and equal to the transcription used (after U+2212 -> `-`) |
| `.../coefficient_method/owned_nonzero_modal_weak_adjustment_v002.py` (80 lines) | `5cae4ee994f1ca07fdf703af529e7f5df9df2c2ed642d478df89beb692a25c51` | matches pin; read only |
| `.../coefficient_method/owned_32q8_regular_helicity_maps_v001.py` | `280149dc028260d865604948633bb8a1332c5ee01be916895c02df42e2b280c6` | matches pin; read only |
| `FROM_CODEX/0438_2026-10-16_claude_free_surface_density_projection.md` | `83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c` | no pin supplied; hash recorded |
| `FROM_CODEX/0439_2026-10-16_claude3_weak_euler_assembly.md` | `12905749dbc3d2e96ec2b33f69fb5f5952a4341a8d70f75c591a4a5984fe9543` | context |
| `FROM_CODEX/0440_2026-10-16_claude4_weak_euler_independent_review.md` | `ed7ccc60fae6056ae8133fc430ea7b05b8c9c8bae3787381e8c4e7ac5e751592` | context |
| `FROM_CODEX/0441_2026-10-16_parallel_lane_execution_addendum.md` | `a5cab71ad8a296760c5cab455c8b56a18fe61344e1189bc19d57a10b99cc5987` | context |
| `FROM_CODEX/0442_2026-10-16_claude3_recipient_correction.md` | `e1e94e32d86cc9c4abad4dffcb805ed793aede90562a3c7dd3fb0f9f5c17df53` | context |
| `UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md` | `0500c1902f25cae550f87671df688e46286c68299d9493226e96bc1db2877094` | read first |
| `UNT_PROGRAM_CONTROL/CLAUDE4_START_HERE_2026-10-16_V001.md` | `f93190c38cd1565c8dc108325ef5dc5dbe1e4810c169044bf271ecdebc9cd47d` | context |

H1 files in this directory: `algebra_oracle_h1v001.py` sha256 `29fc7fd429c921c4e6e7c04a624ce4db6ffcb0b32a8c0f5a432413ce73feb23e`; `check_h1_oracle_v001.py` sha256 `ae5238153a1efe6dd1354488620d3d8d07713f3e77dd2255350d5621ae78d53a`. This note's own hash is reported in H1's structured return; a file cannot contain its own hash.

## 0. Findings

1. **The derivation agrees with the contract.** Starting from first principles, every equation reappears term by term: E, PM, VR, VP, VZ, AR, AP, AZ, the three parts of A, and b. **No sign or algebra error was found in the contract.**
2. **All sources use the same modal convention, exp(+i m φ).** It holds in the v002 FFT/16 extraction (L56), in `fp = i m pot/R` (L57), in the helicity divU (`+1j*m*UP/R`, L64), in the v002 G (L43, `-im*rho*UP/R`) and in the 0438 b-map (`-i m V^H W rho xi_phi/R`).
3. **Closed form.** The pointwise inertial matrix M_p is given in §1h. Its only non-Hermitian piece is the vertical-shear entry 2RΩΩ_z in position (R,z), and that entry has no (z,R) partner. In the weak inertial block it appears as `U_R^H D(2 w ρ R Ω Ω_z) U_z`.
4. **Self-adjointness (exact algebra, confirmed by fixture).** Assume four things:
   - P = Kρ^γ;
   - the gradients are consistent with it;
   - the background obeys the thermal-wind relation 2RΩΩ_z = (P_z ρ_R − P_R ρ_z)/ρ²;
   - G is the pointwise conservative density, G = −(ρ divU + ρ_R U_R + ρ_z U_z).

   Under those assumptions the contract's A is exactly Hermitian, to 3.4e-16, even though its inertial and pressure/density parts are each non-Hermitian. The baroclinic pressure/density term cancels the vertical-shear term.

   This fixture detects 17 of the 18 sign/factor mutants of A. Consequence: the non-Hermiticity of the actual assembled A comes from the discrete G and from inconsistency in the supplied background, not from the contract's signs. It must not be symmetrized away.
5. **The oracle matches the contract chain.** Over 72 random complex cases (non-square 7x3 and square 4x4, m = 1..6, nonzero Ω_R and Ω_z), the maximum relative error is **6.0e-16 for A** and **4.3e-16 for b**.
6. **Comparison with v002.**
   - The equations are identical in form to v002 L44-48, L52-54 and L58.
   - The G construction differs. This is intended by 0438: same continuum weak equation and same signs, but a different finite map, so A differs numerically.
   - The 2π volume-weight convention is a global scale only. It leaves G, the maps and the solution of A y = b unchanged.
   - The forcing, background derivatives and normalization are now supplied by root. This changes no operator, provided root follows the convention in §3.

## 1. Derivation (Task 1)

Notation: D(d) is the diagonal of a point vector d (never formed); w = volume_weights; subscripts R and z denote partial derivatives; Ω_R = ∂_R Ω and Ω_z = ∂_z Ω. The unit-vector derivatives are ∂_φ e_R = e_φ and ∂_φ e_φ = −e_R; all other derivatives of e_R, e_φ, e_z vanish.

### 1a. Background, modal and frame conventions

- **Background.** The flow is steady and axisymmetric: v0 = V e_φ with V = RΩ(R,z), and the fields ρ, P, K depend on (R,z) only. P = Kρ^γ is assumed; see 1e.
- **Perturbations.** X = X_m(R,z) exp(+i m φ), so ∂_φ → +i m. The pattern is static in the inertial frame (ω = 0), so every ∂_t is dropped. For a pattern speed Ω_p, every factor i m Ω below becomes i m (Ω − Ω_p); the Coriolis factor 2Ω and the shear terms are unchanged.
- **v002 L56, `pot = (np.fft.fft(forcing,axis=1)/16)[:,m,:]`.** The numpy forward FFT is X_k = Σ_n x_n e^{−2πikn/N}. For x_n = c0 + c e^{imφ_n} + c̄ e^{−imφ_n} + (other modes), this gives X_m/16 = c e^{imφ_0}, where φ_0 is the azimuth of the first sample. So `pot` is the coefficient of e^{+imφ}, with its phase referenced to φ_0. Fixture [E] confirms this to 1.5e-15 for φ_0 = 0 and to 1.0e-15 for a half-cell offset. Index 16−m returns the conjugate.
- **v002 L57, `fp = im*pot/RR`.** This is (1/R)∂_φ(pot e^{imφ}) e^{−imφ}. In fixture [E], FFT/16 of the sampled ∂_φΦ at index m equals i m × pot to 1.4e-15.
- **Helicity L64, `div = ∂_R U_R + U_R/R + (1j*m) U_P/R + ∂_z U_Z`.** This is (1/R)∂_R(R U_R) + (1/R)∂_φ(U_φ e^{imφ})e^{−imφ} + ∂_z U_z under exp(+imφ).
- **v002 L45 and L68.** VR = i m Ω U_R, and `strongrho = ... − im*rho*xp/RR ...`. Same convention.

### 1b. Velocity perturbation

The linear Eulerian velocity perturbation is δv = ∂_t ξ + (v0·∇)ξ − (ξ·∇)v0. For the static pattern this is δv = (v0·∇)ξ − (ξ·∇)v0.

Note that (v0·∇) = (V/R)∂_φ = Ω ∂_φ, applied to the vector including its unit vectors:

(v0·∇)ξ = Ω[(∂_φξ_R − ξ_φ) e_R + (∂_φξ_φ + ξ_R) e_φ + ∂_φξ_z e_z] = Ω[(imξ_R − ξ_φ) e_R + (imξ_φ + ξ_R) e_φ + imξ_z e_z]

(ξ·∇)v0 = ξ_R ∂_R(V e_φ) + (ξ_φ/R)∂_φ(V e_φ) + ξ_z ∂_z(V e_φ) = −Ωξ_φ e_R + (V_R ξ_R + V_z ξ_z) e_φ, with V_R = Ω + RΩ_R and V_z = RΩ_z.

Subtracting gives the three components:

- δv_R = imΩξ_R − Ωξ_φ + Ωξ_φ = **imΩξ_R**. The unit-vector rotation term and the advection of v0 cancel.
- δv_φ = imΩξ_φ + Ωξ_R − (Ω + RΩ_R)ξ_R − RΩ_zξ_z = **−RΩ_R ξ_R + imΩξ_φ − RΩ_z ξ_z**.
- δv_z = **imΩξ_z**.

With U in place of ξ, these are exactly the contract's VR, VP and VZ.

**Independent consistency check (linearized continuity for a static pattern).** The condition is ∇·(ρδv) + v0·∇δρ = 0 with δρ = −∇·(ρξ). Expanding:

∇·(ρδv) = (1/R)∂_R(Rρ imΩξ_R) + (im/R)ρ(imΩξ_φ − RΩ_Rξ_R − RΩ_zξ_z) + ∂_z(ρ imΩξ_z)
= imΩ∇·(ρξ) + [imΩ_R ρξ_R − imρΩ_R ξ_R] + [imΩ_z ρξ_z − imρΩ_z ξ_z]
= −imΩδρ.

Also v0·∇δρ = imΩδρ, so the sum is zero. The shear terms in δv_φ are exactly what cancels the Ω-gradient terms, so mass conservation also fixes their signs.

Fixture [C] (3-D Cartesian 4th-order finite differences, analytic Ω(R,z) with Ω_R and Ω_z bounded away from zero, complex polynomial U, m = 1..6, both phases):

| check | result |
|---|---|
| δv from FD vs contract VR, VP, VZ | max rel err 7.6e-12 |
| mutant VP with +RΩ_z U_z | deviation ≥ 2.0e-2 |
| mutant VP with +RΩ_R U_R | deviation ≥ 4.2e-2 |
| continuity residual | 1.2e-11 |
| continuity residual, VP +RΩ_z mutant | ≥ 4.4e-2 |

### 1c. Acceleration perturbation

For the static pattern, δa = (v0·∇)δv + (δv·∇)v0.

(v0·∇)δv = Ω[(imδv_R − δv_φ) e_R + (imδv_φ + δv_R) e_φ + imδv_z e_z]

(δv·∇)v0 = −Ωδv_φ e_R + ((Ω + RΩ_R)δv_R + RΩ_z δv_z) e_φ

Adding the two:

- δa_R = **imΩ δv_R − 2Ω δv_φ** (= AR)
- δa_φ = **imΩ δv_φ + (2Ω + RΩ_R) δv_R + RΩ_z δv_z** (= AP)
- δa_z = **imΩ δv_z** (= AZ)

**Independent route.** Take a0 = (v0·∇)v0 = −Ω²R e_R. From the Cartesian commutator [v0·∇, ξ·∇] = ((v0·∇)ξ − (ξ·∇)v0)·∇ it follows that δa = (v0·∇)²ξ − (ξ·∇)a0, with

(v0·∇)²ξ = Ω²[(−(m²+1)ξ_R − 2imξ_φ) e_R + (2imξ_R − (m²+1)ξ_φ) e_φ − m²ξ_z e_z]

(ξ·∇)a0 = [−(Ω² + 2RΩΩ_R)ξ_R − 2RΩΩ_z ξ_z] e_R − Ω²ξ_φ e_φ

Their difference is exactly M_p of §1h.

Fixture [C] results:

| check | result |
|---|---|
| δa from FD vs contract AR, AP, AZ and vs closed-form M_p | max rel err 9.3e-12 |
| mutant AP with −RΩ_z VZ | ≥ 2.8e-2 |
| mutant AR with +2ΩVP | ≥ 0.56 |

### 1d. Linearized momentum equation and the equilibrium identity

Start from ρ(∂_t v + (v·∇)v) = −∇P − ρ∇Φ. The m = 0 equilibrium is (v0·∇)v0 = −∇P/ρ − ∇Φ0, that is, −Ω²R = −P_R/ρ − Φ0_R and 0 = −P_z/ρ − Φ0_z.

At first order, for the static pattern: ρδa + δρ(v0·∇)v0 = −∇δP − δρ∇Φ0 − ρ∇δΦ.

Gather the δρ terms: δρ[(v0·∇)v0 + ∇Φ0] = −δρ∇P/ρ, by the equilibrium identity. Therefore

**ρ δa + ∇δP − (δρ/ρ)∇P = −ρ f**, with f = ∇δΦ = (∂_RδΦ, imδΦ/R, ∂_zδΦ).

The background ∇P has no φ component, so the δρ term has R and z components only.

Dividing by ρ gives δa + ∇δP/ρ − (δρ/ρ²)∇P + f = 0, which is exactly the prior strong residual at v002 L67:

- `AR@y + DR@dP/rho − PR*drho/rho**2 + fr`
- `AP@y + im*dP/(rho*RR) + fp`
- `AZ@y + DZ@dP/rho − PZ*drho/rho**2 + fz`

The /ρ² in L67 belongs to the strong form after division by ρ. The weak form tests the undivided equation, so it carries /ρ (see 1f). v002 L68 (`strongrho`) is −∇·(ρξ) in the same convention.

### 1e. Adiabatic pressure

Lagrangian entropy conservation gives ΔK = 0 for K = P/ρ^γ. The Eulerian perturbation is then δK = ΔK − ξ·∇K = −(ξ_R K_R + ξ_z K_z), since K is axisymmetric. This is **E**.

With P = Kρ^γ: δP = (∂P/∂ρ)_K δρ + (∂P/∂K)_ρ δK = γKρ^{γ−1}δρ + ρ^γ δK = **(γP/ρ)δρ + ρ^γ δK**. This is **PM**, with δρ represented by G.

- The step γKρ^{γ−1} = γP/ρ requires the supplied P to equal Kρ^γ pointwise.
- If δρ = −∇·(ρξ) exactly and ∇P = ρ^γ∇K + (γP/ρ)∇ρ, then PM reduces to the textbook Eulerian δP = −γP∇·ξ − ξ·∇P.
- K and ∇ρ are not module inputs, so neither relation can be checked inside the module.

### 1f. Weak form, the volume measure and conjugation

The test field is W = U(R,z)e^{imφ}, using the same maps as the trial (Galerkin). The inner product is ⟨W,F⟩ = ∫ conj(W)·F dV with dV = R dR dφ dz. For modal F = F_m e^{imφ}, the φ-integral of e^{−imφ}e^{imφ} gives 2π, so ⟨W,F⟩ = 2π∫ conj(U)·F_m R dR dz.

The discrete rule replaces ∫(·)R dR dz by Σ_i w_i(·)_i. The 2π is a global constant: v002's azimuthal sum at L39 includes it, and the 0438-style weights exclude it. In matrix entry A_jk, j is the test column and k the trial column.

1. **Inertial.** ∫conj(U)·ρδa gives `U_R^H D(wρ) AR + U_phi^H D(wρ) AP + U_z^H D(wρ) AZ`.
2. **Pressure, component by component, with boundary terms dropped as declared.**
   - R: ∫conj(U_R)∂_RδP R dR dz = [R conj(U_R) δP]_bdry − ∫∂_R(R conj(U_R)) δP dR dz = −∫conj(∂_R U_R + U_R/R) δP R dR dz.
   - φ: conj(U_φ)·(1/R)∂_φ(δP e^{imφ})e^{−imφ} = conj(U_φ)(imδP/R) = **−conj(imU_φ/R) δP**, because conj(i) = −i. No integration by parts is involved. This is the point where conjugating the test side fixes the sign that pairs with divU's +im.
   - z: ∫conj(U_z)∂_zδP R dR dz = −∫conj(∂_z U_z) δP R dR dz.
   - Sum: ∫conj(U)·∇δP = −∫conj(∂_R U_R + U_R/R + imU_φ/R + ∂_z U_z) δP = **−∫conj(divU) δP**, using exactly the helicity divU. This gives the term **`−divU^H D(w) PM`**, with one weight and no ρ.
   - In 3-D form: ∫conj(W)·∇(δP e^{imφ})dV = ∮conj(W·n)δP e^{imφ}dS − ∫conj(∇·W)δP e^{imφ}dV, with ∇·W = divU e^{imφ}.
   - Fixture [D] (Gauss-Legendre, 24x24 nodes on R∈[1,2], z∈[−1,1], exact for the polynomial integrands, δP vanishing on the boundary): per-component and total agreement to 1.4e-15. With divU built from −imU_φ/R the mismatch is ≥ 1.28. With no conjugation at all the mismatch is ≥ 0.925, because the φ term changes sign.
3. **Density.** −∫conj(U)·(δρ/ρ)∇P gives **`−[U_R^H D(w P_R/ρ) + U_z^H D(w P_z/ρ)] G`**: leading minus, **/ρ and not /ρ²**, no U_φ term, one weight.
4. **Forcing.** −∫conj(U)·ρf gives **`b = −U_R^H(wρ f_R) − U_phi^H(wρ f_phi) − U_z^H(wρ f_z)`**. The supplied f_phi already contains imδΦ/R.

So A y = b states ⟨W, ρδa + ∇δP − (δρ/ρ)∇P + ρf⟩ = 0 for every test column, with the surface terms dropped. **Each of the five A terms and each of the three b terms carries exactly one w. E, PM, VR, VP, VZ, AR, AP, AZ and G carry none.** In fixture [G], multiplying w by 2π scales A and b by exactly 2π (deviation 4.4e-16), and the five maps are unchanged.

### 1g. 0438's G is the weak form of δρ = −∇·(ρξ) and agrees with v002 L43

In modal form, −∇·(ρξ) = −(1/R)∂_R(Rρξ_R) − imρξ_φ/R − ∂_z(ρξ_z). Take the test function ψ_j e^{imφ}, where ψ_j is a column of 0438's real scalar map V (so conj(ψ_j) = ψ_j):

∫ψ_j δρ R dR dz = ∫∂_Rψ_j ρξ_R R dR dz − im∫ψ_j (ρξ_φ/R) R dR dz + ∫∂_zψ_j ρξ_z R dR dz + (flux terms ψ_j ρ ξ·n R).

The flux terms vanish under the declared zero-flux and physical-vacuum assumption. With quadrature W (R dR dz):

V^H W δρ = Vr^H W(ρξ_R) − im V^H W(ρξ_φ/R) + Vz^H W(ρξ_z).

This is the 0438 b-map with all signs (+, −im, +).

- **Naming hazard.** 0438's `VR`/`VZ` are the scalar partial_R/partial_z maps, written Vr/Vz above. They are not the contract's velocity maps VR/VZ.
- **What G is.** With δρ = V a and M a = b, M = V^H W V, G = V a is the W-weighted L2 projection of −∇·(ρξ) onto span(V).
- **Complex test.** For a complex ψ the φ term is −im conj(ψ)ρξ_φ/R. Fixture [D] verifies the identity for complex and real ψ to 1.1e-14; the +im mutant mismatches by 2.0.

**v002 L43:** `G = [DR^T(vol ρ U_R) + DZ^T(vol ρ U_z)]/vol − im (ρ/R) U_φ`. Use nodal Lagrange test functions φ_j, with DR[i,j] = ∂_Rφ_j(x_i) and DZ[i,j] = ∂_zφ_j(x_i), and the lumped mass ∫φ_j δρ ≈ vol_j δρ_j. Then

vol_j G_j = Σ_i ∂_Rφ_j(x_i) vol_i ρ_i U_R,i + Σ_i ∂_zφ_j(x_i) vol_i ρ_i U_z,i − im vol_j ρ_j U_φ,j/R_j.

This is the same weak equation, with the same three signs and the same flux drop. The two constructions differ only in discretization: a lumped nodal mass versus a consistent-mass projection onto 8 vertical coefficients per radius. Their G maps, and hence A, therefore differ numerically.

**Join requirements, not checkable in the Euler module.** G must be built with mode = m, with xi = (U_R, U_phi, U_z) being the same maps and columns, with W = volume_weights, and with the same ρ and R.

### 1h. Closed forms for the oracle

Substituting VR, VP, VZ into AR, AP, AZ:

- **AR** = imΩ(imΩU_R) − 2Ω(−RΩ_R U_R + imΩU_φ − RΩ_z U_z) = (−m²Ω² + 2RΩΩ_R)U_R − 2imΩ²U_φ + **2RΩΩ_z U_z**.
- **AP** = imΩ(−RΩ_R U_R + imΩU_φ − RΩ_z U_z) + (2Ω + RΩ_R)(imΩU_R) + RΩ_z(imΩU_z), by coefficient:
  - U_R: −imRΩΩ_R + 2imΩ² + imRΩΩ_R = **2imΩ²**. The radial-shear terms cancel.
  - U_φ: **−m²Ω²**.
  - U_z: −imRΩΩ_z + imRΩΩ_z = **0**. The vertical-shear terms cancel.
- **AZ** = −m²Ω² U_z.

The resulting pointwise matrix, with rows and columns ordered (R, φ, z), acts as (AR,AP,AZ)ᵀ = M_p (U_R,U_φ,U_z)ᵀ:

```
M_p = [[ -m^2 Ω^2 + 2RΩΩ_R ,  -2 i m Ω^2 ,  2RΩΩ_z  ],
       [  2 i m Ω^2        ,  -m^2 Ω^2   ,  0       ],
       [  0                ,   0         , -m^2 Ω^2 ]]
    = -m^2Ω^2 I  +  2imΩ^2 J  +  R∂_R(Ω^2) e_R e_Rᵀ  +  R∂_z(Ω^2) e_R e_zᵀ,
      J = e_φ e_Rᵀ − e_R e_φᵀ = [[0,-1,0],[1,0,0],[0,0,0]].
```

Splitting by powers of m:

- **m² part:** −m²Ω² I. Hermitian; its weak form is negative semidefinite, and definite when the stacked maps have full column rank.
- **m¹ part:** 2imΩ² J. Hermitian, since (2imΩ²J)^H = −2imΩ²Jᵀ = 2imΩ²J. Indefinite.
- **m⁰ part:** R∂_R(Ω²) e_R e_Rᵀ is Hermitian. **R∂_z(Ω²) e_R e_zᵀ is real with entry (R,z) = 2RΩΩ_z and entry (z,R) = 0.** This is the only non-Hermitian part of M_p, and it is present if and only if Ω_z ≠ 0.

Physics sanity check: the determinant of the (R,φ) block is m²Ω²(m²Ω² − κ²), with κ² = 4Ω² + 2RΩΩ_R = R dΩ²/dR + 4Ω². The static-pattern Lindblad condition m²Ω² = κ² follows. Fixture [B] confirms this to 2.0e-16.

The weak blocks used by the oracle, with no VR..AZ chaining:

```
A_inertial = −m^2 Σ_{c∈R,φ,z} U_c^H D(wρΩ^2) U_c
             + 2im [ U_φ^H D(wρΩ^2) U_R − U_R^H D(wρΩ^2) U_φ ]
             + U_R^H D(2wρRΩΩ_R) U_R + U_R^H D(2wρRΩΩ_z) U_z
A_press+dens = −divU^H D(wγP/ρ) G + divU^H D(wρ^γ K_R) U_R + divU^H D(wρ^γ K_z) U_z
               − U_R^H D(w P_R/ρ) G − U_z^H D(w P_z/ρ) G
b = −U_R^H(wρ f_R) − U_φ^H(wρ f_φ) − U_z^H(wρ f_z)
```

The second line uses −divU^H D(w)PM = −divU^H D(wγP/ρ)G − divU^H D(wρ^γ)E, with E = −K_R U_R − K_z U_z. Every term has the form X^H D(d) Y with Y ∈ {U_R, U_φ, U_z, G}.

### 1i. Self-adjointness and the source of non-Hermiticity (supports Task 4)

Insert the pointwise conservative density G = −(ρ divU + ρ_R U_R + ρ_z U_z) and the relation P_R = ρ^γK_R + (γP/ρ)ρ_R (and its z analogue):

```
A_press+dens = divU^H D(wγP) divU
             + [divU^H D(wP_R) U_R + U_R^H D(wP_R) divU] + [divU^H D(wP_z) U_z + U_z^H D(wP_z) divU]
             + U_R^H D(wP_Rρ_R/ρ) U_R + U_z^H D(wP_zρ_z/ρ) U_z
             + U_R^H D(wP_Rρ_z/ρ) U_z + U_z^H D(wP_zρ_R/ρ) U_R
```

- The pressure/density anti-Hermitian part comes only from the last line: ½[U_R^H D(w(P_Rρ_z − P_zρ_R)/ρ) U_z − (same)^H].
- The inertial anti-Hermitian part is ½[U_R^H D(2wρRΩΩ_z) U_z − (same)^H].
- The thermal-wind relation follows from ∂_z of the R-equilibrium minus ∂_R of the z-equilibrium, which eliminates Φ0: ∂_z(P_R/ρ) − ∂_R(P_z/ρ) = ∂_z(Ω²R), so (P_zρ_R − P_Rρ_z)/ρ² = 2RΩΩ_z, and therefore (P_Rρ_z − P_zρ_R)/ρ = −2ρRΩΩ_z.
- The two anti-Hermitian parts therefore cancel exactly. The ω = 0 operator is Hermitian; this is the hydrodynamic Frieman–Rotenberg self-adjointness.

Fixture [F] uses a pointwise background with P = Kρ^γ, consistent gradients, thermal-wind Ω_z and pointwise G, over 36 cases with shapes 9x4 and 5x5 and m = 1..6:

| case | anti-Hermitian relative norm |
|---|---|
| full contract A (chain and oracle) | max 3.4e-16 |
| inertial part alone | 5.2e-3 to 0.79 |
| pressure/density part alone | 3.2e-2 to 0.67 |
| Ω_z replaced by inconsistent values | 1.1e-2 to 0.69 |
| G replaced by a non-pointwise map | 2.5e-2 to 1.16 |

This is a fact about the algebra, not a physics decision. The non-Hermiticity of the actual discrete A is expected and has two sources:

- (a) the discrete G (the 0438 projection and quadrature) is not the pointwise −∇·(ρU);
- (b) the supplied background does not exactly satisfy P = Kρ^γ, gradient consistency or thermal wind.

Neither source reflects an error in the contract's signs. Its size can serve root as a diagnostic. Symmetrizing A would be the forbidden "spectrum repair".

## 2. Oracle and checks (Task 2)

**`algebra_oracle_h1v001.py`** provides `oracle_A_b(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z, volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z, m, gamma) -> (A_unscaled, b_unscaled)`.

- It is built only from the closed forms in 1h, using `einsum('ij,i,ik->jk', conj(X), d, Y)`. It forms no VR..AZ, E or PM, and no diagonal or identity matrices.
- It also exposes `oracle_parts` (the m², m¹ and m⁰-radial terms, the m⁰ vertical-shear term, and the pressure/density part) and `pointwise_inertial_matrix` (M_p, shape (n,3,3)).
- Validation: dtype/shape/finite checks; complex rejected for the real vectors before any cast; `type(m) is int` with 1..6, which excludes bool; strictly positive R, ρ, P and w; inputs are copied and never modified.
- `gamma` is not forced to 5/3 in the oracle, because that is the implementation's check.
- Its first line follows the environment's numpy-path rule. It is meant for small fixtures; einsum with optimize=False is not intended for full-size arrays.

**`check_h1_oracle_v001.py`** was run with `/usr/bin/python3 -I -B` (Python 3.9.6, numpy 2.0.2) in about 0.3 s, exit code 0, and wrote no files. It contains a plain inline transcription of the contract chain, whose text was verified against the pinned JSON. Results:

| section | quantity | result |
|---|---|---|
| [0] | contract sha256 = pin; equations 1-10 = transcription | True; True |
| [A] | 72 cases: seeds 0-5 × shapes (7,3),(4,4) × m=1..6; Ω_R, Ω_z ∈ ±[0.2,0.8]; maps with O(1) imaginary parts | |
| [A] | max rel err A, oracle vs chain (max-abs / Frobenius) | **6.011e-16 / 3.631e-16** |
| [A] | max rel err b | **4.311e-16** |
| [A] | M_p·U vs chain (AR,AP,AZ), map level | 4.284e-16 |
| [A] | sensitivity: change of A when Ω_z→0 (min) | 5.272e-3 (vertical-shear term always resolvable) |
| [A] | sensitivity: inertial A with `.T` instead of `.conj().T` (min) | 0.5807 |
| [A] | oracle left inputs unmodified | True |
| [A2] | VR missing `[:,None]` at shapes (7,3) / (4,4) / (7,1) | ValueError / **silent, rel err 0.115** / **silent, A shape (1,7) instead of (1,1)** |
| [A2] | pressure weight missing `[:,None]` at (7,3) / (4,4) | ValueError / **silent, rel err 0.358** |
| [A2] | `divU.conj().T * w` (row vector over points) | correct, 1.7e-16 |
| [B] | Lindblad determinant identity | 1.993e-16 |
| [C] | FD δv / δa / continuity vs contract | 7.642e-12 / 9.346e-12 / 1.184e-11 |
| [C] | mutants VP+RΩ_z, VP+RΩ_R, AP−RΩ_zVZ, AR+2ΩVP, continuity (VP+RΩ_z) | ≥2.03e-2, ≥4.23e-2, ≥2.76e-2, ≥0.556, ≥4.40e-2 |
| [D] | pressure by parts under conjugation | 1.445e-15 (mutants: −im divU ≥1.28; bilinear ≥0.925) |
| [D] | weak density, complex and real ψ | 1.144e-14 (mutant +im ≥2.0) |
| [E] | FFT/16 coefficient; derivative = i m × coefficient; index 16−m = conj | φ_0=0: 1.5e-15, 1.4e-15, 7.3e-17; half-cell: 1.0e-15, 1.1e-15, 2.9e-16 |
| [F] | consistent-fixture Hermiticity of the full A | 3.439e-16 |
| [G] | w→2πw scales A and b by exactly 2π; maps independent of w | 4.412e-16; True |

**Mutant detection matrix.** Each value is the minimum over 36 cases. The baseline is 6e-16 for the oracle columns and 3.4e-16 for the Hermiticity column.

| mutant (one deliberate defect in the chain) | dev vs oracle A | dev vs oracle b | anti-Herm. on consistent fixture |
|---|---|---|---|
| no_test_conj (`.T` for every test map) | 0.580 | 0.729 | 1.09 |
| trial_conj (conj on U and G as trial) | 0.207 | 0.729 | 2.1e-2 |
| divU_unconj (`divU.T`) | 1.9e-2 | 0 | 1.9e-2 |
| minus_i_inertial (−im in VR..AZ) | 0.165 | 0 | **8.8e-17 (not detectable by Hermiticity)** |
| E_sign | 1.2e-2 | 0 | 1.8e-2 |
| PM_no_gamma (P/ρ for γP/ρ) | 2.3e-3 | 0 | 5.1e-3 |
| PM_rho_not_rho_gamma (ρ for ρ^γ) | 1.2e-3 | 0 | 1.1e-3 |
| VP_RR_sign | 4.8e-2 | 0 | 6.4e-2 |
| VP_Rz_sign | 3.0e-2 | 0 | 2.1e-2 |
| AR_coriolis_sign (+2ΩVP) | 0.133 | 0 | 0.155 |
| AP_RR_sign (2Ω−RΩ_R) | 3.9e-2 | 0 | 6.2e-2 |
| AP_Rz_sign (−RΩ_zVZ) | 2.9e-2 | 0 | 1.6e-2 |
| pressure_sign (+divU^H PM) | 2.2e-2 | 0 | 3.0e-2 |
| density_sign | 5.7e-3 | 0 | 3.6e-2 |
| density_rho2 (/ρ²) | 8.9e-4 | 0 | 6.9e-3 |
| rho_in_pressure (wρ in PM term) | 5.8e-3 | 0 | 5.7e-3 |
| vw_twice_inertial | 8.1e-2 | 0 | 9.8e-4 |
| no_vw_density | 4.0e-3 | 0 | 1.1e-2 |
| b_sign | 0 | 2.0 | 0 |
| f_phi_extra_im_over_R | 0 | 0.300 | 0 |

"0" in the table means at roundoff (≤ 8.3e-17). The oracle comparison detects all 20 mutants; the smallest margin is 8.9e-4 for /ρ², which is still 12 orders of magnitude above roundoff. The Hermiticity fixture detects 17 of the 18 A-mutants. It cannot see a consistent complex-conjugate convention in the inertial block, because −im keeps that block Hermitian.

## 3. Contract versus pinned prior v002, line by line (Task 3)

| item | v002 lines | status | note |
|---|---|---|---|
| E | L44 (KR,KZ from L40) | identical | Same expression; K_R, K_z are now supplied instead of DR@K, DZ@K. |
| PM | L44 | identical | `(rho**gamma)[:,None]` vs `rho[:,None]**gamma` give the same values. γ: hard-coded 5/3 at L39 vs supplied and validated. |
| VR | L45 | identical | W = Ω. |
| VP | L45 | identical | WR, WZ = DR@W, DZ@W (L40) vs supplied Omega_R, Omega_z; RR = R. |
| VZ | L45 | identical | |
| AR | L46 | identical | |
| AP | L47 | identical | |
| AZ | L48 | identical | |
| divU | L49 | equivalent | Computed internally with DR/DZ vs supplied map; same +1j·m·U_φ/R convention as helicity L64. |
| A inertial | L52 | identical | wrho = vol·ρ. |
| A pressure | L53 | identical | `−divU^H(vol·PM)`. |
| A density | L54 | identical | `(UR^H*(vol·PR/ρ)[None,:])@G` = U_R^H D(vol P_R/ρ) G. |
| G | L43 | **different (discretization)** | Lumped nodal adjoint weak divergence vs the 0438 consistent-mass projection. Same continuum equation and signs; different finite operator; intended (0438: old reconstruction "must not be reused on this mesh"). |
| b | L58 | identical (form) | Supplied f vs L57 gradients. |
| forcing | L55-57 | equivalent (root convention) | FFT/16 coefficient of e^{+imφ} of (angular_forcing_dPhi + lagged_feedback_Phi), then DR, i m/R, DZ. Root must supply f = ∇δΦ_m with f_phi = i m δΦ_m/R included. |
| volume weights | L39 | **different (global 2π scale only)** | L39 sums mesh weights over the 16 azimuthal cells, which includes the φ-integral's 2π. The new weights are R dR dz without 2π. A and b scale by 1/(2π); G, maps and solution unchanged. |
| normalization | L59-61 | equivalent | mass·aref·L vs supplied positive scalar; only A and b divided. |
| background derivatives | L40 (fields L38) | equivalent | DR/DZ on the old 8-node mesh vs supplied gradients. Form identical; values root-owned. |
| hard-constraint SVD, weak SVD rank test, solve, acceptance, strong/surface diagnostics | L26-29, L62-80 | different (removed by design) | The contract forbids solve, inverse, rank repair and tolerances. |

Assessment of the five known non-equation differences:

- **G construction.** This changes the finite operator, by design; it is neither a sign nor an equation discrepancy. Both constructions are conservative weak forms of δρ = −∇·(ρξ) with identical signs and zero-flux assumptions (§1g). Do not expect agreement with v002 numbers; the size of A's non-Hermitian part also changes (§1i).
- **Volume weights.** No operator change. On a common (R,z) quadrature, every A and b term is multiplied by the same constant (exactly one w per term). The 0438 projection is homogeneous of degree 0 in W (M and b are each linear in W), and v002 L43 divides vol back out, so G is unchanged; E, PM and the velocity maps carry no weight. The solution of A y = b is therefore unchanged (fixture [G]). Only absolute magnitudes of A/normalization_scale and b/normalization_scale, and any absolute-threshold diagnostics downstream, would see the 2π. H1 did not verify that the actual new weights equal the old ring weights divided by 2π on a common mesh (mesh arrays were not opened).
- **Forcing.** No operator change; b only. Equivalent if root supplies ∇δΦ_m (a potential gradient, not the acceleration −∇δΦ) in the FFT/16 e^{+imφ} convention, with f_phi already containing i m/R, and with native forcing and lagged feedback summed once. The module must use f_phi verbatim. The FFT phase reference e^{imφ_0} rotates b and y together and does not affect A (fixture [E]).
- **Normalization.** No operator change. A common positive scalar leaves y unchanged; the maps stay unscaled.
- **Background derivatives.** No change in form. P = Kρ^γ, gradient consistency and thermal wind are root responsibilities (§1e, §1i).

**Precise discrepancies in the contract:** none in its equations. One naming hazard: 0438's `VR`/`VZ` (scalar-basis derivative maps) and the contract's `VR`/`VZ` (velocity maps) share names.

## 4. Scope assumptions, not implementation defects (Task 4)

1. **Static pattern, ω = 0 in the inertial frame.** For a pattern speed Ω_p, replace imΩ by im(Ω − Ω_p) in VR, VP, VZ, AR, AP and AZ; 2Ω and the shear terms are unchanged. The contract covers Ω_p = 0 only.
2. **The axisymmetric equilibrium identity is used.** δρ[(v0·∇)v0 + ∇Φ0] is replaced by −δρ∇P/ρ. Any m = 0 equilibrium residual of the supplied background is not carried into the nonzero modes ("no m0 residual injected").
3. **P = Kρ^γ pointwise, with consistent gradients.** This includes P_R = ρ^γK_R + (γP/ρ)ρ_R, P_z likewise, and a thermal-wind-consistent Ω_z. PM presupposes these relations, and the Hermitian structure depends on them. They cannot be checked in the module because K and ∇ρ are not inputs.
4. **Zero surface terms.**
   - The pressure surface term ∮conj(U·n)δP is dropped. Its natural boundary condition is Eulerian δP = 0 on the free boundary. At R = L the hard constraint U_R = 0 removes the radial-face term; on the axis the factor R removes it.
   - The zero-flux density term ∮ρξ·n is dropped in G (0438).
   - These are continuum weak-domain assumptions. The routine does not certify boundary traces; v002 L69 computed the Lagrangian surface ΔP only as a diagnostic.
5. **A is non-Hermitian.** The vertical-shear m⁰ term 2wρRΩΩ_z (R,z) has no partner, and the discrete G is not pointwise. With exact relations, the continuum operator is Hermitian (§1i). Non-Hermiticity is therefore expected and must not be symmetrized away.
6. **Modal amplitude and phase conventions.** The FFT/16 coefficient c_m of a real field c_0 + Σ 2Re(c_m e^{imφ}) is referenced to the first sample's azimuth. y is in the same convention. Root's reconstruction and feedback must use the same convention.
7. **Join requirements.**
   - G must come from 0438 with mode = m, the same U columns, W = volume_weights, and the same ρ and R.
   - divU must be the divergence of the same U maps with +im (helicity L64).
   - The same maps serve as trial and test, the Galerkin condition.
8. **Linear theory.** Eulerian perturbations are taken at the unperturbed positions. δΦ is supplied (native forcing plus lagged feedback); it is not solved within A.

## 5. Code-review checklist for the frozen implementation (Task 5)

Each item can be checked against specific lines of the frozen file. `w` = volume_weights.

**Signature and validation**

1. **Signature.** `assemble_weak_euler` takes every input after a bare `*`, with no defaults. Check: for every parameter, `inspect.signature(...)` reports kind `KEYWORD_ONLY` and default `Parameter.empty`. There must be no `*args`/`**kwargs` that could swallow typos. Required names: R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z, volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z, m, gamma, normalization_scale, provenance.
2. **m.** Use `type(m) is int`, or reject `bool` explicitly before `isinstance(m, int)` (True is an int), and require `1 <= m <= 6`. If numpy integers are accepted, bool and `np.bool_` must still be rejected.
3. **gamma.** Reject bool, complex and non-finite values. Require exact `gamma == 5/3`, with no tolerance. The supplied γ, or the identical constant, must be used in both `gamma*P/rho` and `rho**gamma`. Watch for integer `5//3`.
4. **normalization_scale.** A real finite scalar `> 0`, with bool rejected.
5. **provenance.** A non-empty `str`.
6. **Real vectors.** Reject complex dtype before any cast: `np.asarray(x, float)` on complex input silently drops the imaginary part with only a ComplexWarning. Also reject bool/object dtypes. Require ndim 1 and shape `(npoints,)`, rejecting `(npoints,1)`. Require all values finite, and R, rho, P and w strictly `> 0`.
7. **Maps** U_R, U_phi, U_z, divU, G: ndim 2 with one common shape `(npoints, nfree)`, nfree ≥ 1, finite (`np.isfinite` on complex checks both parts). No `.real` or `abs` projection.
8. **Forcing vectors** f_R, f_phi, f_z: shape `(npoints,)`, finite, complex accepted. npoints must agree across every input.

**Equations**

9. **Conjugation on the test side only.** Every A and b term must be `X.conj().T @ (...)`, or an equivalent einsum with `np.conj` on the test index, for X ∈ {U_R, U_phi, U_z, divU}. Forbidden: `.T` without conj; conj on trial factors (AR, AP, AZ, PM, G, E, or U inside VR..VZ); conj of a whole product; `np.vdot`/`np.inner`. Fixture [A]: dropping the conj changes the inertial A by ≥ 0.58.
10. **Row broadcasting.** Every point-vector coefficient that multiplies an `(npoints,nfree)` map needs `[:,None]`. The contract has 15 such sites in E, PM and VR..AZ, plus the weight factors in the five A terms. Writing `X.conj().T * d` or `X.conj().T * d[None,:]` is correct, since it broadcasts over points.
    - A missing `[:,None]` raises an error only when npoints ≠ nfree.
    - When **npoints == nfree** the result is silently wrong (fixture [A2]: rel err 0.115 and 0.358).
    - When **nfree == 1** it silently produces an outer product, giving A of shape (1,npoints).
    - Require square and nfree = 1 fixtures, plus output-shape assertions: A `(nfree,nfree)`, b `(nfree,)`, maps `(npoints,nfree)`.
11. **Weights exactly once.**
    - Inertial terms use `w*rho`. The pressure term uses `w` only, with no ρ. Density terms use `w*P_R/rho` and `w*P_z/rho`. b terms use `w*rho`.
    - w must not appear in E, PM, VR, VP, VZ (or AR..AZ, if formed), and G must stay untouched.
    - There must be no extra 2π, R or annular factor; R is already inside w.
12. **Density term.** `-(U_R^H D(w P_R/rho) + U_z^H D(w P_z/rho)) @ G`: divide by `rho`, not `rho**2`; leading minus; uses G; no U_phi term.
13. **Pressure term.** `- divU.conj().T @ (w[:,None]*PM)`.
14. **Signs.**
    - Minus signs: E has two (`-K_R...-K_z...`); VP has `-(R*Omega_R)` and `-(R*Omega_z)`; AR has `-2*Omega*VP`; A has the divU term and the density bracket; b has all three terms.
    - Plus signs: PM (both terms); AP has `+(2*Omega+R*Omega_R)*VR` and `+(R*Omega_z)*VZ`.
15. **Imaginary unit.** `1j*m` in VR, the U_phi term of VP, VZ, AR, AP and AZ. Not `-1j*m` (Hermiticity cannot catch this; the oracle can, at 0.165), and not `m` alone.
16. **AP coefficient.** It is `(2*Omega + R*Omega_R)` and multiplies VR; it is not `2*Omega*R*Omega_R`. `R*Omega_z` multiplies VZ, not VR.
17. **PM.** `rho[:,None]**gamma*E`: ρ^γ, not ρ (oracle 1.2e-3) and not ρ^γ/ρ; the G coefficient is `gamma*P/rho`.
18. **f_phi verbatim.** No additional `1j*m/R` or `1/R`, no FFT, no re-differentiation (oracle detects 0.30).
19. **No extra forcing or equilibrium terms.** No m = 0 / Phi0 / equilibrium-residual / background-forcing term in A or b, and no δρ∇Φ0 term; the equilibrium identity absorbs it.
20. **G used exactly as supplied.** Not recomputed from U, re-projected, rescaled, conjugated, real-parted or symmetrized.
21. **Normalization.** Only `A/normalization_scale` and `b/normalization_scale`, as a division applied once. E, PM, VR, VP and VZ are returned unscaled. Inputs and G are not scaled.
22. **No symmetrization.** A must not be symmetrized or Hermitized (§1i).
23. **No input mutation.** No in-place `*=`/`-=`/`[...]=`/`out=` on arrays from `np.asarray(input)`, which aliases ndarray inputs. Fixture: compare deep copies before and after the call.

**Forbidden calls, imports and outputs**

24. **Forbidden-call scan.** Grep for `inv`, `pinv`, `solve`, `lstsq`, `svd`, `eig`, `eigh`, `eigvals`, `cond`, `matrix_rank`, `clip`, `diag`, `diagflat`, `eye`, `identity`, `nan_to_num`, `scipy`, any `where(` used as clipping, and `.real`/`np.real` on A, b or the maps. Note the false positive: "eig" occurs inside "volume_w-eig-hts".
25. **Imports.** numpy only, plus at most pure-stdlib validation helpers. No project modules, no I/O, no globals mutated, no randomness, no hidden callbacks or defaults.
26. **Economy.** No `(npoints, npoints)` intermediates: no `np.diag(w)`, no `np.outer` of point vectors, no `kron`. The cost should be O(npoints·nfree²).
27. **Returns.** A `(nfree,nfree)` complex, b `(nfree,)` complex, maps E, PM, VR, VP, VZ `(npoints,nfree)`, and provenance. No solution, acceptance flag or tolerance.
28. **One code path for all m.** The same m is used everywhere, with no hard-coded mode; modes 1..6 share one path.

**Fixtures**

29. **Fixture design.** Use complex maps with O(1) imaginary parts and Ω_z bounded away from zero; in fixture [A] the shear term is at least 0.5% of max|A|. Cover non-square, square and nfree = 1 shapes and all m = 1..6. Compare against the H1 oracle as `oracle_A_b(...)[0]/normalization_scale` and `[1]/normalization_scale`. The expected agreement is roundoff (~1e-15).

## 6. Limits of this note

- H1 inspected no Claude3 file. PASS/FAIL on the frozen implementation is the lead's consolidation, and H2 owns the manufactured cases against it.
- H1 inspected no actual mesh weights, maps, G or background. The 2π statement assumes a common (R,z) quadrature and is not verified on real arrays.
- The Hermiticity fixture uses a pointwise G, not the 0438 projection. It establishes the contract's sign consistency, not the size of the non-Hermiticity of a real assembly.
- The finite-difference and quadrature fixtures verify the continuum algebra. They do not address discretization accuracy, boundary traces, conditioning or physical admissibility.
