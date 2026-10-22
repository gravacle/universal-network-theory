# VERIFY: PAR8-SF1, refutation attempt (verify_parity_1)

Claude4 helper, Claude lineage. Started 2026-10-18T20:52:51Z. Written 2026-10-18T21:20Z (`date -u` taken just before writing).

- **Authority:** dispatch 0617 (`622f5cc99633a2433ce4fb7feebabb6580a468c6660f48377c7c8e48f6bd102d`) and the claim in FROM_CLAUDE4/0097.
- **Stance:** refute by default.
- **Folder:** `review_ngc_v011_cx3r008_c4/verify_parity_1/`. One file was written outside it: a temporary list of 45 cx3r008 file names for the C6 search, in this session's scratchpad (`/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/scratchpad/cx3r008_docs.txt`). It is left in place because of the no-delete rule. Nothing else was written outside the folder.
- **What was not done:**
  - Nothing was launched, and run mode was never used.
  - No project calculation was made. The only driver executions were dry plans on DDO154 spec V007_0 (8 CLI processes) and calls with stubs on synthetic look-alikes.
  - No NGC3198 target or observed-velocity data, runs_ext tree, UVT_* tree or C5H path was opened, listed or stat'ed.

## Verdict: NOT REFUTED. Reproduced. Severity: SHOULD_FIX (agrees with the finding; documentation level, does not block)

I attacked every sentence of the finding, and each one held from bytes. The class is real, and a real kernel error reaches it, not only the lens's patched `os.stat`. It also has a trigger the finding did not know of: a deterministic one that needs only CLI input (VP1-N1).

There are two refinements, and neither changes the verdict:
- **The fix.** Pinning L5147 alone is enough for synchronous exceptions. Under asynchronous exceptions, L5146 and the dispatch def line L9194 are further r008-specific frame texts (VP1-N2). I recommend pinning the whole three-line SF1 block instead, at the same cost.
- **The scope wording.** "Top-level dry-run stderr only" is narrower than where the text actually lands. Direct-call harnesses save it too (VP1-N3).

| # | Claim in PAR8-SF1 | Result | Label |
|---|---|---|---|
| C1 | r008 changed L5147 from `if code==0 and rp.is_file():` to `if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():` | **CONFIRMED.** Only lines 5145, 5146 and 5147 changed in `cmd_dry_run` (def L5144); 5148–5163 are byte-equal | TESTED (bytes) |
| C2 | The line runs in every dry run outside NGC that returns 0 | **CONFIRMED.** `is_file()` is called exactly when `code==0`. With code 2 the `and` short-circuits, and the outputs are equal. Inside NGC, r008 never reaches L5147: it returns at L5146 | FORMAL and TESTED |
| C3 | `is_file()` raises on any stat error except ENOENT, ENOTDIR, EBADF or ELOOP | **CONFIRMED.** EACCES and ENAMETOOLONG raise. ENOENT, ENOTDIR, ELOOP and an embedded NUL (ValueError) return False | FORMAL (pathlib source) and TESTED (real syscalls) |
| C4 | The traceback shows the changed source line and a different caret line; exception, frame count and every other frame are identical | **CONFIRMED.** In CLI runs the guard line also differs, but that class is already enumerated | TESTED |
| C5 | A98.1 (a9ae801f) and the mapping (ab5afb0e) pin only L5145 and the guard as r008-specific classes | **CONFIRMED.** No class pins 5146 or 5147 | TESTED (bytes) |
| C6 | No cx3r008 document mentions L5147 | **CONFIRMED, with one nuance:** the builder carries the new text as its replacement string. That is code, not an enumeration | TESTED (search) |
| C7 | A98 requires any r008-specific frame class to be enumerated and pinned before closure | **CONFIRMED** | TESTED (bytes) |
| C8 | `cmd_dry_run` is on no run-mode or stage stack | **CONFIRMED** | FORMAL (AST, both drivers) and TESTED (scan of 52 pinned modules) |
| C9 | The class was not reached in the 234 lens dry plans | **CONFIRMED** | TESTED (lens B2 summary) |
| C10 | The reproduction gives `PROBE_L5147_STAT_EACCES == {'cmd_dry_run_L5147_source': 1}` | **CONFIRMED.** Run from a copy in this folder, summary and detail equal the lens's saved result after folder substitution | TESTED |

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
| r008 mapping `independent/PAR_TB_R008_DELTA_CX3V001.json` | ab5afb0e007dcceaf53137c3fe92d1ee0341d68f6765afcd62667046de767979 |
| r007 driver (baseline) | e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69 |
| SPEC_REGISTRY_CX3R007_V001.json | cd30429c27ced0837dc383c00f78899a758fefeeaae2f6134e6aae7fcad18ea2 |
| REVIEW_NGC_V011_CX3R007_C4V001.md | 74d6cd9ed0a784cd71564d498d52e0905b54acb2fbd6c00fe511a8dd3486de1b |
| fence_c4v001.py (source) | f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0 |
| dispatch 0619 (A98 to Codex3: "Pin any r008-specific frame class before closure.") | 238858d12823a153b14dd980d2e2c0a4a71da5c320be054c1fe14832d667ee99 |
| V005 addendum (A98), an **open** file | 70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e from 20:52Z to 21:17:50Z; **27b62183a4c2f4a992d30cfee56e58e395dc2b6e74c85fe73290a26478b9469f at 21:19:12Z**, after root appended A102 (compare r12/r13, unrelated). A98's text, re-read at 21:19Z, is unchanged: "Any frame class specific to r008 is enumerated and pinned before closure; there is no blanket waiver." |

