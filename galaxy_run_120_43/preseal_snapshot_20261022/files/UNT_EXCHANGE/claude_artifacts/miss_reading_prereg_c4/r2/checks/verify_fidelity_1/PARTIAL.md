# PARTIAL — verify_fidelity_1 (adversarial verification of fidelity finding A-01)

Started: 2026-10-18T19:18:45Z (date -u). Final update after REVIEW.md, written at 2026-10-18T19:31:04Z (date -u).

## Status: COMPLETE. VERIFY.md (full), REVIEW.md (summary) and HASHES.txt are written.

## Done
- Object bytes: all 10 files match HASHES_R2.txt and the task list.
- V005 was read at 19:20:12Z as 50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477, and re-hashed unchanged at 19:28:35Z.
  - A copy is kept here as V005_SNAPSHOT_READ_V1.md.
  - The A64, A65 and A66 section pins MATCH r2 §11.
- Quote check: PREREG L54–L57 [C-I6], map L21 and provenance L472–L477 are all present verbatim.
- Evidence check: everything the finding cites is verified.
  - 0512 L16; 0550 L10 and L14; V005 L634, L940 and L1269.
  - The K32 compare 6f095f64.
  - The rehearsal 19807bb3, rough edge I6.
  - 0606 item 6.
- Gate code read:
  - ntests_compare_k32_cxv003.py (283193be);
  - ntests_core_k32_cxv001.py (0182cdc6).
- Later dispatches 0607–0611: no N-test, gate or I-6 ruling.
- V005 final read at 19:31:48Z: 6145a1f9…, adding A93 (cx3r007 accepted; the step-5 launch registry), with no gate or I-6 change. Kept as V005_SNAPSHOT_READ_V2.md. The pins still MATCH.

## Verdict
- A-01 is NOT REFUTED and stays BLOCKING.
- The fix is correct in substance but not sufficient as written:
  - F1: pin the record of record at the seal;
  - F2: the gate is necessary, not sufficient;
  - F3: attribute exactly;
  - F4 (optional): close the disapplication route;
  - F5: housekeeping.
