# REVIEW 0458 CONTRACT V001: contract, cache and convention lens

**Role:** distinct reviewer, not the author. I wrote neither the module nor the fixtures, and I did not read the other reviewer's review.
**Verdict: PASS_WITH_NOTES.** There are no blocking issues.

The module `grouped_density_fourier_c2v001.py` meets task 0458 on every contract, cache and convention point I checked:

- identity binding
- stale, tamper and convention rejection
- no rho-dependent caching
- limits checked before allocation
- fail-closed statuses with retention
- FloatingPointError and interrupt handling
- unmutated inputs, no I/O, inert import
- the lane convention
- an adapter faithful to 0445 for the 0449/0452 code
- an accurate frozen INTERFACE

Two items are notes, not blockers: an interrupt window during COMPLETE packaging (the same structure as pinned 0445), and a small understatement in the per-evaluation hashed-bytes formula.

The module is still UNTESTED at root scale and on root geometry. The deciding test is root's comparison with the saved actual 0445 output, using a roundoff tolerance against the per-wave bound c^2*2pi*sum_q |w_q J_m|*2|rho_q|.

## Hashes (sha256 from bytes; checked at start and again after all runs)

| File | sha256 |
|---|---|
| Task 0458 (binding) | `18eb2dba463378903a952fd408d1f3b8a5cff9fc9be1b580921cbab9c1e51fdf` |
| 0445 contraction | `255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4` |
| 0445 Jn provider (used unchanged) | `9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67` |
| 0455 pattern | `0dab62be91cfd793949ef251aa3e731b4544e7131606599784762cb4101175ea` |
| Module under review | `9db7efd1ef18927c5886ab9b28d4f72cae16770cb3d3b04f574237b006a4bcbe` |
| INTERFACE_0458_V001.md | `74fc9b4a51076ffb9013cef6bb6ccbf5bc1425c990ccf8610129eab53f5c7f0d` |
| fixtures_0458_c2v001.py | `65ffda168ffb57fddb19ca9de0810e95ba794fb672d1e21300fa12ea5d71a7ba` |
| 0449 module (consumer, loaded read-only) | `1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95` |
| 0452 module (consumer, loaded read-only) | `b3d6d3907822e9bcb1954bc9dc4c2b2eaebd8743febc8bcf3836342e73df8991` |

All 9 evidence hashes in the author and fixture reports reproduce from bytes:

- author: smoke `9cc72143…`, run_final `e41a723f…`, bench `b89d023a…`, bench_final `724d0b8e…`
- fixtures: final_run `72dcb98c…`, final_results `110fed7a…`, mutants summary `914e3d30…`, mutants json `3ec3e2e0…`, driver `9b19ed4f…`

The CONVENTION digest recomputed from the installed module is `da0e164a979b3706f79e92dbd85d07c81083ab3ebfa036b2689d853842b2df78`. It equals the INTERFACE value and the digest recorded in every geometry.

**No existing file was modified.** Every file in the 0445, 0449, 0452 and 0455 folders has an mtime of 15:46:10 or earlier, before the task file (15:52:23). The 0458 folder held only the module, the INTERFACE and the fixtures before this review. No project data, NPZ, root worker or root path was read or imported.

## What was executed

