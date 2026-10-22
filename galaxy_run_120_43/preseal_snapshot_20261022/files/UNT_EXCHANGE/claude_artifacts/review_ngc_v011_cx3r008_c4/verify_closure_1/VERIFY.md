# VERIFY: PT8-SF1 (closure lens, cx3r008). Claude4 helper verify_closure_1, dispatch 0617, claim FROM_CLAUDE4/0097

Written 2026-10-18T21:18:52Z (`date -u` taken just before writing). Refute by default. Nothing was launched: no `main()`, no `cmd_run`, no run handler, no project calculation. I did not open NGC3198 target, observed-velocity or data tables, any `runs_ext` tree, the C5H run or any `UVT_*` tree. I wrote only inside this folder.

## VERDICT: NOT REFUTED, but narrowed from six classes to one. SHOULD_FIX on class (f) only

| Part of PT8-SF1 | Result | Label |
|---|---|---|
| The disposition (a9ae801f) and mapping (ab5afb0e) pin only two r008-specific classes: L5145 and the guard move 9220→9329 | **Confirmed.** One qualifier: the inherited selector class in a9ae801f lists `r007_r008_dispatch_lines: [9194, 9206]`, which contains L9205 | TESTED (bytes) |
| 0 of the 17 refused dry-plan logs show L9205 | **Confirmed.** 78 logs; 17 have an exception; none contains `line 9205` or a frame at 9205; all 17 go through the generic branch at L9206 | TESTED |
| Classes (a)–(f) exist | **Confirmed, all six.** Exception class and message are identical in every class probe. Only traceback text, line numbers or frames differ | TESTED (P1–P6, with controls) |
| A98.1 requires (a)–(e) to be enumerated and pinned before closure | **Refuted.** (a)–(e) occur only inside NGC. PAR-TB and A98.1 govern the outside-NGC byte-identity requirement and nothing else | FORMAL (governing bytes); reductio TESTED (P4b, P4c) |
| A98.1 requires (f) to be enumerated and pinned before closure | **Not refuted.** (f) is outside NGC, specific to r008, and not enumerated | TESTED (P6), FORMAL (reach map) |
| No decision field changes outside NGC | **Confirmed** | TESTED (P0, P0b, P6), FORMAL |

**The narrowed finding (SHOULD_FIX; documentary; practical risk nil).**
- **What is missing.** The A98.1 disposition leaves out one outside-NGC traceback class that is specific to r008: `cmd_dry_run` L5147.
  - r006 and r007 text: `if code==0 and rp.is_file():`
  - r008 text: `if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():`
  - The caret line under each also differs.
- **Why it matters.** The disposition says "The r008-specific classes were enumerated and byte-pinned before closure" (addendum f9632697, line 9). That sentence is incomplete by this one class, so A98.1's condition for closure is not yet literally met.
- **How it can be reached.** Only when `Path.is_file()` raises an OSError that Python 3.12.14 does not ignore (EACCES, EPERM or EIO; it ignores only ENOENT, ENOTDIR, EBADF and ELOOP). That has to happen after the planner has itself written the report into the same directory.
- **What it touches.** Top-level dry-run stderr only. Exception class and text are identical. No saved record, stage stderr, result hash or decision field is affected.
- **Fix.** A disposition successor with no code change. Add one `r008_specific_classes` entry for L5147, giving both exact texts and that scope. Optionally:
  - one sentence recording that (a)–(e) are consequences of SF1/SF2 inside NGC and fall outside PAR-TB scope;
  - correct the registry V002 wording (see N1).

## Pins (all re-hashed from bytes; all match)

