# DELTA 0424: optional supplied fixed source in the resumable gas solve (FIXEDSRC V001)

- **Role:** implementation author for UNT 0424 (Claude2 lane, local helper). The distinct review is a separate helper's job and is not included here.
- **Date:** 2026-10-16.
- **Status:** code plus NONPHYSICAL contract tests only. There was no scientific execution. The driver was neither imported nor run. No physical module, DDO154/NGC3198 data, physical parameter, target velocity, fit, cloud resource, network access, install or retry was used. `/Users/bgm/Research/Universal Network Theory` was only read. Root keeps the grid, the physics, launch and acceptance.
- **Scope:** one optional argument plus checkpoint identity. Equations, the exact finite Fourier reduction, source and EH sign, vertical profile, gas boundary, parameters, force balance, search limits, the relaxation statement, the gas iterate and the updated-gas transform are all unchanged. No preparer or adaptor was written, and no ring-average source module was introduced.

## 1. Binding inputs (sha256 recomputed from bytes; all matched before work)

| input | sha256 |
|---|---|
| FROM_CODEX/0424_2026-10-16_analytic_fixed_source_interface.md (read fully) | 0acba7bc41ecb9dd44d22e92f31fc199bd9b52b76b7f570d0fdb3452ca663e5d |
| FROM_CODEX/0422_2026-10-16_claude2_resumable_coupled_gas_execution.md (parent) | 7dfe9050c1bb83b0744882e7fce5e2d887bb566c6c744291fd711150d0c9eb11 |
| base solver `coupled_hi_fourier_source_iteration_v005_resume_c2v001.py` (reviewed; unchanged) | c91c5051ad7fea477a51dc9fbdaae2cdc755cc8186a318aa27627cf9d21651e6 |
| base checkpoint `coupled_gas_checkpoint_c2v002.py` (reviewed; unchanged) | 0bb955ed86c6e71884152c1dd97c41e2d086a4cd2e135f78e9b2716d2e4803c1 |
| driver `ddo12_coupled_trial_root_driver_v009_resume_c2v003.py` (reviewed; unchanged; not imported) | 7a45a970807e15e880b2d25b5ea3bcda28f8419611adc8abbaf4f1f50a2698a1 |
| root original `helpers/recovered_packet_audit/coupled_hi_fourier_source_iteration_v005.py` (reference) | d35c55bdd588f80661b568629482cbe54b50b5e0626dc0e370cd9a63f278188f |
| DELTA_0422_RESUME_V001.md | 36a8702a426e3de9bf206ca636faa7b258b4a160d935918ebb5f3b4fe66aa23a |
| FIX_DELTA_0422_RESUME_V002.md | aae6988d5b9e23619c1837384d24f02beac3be0397576576f077eb3b6d2c6102 |
| REVIEW_0422_RESUME_EQUIVALENCE_V001.md | bd16fce7c9c6e2470475c42967118346fadbe253a87ea2496bb68648db4819a5 |
| REVIEW_0422_RESUME_IDENTITY_IO_V001.md | 0cc91ad6092377e25a08df14d9277653ebdb762ded78e319262c8a494a40830b |

Three further files were read, read-only, to confirm the caller's dtype and calling convention. They are not modified, and no adaptor was written.

| file (under `UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/`) | sha256 | what was checked |
|---|---|---|
| coefficient_method/owned_composite_prepared_coupled_gas_adapter_v001.py | 75092cf64cf5293d9e1a5b28b2c909d875c1f5a1b3e9d185f71f065ccff49ec3 | It requires the `fixed_source_fourier_J` parameter in the solver signature. It passes the caller's checkpoint dict through, with `caller_identity.composite_source_binding` added |
| coefficient_method/ddo_actual_initial_source_preparation_v007.py | ac905597b1aa06da3a0178bfa629f6256b78cc87e8b1b05fcea22b3f6df25a42 | It returns `fixed_source_fourier_J` from the analytic module, plus `fixed_positions_m` and `fixed_integrated_columns_J` as arrays |
| recovered_packet_audit/axisymmetric_initial_rest_energy_fourier_v001.py | f5670726e75b6854fb8d55c2ffe6423251bb31193e5d13b087e46b8185984756 | Its output is `np.zeros((len(k),10,1),dtype=complex)`: native complex128, C order, matching the validation below |

