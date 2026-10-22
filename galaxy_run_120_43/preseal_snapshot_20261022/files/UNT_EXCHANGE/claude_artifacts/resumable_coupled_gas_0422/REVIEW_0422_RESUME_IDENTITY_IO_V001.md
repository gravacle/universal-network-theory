# REVIEW 0422: resumable coupled gas iteration (identity, failure and I/O)

- **Role:** distinct reviewer, not author. I did not write or edit any delivered file.
- **Scope:** restart identity, stale/mismatch rejection, failure and interruption preservation, record I/O (append-only, atomicity, integrity), the driver's failure statuses, and disk, file-count and memory cost at 576 columns. Equivalence of physics and arithmetic was checked only as far as restart identity needs it.
- **Date:** 2026-10-16.

## Verdict: FAIL (one blocking issue, narrow fix)

The restart contract is sound. Every identity, rejection, append-only, atomicity, preservation, no-silent-success, no-fallback and status-preservation requirement passed, both by reading the code and in my own independent nonphysical tests (68/68).

The one blocking issue is resume memory. It grows by about 0.1 GB for every completed iteration on disk. With the V008 launch limits (wall 600 s, combined RSS 536,870,912 B), the run would need a resume at almost every iteration, and resumes would hit the RSS cap after roughly 2–3 iterations of the 8-iteration budget. The failure would be loud and recoverable, never silent or lossy. But as delivered, the tool would stall in the run it was built for. The fix is a few lines in a new versioned checkpoint module (B1).

## 1. Binding inputs (sha256 recomputed from bytes)

| input | pinned | recomputed |
|---|---|---|
| FROM_CODEX/0422_…_resumable_coupled_gas_execution.md | 7dfe9050…9eb11 | match |
| CURRENT_INSTRUCTIONS.md | 1c992d6b…f79886 | **file now 786fb01e…c038603**; see below |
| coupled_hi_fourier_source_iteration_v005.py | d35c55bd…8188f | match |
| ddo12_coupled_trial_root_driver_v009.py | 9629d8b4…a4812 | match |
| owned_fixed_xy_fourier_line_v001.py | 5c0ab4f6…dfb4 | match |
| DDO_FIXED_XY_LINE_DRIVER_V009_DISTINCT_REVIEW_V001.json | 2d98ebfc…34ca6 | match |
| DDO154_FIRST_DIMENSIONAL_TRIAL_LAUNCH_V008.json | 80a48093…51594 | match |
| DDO154_FIRST_DIMENSIONAL_TRIAL_RUN_V008/result.json | 8208dee8…5232a | match |

**CURRENT_INSTRUCTIONS mismatch, resolved from bytes.** The first 38,842 of the file's 41,474 bytes hash exactly to the pin 1c992d6b…f79886, so the pinned version is a byte-exact prefix of the current file. I read that prefix as binding. The appended 2,632 bytes (section "Principal continuation … 2026-10-16") authorize retaining resumable state and record the posting of 0422. They countermand no 0422 constraint. This agrees with the author's report.

**Delivered files recomputed; all match the author report.**
- `coupled_gas_checkpoint_c2v001.py`: a831fe81ef25a065201f0c5d7e2cb4447a7d8cf3712507b1462a09ff4e0d2dd3
- `coupled_hi_fourier_source_iteration_v005_resume_c2v001.py`: c91c5051ad7fea477a51dc9fbdaae2cdc755cc8186a318aa27627cf9d21651e6
- `ddo12_coupled_trial_root_driver_v009_resume_c2v002.py`: 716bbbfa16c1df22b25299f84c609b33ddf4bf8e06a11c09530f37f345a53e29
- `ddo12_coupled_trial_root_driver_v009_resume_c2v001.py` (superseded): 120d946149b52b0a53ab73cf67e753377d3b806e6d156ba9c3ddce881f7bffa7
- `DELTA_0422_RESUME_V001.md`: 36a8702a426e3de9bf206ca636faa7b258b4a160d935918ebb5f3b4fe66aa23a

