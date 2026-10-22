# PARTIAL — verify_targetfree_1 (R2C-B1)

Started: 2026-10-18T20:28:45Z (date -u)
Status: started; reading the object, the lens report and the V005 root text.

## Progress 2026-10-18T20:34:08Z
- Object: all 10 HASHES_R2 entries match shasum (20:28Z).
- V005 read 20:29:39Z: 7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2 (copied to snapshots/V005_AT_VERIFY.md). No V006.
- Quotes verified: INDEX_R2 L12, ROOT_ITEMS_R2 L129, PREREG L584 (no-change list), PREREG L561/L565.
- Independent T7/pin recheck (tools/recheck_t7_vtf1.py -> runs/T7_RECHECK_VTF1.json): 991cc242 later=[] (PASS at assembly);
  cf9bbf19 later=[A97,A98]; ff7980e8 later=[A97,A98,A99]; 7f552858 later=[A97..A100]; 14/14 pins match in all four.
- Diffs: 991cc242->cf9bbf19 is a pure 33-line insert after L889 (A98 L890-901, A97 L903-921); later snapshots pure inserts (A99, A100).
- Next: which round did Codex2 0490 review (round 1 or round 2)? Does A98 apply to round 2's bytes?

## Progress 2026-10-18T20:39:21Z
- Codex2 0490 (20:01:30Z, 3a922168...) reviewed ROUND 2 (PREREG 97d5ce33...): FAIL, REACH-B1 blocking. A98.2 (20:04Z) adopts it; 0619 orders r3.
- Same semantic blocker already BLOCKING in closure F2 and newdefects R2B-01. newdefects R2B-13 rates the same currency fact NOTE.
- Round-1 precedent: the same later-entry class (B-6, L-C11, A-11) was SHOULD_FIX, when the tool did not catch it; round-2 T7 catches it.
- A98 section sha stable under root insertions (cf9bbf19, ff7980e8, 7f552858): runs/NEW_ENTRY_SECTIONS_VTF1.json.
- Object mentions V007 only at PREREG L561; no B2/BUILD/prereg r5 refs, so A97, A99, A100 do not touch the text.
- Draft verdict: facts confirmed (not refuted); BLOCKING overstated -> NOTE (dedupe into A98 / F2 / R2B-01); fix incomplete (no seal-time T7 re-run).

## Done 2026-10-18T20:44:05Z
- Complement replay (runs/COMPLEMENT_REPLAY_VTF1.json): generator v003 logic reproduces L584 on 991cc242; on 7f552858 gives A91-A100 (A98 inside) and T7 PASS.
- VERIFY.md and REVIEW.md written. Verdict: not refuted on facts; severity NOTE; fix partly sufficient (better fix in VERIFY section 4).

## Addendum 2026-10-18T20:45:17Z
- V005 changed during verification: 5a996e97... at 20:44:14Z adds only A101 (B2 record of record; registry V008; V007 path). Snapshot V005_AT_VERIFY_2.md.
- Rechecks on 5a996e97: 14/14 pins match; T7 later A97-A101; A98 section sha unchanged; complement replay A91-A101, T7 PASS. VERIFY and REVIEW updated.

## Final 2026-10-18T20:48:40Z
- V005 changed again: 70a48f51... at 20:45:25Z; A101 amended in place (L898-904): V007 case block and "Step-5 open item closed (A90)" (LO I1-T TESTED PASS, Codex1 0066).
  That part touches PREREG [C-I6] L79 ("NOT_RUN") and D-4 L451; it needs a reasoned disposition. VERIFY section 3c and section 4 gap 5 updated. Pins still 14/14; A98 section unchanged.
- V005 still 70a48f51 at 20:48:01Z; no V006.
- VERIFY.md.tmp_vtf1 and REVIEW.md.tmp_vtf1 are byte-identical copies of the finals, left in place (rule 3: no deletes, no moves).
- Verdict unchanged: refuted false (facts confirmed); severity NOTE; fix insufficient as worded (better fix in VERIFY section 4).
