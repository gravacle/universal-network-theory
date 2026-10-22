# ALGEBRA_N1_0451_V001 — N1 algebra and numerics for the 0451 annular-knot review

Author: N1, a local helper in the Claude4 review lane (not an external account), 2026-10-16. Synthetic analytic fixtures only. No project data, outputs, runs, or field or parameter searches. Claude3's files were read, never edited.

## Pins read

**Verified.**
- Root contract `ANNULAR_KNOT_RADIAL_CORRECTION_CHOICE_V001.json`: `58ffcbb86cd6512bb02ddf384a593311d1a9483f73f0cd83633432a9f5ef073e`.
- References:
  - v001 scalar maps: `3bd792ba…`
  - v001 helicity: `280149dc…`
  - binding v002: `87866875…`. This is the only reference loaded, and only on synthetic data.

**Code text only.** Neither file was run, and none of their outputs were opened:
- Root IBP diagnostic `ddo32q8_integration_by_parts_diagnostic_root_v001.py`: `c399bfc5181d755210942d09312ec64f0c778568d8adecacd3a81ba7c32b1ae4`.
- Root draft `ddo32q8_annular_knot_modal_assembly_root_DRAFT_v002.py`: `af815358fce8b25f99a4afe851970f5f519b4d38bafc276e3d5f564a792cfb6d`.

**Under review.** `annular_knot_maps_c3v001.py`, `23bb22fb94c3a6b39b84479a1c5e03812fbcdeaf6180ca85ddad083a3d3d92c4`. These are the frozen bytes per FROM_CLAUDE3 0005.

**Files.**
- `oracle_n1v001.py`: inert, numpy only. SHA-256 `1bbce209437ec048a67618f812171e5a5beb34dcaf1756d2483bc51354ecaec8`.
- `check_n1v001.py`: prints one JSON summary and writes nothing. SHA-256 `437710413d5bcfa896b8ded65f0f09eeac41c22616096e5c04dfea7d8c3e26d0`.