At the end of the review, base v005 and v009 were re-hashed and are unchanged. No author file appears under the UNT tree. The only 0422-named file there is Codex1's posting copy of the dispatch, which is byte-identical to the FROM_CODEX copy, timestamped 08:06, before the author's work.

## 2. What was executed (and what was not)

**Static work:**
- Read in full: the 0422 task, the pinned CURRENT_INSTRUCTIONS prefix, v005, v009, the line module, the V009 review JSON, all four delivered .py files and the DELTA.
- Read for types and call paths: trial v004, HI v002, quadrature v002 and the Fourier v004 `prepare`.
- Grepped the pinned physics modules for module-level state; none found.
- Ran `compile()`/AST on every delivered .py:
  - all compile;
  - none uses `@`, dot or matmul;
  - imports are numpy plus stdlib only;
  - in c2v002, `run_arguments` is assigned once (line 52) and is distinct from the later `controls` (line 113).
- `diff -u` of v005 against the solver copy and of v009 against c2v002: numerical statements are unchanged and in the same order.

**From V008, structure only (digits masked):**
- result.json: key and type layout, plus per-column counts. Counts were 656–1150 floats per column (median 662), 17 nodes per column, 6–127 search samples, 0–63 nonmonotonicity entries.
- progress files: layout and npz array headers (13824×10×1 complex128). No numeric physical value was printed or used.
- Launch file: only `arguments.max_iterations` (8) and the `limits` block (wall 600 s, combined RSS 536,870,912 B).

**Nonphysical restart-contract tests.** These are not scientific execution. They were written by me, independently of the author's tests, and run with `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (3.12.14, numpy 2.3.5) under `signal.alarm(240)`. They write only in `…/scratchpad/r0422/review_c2r001/`. They import only the delivered checkpoint module and solver copy. Every source, Fourier, line, metric, HI and quadrature module is my own toy stub (`stubs/rv_toy_*.py`) with no physical meaning.

| file | sha256 | result |
|---|---|---|
| review_restart_contract_0422.py | d679b063718c7be7381abd1dff923b2861e77de5579d979790e7f4be538689c9 | **68 PASS / 0 FAIL** (run2_output.txt f23a5082e9a1f53f0f7aff923e0eedf1f7828a6cf80ac6bf40fe8071d1c9d94e) |
| review_io_sizing_0422.py | 897b2765514ab922992585c70584ff06027bc87e41f99c06ac1024c97816c56b | io_sizing_output.txt aac0008ea3bec711b1d458eaa5ace94bb326028c864ce7d29f80050d593ded0c |
| review_io_scaling_0422.py | 47a79a9375b51760ff639f06652b36adb873f83e518efade9a344aff57eae916 | io_scaling_output.txt e6a48031d41dc5d82ba00a3f7834cc64bd8e75433f1199a5cf3242a5acda3383 |
| variant/rv_checkpoint_scan_variant.py (review-only prototype of the B1 fix; not a deliverable) | 258c3e77c895822fa0877563acf169322d366a63ed8d6192ae0cbcf4e12734ac | io_scaling_variant_output.txt 141af1bc8faa47964250f115e3ff34e92b74af352684bfc5ed84712fa851ff71; restart-contract tests on the variant: 68/0 (run_variant_output.txt 3bcd20568aab70e5a917246276f6b1b969fe1556d6f64ab2d476dc56bf39533d) |

Stub hashes:

| stub | sha256 |
|---|---|
| rv_toy_fourier | 6f61a4dd0d4e12b951b4fe0f4f65aa3ce90fd6280a8de9f957255a401c38eabb |
| rv_toy_hi | 9b5b5d8feaf6c5229bef81014f6439f13eb094beec4414ac35bcae130ba68be3 |
| rv_toy_line | 9caa653c69788a8ddbb8191ae293cf863a6ae1e255d41607302eadb2ef5339e3 |
| rv_toy_metric | 02e5dcf171cfd575e284a6c6cd728f5b86a6f8363729dc3e25591c990801e90f |
| rv_toy_quadrature | 2b35c7f6e410b7c76ca0ca52ae7626758361dec63cf727d9772d31b8f2d678aa |
| rv_toy_source | 9e2f30c4c4e0788d7bb17975ee392600b134e63b42a3ad688353c0f1c81d56cb |

