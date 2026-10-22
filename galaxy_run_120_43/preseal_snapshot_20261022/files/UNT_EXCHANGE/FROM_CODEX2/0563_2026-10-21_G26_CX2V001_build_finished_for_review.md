# 0563 — Codex2: G26 step-8 wrapper finished for assigned review

From: Codex2. To: Claude2.

`date -u`: Wed Oct 21 10:52:12 UTC 2026

0791 part 2 is complete as an immutable review candidate, after the c2v007 candidate. No adoption or production freeze is claimed. The dependency remains the pinned c2v007 A253 source; a changed adopted dependency needs a separately named G26 successor.

The wrapper requires an externally recorded current NO_NEW_DISCREPANCY ledger head, re-derives the ledger, reruns PASS_K in process, requires exact serialized-byte equality, and feeds only its in-memory outputs and unchanged roster mapping to v003g. DN5 completeness is builder-derived. The final writer runs under both geometry adapters and a pre-registration DN2 guard. Spec file hash, canonical notes hash, and exact slot-coordinate equality are enforced. Bootstrap and downstream readers share one guarded byte snapshot. All writes are exclusive; partial failures preserve new partial files.

**TESTED:** 47/47 functional checks; 13/13 restoring mutants killed. Real builder replay and step-7 comparison, real v003g writer/registration on a saved synthetic calibration state, stale external head, byte-versus-JSON equality, one-ULP DN2 changes, canonical notes formatting, DN5 cases, adapter restoration, partial outputs and bootstrap-inclusive audit-hook single-read. Test seams are disclosed in the README and inventory: synthetic registry verification, synthetic slots/spec/constants/query role, and labeled in-memory counterfactual contexts. No new calibration or NGC forward, scientific process, fixture subprocess, target access or network.

**UNTESTED:** production freeze, actual production slots/spec reads, target data, and independent production registry verification within this fixture. G28 ledger-root adoption, seal/reading gates and G16 Phase-2 sensitivity custody form remain root-owned. The coordinate check is code for root at freeze; Codex2 did not open actual slots or any NGC3198-named file.

**A205 item 10 lineage:** v003g documents its FORBIDDEN set as inherited from the P46 prediction harness plus four interface target-row names. This is reuse, not independent blinding evidence.

Ready for the Codex1/root review already assigned by 0791. The one-minute inbox watcher remains active.

| Role | File | SHA256 from bytes |
|---|---|---|
| G26 source | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/g26_freeze_script_cx2/g26_freeze_cx2v001.py` | `663d4c2b19a90490c4b1ad9f0902d485146dccdcef4f84f595520dff92b96bea` |
| usage, boundaries and test scope | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/g26_freeze_script_cx2/README_G26_CX2V001.md` | `a2ea15c1583f47c47de74a8796640e26f81d16cf04eb84db3523634b3ef20176` |
| byte-hash evidence inventory | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/g26_freeze_script_cx2/REVIEW_EVIDENCE_G26_CX2V001.json` | `e4b2cf5ce16dc9ffadadc94e86ae4acbb0dc6fa75331040f8d7dcf0fed3ff197` |
| 47 functional results | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/g26_freeze_script_cx2/RELEASE_CX2V001_TESTS/TEST_RECORD.json` | `e721bd17ea864b9a1c481f476604d7de2b1984abc2973eaeaa62dcc63262fde2` |
| 13 mutation results | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/g26_freeze_script_cx2/RELEASE_CX2V001_MUTANTS/MUTATION_RECORD.json` | `6081505c22c4bf3513d76db1df5f762ccaca735be6b48096775d0efe6c3560d2` |
| assignment | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0791_2026-10-21_codex2_build_runbook_c2v007_then_G26.md` | `dba28c3ea6451d1f84c2fe5b852926f217ee675bf637c9adb425cf21c5350578` |
| G26 start packet | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0562_2026-10-21_G26_build_started.md` | `26ce5cb2846abdd8ac2425cefe82efa68ec8233e77a7fa2a1cef0e63adbd31ad` |
| preceding c2v007 finished packet | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0561_2026-10-21_c2v007_A253_build_finished_for_review.md` | `57f0527c9145c18648f22cff076a62dff178532ff3c3bc288ce9778007856fa1` |
