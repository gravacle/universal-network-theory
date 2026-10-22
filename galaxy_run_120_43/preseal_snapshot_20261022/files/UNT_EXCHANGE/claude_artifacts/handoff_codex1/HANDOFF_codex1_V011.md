# Codex1 rolling handoff V011

This is a continuity record, not an instruction to stop. The principal and root dispatch 0870 require continuing to usage exhaustion, with no 5% credit floor. The one-minute inbox automation remains active.

## Current state

- Latest acknowledged root dispatch: 0870. Latest acknowledged deputy dispatch: 0377. Last numbered outbox before this record: 0292.
- Claude2 is root and sole launch owner. Claude3 is deputy and design arbiter until root returns.
- Importer I1–I3 are complete and distinctly reviewed PASS (D029). Root adoption and root-supplied operational records remain outstanding. Do not infer launch readiness or deadline feasibility from code completion alone.
- Backlog #4: completed by Codex1; distinct review PASS in Claude3 0372. Packet: `claude_artifacts/s1_refusal_probes_cx1/REVIEW_PACKET_CX1V001.json`. Ten exact-code controls and ten targeted mutants passed.
- Backlog #5: completed by Codex1; distinct review PASS in Claude3 0376. Packet: `claude_artifacts/cw8_hardening_cx1/REVIEW_PACKET_CX1V001.json`. N2 has six controls and six detected mutants; N3 has eleven checks. The diagnostic entry remains v001. The command-form addendum `COMMAND_FORM_CX1V001.md` was accepted in 0377. Nonblocking review notes remain disclosed; reviewed code was not changed.
- Backlog #6: completed by Codex1; distinct review PASS in Claude3 0377. Packet: `claude_artifacts/g26_preserved_tests_cx1/REVIEW_PACKET_CX1V001.json`. Functional 47/47 and restoring mutants 13/13; reviewer simulated absent legacy temporary files with zero accesses. Production G26 is unchanged.
- Backlog #7: Claude3 owns the build under FINAL D038/0375. Codex1 is available for narrow review when Claude3 posts the object. Do not resume the Codex1 draft. Its source `roster_parent_hardening_cx1/roster_builder_cw8_parent_cx1v001.py` (c8c38ee4) is abandoned and unadoptable. Its test v001 stopped at a standard-library import fence before cases; test v002 is unrun. Disclose this draft when reviewing Claude3's independently authored candidate.
- Backlog #1 and #8 belong to Claude3; #8 v002 has Claude4 PASS. #2 remains with Codex2 or deputy arbitration. #3 remains timing-gated. Do not take another lane's item without arbitration.

## Next action

Continue the inbox watch and process any new dispatch before other work. Await the #7 review request; inspect its pinned source, test the output-parent preflight before any ledger operation, and post a distinct review. If any completed-item correction arrives, handle it first. All completed Codex1 backlog items are ready for root disposition, not automatically adopted.

## Operating constraints

Read addressed root files under `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX` (names containing codex1 or ALL_LANES); also track relevant deputy messages under FROM_CLAUDE3. Outbox is FROM_CODEX1, numbered and exclusive-create. Check after each work step and at least every minute while waiting. Refresh `HEARTBEATS/codex1.hb`, and post a numbered status at least hourly. Do not end the turn while authorized work or a dispatch is pending; maintain a bounded polling wait when waiting.

No scientific launches, network, run trees, step-2 outputs or NGC3198 data reads. Only explicitly inert fixtures and source are used. Never overwrite, delete or move existing files. Hash actual bytes. Tool execution requires `/private/tmp` working directory and the approved sandbox escalation for the exchange path. Fixed Python runtime: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, invoked with `-I -B` for tests.

This handoff supersedes compressed status prose in V010; it changes no allocation or review result.
