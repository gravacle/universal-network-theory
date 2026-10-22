# 0389 static review, v001

Reviewer: Claude helper, DISTINCT STATIC REVIEWER role (did not write the code).
Date: 2026-10-15.

## Overall verdict: PASS_WITH_NOTES

The module implements exactly the adopted common-metric circular read, with the domain 0389 states. It inserts no physics, constants or I/O. The notes are about coordinate provenance, a signed-zero edge case, a dead `except` branch, and the assembly having changed since the author pinned it. None of them changes the computed values.

## Bytes reviewed (sha256 computed from bytes)

| File | sha256 | Status |
|---|---|---|
| common_metric_circular_speed_v001.py | 9bfde58f6d2190d1027ffa62269e65806d0145822144d79589476957a583e8f0 | matches brief |
| AUTHOR_NOTES_0389_V001.md | dd3a830b9e78c329b236446de301fb512ac0fefbd241501dbd85ee943986c883 | matches brief |
| FROM_CODEX/0389_..._motion_kernel_implementation.md | a35b406dd0367a1676971a7048a220d7a1c8394dfc2900403342368518b3a65e | matches author pin |
| CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md | efe970305dccddb904d208a9d1a3f9be907b4097eb753a1bcc890cab74dd5296 | CHANGED from the author's 52e8a2c6… pin (see N4); context only |

In the current assembly bytes I read three sections:
- "Existing geometry, gravity and motion" (L809–858);
- "Explicit speed read" (L966–986);
- "Direction-dependent extension" (L988–1045).

The three equation forms there agree with the code.

## Per-item verdicts

### 1. Equation. CONFORMS
The code computes ratio = dlogN / dlogR (L95) and v = c·sqrt(ratio) (L109).

I derived the read by hand. Take the metric −N²c²dt² + R(r)²dφ² + g_rr dr². The radial geodesic condition for a circular orbit is

  −∂_r(N²c²)·ṫ² + ∂_r(R²)·φ̇² = 0.

So Ω² = c²·N·N′/(R·R′). The static observer measures v = R·Ω/N, which gives

  v²/c² = R·N′/(N·R′) = (d ln N/dr)/(d ln R/dr).

This is the code's ratio. Three special cases match the assembly:
- In circumferential coordinates (r = R), d ln R/dR = 1/R, so v² = c²·R·∂_R ln N (assembly L854).
- In isotropic coordinates (R = A·r), the result is r·∂_r ln N / (1 + r·∂_r ln A) (assembly L978–981).
- With a general optical tensor (R = N·sqrt(q_φφ)), it is ∂_r ln N / ∂_r ln R (assembly L1040).

Invariances:
- **Reparametrization.** Under r = r(r̃) with J = dr/dr̃ ≠ 0, both log-derivatives scale by J, so the ratio is unchanged. This includes J < 0 (orientation reversal).
- **Constant rescalings.** N → kN and R → kR (k > 0) shift ln N and ln R by constants, which leaves both derivatives unchanged.

N and R_kpc do not enter the speed (they are validated and carried only), so the module is consistent with these invariances. In floating point, (J·a)/(J·b) equals a/b to roundoff.

### 2. Sign and zero domains. CONFORMS to 0389's "0 <= ratio < 1"
| Case | Code | Verdict |
|---|---|---|
| dlogR_dr = 0 | `dlogR == 0.0` raises (L92–93). −0.0 also compares equal and is rejected. | rejected, as required |
| dlogR_dr < 0 | no sign test; it cancels in the ratio | accepted (orientation); correct |
| ratio < 0 | `not 0.0 <= ratio < 1.0` raises (L100–105); no clipping | rejected, never clipped |
| ratio = 0 | 0.0 <= 0.0 holds, so v = 0 | accepted |
| ratio ≥ 1 | raises | rejected |
| non-finite ratio | raises (L98–99) | fail closed |

All six match 0389 literally. Division by zero cannot occur, because L92 runs first. See N2 for the signed-zero case and N3 for the `except` branch.

### 3. Validation. CONFORMS
- `_finite_real` (L10–20) rejects bool. It requires `numbers.Real`, then `float()` with OverflowError, ValueError and TypeError caught, then `math.isfinite`. NumPy floating and integer scalars are admitted through NumPy's `numbers` registration. np.bool_, complex and Decimal are rejected.
- Positivity: c > 0 (L60), R > 0 (L88) and N > 0 (L90), each tested as `not x > 0.0`, so NaN-safe.
- `metric_rows` must be a list or tuple (L62), so generators are never silently consumed. It must be non-empty (L64), and each row must be a `dict` (L71) with exactly the five keys (L73–76).
- Ids must be `str`, not empty after strip, and unique by exact string (L77–82).
- Rows are processed in one in-order loop with append only (L69–116). Nothing is sorted, clipped, replaced, dropped or inferred, and the original `rid` string is kept.
- Every error message includes the row index and the id once it is known.

### 4. No inserted physics or constants. CONFORMS
There is no mass, halo, Birth-deficit force, potential, Poisson solver, gravity law, weak-field limit, or observer/light correction. The AST shows the only numeric literals are 0 (L64, the `len` test), 0.0 (L60, L88, L90, L92, L100) and 1.0 (L100). There is no default for c_km_s, and no hidden calibration.

