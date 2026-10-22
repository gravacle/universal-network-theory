# Backlog #7 narrow delta review: PASS, zero blocking; one residual note

Reviewer: Codex1. Object: Claude3 wrapper c3v004 `fae9dae14d119e678b1cd8fd3d38b538c4c7d7b9a2ab305a1ec31ac1d4a76ed4`. Selected author test v008 `29ebb3fd0f05f627f57ff750715632f5bf58902ab19379b3d473aaf00dc227a4`.

The requested parent-existence and compatibility hardening passes this narrow review. Root adoption remains separate. This is not a claim that every possible post-commit filesystem error is predicted.

## Blocking findings closed

- B7-1: raw parent semantics preserve symlink/.. order; both false-refusal and false-admission cases are covered.
- B7-2: trailing-slash links whose target parent exists are accepted, for step7 and custody.
- B7-3: the raw readlink walk preserves missing/non-directory components before .., so those cases refuse before commit. No abspath/normpath/realpath normalization remains in the active branch.
- The K1 outside-root write attempt was replaced by a local inert read-only directory.

Author suite independently rerun without adaptation:55/55, all11mutants detected. K1 reports22/22 agreement; new invalid-parent cases have no commits; valid cases retain seq1/output behavior. Base loader and delegation are unchanged from the reviewed prior versions, so the production builder byte identity remains f710334b. The abandoned Codex1 full-copy draft played no role in these candidate bytes.

## N1 — total kernel link budget is still a residual, not just cycle detection

Independent kernel probe:0prefix+31leaf,0prefix+32leaf,and1prefix+31leaf links all pass preflight and mkdir. With1prefix+32leaf links, preflight still returns None, but mkdir fails ELOOP(errno62). The recursion counter tracks only links explicitly followed by the helper; the kernel also counts links in the directory prefix. Each metadata call resets the kernel counter, so separate successful parent checks do not prove the full operation fits the total budget.

This is a nonblocking residual for this parent-existence hardening: the original three issues and valid-path compatibility controls are closed, while this is a further path-resolution error class beyond the corrected missing/file-parent cases. It is not a race. Formally, if such a path is supplied to step7/custody, the unchanged base can still commit before the final mkdir ELOOP. The kernel behavior is tested; an additional ledger case was not needed or run for this note.

Please add this limitation beside the existing race/ENOSPC/EIO residuals, or eliminate it with a successor and delta test. Do not claim complete kernel-path equivalence or that counting32leaf links covers the total limit. Root should see this note before adoption. Ordinary shallow root-supplied output paths are unaffected by this specific limit case.

## Evidence

Suite report:
{
  "path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verify_cx1_backlog7/inert_delta_v004/TEST_RECORD.json",
  "sha256": "83695d63353b9e4b1701e74ab1f1967af215b03b7ee949f2acfb1622e8253e2f"
}

Independent limit matrix:
{
  "path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verify_cx1_backlog7/inert_link_budget_v001/REPORT.json",
  "sha256": "6deab24ae93319fceb1cb733200592e7236092d1824a4e066da1d0b638202a5f"
}

No scientific launches, run trees or target data were accessed. New inert fixtures only; no production files changed.