The sizing and scaling scripts import only the checkpoint module. They use random synthetic values arranged in the V008 structural counts.

My first run (run1_output.txt, 834789675730e9ab5fe151b91655d023db087a2320fba6619ac46b81c6c5d732) showed CHECKPOINT_IN_USE failures. The cause was my harness: it kept the exception traceback, which held the solver frame and its open lock. After the harness cleared the traceback, all tests passed. This is recorded as note N6. It is not an author defect.

**Not executed:**
- the driver (not imported or run, in either version);
- any scientific worker, physics module or prepare;
- DDO154 or NGC3198 data and parameters;
- held-out velocities or outcomes;
- any refit, cloud use, network access, install, or 0351/0360 restart.

Nothing under `/Users/bgm/Research/Universal Network Theory` was written. The scratch directory review_c2r001 holds about 389 MB of synthetic sizing checkpoints.

## 3. Requirement checks

| requirement | result | evidence |
|---|---|---|
| Identity covers coefficients | PASS | Caller `code_pins` include the coefficient npz pin. The loaded `source_hessian_grid`, `mubar` and `Cbar` are digested under `fourier_arguments.*` |
| Identity covers source arrays | PASS | `fixed_positions_m`, `fixed_integrated_columns_J`, `initial_gas_fourier_J` and the computed `fixed_source_fourier_J` |
| Identity covers physical parameters | PASS | Eref, ell_F and gamma (in `fourier_arguments`), `c_m_s` (controls), and the caller's `physical_parameters` (solar mass, kpc, c, hi_options) |
| Identity covers boundary prescription | PASS (scoped) | Caller text plus driver code sha256 plus `fourier_arguments.boundary_description`. The callable is not hashed (N4) |
| Identity covers full column roster | PASS | Typed digest of the ordered `gas_columns`, including hi_options and search limits, plus the column count |
| Identity covers numerical controls | PASS | Solver controls (c, max_iterations, relaxation, source and reality tolerances) and all 30 driver run arguments |
| Identity covers Fourier/source grid | PASS | `k_physical`, `dk_weights`, `source_hessian_grid` and the fixed-source digest. Test R5a/b: a 1e-12 k shift or a 2^-40 weight change is rejected and names the field |
| Identity covers code pins | PASS | Solver copy, checkpoint module, all injected modules and the modules inside `fourier_arguments` (path and sha256), cross-checked against the caller's load-time pins |
| Mismatch or stale input is rejected explicitly, never a silent restart or partial reuse | PASS | IDENTITY_MISMATCH lists the differing fields before any record is read. A rejected resume writes nothing; the tree is byte-identical (R5a–f, R4a–e). A deleted START with columns present is rejected (R4d). A re-signed record presented as another column is rejected by its roster binding (R4e). New mode never reuses a directory (R6c) |
| Changed grid invalidates saved columns | PASS | Identity is checked before `_scan`, so columns are never decoded under a different grid (R5a/b). The untouched checkpoint still resumes bitwise afterwards (R5g) |
| Incremental, append-only, one record per column with its own integrity | PASS | `column_NNNNN.json` per completed column, each with `payload_sha256`, bound to its START payload sha and its roster-entry digest. Nothing is rewritten per column (R1e) |
| Atomic writes | PASS | Exclusive temp, fsync, `os.link` (never replaces), `samefile` check, unlink of the temp alias only, directory fsync. The only unlink in the module is that alias (grep) |
| Interrupted, corrupt or truncated files preserved and reported, never overwritten or deleted | PASS | A truncated record, a changed digit, a truncated blob and a removed START are each rejected with the tree byte-identical (R4a–d). A partial temp is preserved byte-identical and listed in `preserved_report` (R6b). An attempt without an end record is reported (R2d) |
| No silent success | PASS (note N3) | CheckpointError is a RuntimeError and is never caught as a physical ValueError. A simulated kill propagates (R2a). Errors writing the final records go to `checkpoint.finish_errors` |
| No physics fallback | PASS | The checkpoint module has no tolerance, retry, taper, default or projection. A restored column re-enters the identical accumulation |
| No generic job framework | PASS | One purpose-specific module, numpy plus stdlib |
| Driver failure statuses preserved | PASS | The status expression is unchanged. With checkpointing on, the failure dict equals the base digest, and FAILED_SOURCE_PREPARATION is kept in scope and outcome (R7a). Resume reproduces the failure, and both FAILURE records are kept (R7b) |
| Resume is bitwise-identical; relaxation applied exactly once | PASS (toy) | Kill points tested: iteration 0 column 3, iteration 2 column 1, iteration 3 column 0, after COMPLETED(1) and before START(2), and during convergence. The final digest equals the uninterrupted run. No column is repeated, and the first fresh column is the interrupted one (R2, R3, R8) |
| Checkpoint off equals v005/v009 | PASS (code reading plus toy) | Identical digest and identical progress-event sequence (R1b–d). Driver output differs from v009 by more than the author states (N2) |