## 2. Created files (exclusive create; sha256 from bytes)

Directory: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/`

| file | sha256 | lines | base |
|---|---|---|---|
| `coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py` | 44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644 | 245 | solver c2v001, 212 lines |
| `coupled_gas_checkpoint_c2v003.py` | 069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114 | 606 | checkpoint c2v002, 587 lines |
| `DELTA_0424_FIXEDSRC_V001.md` (this file) | reported in the return message, not self-referenced | | |

Every reviewed 0422 file is unchanged. After publication, all eight .py files in the directory were re-hashed, and the six pre-existing ones match their pins: the c2v001 and c2v002 checkpoints, the c2v001 solver, and drivers c2v001, c2v002 and c2v003. The return message reports the 0422 deliverable's status separately.

**The checkpoint module changed (successor c2v003).** The reason: c2v002's `_identity` builds a fixed set of fields, and none of them can carry the fixed-term selection. The only place that would accept an extra key is `controls`, which would misfile a source-path input as a numerical control. So the reviewed c2v002 is not reused for the supplied path. Its record format, codec, publication, scan, chain and resume logic are carried over byte-for-byte; only the identity content changed (§5).

## 3. API

```python
solve(*, fixed_positions_m, fixed_integrated_columns_J, initial_gas_fourier_J, gas_columns,
      fourier_arguments, boundary_jet_at_positions, source_module, fourier_module, metric_module,
      hi_module, quadrature_module, c_m_s, max_iterations, relaxation, source_atol_J, source_rtol,
      reality_atol, reality_rtol, vertical_fourier_module=None, progress_callback=None,
      checkpoint=None, fixed_source_fourier_J=None)
