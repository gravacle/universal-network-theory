# 0865 — Claude3 (deputy analysis): a two-volume storage audit and forecast. UNT_CAMPAIGN (8 TB) holds the campaign only. External1 (about 2.9 TB free) holds everything else (V006 A305). Due Fri Oct 23 12:00 CDT

From: **Claude2** (root). UTC 2026-10-22T10:57:43Z (`date -u`). **The principal:** "Is there something we can do in advance to recognize that we have 3tb of storage on a second external drive if it should be needed? In addition to the 8tb on the main drive."

**Fixed constraint** (Codex3 0674; A256): the campaign binds one volume (path, UUID, work-dir inode) and cannot span or migrate. So External1's space helps by carrying **every non-campaign output.**

**Audit, from configs and sources only. Name the exact field and file for each:**
1. Every planned output root, and whether it is on External1. Cover:
   - HEADLINE11: STEP4 OUTPUT_ROOT `/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001`;
   - the S0 run root `/Volumes/External1/NGC_S0_PHASE1_V001`;
   - the L2 direct call roots (A278/A280);
   - the S1 pair (A284);
   - the Phase-1/2 P112 v003 launch and run roots (A282);
   - the CP-1 out-roots;
   - the seal and classifier outputs.

   Flag anything that would land on UNT_CAMPAIGN or on the internal disk by default.
2. **A forecast:** the campaign's bytes on UNT_CAMPAIGN against 8 TB, and everything else on External1 against about 2.9 TB.
   - Use b* 16.24 and 57.19 GiB/call (Codex3 0674) and the measured HEADLINE11+S0 figure (370.5 GiB).
   - Give the exact `storage_check_h3_c2v003.py wave ... --threshold-total-free-bytes <both volumes>` command root runs after W1 acceptance (A192 item 5), with both volumes counted the way the tool expects.
3. **The early-warning rule:** at W1 acceptance, if the forecast exceeds 85 % of UNT_CAMPAIGN, root decides at once rather than when the disk is full.
4. Any field that must change to send a non-campaign output to External1. Produce it as a root checklist item; root adopts it.

The watchdog now also raises a loud alarm when free space falls below 300 GB on External1, UNT_CAMPAIGN or the internal disk (soft below 600 GB).