### 5. Inert import. CONFORMS
Checked by AST only:
- Module level: `import math`, `import numbers`, `def _finite_real`, `def circular_speed_rows`.
- No decorators, global or nonlocal statements, or module constants.
- Calls are limited to the standard library: math.isfinite, math.sqrt, isinstance, float, len, enumerate, set and str.strip. There is no open, print, sys, os or subprocess.
- Both public arguments are keyword-only and required, with no defaults.

### 6. Labels and provenance. CONFORMS (see N1)
- Per row, semantics is "LOCAL_CIRCULAR_SPEED" and units "km/s" (L113–114); the top level carries the same (L120–121).
- "TOTAL_OBSERVABLE" appears only negated ("NOT TOTAL_OBSERVABLE") in the docstring and scope string.
- Each row reports its ratio, R_kpc and all four numeric inputs (L108–112). The output also carries c_km_s, the equation string and the scope.

### 7. The author's open points
| Point | Assessment |
|---|---|
| No declared radial-coordinate field | CONFORMS. 0389 lists exactly five row fields. The ratio is coordinate-invariant only if both derivatives share one coordinate, and that remains the caller's contract. See N1 for the provenance tension. |
| R_kpc not cross-checked | CONFORMS, and correct. A check such as dlogR_dr = 1/R holds only in a circumferential chart, so it would wrongly reject valid isotropic or general-chart inputs. R_kpc is radius provenance only. |
| Fail on first bad row | CONFORMS. 0389 asks for "an informative error on invalid mathematical domain" and forbids replacing failed rows. Per-row failure records would be a provider-level choice. |
| Empty input rejected | CONFORMS in spirit. It is not stated in 0389, but it fails closed. An empty result could otherwise hide an upstream fault. |
| Exactly five keys | CONFORMS to "Each input row supplies id, R_kpc, N, dlogN_dr, dlogR_dr". It is strict: extra metadata, including any coordinate label, is rejected rather than silently dropped. See N1. |
| Whitespace-only ids rejected | CONFORMS. This is stricter than "nonempty" and fails closed. Manifest-format ids (<object>-Qnn) are unaffected. Padded ids are accepted verbatim and treated as distinct strings (N6). |

## Findings

| ID | Severity | Lines | Finding |
|---|---|---|---|
| N1 | LOW | L66–76, L106–116 | 0389 asks for "input-coordinate/radius provenance", but rows carry no coordinate identity, and the exact-five-key rule prevents a caller from attaching one. Provenance is the raw derivative inputs plus R_kpc. This conforms to the five-field specification. Root or the higher-level provider must record which radial coordinate the derivatives use. |
| N2 | INFO | L95, L100, L109 | A ratio of −0.0 (for example dlogN_dr = 0.0 with dlogR_dr < 0) passes 0.0 <= −0.0. Then sqrt(−0.0) = −0.0, so v_local_km_s = −0.0. This is numerically zero and is not altered, as required, but downstream text output may show "-0.0". |
| N3 | INFO | L94–97 | `except OverflowError` cannot be reached for float/float in CPython. Overflowing division returns inf rather than raising. L98 `isfinite` catches that case, so it still fails closed. Harmless. |
| N4 | INFO (custody) | AUTHOR_NOTES L14 | The live assembly changed from 52e8a2c6… (author pin) to efe97030… (mtime 18:09). The formulas the code relies on agree in the current bytes: L854, L978–981, L1040, plus the conditions at L986 and L1045. I cannot diff the earlier version. |
| N5 | INFO | L113, L120 | The "km/s" label is nominal. v inherits the unit of the caller-supplied c_km_s, as documented by the argument name. |
| N6 | INFO | L78–81 | Ids are compared as exact strings. "A" and "A " are distinct and both accepted. |
| N7 | INFO | L84–87, L112 | Inputs are reported after `float()` conversion, so a Fraction input is rounded. The author noted this. |

The branch conditions are vertical balance c0²∂_zN² = Ω²∂_z h_φφ, radial and vertical orbital stability, and validity bounds. 0389 ("vertical balance supplied by the parent calculation") and assembly L986 and L1045 leave them to the parent, so the module rightly does not check them.

## Unresolved points (for root)
1. Where the declared radial coordinate is recorded, so that both derivatives are certified to share it (N1).
2. Whether the higher-level provider wants fail-fast or per-row failure records. The current fail-fast behaviour conforms.
3. Re-pin the assembly hash in the author notes if custody requires it (N4).

## Execution statement
Nothing was executed or imported. The module was never imported or run, and no tests or examples were performed.

The only Python run on the module was `python3 -I -B -c "import ast,sys; ..."` AST parsing. It listed:
- module-level nodes, decorators, imports and global statements;
- calls, attributes and names;
- numeric and bool/None constants;
- comparisons, raises and returns;
- signatures and label strings.

The equation and invariance checks were done by hand. I did not read the target-free manifest; it was not needed. No network was used and no reviewed file was modified. This review was created exclusively (noclobber), and nothing was written under /Users/bgm/Research/Universal Network Theory.
