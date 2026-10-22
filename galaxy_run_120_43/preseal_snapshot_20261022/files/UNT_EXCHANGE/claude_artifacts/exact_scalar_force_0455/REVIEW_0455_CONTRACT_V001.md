# REVIEW 0455 CONTRACT V001: contract, cache and convention lens

Role: distinct reviewer, not author. I wrote neither the module, the INTERFACE nor the fixtures. I did not read the concurrent exactness reviewer's output.
Date: 2026-10-16.

## Verdict

**PASS_WITH_NOTES.** There are no blocking issues. The module meets the 0455 contract on cache and identity safety, fail-closed statuses with retention, limits checked before allocation, FloatingPointError handling, lane convention, the no-Hessian statement and the 0449 LINEAR convention. The notes below are wording and usability points only. None of them changes a result.

## Hashes (sha256, computed from bytes)

| File | sha256 | Pin |
|---|---|---|
| Task 0455 `FROM_CODEX/0455_2026-10-16_claude2_exact_scalar_force_acceleration.md` | `b467a0c0c6e2fe3498a44ebdecca110776528dde7b4304d204cd42e64c67062c` | matches |
| Line module `owned_fixed_xy_fourier_line_v002.py` (read-only) | `3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18` | matches |
| 0449 `nonzero_cached_feedback_c2v001.py` (read-only) | `1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95` | matches, unchanged at end of review |
| Module `exact_scalar_force_c2v001.py` | `0dab62be91cfd793949ef251aa3e731b4544e7131606599784762cb4101175ea` | equals author report |
| `INTERFACE_0455_V001.md` | `c5b00a771adbca4b9748e4e0405a98c6737cafc8a0aca80358d5b4c11b855dff` | equals author report |
| `fixtures_0455_c2v001.py` | `d1b28438273fab010ef4b3e28e07d1047f86916c9e0541ea5d232903e59b917e` | equals fixture report |
| Fixture author's result JSON | `a8092c74387e4cf07ed990182d507dea9499cd2240aae8b1a21637f581363603` | equals fixture report |

The author's scratch copy `r0455/author/exact_scalar_force_c2v001.py` is byte-identical to the delivered module.

## What was executed

All runs used the root interpreter `-I -B` with `VECLIB/OPENBLAS/OMP/MKL_NUM_THREADS=1` (numpy 2.3.5, Python 3.12.14) on synthetic inputs only. No .npz file, project data or root worker was read, loaded or imported.

Scratch directory: `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0455/REVIEW_0455_CONTRACT_V001/`

1. **Fixture script, re-run independently** (log `fixture_run.log`, sha256 `187693df7e4e9bbaa449c8f1fdbc46cf8d1ee7e7b056f3677f41887c088423b6`):
   - BINDING 40/40 PASS, ADVISORY 7/7 PASS.
   - My result JSON (`e6236807dbfab5d5338a4d5cc89c04a8d57aa9147d12127aa6dc05a93c9518c9`) differs from the fixture author's only in timing fields. Every verdict and every non-timing detail is identical.
