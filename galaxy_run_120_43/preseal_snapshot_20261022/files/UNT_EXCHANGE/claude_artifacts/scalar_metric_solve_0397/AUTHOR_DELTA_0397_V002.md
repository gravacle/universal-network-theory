# AUTHOR DELTA 0397 V002: scalar_metric_particular_solve v001 to v002

Author: Claude helper (AUTHOR role for V002). A different static/source checker must review V002; this author does not review it.

V001 inputs, all verified by sha256 from bytes before editing:
- module v001: c7dbbba8ccb5bff025cf874410d769e96b7757b214d77d7f7f2fbf8c420dc0db
- USAGE_CONTRACT_0397_V001.md: e8ffbf92fd6b0a68568929f07552bf3715318f4c659b151236236f681bc2afbf
- AUTHOR_NOTES_0397_V001.md: d51f0ad9070a310888aa741e7092d02e46cb897d2882bed74763350b6158cc60
- REVIEW_0397_V001.md: 8da4c9c2f2a5b0379602645aa8a54571d26e8573d0fbc576d8035216a7147f68
- Codex 0398: cf798ab64a7ca91733e28dc29ea5491ce9974f5edc4a5f406ff304cbf1d861a5
- frozen formula source: f5e28809a8ac24212d1d30bf6be92ab0d064407ae139f72f5146334c86308dd7

Output: module v002, sha256 ef767fd79f60852e23ec0de29b04737cf4acfacca3461d83f5b3d01413abaecf.

## diff -u scalar_metric_particular_solve_v001.py scalar_metric_particular_solve_v002.py

