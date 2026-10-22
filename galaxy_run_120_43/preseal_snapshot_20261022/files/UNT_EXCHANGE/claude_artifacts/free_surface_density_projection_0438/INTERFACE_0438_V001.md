# INTERFACE 0438 V001: free-surface conservative density projection (Claude2, c2v001)

Module: `free_surface_density_projection_c2v001.py`, in this directory (numpy only; inert at import; no I/O).
Task: `UNT_EXCHANGE/FROM_CODEX/0438_2026-10-16_claude_free_surface_density_projection.md`
(sha256 83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c).
Layout source, read as text and never imported: `owned_free_surface_32q8trial_maps_v001.py` (sha256 3bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943), with its review JSON `FREE_SURFACE_32Q8TRIAL_MAPS_V001_REVIEW_V001.json` (sha256 1dad13cffd17d8a08961f4b56ac3b41f5da53d694f01406f695c28f6bfc735ca).

## Signature
`project_density(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode, provenance)`.
All arguments are keyword-only and required, with no defaults. A missing argument raises Python's own TypeError. Every other outcome comes back as a dict.

## Equation (verbatim, binding)
`M=V^H W V; b=VR^H W(rho*xi_R) - i*mode*V^H W(rho*xi_phi/R) + VZ^H W(rho*xi_z); M*a=b; delta_rho=V*a.`
The code writes `^H` as `.conj().T`. W enters each integral exactly once. No 2*pi or annular factor is added. The routine solves the 72 diagonal 8x8 blocks of the assembled M with `numpy.linalg.solve`. It never inverts M, adds a ridge, clips, rescales mass or applies a tolerance.

## Block layout (from the source text)
V is built with shape (72,32,72,8), `V[i,:,i,:]=P[i]`, then reshaped in C order to (2304,576). So row = 32i+l and column = 8j+a. Block i covers rows 32i..32i+31 and columns 8i..8i+7. The weights are `(wr[:,None]*wz).reshape(-1)` and use the same row index.

## Validation (fail-closed `status="rejected_input"`, with `field` and `reason`)
- value, partial_R, partial_z: exact `numpy.ndarray` (no subclasses or lists), real floating dtype (itemsize <= 8), shape exactly (2304,576), finite. Complex, integer and bool dtypes are rejected.
- V must be exactly zero outside its 72 diagonal 32x8 blocks. Any nonzero entry is rejected, including subnormals; the first offending position is reported. -0.0 counts as zero. VR and VZ may be dense.
- weights, radius, rho: same type and dtype rules, shape (2304,), finite, strictly positive.
- xi_R, xi_phi, xi_z: complex64 or complex128, shape (2304,), finite. **Real-dtype xi is rejected, not promoted.**
- mode: Python int or numpy integer in 0..8. bool and numpy.bool_ are rejected.
- provenance: a str that is non-empty after stripping whitespace.

## Returns
**`status="computed"`:** returns
- the solution: `a` (576,), `delta_rho` (2304,), `b` (576,), and `b_terms` (radial, azimuthal, vertical);
- the mass blocks: `M_blocks` (72,8,8) and `M_offblock_max_abs`;
- block diagnostics with no threshold: `block_singular_values` (72,8), `block_singular_value_min` and `_max`, and `block_condition_number`;
- the residual, computed directly with the assembled M: `residual` = M·a − b (576,), `residual_block_norm` (72,) and `residual_global_norm`;
- the mass diagnostic: `dot_W_delta_rho` (complex, not forced to zero);
- bookkeeping: `completed_blocks`, `layout`, `equation`, `assumptions_not_verified` and `not_computed`.

**`status="failed_closed_solve"`:** returned on a singular block (LinAlgError), a non-finite M block or b block, a non-finite block solution, non-finite delta_rho or residual, or an assembled M that is not exactly block diagonal. It keeps `failed_block`, `completed_blocks` and `solved_coefficients` (the first 8·completed coefficients), plus b and the diagnostics. `a` and `delta_rho` are None.

**`status="failed_closed_internal"`:** returned on any unexpected exception.

There is no physical acceptance flag. Floating-point status flags are ignored locally, because Accelerate BLAS raises spurious matmul flags on finite data. Explicit isfinite checks make every decision.

## Assumptions, stated and not verified
- Physical-vacuum vanishing density on the free surfaces, so the weak form has no surface term.
- Root-enforced radial boundary flux, so no radial boundary term is added.

## Not computed
Pressure, velocity, source response, equilibrium, modal solution, physical acceptance.

## Private test hook
`_project_density_sized(..., n_radii, n_nodes, n_coeffs)` exists only for reduced-size stubs. The public API fixes (72,32,8), so arrays must be (2304,576) and (2304,).
