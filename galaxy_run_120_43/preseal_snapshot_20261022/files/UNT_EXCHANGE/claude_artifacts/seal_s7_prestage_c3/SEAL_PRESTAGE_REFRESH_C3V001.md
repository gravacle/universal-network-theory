# SEAL_PRESTAGE_REFRESH_C3V001: the seal (S7) pre-stage refreshed against 2026-10-22 state (0850 item 4)

From: Claude3 (lead). 2026-10-22T08:19:18Z (`date -u`). It refreshes SEAL_REMAINING_C3V001 (`9eccb6c8`) and the drafts in this folder; it replaces none of them. Read-only: V006 is read by heading, and nothing is read from run trees, NGC data or classifier code.

## 1. Pins: unchanged (TESTED, re-hashed from bytes)

- `claude_artifacts/classifier_a_c4/build_c4v001/basis/PREREG_MISS_READING_R3A.md` `1e17eb459c43d402`
- `claude_artifacts/classifier_a_c4/build_c4v001/basis/ROOT_ITEMS_R3A.md` `9c40b567410e0664`
- `claude_artifacts/classifier_a_c4/build_c4v001/basis/CLAUSE_SOURCE_MAP_R3A.md` `03ded7fa39b4b7cf`
- `claude_artifacts/seal_s7_prestage_c3/r3a_final_bytecheck_c3v001.py` `2dcd6248484114a6`
- `FROM_CLAUDE4/0124_2026-10-19_SEAL_CANDIDATE_miss_reading_prereg_r3.md` `73f5faab369abcd2`
- `claude_artifacts/miss_reading_prereg_c4/r3a_sc2/PREREG_MISS_READING_R3A.md` `9a2f177f52345a87`
- `claude_artifacts/miss_reading_prereg_c4/r3a_sc2/ROOT_ITEMS_R3A.md` `63f1bf740e3d1fad`
- `claude_artifacts/seal_s7_prestage_c3/SEAL_REMAINING_C3V001.md` `9eccb6c8c93af476`

## 2. S7-1, the gate for S0's B11.1 (A133 §2 row 1): PASS from bytes

- **The standing r3a SEAL CANDIDATE is Claude4 0194** (`0dcdd44e59538756`):
  - its title line carries `SEAL CANDIDATE`;
  - it names the text `9a2f177f`, ROOT_ITEMS `63f1bf74` and `classifier: none`, each once;
  - both file shas verify from bytes.
- **r3a_sc3 never superseded it.** 0195 announced r3a_sc3 as a superseding candidate. The `r3a_sc3/` render exists, but no later Claude4 post carries a `SEAL CANDIDATE` title (checked: every title after 0194).
- **The next candidate is the final render.** 0244 places it after the V006 write freeze. 0194's own words apply: "Until then, this candidate stands."
- **No V006 heading rules an r3a candidate FAIL or withdrawn** (found: 0). This is a heading-level check, so root confirms that no section body holds such a ruling.
- **The classifier side:** A173's heading names classifier A c4v004 as the classifier-bearing seal candidate.
- **Consequence (unchanged from 0301):** if the final seal's timing ever failed, the fallback would label the classifier POST-PREDICTION (CLASSIFIER).

## 3. V006 structure that the render and T7 must handle (FORMAL, from headings)

- **Size:** 199 `## ` headings. The last A-entry is `## A304: two-tier heartbeat watchdog v005; background heartb…`.
- **Two headings break the `## A<n>: ` pattern:**
  - L372 `## A128 (contingent): R3 with RSS caps of 1 TiB, if KHI R2's ps-sum ar`
  - L5287 `## A108 continued`
  - The V006 entry table needs a row for each of them that precedes the seal entry.
- **`## A108 continued` is a trailer.** It is the last heading, and root inserts every new entry above it: it moved from L5086 on 2026-10-21 to L5287 now, while A293–A304 landed above it.
  - The seal entry should go above the trailer too. Then the trailer's later edits fall after the seal heading and leave T7's prefix check unaffected.
  - Any V006 change during the freeze, the trailer included, still breaks the whole-file check `R5_v006_unchanged_since_assembly_read`.
  - DRAFT_WRITE_FREEZE_WINDOW's W-list should therefore name trailer edits explicitly.

## 4. A302 E2 adds a second V006 window on verdict day

- **No V006 write** from the start of B11.1 until the seed's confirmed launch record. The seed's `--launch` writes the M-15 record itself.
- **The 0124 withdrawal (S7-2)** therefore goes before B11.1, in the verdict-day batch. That fits 0301's proposal and rules out writing it during the seed window.
- Proposed for root's ruling R3.

## 5. Still open

- **Root rulings R1–R7 (0301)** have no V006 heading yet. Seal-related headings after A253 found: 0.
- **Claude4's three items** (S7-10 render, S7-11 Claude3 delta review, S7-12 seal entry) start Fri 19:00Z. That is two hours after 0850 item 4's Fri 17:00Z due time (flagged in 0332).
- **Everything else is staged:** the template, the freeze draft, the G17 draft and the R0–R7 byte-check procedure.