All runs used the root interpreter `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (Python 3.12.14, NumPy 2.3.5, arm64), with `VECLIB_MAXIMUM_THREADS=OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`. Inputs were synthetic only. Scratch is `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0458/REVIEW_0458_CONTRACT_V001/`.

1. **Fixture script** (`--module` set to the installed module): **PASS 23, INFO 2, exit 0, 4.4 s.** Outputs are `fixture_run_reviewer.txt` (`5e83f976…20fd`) and `fixture_results_reviewer.json` (`bcba0269…572d`).
2. **My independent checks** in `review_checks_0458.py` (`1b105520bc28c9fd386225f291f56ada803adfac6b2e79f50755ddb7f86dee04`): **PASS 18, NOTE 1, exit 0.** The output is `review_run_final.txt` (`4d57b13db301618c5576401a6c8b944c9a77ac89fe02e4e41203f8386d0757c3`). I wrote my own oracles:
   - an exact-rational oracle: Fractions sum the float per-term factors, with the bracket in the algebraically different form 2·Re(rho·e^{imα}) and using math.hypot, math.atan2, math.cos and math.sin;
   - an fsum oracle;
   - a Bessel-free azimuthal-quadrature oracle of the real field rho·e^{imφ}+c.c. under e^{-ik·x}, using kx and ky directly with no hypot, arctan2 or (-i)^m.

   The modules were loaded by exec of hash-verified bytes.
3. **Root-shaped synthetic sizes** in `review_rootshape_0458.py` (`2df4e6c70cc2a37222bbc58665ce80a6eb763824bef4cbd0c3299e4bdace4029`), output `review_rootshape_run.txt` (`cfda6c1c36b8a48e863170a3668cf418bc0a0579fd3a2b561a774ae1dab7666d`): **PASS.** The case had nq = 373248 and nk = 2304. The group counts were mine (nz 16, np 27, nr 72, nc 432), not root's.
4. **Interrupt-window probe** in `review_t18c_probe.py` (`e4e6d700…274c`), output `review_t18c_probe_out.txt` (`524fe4e3…0619`).

## Findings by required item

In the tables below, "norm." means normalized by the per-wave bound.

**Law and equivalence (C05, C06, C07, C17)**

| Comparison | Result |
|---|---|
| Module vs my exact-rational oracle (R1: q 37, nk 30; duplicates, holes, ±0 k_z and z, k_perp = 0 with signed zeros, 1-ulp-apart R, duplicate q), m = 1..6 | 2.7e-16 norm. |
| Module vs fsum oracle (R1 and R2: q 600, nk 150 lattice with holes) | 2.7e-16 norm. |
| Module vs pinned 0445 | 1.3e-16 norm. |
| Module vs Bessel-free quadrature | 9.3e-14 norm. This confirms e^{-ik·x}, (-i)^m, -c^2·2π, no extra 2, and the same e^{-ik_z z} on the minus branch. |
| Adapter vs `evaluate_mode` | bitwise equal |
| k_perp = 0 outputs | exactly 0 |
| Duplicate waves | bitwise identical |
| Linearity | Real-linear to 2.6e-16. Not complex-linear: \|F(iρ) − iF(ρ)\| is 0.47–0.77 norm. |
| Single-q sources (37 q, m = 1 and 5) | 1.0e-14. Every q is included once. |

**Identity binding and stale/tamper rejection (C08)**

| Case | Result |
|---|---|
| waves, R, z or w moved by 1 ulp | INVALID_INPUT |
| Reversed waves | INVALID_INPUT |
| Signed-zero flip of z | INVALID_INPUT |
| Unbound mode | INVALID_INPUT |
| Second provider instance | INVALID_INPUT |
| Wrapper callable as provider | INVALID_INPUT |
| Same values passed as a list | COMPLETE. The validated float64 copy is identical, as the INTERFACE states. |
| Each of the 19 geometry arrays modified in place after `writeable=True` | INVALID_INPUT, and COMPLETE again once restored |
| **Deep tamper**: the `bessel` entry swapped through the MappingProxyType's underlying dict (via `gc`) | INVALID_INPUT (digest), COMPLETE once restored |
| Forged plain-dict copies of kind, module_version, task, convention, modes, wave_sha, provenance, counts, controls, provider or a missing array | INVALID_INPUT |
| Unchanged plain-dict copy | COMPLETE |
| Module CONVENTION changed after preparation | evaluate gives INVALID_INPUT and the adapter bind is refused; COMPLETE once restored |
| Item assignment on the proxy | TypeError |
| Array write | ValueError |

**No rho-dependent cache (C09)**

- A/B/A source refresh is bitwise for m = 1..6.
- B on the reused geometry is bitwise equal to B on a fresh geometry built with other chunks.
- Geometry array bytes and module globals are unchanged afterwards.

**Limits checked before allocation (C10, plus root-shaped run)**

- I derived the five entry formulas from my own bitwise group counts. Each limit is accepted at its exact value. At value − 1 it gives FAILED_CLOSED at `cache_limit`, with zero provider calls and every cache `None`.
- The realized E, J and angular sizes equal the formulas.
- The evaluation wave block is COMPLETE at the limit and FAILED_CLOSED at `block_limit` one above it.
- In a large case (q 150000, nz 99), tiny limits gave a traced peak of 9.8 MB against a would-be E of 237.6 MB.
- In the root-shaped case:
  - A tiny-limit probe returned the group counts after 0.05 s with no provider call.
  - Realized geometry bytes equal the scaling figure exactly (104.9 MB).
  - The traced prepare peak was 117.6 MB.
  - The traced evaluation extra peak was 30.2 MB, within the claimed 24.0 MB of work plus 9.0 MB of validation copies.
  - The provider was called 0 times during evaluation.
  - Grouped vs pinned 0445 on 48 waves × m in {1, 4, 6}: 2.0e-17 norm.

**Floating point (C11)**

| Case | Result |
|---|---|
| w·ρ overflow under `raise` | FAILED_CLOSED at `source_weighting` (FloatingPointError) |
| Same overflow under `ignore` | FAILED_CLOSED (`_FailClosed`), via the finiteness check |
| Overflow inside the scatter (einsum raises no flag) | FAILED_CLOSED at `scatter`; 1 of 6 R groups retained |
| `warn` | the RuntimeWarning reaches the caller, so nothing is suppressed |
| Warnings set to errors | FAILED_CLOSED |
| Prefactor overflow | FAILED_CLOSED at `prefactor`; 2 committed chunks retained exactly, other rows NaN |
| k_z·z overflow at prepare under `raise` or `ignore` | FAILED_CLOSED at `vertical_phase`, with partial caches retained |
| Normal case under `raise` | COMPLETE and bitwise equal |

**Interrupts (C12)**

Each case re-raised the interrupt with `unt0458_retained_result`, status INTERRUPTED and `complete` False:

| Injection point | Retained state |
|---|---|
| Scatter | R-group mask partial |
| Cell sum | cell mask partial |
| Gather | 10 waves committed, bitwise equal to the COMPLETE values |
| Gather, with SystemExit | 5 waves committed, bitwise equal to the COMPLETE values |
| Adapter | `unt0445_retained_result` is the same object |
| Prepare (provider interrupt on call 3) | INTERRUPTED at `bessel_provider`, with 4 Bessel rows retained |

- The geometry can be reused afterwards.
- End to end in the **actual 0452 code**: an interrupt inside mode 3 gave a 0452 INTERRUPTED record whose retained mode-3 entry is the 0458 record itself, while modes 1 and 2 stayed COMPLETE.

**Statuses (C15)**

- 13 malformed `evaluate_mode` inputs give INVALID_INPUT at `validation`, matching 0445 status for status.
- 13 malformed `prepare_geometry` inputs give INVALID_INPUT with zero provider calls.
- Bad adapter binds (None, `{}`, a list, a prepare result) are refused.
- COMPLETE keys are a superset of 0445's: `counts.waves`, `counts.mode` and `counts.positions` are equal, the mask is all True, and the output is complex128 (nk,).

**Inputs, I/O and import (C03, C14)**

- Inputs are unmutated in bytes, dtype and flags, including F-order, read-only and complex64 inputs.
- The geometry shares no memory with the inputs.
- The provider's non-counter metadata is unchanged.
- The audit hook recorded zero file or OS events during evaluate, the adapter, a failure path and prepare.
- Import in a subprocess with an audit hook produced only `exec`. Globals are only functions, classes, strings, a tuple, the MappingProxyType and modules; there are no arrays.

**Lane (C02, by AST)**

- No `@`, dot, matmul, vdot, inner, tensordot, outer or linalg.
- Exactly 2 `np.einsum` calls (L827 and L855), both `optimize=False`.
- No errstate, seterr or warnings control.
- No open, eval, exec or print.
- Imports are hashlib, math, numbers, time, collections.abc, types and numpy only.
- The top level contains only definitions.
- Every public function, and the adapter callable, is keyword-only with no defaults.
- No `.real` or `.imag`.

**Adapter (C04, C13)**

- `inspect.signature` of `density_fourier` equals that of 0445 (names, order, kinds, no defaults). `evaluate_mode` takes `geometry` followed by the 0445 keywords.
- Inside the **actual 0452 code**, with a reviewer stub line that stops the run at `line_prepare` after Steps 1 and 2:
  - The adapter run and the pinned-0445 run reach the same status, stage and `all_modes_complete=True`.
  - Per-mode deltaJ0 agree to 2.5e-16 norm, and the total to 3.3e-16 relative.
  - With mode 6 unbound, 0452 returns INVALID_INPUT at `density_fourier_validation`.
- Inside the actual 0449 code (m = 2), deltaJ0 matches the 0445 run to 3.6e-16 relative to max |deltaJ0|.

**INTERFACE accuracy (C16, C18)**

- The documented key sets for the prepare result, evaluate result, geometry, counts and provenance equal the installed ones exactly.
- The constants hold, and the equation is verbatim from 0445.
- The text includes FROZEN API v001, "not a performance promise", the UNTESTED-at-root-scale limitation and a Limitations section.
- The `scaling()` entry formulas equal my independent counts. The public `scaling()` equals prepare's plan and returns INVALID_INPUT for a non-positive argument.

## Blocking issues

None.

## Notes (non-blocking; recommended for a c2v002 or an erratum)

1. **Interrupt during COMPLETE packaging loses the record.**
   - Where: `return finish('COMPLETE', None)` at L901 is outside the guarded block. `finish` (L756–786) then sha256-hashes the output at L776. The same pattern is at prepare L635.
   - Probe: a KeyboardInterrupt injected at L776 propagated with no `unt0458_retained_result`. An interrupt during validation, by contrast, does carry an INTERRUPTED record (L713–721).
   - This mirrors pinned 0445 L294, which 0449/0452 also mirror. The extra work in the window is hashing nk·16 bytes (36,864 B at nk = 2304), which takes microseconds.
   - Suggested fix: compute `result_sha256` inside the try block, or wrap the COMPLETE packaging in the same BaseException handler.
2. **The per-evaluation hashed-bytes formula is understated.**
   - Where: INTERFACE "Operations" (sha256 bullet), and `scaling()['operations']['evaluate_per_mode']['digest_bytes_hashed']` (L350–351). Both omit the rho digest (L681, 16·nq bytes) and the result digest (L776, 16·nk bytes).
   - Measured: 7,806,422 bytes hashed against 7,474,936 claimed. The gap of 331,486 is 16·nq + 16·nk = 326,400, plus header text.
   - Impact at root nq: about 6 MB per evaluation, which is negligible beside E.
   - Byte columns for transient blocks are lower bounds. For example, the provider-check temporaries `np.abs` and `isfinite` add about 10 B per element. The *enforced* entry counts are exact.
3. **Provider custody is identity only.**
   - Evaluation checks the provider by object identity (`is`), and prepare records a static metadata snapshot. The module does no I/O, so it cannot check the provider's file bytes; root must load the pinned provider (`9ec3f1c9…`).
   - The geometry digest does not cover the `provider_bessel_jn` object. This does not affect results, because evaluation never calls it (J is cached; 0 calls observed).
   - Digests are custody checks, not authentication, as the INTERFACE states.
4. **Every evaluation re-hashes the full cache.** In the root-shaped synthetic case (E = 95.6 MB) the 6-mode evaluation took 0.41 s (indicative, not a promise). Real cost scales with root's actual nz.
5. **Read-only output.** `deltaJ0_J` is read-only on COMPLETE, whereas 0445's is writeable. Both 0449 and 0452 copy it first, which I confirmed in their actual code.
6. **Floating-point exception set differs from 0445.** Under caller `errstate(all='raise')`, a different set of operations can raise than in 0445: w·ρ at `source_weighting`, and the gather products. Overflow inside einsum surfaces as `_FailClosed`, not FloatingPointError. Both outcomes are fail-closed, and this is documented (INTERFACE difference 5).
7. **Root must size `max_block_entries` for the consumers' wave_chunk.** With the adapter, the `wave_chunk` that 0449/0452 pass must be ≤ the `max_block_entries` set at prepare. Otherwise the call is FAILED_CLOSED at `block_limit`, which is documented and safe.
8. **Geometry-level faults fail the whole prepare.** 0445 would have kept earlier wave chunks; this is documented and fail-closed.
9. **Mutation summary miscount.** The fixture mutation summary reads "killed 40 / applied 40 (listed 41)", so one listed mutant was not applied. This does not affect the verdict.
