# REVIEW: cx3r008 delta check, Lens 2 (parity and regression)

Claude4 helper, Claude lineage. Started 2026-10-18T20:06:34Z. This file was written at 2026-10-18T20:44:29Z (`date -u` taken just before writing).

- Authority: dispatch 0617 (`622f5cc99633a2433ce4fb7feebabb6580a468c6660f48377c7c8e48f6bd102d`) and the claim in FROM_CLAUDE4/0097.
- Stance: refute by default.
- Folder: `review_ngc_v011_cx3r008_c4/parity/`. Nothing was written outside it.
- What was not done: nothing was launched, run mode was never used, no project calculation was made, and no NGC3198 target or observed-velocity data, runs_ext tree or C5H path was opened, listed or stat'ed.

## Verdict: PASS_WITH_FINDINGS. 0 BLOCKING, 1 SHOULD_FIX, 6 NOTE

| Claim | Result | Label |
|---|---|---|
| (a) The r007 → r008 AST delta is confined to ST7-SF1, ST7-SF2 and A98.1, and is inert outside NGC | **CONFIRMED** | FORMAL and TESTED |
| (b) Outside NGC, every emitted dry-plan artifact is byte-identical apart from closed substitutions | **CONFIRMED**: all 78 specs, 234 processes, 722/722 files, 0 residual | TESTED |
| (b) Codex3's "934 artifact comparisons pass (377 raw, 557 closed)" | **CONFIRMED where checkable**: 722 recomputed in full from bytes, 34 NGC report-level files token-checked, 178 NGC simulated inputs not opened | TESTED |
| (c) Registry: only the driver pin changes, for the same 8 specs, and every pin resolves | **CONFIRMED for specs and pins** (32/32). Further changes are top-level metadata and the derived report/readiness pins (NOTE PAR8-N4) | TESTED |
| (d) RO1 parity outside NGC, synthetic, sampled | **CONFIRMED**: 18,460/18,460 pairs identical | TESTED and FORMAL |
| PAR-TB-1 closed by A98.1, "r008-specific classes enumerated and byte-pinned" | **REFUTED, narrowly**: one more r008-specific traceback class outside NGC exists and is not enumerated (PAR8-SF1) | TESTED and FORMAL |

## Pins (sha256 from bytes; every one matches the task text)

| Object | sha256 |
|---|---|
| r008 driver `ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py` | 577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377 |
| SELECTED_CX3R008_CX3V002.json | 4c5be34c9812bdf8b3ddf669d544cb449eccc68d180532cde8ffa2e5b14718e4 |
| SPEC_REGISTRY_CX3R008_V002.json | 2c3f421d9a933d1a841f134574984cb0c33e7a0544de0b20514103492214413a |
| A98_1_DISPOSITION_ADDENDUM_CX3V001.md | f9632697961c5549c9401a13a85346068c67d5e896a34d2c4b72f4b1f51e0fcf |
| PAR_TB_A98_1_DISPOSITION_CX3V001.json | a9ae801f7a13f18864200cb99f49ac9241e4d4154b318feb68b86b41a18dc625 |
| HANDOFF_CX3R008_CX3V001.json | 150650fd317ba6752f715b21814b1a151356c8204b3877ac3807a822c1971d15 |
| FROM_CODEX3/0624 | 8085f4be5032493beede70c7f25c47f113ecade065c4208c5e47b6391023029f |
| r007 driver (baseline) | e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69 |
| SPEC_REGISTRY_CX3R007_V001.json | cd30429c27ced0837dc383c00f78899a758fefeeaae2f6134e6aae7fcad18ea2 |
| REVIEW_NGC_V011_CX3R007_C4V001.md | 74d6cd9ed0a784cd71564d498d52e0905b54acb2fbd6c00fe511a8dd3486de1b |
| V005 addendum (A98), an **open** file | cf9bbf19eae3d2fb0262c31c3a0af43ecc2f100b9295c4075a591716b6ebb9dc at 20:07Z; **70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e at 20:47:58Z** (mtime 20:45Z). Root appended A99 (20:20Z) and A100 (20:24Z) during the review. A98's text, re-read at 20:47Z, still says "Any frame class specific to r008 is enumerated and pinned before closure; there is no blanket waiver." The task gave no sha for this file, and every OBJECT pin above still matched at the end |
| Evidence pinned by 0624, all re-hashed | DRY_PLAN_IDENTITY_CX3V001 4954757e…, PAR_TB_R008_DELTA_CX3V001 ab5afb0e…, REGISTRY_VERIFICATION_CX3V002 078ee2f6…, REVIEW_CX3V002 ecc79d49…, DECISION_CX3V002 3e16718f…, ARTIFACT_IDENTITY_VERIFICATION 9af352e8…, MANIFEST_VERIFICATION 6efe6dd4…, HASHES_CX3V002 (implementation) 475f7d30… and (independent) 4feff452… (full values in the RESULTS file) |

