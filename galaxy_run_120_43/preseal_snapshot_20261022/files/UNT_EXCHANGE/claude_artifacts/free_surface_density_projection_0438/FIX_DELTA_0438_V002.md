# FIX DELTA 0438 V002: c2v001 → c2v002 (lane numerics convention)

**Role:** fix author. I did not write c2v001 or its V001 interface, and I am not the V001 checker.

**Why this fix exists.** The original 0438 brief omitted the standing lane convention from Codex 0354/0397/0414:
- no BLAS products in scientific arithmetic;
- explicit `numpy.einsum(..., optimize=False)` instead;
- no floating-point suppression, so the root caller's errstate and warning rules govern;
- `numpy.linalg.solve` per 8x8 block and `numpy.linalg.svd` for diagnostics remain allowed;
- every explicit `isfinite` check is kept.

c2v001 used `@` and `np.dot`, and wrapped all its arithmetic in `np.errstate(all="ignore")`. CHECK_0438_V001 (PASS_WITH_NOTES) recorded this as note 5.

## Files (sha256 from bytes)

| File | sha256 |
|---|---|
| Base `free_surface_density_projection_c2v001.py` (unchanged) | b07fd00875e90e92c396b31103f3306dd8d85fbb1a10a44725f809a1553c6112 |
| Base `INTERFACE_0438_V001.md` (unchanged) | 0879a70bed60c2372f8f73641875dcb686ec0fdcdd2240fdfafd5f5ce5dc6163 |
| Base `CHECK_0438_V001.md` (unchanged) | 738a5029aadf9720c62e5bac728ed36a351855a52b6e211b4b86c10a734605f7 |
| **New** `free_surface_density_projection_c2v002.py` | d1d73bbc178c869f5492bb1bb2e6ec06f9342bffcf73280b1416052bc9f25f8c |
| **New** `INTERFACE_0438_V002.md` | bde6eb0f55eeb2cf79ba05294cb5da0ed8a942d39e26b52fdeb25a0ee954992f |
| Fixtures `scratchpad/r0438v2/fixtures_0438v2.py` | ba2ad10b933045a1df775d9bb4de800fe35cc49634714b53eaa6bd07a7832a2b |
| Fixture output `scratchpad/r0438v2/final_run.out` (173/173) | ac412977d65612a9eedb52e1d877392427a4ef3d5d60d216bbfc76eccad00947 |
| Unmodified c2v001 author fixtures `scratchpad/r0438/fixtures_0438.py` | 18076dca0ad41833b7579b802d613bf5ddf652735ddf56e7bb8d8ad9bfce8b4a |
| Their output on c2v002, `scratchpad/r0438v2/original_fixtures_on_c2v002.out` (117/117) | 48f9f8d8e15d254efca3c765122b0ee12cb112d0db54401e48c05312e9840ece |
| The diff below, `scratchpad/r0438v2/c2v001_to_c2v002.diff` | 6fcbc53a7cf8db066f03ddc3186f1c213a2179ad590221fe10146ae65f519b68 |

The scratchpad is `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad`.

## Changes and rationale

**1. Requested: products become einsum.** All seven products are now `einsum(..., optimize=False)` with explicit subscripts. Conjugation sits exactly where c2v001 had it (the three `.conj().T` on V, VR, VZ). delta_rho, the residual and dot(W, δρ) stay unconjugated.

| Quantity | c2v001 | c2v002 |
|---|---|---|
| M | `VH @ (W[:,None]*V)` | `einsum("il,lj->ij", VH, W[:,None]*V)` |
| b_radial | `VR.conj().T @ (W*(rho*xi_R))` | `einsum("il,l->i", VR.conj().T, ...)` |
| b_azimuthal | `(-1j*mode)*(VH @ (...))` | `(-1j*mode)*einsum("il,l->i", VH, ...)` |
| b_vertical | `VZ.conj().T @ (...)` | `einsum("il,l->i", VZ.conj().T, ...)` |
| delta_rho | `V @ a` | `einsum("ij,j->i", V, a)` |
| residual | `M @ a - b` | `einsum("ij,j->i", M, a) - b` |
| dot_W_delta_rho | `np.dot(W, delta_rho)` | `einsum("l,l->", W, delta_rho)` |

