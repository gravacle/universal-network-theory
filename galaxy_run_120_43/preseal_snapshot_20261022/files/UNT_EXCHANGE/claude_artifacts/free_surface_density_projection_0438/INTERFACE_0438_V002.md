# INTERFACE 0438 V002: free-surface conservative density projection (c2v002)

Module: `free_surface_density_projection_c2v002.py`, in this directory (sha256 d1d73bbc178c869f5492bb1bb2e6ec06f9342bffcf73280b1416052bc9f25f8c). It imports numpy only, is inert at import and does no I/O.
It replaces c2v001 (sha256 b07fd00875e90e92c396b31103f3306dd8d85fbb1a10a44725f809a1553c6112). c2v001, `INTERFACE_0438_V001.md` and `CHECK_0438_V001.md` are unchanged on disk.
Task: `UNT_EXCHANGE/FROM_CODEX/0438_2026-10-16_claude_free_surface_density_projection.md` (sha256 83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c).
Layout source, read as text and never imported: `owned_free_surface_32q8trial_maps_v001.py` (sha256 3bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943). Its review JSON is `FREE_SURFACE_32Q8TRIAL_MAPS_V001_REVIEW_V001.json` (sha256 1dad13cffd17d8a08961f4b56ac3b41f5da53d694f01406f695c28f6bfc735ca).
The diff and rationale are in `FIX_DELTA_0438_V002.md`.

## Changes from V001
1. **Lane numerics convention (Codex 0354/0397/0414).**
   - Every product is now an explicit `numpy.einsum(..., optimize=False)`.
   - There is no `@`, `numpy.dot`, `matmul`, `vdot` or `inner`. `numpy.linalg.norm` is also gone, because it calls `dot` internally.
   - `numpy.linalg.solve` (per 8x8 block) and `numpy.linalg.svd` (diagnostics) are unchanged.
2. **No floating-point suppression.**
   - The `np.errstate(all="ignore")` that c2v001 placed around the arithmetic is removed.
   - The caller's numpy errstate and warnings filters now govern.
   - Every explicit `isfinite` decision is unchanged: 8 call sites in both versions.
3. **New fail-closed status `failed_closed_floating_point`.** See "Floating-point behaviour" below.
4. **Condition number.** It is computed without evaluating a division by an exactly zero singular value. The values are the same as c2v001: inf where sv_min == 0, NaN for a skipped block, sv_max/sv_min elsewhere.

The signature, validation, block layout, equation, conjugation and result keys are the same as V001. The full-size stub returns an identical key set.

## Signature (unchanged)
`project_density(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode, provenance)`.
All arguments are keyword-only and required, with no defaults. A missing or extra argument raises Python's own TypeError. Every other outcome comes back as a dict.

## Equation (verbatim, binding; unchanged)
`M=V^H W V; b=VR^H W(rho*xi_R) - i*mode*V^H W(rho*xi_phi/R) + VZ^H W(rho*xi_z); M*a=b; delta_rho=V*a.`

The code writes `^H` as `.conj().T`, with conjugation exactly where c2v001 conjugates: on V, VR and VZ (three sites). Each product is written as follows.
- **Mass matrix:** `M = einsum("il,lj->ij", V.conj().T, W[:,None]*V)`.
- **Radial term:** `einsum("il,l->i", VR.conj().T, W*(rho*xi_R))`.
- **Azimuthal term:** `(-1j*mode) * einsum("il,l->i", V.conj().T, W*(rho*xi_phi/R))`.
- **Vertical term:** `einsum("il,l->i", VZ.conj().T, W*(rho*xi_z))`.
- **Density:** `delta_rho = einsum("ij,j->i", V, a)`.
- **Residual:** `residual = einsum("ij,j->i", M, a) - b`.
- **Mass diagnostic:** `dot_W_delta_rho = einsum("l,l->", W, delta_rho)`. It is unconjugated, as `numpy.dot` was.
- **Residual norms:** `sqrt(einsum("i,i->", r.real, r.real) + einsum("i,i->", r.imag, r.imag))`, which is numpy.linalg.norm's own formula.

