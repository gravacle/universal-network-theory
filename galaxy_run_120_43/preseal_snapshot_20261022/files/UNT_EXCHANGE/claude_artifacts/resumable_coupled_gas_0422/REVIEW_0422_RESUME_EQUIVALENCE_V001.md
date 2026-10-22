# REVIEW 0422: resume equivalence (distinct review V001)

- **Role:** distinct reviewer, not the author. This is a Claude2 support-lane local helper, separate from the 0422 implementation author. It has written no line of the reviewed code.
- **Verdict: PASS_WITH_NOTES.**
- **Blocking issues:** none.
- **Driver to use:** `ddo12_coupled_trial_root_driver_v009_resume_c2v002.py`. Do not use c2v001; its defect is confirmed in N4.
- **What I executed:** nonphysical restart-contract tests only (§7). These were the author's 97 tests, re-run in my own scratch subdirectory, plus 19 tests of my own. I also ran one static AST script. None of this is scientific execution. I did not import or run any driver. No scientific worker ran, and no DDO154 or NGC3198 data or physical parameter was used. I did not read held-out velocities or outcomes. Nothing was refit, and I used no cloud or network. No file under `/Users/bgm/Research/Universal Network Theory` was modified. From V008 `result.json` I printed only key names and types, with digits masked.

## 1. Binding inputs (sha256 recomputed from bytes)

| input | sha256 | match |
|---|---|---|
| FROM_CODEX/0422_..._claude2_resumable_coupled_gas_execution.md | 7dfe9050c1bb83b0744882e7fce5e2d887bb566c6c744291fd711150d0c9eb11 | yes |
| CURRENT_INSTRUCTIONS.md (pin) | 1c992d6b2fa3dbc38b831295289bda53f9c9dc703f2c7fdbba86f9aa23f79886 | see note |
| coupled_hi_fourier_source_iteration_v005.py | d35c55bdd588f80661b568629482cbe54b50b5e0626dc0e370cd9a63f278188f | yes |
| ddo12_coupled_trial_root_driver_v009.py | 9629d8b4e1ac9fed9bf7b1e6e39657a73d9e57e81d293a33b31dd26df27a4812 | yes |
| owned_fixed_xy_fourier_line_v001.py | 5c0ab4f6dcd14b79d5ec012f3eee6f58704b8e2982657ac58862b94b9429dfb4 | yes |
| DDO_FIXED_XY_LINE_DRIVER_V009_DISTINCT_REVIEW_V001.json | 2d98ebfca74e873979c953b7a2a34e95189af050e094bdb80e24ab8865434ca6 | yes |
| DDO154_FIRST_DIMENSIONAL_TRIAL_LAUNCH_V008.json | 80a48093d5de741fbe92694ec998afc24e5f59b33a797c97ba2c23eca3851594 | yes |
| DDO154_FIRST_DIMENSIONAL_TRIAL_RUN_V008/result.json | 8208dee8a0b148587052397bca0b8d06b657dc26d416b5d6a3850abe2715232a | yes |

**Note on CURRENT_INSTRUCTIONS.md.** The file now hashes to 786fb01e79b46d30bdc43bd0388f05dd755e716b4ee344ce38162c332c038603 (41474 B). I checked whether the pinned version survives inside it, and it does: its first 38842 bytes hash exactly to the pin 1c992d6b…f79886. So the pinned text is intact, and the appended section is the "Principal continuation" block. That block authorizes the resumable state and says that a 32 kpc search failure does not prove unbounded gas. It posts 0422. Nothing in it countermands 0422.

## 2. Delivered files (recomputed)

| file | sha256 |
|---|---|
| coupled_gas_checkpoint_c2v001.py (569 lines) | a831fe81ef25a065201f0c5d7e2cb4447a7d8cf3712507b1462a09ff4e0d2dd3 |
| coupled_hi_fourier_source_iteration_v005_resume_c2v001.py (212 lines) | c91c5051ad7fea477a51dc9fbdaae2cdc755cc8186a318aa27627cf9d21651e6 |
| ddo12_coupled_trial_root_driver_v009_resume_c2v002.py (310 lines; the driver to use) | 716bbbfa16c1df22b25299f84c609b33ddf4bf8e06a11c09530f37f345a53e29 |
| ddo12_coupled_trial_root_driver_v009_resume_c2v001.py (superseded) | 120d946149b52b0a53ab73cf67e753377d3b806e6d156ba9c3ddce881f7bffa7 |
| DELTA_0422_RESUME_V001.md | 36a8702a426e3de9bf206ca636faa7b258b4a160d935918ebb5f3b4fe66aa23a |

