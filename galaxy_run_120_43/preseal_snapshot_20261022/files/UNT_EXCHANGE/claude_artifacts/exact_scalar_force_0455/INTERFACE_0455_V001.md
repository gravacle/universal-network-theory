# INTERFACE 0455 V001: exact scalar-force evaluator (c2v001)

Module: `exact_scalar_force_c2v001.py` (same directory). Task 0455 sha256 `b467a0c0c6e2fe3498a44ebdecca110776528dde7b4304d204cd42e64c67062c`.
It is inert: importing it only defines things. numpy and stdlib only, no BLAS products (`np.einsum(..., optimize=False)`), no warning suppression. Every argument is keyword-only and none has a default. Every function returns a fail-closed dict whose `status` is `COMPLETE`, `INVALID_INPUT` (nothing evaluated) or `FAILED_CLOSED` (the `retained` key holds the partial work). On a non-Exception interrupt the retained dict is attached as `exc.unt0455_retained_result` and the exception is re-raised.

## Signatures

```
prepare_geometry(*, wavevectors, x_m, y_m, z_m, max_dense_entries, max_block_entries, column_chunk, point_chunk)
bind_base(*, n_base, grad_n_base, x_m, y_m, z_m)
exact_finite_sum(*, geometry, wavevectors, amplitudes, x_m, y_m, z_m)                      # raw complex, NO admission
admit_scalar_force(*, finite_sum, base, c_m_s, gradient_length_scale_m,
                   base_reality_atol, base_reality_rtol, increment_reality_atol, increment_reality_rtol)
exact_scalar_force(*, geometry, base, wavevectors, amplitudes, x_m, y_m, z_m, c_m_s, gradient_length_scale_m,
                   base_reality_atol, base_reality_rtol, increment_reality_atol, increment_reality_rtol)
```

- `wavevectors`: (nk, 3) real, signed, in 1/m, in the actual order.
- `amplitudes`: (nk,) complex in the same order, already `unit_lapse*deltaJ`. They are used exactly as supplied.
- `x_m`, `y_m`, `z_m`: equal-shape real arrays (any ndim of at least 1), in m.
- `n_base`: complex, with the point shape. `grad_n_base`: complex, with the point shape plus (3,), Cartesian.
- Outputs:
  - `dn_complex` and `grad_dn_complex` (Cartesian x, y, z) are always retained.
  - `Nb`, `deltaPhi_m2_s2` and `grad_deltaPhi_cartesian_m_s2`.
  - The `reality` reports.
  - The identity digests.
  - `hessian = 'NONE EVALUATED'`.

## Finite equation and grouping

The module computes `dn = SUM_j a_j exp(i k_j.x)` and `grad dn = SUM_j (i k_j) a_j exp(i k_j.x)`. Nothing else enters the sum: no weight, boundary term, factor 2, c^2, reflection, symmetry, mode removal or `.real`.

1. Waves are grouped by exact-equal (kx, ky) pairs (lexsort followed by an adjacent `!=` test) and by exact-equal kz (stable argsort). The dense stack `D[3, n_kz, n_pairs] = [S, (1j kx) S, (1j ky) S]` is built fresh on every call. S comes from `np.add.at` in the supplied order. Exact duplicate waves are summed, and a hole is an exact zero, meaning no supplied term.
2. Points are grouped into exact-equal (x, y) columns. z is free per point, so it can be nonuniform within a column.
3. For each block of `cb` columns:
   - `E = exp(1j*(kx*x + ky*y))`.
   - `C_f = einsum('cp,qp->cq', E, D[f])` for f = 0, 1, 2.
   - `Cz = C_0 * (1j kz)`.
4. Within the block, for each block of `pb` points: `V = exp(1j*(kz*z))`, then `value_f = einsum('pq,pq->p', V, C_f[column])`.

No complete Cartesian product, symmetry, binning or interpolation is assumed. Only the grouping of roundoff changes. The phase convention follows the read-only line module `owned_fixed_xy_fourier_line_v002.py` (sha256 `3a47419d…2d18`).

## Identity guards

