# ALGEBRA_K1_0448_V001: kinematic density map, algebra review

Lane: Claude4 review lane, dispatch 0448. Author: local helper **K1** (algebra). This is a helper note for the Claude4 lead. It is not an external-account response and not a physical verdict. Codex1 (root) owns physics, launches and acceptance.

What K1 did not do:
- read or run Claude3's module;
- import or run any project module;
- open galaxy data, solve outputs (finish.json and the like), calibration or target velocities, or validation outcomes.

The provider and the 0438 scalar-map module were read as text only. Every number below comes from the synthetic fixtures in `demo_pointwise_vs_weak_k1v001.py`, which sits next to this note.

## Sources

Hashes are from `shasum -a 256`. Every pinned file matches its pin.

| file | sha256 |
|---|---|
| `FROM_CODEX/0448_..._claude4_kinematic_density_review.md` | `99a0db72fa6cecfb6385f570ad517a0ad69387b15d0fade287e85a301cde7445` (pin) |
| `CODEX1/KINEMATIC_DENSITY_COMPARISON_CHOICE_V001.json` (root contract) | `9e4c070e88bf431cac9e001958016f9ca022f8cdef2c0c4f039fb7cd1128e14d` (pin) |
| `FROM_CODEX/0447_..._claude3_kinematic_density_map.md` | `5e2a5a52143896de3eebb94d399505cd18d6d3c969a58c5997d9cfca3c24a2fd` (no pin given) |
| `helpers/recovered_packet_audit/owned_32q8_physical_array_provider_v001.py` | `b530ca34a09b55f23d655ee6d23018942cdb6a51abec2c61a0d4231ac5a39fb6` (pin) |
| `helpers/coefficient_method/owned_free_surface_32q8trial_maps_v001.py` (0438 maps) | `3bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943` (pin) |
| `CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json` (0439 eqs 0-9) | `5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe` |
| `UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md` | `0500c1902f25cae550f87671df688e46286c68299d9493226e96bc1db2877094` |

Two earlier lane notes are reused, not repeated:
- (a) `weak_euler_review_0440/PARTIAL_REVIEW_0440_V002_MAP_STRUCTURE.md`, `dbf24adc…5ec1`;
- (b) `weak_euler_review_0440/ALGEBRA_SIGN_H1_V001.md`, §1d-1e and §1i, `b42bab82…251e`.

## 0. Findings

1. **There is no blocking issue in the contract formula.** `Gkin = -rho*divU - rho_R*U_R - rho_z*U_z` is exactly −∇·(ρξ) for ξ = U y with axisymmetric ρ under exp(+imφ):
   - the sign is right;
   - the form is cylindrical;
   - U_φ and ξ_R/R each appear only inside divU;
   - the perturbation is Eulerian.

   The finite-difference check agrees to 1.3e-10, and all five convention mutants are detected.
2. **PM reduction.** PM(Gkin) = −γP divU − P_R U_R − P_z U_z is an **algebraic identity of the provider construction** (L44-46). It holds whether or not P = Kρ^γ: the error is 2.2e-16 even with a 7.2% EOS violation. P = Kρ^γ matters only for the physical reading, and the identity cannot detect its failure.
3. **Pointwise continuity and the weak identity do not imply each other on their own.** Exact pointwise Gkin gives G_proj = Gkin only if three conditions hold: (i) discrete integration by parts is exact, (ii) the dropped boundary flux is zero, and (iii) Gkin lies in range(V). The weak identity never implies pointwise continuity. G_proj − Gkin splits exactly and W-orthogonally into an in-span defect and the out-of-span residual (§3). The 1-D demo shows:
   - roundoff-level agreement (1e-14) when all three conditions hold;
   - 0.31 to 1.48 from surface flux, and unbounded for a rigidly shifted uniform column;
   - 0.83 from out-of-span content alone;
   - 0.02 to 0.82 for the γ = 5/3 polytrope, where quadrature contributes only about 2e-4;
   - about δ for a relative gradient-input mismatch δ.