- All five hashes match the author report.
- There is no `__pycache__` in the output directory.
- The delivered `.py` files contain no `@`, `.dot(`, `matmul`, `inner` or `vdot`; the base files have none either.
- The checkpoint module imports only stdlib and numpy.

## 3. Checkpointing disabled: equal to v005/v009

**Solver.** I ran my own `diff -u` of v005 against the copy, and every hunk is checkpoint-only. A static AST script then stripped only the checkpoint constructs from the copy (no import or execution). It removed:
- the `checkpoint` kwarg;
- `cm/ck/start_iteration/restored/resumed/fresh`;
- the `if checkpoint/ck/resumed` blocks;
- `def _finish`.

It also undid these rewrites:
- `range(start_iteration,max_iterations)` back to `range(max_iterations)`;
- `X if fresh else restored[i]` back to `X`;
- `_finish(X,..)` back to `X`;
- `... and fresh` back to `...`.

Result: **the AST is equal to v005** (`SOLVER_DISABLED_PATH_AST_EQUAL_TO_V005: True`), with no checkpoint-only name left over.

With `checkpoint=None`, the copy behaves as follows:
- `start_iteration=0` and `restored=[]`, so `fresh` is always True.
- The HI call is the unchanged expression.
- No checkpoint call runs, `_finish` returns the same dict object, and there is no extra progress event.

Every numerical statement is unchanged and in the same order: `fixed`, `gas`, `current=fixed+gas`, `prepare`, `metric_point`/line cache, `at_z`, the J accumulation, `updated`, the residual and bound, `history.append`, and the relaxation.

**Driver (c2v002 against v009).** The same AST strip removed:
- `R0422`;
- the two kwargs;
- the `run_arguments` capture and its `for`;
- the resume guard;
- the two `if checkpoint_directory` blocks;
- `checkpoint=None`;
- `ca` `checkpoint=`;
- the two CLI flags.

What remains differs from v009 **only** in the `'coupled'` path, which now points to the solver copy. See N1 for one output-metadata difference that the delta omits.

## 4. Resume hand trace (requirement by requirement)

| 0422 requirement | where / how | verdict |
|---|---|---|
| Actual iteration index | `START.iteration`. `_resume_point` takes the top committed START, and the solver loop starts at `range(start_iteration,max_iterations)` | correct |
| Gas iterate stored directly, never reconstructed by subtraction | `START.gas_fourier_J` is a blob of the actual `gas` array. On resume, `gas = START blob`. For j>0 the chain checks `digest(relax(gas_{j-1},updated_{j-1})) == START_j.gas`, using the same expression as v005 line 182 | correct |
| Fixed/current source | Both stored. `fixed` is recomputed and must equal the identity digest. In `_resume_point`, `fixed+gas` must equal the stored current bitwise, and `begin_iteration` re-checks gas, current and fixed | correct |
| Prepared waves | `wavevectors` and `weighted_responses` blobs, plus a typed digest of the **whole** prepared dict. On resume `prepare` is recomputed and must reproduce all of these bitwise, or the resume fails with RESUMED_ITERATION_NOT_REPRODUCED. I checked statically that the real Fourier v004 `prepare()` returns only digest-supported types (ndarray, float, str, dict/list), including the cardinal and binding diagnostics | correct |
| Prior iteration history | `START.history` is an exact typed encoding. Chain: `history_j == history_{j-1} + [COMPLETED_{j-1}.history_entry]`. `begin_iteration` requires `encode(history)==START.history` | correct |
| Ordered, complete completed-column solutions, including source quadrature | `column_NNNNN.json.result` holds the full `solve_hi_column` return. I checked statically that HI v002 and quadrature v002 return only float/int/bool/str/list/tuple/dict. Each record is bound to its START sha, roster digest, index and identity. Contiguity 0..k-1 is enforced | correct |
| Next column index | `len(restored)`. Recorded in the attempt-start `resume_point`, the `iteration_resumed` event and `checkpoint.resumed_from` | correct |
| Input identity: coefficients, source arrays, physical parameters, boundary, roster, controls, code pins | IDENTITY covers code pins (solver, checkpoint, all injected modules and the modules inside `fourier_arguments`), the environment, typed digests of fixed positions/J, initial gas, computed fixed source, the full roster (hi_options included) and every `fourier_arguments` value (grid, k, dk, mubar, Cbar, Eref, ell_F, gamma, tolerances, descriptions), plus the controls. The caller part adds every driver pin (coefficient npz, data JSONs, trial/streaming/observation/kernel modules), the driver's sha, the physical parameters, all 30 run arguments and the boundary text | correct |
| Rebuild gas positions/J in **original** order | Restored and fresh results go through the **same** accumulation statements inside one `enumerate(gas_columns)` loop | correct |
| Rebuild the exact-line cache | `line_key=None` at each iteration start, so the first fresh column calls `prepare_line`. Line v001 `prepare_line` is a pure function of (prepared, x, y) with no module state, so a rebuilt line equals a reused one. Test R6 covers the duplicate-key reuse case | correct |
| Continue at the next column | `fresh = column_index>=len(restored)`. `write_column` enforces `next_column==column_index` and roster object identity | correct |
| Updated gas formed and relaxation applied exactly once, after all columns | `updated` is computed once after the loop. `complete_iteration` requires all columns, and on resume it must reproduce an existing COMPLETED bitwise. Relaxation comes only from the unchanged line 182. If START(i+1) exists, the run resumes there with the stored iterate and no relaxation. Forged double or zero relaxation is rejected (author tests E1/E2) | correct |
| Operation order identical to an uninterrupted run | Restoring only replaces the HI call's return with its exact decoded value; every arithmetic statement runs in v005 order. The checkpoint calls only read arrays (digest, np.save to BytesIO, encode) and mutate no physics object | correct |
| Reject stale or mismatched inputs; a changed grid invalidates columns | IDENTITY_MISMATCH lists the differing fields. Grid, k or dk changes reach `fourier_arguments.*` and `fixed_source_fourier_J`, and saved columns are never read under a different identity. A rejected resume writes nothing | correct |
| Incremental, append-only, per-record integrity; atomic; never overwrite or delete | One canonical JSON per column, each with `payload_sha256`. Publication is temp, fsync, `os.link` (never replaces), samefile check, then unlink of the temp alias only, then a dir fsync. Interrupted temps, uncommitted dirs, failures and attempts without an end are preserved and reported | correct |
| No physics change, taper, Birth ceiling or fallback | None in any file. `CheckpointError` is a RuntimeError and every checkpoint call sits outside the `except ValueError` | correct |

