# REVIEW_0451_V001 addendum: supplementary helper results and expectations for root's diagnostic

Claude4, 2026-10-16, about 20:30 UTC. REVIEW_0451_V001.md (4a6b6d7285177e08871070e22afbff0a37677bfd3aaa93817c8c86c1ab85af15) stays as posted. **The verdict is still PASS, with no defects, on 23bb22fb94c3a6b39b84479a1c5e03812fbcdeaf6180ca85ddad083a3d3d92c4.**

## Supplementary confirmations

- **N1, independent oracle.** N1 wrote its own Hermite-form natural cubic spline, Legendre recurrences and closed-form GL4 recovery. Against the frozen module: edges 5.6e-17; V, d_R V and d_z V at most 1.9e-15; outer trace and preserved arrays bitwise. For helicity m = 1..6, the projected maps agree to at most 2.6e-15. The comparison is made through products with Z^T, because the QR basis is not unique.
- **N2, synthetic-geometry harness.** Three geometries (L = 3, 2.5e20 and 0.7; split and plain z panels): **390 pass, 20 info, 0 fail**.
  - Chain-rule finite differences: d_R V 3.9e-9, d_z V 1.4e-10, physical fields 6.2e-9.
  - All ten maps equal the raw maps times the one returned transform, to 5.7e-14.
  - Fail-closed behavior: 69 of 69. The mutation study detected 14 of 14.
- Neither helper found a defect.

## Expectations for root's next diagnostic (not defects)

1. **Root's radial IBP metric will not reach roundoff with the annular knots.** N1 read root's IBP-diagnostic code text only: v001 L38-41 and draft v002 L71-72. root's radial_scalar_SBP is the cylindrical R-form, with integrand d/ds[s^(1/2) B_i B_j].
   - With annular knots it is about **0.051 R1/L**: 0.85e-2 to 1.2e-2 on synthetic grids, and 2.8e-3 for edges uniform in R. With the old knots it is 0.83 to 0.88, consistent with root's measured 0.79.
   - **At least 99.4% comes from the axis annulus.** The s^(-1/2) behaviour near R = 0 is not polynomial in s. Lead check: GL4 on [0,1] gives the integral of u^(-1/2) as 1.806 instead of 2, a 9.7% error, while polynomial integrands are exact.
   - It decreases only as O(R1/L) under refinement: 1.20e-2, 8.46e-3, 5.98e-3, 4.23e-3 at N = 18, 36, 72, 144.
   - The roundoff-level check of the knot fix is the **s-form**, equivalently the planar dR summation-by-parts identity: about 1e-14.
   - On a synthetic grid, replacing only annulus 0 with 8-point Gauss-Legendre in r = sqrt(s) reduces the R-form defect to 1.6e-6. That changes the physical radial quadrature, which is outside the 0451 same-grid contract, so it is root's decision.
2. **The m = 1 fluid radial identity contains the |m-1| = 0 regularity component.** That component has the same axis-singular structure; a flat-slab proxy gives 1.2e-2. Odd e <= 3 is exact in that proxy; e = 2 gives 1.4e-5 and e = 4 gives 2.4e-7. The physical fields, the body-fitted h(s) and the preserved 72-knot root slopes add further non-polynomial error. Expect the m = 1 radial residual to stay above roundoff and to decrease only slowly with refinement.
3. **Do not reuse v001's block slicing.** Root's v001 IBP diagnostic at L44 slices nodal 8x8 blocks (columns 8i:8i+8). That is invalid for the annular maps, because V is not block diagonal. Root's draft v002 does not reuse it.
4. **Tolerances.** Root's 1e-12 for both `edge_absolute_tolerance` and `weight_relative_tolerance` is appropriate. Do not tighten the weight tolerance to about 64 eps:
   - The L134-137 custody check shares that tolerance and would refuse a valid v001 packet whose z-weight sums are off by 5e-13, which is inside v001's own rtol of 1e-12.
   - The L162-166 residual floor scales as about eps * s/delta s, so an annulus narrower than about 4e-4 in s would need a looser value.
5. **Same numpy for the old maps.** The module's exact custody equalities (legvander blocks at L125 and root derivatives at L130) need the same numpy that produced the stored v001 arrays. Build the old maps with the root interpreter. A mismatch fails closed, not silently.
6. **Preserved geometry slopes.** On nonlinear synthetic geometries, the preserved v001 72-node root derivatives (contract item 3) differ from the analytic geometry derivative by about 3e-3 to 4e-3 of max|d_R V|. This is a remaining approximation, retained by the contract.

## Files (SHA-256)

| File | SHA-256 |
|---|---|
| ALGEBRA_N1_0451_V001.md | 2e4db9b01f6c7ac7d73092b7ce0f0c12e98c0347cd1ba6af0e82a2d87eb89852 |
| oracle_n1v001.py | 1bbce209437ec048a67618f812171e5a5beb34dcaf1756d2483bc51354ecaec8 |
| check_n1v001.py | 437710413d5bcfa896b8ded65f0f09eeac41c22616096e5c04dfea7d8c3e26d0 |
| fixtures_n2v001.py | ae9e35cd699d8ccbc0b06a8efd39bab0311f12f8bbdc9282a4082d139f9dae79 |
| FIXTURES_N2_0451_V001.md | df2219920808e69b11f2901fdb813f46fc8ced7067761cc81f6849ca793a3a82 |
| fixture_results_n2v001_self.json | 79a7586ffd5a1164e919c14242c511cb3087b94339d6b926ecc06aca6fbd5d2f |
| fixture_results_n2v001_c3.json | ac2070ae371c6c17d09887908a056e397f59b6c77d18ee300e00a0ceb94ac165 |
