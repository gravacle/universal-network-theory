# INTERFACE 0452 V001: combined retained density harmonics through one cached full-ten evaluation (Claude2 module author)

## Pins (sha256 from bytes)

| File | sha256 | Use |
|---|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/combined_nonzero_feedback_0452/combined_nonzero_feedback_c2v001.py` | `b3d6d3907822e9bcb1954bc9dc4c2b2eaebd8743febc8bcf3836342e73df8991` | **this deliverable** (628 lines) |
| Task `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0452_2026-10-16_claude2_combined_nonzero_feedback.md` | `2cb7cc47429d14803a71cf0acb0ec57407c4aed414998e08ee71fac967efe3e3` | binding |
| `.../nonzero_cached_feedback_0449/nonzero_cached_feedback_c2v001.py` | `1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95` | source of the copied stage; not modified, not imported |
| `.../nonzero_cached_feedback_0449/INTERFACE_0449_V001.md` | `0c72f717640aefe6838938adaf67b8010a123bab0f29063a2de232cb3945ac77` | read |
| `.../nonzero_cached_feedback_0449/REVIEW_0449_V001.md` | `68327d2bc23cb2e7e76d861b4d5533f1f3a75fb0346f491bf23efb8238b9a274` | read; its notes still apply to the copied stage |
| `.../nonzero_cached_feedback_0449/fixtures_0449_c2v001.py` | `dff1ab5c39cc25cf052258dee2babde713acd0f682cb398c7316286099a78c25` | read (references reused in spirit, not executed) |
| `.../nonzero_density_fourier_0445/nonzero_density_fourier_c2v001.py` | `255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4` | injected as `density_fourier`, called once per mode, unchanged |
| `.../nonzero_density_fourier_0445/posix_libm_bessel_jn_provider_c2v001.py` | `9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67` | injected as `jn_provider` (READY dict) |
| `.../recovered_packet_audit/owned_fixed_xy_fourier_line_v002.py` | `3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18` | injected as `prepare_line` / `evaluate_line` |

All 0449 files had the same hashes before and after the work.

## Reuse of 0449 (copy with provenance, no new force law)

The module was assembled by substituting exact 0449 line ranges into a template; each region carries a marker comment.

- **Verbatim** (`# [0449 Lx-Ly verbatim]`, byte-identical; checked mechanically by fixture I): 16 blocks, 255 of 0449's 456 lines.
  - 32-36 imports; 40-42 constants; 73-78 exception classes; 81-92 `_real_array`; 95-115 `_response_packet`; 118-124 `_tolerance`; 131-167 `_validate` body; 173-204 `_point_packet`, `_reality`, `_cylindrical`.
  - 223-225 tolerances; 236-241 unpacking/grid; 251 provenance copy; 261-264 reality/failure/stage init.
  - 331-338 **step 2** `delta_prepared = unit * delta_j[:, None, None]`; 340-394 **step 3** line reads and reality checks; 396-449 **step 4** lapse inputs, LINEAR, optional log difference, `except Exception`; 456 final return.
- **Adapted** (`# [0449 Lx-Ly adapted: ...]`, edit stated in the marker):
  - 44-70 `CONVENTION`: new task pin; added `reused_source`, `modes`, `per_mode_gate`, `summation`, `mode_zero`, `branch`; `source_increment`, `base` and `excluded` name the total increment; other entries textually unchanged.
  - 127-130 / 168-170 `_validate` signature and return: `radius_m`, `rho_modes_kg_m3` replace the single-mode inputs.
  - 207-222 signature/docstring; 226-234 validation call (INVALID_INPUT dict gains `failure_mode`, `modes_included`, `modes_omitted` = None); 242-250 `inputs` summary (`mode` → `modes_included`, `modes_omitted`, `mode_count`, `rho_modes_dtypes`, `positions`, `summation_order`); 253-260 work/checks/tally; 266-295 `finish`.
  - 297-329 **step 1**: the same gate, run once per mode in a loop, plus the wave-array check.
  - 450-455 interruption: attribute `unt0452_retained_result`; an in-flight mode's `unt0445_retained_result` is kept under that mode.