| Object | sha256 |
|---|---|
| cx3r008 driver | `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377` |
| SELECTED_CX3R008_CX3V002.json | `4c5be34c9812bdf8b3ddf669d544cb449eccc68d180532cde8ffa2e5b14718e4` |
| SPEC_REGISTRY_CX3R008_V002.json | `2c3f421d9a933d1a841f134574984cb0c33e7a0544de0b20514103492214413a` |
| A98_1_DISPOSITION_ADDENDUM_CX3V001.md | `f9632697961c5549c9401a13a85346068c67d5e896a34d2c4b72f4b1f51e0fcf` |
| PAR_TB_A98_1_DISPOSITION_CX3V001.json | `a9ae801f7a13f18864200cb99f49ac9241e4d4154b318feb68b86b41a18dc625` |
| HANDOFF_CX3R008_CX3V001.json | `150650fd317ba6752f715b21814b1a151356c8204b3877ac3807a822c1971d15` |
| FROM_CODEX3/0624 | `8085f4be5032493beede70c7f25c47f113ecade065c4208c5e47b6391023029f` |
| PAR_TB_R008_DELTA_CX3V001.json | `ab5afb0e007dcceaf53137c3fe92d1ee0341d68f6765afcd62667046de767979` |
| PAR_TB_ROOT_ITEM_CX3V001.md | `1c5dc1c136d9c84f71025dc4bbbac06e83336d1889a9b3570106354440264084` |
| cx3r007 driver | `e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69` |
| SPEC_REGISTRY_CX3R007_V001.json | `cd30429c27ced0837dc383c00f78899a758fefeeaae2f6134e6aae7fcad18ea2` |
| REVIEW_NGC_V011_CX3R007_C4V001.md | `74d6cd9ed0a784cd71564d498d52e0905b54acb2fbd6c00fe511a8dd3486de1b` |
| fence_c4v001.py (source) | `f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0` |
| dispatch 0617 | `622f5cc99633a2433ce4fb7feebabb6580a468c6660f48377c7c8e48f6bd102d` |
| 0619 (A98.1 to Codex3) | `238858d12823a153b14dd980d2e2c0a4a71da5c320be054c1fe14832d667ee99` |
| 0581 (cx3r007 requirements) | `3e6ea8a721e32546cc88703486edbca5b871bbffdc7cd66f1d3fa7d394371132` |
| FROM_CODEX3/0621, 0622, 0623 | `b01551734260051ffcbaf5c2c883169e392395474283374f144c3136bbd9f2e3`, `b34751aeed4ecf6acb864f5a1c4b257d89cdf30ae215adf1f59f2f04fab3119c`, `e173cbfd4440c9a6c6513cba6fd537cc956a9b7f983165a827645159e1b88343` |
| root V005 addendum (A98 at L965–976) | `70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e` (taken with shasum at 20:52Z and again at 21:18Z) |
| grid-cut helper | `5d037291c8d683d7921f38365640bf41502216a67a5ed6ca84986aa671faf353` |

## 1. Source delta (FORMAL: `out/DIFF_R007_R008_VC1.txt`, `out/REACH_MAP_VC1.json`)

- **Changed lines.** A line diff of the verified bytes gives these r008 lines that differ from r007 at the same number:
  - L5018 (`_ngc_v011_helper`);
  - L5145–5147 (`cmd_dry_run`);
  - L5219–5224 (`final_rows_check`: one line inserted, `except Refusal:raise`, which shifts r007 L5219–5223 by +1);
  - L9194 and L9205 (`_ngc_v011_dispatch`);
  - L9219–9327 (the appended block);
  - the guard, r007 L9220 → r008 L9329.

  Every other line is equal at the same number.
- **Reach map (AST call sites in r008):**
  - `_ngc_v011_helper` is called only from L5056 and L5066 (inside `normalize_spec`'s NGC-tail branch, after the L5048 test `galaxy=='NGC3198' and 'uv_tail' in numerics`) and from L5216 (`final_rows_check`'s cut branch).
  - The new strict clones and the strict sha are installed only by `_ngc_strict_grid_helper_cx3r008`, which is reached only through L5018.
  - `_ngc_finalize_dry_cx3r008` is passed at L5145 but invoked only at L9205, which is inside `with _ngc_v011_context():`.
  - `final_rows_check` L5219–5224 are reached only past `if cut is None: return …` and the NGC3198/uv_tail test (L5211–5213). The generic callers (L3530, L7822) pass no `normalized_spec`, so for them the cut is always `None`.
- **Outside NGC, the r008-specific traceback lines are exactly:**
  - L5145 (pinned);
  - L5146 (`if isinstance(code,tuple):return code[0]`, which cannot raise);
  - **L5147 (not pinned): class (f)**;
  - L9329 (pinned).

