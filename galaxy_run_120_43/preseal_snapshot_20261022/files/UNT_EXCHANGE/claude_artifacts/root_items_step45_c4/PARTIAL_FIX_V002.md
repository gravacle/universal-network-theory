# PARTIAL_FIX_V002 — root_items_step45_c4, FIX stage (Claude4 helper, dispatch 0637)

Append-only progress log of the FIX stage. Created 2026-10-19T02:23:12Z (date -u) by exclusive create. The build-stage PARTIAL.md is left unchanged (its sha is in HASHES_ROOT_ITEMS_STEP45_V001.txt).

## 2026-10-19T02:23:12Z — start; findings checked against source bytes
- Authority: dispatch 0637 e6163c64eaf2193e7730a1819ae0e1cea87420c8a4fa9ddb2678583e460ade01 (TESTED, re-hashed). Object: V001 MD 33d09696, JSON 8a20c334 (TESTED, unchanged). Refuter report REFUTE_ROOT_ITEMS_STEP45.md 0a75e6d8 read in full (8 SHOULD_FIX, 13 NOTE).
- SF-1..SF-8 each confirmed from the named source bytes (details in FIXLOG_V002.md when written).
- New since the refuter (TESTED by listing and hashing): Claude4 0124 SEAL CANDIDATE (02:16:45Z, 73f5faab), Claude4 0125 (02:19:34Z, a58d1804), Codex1 0119 r3 delta PASS 0 blocking (02:18:51Z, ae2374c4), Codex1 0120 (02:20:47Z, 27d2bd75: CX1-MR3-P1 OPEN, P2 CLOSED). Step-4 V003 still in build (no ROOT_ITEMS_FINAL_C4V005). V006 still 43d4562b at 02:09:39Z.
- Plan: copy the V001 builder to the scratchpad as the V002 builder, patch it for SF-1..SF-8, the state that landed since, and the confirmed NOTEs; dry run; self-check; publish by exclusive create.

## 2026-10-19T02:45:49Z — builder patched; dry run 1; V006 moved
- V002 builder (scratchpad tools_v002/build_root_items_step45_v002.py, copied from the V001 builder 5ee49788 by exclusive create, then edited) patched for SF-1..SF-8, the step-6 state (0124, 0125, Codex1 0119/0120), and the confirmed NOTEs. Dry run 1 (02:43:55Z): exit 0, 55 items, 68 summary rows; RI45 ids unchanged; new S4-R-B4a and S4-R-B7.
- Dry run 1 flagged V006 as changed: live V006 is b22bd18ae4c3142be54db0e965b2a2fff4264e787fa29963bd637b6ae2ddc6a4 (mtime 02:42:32Z), 7769 B. TESTED (diff of byte copies): 43d4562b plus one inserted section, A112 (seal tool 4 v004 SELECTED; disclosures file V002; R-02), placed before the A108 continued heading. Copied by exclusive create to V006_ADDENDUM_COPY_AT_FIX.md (b22bd18a, equal before and after the copy). A112 decides no step-4/5/6 item (FORMAL); r3 (rendered at 43d4562b) needs an A112 row in its re-render (FB-3). Builder pins updated.
- Disclosure: one shell command failed before printing (sed range from a grep that matched two lines); no file affected.

## 2026-10-19T02:57:10Z: FIX STAGE DONE (published)
- Dry runs 3-4 (02:47:12Z, 02:53:43Z) clean; the V005 candidate (v003_work/order, 753e7e25, build complete 02:39:38Z, unpublished), dispatch 0648 (seal path, no step-4 builder) and Claude4 0126 (seal path) were folded in or checked before the final build.
- Final build 2026-10-19T02:55:14Z, self-check 175/175 (TESTED), then published by exclusive create in one chain (bytes equal the staged bytes):
  - ROOT_ITEMS_STEP45_V002.md 417de6fef408082695e4e3f68530351a0b71a7c1415d784a29199a8a9ec42ee8
  - ROOT_ITEMS_STEP45_V002.json f6eb430eaf13b1fa8543ff8b14d74e61c3f57da649615a8dd0ddd0315919c910
  - BUILDER_ROOT_ITEMS_STEP45_C4V002.py c74d41f9fa1db5587496f96161d10e74c1e38bbb1f9ac5b999c23d32bdbe4bf3
  - CHECK_ROOT_ITEMS_STEP45_V002.py 8980c60bde8d1db605f19e8f34345afcea994de8d9ff0c0f0ca38c72604f3611
  - FIXLOG_V002.md 01ad5f4f21344002547679e40bbb42405619a7b0dbe305592fedd7552060a6fd
- SF-1..SF-8 all CONFIRMED and fixed; NOTEs N-1..N-13 confirmed and applied. 55 items; 68 summary rows (25 BLOCKS_START, 43 BEFORE_FIRST_RESULT); 12 step-4 start items.
- V006 at this entry: b22bd18ae4c3142be54db0e965b2a2fff4264e787fa29963bd637b6ae2ddc6a4 (equal to V006_ADDENDUM_COPY_AT_FIX.md). HASHES_ROOT_ITEMS_STEP45_V002.txt is written last.
- No launch, no target or protected access, no recursive search, no delete, move or overwrite.
