# Selected helper011 lexical delta — Codex1 local review

`date -u`: Sun Oct 18 23:05:20 UTC 2026

**TESTED PASS; 28/28 checks; 0 new blocking findings in this helper delta.** This selected helper is a baseline awaiting the 0643 integration successor. This is not approval to run a seal.

The only executable delta from helper010 is the new lexical component rejection in `c_output_root`, source lines 1063–1064. Removing that exact `if` produces an AST identical to the entire helper010 module; header comments are the only other textual change. Empty, dot and dot-dot components are checked before `_volume_dev` (line 1069), any no-follow walk, or either `mkdir` (lines 1109 and 1117). Existing `path_policy` already refuses empty arguments, doubled slashes and a trailing slash.

**TESTED runtime:** 21 negative cases cover absent parent plus final `..`, interior `..`, final `.`, interior `.`, empty component/double slash, trailing slash and empty argument, each in check/create/verify mode. Every case raised the expected typed Refuse with zero calls to instrumented filesystem boundaries and unchanged fixture entries; each missing parent remained absent. The boundary traps would fail the case before any unintended underlying IO. A single ordinary owned path passed check without creating its absent parent, then create made its new parent and empty root, then verify accepted the same recorded device/inode using actual macOS kernel calls. Three source/evidence checks and actual nice10 account for the remaining four checks.

**Carried, not repeated:** helper010's independently recorded 29/29 evidence was verified from bytes. The exact whole-module AST equality after removing the new lexical guard limits this delta to that guard. These 29 cases are not included in the new 28-check count.

**UNTESTED/outside scope:** original root script execution, production output directories, scientific work, protected metadata, and final r6/v003 wiring. No author file changed. Runtime compiled the checked owned helper buffer under a non-main name. All created fixtures and reports remain under this exclusive review subdirectory. No full seal or comparator was run.

## Byte SHA256 pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_publication_v003/seal_steps_c3sa_c3v011.py`
  SHA256 `7caad125be19160c6e431dcf6be8f038cb9bba172c95f1f8059ebcdd938a0aff`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_helper010_snapshot_v001/helper.py`
  SHA256 `823c8aca8c230d78f6a4c2e3a7b494a64546030622e4b186db799f873c537df2`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/helper010_controls_v001/RESULTS.json`
  SHA256 `fad8dace9adc7dd2f7d098c780778193c1cc66b26888163ad654c1dfd38c8d93`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_publication_v003/helper_delta_cx1v001/review_helper011_cx1v001.py`
  SHA256 `9c9da8d95f7916a62e519b672db198fa2e6164b16de4386482fe0470b7c5e420`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_publication_v003/helper_delta_cx1v001/RESULTS_CX1V001.json`
  SHA256 `178e443ee8a4f78cb24cd92171509756442ee18cc958a2d26d4d736aa6600090`