Only the summation order changes. On the full-size stub, c2v002 matches c2v001 to these relative differences:

| Quantity | Relative difference |
|---|---|
| a | 3.7e-16 |
| δρ | 4.7e-16 |
| b | 2.0e-16 |
| M_blocks, singular values, condition numbers | bitwise equal |
| dot(W, δρ) | ≤1e-12 relative |

The residual is a roundoff quantity in both versions: 1.6e-12 in c2v002 and 2.0e-12 in c2v001, against max|b| = 220.

**2. Scope reading: `np.linalg.norm` becomes `_norm2`.** numpy 2.0.2's `linalg.norm` for a 1-D vector computes `sqrt(x.real.dot(x.real) + x.imag.dot(x.imag))`, a hidden BLAS dot. `_norm2` uses the same formula with `einsum("i,i->")`. I read the convention's "no dot" as covering this.

**3. Requested: suppression removed.** `with np.errstate(all="ignore")` is gone from `_compute`. The module contains no `errstate`, `seterr` or warnings-filter call anywhere, so the caller's settings govern.

**4. Requested: fail-closed handling of floating-point errors.**
- `_compute` catches `FloatingPointError` around the arithmetic.
- It returns `status="failed_closed_floating_point"` with the same retention fields as `failed_closed_solve`: `failed_block`, `completed_blocks`, `solved_coefficients`, plus b and the diagnostics when computed. It adds `failed_stage` and `floating_point_exception`.
- Progress is tracked in a small `state` dict. `_arithmetic` registers its `fail` closure before any arithmetic statement, then updates the stage, current block and completed count.

Two choices were made here:
- **A separate status, not `failed_closed_solve`.** This tells a caller that its own floating-point policy stopped the arithmetic, as opposed to a detected singular or non-finite solve. A caller that only tests `status == "computed"` is unaffected.
- **`RuntimeWarning` raised as an exception is also caught.** This goes beyond the literal brief. Under `warnings.simplefilter("error")` with errstate "warn", numpy raises the same event as a RuntimeWarning exception. Without this catch it would fall through to `failed_closed_internal` and lose the completed blocks. Catching it gives the same fail-closed outcome as FloatingPointError. The exception text is kept in the result, so it is not hidden. Warnings are not filtered or suppressed anywhere.

**5. Needed as a result of 3: the condition-number expression.**
- c2v001 computed `np.where(sv_min == 0, np.inf, sv_max / sv_min)`. That evaluates the division for every block, so an exactly zero singular value (e.g. an all-zero block) raised divide/invalid flags that c2v001 suppressed.
- Without suppression, the default errstate would print a spurious warning. Under "raise", the singular-block `failed_closed_solve` (3 blocks retained) would become a floating-point failure with 0 retained.
- c2v002 now fills inf and divides only where `sv_min != 0`. The values are identical: inf for an exact zero, NaN for a skipped non-finite block, and the ratio elsewhere.

**6. Needed as a result of 4: statement order.**
- `out`, `a` and `fail` are created at the top of `_arithmetic`, so the handler can retain progress from any stage.
- The residual norms and `dot_W_delta_rho` are computed into locals before any result key is set. A floating-point exception at that last stage therefore leaves no partial `residual*` or `dot*` keys, matching the c2v001 fail-closed contract.

**7. Text only.** The module tag is now c2v002, and the docstrings describe the convention and the new status.

## Unchanged (verified)

- **Signature and validation.** Both are unchanged. The re-implemented T1, T9, T11 and T12 checks all pass, with the expected rejection fields.
- **Equation, layout and outputs.**
  - The equation text and layout are unchanged.
  - The result key set is identical on the full-size stub.
  - The 8 explicit `np.isfinite(` sites are unchanged (counted with AST and text).