4. **Hermiticity diagnostic.** Build A with Gkin and the provider gradients. Then A − A^H = U_R^H D(d) U_z − U_z^H D(d) U_R, with d = wρ[R∂_z(Ω²) + (K_R/K)P_z/(γρ)] when P = Kρ^γ. This is verified to 2e-14, and A − A^H vanishes to 1e-16 at the fixed-K-column thermal wind. It diagnoses input consistency only.
5. Non-blocking notes are in §5: ρ_R must be the fixed-z partial, there is a 1-D map broadcasting hazard, and γ must be the same in both places. A per-component diagnostic for root is in §3.

## 1. Mass-advection identity (Task 1)

Take ρ = ρ(R,z) and ξ = (ξ_R, ξ_φ, ξ_z)(R,z) e^{imφ}, and use ∇·F = (1/R)∂_R(R F_R) + (1/R)∂_φ F_φ + ∂_z F_z. Term by term:

- (1/R)∂_R(Rρξ_R) = ρ(∂_Rξ_R + ξ_R/R) + ρ_R ξ_R
- (1/R)∂_φ(ρξ_φ) = ρ(im/R)ξ_φ + (ξ_φ/R)∂_φρ = ρ(im/R)ξ_φ, because ∂_φρ = 0
- ∂_z(ρξ_z) = ρ∂_zξ_z + ρ_z ξ_z

Summing gives ∇·(ρξ) = ρ divξ + ξ·∇ρ. Here divξ = ∂_Rξ_R + ξ_R/R + imξ_φ/R + ∂_zξ_z, which is helicity L64 as recorded in (a) and (b), and ∇ρ = (ρ_R, 0, ρ_z). With ξ = U y this gives −∇·(ρξ) = Gkin y.

- **No duplicate φ term.** ∇ρ has no φ component, so U_φ enters only through divU. Any U_φ term outside divU, such as a second −ρ imU_φ/R, would duplicate it.
- **No second ξ_R/R term.** ξ_R/R is the geometric part of (1/R)∂_R(Rρξ_R) and is already inside divU. The term ρ_R U_R is advection, not geometry.
- **Eulerian, not Lagrangian.** The Lagrangian change is Δρ = −ρ∇·ξ. The Eulerian change is δρ = Δρ − ξ·∇ρ = −∇·(ρξ). The 0439 equations need the Eulerian one, in two places:
  - PM = (γP/ρ)δρ + ρ^γ δK, where δK = E = −ξ·∇K is also Eulerian (b, §1e);
  - the density force −(δρ/ρ)∇P (b, §1d).

  With the Lagrangian −ρ divU instead, PM would lose −(γP/ρ)ξ·∇ρ and would be neither Eulerian nor Lagrangian δP.

**Demo [1].** The reference is a 3-D Cartesian 4th-order finite difference of ρξe^{imφ}, with analytic nonconstant ρ, complex ξ, m = 1, 2, 3, 6 and 64 random points. The maximum relative error is 1.3e-10. Minimum relative deviation of each mutant:

| mutant | min relative deviation |
|---|---|
| φ term added a second time | 0.65 |
| second ξ_R/R term | 0.23 |
| Lagrangian −ρ divξ only | 0.12 |
| exp(−imφ) sign | 1.29 |
| advection sign flipped | 0.24 |

## 2. EOS provenance and the PM reduction (Task 2)

**Where ρ_R and ρ_z come from (provider L42-47, read only):**
- K_R = K·logK_R, where logK_R is the saved per-column radial log-entropy derivative, shape (72,), broadcast along z.
- K_z = 0. The L44 comment calls this the fixed-K column law, not a fitted derivative.
- P_R = ρ·`rotation_pressure_R_over_rho` and P_z = ρ·`rotation_pressure_z_over_rho`. These are saved analytic lagged rotation relations, not derivatives of P0.
- ρ_R = (P_R − ρ^{5/3}K_R)/((5/3)P/ρ) and ρ_z = P_z/((5/3)P/ρ). These invert dP = ρ^γ dK + (γP/ρ)dρ, and they are exported at L47 as `rho_R` and `rho_z`.

