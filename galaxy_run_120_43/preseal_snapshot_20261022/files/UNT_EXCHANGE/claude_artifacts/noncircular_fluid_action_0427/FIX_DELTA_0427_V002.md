# FIX DELTA 0427 V002: c2v001 → c2v002, INTERFACE V001 → V002

**Who:** fix author Claude2, the implementer of c2v001. I am not a reviewer of this delta, and a distinct reviewer must check it.

**What changed:** the delta changes only what resolves B1 and B2 from `REVIEW_0427_INTERFACE_V001.md` and the two Codex 0428 items. The c2v001 module and INTERFACE V001 are preserved unchanged. Nothing was written under `Universal Network Theory`. No DDO154/NGC3198 data, run packet or target velocities were opened.

## 1. Files (sha256 from bytes)

| file | sha256 |
|---|---|
| `ddo_noncircular_displacement_action_c2v001.py` (preserved, unchanged) | `6b4f2cc6ee0e0c1a4408e555004b510d2d11058bc6f3e9cc82f6ce697ef9e482` |
| `INTERFACE_0427_V001.md` (preserved, unchanged) | `1c34edf3fce32f7705382d9f1b802ec2d53ad6b097c57b4fad4bff64af4b60eb` |
| **new** `ddo_noncircular_displacement_action_c2v002.py` | `056db7b19443d4a88dcb6396531dfe1ff61acd8ba8387e6bfd0a8b64cf179925` |
| **new** `INTERFACE_0427_V002.md` | `82d7c6cdf37eb40b03d429e77ae11e1a3c80cd80f630f67ea8dbba972d834a7c` |
| input `REVIEW_0427_INTERFACE_V001.md` (B1, B2) | `1df58f47d90c457f0ad952489aa3b6118e8c6588e9abf4e5f3358edfc6496f42` |
| input `REVIEW_0427_EQUATIONS_V001.md` (no blocking items) | `95eda7c805b6068d7dee442bddfe7586a4f8bcf625c40976d324617db832d21a` |
| input Codex 0428 `0428_2026-10-16_0427_finite_diagnostics_and_base_clarification.md` | `e94cc68d2ebde91ae839f7a960e964ef909474358993028d860088164266da60` |

Binding inputs I re-verified from bytes before starting, all matching:
- task 0427 `1e9e7cfb4be32cae313543374edb76c647a14530720cb276c83f6e464e95c164`
- spec `d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4`
- equation review JSON `99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e`
- v006 `e0d0888de2487c9de1346b4268c0ef9c12401965134333741b389bb3a5cdca79`
- v004 `61dc1369726413cda55e87b6175adccce095c65495cb3d94afbff1b50a255582`
- 0428 `e94cc68d2ebde91ae839f7a960e964ef909474358993028d860088164266da60`

## 2. Issue → change map

| issue | defect? | change (c2v002 lines / INTERFACE V002 section) |
|---|---|---|
| **B1**: lower-rank arrays broadcast along the wrong axis (`_grid_array`, c2v001 L114-124) | yes; reproduced on c2v001 | **Rank rule:** `_grid_array` accepts only `arr.ndim == 0` or `arr.ndim == len(grid_shape)` (L137-143). Any other rank is rejected at `input_validation` with the rank, the shape and the rule, before any callback. The existing broadcast check still requires each axis to be 1 or equal to the grid axis. This path covers R, phi, z, rho0, K0, P0, Omega, xi, r0, angular forcing and supplied base derivatives. **Shapes recorded:** each accepted input's original shape goes into the new success key `input_shapes` (L152, L534). **Docs:** INTERFACE §2 (rank rule), §6 (`input_shapes`) and §7 fact 6. |
| **B2**: INTERFACE omits the free-surface position and surface-mass source fact (V001 §7) | yes, documentation only; the module has no quadrature and must not choose one | **No code change.** INTERFACE §7 gains **fact 10**: Root must state where the rho0→0 surface lies relative to the grid faces. Root must then either supply the boundary-layer surface-displacement source inside the response adapter, consistent with v004's k=0/boundary-normal assignment, or give the retained-order assessment that shows it is negligible. **Fact 7** now says the `lagrangian_dP = 0` row is the spec s5 condition only at the actual surface. Fact 1 and §1/§3 cross-reference fact 10. |
| **0428-F**: identity diagnostics computed under ignored FP errors and returned with ok=True without finite validation | yes; reproduced on c2v001 (`probe_nonfinite_diagnostics.py`: ok=True, non-finite `linearized_entropy`) | Two independent layers. **Layer 1:** module arithmetic runs under `errstate(divide/over/invalid='raise', under='ignore')` (constant L87; used L256 and L596) instead of `errstate(all='ignore')`. A `FloatingPointError` fails closed with stage `floating_point` and the phase name (L273-276, L631-632). Callbacks still run under the caller's errstate. **Layer 2:** before ok=True, every module-owned returned array and float is checked finite, including both identity diagnostics, the base residuals, Euler terms, `lapse_used` and `boundary_state`. A failure gives stage `output_validation` (helper L222-236, applied L576-583). **Policy:** ok is False whenever any returned residual or diagnostic would be non-finite. I chose fail-closed, not an "unavailable" status, so a returned diagnostic is always a finite array. **Docs:** INTERFACE §3 (floating point) and §6 (stages, finite guarantee). |
| **0428-B**: base wording must not become a new gate or claim r0 = 0; Omega used as given | wording defect only; c2v001 code had no force-balance gate, no Omega² use and no r0 test | **Code wording:** the axisymmetry rejection message no longer says "axisymmetric equilibrated base". It now says the base is the stationary leading continuity/entropy reference and that force imbalance belongs in r0 and is not gated (L393-398, comments L378-380). `NOT_DONE` gains "no force-balance gate: r0 may be nonzero; Omega used as given (no Omega**2 clipping, no dropped radii, no enforced inward force, no source change)" (L94-95). The module docstring states the same. **INTERFACE:** §2 (Omega, base_axisymmetry_rtol, base_residual_r0 rows and the Omega note), §4 (r0 nonzero in general), and §7 fact 4, rewritten from "Equilibrated axisymmetric base" to "Axisymmetric reference base". **Unchanged:** the module still returns all three Euler components, makes exactly one feedback call, retains the full native output by identity, and makes no stationary-state claim. |