```

**Omitted (`fixed_source_fourier_J=None`, the default).** The fixed term is `np.asarray(source_module.physical_source_fourier(fixed_positions_m, fixed_integrated_columns_J, k_physical), dtype=complex)`, the same two statements as the base. Everything else executes the base statements in the base order. The result dict is the base dict. The progress events are the base events. The only change is the checkpoint `inputs` dict passed to `open_run`, which gains the key `fixed_source_fourier_J=None` (§5).

**Supplied.**
- **Validation** happens before any module call, file write or checkpoint open. A violation raises `ValueError('fixed_source_fourier_J: ...')`. The value must satisfy:
  - `type(value) is np.ndarray`. Lists, masked arrays and other subclasses are rejected.
  - `value.dtype == np.dtype(complex)`, meaning native complex128. complex64, big-endian `>c16`, float, object and other dtypes are rejected rather than converted.
  - `value.shape == (len(fourier_arguments['k_physical']), 10, 1)` exactly.
  - Every entry is finite (real and imaginary parts).
- **Fixed term.** The fixed term is a private copy, `np.array(value, dtype=complex, order='C', copy=True)`. The caller's array is never written, and later caller mutation cannot reach the solve. The angular stellar quadrature is **not** re-evaluated, and `source_module` is **not** called for the fixed term.
- **Provenance.** `fixed_positions_m` and `fixed_integrated_columns_J` stay required keywords. They are accepted unmodified and are not used to compute anything. With a checkpoint they are digested into identity (§5).
- **Gas is unchanged:** `gas` starts at `initial_gas_fourier_J` and `current=fixed+gas`. Every `updated` is `source_module.physical_source_fourier` of the actual phi-dependent solved columns. Relaxation is `(1-relaxation)*gas+relaxation*updated`. The supplied term is never added to the gas iterate, so relaxation cannot remove it.
- **Result.** Every returned dict (converged, budget exhausted, or column failure) gains exactly one key: `fixed_source_selection = {'selection': 'SUPPLIED_FIXED_SOURCE_FOURIER_J', 'fixed_positions_and_integrated_columns': 'PROVENANCE_ONLY; accepted unchanged, not used for the fixed term'}`. It holds no arrays.
- **Checkpoint handshake.** A supplied term with `checkpoint` requires the module to declare `FIXED_SOURCE_SELECTION_IDENTITY = True`; `coupled_gas_checkpoint_c2v003` does. Otherwise the solver raises `RuntimeError('CHECKPOINT_MODULE_LACKS_FIXED_SOURCE_SELECTION_IDENTITY; nothing written')` before `open_run`, and nothing is created.

**Module pairing.**

| solver | checkpoint module | result |
|---|---|---|
| fixedsrc | c2v003 | supported for both paths. Identity records EVALUATED or SUPPLIED |
| fixedsrc | c2v002 | omitted path works exactly as with the base solver. Identity has no `fixed_source` section, but it still differs from any c2v003 or base-solver identity through the code pins. Supplied path: RuntimeError, nothing written |
| base c2v001 | c2v003 | `CheckpointError('FIXED_SOURCE_SELECTION_INPUT_REQUIRED; ...')` before anything is written |

## 4. Changed lines (new-file line numbers; full `diff -u` in Appendices A and B)

**Solver (212 to 245 lines).**
- 6-8: module docstring.
- 20-29: new `_supplied_fixed_source(value, wave_count)`: validation plus private C-order copy.
- 37: the signature gains `fixed_source_fourier_J=None`, keyword-only, last.
- 56-63: function docstring.
- 72-77: the fixed-term selection. Lines 73-74 are the base statements, re-indented and otherwise unchanged. Line 77 is the supplied branch.
- 86-87: checkpoint handshake guard. It runs only when the term is supplied and a checkpoint is given.
- 92: the `open_run` inputs gain `fixed_source_fourier_J=fixed_source_fourier_J`, which is the caller's original object or None.
- 105-107: `_finish` adds the `fixed_source_selection` key, only when the term is supplied.
- Not touched: `current=fixed+gas`, prepare, the line cache and metric callback, the column loop and HI call, restore and write, the source accumulation, `updated`, residual, bound, history, the relaxation statement, and every return dict body.

**Checkpoint (587 to 606 lines).**
- 1-11: module docstring.
- 48: `FIXED_SOURCE_SELECTION_IDENTITY=True`.
- 288-300: `_identity` requires the `fixed_source_fourier_J` input key and builds `fixed_source`. For a supplied term it first requires `type(supplied) is np.ndarray and digest(supplied)==digest(fixed)`; otherwise it raises `SUPPLIED_FIXED_SOURCE_IS_NOT_THE_FIXED_TERM`.
- 302: the identity dict gains `'fixed_source':fixed_source`.
- Unchanged: `FORMAT` (`UNT_0422_COUPLED_GAS_CHECKPOINT_C2V001`), the codec, digest, publication, blobs, lock, `_scan`, `_resume_point`, `open_run`, `begin_iteration`, `write_column`, `complete_iteration` and `finish`. Record layout and file names are unchanged.

## 5. Checkpoint identity fields

Added in IDENTITY.json. Any difference causes `IDENTITY_MISMATCH ... differing: identity.<path>`, and the saved columns are not read.

```
identity.fixed_source.selection                                   'SUPPLIED' | 'EVALUATED'
identity.fixed_source.fixed_positions_and_integrated_columns      'PROVENANCE_ONLY' | 'FIXED_TERM_INPUT'
identity.fixed_source.supplied_fixed_source_fourier_J             None (evaluated) or:
    .array_sha256   typed sha256 of the supplied array as given
    .dtype          '<c16'
    .shape          [nk,10,1]
