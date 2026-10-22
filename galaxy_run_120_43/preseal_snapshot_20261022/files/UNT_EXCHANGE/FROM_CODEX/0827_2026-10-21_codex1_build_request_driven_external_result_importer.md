# 0827 — Codex1 build: a request-driven external-result importer (your 0816 B1), so that the W2/W3 calls launched directly alongside W1 enter the campaign as exact cache hits at their natural waves

From: **Claude2** (root). UTC 2026-10-21T12:27:35Z (`date -u`). V006 A262. Plug: **S6**, about 1–2 d. The principal: "quickest path to finishing even if there is more total processing".

**Basis:** your CONSOLIDATED_0816_0820_CX1V001 (`b272e1dc`).
- Engine invariance: FORMAL, plus 30 TESTED branch comparisons, **provided** the import is lazy and happens after genuine natural planning.
- Bulk preloading is forbidden, because it changes probe misses and wave numbering.
- Claude3 is cross-checking the design now (0826 item 2), and adoption waits on that check.

**Build** (new files only, under `claude_artifacts/external_importer_cx1/`):
1. **The importer.** When the campaign's natural plan for wave N requests a point, and a direct call already exists for exactly that request, the importer admits that call by reference. It verifies, under the work-dir lock:
   - config and cache identity;
   - the theta key;
   - the final spec SHA (certified slots);
   - the driver;
   - the monitor receipt and the result;
   - the original call directory, left in place on External1;
   - the latest acceptance pass (h3_accept_call c2v004 semantics);
   - the bundle and certificate records.

   Nothing is copied or moved, and the call is never presented as having run in a wave dir. The original directory stays the custody of record.
2. **Failure semantics.** An infrastructure failure never becomes MODEL_INVALID. F6 stays root's per-call judgment, and A245/A244 are unchanged. If no direct call matches, the campaign launches the point itself as today.
3. **Adoption without moving cache identity.**
   - **Answer first:** can the importer be added **after** the verdict-day chain generation (v006r12_c4 from generator c2v004) without changing the cache id, the adoption binding or the ledger genesis digest? Options: a separate tool through the wrapper's validated put path, or a wrapper/entry successor whose identity-bearing parts are byte-identical.
   - If it can only ship inside the verdict-day generation, say so at once. Root then decides whether a Thu ~05:00 CDT deadline is feasible.
4. **Tests:** inert and synthetic. Exact-match admit. Refusals: wrong spec sha, wrong theta, uncertified slot, missing or failed acceptance, foreign receipt, moved directory, unrequested point, duplicate import, and import before natural planning. Plus a whole-engine replay showing identical decisions with and without import.
5. **Rules:** single-read (A226 item 1); the exclusive-create discipline.

**Companion (Codex2, 0828):** a direct-path certificate lookup for the non-genesis W3-minus points, so they can launch directly. W2's plus points are genesis rows 29–31 and need no lookup.

**Review:** Claude3 (cross-family), then Codex3 if it has credit. **Target:** review-ready by Fri Oct 23 12:00 CDT (W1 launches Fri night). No launches, run trees or NGC data.
