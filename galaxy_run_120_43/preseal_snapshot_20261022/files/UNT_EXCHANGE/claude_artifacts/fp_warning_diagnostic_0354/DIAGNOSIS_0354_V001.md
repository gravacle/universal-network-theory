# 0354: floating-point warnings in the saved 0351 run (generic diagnosis)

Author: CLAUDE2 main lane. Only generic matrices were used: no UNT matrices, spectra, frozen cases or output-derived numbers. Bounded single-thread subprocesses; no network, no installation, no environment change. The saved output is unchanged.

## What the saved run shows (metadata only)
- `BIND_COUPLING_REFERENCE_OUTPUT_V001.json` (bb43d2b0…) ran under Xcode Python 3.9.6, NumPy 2.0.2 (user site), macOS 26.6 arm64, with all five thread variables set to 1.
- Each case captured 1008 RuntimeWarnings. Fifty were retained, all at producer V002 line 136, `eig()`, cycling "divide by zero / overflow / underflow / invalid value encountered in matmul".
- **The count is structural:** 1008 = 4 flags × 252, and 252 is exactly the number of N×N @ N×N products per case:
  - 64 `M@V` in eig: 2 endpoints + 62 blocks;
  - 64 `V.T@V` in eig;
  - 62 spectral-inverse `(V/(w−E1))@V.T`;
  - 62 inverse-residual `A_@Rs`.
  
  The thousands of matrix-vector products in the contractions produced none.

## Generic diagnostic (fp_warning_diagnostic_v001/v002; results V001/V002 retained)
NumPy's BLAS and LAPACK here are **Accelerate** (`np.show_config`).

| Finding | Evidence |
|---|---|
| `matmul` on C-ordered float64 N×N matrices raises all four status flags for N ≥ 15, not at N = 2, 4 or 8 | flags observed per operation via `np.errstate(all='call')` + `seterrcall` |
| Transposed or strided views flag already at N ≥ 8; matrix-vector flags only at N = 32 | same |
| **Results are bit-exact in every flagged case** | integer-valued matrices compared with an independent pure-Python scalar-loop product: `array_equal` true at every size and layout |
| **Data-independent:** all-zero, identity and all-ones matrices flag identically at N = 16 and 24 | probe `data_independence`. A zero product cannot divide by zero, overflow or produce NaN, so the flags cannot come from the arithmetic on the data. |
| Under the default `errstate` the flags surface as the observed RuntimeWarnings (40 at sizes 8/15/16/24, as in the saved run); under `errstate(all='raise')` the same products raise FloatingPointError although exact | probes `matmul_exact_warn`, `matmul_exact_raise` |
| Non-BLAS `np.einsum(..., optimize=False)` gives no flags and identical exact results. `np.dot` gives no warnings because it does not check the status flags (it is not a ufunc), not because the backend behaves differently | all probes |
| Independent of a preceding `eigh`/`solve`, and of the thread variables (set to 1 or unset) | probes `matmul_after_eigh`, `matmul_exact_threads_unset` |
| For the generic eig residual/orthogonality pattern, `matmul` agrees with `einsum` to ≤ 2.2e-16 (orthogonality 0) | probe `eig_residual_pattern` |

**Diagnosis.** These are reproducible backend status-flag artefacts of Accelerate's dgemm path as reported by NumPy's ufunc status check. They are not non-finite arithmetic.
- The saved run's finite values, residual and orthogonality checks, and agreement across the literal, DP, solve and spectral routes are consistent with this diagnosis.
- This explains the warnings. It does not by itself accept the scientific numbers; numerical acceptance stays root's.
- The same pattern is expected for the 0347 four-pattern producer at N = 16 and 24. Its V003 already records the warnings (32 per case on generic blocks in review).

## Inert patch proposal (not a launch version)
`PATCH_PROPOSAL_bind_producer_v003.py`, diff `PATCH_PROPOSAL_bind_producer_V002_to_V003.diff.v2`. The first `.diff` predates the CASE_ERROR flag-attachment edit and is superseded; it is kept, not deleted.
- **Exactly four sites** (eig residual, eig orthogonality, spectral inverse, inverse residual) call `mm(site, A, B)`. It computes the **same `A @ B`** inside a local `np.errstate(all='call')`.
  - Raised flags are recorded per site, with kinds and counts.
  - Each flagged product is **verified**: all finite, and every entry within 64·k·eps·(|A||B|) of an independent non-BLAS `einsum`.
  - An unverified product enters `check_failures` (`backend_flag_unverified`). A non-finite one still fails (CASE_ERROR), with the flag record attached.
- **All other operations** keep the V002 warning capture: visible and counted.
- **No global suppression.** No change to formulas, tolerances or parameters.
- **Numerical equivalence:** bit-identical by construction (the same matmul call). This was verified on a generic 16-site toy: the full computed content is JSON-equal to V002 (E2).

**Evidence** (`patch_evidence_v003.py`, 9/9):

| Test | Result |
|---|---|
| E2 | content identical to V002 |
| E3 | V002 reproduces 1008 warnings per case; the proposal emits 0 RuntimeWarnings |
| E4 | 252 flagged products accounted (64/64/62/62), all VERIFIED |
| E5 | under PYTHONWARNINGS=error: COMPLETED, stderr empty, identical content |
| E6 | a NaN input still gives CASE_ERROR / FAILED |
| E6b | an infinite product is returned unmasked and classified UNVERIFIED |
| E6c | a finite flagged product is bit-identical and VERIFIED |
| E7 | V002 also fails on the NaN input |

**Scope:** applying this needs a separately reviewed producer version with fresh immutable paths and a root decision. The launcher would need only a new producer pin. The same `mm()` pattern applies to the 0347 producer's N×N products, and to 0355 if adopted.

**Controls not done:**
- No other BLAS or NumPy build, because installing packages is not permitted.
- No hardware FP-flag introspection below NumPy.