**Algebra.** Insert G = Gkin into the 0439 equations PM = (γP/ρ)G + ρ^γ E and E = −K_R U_R − K_z U_z:

PM = −γP divU − [(γP/ρ)ρ_R + ρ^γ K_R] U_R − [(γP/ρ)ρ_z + ρ^γ K_z] U_z

The provider definitions give (γP/ρ)ρ_R = P_R − ρ^γ K_R and (γP/ρ)ρ_z = P_z, with K_z = 0. Therefore:

**PM(Gkin) = −γP divU − P_R U_R − P_z U_z**

This needs only three things: the same ρ, P, K_R, P_R and P_z arrays in both places; γ = 5/3 in PM, matching the provider's hard-coded value; and K_z = 0. **It does not need P = Kρ^γ.** Demo [2] gives 1.3e-16 with P = Kρ^γ, and 2.2e-16 with |P − Kρ^γ|/P up to 7.2%.

**When the result is the Eulerian adiabatic pressure perturbation.** The result equals δP = −γP∇·ξ − ξ·∇P of the background only if both of these hold:
- **(E1)** P = Kρ^γ on the supplied arrays. Only then is −γP∇·ξ the adiabatic Lagrangian ΔP, which is γKρ^{γ−1}Δρ = −γKρ^γ∇·ξ.
- **(E2)** (P_R, P_z) = ∇P.

**If (E1) fails** by ε = (P − Kρ^γ)/P:
- The identity still holds exactly, so it cannot detect the failure.
- PM's δρ coefficient γP/ρ differs from (∂P/∂ρ)_K = γKρ^{γ−1} by relative ε (demo: 7.2e-2).
- The provider ρ_R differs by (ρ/γ)(K_R/K)ε from a variant that uses P/K in place of ρ^γ. That variant breaks the identity: the demo deviation is 1.9e-2.
- The thermal-wind condition in §4 must use ρ^γ/P instead of 1/K.

**(E2) is not available,** because the lagged relations are not derivatives of P0.

**What Gkin certifies.**
- At each node p, Gkin_p = −∇·(ρ̂ξ)(x_p) for any differentiable ρ̂ with ρ̂(x_p) = ρ_p and ∇ρ̂(x_p) = (ρ_R,p, 0, ρ_z,p).
- Continuity and pressure use one gradient set. A Gkin-based pressure/density block therefore has the restructured form of note (b), with ∇P being the lagged (P_R, P_z).

**What Gkin does not certify.**
- That (ρ_R, ρ_z) is the gradient of the saved ρ0 between nodes or along a column.
- That it is curl-free, i.e. ∂_zρ_R = ∂_Rρ_z.
- That ρ̂ or ρ̂ξ·n vanishes at the free surfaces.
- That P = Kρ^γ, thermal wind or equilibrium holds.
- That the m1 response is right.
- That it agrees with G_proj.

The weak form integrates the node values of ρ by parts, while Gkin uses the supplied gradients. A strong/weak comparison therefore also tests whether those two are consistent (case D in §3).

## 3. Pointwise vs weak (Task 3)

**Notation.**
- Nodes p: 72 radii × 32 points.
- W = diag(w_p), with R dR dz weights and no 2π.
- ψ_a: the columns of V, the 0438 `value` map.
- VR and VZ: the 0438 `partial_R` and `partial_z` maps. These are fixed-z partials and include the affine term at L29.
- M = V^H W V.
- Weak functional, which is the 0438 b: ℓ_a = Σ_p w_p [∂_Rψ_a ρξ_R − imψ_a ρξ_φ/R + ∂_zψ_a ρξ_z]_p.
- L2(W) functional of Gkin: g = V^H W Gkin.
- G_proj = V M⁻¹ℓ and Π_V Gkin = V M⁻¹g.

**Exact decomposition.**

G_proj − Gkin = V M⁻¹(ℓ − g) + (Π_V − 1) Gkin

The two parts are W-orthogonal, because V^H W(Π_V − 1) = 0. Hence:

‖G_proj − Gkin‖²_W = ‖V M⁻¹(ℓ − g)‖²_W + ‖(1 − Π_V)Gkin‖²_W

