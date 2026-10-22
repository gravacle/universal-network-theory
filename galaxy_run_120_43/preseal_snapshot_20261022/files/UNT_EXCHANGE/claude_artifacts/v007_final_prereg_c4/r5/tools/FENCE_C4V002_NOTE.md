# fence_c4v002: what changed from fence_c4v001, and what every fenced run blocked

Claude4 r5 helper. 2026-10-18T21:04:27Z (`date -u`).

## Files (sha256 from bytes)

| file | sha256 |
|---|---|
| `tools/fence_c4v001.py`, exact copy of `review_launch_packet_0559_c4/tools/fence_c4v001.py` | `f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0` |
| `tools/fence_c4v002.py` | `53078e39b34a22d1ee83e5b2d68c85e7644970838a2c88974397bb31912c1a4e` |
| `tools/make_fence_c4v002.py` (five anchored edits on the exact copy, exclusive create) | see HASHES.txt |
| `out/FENCE_C4V001_TO_C4V002.diff` (unified diff, 120 lines) | `7dbeeb4bde414c459bdd7193bf44af18aaaf4928d0e2b6a7c5199b5d739ecb6e` |

## The only change: two READ-ONLY exceptions

- **(a) `uvt_*.py` source modules outside every runs_ext tree.** It applies only when, in both the literal and the real path:
  - the basename (casefolded) starts `uvt_` and ends `.py`;
  - no directory component starts `uvt_`;
  - no component is `runs_ext`.

  It lifts only the UVT-component rule for that basename.
- **(b) The root decision addenda.** It covers `CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md`, with the literal and real path directly in the CLAUDE2 control folder. It lifts only the NGC3198 rule. These files are decision records, not data (seal rehearsal D-11).
  - Scratch copies of them inside this folder were already readable under v001's in-folder rule, so they needed no change.
- **Both apply to reads only.** `_forbidden_read(lit, real, writing)` grants an exception only when the open carries no write flag. Writes outside this folder stay refused by the unchanged write rule.
- **Every other block is unchanged.** That covers: process creation and kill; network; delete; writes, renames, links and chmod outside this folder; opens of both CLAUDE2 runs_ext roots; any `UVT_*` component (directories included); the C5H run name; the target words rotmod, Vobs, MassModels and SPARC; and other NGC3198 data.
- `selftest()` is unchanged (8 trials). The new `selftest_v002()` (17 cases) tests both exceptions as path predicates only, so no protected file is opened.
  - Allowed: a uvt_*.py read; the V004/V005/FROZEN addendum reads; a `.py` with ngc3198 in its name (as in v001).
  - Refused: the same reads with a write flag; a `UVT_*` directory component; a uvt_ non-.py file; a uvt_*.py under any `runs_ext` component; the C5H name; an addendum name in a subfolder or elsewhere; a non-addendum NGC3198 decision file; `.json` addendum look-alikes; target words.

## Runs under fence_c4v002 (runner `tools/run_fenced_c4r5.py` refuses unless the fence sha matches and both selftests pass)

| run | selftest | selftest_v002 | BLOCKED after the selftests |
|---|---|---|---|
| CB1: `tools/build_case_block_c4v001.py` (the case block build and validation) | 8/8 | 17/17 | [] |
| CB2: `tools/check_r5_case_block_path_c4v001.py` (r12 sealed-mode case-block steps on r5 and r4) | 8/8 | 17/17 | [] |
| T1: seal tool 1 v001, dry run on r5 (it read the frozen V002–V004 addenda under exception (b)) | 8/8 | 17/17 | [] |

The 8 entries `selftest()` itself adds to BLOCKED are its own trials, each refused as designed: popen, os.system, socket, a write outside the folder, a read in runs_ext, a UVT path and a target word, and a delete.

The loader `tools/load_r12_c4r5.py` adds a stat guard as defence in depth, because stat raises no audit event. It refuses stat on a C5H name, on runs_ext/uvt_ and on /.vol. It refused 0 in CB1 and CB2.

The permission system did not refuse running fence_c4v002. The rehearsal's rv1 variant was refused (D-11).
