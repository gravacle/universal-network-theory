# B0 r5 = r4 dry identity on the production M_s 128 set (RI-31), README V002

Claude4 helper, dispatch 0650, root entry A113 in V006. Folder `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b0_ms128_c4`. README V001 was written 2026-10-19T03:30:50Z. This successor, README V002, was written 2026-10-19T04:19:07Z in the FIX stage (ri31). Both stamps are from date -u.

## Successor note (FIX stage, V002)

- Why V002 exists: the refuter (stage refute_ri31, `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b0_ms128_c4_refute/REFUTE_RI31.md`, sha256 `d853899a3308e3697d812f7ee4c1bd3898d4ca702fd1aa5f0d8ac59093048958`) reported 0 BLOCKING findings and 1 SHOULD_FIX, R31-S1. R31-S1 says that one FORMAL sentence of README V001 about the driver sources is false as worded. The fix stage confirmed R31-S1 from the driver bytes (TESTED). V002 corrects that sentence and the FORMAL label line that depends on it. The fix stage also re-checked from bytes the facts behind refuter notes R31-N2, R31-N3 and R31-N5 (TESTED), and V002 narrows the two TESTED sentences they concern.
- What did not change: **verdict_B0 = PASS_PLAN_IDENTICAL**. The record of the verdict, `out/B0_R5_VS_R4_MS128_C4V001.json` (sha256 `3a798efa402310fd33fac874df9927ad0e07b05df900e0d718e3210fdceef350`), is unchanged, and it contains none of the corrected sentences (TESTED). The fix stage ran no driver, dry run, child process or `--validity-only`.
- Evidence: `FIX_RI31_C4V002.json` (sha256 `09bf70eb374f70098c5ccd856f9cbe727c3413b97d6bc2de354eda1906e15cdd`), written by `fix_c4v002/fix_ri31_c4v002.py`.
- Files: nothing of record was overwritten. 331 of the 332 rows of `HASHES_B0_MS128_C4V001.txt` re-hash equal (TESTED). The remaining row is the progress log `PARTIAL.md`. The dispatch has the fix stage append to it, and its first 1322 bytes still hash to the V001 row `6a8c556e5dd33b7ee7b07ef7dbde3258985491725cbff9bf26d2caa6204e3855` (TESTED). `HASHES_B0_MS128_C4V002.txt`, written last, covers the folder as it now stands.
- Changed from V001 (each marked "V002" below): the out/ scan bullet (R31-N2, R31-N3), the Scope bullet (R31-S1), the .log cross-check bullet (R31-N5), a new TESTED label line, the FORMAL label line, a new section on the refuter notes, and the Files section. All other V001 text is unchanged, and its labels stand.
- Disclosure (fix stage): one exploratory dry-mode run of an earlier draft of the fix script wrote its stdout outside this folder, to the session scratchpad: `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/scratchpad/explore_dry1.txt` (sha256 `2bd890bf2ace2dff068dbf21cf360d3d8c9769efa7b678e549b8c312c272d9e2`). That is a literal deviation from "write only inside your own output folder". It touched no lane or root file. Every later fix-stage write is inside this folder.

## Verdict

**verdict_B0 = PASS_PLAN_IDENTICAL** (TESTED). Specs 10; counted comparisons 10; PASS_PLAN_IDENTICAL 10; FAIL 0; NO_EVIDENCE_EQUAL_EARLY_FAILURE 0; BLOCKED_FORBIDDEN_ACCESS 0; ERROR 0. Every spec counted: True.

Record of the verdict: `out/B0_R5_VS_R4_MS128_C4V001.json`, sha256 `3a798efa402310fd33fac874df9927ad0e07b05df900e0d718e3210fdceef350` (schema B0_R5_VS_R4_MS128_C4V001, written 2026-10-19T03:27:55Z).

## What ran