The demo confirms this Pythagorean identity to below 1e-10.

The continuous identity is ∫∇ψ·ρξ dV = ∫ψ(−∇·ρξ) dV + ∮ψρξ·n dS, with the modal factor −im/R on the conjugated test side and no φ boundary. The three conditions:

- **(i) Discrete integration by parts.** Exact pointwise Gkin makes g a quadrature of ∫ψ(−∇·ρξ). But ℓ = g also requires the rule to integrate both integrands exactly.
  - **Vertical.** GL32 is exact to degree 63 in ζ; a 16+16 split rule is exact to degree 31. Exactness fails for non-polynomial ρ. For the γ = 5/3 polytrope, ρ_z behaves like (1−ζ²)^{1/2} at the ends, and the defect falls as N⁻³: 2.1e-4, 2.6e-5 and 3.2e-6 at N = 32, 64 and 128.
  - **Radial.** The 0438 test functions are natural-cubic cardinal splines in (R/R_out)², with nodal values and spline derivatives DR. Radial ℓ = g needs a summation-by-parts property of DR against the radial RdR weights, and the construction does not supply one in general. **The 1-D demo does not test the radial part.**
- **(ii) Dropped flux.** ∮ψρξ·n is dropped in three places:
  - on the free surfaces, which have no lid; n includes the surface slope through the affine term;
  - at R_out, as Rψρξ_R, where 0438 L31-33 supplies an outer normal-displacement trace of 8 coefficient rows;
  - at the axis, where Rψρξ_R → 0 for regular ξ.

  A flux f enters as the degree-7 reproducing kernel at the surface: V M⁻¹(ℓ − g) = f_top K₇(·, top) − f_bot K₇(·, bot), with K₇(1, 1) = 32/h. The demo matches this to 2e-14.
- **(iii) Span.** Even when ℓ = g, G_proj = Π_V Gkin, which differs from Gkin unless Gkin ∈ range(V).
  - V is block-diagonal by radius (0438 L25-27), so range(V) is, column by column, the space of degree-≤7 polynomials in ζ, and Π_V acts one column at a time.
  - Gkin goes beyond degree 7 in general whenever ρ varies along the column and the displacement uses its top degrees, or whenever ρ is non-polynomial.

**Forward direction.** Exact pointwise Gkin gives G_proj = Gkin if and only if ℓ = g, which needs (i) and (ii), and Gkin ∈ range(V), which is (iii). With (i) and (ii) alone, the whole difference is the out-of-span residual.

**Converse.** The weak identity V^H W G = ℓ fixes only 8 W-moments per column, 576 numbers for 2304 node values. W-orthogonal content is invisible to it:
- In demo E, adding a W-orthogonal field changes the 8 moments by only 4e-16, while the added field carries 0.83 of the norm of the random field it was built from.
- G_proj satisfies the weak identity by construction (1.5e-16) without being pointwise continuity.

Agreement of moments implies agreement at the nodes only when both fields lie in range(V).

**φ term.** The −imψρξ_φ/R term of ℓ and the φ part of g are equal node by node; no integration by parts is involved. A nonzero φ contribution to a computed defect therefore means an implementation or convention error, never a representation effect.

**Demo [3].** One column with 32 Gauss-Legendre nodes and P0..P7 in ζ = (z − c)/h, with c = 0.13, h = 0.71 and w = hω. In the table, rel = ‖G_proj − Gkin‖_W / ‖Gkin‖_W.