**Consistency of the A98.1 successor.** SELECTED V002 and the handoff pin only 577f8c94, the parent is e4f5864a, and the disposition records `source_changed: False`. So A98.1 changed no source.

## Harness

**Interpreter.**
- Command: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (Python 3.12.14, numpy 2.3.5).
- Single-thread BLAS env vars throughout.
- `taskpolicy -b` was accepted and used for the dry-plan batch.

**Fence.** `tools/fence_c4v001.py` is an unchanged copy (f813c430…). `tools/fence_c4v002.py` (3628d8fe…) changes only rule 2's exception; the diff is `tools/FENCE_V001_TO_V002.diff` (9297a65e…).
- It now allows a **read-only** open when, for both the literal and the real path, the only `uvt_`-prefixed component is the final one and it ends in `.py`.
- Both runs_ext roots are tested first, so any uvt_*.py inside a runs_ext tree (UVT_* run trees included) is still refused.
- Still refused: UVT_* directories, uvt_* files that are not `.py` (.pyc, .json), write modes and flags, C5H, target words and NGC3198 data.
- `selftest()` is unchanged.

**Stat sentinel.** `tools/c4p8_common.py` (83a70297…) installs the fence first. It then adds a sentinel that refuses stat, lstat, listdir, scandir, access and chdir on protected literal paths before any syscall, with the same single uvt exception. This also keeps the fence's own realpath() lstat calls (HARNESS-N1 from the r007 review) off protected paths.

**Selftest** (`results/F0_FENCE_SELFTEST_C4P8.json`, TESTED):
- the 8/8 v001 trials are refused;
- the 5/5 v002 positive trials (uvt_*.py read-only) are not refused (FileNotFoundError);
- the 15/15 negative trials are refused: UVT dir component, two uvt components, both runs_ext roots, .json, .pyc, r+/x/O_CREAT, a target-word parent directory, and stat/listdir on runs_ext.

**BLOCKED list.**

| Source | Events | Cause |
|---|---|---|
| Fence, 234 dry plans | 54 | Rule `open(NGC3198 data)`, 18 per tag and identical across A7/S8/B7. Files: the 4 NGC3198-named spec files (2 events each per run), GALAXY_CONFIG_NGC3198_GAL_C2V005.json ×18, NGC3198_FREEZE_SLOTS_CX3V003.json ×12 |
| Fence, selftest | 19 | Intentional |
| Sentinel, dry plans | 0 | The r007 lens had 69 here, all on uvt_*.py |
| Sentinel, selftest | 24 | Intentional |
| Fence, first `tools/g1_results_c4p8.py` attempt (20:49Z) | 1 | `open(NGC3198 data)` on `ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md`, refused by filename. It is root's decisions file, not data, and was read with shasum, grep and sed as the task directs. The attempt aborted before writing, and that file was dropped from the fenced pin list |
| Every other process | 0 | |
| **Fence BLOCKED, total** | **74** | |

