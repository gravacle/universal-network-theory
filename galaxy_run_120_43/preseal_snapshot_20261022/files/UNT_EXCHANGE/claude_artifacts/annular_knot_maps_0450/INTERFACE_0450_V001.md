# INTERFACE_0450_V001 — annular-knot radial maps c3v001

- **Module:** `annular_knot_maps_c3v001.py` (this directory). It is inert and uses numpy only. It calls the pinned binding-v002 `_spline_matrices`. Physical status: not_assessed.
- **Contract:** `ANNULAR_KNOT_RADIAL_CORRECTION_CHOICE_V001.json` `58ffcbb8…`.
- **Pin constants:** `OLD_SCALAR_MAP_SHA256` (v001 scalar maps `3bd792ba…`), `BINDING_MODULE_SHA256` (`87866875…`), `OLD_HELICITY_MAP_SHA256` (the v001 helicity reference being generalized, `280149dc…`; not imported).

## 1. `build_annular_scalar_maps(*, ...)`

All arguments are keyword-only and required. Every failure raises ValueError.

| argument | requirement |
|---|---|
| `old_scalar_maps` | the dict returned by v001 `build()` (trial `[72,8]`, quadrature `[72,32]`) |
| `old_scalar_map_sha256` | must equal `OLD_SCALAR_MAP_SHA256` (caller custody assertion) |
| `radial_nodes_m` | real (72,), increasing, 0 < R < L |
| `radial_RdR_weights_m2` | real (72,), > 0 |
| `outer_radius_m` | true outer radius L > 0 |
| `binding_module`, `binding_module_sha256` | module providing `_spline_matrices`; the hash must equal `BINDING_MODULE_SHA256` |
| `edge_absolute_tolerance` | explicit, finite, >= 0, in units of s = (R/L)² |
| `weight_relative_tolerance` | explicit, finite, >= 0 |

### Verification (fails closed, never guesses)

**Edges.** With s = (R/L)², the 72 nodes must be 18 ordered groups of 4, each matching `leggauss(4)` on one annulus. The checks are:
- every node residual;
- agreement of adjacent edges;
- s₀ = 0 and s₁₈ = 1, all within `edge_absolute_tolerance`;
- RdR weights equal to (L²/2)·halfwidth·GL weight within `weight_relative_tolerance`.

**Custody of the old maps:**
- The old `value` diagonal blocks must equal `legvander(zeta, 7)` exactly.
- The old `root_radial_derivatives` must reproduce exactly from the old `radial_derivative`.
- Each column's sum of the preserved `weights_RdRdz` must equal 2·height·RdR within the weight tolerance.

### Returns

`status='ANNULAR_KNOT_SCALAR_MAPS'`, `trial_shape=[19,8]`, `quadrature_shape=[72,32]`, `edge_recovery` (residuals, tolerances, GL nodes and weights), `provenance` (versions, pins, L, R), and `arrays`:

| key | shape | content |
|---|---|---|
| `value`, `partial_R`, `partial_z` | (2304,152) float64 | B_j P_a; B_R,j P_a − B_j P'_a (center_R+ζ height_R)/height; B_j P'_a/height |
| `radial_value`, `radial_derivative` | (72,19) | natural-cubic cardinal B_j(s_i) on the 19 edges; dB/dR = (2R/L²) dB/ds |
| `outer_coefficient_trace` | (8,152) | exactly kron(e₁₈, I₈), since every B_j at s = 1 is the unit vector |
| `lower_surface_trace`, `upper_surface_trace` | (72,152) | **redefined:** the ζ = ∓1 value at the 72 radial nodes, kron(B, (∓1)^a); v001 used kron(I₇₂, ·) |
| `annular_edges_s`, `annular_edges_R_m` | (19,) | recovered edges, s₀ = 0 and s₁₈ = 1 exactly; R = L√s |
| `weights_RdRdz`, `zeta`, `roots_m`, `root_radial_derivatives` | as v001 | preserved copies |

Rows are indexed i·32 + l and columns j·8 + a.

**V is not block diagonal**, because the radial cardinal splines have global support. The 0438 block projection therefore does not apply; use the 0447 pointwise Gkin.

## 2. `build_annular_regular_helicity_maps(*, scalar_maps, radial_nodes_m, outer_radius_m, m, rank_relative_tolerance, rank_absolute_tolerance)`

- **Input checks:** `scalar_maps` must be the output of section 1 from this module version. `radial_nodes_m` and `outer_radius_m` must equal those stored in its provenance. m must be a Python int with 1 ≤ m ≤ 6, and the rank controls must be explicit, finite and ≥ 0.
- **Construction:** this is the v001 construction with n = 152 in place of 576:
  - exponents |m+1|, |m−1|, |m|;
  - normalization from the stacked dimensionless maps;
  - B = [½T, ½T, 0]·diag(1/norms), giving the 8 true-outer ξ_R = 0 rows;
  - the same SVD rank threshold;
  - complete QR, Z = Q[:, 8:].
- **Returns:** the same keys and names as v001: `status` (`REGULAR_HELICITY_MAPS`, or `UNRESOLVED_OUTER_CONSTRAINT_RANK`), `UR`, `UP`, `UZ`, `partial_R_U{R,P,Z}`, `partial_z_U{R,P,Z}`, `divU`, `normalized_nullspace`, `raw_coefficient_transform`, `hard_nullspace_residual(_norm)`, norms, constraints, singular values, threshold, exponents, `outer_radius_m`, `m`.
  - **Shapes:** maps are (2304,448), transforms (456,448).
  - **Dtypes:** as in v001, `UR` and `UZ` are float64 (accepted by 0439 and 0447); `UP` and `divU` are complex128.
  - **Additional keys:** `trial_shape`, `quadrature_shape`, `annular_edges_s`, `scalar_map_provenance`, `module_version`, `reference_generalized`.

## Root call sequence

1. `old = v001.build(...)` (existing).
2. `sm = build_annular_scalar_maps(old_scalar_maps=old, ...)`.
3. `hel = build_annular_regular_helicity_maps(scalar_maps=sm, ...)`.
4. Then:
   - Gkin: `kinematic_density_map(rho=, rho_R=, rho_z=, U_R=hel['UR'], U_z=hel['UZ'], divU=hel['divU'])`.
   - Euler: `assemble_weak_euler(..., U_R=hel['UR'], U_phi=hel['UP'], U_z=hel['UZ'], divU=hel['divU'], G=Gkin, ...)`, which gives A of shape 448×448.

**Memory:** one (2304,448) complex map is 16.5 MB. The ten maps, transforms and Q total under 0.2 GB.

## Verification on synthetic geometry only

Script: `lead_check/lead_equivalence_check_c3v001.py`.

- Fed the old 72-knot maps, the generalized core reproduces the reviewed v001 helicity maps **bitwise**: all 16 compared arrays for m = 1, 2, 3, 6, at L = 2.5 and L = 3.1e20.
- Edges are exact to 1e-16, with s₀ and s₁₈ exact. The outer trace is the exact unit vector, ξ_R(R = L) is about 1e-16 relative and the hard residual about 2e-16.

Independent analytic tests are in `tests/`.

## Not supplied

No density projection, solve, lid, regularization, convergence claim or physical acceptance. The old 72-knot results remain preserved by root.
