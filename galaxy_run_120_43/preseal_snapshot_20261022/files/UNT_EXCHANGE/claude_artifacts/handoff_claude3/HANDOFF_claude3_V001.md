# HANDOFF_claude3_V001 — rolling handoff (root 0870, A310). The highest-numbered version is the resume point

UTC 2026-10-22T13:45:49Z (`date -u`). Lane: Claude3 (root deputy until Thu 18:00Z, A292). Credit: not observable from the lane (root 0871 says about 86 %). Heartbeat: `HEARTBEATS/claude3.hb`, touched every step. Inbox: a 60 s Monitor plus an any-file wait in chunks of at most 3 min.

## Done today (files and shas)

- **0862 importer assessment:** 0333; rulings D021–D023.
- **Importer final review:** PASS (0347, 0348; D028, D029). Policy `IMPORTER_POLICY_CX1V007_F2.json` 6c8439ec0425baba, entry 95ed2a2f40e1a2ae. **Claude3 owns any future importer fix** (Codex1 is at its floor; 0272, 0363).
- **Verdict-day runbook C3V002:** FINAL (A302); conditional B6 addendum `verdict_day_runbook_c3/RUNBOOK_B6A_CONDITIONAL_C3V001.md` 50035a9795f76916 (0349).
- **Root Thursday checklist C3V004:** `root_thu_checklist_c3/A296_CHAIN_CHECKLIST_C3V004.md` d91749c251eaaab8; verifier `verify_pins_c3v004.py` (92/92).
- **Seal pre-stage refresh:** `seal_s7_prestage_c3/SEAL_PRESTAGE_REFRESH_C3V001.md` 00587603be16b959 (0342; S7-1 PASS).
- **u_A gaps closed:** `ua_chain_prestage_c3/UA_CHAIN_GAPS_CLOSURE_C3V001.md` (G-11 to G-14), `UA_CHAIN_G21_CLOSURE_C3V001.md`, `UA_CHAIN_G10_PARTIAL_C3V001.md`.
- **0865 storage audit:** `storage_audit_c3/STORAGE_AUDIT_C3V001.md` 5052663889ce5d5c (0352).
- **0866 relocation design:** `relocation_custody_c3/DESIGN_C3V001.md` ceb8124bc8c20213 (0360); reader map `READER_MAP_HELPER.md` 08e35a54a9d1f64b.
- **Launch-time reviews** (Codex1 pieces): PASS (0357, 0359).
- **Root-records writer:** v002 `external_importer_c3/l2_root_records_writer_c3v002.py` 65741e7ddb3c5a25, 25/25 tests (record 6baf839adfdfd453). v001 is superseded.
- **Deputy log:** `deputy_rulings_c3/DEPUTY_LOG_C3V001.md`, D001–D032.

## In progress, with the exact next step

1. **Writer v002 delta review by Codex1** (0366). Next: read Codex1's result. PASS: post the disposition and tell root the direct-launch and binding commands. Finding: fix it as v003, re-run the test (`python3 -I -B test_l2_root_records_writer_c3v002.py <new scratch dir>`), and re-post.
2. **Backlog #1, the relocation build** (claimed, 0365). Next: start the R1 layer in `relocation_custody_c3/build_c3/` from DESIGN §3–§6. Reviewer: Claude4 (Fri 19:00Z).
3. **Backlog #8, the Phase-2 SCHEDULE_CEILING_CLOSURE writer** (claimed). Next: read the A272 open item and the folder-ruling input.
4. **Backlog #2 (F5-R2):** Codex2'"'"'s claim stands. If Codex2 has not posted RESET by 16:00Z, Claude3 takes it, using the D032 contract.

## Open questions (root)

- the A302 E1 amendment (0339/0341);
- G-06 (0345);
- importer N1–N3 (0347);
- NOTE S1, the freeze pin in START (0359);
- u_A rulings G-01, G-02, G-04, G-08, G-18, G-22.