## 2. The 17 refused dry plans (TESTED: `tools/scan_dry_logs_vc1.py` → `out/SCAN_DRY_LOGS_VC1.json`)

- **The claim holds.** Of the 78 logs in `ngc_cx3r008_closure_cx3/plans/dry_S_v001/*/log.json`, 17 carry an exception. None contains `line 9205` in its traceback or stderr, and there are 0 frames at 9205. All 17 traverse the generic branch at L9206.
- **Refinement (N2).** "The NGC branch was never exercised" is imprecise. The NGC branch did run, in the 10 completed NGC-tail plans 068–077. Each of them wrote `NGC_SOURCE_BUILD_READINESS.json`, which in r008 only the finalizer at L9205 writes. What no evidence exercised is a *failure* through L9205, which is the lens's actual point.

## 3. The six classes exist (TESTED: `tools/probe_classes_vc1.py`, `tools/compare_classes_vc1_v2.py`)

**Method.**
- Each driver ran in its own fenced process, loaded from verified bytes. The compile filename and `__file__` are the real path, so the r007 wrapper loop installs exactly as it does in a launch.
- Every probe used identical stubs and synthetic look-alikes in `sandbox/`.
- The comparison is frame by frame over the whole exception chain. It substitutes only the driver path, the per-process sandbox root, and the harness module name of `Refusal` (N4).
- Run 1 and run 2 give identical comparison records (`out/COMPARE_CLASSES_VC1_V2.json`, `out/COMPARE_CLASSES_VC1_RUN2.json`).

| Probe | Path | Class/message r007 vs r008 | Frame difference |
|---|---|---|---|
| P0 control: generic spec, planner stub refuses | outside NGC | same | only L5145 text and carets (pinned class) |
| P0b control: generic spec, planner returns 0 | outside NGC | same return (0) | none |
| **P1 (a)** NGC-tail spec, planner stub refuses | inside NGC (L9205 is inside `_ngc_v011_context`) | same | L9205 source text differs; carets equal; 5 = 5 frames |
| **P2 (b)** `_ngc_v011_helper()` with a grid_cut pin mismatch | NGC-only function | same (`NGC v011 grid_cut pin mismatch …`) | L5018 text and caret position |
| **P3 (c)** `final_rows_check` with a cut, deep `final` | cut branch | same (RecursionError) | `final_rows_check` frame 5220 → 5221, text identical; 997 = 997 frames |
| **P3b (c)** cut branch, rows without `speed_km_s` | cut branch | same (KeyError) | 5223 → 5224 |
| P3c control: no cut | — | same | **none** (the L5211 path) |
| P3d control: generic rows | — | same | **none** (the L5207 path) |
| **P4 (d)** NGC-tail spec, report `{}` | inside NGC | same (KeyError `normalized_spec`) | r007 `cmd_dry_run` L5148 → r008 L5145, dispatch L9205, finalizer L9251 (3 → 5 frames, counting the harness frame) |
| **P5 / P5b (e)** helper `read_cut_record`, wrong schema / pin mismatch | helper returned by L5018 | same | helper file L121 / L119 frame → clone frame at driver L9306 / L9303 |
| **P6 (f)** generic spec; the planner stub writes the report, then the report dir goes to mode 0600 (EACCES) | **outside NGC** | same (PermissionError [Errno 13]) | **L5147 text and carets** |
| P6b, the same inside NGC | inside NGC | same | r007 L5147 → r008 L5145, L9205, finalizer L9249 |

**(c) reaching saved output (FORMAL).** Both NGC run handlers call `final_rows_check` inside their `try` (L6067, L9031):
- they save `traceback.format_exc()` on any `Exception` (L6112–6116, L9071–9075);
- `finish.json` `result_sha256` is the sha of `result.json` (L6134–6136).

So (c) can reach the saved run-mode record, but only for an NGC spec that declares a cut, and none of the 8 registered specs does. Run mode was not executed.

## 4. Why (a)–(e) are not A98.1 obligations (FORMAL from bytes; reductio TESTED)

**The requirement PAR-TB exists to except is outside-NGC only.**
- 0581 L19: "Behaviour outside the NGC contexts must stay byte-identical to r006."
- PAR-TB-1 as defined in Claude4's cx3r007 review (74d6cd9e, L36, L49) opens "Outside NGC, every traceback …". It says the 0581 wording "does not hold for one output class", and its fix is "a root ruling admitting these closed traceback-text classes in failure diagnostics written to disk outside NGC".

