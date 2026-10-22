# INTERFACE 0458 V001: exact grouped density Fourier regrouping (Claude2 module author)

**Status: FROZEN API v001.** The public names, keyword sets, return keys and semantics below are frozen for `grouped_density_fourier_c2v001.py`. Any change needs a new file version (c2v002) and a new INTERFACE. The module is INERT. It changes the arithmetic order of the 0445 finite sum and nothing else. Root compares it against the saved actual 0445 output before any use.

## Pins (sha256 computed from bytes)

| File | sha256 |
|---|---|
| Module (deliverable) `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/grouped_density_fourier_0458/grouped_density_fourier_c2v001.py` | `9db7efd1ef18927c5886ab9b28d4f72cae16770cb3d3b04f574237b006a4bcbe` |
| Task 0458 `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0458_2026-10-16_claude2_exact_grouped_density_fourier.md` (binding) | `18eb2dba463378903a952fd408d1f3b8a5cff9fc9be1b580921cbab9c1e51fdf` |
| Reference 0445 contraction `.../nonzero_density_fourier_0445/nonzero_density_fourier_c2v001.py` (read; loaded by path only in the test, as a synthetic oracle) | `255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4` |
| Jn provider `.../nonzero_density_fourier_0445/posix_libm_bessel_jn_provider_c2v001.py` (used unchanged; injected by the caller) | `9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67` |
| Cache/custody pattern `.../exact_scalar_force_0455/exact_scalar_force_c2v001.py` (read as a pattern only) | `0dab62be91cfd793949ef251aa3e731b4544e7131606599784762cb4101175ea` |

All four binding inputs were re-verified from bytes after the test runs. No existing file was modified. No project matrices, results, NPZ files, raw samples or target data were read.

`CONVENTION` digest (`_convention_sha256()` of the installed module): `da0e164a979b3706f79e92dbd85d07c81083ab3ebfa036b2689d853842b2df78`. Every geometry records this digest, and evaluation rejects a geometry whose recorded digest differs.

## Law (unchanged from 0445)

```
deltaJ0(k) = -c^2 * 2pi * (-i)^m * sum_q [ w_q J_m(k_perp R_q) exp(-i k_z z_q)
             * ( rho_m(q) exp(+i m alpha_k) + conj(rho_m(q)) exp(-i m alpha_k) ) ]
k_perp = numpy.hypot(k_x, k_y),  alpha_k = numpy.arctan2(k_y, k_x)   (signed inputs, per wave)
w_q = R dR dz WITHOUT 2pi,  m in 1..6,  J = c^2 [m^2 s^-2] x w [m^3] x rho [kg m^-3]
```

The regrouping adds no factor 2 and does not conjugate the vertical exponential on the negative branch. It applies no angle symmetry, interpolation, mode dropping, Fourier weight, native inverse, normalization or acceptance step. Only source coordinate 0 is produced.

## Why the regrouping is exact (finite-sum identity)

The groups are defined as follows:

- r: positions with bitwise-equal R.
- z: waves with bitwise-equal k_z.
- p: waves with bitwise-equal computed k_perp.
- c = (z, p): a filled cell.

J_m(k_perp R_q) depends on q only through R_q, and on k only through k_perp. exp(-i k_z z_q) depends on k only through k_z. So for every wave k in cell c_k = (z_k, p_k):

```
sum_q w_q J_m(k_perp R_q) e^{-i k_z z_q} [rho_q P_k + conj(rho_q) conj(P_k)]
  = P_k       * sum_r J_m(k_perp_p R_r) * sum_{q in r} (w_q rho_q)       e^{-i k_z z_q}     = P_k T+[c_k]
  + conj(P_k) * sum_r J_m(k_perp_p R_r) * sum_{q in r} (w_q conj(rho_q)) e^{-i k_z z_q}     + conj(P_k) T-[c_k]
```

Here P_k = exp(+i m alpha_k). The minus branch uses **the same** e^{-i k_z z_q}. The R groups partition q, so every q appears exactly once.

Because the groups are bitwise-equal, each factor the regrouping uses is bit-identical to the factor 0445 computes for that (wave, position). The test checks this bitwise for E, J_m (m = 1..6) and P on every (wave, q). Only the summation order differs, so the results agree with 0445 to roundoff, not bit for bit.

## Public API (frozen)