- **New** (`# [0452 new: ...]`): pins/`ALLOWED_MODES`, `SUMMATION_ORDER`, `_rho_modes` (mapping validation), included/omitted modes and wave snapshot, `current` (in-flight mode), the summation (lines 477-487).
- **Diff vs 0449** (difflib, n=0): 280 lines added, 108 removed. The 108 removed lines are all in the adapted regions. Steps 2-4 (the field and lapse stage) have no diff lines.

## Signature

```python
combined_nonzero_feedback(*, density_fourier, jn_provider, radius_m, z_m, weights_RdRdz_m3,
    rho_modes_kg_m3, k_physical_inverse_m, unit_response, base_prepared,
    prepare_line, evaluate_line, eval_radius_m, eval_phi_rad, eval_z_m, c_m_s,
    base_reality_atol, base_reality_rtol, increment_reality_atol, increment_reality_rtol,
    wave_chunk, position_chunk, include_log_difference, provenance) -> dict
```

There are 23 keyword-only arguments with no defaults. Import is inert, and the module imports only `math`, `numbers`, `collections.abc` and `numpy`. Every argument except one keeps its 0449 contract (INTERFACE_0449 table). The exception is `rho_modes_kg_m3`, which replaces 0449's `rho_mode_kg_m3` and `mode`:

| Argument | Contract (a violation gives `INVALID_INPUT` at `validation`; nothing is called) |
|---|---|
| `rho_modes_kg_m3` | A nonempty `Mapping` `{m: rho_m}`. Keys must be unique, of type exactly Python `int`, with 1 <= m <= 6; `bool`, numpy integers, floats and strings are rejected, and so are duplicates yielded by a custom Mapping. Each value must be a complex64/complex128 1-D array, finite, with shape equal to `np.asarray(radius_m).shape`, so every mode sits on the **one** common `radius_m`, `z_m`, `weights_RdRdz_m3` roster (R dR dz **without 2pi**). Each value is the 0445 coefficient c_m, with ρ = c_m e^{imφ} + c.c. The module checks all values before any 0445 call, then passes read-only complex128 copies; 0445 validates them again. |
| `radius_m`, `z_m`, `weights_RdRdz_m3` | One roster, passed unchanged to every 0445 call. 0445 validates it, so an invalid roster gives `INVALID_INPUT` at `density_fourier_validation` on the first mode. |
| `include_log_difference` | bool, explicit. Root passes `False` for physical iteration (the LINEAR branch). With `True`, the log difference is added under its own label, and its positivity condition can fail the call (REVIEW_0449 note 1). |

## Operations and summation order

1. **Modes.** Modes are processed in **ascending m**, whatever the mapping's insertion order.
   - `modes_omitted` = the values in 1..6 that were not supplied.
   - m = 0 is not accepted, and there is no m0 source correction.
2. **Per mode.** For each m:
   - Call `density_fourier(radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3=rho_m, k_physical_inverse_m=waves, c_m_s, mode=m, bessel_jn=jn_provider['bessel_jn'], wave_chunk, position_chunk)`. `waves` is the one validated read-only (nk,3) array, bitwise equal to the unit and base wavevectors.
   - Required, as in 0449: `status == 'COMPLETE'`, `complete is True`, `counts.waves == nk`, `counts.mode == m`, a full `retained_wave_mask`, and `deltaJ0_J` complex128 (nk,) and finite.
   - New: the wave array must still be bitwise equal to its snapshot after the call.
   - 0445 returns no wavevectors. Identical signed order is therefore enforced by passing the same array every time and by these checks.
3. **Summation** (`SUMMATION_ORDER`):
   - Left fold in ascending m: `combined = copy(dJ[m_1])`, then `combined = combined + dJ[m_k]` for k = 2, 3, ....
   - These are complex128 elementwise IEEE adds, with no compensation and no reordering. Each per-mode array enters exactly once.
   - With one mode, the total is a bitwise copy of that mode's array.
   - The total is checked finite and stored read-only.
