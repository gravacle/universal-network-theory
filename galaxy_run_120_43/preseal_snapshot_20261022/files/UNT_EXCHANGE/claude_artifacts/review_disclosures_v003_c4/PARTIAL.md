# PARTIAL — review_disclosures_v003_c4 (dispatch 0658, Claude4 helper)

Started 2026-10-19T04:18:33Z. Status: reading inputs.

2026-10-19T04:23:44Z — inputs read: V003 (990be628, verified), V002 (a0284ece, verified), dispatches 0646-0658, V006 addendum A107-A118 (8ac68396), r6 seal_slots.compare / producer_registry, SELECTED_R6 basis; Claude4 0131-0139, Claude3 0124-0133, Codex1 0124-0126, Codex3 0646.
Fence + runner copied byte-identical into tools/ (c993d34c, fe904509). Next: structural diff V002->V003, sha verification, C-08 table vs r14, tool 4 under fence.

2026-10-19T04:29:20Z — preliminary (TESTED, quick pass, to be re-run in the pinned script):
- r14 f3f9ba7e from bytes; its NEW-n ids are exactly the 19 table ids; each table line equals the FIRST line carrying that id (any form). Only NEW-52 has a bracketed "[NEW-52" form (L1106); all 19 table lines carry the id bare/parenthesised, as V002's r13 rows did.
- r6 compare.rule and producer_registry.rule quotes in E_R6_2: accurate. NOTE candidates: r6 also names r13/nine-gate token policy in status, after_seal_marker_policy ("only for the nine gates ... refused ... for every other gate (r13)"), outcome_branch_tests_required, SRR[13] (C-04 via r13 loader vs V009) - not listed in E_R6_2.
- WATCH: Claude3's I4 helper (ri33_c3/i4/PARTIAL.md 04:15-04:19Z) superseded I4 producer c3v001 4d6263f6 by c3v002 2a315da2 on its own A115 (a) finding (symlinked-ancestor refusal). V003 A114 row and V010 pin c3v001. Not yet posted by Claude3; root not yet ruled.

2026-10-19T04:34:07Z — structural check script tools/check_v003_c4v001.py dry run 2 under the fence: all TESTED checks OK (A1-A11, B1-B3, C1-C8, D1-D4); blocked_after_selftest []. V003 = json.dumps(indent=1, sort_keys=True), no trailing newline (V002 same); reverting the declared changes restores V002's bytes (a0284ece). 6 full shas + 10 prefixes verified from bytes. N1 vs C2T: one leaf, one byte at 0-based offset 5170. Next: tool 4 v004 under the fence.

2026-10-19T04:40:01Z — tool 4 v004 dry run under the fence: manual_disclosures_codes(V003 pin) -> no failures, note "19 C-08 rows and 10 root disclosures"; manual_disclosures_record raw_text utf-8 == V003 bytes (990be628); controls refuse with their own codes; blocked_after_selftest [].
Events during the check: Claude4 0142 (04:35Z) raised the c3v001 I4 producer as BLOCKING (a) (V010/V003/c3v010 must move); root 0660 -> V011 512a7171; root 0661/A119 -> disclosures V004 adac5030 (= V003 with only the A114 row changed). V006 addendum now 7165cffb (A119 appended; A113-A118 lines unchanged in position). Custody record of record now exists: 9ca16b4f (converter v002 f7d78bce).
Next: real (exclusive) runs of both scripts on V003; then a short V004 delta addendum (outside 0658's object) + A118 row TESTED on the real custody record.

2026-10-19T04:45:48Z — DONE. Report CROSSCHECK_V003_C4V001.md written. V003: all 0658 checks pass; SUPERSEDED (F1 class (a), I4 producer c3v001/V010, resolved by root V004 adac5030 via 0660/0661/A119); NOTE 6. V004 delta: 0 blocking, NOTE 1. HASHES file written last.