Nothing else changed. In particular:
- the equations
- the signs and the order of the Euler terms
- the forcing partition
- the response contract
- the call counts (the interface reviewer's 7/15/7 and 4/11/4 checks pass)
- the boundary separation
- the public signatures

The equation lines moved by +58, and INTERFACE §4 maps them.

## 3. Issues or parts judged not a defect, or not changed, with reasons

- **B2 code.** I agree with the reviewer that no module change is needed. The module cannot represent the rho0→0 surface (rho0 > 0 is required) and must not choose a quadrature or a surface model. The fix is the missing Root fact.
- **0428-B code.** No gate existed to remove. c2v001 never formed Omega², never tested r0, never dropped radii and never enforced an inward force. The only defect was wording: one rejection message and INTERFACE §7 fact 4. Axisymmetry within `base_axisymmetry_rtol` and the polytrope relation remain the only base gates. 0428 keeps axisymmetric density, entropy and real Omega as the leading continuity/entropy reference.
- **0428-F, "unavailable diagnostic" alternative.** I did not use it. Failing closed is stricter and matches the module's existing contract that a failure returns no partial fields.
- **0428-F, `induced_response_full`.** It is not traversed. It is the caller's object, retained by identity, and it is neither a module residual nor a module diagnostic. The lapse arrays the module actually uses are validated finite and returned under `lapse_used`. **A distinct reviewer should confirm this reading of "every other returned array".**
- **Non-blocking review notes not in this fix list** are unchanged: interface N1-N7 and equation notes 1-8. In particular, N2 (masked arrays lose their mask) still exposes in the interface reviewer's PROBE.

## 4. Fixture re-runs against the published c2v002 bytes

All runs used `python3 -I -B` (codex runtime, Python 3.12.14, numpy 2.3.5) in scratchpad `r0427-fix/`. They are NONPHYSICAL and algebraic only.

| fixture (sha256) | exercised | on c2v002 | on c2v001 |
|---|---|---|---|
| interface reviewer `probe_broadcast_square_grid.py` (`336a8c77e8b844b2aa342650bb33b72096137c9712aef1575521783e79606a6c`), unmodified | B1 | "1-D Omega(R) accepted: False \| explicit (N,1,1) accepted: True". The script then raises KeyError, because it assumes the 1-D input is accepted. | re-run: "1-D Omega(R) accepted: True"; residuals off by 0.0665/0.105/0.00875 (scales 0.16/0.22/0.02) |
| interface reviewer suite `review_0427_interface_fixtures.py` (`144b3638a53e9f659436f1ee855dadef85fd828af762fac1f83c6c5adba00279`), unmodified | B1 PROBE plus contract | 136/138. The B1 PROBE now PASSES. The 2 FAILs are expected: the success key set now includes `input_shapes` (B1 record), and the N2 masked-array PROBE is out of scope. | re-run: 136/138 (B1 PROBE and N2 PROBE fail; output byte-identical to the reviewer's `review_run2.txt`) |
| equation reviewer suite `review_0427_eq_fixtures.py` (`a56c511ed9b08088b872194adf8de1ad5fee898b6fb927c1a467690823a8b4cd`), unmodified | regression | 71/71 | re-run: 71/71 (byte-identical to the reviewer's `run1.txt`) |
| author V001 suite `test_0427_algebraic_fixtures.py` (`89e20cb76a529a920d69ea69b736f9b4fff72e12024dd32fb15eb01d8d67d8b6`), unmodified | regression | 93/93 | re-run: 93/93 |
| `probe_nonfinite_diagnostics.py` (`f0f629fe7410879923cd91c2ee57235d21643fd013a9020a39fd50278fa35c19`), constructed from the 0428 description because Codex's local fixture was not available to me | 0428-F | ok=False, stage `floating_point` (identity_diagnostics), errstate restored | ok=True with non-finite `linearized_entropy` (defect reproduced) |
| V002 suite `test_0427_algebraic_fixtures_v002.py` (`3cec22e4ed834d2910b3067c36641d4a8aafcba287268ffbc2c2813887ec0ab1`) = V001 suite + 34 delta checks | B1, 0428-F, 0428-B, B2 | 127/127 | 107/127; the 20 failures are the delta defects |

Run outputs (sha256):

| output | sha256 |
|---|---|
| `run_v002_final.txt` | `50d48f8f45ee620f22ad9c9ea70583ae2de7e7c16cdb600365e54bedfd9fbd6a` |
| `contrast_c2v001_final.txt` | `932a017e2530d477780b33eefe785527f711b0e2a076db36e7520de0eff3fb03` |
| `rerun_interface_review_on_c2v002.txt` | `3136a99edfeff231a4694967f3554daaa95098eb52e4cd62e55cdb0522e42e21` |
| `rerun_eq_review_on_c2v002.txt` | `caac20cbf06a8ce18b4030e1726956308867fea6dd55c6671865ceaa8d30cf30` |
| `rerun_probe_broadcast_on_c2v002.txt` | `1e3b1eec9ec00a4e70b8346e53e01295edbd737ed67f6172ac1c42eee46e088d` |
| `probe_nonfinite_on_c2v001.txt` | `be21d569976ba4c6aa7f5307d9ddb5dd76a72f9d1cd9f747cef3aa753fa93f82` |
| `probe_nonfinite_on_c2v002.txt` | `b627f4e7771d2bb56d502091abf9acef0c67cfcfc99a449b1453cd7c3e6f3be7` |
| `rerun_v001_suite_on_c2v002.txt` | `5a0aa2e08ede2a4469020d88c83e043d7a6ccf602f8b712dd9a17b3a6b7deb69` |
| `rerun_interface_review_on_c2v001.txt` | `37c9e4e81286a900744e8bc1be71162e8b1bb1924a0be8996ae33463e9a2e4a5` |
| `rerun_eq_review_on_c2v001.txt` | `8fe6024928ed8538ca398b3c3e7c5e1efcb98cfc0d6c32fb9d45230529c0bec0` |
| `rerun_v001_suite_on_c2v001.txt` | `789bae91689c18f90604c04c26ff3237a4aba00d3da67e4d3e0ae9ea8c33363f` |
| `rerun_probe_broadcast_on_c2v001.txt` | `8d118be5cead02037d5069f3f9cb41797330a2dbe7dea4d83245f9fb845a47d2` |

What the delta checks show:
- **B1:**
  - Every array argument rejects rank 1, 2 and 4 with zero callbacks first. This includes the 1-D length-N_z Omega that c2v001 right-aligned to z, and a 1-D `z` that c2v001 accepted.
  - On the 8×8×8 square grid:
    - 1-D Omega(R) is rejected.
    - (N,1,1) gives Omega_R = 0.5 and Omega_z = 0 to within 1.5e-14.
    - (N,1,1) is bitwise equal to the full-array input.
    - 0-d and an explicit (1,1,N) are accepted and recorded.
- **0428-F:**
  - The diagnostic overflow fails closed, with the response called once. The same happens under the caller's `seterr(all='raise')`.
  - A hidden `rho0**2` overflow in the radial Euler term fails closed. c2v001 returned that term as a silent finite 0.
  - **Layer independence.** A scratch copy with the errstate set to ignore was run on the same inputs:
    - The output sweep alone fails closed on `identity_diagnostics['linearized_entropy']`.
    - The same copy returns the overflowed Euler term as a wrong finite 0. That shows why layer 1 is needed.
  - Success results are identical under the caller's errstate set to ignore or to raise.
- **0428-B:**
  - A sign-changing real Omega with a large nonzero r0 is accepted.
  - Omega is used bitwise as given.
  - r0 enters each residual once (1.5e-16).
  - All three components are returned, with one response call and the native output retained.
  - `not_done` wording is present, and no "equilibrated" gate text remains.
- **B2 (illustration; module unchanged):** with rho0 > 0 on the top and bottom faces and an m=0 xi_z, Clenshaw–Curtis integration gives ∫drho dV = −1.514248 = −∮ rho0 xi·n dA, a nonzero net mass in `delta_f_n`.

## 5. Unified diffs (`diff -u`, published bytes)

### 5.1 Module: `diff -u ddo_noncircular_displacement_action_c2v001.py ddo_noncircular_displacement_action_c2v002.py`

````diff
--- ddo_noncircular_displacement_action_c2v001.py	2026-10-16 10:49:07.611975298 -0500
+++ ddo_noncircular_displacement_action_c2v002.py	2026-10-16 11:11:37.752278440 -0500
@@ -1,4 +1,15 @@
-"""INERT leading-order noncircular displacement action (UNT 0427, Claude2 c2v001).
+"""INERT leading-order noncircular displacement action (UNT 0427, Claude2 c2v002).
+
+c2v002 supersedes c2v001 (preserved unchanged). Delta only:
+  B1   array inputs must be 0-d or have exactly len(grid_shape) axes (explicit
+       singleton axes); lower-rank arrays are rejected, never right-aligned.
+       Original input shapes are recorded under 'input_shapes'.
+  0428 module arithmetic runs with divide/overflow/invalid RAISING (underflow
+       ignored); a FloatingPointError fails closed. Every module-owned returned
+       array and float (identity diagnostics included) is finite-validated
+       before ok=True; any non-finite value fails closed.
+  0428 wording: the base is an axisymmetric continuity/entropy reference; r0 may
+       be nonzero and is never gated; Omega is taken as given.
 
 Implements ONLY sections 3-4 of
   DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt
@@ -35,6 +46,12 @@
 Contract: no I/O, nothing executed at import beyond constant definitions,
 numpy + stdlib only, keyword-only public arguments WITHOUT defaults, every
 failure returns a fail-closed dict {'ok': False, ...} with no partial fields.
+Array inputs are 0-d or rank len(grid_shape) with explicit singleton axes.
+Floating-point divide/overflow/invalid are never suppressed in module
+arithmetic, and ok=True only when every module-owned returned array is finite.
+The base is an axisymmetric reference (stationary leading continuity/entropy);
+the caller's real Omega is used as given and r0 (projected-base Euler residual)
+may be nonzero; no force-balance gate, Omega**2 clipping or radius dropping.
 The module never chooses a grid, discretization, Fourier convention, base,
 derivative, circulation, boundary value, fit, closure, isotropization, ridge,
 pseudoinverse or density clamp; it never drops the induced feedback.
@@ -51,7 +68,7 @@
 
 import numpy as np
 
-MODULE_TAG = 'ddo_noncircular_displacement_action_c2v001'
+MODULE_TAG = 'ddo_noncircular_displacement_action_c2v002'
 FORCING_CONVENTION = ('r0=projected_base_residual;'
                       'dPhi_total=angular_forcing+induced_feedback')
 LAPSE_WEAK = 'weak_field_delta_n'
@@ -66,12 +83,16 @@
                           'angular_forcing_excludes_m0_projection',
                           'angular_forcing_includes_induced_feedback',
                           'r0_provenance', 'angular_forcing_provenance')
+# Module arithmetic: never hide non-finite results (0428). Underflow yields finite values.
+_MODULE_ERRSTATE = {'divide': 'raise', 'over': 'raise', 'invalid': 'raise', 'under': 'ignore'}
 NOT_DONE = (
     'no solve or inversion of the action',
     'no boundary realization; boundary rows only via evaluate_boundary_rows',
     'no resonance treatment, ridge, pseudoinverse or mode deletion',
     'no neutral-mode, circulation or annular-mass constraint fixing',
     'no equilibrium base construction; base and r0 are caller-supplied',
+    'no force-balance gate: r0 may be nonzero; Omega used as given (no Omega**2 '
+    'clipping, no dropped radii, no enforced inward force, no source change)',
     'no metric-dependent quadrature/source-measure corrections (spec s4)',
     'no Fourier transform or kernel solve; the response callback owns both',
     'not a stationary state; no corrected velocities or observation rows',
@@ -111,8 +132,15 @@
     return arr
 
 
-def _grid_array(name, value, grid_shape):
+def _grid_array(name, value, grid_shape, shapes):
     arr = _real_array('input_validation', name, value)
+    if arr.ndim != 0 and arr.ndim != len(grid_shape):
+        raise _Reject('input_validation',
+                      '%s: rank %d (shape %s) rejected for grid_shape %s; pass a 0-d scalar or '
+                      'a rank-%d array with explicit singleton axes (e.g. f[:, None, None]); '
+                      'lower-rank arrays are never broadcast (numpy right-alignment would '
+                      'apply them along the trailing axes)'
+                      % (name, arr.ndim, arr.shape, grid_shape, len(grid_shape)))
     try:
         ok = np.broadcast_shapes(arr.shape, grid_shape) == grid_shape
     except ValueError:
@@ -121,6 +149,7 @@
         raise _Reject('input_validation',
                       '%s: shape %s not broadcast-compatible to grid_shape %s'
                       % (name, arr.shape, grid_shape))
+    shapes[name] = tuple(int(n) for n in arr.shape)
     return _readonly(np.broadcast_to(arr, grid_shape))
 
 
@@ -144,11 +173,11 @@
     return value
 
 
-def _triple(name, value, grid_shape):
+def _triple(name, value, grid_shape, shapes):
     if not isinstance(value, tuple) or len(value) != 3:
         raise _Reject('input_validation',
                       name + ': tuple of exactly three components (R, phi, z) required')
-    return tuple(_grid_array('%s[%s]' % (name, c), v, grid_shape)
+    return tuple(_grid_array('%s[%s]' % (name, c), v, grid_shape, shapes)
                  for c, v in zip(('R', 'phi', 'z'), value))
 
 
@@ -190,6 +219,23 @@
     return dict((k, decl[k]) for k in FORCING_PARTITION_KEYS)
 
 
+def _require_finite_outputs(obj, path):
+    """Fail closed if any module-owned returned array/float is non-finite (0428)."""
+    if isinstance(obj, np.ndarray):
+        if obj.dtype.kind not in 'fiu' or not np.all(np.isfinite(obj)):
+            raise _Reject('output_validation', '%s: non-finite or non-real returned array; '
+                          'no residual or diagnostic is returned' % path)
+    elif isinstance(obj, (float, np.floating)):
+        if not math.isfinite(float(obj)):
+            raise _Reject('output_validation', '%s: non-finite returned value' % path)
+    elif isinstance(obj, Mapping):
+        for k, v in obj.items():
+            _require_finite_outputs(v, '%s[%r]' % (path, k))
+    elif isinstance(obj, (tuple, list)):
+        for i, v in enumerate(obj):
+            _require_finite_outputs(v, '%s[%d]' % (path, i))
+
+
 def evaluate_bulk_action(*, grid_shape, R, phi, z, rho0, K0, P0, Omega, gamma,
                          xi, partial_R, partial_phi, partial_z,
                          derivative_rule_description, base_derivative_mode,
@@ -205,9 +251,10 @@
     callback's full output is retained unmodified as 'induced_response_full'.
     """
     caller_err = np.geterr()
+    trace = ['input_validation']
     try:
-        with np.errstate(all='ignore'):
-            return _bulk(caller_err=caller_err, grid_shape=grid_shape, R=R, phi=phi, z=z,
+        with np.errstate(**_MODULE_ERRSTATE):
+            return _bulk(caller_err=caller_err, trace=trace, grid_shape=grid_shape, R=R, phi=phi, z=z,
                          rho0=rho0, K0=K0, P0=P0, Omega=Omega, gamma=gamma, xi=xi,
                          partial_R=partial_R, partial_phi=partial_phi, partial_z=partial_z,
                          derivative_rule_description=derivative_rule_description,
@@ -223,11 +270,15 @@
                          forcing_partition=forcing_partition)
     except _Reject as rej:
         return _fail(rej.stage, rej.reason)
+    except FloatingPointError as exc:  # module arithmetic only; callbacks run under caller errstate
+        return _fail('floating_point', 'module arithmetic during %s raised FloatingPointError (%s); '
+                     'divide/overflow/invalid are not suppressed and no value is returned'
+                     % (trace[-1], exc))
     except Exception as exc:  # fail closed on anything unforeseen
         return _fail('internal', '%s: %s' % (type(exc).__name__, exc))
 
 
-def _bulk(*, caller_err, grid_shape, R, phi, z, rho0, K0, P0, Omega, gamma, xi,
+def _bulk(*, caller_err, trace, grid_shape, R, phi, z, rho0, K0, P0, Omega, gamma, xi,
           partial_R, partial_phi, partial_z, derivative_rule_description,
           base_derivative_mode, base_derivatives, base_axisymmetry_rtol,
           polytrope_consistency_rtol, c_light, unit_system, induced_response,
@@ -239,19 +290,20 @@
                    or n < 1 for n in grid_shape)):
         raise _Reject('input_validation', 'grid_shape: nonempty tuple of positive ints required')
     gs = tuple(int(n) for n in grid_shape)
+    shapes = {}
     _text('derivative_rule_description', derivative_rule_description)
     _text('unit_system', unit_system)
     for name, op in (('partial_R', partial_R), ('partial_phi', partial_phi),
                      ('partial_z', partial_z), ('induced_response', induced_response)):
         if not callable(op):
             raise _Reject('input_validation', name + ': callable required')
-    Rg = _grid_array('R', R, gs)
-    phig = _grid_array('phi', phi, gs)
-    zg = _grid_array('z', z, gs)
-    rho = _grid_array('rho0', rho0, gs)
-    K = _grid_array('K0', K0, gs)
-    P = _grid_array('P0', P0, gs)
-    W = _grid_array('Omega', Omega, gs)
+    Rg = _grid_array('R', R, gs, shapes)
+    phig = _grid_array('phi', phi, gs, shapes)
+    zg = _grid_array('z', z, gs, shapes)
+    rho = _grid_array('rho0', rho0, gs, shapes)
+    K = _grid_array('K0', K0, gs, shapes)
+    P = _grid_array('P0', P0, gs, shapes)
+    W = _grid_array('Omega', Omega, gs, shapes)   # caller's real Omega, used as given
     gam = _scalar('gamma', gamma, positive=True)
     c = _scalar('c_light', c_light, positive=True)
     ax_rtol = _scalar('base_axisymmetry_rtol', base_axisymmetry_rtol, positive=False)
@@ -264,9 +316,9 @@
         raise _Reject('input_validation', 'P0: strictly positive pressure required; no clamp')
     if not np.all(K > 0):
         raise _Reject('input_validation', 'K0: strictly positive polytropic K required')
-    xR, xP, xZ = _triple('xi', xi, gs)
-    r0R, r0P, r0Z = _triple('base_residual_r0', base_residual_r0, gs)
-    forcing = _grid_array('angular_forcing_dPhi', angular_forcing_dPhi, gs)
+    xR, xP, xZ = _triple('xi', xi, gs, shapes)
+    r0R, r0P, r0Z = _triple('base_residual_r0', base_residual_r0, gs, shapes)  # may be nonzero
+    forcing = _grid_array('angular_forcing_dPhi', angular_forcing_dPhi, gs, shapes)
     if lapse_variation_form not in (LAPSE_WEAK, LAPSE_EXACT):
         raise _Reject('input_validation', 'lapse_variation_form: %r or %r required'
                       % (LAPSE_WEAK, LAPSE_EXACT))
@@ -276,7 +328,7 @@
                 SUPPLIED_BASE_DERIVATIVE_KEYS):
             raise _Reject('input_validation', 'base_derivatives: mapping with exact keys %s '
                           'required in supplied mode' % (SUPPLIED_BASE_DERIVATIVE_KEYS,))
-        bd = dict((k, _grid_array('base_derivatives[%s]' % k, base_derivatives[k], gs))
+        bd = dict((k, _grid_array('base_derivatives[%s]' % k, base_derivatives[k], gs, shapes))
                   for k in SUPPLIED_BASE_DERIVATIVE_KEYS)
     elif base_derivative_mode == BASE_DERIV_CALLBACKS:
         if base_derivatives is not None:
@@ -288,6 +340,7 @@
                       % (BASE_DERIV_CALLBACKS, BASE_DERIV_SUPPLIED))
 
     # ---------------- base checks (polytrope relation the dP formula relies on)
+    trace.append('base_checks')
     pol_mismatch = float(np.max(np.abs(P - K * rho ** gam) / P))
     if not math.isfinite(pol_mismatch) or pol_mismatch > pol_rtol:
         raise _Reject('base_checks', 'P0 != K0 rho0**gamma: max relative mismatch %r exceeds '
@@ -323,6 +376,8 @@
         bd = dict((k, _readonly(v)) for k, v in bd.items())
 
     # Base axisymmetry == base stationary continuity/entropy for v0 = R Omega e_phi.
+    # This is the only base gate besides the polytrope relation; radial/vertical
+    # force balance is NOT gated (its residual is the caller's r0, possibly nonzero).
     ax_ratio = {}
     for fname, f, fphi in (('rho0', rho, bd['rho0_phi']), ('K0', K, bd['K0_phi']),
                            ('P0', P, bd['P0_phi']), ('Omega', W, bd['Omega_phi'])):
@@ -338,11 +393,14 @@
         if not ratio <= ax_rtol:
             raise _Reject('base_checks', 'base not axisymmetric within base_axisymmetry_rtol: '
                           'max|d_phi %s|/max|%s| = %r > %r; spec s3 equations assume an '
-                          'axisymmetric equilibrated base' % (fname, fname, ratio, ax_rtol))
+                          'axisymmetric base (stationary leading continuity/entropy reference; '
+                          'radial/vertical force imbalance belongs in r0 and is not gated)'
+                          % (fname, fname, ratio, ax_rtol))
     base_continuity = bd['rho0_phi'] * W + rho * bd['Omega_phi']   # (1/R) d_phi(rho0 R Omega)
     base_entropy = W * bd['K0_phi']                                  # v0 . grad K0
 
     # ---------------- displacement -> fluid perturbation (spec s3)
+    trace.append('perturbation')
     cs2 = gam * P / rho
     flux_R = Rg * rho * xR
     flux_phi = rho * xP
@@ -364,6 +422,7 @@
             raise _Reject('perturbation', name + ': nonfinite')
 
     # ---------------- source feedback (spec s4): exactly one response call
+    trace.append('source_feedback')
     delta_f_n = -(c * c) * drho
     if not np.all(np.isfinite(delta_f_n)):
         raise _Reject('source_feedback', 'delta_f_n: nonfinite')
@@ -418,6 +477,7 @@
         raise _Reject('source_feedback', 'dPhi_total: nonfinite')
 
     # ---------------- stationary linearized Euler residuals (spec s3)
+    trace.append('euler_residual')
     dPhi_R, dPhi_phi, dPhi_z = dR(dPhi), dphi(dPhi), dz(dPhi)
     dP_R, dP_phi, dP_z = dR(dP), dphi(dP), dz(dP)
     dvR_phi, dvP_phi, dvZ_phi = dphi(dvR), dphi(dvP), dphi(dvZ)
@@ -449,7 +509,9 @@
             raise _Reject('euler_residual', 'residual component %s: nonfinite' % comp)
         residual[comp] = _readonly(total)
 
-    # ---------------- diagnostics only (analytically zero about an axisymmetric base)
+    # ---------------- diagnostics (analytically zero about an axisymmetric base); values not
+    # gated, but they are finite-validated with every other returned array below (0428)
+    trace.append('identity_diagnostics')
     lin_cont = (dR(Rg * rho * dvR) / Rg + dphi(rho * dvP + drho * Rg * W) / Rg
                 + dz(rho * dvZ))
     lin_ent = W * dphi(dK) + dvR * bd['K0_R'] + dvP * bd['K0_phi'] / Rg + dvZ * bd['K0_z']
@@ -467,8 +529,9 @@
                            'partial_z': partial_z, 'grid_shape': gs,
                            'unit_system': unit_system,
                            'derivative_rule_description': derivative_rule_description})
-    return {
+    result = {
         'ok': True, 'module': MODULE_TAG, 'stage': 'bulk_action_evaluated', 'grid_shape': gs,
+        'input_shapes': shapes,
         'perturbations': {'drho': ro(drho), 'dK': ro(dK), 'dP': ro(dP), 'cs2': ro(cs2),
                           'dv_R': ro(dvR), 'dv_phi': ro(dvP), 'dv_z': ro(dvZ),
                           'lagrangian_dP': ro(lagrangian_dP)},
@@ -491,7 +554,8 @@
             'linearized_continuity': ro(lin_cont), 'linearized_entropy': ro(lin_ent),
             'scope': 'div(rho0 dv + drho v0) and v0.grad dK + dv.grad K0 via the caller '
                      'callbacks; analytically zero about an axisymmetric base; nonzero values '
-                     'measure base residual or derivative-rule (non)commutation, not gated'},
+                     'measure base residual or derivative-rule (non)commutation; values not '
+                     'gated; finite-validated (a non-finite value fails the whole call closed)'},
         'forcing_partition': partition,
         'conventions': {
             'components': 'physical orthonormal cylindrical (R, phi, z); d_phi per radian',
@@ -509,6 +573,14 @@
                          'euler_residual',
         'boundary_state': types.MappingProxyType(boundary_state),
     }
+    # ---------------- 0428: ok=True only if every module-owned returned value is finite.
+    # 'induced_response_full' is the caller's object, retained by identity and not a module
+    # residual/diagnostic; its lapse arrays actually used are validated above and in lapse_used.
+    trace.append('output_validation')
+    for key, val in result.items():
+        if key != 'induced_response_full':
+            _require_finite_outputs(val, key)
+    return result
 
 
 def evaluate_boundary_rows(*, bulk_result, boundary_row_callbacks):
@@ -521,7 +593,7 @@
     """
     caller_err = np.geterr()
     try:
-        with np.errstate(all='ignore'):
+        with np.errstate(**_MODULE_ERRSTATE):
             if (not isinstance(bulk_result, Mapping) or bulk_result.get('ok') is not True
                     or bulk_result.get('module') != MODULE_TAG
                     or not isinstance(bulk_result.get('boundary_state'),
@@ -556,5 +628,7 @@
                              'the bulk residual; no boundary values invented'}
     except _Reject as rej:
         return _fail(rej.stage, rej.reason)
+    except FloatingPointError as exc:
+        return _fail('floating_point', 'module arithmetic raised FloatingPointError (%s)' % exc)
     except Exception as exc:
         return _fail('internal', '%s: %s' % (type(exc).__name__, exc))
````

### 5.2 INTERFACE: `diff -u INTERFACE_0427_V001.md INTERFACE_0427_V002.md`

````diff
--- INTERFACE_0427_V001.md	2026-10-16 10:49:07.612082423 -0500
+++ INTERFACE_0427_V002.md	2026-10-16 11:13:59.223180519 -0500
@@ -1,12 +1,20 @@
-# INTERFACE 0427 V001: noncircular displacement action (Claude2, c2v001)
+# INTERFACE 0427 V002: noncircular displacement action (Claude2, c2v002)
 
-Module: `ddo_noncircular_displacement_action_c2v001.py` (same folder). It is inert: no I/O, nothing runs at import, it uses numpy and the stdlib only, public arguments are keyword-only with no defaults, and every failure returns a fail-closed dict.
+Module: `ddo_noncircular_displacement_action_c2v002.py` (same folder). It is inert: no I/O, nothing runs at import, it uses numpy and the stdlib only, public arguments are keyword-only with no defaults, and every failure returns a fail-closed dict.
 
-Binding inputs (sha256 checked from bytes before implementation):
+This note supersedes `INTERFACE_0427_V001.md` (`1c34edf3fce32f7705382d9f1b802ec2d53ad6b097c57b4fad4bff64af4b60eb`), and c2v002 supersedes `ddo_noncircular_displacement_action_c2v001.py` (`6b4f2cc6ee0e0c1a4408e555004b510d2d11058bc6f3e9cc82f6ce697ef9e482`). Both earlier files are preserved unchanged. V002 changes only what resolves the following, mapped in `FIX_DELTA_0427_V002.md`:
+- **B1** (interface review): lower-rank arrays were silently broadcast along the wrong axis. Fixed in code; §2 and §6.
+- **B2** (interface review): a missing fact about where the free surface lies and the surface-mass source. INTERFACE only, no code change; §7 facts 7 and 10.
+- **0428-F** (Codex 0428): non-finite identity diagnostics were returned with ok=True. Fixed in code; §3 and §6.
+- **0428-B** (Codex 0428): base wording. The base is not a force-balance gate, r0 may be nonzero, and Omega is used as given. Code wording plus §2, §4 and §7 fact 4.
+
+Binding inputs (sha256 checked from bytes before the fix):
 - Task 0427: `1e9e7cfb4be32cae313543374edb76c647a14530720cb276c83f6e464e95c164`
+- Codex 0428 `0428_2026-10-16_0427_finite_diagnostics_and_base_clarification.md`: `e94cc68d2ebde91ae839f7a960e964ef909474358993028d860088164266da60`
 - Equation spec `DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt`: `d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4` (sections 2-7)
 - Equation review `NONCIRCULAR_DISPLACEMENT_EQUATIONS_REVIEW_V001.json`: `99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e`
-- Context, read as text only: `galaxy_coupled_fourier_hi_prediction_v006.py` `e0d0888de2487c9de1346b4268c0ef9c12401965134333741b389bb3a5cdca79` and `owned_physical_fourier_metric_quadrature_v004.py` `61dc1369726413cda55e87b6175adccce095c65495cb3d94afbff1b50a255582` (source Fourier convention only).
+- Context, read as text only: `galaxy_coupled_fourier_hi_prediction_v006.py` `e0d0888de2487c9de1346b4268c0ef9c12401965134333741b389bb3a5cdca79` and `owned_physical_fourier_metric_quadrature_v004.py` `61dc1369726413cda55e87b6175adccce095c65495cb3d94afbff1b50a255582` (source Fourier convention only)
+- Distinct reviews of c2v001: `REVIEW_0427_INTERFACE_V001.md` `1df58f47d90c457f0ad952489aa3b6118e8c6588e9abf4e5f3358edfc6496f42` and `REVIEW_0427_EQUATIONS_V001.md` `95eda7c805b6068d7dee442bddfe7586a4f8bcf625c40976d324617db832d21a`
 
 ## 1. Scope
 
@@ -17,9 +25,10 @@
 - realize boundaries
 - treat resonances (no ridge, no pseudoinverse, no mode deletion)
 - fix neutral modes, circulation or annular mass
-- construct the base or r0
+- construct the base or r0, or test the base's radial/vertical force balance
 - apply metric/source-measure corrections
 - run a Fourier transform or a kernel solve
+- supply the surface-displacement source at the rho0→0 surface (§7 fact 10)
 - produce a stationary state, corrected velocities or observation rows
 
 ## 2. Public functions
@@ -34,77 +43,122 @@
 evaluate_boundary_rows(*, bulk_result, boundary_row_callbacks)
 ```
 
+The signatures are unchanged from c2v001.
+
 ### Arguments of `evaluate_bulk_action`
 
-All arrays must be real (int, uint or float up to float64; bool, complex and object are rejected), finite, and broadcast-compatible to `grid_shape`. The module copies them to read-only float64 arrays of exactly `grid_shape`.
+All arrays must be real (int, uint or float up to float64; bool, complex and object are rejected) and finite. The module copies them to read-only float64 arrays of exactly `grid_shape`.
+
+**Rank rule (V002, B1).** Every array argument must be one of these two:
+- **0-d:** a scalar, constant on the grid.
+- **Full rank:** exactly `len(grid_shape)` axes, each of length 1 or equal to that grid axis.
+
+This covers `R`, `phi`, `z`, `rho0`, `K0`, `P0`, `Omega`, each `xi` and `base_residual_r0` component, `angular_forcing_dPhi`, and each supplied base derivative.
+
+Singleton axes must be explicit. On an (N_R, N_phi, N_z) grid:
+- a radial profile is passed as `f[:, None, None]`
+- a vertical profile is passed as `f[None, None, :]`
+- a 1-D array is never accepted
+
+Any other rank is rejected at `input_validation`. The reason states the rank, the shape and this rule, and no callback is called first. The rule exists because numpy aligns shapes from the right. Without it, a 1-D radial profile on a grid with N_R == N_z, or with length equal to N_z, would be applied along z, and the axisymmetry and polytrope gates cannot see that.
+
+The original shape of every accepted array is recorded in the result under `input_shapes`.
 
 | argument | meaning / units (SI shown; any caller-consistent system allowed) |
 |---|---|
 | `grid_shape` | nonempty tuple of positive ints. The grid layout and axis order belong to the caller. |
 | `R`, `phi`, `z` | physical cylindrical node coordinates [m, rad, m]. R > 0 everywhere. The module uses only R algebraically; phi and z go to boundary callbacks. |
-| `rho0` | base density [kg m^-3], > 0 everywhere. Never clamped. |
+| `rho0` | base density [kg m^-3], > 0 everywhere. Never clamped. This excludes the rho0→0 surface from the grid; see §7 fact 10. |
 | `K0` | base polytropic K [Pa (kg m^-3)^-gamma], > 0 |
 | `P0` | base pressure [Pa], > 0. Must satisfy P0 = K0 rho0**gamma within `polytrope_consistency_rtol` (max relative). |
-| `Omega` | base angular velocity Omega(R,z) [rad s^-1], any sign. Vertical shear is retained. |
+| `Omega` | the caller's real base angular velocity Omega(R,z) [rad s^-1], **used exactly as given**. Any sign is allowed and vertical shear is retained. See the note after this table. |
 | `gamma` | real scalar > 0 (bool rejected) |
 | `xi` | tuple `(xi_R, xi_phi, xi_z)` of physical orthonormal components [m]. xi_phi is a length, not an angle. |
 | `partial_R`, `partial_phi`, `partial_z` | caller's consistent linear derivative operators; see section 3 |
 | `derivative_rule_description` | nonempty provenance string for the derivative rule |
 | `base_derivative_mode` | `'caller_derivative_callbacks'`: the module computes base derivatives only through the three callbacks. `'supplied'`: the caller gives them all. |
 | `base_derivatives` | `None` in callbacks mode. In supplied mode, a mapping with exactly the keys `rho0_phi, K0_R, K0_phi, K0_z, P0_R, P0_phi, P0_z, Omega_R, Omega_phi, Omega_z` (d_phi per radian). Mixing the two modes is rejected. |
-| `base_axisymmetry_rtol` | >= 0. For each f in {rho0, K0, P0, Omega}, max\|d_phi f\| / max\|f\| must not exceed it. This is the base stationary continuity/entropy precondition, because the spec s3 equations assume an axisymmetric base. |
+| `base_axisymmetry_rtol` | >= 0. For each f in {rho0, K0, P0, Omega}, max\|d_phi f\| / max\|f\| must not exceed it. This checks the base as the stationary leading continuity/entropy reference: an axisymmetric rho0 and K0 carried by v0 = R Omega e_phi conserve mass and entropy at leading order. **It is not an equilibrium or force-balance gate.** With the polytrope relation, it is the only base gate. |
 | `polytrope_consistency_rtol` | >= 0 (see `P0`) |
 | `c_light` | > 0 [m s^-1], in the same unit system |
 | `unit_system` | nonempty declaration, e.g. `'SI'` |
 | `induced_response` | the caller's complete native response; see section 3 |
 | `lapse_variation_form` | `'weak_field_delta_n'` (dPhi = c^2 delta_n) or `'exact_ln_N_first_variation'` (dPhi = c^2 delta_N/N0). There is no default and no silent choice. |
 | `angular_forcing_dPhi` | the caller's angular forcing potential [m^2 s^-2]: the saved-field potential on this grid minus its m=0 projection |
-| `base_residual_r0` | tuple `(r0_R, r0_phi, r0_z)`, the projected-base acceleration residual [m s^-2] in physical components (sign in section 4) |
+| `base_residual_r0` | tuple `(r0_R, r0_phi, r0_z)`: the projected-base Euler residual [m s^-2] in physical components, sign in section 4. **It may be nonzero**, as the reviewed spec s3 explicitly allows. It is never tested and never required to vanish. It enters each residual component exactly once. |
 | `forcing_partition` | declaration mapping; see section 5 |
 
+**What the module does with Omega (V002, 0428-B).** It takes the caller's real Omega as given. It never derives Omega from a force balance, never forms or clips Omega**2, never drops radii, never enforces an inward force and never changes the source. Some reference nodes have no real circular balance, because the radial pressure gradient exceeds an inward lapse force. At those nodes the caller's chosen real Omega is still used, and the full radial/vertical Euler imbalance stays in r0. The success result carries this statement in `not_done`.
+
 ## 3. Callback signatures
 
-- `partial_R(f)`, `partial_phi(f)`, `partial_z(f)`. The argument is one positional read-only float64 array of exactly `grid_shape`. Each must return a real finite array of exactly `grid_shape`: d/dR, d/dphi (per radian) and d/dz on the caller's grid. They must be linear and mutually consistent. The module never picks a stencil, spectral rule or grid library. They run under the caller's own numpy errstate.
-- `induced_response(*, delta_f_n)`. This is called exactly once, and only after every other validation has passed.
-  - Input: a read-only array `delta_f_n = -c_light**2 * drho` [J m^-3] on the grid. It is the signed leading mass-source perturbation, and the module checks that the callback did not mutate it.
+- **Derivatives:** `partial_R(f)`, `partial_phi(f)`, `partial_z(f)`.
+  - The argument is one positional read-only float64 array of exactly `grid_shape`.
+  - Each must return a real finite array of exactly `grid_shape`: d/dR, d/dphi (per radian) and d/dz on the caller's grid.
+  - They must be linear and mutually consistent. The module never picks a stencil, spectral rule or grid library.
+  - They run under the caller's own numpy errstate.
+- **Response:** `induced_response(*, delta_f_n)`. It is called exactly once, and only after every other validation has passed. It runs under the caller's own numpy errstate.
+  - Input: a read-only array `delta_f_n = -c_light**2 * drho` [J m^-3] on the grid. It is the signed leading mass-source perturbation of the bulk only (see §7 fact 10). The module checks that the callback did not mutate it.
   - Output: a mapping with at least two keys:
-    - `'native_response'`: the complete native 10-field response, not None. The module retains it unmodified, without copying or mutating it, as `'induced_response_full'`.
+    - `'native_response'`: the complete native 10-field response, not None. The module retains the whole callback output mapping unmodified, by identity, as `'induced_response_full'`.
     - `'lapse_component'`: exactly one of:
       - `{'form': 'weak_field_delta_n', 'delta_n': array}`
       - `{'form': 'exact_ln_N_first_variation', 'delta_N': array, 'N0': array}`, with N0 > 0.
   - Lapse arrays must be real, finite and exactly `grid_shape`. Extra keys, mixed keys, or a form that differs from `lapse_variation_form` are rejected.
   - The callback owns the Fourier transform. The existing convention (read from v004) is source F(k) = ∫ dV exp(-i k·x) f(x), with inverse x(x) = Σ_q w_q exp(+i k_q·x) x̃_q / (2π)^3. The callback also owns the kernel solve, k=0 handling, the reality tolerance and the extraction of n.
-- `boundary_row_callbacks[name](*, fields)`. `fields` is a read-only `MappingProxyType` with these entries:
+- **Boundary rows:** `boundary_row_callbacks[name](*, fields)`. `fields` is a read-only `MappingProxyType` with these entries:
   - read-only arrays: grid, base fields, base derivatives, `xi_R/xi_phi/xi_z`, `drho, dK, dP, cs2, dv_R, dv_phi, dv_z, lagrangian_dP, dPhi_total`
   - the three derivative callbacks
   - `grid_shape`, `unit_system`, `derivative_rule_description`
 
   Each callback must return a real finite array with ndim >= 1 and size >= 1.
 
-## 4. Equations to code (line numbers in the c2v001 file)
+**Floating point (V002, 0428-F).** The module's own arithmetic runs under `numpy.errstate(divide='raise', over='raise', invalid='raise', under='ignore')`. Underflow is ignored because it can only give finite values.
+- Any division by zero, overflow or invalid operation in module arithmetic fails closed with stage `floating_point`. The reason names the phase: `input_validation`, `base_checks`, `perturbation`, `source_feedback`, `euler_residual`, `identity_diagnostics` or `output_validation`.
+- This also catches an intermediate overflow that a later operation would turn into a finite but wrong value. One example is `rho0**2` overflowing, so that `drho P0_R / rho0**2` silently becomes 0.
+- The caller's errstate is restored on return. The callbacks run under it.
+
+## 4. Equations to code (line numbers in the c2v002 file)
+
+The equations and their code are unchanged from c2v001; they are shifted by +58 lines.
 
 | spec s3/s4 | code |
 |---|---|
-| cs2 = gamma P0/rho0 | L346 |
-| drho = -div(rho0 xi), cylindrical: (1/R) d_R(R rho0 xi_R) + (1/R) d_phi(rho0 xi_phi) + d_z(rho0 xi_z) | L347-351 (conservative form, 1/R applied after d_R) |
-| dK = -xi·grad K0 = -(xi_R K0_R + xi_phi K0_phi/R + xi_z K0_z) | L352 |
-| dP = cs2 drho + rho0^gamma dK | L353 |
-| dv_R = Omega d_phi xi_R; dv_z = Omega d_phi xi_z; dv_phi = Omega d_phi xi_phi - R(Omega_R xi_R + Omega_z xi_z) | L357-359 |
-| Lagrangian dP + xi·grad P0 (s5 free-surface quantity; a field only, never imposed) | L360 |
-| df_n = -c^2 drho, one response call | L367, L373 |
-| dPhi_induced = c^2 delta_n (weak) or c^2 delta_N/N0 (exact) | L404 / L414 |
-| dPhi_total = angular forcing + induced, each once | L416 |
-| radial residual: Omega d_phi dv_R - 2 Omega dv_phi + d_R dPhi + d_R dP/rho0 - drho P0_R/rho0^2 + r0_R | L424-427; order L436-441; summed L442-450 |
-| angular residual: Omega d_phi dv_phi + (2 Omega + R Omega_R) dv_R + R Omega_z dv_z + d_phi dPhi/R + d_phi dP/(rho0 R) + r0_phi | L428-432 |
-| vertical residual: Omega d_phi dv_z + d_z dPhi + d_z dP/rho0 - drho P0_z/rho0^2 + r0_z | L433-435 |
-| base continuity/entropy residuals (d_phi(rho0 Omega), Omega K0_phi) | L342-343 |
-| diagnostics: div(rho0 dv + drho v0) and v0·grad dK + dv·grad K0 | L453-455 |
+| cs2 = gamma P0/rho0 | L404 |
+| drho = -div(rho0 xi), cylindrical: (1/R) d_R(R rho0 xi_R) + (1/R) d_phi(rho0 xi_phi) + d_z(rho0 xi_z) | L405-409 (conservative form, 1/R applied after d_R) |
+| dK = -xi·grad K0 = -(xi_R K0_R + xi_phi K0_phi/R + xi_z K0_z) | L410 |
+| dP = cs2 drho + rho0^gamma dK | L411 |
+| dv_R = Omega d_phi xi_R; dv_z = Omega d_phi xi_z; dv_phi = Omega d_phi xi_phi - R(Omega_R xi_R + Omega_z xi_z) | L415-417 |
+| Lagrangian dP + xi·grad P0 (s5 free-surface quantity; a field only, never imposed) | L418 |
+| df_n = -c^2 drho, one response call | L426, L432 |
+| dPhi_induced = c^2 delta_n (weak) or c^2 delta_N/N0 (exact) | L463 / L473 |
+| dPhi_total = angular forcing + induced, each once | L475 |
+| radial residual: Omega d_phi dv_R - 2 Omega dv_phi + d_R dPhi + d_R dP/rho0 - drho P0_R/rho0^2 + r0_R | L484-487; order L496-501; summed L502-510 |
+| angular residual: Omega d_phi dv_phi + (2 Omega + R Omega_R) dv_R + R Omega_z dv_z + d_phi dPhi/R + d_phi dP/(rho0 R) + r0_phi | L488-492 |
+| vertical residual: Omega d_phi dv_z + d_z dPhi + d_z dP/rho0 - drho P0_z/rho0^2 + r0_z | L493-495 |
+| base continuity/entropy residuals (d_phi(rho0 Omega), Omega K0_phi) | L399-400 |
+| diagnostics: div(rho0 dv + drho v0) and v0·grad dK + dv·grad K0 | L515-517 |
+
+These lines are new in V002:
+
+| new in V002 | code |
+|---|---|
+| module errstate constant (raise divide/over/invalid; ignore under) | L87 |
+| rank rule; recording of input shapes | L137-143; L152 |
+| finite sweep of module-owned outputs | helper L222-236; applied L576-583 |
+| errstate applied; FloatingPointError fails closed | L256, L273-276; boundary rows L596, L631-632 |
+| `not_done` line: no force-balance gate, Omega used as given | L94-95 |
+
+**Residual sign.** Each residual is the spec's LHS minus its RHS, so a solution gives zero. With this sign, r0 is the projected-base acceleration residual (v0·∇)v0 + ∇Φ0 + ∇P0/ρ0. For an axisymmetric base:
+- r0_R = P0_R/rho0 + Phi0_R - R Omega^2
+- r0_z = P0_z/rho0 + Phi0_z
+- r0_phi = 0 unless supplied
 
-Each residual is the spec's LHS minus its RHS, so a solution gives zero. With this sign, r0 must be the projected-base acceleration residual (v0·∇)v0 + ∇Φ0 + ∇P0/ρ0. For an axisymmetric base that means r0_R = P0_R/rho0 + Phi0_R - R Omega^2, r0_z = P0_z/rho0 + Phi0_z, and r0_phi = 0 unless supplied.
+**r0 is in general nonzero.** The projected base need not be in radial/vertical force balance. Its full radial/vertical Euler residual stays in r0, and the module neither tests it nor removes it.
 
 All derivatives of dP, dPhi_total and dv go through the caller callbacks. The analytic gradient that the response may carry is retained in `induced_response_full` but is not used.
 
-## 5. Forcing partition (fixed for 0427)
+## 5. Forcing partition (fixed for 0427; unchanged)
 
 `forcing_partition` must have exactly these keys:
 - `convention == 'r0=projected_base_residual;dPhi_total=angular_forcing+induced_feedback'`
@@ -126,64 +180,129 @@
 
 ## 6. Return keys
 
-On failure the result is exactly `{'ok': False, 'module', 'stage', 'reason'}`. The stage is one of `input_validation | forcing_partition | base_checks | derivative_callback | perturbation | source_feedback | euler_residual | internal`. No partial fields are returned.
+**On failure** the result is exactly `{'ok': False, 'module', 'stage', 'reason'}`. No partial fields are returned. The stage is one of:
+- `input_validation`
+- `forcing_partition`
+- `base_checks`
+- `derivative_callback`
+- `perturbation`
+- `source_feedback`
+- `euler_residual`
+- `floating_point` (new in V002)
+- `output_validation` (new in V002)
+- `internal`
 
-On success the result has `'ok': True, 'module', 'stage', 'grid_shape'` plus:
+**On success** the result has `'ok': True, 'module', 'stage', 'grid_shape'` plus:
+- `input_shapes` (new in V002): a mapping from argument name to the original shape tuple of each accepted array. `()` means 0-d. Keys are the argument names, with components as `xi[R]` and `base_residual_r0[z]`, and supplied derivatives as `base_derivatives[K0_R]`.
 - `perturbations`: `drho, dK, dP, cs2, dv_R, dv_phi, dv_z, lagrangian_dP`
 - `source_feedback`: `delta_f_n`, `response_call_count` (=1), `lapse_variation_form`, `lapse_used`, `dPhi_forcing`, `dPhi_induced`, `dPhi_total`
 - `induced_response_full`: the callback output object, unmodified
-- `euler_residual`: `{'R','phi','z'}`
+- `euler_residual`: `{'R','phi','z'}`, all three components
 - `euler_terms`: per-component term arrays, summed in a fixed order
 - `base_checks`: `polytrope_max_relative_mismatch`, `axisymmetry_max_ratio`, `base_continuity_residual`, `base_entropy_residual`, `base_derivative_mode`, `base_derivatives`
-- `identity_diagnostics`: `linearized_continuity`, `linearized_entropy`, `scope`. These are not gated. They are zero analytically; a nonzero value measures base residual or non-commuting derivative rules.
+- `identity_diagnostics`: `linearized_continuity`, `linearized_entropy`, `scope`. Their values are not gated. They are zero analytically; a nonzero value measures base residual or non-commuting derivative rules.
 - `forcing_partition`, `conventions`, `not_done`
 - `boundary_rows`: the string `NOT_EVALUATED...`
 - `boundary_state`: a read-only mapping for `evaluate_boundary_rows`
 
 All arrays are read-only float64.
 
-`evaluate_boundary_rows` returns `{'ok': True, 'boundary_rows': {name: array}, 'call_counts', 'scope'}`. Rows are unweighted and are never added to `euler_residual`.
+**Finite guarantee (V002, 0428-F).** `ok` is True only if every module-owned returned array and float is finite. That covers every key above except `induced_response_full`, and it includes both identity diagnostics, the base residuals, all Euler terms, `lapse_used` and every array in `boundary_state`.
+- A non-finite value fails the whole call closed with stage `output_validation` or `floating_point`.
+- No "unavailable diagnostic" status exists. Whenever ok=True, every returned residual and diagnostic is a finite array, and no non-finite value is ever returned as one.
+- `induced_response_full` is the caller's object, retained by identity. It is not a module residual or diagnostic and is not traversed. The lapse arrays the module actually uses are validated as finite, and their read-only copies are returned under `source_feedback['lapse_used']`.
 
-The action is affine: L[xi] = action(xi) - action(0) when the callbacks and the response are linear. action(0) is grad(angular forcing) + r0.
+**Boundary rows.** `evaluate_boundary_rows` returns `{'ok': True, 'boundary_rows': {name: array}, 'call_counts', 'scope'}`. Rows are unweighted and are never added to `euler_residual`. They run under the same module errstate (stage `floating_point` on a floating-point error) and must be finite.
+
+**The action is affine.** L[xi] = action(xi) - action(0) when the callbacks and the response are linear. action(0) is grad(angular forcing) + r0.
 
 ## 7. Missing interface facts Root must supply
 
 1. **Response adapter.** This is the actual `induced_response`. It must:
-   - transform grid-sampled `delta_f_n` with the existing v004 convention. That needs the physical volume quadrature on this grid (R dR dphi dz weights), the k-node set and weights, the finite-domain/tail scope, and k=0 handling, which v004 refuses and assigns to the boundary/normal solution.
+   - transform grid-sampled `delta_f_n` with the existing v004 convention. That needs the physical volume quadrature on this grid (R dR dphi dz weights), the k-node set and weights, the finite-domain/tail scope, and k=0 handling, which v004 refuses and assigns to the boundary/normal solution. See also fact 10.
    - solve through the same complete kernel at the declared fixed coefficient/state point
    - evaluate on the grid nodes (Cartesian↔cylindrical mapping)
    - check reality with its own tolerance
    - extract the lapse field, which is n at index 0 of (n, C_Mandel6, mu3) in v004 ordering. Root must confirm this, and confirm which source column.
 2. **Other nine source components.** The spec keeps them "as admitted in that branch". Root must state whether they are unperturbed under displacement in the leading mass-source approximation, or supply them inside the adapter.
 3. **Lapse relation.** Root must declare whether N = 1 + n, which makes the weak form exact to first order only when N0 ≈ 1, or provide delta_N and N0 for the exact c^2 deltaN/N0 option.
-4. **Equilibrated axisymmetric base.** This means rho0, K0, P0 and Omega(R,z) with gamma, their provenance, Phi0, and r0 in the section 4 sign. The saved circular trial and N-only columns do not supply it (spec s2/s7).
+4. **Axisymmetric reference base (V002 wording, 0428-B).**
+   - **What Root supplies:**
+     - rho0, K0, P0 (polytropic, gamma) and the caller's real Omega(R,z), with provenance and Phi0
+     - r0 = the projected-base Euler residual in the §4 sign. **It may be nonzero.** The reviewed spec s3 allows a nonzero base acceleration residual "not already included in dPhi forcing".
+   - **What the module requires:** only axisymmetry within `base_axisymmetry_rtol` and the polytrope relation within `polytrope_consistency_rtol`. Axisymmetric density and entropy with a real Omega provide the stationary leading continuity/entropy reference.
+   - **What the module does not require:**
+     - radial/vertical force balance
+     - r0 = 0
+     - a positive Omega**2
+     - a particular source
+
+     The full radial/vertical Euler residual remains in r0.
+   - The saved circular trial and N-only columns are not, by themselves, this reference: spec s2/s7 say the base must be independently constructed and its residual evaluated before use. Supplying an arbitrary reference with its residual in r0 yields an evaluable action, not a stationary state. No final stationary-state claim follows.
 5. **Angular forcing array.** The saved-field Phi on this grid minus its m=0 projection, from prepared-field evaluation, with no resampling or rerun.
-6. **Grid and derivative rules.** Consistent operators, including near the radial and free-surface boundaries, plus periodic azimuth, all declared by Root. The gradient of dPhi uses these callbacks, not response-supplied analytic gradients. Using the latter would be a versioned interface change.
+6. **Grid and derivative rules.** Consistent operators, including near the radial and free-surface boundaries, plus periodic azimuth, all declared by Root. The gradient of dPhi uses these callbacks, not response-supplied analytic gradients. Using the latter would be a versioned interface change. Every array argument is passed 0-d or at full rank with explicit singleton axes (§2).
 7. **Boundary rows.** Root must supply:
    - xi·n = 0 on the actual radial source domain
-   - the free surface Lagrangian dP + xi·grad P0 = 0 (the `lagrangian_dP` field is provided), with the surface-location representation
+   - the free surface Lagrangian dP + xi·grad P0 = 0 (the `lagrangian_dP` field is provided), with the surface-location representation. This row is the spec s5 free-surface condition **only at the actual rho0→0 surface**. At a grid face where rho0 > 0 it is not the spec condition (see fact 10).
    - reflection only if the source and metric support it
    - circulation and neutral-mode data, plus the optional annular-mass constraint
 8. **Metric-dependent source-measure corrections** and the retained-order assessment (spec s4/s6), plus full residual re-evaluation at any resulting state.
 9. **Tolerances** for `base_axisymmetry_rtol` and `polytrope_consistency_rtol`, chosen by Root. No default is supplied.
+10. **Free-surface position and the surface-mass source (V002, B2).**
+    - **Why the bulk source is not mass-conserving at the faces.** The module requires rho0 > 0 and P0 > 0 at every node, so the grid can never contain the zero-density polytropic surface that spec s5 relies on ("no spurious surface-mass delta"). At any grid face where rho0 > 0 and xi·n ≠ 0 (typically the top and bottom faces), the bulk `drho = -div(rho0 xi)` omits the mass carried across that face. Its volume integral is ∫ drho dV = −∮ rho0 xi·n dA, not zero. So `delta_f_n` carries a spurious net mass: k→0 content, which v004 refuses.
+    - **What Root must state:** where the physical rho0→0 surface lies relative to the grid faces.
+    - **Then Root must do one of the following:**
+      - (a) supply the boundary-layer surface-displacement source contribution inside the response adapter, consistent with v004's k=0/boundary-normal assignment
+      - (b) give the retained-order assessment showing it is negligible
+    - **What the module does:** it is unchanged and supplies neither. It has no quadrature and does not choose one.
+    - **Illustration:** fixture B2 in §8 confirms the identity algebraically.
 
 ## 8. Fixtures run (NONPHYSICAL, algebraic only)
 
-The fixtures live in the scratchpad (`test_0427_algebraic_fixtures.py`). They were run with `python3 -I -B` (codex runtime, numpy 2.3.5, Python 3.12.14). They use synthetic polynomial/trig fields on a 21×16×17 grid, with Chebyshev R and z and FFT phi callbacks that are exact for the fixture. The response is a stub. No project data, run, or target velocities were used.
+The fixtures were run against the published c2v002 bytes (`056db7b19443d4a88dcb6396531dfe1ff61acd8ba8387e6bfd0a8b64cf179925`).
+- **Runtime:** `python3 -I -B` (codex runtime, Python 3.12.14, numpy 2.3.5)
+- **Location:** scratchpad `r0427-fix/`
+- **Data:** synthetic fields only. No project data, run, or target velocities were used.
 
-Result: 93/93 checks passed. The two independent references:
-- **Engine A**, an exact polynomial/trig symbolic engine (gamma = 2, nonlocal stub, weak form). Every output agrees within 2.3e-11 relative, and the continuity and entropy identities are at 3e-13 and 9e-16.
-- **Engine B**, a Cartesian coordinate-free reference: complex-step plus central differences, Lie bracket, and (v0·∇)dv + (dv·∇)v0 + ∇dΦ + ∇dP/ρ0 − δρ∇P0/ρ0² (gamma = 5/3, exact lnN form). All fields and the three residuals agree within 9.7e-11.
-
-The suite also covers:
-- linearity
-- the xi=0 affine part, which is exact
-- the response contract: one call, a bitwise source, a read-only input, mutation detection, and form/key/shape/dtype/N0 rejections
-- forcing-partition rejections
-- 32 validation rejections, none of which calls a callback before static validation
-- boundary-row separation
-- errstate preservation
-- an import audit with no open/os/socket events
-- keyword-only signatures
-
-Twelve planted sign/factor mutants were all detected, each of them by engine B.
+| run | result |
+|---|---|
+| V001 author suite, unchanged file (`89e20cb76a529a920d69ea69b736f9b4fff72e12024dd32fb15eb01d8d67d8b6`), on c2v002 | 93/93 |
+| V002 suite `test_0427_algebraic_fixtures_v002.py` (`3cec22e4ed834d2910b3067c36641d4a8aafcba287268ffbc2c2813887ec0ab1`), on c2v002 | 127/127 (93 unchanged + 34 delta checks) |
+| same V002 suite on c2v001 (contrast) | 107/127. The 20 failing checks are exactly the delta defects. |
+| interface reviewer suite, unmodified (`144b3638a53e9f659436f1ee855dadef85fd828af762fac1f83c6c5adba00279`), on c2v002 | 136/138. The B1 PROBE now passes. See the note below the table for the two expected FAILs. |
+| equation reviewer suite, unmodified (`a56c511ed9b08088b872194adf8de1ad5fee898b6fb927c1a467690823a8b4cd`), on c2v002 | 71/71 |
+| interface reviewer probe `probe_broadcast_square_grid.py` (`336a8c77e8b844b2aa342650bb33b72096137c9712aef1575521783e79606a6c`), on c2v002 | "1-D Omega(R) accepted: False \| explicit (N,1,1) accepted: True". The script then stops with a KeyError because it assumes the 1-D input is accepted. |
+| `probe_nonfinite_diagnostics.py` (`f0f629fe7410879923cd91c2ee57235d21643fd013a9020a39fd50278fa35c19`) | c2v001: ok=True with a non-finite `linearized_entropy`. c2v002: ok=False, stage `floating_point` in `identity_diagnostics`. |
+
+The two expected FAILs in the interface reviewer suite:
+- **Success key set:** it now includes the added `input_shapes` key, by design (B1).
+- **Masked-array PROBE:** this is review note N2, which is outside this fix.
+
+The 34 delta checks are:
+- **B1:**
+  - Rank-1, rank-2 and rank-4 inputs are rejected for every array argument, with zero callbacks first. This includes a 1-D length-N_z Omega that numpy would right-align to z, and 1-D `z`, xi, r0, forcing and supplied-derivative inputs.
+  - On an 8×8×8 square grid:
+    - 1-D Omega(R) is rejected.
+    - (N,1,1) is accepted, with Omega_R = 0.5 and Omega_z = 0 to within 1.5e-14.
+    - The residuals are bitwise equal to the full-array input.
+    - 0-d and an explicit (1,1,N) are accepted and recorded in `input_shapes`.
+- **0428-F:**
+  - On success, every module-owned returned value is finite.
+  - The diagnostic overflow fails closed (`floating_point`, `identity_diagnostics`). The response is called once and errstate is restored. The same happens under the caller's `seterr(all='raise')`.
+  - A hidden `rho0**2` overflow in an Euler term fails closed (`floating_point`, `euler_residual`).
+  - **Layer independence.** A scratch copy with the module errstate set to ignore was run on the same inputs:
+    - The output sweep alone fails closed on `identity_diagnostics['linearized_entropy']`.
+    - The same copy returns the overflowed Euler term as a finite, wrong 0. That is why errors are not suppressed.
+  - Success results are identical under the caller's errstate set to ignore or to raise.
+- **0428-B:**
+  - A sign-changing real Omega with a large nonzero r0 is accepted.
+  - Omega is used bitwise as given.
+  - r0 enters each residual once (1.5e-16).
+  - All three components are returned, with one response call and the full native output retained.
+  - `not_done` states that there is no force-balance gate and no stationary state.
+  - The module text contains no "equilibrated base" gate wording.
+- **B2 (illustration, module unchanged).** On the 21×16×17 Chebyshev/FFT grid, rho0 > 0 on the top and bottom faces and an m=0 xi_z = 0.02 z R is applied. Integrating with Clenshaw–Curtis weights gives ∫drho dV = −1.514248 = −∮ rho0 xi·n dA. That is a nonzero net mass in `delta_f_n` (fact 10).
+
+Engine errors on c2v002 are unchanged from c2v001:
+- **Engine A:** at most 2.3e-11 relative.
+- **Engine B:** at most 9.7e-11.
````
