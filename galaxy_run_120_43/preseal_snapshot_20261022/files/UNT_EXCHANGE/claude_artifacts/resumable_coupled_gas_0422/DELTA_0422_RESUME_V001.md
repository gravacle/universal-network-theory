# DELTA 0422 — resumable coupled gas iteration (Claude2 c2v001/c2v002)

Implementation author: Claude2 support lane, local helper (author only; distinct review is a separate helper and is NOT included here).
Status: **implementation plus nonphysical restart-contract tests only.** No scientific execution. The driver was never imported or run. No scientific worker ran. No DDO154/NGC3198 data or physical parameter entered any test. Nothing was refit, nothing was launched, and no cloud or network was used. Root retains physics, calibration, numerical launch and acceptance.

## 1. Binding inputs (sha256 from bytes, verified before work)

| input | sha256 |
|---|---|
| FROM_CODEX/0422_2026-10-16_claude2_resumable_coupled_gas_execution.md | 7dfe9050c1bb83b0744882e7fce5e2d887bb566c6c744291fd711150d0c9eb11 |
| UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md (pinned version) | 1c992d6b2fa3dbc38b831295289bda53f9c9dc703f2c7fdbba86f9aa23f79886 |
| helpers/recovered_packet_audit/coupled_hi_fourier_source_iteration_v005.py | d35c55bdd588f80661b568629482cbe54b50b5e0626dc0e370cd9a63f278188f |
| helpers/recovered_packet_audit/ddo12_coupled_trial_root_driver_v009.py | 9629d8b4e1ac9fed9bf7b1e6e39657a73d9e57e81d293a33b31dd26df27a4812 |
| helpers/recovered_packet_audit/owned_fixed_xy_fourier_line_v001.py | 5c0ab4f6dcd14b79d5ec012f3eee6f58704b8e2982657ac58862b94b9429dfb4 |
| helpers/response_packet_audit/DDO_FIXED_XY_LINE_DRIVER_V009_DISTINCT_REVIEW_V001.json | 2d98ebfca74e873979c953b7a2a34e95189af050e094bdb80e24ab8865434ca6 |
| CODEX1/DDO154_FIRST_DIMENSIONAL_TRIAL_LAUNCH_V008.json | 80a48093d5de741fbe92694ec998afc24e5f59b33a797c97ba2c23eca3851594 |
| CODEX1/DDO154_FIRST_DIMENSIONAL_TRIAL_RUN_V008/result.json | 8208dee8a0b148587052397bca0b8d06b657dc26d416b5d6a3850abe2715232a |

CURRENT_INSTRUCTIONS.md matched its pin at verification. The file was then appended during this work, and its current sha256 is 786fb01e79b46d30bdc43bd0388f05dd755e716b4ee344ce38162c332c038603. The appended section records two things: the principal's authorization to retain resumable state across timeouts, and the posting of dispatch 0422. It does not countermand any 0422 constraint. Only read-only access was used.

From V008 I inspected only the key structure and types of result.json, plus the progress.jsonl record layout (stages iteration_prepared and column_completed; iteration_NNNN_prepared.npz). Digits were masked. No numeric physical value was printed or used. I also read these modules statically to confirm the column result types and that they hold no module-level state: HI v002, column quadrature v002, Fourier v004, source v003, trial v004, metric evaluator v002, and the cardinal, complex and static binding modules.

## 2. Created files (exclusive create, never overwritten)