- Use of the v002 exception: 414 read-only `'r'` opens of exactly two modules, `tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/{route_b/uvt_route_b_binding_c2v001_r5.py, nodes_v001/route_b/uvt_route_b_binding_nodes_c2v001_r5.py}`.
- Across all 104,175 dry-plan opens: 0 runs_ext opens and 0 target-word or C5H opens.
- There was no `__pycache__` next to either driver, so every import compiled the exact source bytes. `runpy.run_path` always compiles from source.

**Harness artifacts, superseded (not findings):**
- `c2_changed_fn_parity_c4p8.py` v001: its `opens` included linecache reads made after the call, and it compared harness frames. Fixed in v002 (95a960bf…).
- `a1c_nonngc_bytecode_c4p8.py` v001 (97dd0703…) and v002 (80560b6a…): carried line numbers forward onto relocated handler code. Fixed in v003 (70ae7c66…).
- The v001/v002 outputs are kept in `results/` as written.

## (a) AST and bytecode delta, r007 → r008 (FORMAL, with TESTED import effects)

**Build.**
- r008 is r007 with six in-place, line-preserving text replacements, made by Codex3's `implementation/build_successor_cx3v001.py`.
- An appended fragment of 6 new top-level defs sits before the unchanged `__main__` guard.
- r008 has 9,329 lines and 669,113 bytes; r007 has 9,220 lines and 661,973 bytes.

**Tools.** `tools/a1_ast_delta_c4p8.py`, `a1b_delta_detail_c4p8.py`, `a1c_nonngc_bytecode_c4p8_v003.py`, `e1_a98_1_pins_vs_bytes_c4p8.py`.

| r007 → r008 lines | Statement | Closure item | Reachable outside NGC? |
|---|---|---|---|
| 5018 | `_ngc_v011_helper` now returns `_ngc_strict_grid_helper_cx3r008(exec_verified(...))` | SF2 | **No.** Its callers are L5056 and L5066, after normalize_spec's NGC gate at L5043, and L5216, after final_rows_check's gate at L5212 |
| 5145–5147 | `cmd_dry_run`: dispatch gets `_ngc_post=_ngc_finalize_dry_cx3r008`; new `if isinstance(code,tuple):return code[0]`; `rp` is now bound by walrus inside the `if` | SF1 | **Yes, shared, and inert.** See below |
| +5219 / −5224 | `final_rows_check` gets `except Refusal:raise` ahead of the existing handler; one blank line is removed so later def lines keep their numbers | SF2 | **No.** It sits inside the try that follows the L5212 NGC gate. Lines 5219–5223 move +1, all after that gate |
| 9194 | `_ngc_v011_dispatch(fn, spec_path, *args, _ngc_post=None)` | SF1 | It is a def line, so never a frame line. The non-NGC body is unchanged |
| 9205 | NGC branch: `code = fn(...); return (code, _ngc_post(code, *args)) if _ngc_post is not None else code` | SF1 | **No.** It is inside the NGC predicate at L9201 |
| 9218–9326 (new) | `_ngc_helper_sha_cx3r008`, `_ngc_strict_grid_helper_cx3r008`, `_ngc_finalize_dry_cx3r008`, `_cx3r008_helper_{apply_cut,read_cut_record,registered_route_b_nodes}` | SF1 and SF2 | **Definitions only.** Referenced only at L5018 and L5145, and from each other |
| 9220 → 9329 | `sys.exit(main())` guard: AST-equal, moved | A98.1 class | Yes. It is enumerated |

There is no other changed statement. A98.1 itself changed no source.

**FORMAL inertness proof outside NGC.** "Outside NGC" means the dispatch predicate `raw.get('galaxy')=='NGC3198' and 'uv_tail' in raw.get('numerics',{})` is False.

