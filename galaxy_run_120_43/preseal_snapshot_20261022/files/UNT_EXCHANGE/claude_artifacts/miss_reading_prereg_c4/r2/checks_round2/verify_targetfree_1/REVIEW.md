# REVIEW: verify_targetfree_1, the adversarial verification of round-2 targetfree finding R2C-B1

Written 2026-10-18T20:43Z and updated at 20:48Z (`date -u`). The full record is in `VERIFY.md`, in this folder.

- **Finding:** R2C-B1 (BLOCKING). T7 currency now FAILs, because A97 and A98 postdate assembly and A98 rules this r2 FAIL.
- **Object:** round 2. All 10 HASHES_R2 entries match. V005 was read at 20:29:39Z as `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2`, and it was the same at 20:39:54Z.
  - At 20:44:14Z it was `5a996e97d633cc11a4cb255fe8ba1cdf746d93367621c004aca29382affb6a26`. That adds A101 (the B2 record and registry V008).
  - At 20:45:25Z it was `70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e`. A101 had been amended in place: the V007 case block, and "Step-5 open item closed (A90)", with the LO I1-T precondition TESTED PASS.
  - On both, T7 later = [A97–A101] and the pins still match 14/14. No V006 exists.
- **Result: NOT REFUTED on the facts. The severity is reduced to NOTE.**

**Facts confirmed from bytes:**
- The quotes are verbatim: INDEX L12 and ROOT_ITEMS L129.
- A97 (20:02Z), A98 (20:04Z), A99 (20:20Z) and A100 (20:24Z) are in V005. A98.2 reads "Miss-reading prereg r2 (Codex2 0490): FAIL, 1 blocking and 1 should-fix" and "Claude4 builds r3 (0619)".
- Codex2 0490 reviewed round 2 itself (PREREG `97d5ce33…`).
- The lens's runs show what it says: T7 later = [A97, A98] at 20:06:05Z and [A97–A100] at 20:25:52Z, 14/14 pins match, and mutation all_ok is False only through the baseline currency.
- The `991cc242` → `cf9bbf19` diff is a pure insert of A98 (L890–901) and A97 (L903–921).
- An independent recheck from separate code agrees: 14/14 pins on four snapshots, and T7 later = [] at assembly.

**Not defective:**
- INDEX L12 truly describes the bundled check, which was computed at 19:55:19Z against the V005 sha that INDEX L18 names.
- ROOT_ITEMS L129 is the rule being applied, and T7 is doing what L129 says it does.
- One loose step: L129 allows "an explicit no-change note in the seal entry". So what bars sealing r2 is A98.2's content, not item 4 alone.

**Severity: NOTE, not BLOCKING.**
- The blocker is A98.2, root's adoption of Codex2 REACH-B1. That is already BLOCKING in this round as closure F2 and newdefects R2B-01. B1 counts it again.
- A T7 FAIL after assembly is the designed signal (check L353).
- A97, A99 and A100 trip T7 too, yet none touches the text.
- Amended A101 does touch it, without danger. It closes the A90 LO I1-T item, which PREREG [C-I6] L79 calls "NOT_RUN" and which D-4 L451 already says to record. It needs a reasoned disposition, which is routine M-6 item 4 work.
- Round 1 rated this class SHOULD_FIX when the tool could not see it (B-6, L-C11, A-11). The newdefects lens rates the same fact NOTE (R2B-13).
- The work left for r3 is already SHOULD_FIX under R2C-S6(a) and closure F3.

**Fix: right in part.**
- The dispositions are right.
- An A98 section pin is stable across the five snapshots that contain A98: `181248d91db1437786cc8654c4dc82bb3983ea36a069f702f6dfd2acadfd8aa9`.
- **Gaps:**
  - "Re-run T7 at r3 assembly" passes by construction while generator v003 computes the list. In the replay, A98 and A101 land in "A91–A101" and T7 passes.
  - Nothing re-checks at the seal, and the CLI exits 0 on a currency FAIL.
  - The INDEX line has no basis.
  - A98's section also holds A98.1 (PAR-TB), which may be amended in place, as A77.2 and A101 were. That is fail-closed, but the way to clear it should be stated.
- **Better fix** (VERIFY §4):
  - merge B1 into R2B-13 as a NOTE;
  - in the r3 generator, put A98 in CITED, with its pin computed from bytes;
  - use a hand-written disposition table that the generator only verifies;
  - scope the INDEX T7 line to its V005 sha and time;
  - at the seal, re-run T7, read `verdict_currency` from the JSON, and disposition every later entry in the seal entry.
