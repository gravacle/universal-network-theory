# SEAL_CHECKLIST r3: V007 (for root; the draft is unsealed)

State at assembly (2026-10-18T17:47:27Z). DONE, PENDING or SUPERSEDED, each with its source.

| # | step | state | source |
|---|---|---|---|
| 1 | Freeze the V005 addendum (exclusive-create ..._V005_ADDENDUM_FROZEN.md) at seal assembly and pin it here and in the compare (PIN_ADDENDUM_V005). | PENDING | 0576; A67 |
| 2 | Root rulings on the OPEN root items (RI-19, RI-20, RI-21, RI-22, RI-23, RI-24, RI-25, RI-26). | PENDING | ROOT_ITEMS_R3 |
| 3 | A72 branch: decide r5 or r6 on conditions (a)-(c); if r6: r6 BUILD and cascade map published, r6 template and bound plan, identity reruns on r6 with the cache. | PENDING | A72 |
| 4 | Driver r5 built (b5cc62af); dry runs 25/25 with 0 blockers; Codex3 cross-lineage review PASS_WITH_FINDINGS (A69). A Claude-lineage independent check, driver_r5/check/CHECK.md (89a6de88), reads PASS_WITH_FINDINGS (on disk at assembly, not yet logged in an A-entry). | DONE | A67; A69; driver_r5/check |
| 5 | CASCADE_MAP_R5_ADDENDUM (immutable inventory addendum) written, if the driver slot is r5. | PENDING | A69 |
| 6 | Identity runs on the driver slot compared by the c2v007-lineage comparator (Z2 with A59 replace-mode tokens, Z2_OFF_RO1, B0P_RERUN); records of record emitted. | PENDING | A67; A74; A76 |
| 7 | B3 final: PASS (Claude4 0060, GATE_B3_C4_V002 465cb3c3). | DONE | R1 B3; 0509 |
| 8 | Final compare round r11 (or r12): A79.1-6, A75 in full, A77.2, A73 F2, the r10 recheck items, A71, A68 CHK-1, A69, RI-10 dispositions; three recheck lenses; distinct reviews of record by Claude3 and Codex2. | PENDING (r11 building) | A79; A80; 0582; A75 |
| 9 | Compare r8 and r10: superseded for the seal (r10 frozen e801adc4; both r10 rechecks FAIL: order 4 blocking, validity 2 blocking). | SUPERSEDED | A79; A80 |
| 10 | Run `--gates-only` and `--validity-only --case C5H` on the real records with the sealed compare; paste their output; state that no row value was shown. | PENDING | A46 RA13; A47 I3 |
| 11 | PICARD member successor specs (A53 shape) with B0 EXT evidence: gates_v004 PASS (18/18 leaves; 10/10 negative controls). | DONE | A68 |
| 12 | Certificates DDO: EPS_CERT_V006 598c8fa3 (retained), LO_CERT_V004_MS128 1c384f76 (PASS_WITH_FINDINGS), GQ_CERT_V005_MS128 fbceefe6 (PASS; V004 FAIL control). | DONE (root confirms slots) | A67 SF2; A68; A70; A73 |
| 13 | Certificates NGC at K_big 32: EPS_NGC91 (admission test passed), LO_NGC to 91 (absent; sole N-test blocker), GQ_NGC to 91 (with Codex1). | PENDING | A64.2; A70; Codex1 0049 |
| 14 | DOUBLING merged record (DDO half PASS at 128/256, max 4.7e-13 tau; NGC half from NQ at 32). | PENDING (format) | A58 RI-03; A73 |
| 15 | P128/M_s 128 spec set registered (SPEC_REGISTRY_R5_MS128_CX1V004 c7023846), dry-run 10/10, case block accepted. | DONE | A72 (packet final); A78 |
| 16 | Launch packet BUILD_V005 (46bc5b5d): ramp gate, admission, outputs and aggregate fixes reviewed PASS (Claude4 0079). | DONE | A78; Claude4 0079 |
| 17 | Bound plan and command written by the binder from the selected template, the driver slot and the frozen addendum (exclusive create). | PENDING | 0576; A78 |
| 18 | Root admission config names the BUILD_V005 launcher and guard sources exactly. | PENDING | A78 N2 |
| 19 | Publication order: freeze, bind, SEAL_RECORD, config, receipt; numbered root packet; UNT_ROOT_ADMISSION_SHA256 exported from the published value. | PENDING | 0561; 0576; RUNBOOK_V005 |
| 20 | Producer registry with producer paths, producer shas and gate-record shas of record (PIN_PRODUCER_REGISTRY). | PENDING | A62.2; A67 N2; A69.1 |
| 21 | Key-equivalence map in the seal record. | PENDING | A48 AMB-13 |
| 22 | Seal-record disclosures and quotes: E5-08, raw successor custody, the NEW-item disposition list. | PENDING | A62; A59; A58 RI-10 |
| 23 | Successor B0 tool and B0 record rerun (B0-EMPTY rule) on the driver slot. | PENDING (no A-entry records completion) | A54; 0530 |
| 24 | r2 checklist item "identity runs compared by c2v004": superseded by the c2v007 lineage. | SUPERSEDED | A68; A70; A76 |