**What A98.1 ruled on was framed the same way.**
- A98.1 rules on "PAR-TB (Codex3 0621/0622)".
- The root item it relies on (1c5dc1c1, L19) asks for the classes to be recorded "as diagnostic-only NOTE under the existing outside-NGC requirement". It anticipates the r008 duty as "added cmd_dry_run selection-frame classes" (L17).
- 0621 L11 promises that "any r008-specific dry-run callback source-line class will be separately enumerated". A98.1's "Any frame class specific to r008 is enumerated and pinned before closure" and 0619 L15 echo this.
- 0622 L9 excludes inside-NGC frames explicitly: "New active NGC strict callback/helper refusals are intentional behavior changes under separate review, excluded from this request." The disposition repeats this (a9ae801f `excluded`; addendum L14).

**Reductio (TESTED).** A98.1 grants no exception for "exception class or text, refusal reasons, decision branches". If its regime governed inside NGC, the SF1/SF2 closure that root ordered (A93, 0617) would itself be non-compliant:
- **P4c, decision branch.** Given a duplicate-key NGC report, r007 returns 0 and writes readiness `PENDING_CERTIFICATES` from the last occurrence. r008 raises a typed `NGC_JSON_DUPLICATE_KEY` and writes no readiness.
- **P4b, exception class.** A malformed report raises `JSONDecodeError` in r007 and `Refusal NGC_JSON_PARSE_REFUSED` in r008.

So A98.1, including its pinning duty, is scoped to outside-NGC parity. The lens reaches the same conclusion for inside-NGC behaviour deltas in ST8-N2 (closure REVIEW L154): "A98 gives no diagnostic waiver for them, and none is needed". Traceback text inside NGC is a strictly weaker difference than those deltas, so it needs no waiver either.

**The specific classes.**
- (a) and (d) are the SF1 callback, both its invocation line and its frames.
- (b) and (e) are the SF2 strict helper, both its installation line and its frames.
- (c) is the mechanical +1 shift caused by SF2's inserted re-raise. It appears only on the cut branch (the P3c and P3d controls are identical).
- The disposition's exclusion of "new active NGC strict callback/helper frames or refusal behavior … intentional SF1/SF2 behavior" is therefore the correct treatment, not an incomplete enumeration.
- Even on the lens's broader reading, (a) lies inside the enumerated r008 dispatch range [9194, 9206] of the inherited selector class. That class's scope is top-level stderr, and that is the only place (a) can appear (FORMAL):
  - dry-run failures escape to the top level;
  - in run mode, both NGC handlers catch every `Exception` inside their `try`, and the traceback they save starts below the dispatch frame.
- No r007 NGC run exists for any r008 NGC output to be compared against.

## SHOULD_FIX (1, narrowed)

| id | finding | reproduction | fix |
|---|---|---|---|
| **PT8-SF1 (narrowed)**, TESTED | The A98.1 r008 enumeration (a9ae801f, ab5afb0e) omits the outside-NGC class (f), `cmd_dry_run` L5147: r006/r007 `if code==0 and rp.is_file():` becomes r008 `if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():`, caret line included. A second variant is FORMAL only: a `Path(report_dir)` failure shows at r007 L5146 but r008 L5147, and the real planner cannot reach it because it uses `report_dir` first. Visible only if `is_file()` raises a non-ignored OSError after the planner's own write. Top-level dry-run stderr only; class and text identical. | `tools/probe_classes_vc1.py r007 …` / `r008 …`, then `tools/compare_classes_vc1_v2.py … modname`: probe P6 | Disposition successor, no code change, adding this one entry with both texts and that scope. (a)–(e) need no entry. |

## NOTE (4)