4. **Unchanged 0449 steps 2-6**, run once:
   - `delta_prepared = unit * deltaJ0_total[:, None, None]`.
   - One base read and one increment read per (R_i, phi_j, z_ijl), with zero boundaries and per-point reality checks.
   - LINEAR lapse feedback, plus the optional separately labelled finite log difference.
   - All supplied angles are kept, and there is no DFT.
   - There is no extra minus, c², 2π, R, dk or volume weight, no F2 source subtraction and no base accumulation.

## Return dict

- **Top level:**
  - `status`, `complete`, `reason`, `failure_stage`, `failure_mode`, `exception_type`, `failure_point`, `failure_check`.
  - **`modes_included`** (ascending tuple) and **`modes_omitted`** (tuple, from 1..6).
  - `provenance`, `inputs`, `jn_provider_metadata`, `completeness`, `reality`, `convention`, `retained`.
  - There is no `mode` key anywhere, so a combined source carries no single-mode tag.
- **`inputs`:**
  - Mode fields: `modes_included`, `modes_omitted`, `mode_count`, `rho_modes_dtypes` `{m: dtype}`, `positions`, `waves`, `summation_order`.
  - Plus the 0449 fields: dtypes, `layout`, `eval_grid`, eval arrays, `angles_equal_2pi_j_over_n`, `c_m_s`, `tolerances`, chunks, `include_log_difference`, `boundary`.
- **Payload, set only on `COMPLETE`:**
  - `density_fourier_results`: `{m: full 0445 dict}`.
  - **`deltaJ0_J_by_mode`**: `{m: (nk,) complex128, read-only}`.
  - **`deltaJ0_J_total`**: (nk,).
  - `delta_prepared`: `{wavevectors, weighted_responses (nk,10,1)}`.
  - `base_line` and `increment_line`: each `{fields (nR,nphi,nz,10), gradient (...,10,3), hessian (...,10,3,3)}`, complex Cartesian.
  - `point_mask`.
  - `lapse`: `nb`, `grad_nb_cartesian`, `dn`, `grad_dn_cartesian`, `Nb`.
  - `linear`: `label`, `deltaPhi_m2_s2`, `grad_deltaPhi_cartesian_m_s2`, `grad_deltaPhi_cylindrical_R_phi_z_m_s2`.
  - `log_difference`: the same keys under its own label, or None.
- **`completeness`:**
  - Per mode: `density_fourier_status_by_mode` `{m: status, or None if not called}`, `modes_complete`, `density_fourier_calls` / `_expected`.
  - Points: `points_expected` / `points_evaluated` / `all_points_evaluated`.
  - Line calls: `line_prepare_calls` / `_expected` = 2·nR·nphi and `line_evaluate_calls` / `_expected` = 2·points. Both are independent of the number of modes.
  - `checks`: `all_modes_complete`, `all_mode_deltaJ0_finite`, `deltaJ0_total_finite`, `delta_prepared_finite`, `all_points_finite_and_real`, `lapse_inputs_finite_Nb_positive`, `linear_finite`, `log_difference_finite` (None if not requested).

## Failure semantics (fail closed, retention)

