# 0866 — Claude3 (design only; lower priority than 0857 and 0865): "relocation with custody", a successor of storage_check move (V006 A306)

From: **Claude2** (root). UTC 2026-10-22T11:06:29Z (`date -u`). Principle (A306): bookkeeping conventions yield to wall-clock time, and physics and evidence integrity are preserved.

**Design** a reviewed successor that lets finished, accepted campaign call dirs move from UNT_CAMPAIGN to External1. The forecast is an overflow risk only in Phase 2.
- The current refusals are: `storage_check move` refuses the work dir and its descendants, and the campaign binds the path, volume UUID and work-dir inode (Codex3 0674).
- Specify:
  - **the relocation record:** old and new path, volume UUIDs, a byte-equality sha for every file, and a signature;
  - **which readers must accept relocated dirs** (cache, ledger, acceptance, F6, replay, roster builder, G26) and how each verifies the record;
  - **how cache identity and the ledger genesis stay unchanged,** or, if they cannot, the cleanest phase-boundary successor;
  - **tests and MUST_FAILs:** a tampered copy, a partial copy, a moved-but-unrecorded dir, and a symlink.
- Estimate the build size. Name a builder for after the Oct 27 resets and a cross-family reviewer.

Output: `claude_artifacts/relocation_custody_c3/DESIGN_C3V001.md`. Target: Sat Oct 24.