Reproduce with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 <root python3> -I -B check_n1v001.py [c3_path c3_sha256]` (about 3 s). Every number below comes from that output.

## Headline

1. **No defect found in c3v001 (23bb22fb) on the algebra and numerics side.** My independent oracle agrees with it to about 1e-15 (section 5).
2. **Root's own radial metric will not reach roundoff after this correction. That is expected, not an implementation failure.**
   - Root's `radial_scalar_SBP` (diagnostic v001 L38-41, regeneralized in draft v002 L71-72) is the cylindrical R-form: ∫(R(uv)' + uv) dR = [Ruv].
   - In s its integrand is d/ds[s^{1/2} B_i B_j], which is not a polynomial.
   - With annular knots, this metric is ≈ **0.051·√t1 = 0.051·R1/L**, where R1 is the first annular edge (`annular_edges_R_m[1]`).
     - Synthetic layouts with 18 annuli give 0.85e-2 to 1.2e-2.
     - Old-style knots at the nodes, in root's exact formula, give 0.83 to 0.88.
     - The s-form identity becomes 1.0e-14 to 1.4e-14.
   - The residual is the first-annulus axis quadrature of the pinned GL-in-s R dR rule.
     - The (0,0) entry carries more than 99.4% of it.
     - Integrating annulus 0 alone with 8-point GL in r = √s leaves 1.6e-6.
   - The m=1 fluid radial identity has the same e=0 axis structure.

## 1. Edge recovery

**Gauss-Legendre constants.** GL4 on [-1,1] has nodes X = (−x2, −x1, x1, x2) and weights W = (W2, W1, W1, W2), with:
- x1 = √(3/7 − (2/7)√(6/5)) and x2 = √(3/7 + (2/7)√(6/5));
- W1 = (18 + √30)/36 and W2 = (18 − √30)/36;
- x1² + x2² = 6/7 and ΣW = 2.

**Nodes and weights of annulus k = [a,b] in s.**
- Nodes: s_i = c + hX_i, where c = (a+b)/2 and h = (b−a)/2.
- Weights: since R dR = (L²/2) ds, each weight is w_i = (L²/2)hW_i = (L²/4)(b−a)W_i.

**Closed-form recovery.**
- c = (s0+s1+s2+s3)/4, which holds because ΣX = 0.
- h = [x2(s3−s0) + x1(s2−s1)] / (2(x1²+x2²)) = 7[x2(s3−s0) + x1(s2−s1)]/12. This is the least-squares fit, (g·X)/(X·X).

**Redundant checks.** All are absolute in s, with ŵ = 2w/L², which sums to 1:
- all 4 node residuals |s_i − c − hX_i|, which covers both symmetry and the x1:x2 ratio;
- 17 adjacent-edge differences |b_k − a_{k+1}|;
- |a_0|, the s0 = 0 check;
- |b_17 − 1|, the s18 = 1 check;
- |ŵ_i − h_k W_i|, the weights check (c3 uses the equivalent relative form);
- optionally, independent weight-only edges t_k = Σ_{groups<k} Σ_i ŵ. The last of these, t_18 = 1, is v001's Σw = L²/2.

**Knots.** Use [0, (b_k + a_{k+1})/2, 1], with an exactly representable 0 and 1. The helper then gives a = 0 and b = 1 exactly at s = 1, so the trace is exactly e_18.

**Tolerance.**
- s = (R/L)² carries at most about 3 ulp, and the recovered c and h inherit a few ulp.
- **Measured worst case:** 3 eps (6.7e-16 in s) over 20 seeds and two pipelines, direct and kpc²-to-metres. The knot error versus truth is at most 3.3e-16.
- **Recommended absolute tolerance in s:** 64 eps = 1.42e-14.
- **Root draft's 1e-12 for both c3 tolerances is also defensible.**
  - It is at least 1500 times the synthetic edge floor.
  - It is 60 to 130 times c3's relative-weight floor (7.5e-15 to 1.7e-14). That floor scales as about (a few 1e-16)/Δs_min, so it reaches 1e-12 only for an annulus narrower than about 4e-4 in s.
  - It is at least 9 orders below a structural mismatch. A GL-in-R grid gives residuals of 3e-5 to 5.6e-3, and is rejected.

**Fail closed.** Raise with every residual. Do not fall back to the old knots, repair, refit or default the tolerances.
- The oracle rejects a GL-in-R grid, a node changed by a relative 1e-10, weights multiplied by (1 + 1e-9), and groups shifted by one node.
- c3 L139-166 conforms. On synthetic data it reports node 2.2e-16, adjacency 2.2e-16, s0 6.9e-18 and s18 ≤ 2.2e-16.

## 2. What the annular knots make exact, and what they do not

**Change of variables.**
- R = L s^{1/2}
- R dR = (L²/2) ds
- dR = (L/2) s^{−1/2} ds
- ∂_R|_ζ = (2/L) s^{1/2} ∂_s
- 1/R = s^{−1/2}/L
- (R/L)^e = s^{e/2}

**Exactness rule.** On each annulus, 4-point GL in s is exact for polynomials of degree ≤ 7. Write each full integrand, measure included, as s^{p/2}·q(s), with q a polynomial on each annulus. The integral is exact if and only if p is even and the total degree is ≤ 7. When p is negative and odd, the integrand is singular at the axis.

**Old versus annular knots.**
- Annular knots make each B_j a single cubic on every annulus.
- Knots placed at the nodes break that cubic inside every GL group. The nodal basis also has V = I, which lumps the mass and leaves diag(w)D + Dᵀdiag(w) far from the boundary term.

**Exact with annular knots:**
- the s-form SBP, Σŵ(B_i′B_j + B_iB_j′) = δ_{i18}δ_{j18} − δ_{i0}δ_{j0} (degree 5). This is the same as the planar form Σ(w/R)∂_R(B_iB_j).
- the radial mass, (L²/2)ΣŵB_iB_j (degree 6).
- the radial stiffness, Σw ∂_R B_i ∂_R B_j = 2Σŵ s B_i′B_j′ (degree 5).
- the moment Σŵ s B_iB_j (degree 7).

**Not exact:**
- Σw ∂_R B_i B_j = LΣŵ s^{1/2} B_i′B_j (p = 1).
- Σ(w/R)B_iB_j = (L/2)Σŵ s^{−1/2} B_iB_j (p = −1, singular at the axis).
- Root's cylindrical identity, which is the sum of the two.

**Regularity powers.** Take the cylindrical radial identity with trial (R/L)^e B_j and test B_i, in a flat slab with constant density. Its integrand is d/ds[s^{(e+1)/2} B_iB_j], which is exact if and only if e is odd and e ≤ 3.
- Measured on 18 uniform annuli:
  - e=0: 1.2e-2
  - e=1: 1.2e-14
  - e=2: 1.4e-5
  - e=3: 1.1e-14
  - e=4: 2.4e-7
  - e=5: 4.3e-7
- Mapped onto the helicity radial exponents (|m+1|, |m−1|):
  - m=1 uses (2,0), which includes the axis-singular e=0.
  - m=2 uses (3,1), exact only in this proxy.
  - m=3..6 are not exact.

**Other non-polynomial factors.**
- **Body-fitted geometry.** The measure carries h(s), and ∂_R carries −(c_R + ζh_R)/h·∂_ζ.
  - The vertical IBP is exact at each radial node (ζ-polynomials; root measured 2.0e-15).
  - The 2D radial identity would need ∂_s(hRF) integrated exactly, with h_R the exact derivative of h. The preserved v001 slopes come from the 72-knot nodal spline, so it is not exact.
- **Physical fields** (ρ, ρ_R, ρ_z, P, K, Ω). B_iB_j already uses degree 6 of the 7 available, so any weight that varies beyond linearly in s is inexact. Synthetic examples: exp(−s/0.1) gives 7.5e-6, and (1−s)^{3/2} gives 1.4e-5.

**Measured values.** The table uses root's normalization, ‖D‖_F/(‖lhs‖_F + ‖bnd‖_F):

| synthetic 18 annuli | old knots at nodes: s-form / root R-form | annular: s-form / root R-form |
|---|---|---|
| uniform | 0.828 / 0.828 | 1.0e-14 / 1.20e-2 |
| random, seed 7 | 0.881 / 0.879 | 1.3e-14 / 1.06e-2 |
| random, seed 11 | 0.872 / 0.852 | 1.4e-14 / 8.5e-3 |

**Scaling of the annular root R-form.**
- The ratio to √t1 is 0.0506 to 0.0512 over 12 random layouts plus a layout uniform in R. The uniform-in-R layout itself gives 2.8e-3.
- Under uniform refinement, N = 18, 36, 72 and 144 give 1.20e-2, 8.46e-3, 5.98e-3 and 4.23e-3, an O(R1/L) decrease.
- The leading term is ½·0.0968·√t1. Here 0.0968 is the GL4 relative error of ∫₀¹u^{−1/2} du (1.80634 against 2).
- The single (0,0) entry gives |D00|/‖D‖ ≥ 0.994.

The 0.83 to 0.88 for old-style knots has the same order as root's measured 0.7938 and is consistent with the nodal-basis mechanism. It does not reproduce root's value: the geometry differs, and I did not read finish.json.

**Consequences for root.**
- (a) The s-form, equivalently the planar dR radial SBP, is the roundoff-level check of spline-quadrature compatibility; expect about 1e-14.
- (b) Expect the cylindrical `radial_scalar_SBP` to come out near 0.05·R1/L. A value well above that would be a real signal.
- (c) Expect the m=1 fluid radial identity to stay above roundoff. The e=0 axis term, ρ, the geometry and the degree limit all contribute. Its axis part falls only as O(R1/L) with radial refinement. The project value cannot be predicted from here.
- (d) Making the axis terms exact would require a different radial quadrature, such as GL in r on annulus 0, which is outside 0451's same-grid contract. This is attribution only, not a recommendation.

## 3. Chain rule

With ζ = (z − c(R))/h(R):
- ∂ζ/∂R|_z = −(c_R + ζh_R)/h
- ∂ζ/∂z = 1/h
- ds/dR = 2R/L²

The derivatives of the scalar map follow:
- ∂_R V = B_j′(s)(2R/L²)P_a − B_j P_a′(c_R + ζh_R)/h
- ∂_z V = B_j P_a′/h

For the helicity maps:
- ∂_R[(R/L)^e V] = (R/L)^e ∂_R V + (e/R)(R/L)^e V
- ∂_z[(R/L)^e V] = (R/L)^e ∂_z V

**Finite-difference check.** Central differences with Richardson extrapolation, step 1e-4·L. The stencil stays inside each annulus; the minimum node-to-knot gap is 8.1e-4·L. Analytic c and h are used, with their exact derivatives.
- V: ∂_R 7.4e-11, ∂_z 3.8e-11.
- Helicity, m=1..6: ∂_R U* ≤ 9.7e-11, ∂_z U* ≤ 4.0e-11, divU ≤ 6.0e-11.
- U_R at R = L is ≤ 9.9e-17 relative.

These formulas are exact derivatives only when the supplied c_R and h_R are the derivatives of the c and h that define ζ. In the project they are the preserved v001 nodal-spline slopes (contract item 3).

## 4. Dimensions and helicity

- **Scalar maps.** 19 knots × 8 Legendre gives 152 coefficients (index j·8+a), and the rows are i·32+l. V is 2304×152 with rank 152.
- **Outer trace.** B_j(1) = δ_{j18}, so T = kron(e_18ᵀ, I8) is 8×152, bitwise.
- **Raw helicity.**
  - The raw space is 3×152 = 456 with Braw = [½T, ½T, 0] (v001 L36). At R = L, (R/L)^e = 1, so these 8 rows are exactly ξ_R(L,ζ) = 0 as a degree-7 polynomial. There is no ξ_z lid.
  - Rows of B = Braw·diag(1/n) have disjoint supports at columns 144+a and 296+a. So σ_a = ½(n₊⁻² + n₋⁻²)^{1/2} > 0, and the rank is always 8.
  - span(raw_transform) = null(Braw) = {c₊[18,a] = −c₋[18,a]}, independent of the normalization.
- **Reduced space.** 456 − 8 = 448. Z is 456×448 and the maps are 2304×448. Measured for m=1..6:
  - BZ ≤ 2.2e-16
  - ZᵀZ − I ≤ 3.3e-16
  - ‖Braw·raw‖/(‖Braw‖‖raw‖) ≤ 1.4e-18
- **Unchanged.** The exponents (|m+1|, |m−1|, |m|), the one raw_transform = Z/n shared by every U, ∂U and divU, and the slices [:n], [n:2n], [2n:].

## 5. Oracle (`oracle_n1v001.py`)

**API.** All arguments are keyword-only and the module is inert:
- `recover_annular_edges`
- `natural_cubic_cardinal` / `evaluate_cardinal`, in the Hermite slope form, with exact unit rows at the knots and no extrapolation unless requested
- `legendre`, by recurrences
- `nodal_radial_derivative`, the v001 definition
- `annular_scalar_maps`
- `regular_helicity_maps`, with `nullspace='qr'|'eigh'`
- `scalar_basis_at` and `helicity_fields_at`, for finite differences

**Self-checks against the pinned helper.**
- Annular knots: values 5.0e-16 absolute, derivatives 5.6e-16 relative. Both give the exact e_18 at s = 1.
- The 72 nodal knots, with 0 and 1 extrapolated: 1.4e-14 and 6.2e-14 relative.
- Legendre against legvander/legder: P 9.5e-16; P′ 1.4e-14 absolute (|P7′(±1)| = 28).
- GL4 closed form against leggauss: 5.6e-17 and 3.9e-16.

**The QR nullspace is not unique, so compare products.**
- LAPACK's wide-matrix SVD reuses the Householder LQ and reproduces the QR basis bitwise, so it is no test.
- An eigh basis differs from the QR basis by O(1) in its raw columns. Yet X·Zᵀ agrees to ≤ 3.1e-15 for all ten maps and raw_transform.
- So compare X·Zᵀ, B·Z and the spans, never the raw Z columns.

**Oracle against frozen c3v001.** Two synthetic geometries: L = 2.5 direct, and kpc² to metres with L ≈ 2.25e20 m.
- Edges agree to 5.6e-17. V, ∂_R V and ∂_z V agree to ≤ 1.9e-15, and radial_value and radial_derivative to ≤ 1.8e-15.
- The outer trace is bitwise equal. weights_RdRdz, zeta, roots and root derivatives are preserved bitwise.
- The surface traces equal kron(B, (∓1)^a) to 1.2e-15.
- Helicity, m=1..6:
  - All return REGULAR_HELICITY_MAPS, with shapes (2304,448) and (456,448). The exponents are equal and Braw is bitwise equal.
  - Column norms agree to ≤ 1.3e-15, and X·Zᵀ to ≤ 2.6e-15.
  - c3's hard residual is ≤ 2.2e-16.
  - dtypes: UR and UZ are float64; UP and divU are complex128.

## 6. Code-review checklist for c3v001 (observed in the 23bb22fb bytes)

- [x] Edge recovery fails closed. Tolerances are explicit and root-supplied, with no defaults (L89-92, L139-166). Residuals are returned in `edge_recovery`.
- [x] Knots are exactly [0, the interior midpoints, 1] (L157-159), and the edges are strictly increasing (L160).
- [x] The helper is called as `_spline_matrices(edges, s + [1.0])` (L169). Every evaluation point lies in (0,1), so there is no extrapolation. The exact e_18 trace is asserted (L177).
- [x] dB/dR = (2R/L²)·dB/ds (L175). The chain-rule maps are at L182-186, with shape 2304×152, rows i·32+l and columns j·8+a (L187).
- [x] The v001 geometry is preserved bitwise (L110-131, L191-192). center_R and height_R come from the v001 72×72 DR.
  - Note: the exact-equality custody checks (the legvander blocks and the einsum root derivatives) need the same numpy that produced the stored v001 arrays. Otherwise they fail closed.
- [x] Legendre degree 7, with the v001 expressions (L121-123).
- [x] Helicity is generalized only in n: the slices are [:n], [n:2n] and [2n:]; Braw = [.5T, .5T, 0]; Z = Q[:, 8:]; the SVD threshold rule is unchanged (L261-329).
  - The exponents are the same, and the norms come from the new stacked dimensionless maps.
  - There is no lid, and one raw_transform is shared by every map.
- [x] The same returned names, with trial_shape [19,8] and quadrature_shape [72,32]. The new keys are documented.
  - `radial_derivative` is now 72×19. Its meaning (basis d/dR at the nodes) is unchanged, and root's draft consumes it as such.
  - The surface traces are now kron(B, ·), 72×152, which are the values at the 72 nodes.
- [x] V is not block-diagonal, and this is documented. Root must not reuse the nodal 8×8 slicing at v001 diagnostic L44 on these maps. Root draft v002 does not.
- [x] No density projection, solve, symmetrization, ridge or physics (the lead's AST check plus my reading).

## Limitations

- **Synthetic geometry only.** The project's first annular width, and the values its metrics will actually take, are unknown to me. Root can evaluate 0.051·R1/L from the returned edges.
- **Source of root's metric definition.** It is read from code text that I did not run.
- **The oracle implements the contract's construction independently.** That checks the implementation against the specification, not whether the specification is physically adequate.
