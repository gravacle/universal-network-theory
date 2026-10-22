# REVIEW 0424: optional supplied fixed source (FIXEDSRC V001), distinct review

- **Role:** distinct reviewer, not author. I wrote neither the 0424 delta nor the 0422 base, and I modified no delivered file. This review file is the only file I created outside scratch (exclusive create).
- **Date:** 2026-10-16.
- **Scope:** the 0424 delta only. That is the solver successor `coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py`, the checkpoint successor `coupled_gas_checkpoint_c2v003.py`, and `DELTA_0424_FIXEDSRC_V001.md`, each checked against the reviewed 0422 base and the 0424 brief.
- **Status:** this was static review plus NONPHYSICAL toy contract tests only. There was no scientific execution and no physical claim.

## Verdict: PASS_WITH_NOTES. No blocking issues.

Every 0424 requirement is met:

| requirement (0424 brief) | finding | evidence |
|---|---|---|
| Argument omitted: computation and API identical to the base | Met. When `fixed_source_fourier_J=None`, the fixedsrc `solve` AST reduces exactly to the reviewed base `solve` AST (docstrings stripped). The only effect outside the solver is one extra `inputs` key handed to the checkpoint module. | static S0-S2; author P1/P2/C1; the verbatim 0422 suite passes 97/97 on the new pair |
| Supplied: strict validation of a finite complex array of exact shape [len(waves),10,1] | Met, and stricter than asked: the array must be a plain ndarray of native complex128, with no conversion. Invalid input raises before any module call or write. | code lines 20-29, 72-77; author V1-V12 |
| Used as the fixed term without re-evaluating the angular stellar quadrature | Met. In supplied mode `source_module` is called only for the per-iteration updated-gas transforms. | D1a; author P3 and C6 (no fixed evaluation on resume) |
| Fixed positions and integrated columns kept as provenance, not used | Met. They stay required arguments, are unused, and are digested into the checkpoint identity. | D6a, author P5/C4 (see N2/N3) |
| No analytic-star term in the gas iterate | Met. At every iteration `current == supplied + gas_j` holds bitwise, gas_0 is the initial gas, and each later gas is exactly one relaxation toward the actual update. | D2 (all iterations, both line paths); author C5/P10 |
| No ring-average substitution; updated gas depends on phi | Met. The update transform receives every actual (R cos phi, R sin phi, z) node in roster order. Toy column sources differ between azimuths at equal R. The update is bitwise the exact transform of those columns, recomputed independently. | D1b-D1e |
| Identity includes an exact typed byte hash of the supplied array (dtype, shape) and the selection | Met. `identity.fixed_source.{selection, fixed_positions_and_integrated_columns, supplied_fixed_source_fourier_J{array_sha256,dtype,shape}}`. For bitwise-equal arrays, the evaluated and supplied identities differ only in these three fields. | D4a; author C3/H6 |
| Actual gas, current and fixed arrays preserved | Met. Blob sets and every START, column and COMPLETED record match between the evaluated path and a bitwise-equal supplied path, apart from the identity hash and attempt token. The START fixed blob is the supplied array, bitwise. | D4b-D4d |
| Resume rejects any changed input and leaves the tree unchanged | Met. Rejected cases: one ulp, a signed-zero byte change, a row permutation, a different array, selection flipped either way, changed provenance (values, or list in place of ndarray), and a dtype change (rejected by validation before the checkpoint opens). | D5a-D5c; author R1-R7 |
| Checkpoint successor only if needed; reviewed module untouched | Met. c2v002 cannot carry the selection except by misfiling it under `controls`, so c2v003 is justified. Against c2v002, the only changes are the module docstring, one handshake constant and `_identity`. Format, codec, publication, scan, chain, resume and writes are unchanged. | static S3-S8; `diff -u` |
| No preparer adaptor; root grid and physics unaltered; 0422 files immutable | Met. No other new file from the author. Every 0422 pin is unchanged (table below). | hashes |

## Blocking issues

None.

## Notes (non-blocking)

