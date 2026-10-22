# INTERFACE_V007: route-B driver `galaxy_m0_forward_c2v007.py` (Claude2 lane `driver_v007_c2`)

## Status

READY_FOR_CHECK. Nothing has been launched on real inputs. The two deciding tests are below; root launches them.

## Files (sha256 from bytes; the full list is in HASHES.txt)

| File | sha256 |
|---|---|
| `galaxy_m0_forward_c2v007.py` | `0338584b4ba8d12609aa3b95f422845a86fb09379de65e2e9980a72bd44e3d4c` |
| `DIFF_V006_V007.diff` (`diff -u` from v006 `c53997b4` to v007) | `933d234fd6429bcc78c8e77755467cae44a49b83feeb4b3fa22e1d6df0cb48b7` |
| `deciding/CALL_A2_ANCHOR_F10_ROUTE_A_PARALLEL_N8_C2V007.json` | `038c43980091ddd65d3d57d445cacdb4275918aee0967991b7bea4e022bbe79d` |
| `deciding/compare_deciding_ii_c2v007.py` | see HASHES.txt |
| `deciding/LAUNCH_DECIDING_I_C2V007.json`, `deciding/LAUNCH_DECIDING_II_C2V007.json` | see HASHES.txt |

Base: v006 `c53997b4`. The four fixes come from v003c `ed326130`; the cited hunks are in `absorb_c2_0473/driver_f/DIFF_V003B_V003C.txt`.

## What v007 changes (nothing else)

### (a) The four v003c RD1 fixes, ported onto the v006 structure

**F1: a route A with no fixed point gets its own status.**
- The route-A outcome is classified from the attempt's own `result.json`. `route_a_outcome_record` is verbatim from v003c.
- No fixed point raises `RouteANoFixedPoint`. The run then ends with status `ROUTE_A_NO_FIXED_POINT`, not `BLOCKED`. `result.json` carries `route_a_outcome` for every status.
- This is checked before v006's strict reader. Without that ordering, a non-converged checkpoint would end as `ROUTE_A_ITERATION_AMBIGUOUS`.
- Adaptation: v006 has no iteration-4 lock. v003c's rule "converged at k≠4 → `Blocked ROUTE_A_ITERATION_NOT_4`" therefore becomes "the converged iteration in result.json differs from the strict reader's iteration → `Blocked ROUTE_A_ITERATION_MISMATCH`".
- An inconsistent record (flag converged, token not) raises `StageFailed ROUTE_A_RESULT_INCONSISTENT`.

**F2: absolute paths.**
- The run outdir and the dry-run report dir go through `os.path.abspath`. This is lexical and resolves no symlinks.
- `run_stages` refuses, in every mode, any request whose path values or stage dir are relative (`RELATIVE_PATH_IN_REQUEST`).
- Adaptation: v006's sentinel `NONE_IN_REVIEWED_CODE…` is skipped, like `PENDING…`, through `_has_pending`.

**F3: canonical override keys.**
- The keys of `fs_absolute_overrides`, `rfs_factor_overrides`, and the pass and index keys of `le_factor_overrides` must match `0|[1-9][0-9]*`.
- The lookups are unchanged (`str(i)`) and are now consistent with the keys.

**F4: background μ/C custody.**
- `route_a_custody` checks the coefficient npz `background_mu`/`background_C` against the checkpoint's `fourier_arguments.mubar/Cbar` digests and against the caller `physical_parameters` arrays. These are the same checks offset v003 makes (`Frozen background mismatch`).
- A mismatch blocks with `ROUTE_A_BACKGROUND_MISMATCH` before any route-B stage.

### (b) Optional parallel route A for DDO154

Call spec field: `numerics.route_a = {"column_workers": N}`.