- **N1 (TESTED, bytes).** The `scope` of SPEC_REGISTRY_CX3R008_V002 says "including the separately pinned r008 frame class" in the singular, but the disposition pins two r008-specific classes, and three once (f) is added.
- **N2 (TESTED).** The lens wording "the NGC branch was never exercised" is imprecise (see section 2). The conclusion it supports stands.
- **N3 (FORMAL; UNTESTED).** L5018 could appear outside the NGC contexts only through the known ST7-N6 routing race (the spec is rewritten between the dispatch read and the planner re-read), combined with a helper-load failure. This is covered by the existing ST7-N6 NOTE.
- **N4 (harness).** Formatted tracebacks name `Refusal` by my loader module (`vc1_r007`, `vc1_r008`). This is substituted as `<MOD>` in compare v2; in a real process both drivers use `__main__`. In P3 the raw text was truncated before normalization, so the second diff line there is a truncation artifact. The frame-level diff shows one changed frame only.

## Fence

- **Variant.** `tools/fence_c4v001.py` is a verbatim copy of f813c430, checked by sha. `tools/fence_c4v002.py` was produced by `tools/make_fence_v002_vc1.py`: four exact string replacements, a dry compile first, then an exclusive write. The changes:
  - a new function `_uvt_source_exception`;
  - `_forbidden_read` gains a `writing` flag;
  - the hook passes that flag in;
  - a header comment.

  A read-only open of a `uvt_*.py` source module is admitted only when the file name alone carries the `uvt_` prefix and no `runs_ext` component appears in the path. Both CLAUDE2 `runs_ext` roots are still refused first. Nothing else changes. The diff is `FENCE_DIFF_C4V001_TO_C4V002.txt`.
- **Self-test.** 24/24 pass (`FENCE_SELFTEST_C4V002_VC1.json`), with 14 intentional fence refusals and 12 intentional literal-stat refusals.
- **Installed first.** `tools/vc1_common.py` installs fence_c4v002 first, then:
  - a literal-path stat/list sentinel, so the fence's own `realpath()` never stats a protected path;
  - an open logger;
  - `sys.pycache_prefix`, pointed inside this folder.
- **BLOCKED lists in the probe processes (r007 and r008, both runs).** Fence 0, stat 0, protected opens 0. Outside this folder and the Python runtime, each process opened only its own driver and six pinned `.py` code modules, all read-only: the grid-cut helper, plus the five sources that `_ngc_v011_context` verifies (route-B binding, tail-manifest writer, worker, parallel worker, binding).
- **One refused open, in a process with no driver.** The first `build_results_vc1.py` attempt (21:18:18Z) was refused by the fence's NGC3198 name rule on the root V005 addendum. The open never happened, and that process wrote nothing. The addendum is a root decision record, not data; I read it with the Read tool for the A98 text, as the task directs. The builder now records that file's sha from `shasum` and does not open it.
- **Priority.** `taskpolicy -b` was accepted.

## Reproduction

Run from `verify_closure_1/` with `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` and `OMP/OPENBLAS/MKL/VECLIB_MAXIMUM/NUMEXPR_NUM_THREADS=1`. Each probe run needs a fresh run label, because sandbox directories are never reused.

1. `tools/make_fence_v002_vc1.py dry` then `tools/make_fence_v002_vc1.py real`, then `diff tools/fence_c4v001.py tools/fence_c4v002.py`.
2. `tools/fence_selftest_vc1.py`
3. `tools/diff_r007_r008_vc1.py`, then `tools/reach_map_vc1.py`.
4. `tools/scan_dry_logs_vc1.py`
5. `tools/probe_classes_vc1.py r007 out/PROBES_R007_VC1_<L>.json <L>` and `tools/probe_classes_vc1.py r008 out/PROBES_R008_VC1_<L>.json <L>`, where `<L>` is the run label.
6. `tools/compare_classes_vc1_v2.py out/PROBES_R007_VC1_<L>.json out/PROBES_R008_VC1_<L>.json out/COMPARE_<L>.json modname`
7. `tools/build_results_vc1.py <date -u>`
8. `shasum -a 256` on the root addendum.

The runs of record are `run2` (21:15:10Z). `run1` (21:10:57Z) used the same probes before an opens-report field was added, and gives the same comparison.

## UNTESTED

- Run mode and end-to-end saved records. That (c) reaches the saved `result.json` is FORMAL.
- A real-planner trigger for (f). I used a stub planner; L5147 runs after the dispatch returns, independent of the planner's internals.
- Codex3's 241/82/26 suites and its 78-plan identity, which belong to the author and lens 2.