1. **Every other code object is bytecode-identical**, line tables included. The two sources were compiled under one filename and every code object was paired by qualified name.
   - Only these differ: `<module>`, `_ngc_v011_helper`, `cmd_dry_run`#2 (L5144), `final_rows_check`#2 (L5203) and `_ngc_v011_dispatch`#2 (L9194). The 11 new code objects are r008-only.
   - No other code object differs, even in its line table alone.
   - The module-level instruction stream differs only by:
     - the `{'_ngc_post': None}` kwdefault;
     - six `MAKE_FUNCTION`/`STORE_NAME` pairs for the new names;
     - the guard's `POP_JUMP_IF_FALSE` target.
   - So there are no new imports or import-time effects, and no existing name is rebound (`results/A1_AST_DELTA_C4P8.json`, `A1B_DELTA_DETAIL_C4P8.json`).
2. **Non-NGC paths of the three shared changed functions are instruction-identical** after normalization. Normalization compares names rather than slot indices, resolves jump targets to the target instruction, and identifies exception handlers by their content. The comparison covers:
   - `final_rows_check` L5203–5212: 105 instructions, including its exits at L5207, L5211 and L5212;
   - `_ngc_v011_dispatch` L9194–9201 plus L9206: 58 instructions, with the NGC test's false branch landing on L9206 in both;
   - `cmd_dry_run` block B L5148–5162: 141 instructions.

   See `results/A1C_NONNGC_BYTECODE_C4P8_V003.json`.
3. **The remaining shared change, `cmd_dry_run` L5145–5147, is semantically equivalent outside NGC.**
   - The non-NGC branch returns `fn(spec_path,*args)` and ignores `_ngc_post`.
   - `fn` is `_V010_DRY`, which returns only an int. v010 `cmd_dry_run` L3682 returns 2 at L3686, `ngc_dry_run(...)` at L3691, or 0 at L3929. `ngc_dry_run` returns 0 at L4968; its only tuple return, at L4906, belongs to the nested `writer`. The strict copy at L7925 has the same returns. So `isinstance(code,tuple)` is always False.
   - `report_dir` is the str from argparse `--report-dir required=True`, so `Path(report_dir)/'DRYRUN_REPORT.json'` is pure.
   - `rp` is loaded only inside the `if` block (L5148, L5154), and `is_file()` is called exactly when `code==0`, in both versions.
   - The `_ngc_finalize_dry_cx3r008` global lookup cannot fail.
4. **Reachability and introspection.**
   - `_ngc_v011_helper` (L5017) and `final_rows_check` (L5203) are not keys of r007's `_CX3R007_STRICT_BY_LINE`, so r008's edits run on the active NGC path. `cmd_dry_run` L5144 is a key, but it is entered only from `main()` with both flags False.
   - `exec_verified` (L577) builds a fresh `types.ModuleType` each call and caches nothing, so the helper mutation cannot leak.
   - The new names appear in no string constant and not in r007.
   - Every `globals()` iteration runs before the new defs exist (the wrap loop at L9185). `dir(m)` (L3468) iterates exec'd stage modules only.
   - Introspection-site counts are identical between r007 and r008.

**TESTED import effects** (`results/A3_IMPORT_r00{7,8}_C4P8.json`):
- the same 8 new stdlib modules;
- no change to recursion limit, warnings, environment, cwd, numpy error state, profile/trace hooks, excepthook, atexit or signals;
- the same 49 wrapped globals (48 wrapped objects) and identical `_V010_*` alias targets;
- the same 8 import-time opens apart from each driver's own path and .pyc probe path;
- globals: 358 in r007 and 364 in r008, the difference being exactly the 6 new names;
- every common global is unchanged.

**TESTED recursion-limit behaviour** (A98 grants no exception for it). These are the largest harness depths at which the normal outcome still appears, identical under both drivers (`results/E2_RECURSION_HEADROOM_C4P8.json`):

| Entry point | Depth |
|---|---|
| `final_rows_check` (DDO) | 992 |
| dispatch (DDO, stub fn) | 984 |
| `cmd_dry_run` (DDO, stubbed `_V010_DRY`) | 982 |
| `verify_pin` control | 983 |