**Values of N:**
- N must be an `int`, not a `bool`, in 1..64. Anything else is a `Refusal`, and so are unknown keys and a non-object value.
- **Absent, or N=1:** the reviewed serial worker `c4cb6826` with the reviewed solver `44d9c23c`. The request is byte-identical to v006, and a spec without the field normalizes exactly as in v006.
- **N>1:**
  - `script` is the parallel worker `9dbdaf11`.
  - `--solver`/`--solver-sha256` point to the parallel solver `aed4dd59`.
  - `--column-workers N` is appended.
  - Everything else is unchanged: seed, checkpoint module, outdir, the prep `COEFFICIENT` module patch, and the prep-v008 `LOCAL['prep']` item. The worker keeps the same `LOCAL` keys.

**When the option is refused:**
- N>1 together with `admit.route_a`, because that route A would never run.
- `numerics.route_a` on an NGC3198 route-B spec (unknown key). This driver never runs NGC route A.

**Pins:** the two parallel files are pinned in `all_static_pins` and in the dry-run transitive scan only when N>1.

**Admission downstream:**
- A route A from the parallel worker is admitted by the same code path as the serial one: `route_a_custody` → strict reader → per-call `custody.checkpoint_identity_sha256` and `route_a.accepted_iteration`.
- No route-B stage reads `IDENTITY` `code`, a solver sha or a worker sha. This was checked by grep of all 11 gal_c2v004 stages and the reuse module: 0 hits.

**Identity fields that differ, and how custody records them:**

| Field | Serial | Parallel | Recorded by v007 |
|---|---|---|---|
| checkpoint `IDENTITY.identity.code.solver.{path,sha256}` | `…/resumable_coupled_gas_0422/…_c2v001.py`, `44d9c23c` | `…/parallel_route_a_c2/…_parallel_c2v001.py`, `aed4dd59` | `identity.route_a.custody.solver_code`, read from IDENTITY bytes. For a route A computed in run mode it must equal the launched solver, else `Blocked ROUTE_A_SOLVER_MISMATCH`. For an admitted route A, or in simulate mode, it is recorded only. |
| `identity_sha256`, and every record's `payload_sha256`/`identity_sha256`/`iteration_start_sha256` | — | differ as a consequence | per-call `custody.checkpoint_identity_sha256` (already per call in v006) |
| caller `worker.{path,sha256}`, caller `code_pins` solver key | `c4cb6826` | `9dbdaf11`, parallel solver path | `identity.route_a.implementation` = `{column_workers, kind REVIEWED_SERIAL / PARALLEL_C2V001, worker, solver}` (computed mode) |
| attempt `start.json` | — | adds `column_workers` | in the stage outputs |

- `N` is not identity: a killed parallel run resumes with any N (CHECK_V001).
- A serial checkpoint and a parallel checkpoint are not cross-resumable. This driver never resumes (`--start-iteration 0`, no `--resume`).

### One deliberate non-change

- `per_call_seed` keeps the annotation literal `'galaxy_m0_forward_c2v006'`. The seed-composition code is unchanged, so v007 writes the byte-identical seed and therefore the byte-identical `--seed-sha256` of v006.

## Hunk-by-hunk justification (`DIFF_V006_V007.diff`)