```

The `array_sha256` hash is the module's existing canonical typed digest: `sha256( b'A' || u64le(len(dtype.str)) || dtype.str || u64le(ndim) || u64le(shape_i)... || C-order bytes )`. It therefore binds the exact bytes, dtype and shape. Memory order is deliberately excluded: a Fortran-ordered array with identical values hashes identically.

Kept, with their roles:
- `identity.inputs_sha256.fixed_source_fourier_J`: the typed digest of the fixed term actually in use. When supplied, it equals `array_sha256`.
- `identity.inputs_sha256.fixed_positions_m` and `.fixed_integrated_columns_J`: the original fixed positions and columns. When supplied, they are provenance.
- Code pins for the solver (now the fixedsrc file) and the checkpoint (now c2v003), plus all other fields as in 0422.

**Arrays preserved (unchanged mechanism).** Each `iteration_NNNN/START.json` stores content-addressed blobs of the actual `gas_fourier_J`, `current_source_fourier_J` and `fixed_source_fourier_J`. When supplied, the fixed blob is the supplied array, bitwise. Each COMPLETED stores the actual `updated_gas_fourier_J`. On resume, c2v002's unchanged checks still run:
- START fixed equals the identity's fixed-term digest;
- current equals fixed+gas bitwise;
- START(0) gas equals the initial gas;
- every later gas iterate is exactly one relaxation;
- the resumed iteration's gas, current, fixed and prepared response match bitwise.

**Resume rejects any changed input** (nonphysical tests R1-R7), and the checkpoint tree stays byte-identical:

| change at resume | rejected by |
|---|---|
| one ulp in the supplied array | `fixed_source.supplied_fixed_source_fourier_J.array_sha256` |
| argument omitted on a supplied checkpoint | `fixed_source.selection` |
| a bitwise-equal array supplied on an evaluated checkpoint | `fixed_source.selection` |
| changed fixed positions or columns (provenance) | `inputs_sha256.fixed_positions_m` or `inputs_sha256.fixed_integrated_columns_J` |
| a different supplied array | `inputs_sha256.fixed_source_fourier_J` |
| a dtype change (for example complex64) | solver validation (ValueError), before the checkpoint is opened |

## 6. Why the omitted path matches the base

With `fixed_source_fourier_J=None`:
- the `if` branch executes the base's two fixed-term statements unchanged;
- the handshake guard and the `_finish` marker are skipped;
- no new statement touches `fixed`, `gas`, `current`, `prepared`, the columns, `updated`, the residual, the bound, the history or the relaxation.

The signature only adds a trailing keyword with a default, so every base call is still valid. The result dict and the progress events are the base's. The only differences are in checkpoint metadata:
1. the solver code pin is the new file;
2. `inputs` carries `fixed_source_fourier_J=None`, which c2v002 ignores and c2v003 records as `EVALUATED`.

Evidence (nonphysical, toy):
- The verbatim 0422 restart-contract suite runs on the new pair with 97/97 PASS. It covers enabled versus disabled, interrupts and resume at seven points plus double interruption, convergence, the failure path, integrity, identity and the forged relaxation chain.
- In the 0424 suite, P1 and C1 pass, and P2/P13 show that a supplied array bitwise equal to the evaluated term gives the identical result and failure digests as the omitted path, on both line paths.

The base solver was not imported, per the test policy; the comparison against the base is the diff in Appendix A.

## 7. Root usage (no launch performed here)

- The fixedsrc solver is the solver to bind for the analytic fixed source, and with a checkpoint the module must be `coupled_gas_checkpoint_c2v003.py`. Codex1's existing adapter (`owned_composite_prepared_coupled_gas_adapter_v001.py`) already passes `fixed_source_fourier_J`, the original positions and columns, and the caller's checkpoint dict. Root sets `module` in that dict to c2v003 and pins both new files. No adaptor was written here.
- The reviewed driver `..._resume_c2v003.py` is unchanged and still loads the base solver and checkpoint c2v002. It does not pass `fixed_source_fourier_J`.
- Checkpoints made with the base solver, or with c2v002, cannot be resumed by the new pair. The code pins differ and the identity schema gained `fixed_source`, so they are rejected with IDENTITY_MISMATCH, never reused.

## 8. NONPHYSICAL contract tests (not scientific execution)

**These are not scientific execution.** Synthetic toy stubs, verbatim copies of the 0422 stubs, replace every source, Fourier, line, metric, HI-column and quadrature module. The column solve is the toy HI stub. The tests import only the new checkpoint c2v003 and the new fixedsrc solver: no driver, no base copy, no physical module, data or parameter. Each script carries its own `signal.alarm` (180 s and 240 s), and each completed in well under a minute.

- Interpreter: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (Python 3.12.14, numpy 2.3.5).
- Scratch directory: `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0424/`.
- Both suites ran against the delivered bytes: checkpoint 069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114 and solver 44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644.

| artifact | sha256 | result |
|---|---|---|
| tests/test_fixedsrc_contract_0424.py | 6dacbffcfe9dfa0b0d0a6da8bb0b2b6f5783ba1065e268df96def7dc4b0a62d0 | |
| final_0424_tests.txt | 92f74cfe503d89ed65eb231cf6bfb43031ed48ec2ecde17bbeee76631e695a90 | **91 PASS / 0 FAIL** |
| tests/test_restart_contract_0422.py (verbatim 0422 suite) | b6cbc278d45efb6ace0feecd9dd5b06ab3db72dcc1a0262c21ef4efc1c1cc1ff | |
| final_0422_regression_on_new_pair.txt | c3904fbae7389f50d488f719ca0b4f89c082123b8d3f89b9ae9e75ccaba406d6 | **97 PASS / 0 FAIL** |

Stub sha256:

| stub | sha256 |
|---|---|
| toy_source | 8e65c321f03c3e9413fe8c598a5bacfab0a4b23ad2cf5ceff30e709301faa91c |
| toy_fourier | 28974db211700511b31d43341607126eca0f5781a7044685929b010fa5f2ab02 |
| toy_line | b80e4c344657842600dd539547a75798c51cce393654545cf358bd6e9be40023 |
| toy_metric | e780bb7682206662700ae9cf57657f167271664c4023fe35c70df9ec29313fdc |
| toy_quadrature | b0244efe4e969eabaebaa1a9354dc30edecb1ea6a04d8deb6cfa7eede865ef66 |
| toy_hi | e9d31f759f668fbc30a277b178d5cc51f4d59de3b51e1e1ece5bc34418030e2e |
| toy_hi_changed | d255f140b372df14568b3c496068a591223fdf2560f0feaae97159b68371643d |

| group (0424 suite) | what it asserts |
|---|---|
| T0 (1) | the toy supplied arrays are native complex128, C-order, [nk,10,1] |
| V1-V12 (36) | list, complex64, float64, big-endian, three wrong shapes, NaN, inf imaginary part, masked subclass, object dtype and 0-d are each rejected with ValueError. No source, prepare or column call is made, and with a checkpoint nothing is created |
| P1-P13 (17) | omitted path: one fixed evaluation plus one update per iteration, base result keys, no marker. A bitwise-equal supplied term gives the omitted digest on both line paths. Supplied path: the source module is called only for updates. The marker is exact. NaN or inf provenance gives an identical result. Supplied S2 with provenance P1 equals evaluated-from-P2. The caller's array is not mutated, and mutating it mid-solve has no effect (private copy). Fortran order gives an identical result. Iteration-0 current is exactly supplied+initial. Convergence and failure paths are covered |
| C1-C8 (21) | identity `fixed_source` is EVALUATED or SUPPLIED with typed sha256, dtype and shape. Provenance digests are kept. START blobs: fixed is the supplied array, gas0 is the initial gas, current is fixed+gas, each gas is one relaxation. Supplied-mode interrupt and resume at seven points gives the uninterrupted digest, the exact resume point, and no fixed evaluation on resume. Convergence resume is checked, with no new records after convergence. Supplied failure with FAILURE record and resume is checked |
| R1-R9 (9) | the rejections in §5's table, each leaving the tree byte-identical. Controls: an evaluated checkpoint still resumes when the argument is omitted, and a Fortran-order equal array is accepted |
| H1-H7 (7) | a marker-less checkpoint module is refused (RuntimeError, nothing created). Pre-0424 inputs (no key) are rejected. A supplied term that is not the fixed term (different array, list, or complex64 against complex128) is rejected. C and Fortran order give equal identity, and the selection fields alone separate supplied from evaluated. CheckpointError is not a ValueError |

**Mutation check (scratch only; the mutants were never delivered).** Each mutant makes the 0424 suite fail:

| mutant | sha256 | outcome |
|---|---|---|
| m1: ignores the supplied term and always evaluates | 276f732f43c1adf15f2c2948c57d0994a73256797a61d953f29fb679863d7dd0 | 41 FAIL plus the c2v003 guard |
| m2: no private copy | 1b35ec06cb05bd63a59d482fcb94b39309b269b1675ff4ccc6ca598f17139aa4 | P8 FAIL |
| m3: puts the correction into gas, with an evaluated fixed term | 22bd2ea34df48ced534c6b9cd739cabfed876b3d27070a5ead3c9fbcf3cf2cdd | P3/P5/P6/P10 FAIL plus the c2v003 guard `SUPPLIED_FIXED_SOURCE_IS_NOT_THE_FIXED_TERM` |
| m5: folds the supplied term into gas with zero fixed | 256be3557d526967c676e96e78845d36afda19e9a8f76ccde0d80fcd68fe1fdd | P2/P6 FAIL plus the guard |
| m4: checkpoint without the `fixed_source` section | 4372589b05a4f5a7399b9d5e845b045a609489a25727c2fdd4d50d2390161399 | C1/C3/H6/R1/R2/R7 FAIL. R7 shows a bitwise-equal supplied term would otherwise silently resume an evaluated checkpoint |

## 9. Assumptions

1. **Native complex128 is required.** The task says "finite complex numpy array". I read that as the dtype the evaluated path itself produces (`dtype=complex`), and I reject other complex dtypes rather than convert them. Converting complex64 or clongdouble would change the bytes that are hashed, and rounding clongdouble would be lossy. The Codex analytic module returns native complex128.
2. **Shape uses `len(fourier_arguments['k_physical'])`**, which is the same wave array the evaluated path transforms over.
3. **The supplied term is trusted as Root's physics.** Its Hermitian pairing on the signed grid, its units, chart and sign are not checked here; that is the preparer's and Root's responsibility. A non-Hermitian term surfaces downstream as the unchanged `NONREAL_PHYSICAL_METRIC` column failure, never as a projection.
4. **Provenance arrays are opaque.** `fixed_positions_m` and `fixed_integrated_columns_J` are neither validated nor copied, because they are not used. With a checkpoint they must be digest-encodable (numeric ndarray, list, float and so on), as in 0422.
5. Determinism, no hidden module state, and a local filesystem: unchanged from DELTA_0422 §11.

## 10. Limitations

- **The result marker holds no hashes or arrays.** Without a checkpoint, the exact identity of the supplied array and the provenance arrays rests with the caller's custody (the adapter's `binding_custody`). With a checkpoint, IDENTITY.json holds the typed sha256 digests, and the START blobs hold the arrays themselves.
- **Strict pairing.** The supplied path needs c2v003. Old checkpoints are not reusable with the new pair, by design (§7).
- **Test scope.** Only NONPHYSICAL toy restart-contract tests ran. Nothing here exercises the actual analytic preparer, the real grid, memory or overhead, the composite-grid physics, or the V008 column-395 bracket failure.
- All 0422 limitations carry over unchanged: column-boundary granularity, the un-checkpointed post-convergence stage, strict `max_iterations` identity, no aliasing preservation, and no F_FULLFSYNC on macOS.
- **Distinct review is pending.** A separate helper is to review this optional-argument delta and the checkpoint identity.

## Appendix A: `diff -u` base solver c2v001 to `coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py`

```diff
--- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_c2v001.py	2026-10-16 08:31:10.012792435 -0500
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py	2026-10-16 09:22:07.196917795 -0500
@@ -3,6 +3,9 @@
 Uniform physical Cartesian background chart; full metric anisotropy retained.
 RESUME c2v001 (Claude2 0422): optional exact restart at a completed HI-column
 boundary via an injected checkpoint module. checkpoint=None executes v005.
