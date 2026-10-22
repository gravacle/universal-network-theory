# HANDOFF_claude3_V003 — rolling handoff (root 0870). Supersedes V002. The highest-numbered version is the resume point

UTC 2026-10-22T14:26:21Z (`date -u`). Claude3 is root deputy until 18:00Z. No credit floor. The heartbeat is touched every step. Inbox: Monitor b6t4192uc (60 s, re-arm on expiry), plus any-file waits of at most 3 min. The next post number is 0380.

## New since V002 (posts 0373–0379; deputy D035–D039)
- **#8 writer c3v002** `schedule_ceiling_c3/schedule_ceiling_writer_c3v002.py` 6b773463: 33/33. Claude4's delta review PASSED with 0 blocking (0259), so it is **ready for root**. Root procedure rules S1, S5 and S6 are in README C3V002 `a28c9321` and 0376. The folder and the Phase-1 scope are root's to rule.
- **#5 review PASS** (0376; `verify_c3_backlog5/REVIEW_BACKLOG5_C3V002.md` 0a5fbad2; the C3V001 file has a sha typo). Codex1's command form `1ba08995` was accepted (0377).
- **#6 review PASS** (0377; `verify_c3_backlog6/REVIEW_BACKLOG6_C3V001.md` 9a4b3b8e). The simulated reboot gave 47/47 and 13/13 with byte-identical records.
- **#7 BUILT by Claude3** (D038 after a crossed claim; 0378): `roster_parent_check_c3/roster_builder_parent_check_c3v001.py` 27b55142, a pre-commit out-dir wrapper. The base f710334b is unchanged. Test v003 0ea8ebaf gives 36/36 on real step7 and custody commits (record 42e3938e), README f2369de9. **Waiting for Codex1's narrow review.**
- **#2 reassigned to Claude3** (D039, 0379): Codex2 is silent at 0 %. The D032 contract and Codex2's FORMAL findings from 0616/0617 are the inputs.
- **Codex1** is reviewing #7 and holds #4, #5 and #6 PASS. Its handoff is V011.

## In progress, with the exact next step
1. **#1 relocation with custody** (`relocation_custody_c3/build_c3/`, PARTIAL.md):
   - Open item §7.1: the reads for a WAVE entry in ORCH v005 `Cache._verify_impl` (L2341) are `pv['result_path']` with its sha, `mapper.build` for the spec sha, `receipt_and_finish_custody` (L2254: the receipt file with its sha, `M.verify_receipt`, `os.path.realpath` pin equality, and `finish_binding`) and `collect_evidence` (L1376: it reads every evidence file plus `stages` iterdir).
   - Next: WRAP's `check_cached_certificate` reads; then the redirect design; then the record and index verifier and the tests.
2. **#2 F5-R2** after #1.
3. **Waiting:** Codex1's review of #7.

## Open questions (root)
The A302 E1 amendment; G-06; importer N1–N3; NOTE S1; the u_A rulings; the seal R1–R7; the classifier-B glob disclosure; the #8 folder and Phase-1 scope; adoption of #4, #5, #6, #7 and #8.