## (b) Dry plans (TESTED)

**What ran.**
- All 78 specs of SPEC_SET_78 (6b91a8f2; ordered sha 155b1095 recomputed). Codex3's r008 copy is byte-equal to r007's.
- This is a superset of the ≥20-spec spot check and covers every family: B0_GATE 37, V007_REGISTRY 23, V007_SUPERSEDED 2, DERIVED6 6, NGC_REGISTRY_CX3R005 8, NGC_EXTRA_ON_DISK 2.
- 234 fenced processes: A7 = r007, S8 = r008, B7 = r007 again as a determinism control. Each ran through the driver CLI as `__main__`, so the guard was exercised. They ran from 20:23:36Z to 20:25:23Z, 6 at a time.
- Tools: `tools/b1_jobs_c4p8.py`, `dry_one_c4p8.py`, `b2_compare_c4p8.py`. Output: `results/B2_DRY_COMPARE_C4P8.json`.

**Status.**
- 49 completed plans:
  - B0_GATE 19, V007 22, SUPERSEDED 2, DERIVED6 6;
  - **all 23 DDO V007/SUPERSEDED specs that the r007 fence cut short now complete end to end**.
- 15 driver refusals (B0_GATE).
- 14 fence-stopped: 4 NGC3198-named specs (GATE_NGC_* ×3 and V007_21) and the 10 NGC v011 specs. These stopped at the first NGC3198-named config.

**Emitted artifacts.**
- 722 vs 722 files: 331 raw-equal and 391 equal after closed substitution. 0 residual, 0 missing, 0 size changes.
- The substitutions are the r007 → r008 driver path, the full sha, the per-run root, and derived file shas (391 derived pairs).
- In practice the only driver-dependent bytes are `driver_sha256` in the 49 completed DRYRUN_REPORT.json files. No emitted file contains a driver path.
- The determinism control matches 722/722.

**Logs.**
- Exit, exception text, stdout, stderr, the ordered 104,175 opens, fence and sentinel blocks, RO1 watched calls and their callers are all equal.
- The calls to r008-changed functions match the counts expected outside NGC: 0 calls to r008-new functions, 0 active flags at any changed-function call, and 0 strict calls under either driver.
- r008-new functions were called only inside NGC, 6 times (`_ngc_strict_grid_helper_cx3r008` with both flags True).
- Resources: peak RSS was 364.9 MB for r007 and 364.2 MB for r008; summed wall time was 195.8 s and 196.2 s.

**Traceback differences.**
- **Outside NGC:** exactly the two A98.1 r008-specific classes:
  - `GUARD_L9220_to_L9329` ×29;
  - `DISPATCH_CALLBACK_L5145` ×29 (source line plus caret line).

  Frame counts are equal in every case.
- **Inside NGC:** one more frame, the dispatch L9205 source line, in 6 NGC v011 plans (NOTE PAR8-N1).

**Cross-harness reproduction** (`tools/b5_cross_harness_c4p8.py`, `results/B5_CROSS_HARNESS_C4P8.json`).
- For all 64 DDO154 cases under both drivers, my CLI trees reproduce Codex3's direct-call trees: `ngc_cx3r008_closure_cx3/plans/dry_S_v001` for r008 and `ngc_launch_record_strictness_cx3/plans/dry_S_v004` for r007.
- That is 1,444 files: 662 raw-equal and 782 equal after root/derived substitution, with 0 residual. Exit, exception and stdout are all equal.

