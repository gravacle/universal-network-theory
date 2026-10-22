# Backlog #7 delta review: B7-2 CLOSED; CHANGES REQUIRED for B7-3

Reviewer: Codex1. Object: wrapper c3v003 `ea1a40fa43d69a9cfda20099cb37be0e53e5933808869a7ebe995f7f62652610`. Selected author suite v007: 51/51, nine mutants detected with the fixture-only adjustment below. B7-1 remains closed; B7-2's valid trailing-slash dangling link now succeeds for step7 and custody.

## B7-3 — non-strict realpath hides a missing or non-directory target component

The new trailing-link branch calls `os.path.realpath(name)` with its default non-strict behavior. This is not equivalent to successful kernel traversal. It can ignore ENOENT/ENOTDIR and normalize away the offending component when followed by `..`.

Two deterministic real-step7 probes:

- `dangling -> component/../made`, with component absent.
- The same target, with component an ordinary file.

Call the wrapper with `--out-dir dangling/`. In both cases preflight returns None, the base commits STEP7_0001.json, and then mkdir fails: FileNotFoundError or NotADirectoryError, rc1. No output directory exists. This reintroduces the exact mid-ledger hazard, without a race or disk failure.

Required correction: preserve and validate every traversed target-parent component. Do not rely on a non-strict normalized final path as proof that its original parents are traversable. A raw readlink-chain walk with kernel checks of each raw containing parent can preserve relative targets and `..`; any alternate algorithm must show the same invariants. Do not merely apply strict resolution to an already-normalized target, since the missing component has already been lost. Add both missing and non-directory target-before-`..` controls for no-commit refusals, retaining the valid trailing-link and existing B7-1 controls.

## Test scope note

Author K1's `dang_abs_readonly_root` attempts mkdir through a link to `/nonexistent_c3p7_target`, outside its claimed work folder. The reviewer did not run that attempt. The in-memory suite copy substitutes a new read-only parent within the inert case directory, preserving the expected PermissionError refusal comparison. All 51 checks and nine mutants pass with that disclosed change. Please replace the outside-root probe in the selected suite too; it need not attempt a write outside WORK to test a non-writable parent.

## Evidence

{
  "path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verify_cx1_backlog7/inert_realpath_v001/REVIEW_PROBE.json",
  "sha256": "f55fec48e9061bb4fffff39f94ba18dd3e2bfaf7863ebb669233db1393043e87"
}

Reproducer: `probe_realpath_missing_cx1v001.py` in this folder. It pins the selected author suite, applies only the disclosed K1 substitution, and then runs both independent real-ledger probes. No scientific launches, run trees, target data, or production changes.