Other rules are unchanged:
- W enters each integral exactly once, and no 2π or annular factor is added.
- The 72 diagonal 8x8 blocks are each solved with `numpy.linalg.solve`.
- The routine never inverts M, adds a ridge, clips, rescales mass or applies a tolerance.

## Block layout (unchanged)
- Row = 32i+l and column = 8j+a.
- Block i covers rows 32i..32i+31 and columns 8i..8i+7.
- The weights `(wr[:,None]*wz).reshape(-1)` use the same row index.

## Validation (unchanged; fail-closed `status="rejected_input"` with `field` and `reason`)
- value, partial_R, partial_z: exact `numpy.ndarray`, real float16/32/64, shape (2304,576), finite. V must be exactly zero outside its 72 diagonal 32x8 blocks; -0.0 counts as zero. VR and VZ may be dense.
- weights, radius, rho: shape (2304,), finite, strictly positive.
- xi_R, xi_phi, xi_z: complex64 or complex128, shape (2304,), finite. Real-dtype xi is rejected, not promoted.
- mode: Python int or numpy integer in 0..8. bool is rejected.
- provenance: a str that is non-empty after stripping whitespace.

## Returns
**`status="computed"`:** the same keys as V001.
- The solution: `a` (576,), `delta_rho` (2304,), `b` (576,) and `b_terms`.
- The mass blocks: `M_blocks` (72,8,8) and `M_offblock_max_abs`.
- Block diagnostics with no threshold: `block_singular_values`, `_min`, `_max` and `block_condition_number`.
- The residual: `residual` = M·a − b, with `residual_block_norm` and `residual_global_norm`.
- The mass diagnostic: `dot_W_delta_rho` (complex, not forced to zero).
- Bookkeeping: `completed_blocks`, `failed_block`, `layout`, `equation`, `assumptions_not_verified` and `not_computed`.

**`status="failed_closed_solve"` (unchanged):**
- **Returned on:**
  - a singular block (LinAlgError);
  - a non-finite M or b block;
  - a non-finite block solution;
  - a non-finite delta_rho or residual;
  - an assembled M that is not exactly block diagonal.
- **Keeps:**
  - `failed_block`;
  - `completed_blocks`;
  - `solved_coefficients` (the first 8·completed values);
  - b and the diagnostics, when they were computed.
- `a` and `delta_rho` are None, and no residual keys are present.

**`status="failed_closed_floating_point"` (new):**
- **Returned on:**
  - a `FloatingPointError` raised inside the arithmetic under the caller's errstate;
  - a `RuntimeWarning` raised as an exception by the caller's warnings filter.
- **Keeps:**
  - the same fields as `failed_closed_solve`: `failed_block`, `completed_blocks`, `solved_coefficients`, and b and the diagnostics when they were computed;
  - `failed_stage`: `"assembly of M and b"`, `"off-block check and block diagnostics"`, `"block solves"` or `"delta_rho, residual and their diagnostics"`;
  - `floating_point_exception`, e.g. `"FloatingPointError: overflow encountered in multiply"`.
- `a` and `delta_rho` are None.
- None of `residual`, `residual_block_norm`, `residual_global_norm` or `dot_W_delta_rho` is present. They are computed into locals before any result key is set.

**`status="failed_closed_internal"` (unchanged):** returned on any other unexpected exception.

There is no physical acceptance flag.

## Floating-point behaviour (the caller's settings govern; nothing is suppressed)

