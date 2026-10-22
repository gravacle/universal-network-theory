# INTERFACE 0445: libm integer-order Jn provider (c2v001)

Module: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/nonzero_density_fourier_0445/posix_libm_bessel_jn_provider_c2v001.py`
sha256 `9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67`

Binding inputs verified from bytes: task 0445 `29ebcffd...720835`, j0 provider pattern `c7c93416...38a1d`, m0 Fourier convention `f5670726...84756`, root v004 `6da11133...02ed`. All were read as text only. None is imported.

## API

```
create_jn_provider(*, library_policy, expected_library_path, max_cache_entries) -> dict
```

- `library_policy`: must be the str `'posix_find_library_m'`, meaning `ctypes.util.find_library('m')` as in the j0 provider.
- `expected_library_path`: `None` records whatever the lookup resolves. A str must equal the resolved path exactly. On this host that path is `'/usr/lib/libm.dylib'`.
- `max_cache_entries`: a Python `int` >= 0. `0` disables cross-call caching. bool, float and numpy ints are rejected.
- Invalid caller arguments raise `TypeError` or `ValueError` before any lookup. All three arguments are keyword-only and none has a default.
- Returns `dict(status, bessel_jn, metadata, finding)`. Only `status == 'READY'` gives a callable. Any other status returns `bessel_jn=None` and a precise `finding` string, and no substitute is ever made:
  - `LIBM_NOT_DISCOVERABLE`
  - `LIBM_PATH_MISMATCH`
  - `LIBM_LOAD_FAILED`
  - `LIBM_JN_SYMBOL_UNAVAILABLE`
  - `LIBM_JN_ALIASES_J0` (the jn entry address equals the j0 address)

```
bessel_jn(n, x_array) -> numpy.ndarray (float64, shape of x_array; 0-d in gives 0-d out; new array)
```

- `n`: a Python `int` or `numpy.integer`, not bool, in the declared range `MIN_ORDER..MAX_ORDER = 0..6`. Floats, strs, arrays and orders 7 or -1 are rejected.
- `x_array`: an array-like with a float16/32/64 dtype, or an int/uint dtype with |v| <= 2**53. Every value must be finite. Negative values are allowed and libm applies parity; the exact parity check passed. complex, bool, object, str and >8-byte float dtypes are rejected.
- Errors: invalid input raises `TypeError` or `ValueError` before any evaluation. A `RuntimeError` is raised if libm returns a nonfinite value, a value with |J|>1, or a J_n(0) other than exactly 1.0 (n=0) or 0.0 (n>=1). No partial output is ever returned.
- Use in 0445: the argument is `k_perp*R_q` (>= 0). At k_perp=0, J_m(0) for m=1..6 comes back as exact +0.0, and every evaluation checks this. Any finite alpha_k therefore gives an exactly zero term with no division by k_perp.
- Positional and keyword calls both work: `bessel_jn(m, arg)` and `bessel_jn(n=m, x_array=arg)`.
- Root pattern: `r = create_jn_provider(...)`, then require `r['status']=='READY'`, then pass `r['bessel_jn']` and log `r['metadata']`. This is a dict, where the j0 provider returned a tuple.

## Loading details

- Lookup: `ctypes.util.find_library('m')` resolved `/usr/lib/libm.dylib` on macOS arm64 (Darwin 25.6.0, Python 3.12.14, NumPy 2.3.5).
- Binding: `ctypes.CDLL(path).jn` with `argtypes=[c_int, c_double]` and `restype=c_double`, i.e. `double jn(int, double)`.
- Symbol image: `dladdr` on the process handle gives image `/usr/lib/system/libsystem_m.dylib` and symbol name `jn`.
- `j0` is resolved only for an address comparison. The addresses are distinct (`j0_symbol_distinct=True`), and j0 is never evaluated.
- Construction evaluates nothing (`evaluations == 0`).
- Import performs no lookup or load. This was tested by importing with `find_library` patched to raise.
- I/O is limited to libm discovery and loading. On Linux, the stdlib `find_library` may consult ldconfig or gcc.
- The live `metadata` dict holds the static fields: `provider`, `library_policy`, `lookup`, `expected_library_path`, `resolved_library_path`, `loaded_library_name`, `symbol`, `signature`, `symbol_image_path`, `symbol_image_name`, `image_resolution`, `j0_symbol_distinct`, `order_range`, `max_cache_entries`, `cache_policy`, `exact_argument_reuse`, `signed_zero`, `output_invariants` and `scope`.
- It also holds counters: `calls`, `evaluations`, `cache_hits`, `cache_evictions` and `cache_entries`.

## Evaluation and cache semantics

- Each call flattens x and adds 0.0, which turns -0.0 into +0.0. It then runs `np.unique`, and each unique (order, argument) gets one libm `jn` call in a plain Python loop. This happens whatever the cache setting.
- The module has no recurrence, series, interpolant, asymptotic form or J0 substitution of its own.
- `max_cache_entries > 0` turns on an `OrderedDict` LRU keyed by `(int order, float argument)`:
  - A hit moves its entry to most recent.
  - An entry is inserted only after the output invariants pass.
  - When the cache exceeds the bound, the oldest entry is evicted.
  - The cache is keyed by order, so J_1(x) and J_2(x) are separate entries.
- Results are bitwise identical with cache 0, 2, 100 and 4096 (tested).
- Interruption and failure: input rejection happens before any evaluation. If a libm invariant fails, the call raises and its partial output is discarded. Values validated earlier in that call stay cached because they are valid. The fault-injection test confirmed both points.
- Single-threaded use only.
- Floating point: the provider suppresses nothing and catches nothing. The caller's `np.errstate` governs. Valid inputs ran clean under `errstate(all='raise')`, including the underflow cases 5e-324, 1e-300 and 1e-160, and the large values 1e5 and 1e300.
- Throughput on this host is roughly 0.33 µs per uncached evaluation: 65,536 unique arguments took 0.022 s. This is indicative only.

## Accuracy observed (libm jn on this host; TESTED-POSITIVE at these points only)

Reference functions exist only in the test and are not part of the provider:

- **Poisson integral:** `J_n(x) = (x/2)^n 4^n n!/(pi (2n)!) * int_0^pi cos(x cos t) sin^{2n} t dt`, evaluated with a 512-point periodic trapezoid and `math.fsum`. It is relatively accurate at small x and for x < n.
- **Bessel integral:** `(1/2pi) int_0^{2pi} cos(n t - x sin t) dt`, evaluated with a periodic trapezoid with N >= 2(|x|+n)+512 and `math.fsum`. Its accuracy is absolute.
- **Hankel asymptotic (secondary, x >= 1e3):** 24 terms, with the phase computed through cos/sin addition so that x is never rounded.
- The Poisson and Bessel references agree to 2.2e-16 for x in [0.01, 7.5].

Grid: n = 0..6 at these x values:

- Small: {5e-324, 1e-300, 1e-150, 1e-30, 1e-12, 1e-6, 1e-3, 0.01, 0.1}
- Below 6: {0.25, 0.5, 1, 1.5, 2, 3, 4, 4.9, 5.5, 5.99}
- Moderate: {6, 7.5, 10, 13.7, 25.3, 50, 77.7}
- Large: {100, 333.3, 1000, 3141.59, 1e4, 1e5}

| regime (reference) | points | max abs err | max rel err | tolerance applied (all passed) |
|---|---|---|---|---|
| x <= 0.1 (Poisson) | 63 | 1.1e-16 | 4.1e-16 | rel 4e-15 + 1e-307 floor |
| x < n, x >= 0.25 (Poisson) | 35 | 8.3e-17 | 4.2e-16 | rel 4e-15 |
| n <= x < 6 (Poisson) | 35 | 1.1e-16 | 5.6e-16 | rel 4e-15 |
| 6..77.7 (Bessel integral) | 49 | 3.1e-16 | 6.1e-14 (near a J_0 zero) | abs 1e-15·max(1,x) |
| 1e2..1e5 (Bessel integral) | 42 | 6.4e-14 | 3.7e-11 | abs 1e-15·x (reference-limited by x·sin t rounding) |
| 1e3..1e5 (Hankel, secondary) | 28 | 3.1e-17 | 6.2e-15 | abs 1e-15 |

- Example of the small-x behavior: `jn(6, 1e-3) = 2.17013881138393e-23`, which equals (x/2)^6/720. libm is therefore not using an unqualified forward recurrence at small x.
- Exact checks passed:
  - J_0(0) is exactly 1.
  - J_n(0) is exactly +0.0 for n = 1..6, including at -0.0.
  - J_m differs from J_0 at every probe for m = 1..6.
  - Parity J_n(-x) = (-1)^n J_n(x) holds bitwise.
  - The three-term recurrence identity, a test-only consistency check, has a residual of 5.6e-17.
- UNTESTED: |x| > 1e5, and points outside this grid. The deciding test is to extend the Hankel comparison to the argument range the root actually uses. No analytic floating-point bound is claimed.

## Evidence (scratch, not deliverables)

- Test: `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0445/jn_provider/test_jn_provider_c2v001.py`, sha256 `0a9a5d0594c8e4940a05e88a9c3d7e81314d45d41d52fa0ef1d68b7b8d90dc2d`.
- Command: `env VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B test_jn_provider_c2v001.py <module path>`.
- The run against the deliverable path gave `status: PASS` with 0 failures and finished in about 0.3 s. The output is `run_final.json` in the same folder, sha256 `9dda836866d2cd26aca7e97049d2e119d6c5890822809a2f3c3fb7cac640d31d`.
- What the test covers:
  - Import inertness and the factory contract.
  - The five non-READY findings. Four were simulated by test-only monkeypatches that were restored afterwards. The path mismatch was produced by passing a wrong expected path.
  - Fault injection: libm output that is NaN, has |J|>1, or gives J_1(0) != 0 is refused, and validated entries are retained.
  - Validation, shapes and dtypes.
  - Accuracy, parity, the recurrence identity, cache, LRU and signed zero.
  - Behavior under errstate.

## Lane compliance and scope

- Dependencies are numpy, the stdlib and ctypes.
- No BLAS products and no warning suppression.
- The factory is keyword-only with no defaults.
- Only definitions run at import.
- There was no project data, no target access, no scientific run and no acceptance. The contraction, the normalization and the use of the response all belong to other roles or the root.