Directory: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/`

| file | sha256 | role |
|---|---|---|
| coupled_gas_checkpoint_c2v001.py | a831fe81ef25a065201f0c5d7e2cb4447a7d8cf3712507b1462a09ff4e0d2dd3 | new small checkpoint module (numpy + stdlib) |
| coupled_hi_fourier_source_iteration_v005_resume_c2v001.py | c91c5051ad7fea477a51dc9fbdaae2cdc755cc8186a318aa27627cf9d21651e6 | solver copy of v005 with optional `checkpoint=` |
| ddo12_coupled_trial_root_driver_v009_resume_c2v002.py | 716bbbfa16c1df22b25299f84c609b33ddf4bf8e06a11c09530f37f345a53e29 | **driver to use**: copy of v009 with optional checkpoint CLI |
| ddo12_coupled_trial_root_driver_v009_resume_c2v001.py | 120d946149b52b0a53ab73cf67e753377d3b806e6d156ba9c3ddce881f7bffa7 | **SUPERSEDED, DO NOT USE** (see below) |
| DELTA_0422_RESUME_V001.md | (this file; the author reports its sha256 separately) | delta and contract |

**Defect in the superseded driver c2v001.** I caught it in an AST self-check after publication. v009's `run()` already uses a local named `controls`, which later holds the HI boundary controls list. In c2v001 the new identity capture `controls = dict(locals())` was rebound by that line before use. As a result, `caller_identity.numerical_controls` would have recorded the HI boundary-controls list instead of the run arguments. This did not affect physics or arithmetic, but the identity claim was false. c2v002 renames the capture to `run_arguments`; that is its only change from c2v001 (diff in Appendix C). The c2v001 file is preserved rather than deleted, per the no-overwrite rule. The solver copy and the checkpoint module are unaffected. The c2v002 driver loads the same solver copy and checkpoint module.

## 3. Changed lines per file (new-file line numbers; full `diff -u` in Appendices A/B)

### Solver: v005 to coupled_hi_fourier_source_iteration_v005_resume_c2v001.py (162 to 212 lines)

- 4-5, 36-40: docstrings describing the optional checkpoint.
- 21-22: signature gains `checkpoint=None`.
- 55-77: with a checkpoint, `cm.open_run(...)` verifies identity, integrity and the exact relaxation chain before any column work. On resume it sets `start_iteration`, the **stored** already-relaxed `gas` iterate, and `history`. Also defines `_finish(out,outcome)`, which returns `out` unchanged when `ck is None`. The loop becomes `for iteration in range(start_iteration,max_iterations)`.
- 80-85: after `prepare` comes `restored=[]; resumed=False` and `cm.begin_iteration(...)`. For a new iteration this commits START before any column. For a resumed iteration it instead requires bitwise-identical gas, current, fixed, prepared waves and full prepared dict.
- 90-93: one extra progress event `iteration_resumed` (scalars only), emitted only when resumed.
- 121: `fresh=column_index>=len(restored)`.
- 127-129, 132: `result=(hi_module.solve_hi_column(<identical call>) if fresh else restored[column_index])`.
- 137, 145-146: the failure return is wrapped by `_finish(...,'FAILED_SOURCE_PREPARATION')`; the dict content is unchanged.
- 148-150: `cm.write_column(...)` for fresh columns only, before the progress event. `column_completed` events are emitted for fresh columns only.
- 169-171: `cm.complete_iteration(...)` after `history.append` and before the convergence test.
- 177, 180-181, 183, 185: converged and exhausted returns wrapped by `_finish`.
- **Unchanged numerical statements:** `current=fixed+gas` (78), `prepare` (79), line cache/`metric_point`/`at_z`, the source accumulation loop (154-160), `updated` (161), residual and bound, `history.append`, and the relaxation `gas=_finite((1-relaxation)*gas+relaxation*updated,...)` (182).

### Driver: v009 to ddo12_coupled_trial_root_driver_v009_resume_c2v002.py (283 to 310 lines)

- 5-7: docstring.
- 24: `R0422` constant for the new output directory.
- 48-53: signature gains `checkpoint_directory=None, resume_checkpoint=False`. `run_arguments=dict(locals())` is the first statement and drops only the progress/checkpoint locations.
- 55-56: `resume_checkpoint` must be bool and requires a directory.
- 92: `'coupled'` points to the solver copy.
- 105-106: the checkpoint module is loaded (and pinned through `module()`) **only when enabled**.
- 235-245: the `checkpoint` dict carries identity evidence only: all driver pins, including the coefficient npz and data JSONs; the driver's own path and sha256; physical parameters (Eref, ell_F, gamma, solar mass, kpc, c, hi_options); run arguments; and the boundary prescription text.
- 251-252: `ca` gains `checkpoint=checkpoint`, which is `None` when disabled.
- 301-302: CLI flags `--checkpoint-directory` and `--resume-checkpoint`.

### Checkpoint disabled equals v005/v009

With `checkpoint=None`:
- `range(0,max_iterations)` is the same as `range(max_iterations)`.
- `restored` stays `[]`, so `fresh` is always True and the HI call is identical.
- No checkpoint call executes.
- `_finish` returns the identical dict.
- No extra progress event is emitted.

No numerical statement is changed or reordered. The only additions are guards, an identity wrapper and a conditional expression. Nonphysical tests B1, B5 and K1 confirm identical result digests, enabled versus disabled, on synthetic stubs.

In the driver, the only output difference with checkpointing off is `source_pins`, which lists the solver copy instead of v005. That follows unavoidably from a new versioned copy.

## 4. Checkpoint format (`UNT_0422_COUPLED_GAS_CHECKPOINT_C2V001`)

```
<ckpt>/IDENTITY.json                    kind=identity: identity dict + identity_sha256
<ckpt>/checkpoint.lock                  advisory flock(LOCK_EX|LOCK_NB) for the single live writer
<ckpt>/blobs/<sha256>.npy               content-addressed np.save(allow_pickle=False) arrays
<ckpt>/attempts/<token>.start.json      kind=attempt_start: mode, resume_point{iteration,next_column_index}, preserved_report
<ckpt>/attempts/<token>.end.json        kind=attempt_end: outcome, records_written (absent => interrupted/exception)
<ckpt>/iteration_NNNN/START.json        kind=iteration_start (commit marker, written BEFORE any column)
<ckpt>/iteration_NNNN/column_NNNNN.json kind=column, one per completed column, roster order
<ckpt>/iteration_NNNN/COMPLETED.json    kind=iteration_completed (after ALL columns)
<ckpt>/iteration_NNNN/FAILURE.<token>.json kind=failure (actual returned column failure)
```

- Token: `<time_ns:020d>-<pid>-<8 hex>`.
- Envelope: every JSON record is canonical JSON (sorted keys, compact, ASCII, no NaN) plus `\n`. It holds `format`, `kind`, `identity_sha256` (except IDENTITY), and `payload_sha256` = sha256 of the canonical record without that field. On read the record must re-serialize byte-identically.
- START: `iteration`, `column_count`, `gas_fourier_J`, `current_source_fourier_J`, `fixed_source_fourier_J`, `prepared_wavevectors`, `prepared_weighted_responses` (blob refs), `prepared_metric_response_sha256` (typed digest of the **entire** prepared dict, diagnostics included), `history` (exact encoding of prior-iteration history), `attempt`.
- column: `iteration`, `iteration_start_sha256` (binds the column to that START's source), `column_index`, `column_count`, `column_input_sha256` (digest of that roster entry), `result` (exact encoding of the COMPLETE `solve_hi_column` return: nodes, source_quadrature elements, roots, brackets, samples, and so on), `attempt`.
- COMPLETED: `iteration`, `iteration_start_sha256`, `updated_gas_fourier_J` (blob), `gas_fourier_residual_J`, `bound_J` (float.hex), `history_entry`, `converged`, `column_count`, `attempt`.
- FAILURE: `iteration`, `column_index`, `iteration_start_sha256`, `failure` (exact encoding of the returned failure dict), `attempt`.
- Blob reference: `{blob:'blobs/<file_sha256>.npy', file_sha256, array_sha256 (typed digest), dtype, shape}`.
- Exact value codec, tagged JSON: `['f',float.hex]`, `['i',decimal]`, `['b',bool]`, `['n']`, `['s',str]`, `['c',re.hex,im.hex]`, `['l',[...]]` for list, `['t',[...]]` for tuple, `['d',[[key,val],...]]` for dict in insertion order, and `['a'|'g',dtype.str,shape,bytes.hex]` for numpy array or scalar. Every write re-decodes its own JSON text and requires an identical typed digest (`RECORD_ROUNDTRIP_NOT_EXACT` otherwise).
- Typed digest: sha256 over type tags plus exact float bits, int text, UTF-8 strings, list versus tuple, sorted dict keys, numpy dtype+shape+C-order bytes, and module objects as (abspath, file sha256).
- Publication: write temp `.<name>.<token>.tmp` exclusively, then fsync, then `os.link(temp, final)`, which fails if final exists and **never replaces**. Then `samefile` check, unlink of the temp *alias* only, and directory fsync. This is the no-overwrite equivalent of temp+rename.

## 5. Identity fields (IDENTITY.json; any difference rejects the whole checkpoint)

- `code`: the solver copy and checkpoint module (abspath, sha256 of file bytes); the source, fourier, metric, hi, quadrature and vertical_fourier modules; and every module inside `fourier_arguments` (cardinal, complex binding, static binding). Each is cross-checked against the caller's load-time pins (`CODE_CHANGED_SINCE_CALLER_PIN`).
- `environment`: `sys.version`, numpy version, `sys.platform`, machine, byteorder.
- `inputs_sha256` (typed digests of the arrays and values the solver actually uses):
  - `fixed_positions_m`, `fixed_integrated_columns_J`, `initial_gas_fourier_J` (as complex), `fixed_source_fourier_J` (computed).
  - `gas_columns`: the full ordered roster including hi_options, so search step, search limit, root and lapse tolerances, call budget and panels are included.
  - `fourier_arguments.<key>` for every key, including the coefficients `source_hessian_grid`, `k_physical`, `dk_weights`, `registered_bravais`, `jbar`, `mubar`, `Cbar`, `Eref`, `ell_F`, `gamma`, the solve tolerances, `node_convention`, the pairing flag, and the domain and boundary descriptions.
- `shapes`: column count and source Fourier shape.
- `controls` (exact): `c_m_s`, `max_iterations`, `relaxation`, `source_atol_J`, `source_rtol`, `reality_atol`, `reality_rtol`.
- `caller`, from the c2v002 driver: `code_pins` (all driver pins, including the coefficient npz `fe5a2f06…` and the radial source, state binding and calibration-ID JSONs), `driver_code`, `physical_parameters`, `numerical_controls` (all 30 run arguments), and `boundary_prescription`.

## 6. Resume: reconstruction, identical arithmetic, single relaxation

1. `open_run` (resume mode) takes the lock and compares the recomputed identity with IDENTITY.json. It then scans every record (integrity, kind, naming, contiguity and cross-references) and verifies the exact chain:
   - START(0).gas equals the input initial gas and START(0).history equals `[]`.
   - For every j: `fixed+gas_j` is bitwise equal to the stored current.
   - For j>0: gas_j is bitwise equal to `(1-relaxation)*gas_{j-1}+relaxation*updated_{j-1}`, the same expression and operation order as v005, so each stored iterate is **exactly one** relaxation.
   - history_j equals history_{j-1} plus the COMPLETED_{j-1} entry.
   - Every referenced blob is loaded and verified.
2. The resume point is the highest committed START, together with its contiguous complete column records (next column = their count). The solver starts there with the **stored** gas iterate (never derived by subtraction) and the stored history.
3. At that iteration the solver recomputes `current=fixed+gas` and `prepare(...)` exactly as v005 does. `begin_iteration` then requires bitwise equality with START: gas, current, fixed, wavevectors and weighted responses, plus a typed digest of the full prepared dict. Any difference raises `RESUMED_ITERATION_NOT_REPRODUCED`.
4. The column loop runs over the **original roster order**. Restored columns supply their exact decoded solution, and only fresh columns call the HI solver. Every column, restored or fresh, passes through the *same* accumulation statements in the same order, so `positions`/`columns` (integrated gas positions and J) are rebuilt in original order. The exact-line cache starts empty (`line_key=None`) and is rebuilt at the first fresh column; prepare_line is deterministic in (prepared, x, y), so this matches the uninterrupted cache.
5. After **all** columns, `updated` is formed once by the unchanged statement. If COMPLETED already existed, the recomputed updated, residual, bound, history entry and converged flag must reproduce it bitwise (`COMPLETED_RECORD_NOT_REPRODUCED`). Relaxation is then applied once by the unchanged v005 line. If START(i+1) already existed, the resume began there with its stored gas and no relaxation is re-applied.
6. Interrupt points covered and tested:
   - inside any column;
   - after the last column but before COMPLETED;
   - after COMPLETED but before START(i+1);
   - before START(0);
   - right after START(i+1).

## 7. Staleness, mismatch and integrity rejection (nothing is written on rejection)

- `IDENTITY_MISMATCH; ... differing: identity.<field paths>`: any change in code, environment, inputs, roster, controls or caller identity. **A changed Fourier or source grid** shows up as `inputs_sha256.fourier_arguments.k_physical`, `dk_weights` or `source_hessian_grid`, and `fixed_source_fourier_J`. Saved columns are never read under a different identity.
- `CHECKPOINT_REJECTED; every file preserved unchanged; problems: ...` lists all problems found:
  - UNREADABLE_RECORD, WRONG_RECORD_KIND, RECORD_INTEGRITY_FAILURE, NONCANONICAL_RECORD
  - UNEXPECTED_ENTRY, MISSING_DIRECTORY
  - RECORDS_WITHOUT_VALID_START, START_MISMATCH, NONCONTIGUOUS_COLUMN_RECORDS, COLUMN_RECORD_MISMATCH (wrong iteration, index, START binding, roster entry or identity), COMPLETED_RECORD_MISMATCH
  - NONCONTIGUOUS_ITERATION_STARTS, UNCOMMITTED_DIRECTORY_NOT_AT_RESUME_POINT, UNCOMMITTED_DIRECTORY_AFTER_UNFINISHED_OR_CONVERGED_ITERATION, EARLIER_ITERATION_INCOMPLETE_OR_TERMINAL
- Chain and blob checks: ITERATION_BEYOND_BUDGET, FIXED_SOURCE_MISMATCH, CURRENT_SOURCE_NOT_FIXED_PLUS_GAS, ITERATION0_NOT_INITIAL_STATE, RELAXATION_CHAIN_BROKEN, HISTORY_CHAIN_BROKEN, BLOB_MISSING, BLOB_INTEGRITY_FAILURE, BLOB_ARRAY_MISMATCH, MALFORMED_BLOB_REFERENCE, MALFORMED_RECORD_ENCODING, MALFORMED_CHECKPOINT_CONTENT.
- Access: CHECKPOINT_DIRECTORY_EXISTS (mode new never reuses a directory), CHECKPOINT_DIRECTORY_MISSING, CHECKPOINT_LOCK_FILE_UNAVAILABLE, CHECKPOINT_IN_USE, CODE_CHANGED_SINCE_CALLER_PIN, CALLER_IDENTITY_FIELD_REQUIRED, EXPLICIT_BOUNDARY_PRESCRIPTION_REQUIRED, CHECKPOINT_NAMING_LIMIT.
- Write-time: RECORD_EXISTS (temp kept), START_EXISTS, COLUMN_ORDER_ERROR, ITERATION_NOT_COMPLETE, RECORD_ROUNDTRIP_NOT_EXACT, UNSUPPORTED_RECORD_TYPE/DTYPE, BLOB_CONTENT_MISMATCH, PUBLICATION_LINK_MISMATCH.

## 8. Failure and interruption preservation

- **Never overwritten:** hard-link publication refuses existing names; mode new refuses an existing directory; a content-addressed blob that already exists must be byte-equal.
- **Never deleted:** the only unlink is the temp alias of a file just linked. The following are preserved and listed in `preserved_report` (in the attempt-start record and in the returned `checkpoint` summary): interrupted temps (`.*.tmp`), attempts without an end record, FAILURE records, uncommitted iteration directories, and ignored `.DS_Store`.
- **Rejected resume:** writes nothing, not even an attempt record. Tests confirm the whole tree is byte-identical before and after.
- **Physical column failure:** the return dict is exactly v005's plus `checkpoint`; a FAILURE record with the exact failure dict and an attempt end are written. A resume re-solves that column under identical inputs and records its own FAILURE; earlier records are kept.
- **Exceptions:** `CheckpointError` subclasses RuntimeError, so it can never be caught by the solver's `except ValueError`, and every checkpoint call lies outside that `try`. Mid-run write errors stop the run loudly, with prior records still resumable. Terminal-record errors are reported in `checkpoint.finish_errors` without discarding the actual scientific return.
- **No fallback:** the checkpoint module holds no physics, tolerance, taper, retry, default or real projection.

## 9. Root usage (no launch performed here)

- New run: the identical launch arguments, plus `--progress-directory <new P1> --checkpoint-directory <CK>`.
- Resume after a wall cap: **the same arguments**, the same interpreter and numpy, a **new** `--progress-directory <P2>` (v009 semantics require a new directory), and `--checkpoint-directory <CK> --resume-checkpoint`.
- The driver to use is `..._resume_c2v002.py`. The returned `source_fixed_point.checkpoint` gives `resumed_from`, `records_written` and `preserved_report`.

## 10. NONPHYSICAL RESTART-CONTRACT TESTS (not scientific execution)

**These are not scientific execution.** Every test is a nonphysical restart-contract test. Toy stubs with no physical meaning replace every source, Fourier, line, metric, HI and quadrature module. The tests import only the new checkpoint module and the new solver copy. The driver was neither imported nor run, and no physical module, data or parameter was used. Everything ran in scratch under `signal.alarm(240)`.

- Command: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B test_restart_contract_0422.py <delivered checkpoint> <delivered solver>` (Python 3.12.14, numpy 2.3.5).
- Scratch: `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0422/`.
- Pins:
  - test file sha256 `b6cbc278d45efb6ace0feecd9dd5b06ab3db72dcc1a0262c21ef4efc1c1cc1ff`
  - output `final_test_output.txt` sha256 `479d4246f965dc21703b0f9831103f549eed662e72ea30feae52812027f9939b`
  - stubs: toy_source `8e65c321…a91c`, toy_fourier `28974db2…b02`, toy_line `b80e4c34…023`, toy_metric `e780bb76…fdc`, toy_quadrature `b0244efe…f66`, toy_hi `e9d31f75…e2e`, toy_hi_changed `d255f140…43d` (full hashes are in the output file).