- **linalg calls.** `np.linalg` use is limited to `solve`, `svd` and `LinAlgError`.
- **Old fixtures.** The unmodified c2v001 author fixtures pass 117/117 on c2v002.
  - Their run log shows spurious Accelerate "divide by zero / overflow / invalid value encountered in matmul" warnings.
  - All of those come from the fixtures' own test-side `@` reference products, at fixture lines 198–205, on finite data. That is the lane problem itself, reproduced on the test side.
  - None comes from the module: their T14 no-warning check passes.

## Verification

I re-implemented the c2v001 author fixtures as `fixtures_0438v2.py`.
- Test-side products also use einsum, and the single dense 576x576 solve is test-only.
- It ran under `/usr/bin/python3 -I -B` (Python 3.9.6, numpy 2.0.2) with `signal.alarm(170)`, using synthetic stubs only, against the installed c2v002 (its hash is printed in the run).
- The result is **173/173 PASS**.

- **T0 convention, by AST.**
  - There is no `@` operator, and no dot, matmul, vdot, inner, tensordot or norm.
  - There is no errstate, seterr or warnings-filter call, and no `with` statement.
  - All 9 einsum calls have literal subscripts and `optimize=False`.
  - There are three `.conj().T`.
  - The isfinite count is 8, the same as c2v001.
  - Importing prints nothing, warns nothing and imports nothing besides numpy.
- **T3–T7 analytic checks.** These cover the vertical, radial and azimuthal signs, superposition, loop references for each b term and for M, b(iξ) = i·b(ξ), and Fourier conjugation (δρ = sin z, and the unconjugated variant is wrong). All pass at ≤1e-13.
- **T8 full-size dense reference (72×32×8 public API).**
  - The reference uses an independent three-operand `einsum("li,l,lj->ij")` M and a dense solve.
  - rel(a) = 3.9e-16 and rel(δρ) = 9.7e-16. Modes 0..8 are worst at 9.7e-16.
  - The off-block part of M is exactly 0 in both module and reference.
  - The residual matches a direct recomputation, and the condition number equals the SVD ratio.
  - No warnings were raised.
- **T8b c2v002 vs c2v001.** The figures are those listed under change 1, and the key sets are identical.
- **T10 failure retention.** These cases behave as in c2v001, and none of them emits a warning:
  - singular block 2 (2 retained, bitwise);
  - singular block 0 (0 retained);
  - all-zero block 3 (3 retained, cond = inf);
  - a 1e200 block (1 retained).
- **T14 under `np.seterr(all="raise")` on finite inputs (required not to fail).**
  - The full-size stub is `computed` and bitwise equal to the default-errstate run. Modes 0..8 are all `computed`.
  - The reduced stub and the complex-V core are also `computed`.
  - Singular and all-zero blocks still give `failed_closed_solve` with retention.
  - The 1e200 block gives `failed_closed_solve` with 1 block retained: einsum overflow is silent, and `isfinite` decides.
  - With raise plus `warnings.simplefilter("error")`, the stub is `computed`.
  - The caller's errstate is untouched.
- **T15 genuine floating-point events.** The input is ρ·ξ_R = 1e200·1e200 in assembly.

  | Caller setting | Outcome |
  |---|---|
  | `seterr(all="raise")` | `failed_closed_floating_point`, stage assembly, 0 retained, exception `FloatingPointError: overflow encountered in multiply`; caught, not propagated |
  | Default errstate | Visible RuntimeWarnings (overflow, invalid), then `failed_closed_solve` |
  | `warnings` "error" | `failed_closed_floating_point` with `RuntimeWarning: overflow...` |
  | `seterr(all="ignore")` | Silent `failed_closed_solve`, as in c2v001 |

- **T15d condition-number overflow.** The block is diag(~1e300, ~1, ~1e-10).
  - Under "raise", it returns `failed_closed_floating_point` at the diagnostics stage, with b and M_blocks present.
  - Under the default errstate, a visible warning is emitted and the result is `computed` with cond = inf. This matches c2v001's silent result.