2. **`spot_contract.py`** (`97b095881ffd1defd889e7713c3e49009cfd6a129d42675e83e270523900bf16`, log `182a04db35c37e041fd7648f4c0b97955ebbb91d75a1aa5555ceb7fc9ba26224`). 35 checks, 33 PASS. The 2 FAILs were my own mis-designed inputs, which never triggered an overflow (L·grad and the amplitude sums stayed below the float64 limit). Both were re-done correctly in item 3. They are not module defects.
   - Independent direct-sum oracle on a 2-D point shape with exact duplicates, signed zeros, holes and nonuniform z per column: field 5.5e-17, gradient 1.4e-16 (relative to Σ|a|).
   - A, B, A amplitude sequence on one geometry: A reproduced bitwise and B matches the direct sum. The dense stack is a distinct object each call, and the retained amplitudes do not alias the caller buffer.
   - Mutating the amplitude buffer in place between calls refreshes the result. An earlier result is unchanged by later mutation.
   - Rejected as INVALID_INPUT:
     - point +1e-9;
     - the same values in a different shape;
     - float32-rounded waves;
     - reordered waves;
     - -0.0 vs 0.0 in a wave (`spot_pickle.py`).
   - Tampering with each of 10 geometry arrays, after re-enabling `writeable` on the owner, gives INVALID_INPUT through the digest. Assigning to the geometry mapping raises TypeError.
   - Rejected as INVALID_INPUT by `admit_scalar_force`:
     - a tampered bound base;
     - a finite sum on P(+1 ulp) paired with a base on P;
     - a finite-sum dn mutated through its owning array.
   - deltaPhi and its gradient against an independent linear quotient at c = 2.9e8: 2.9e-16 and 7.2e-16. Complex dn and grad_dn are retained, and `hessian` is a "NONE" string with no Hessian arrays.
   - Caller arrays are unmutated and stay writeable.
   - **Memory.** An irregular 200,000-wave set (dense 4e10) is rejected at `dense_limit` with a traced peak of 19.4 MB, which is only the O(nk) grouping. A point-block overflow is rejected at `block_limit` during prepare.
   - **Synthetic signed 72³ lattice, permuted, at the suggested limits** (`max_dense_entries=373248`, `max_block_entries=82944`, `column_chunk=16`, `point_chunk=1152`):
     - grouping 5184 × 72;
     - direct-sum agreement 4.5e-18 / 1.0e-17;
     - prepare 0.066 s, evaluation 1.18 ms per column (32 columns × 8 z);
     - whole-call traced peak 42.5 MB.
     The op tallies equal exactly 3·373,248 MAC and 5,184 exps per column, and 72 exps plus 288 MAC per point, as the INTERFACE states.
   - **Interrupt.** A KeyboardInterrupt injected by SIGALRM mid-evaluation is re-raised with `exc.unt0455_retained_result`: status INTERRUPTED, stage `collapse`, 192 points filled and the rest NaN.
   - The public API is keyword-only with no defaults, and a positional call raises TypeError.
   - **AST lane scan:**
     - no `@`, `dot`, `matmul`, `vdot`, `inner` or `tensordot`;
     - no I/O, `print`, `seterr`, `errstate` or `warnings` use;
     - both einsum calls pass `optimize=False`;
     - imports are numpy plus stdlib (hashlib, math, numbers, collections, types);
     - the top level holds definitions only, and its only calls are `MappingProxyType` and `dict`.
3. **`spot_fpe.py`** (`8040c2dea01586be920024995a8f54c7c3eb18501955ab6ddf1e3de9030de2bb`, log `847d5d56c150bde497fd19e633cf1433c9b5144686ca47e21e9f1d48cb7acc4a`):
   - **Overflow inside the collapse einsum.**
     - `errstate(raise)`: FAILED_CLOSED at `collapse` with FloatingPointError, raised by the next ufunc. Retained: amplitudes, dense stack, masks, and NaN-filled dn and grad.
     - `ignore` / `warn`: FAILED_CLOSED at `collapse` via the explicit finite check. The warning is not suppressed.
   - **L·grad overflow in admission.** Under `raise`: FAILED_CLOSED at `admission:reality` with FloatingPointError, and dn_complex and grad_dn_complex retained. Under `ignore`: FAILED_CLOSED through the nonfinite reality report.
4. **`spot_pickle.py`** (`7c302c1d4859ec55015c125105d059b1ac0c8502071a94d9ab9f9f66e9d61bc8`, log `c0f61ae385b52a2e8e2b28c3ae2964cf02cb1a91c2371100d8cdb9f1747aa487`): probes for pickling, prepare-failure retention, numpy-int limits and the signed-zero identity (see notes 3, 7 and 8).

## Contract findings (all satisfied)

- **Finite equation.** `dn = Σ a_k e^{ik·x}` and `grad = Σ (ik) a_k e^{ik·x}`:
  - Amplitudes are used as supplied. There is no `.real` before admission (`.real` appears only at lines 269 and 593–596), and no weight, factor 2, c², reflection or mode removal.
  - The regrouping is the dispatch's: dense S[kz, pair] by `np.add.at`, `C = E·S`, `Cx` and `Cy` from `(1j kx/ky)S`, `Cz = C·(1j kz)`, and exact per-point vertical phases.
  - The phase split `(kx x + ky y)` then `kz z` matches the read-only line module.
- **Cache and identity.**
  - Geometry holds read-only float64 copies and is covered by a digest recomputed on every call (lines 215–225).
  - Waves and points must be byte-identical as float64 (lines 228–236).
  - The base is bound to the points' sha256 (lines 366–381). It is checked against the geometry (lines 675–678) and against the finite-sum identity (lines 643–646).
  - The finite-sum result is integrity-hashed and rechecked at admission (line 549).
  - Amplitudes, S and the collapsed lines are rebuilt on every call (lines 434–468). Nothing source-dependent is cached.