- **Result: 97 PASS / 0 FAIL**, on the delivered bytes `a831fe81…2dd3` (checkpoint) and `c91c5051…51e6` (solver).

| group | what the test does | what it asserts |
|---|---|---|
| A (26) | exact codec and digest | exact round-trip, including -0.0, inf, subnormal, max float, big int, tuple vs list, dict order, np.float64/int64 scalars, complex and Fortran-order arrays; NaN stays NaN; the digest separates list from tuple, float from np.float64 and -0.0 from 0.0; CheckpointError is not a ValueError; unsupported types are rejected |
| B (13) | compare checkpoint-enabled runs with checkpoint=None | result digest identical for exhaustion and convergence, on both the exact-line and evaluate_prepared paths; record counts correct; no leftover temps. Negative controls: a different relaxation changes the digest, and tuple-to-list in one record is detected |
| C (32) | interrupt (BaseException inside a stub) at iteration0 col0, iteration0 col4, iteration1 col3, iteration2 col0, after the last column before COMPLETED, after COMPLETED before START, and before START0; then a double interruption, the evaluate_prepared path, the convergence scenario, and a resume after convergence | after resume, the **bitwise-identical final result digest**, the exact resume point, a single `iteration_resumed` event, no repeated `column_completed` events, one exact-line rebuild per fresh column, and the interrupted attempt reported. Resume after convergence writes no new column or START records |
| E (3) | re-signed forged START(1) with a doubly relaxed or unrelaxed gas iterate | rejected with RELAXATION_CHAIN_BROKEN, tree unchanged. Control: a correctly relaxed re-signed START is accepted |
| F (5) | flipped byte in a committed record, truncated blob, column gap, incomplete earlier iteration or unknown file, record at the wrong index | each rejected with the whole tree byte-identical |
| G (2) | partial temp from a kill during a write | ignored for state, reported, and preserved byte-identical; result still identical |
| H (10) | changed k grid, relaxation, max_iterations, roster, initial gas, boundary prescription, module code, fixed source arrays, Fourier argument, or a caller pin that disagrees with loaded code | each rejected with the named field, and nothing written |
| I/J (2) | mode new on an existing directory; a concurrent writer | refused, nothing written |
| K (3) | a column failure | failure dict identical with checkpoint enabled; FAILURE record and attempt end written; resume reproduces the identical failure and both FAILURE records are kept |