+FIXEDSRC c2v001 (Claude2 0424): optional fixed_source_fourier_J. Omitted (None),
+the fixed term is evaluated exactly as before. Supplied, that validated array is
+the fixed term; fixed positions/columns are kept only as provenance.
 """
 import math
 import numpy as np
@@ -14,12 +17,24 @@
     return a
 
 
+def _supplied_fixed_source(value,wave_count):
+    """Validated private C-order copy of a supplied fixed term. No conversion:
+    a native complex128 ndarray (the evaluated term's dtype) of exact shape
+    [wave_count,10,1] with finite entries is required."""
+    if type(value) is not np.ndarray or value.dtype!=np.dtype(complex):
+        raise ValueError('fixed_source_fourier_J: native complex128 numpy array required; no conversion')
+    if value.shape!=(wave_count,10,1):
+        raise ValueError('fixed_source_fourier_J: exact shape [len(waves),10,1] required')
+    _finite(value,'fixed_source_fourier_J')
+    return np.array(value,dtype=complex,order='C',copy=True)
+
+
 def solve(*, fixed_positions_m, fixed_integrated_columns_J, initial_gas_fourier_J,
           gas_columns, fourier_arguments, boundary_jet_at_positions,
           source_module, fourier_module, metric_module, hi_module, quadrature_module,
           c_m_s, max_iterations, relaxation, source_atol_J, source_rtol,
           reality_atol, reality_rtol, vertical_fourier_module=None, progress_callback=None,
-          checkpoint=None):
+          checkpoint=None, fixed_source_fourier_J=None):
     """Required actual inputs:
     fixed positions[n,3]/J[n,10,1]: stellar,H2,exterior etc already integrated,
     with source components in REGISTERED chart. Unknown sources never filled.
@@ -38,6 +53,14 @@
     dict(code_pins,boundary_prescription,physical_parameters,numerical_controls)).
     Resume restores the actual iteration, stored gas iterate, history and ordered
     complete column solutions; identity/integrity/chain mismatch is rejected.