- **Admission order** is reality (four checks, gradients scaled by L), then `Nb = 1 + Re n_b > 0`, then the LINEAR forms. Lines 597, 609 and 610 match the 0449 module's lines 402, 416 and 417 character for character. The 0455-required L-scaling of gradient reality is an intended addition to 0449's unscaled check.
- **Limits** are checked at prepare (lines 320–344), before the dense stack or any block is allocated.
- **Statuses.** INVALID_INPUT, FAILED_CLOSED (with `retained`), COMPLETE, and an INTERRUPTED result attached to a re-raised BaseException.
- **Hessian.** None is evaluated, and the `HESSIAN` string says so.
- **INTERFACE accuracy.** The signatures, grouping algorithm, identity guards, admission line numbers (581–610, 597, 609, 610), op counts and per-buffer byte formulas match the code. The no-actual-data statement is present.

## Blocking issues

None.

## Notes (non-blocking)

1. **einsum ignores `errstate`.** This is a numpy property: an overflow inside either einsum produces inf/nan silently. The module still fails closed, through the explicit `isfinite` checks after the collapse (line 466) and the vertical read (line 487), or through the next ufunc's FloatingPointError. I verified this. The INTERFACE could say that einsum overflow is caught by the finite checks rather than by FloatingPointError.
2. **"All four checks are evaluated and reported"** (INTERFACE, admission rule 1) does not hold under a caller `errstate(all='raise')`. A FloatingPointError inside one reality check, for example L·grad overflow, aborts the remaining checks, so only `base_fields` was reported in my test. The status is still FAILED_CLOSED with retention.
3. **prepare failures.** `prepare_geometry` returns FAILED_CLOSED with `retained=None`, and only `counts` is reported. That is appropriate because nothing source-dependent exists yet, but the INTERFACE's general sentence that `retained` holds the partial work does not apply to prepare.
4. **Retained memory.** Each COMPLETE finite-sum result keeps the full dense stack (48·n_kz·n_pairs B, about 17.9 MB at 72³) plus the last collapsed block in `retained`. A coupled solver that keeps every iteration's result holds that memory. The INTERFACE describes the peak but not this retention lifetime.
5. **Suggested limits.** The 72³ suggestion (`column_chunk=16`, `max_block_entries>=82,944`) implicitly needs `point_chunk <= 1152`, because pb·72 must be ≤ the limit. A larger `point_chunk` fails closed at prepare, which is safe.
6. **Traced peak.** The INTERFACE's "traced peak 27 MB" has no stated scope. My whole-call peak, prepare plus evaluation with identity re-hashing, was 42.5 MB. Timing agrees: about 1.2 ms per column.
7. **Not picklable.** The geometry and base records are `MappingProxyType`, so they cannot be pickled or deep-copied (TypeError, which is loud). Multiprocess use must prepare per process.
8. **Limit types.** Limits must be Python `int`. A numpy integer gives INVALID_INPUT, which fails closed, but the INTERFACE does not mention it.
9. **Repeated hashing.** `exact_scalar_force` re-hashes the geometry, waves, points and base in both the wrapper and the inner calls. This is O(nk + points) per call, negligible against column evaluation, and not a correctness issue.
10. **Fixture temp directory (fixture, not module).** T19 creates a transient, empty, auto-removed `tempfile.TemporaryDirectory()` under the system TMPDIR (`/var/folders/...`) rather than the assigned r0455 scratch. This is a minor deviation from the scratch policy.
11. **Project tree.** No 0455 Claude scratch script references the project tree. Root-named drafts `owned_exact_scalar_force0455_comparison_{root,monitor}_DRAFT_v00{1,2}.py` exist under `helpers/recovered_packet_audit/`, with mtimes 15:25 and 15:34. Their `owned_` prefix is root's naming, and I did not read them. Nothing from this lane was found written there.
12. **0449 and 0452.** The 0449 module hash is unchanged. The 0452 directory was not modified by me; it is owned by a concurrent task.

## Files written by this reviewer

- This file, created exclusively with noclobber.
- Scratch files only under `r0455/REVIEW_0455_CONTRACT_V001/`: `spot_contract.py`, `spot_fpe.py`, `spot_pickle.py`, their logs, `fixture_run.log` and `fixture_run/`.