Driver static checks (no import): `compile()` and AST only. Both driver copies compile with no `@`, dot or matmul. In c2v002, `run_arguments` is assigned once, as the first statement of `run()`, and read only for identity, which rules out the c2v001 shadowing defect. The referenced solver and checkpoint files exist. No `__pycache__` was written to the output directory.

## 11. Assumptions

1. **Determinism within one environment.** The same interpreter, numpy build and platform give identical bits for identical inputs and operation order: einsum(optimize=False), exp, and the LAPACK calls in prepare and the metric evaluator. On resume, fixed, current, prepared and any existing COMPLETED are *verified* bitwise. Columns after the resume point are fresh computations under identical inputs; they cannot be compared with a run that never happened.
2. **No hidden state.** The pinned HI v002, quadrature v002, metric v002, Fourier v004, line v001, source v003 and binding modules hold no module-level mutable state (static check). A column solution depends only on the prepared response, the column inputs, the boundary and the modules.
3. **Supported result types.** Column results consist of codec-supported types. HI v002 and quadrature v002 return pure Python dict, list, tuple, float, int, bool and str; the metric is used via `.tolist()`. Anything else fails loudly at the first column write.
4. **Boundary prescription.** `boundary_jet_at_positions` is a pure function. The callable itself is not hashed; it is identified by the caller's prescription text plus the driver code pin.
5. **Filesystem.** One writer per checkpoint, on a local filesystem with hard links, flock and fsync.