- Spec set: exactly the ten FILLED specs of `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/SPEC_REGISTRY_R5_MS128_CX1V004.json` (sha256 `c7023846299bae03c5793c4187ca334d35ca3108401208761edbca37574dee90`). Each parent, template and filled spec sha, and the registry pins of the driver, module, EPS, LO and fill tool, were checked from bytes (TESTED). All ten specs are galaxy DDO154 with uv_tail gas M_s 128, and their certificate slots equal the registry EPS and LO (TESTED).
- Drivers: r4 `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py` (`b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b`), r5 `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` (`b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`).
- Declared map T: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/CASCADE_MAP_R5_C2V001.json` (sha256 `a7281e10a15c7f51eae8b5d5336648c1d0a7d04a8cf932b3860c9eba3636a880`, from bytes), 103 pairs as built by root's declared_map().
- Method of record: root's B0 tool `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/gates/b0_r5_vs_r4_c2v001.py` (sha256 `857ccb8a49e11314c7534b1651bfd316b5eab156b2f26b8b148fea385ef4ce5c`), executed INERT from its pinned bytes. Its declared_map, compare, apply, files and ENV were used unchanged, and its main() was never called.
- Harness: `tools/b0_ms128_c4v001.py` (sha256 `1a5dd386d31d12b188009c40dd948f1386521c56e411f0203a5ce94a5a0033be`). Run as `check` and then `run` in one && chain (launch stamp 2026-10-19T03:26:56Z). Children ran from 2026-10-19T03:26:56Z to 2026-10-19T03:27:54Z.
- 20 dry-run children, one for each (driver, spec) pair: `/usr/sbin/taskpolicy -b /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b0_ms128_c4/tools/run_fenced_c4st2.py DRIVER dry-run --spec SPEC --report-dir RD` with cwd `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b0_ms128_c4/out/dry` and root's single-thread ENV. At most 4 ran at once, and each spec ran R4 first, then R5. One fence smoke child (`tools/fence_probe_c4v001.py`, sha256 `7d3f9fa399761cdbfe7bfc0000affe5b10c11bf0800261dbdca1fd21d1f68be0`) ran before them. No stage was executed, because a dry run only plans (executed_stages 0). `--validity-only` was never run.

## Per spec

| case | filled spec sha256 (16) | r4 exit / s | r5 exit / s | files r4/r5 | raw equal | equal after T | derived hash pairs | verdict | cross-check vs BUILD_V005 dry |
|---|---|---|---|---|---|---|---|---|---|
| C2T | `84933cad8fa19bd9` | 0 / 16.49 | 0 / 17.17 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |
| C3T | `212f4b3673903ef2` | 0 / 16.49 | 0 / 17.17 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |
| C4T | `de6d7d77d053d9c9` | 0 / 16.49 | 0 / 17.17 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |
| C6T | `e4016037423b6302` | 0 / 16.49 | 0 / 17.17 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |
| S4T | `8e71be9bee2887f9` | 0 / 20.46 | 0 / 1.31 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |
| C4T-C5c | `0d60cd7b6a2fa8ec` | 0 / 20.49 | 0 / 1.30 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |
| C4T-KLO | `3001aa3a5e34fe42` | 0 / 20.47 | 0 / 1.29 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |
| C4T-KHI | `ce3bee66a3721293` | 0 / 20.48 | 0 / 1.30 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |
| C4T-A | `96c73b1e478ee7d5` | 0 / 1.19 | 0 / 1.09 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |
| C4T-D5 | `51551ee7cac54600` | 0 / 1.19 | 0 / 1.10 | 14/14 | 6 | 8 | 7 | PASS_PLAN_IDENTICAL | EQUAL |

For every spec, both dry runs exited 0 and wrote non-empty DRYRUN_REPORT.json and DRYRUN_PLAN.txt, so the comparison counted. There were no only-r4 or only-r5 files, and no file differs after T. In every child, stderr held only the runner's summary line, so the driver's terminal stderr line was empty on both sides (TESTED).

## Fence evidence (TESTED unless marked)

- `tools/fence_c4v002.py` (`c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5`) and `tools/run_fenced_c4st2.py` (`fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25`) are byte-identical copies of `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/tools/fence_c4v002.py` and `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/tools/run_fenced_c4st2.py` (cmp and sha, checked again inside the harness). The review root is this folder.
- All 21 children (the smoke child and the 20 dry runs) printed FENCE_C4ST2_SUMMARY with fence sha c993d34c, review_root equal to this folder, selftest 8/8, v002 exception probes 15/15 and **blocked_after_selftest = []**. every_child_blocked_after_selftest_empty = True; every_child_fence_selftest_8_of_8 = True.
- The fence raised no PermissionError, so no spec was stopped and nothing was retried or worked around.
- Parent guard (the harness's own audit hook): 0 refusals. Spawn events numbered 21, equal to the 21 sanctioned argvs, so no other process was created.
- Every file under `out/` was scanned after the run. V002: the fix stage re-counted the text of the 326 out/ files that HASHES V001 lists (TESTED). No file contains runs_ext, C5H, rotmod, Vobs, MassModels, NGC3198 or /Volumes. SPARC occurs 1440 times, each time as a whole non-path row id of the form DDO154_SPARC12_nn (R31-N3). The only path components that start with uvt_ are uvt_*.py source modules (uvt_route_b_binding_c2v001.py, uvt_route_b_binding_c2v001_r5.py, uvt_route_b_binding_nodes_c2v001.py, uvt_route_b_binding_nodes_c2v001_r5.py). Correction (R31-N2): by "run-tree", V001 meant the two CLAUDE2 runs_ext roots. `out/` does contain one CLAUDE2 runs path, `.../CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001/result.json`, 80 times in 40 files. Both drivers pin that path (driver line 343). It is not under runs_ext, and it is neither a UVT_* path nor a C5H path.
- Pins were re-hashed after the runs, and all were unchanged: b0_tool True, r5 True, r4 True, map True, registry True, fence True, runner True.
- Scope (FORMAL): the fence hooks open, write, process creation, network and delete. It does not hook stat or directory listing in the children. V002 correction (R31-S1): V001 said here that neither driver's source contains a runs_ext, C5H or target-word string. That is false as worded. The corrected statement below is TESTED by byte count, tokenizer and AST over both driver files, with identical results for r4 and r5. runs_ext, C5H and KMAX_A2F10 occur 0 times in each driver, and so do MassModels and SPARC. rotmod occurs twice and vobs once, each time as non-path text inside a string literal. Line 4580 is in the docstring of ngc_sources_summary ("The rotmod .dat named in the manifest provenance is NOT opened."). Line 4596 is the manifest key 'rotmod_header' in ngc_sources_summary. Line 4560 is the element 'vobs' of the key-name hint tuple _VELOCITY_KEY_HINTS, which only _key_scan reads. This is NGC3198-only code (FORMAL, read from the AST call graph, which is TESTED). _key_scan is called only by itself and by ngc_sources_summary. ngc_sources_summary is called only by _ngc_collect, and _ngc_collect only by ngc_dry_run and ngc_run_blocked. cmd_dry_run and cmd_run call those two only under `nspec.get('config') == 'NGC3198_C2V002'`. In all 20 fresh reports the normalized spec is galaxy DDO154 with no config field, and no file in out/ contains NGC3198 (both TESTED). So that branch was not taken (FORMAL inference). Each driver also contains 11 NGC3198 non-.py path literals: galaxy configs and inputs, NGC3198 source and reduction files, a target-free query manifest, and one probe-file name pattern. The full list is in the fix record. The fence classes all of them as NGC3198 data. None of them was opened in any child (TESTED: every BLOCKED list is empty; FORMAL: the fence refuses every Python open of a non-.py NGC3198 path, fence line 86). The dry-run path is simulate mode, and Ctx.run_stages returns before its Popen when mode != run, so it launches nothing.
- As designed, the runner reads 64 bytes from each of its three allowed files in every child before the driver starts: the r5 cascade `uvt_route_b_binding_c2v001_r5.py` and the V005 and V004 ROOT_DECISIONS addenda in the CLAUDE2 control folder. These are decision records, not data, and seal_tools_v004 does the same.

## Declared adaptations of root's main()

- child = fence runner run_fenced_c4st2.py (fe904509) under taskpolicy -b, not the bare driver under nice -n 10
- terminal stderr line = the driver's last stderr line: last line of stderr.strip() after removing the runner's trailing FENCE_C4ST2_SUMMARY line (that line is recorded per child as fence_summary)
- spec set = exactly the ten FILLED specs of SPEC_REGISTRY_R5_MS128_CX1V004 (c7023846), labels = registry case
- task rule 4: a fence refusal makes the spec BLOCKED_FORBIDDEN_ACCESS (not counted) and stops it; verdict_B0 is then BLOCKED_FORBIDDEN_ACCESS unless a FAIL exists
- In practice, adaptation 2 had no effect: the driver stderr was empty on all 20 children, and the early-failure branch of the B0-EMPTY rule was never reached.

## Cross-check (NOTE, not part of the verdict)

- Pin chain checked from bytes: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/BUILD_V007.md` (`94bc05a5db1e6350`) pins `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/BUILD_V006.md` (`fb9e6a4a19395f35`); `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/BUILD_V006.md` pins `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/BUILD_V005.md` (`46bc5b5d23bb39e7`); BUILD_V005 pins `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/DRY_R5_MS128_V004.json` (`ff60cd6b7d33b9a89326b90329e55a4b589f516b7e63cb2d28b41c4e83b7ceed`) and each per-case DRYRUN_REPORT.json under `v007_launch_packet_cx1/P128/dry/<case>_DRY_R5_MS128_V004/`.
- I ran root's compare() with each fresh `out/dry/R5_<case>` directory against the matching existing directory, substituting only the report-dir path. Equal: 10/10 (C2T, C3T, C4T, C4T-A, C4T-C5c, C4T-D5, C4T-KHI, C4T-KLO, C6T, S4T). Differ: none.
- Checked outside the record, after the run (TESTED): each fresh R5 stdout is byte-identical to `v007_launch_packet_cx1/P128/<case>_DRY_R5_MS128_V004.log` for all 10 cases, and T(r4 stdout) == r5 stdout for all 10. V002 note (R31-N5): these .log files are neither named nor pinned by sha in BUILD_V005, BUILD_V006, BUILD_V007 or DRY_R5_MS128_V004.json (TESTED in the fix stage). This line is therefore a comparison against unpinned files, and the verdict does not use it.