## 5. Failure path

A column ValueError returns v005's exact failure dict plus `checkpoint`, and `finish` writes FAILURE and the attempt end. A resume restores columns 0..k-1 and re-solves column k. Under identical identity that failure is deterministic, so it recurs and is recorded again, never skipped. This is also why V008's column-395 bracket failure cannot be helped by a checkpoint unless Root changes code or inputs, and any such change invalidates the checkpoint by design.

## 6. c2v001 to c2v002

I confirmed by diff that the only code change is the rename of `controls` to `run_arguments` (plus the docstring and comment). In c2v001 the HI boundary-controls list rebound `controls`, so `hi_profile` still read the list and the physics was unaffected. The identity would have recorded the wrong object.

## 7. Executed: NONPHYSICAL RESTART-CONTRACT TESTS ONLY

- **Runtime:** `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (3.12.14, numpy 2.3.5), with a 240 s alarm. All writes went to `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0422/distinct_review_v001/`.
- **Author tests re-run.** These are copies, with hashes checked against the author's:
  - test file b6cbc278d45efb6ace0feecd9dd5b06ab3db72dcc1a0262c21ef4efc1c1cc1ff
  - toy_source 8e65c321f03c3e9413fe8c598a5bacfab0a4b23ad2cf5ceff30e709301faa91c
  - toy_fourier 28974db211700511b31d43341607126eca0f5781a7044685929b010fa5f2ab02
  - toy_line b80e4c344657842600dd539547a75798c51cce393654545cf358bd6e9be40023
  - toy_metric e780bb7682206662700ae9cf57657f167271664c4023fe35c70df9ec29313fdc
  - toy_quadrature b0244efe4e969eabaebaa1a9354dc30edecb1ea6a04d8deb6cfa7eede865ef66
  - toy_hi e9d31f759f668fbc30a277b178d5cc51f4d59de3b51e1e1ece5bc34418030e2e
  - toy_hi_changed d255f140b372df14568b3c496068a591223fdf2560f0feaae97159b68371643d
  - **Result: 97 PASS / 0 FAIL** on the delivered checkpoint a831fe81… and solver c91c5051…. Output `rerun_author_tests_output.txt` 68eb48e3f3c252e392d512bd885226d14404ed44f456f79a3f62e28b40bbe941.
- **Reviewer supplement.** `tests/reviewer_supplement_0422.py` (37fd42bb0fa06cb81ac229c783ec098ba3bc54a590aaaaffa0d959ca8bb3dfd3) uses the same toy stubs and imports only the delivered checkpoint and solver. **Result: 19 PASS / 0 FAIL.** Output `reviewer_supplement_output.txt` 4476d21827d4314e5282c4ca3a76105534dded7d0629a9128611563628d491a5. The tests:
  - R1: a kill between `os.link` and the temp unlink resumes after the linked column, with the result bitwise equal to the uninterrupted run and the temp alias preserved and reported.
  - R2: a kill before the link means the column is recomputed, the result is bitwise equal, and the temp is preserved.
  - R3: a kill after the START(2) blobs and mkdir but before the START record replays iteration 1 from its records with no solves, relaxes once, and gives a bitwise-equal result; the uncommitted dir is reported.
  - R4: a Fortran-order initial gas resumes bitwise equal.
  - R5: negative and payload NaNs are rejected loudly (RECORD_ROUNDTRIP_NOT_EXACT), and the canonical NaN round-trips exactly.
  - R6: consecutive duplicate (R,phi) columns (an uninterrupted run reuses the line cache, a resumed one rebuilds it) give a bitwise-equal result.
  - R7: switching the vertical-line module on resume is rejected, with the tree unchanged.
  - R8: relaxation=1 resumes bitwise equal.
  - R9: resuming a budget-exhausted checkpoint writes only attempt records and does no column solves.
  - R10: the evaluate_prepared path resumes bitwise equal.
- **Static check.** `static/ast_disabled_path_equivalence.py` (0c46f7450f32b54212f818c90efffc320853422fbd274109c3a2236b555f0eec) only parses files, with no import of the analysed code. Output 39deaa93ea12b83b6a814932cdb4d49460e7080d9bb3e6aa36125e2c9041b294 (§3).
- **Scope of the stubs.** The stubs show the restart contract on toy arithmetic only. Equivalence on the real modules rests on the hand trace above, together with determinism within one environment, which the resume itself re-verifies (N5).

## 8. Notes (non-blocking)

- **N1. Delta §3 overstates driver output identity.** It says the only output difference with checkpointing off is `source_pins`. That is incomplete: `main()` stores every CLI argument in `numerical_inputs`, which now also carries `checkpoint_directory: null` and `resume_checkpoint: false`. This is metadata only, with no arithmetic effect. The text should be corrected in a later delta version; no code change is needed.
- **N2. Abbreviated pins in the delta.** The delta abbreviates the stub hashes and the coefficient pin (`fe5a2f06…`). The coding rule asks for the full 64-hex. The full stub hashes are in §7 above and in the pinned test output, and the full coefficient pin is the driver constant fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f.
- **N3. CURRENT_INSTRUCTIONS append.** Already covered in §1: the pinned bytes are verified as an exact prefix.
- **N4. c2v001 must not be used.** The defect is confirmed (§6), and the file is preserved as the author states.
- **N5. Environment identity and BLAS/LAPACK.** The identity records Python, numpy, platform and machine. It does not record the BLAS/LAPACK backend or thread environment variables. This cannot cause a silent mismatch at the resume point, because fixed, current, the full prepared dict (including LAPACK diagnostics) and any existing COMPLETED are re-verified bitwise, and a divergence is rejected. Columns after the resume point are fresh computations, and their equality to an uninterrupted run rests on within-environment determinism, as for any rerun. Root should keep the interpreter and the thread environment unchanged between the original run and its resume.
- **N6. Read `finish_errors` and `preserved_report`.** Errors writing terminal records are reported in `source_fixed_point.checkpoint.finish_errors`, not raised. Root's acceptance should read that field and `preserved_report`.
- **N7. Object aliasing.** Restored results do not keep object aliasing (`mode_weights` shared lists). Values, types and order are exact. Neither the solver nor trial v004 mutates `gas_columns`, and the driver's `serial()` flattens the output in any case.
- **N8. Checkpoint scope.** A checkpoint helps only for interrupting a configuration that is otherwise unchanged (a wall cap, a kill). Any code or input change, for example Root's vertical-field work, the search limit or `max_iterations`, requires a new checkpoint. That is correct behaviour and is documented. A resume also needs a **new** `--progress-directory`, because v009 uses `mkdir(exist_ok=False)`; this is documented in delta §9.
- **N9. Module size.** The checkpoint module is 569 lines, larger than "small", but it is specific to this solver and is not a generic job framework. The post-convergence trial stage is not checkpointed, as documented.

## 9. Not covered by this review

- Physics correctness of v005/v009 and the physical modules.
- The cause of the V008 column-395 bracket failure.
- Overhead on the real problem.
- Durability under power loss: macOS fsync does not issue F_FULLFSYNC. A damaged record would be detected and rejected, never used.