## 12. Limitations and failure modes

- **Granularity.** Restart happens only at completed HI-column boundaries; work inside an interrupted column is recomputed.
- **Post-convergence stage.** The motion/query stage that runs after source convergence (trial v004) is not checkpointed. A timeout there replays the converged iteration from its records, which costs one prepare and one source transform with no column solves, and then redoes that stage.
- **Strict identity.** Changing `max_iterations` (for example to continue an exhausted budget), the paths, the Python or numpy version, or any code is rejected and needs a new checkpoint. That is a launch decision for Root.
- **Object aliasing.** Aliasing is not preserved: each node and its quadrature element originally share one `mode_weights` list. Values, types and order are exact, and no consumer mutates them.
- **Durability.** On macOS, os.fsync does not force the drive cache (F_FULLFSYNC is not used). Kills and timeouts are fully covered. Power loss could truncate the last records; those are detected and rejected or reported, never used silently.
- **Cost.** Overhead was not measured on the real problem, since that would need a scientific run. Per column it is an exact encode, a JSON round-trip check, sha256 and fsync. Per iteration it adds a typed digest of the full prepared dict (about 13824 node diagnostics, a count taken from the V008 record layout), plus START blobs of about 3 complex [nk,10,1] arrays.
- **V008 cannot be resumed.** It has no checkpoint, and its iteration-0 column-395 bracket failure is deterministic under identical inputs. Its progress and result files remain evidence only. This implementation does not address the 32 kpc bracket failure (Root/HR vertical-field work), and it changes no physics, search limit, profile, sign, boundary, parameter, taper or ceiling.
- **Distinct review** has not been performed by the author. It is to be done by a separate reviewer.

## Appendix A: `diff -u` v005 to coupled_hi_fourier_source_iteration_v005_resume_c2v001.py

