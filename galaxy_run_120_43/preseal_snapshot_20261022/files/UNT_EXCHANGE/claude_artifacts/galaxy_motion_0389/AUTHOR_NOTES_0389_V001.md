# 0389 author notes, v001

Author: Claude helper (AUTHOR role). A different helper does the static review.

Artifact: `common_metric_circular_speed_v001.py` in this directory. It has 130 lines and uses the standard library only (`math`, `numbers`).

There is one public function, `circular_speed_rows(*, metric_rows, c_km_s)`. Both arguments are keyword-only and required, and there are no defaults.

## Sources (sha256 computed from bytes when read)

| Source | Role | sha256 |
|---|---|---|
| FROM_CODEX/0389_2026-10-15_common_metric_motion_kernel_implementation.md | task and formula authority | a35b406dd0367a1676971a7048a220d7a1c8394dfc2900403342368518b3a65e |
| CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md (live file; read L809–859 and L966–1057) | equation context | 52e8a2c683aba7bfcbc71f30608d8653bd09d4e5c5b65473c73cf3979dbffa73 |
| CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json | id FORMAT only | a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494 |

**What was read from the manifest.** Only key paths and the `rows[].query_id` strings were printed: 43 ids, `NGC3198-Q01` … `NGC3198-Q43`. No radii and no other values were printed. No case is hard-coded, and the id pattern is documented but not enforced.

## Spec-to-code mapping

| 0389 item | Code |
|---|---|
| Standard library only; module level holds only imports and defs | L6–7, plus two `def`s |
| `circular_speed_rows(*, metric_rows, c_km_s)`, required, no default constants | L23 |
| Finite real, non-bool values (`numbers.Real`, then `float`, then `isfinite`) | `_finite_real` L10–20 |
| c > 0 | L59–61 |
| Rows: a non-empty list or tuple of dicts with exactly the keys id, R_kpc, N, dlogN_dr, dlogR_dr | L62–76 |
| IDs are unique, non-empty strings | L77–82 |
| R > 0, N > 0, dlogR_dr ≠ 0 | L84–93 |
| ratio = dlogN_dr / dlogR_dr, finite | L94–99 |
| 0 ≤ ratio < 1, otherwise an informative ValueError | L100–105 |
| v_local_km_s = c_km_s·sqrt(ratio) | L109 |
| Order and ids preserved; nothing clipped, sorted, replaced or inferred | single in-order loop, append only, L68–116 |
| Per-row id, speed, ratio, R_kpc, inputs, units "km/s", semantics LOCAL_CIRCULAR_SPEED | L106–116 |
| Scope note; not TOTAL_OBSERVABLE; no gravity law, mass, halo, force, weak-field or light correction | docstring L53–57; return L117–130 |

## Manual symbolic checks

### Radial-coordinate rescaling invariance

Let r = r(r̃) be any differentiable reparametrization with dr/dr̃ ≠ 0. The scalars N and R are coordinate-independent functions on the orbit plane. By the chain rule:

- d ln N/dr̃ = (dr/dr̃)·d ln N/dr
- d ln R/dr̃ = (dr/dr̃)·d ln R/dr

The common factor dr/dr̃ cancels in the ratio, so ratio is invariant. This holds for either orientation: if dr/dr̃ < 0, both derivatives change sign and the ratio is unchanged. That is why a negative dlogR_dr is admitted.

Two further invariances follow because constants drop out of log-derivatives:
- N → kN (lapse or clock normalization) leaves the ratio unchanged.
- R → kR (radius units) leaves the ratio unchanged.

So R_kpc and the lapse normalization never enter the speed.

### Reduction to the assembly forms

- **Circumferential coordinate, r = R.** Here dlogR_dr = 1/R, so ratio = R·∂_R ln N. This is v² = c²R·∂_R ln N.
- **Isotropic chart, R = A·r.** Here dlogR_dr = 1/r + ∂_r ln A, so ratio = r·∂_r ln N / (1 + r·∂_r ln A). This is the boxed reconstructed-profile form.
- **General optical tensor, R = N·sqrt(q_φφ).** The ratio is ∂_r ln N / ∂_r ln R, which is the Direction-dependent extension form.

### Sign and zero domains

| Quantity | Domain | Reason |
|---|---|---|
| N | > 0 | Lapse must be positive for ln N to exist; N = 0 is a horizon or degenerate clock. |
| R | > 0 | ln R must exist. |
| dlogR_dr = 0 | rejected | dR/dr = 0 means r does not label the circumference locally, so the read is undefined. The assembly requires dR/dr ≠ 0. Signed zero −0.0 also compares equal to 0 and is rejected. |
| dlogR_dr < 0 | admitted | Only orientation; it cancels in the ratio. |
| ratio < 0 | rejected, never clipped to 0 | The lapse decreases outward in R, so v² < 0 and the branch has no real circular orbit. |
| ratio = 0 | admitted | v = 0. If dlogN_dr is −0.0, the result can be a signed zero −0.0, numerically 0. It is not altered. |
| 0 < ratio < 1 | admitted | Subluminal timelike circular orbit. |
| ratio ≥ 1 | rejected | v ≥ c is a null or spacelike orbit, not a massive circular orbit. |
| c_km_s | > 0 | Supplied by the caller. Its unit cannot be verified, and v carries whatever unit c_km_s has. |

### What the module does not insert

There is no mass, halo, Birth-deficit force, potential, Poisson solve, gravity law, weak-field limit (R·∂_RΦ), observer or light correction, calibration constant, file I/O or import-time work.

## Unresolved points

1. **No radial-coordinate declaration.** 0389 lists only the five fields, so the function cannot verify that both derivatives refer to the same coordinate. That remains the caller's contract.
2. **R_kpc is provenance only.** It does not enter the speed and is not cross-checked against dlogR_dr. A consistency check would be possible only if the coordinate were declared, for example dlogR_dr = 1/R in a circumferential coordinate.
3. **Branch conditions are not checked here.** Vertical balance (c²∂_z N² = Ω²∂_z h_φφ), radial and vertical orbital stability, and the validity bounds of the branch belong to the parent calculation.
4. **Errors are fail-fast.** The first invalid row raises, and no partial results are returned. Whether the higher-level provider prefers per-row failure records is root's decision; 0389 asks for an informative error.
5. **Author choices beyond the literal text.**
   - An empty metric_rows is rejected.
   - Rows must be `dict` instances with exactly the five keys, so extra keys are rejected rather than silently dropped.
   - A whitespace-only id counts as empty.
   - Inputs are reported after conversion with `float()`. This is lossless for floats, but a `Fraction` input is rounded.

## Execution statement

The module was never executed or imported, and no tests or examples were run. The only Python run on it was AST parsing:
- `ast.parse` as a syntax check, which passed;
- a walk listing module-level nodes, imports, I/O names, the signature and defaults, and numeric literals.

The walk found module level is Import, Import, FunctionDef, FunctionDef; the imports are math and numbers; there are no I/O names and no defaults; and the only numeric literals are 0 and 1.0.

The manifest was read with a `python3 -I` JSON one-liner that printed key paths and `query_id` strings only.

The files were drafted in the session scratchpad and then created exclusively in a new directory. No network was used. Nothing was written under /Users/bgm/Research/Universal Network Theory.
