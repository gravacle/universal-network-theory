# INTERFACE 0445 V001: nonzero-mode density Fourier contraction (Claude2 contraction author)

## Pins (sha256 computed from bytes)

| File | sha256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/nonzero_density_fourier_0445/nonzero_density_fourier_c2v001.py` | `255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4` |
| Task `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0445_2026-10-16_claude2_nonzero_density_source_transform.md` (binding) | `29ebcffdf8dca98212b859e0a07f041608afe32d2ed19a9e28df9f5870720835` |
| Ref (text only) `.../recovered_packet_audit/axisymmetric_initial_rest_energy_fourier_v001.py` | `f5670726e75b6854fb8d55c2ffe6423251bb31193e5d13b087e46b8185984756` |
| Ref (text only) `.../recovered_packet_audit/posix_libm_bessel_j0_provider_v001.py` | `c7c9341660beb879da5c6e3362b67256154f2600ec33a7b8d961ed63fc538a1d` |
| Ref (text only) `.../coefficient_method/ddo_free_surface_native_feedback_root_v004.py` | `6da11133734e65fe31b6408d4f64d0e50df9f453c8872308b960678d80ec02ed` |
| Sibling provider used in the integration test only, as observed at test time (not owned here) `.../nonzero_density_fourier_0445/posix_libm_bessel_jn_provider_c2v001.py` | `9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67` |

The references were read as text. Nothing imports them, and no project data was read.

## Equation (0445, binding, verbatim)

```
deltaJ0(k) = -c^2 * 2pi * (-i)^m * sum_q [ w_q J_m(k_perp R_q) exp(-i k_z z_q)
             * ( rho_m(q) exp(+i m alpha_k) + conj(rho_m(q)) exp(-i m alpha_k) ) ]
k_perp = hypot(k_x, k_y),  alpha_k = atan2(k_y, k_x),  w_q = R dR dz WITHOUT 2pi,  m in 1..6
```

The equation uses one `(-i)^m` for both harmonics. It has no extra factor 2, no conjugated vertical exponential, no Fourier integration weights, no native inversion, no normalization, no mass adjustment, no pressure source and no acceptance step. The function returns only source coordinate 0, as a scalar complex increment in joules.

**Unit chain:** c^2 [m^2 s^-2] x w_q [m^3] x rho_m [kg m^-3] = kg m^2 s^-2 = J. The factors 2pi, (-i)^m, J_m and the exponentials are dimensionless.

**Placement for the root:** this module does not do the placement. The root embeds the result as `delta[:,0,0] = deltaJ0_J`, with the other nine coordinates set to zero. It then multiplies the cached full10 `weighted_responses` once, as `unit * delta[:,0:1,:]`. This is the v004 convention, and it adds no dk/(2pi)^3 factor.

## Signature

```python
nonzero_mode_density_fourier(*, radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3,
                             k_physical_inverse_m, c_m_s, mode, bessel_jn,
                             wave_chunk, position_chunk) -> dict