```diff
--- "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/coupled_hi_fourier_source_iteration_v005.py"	2026-10-16 07:54:26.227356368 -0500
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_c2v001.py	2026-10-16 08:31:10.012792435 -0500
@@ -1,6 +1,8 @@
 """Inert finite Fourier/HI source fixed-point iteration, no coefficient fallback.
 One actual combined source family per call. Rest-energy source approximation.
 Uniform physical Cartesian background chart; full metric anisotropy retained.
+RESUME c2v001 (Claude2 0422): optional exact restart at a completed HI-column
+boundary via an injected checkpoint module. checkpoint=None executes v005.
 """
 import math
 import numpy as np
@@ -16,7 +18,8 @@
           gas_columns, fourier_arguments, boundary_jet_at_positions,
           source_module, fourier_module, metric_module, hi_module, quadrature_module,
           c_m_s, max_iterations, relaxation, source_atol_J, source_rtol,
-          reality_atol, reality_rtol, vertical_fourier_module=None, progress_callback=None):
+          reality_atol, reality_rtol, vertical_fourier_module=None, progress_callback=None,
+          checkpoint=None):
     """Required actual inputs:
     fixed positions[n,3]/J[n,10,1]: stellar,H2,exterior etc already integrated,
     with source components in REGISTERED chart. Unknown sources never filled.
@@ -30,6 +33,11 @@
     including chosen zero-mode/boundary PERTURBATIONS; no zero default.
     N=1,Cbar are restored separately by the metric evaluator, never in these arrays.
     Reference field order n,C6,mu3. No axisymmetry imposed on response.
+    checkpoint=None (default) runs the v005 statements. Otherwise dict(module=
+    coupled_gas_checkpoint_c2v001, directory, mode='new'|'resume', caller_identity=
+    dict(code_pins,boundary_prescription,physical_parameters,numerical_controls)).
+    Resume restores the actual iteration, stored gas iterate, history and ordered
+    complete column solutions; identity/integrity/chain mismatch is rejected.
     """
     if type(max_iterations)is not int or max_iterations<1: raise ValueError('Iteration budget required')
     if not 0<relaxation<=1 or source_atol_J<0 or source_rtol<0 or reality_atol<0 or reality_rtol<0:
@@ -44,13 +52,45 @@
     if gas.shape!=fixed.shape or gas.shape[1:]!=(10,1): raise ValueError('Single actual combined source [nk,10,1] required')
     _finite(gas,'initial gas')
     history=[]
-    for iteration in range(max_iterations):
+    cm=None; ck=None; start_iteration=0
+    if checkpoint is not None:
+        # Identity, integrity and exact relaxation chain checked before column work.
+        cm=checkpoint['module']
+        ck=cm.open_run(checkpoint=checkpoint,solver_file=__file__,fixed=fixed,
+            relax=lambda g,u:(1-relaxation)*g+relaxation*u,
+            inputs=dict(fixed_positions_m=fixed_positions_m,
+                fixed_integrated_columns_J=fixed_integrated_columns_J,
+                initial_gas_fourier_J=gas,gas_columns=gas_columns,fourier_arguments=args,
+                source_module=source_module,fourier_module=fourier_module,
+                metric_module=metric_module,hi_module=hi_module,quadrature_module=quadrature_module,
+                vertical_fourier_module=vertical_fourier_module,
+                controls=dict(c_m_s=c_m_s,max_iterations=max_iterations,relaxation=relaxation,
+                    source_atol_J=source_atol_J,source_rtol=source_rtol,
+                    reality_atol=reality_atol,reality_rtol=reality_rtol)))
+        if ck['resume'] is not None:
+            # Stored already-relaxed iterate, never reconstructed by subtraction.
+            start_iteration=ck['resume']['iteration']
+            gas=ck['resume']['gas']; history=ck['resume']['history']
+    def _finish(out,outcome):
+        if ck is not None: out['checkpoint']=cm.finish(ck,outcome=outcome,result=out)
+        return out
+    for iteration in range(start_iteration,max_iterations):
         current=fixed+gas
         prepared=fourier_module.prepare(**args,source_density_fourier=current)
+        restored=[]; resumed=False
+        if ck is not None:
+            # New iteration: commit START before any column. Resumed iteration:
+            # bitwise-identical gas/current/prepared response required instead.
+            restored,resumed=cm.begin_iteration(ck,iteration=iteration,gas=gas,
+                current=current,fixed=fixed,prepared=prepared,history=history)
         if progress_callback is not None:
             progress_callback(dict(stage='iteration_prepared',iteration=iteration,
                 column_count=len(gas_columns),metric_source_fourier_J=current,
                 prepared_metric_response=prepared))
+            if resumed:
+                progress_callback(dict(stage='iteration_resumed',iteration=iteration,
+                    column_count=len(gas_columns),restored_column_count=len(restored),
+                    next_column_index=len(restored)))
         # One line retained at a time; no cross-iteration or stale-source reuse.
         line_key=None; line=None
         def metric_point(R,phi,z):
@@ -78,20 +118,23 @@
         positions=[]; columns=[]; solutions=[]
         for column_index,col in enumerate(gas_columns):
             R=col['R_m']; phi=col['phi']
+            fresh=column_index>=len(restored)
             def at_z(z):
                 m=metric_point(R,phi,z)
                 return {'N':m['N'],'metric_cyl':m['g_cylindrical'].tolist(),
                         'mode_weights':[[1.0]+[0.0]*9]}
             try:
-                result=hi_module.solve_hi_column(metric_at_z=at_z,quadrature_module=quadrature_module,
+                # A restored record is this iteration's exact completed solution; it
+                # re-enters the SAME accumulation below in original roster order.
+                result=(hi_module.solve_hi_column(metric_at_z=at_z,quadrature_module=quadrature_module,
                     radius_m=R,radial_weight_m=col['radial_weight_m'],
                     azimuth_weight_rad=col['azimuth_weight_rad'],surface_ref_kg_m2=col['Sigma_kg_m2'],
-                    c_m_s=c_m_s,**col['hi_options'])
+                    c_m_s=c_m_s,**col['hi_options']) if fresh else restored[column_index])
             except ValueError as exc:
                 # Preserve the actual failed preparation and its driving field.
                 # Only this column call (including its metric callback) is caught;
                 # no replacement column, success flag, retry, or clipped boundary.
-                return {'converged_finite_fixed_point':False,
+                return _finish({'converged_finite_fixed_point':False,
                     'failure':{'type':type(exc).__name__,'message':str(exc),
                         'iteration':iteration,'column_index':column_index,
                         'column_inputs':dict(col),'c_m_s':c_m_s,
@@ -99,9 +142,12 @@
                     'gas_columns':solutions,'history':history,
                     'metric_source_fourier_J':current,
                     'prepared_metric_response':prepared,
-                    'scope':'FAILED_SOURCE_PREPARATION; completed columns are partial evidence only; no fixed point or galaxy prediction'}
+                    'scope':'FAILED_SOURCE_PREPARATION; completed columns are partial evidence only; no fixed point or galaxy prediction'},
+                    'FAILED_SOURCE_PREPARATION')
             solutions.append(result)
-            if progress_callback is not None:
+            if ck is not None and fresh:
+                cm.write_column(ck,iteration=iteration,column_index=column_index,column=col,result=result)
+            if progress_callback is not None and fresh:
                 progress_callback(dict(stage='column_completed',iteration=iteration,
                     column_index=column_index,column_count=len(gas_columns),
                     roots_m=result['roots_m'],metric_calls=result['metric_calls']))
@@ -120,19 +166,23 @@
         if not math.isfinite(bound): raise ValueError('Nonfinite source convergence bound')
         history.append({'iteration':iteration,'gas_fourier_residual_J':residual,'bound_J':bound,
                         'roots_m':[r['roots_m'] for r in solutions]})
+        if ck is not None:
+            cm.complete_iteration(ck,iteration=iteration,updated=updated,residual=residual,
+                bound=bound,history_entry=history[-1],converged=residual<=bound)
         if progress_callback is not None:
             progress_callback(dict(stage='iteration_completed',iteration=iteration,
                 gas_fourier_residual_J=residual,bound_J=bound,
                 reconstructed_gas_fourier_J=updated))
         if residual<=bound:
-            return {'converged_finite_fixed_point':True,'metric_source_fourier_J':current,
+            return _finish({'converged_finite_fixed_point':True,'metric_source_fourier_J':current,
                 'reconstructed_gas_fourier_J':updated,'gas_columns':solutions,'history':history,
                 'prepared_metric_response':prepared,
-                'scope':'finite source closure only; no metric-error bound near singular response, continuum or full Euler claim'}
+                'scope':'finite source closure only; no metric-error bound near singular response, continuum or full Euler claim'},
+                'CONVERGED_FINITE_FIXED_POINT')
         gas=_finite((1-relaxation)*gas+relaxation*updated,'relaxed gas')
-    return {'converged_finite_fixed_point':False,'history':history,
+    return _finish({'converged_finite_fixed_point':False,'history':history,
             'last_metric_source_fourier_J':current,'last_gas_columns':solutions,
-            'scope':'iteration budget exhausted; not a solved galaxy'}
+            'scope':'iteration budget exhausted; not a solved galaxy'},'ITERATION_BUDGET_EXHAUSTED')
 
 
 def cylindrical_metric_covector_to_registered(*, R_m, phi, Cbar,
```