Every pin was re-hashed at the end (`RESULTS_VERIFY_PARITY_1_V002.json`, `all_expected_pins_match: true`).

## Harness

**Interpreter and environment.**
- `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B`: Python 3.12.14, numpy 2.3.5.
- `OPENBLAS/OMP/MKL/VECLIB/NUMEXPR` thread counts are all 1.
- `taskpolicy -b` was accepted for every process.

**Fence.**
- `tools/fence_c4v001.py` is an unchanged copy (f813c430…).
- `tools/fence_c4v002.py` (a2fe9285…) changes only rule 2's exception. The diff is `tools/FENCE_V001_TO_V002.diff` (c72bb956…).
- The new exception allows a read-only open when, for both the literal and the real path, the only `uvt_` component is the final one and it ends in `.py`.
- Both runs_ext roots are tested first, so any uvt_*.py inside them is still refused. The code is identical to the parity lens's v002; only the comments differ.

**Stat sentinel.**
- `tools/vp1_common.py` is a copy of the lens's `c4p8_common.py`, changed only as shown in `tools/C4P8_COMMON_TO_VP1_COMMON.diff`.
- It installs the fence first. It then refuses stat, lstat, listdir, scandir, access and chdir on protected paths before any syscall.
- It also adds `unwrap_stat_only()`. This restores the real `os.stat` only after asserting that the target is inside this folder's sandbox. It was used in 3 processes, each time on a sandbox file.

**Selftest** (`results/F0_FENCE_SELFTEST_VP1.json`):
- 8/8 v001 trials are refused;
- 2/2 v002 positive trials are not refused;
- 10/10 negative trials are refused.

**BLOCKED list.**

