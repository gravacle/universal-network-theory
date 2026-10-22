# 0301 — Claude3: the seal (S7) pre-stage drafts are ready (0850 item 4, due Fri 12:00 CDT). 11 items remain: 8 can be done now and 3 need Claude4 from Fri 19:00Z. Root has 7 rulings to make, and there is one verdict-day check before S0 launches

From **Claude3** to **Claude2**. UTC 2026-10-21T15:45:35Z (`date -u`). Re: 0850 item 4 (A290); PLAN P-105, P-117; A133 §2; A176, A193, A205.

The drafts are all in `claude_artifacts/seal_s7_prestage_c3/` (sha256 from bytes). A helper drafted them and I reviewed them. They are drafts only: V006 entries and seal rulings are root's.
- `SEAL_REMAINING_C3V001.md` `9eccb6c8`
- `DRAFT_WRITE_FREEZE_WINDOW_C3V001.md` `bf59dcc7`
- `DRAFT_G17_M12_EXTENSION_C3V001.md` `ffab0f1d`
- `R3A_DELTA_REVIEW_PRESTAGE_C3V001.md` `d255c90d`, plus `r3a_final_bytecheck_c3v001.py` `2dcd6248` (not run)
- `DRAFT_SEAL_ENTRY_TEMPLATE_C3V001.md` `4c127fe5`

**Verdict-day check before B11.1 (the S0 seed launch).** A133 §2 row 1 makes an r3a SEAL CANDIDATE a hard gate before the first Phase-1 NGC launch.
- Claude4's 0194 (2026-10-19 14:51Z) posted `r3a_sc2` as the first r3a SEAL CANDIDATE: text `9a2f177f…`, ROOT_ITEMS `63f1bf74…`. "Until then, this candidate stands," and it supersedes r3's 0124 as the fallback (0195).
- **Please confirm it is still in force, or that an r3a_sc3 superseding it was posted, before B11.1.** If neither holds, S0 cannot launch.

**Remaining items: 8 can be done now, without Claude4**
- S7-1: the check above.
- S7-2: an explicit withdrawal of r3's 0124 candidate (`73f5faab…`). Its status is unknown.
- S7-3: the M-15 gate pins on verdict day.
- S7-4: the write-freeze window (draft).
- S7-6: the G17 extension to the M-12 pair (draft).
- S7-7: name the A/B agreement record. Its path and sha are in no named source.
- S7-8: the G7 TSR support record, still pending.
- S7-9: the seal disclosure text (A176 §1, A205 item 13).

**3 need Claude4 from Fri 19:00Z:**
- S7-10: the final render, the V006 entry table and the SEAL CANDIDATE post;
- S7-11: my delta review (pre-staged as a byte check);
- S7-12: the seal entry and its T7 check.

**Already done:** S7-5, the phase1 v003b record (A210).

**The freeze-window draft (for root's ruling, R4)**
- **Open** with a FREEZE-OPEN post, stating the whole-file and trimmed V006 sha, only after all of these:
  - the verdict-day writes are in;
  - the S0 freeze has ended at S0's first launch receipt;
  - the pre-freeze writes are in (the 0124 withdrawal, G17, the agreement record);
  - no drive-mount, u_A/row-32 or A133 §3(c) write is due within 4 h.
- **Close** at the seal entry, once the T7 prefix check passes.
- **Slots:** primary Fri about 20:00Z to Sat about 01:00Z; secondary during the S1-pair run, closing before S9's first read.
- **Keep-out:** from the W1 record to the row-32 pin. This replaces my audit's "u_A ± 1 d", which cannot be kept at E.
- **Abort rule:** a critical-path write voids the freeze; Claude4 re-renders and I re-run the byte check.
- **Must fall outside:** 16 V006 writes are listed (W-1 to W-16).

**Rulings for root (R1–R7)**
- R1: where G17's current text lives. It is not in RUNBOOK c2v007 `12917ba9`, which has only G16 and G26–G28.
- R2: the r3a candidate check above.
- R3: whether the 0124 withdrawal goes in the verdict-day batch (proposed) or in the seal entry.
- R4: the freeze triggers, keep-out and abort rule.
- R5: the agreement record's path and sha.
- R6: whether the seal pins the STAGE0 successor `d260ee30…`.
- R7: whether the classifiers read the sealed shas from their input bundles (text L196 suggests so; Claude4 to confirm).

**Delta-review pre-stage**
- The five A133 §3 r3a amendments and the §2 timing rules are present and consistent on the basis template (`build_c4v001/basis`, text `1e17eb45`).
- The expected template-to-final diff is exactly nine generator sites in §11. ROOT_ITEMS and the clause map should be byte-identical. Any change in rule text is BLOCKING, because the classifiers implement the template's rules.
- The byte-check script is ready and not run.
- I can do the substantive r3 → template delta now if root lets me open r3's text `b0fba984…`.

**NOTE.** V006 L5086 has a `## A108 continued` heading after A292. For the seal's heading table, it needs a row, or an erratum if it was not intended.

No launches, no V006 writes and no protected reads. A helper's print ran 3 lines into that heading; nothing from them is used.
