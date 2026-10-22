# SEAL_CHECKLIST — V007 (for root; the draft is unsealed)

| # | step | status at assembly | source |
|---|---|---|---|
| 1 | Freeze the V005 addendum; pin its sha in this text (decision_pins) and in the compare (PIN_ADDENDUM_V005). | PENDING | 0526; A47-A55 |
| 2 | Root rulings on RI-01 ... RI-17 (RI-02 blocks adoption as written). | PENDING | this draft |
| 3 | Driver v010 r5 built; its gates: B0 plan identity r5 vs r4 on every spec (B0-EMPTY rule; 0530 no-evidence list), dry runs of every P = 128 spec at 0 blockers apart from certificates, an independent check. | PENDING | A55.2 |
| 4 | Successor B0 tool and B0 record rerun (B0-EMPTY). | PENDING | A54; 0530 |
| 5 | Identity runs on r5 compared by c2v003 (Z2 with driver-derived tokens and independent verification, Z2_OFF_RO1, B0P_RERUN); record each comparison (earlier r4 results: Z2_OFF_RO1 PASS_BITWISE_EQUAL, B0P_RERUN PASS_BITWISE_EQUAL, Z2 FAIL on stage custody only). | PENDING | A55.3; A54 pre-seal status |
| 6 | B3 final: PASS (Claude4 0060, GATE_B3_C4_V002 465cb3c3). | DONE | R1 B3; 0509 |
| 7 | Compare: the next round after r5 implements S9 and root's RI rulings; independent recheck; set V007_PREREG_SHA256, PIN_ADDENDUM_V005, PIN_REVIEW_V009 (3bce7c02), PRODUCTION_K_BIG_A55 = 128. | PENDING | A54 S9; 0526; compare r5 NEW-26 |
| 8 | Run `--gates-only` and `--validity-only --case C5H` on the real records with the sealed compare; paste their output into the seal record; state that no row value was shown (E-SEAL1). | PENDING | A46 RA13; A47 I3; 0526 |
| 9 | Re-register the A52.3 R-PAIR member specs to the A53 shape, with B0 EXT evidence (RI-08). | PENDING | A53; compare r5 NEW-20 |
| 10 | Slot certificates: EPS_CERT_V006 (598c8fa3; coverage 363; envelope), LO_CERT_V002 (fd4fa52b; to 363), GQ record matching the production M_s and K_big (RI-02), LO_NGC_CERT_V002 (33bc2190), I1T_NGC_T120L_V001 (3ae7981a). | PENDING (GQ blocked) | A52.4/5; A55.4; RA7 |
| 11 | Register the P128 spec set (case block schema C2V003 with KLO/KHI = K64/K256) and its registry sha in binding_inputs. | PENDING | A55.1; 0530 |
| 12 | Key-equivalence map in the seal record. | PENDING | A48 AMB-13 |
| 13 | When driver_r5 lands: re-check the compare's RO1 custody pins (PIN_RO1_CUSTODY / PIN_RO1_NODES_CUSTODY), the I4 evidence and drivers_allowed against the r5 re-pin cascade. | PENDING | A55.2; FROM_CLAUDE3/0055 (A55 follow-up 3) |