## Labels

- TESTED: the pin checks, the 20 fenced dry runs, the B0 verdict, the fence summaries, the parent-guard counts, the cross-check and the output scan, all run on bytes in this folder.
- TESTED in the fix stage (V002): the R31-S1 byte, token and AST evidence for both drivers; the ten specs' schema and galaxy; the normalized spec, driver sha and executed_stages of the 20 fresh reports; the 21 fence summaries in out/logs; the out/ re-count; the .log pin search; the refuter-file shas; and the integrity of the V001 files.
- FORMAL: that the dry-run path launches nothing, and that the fence does not cover stat or listdir. V002 replaces V001's "has no source references to forbidden trees" with this: the driver code that holds target words is NGC3198-only and is not reached for these DDO154 specs. The drivers do contain target words as non-path text, and NGC3198 path literals (see Scope).
- UNTESTED: anything beyond plan identity. That covers run mode, launch, `--validity-only`, the scientific content of the plans, and the r4 and r5 drivers' behaviour on inputs other than these ten specs.

## Refuter notes (V002)

- R31-N1: the refuter re-derived PASS_PLAN_IDENTICAL from bytes. No action.
- R31-N2, R31-N3 and R31-N5: re-checked from bytes and carried into the scan, Scope and .log bullets above.
- R31-N4: in the fence, `_hook` runs `real = os.path.realpath(lit)` (fence line 135) before `_forbidden_read` (line 136). So, as the refuter says, the runs_ext probes in each fenced child also lstat the CLAUDE2 runs_ext root entry (line text TESTED, effect FORMAL). No C5H path and no UVT_* run output is touched. Changing this needs a new fence version, so no action here.
- R31-N6: README V001 and HASHES V001 were written through a helper in the session scratchpad that was not kept, so their exclusive creation is UNTESTED. The fix-stage script is kept in `fix_c4v002/` and listed in HASHES V002. One fix-stage capture went outside the folder; see the disclosure in the successor note.
- R31-N7: the runner's `except SystemExit` handler (runner line 75) keeps only an int exit code and drops a text message (FORMAL). Per the refuter, both drivers exit with int codes (FORMAL), and all 20 driver stderrs are empty (TESTED here). So it had no effect. No action.
- R31-N8: per the refuter, the equal batch-1 timings are real. No action.