| case | rel | in-span part | out-of-span part |
|---|---|---|---|
| A1: ρ = 1−ζ², ξ_z degree 4 (Gkin degree 5) | 1.2e-14 | | |
| A2: ρ = 1−ζ², ξ_z degree 6 (Gkin degree 7) | 1.1e-14 | | |
| A3: ρ = 1−ζ², ξ_z = P7 (Gkin degree 8) | 0.832 | 1.6e-15 | 0.832 |
| B1: ρ = 1−0.8ζ² (surface value 0.2) | 1.484 | flux kernel, to 1.9e-14 | 3.4e-16 |
| B2: ρ = 1.05−ζ² (surface value 0.05) | 0.308 | flux kernel, to 2.4e-14 | 3.2e-16 |
| B3: ρ = 1, rigid ξ_z | unbounded: Gkin = 0, ‖G_proj‖_W = \|ξ_z\|√(72/h) | | |
| C1: ρ = (1−ζ²)^1.5, rigid ξ_z | 1.92e-2 | 2.1e-4 | 1.92e-2 |
| C2: ρ = (1−ζ²)^1.5, ξ_z ∝ ζ | 4.23e-2 | 2.8e-4 | 4.23e-2 |
| C3: ρ = (1−ζ²)^1.5, ξ_z ∝ P7 | 0.820 | 1.8e-4 | 0.820 |
| D: ρ = 1−ζ², supplied ρ_z × (1+δ), δ = 0.01 / 0.1 | 9.9e-3 / 9.3e-2 | all of it | 3.7e-16 |

- In B1 and B2, the P0 moment Σ_p w_p Gkin_p equals −[ρξ_z]_bot^top to 1.6e-14 and 8.1e-14.
- Changing the complex amplitude from 1 to 7.75e^{0.7i} leaves every relative difference unchanged, because the maps are linear. The size of a displacement does not matter here; its shape does, meaning its surface value and its top-degree content.
- With an illustrative 16+16 split rule at ζ = 0 (the actual split location was not inspected), C1 gives 1.83e-2.

**Classes of effect that can make the strong/weak difference large.** No claim is made about which of these, if any, produces the project value of 6.339.
1. **Normal mass flux at an edge of the weak domain.** This arises at a free surface where ρ̂ξ·n ≠ 0 at the trial-domain edge, and also at the outer trace or the axis. Relative to Gkin it is unbounded.
2. **Out-of-span content of Gkin,** meaning vertical degree above 7. It reaches about 0.8 here for degree-7 displacement shapes, with either polynomial or polytropic ρ.
3. **Inconsistency between the supplied (ρ_R, ρ_z) and the ρ node values.** The relative difference is about equal to the relative mismatch.
4. **Defects in discrete integration by parts.** The vertical quadrature part is small here: at most 3e-4 for the polytrope at N = 32. The radial spline/RdR summation-by-parts defect was not tested and is not bounded by this note.

**Actionable diagnostic for root.** This is comparison only; it changes nothing in G, A, source or weights, and it needs only the existing 8×8 blocks with no ridge. At the actual 32q points, compute:
- the out-of-span part, ‖(1 − Π_V)Gkin‖_W;
- the in-span defect by component:
  - δ_R = VR^H W ρU_R − V^H W[−ρ(∂_RU_R + U_R/R) − ρ_R U_R];
  - δ_z = VZ^H W ρU_z − V^H W[−ρ∂_zU_z − ρ_z U_z];
  - δ_φ, which should be zero exactly.

Then ‖G_proj − Gkin‖²_W = ‖V M⁻¹(δ_R + δ_z)‖²_W + ‖(1 − Π_V)Gkin‖²_W, which divides the measured G_proj − Gkin difference between radial, vertical and span classes. K1 does not know how the earlier 6.339 "strong" density was defined, so this split applies to the new Gkin comparison only.

The P0 entry of δ_z for each column is Σ_l w_l(ρ∂_zU_z + ρ_zU_z), because the P0 column of VZ is zero. It equals that column's net vertical surface flux plus quadrature and gradient-input error.

## 4. Hermiticity diagnostic (Task 4)

**Specializing (b), §1i.** For the provider gradients with K_z = 0, the relations P_R = ρ^γK_R + (γP/ρ)ρ_R and P_z = (γP/ρ)ρ_z hold identically, so the restructured form of (b) applies whenever G = Gkin. The only anti-Hermitian slots are U_R^H U_z and U_z^H U_R:

A − A^H = U_R^H D(d) U_z − U_z^H D(d) U_R, with d = w[2ρRΩΩ_z + (P_Rρ_z − P_zρ_R)/ρ]

The provider gradients give P_Rρ_z − P_zρ_R = ρ^{γ+1}K_R P_z/(γP). Therefore:

**d = wρ[R∂_z(Ω²) + (ρ^γ/P) K_R P_z/(γρ)]**, which becomes **wρ[R∂_z(Ω²) + (K_R/K) P_z/(γρ)]** when P = Kρ^γ.

Since w > 0 and ρ > 0, d vanishes at a point if and only if **R∂_z(Ω²) = −(K_R/K) P_z/(γρ)**. This is the fixed-K-column thermal wind, with ρ^γ/P in place of 1/K if P ≠ Kρ^γ. Note that K_R/K = logK_R is constant along each column.

**Demo [4].** 24 random pointwise cases: 13 points × 5 columns, m = 1..6, independent complex U_R, U_φ, U_z and divU, and A built from a fresh transcription of 0439 equations 0-8.

| case | result |
|---|---|
| prediction of A − A^H | matches to 2.0e-14 |
| generic random Ω_z | ‖antiH‖/‖A‖ ≥ 3.8e-3 |
| thermal wind, both forms, P = Kρ^γ | 1.2e-16 |
| 5% EOS violation, ρ^γ/P form | 1.4e-16 |
| 5% EOS violation, K_R/K form | leaves exactly −w(K_R/K)(P_z/γ)ε, matched to 5.9e-12; size 1e-5 to 2e-4 of ‖A‖ |
| at thermal wind, Lagrangian G | 2.7e-3 |
| at thermal wind, duplicated φ term | 4.4e-2 |
| at thermal wind, 5% non-pointwise perturbation of G | 3.6e-4 |

**Use.** Two pointwise quantities can be computed from the provider arrays, with no assembly or solve:
- τ_p = R∂_z(Ω²) + (ρ^γ/P)K_R P_z/(γρ);
- ε_p = (P − Kρ^γ)/P.

They measure whether the lagged rotation relations are consistent with the fixed-K EOS. With Gkin, the anti-Hermitian part of A is exactly ½[U_R^H D(wρτ) U_z − h.c.]. With G_proj, the difference G_proj − Gkin adds further non-Hermitian terms. This is a diagnostic only:
- no symmetrization;
- no claim that the background is in equilibrium;
- no claim that a Hermitian A would be physically correct.

## 5. Contract formula: blocking issues (Task 5)

**None found.** The sign, the terms, the cylindrical form, the exp(+imφ) convention, the Eulerian character and the `[:,None]` row broadcasting are all correct for (npoints,) vectors and (npoints, nfree) maps.

Non-blocking items for the lead and root:
1. **ρ_R must be ∂ρ/∂R at fixed z,** as in divU (0438 `partial_R` includes the fixed-z affine correction). The lagged P_R is assumed to be the fixed-z partial. K1 did not check how `rotation_pressure_R_over_rho` was produced.
2. **The formula assumes 2-D maps.** For a 1-D map of shape (n,), `rho[:,None]*divU` silently broadcasts to (n, n); this was checked in numpy. Shape validation in the module must reject 1-D maps. This belongs to the implementation review.
3. **γ in PM must equal the provider's hard-coded 5/3** for the §2 identity to be exact.
4. **Scope is preserved.** Gkin is a comparison object. G_proj and the 0439 A remain the preserved weak representation.

## 6. Reproduction

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kinematic_density_review_0448/demo_pointwise_vs_weak_k1v001.py
```

| interpreter | result |
|---|---|
| Python 3.12.14, numpy 2.3.5 | exit 0, "ALL CHECKS PASS", well under 1 s, no warnings |
| `/usr/bin/python3` 3.9.6, numpy 2.0.2 | exit 0, all checks pass, same results within roundoff |

Under 3.9.6/numpy 2.0.2, numpy emits RuntimeWarnings (divide by zero, overflow, invalid value) inside the small matmuls, although every result is finite and every check passes.

The script uses a fixed seed (448). It reads no files, writes no files and imports only numpy. Its sha256 is `f13a63b7a2cc2d1d036c1295dc704cf8018245ed5896a18b2911e4d5f0b73836`. This note's own hash is given in K1's structured return.