| Caller setting | Genuine overflow/invalid/underflow in an elementwise step | Overflow or underflow inside an einsum product or sum | Finite, well-scaled input |
|---|---|---|---|
| numpy default (`over/divide/invalid="warn"`, `under="ignore"`), default warnings filter | A RuntimeWarning goes to the caller (visible, not suppressed). The computation continues, and the explicit `isfinite` checks decide, typically `failed_closed_solve`. | Silent inf/NaN. `isfinite` gives `failed_closed_solve`. | `computed`, no warnings |
| `np.seterr(all="raise")` | A FloatingPointError is raised inside the call. `_compute` **catches it** and returns `failed_closed_floating_point`, so it does **not propagate**. | Silent. `isfinite` gives `failed_closed_solve`. | `computed`, bitwise equal to the default run |
| `warnings.simplefilter("error")` with errstate "warn" | A RuntimeWarning is raised as an exception. It is caught and returned as `failed_closed_floating_point`. | Silent. `isfinite` gives `failed_closed_solve`. | `computed` |
| `np.seterr(all="ignore")` | Silent. `isfinite` decides (c2v001 behaviour). | Silent. `isfinite` decides. | `computed` |

- **Which steps honour errstate.** These elementwise ufuncs do:
  - `W[:,None]*V`, the `rho*xi` products, `/R` and `W*(...)`;
  - the `(-1j*mode)` factor and the b sum;
  - the residual subtraction;
  - `abs` for `M_offblock_max_abs`;
  - the condition-number division;
  - the norm's final sum.
- **numpy 2.0.2 `einsum` does not check floating-point status.** An overflow or underflow inside a product or sum is silent in every errstate mode. This was verified with a probe and with fixtures T10o and T14o. The explicit `isfinite` checks are the backstop there, exactly as in c2v001.
- **`numpy.linalg.solve` and `svd` set their own errstate internally** (over, divide and under ignored; invalid raises LinAlgError). The caller's settings do not reach inside them. This is unchanged from c2v001.
- **Underflow.** `np.seterr(all="raise")` includes `under="raise"`. A genuine elementwise underflow, such as a very small rho·xi or W·V product, then fails closed as `failed_closed_floating_point`. That is the caller's choice.
- **Diagnostics are not exempt.**
  - With a finite block whose condition number exceeds ~1.8e308, sv_max/sv_min overflows.
  - Under "raise", this returns `failed_closed_floating_point` at stage "off-block check and block diagnostics" with `completed_blocks` 0.
  - Under the default errstate, it emits a visible RuntimeWarning and the result is `computed` with cond = inf. c2v001 gave inf silently. Fixture T15d verifies this.
- **Completed blocks.**
  - M and b are fully assembled before any block solve, so an exception during assembly or diagnostics has `completed_blocks` 0 and `failed_block` None.
  - During block solves, `completed_blocks = failed_block = i`.
  - After all solves, `completed_blocks` is 72, `failed_block` is None, and `solved_coefficients` holds all 576 values.
  - In the code as written, no FloatingPointError can arise inside the solve loop: it contains only isfinite checks, `linalg.solve` with its own errstate, and an assignment. The retention path for the "block solves" stage was therefore verified by test-side injection only (T15j).
- **Other errstate modes** ("call", "print", "log") act as the caller configured them. An exception of another type raised by a "call" handler lands in `failed_closed_internal`.
- **The module never calls `np.seterr` or `np.errstate`.** It leaves the caller's settings unchanged (verified).
- **Spurious flags.** c2v001's local suppression existed because Accelerate BLAS raises spurious flags on finite matmul. c2v002 has no BLAS product. On the full-size finite stub, modes 0..8 gave:
  - no warnings under the default errstate;
  - `computed` under `np.seterr(all="raise")`;
  - `computed` under `warnings.simplefilter("error")`.

## Assumptions, stated and not verified (unchanged)
- Physical-vacuum vanishing density on the free surfaces, so the weak form has no surface term.
- Root-enforced radial boundary flux, so no radial boundary term is added.

## Not computed (unchanged)
Pressure, velocity, source response, equilibrium, modal solution, physical acceptance.

## Private test hooks
- `_project_density_sized(..., n_radii, n_nodes, n_coeffs)` exists only for reduced-size stubs. The public API fixes (72,32,8).
- `_compute(...)` keeps its c2v001 keyword interface. It builds the progress state internally.