- **T15j/T15k injected FloatingPointError (test-side proxies).**
  - At the block-2 solve, `completed_blocks = failed_block = 2`, the retained coefficients are bitwise equal to the good run, and the stage is "block solves".
  - In the residual norm, all 4 blocks are retained and no `residual*` or `dot*` keys are present.
  - Any other exception type is still `failed_closed_internal`.

## Notes

- **einsum is silent.** numpy 2.0.2 `einsum` does not check floating-point status, so overflow or underflow inside a product is silent under every errstate. The explicit `isfinite` checks remain the only guard there, as in c2v001. This is stated in INTERFACE V002.
- **Underflow under "raise".** `np.seterr(all="raise")` includes underflow. On real data, very small elementwise products (e.g. rho·xi near a vanishing-density surface) would fail closed. That is the caller's errstate governing, as the convention requires. The synthetic stubs did not underflow.
- **Scope.** No project data, no project runs and no source-contract import. Nothing was written under `/Users/bgm/Research/Universal Network Theory`. The new files were written with exclusive create. Scratch files are in `scratchpad/r0438v2/`.

## diff -u (from this directory; c2v001 → c2v002)

```diff
--- free_surface_density_projection_c2v001.py	2026-10-16 12:44:54.013265081 -0500
+++ free_surface_density_projection_c2v002.py	2026-10-16 13:06:20.667448690 -0500
@@ -1,4 +1,13 @@
-"""UNT 0438 -- conservative density projection on the reviewed 32-point free-surface mesh (Claude2, c2v001).
+"""UNT 0438 -- conservative density projection on the reviewed 32-point free-surface mesh (c2v002).
+
+c2v002 is c2v001 (sha256 b07fd00875e90e92c396b31103f3306dd8d85fbb1a10a44725f809a1553c6112) brought under the
+standing lane numerics convention (Codex 0354/0397/0414). Every matrix/vector product is an explicit
+numpy.einsum(..., optimize=False) instead of @ / numpy.dot / BLAS (including the hidden dot inside
+numpy.linalg.norm). There is no local floating-point suppression: the caller's numpy errstate and warnings
+filters govern. A FloatingPointError, or a RuntimeWarning raised as an exception by the caller's warnings
+filter, inside the arithmetic returns status "failed_closed_floating_point" with completed blocks retained.
+numpy.linalg.solve per 8x8 block and numpy.linalg.svd for diagnostics are unchanged. Every explicit isfinite
+decision is unchanged.
 
 Pure inert module. Imports numpy only; defines constants and functions; performs no computation and no I/O at
 import; every outcome is returned as a dict (fail-closed). It never imports project workers and never reads data.
@@ -178,32 +187,69 @@
     return None, arrays
 
 
+def _norm2(x):
+    """2-norm of a 1-D vector by numpy.linalg.norm's own formula (square root of the summed squares of the real
+    and imaginary parts), with einsum(..., optimize=False) in place of the BLAS dot that norm uses internally."""
+    xr = x.real
+    xi = x.imag
+    return np.sqrt(np.einsum("i,i->", xr, xr, optimize=False) + np.einsum("i,i->", xi, xi, optimize=False))
+
+
 def _compute(**kwargs):
-    """Arithmetic on already-validated arrays. Floating-point status flags are ignored locally (some BLAS builds,
-    e.g. Accelerate, raise spurious matmul flags on finite data); every decision is an explicit isfinite check."""
-    with np.errstate(all="ignore"):
-        return _arithmetic(**kwargs)
+    """Arithmetic on already-validated arrays. No local floating-point suppression: the caller's numpy errstate
+    and warnings filters govern, and every decision is an explicit isfinite check. A FloatingPointError (caller
+    errstate "raise") or a RuntimeWarning raised as an exception (caller warnings filter "error") inside the
+    arithmetic is returned fail-closed as status "failed_closed_floating_point", with the stage, the block in
+    progress, completed_blocks and solved_coefficients retained. Nothing is suppressed, retried or recomputed."""
+    state = {"stage": "assembly of M and b", "failed_block": None, "completed": 0, "fail": None}
+    try:
+        return _arithmetic(state=state, **kwargs)
+    except (FloatingPointError, RuntimeWarning) as exc:
+        text = "%s: %s" % (type(exc).__name__, exc)
+        # state["fail"] is registered by _arithmetic before any arithmetic statement.
+        out = state["fail"]("failed_closed_floating_point",
+                            "%s raised under the caller's numpy errstate / warnings filter during %s"
+                            % (text, state["stage"]), state["failed_block"], state["completed"])
+        out["failed_stage"] = state["stage"]
+        out["floating_point_exception"] = text
+        return out
 
 
-def _arithmetic(*, V, VR, VZ, W, R, rho, xi_R, xi_phi, xi_z, mode, provenance, n_radii, n_coeffs):
-    """Arithmetic of the binding equation. ^H is written as .conj().T."""
+def _arithmetic(*, V, VR, VZ, W, R, rho, xi_R, xi_phi, xi_z, mode, provenance, n_radii, n_coeffs, state):
+    """Arithmetic of the binding equation. ^H is written as .conj().T. Every product is an explicit
+    numpy.einsum(..., optimize=False), never @ / dot / matmul (no BLAS). state records progress for _compute."""
     n_cols = n_radii * n_coeffs
+    out = _result("computed", None, provenance)
+    out["mode"] = mode
+    out["n_blocks"] = n_radii
+    out["block_size"] = n_coeffs
+    a = np.zeros(n_cols, dtype=np.complex128)
+
+    def fail(status, reason, failed_block, completed):
+        out["status"] = status
+        out["reason"] = reason
+        out["failed_block"] = failed_block
+        out["completed_blocks"] = completed
+        out["solved_coefficients"] = a[:n_coeffs * completed].copy()
+        out["a"] = None
+        out["delta_rho"] = None
+        return out
+
+    state["fail"] = fail
+
     VH = V.conj().T
     # M=V^H W V  (W used once)
-    M = VH @ (W[:, None] * V)
+    M = np.einsum("il,lj->ij", VH, W[:, None] * V, optimize=False)
     # b=VR^H W(rho*xi_R) - i*mode*V^H W(rho*xi_phi/R) + VZ^H W(rho*xi_z)  (W used once in each integral)
-    b_radial = VR.conj().T @ (W * (rho * xi_R))
-    b_azimuthal = (-1j * mode) * (VH @ (W * (rho * xi_phi / R)))
-    b_vertical = VZ.conj().T @ (W * (rho * xi_z))
+    b_radial = np.einsum("il,l->i", VR.conj().T, W * (rho * xi_R), optimize=False)
+    b_azimuthal = (-1j * mode) * np.einsum("il,l->i", VH, W * (rho * xi_phi / R), optimize=False)
+    b_vertical = np.einsum("il,l->i", VZ.conj().T, W * (rho * xi_z), optimize=False)
     b = b_radial + b_azimuthal + b_vertical
 
-    out = _result("computed", None, provenance)
-    out["mode"] = mode
     out["b"] = b
     out["b_terms"] = {"radial": b_radial, "azimuthal": b_azimuthal, "vertical": b_vertical}
-    out["n_blocks"] = n_radii
-    out["block_size"] = n_coeffs
 
+    state["stage"] = "off-block check and block diagnostics"
     off = M[~_coeff_block_mask(n_radii, n_coeffs)]
     out["M_offblock_max_abs"] = float(np.max(np.abs(off))) if off.size else 0.0
 
@@ -221,31 +267,25 @@
                 pass
     sv_min = np.min(sv, axis=1)
     sv_max = np.max(sv, axis=1)
-    cond = np.where(sv_min == 0, np.inf, sv_max / sv_min)
+    # inf where the smallest singular value is exactly zero, without evaluating a division by zero.
+    cond = np.full(n_radii, np.inf)
+    nonzero = sv_min != 0
+    cond[nonzero] = sv_max[nonzero] / sv_min[nonzero]
     out["block_singular_values"] = sv
     out["block_singular_value_min"] = sv_min
     out["block_singular_value_max"] = sv_max
     out["block_condition_number"] = cond
 
-    a = np.zeros(n_cols, dtype=np.complex128)
-
-    def fail(status, reason, failed_block, completed):
-        out["status"] = status
-        out["reason"] = reason
-        out["failed_block"] = failed_block
-        out["completed_blocks"] = completed
-        out["solved_coefficients"] = a[:n_coeffs * completed].copy()
-        out["a"] = None
-        out["delta_rho"] = None
-        return out
-
     if off.size and not np.all(off == 0):
         return fail("failed_closed_solve",
                     "assembled M is not exactly block diagonal (non-finite or nonzero off-block entries); "
                     "separate block solves would not be the stated equation", None, 0)
 
     # M*a=b, solved as the separate diagonal blocks with ordinary direct solves.
+    state["stage"] = "block solves"
     for i, s in enumerate(blocks):
+        state["failed_block"] = i
+        state["completed"] = i
         Mi = M_blocks[i]
         bi = b[s]
         if not (np.all(np.isfinite(Mi)) and np.all(np.isfinite(bi))):
@@ -258,23 +298,31 @@
             return fail("failed_closed_solve", "non-finite solve result at block %d" % i, i, i)
         a[s] = ai
 
+    state["stage"] = "delta_rho, residual and their diagnostics"
+    state["failed_block"] = None
+    state["completed"] = n_radii
     # delta_rho=V*a
-    delta_rho = V @ a
+    delta_rho = np.einsum("ij,j->i", V, a, optimize=False)
     # Directly computed residual M*a-b with the assembled M.
-    residual = M @ a - b
+    residual = np.einsum("ij,j->i", M, a, optimize=False) - b
     if not (np.all(np.isfinite(delta_rho)) and np.all(np.isfinite(residual))):
         return fail("failed_closed_solve", "non-finite delta_rho or residual after all block solves",
                     None, n_radii)
 
+    # Computed before any result key is set, so a floating-point exception here leaves no partial result keys.
+    residual_block_norm = np.array([_norm2(residual[s]) for s in blocks])
+    residual_global_norm = float(_norm2(residual))
+    # Complex diagnostic, not forced to zero (unconjugated, as numpy.dot(W, delta_rho) in c2v001).
+    dot_W_delta_rho = complex(np.einsum("l,l->", W, delta_rho, optimize=False))
+
     out["completed_blocks"] = n_radii
     out["failed_block"] = None
     out["a"] = a
     out["delta_rho"] = delta_rho
     out["residual"] = residual
-    out["residual_block_norm"] = np.array([np.linalg.norm(residual[s]) for s in blocks])
-    out["residual_global_norm"] = float(np.linalg.norm(residual))
-    # Complex diagnostic, not forced to zero.
-    out["dot_W_delta_rho"] = complex(np.dot(W, delta_rho))
+    out["residual_block_norm"] = residual_block_norm
+    out["residual_global_norm"] = residual_global_norm
+    out["dot_W_delta_rho"] = dot_W_delta_rho
     return out
 
 
@@ -315,8 +363,10 @@
     Returns a dict. status "computed": a (576,), delta_rho (2304,), b (576,) and its three terms, M blocks,
     per-block singular values / ranges / condition numbers (diagnostics, no threshold), residual M*a-b with
     per-block and global norms, dot(W, delta_rho) (complex diagnostic). status "rejected_input",
-    "failed_closed_solve" (completed_blocks and solved_coefficients retained) or "failed_closed_internal"
-    otherwise. There is no physical acceptance flag.
+    "failed_closed_solve" (completed_blocks and solved_coefficients retained), "failed_closed_floating_point"
+    (a FloatingPointError or escalated RuntimeWarning under the caller's errstate / warnings filter; same
+    retention plus failed_stage and floating_point_exception) or "failed_closed_internal" otherwise. There is no
+    physical acceptance flag. Products are numpy.einsum(..., optimize=False); no floating-point suppression.
     """
     return _project_density_sized(value=value, partial_R=partial_R, partial_z=partial_z, weights=weights,
                                   radius=radius, rho=rho, xi_R=xi_R, xi_phi=xi_phi, xi_z=xi_z, mode=mode,
```
