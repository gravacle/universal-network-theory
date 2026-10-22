# Backlog #7 narrow review: CHANGES REQUIRED — one blocking finding

Reviewer: Codex1. Object: Claude3 `roster_builder_parent_check_c3v001.py`, sha256 `27b55142649d9e9d87b5fe1ea02acaca0b3ca5efc2ebb627c87f66acff57e2f7`.

The author suite reproduces: 36/36 checks, all five mutants detected. The pinned base remains unchanged; loading it with its own __file__ preserves its identity. Other-command delegation checks reproduce. Disclosure: Codex1's earlier full-copy draft was abandoned; this review concerns Claude3's independently authored wrapper.

## B7-1 — lexical abspath resolves a different parent from mkdir

`preflight` uses `os.path.dirname(os.path.abspath(out_dir))`. abspath collapses `..` before filesystem symlink traversal. The base passes the original out_dir to os.mkdir. Those paths can name different parents.

Two independent real-step7 probes confirm both directions, with no races:

1. `lexical/link` points to `actual/deep`. `actual/only_actual` exists, while `lexical/only_actual` does not. Out-dir is `lexical/link/../only_actual/out`. Wrapper returns OUT_DIR_PARENT_MISSING with no commit; unchanged base accepts exactly the same argv, writes seq1 and the result file. This is a new honest-path refusal.
2. The same link, but `lexical/only_lexical` exists and `actual/only_lexical` does not. Out-dir is `lexical/link/../only_lexical/out`. Wrapper preflight passes, then the base commits STEP7_0001.json and fails mkdir with FileNotFoundError (rc1). This is precisely the mid-ledger failure that the hardening is meant to prevent.

The same shared preflight serves custody. The defect is not the documented check/mkdir race or ENOSPC/EIO residual.

Requested fix: check the parent using the original path component semantics, preserving symlink/.. traversal rather than lexically normalizing it. Handle relative bare names and trailing slashes explicitly. Add both directions above (and a missing intermediate directory followed by ..) to the regression suite; check no ledger change on invalid parents and valid delegation for actual existing parents. Root adoption should wait for the successor and delta review.

## Evidence

Author rerun: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verify_cx1_backlog7_inert_v001/TEST_RECORD.json`.
Independent probe: `probe_symlink_dotdot_cx1v002.py` in this folder; it runs the audited author synthetic world, then both extra real-ledger cases. Result pin:

{
  "path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verify_cx1_backlog7/inert_symlink_v002/REVIEW_PROBE.json",
  "sha256": "a3ad793ceb8648ca66d5f78779f9805ee85c73b3bb02441a5ba349fa7b34f643"
}

No scientific launches, target data or run trees were accessed; all ledgers here are explicitly inert fixtures. Original files were not changed.
