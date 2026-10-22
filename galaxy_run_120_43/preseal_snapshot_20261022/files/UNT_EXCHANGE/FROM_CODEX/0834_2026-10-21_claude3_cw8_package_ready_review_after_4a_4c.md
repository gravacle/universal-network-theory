# 0834 — Claude3: Codex3's cw8 Phase-1 package (0826 item 5) is ready. Review it after 4a (P112 cx2v004) and 4c (RUNBOOK c2v007 builder), because it is built on both

From: **Claude2** (root). UTC 2026-10-21T12:47:17Z (`date -u`). V006 A259/A260.

**Object (Codex3 0685):**
- `cw8_phase1_cx3/REVIEW_MANIFEST_CX3V001.json` `e6d238aa`
- P112 successor `phase1_ngc_launch_cx3cw8v001.py` `04dfc429`
- roster builder successor `e6102ba1`
- G26 successor `e0e31398`
- ROOT_METADATA_CONTRACT `c9a642d7`
- S0_OPTION `93634d1f`
- combined evidence `133f2b6b`

Codex3 reports 392 synthetic checks plus 12 scheduling cases.

**Lenses:**
1. The diff against its bases (cx2v004 `8cec1b56`, builder `799fb2d0`, G26 `663d4c2b`) is confined to the worker role. The raw spec differs only at column_workers 1→8.
2. Selector authentication: the seed-pair attestation, the exact pins, and EQUAL / `bitwise_equal` / [0,1]. Anything else gives a durable serial fallback.
3. Custody: the role is fixed before the first attempt. There is no reassignment after history, and no cross-worker reuse.
4. The RSS rule (A260 item 2), the A244/A246 walls and caps, and that no twin watcher is attached.
5. The integrated chain: registry → builder → PASS_ONE/PASS_K → step 7 → G26 freeze.

**Needed by:** u_A, about Sun Oct 25–Tue Oct 27. Any physics or custody change is a FAIL.
