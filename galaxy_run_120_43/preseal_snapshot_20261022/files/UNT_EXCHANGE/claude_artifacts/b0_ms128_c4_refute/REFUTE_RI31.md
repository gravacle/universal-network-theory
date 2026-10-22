# REFUTE RI-31: B0 r5 = r4 dry identity on the M_s 128 set (c7023846)

Claude4 helper, dispatch 0650, root entry A113 in V006, stage refute_ri31. Written 2026-10-19T03:53:12Z (date -u).
Build under review (read-only): `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b0_ms128_c4`.
Refute folder: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b0_ms128_c4_refute`.

## Result

**The build's verdict_B0 = PASS_PLAN_IDENTICAL holds when re-derived from bytes (TESTED).** All ten specs of
SPEC_REGISTRY_R5_MS128_CX1V004 (c7023846) are counted and PASS_PLAN_IDENTICAL. FAIL, NO_EVIDENCE_EQUAL_EARLY_FAILURE,
BLOCKED_FORBIDDEN_ACCESS and ERROR are all empty. A6 can read PASS_PLAN_IDENTICAL.

There are no BLOCKING findings. There is one SHOULD_FIX: a FORMAL claim in the builder's README and finding RI31-N4 is
false as worded. It does not affect the verdict. The other findings are NOTEs (see Findings).

The record of my checks is `REFUTE_RI31_CHECKS_C4V001.json`, sha256
`fc943107f25c2333ef06ba9556ee07ce9f497d46e2367b8ebf7dfdfdcd61453c`, written by exclusive create. It holds 235 checks;
234 are claims about the build and all of them hold. The 235th, `H.log_paths_pinned_in_BUILD_chain`, is a provenance
probe that is expected to be False, and it is False (finding R31-N5). The checks JSON was produced by
`work/refute_ri31_c4v001.py` (sha256 `9c0b65b0400dfabb0052a6a20a102bc7658982d6214aac008a3ca4fe9cd26f6d`), run as
`dry && write` in one chain. The dry and write stdout are identical except for the final WROTE line.

## How (labels: TESTED = run on bytes here; FORMAL = source reading; UNTESTED = not checked)

- Each script ran as one Python process (python3 -I -B, single-thread env). The main script ran under taskpolicy -b.
  Each script installs an audit hook first.
  - The main script's hook refuses every process creation, every network call, every delete and any write outside
    this folder. It also refuses any open or listing whose LITERAL path names runs_ext, the C5H run name, a target
    word, NGC3198 or a uvt_* component. The literal path is checked before any filesystem access.
  - The two small helper scripts use a reduced hook. It refuses process creation, deletes, socket connects, every
    write, and opens with forbidden names.

  TESTED: the main guard refused nothing and recorded 1771 allowed opens. None of the hooks refused anything, and no
  child process was created.
- I did not run any driver, dry run or `--validity-only`. I did not re-run the 20 dry runs, because no verdict depended
  on them: the builder's report directories are on disk and pinned by its HASHES file.
- Root's tool `b0_r5_vs_r4_c2v001.py` (857ccb8a) was exec'd INERT from its pinned bytes, into a fresh module. Its
  `declared_map`, `compare`, `apply` and `files` were used unchanged.

## Claim-by-claim

| # | Builder claim | Status | Label | Evidence |
|---|---|---|---|---|
| 1 | Pins: b0 tool 857ccb8a, r5 b5cc62af, r4 b9ae92d5, registry c7023846, fence c993d34c, runner fe904509; map a7281e10 recorded from bytes | CONFIRMED | TESTED | shasum and in-script hashes; both fence and runner copies are cmp-identical to seal_tools_v004; the runner pins FENCE_SHA c993d34c |
| 2 | The 13 listed output files have the listed shas | CONFIRMED | TESTED | all 13 match |
| 3 | Spec set = exactly the ten FILLED specs of c7023846; 30 parent/template/filled shas match; all DDO154, M_s 128, EPS/LO slots equal the registry | CONFIRMED | TESTED | record rows are exactly the registry cases, in registry order; registry driver = r5; module/EPS/LO/fill_tool pins match; out/dry holds exactly the 20 R4_/R5_ dirs of these cases |
| 4 | T = root's declared_map, 103 pairs, nothing else | CONFIRMED | TESTED + FORMAL | my in-process declared_map() gives 103 pairs: 33 re-pinned path pairs + 2 driver-path pairs (one from the map files list, one explicit) + 33 declared_sha_map pairs + 2 driver-sha pairs + 33 basename pairs. Every pair comes from CASCADE_MAP_R5_C2V001 (36 files, 34 re-pinned, 34 sha-map rows) or the driver pin; none is unclassified. The harness passes this base unchanged to root's compare() (FORMAL, harness lines 361, 425, 340) |
| 5 | Derived hash pairs only from root's fixpoint | CONFIRMED | TESTED | 7 per spec, the same 7 files on every spec: 6 simulated_call inputs (fs_manifest and 5 galaxy_config probes) + DRYRUN_REPORT.json, each added only where T(r4 bytes) == r5 bytes. Every derived input hash is consumed by DRYRUN_REPORT.json (fs_manifest also by DRYRUN_PLAN.txt); no file consumes the report's own pair. The count equals compare()'s count for all 10 specs (`work/derived_pairs_c4v001.py`) |
| 6 | Per spec: 14/14 files, 6 raw-equal, 8 equal after T, nothing only on one side or differing | CONFIRMED | TESTED | root's compare() re-run on the builder's 20 dirs equals the record's files block exactly (all 10). The raw-equal files are fs_controls_00/01, galaxy_config_reference probe, seed, uv_tail_config, uv_tail_route_a_request |
| 7 | Verdict per root's B0-EMPTY rule; overall PASS_PLAN_IDENTICAL | CONFIRMED | TESTED | rule re-applied with exits from the record and stderr tails re-parsed from the logs: 10 counted, 10 PASS, summary equals the record. Not vacuous: all ten are counted (A55 ruling 2, every spec) |
| 8 | Exit 0 for all 20 children | CONFIRMED | TESTED + FORMAL | record and RUN log. Also: all 20 stdout logs parse as the driver's final summary JSON, and cmd_dry_run prints that JSON immediately before `return 0` (r5 lines 3925-3929) |
| 9 | Each report is the right driver on the right spec, plan only | CONFIRMED | TESTED | each DRYRUN_REPORT.json has call_spec = the filled spec path, call_spec_sha256 = its sha, driver_sha256 = b9ae92d5 (R4) or b5cc62af (R5), and executed_stages 0 (all 20) |
| 10 | Child argv, cwd, env, at most 4 at once | CONFIRMED | TESTED (argv/cwd) + FORMAL (concurrency/env) | every row's argv is `/usr/sbin/taskpolicy -b PY -I -B <folder>/tools/run_fenced_c4st2.py DRIVER dry-run --spec SPEC --report-dir RD` with cwd = RD's parent. ThreadPoolExecutor(4) runs R4 then R5 sequentially per spec. ENV = root's ENV |
| 11 | Every child's BLOCKED list after the selftest is empty; selftest 8/8; probes 15/15 | CONFIRMED | TESTED | 23 FENCE_C4ST2_SUMMARY lines were parsed: the 20 children, the run smoke child, and the smoke children in CHECK_1 and CHECK_2. Each has fence c993d34c, review_root = build folder, 8/8, 15/15, blocked_during_selftests 20 and blocked_after_selftest []. The stderr of each of the 21 run-pass children is exactly `\nFENCE_C4ST2_SUMMARY {...}\n`, so driver stderr was empty, with no FENCE_C4 line, REFUSED line or traceback |
| 12 | Parent guard refused nothing; 21 spawns = 21 sanctioned argvs | CONFIRMED | TESTED (record/logs) + FORMAL | record parent_guard = {blocked: [], spawn_events: 21, sanctioned_argvs: 21}; CHECK_1/CHECK_2/RUN logs guard_blocked [] |
| 13 | No forbidden path string in out/ | CONFIRMED (path level) | TESTED | 326 out/ files and the 10 specs were scanned, each occurrence classified by its enclosing token. No path string contains runs_ext, C5H, rotmod, vobs, massmodels, sparc or NGC3198. No runs_ext, C5H, NGC3198 or /Volumes text appears anywhere in out/. The only uvt_ paths are 4 uvt_*.py source modules outside runs_ext. See R31-N2 and R31-N3 for what does appear |
| 14 | Neither driver's source contains a runs_ext, C5H or target-word string (FORMAL) | REFUTED as worded | TESTED | each driver contains `rotmod` twice and `vobs` once. None is a path; all three are in NGC3198-only code. See R31-S1 |
| 15 | Simulate mode: Ctx.run_stages returns before its Popen | CONFIRMED | FORMAL | r5 lines 1825-1847: `if self.mode != 'run': ... return recs` precedes Popen; cmd_dry_run builds Ctx('simulate'). With uv_tail present, repro_like is False, so no saved-run map is used (r5 line 3718 region) |
| 16 | The fence does not hook stat or directory listing | CONFIRMED | FORMAL | fence_c4v002 _hook handles process, network, delete, write-path and open events only |
| 17 | Cross-check: BUILD_V007 94bc05a5 -> V006 fb9e6a4a -> V005 46bc5b5d -> DRY_R5_MS128_V004 ff60cd6b7d33b9a89326b90329e55a4b589f516b7e63cb2d28b41c4e83b7ceed + 10 reports; fresh R5 = existing (10/10); R5 stdout = existing .log; T(r4 stdout) = r5 stdout | CONFIRMED, with a provenance note | TESTED | every link was re-hashed from bytes and compare(existing, fresh, []) gives EQUAL 10/10, identical to the record. The .log files are byte-identical (10/10) but not pinned (R31-N5) |
| 18 | HASHES: 332 rows, written last, every other file | CONFIRMED | TESTED | 332 rows all match bytes; they cover every file in the folder except HASHES itself. There is no symlink or special file. out/ holds 326 files (280 in dry/, 45 in logs/, 1 record) |
| 19 | Seconds 1.1 s to 20.5 s; pins unchanged after the run | CONFIRMED | TESTED | record 1.09 to 20.49 s. All pins re-hashed now (again unchanged) |
| 20 | README/HASHES written by exclusive create | NOT VERIFIABLE | UNTESTED | the scratchpad helper that wrote them is not in the folder (R31-N6). The files exist with the claimed shas (TESTED) |

"Tool 4's own checks on the forms": not applicable to RI-31, which has no forms. The RI-31-specific items (fence
evidence, spec set, map T) are rows 3-5 and 11-16.

## Findings

- **R31-S1 (SHOULD_FIX).** Claim 14 is false as worded (TESTED, byte count of the two named driver files). Each driver
  (r4 b9ae92d5, r5 b5cc62af) contains `rotmod` twice and `vobs` once:
  - line 4580, a docstring: "The rotmod .dat named in the manifest provenance is NOT opened.";
  - line 4596, the manifest key `rotmod_header`;
  - line 4560, `_VELOCITY_KEY_HINTS` (`'vobs'`).

  All three are in NGC3198-only helpers (`ngc_sources_summary`, `_key_scan`), and none is a path literal. The safety
  conclusion still stands on the empty BLOCKED lists and the path-level output scan. The verdict is unaffected.
  Fix: wherever the coverage argument is cited (A6 / root acceptance), replace it with: "no runs_ext or C5H string;
  target words occur only as non-path text in NGC-only code". No file edit is needed; record the correction in the
  acceptance note.
- **R31-N1 (NOTE, confirmation).** Gate B0 on c7023846 is PASS_PLAN_IDENTICAL, re-derived in-process from the
  builder's bytes with root's own functions. Pins, the ten-spec set, T, the per-spec files blocks, the rule, the
  summary, the fence evidence, the cross-check and HASHES all agree with the record (claims 1-13 and 15-19).
- **R31-N2 (NOTE).** "Run tree" in the builder's scan claim means the two runs_ext roots. out/ does contain a CLAUDE2
  *runs* path: `.../CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001/result.json`, 80 occurrences in 40 files (TESTED). Both
  drivers hash it as a static pin and as the `v_ref_km_s` source. It is not under runs_ext, not UVT_* and not C5H, so
  the fence admitted it. The BUILD_V005 dry runs read the same file (cross-check EQUAL). Not forbidden by the
  absolute rules. Fix: when citing the scan, say "no runs_ext path".
- **R31-N3 (NOTE).** `SPARC` occurs 1440 times in out/ (TESTED). Every occurrence is a non-path row id
  `DDO154_SPARC12_nn`, in the drivers' simulated_call/inputs/galaxy_config_*_PENDING_PROBE.json files
  (observation.query_rows: id + radius_m). The builder's claim says "path string", so it holds.
- **R31-N4 (NOTE).** The runner's stat footprint is slightly larger than disclosed in RI31-N5. posixpath.realpath
  (Python 3.12.14) lstats every prefix of a path. So each child's two runs_ext probes (selftest `read_runs_ext`;
  v002 probe `uvt_py_under_runs_ext`) also lstat the CLAUDE2 runs_ext root directory entry itself, not only the
  non-existent probe names: 2 x 23 children. This is FORMAL, from fence `_hook`: `real = os.path.realpath(lit)` runs
  before `_forbidden_read`. No C5H path or UVT_* run output is touched, because the probe names are fixed literals.
  The absolute rules do not forbid this, and it is inherent to the dispatched runner fe904509. Fix (future fence
  version): test the literal path before calling realpath, so a refused path is never lstat'ed.
- **R31-N5 (NOTE).** Cross-check provenance. The per-case `.log` files compared in builder RI31-N2
  (`v007_launch_packet_cx1/P128/<case>_DRY_R5_MS128_V004.log`) are in no BUILD_V005/6/7 sha row (TESTED), and their
  paths do not come from those records' bytes. They are byte-identical to the fresh R5 stdout (TESTED, 10/10).
  In each pinned existing dry dir, 12 of the 13 non-report files are bound by shas recorded inside the pinned
  DRYRUN_REPORT.json. DRYRUN_PLAN.txt is bound by no pin (TESTED). The cross-check is not part of the verdict.
- **R31-N6 (NOTE).** The builder disclosed one helper written in the session scratchpad, outside its folder. That is
  a literal deviation from "write only inside your own output folder"; it touched no lane or root file. Because the
  helper is not preserved, the claim that README and HASHES were exclusive-created is UNTESTED. Fix: future helpers
  keep temporary scripts under <folder>/work.
- **R31-N7 (NOTE).** Adaptation (2), latent gap (FORMAL). run_fenced_c4st2 catches SystemExit and drops a non-int
  exit message (runner lines 73-76). So a driver that ended with `sys.exit('text')` would lose its terminal stderr
  line under the fence, unlike root's bare-driver run. Both drivers exit only through `sys.exit(main())` with an int
  (FORMAL), and all 20 driver stderrs are empty (TESTED), so there was no effect here. Fix: root to confirm the
  terminal-line definition before the early-failure branch is ever needed under the runner (as builder RI31-N3 asks).
- **R31-N8 (NOTE).** The equal timings in batch 1 (four R4 at 16.49 s, four R5 at 17.17 s) are real; the rows were not
  duplicated (TESTED). The four R4 report dirs were born at the same millisecond (03:26:57.326Z) and their reports
  were written within 6 ms (03:27:13.447-.452Z), consistent with background-band release under taskpolicy -b. Every
  row's argv, logs (size and sha) and report binding (spec sha, driver sha) are specific to its spec.

## Files written here

All are inside the refute folder.

- The records (REFUTE_RI31.md, REFUTE_RI31_CHECKS_C4V001.json and HASHES_REFUTE_RI31_C4V001.txt) were written by
  exclusive create.
- The scripts and the draft were written with the editor tool, the two stdout captures by shell redirect, and
  PARTIAL.md by append.
- `HASHES_REFUTE_RI31_C4V001.txt` is written last and lists every other file with its sha.

Not verifiable from bytes (UNTESTED): the builder's statements that nothing was deleted, that there was no network
access and that no recursive grep was run. For the harness and the children these are enforced FORMALLY by the parent
guard and the fence.

- `REFUTE_RI31_CHECKS_C4V001.json`: the 235 checks and the recomputed rows, summary, cross-check and scan.
- `work/refute_ri31_c4v001.py`: the re-derivation script (9c0b65b0...); `work/dry_stdout_c4v001.txt`,
  `work/write_stdout_c4v001.txt`.
- `work/inspect_hits_c4v001.py` (a11d7da7...): the word-hit contexts. `work/derived_pairs_c4v001.py` (4ec9b5de...):
  the derived pairs and pin coverage. `work/REFUTE_RI31.draft.md`: the draft of this file.
- `PARTIAL.md`: the progress log.

## Labels

- TESTED: claims 1-3, 5-9, 11-14, 17-19 and the argv/cwd part of claim 10; findings R31-S1, N2, N3, N5, N8.
- FORMAL: claims 15 and 16, the concurrency and env part of claim 10, the derivation of claim 4 through the harness
  code, findings N4 and N7, and that the drivers' stat/listing behaviour outside out/ is limited (no hook covers it).
- UNTESTED: claim 20; run mode, launch, `--validity-only`; any stat or listing that a child made and that left no
  trace in out/.