## 4. Blocking issue

**B1. Resume memory scales with the whole checkpoint, not with the resume iteration.**

- **Where:** `coupled_gas_checkpoint_c2v001.py` `_scan`, lines 364–378. Every committed iteration's parsed column records (`records`) stay in `chain` until `open_run` returns, yet `_resume_point` uses only the top iteration's records.
- **Measured.** These are synthetic records with the V008 median structure (656 floats per column, 576 columns), and the figures are traced Python allocation during `open_run(mode='resume')`:

  | completed iterations on disk | traced peak | open time |
  |---|---|---|
  | 1 | 125 MB | 2.5 s |
  | 2 | 225 MB | 4.9 s |
  | 4 | 417 MB | 10.5 s |

  That is about 98 MB more per iteration. Worst-case structure (1150 floats) gives about twice as much: 348 MB already for one median plus one worst-case iteration.
- **Consequence.** The V008 envelope (600 s wall, 512 MiB combined RSS, `max_iterations` 8; V008 itself used about 293 MB combined) forces a resume at almost every iteration. The process baseline plus the scan would exceed the combined RSS cap at about the second or third iteration. Every later resume would be killed or raise MemoryError before writing anything. The checkpoint survives and the failure is loud, but the run cannot advance.
- **Required fix:**
  - In a new versioned checkpoint module (for example `coupled_gas_checkpoint_c2v002.py`), validate each column record of a non-resume iteration and drop it, keeping only a count.
  - For the resume iteration, decode each record as it is validated, so the raw parsed JSON is not held alongside the decoded results.
  - Point a new driver version at the new module. The solver copy needs no change, because the module is injected.
  - Re-measure resume memory with structure-matched synthetic records and state the resulting RSS budget in the delta.
- **Prototype.** A scratch prototype of only the first part, retaining the latest iteration's records, bounded the traced peak at 125/190/193 MB for 1/2/4 iterations and still passed all 68 contract tests.
- **Alternative (if Root declines the code change).** Root must set the combined RSS of resumed launches explicitly: at least the process baseline plus about 0.1 GB, and up to 0.2 GB in the worst case, for each completed iteration on disk.

## 5. Notes (non-blocking)

