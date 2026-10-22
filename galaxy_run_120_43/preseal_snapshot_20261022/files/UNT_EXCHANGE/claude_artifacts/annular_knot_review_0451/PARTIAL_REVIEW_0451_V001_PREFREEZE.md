# Claude4 partial review 0451, V001: pre-freeze reading of the 0450 annular-knot module

Lead: Claude4. 2026-10-16, about 19:55 UTC. **This is not the verdict.** Claude3 had not posted done-0450. The pinned pre-freeze bytes are claude_artifacts/annular_knot_maps_0450/annular_knot_maps_c3v001.py, SHA-256 **23bb22fb94c3a6b39b84479a1c5e03812fbcdeaf6180ca85ddad083a3d3d92c4** (329 lines), with a cmp-verified copy at lead_copy_23bb22fb/. Everything here is re-checked against the hash in done-0450.

## Line trace against the root contract (58ffcbb8...)

**Edge recovery (L139-166).**
- s = (R/L)^2 is split into 18 groups of 4. Each group's centre is its mean, valid because the Gauss-Legendre nodes are symmetric; its half-width is the least-squares fit (groups @ x)/(x @ x).
- The checks cover all four nodes, adjacent-edge agreement, s0 = 0 and s18 = 1, against `edge_absolute_tolerance`, which root must supply.
- Edges are set to [0, midpoint of the two estimates of each interior edge, 1].
- R dR weights must equal (L^2/2)(delta s/2) W_i within `weight_relative_tolerance`, also root-supplied.
- Any failure raises ValueError and nothing is guessed. Neither tolerance has a default.

**Preserved v001 geometry (L110-137).**
- The old value blocks must reproduce legvander(zeta, 7) exactly. This proves the stored zeta is the one the v001 maps used.
- root_radial_derivatives must equal what the stored 72x72 radial_derivative operator gives for center and height, exactly. The body-fitted chain rule therefore keeps the v001 72-knot center_R and height_R, as the contract requires.
- The column sums of weights_RdRdz must equal 2*height*wr within `weight_relative_tolerance`.
- weights_RdRdz, zeta, roots and root derivatives are copied unchanged.

**Splines (L169-178).**
- `binding_module._spline_matrices(edges, list(s) + [1.0])` is called with knots at the 19 edges, evaluated at the 72 nodes plus s = 1. All nodes lie strictly inside the annuli, so there is no extrapolation.
- dB/dR = (2R/L^2) dB/ds.
- The outer trace must equal e_18 exactly. In the helper's code, at q = 1 we have i = 17, a = 0 and b = 1, so the cubic correction terms (a^3 - a) and (b^3 - b) are exactly zero.

**Scalar maps (L182-187).**
- V = B_j P_a; d_R V = B_R,j P_a - B_j P'_a (center_R + zeta height_R)/height; d_z V = B_j P'_a/height. These match the contract formulas.
- They are reshaped to 2304x152, with rows i*32 + l (the v001 order) and columns j*8 + a.
- The returned trace rows are kron(e_18, I8) for the outer trace, kron(B, (-1)^a) for the lower surface and kron(B, 1) for the upper surface.

**Helicity (L220-329).**
- The core `_regular_helicity_core`, compared as a normalized token stream, is **identical to reviewed v001 L27-71** (3194/3194 characters). This holds after substituting 576 and 1152 with n and 2n and removing line wrapping. The only exclusions are the dropped `scalar_map_sha256` metadata field and the dimension-specific `resource_scope` string.
- So the exponents, norms, Braw = [.5T, .5T, 0], the SVD rank threshold, the complete-QR nullspace Q[:, 8:], the one shared raw_transform for every U, d_R U and d_z U, divU and the no-lid boundary contract are all unchanged.
- The wrapper adds checks that R and L equal the scalar-map provenance, and that the scalar-map status and version match.

**Static AST check** (lead_copy_23bb22fb/STATIC_REPORT_c4lead_*.json):
- Only numpy and the stdlib module numbers are imported. There are no module-level statements and no side-effect calls.
- Both functions take only required keyword-only arguments, with no defaults, and neither writes to a parameter in place.
- linalg.svd, linalg.qr and np.eye appear only where the v001 construction uses them.
- There is no density projection, solve or symmetrization.

## Notes so far (no defects)

1. `arrays['radial_derivative']` now holds the 72x19 derivative of the new cardinal basis at the nodes. In v001 it held the 72x72 nodal spline derivative operator. The meaning ("radial basis derivative at the nodes") is the same, but the shape differs. Root code that consumes this key expecting 72x72 would fail loudly, not silently.
2. `old_scalar_map_sha256` and `binding_module_sha256` are caller custody assertions, string-compared to the pins, as in v001. The module cannot hash the objects it is passed.
3. The annular knots make the radial basis piecewise cubic within each Gauss-Legendre group. The preserved geometry derivatives (from the 72-knot spline), the regularity powers s^(e/2), the sqrt(s) factor in d_R and the physical fields stay non-polynomial in s. The correction therefore targets root's measured scalar radial defect; it cannot by itself make every fluid integral exact. This is consistent with the contract's "no convergence claim". N1 is quantifying this.

Pending: Claude3's done-0450 and frozen hash; the N1 oracle and analytic statement; the N2 synthetic-geometry harness run.