```diff
--- scalar_metric_particular_solve_v001.py	2026-10-15 19:36:07.291286282 -0500
+++ scalar_metric_particular_solve_v002.py	2026-10-15 19:47:16.825717473 -0500
@@ -1,4 +1,6 @@
-# UNT support task 0397 -- inert author implementation, v001.
+# UNT support task 0397 -- inert author implementation, v002.
+# v002 applies the four Codex 0398 corrections to v001 (listed in the docstring of
+# scalar_metric_particular_solve); formula, ordering, sign and scope are unchanged.
 # One public function, scalar_metric_particular_solve, plus private helpers.
 # numpy only. Module-level code is limited to the numpy import and function
 # definitions: no constants, no work at import, no I/O, no subprocesses, no CLI.
@@ -51,8 +53,13 @@
 
 
 def _complex_vector2_input(name, value, failures):
-    """Admit a length-2 list/tuple or shape-(2,) array of finite complex scalars."""
+    """Admit a length-2 list/tuple or plain shape-(2,) ndarray of finite complex scalars."""
     if isinstance(value, np.ndarray):
+        if type(value) is not np.ndarray:
+            failures.append(
+                f"input {name}: ndarray subclass {type(value).__name__} is not admitted"
+            )
+            return None
         if value.shape != (2,):
             failures.append(f"input {name}: array shape {value.shape!r} is not (2,)")
             return None
@@ -72,8 +79,13 @@
 
 
 def _complex_matrix2_input(name, value, failures):
-    """Admit a 2x2 nested list/tuple or shape-(2,2) array of finite complex scalars."""
+    """Admit a 2x2 nested list/tuple or plain shape-(2,2) ndarray of finite complex scalars."""
     if isinstance(value, np.ndarray):
+        if type(value) is not np.ndarray:
+            failures.append(
+                f"input {name}: ndarray subclass {type(value).__name__} is not admitted"
+            )
+            return None
         if value.shape != (2, 2):
             failures.append(f"input {name}: array shape {value.shape!r} is not (2, 2)")
             return None
@@ -110,6 +122,26 @@
     return float(np.sqrt(np.sum(v.real * v.real + v.imag * v.imag)))
 
 
+def _nonfinite_entries(name, Z):
+    """Name each non-finite part of a complex array as 'name[i][j] part kind'."""
+    out = []
+    for index in np.ndindex(Z.shape):
+        label = name + "".join(f"[{n}]" for n in index)
+        for part, x in (("real", Z[index].real), ("imag", Z[index].imag)):
+            if not np.isfinite(x):
+                out.append(f"{label} {part} {'nan' if np.isnan(x) else 'inf'}")
+    return out
+
+
+def _nonfinite_scalars(named):
+    """Name each non-finite (name, float) pair as 'name (kind)'; None is skipped."""
+    return [
+        f"{n} ({'nan' if np.isnan(v) else 'inf'})"
+        for n, v in named
+        if v is not None and not np.isfinite(v)
+    ]
+
+
 def _new_result():
     return {
         "ok": False,
@@ -145,8 +177,9 @@
             "not a raw susceptibility; F_eff already contains the ordinary and retained "
             "first derivatives in the reviewed sign convention. G_EH is not equated to "
             "laboratory G. No galaxy data, fit parameters or 43 velocities are computed "
-            "here. cond_tol only flags ill-conditioning; it is not a physical acceptance "
-            "rule."
+            "here. cond_tol only flags finite ill-conditioning; it is not a physical "
+            "acceptance rule. An exactly singular A (LU failure or s_min == 0) is a "
+            "failure."
         ),
     }
 
@@ -154,9 +187,27 @@
 def scalar_metric_particular_solve(*, k, z, G_EH, Pi_eff, F_eff, cond_tol):
     """Particular solution q = (n, psi) of (K0 + Pi_eff) q = -F_eff on the scalar branch.
 
+    Version v002. The v001 formula, ordering, sign, scope and output keys are kept.
+    Four corrections from Codex 0398 (REVIEW_0397_V001 F1, F2, F4, F5) are applied:
+      1. s_min == 0 from the SVD is rejected as singular (failure, ok False) even
+         when numpy.linalg.solve returned. A finite cond_2 > cond_tol stays a
+         report-only flag that does not change ok.
+      2. ndarray subclasses (e.g. np.matrix) are rejected for Pi_eff and F_eff, so
+         an admitted array is a plain ndarray and chained indexing cannot escape.
+      3. residual_norm, F_norm, q_norm, s_max, s_min, s_max*q_norm, cond_2 and each
+         non-None relative residual are checked. Any non-finite one is the failure
+         "diagnostics: unrepresentable ..." (stage 'diagnostics', ok False) and the
+         diagnostics field stays None, so an overflow can never read as a zero
+         residual or as a finite cond_2.
+      4. K0 and A after assembly, and q after the solve, are finite-checked before
+         they are packaged. A non-finite array is left None and its entries (index,
+         part, nan or inf) are named in the failure. Nothing is replaced by zero.
+
     Sources (read-only):
       * Task: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/
         0397_2026-10-15_scalar_metric_particular_solver.md
+      * Corrections: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/
+        0398_2026-10-15_scalar_solver_review_corrections.md
       * Frozen formula: helpers/coefficient_method/
         EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_PROPOSED_V001.md (sha256 f5e28809...)
       * Distinct review: helpers/response_packet_audit/
@@ -170,26 +221,32 @@
 
     Arguments (keyword-only, required, no defaults):
       k: finite real > 0.  z: finite complex, Im(z) >= 0.  G_EH: finite real > 0.
-      Pi_eff: finite complex 2x2 (nested list/tuple or shape-(2,2) array).
-      F_eff: finite complex length-2 (list/tuple or shape-(2,) array).
+      Pi_eff: finite complex 2x2 (nested list/tuple or plain shape-(2,2) ndarray).
+      F_eff: finite complex length-2 (list/tuple or plain shape-(2,) ndarray).
       cond_tol: finite real > 0, the caller's threshold for FLAGGING ill-conditioning.
-    Booleans, other shapes and non-finite values are rejected.
+    Booleans, ndarray subclasses, other shapes and non-finite values are rejected.
 
-    Returns a plain dict. "ok" is True only if inputs are admitted, A is finite,
-    numpy.linalg.solve succeeds (exact singularity raises LinAlgError and is reported
-    as a failure), and q and every diagnostic are finite. If the 2-norm condition
-    number exceeds cond_tol, "ill_conditioned" is True and a flag is recorded, but ok
-    is NOT changed: cond_tol is reported, never a physical acceptance rule.
-    Complex values are {"real", "imag"} fields. Diagnostics: residual A q + F_eff
-    (einsum, optimize=False), its 2-norm, relative to |F_eff| and to ||A||_2 |q|, the
+    Returns a plain dict. "ok" is True only if inputs are admitted, K0 and A are
+    finite, numpy.linalg.solve succeeds (exact singularity raises LinAlgError and is
+    reported as a failure), q is finite, the smallest singular value of A is > 0, and
+    every diagnostic is finite. A field is filled only with finite values: a
+    non-finite K0, A or q stays None, and diagnostics stays None unless all of its
+    values are finite. If the finite 2-norm condition number exceeds cond_tol,
+    "ill_conditioned" is True and a flag is recorded, but ok is NOT changed: cond_tol
+    is reported, never a physical acceptance rule, and the caller must decide
+    explicitly before using such a result. When ok is False, every populated field is
+    failure evidence only. Complex values are {"real", "imag"} fields. Diagnostics:
+    residual A q + F_eff (einsum, optimize=False), its 2-norm, relative to |F_eff|
+    and to ||A||_2 |q| (each None only when its denominator is exactly 0), the
     singular values of A (numpy.linalg.svd, compute_uv=False; a LAPACK call, not a
     matrix product) and cond_2 = s_max / s_min.
 
     Scope: translation-stationary scalar branch, particular solution only; no
     homogeneous, boundary or k = 0 modes, nonstationary convolution or retained-block
     elimination. Pi_eff is a matched residual ACTION Hessian, not a raw
-    susceptibility. G_EH is not laboratory G. No 43 velocities. Warnings are not
-    suppressed.
+    susceptibility. F_eff = F_b + ell_eff in the reviewed sign convention. G_EH is
+    not laboratory G. No 43 velocities, galaxy data or fit parameters. Warnings are
+    not suppressed.
     """
     result = _new_result()
     failures = result["failures"]
@@ -234,10 +291,16 @@
         dtype=np.complex128,
     )
     A = K0 + Pi_in
-    result["K0"] = _pairs_matrix(K0)
-    result["A"] = _pairs_matrix(A)
-    if not (np.all(np.isfinite(K0)) and np.all(np.isfinite(A))):
-        failures.append("assembly: K0 or A has a non-finite entry")
+    # Finite admission before packaging: a non-finite array stays None.
+    K0_bad = _nonfinite_entries("K0", K0)
+    A_bad = _nonfinite_entries("A", A)
+    result["K0"] = None if K0_bad else _pairs_matrix(K0)
+    result["A"] = None if A_bad else _pairs_matrix(A)
+    if K0_bad:
+        failures.append("assembly: K0 left None; non-finite " + ", ".join(K0_bad))
+    if A_bad:
+        failures.append("assembly: A left None; non-finite " + ", ".join(A_bad))
+    if failures:
         return result
 
     # ---- Stage 3: solve A q = -F_eff ------------------------------------------
@@ -248,12 +311,16 @@
     except np.linalg.LinAlgError as exc:
         failures.append(f"solve: A is singular to working precision ({exc})")
         return result
-    result["q"] = [_pair(q[i]) for i in range(2)]
-    if not np.all(np.isfinite(q)):
-        failures.append("solve: q has a non-finite component")
+    # Finite admission before packaging: a non-finite q stays None.
+    q_bad = _nonfinite_entries("q", q)
+    if q_bad:
+        failures.append("solve: q left None; non-finite " + ", ".join(q_bad))
         return result
+    result["q"] = [_pair(q[i]) for i in range(2)]
 
     # ---- Stage 4: residual and conditioning diagnostics -----------------------
+    # Every value is checked before diagnostics is packaged; on any failure here
+    # diagnostics stays None. A finite residual_norm implies a finite residual.
     result["stage_reached"] = "diagnostics"
     residual = np.einsum("ij,j->i", A, q, optimize=False) + F_in
     residual_norm = _vector_norm(residual)
@@ -266,33 +333,64 @@
         return result
     s_max = float(singular_values[0])
     s_min = float(singular_values[-1])
-    cond_2 = float(s_max / s_min) if s_min > 0.0 else float("inf")
     scale_Aq = s_max * q_norm
-    diagnostics = {
+    unrepresentable = _nonfinite_scalars(
+        [
+            ("residual_norm", residual_norm),
+            ("F_norm", F_norm),
+            ("q_norm", q_norm),
+            ("s_max", s_max),
+            ("s_min", s_min),
+            ("s_max*q_norm", scale_Aq),
+        ]
+    )
+    singular = bool(np.isfinite(s_min)) and not s_min > 0.0
+    if singular:
+        failures.append(
+            f"diagnostics: A is singular: smallest singular value s_min = {s_min!r} "
+            "although numpy.linalg.solve returned; rejected (no pseudoinverse, "
+            "regularization or cutoff); the q above is failure evidence, not a solution"
+        )
+    cond_2 = None
+    relative_to_F = None
+    relative_to_Aq = None
+    if not unrepresentable and not singular:
+        cond_2 = s_max / s_min
+        relative_to_F = residual_norm / F_norm if F_norm != 0.0 else None
+        relative_to_Aq = residual_norm / scale_Aq if scale_Aq != 0.0 else None
+        unrepresentable = _nonfinite_scalars(
+            [
+                ("cond_2", cond_2),
+                ("relative_residual_to_F", relative_to_F),
+                ("relative_residual_to_A_norm_q_norm", relative_to_Aq),
+            ]
+        )
+    if unrepresentable:
+        failures.append(
+            "diagnostics: unrepresentable " + ", ".join(unrepresentable)
+            + "; diagnostics left None (no value is reported as finite)"
+        )
+    if failures:
+        return result
+    result["diagnostics"] = {
         "residual": [_pair(residual[i]) for i in range(2)],
         "residual_norm": residual_norm,
         "F_norm": F_norm,
         "q_norm": q_norm,
-        "relative_residual_to_F": residual_norm / F_norm if F_norm > 0.0 else None,
-        "relative_residual_to_A_norm_q_norm": (
-            residual_norm / scale_Aq if scale_Aq > 0.0 else None
-        ),
+        "relative_residual_to_F": relative_to_F,
+        "relative_residual_to_A_norm_q_norm": relative_to_Aq,
         "singular_values": [s_max, s_min],
         "A_norm_2": s_max,
         "cond_2": cond_2,
         "cond_tol": tol_in,
     }
-    result["diagnostics"] = diagnostics
-    finite_checks = [residual_norm, F_norm, q_norm, s_max, s_min]
-    if not all(np.isfinite(v) for v in finite_checks):
-        failures.append("diagnostics: a residual, norm or singular value is not finite")
-        return result
     ill = not cond_2 <= tol_in
     result["ill_conditioned"] = ill
     if ill:
         result["flags"].append(
             f"ill_conditioned: cond_2 = {cond_2!r} exceeds cond_tol = {tol_in!r} "
-            "(reported only; not a physical acceptance rule)"
+            "(reported only; not a physical acceptance rule; the caller must decide "
+            "explicitly before any use)"
         )
 
     result["ok"] = True
```