**Codex3's 934-comparison claim** (`tools/b4_verify_cx3_934_c4p8.py`, `results/B4_VERIFY_CX3_934_C4P8.json`):
- **Recount from the per-file rows** of DRY_PLAN_IDENTITY_CX3V001 (4954757e): 78 cases, 934 = 377 RAW_EQUAL + 557 IDENTITY_ONLY, 61 completed, 17 matched refusals, metadata all true.
- **Token audit: 78/78.** Each case's tokens are exactly the 3 closed ones (driver path, sha, case dir) plus that case's recorded derived-hash proofs.
- **Full recomputation of 722/934 from bytes:** all 64 DDO154 cases, both trees, with my own closure in the r007 → r008 direction. All 722 statuses agree, with 0 sha mismatches against the rows and 0 against the baseline custody manifest (6ef8a6eb).
- **NGC cases (14):** the 34 report-level files (DRYRUN_REPORT, NGC_SOURCE_BUILD_READINESS, DRYRUN_PLAN) all pass:
  - shas match the rows and custody;
  - non-hex text is equal after the 3 closed tokens;
  - the hex map is bijective;
  - every changed token is a recorded derived proof.

  The **178 NGC simulated-input files were not opened**, because they may carry NGC3198 source data. No content of any NGC file was printed.
- **Metadata** recomputed from both logs for 64 cases: all agree.

## (c) Registry (TESTED; `tools/d1_registry_c4p8.py`, `results/D1_REGISTRY_C4P8.json`)

- **Cases.** The same 8 cases in the same order. Every spec pin (path and sha), comparison block and status is unchanged. Per case, only `new_report` and `new_readiness` change; both are derived from the driver and now point at Codex3's r008 `dry_S_v001` trees.
- **Pins.** **32/32 pins resolve from bytes**, sizes included, with none refused.
- **NGC report and readiness pins.** These hold for all 8 cases:
  - the pins equal DRY_PLAN_IDENTITY's candidate rows;
  - each report's `driver_sha256` is 577f8c94;
  - each readiness record's `report` field pins its own r008 report;
  - readiness is `PENDING_CERTIFICATES`, as in r007.