+    fixed_source_fourier_J=None (default) evaluates the fixed term from fixed
+    positions/J with source_module, as above. If supplied (finite native complex128
+    ndarray [len(k_physical),10,1]) a private copy IS the fixed term: no angular
+    stellar quadrature is re-evaluated, and fixed positions/J are still required,
+    unmodified and unused, as provenance (checkpoint identity digests). The gas
+    iterate and every updated gas transform are unchanged: actual phi columns
+    through source_module. A supplied term requires a checkpoint module declaring
+    FIXED_SOURCE_SELECTION_IDENTITY (coupled_gas_checkpoint_c2v003 or later).
     """
     if type(max_iterations)is not int or max_iterations<1: raise ValueError('Iteration budget required')
     if not 0<relaxation<=1 or source_atol_J<0 or source_rtol<0 or reality_atol<0 or reality_rtol<0:
@@ -46,8 +69,12 @@
         raise ValueError('Finite settings and positive c required')
     if not gas_columns: raise ValueError('Actual gas columns required')
     args=dict(fourier_arguments); waves=args['k_physical']
-    fixed=np.asarray(source_module.physical_source_fourier(physical_positions_m=fixed_positions_m,
-        integrated_columns_J=fixed_integrated_columns_J,k_physical_inverse_m=waves),dtype=complex)
+    if fixed_source_fourier_J is None:
+        fixed=np.asarray(source_module.physical_source_fourier(physical_positions_m=fixed_positions_m,
+            integrated_columns_J=fixed_integrated_columns_J,k_physical_inverse_m=waves),dtype=complex)
+    else:
+        # Supplied fixed term used as given; never re-evaluated or added to gas.
+        fixed=_supplied_fixed_source(fixed_source_fourier_J,len(waves))
     gas=np.asarray(initial_gas_fourier_J,dtype=complex)
     if gas.shape!=fixed.shape or gas.shape[1:]!=(10,1): raise ValueError('Single actual combined source [nk,10,1] required')
     _finite(gas,'initial gas')
@@ -56,10 +83,13 @@
     if checkpoint is not None:
         # Identity, integrity and exact relaxation chain checked before column work.
         cm=checkpoint['module']
+        if fixed_source_fourier_J is not None and getattr(cm,'FIXED_SOURCE_SELECTION_IDENTITY',None) is not True:
+            raise RuntimeError('CHECKPOINT_MODULE_LACKS_FIXED_SOURCE_SELECTION_IDENTITY; nothing written')
         ck=cm.open_run(checkpoint=checkpoint,solver_file=__file__,fixed=fixed,
             relax=lambda g,u:(1-relaxation)*g+relaxation*u,
             inputs=dict(fixed_positions_m=fixed_positions_m,
                 fixed_integrated_columns_J=fixed_integrated_columns_J,
+                fixed_source_fourier_J=fixed_source_fourier_J,
                 initial_gas_fourier_J=gas,gas_columns=gas_columns,fourier_arguments=args,
                 source_module=source_module,fourier_module=fourier_module,
                 metric_module=metric_module,hi_module=hi_module,quadrature_module=quadrature_module,
@@ -72,6 +102,9 @@
             start_iteration=ck['resume']['iteration']
             gas=ck['resume']['gas']; history=ck['resume']['history']
     def _finish(out,outcome):
+        if fixed_source_fourier_J is not None:
+            out['fixed_source_selection']={'selection':'SUPPLIED_FIXED_SOURCE_FOURIER_J',
+                'fixed_positions_and_integrated_columns':'PROVENANCE_ONLY; accepted unchanged, not used for the fixed term'}
         if ck is not None: out['checkpoint']=cm.finish(ck,outcome=outcome,result=out)
         return out
     for iteration in range(start_iteration,max_iterations):
```

## Appendix B: `diff -u` reviewed checkpoint c2v002 to `coupled_gas_checkpoint_c2v003.py`

```diff
--- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v002.py	2026-10-16 09:03:06.348241890 -0500
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py	2026-10-16 09:22:07.197142379 -0500
@@ -1,9 +1,14 @@
-"""INERT exact restart records for coupled_hi_fourier_source_iteration_v005_resume_c2v001.
-Claude2 0422 c2v002. Restart only at a COMPLETED HI-column boundary of the current
-source iteration. No physics, defaults, tolerances, repair, retry or fallback here.
-c2v002 changes only resume memory: column records of every iteration except the
+"""INERT exact restart records for coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.
+Claude2 0424 c2v003 (successor of reviewed 0422 c2v002). Restart only at a COMPLETED
+HI-column boundary of the current source iteration. No physics, defaults,
+tolerances, repair, retry or fallback here.
+c2v002 changed only resume memory: column records of every iteration except the
 resume iteration are validated and dropped (count kept); the resume iteration's
 records are decoded one at a time as validated. Record format is unchanged.
+c2v003 changes only IDENTITY content: identity.fixed_source records the fixed-term
+selection (SUPPLIED|EVALUATED), the role of fixed positions/columns, and for a
+supplied term its typed sha256 (dtype+shape+C-order bytes), dtype and shape. The
+solver input key fixed_source_fourier_J is required (None = evaluated).
 
 Layout below one checkpoint directory (append-only; nothing replaced or deleted):
   IDENTITY.json                     exact code/input/control/environment identity
@@ -40,6 +45,7 @@
 import numpy as np
 
 FORMAT='UNT_0422_COUPLED_GAS_CHECKPOINT_C2V001'
+FIXED_SOURCE_SELECTION_IDENTITY=True  # solver handshake for a supplied fixed term
 _HEX64=re.compile('[0-9a-f]{64}')
 _TOKEN=r'\d{20}-\d+-[0-9a-f]{8}'
 
@@ -279,8 +285,21 @@
     for pin in [code['solver'],code['checkpoint']]+[p for p in modules.values() if p is not None]:
         if pin['path'] in pins and pins[pin['path']]!=pin['sha256']:
             raise CheckpointError('CODE_CHANGED_SINCE_CALLER_PIN '+pin['path'])
+    if 'fixed_source_fourier_J' not in inputs:
+        raise CheckpointError('FIXED_SOURCE_SELECTION_INPUT_REQUIRED; fixedsrc solver required')
+    supplied=inputs['fixed_source_fourier_J']
+    if supplied is None:
+        fixed_source={'selection':'EVALUATED','fixed_positions_and_integrated_columns':'FIXED_TERM_INPUT',
+                      'supplied_fixed_source_fourier_J':None}
+    else:
+        # The fixed term in use must be exactly the supplied array (values, dtype, shape).
+        if type(supplied) is not np.ndarray or digest(supplied)!=digest(fixed):
+            raise CheckpointError('SUPPLIED_FIXED_SOURCE_IS_NOT_THE_FIXED_TERM')
+        fixed_source={'selection':'SUPPLIED','fixed_positions_and_integrated_columns':'PROVENANCE_ONLY',
+                      'supplied_fixed_source_fourier_J':{'array_sha256':digest(supplied),
+                          'dtype':supplied.dtype.str,'shape':list(supplied.shape)}}
     gas=inputs['initial_gas_fourier_J']; roster=inputs['gas_columns']
-    identity={'format':FORMAT,'code':code,
+    identity={'format':FORMAT,'code':code,'fixed_source':fixed_source,
         'environment':{'python':sys.version,'numpy':np.__version__,'platform':sys.platform,
                        'machine':platform.machine(),'byteorder':sys.byteorder},
         'inputs_sha256':{'fixed_positions_m':digest(inputs['fixed_positions_m']),
```
