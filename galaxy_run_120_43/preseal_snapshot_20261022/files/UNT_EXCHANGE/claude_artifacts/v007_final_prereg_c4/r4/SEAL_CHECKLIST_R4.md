# SEAL_CHECKLIST r4: V007, in the order root will execute it

State at assembly (2026-10-18T17:56:01Z). The draft is unsealed; the slots stay PENDING.

| step | state | source |
|---|---|---|
| **A. Before seal assembly (any order; each must be complete before step B1)** | | |
| A1. Final compare round (r11, or r12): three recheck lenses and the distinct reviews of record (Claude3, Codex2) report 0 blocking; its IMPL lists every NEW item with disposition and MUST_FAIL tests. Fix its reviewed source (seal-time pins unset, `None`) for the compare slot. | PENDING (r11 building) | A80; A81 RI-20 |
| A2. Identity comparator: the c2v007-lineage round whose own check and Codex2's review report 0 blocking. | PENDING | A81 RI-21 |
| A3. A72 decision: r5, or r6 if (a) independent check incl. stale-cache attacks, (b) bitwise equality at K_big 32/128/256 and (c) a measured net saving all hold. r6: BUILD, cascade map and template published. | PENDING | A72 |
| A4. r5 only: CASCADE_MAP_R5_ADDENDUM written (immutable inventory addendum). | PENDING | A69 |
| A5. Identity runs of the chosen driver (Z2, Z2_OFF_RO1, B0prime_RERUN; reruns on r6 with the cache if r6) compared by the A2 round, with A59 replace-mode tokens from that driver and the raw successor-custody check: records of record. | PENDING | A81 RI-21; A59; A67 N1 |
| A6. Successor B0 tool and B0 record rerun (B0-EMPTY rule) on the chosen driver. | PENDING (no A-entry records completion) | A54; 0530 |
| A7. Certificates of record confirmed: EPS_CERT_V006 598c8fa3, LO_CERT_V004_MS128 1c384f76, GQ_CERT_V005_MS128 fbceefe6 (V004 FAIL control); I1T_NGC; the V007 LO_NGC slot takes the LO_NGC record of record existing now (reported only). | DDO DONE; root confirms | A70; A81 RI-23 |
| A8. The merged DOUBLING record (DDO half PASS; NGC half from NQ at K_big 32, <= theta/20), registered. | PENDING | A81 RI-22; A73 |
| A9. Producer registry: producer paths, producer shas, gate-record shas of record (SR_K included). | PENDING | A62.2; A67 N2; A69.1 |
| A10. Key-equivalence map assembled for the seal record. | PENDING | A48 AMB-13 |
| **B. Seal assembly (strict order; every file exclusively created; none edited afterwards)** | | |
| B1. Freeze the V005 addendum: exclusive-create ..._V005_ADDENDUM_FROZEN.md after the last pre-seal entry; verify every A-entry this text cites (A47-A81) is present; any later entry touching this text gets a revision or a no-change note; it cites no sealed-prereg sha. | PENDING | A81 RI-26; 0576; RI-27 |
| B2. Fix the driver path and sha (A3). r6 only: create a fresh, empty cache directory (no pre-warming). | PENDING | A72; A81 RI-24 |
| B3. Run the build-only binder (template for the chosen driver; driver path and sha; frozen addendum path and sha): bound plan and command, exclusive create, under the build folder. | PENDING | 0576; A81 RI-25 |
| B4. Write the sealed prereg: this text with every seal slot filled from bytes (frozen addendum, driver, compare reviewed source, identity comparator and records, launch packet with bound plan and command, certificates, producer registry; r6 cache directory). | PENDING | 0580; A81 |
| B5. Create the sealed compare: the A1 reviewed source with exactly the seal-time pins set (V007_PREREG_SHA256 = B4's sha, PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK, PIN_PRODUCER_REGISTRY); verify it differs from the reviewed source only in those lines. | PENDING | RI-27 (draft); A67 |
| B6. Run `--gates-only` and `--validity-only --case C5H` with the sealed compare on the real records; keep their output for the SEAL_RECORD; no row value shown. | PENDING | A46 RA13; A47 I3 |
| B7. Exclusive-create the SEAL_RECORD: sealed prereg sha (first pin), sealed compare, driver, frozen addendum, bound plan and command shas, r6 cache directory; B6 output; E5-08; raw successor custody; the NEW-item disposition list; key-equivalence map; no-row-shown statement. | PENDING | A81 RI-19/25; A62; A59; A58 RI-10 |
| B8. Exclusive-create the ROOT_SEAL_ADMISSION config pinning the SEAL_RECORD's full sha, prereg, compare and BUILD_V005; its producer_allowlist names exactly the 13 BUILD_V005 sources (launcher v007 and guard v008 by exact path). | PENDING | 0561; A78 N2; FORMAT_V004 |
| B9. Exclusive-create the SEAL_ADMISSION_RECEIPT naming the config and seal shas; post it in a numbered root packet. | PENDING | 0561; A81 RI-19 |
| **C. Launch (Claude2 only)** | | |
| C1. Verify the receipt and config against the numbered root packet; export UNT_ROOT_ADMISSION_SHA256 from the published value (never from the local file). | PENDING | RUNBOOK_V005 step 3 |
| C2. Verify the bound plan and command shas from bytes immediately before running the command; run it (ramp-gated; KHI first). | PENDING | A81 RI-25; A72; 0559 |
| **Already DONE (preconditions)** | | |
| Driver r5 built (b5cc62af), dry runs 25/25, Codex3 review PASS_WITH_FINDINGS; a Claude-lineage check (driver_r5/check, 89a6de88) PASS_WITH_FINDINGS. | DONE | A67; A69 |
| B3 gate final PASS (GATE_B3_C4_V002 465cb3c3); PICARD member specs gates_v004 PASS; P128/M_s 128 spec set registered (c7023846); launch packet BUILD_V005 (46bc5b5d) reviewed PASS. | DONE | R1 B3; A68; A72; A78; Claude4 0079 |
| **SUPERSEDED** | | |
| Compare r8 and r10; comparators c2v004-c2v006; r2/r3 checklist orderings. | SUPERSEDED | A79; A80; A76; this revision |
