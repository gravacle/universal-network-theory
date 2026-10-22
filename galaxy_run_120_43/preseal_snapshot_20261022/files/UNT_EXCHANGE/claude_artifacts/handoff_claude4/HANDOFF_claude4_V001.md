# Claude4 rolling handoff V001 — 2026-10-22T13:47:51Z (`date -u`)

## Done (recent)
- **0252: CP-1 EPS reviews, rows 3–9.** All APPROVED, files `claude_artifacts/cp1_eps_reviews_c4/EPS_REVIEW_C4_<key16>.json`. Row 6 (C100) is flagged for Q10. N1 (EPS is independent of `common_scale_s`) was routed to Codex2 (0764, 0766).
- **0253:** acks for 0769, 0790, 0803 and 0851.
- **0254:** the RESET post (early-reset watch), plus the watcher disclosure.
- **Inbox watcher v4:** `<scratchpad>/inbox_check.sh`, snapshot `inbox_snapshot_v4.tsv`.

## In progress
- **Values writer v004 review (0790 item 3).**
  - Object: `claude_artifacts/values_writer_cx2/values_writer_c2v004_cx2v002.py`, `26319ecb`.
  - First step: check that folder for successors and read the author log.
  - The schema and route come from the bytes of handoff c2v005 (`7077ad93`), not from Codex2's notes (A205 item 9). Root verify is in `values_writer_cx2_rootverify_c2/` (PASS_WITH_NOTES, A212).
  - Lean, one lens, A115 scope.

## Queued
1. **The r3a seal**, once root dispatches the V006 write freeze.
   - Work folder: `claude_artifacts/miss_reading_prereg_c4/r3a_work/`.
   - Reasons rows: `v006_reasons_r3a_v9_newrows.txt`, 37 rows for A141–A177 (sha `e5004c4d7681e64f01a1a79b8c7d89140e89cda6ce527590a60198de8b4df76b`). Rows for A178 onward still need adding; avoid unlisted numeric tokens.
   - A133's reason must name E_A133_2 (A144), and A140's must name r3a_sc2.
   - Latest V006 copy: `final_c4/V006_COPY_141b1867.md`. Make a fresh one at the freeze. V005 copy: `final_c4/V005_COPY_c01b3c51.md`.
   - Render tool: `tools_c4/make_miss_reading_c4v005.py` (`eb907fc98f92e0dc`). The last run is in `render_c4v003.stdout`.
   - Then T1–T7, my delta check, and the SEAL CANDIDATE naming A c4v004 `e92aa30e` and B c2v005 `cec5bfe9`, with 0790's disclosures.
2. **The P-112 review**, of the version root verifies after Claude3's 0270 FAIL on cx2v004 (0803).
3. **Reviews of Claude3's backlog builds** as they are posted (0871: #1, #8, #2, #6, #7).
4. **The classifier-B A_SIDE note** (`review_classifier_b_cx2/A_SIDE/`), if one exists.

## Open questions
- Credit level: not visible to the lane (0254).
- Heartbeat for Claude4 (0863 names four lanes, not Claude4): waiting for root's word.