- **Geometry record.** A read-only `MappingProxyType` holding read-only float64 copies and grouping indices, plus `wave_sha256`, `point_sha256` and `geometry_sha256`. Each digest is a sha256 over dtype, shape and bytes.
- **Every evaluation:**
  - recomputes `geometry_sha256`, so tampered arrays give `INVALID_INPUT`;
  - requires the supplied wavevectors and points, converted to float64, to be byte-identical to those prepared;
  - copies the amplitudes and records their sha256.
  S and the collapsed lines are never cached between calls.
- **Base.** `bind_base` binds n_b and grad n_b to the sha256 of the points they were evaluated on, and stores a `base_sha256`. Both the integrity check and the point-digest equality with the finite sum or geometry are required.
- **Finite-sum result.** It carries `result_sha256`. Admission rechecks it, so a mutated dn or grad gives `INVALID_INPUT`.
- Caller inputs are never mutated.

## Admission rule (code lines 581–610)

1. All four checks are evaluated and reported. Each requires the values to be finite and to satisfy `|Im v| <= atol + rtol |Re v|` elementwise:
   - `v = n_b` and `v = L*grad n_b`, with the base tolerances;
   - `v = dn` and `v = L*grad dn`, with the increment tolerances.
   Here `L` is `gradient_length_scale_m`.
2. `Nb = 1 + Re n_b > 0` at every point (`lapse_base = 1.0 + nb`, line 597).
3. `deltaPhi = c_squared * (dn / lapse_base)` (line 609) and `grad_deltaPhi = c_squared * (grad_dn / nb3 - dn[..., None] * grad_nb / (nb3 * nb3))` (line 610). These use the real parts and are identical to the 0449 LINEAR form. There is no log replacement.

## Limits (fail closed before allocation)

- `n_kz * n_pairs <= max_dense_entries`.
- With `cb = min(column_chunk, columns)` and `pb = min(point_chunk, points)`, each of `cb*n_pairs`, `4*cb*n_kz` and `pb*n_kz` must be `<= max_block_entries`.
- Peak bytes are roughly:
  - `48*n_kz*n_pairs` for the dense stack;
  - `40*cb*n_pairs` for the transverse block;
  - `64*cb*n_kz` for the collapsed block;
  - `56*pb*n_kz` for the vertical block;
  - plus O(nk + points) for indices and copies.

## Op count and memory for the actual 72^3 wave set (373,248 waves = 5,184 pairs x 72 kz)

| Item | Per call | Per column | Per point |
|---|---|---|---|
| Dense stack | 373,248 entries x 48 B = 17.9 MB, plus 2 x 373,248 complex multiplies | | |
| Transverse | | 5,184 complex exps | |
| Collapse | | 3 x 373,248 = 1,119,744 complex MAC | |
| Vertical | | | 72 exps + 288 complex MAC |
| Direct sum (comparison) | | | 373,248 exps + 1,492,992 complex MAC |

- Suggested limits: `max_dense_entries >= 373,248`, and for example `column_chunk = 16` with `max_block_entries >= 82,944` (a 1.3 MB E block).
- Synthetic timing for a randomly generated irregular signed 72x72x72 set (not actual data), single thread: prepare 0.075 s. Evaluating 64 columns x 6 z took 0.066 s (about 1.0 ms per column, including the sha256 identity checks) against about 9 ms per point for the direct sum. The traced peak was 27 MB.

## Limitations

- Agreement with the direct sum holds up to regrouping roundoff only. There is no error certificate. Phase angles are rounded as `(kx x + ky y)` and `kz z` separately, and the duplicates are summed first.
- Identity is byte identity. -0.0 and 0.0 count as different identities, but they are grouped as equal values. Any change to a point or wave requires a new geometry.
- The dense grid is O(n_kz * n_pairs). For irregular sets with few repeats it can approach nk^2 and will then be rejected by the limit.
- There is no Hessian, cylindrical projection, boundary term, solve, DFT or acceptance. The root owns the comparison with the actual m1 packet.
- `-0.0` columns and kz values use the first sorted representative. This changes only the signs of zeros.

## Data statement

No actual project data was read or used. Development and smoke checks used synthetic fixtures only, under scratch `r0455/author`.
