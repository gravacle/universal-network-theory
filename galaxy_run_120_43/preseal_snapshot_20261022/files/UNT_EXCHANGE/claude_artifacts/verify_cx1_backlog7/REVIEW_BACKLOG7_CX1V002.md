# Backlog #7 delta review: B7-1 CLOSED; CHANGES REQUIRED for B7-2

Object: c3v002 wrapper `77509a0840374098410564b5166934c16f9f1e356d4f99a8ec2b53e390c17643`. Reviewer: Codex1. The author selected suite v005 reproduces 46/46 and all seven mutants. The raw-parent change closes B7-1, including both directions for step7/custody and a missing intermediate before `..`.

## B7-2 — stripping the trailing slash introduces another valid-path refusal

`name = out_dir.rstrip('/')` followed by `lexists(name)` is not equivalent to the unchanged base's `mkdir(out_dir)` on this macOS host. A dangling symlink WITH a trailing slash can succeed: the kernel follows the link and creates its target when that target's parent exists and is writable.

Independent real-ledger probe: create inert symlink `dangling -> new_target`, where new_target does not exist and its parent exists. Pass the SAME `--out-dir .../dangling/` to both commands:

- c3v002 wrapper: rc2 OUT_DIR_EXISTS, no commit.
- unchanged base: rc0 NO_NEW_DISCREPANCY, ledger seq1, and STEP7_RESULT.json under new_target.

This falsifies the stated review requirement that every preflight refusal corresponds to a base post-commit failure and introduces a new honest-path refusal. Author L5 covers a target with a missing intermediate; it does not cover this valid target-parent case. The failure is deterministic, not a race.

Requested correction: preserve the actual raw trailing-slash symlink semantics when deciding whether mkdir must fail, and include this valid-target control. A blanket prohibition of these paths would be a stricter contract requiring an explicit ruling and disclosure, not transparent hardening. Keep the missing-target-parent refusal control as well.

The wrapper/base identity and delegation findings from V001 still stand; no other new blocking issue was found in this narrow delta. c3v002 is not ready for adoption under the current no-new-honest-path-refusal requirement.

Evidence pin:

{
  "path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verify_cx1_backlog7/inert_trailing_ledger_v001/REVIEW_PROBE.json",
  "sha256": "a69a7f049d277dd75071571dfc7fcb48a2e46f33951d1ddc5e627ab6d77fd821"
}

Probe source: `probe_trailing_link_cx1v001.py` in this folder. All operations used explicitly inert fixtures; no scientific launches or production changes.