- **Top-level changes** besides `driver` (NOTE PAR8-N4): date_u, schema, parent_registry (cd30429c), dry_plan_identity (4954757e), exact_78_spec_set.path (a byte-identical copy), scope, plus the new keys `diagnostic_disposition` and `supersedes_build_registry` (V001 db2d1fc2, whose cases equal V002's).

## (d) RO1 and changed-function parity outside NGC, synthetic (TESTED)

**RO1** (`tools/c1_ro1_parity_c4p8.py`, `results/C1_RO1_PARITY_C4P8.json`).
- These are the r007 review's matrices.
- A and E are sampled: seed 8008, 3,000 of the 17,640 pin × record × prediction × start combinations. B, C, D and F are complete.
- Two contexts: OUTSIDE and STAGE0_ONLY. The flags stay False in both.
- **18,460/18,460 pairs are identical**, including the ordered read traces: A 12,000, E 6,000, B 288, C 18, D 10, F 144.
- The module RO1 constants are equal.
- FORMAL backing: every RO1 code object is bytecode-identical.

**Changed functions** (`tools/c2_changed_fn_parity_c4p8_v002.py`, `results/C2_CHANGED_FN_PARITY_C4P8_V002.json`).
- **P1, dispatch.** 15 synthetic specs with the NGC predicate False or malformed (dup keys, lowercase galaxy, numerics list/null, bad JSON, BOM, missing file), × 6 stub behaviours. 90/90 are equal, and 90/90 are equal when r008 also gets `_ngc_post`. The post callback never ran.
- **P2, `cmd_dry_run` with a stubbed `_V010_DRY`.** All 8 real behaviours are equal after the root substitution:
  - with no report;
  - with a DDO report;
  - with an NGC-looking report, and with an NGC-looking report carrying duplicate keys (both drivers parse permissively and write equal readiness bytes when the spec predicate is False);
  - with return 2;
  - with a Refusal;
  - with a bad-JSON report;
  - with a report missing `normalized_spec`.

  There are two labelled probes:
  - `PROBE_TUPLE_RETURN`: (0,'x') vs 0, a return the real `_V010_DRY` cannot produce (NOTE PAR8-N2);
  - `PROBE_L5147_STAT_EACCES` (PAR8-SF1).
- **P3, `final_rows_check`.** 351/351 equal across 13 row sets × n_queries {0, 2, 43} × 9 specs. Every case is asserted to stop before the NGC try block, which opens the NGC manifest.

## Findings

### PAR8-SF1, SHOULD_FIX (TESTED and FORMAL): A98.1 misses one r008-specific traceback class outside NGC, `cmd_dry_run` L5147

**Claim.**
- r008 changed L5147 from `if code==0 and rp.is_file():` to `if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():`.
- This line runs in every dry run outside NGC that returns 0 (49/49 completed plans).
- If `Path.is_file()` raises, the top-level dry-run traceback shows the changed source line and a longer caret line. `is_file()` raises for any stat error other than ENOENT, ENOTDIR, EBADF or ELOOP, for example EACCES or EIO on the report the process has just written.
- Exception class and message, frame count and every other frame are identical.
- A98.1 (a9ae801f) and the r008 mapping (`independent/PAR_TB_R008_DELTA_CX3V001.json`, ab5afb0e) pin only L5145 and the guard 9220 → 9329. Neither they nor any other cx3r008 document mentions L5147; the enumeration was built from observed differences.
- A98 requires that *any* r008-specific frame class be enumerated and pinned before closure.

**Reproduction.** Run `python3 -I -B tools/c2_changed_fn_parity_c4p8_v002.py OUT.json` and read `summary.P2_frame_classes.PROBE_L5147_STAT_EACCES == {'cmd_dry_run_L5147_source': 1}`.
- The exceptions are equal: `PermissionError: [Errno 13] Permission denied (C4P8 synthetic probe): <rd>/DRYRUN_REPORT.json`.
- The frames are equal apart from L5147:
  - r007: `[['DRV',6548,'scoped','return original(*args, **kwargs)'], ['DRV',5147,'cmd_dry_run','if code==0 and rp.is_file():']]`
  - r008: `[..., ['DRV',5147,'cmd_dry_run',"if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():"]]`
- The probe makes `os.stat` raise EACCES only when called from `cmd_dry_run` at L5147. It runs on look-alikes in my sandbox.

**Impact.**
- Diagnostic text only.
- It reaches top-level dry-run stderr only, never a saved run-handler traceback or stage stderr (FORMAL: `cmd_dry_run` is on no run-mode or stage stack).
- It was not reached in any of the 234 dry plans; it needs a stat failure on a file the same process just wrote.
- It does not affect use on the NGC launch path. It is a gap in the closure accounting.

**Fix.** A one-line A98.1 addendum pinning this class with the same scope as the L5145 class: r007 text, r008 text, "top-level dry-run stderr only". This needs no code change. A refuter may reasonably assess NOTE, given how hard the class is to reach. It is rated SHOULD_FIX because, as with r007's PAR-TB-1, a literal root requirement is unmet.

### PAR8-N1, NOTE (TESTED): r008-specific traceback frames inside NGC, not enumerated

- L9205's source line changed. It appears in every NGC top-level traceback through the NGC branch: in 6 of my 10 fence-stopped NGC v011 plans, and in any NGC run-mode exception that reaches top level.
- NGC `final_rows_check` lines r007 5219–5223 become r008 5220–5224 (+1, FORMAL). This could appear in NGC run-mode saved tracebacks.
- A98.1 treats new active NGC callback and helper behaviour as intentional, but L9205 also appears for NGC exceptions unrelated to SF1 or SF2.
- It has no bearing on parity outside NGC. Recommend root record both as intentional NGC-internal diagnostics on adoption.

### PAR8-N2, NOTE (FORMAL and TESTED): inertness of `if isinstance(code,tuple): return code[0]` rests on an invariant

- Outside NGC it is inert only because `_V010_DRY` and its strict copy never return a tuple (proof in (a), item 3).
- The P2 probe shows the divergence that a tuple-returning target would cause.
- Recommend recording the invariant: a non-NGC dispatch target must return an int.

### PAR8-N3, NOTE (FORMAL and TESTED): the strict copy `_cx3r007_strict_cmd_dry_run_L5144` (L8361) is stale

- It remains the active-path target of the `cmd_dry_run` wrapper but no longer mirrors r008's original: it calls dispatch without `_ngc_post` and parses the report itself.
- It is unreachable: `cmd_dry_run` is entered only from `main()` with both flags False, and there were 0 strict calls in 234 plans.
- This carries over r007's PAR-N-REACH.

### PAR8-N4, NOTE (TESTED): registry metadata and scope text

- Several items change besides the driver pin; they are listed in (c).
- The V002 scope restores r006's "no calibration admission" and "synthetic RO1 guard correctness claim", which closes r007's PAR-N-REG.
- But it drops "prediction, convergence", which both r006 and r007 stated. "Dry plans only" arguably covers this.
- It also says "the separately pinned r008 frame class" in the singular, while A98.1 pins two r008-specific classes.

### PAR8-N5, NOTE (TESTED): coverage

- By design, my fence keeps the NGC3198-name rule. So 14 NGC3198 specs stop at their first NGC3198-named open, with identical stops across tags.
- 178 of the 934 comparisons, the NGC simulated inputs, were not opened by me. Their equality rests on Codex3's evidence, its parent's evidence, and my token check of the 34 NGC report-level files that reference them by sha.

### PAR8-N6, NOTE (TESTED): Codex3's dry-harness guard is weaker than this fence

- In `plans/dry_one_cx3v001.py`, `prohibited()` refuses target words only when the path also contains `ngc3198`.
- My fully fenced runs of the same 78 specs show 0 target-word opens, and they reproduce Codex3's DDO trees byte for byte. So no such read occurred on these code paths.
- Recommend the stricter guard for future evidence runs.

## Closure status from this lens

- **ST7-SF1.**
  - The change is confined to the NGC branch: the dispatch L9205 callback and `_ngc_finalize_dry_cx3r008` (FORMAL).
  - Outside NGC, `cmd_dry_run` is unchanged (FORMAL and TESTED).
  - The 8 registered NGC readiness records equal r007's under closed substitution, and readiness is unchanged (TESTED).
  - Whether the strict parse itself is correct is for Lens 1.
- **ST7-SF2.**
  - Confined to NGC (FORMAL). The edits are live there because L5017 and L5203 are not wrapped.
  - The helper mutation cannot leak.
  - Outside NGC, `final_rows_check` is 351/351 equal (TESTED).
  - Whether the strictness and Refusal propagation are correct is for Lens 1.
- **PAR-TB-1.**
  - Outside NGC, the observed differences are exactly A98.1's two r008-specific classes (TESTED), and all of A98.1's inherited and r008 pins match the bytes (`results/E1_A98_1_PINS_VS_BYTES_C4P8.json`).
  - But the L5147 class is unenumerated (PAR8-SF1).
  - It closes once A98.1 gains that one-line addendum.

## UNTESTED

- Run-mode parity end to end. There were no launches; run-mode inertness outside NGC is FORMAL only.
- NGC dry plans past the NGC3198 fence stops.
- The 178 NGC simulated-input comparisons.
- The closure correctness of SF1 and SF2 (Lens 1).
- Mutual recursion among wrapped functions.

## Files

- `REVIEW.md`, this file.
- `RESULTS_PARITY_C4P8_V002.json`, the structured results. It supersedes `RESULTS_PARITY_C4P8.json` (657e54f4…), which carries the sha of an earlier REVIEW.md, before the BLOCKED row above was added. Both are generated by `tools/g1_results_c4p8.py`.
- `HASHES.txt`: sha256 of every file under `parity/` except HASHES.txt itself.
- `PARTIAL.md`, the progress log.
- `tools/`: every tool above.
- `results/`: every result JSON.
- `dry/`: 234 logs and trees.
- `trial/`: the V007_0 trial.
- `sandbox/`: synthetic look-alikes only.
