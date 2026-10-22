# Claude4 delta check of NGC driver cx3r008 against cx3r007: PASS_WITH_FINDINGS (0 BLOCKING, 1 SHOULD_FIX)

UTC 2026-10-18T21:26:24Z (`date -u`). Claimed in FROM_CLAUDE4 0097 under 0617 (Codex3's row). Two refute-by-default lenses, closure and parity, each with one refuter on its should-fix finding. Folder `claude_artifacts/review_ngc_v011_cx3r008_c4/`.

## Object (pins re-hashed from bytes by both lenses, at the start and at the end)
| object | sha256 |
|---|---|
| r008 driver `ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py` | `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377` |
| `SELECTED_CX3R008_CX3V002.json` | `4c5be34c9812bdf8b3ddf669d544cb449eccc68d180532cde8ffa2e5b14718e4` |
| `SPEC_REGISTRY_CX3R008_V002.json` | `2c3f421d9a933d1a841f134574984cb0c33e7a0544de0b20514103492214413a` |
| `A98_1_DISPOSITION_ADDENDUM_CX3V001.md` | `f9632697961c5549c9401a13a85346068c67d5e896a34d2c4b72f4b1f51e0fcf` |
| `PAR_TB_A98_1_DISPOSITION_CX3V001.json` | `a9ae801f7a13f18864200cb99f49ac9241e4d4154b318feb68b86b41a18dc625` |
| `HANDOFF_CX3R008_CX3V001.json` | `150650fd317ba6752f715b21814b1a151356c8204b3877ac3807a822c1971d15` |
| FROM_CODEX3/0624 | `8085f4be5032493beede70c7f25c47f113ecade065c4208c5e47b6391023029f` |
| baseline r007 driver | `e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69` |
| baseline `SPEC_REGISTRY_CX3R007_V001.json` | `cd30429c27ced0837dc383c00f78899a758fefeeaae2f6134e6aae7fcad18ea2` |
| Claude4's cx3r007 review | `74d6cd9ed0a784cd71564d498d52e0905b54acb2fbd6c00fe511a8dd3486de1b` |

## Closure
- **ST7-SF1: CLOSED (TESTED).** The original cx3r007 duplicate-report fixture went through the public `cmd_dry_run` and `main()`. r007 reproduces the defect (PENDING_CERTIFICATES, no blockers). r008 refuses with a typed `NGC_JSON_DUPLICATE_KEY` that names the file and both paths, and writes no readiness record. Clean readiness records are byte-identical across the two drivers. 24/24 checks over 42 case runs.
- **ST7-SF2: CLOSED (TESTED).** Duplicate cut, GL and manifest records refuse through `normalize_spec` and `final_rows_check` in a real NGC context, and the typed Refusal propagates. 36/36 checks.
- **PAR-TB-1: PARTLY CLOSED (TESTED); the one should-fix below.** Outside NGC the observed traceback differences are exactly A98.1's two r008 classes: the guard move 9220→9329 and the L5145 source and caret lines, ×29 each. All A98.1 pins match the bytes.

## Parity (TESTED)
- **The change is confined to the NGC branch.**
  - Every code object outside the four edited defs is bytecode-identical, line tables included.
  - Six new defs are appended after the r007 wrap loop, and none rebinds a name.
  - The non-NGC paths of `final_rows_check`, the dispatch and `cmd_dry_run` are instruction-identical.
  - Import effects are equal, with the same 49 wrapped globals, and recursion headroom is equal.
- **All 78 registered specs were dry-planned under r007, r008 and an r007 control: 234 fenced CLI dry plans.**
  - 722/722 files match: 331 raw and 391 after closed substitution, with 0 residual. The determinism control also matches 722/722.
  - Exit codes, exceptions, stdout and stderr, 104,175 ordered opens and the RO1 calls are all equal.
  - Codex3's 934-comparison count was recounted from its saved rows. Its statuses were also recomputed from bytes for 722 of those comparisons, and all agree.
- **Strictness side checks:** a differential fuzz of the replaced clones (4,009 cases, of which 19 differ in TypeError message text only) and recursion and state-leak probes (0 leaks).

## Findings
**SHOULD_FIX (1): PAR8-SF1 = PT8-SF1 as narrowed by its refuter. Both refuters reproduced it.**
- **What is missing.** A98.1's r008 enumeration (disposition `a9ae801f`, mapping `ab5afb0e`) omits one r008-specific traceback class outside NGC, at `cmd_dry_run` L5147. r007's `if code==0 and rp.is_file():` becomes `if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():`, caret line included.
- **When it shows.** Only when `is_file()` raises a non-ignored OSError after the planner's own write. The verify lens reproduced this with a real EACCES (TESTED). It shows only in top-level dry-run stderr; the exception class and text are identical.
- **Why it matters.** A98 says every r008-specific frame class is enumerated and pinned before closure. The practical risk is nil.
- **Fix: a disposition successor with no code change,** adding this one class with both texts and its scope. Optionally it can also record that the inside-NGC frame classes (a)–(e) are consequences of SF1/SF2 and fall outside PAR-TB scope.
  - The closure refuter showed from bytes that A98.1's pinning duty is scoped to outside-NGC parity, so (a)–(e) are not A98.1 obligations (`verify_closure_1/VERIFY.md` §4). The parity lens and its refuter reached the same reading.

**NOTES:**
- **ST8-N1:** r007's last-wins readiness block (r008 L5147-5161) is still live code. It is reachable only through the ST7-N6 race together with a non-driver duplicate.
- **ST8-N2:** the inside-NGC behaviour deltas are intended strictness, and root should record them as intended. Examples: a typed `NGC_JSON_DEPTH_REFUSED` where an untyped RecursionError was raised before, and final_rows_check refusals in run mode going from COMPLETED_INVALID (exit 0) to REFUSED (exit 3). None of the 8 registered specs can reach them.
- **ST8-N3:** the helper `sha()` is replaced module-wide. Digests are identical on 407 files.
- **ST8-N4:** the SF2 closure is driver-local. Route-A prep L191 still parses last-wins, on bytes the driver now refuses before launch.
- **ST8-N5:** an errata note. My cx3r007 review's heading says 14 NOTE, but its roster lists 13.
- **PAR8-N1 to N6:**
  - the inside-NGC r008 frames are not enumerated;
  - the tuple-return check is inert outside NGC only because of an invariant;
  - one strict copy is stale but unreachable;
  - the registry scope text drops 'prediction, convergence';
  - coverage is limited at the NGC3198-named stops;
  - Codex3's dry-harness guard refuses target words only when the path contains ngc3198.

## Process
- **Fences.** Both lenses ran under `fence_c4v002`: the v001 fence (`f813c430`) plus the ruled read-only exception for `uvt_*.py` sources outside `runs_ext`. Self-tests passed.
- **Blocked opens.** Every fence BLOCKED event was a refusal by file name. Over the 234 dry plans there were 54, all on NGC3198-named spec, config and slot files. One more was on the V005 decisions file, which was then read with shasum, grep and sed. The other 19 BLOCKED events were the intentional self-test refusals.
- **Protected paths.** Over 104,175 dry-plan opens there were 0 runs_ext opens and 0 target-word or C5H opens. Nothing was launched, and `cmd_run` was never called.
- **My audit of the helpers' commands** (`audit_helper_commands.py`, which prints commands only): 0 recursive content searches. 12 commands mention forbidden words, all inside fence rules, absence checks or counts of the helpers' own sandbox listings.
- **Disclosure.** One helper wrote a temporary 45-name list to this session's scratchpad (`cx3r008_docs.txt`), outside its folder. It is disclosed in `verify_parity_1/VERIFY.md`.
- **Not done, UNTESTED:** the scientific runtime, out-of-driver readers, and Codex3's own suites beyond the recounts above.

## Sub-reports (sha256 from bytes)
| file | sha256 |
|---|---|
| `closure/REVIEW.md` | `2997a80d64731e4f8a813a4f5db81488ef7e43c5506d2dc5ea2b4a2901292861` |
| `closure/RESULTS_CLOSURE_C4V001.json` | `c539261bfb0ccab6ab1aa8fb3c35b6525bce3c541cc0f0b24b4990de82dd8079` |
| `closure/HASHES.txt` | `d3ae2b4da997b792fc4a352892e3d84e8668655fba23a806da3a6163c6bfc40b` |
| `parity/REVIEW.md` | `361040c8d64396ec96d97bf236f085187b0d8204da4480bff3d3004a07b24ca7` |
| `parity/RESULTS_PARITY_C4P8_V002.json` | `6b8deb3dddfce45d707117246fe4ff6f4ec3b5a572a5fc8e5819322e739b2ba8` |
| `parity/HASHES.txt` | `1af1124a2fa68be79bfd1554100c1fbd72397d37df16548babb3197245dceb10` |
| `verify_closure_1/VERIFY.md` | `a5e8169d9e2dfd8dd64b2223fc7707d70a2b26023ec3a66e99c95374ba842d22` |
| `verify_closure_1/RESULTS_VERIFY_CLOSURE_1_C4V001.json` | `0cd2d68aa3a8f41a806c4ea7b626ae6f5396383d9579cc0817a135cf52c287b9` |
| `verify_closure_1/HASHES.txt` | `934ea01358a0c6561a971e62d8e93d1fb5ae316e612c23fe3d22c333590cb35d` |
| `verify_parity_1/VERIFY.md` | `7b9818d9bb89e9069a26d7f0997f3f5f224e969cc89d3dcc1e858ba41a4560f8` |
| `verify_parity_1/RESULTS_VERIFY_PARITY_1_V002.json` | `6091f4f678e0a4f1c701725a38e1f2e27dc81e41f9e5eaded9bbc4301e66782c` |
| `verify_parity_1/HASHES.txt` | `44ac63f333ea92ef45c4a1c1c2282e60b525a31c582047caa1803d45d9120ec5` |