- **N1. Narrower dtype than the brief.** The brief asks for a "finite complex" array. Only native `complex128` (`<c16`) in a plain `np.ndarray` is accepted, and complex64, big-endian, `np.memmap` and other subclasses are rejected without conversion. I read the caller read-only to confirm compatibility: `axisymmetric_initial_rest_energy_fourier_v001.py` (f5670726e75b6854fb8d55c2ffe6423251bb31193e5d13b087e46b8185984756) builds its output with `np.zeros((len(k),10,1),dtype=complex)`. `ddo_actual_initial_source_preparation_v007.py` (ac905597b1aa06da3a0178bfa629f6256b78cc87e8b1b05fcea22b3f6df25a42) returns that output unchanged. If Root ever loads the term with `np.load(..., mmap_mode=...)`, the solver will reject it.
- **N2. Provenance is preserved only as digests, and only with a checkpoint.** IDENTITY.json holds typed sha256 values of `fixed_positions_m` and `fixed_integrated_columns_J`, not the arrays themselves. Without a checkpoint, nothing records which supplied array or which provenance was used: the result marker holds only strings, and Codex1's adapter (`owned_composite_prepared_coupled_gas_adapter_v001.py`, 75092cf64cf5293d9e1a5b28b2c909d875c1f5a1b3e9d185f71f065ccff49ec3) puts no array digest in its `binding_custody`. 0424 does not require more. If Root wants no-checkpoint provenance, a later successor could put the three typed digests in the marker.
- **N3. Provenance is opaque in supplied mode.** Without a checkpoint, None, a string or NaN arrays are accepted and do not affect the result (D6a, author P5). With a checkpoint, provenance must be digest-encodable: `object()` is refused before the directory is created (D6b). Because the digest is typed, an equal-valued list is not the same identity as the ndarray (D5c), so a resume must pass the same types.
- **N4. Identity is exact to the byte, by design.** A signed-zero change, which compares equal by value, is rejected (D5a). Memory order is excluded: Fortran-order and non-contiguous views with identical values resume normally (D5d, author R9).
- **N5. Memory and overhead are untested at real scale.** The private C-order copy adds one [nk,10,1] complex128 array (160·nk bytes) while the caller's `prepared` dict still holds the original. With a checkpoint, `_identity` digests the same array up to four times, and each digest makes a transient contiguous byte copy. Both costs are small next to the column work at toy scale but were not measured on the composite grid.
- **N6. FORMAT is unchanged.** c2v003 keeps `FORMAT='UNT_0422_COUPLED_GAS_CHECKPOINT_C2V001'`, so c2v002 and c2v003 records cannot be told apart by format. Cross-version separation rests on the identity: the `code.checkpoint` pin, the `fixed_source` section, and the required `fixed_source_fourier_J` input key (`FIXED_SOURCE_SELECTION_INPUT_REQUIRED` for the base solver). The disclosed consequence: base-solver and c2v002 checkpoints cannot be resumed by the new pair, and Root must point the adapter's checkpoint dict at c2v003.
- **N7. Stale inherited docstring.** Solver line 52 still names `coupled_gas_checkpoint_c2v001` as the checkpoint module. Line 63 correctly requires c2v003 for the supplied path. This is documentation only.
- **N8. New result key.** In supplied mode every returned dict gains `fixed_source_selection`, which holds strings only. Any consumer that checks exact key sets must allow it. The omitted path adds nothing (D3a).
- **N9. The supplied term's physics is not checked here.** Hermitian pairing on the signed grid, units and sign belong to Root and the preparer. A term that is not paired surfaces as the unchanged `NONREAL_PHYSICAL_METRIC` column failure, with no projection. My own random toy term needed explicit ± pairing to avoid exactly that failure.
- **N10. A new file appeared in the directory during this review.** `REVIEW_0422_FIX_V002_V001.md` (9f499af95e7f4e1bcee19cec29708da84dc84dddacc8c0f38c6e9f314bb8794c) is dated 09:29:46, after the 0424 deliverables (09:22-09:24). It is another reviewer's review of the 0422 fix, outside the 0424 scope, and it changed no pinned file.

## Pins (sha256 recomputed from bytes, before and after the review; all unchanged)

| file | sha256 |
|---|---|
| FROM_CODEX/0424_2026-10-16_analytic_fixed_source_interface.md (read fully) | 0acba7bc41ecb9dd44d22e92f31fc199bd9b52b76b7f570d0fdb3452ca663e5d |
| FROM_CODEX/0422_2026-10-16_claude2_resumable_coupled_gas_execution.md | 7dfe9050c1bb83b0744882e7fce5e2d887bb566c6c744291fd711150d0c9eb11 |
| root original `coupled_hi_fourier_source_iteration_v005.py` (reference) | d35c55bdd588f80661b568629482cbe54b50b5e0626dc0e370cd9a63f278188f |
| **reviewed base** solver `..._v005_resume_c2v001.py` | c91c5051ad7fea477a51dc9fbdaae2cdc755cc8186a318aa27627cf9d21651e6 |
| **reviewed base** checkpoint `coupled_gas_checkpoint_c2v002.py` | 0bb955ed86c6e71884152c1dd97c41e2d086a4cd2e135f78e9b2716d2e4803c1 |
| **reviewed** driver `ddo12_coupled_trial_root_driver_v009_resume_c2v003.py` (still loads base solver + c2v002) | 7a45a970807e15e880b2d25b5ea3bcda28f8419611adc8abbaf4f1f50a2698a1 |
| DELTA_0422_RESUME_V001.md | 36a8702a426e3de9bf206ca636faa7b258b4a160d935918ebb5f3b4fe66aa23a |
| FIX_DELTA_0422_RESUME_V002.md | aae6988d5b9e23619c1837384d24f02beac3be0397576576f077eb3b6d2c6102 |
| REVIEW_0422_RESUME_EQUIVALENCE_V001.md | bd16fce7c9c6e2470475c42967118346fadbe253a87ea2496bb68648db4819a5 |
| REVIEW_0422_RESUME_IDENTITY_IO_V001.md | 0cc91ad6092377e25a08df14d9277653ebdb762ded78e319262c8a494a40830b |
| older 0422 files: checkpoint c2v001 / driver c2v001 / driver c2v002 | a831fe81ef25a065201f0c5d7e2cb4447a7d8cf3712507b1462a09ff4e0d2dd3 / 120d946149b52b0a53ab73cf67e753377d3b806e6d156ba9c3ddce881f7bffa7 / 716bbbfa16c1df22b25299f84c609b33ddf4bf8e06a11c09530f37f345a53e29 |
| **under review** solver `..._resume_fixedsrc_c2v001.py` (245 lines) | 44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644 |
| **under review** checkpoint `coupled_gas_checkpoint_c2v003.py` (606 lines) | 069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114 |
| **under review** `DELTA_0424_FIXEDSRC_V001.md` | fc41dc0b39f13cffbddcf6ca1717b183e5e6f7f1951a8ad2fa1aaf52aa4615a6 |

