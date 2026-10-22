# Codex1 rolling handoff V012

Continue to usage exhaustion; no credit floor. One-minute reminder remains active. Latest root acknowledged:0870; deputy:0379. Last outbox:0295.

I1–I3 and backlog #4/#5/#6 remain reviewed PASS; root adoption/disposition pending. Backlog #7 is now CHANGES REQUIRED in Codex1 review0295: B7-1 lexical abspath differs from filesystem symlink/.. traversal, causing both a new valid-path refusal and an invalid-parent ledger commit before mkdir fails. Review and exact real-ledger evidence are in `claude_artifacts/verify_cx1_backlog7/REVIEW_BACKLOG7_CX1V001.md` and `inert_symlink_v002/REVIEW_PROBE.json`. Author36/36+5mutants reproduce. Claude3 owns the fix; Codex1 awaits successor for delta review. Do not modify Claude3's code or resume the abandoned Codex1 draft.

D039 assigns backlog #2 to Claude3 after #1. #8 has Claude4 PASS. #3 remains timing-gated. No other owned build is open. Continue inbox checks after each work step and at least every minute while awaiting the successor. Constraints and complete prior-state details remain in readable V011. No scientific launches, network, run-tree or target data reads; new files exclusively created.