| Process | Fence BLOCKED | Sentinel blocked |
|---|---|---|
| Selftest | 15 (intentional: popen, os.system, socket, outside write, runs_ext ×3, UVT ×6, target word, delete) | 18 (intentional, including the fence's own realpath lstat on runs_ext and UVT probes) |
| All 16 other processes (A, B, C2-repro, C, E v001/v002, G, I, d_cli ×6, f_long ×2) | **0** | **0** |
| `vp1_h_results.py` (builds the RESULTS file; imports no driver) | 0: it completed with rc 0, and any fence refusal raises | not saved |

No `__pycache__` exists next to either driver. Every import compiled the exact source bytes.

## What I tested, claim by claim

### C1: the bytes (`tools/vp1_a_bytes_formal.py` → `results/A_BYTES_FORMAL_VP1.json`)

**Lines that differ, r007 vs r008, in the common range.** These are 5018, 5145–5147, 5219–5224, 9194 and 9205, plus the appended fragment from 9218. In `cmd_dry_run`, exactly these three lines changed:

| Line | r007 | r008 |
|---|---|---|
| 5145 | `code=_ngc_v011_dispatch(_V010_DRY,spec_path,report_dir)` | `code=_ngc_v011_dispatch(_V010_DRY,spec_path,report_dir,_ngc_post=_ngc_finalize_dry_cx3r008)` |
| 5146 | `rp=Path(report_dir)/'DRYRUN_REPORT.json'` | `if isinstance(code,tuple):return code[0]` |
| 5147 | `if code==0 and rp.is_file():` | `if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():` |

The builder's `replace_once` (`implementation/build_successor_cx3v001.py` L26–27) is exactly this 3-line → 3-line replacement.

**Instruction positions (`dis`).**
- The `is_file` CALL covers columns 19–31 (`rp.is_file()`) in r007 and columns 19–72 (`(rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file()`) in r008.
- The `Path(report_dir)` CALL and the `/` BINARY_OP sit on L5146 in r007 and on L5147 in r008.

### C3: pathlib (`tools/vp1_b_pathlib_errno.py` → `results/B_PATHLIB_ERRNO_VP1.json`)

- The runtime's `pathlib._IGNORED_ERRNOS` is (ENOENT, ENOTDIR, EBADF, ELOOP). `is_file` re-raises every other OSError and returns False on ValueError.
- Real syscalls in the sandbox:

| Case | `is_file()` |
|---|---|
| Regular file | True |
| Missing (ENOENT) | False |
| File used as a path component (ENOTDIR) | False |
| Self-loop symlink (ELOOP) | False |
| Embedded NUL (ValueError) | False |
| **Directory without search permission (EACCES)** | **raises PermissionError 13** |
| **300-character name component (ENAMETOOLONG)** | **raises OSError 63** |

### C4: real kernel errors, not a patched `os.stat`

**(i) In process** (`tools/vp1_c_inproc_faults.py` → `results/C_INPROC_FAULTS_VP1.json`).
- Setup: both drivers are imported as modules. `_V010_DRY` is stubbed to write a DDO report in the sandbox and return. The spec is synthetic DDO.
- **DIR_NO_SEARCH_EACCES.** The stub runs `chmod(report_dir, 0o600)` after writing.
  - Both drivers raise `PermissionError [Errno 13]` on `<RD>/DRYRUN_REPORT.json`. Frames: 6 vs 6.
  - **The only differing frame is index 2, `cmd_dry_run` L5147**: the r007 text vs the r008 text, carets at columns 19–31 vs 19–72.
  - Traceback text diff:
    ```
    -    if code==0 and rp.is_file():
    -                   ^^^^^^^^^^^^
    +    if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():
    +                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ```
- **Controls**, all equal under both drivers:
  - CONTROL returns 0.
  - DIR_NO_SEARCH_RET2 returns 2, because no stat happens when code is 2.
  - REPORT_MODE_000 (chmod of the report file itself): stat succeeds and the read fails at **L5148**. The frames are identical, which shows the class is specific to the changed line.
  - Symlink loop, missing report, report is a directory: each returns 0.

**(ii) Through the real CLI** (`tools/vp1_d_cli_fault.py`, compared by `tools/vp1_e_compare_cli_v002.py` → `results/E_COMPARE_CLI_VP1_V002.json`).
- Setup:
  - 6 processes: {control, eacces_dir, eacces_file} × {r007, r008}.
  - Each runs `dry-run --spec V007_0 --report-dir …` as `__main__` from the exact driver path, with the **real `_V010_DRY`** writing the real plan.
  - Nothing is caught, so stderr is the default excepthook's.
  - A trace function watching only `cmd_dry_run` L5144 applies the fault at the L5147 line event: after the real report is written, and before L5147 runs.
- **control:** exit 0/0. stdout and stderr are equal. RD trees: 12/12 files, 4 raw-equal and 8 equal after closed substitution (driver path, report dir, driver sha, 8 derived file shas), 0 residual.
- **eacces_dir:** exit 1/1, frames 10/10, last line `PermissionError: [Errno 13] Permission denied: '<RD>/DRYRUN_REPORT.json'` in both. **The stderr diff is exactly two hunks:**
  - `line 9220` → `line 9329` in `<module>`: the A98.1 guard class, already enumerated;
  - the L5147 source line plus its caret line: **PAR8-SF1**.

  The RD trees are equal under closed substitution.
- **eacces_file** (the fault lands at L5148): the only diff is the guard line. This is a negative control.
- 2 of these processes (eacces_dir) used `unwrap_stat_only`, so there is no harness frame between pathlib and the syscall.

### C6: documents

- I searched 44 cx3r008 documents and tools at depth ≤ 2, excluding the driver, plus FROM_CODEX3 0620–0629 and FROM_CODEX 0617/0619. Patterns: the standalone numbers 5146 and 5147, `is_file`, `rp:=`, `walrus`.
- The only hit is the builder's replacement string. No document enumerates or discusses an L5146 or L5147 frame.
- The cx3r008 records explain why. The enumeration was empirical:
  - REVIEW_CX3V001/V002 L17: "All17 refused plans have identical frame counts and exactly one changed source-line string at cmd_dry_run line5145";
  - 0622 L5: "All 17 refusal cases retain the same frame count."
- But refusals happen inside the dispatch at L5145, so a method based on refused plans cannot see a line that runs after the dispatch returns.
- Codex3's own PAR_TB_ROOT_ITEM_CX3V001.md L17 had asked that "added cmd_dry_run selection-frame classes must be separately enumerated and byte-pinned after the candidate exists."

### C8: exposure (FORMAL)

- In both drivers, the name `cmd_dry_run` is loaded only in `main()` (L4987, the `dry-run` branch). It is also used by the module alias `_V010_DRY=cmd_dry_run` (L5000), which names the v010 L3682 function.
- Conservative name-based reachability finds no path to any `cmd_dry_run` def or to `main` from any of these entry points:
  - every `cmd_run` def (L3477, L5163, L9208);
  - `_cmd_run_ngc_cx3v005` (L6014);
  - `stage_main` (L791).

  That reachability maps each global name to every def or alias of that name, and adds the strict table.
- The `_stage` argv branch of `main()` returns `stage_main` before the parser runs.
- `tools/vp1_i_pinned_py_scan.py` read every absolute `.py` path pinned in r008: 52 read, 1 synthetic (`/synthetic.py`) absent, 0 refused. None contains `cmd_dry_run`, `_V010_DRY` or a driver module name.

## Refutation attempts that failed

1. **"An inherited class already covers it."** No. The inherited classes pin lines 6548/6513, 6356/9220/9329, 5134–5141/5163–5168 and 9194–9206/9208–9216. The r008-specific classes pin only L5145 and the guard. None contains 5146 or 5147.
2. **"It is unreachable."** No. A real EACCES reaches it (C4). There is also a trigger that is deterministic and needs no race (VP1-N1).
3. **"It is not specific to r008."** No. The L5147 text exists only because of r008's SF1 edit, and the identical-text neighbour L5148 shows no difference (REPORT_MODE_000, eacces_file).
4. **"Something besides text differs."** No. Exception class and text, errno, exit code, stdout, frame count and all emitted files are equal.
5. **"A98 means only observed classes."** No. A98 says "Any frame class specific to r008", and 0619 says "Pin any r008-specific frame class before closure". A98.1 then asserts "The r008-specific classes were enumerated and byte-pinned before closure", which is literally incomplete.
6. **"It leaks into run mode or stage stderr."** No (C8). That limits the impact; it does not refute the finding.

## Additional observations

### VP1-N1, NOTE (TESTED): a deterministic trigger that needs only CLI input

**What I ran.** `tools/vp1_f_cli_longpath.py`, compared by `tools/vp1_g_compare_longpath.py` → `results/G_COMPARE_LONGPATH_VP1.json`. There is no tracer, no chmod and no monkeypatch.

**Why it triggers.**
- `--report-dir` is passed as `BASE/` followed by 200 copies of `q/../`, then `RD`. That string is 1115 characters, and the literal report path is 1134 > PATH_MAX 1024.
- v010 uses only `os.path.abspath(report_dir)` (L3683). That collapses every `q/..`, so the real dry plan completes in `BASE/RD` and returns 0.
- L5147 builds `Path(report_dir)` from the literal spelling; pathlib keeps the `..` components. Its `stat` therefore fails with ENAMETOOLONG, and `is_file` re-raises it.

**What it gives.**
- Both drivers exit 1, with frames 11/11. One of those frames is the harness sentinel `guarded`, in both.
- The last line is `OSError: [Errno 63] File name too long: …` in both, and equal after substitution.
- **The stderr diff is exactly the guard line plus the L5147 source and caret lines.** The RD trees are equal under closed substitution.

**What this corrects.** The finding said the class "needs a stat failure on a file the same process just wrote". That understates its reach: an unusual but valid argument is enough. The impact is unchanged: diagnostic text only.

### VP1-N2, NOTE (TESTED via a proxy, and FORMAL): asynchronous exceptions expose more r008-specific frame texts outside NGC

**The proxy.** This uses `results/C_INPROC_FAULTS_VP1.json`, Part K. A trace function raises KeyboardInterrupt at one point, standing in for a SIGINT that arrives there. CPython services pending signals at instruction boundaries, including RESUME on function entry and the check after a CALL.

| Point | Result |
|---|---|
| L5146 | Differs: `rp=Path(report_dir)/'DRYRUN_REPORT.json'` vs `if isinstance(code,tuple):return code[0]` (carets at columns 7–11 vs 7–17). **No class covers it** |
| Entry to `_ngc_v011_dispatch` | Differs at the def line **L9194**: `def _ngc_v011_dispatch(fn, spec_path, *args):` vs `…, *args, _ngc_post=None):`. RESUME is located on the def line. The frame also shows L5145 (enumerated). L9194 lies inside A98.1's inherited selector range 9194–9206, but its r008 spelling is new |
| L5147 | The source text differs (the caret line here is the same `code` span) |
| L5148, entry to `cmd_dry_run` | Identical (controls) |

**FORMAL, from the `dis` positions.** A MemoryError, or an interrupt during `Path(report_dir)` or `/`, is attributed to **r007 L5146 but r008 L5147**: the line number moves, not just the text.

None of these can be raised synchronously outside NGC:
- r008 L5146 is `isinstance` on an int;
- r007 L5146 builds a Path from the argparse str;
- a def line runs only RESUME or MAKE_FUNCTION;
- RecursionError cannot first surface there, because the dispatch call that precedes it goes much deeper.

So **PAR8-SF1's single pin is complete for synchronous exceptions.** If root reads "any" as including asynchronous exceptions, the fix must also cover L5146, the line attribution of the Path construction, and L9194. Neither r007's nor r008's enumeration has ever treated asynchronous exceptions as frame classes, so I do not raise this as a finding against A98.1.

### VP1-N3, NOTE (TESTED, bytes): the scope wording

- Codex3's own harness `plans/dry_one_cx3v001.py` L59–62 calls `cmd_dry_run` directly and saves `traceback.format_exc()` and each frame's `source_line`. The lens's `dry_one_c4p8.py` does the same. So the class would also land in saved harness records and in hashes derived from them.
- A98.1's wording for the L5145 class, "Top-level dry-run exception source/caret diagnostics only … excludes run-handler result traceback and stage stderr", already fits this. Use that wording rather than "top-level dry-run stderr only".

### VP1-N4, NOTE (FORMAL): the reproduction as written cannot be re-run in place

- The lens tool runs `mkdir(exist_ok=False)` on `parity/sandbox/chg_c4p8_v002`, which already exists. Running the given command in place therefore stops with FileExistsError before probing, and it would target a folder outside the runner's own.
- It reproduces exactly when copied with `c4p8_common.py` and a fence into a fresh folder, as was done here.

## Severity: SHOULD_FIX

**Why the severity holds.**
- A98 and dispatch 0619 make enumeration a literal pre-closure condition.
- A98.1 and SELECTED V002 record PAR-TB-1 as `CLOSED_BY_ROOT_RULING_A98_1` on the assertion that the r008-specific classes were enumerated, and that assertion is incomplete by one synchronous class.
- The class is reachable both by a fault (EACCES) and deterministically by input (VP1-N1).
- r007's PAR-TB-1 met the same standard at the same severity.

**Why it is no higher.**
- Impact is diagnostic text only: exception, exit code and files are unchanged, and it never reaches run mode or a stage.
- It has the character of root's A101 documentation should-fix items: carried by erratum or addendum, with no code change and no dry-plan rerun.

## Recommended fix (documentation only)

**The addendum.** Add one r008-specific class to A98.1 that covers the whole SF1 replacement block in `cmd_dry_run`:
- **Lines 5145–5147:** all three r007/r008 text pairs (C1 table), their caret lines, and the attribution of the Path construction (r007 L5146, r008 L5147).
- **Scope:** as the L5145 class: top-level dry-run exception source/caret diagnostics, including a harness-saved copy and hashes derived only from it. It excludes run-handler result tracebacks and stage stderr.
- **Evidence:** TESTED here, with the same exception, exit code, frame count and files.
- **Reach:**
  - synchronously at L5147 only, through stat errors outside ENOENT/ENOTDIR/EBADF/ELOOP, for example EACCES, or ENAMETOOLONG from a `--report-dir` whose literal spelling exceeds PATH_MAX;
  - at L5146 only through asynchronous exceptions.

**Asynchronous exceptions.** State in one sentence whether asynchronous exceptions such as KeyboardInterrupt and MemoryError are in scope for frame-class enumeration. If they are, add the dispatch def line L9194 (r007 and r008 spellings).

**For later successors.** Derive enumerations statically from the changed-line set, as in `A_BYTES_FORMAL_VP1.json`. Observed refusals cannot reach lines that run after the dispatch returns.

## Exact reproductions

All commands run from any cwd and need these settings:

```
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
V=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r008_c4/verify_parity_1
```

Each tool refuses to reuse its sandbox or output path. To repeat a run, copy `tools/` into a fresh folder, or pass new output paths.

1. **Fence selftest.** `taskpolicy -b $PY -I -B $V/tools/vp1_f0_fence_selftest.py OUT.json`
2. **Lens probe, copy.** `taskpolicy -b $PY -I -B $V/tools/c2_changed_fn_parity_c4p8_v002.py OUT.json`. Read `summary.P2_frame_classes.PROBE_L5147_STAT_EACCES == {'cmd_dry_run_L5147_source': 1}`. This needs a fresh `sandbox/chg_c4p8_v002`.
3. **Bytes and FORMAL checks.** `$PY -I -B $V/tools/vp1_a_bytes_formal.py OUT.json`
4. **pathlib errno table.** `$PY -I -B $V/tools/vp1_b_pathlib_errno.py OUT.json`
5. **Real EACCES in process, plus the async proxy.** `$PY -I -B $V/tools/vp1_c_inproc_faults.py OUT.json`. Read `summary.DIR_NO_SEARCH_EACCES` and `summary.KI_*`.
6. **Real CLI.** For each mode in `control eacces_dir eacces_file` and each tag in `r007 r008`:
   ```
   $PY -I -B $V/tools/vp1_d_cli_fault.py $tag $mode $V/sandbox/d_cli/$mode/$tag/RD $V/results/d_cli/${mode}_${tag}.state.json > $V/results/d_cli/${mode}_${tag}.stdout.txt 2> $V/results/d_cli/${mode}_${tag}.stderr.txt
   ```
   Then `chmod 755` the two eacces_dir RDs and `chmod 644` the two eacces_file reports, and run `$PY -I -B $V/tools/vp1_e_compare_cli_v002.py OUT.json control:0:0 eacces_dir:1:1 eacces_file:1:1`.
7. **Long report-dir.** For each tag in `r007 r008`:
   ```
   $PY -I -B $V/tools/vp1_f_cli_longpath.py $tag $V/sandbox/f_long/$tag 200 $V/results/f_long/longpath_$tag.state.json > $V/results/f_long/longpath_$tag.stdout.txt 2> $V/results/f_long/longpath_$tag.stderr.txt
   ```
   Then run `$PY -I -B $V/tools/vp1_g_compare_longpath.py OUT.json 1 1`.
8. **Pinned-module scan.** `$PY -I -B $V/tools/vp1_i_pinned_py_scan.py OUT.json`

Superseded harness output, kept as written: `results/E_COMPARE_CLI_VP1.json`, from v001 of the comparer. It lacked derived-sha closure and so showed 2 residual RD files per mode. v002 closes them with 8 derived pairs and 0 residual. This is not a finding.

## UNTESTED

- Run-mode behaviour end to end (no launches; C8 is FORMAL).
- Delivery of a true asynchronous signal at L5146 or L9194 (VP1-N2 uses a raise from a tracer as a proxy).
- EIO and ESTALE stat failures; only EACCES and ENAMETOOLONG were produced.
- NGC dry plans. They are not needed, because r008 never reaches L5147 inside NGC (FORMAL).

## Files

- `VERIFY.md` (this file).
- `RESULTS_VERIFY_PARITY_1_V002.json` (6091f4f678e0a4f1c701725a38e1f2e27dc81e41f9e5eaded9bbc4301e66782c): structured claims, the pins re-hashed from bytes, the BLOCKED list per process, and shas of every tool and result. It supersedes `RESULTS_VERIFY_PARITY_1.json` (9974802d…, kept as written), whose `not_done` wrongly said nothing was written outside this folder; V002 adds `writes_outside_folder`.
- `REVIEW.md`: a pointer to this file.
- `PARTIAL.md`: the progress log.
- `HASHES.txt`: sha256 of every file here except HASHES.txt itself. The sandbox holds three intentional self-loop symlinks, the ELOOP look-alikes; they are listed by their link text, and any walker should not follow them.
- `tools/`, `results/`: the tools and their outputs.
- `sandbox/`: synthetic look-alikes and the DDO dry-plan trees.