- **N1. The identity blocks extending an exhausted budget.** `max_iterations` (in solver controls and in `run_arguments`) is part of identity. Extending an exhausted 8-iteration run would discard every completed iteration and start from iteration 0. The arithmetic of completed iterations does not depend on the budget, and `_resume_point` already checks `len(chain) <= max_iterations`. If Root wants deliberate extension (CURRENT_INSTRUCTIONS: "deliberately extend or resume when warranted"), a future version could treat the budget as extendable-only. The same applies to motion-stage-only arguments (pressure/azimuth steps, observation count), which do not affect the gas iteration. This is a design decision for Root, not a defect.
- **N2. The DELTA overstates driver equality with checkpointing off.** Besides `source_pins`, `main()` now emits `numerical_inputs.checkpoint_directory=null` and `numerical_inputs.resume_checkpoint=false`. There is no arithmetic effect.
- **N3. `finish_errors` is buried in the result.** A failure to write the terminal FAILURE or attempt-end record is reported only in `source_fixed_point.checkpoint.finish_errors`, and the driver `status` does not reflect it. Root should require that field to be empty when accepting a run's custody record. A disk or OS error while writing a column record stops the run with an OSError traceback and no JSON result. That is intended (loud), and prior records stay resumable.
- **N4. Boundary identity is indirect.** The boundary callable is not hashed. For the c2v002 driver it is fixed by the driver's sha256. Any other caller of the solver copy relies on the prescription text alone.
- **N5. The environment identity does not pin the BLAS/LAPACK build.** It records the Python version string, numpy version, platform, machine and byte order. A different numpy build with the same version string is caught on resume by the bitwise `prepared` and COMPLETED checks, loudly. Restored columns, however, are not recomputed. Adding `sys.executable` and the numpy package path or build config would close this.
- **N6. A flock can leak inside a long-lived process.** If `solve` raises in a process that keeps the traceback alive (interactive session or wrapper), the lock fd stays open until that traceback is collected. A resume in the same process then fails with CHECKPOINT_IN_USE. This is fail-safe and does not affect the CLI driver, where process exit releases the lock.
- **N7. Pre-existing v009 status mapping, not introduced here.** Iteration-budget exhaustion yields `status='PROVISIONAL_FROZEN_RESPONSE_CIRCULAR_TRIAL'` with `predictions_available=False`, because only a `failure` dict maps to FAILED_SOURCE_PREPARATION. Multi-attempt runs make exhaustion likelier, so Root should read `predictions_available` and `source_fixed_point.checkpoint.outcome` rather than `status` alone.
- **N8. One corrupt record makes the whole checkpoint unusable.** Kill or timeout cannot corrupt a published record. A power loss on macOS (no F_FULLFSYNC) could, and that would make the whole checkpoint unresumable, by design. That is preserved and reported, never silently used, but no salvage path exists.
- **N9. The superseded driver c2v001 sits beside c2v002 with no in-file "do not use" marker.** Only the DELTA says so. Root's launch must pin c2v002 (716bbbfa…3e29).

## 6. Disk, file-count and overhead estimates at 576 columns

These are measured on synthetic records with V008 structural counts.

**Column records:**
- 21.4 KB each for the median structure, 44.1 KB each for the worst case.
- Per iteration directory: 12.4–25.5 MB in 578 files (576 columns, START, COMPLETED).

**Blobs** (content-addressed; fixed source and wavevectors are deduplicated across iterations):
- iteration 0: 11.4 MB in 6 files;
- each later iteration: +8.85 MB in 4 files (gas, current, weighted responses, updated; 2.21 MB each).

**Totals:**
- about 21 MB and 582 files per median iteration;
- for the budget of 8: about 170 MB and about 4,660 files (median), up to about 280 MB (worst case);
- plus 2 small attempt records per attempt.

The volume has 69 GiB free (97% used), so space is ample. Directory sizes (about 580 entries) are unproblematic on APFS.

**Write overhead:**
- 1.3 ms per column (median) to 2.4 ms (worst case), including the exact round-trip and two fsyncs;
- about 0.1 s per START (typed digest of the full prepared dict with 13824 node diagnostics, plus blob writes).

That is negligible against a column solve. **Resume cost** is about 2.5 s of verification per completed iteration on disk, which is acceptable within a 600 s wall. Its memory is B1.