All functions are keyword-only with no defaults. Positional calls and missing arguments raise `TypeError`. Every function returns a fail-closed dict. Nothing runs at import beyond definitions. The module uses numpy and the stdlib (`hashlib`, `math`, `numbers`, `time`, `collections.abc`, `types`). It does no file I/O.

```python
prepare_geometry(*, radius_m, z_m, weights_RdRdz_m3, k_physical_inverse_m, modes, jn_provider,
                 position_chunk, perp_chunk, cell_chunk, max_vertical_entries,
                 max_bessel_entries, max_angular_entries, max_work_entries,
                 max_block_entries) -> dict

evaluate_mode(*, geometry, radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3,
              k_physical_inverse_m, c_m_s, mode, bessel_jn, wave_chunk, position_chunk) -> dict

bind_0445_adapter(*, geometry) -> dict
    # dict['density_fourier'] is a callable with EXACTLY the 0445 keyword contract:
    density_fourier(*, radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3, k_physical_inverse_m,
                    c_m_s, mode, bessel_jn, wave_chunk, position_chunk) -> dict

scaling(*, nq, nk, n_kz_unique, n_perp_unique, n_R_unique, n_cells, n_modes, max_cells_per_kz,
        position_chunk, perp_chunk, cell_chunk) -> dict
```

The module also exports these constants: `GEOMETRY_KIND`, `PREPARE_KIND`, `RESULT_KIND`, `ADAPTER_KIND`, `INTERRUPT_ATTRIBUTE = 'unt0458_retained_result'`, `INTERRUPT_ATTRIBUTE_0445 = 'unt0445_retained_result'`, `CONVENTION` (read-only), `EQUATION_0445` (verbatim from 0445), `UNIT_CHAIN`, `ACCUMULATION_ORDER`, `ALPHA_AT_K_PERP_ZERO`, `MODULE_VERSION = 'c2v001'`, and the four pin constants.

**Root usage.**

1. `prov = create_jn_provider(...)` from the pinned provider, and require `prov['status'] == 'READY'`.
2. `prep = prepare_geometry(..., modes=(1,2,3,4,5,6), jn_provider=prov, ...)`, and require `prep['status'] == 'COMPLETE'`.
3. Either:
   - call `evaluate_mode(geometry=prep['geometry'], ..., bessel_jn=prov['bessel_jn'], ...)` once per mode, or
   - call `ad = bind_0445_adapter(geometry=prep['geometry'])` and pass `ad['density_fourier']` wherever 0449/0452 take `density_fourier`, together with the same `jn_provider` dict.

### prepare_geometry arguments

Any violation returns `INVALID_INPUT`, and no provider call is made.

| Argument | Contract |
|---|---|
| `radius_m`, `z_m`, `weights_RdRdz_m3` | 0445 rules: 1-D, real (float with itemsize <= 8, or an int dtype), finite, equal length q >= 1, R > 0, w > 0. These are the actual source positions. Any order is accepted, with any repetition of R, z or w. |
| `k_physical_inverse_m` | shape (nk, 3), nk >= 1, real, finite, signed, any order, duplicates allowed |
| `modes` | tuple or list of distinct Python `int` in 1..6, nonempty. bool, numpy ints and floats are rejected. Stored sorted. Root uses (1,2,3,4,5,6). |
| `jn_provider` | READY gate: a Mapping with `status == 'READY'`, a callable `bessel_jn` and a Mapping `metadata`. Use the unchanged 0445 provider dict. Its callable is called as `bessel_jn(m, x)` with a read-only float64 x of shape (block, n_R_unique), x >= 0. 0445 checks apply verbatim: float64, same shape, finite, abs(J) <= 1, and **exactly 0.0 wherever x == 0.0**. Any violation gives `FAILED_CLOSED` at `bessel_provider`. |
| `position_chunk` | positive int: slots per vertical-phase build block |
| `perp_chunk` | positive int: k_perp groups per provider call |
| `cell_chunk` | positive int: filled cells per J-row gather during evaluation (bound into the geometry) |
| `max_vertical_entries`, `max_bessel_entries`, `max_angular_entries`, `max_work_entries`, `max_block_entries` | positive int element counts. Each is checked **before** the corresponding allocation; see Scaling. Exceeding any of them gives `FAILED_CLOSED` at `cache_limit`, with no cache allocated and no provider call. |

### prepare_geometry result