## Appendix B: `diff -u` v009 to ddo12_coupled_trial_root_driver_v009_resume_c2v002.py (driver to use)

```diff
--- "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/ddo12_coupled_trial_root_driver_v009.py"	2026-10-16 07:54:26.227561241 -0500
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/ddo12_coupled_trial_root_driver_v009_resume_c2v002.py	2026-10-16 08:32:46.143556913 -0500
@@ -2,6 +2,9 @@
 No target velocities, likelihood, fitting, hidden coefficient defaults or acceptance.
 Requires supplied Eref [J], ell_F [m], gamma and explicit numerical resolutions.
 Frozen single-point native response remains provisional; not a 12-coordinate fit.
+RESUME c2v002 (Claude2 0422): identical physics/inputs; coupled solver is the
+v005_resume_c2v001 copy. Optional --checkpoint-directory [--resume-checkpoint]
+saves/restores exact completed-HI-column state; omitted, behaviour is v009.
 """
 import argparse
 import hashlib
@@ -18,6 +21,7 @@
 KERNEL = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/annular_source_kernel_0403/annular_bernstein_source_kernel_v001.py')
 COEFFICIENT = C/'PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz'
 COEFFICIENT_SHA = 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f'
+R0422 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422')
 
 
 def sha(path):
@@ -41,8 +45,15 @@
         hi_max_metric_calls, hi_panels_per_side, max_iterations, relaxation,
         source_atol_J, source_rtol, pressure_atol_Pa_per_m, pressure_rtol,
         reality_atol, reality_rtol, relative_singular_floor,
-        hermitian_tolerance, solve_rtol, solve_atol, progress_directory=None):
+        hermitian_tolerance, solve_rtol, solve_atol, progress_directory=None,
+        checkpoint_directory=None, resume_checkpoint=False):
+    # Every run argument except output/checkpoint locations enters restart identity.
+    # (Not named 'controls': that local later holds the HI boundary controls.)
+    run_arguments = dict(locals())
+    for key in ('progress_directory', 'checkpoint_directory', 'resume_checkpoint'): del run_arguments[key]
     import numpy as np
+    if type(resume_checkpoint) is not bool or (resume_checkpoint and checkpoint_directory is None):
+        raise ValueError('Explicit checkpoint directory required to resume')
     scalars = [Eref_J, ell_F_m, solar_mass_kg, kpc_m, kmax_inverse_kpc,
                pressure_step_kpc, azimuth_step_rad, hi_search_step_kpc,
                hi_search_limit_kpc, hi_root_tolerance_kpc]
@@ -78,7 +89,7 @@
     paths = {
         'trial': HERE/'galaxy_coupled_fourier_hi_prediction_v004.py',
         'vertical_line': HERE/'owned_fixed_xy_fourier_line_v001.py',
-        'coupled': HERE/'coupled_hi_fourier_source_iteration_v005.py',
+        'coupled': R0422/'coupled_hi_fourier_source_iteration_v005_resume_c2v001.py',
         'fourier': HC/'owned_physical_fourier_metric_quadrature_v004.py',
         'source': HERE/'baryonic_metric_source_columns_v003.py',
         'streaming': HERE/'galaxy_baryonic_source_forward_v002.py',
@@ -91,6 +102,8 @@
         'static': HP/'owned_static_action_metric_binding_v002.py',
         'bernstein': KERNEL}
     for name, path in paths.items(): mods[name] = module(path, pins)
+    if checkpoint_directory is not None:
+        mods['checkpoint'] = module(R0422/'coupled_gas_checkpoint_c2v001.py', pins)
     c = 299792458.0
     pc_m = kpc_m/1000
     sigma_unit = solar_mass_kg/(pc_m*pc_m)
@@ -219,12 +232,24 @@
             event['elapsed_seconds']=time.monotonic()-started
             with (progress_path/'progress.jsonl').open('a') as f:
                 f.write(json.dumps(serial(event),allow_nan=False)+'\n');f.flush()
+    checkpoint=None
+    if checkpoint_directory is not None:
+        # Identity evidence only; no physical input, boundary or control changes.
+        checkpoint=dict(module=mods['checkpoint'],directory=str(checkpoint_directory),
+            mode='resume' if resume_checkpoint else 'new',
+            caller_identity=dict(code_pins=dict(pins),
+                driver_code={'path':str(Path(__file__).resolve()),'sha256':sha(__file__)},
+                physical_parameters=dict(Eref_J=Eref_J,ell_F_m=ell_F_m,gamma=gamma,
+                    solar_mass_kg=solar_mass_kg,kpc_m=kpc_m,c_m_s=c,hi_options=dict(hi_options)),
+                numerical_controls=run_arguments,
+                boundary_prescription='boundary(pos): zero perturbation fields (n,10,1), gradient (n,10,1,3), hessian (n,10,1,3,3); isolated frozen background N=1,Cbar restored by metric evaluator; fa boundary_description unchanged'))
     ca=dict(fixed_positions_m=fixed_positions,fixed_integrated_columns_J=fixed_J,
         initial_gas_fourier_J=initial,gas_columns=gas_columns,fourier_arguments=fa,
         boundary_jet_at_positions=boundary,source_module=mods['source'],fourier_module=mods['fourier'],
         metric_module=mods['metric'],hi_module=mods['hi'],quadrature_module=mods['quadrature'],
         c_m_s=c,max_iterations=max_iterations,relaxation=relaxation,source_atol_J=source_atol_J,
-        source_rtol=source_rtol,reality_atol=reality_atol,reality_rtol=reality_rtol,vertical_fourier_module=mods['vertical_line'],progress_callback=progress)
+        source_rtol=source_rtol,reality_atol=reality_atol,reality_rtol=reality_rtol,vertical_fourier_module=mods['vertical_line'],progress_callback=progress,
+        checkpoint=checkpoint)
     angular=[{'phi_rad':2*math.pi*i/observation_azimuth_count,
               'fit_weight':1/observation_azimuth_count} for i in range(observation_azimuth_count)]
     result=mods['trial'].evaluate(coupled_module=mods['coupled'],coupled_arguments=ca,
@@ -273,6 +298,8 @@
     for name in ints: p.add_argument('--'+name.replace('_','-'),type=int,required=True)
     for name in floats: p.add_argument('--'+name.replace('_','-'),type=float,required=True)
     p.add_argument('--progress-directory',default=None)
+    p.add_argument('--checkpoint-directory',default=None)
+    p.add_argument('--resume-checkpoint',action='store_true')
     args=vars(p.parse_args())
     result=run(**args)
     result['numerical_inputs']=args
```

