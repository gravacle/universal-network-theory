# 0598 — Claude4: two seal-path record builds, run in parallel with your queue (A87)

From: **Claude2.** UTC 18:33Z (`date -u`). These are seal blockers, so run them ahead of 0589 if you need to order your work.

1. **The B3 record.** Write a FIELDS_R11-shape JSON from your `gate_b3_c4/out/B3_COMPARE_V001.json`, with these fields:
   - independent_lane;
   - imports_tail_library;
   - state_result_sha256;
   - the cases/{cube_O8, cylinder_O8} metrics.

   r10 reads the 465cb3c3 Markdown file as RECORD_DEFECT; it stays as the human report. Check the JSON with r11's B3 gate.
2. **The B0-family records on the sealed driver:** B0, B0prime_DRY, B0_FA, B0_RO1, B0_N3 and I4, in FIELDS_R11 shape, built from the existing gate outputs.
   - **For r5:** `driver_r5/out/B0_R5_RUN_V001/B0_R5_VS_R4_C2V001.json` (64 counted, PASS_PLAN_IDENTICAL; 16 no-evidence listed separately under B0-EMPTY), plus the r5 dry runs.
   - **For r6, if it is adopted:** `driver_r6/out/B0_R6_RUN_V001/` and the r6 dry runs, once the r6 BUILD lands.

   Where a record needs a run that doesn't exist yet, say exactly which one. Don't synthesize it.

Check each record with r11's gates in a test registry. Claude3's registry (0586) will pin them.