The 0422 document hashes and the older 0422 code hashes also appear independently, in FROM_CLAUDE2 0136/0137, FIX_DELTA_0422_RESUME_V002 or REVIEW_0422_FIX_V002_V001.

## What was executed

All work happened in `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0424/distinct_review_0424_v001/`, using `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (Python 3.12.14, numpy 2.3.5). Each script ran under its own `signal.alarm` limit (60 s, 180 s or 240 s) and finished within it.

**What was not run or touched:**
- No driver was run.
- The base solver and c2v002 were never imported; they were only parsed as text for the AST check.
- No physical module, scientific data or parameters, target velocities, fitting, cloud, network, installs or retries.
- `/Users/bgm/Research/Universal Network Theory` was only read: three files (adapter, preparer v007, analytic module; hashes in N1/N2) to confirm the caller's dtype and calling convention.

1. **Hashes and diffs.** Every pin above was recomputed. I produced my own `diff -u` of the base solver against fixedsrc (`my_solver.diff`, b4eae2b4ec1f9359cfc5c0b449d28b9181f871b6e41f427efa40d7d47a08599f) and of c2v002 against c2v003 (`my_checkpoint.diff`, 4ef4f872b85cfe73188cdfff93b6553f989dfde2b98ebb0fb80f9cfaa7fc6101). Both match DELTA Appendices A and B line for line, blank lines aside.
2. **Static AST check, parse only** (`ast_equivalence_0424.py` 2a9292fe549a2b3e1527a5001fe1e329fe4ed51b63a24d017e3cb27a2a51f7c3; output 5c4c2e2254988abdaa923554e0124b03148a3adbb9ade4a498fc711665f4b43f): **9/9 PASS**.
   - Specialising the fixedsrc solver to `fixed_source_fourier_J=None` takes six reductions: drop the helper, drop the signature keyword, take the `is None` branch, drop the handshake guard, drop the inputs key, drop the `_finish` marker. No reference to the name remains, and the result's AST equals the base AST.
   - In c2v003 the only top-level changes are the added constant and `_identity`. Within `_identity`, three statements are inserted and the identity dict gains `fixed_source`.
3. **Author's suites, rerun on the delivered bytes** (stubs verbatim from 0422, hashes as in DELTA §8):
   - `test_fixedsrc_contract_0424.py` (6dacbffcfe9dfa0b0d0a6da8bb0b2b6f5783ba1065e268df96def7dc4b0a62d0): **91/91 PASS** (output ef3c6d90277f9b9df4616cbc7c8730e6bddbdef653c2c328d217c143b4252f9a).
   - Verbatim `test_restart_contract_0422.py` (b6cbc278d45efb6ace0feecd9dd5b06ab3db72dcc1a0262c21ef4efc1c1cc1ff) on c2v003 + fixedsrc: **97/97 PASS** (output ec3643d07165f4dd8cf7fc19a659ab5c82d38bb2c6111a3384228c50aa5d2094).
4. **Reviewer-written NONPHYSICAL tests** (`test_distinct_review_0424.py` 52796dc019b2a579a636d18ee4e7430acd8e5948e05e5c4afbf4e46ff4a3cdd6; output ebc349fcf3f424cbc3348778ff91b3d3a0a33bf721302702f91f9f69e38950c6): **28/28 PASS**.
   - They use my own toy waves, roster, supplied term and relaxation, which differ from the author's. They import only c2v003, fixedsrc and the toy stubs, and the column solve is the toy HI stub.
   - Groups: D1 (phi-resolved update, with a spy source module), D2 (gas chain at every iteration), D3 (None equals omitted), D4 (checkpoint content of evaluated vs supplied), D5 (further resume rejections and controls), D6 (opaque provenance).
5. **Discrimination check, scratch only.** My suite was run against the author's scratch mutants, none of them delivered:
   - m1 (always evaluate) and m3 (correction in gas) fail at D1a.
   - m5 (supplied term folded into gas) fails D2 and D3b and trips the c2v003 guard.
   - m2 (no private copy) is not caught by my suite; the author's P8 covers it.

The test data have no physical meaning. Nothing here exercises the actual analytic preparer, the composite grid, memory, overhead, or the V008 column-395 bracket failure.