| Key | Meaning |
|---|---|
| `kind` | `PREPARE_KIND` |
| `status` | `COMPLETE`, `INVALID_INPUT` or `FAILED_CLOSED`. `INTERRUPTED` appears only on the attached record. |
| `complete` | True only for `COMPLETE` |
| `geometry`, `geometry_sha256` | the read-only record and its digest on `COMPLETE`, otherwise None |
| `reason`, `exception_type` | set on failure |
| `failure_stage` | one of: `validation`, `wave_geometry`, `grouping`, `cache_limit`, `angular_phase`, `vertical_phase`, `bessel_argument`, `bessel_provider`, `record` |
| `failure_block` | the block in progress at failure: slots, or mode plus perp_groups |
| `counts` | nk, nq, n_modes, n_kz_unique, n_perp_unique, n_R_unique, n_cells, dense_cells = n_kz*n_perp, max_cells_per_kz, max_positions_per_R, k_perp_zero_waves, distinct_wave_rows, provider_calls, provider_elements, zero_argument_elements, vertical_blocks, realized_max_block_entries |
| `scaling` | exact entries, bytes and operations; see Scaling. It is filled in before any cache allocation. |
| `limits` | the chunk and limit controls as supplied |
| `identity` | wave_sha256, radius_sha256, z_sha256, weight_sha256, provider_provenance_sha256 |
| `timing` | seconds for validation, grouping, angular, vertical, bessel, digest and total |
| `retained` | on failure only: vertical_phase and vertical_slot_mask, bessel and bessel_row_mask (n_modes x n_perp), and angular_plus. Each is partial or None. |
| `convention` | `CONVENTION` |

A non-`Exception` interruption (KeyboardInterrupt, SystemExit) is **re-raised**. Before that, the same dict with `status 'INTERRUPTED'` and the partial retained arrays is attached as `exc.unt0458_retained_result`.

**Geometry record.** It is a `MappingProxyType`, every array in it is read-only and C-contiguous, and it binds the identity of the actual inputs. Its keys are:

- `kind`, `module_version`, `task_sha256`, `convention_sha256`, `modes`
- `provider_bessel_jn` (a strong reference), `provider_provenance` (a static metadata snapshot that excludes the counters, plus the callable's qualname and module), `provider_provenance_sha256`
- `wave_sha256`, `radius_sha256`, `z_sha256`, `weight_sha256`
- arrays: `kz_unique`, `kperp_unique`, `R_unique`, `wave_kz_index`, `wave_perp_index`, `wave_cell_index`, `cell_kz_index`, `cell_perp_index`, `kz_cell_offsets`, `position_r_index`, `position_order`, `r_offsets`, `weights_sorted`, `k_perp`, `alpha`, `perp_zero`, `angular_plus` (n_modes, nk) c128, `vertical_phase` (nq, n_kz) c128, `bessel` (n_modes, n_perp, n_R) f64
- `counts`, `controls`, `geometry_sha256`

### evaluate_mode arguments

The function takes the 0445 keywords plus `geometry`. Any violation gives `INVALID_INPUT`, and nothing is evaluated.

| Argument | Contract |
|---|---|
| `geometry` | a `prepare_geometry(...)['geometry']` record. All of the following must hold: the kind is right; the recorded convention digest equals the module's; the recomputed geometry digest (all arrays, counts, controls, modes and identities) equals the recorded one; the provenance digest matches the stored snapshot. |
| `radius_m`, `z_m`, `weights_RdRdz_m3`, `k_physical_inverse_m` | 0445 validation rules, and also **sha256-identical** to the prepared inputs: the float64 validated copy (dtype, shape, bytes, signed order). |
| `rho_mode_kg_m3` | complex64 or complex128, shape (q,), finite. Complex data is kept as complex throughout. The function is real-linear in rho, not complex-linear. |
| `c_m_s` | real (bool rejected), finite, > 0, with c*c finite and > 0 |
| `mode` | Python `int` in 1..6 that is **bound in the geometry** |
| `bessel_jn` | callable, and **the same object** (`is`) bound at preparation. It is not called, because J_m is cached. |
| `wave_chunk` | positive int: waves gathered and committed per block (retention granularity). min(wave_chunk, nk) <= max_block_entries, otherwise `FAILED_CLOSED` at `block_limit` before any allocation. |
| `position_chunk` | positive int: a scatter retention batch closes after it reaches >= position_chunk positions. It always contains whole R groups and at least one group. It never changes the arithmetic or the memory. |

### evaluate_mode / adapter result

The result is a superset of the 0445 result keys. The test confirms this for both `COMPLETE` and `INVALID_INPUT`.

| Key | Meaning |
|---|---|
| `status`, `complete` | `COMPLETE`, `INVALID_INPUT` or `FAILED_CLOSED`. `INTERRUPTED` appears only on the attached record. `complete` is True only for `COMPLETE`. |
| `deltaJ0_J` | complex128 (nk,) in J, in input wave order. Read-only, set only on `COMPLETE`, otherwise None. Duplicate wave rows give identical values in place. |
| `units` | `'J'` |
| `retained_deltaJ0_J`, `retained_wave_mask`, `completed_wave_chunks` | as in 0445. On failure: the committed wave chunks, other rows NaN+NaNj. The mask is all True on `COMPLETE`. |
| `reason`, `exception_type`, `failure_block` | set on failure |
| `failure_stage` | one of: `validation`, `block_limit`, `source_weighting`, `scatter`, `cell_sum`, `gather`, `prefactor`, `commit` |
| `counts` | waves, positions and mode (the keys 0449/0452 read); wave_chunks_total, wave_chunks_completed, waves_completed; provider_calls = provider_elements = 0 (the provider is not called during evaluation); n_kz_unique, n_perp_unique, n_R_unique, n_cells; scatter_batches, r_groups_scattered, positions_scattered, cell_blocks, cells_summed; k_perp_zero_waves (committed chunks only) |
| `chunking` | wave_chunk, position_chunk, cell_chunk, order |
| `convention` | dict(`CONVENTION`), with the 0445 keys equation, unit_chain, accumulation_order, alpha_at_k_perp_zero, source_coordinate, weights, fourier_sign and excluded, plus 0458 keys |
| `kind` | `RESULT_KIND` |
| `provenance` | geometry_sha256, convention_sha256, wave/radius/z/weight sha256, provider_provenance_sha256, rho_sha256 (complex128 copy), mode, modes_bound, c_squared, result_sha256 (on `COMPLETE`) |
| `timing` | seconds for validation (including the full geometry digest), source_weighting, scatter, cell_sum, gather and total |
| `retained_work` | on failure: source_weighted (nq, 2), scatter_V (n_R, 2, n_kz) with r_group_mask, cell_T (2, n_cells) with cell_mask |

**Interruption.** `evaluate_mode` re-raises a non-`Exception` interruption after attaching the `INTERRUPTED` dict as `exc.unt0458_retained_result`. The adapter also attaches **the same object** as `exc.unt0445_retained_result`, because the 0452 handler reads that name.

**0445 keys not reproduced.**

- `counts`: position_chunks_per_wave_chunk, blocks_evaluated, zero_argument_elements and realized_max_block_elements are absent. Their 0445 meanings do not apply. The grouped zero-argument and provider counts are in the prepare result.
- `chunking`: block_element_bound and realized_max_block_elements are absent.

0449 and 0452 read none of these keys.

### bind_0445_adapter result

The result is `dict(kind=ADAPTER_KIND, status 'READY'|'INVALID_INPUT', density_fourier, geometry_sha256, reason, exception_type)`.

- The geometry is checked at bind time.
- The geometry is checked again on every call, because the adapter delegates to `evaluate_mode`.
- The callable carries the attribute `unt0458_geometry_sha256`.
- With the adapter, 0449/0452 keep passing their unchanged keywords. The caller has to bind a geometry prepared from exactly the radius, z, weights, waves and provider that 0449/0452 will pass.

### scaling

`scaling(...)` returns `dict(status 'COMPLETE', complete, entries, bytes, operations)` with the formulas below. It returns `INVALID_INPUT` when any argument is not a positive Python int. `prepare_geometry` uses the same function, so the counts it reports and checks are the ones listed here.

## Grouping algorithm (exact, installed)

1. Compute `k_perp = np.hypot(kx, ky)` and `alpha = np.arctan2(ky, kx)` on the signed float64 copy, for each wave. A nonfinite value fails closed at `wave_geometry`. Set `perp_zero = k_perp == 0.0`.
2. Group exactly with `_group_exact`:
   - Use the float64 bits (a uint64 view) with `np.unique(return_inverse=True)`.
   - Order the groups numerically. When both +0.0 and -0.0 occur, +0.0 comes first.
   - Members of a group have identical bits. The test confirms that k_z +0.0 and -0.0 form two groups.
   - This is applied to k_z (wave_kz_index, kz_unique), k_perp (wave_perp_index, kperp_unique) and R (position_r_index, R_unique).
3. Form cells:
   - key = kz_index * n_perp + perp_index (int64).
   - `np.unique(return_inverse)` gives cell_kz_index and cell_perp_index (sorted by k_z, then k_perp) and wave_cell_index.
   - kz_cell_offsets = `searchsorted`. Only filled cells exist, so holes cost nothing.
4. Order positions:
   - position_order = `argsort(position_r_index, kind='stable')`. Slot s holds q = position_order[s], ascending q inside each R group.
   - r_offsets = [0, cumsum(group sizes)].
   - Invariants are checked: the groups partition 0..q-1, every group is nonempty, every k_z group has at least one cell, and position_order is a permutation. A violation fails closed at `grouping`.
5. Check all entry limits (`cache_limit`).
6. Build the caches:
   - angular_plus[mode] = `np.exp(1j*(float(m)*alpha))`.
   - vertical_phase[s, z] = `np.exp(-1j*(kz_unique[z]*z_q))`, built in slot blocks with an explicit finiteness check.
   - bessel[mode, p, r] = provider(m, `kperp_unique[p]*R_unique[r]`), built in perp blocks with the 0445 provider checks.
7. Freeze the record: make every array read-only, then take the sha256 digest of the header (kind, version, task, convention, identities, modes, counts, controls) followed by every array's (dtype, shape, bytes).

**Evaluation of one mode.** The mode slot is the index of m in the digest-bound `modes`.

1. Weight the source in slot order: A[:,0] = w*rho and A[:,1] = w*conj(rho).
2. For each R group g, compute `V[g] = np.einsum('sb,sz->bz', A[s0:s1], E[s0:s1], optimize=False)`. This is batched for retention, with a finiteness check per batch. Then check that positions_scattered == nq and that every group is masked.
3. For each k_z group z and each cell block, compute `T[:, c0:c1] = np.einsum('rb,cr->bc', V[:, :, z], J[slot][cell_perp[c0:c1]], optimize=False)`. Check finiteness, then check that every cell was summed exactly once.
4. For each wave chunk:
   - acc = T[0, cell] * P + T[1, cell] * conj(P)
   - values = (-(c*c)*(2*pi)) * ((-i)^m * acc), the 0445 prefactor arithmetic and order, applied once
   - check finiteness
   - check that `values[perp_zero] == 0.0` exactly
   - commit

## Caching and identity guards

- **Cached (source independent):** E, J_m for the bound modes, exp(i m alpha), group maps, weights in slot order, k_perp, alpha and perp_zero.
- **Never cached:** rho, A, V, T and outputs. They are rebuilt on every call, so an A/B/A refresh reproduces A bitwise.
- **Rejected as `INVALID_INPUT`:**
  - waves, radius, z or weights that are not sha256-identical (including reordered waves)
  - a mode not bound in the geometry
  - a different `bessel_jn` object, such as a second `create_jn_provider` instance
  - a changed cached array, detected even when restored to writeable and modified, by the digest
  - changed counts, modes or provenance in a forged dict copy
  - a different convention digest or kind
  - a missing provider
- `MappingProxyType` blocks item assignment.
- The guards are custody checks, not cryptographic authentication. A deliberately forged record with a recomputed digest is out of scope.

## Scaling (exact element counts)

Notation:

- nz = n_kz_unique, np_ = n_perp_unique, nr = n_R_unique
- nc = n_cells, the filled (k_z, k_perp) cells, with nc <= min(nk, nz*np_)
- nm = n_modes
- pc, pp, cc = position_chunk, perp_chunk, cell_chunk (prepare)
- mc = max_cells_per_kz

| Item | Elements | dtype / bytes | Limit |
|---|---|---|---|
| E vertical cache | nz*nq | c128, 16*nz*nq | max_vertical_entries |
| J Bessel cache | nm*np_*nr | f64, 8*nm*np_*nr | max_bessel_entries |
| angular cache | nm*nk | c128, 16*nm*nk | max_angular_entries |
| work per evaluation: rho copy, rho in slot order, A, V, T, output | 4*nq + 2*nr*nz + 2*nc + nk | c128, 16x | max_work_entries |
| prepare phase block | min(pc,nq)*nz | f64 phase plus a c128 temporary, 24 B per element | max_block_entries |
| provider block | min(pp,np_)*nr | 17 B per element, plus the provider's internal unique/sort | max_block_entries |
| J-row gather block | min(cc,mc)*nr | f64 | max_block_entries |
| evaluation wave block | min(wave_chunk,nk) | O(1) arrays of that length | max_block_entries |
| group maps and vectors (not limited, O(nk+nq), allocated before the limit check) | - | 8*(3nk + 2nc + (nz+1) + 3nq + (nr+1)) + 8*(nz+np_+nr) + 16nk + nk | - |
| validation copies per call (as in 0445) | - | 8*(3nq + 3nk) | - |
| geometry digest bytes (hashed on every evaluation) | - | 16nz*nq + 8nm*np_*nr + 16nm*nk + maps | - |

**Operations.**

Prepare:

- nk hypot and nk arctan2
- nz*nq real products and nz*nq complex exp
- nm*np_*nr argument products and the same number of provider elements, in nm*ceil(np_/pp) provider calls; libm runs once per unique argument per call
- nm*nk complex exp

Evaluation, per mode:

- 2nq real-by-complex products
- **scatter: 2*nq*nz complex MAC** in nr einsum calls
- **cell sum: 2*nc*nr complex-by-real MAC** in at most nz + nc//cc einsum calls, plus nc*nr float gather copies
- 2nk complex products, nk adds and 2nk prefactor products
- sha256 over the geometry digest bytes plus 8*(3nq + 3nk) input bytes

The equivalent direct 0445 sum is nk*nq terms, each with a provider element and complex exps.

**At root's known sizes only (nq = 373248, nk = 2304, nm = 6), with no other dimension guessed:**

- E = 5.97 MB per unique k_z.
- J = 48*np_*nr bytes.
- angular = 221,184 B.
- work = 16*(1,495,296 + 2*nr*nz + 2*nc) B, which is about 23.9 MB plus the V/T terms.
- scatter = 746,496*nz complex MAC per mode.
- The direct 0445 sum is 859,963,392 terms per mode.

Root reads n_kz_unique, n_perp_unique, n_R_unique and n_cells from `prepare_geometry(...)['counts']`. A run with deliberately small limits returns them with `FAILED_CLOSED` at `cache_limit` after only the O(nk+nq) grouping work.

## Differences from 0445 behaviour (explicit)

1. **Summation order.** Results agree with 0445 to roundoff only. They are not bitwise equal: 46 of 156 fixture-A outputs were bitwise equal, and 30 of those are exact zeros. Within 0458, the output was observed to be bitwise independent of wave_chunk, position_chunk, perp_chunk and cell_chunk. That was observed, not guaranteed.
2. **Geometry-level faults fail at prepare.** These are a nonfinite k_perp or alpha, k_perp*R, k_z*z, or a provider fault. 0445 would have committed the earlier wave chunks, while 0458 builds no geometry.
3. **Identity and stale-geometry rejections are new `INVALID_INPUT` causes.** `bessel_jn` is identity-checked and not called during evaluation.
4. **wave_chunk and position_chunk** keep the 0445 validation, but they control retention granularity only. The per-block memory bound is governed by the prepare limits instead.
5. **Floating-point flags.**
   - Ufunc stages honor the caller's `np.errstate`. Examples are hypot, the products, exp, w*rho, the gather and the prefactor.
   - `np.einsum` raises no floating-point flags; this was observed in NumPy 2.3.5, where an overflow gives inf and no FloatingPointError under `errstate(all='raise')`.
   - Every stage therefore checks finiteness explicitly, so an overflow always fails closed.
   - Underflow inside einsum is silent, as it is inside 0445's einsum. The set of operations that can raise a FloatingPointError differs from 0445.
6. **Interrupt attribute.** It is `unt0458_retained_result`. The adapter adds the `unt0445_retained_result` alias.

## Author smoke evidence (synthetic only; installed bytes)

Interpreter: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (Python 3.12.14, NumPy 2.3.5), run with `VECLIB_MAXIMUM_THREADS=OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`. The pinned 0445 module and provider were loaded by path after sha256 verification and run only on synthetic inputs. The provider resolved `/usr/lib/libm.dylib` and the symbol image `/usr/lib/system/libsystem_m.dylib`.

| Item | Path | sha256 |
|---|---|---|
| Test | `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0458/author/smoke_0458_author.py` | `9cc72143d9c33119d510f172c79f6ee1d4a3b4bcea5e041a10ae4a91db604fbb` |
| Output | `.../r0458/author/run_final.txt` | `e41a723fe1ea3d064c74260455b4406c4f9c1a8dfe207447087c1c869cc497cd` |
| Indicative timing | `.../r0458/author/bench_moderate.py` | `b89d023ac5255444df45fbc0fdca22f84f26932aa9a6a4fd555b18c4077155d2` |
| Timing output | `.../bench_final.txt` | `724d0b8ed26d2f6893c1f6cda08fed7e9aa45c0ac64e715797fcd1c845c2ee17` |

**Result: 175 of 175 checks pass (STATUS PASS, 0.93 s).**

**Fixture A** (q = 41 and nk = 26):

- Positions:
  - Irregular R from 7 values with repeats and an unsorted order.
  - z repeated inside and across R groups, and continuous.
  - Irregular weights, including two equal ones.
  - One rho exactly 0.
- Waves:
  - Signed, permuted and holey.
  - An exact duplicate row, and 4 waves with k_perp = 5 at different alpha.
  - 5 waves with k_perp = 0 (±0 combinations, including k = 0).
  - k_z = +0.0 and -0.0, and 6 ±k pairs.
- Group counts: nz = 9, np_ = 8, nr = 7, nc = 16 (dense 72).

| Check (m = 1..6 unless stated) | Result |
|---|---|
| Cached E, J_m and exp(i m alpha) compared with 0445's per-term factors for every (wave, q) | bitwise equal |
| vs independent pure-Python `math.fsum` direct sum (relative to the per-wave bound c²2π Σ w·abs(J)·2·abs(ρ)) | max 1.06e-16 |
| vs direct-angle 256-node trapezoid (no Bessel function, no (-i)^m) | max 7.1e-17 |
| vs pinned 0445 | max 1.11e-16 |
| k_perp = 0 outputs | exactly 0 |
| duplicates | identical outputs in place |
| reality deltaJ(-k) = conj(deltaJ(k)) over 17 pairs | at most 2.2e-15 relative |
| Negative branch uses the same E | A variant with conjugated E on the minus branch differs by 0.13–0.54 of the bound, while 0458 matches the correct direct sum to 1e-16 |
| Phase rotation, closed form -c²2π(-i)^m w J e^{-ik_z z}·2·abs(ρ)·cos(mα+θ), m in {1,4,6}, θ in {0, π/2, -2.2, π} | 1.6e-15 |
| Real-linearity f(aρ1+bρ2) = a f(ρ1) + b f(ρ2) | 6e-17 |
| Not complex-linear: f(iρ) vs i f(ρ) | differ by 1.3–1.5 relative; f(iρ) matches the direct sum |
| zero ρ | exactly 0 |
| Source refresh A/B/A | A bitwise repeatable, B differs, geometry digest unchanged, result and ρ digests recorded |

**Fixture B** (q = 1500 with 55 R values; nk = 260 random waves with 12 k_z values and 7 k_perp = 0 waves): against the pinned 0445 for m = 1..6, the maximum is 7.2e-17 relative to the bound.

| Contract check | Result |
|---|---|
| Stale identity: one wave nudged by 1 ulp, reversed wave order, R, z or w nudged by 1 ulp, unbound mode, second provider instance | each gives `INVALID_INPUT` |
| Tampered E element after `writeable=True` | `INVALID_INPUT` (digest), and the adapter bind is refused. A restored value is accepted. |
| Forged dict copy with a changed convention, kind, counts, modes, provenance or a missing provider | `INVALID_INPUT` |
| Cache write and mapping assignment | blocked |
| 12 malformed evaluate inputs and 20 malformed prepare inputs | `INVALID_INPUT` with zero provider calls |
| Positional call | `TypeError` |
| Limits | Each of the five limits exceeded by 1 gives `FAILED_CLOSED` at `cache_limit` with no provider call and no cache. A limit exactly equal is accepted. A wave block over the limit gives `FAILED_CLOSED` at `block_limit`. |
| `scaling` | entries equal the realized cache sizes; digest bytes equal the realized total (13,730 B); the public `scaling()` matches |
| Provider faults (raise, NaN, float32, wrong shape, abs(J) > 1) on call 3 | `FAILED_CLOSED` at `bessel_provider` with the 4 earlier rows retained |
| J0-substituting provider | `FAILED_CLOSED` at the mode-2 k_perp = 0 block, with all mode-1 rows retained |
| KeyboardInterrupt in the provider | re-raised, with `unt0458_retained_result` keeping 6 rows |
| `errstate(all='raise')` with k_perp·R overflowing | `FloatingPointError` gives `FAILED_CLOSED` at `bessel_argument` |
| Same under `errstate(all='warn')` | the RuntimeWarning is emitted, not suppressed, and the nonfinite check fails closed |
| hypot overflow | `FAILED_CLOSED` at `wave_geometry` |
| k_z·z overflow | `FAILED_CLOSED` at `vertical_phase` |
| Scatter overflow | `FAILED_CLOSED` at `scatter`, keeping the finite first R group |
| Prefactor overflow | `FAILED_CLOSED` at `prefactor`, keeping two committed k_perp = 0 chunks |
| Normal fixture under `errstate(all='raise')` | `COMPLETE`, bitwise equal |
| KeyboardInterrupt and SystemExit inside the 4th einsum, through the adapter | re-raised; `unt0458_retained_result is unt0445_retained_result`, `INTERRUPTED` at `scatter`, 3 R groups retained |
| Adapter signature | equals the 0445 signature: same names, keyword-only, no defaults |
| `evaluate_mode` signature | `geometry` plus the 0445 keywords |
| Adapter result keys | superset of 0445's for both `COMPLETE` and `INVALID_INPUT`; bitwise equal to `evaluate_mode` |
| 0449/0452 Step-1 consumer gate (restated) | accepts m = 1..6 |
| Read-only waves and complex64 ρ | accepted |
| Inputs | unmutated: bytes and writeable flags |
| Static check (tokenized) | no `@`, dot, matmul, vdot, inner, tensordot, linalg, errstate, seterr, warnings, open, ctypes or scipy; exactly 2 einsum calls, both `optimize=False`; imports are stdlib and numpy only; module globals are definitions only |

**Indicative timing.** These are synthetic numbers, not a performance promise. q = 24,000, nk = 775, nz = 12, np_ = 45, nr = 120, nc = 416.

- prepare: 0.02 s.
- evaluate per mode: about 0.004 s, of which the validation and digest take 0.002 s.
- pinned 0445 on the same input: about 1.24 s per mode.
- maximum difference vs 0445: 5.8e-17 relative to the bound.
- sha256 on this host: about 2.6–2.8 GB/s.

Root-scale cost was not measured. It depends on the real nz, np_, nr and nc.

## Limitations

- **UNTESTED at root scale and on root geometry.** The deciding test is root's comparison against the saved actual 0445 output. For that comparison, use a roundoff tolerance relative to the per-wave bound c²2π Σ_q w_q·abs(J_m)·2·abs(ρ_q), not a bitwise or plain relative test, because outputs near cancellation can be tiny.
- E is stored densely as nq x n_kz_unique. Many distinct k_z values make it large, which is why `max_vertical_entries` exists.
- Grouping is bitwise, with no tolerance merging. Values that differ by 1 ulp, or ±0 in k_z, form separate groups. This is correct but groups less.
- Two loops run in Python: nr einsum calls for the scatter, and per-k_z cell blocks. With all R distinct this means nq calls.
- Every evaluation hashes the full cache (about 0.36 s per GB at the measured rate).
- Provider binding is object identity plus a static metadata snapshot. The module does no I/O and cannot verify provider file bytes, so root must load the pinned provider (sha 9ec3f1c9…).
- The digests are custody checks, not authentication.
- The O(nk+nq) grouping arrays are allocated before the limit check.
- `retained_work` keeps A (2nq complex) on failure.
- The summation order inside einsum is NumPy-internal. It is described as observed.
- Concurrent use is untested. The geometry is read-only.
- 0449/0452 were not run end to end with the adapter. Their fixture line module lives outside this lane, so only their Step-1 gate was restated and checked.
- No native inversion, normalization, acceptance, project run or physics claim is made here.