```

All arguments are keyword-only and have no defaults. The import has no side effects. The only dependencies are numpy and the stdlib modules `math` and `numbers`.

| Argument | Contract (violation returns `INVALID_INPUT`; nothing is evaluated) |
|---|---|
| `radius_m` | 1-D, real (`f` dtype at most 8 bytes, or an integer dtype), finite, length q >= 1, every value > 0 |
| `z_m` | 1-D, real, finite, length q, any sign |
| `weights_RdRdz_m3` | 1-D, real, finite, length q, every value > 0. These are R dR dz weights **without 2pi**; the caller is responsible for that. |
| `rho_mode_kg_m3` | complex64 or complex128 dtype, shape (q,), finite. Signed, with no positivity check. A real-valued harmonic must be passed with a complex dtype. |
| `k_physical_inverse_m` | shape (nk, 3), nk >= 1, real, finite. Signed and in any order; the output keeps the input order. |
| `c_m_s` | real number (bool rejected), finite, > 0, and c*c finite and > 0 |
| `mode` | Python `int` in 1..6. `bool`, numpy integers and floats are rejected. |
| `bessel_jn` | callable `(n, x)`. Each call gets `n = mode` and a read-only float64 array x of shape (kw, pq) with x >= 0. It must return a float64 array of the same shape with finite values, abs(J) <= 1, and **exactly 0.0 wherever x == 0.0**. Any violation gives `FAILED_CLOSED` at stage `bessel_provider`. |
| `wave_chunk`, `position_chunk` | Python `int` >= 1 (bool rejected), supplied by the caller and never chosen silently |

## Return dict (fail-closed)

| Key | Meaning |
|---|---|
| `status` | `COMPLETE`, `INVALID_INPUT`, `FAILED_CLOSED`, or `INTERRUPTED` (the last only on an attached exception, see below) |
| `complete` | True only for `COMPLETE` |
| `deltaJ0_J` | complex128 array (nk,) in J, in input wave order. Set only for `COMPLETE`, otherwise None. |
| `units` | `'J'` |
| `retained_deltaJ0_J`, `retained_wave_mask` | On failure: rows from every committed wave chunk, other rows NaN+NaNj, plus a bool mask. The mask is all True on `COMPLETE`. |
| `completed_wave_chunks` | tuple of `(start, stop)` pairs in commit order |
| `reason`, `failure_stage`, `exception_type` | Set on failure. The stage is one of: validation, wave_geometry, bessel_argument, bessel_provider, vertical_phase, azimuthal_bracket, position_sum, prefactor, commit. |
| `counts` | waves, positions, mode, wave_chunks_total, wave_chunks_completed, position_chunks_per_wave_chunk, waves_completed, blocks_evaluated, provider_calls, provider_elements, k_perp_zero_waves (committed chunks only), zero_argument_elements, realized_max_block_elements |
| `chunking` | wave_chunk, position_chunk, block_element_bound = wave_chunk*position_chunk, realized_max_block_elements, order |
| `convention` | Strings for the equation, unit chain, accumulation order, alpha rule at k_perp = 0, source_coordinate = 0, weights, Fourier sign and exclusions |

**Interruption.** An `Exception`, including a `FloatingPointError` raised under the caller's `np.errstate`, returns `FAILED_CLOSED` with the completed chunks retained. A `KeyboardInterrupt`, `SystemExit` or other non-`Exception` is **re-raised**. Before that, the same retained dict, with status `INTERRUPTED`, is attached to it as `exc.unt0445_retained_result`.

A wave chunk is committed only after all of its position blocks finish: the values are written first, then the mask, then the chunk list. The module does no I/O. Persisting across a process kill is the caller's job, for example by calling on wave slices. Each wave is independent and the output order is preserved.

## Equation to line map (installed file)

| Equation element | Line(s) |
|---|---|
| (-i)^m as an exact unit table (no complex power) | 54 (table), 192 |
| -c^2 * 2pi (c*c computed and validated as finite in `_validate`) | 193 |
| conj(rho_m(q)) | 191 |
| wave chunk loop (ascending) | 230 |
| k_perp = hypot(k_x, k_y) | 236 |
| alpha_k = atan2(k_y, k_x) | 237 |
| exp(+i m alpha_k) | 240 |
| exp(-i m alpha_k) = conj of line 240 (exact conjugate, so the bracket is exactly real) | 241 |
| position block loop (ascending) | 244 |
| k_perp R_q argument | 247 (read-only at 250) |
| J_m(k_perp R_q), provider checks | 257; checks at 133 (float64), 137 (abs(J) <= 1), 139 (J_m(0) == 0) |
| k_z z_q and exp(-i k_z z_q) | 260, 263 |
| rho_m exp(+i m alpha) + conj(rho_m) exp(-i m alpha) | 265-266 |
| sum_q w_q J_m exp(...) [bracket] | 268 (`einsum('q,kq,kq,kq->k', ..., optimize=False)`) |
| per-wave accumulation over position blocks | 243 (start at zero), 272 |
| -c^2 * 2pi * (-i)^m * sum | 275 |
| k_perp = 0 result checked to be exactly zero | 278 |
| commit (retention) | 281-283 |
| fail-closed handlers | 286, 288 |

**Alpha at k_perp = 0.** `numpy.arctan2` is used everywhere. At signed zeros it gives a finite value (0, -0, pi or -pi). Nothing is divided by k_perp. The J_m(0) = 0 factor, which the provider must return exactly, makes every term zero. Line 278 then checks that the output is exactly 0. k_perp = 0 happens only when k_x and k_y are both ±0.

## Batching bound and accumulation order

**Bound.** No (wave, position) array exceeds `min(wave_chunk, nk) * min(position_chunk, q) <= wave_chunk * position_chunk` elements. Per block the module creates the argument, its zero mask, J, the phase, the vertical exponential, the two bracket products and the bracket. Peak memory is roughly 100 bytes per block element, plus the provider's own transients. Only per-wave (nk,) and per-position (q,) vectors exist outside a block.

**Order.** For each wave, a complex128 accumulator starts at 0. Position blocks are added with in-place `+=` in ascending order. Inside a block, the reduction over q uses the internal uncompensated sum-of-products order of `numpy.einsum(optimize=False)`; operands are multiplied in the order w, J_m, vertical, bracket. After the last block the sum is multiplied by `(-i)^m`, which is exact, and then by the real scale `-(c*c)*(2*pi)`. There is no `math.fsum`, no pairwise `np.sum` and no BLAS.

Results for different `position_chunk` values agree only to rounding. On the fixtures, changing `wave_chunk` while holding `position_chunk` fixed gave bitwise-identical output. That was observed, not guaranteed.

## Lane compliance

- numpy and stdlib only.
- No `@`, `dot`, `matmul`, `vdot`, `inner`, `tensordot` or `linalg`. The only contraction is `np.einsum(optimize=False)`.
- No `errstate`, `seterr` or `warnings`. The caller's floating-point state governs.
- No I/O, no ctypes, no scipy.
- Nothing runs at import except definitions.
- Input arrays are copied to float64/complex128 at validation, so the caller can change its arrays without affecting a call in progress.

## Fixtures and results

Interpreter: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (Python 3.12.14, NumPy 2.3.5), with `VECLIB_MAXIMUM_THREADS=OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=1`.

The test scripts are in scratch:

- `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0445/contraction_author/test_contraction_c2v001.py`, sha256 `4081b8fcaa7e6567ef149b0c5344b06363e0e9b56d0857f68a9beeff675f04b2`
- `.../test_integration_sibling_provider.py`, sha256 `818b3dd9f676b8942f8ed8a32417a88611873070f0a2dee21881d54546638068`

Both ran against the installed bytes. **Result: 70 of 70 checks pass, and the integration test passes.**

**Reference J_n, test-only.** The reference is a periodic 512-node trapezoid of (1/2pi) ∫ cos(n t - x sin t) dt.

- Against literature values: max error 1.7e-15.
- Against libm `jn` for n = 1..6 and x in [0, 30]: max error 2.4e-16.

| Fixture | Result |
|---|---|
| Direct-angle check, m = 1..6: brute-force azimuthal trapezoid with 2048 nodes, with no Bessel function and no (-i)^m. Uses q = 4, 9 signed k including k_perp = 0, and mixed rho phases. | max relative error 1.4e-15 |
| Phases: m in {1, 4, 6}, theta in {0, pi/2, -2.2, pi} | relative error vs the closed form -c²2π(-i)^m w J_m e^{-ik_z z}·2|ρ|cos(mα+θ) is at most 1.8e-16; vs direct angle at most 1.2e-13 (limited by the reference) |
| Reality: deltaJ0(-k) = conj(deltaJ0(k)), m = 1..6, scrambled signed order | relative error below 1e-14; a permuted wave order with wave_chunk = 1 gives bitwise-permuted output |
| k_perp = 0: (±0, ±0, k_z), including k = 0, all m | exactly 0. A provider that substitutes J0 gives `FAILED_CLOSED` at `bessel_provider` and keeps the earlier chunk. |
| Batch consistency: 8 (wave_chunk, position_chunk) pairs, from (1,1) to (100,100) | max relative error 2.4e-16. Every provider block was at most wave_chunk x position_chunk, and the provider call count equals ceil(nk/wc)·ceil(q/pc). |
| Units: a point with w = 1 m³, ρ = 1 kg/m³, c = 299792458 | equals -c²2π(-i)^m J_m(x)·2 exactly (relative error 0) |
| Scaling | c x 1024 scales the output by exactly 1024²; ρ x 8 scales it by exactly 8 |
| Physical scale: kpc radii, ρ about 1e-21 | finite, about 6.5e54 J, consistent with the scaling to 5e-16 |
| Validation: 33 malformed inputs (mode bool/0/7/np.int64/float, bad R/w/z/ρ/k/c, chunks, non-callable) | all return `INVALID_INPUT` with zero provider calls. Positional calls and missing arguments raise `TypeError`. The signature is keyword-only with no defaults. |
| Provider faults (raise, wrong shape, complex, float32, NaN, abs(J) > 1) on call 6 | `FAILED_CLOSED`. Chunks (0,2) and (2,4) are retained and bitwise equal to the full run; the other rows are NaN. |
| KeyboardInterrupt from the provider | re-raised, with an `INTERRUPTED` dict attached that retains chunk (0,2) |
| `np.errstate(all='raise')` with k_perp R overflowing | `FloatingPointError` gives `FAILED_CLOSED` and keeps the first chunk |
| Same overflow under `errstate(all='warn')` | the RuntimeWarning is not suppressed and the non-finite check fails closed |
| Normal fixtures under `errstate(all='raise')` | complete |
| Sibling libm `jn` provider injected (`create_jn_provider`), m = 1..6, k_perp = 0 included | `COMPLETE`. Max relative error vs direct angle 1.4e-15, and k_perp = 0 output is exactly 0. |
| Static lane check (tokenized code, strings and comments excluded) | no banned tokens; the only einsum is `optimize=False`; module globals are definitions only |

## Not done here

This module does not provide a native inversion, normalization, mass adjustment, pressure source, target access, scientific run, provider, or physics acceptance. The root owns launches and acceptance.