## Change map (v002 line numbers)

- **0398 item 1 / REVIEW F1: s_min == 0 is rejected.**
  - L347–353: `singular` is true when s_min is finite and not > 0. It records the failure `diagnostics: A is singular …`, gives ok False, keeps stage at 'diagnostics' and leaves diagnostics None.
  - L357–358: cond_2 = s_max/s_min is computed only when s_min > 0. The v001 fallback `float("inf")` (v001 L269) is removed.
  - L387–394: a finite cond_2 > cond_tol is still a report-only flag that does not change ok. The flag text now says the caller must decide explicitly before any use.
  - L180–182: scope text updated.
- **0398 item 2 / REVIEW F2: ndarray subclasses are rejected.**
  - L58–62 and L84–88: `type(value) is not np.ndarray` gives the failure `input <name>: ndarray subclass <type> is not admitted`, so np.matrix can no longer reach `value[i][j]`.
  - The same rule is applied to F_eff, so there is one admission rule for both arrays.
  - Scalar admission via `_complex_input` is unchanged for every element.
- **0398 item 3 / REVIEW F5 (and F4 for diagnostics): unrepresentable diagnostics fail.**
  - L136–142: new `_nonfinite_scalars` helper.
  - L337–346: checks residual_norm, F_norm, q_norm, s_max, s_min and s_max*q_norm.
  - L357–367: cond_2 and the two relative residuals are computed only from finite inputs, then checked themselves. A relative residual is None only when its denominator is exactly 0 (`!= 0.0`, replacing v001's `> 0.0`, which sent nan to None).
  - L368–374: any non-finite value gives the failure `diagnostics: unrepresentable <name> (<kind>) …`, with stage 'diagnostics' and ok False.
  - L375–386: diagnostics is packaged only after every check passes. v001 packaged it first (v001 L285) and had no check on the ratio or on s_max*q_norm.
  - The output keys are unchanged.
- **0398 item 4 / REVIEW F4: finite admission for K0, A and q before packaging.**
  - L125–133: new `_nonfinite_entries` helper, which names each entry by index, part (real/imag) and kind (nan/inf).
  - L294–304: K0 and A are checked before packaging. A non-finite array is left None and a finite one is still reported. Failures read `assembly: K0|A left None; non-finite …`.
  - L314–319: q is checked before packaging. A non-finite q is left None, with the failure `solve: q left None; non-finite …`.
  - Nothing is replaced by zero. K0[0][0] = prefactor*0.0 still produces nan when prefactor overflows, so that case is reported, not hidden.
- **Text only.**
  - L1–3: header updated to v002.
  - L190–204: docstring now has a v002 change list; L209–210 add the 0398 source.
  - L224–227: argument text says plain ndarray and ndarray subclasses are rejected.
  - L229–242: return semantics updated.
  - L247–249: scope adds F_eff = F_b + ell_eff and "no galaxy data or fit parameters".
  - Every 0397 scope exclusion is kept.
- **Unchanged.**
  - K0 formula and q = (n, psi) ordering.
  - A = K0 + Pi_eff, and solve(A, -F_eff).
  - einsum(optimize=False) residual and svd(compute_uv=False).
  - Keyword-only required arguments with no defaults.
  - No @, dot, matmul, pinv, lstsq or inv. No symmetrization, Hermitization, real projection, clipping, regularization or defaults.
  - No warning suppression, I/O or threads; numpy is the only import.
  - The units and sign_convention text.

## Residual open points

1. **Underflow is not guarded (F3 class; 0398 excluded broader scale coverage).**
   - The sum-of-squares norms underflow for components below about 1e-154. A nonzero residual can then give residual_norm = 0.0, which reads as a relative residual of 0.0.
   - A nonzero F or q can likewise give a norm of 0, so the ratio is None.
   - Overflow is fully guarded. Root should keep normalized components within roughly 1e-154 to 1e154.
2. **q stays in the output in the s_min == 0 case.** The q returned by LU is finite and is kept as evidence alongside ok False. The failure text and the contract say it is not a solution.
3. **Overflowed cond_2 leaves ill_conditioned as None.** An overflowed cond_2 is reported as an unrepresentable failure, not as ill-conditioned=True. ill_conditioned is True or False only when ok is True.
4. **REVIEW F6 is unchanged.** svd remains a second LAPACK call.
5. **V002 is not yet reviewed.** It has not been executed or imported. A distinct static checker review of V002 is still pending.

## Execution statement

Static only:
- Neither v001 nor v002 was imported or executed.
- The only Python run was `python3 -I` on a scratchpad AST script that does `ast.parse` over the v002 file text.
- Files were drafted in the session scratchpad and created here exclusively (open mode 'x').
- No network was used, and nothing was written under Universal Network Theory.