| Case | status / failure_stage / failure_mode | Retained |
|---|---|---|
| Malformed argument or mode mapping | `INVALID_INPUT` / `validation` / None | nothing is called; `retained` None; modes keys None |
| 0445 returns INVALID_INPUT for mode m | `INVALID_INPUT` / `density_fourier_validation` / m | earlier per-mode results and deltaJ0, plus the 0445 dict for m |
| Mode m not COMPLETE, forged, wrong counts/mode/mask/dtype/shape, nonfinite, or waves changed | `FAILED_CLOSED` / `density_fourier` / m | every 0445 dict obtained, including m's partial `retained_deltaJ0_J`; deltaJ0 of the modes that passed. Later modes are **not called** (status None). No total is formed and no line call is made. |
| Overflow/nonfinite in the sum (FloatingPointError under the caller's errstate) | `FAILED_CLOSED` / `deltaJ0_sum` / None | all per-mode results |
| Any later stage (`delta_prepared`, `line_*`, `point_checks`, `lapse_inputs`, `linear_feedback`, `log_difference`) | as in 0449 | per-mode results, total, line arrays (NaN where not evaluated), `point_mask` |
| KeyboardInterrupt or other non-Exception | re-raised; `exc.unt0452_retained_result` (status `INTERRUPTED`) | as above; the in-flight mode's `unt0445_retained_result` is kept under that mode |

Payload keys are None on every non-COMPLETE status. No warning is suppressed.

## Fixtures (synthetic analytic only): 100/100 PASS

Setup:
- Interpreter: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (Python 3.12.14, NumPy 2.3.5), with `VECLIB_MAXIMUM_THREADS=OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`.
- Every pinned module was read once, hashed, and executed from those exact bytes. The provider was built with `create_jn_provider(library_policy='posix_find_library_m', expected_library_path=None, max_cache_entries=0)` and was READY (`/usr/lib/libm.dylib`, symbol `jn`).
- No `.npz` file, root worker, project run or target data was used. The run took 3.3 s.

Scratch files in `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0452/module_author/`:

| File | sha256 |
|---|---|
| `template_c2v001.py.txt` | `e80aa036177d345606100ba6775bf0948cfc7706443bb4810be40cc861a15c34` |
| `build_c2v001.py` (substitutes 0449 lines after its pin check) | `361fc0afc550ba6264cd1bfb562158ef194a07d042990e1966e0780fd83e41da` |
| `test_combined_c2v001.py` | `5a9f41fbc29afcd40de8bb055656eaba6076cbb29d208a6355228d5ff0974bfe` |
| `run1.json` (records target `b3d6d390…`) | `9b711dba1488d5551d936d6ecc069c8f9c807cfa8002231c3a2d6fa598ae23c5` |
| `run1_diff_0449_to_0452.txt` | `d2d03e75cfb7c5efc9c7c00a044f46ed0c18769308f672c9a4e450b7cd2a3578` |

**Base case:**
- c = 3.7; 4 ring points (R dR dz without 2π).
- 10 signed waves in scrambled order: 4 ± pairs plus a k⊥ = 0 pair.
- Hermitian-paired synthetic unit and base (nk,10,1), with all ten components nonzero.
- Evaluation over 2 radii × 16 roster angles × 3 angle-dependent heights. Tolerances are 1e-11.

| Fixture | Result |
|---|---|
| **A. Two harmonics {1,3}** | **Source.** Per-mode deltaJ0 vs a direct 2048-node azimuthal trapezoid of the real density with e^{-ik·x} (no Bessel, no (-i)^m): 2.8e-16 / 8.9e-16. The total vs the trapezoid of the combined density: 1.3e-16. The total is bitwise `by_mode[1] + by_mode[3]`, and `delta_prepared` is bitwise `U*total`. **Fields.** Increment and base fields, gradient and Hessian vs a brute Σ_k: ≤ 3.9e-16. LINEAR ΔΦ and its gradient vs the formula: ≤ 6.3e-16. **Against 0449.** The combined result equals the sum of two separate 0449 runs (increment fields, Hessian, LINEAR ΔΦ and cylindrical gradient) to ≤ 4.5e-16. Per-mode deltaJ0 and `base_line` are bitwise equal to 0449. **Bookkeeping.** All 16 angles are kept, with complex128 full jets. Call counts are 2 contractions, 64 prepares and 192 evaluates. Metadata reads included (1,3) and omitted (2,4,5,6), with no `mode` key. `log_difference` is None. |
| **A6. All six modes, inserted 5,2,6,1,4,3** | Processed in ascending order. The total is bitwise the ascending left fold. A descending fold differs by 1.7e-18, which shows the stated order is the one used. Total vs the direct six-harmonic trapezoid: 2.6e-16. Increment jets vs brute: ≤ 3.8e-16. Combined vs the sum of six 0449 runs: ≤ 3.5e-16. Line calls stay 64/192. |
| **B. One mode vs 0449** | Cases: m=1 without log; m=4 and m=6 with log; m=2 with complex64 input. **Every payload array is bitwise equal to 0449**, max \|diff\| = 0.0, over 18 or 21 arrays: deltaJ0 (total and by_mode), delta_prepared, base and increment f/g/h, point_mask, 5 lapse arrays, 3 linear and 3 log arrays. The reality summaries and call counts are also identical. |
| **C. Cancellation and zero** | **Zero.** Zero coefficients for {1,2} give a total, increment f/g/h, dn, ΔΦ and gradient that are all exactly 0; the base read is bitwise equal to 0449. **Cancellation.** One ring point and one ±k pair with ρ₃ chosen so J₃Re(ρ₃e^{3iα}) = J₁Re(ρ₁e^{iα}). Per-mode \|deltaJ0\| is 4.7e-3 and both are retained; the total is 8.7e-19 (1.8e-16 relative). The increment is 1.8e-16 of the single-mode increment. k⊥=0 entries are exactly 0. |
| **D. No duplicated base** | For 1, 2, 3 and 6 modes, counting wrappers show M contractions, exactly 32 base prepares (each with weighted_responses bitwise equal to the supplied base), 32 increment prepares and 192 evaluates. `base_line` is bitwise identical across mode counts. |
| **E. Partial mode rejects the total** | **Provider failure.** A provider fails inside mode 3 of {1,3,5}, giving FAILED_CLOSED at `density_fourier` with failure_mode 3 and 0 line calls; no total is formed. Retained: m1 COMPLETE plus its deltaJ0, and m3 FAILED_CLOSED with its partial 0445 retention (waves retained 0 < n < nk); m5 is never called (status None). **Forged mode-3 results** (9 forms: complete False, status PARTIAL, wrong counts.mode, wrong counts.waves, incomplete mask, complex64, wrong length, inf, non-mapping) all give FAILED_CLOSED with m1 retained. **Other cases:** a wave array mutated by the callable gives FAILED_CLOSED. A 0445 INVALID_INPUT at mode 4 gives INVALID_INPUT at `density_fourier_validation` with m2 kept. A J0-substituting provider gives FAILED_CLOSED at mode 1. An invalid roster gives INVALID_INPUT after one call. |
| **F. Anisotropic mixing retained** | Ring of 48 directions × kz ±0.5, modes {1,4}. Increment vs brute at all 16 angles: ≤ 8.5e-16. Anisotropic combined vs the sum of 0449 runs: 6.3e-16. In the 16-angle DFT of dn, the response (1+0.6cos2α) puts m3/m1 = 4.5e-2, m6/m4 = 6.3e-3 and m2/m4 up to 11.9. The isotropic response leaves these slots at 5e-16 to 6e-12. The output is not projected. |
| **G. Validation** | 27 malformed inputs give INVALID_INPUT at validation, with no 0445 or line call. They include: non-mapping, empty, keys True/0/7/-1/np.int64/2.0/'1', duplicate keys, real/int/object rho, length q+1, (1,q), NaN, inf, a malformed second mode, a non-READY provider, an int log flag, (nk,10,10), permuted base waves, bool c/tolerance/chunk, bad eval_z shape and non-mapping provenance. The function has 23 keyword-only parameters with no defaults, and a missing keyword raises TypeError. |
| **H. Errstate, interruption, inherited checks** | **Errstate.** A sum overflow under `raise` gives FloatingPointError, then FAILED_CLOSED at `deltaJ0_sum` with both modes retained. Under `ignore` it fails closed as nonfinite. Under `warn` the RuntimeWarning is emitted and the call fails closed. **Interruption.** A KeyboardInterrupt on the 41st read is re-raised with INTERRUPTED, 20 points and the total retained. A KeyboardInterrupt inside the mode-3 contraction is re-raised with m1 COMPLETE and m3's 0445 INTERRUPTED record. **Inherited checks.** Nb ≤ 0 gives FAILED_CLOSED at `lapse_inputs` with all points retained. Nb+dn ≤ 0 with log gives FAILED_CLOSED at `log_difference` with linear retained; without log it is COMPLETE. A non-Hermitian unit row gives FAILED_CLOSED at `point_checks` (increment, fields, (0,0,0)). |
| **I. Lane and provenance** | Imports are as stated and the top level holds only definitions. There is no `@`, einsum, dot, matmul, linalg, errstate, seterr, warnings, open, print, eval, exec, fft, clip, mean or nan_to_num. Import is inert. All 16 verbatim blocks are byte-identical to 0449. |
| **J. kpc scale** | Physical c, ρ ~ 1e-21, kpc radii and k, modes {2,5}, under `raise`: COMPLETE and finite. The total vs the direct trapezoid agrees to 2.0e-15, and max \|dn\| is 6e-5. |
| **K. Mutants of the combining delta** | All 10 are detected by fixtures A, A6, D and E: last mode dropped, first counted twice, base re-added into the increment, base accumulated per mode, failed mode skipped, conj(deltaJ0), a nominal `mode` tag, per-mode result not retained, log substituted into linear, last mode summed twice. |
| **pins** | All pins and the target are unchanged after the run. |

## Root use

Use is the same as 0449 (INTERFACE_0449, "Root use"), with one change: instead of `rho_mode_kg_m3` and `mode`, pass `rho_modes_kg_m3 = {m: c_m on the common roster}` for the solved retained modes, and `include_log_difference=False` for physical iteration. Root records in `provenance` which modes were solved and which are absent. The module reports `modes_included` and `modes_omitted` but does not judge an omission.

## Limitations

1. **Omitted modes are reported, not judged.** `modes_omitted` only lists the values in 1..6 that were not supplied. Whether an absent mode is negligible or still unsolved is root's call.
2. **The first failing mode stops the call.** Modes after it are not contracted, so their status is None. Root re-runs after fixing the cause; there is no partial combined total by design.
3. **Summation is plain IEEE in ascending m.** A different order changes only roundoff (A6: 1.7e-18). The sum is uncompensated, so with strongly cancelling modes the relative error of the total grows as \|total\| / max\|deltaJ0_m\| shrinks (C: absolute 8.7e-19 at per-mode 4.7e-3).
4. **16 angles resolve \|m\| ≤ 7.** With m ≤ 6 sources and an anisotropic response (m ± 2 and beyond), output content above 7 aliases in the 16 samples. No DFT is made here (as in 0449).
5. **Cost scales with M only in 0445.** There are M contractions over nk × q. The line stage is fixed at 2·nR·nphi prepares and 2·points evaluates, as in 0449, with the same memory (about 153 MB for 72×16×32 points) plus M × nk × 16 B for the per-mode deltaJ0. Production timing is UNTESTED; the deciding test is root timing one radius at production nk with all retained modes.
6. **Inherited from 0449 and REVIEW_0449, unchanged:**
   - one (atol, rtol) pair per role across three units;
   - a failure of the log positivity condition suppresses the linear payload;
   - stored packet dtypes are UNTESTED;
   - callable identity and F2 base identity rest on root's `provenance`;
   - the rho_m convention is c_m with ρ = c_m e^{imφ} + c.c. Root must confirm its solved annular modes use c_m and not 2c_m.
7. **Wave-order evidence is indirect.** 0445 does not echo wavevectors. Signed order rests on passing the same validated read-only array to every call and re-verifying it bitwise afterwards.
8. **Not reviewed yet.** This is author-side evidence only. Per 0452, a distinct helper reviews the factoring/combining delta and final pins.