| # | Hunk (v006→v007) | Content | Justification |
|---|---|---|---|
| 1 | `-1,4 +1,21` | Docstring c2v007 section | documentation |
| 2 | `-174,6 +191,16` | `PARALLEL_ROUTE_A` pins (`9dbdaf11`, `aed4dd59`), `ROUTE_A_COLUMN_WORKERS_MAX=64` | (b) |
| 3 | `-324,6 +351,18` | `class RouteANoFixedPoint` | F1, v003c `@@ -207`; the docstring is corrected per v003c CHECK D2 (only returned outcomes; raised errors → FAILED_AT_STAGE) |
| 4 | `-599,6 +638,29` | `_canon_key`; `normalize_route_a_numerics`; `route_a_column_workers` | F3, v003c `@@ -482`; (b) validation |
| 5 | `-638,7 +700,7` | numerics allowed keys + `route_a` | (b) |
| 6 | `-697,17 +759,17` | `isdigit` → `_canon_key` at the 3 validation sites; refusal text names the key | F3, v003c `@@ -577` (verbatim) |
| 7 | `-740,6 +802,8` | `out_num['route_a']` only when declared | (b); keeps default normalization identical |
| 8 | `-752,6 +816,8` | refuse N>1 with `admit.route_a` | (b) fail-closed |
| 9 | `-804,6 +870,8` | comment only (seed annotation kept) | byte-identical seed |
| 10 | `-812,6 +880,54` | `_relative_request_paths` | F2, v003c `@@ -865`; sentinel via `_has_pending` (adaptation) |
| 11 | `-829,6 +945,7` | `Ctx.route_a_outcome` | F1, v003c `@@ -882` |
| 12 | `-873,6 +990,11` | `run_stages` relative-path refusal | F2, v003c `@@ -926` (verbatim) |
| 13 | `-920,11 +1042,78` | `ROUTE_A_CONVERGED`, `route_a_outcome_record` (verbatim), `require_route_a_fixed_point` (iteration rule adapted), `route_a_custody(…, outcome, expected_solver)` signature and docstring | F1, v003c `@@ -973`; (b) |
| 14 | `-937,9 +1126,27` | background μ/C check; F1 before the reader; solver_code; reader iteration vs result.json | F4, v003c `@@ -993` (verbatim check); F1 ordering; (b) |
| 15 | `-949,7 +1156,8` | custody returns `solver_code` | (b) custody record |
| 16 | `-1672,34 +1880,58` | route-A request built with the N=1 / N>1 branch; `implementation` record; F1 classification before custody; outcome-first when IDENTITY is absent; `route_a_rows` from the already-read result | (b); F1, v003c `@@ -1229` (adapted to v006's NGC branches: the NGC `IDENTITY`-missing refusal is kept, after the outcome check) |
| 17 | `-2108,6 +2340,9` | `all_static_pins` + parallel pins when N>1 | (b) |
| 18 | `-2185,7 +2420,10` | `cmd_run` abspath outdir | F2, v003c `@@ -1653`; the comment is corrected per CHECK D3 (lexical normalization) |
| 19 | `-2267,6 +2505,9` | `except RouteANoFixedPoint` → status `ROUTE_A_NO_FIXED_POINT` | F1, v003c `@@ -1715` |
| 20 | `-2276,6 +2517,8` | `result['route_a_outcome']` | F1, v003c `@@ -1724` |
| 21 | `-2376,7 +2619,7` | dry-run abspath report dir | F2, v003c `@@ -1812` |
| 22 | `-2389,7 +2632,9` | transitive scan + parallel roots when N>1 | (b) |

## Tests (synthetic, simulate and replay only; no real forward or route-A run)

Every test ran with `nice -n 10`, `OMP/VECLIB/OPENBLAS=1` and at most 3 spawned workers. Every guarded run used `tests/guard_c2v007.py`, which:
- refuses process creation;
- allows writes only inside this lane;
- under CLAUDE2/runs, allows only reads of A2_ANCHOR_F10_RUN_V001 and REPRO_PINNED_*.

| Suite | Result file | Count | Verdict |
|---|---|---|---|
| Dry runs of v006 and v007 (23 runs) and their comparison | `tests/runs/COMPARE_DRY_C2V007.json` | 18/18 PASS | see below |
| Unit and run-mode tests | `tests/runs/unit_try1/TEST_RESULTS.json` | 56/56 PASS | |
| Shim + spawn (synthetic) | `tests/runs/shim/SHIM_RESULTS.json` | 5/5 PASS | |
| Comparator fixtures | `tests/runs/comparator/fixtures/FIXTURE_RESULTS.json` | 11/11 PASS | |
| Comparator self-test, A2F10 against itself | `tests/runs/comparator/SELFTEST_A2F10_VS_A2F10.json` | 12/12 checks, PASS_BITWISE_EQUAL | |
| v006 suite (27 tests) run on v007 | `tests/runs/v006_suite_on_v007_*/TEST_RESULTS_C2V006.json` | 27/27 PASS | no regression |

**Default numerics give byte-identical requests: TESTED-POSITIVE (D1).**
- The specs: root's v006 deciding spec ADMIT_PREFIX_C2V005 (`4ac5527a`), ADMIT_ROUTE_A_C2V005, ADMIT_PREFIX_C2V001, PINNED_FULL_C2V001, RULE_FULL_C2V001, the A2F10 anchor spec (which includes a computed route-A request), and both NGC3198 templates.
- For every spec, every planned stage request (script, sha, argv, globals, patches, mask, dict items, galaxy-config meta) is identical between v006 and v007. This holds after the run's own report-dir prefix is replaced by `<RD>`, and after the digest of a dry-run file that embeds its own report dir (the PENDING placeholder probes) is taken over its normalized bytes.
- Generated inputs, the normalized spec and the remaining refusals are identical.
- Explicit `route_a.column_workers: 1` gives requests identical to the default.

**Parallel command: TESTED-POSITIVE (D2), at N = 2, 8 and 64.**
- The route_a request differs from default in exactly: `script`/`script_sha256` (`9dbdaf11`), `--solver`/`--solver-sha256` (`aed4dd59`), and the appended `--column-workers N`.
- All other requests and inputs are identical.
- Static pins add exactly the two files. The transitive scan covers 42 files with 0 problems and 0 scipy imports.
- **Refused:** N of 0, 65, -1, `true`, `8.0`, `"8"`, `null`, an extra key, a non-object, N>1 together with admit.route_a, and route_a on an NGC spec.

**F1: TESTED-POSITIVE.**
- The synthetic solver-shaped returns classify correctly: converged, budget exhausted, HI failure at iteration 2 column 13, HI failure at iteration 0, inconsistent, and an unreadable layout.
- Run mode with admitted synthetic attempts (no stage executed; a second barrier replaces `subprocess.Popen`):

| Case | v007 | v006 baseline |
|---|---|---|
| no fixed point + IDENTITY-only checkpoint | `ROUTE_A_NO_FIXED_POINT` | `BLOCKED` (`ROUTE_A_ITERATION_AMBIGUOUS`) |
| HI failure | `ROUTE_A_NO_FIXED_POINT`, with the failure text | — |
| converged at 3 + saved checkpoint (reader 4) | `BLOCKED ROUTE_A_ITERATION_MISMATCH` | — |
| inconsistent | `FAILED_AT_STAGE` | — |

- The saved V002 attempt and the A2F10 attempt classify CONVERGED at iteration 4.

**F2: TESTED-POSITIVE.**
- A relative run outdir resolves to the absolute path, and finish.json records absolute paths.
- A relative dry-run report dir gives a plan identical to the absolute-dir plan. v006 plans 52 relative argv paths in the same case.
- `run_stages` refuses a relative argv path and a relative stage dir, and accepts the `PENDING`/`NONE_IN_REVIEWED_CODE` sentinels.

**F3: TESTED-POSITIVE.**
- Refused: `'05'`, U+0665, U+2075, `'071'`, `'+5'`, pass key `'01'`, index `'03'`.
- Accepted: `'0'` and canonical le keys.
- In the v006 baseline, `'05'` is accepted and silently dropped: column 5 gets the nominal bracket `[1.5125e8, 3.025e8]` instead of the declared one.

**F4: TESTED-POSITIVE.**
- A one-ulp change to μ or to C, with the same grid, gives `BLOCKED ROUTE_A_BACKGROUND_MISMATCH`:
  - on an IDENTITY-only checkpoint, before the strict reader (a byte-identical copy reaches the reader instead);
  - on the saved V002 checkpoint;
  - in run mode, with 0 stage records.
- The saved V002 checkpoint (fe5a2f06) and the A2F10 checkpoint (2e3a36d8) pass custody.

**Solver custody: TESTED-POSITIVE.** The A2F10 checkpoint passes with the expected serial solver, and is refused (`ROUTE_A_SOLVER_MISMATCH`) when the parallel solver is expected.

**Seed: TESTED-POSITIVE.** Under v007, the A2F10 seed equals the saved A2F10 seed except for the annotation, and numerical_inputs are bitwise equal.

**Shim + spawn: TESTED-POSITIVE (synthetic).**
- The parallel solver was called from a stage executed by v007's `_stage` shim. The shim's main is the driver, and spawned workers re-import it as `__mp_main__`.
- At N=1, 2 and 3 it is bitwise equal to the reviewed solver in output, progress, checkpoint records and blobs. IDENTITY differs only in `code.solver`.
- A shim `module_patches` override of a closure-read global reaches the spawned workers.

## Deciding tests (real runs; root launches)

The launch records hold the exact command arrays: `deciding/LAUNCH_DECIDING_I_C2V007.json` and `deciding/LAUNCH_DECIDING_II_C2V007.json`. The environment is `OMP/OPENBLAS/MKL/NUMEXPR/VECLIB/BLIS_NUM_THREADS=1`; the monitor sets these itself.

### (i) DDO154 ADMIT_PREFIX bitwise reproduction, default numerics

This is the same test as v006's; only the driver sha differs.

```
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py \
  --driver /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v007_c2/galaxy_m0_forward_c2v007.py \
  --driver-sha256 0338584b4ba8d12609aa3b95f422845a86fb09379de65e2e9980a72bd44e3d4c \
  --spec /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_impl_c2/binding/specs/CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json \
  --outdir "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_ROUTE_B_C2V007_DECIDING_ADMIT_PREFIX_RUN_V001" \
  --receipt "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_ROUTE_B_C2V007_DECIDING_ADMIT_PREFIX_RUN_V001.receipt.json" \
  --wall-cap-s 14400 --rss-cap-bytes 3221225472 --output-cap-bytes 8589934592 --poll-s 2.0
```

- Spec: `CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json`, sha256 `4ac5527ad1731353d798c2648adc1033335a12102ec071b3ae6a619334313cb7`.
- **PASS requires all of:**
  - `finish.json` status is COMPLETED.
  - `result.json` `deciding_test.verdict` is `PASS_BITWISE_EQUAL`.
  - `route_a_outcome.classification` is CONVERGED with `converged_iteration` 4.
  - `identity.route_a.custody` has `iteration` 4 and `solver_code` `44d9c23c`.
- This test does not exercise the parallel option, because route A is admitted.

### (ii) Full DDO154 call at the A2 F10 anchor spec with `numerics.route_a.column_workers = 8`

```
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py \
  --driver /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v007_c2/galaxy_m0_forward_c2v007.py \
  --driver-sha256 0338584b4ba8d12609aa3b95f422845a86fb09379de65e2e9980a72bd44e3d4c \
  --spec /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v007_c2/deciding/CALL_A2_ANCHOR_F10_ROUTE_A_PARALLEL_N8_C2V007.json \
  --outdir "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V007_DECIDING_RUN_V001" \
  --receipt "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V007_DECIDING_RUN_V001.receipt.json" \
  --wall-cap-s 14400 --rss-cap-bytes 8589934592 --output-cap-bytes 8589934592 --poll-s 2.0
```

After the run, compare:

```
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v007_c2/deciding/compare_deciding_ii_c2v007.py \
  --reference "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001" \
  --new "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V007_DECIDING_RUN_V001" \
  --column-workers 8 \
  --out "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V007_DECIDING_RUN_V001.COMPARE_DECIDING_II_C2V007.json"
```

**The spec** (`038c4398`) is the A2F10 spec `a93c95b9` with only `label` changed and `numerics.route_a = {column_workers: 8}` added. Its dry run is in `deciding/dry/DRY_II_A2F10_N8`.

**Caps:**
- RSS cap 8 GiB. The serial A2F10 tree peaked at 1.45 GB; 8 workers add 0.36–0.55 GB each, measured.
- Output cap 8 GiB. A2F10 peaked at 6.08 GB.

**PASS requires** compare verdict `PASS_BITWISE_EQUAL`, with all of these checks:

Route-A outputs:
- **RA_BLOBS:** the checkpoint `blobs/*.npy` are byte-identical.
- **RA_RECORDS:** every iteration record passes the checkpoint module's own integrity read, and is equal once `attempt`, `payload_sha256`, `identity_sha256` and `iteration_start_sha256` are dropped.
- **RA_IDENTITY:** the self-hash verifies on both sides. The identity is equal after only the expected substitutions. Ref code.solver is `44d9c23c` and new is `aed4dd59`. The caller worker is `c4cb6826` for ref and `9dbdaf11` for new.
- **RA_SEED:** the two seeds are equal except the annotation.
- **RA_END:** the end-record outcome and `records_written` are equal.
- **RA_RESULT:** the attempt `result.json` is equal after the substitutions, with `elapsed_seconds` dropped and NPZ file digests replaced by array-content digests.
- **RA_ARRAYS:** `arrays/*.npz` arrays are equal bytewise.
- **RA_NODES:** `node_diagnostics` are equal after the substitutions.
- **RA_START:** `start.json` is equal except `column_workers`, which must be 8, and the seed annotation.
- **RA_FINISH:** finish status is RETURNED_ACTUAL_RESULT on both.
- **RA_ROWS:** `route_a_rows` are equal.

Speeds:
- **SPEEDS:** COMPLETED and valid on both; `speeds_km_s` (12) equal as exact floats; `rows`, `final_pass`, and every pass's rows and `max_abs_change_km_s` equal.

New-run custody:
- **NEW_CUSTODY:** `implementation` is PARALLEL_C2V001 with N=8; `custody.solver_code` is `aed4dd59`; `route_a_outcome` is CONVERGED at the reader's iteration.

**Expected to differ:** code.solver; caller.worker; the caller code_pins solver and seed keys; the seed path and sha (`f7c6b40c` vs `059b4a16`, which is the annotation only); identity sha and the identity-bound record fields; attempt tokens; NPZ file bytes (zip timestamps); `start.json` `column_workers`.

**Comparator status: TESTED-POSITIVE on fixtures** (baseline PASS; 10 single mutations each fail at the named check) **and on A2F10 against itself.**

**How to read the outcome:**
- All checks pass: the parallel option may be used.
- RA_* pass but SPEEDS fails: the cause is route-B lineage (driver c2v001→c2v007 at this rule-mode spec), not the parallel route A. Read it together with (i). A serial control (the same spec without `numerics.route_a`) would localize it.
- Any RA_* fails: TESTED-NEGATIVE for the option.

## Open items (not changed, by scope)

- **UNTESTED: v003c CHECK D1.**
  - The admitted attempt is not tied to the admitted checkpoint, i.e. `source_fixed_point.checkpoint.identity_sha256` is not compared with IDENTITY. F1 makes the attempt decision-relevant, and the run-mode test NFP_SAVEDCKPT shows that a no-fixed-point attempt paired with a converged checkpoint ends as `ROUTE_A_NO_FIXED_POINT`.
  - A computed route A is unaffected.
  - Deciding test: the same pairing must refuse once the linkage check is added (a candidate for v008).
- **UNTESTED for NGC3198.**
  - F1 reads the NGC route-A `result.json` with the DDO layout (same binding, prediction and solver return types). An unreadable layout fails closed with `StageFailed ROUTE_A_RESULT_UNREADABLE`.
  - Deciding test: the v007 dry run of the filled NGC route-B spec on the real NGC A2F10 route-A bytes must show `identity.route_a.outcome.classification == CONVERGED`.
- **Not addressed.** Claude4 0030 A2 (NGC route-A rows must not be used as calibrated predictions; the reader `ngc_read_route_a_result` is unchanged) is outside this task. NGC route A is not run by this driver, and the parallel option is DDO-only.
- **Rule note.**
  - Inside this lane's own output directory, three of my own test outputs were renamed or moved: `tests/runs/COMPARE_DRY_C2V007.json` → `_try1`, `tests/runs/logs/compare_dry.json` → `_try1`, and `tests/runs/shim_try1` → `tests/runs/superseded/`.
  - The first try was superseded because of a comparator normalization issue, and the second because of an S0 check that counted synthetic argv tokens.
  - Nothing was deleted, and nothing outside this lane was moved.