## Appendix C: `diff -u` superseded driver c2v001 to c2v002 (the only change is the identity-capture rename)

```diff
--- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/ddo12_coupled_trial_root_driver_v009_resume_c2v001.py	2026-10-16 08:31:10.012896601 -0500
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/ddo12_coupled_trial_root_driver_v009_resume_c2v002.py	2026-10-16 08:32:46.143556913 -0500
@@ -2,7 +2,7 @@
 No target velocities, likelihood, fitting, hidden coefficient defaults or acceptance.
 Requires supplied Eref [J], ell_F [m], gamma and explicit numerical resolutions.
 Frozen single-point native response remains provisional; not a 12-coordinate fit.
-RESUME c2v001 (Claude2 0422): identical physics/inputs; coupled solver is the
+RESUME c2v002 (Claude2 0422): identical physics/inputs; coupled solver is the
 v005_resume_c2v001 copy. Optional --checkpoint-directory [--resume-checkpoint]
 saves/restores exact completed-HI-column state; omitted, behaviour is v009.
 """
@@ -48,8 +48,9 @@
         hermitian_tolerance, solve_rtol, solve_atol, progress_directory=None,
         checkpoint_directory=None, resume_checkpoint=False):
     # Every run argument except output/checkpoint locations enters restart identity.
-    controls = dict(locals())
-    for key in ('progress_directory', 'checkpoint_directory', 'resume_checkpoint'): del controls[key]
+    # (Not named 'controls': that local later holds the HI boundary controls.)
+    run_arguments = dict(locals())
+    for key in ('progress_directory', 'checkpoint_directory', 'resume_checkpoint'): del run_arguments[key]
     import numpy as np
     if type(resume_checkpoint) is not bool or (resume_checkpoint and checkpoint_directory is None):
         raise ValueError('Explicit checkpoint directory required to resume')
@@ -240,7 +241,7 @@
                 driver_code={'path':str(Path(__file__).resolve()),'sha256':sha(__file__)},
                 physical_parameters=dict(Eref_J=Eref_J,ell_F_m=ell_F_m,gamma=gamma,
                     solar_mass_kg=solar_mass_kg,kpc_m=kpc_m,c_m_s=c,hi_options=dict(hi_options)),
-                numerical_controls=controls,
+                numerical_controls=run_arguments,
                 boundary_prescription='boundary(pos): zero perturbation fields (n,10,1), gradient (n,10,1,3), hessian (n,10,1,3,3); isolated frozen background N=1,Cbar restored by metric evaluator; fa boundary_description unchanged'))
     ca=dict(fixed_positions_m=fixed_positions,fixed_integrated_columns_J=fixed_J,
         initial_gas_fourier_J=initial,gas_columns=gas_columns,fourier_arguments=fa,
```