## Files

- `tools/`: fence_c4v002.py and run_fenced_c4st2.py (byte-identical copies), fence_probe_c4v001.py, b0_ms128_c4v001.py.
- `out/B0_R5_VS_R4_MS128_C4V001.json`: the record. `out/dry/{R4,R5}_<case>/`: the 20 dry-run report directories, 14 files each.
- `out/logs/`: for each child, `{R4,R5}_<case>.stderr.txt` and `.stdout.txt`; `FENCE_SMOKE_RUN_C4V001.*`; `CHECK_1_C4V001.txt` and `CHECK_2_C4V001.txt` (check-mode outputs); `RUN_C4V001.txt` (the run summary).
- `PARTIAL.md` (progress log; the fix-stage lines come after byte 1322), `README_B0_MS128_C4V001.md` (V001, unchanged), this README V002, and `HASHES_B0_MS128_C4V001.txt` (the V001 state, unchanged).
- V002, fix stage: `FIX_RI31_C4V002.json` (the fix record); `fix_c4v002/fix_ri31_c4v002.py` (the fix script, with modes dry, write, hashes and verify); `fix_c4v002/dry_stdout_c4v002.txt` and `fix_c4v002/write_stdout_c4v002.txt` (its captured output); and `HASHES_B0_MS128_C4V002.txt`, written last, which lists every other file in the folder.
