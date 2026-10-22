# SEAL_CHECKLIST — V007 (for root; the draft is unsealed)

| # | step | status at assembly | source |
|---|---|---|---|
| 1 | Freeze the V005 addendum; pin its sha in this text (decision_pins) and in the compare (PIN_ADDENDUM_V005). | PENDING | 0526; A47-A57 |
| 2 | Root rulings on the OPEN root items (RI-01, RI-03, RI-05, RI-06, RI-09, RI-10, RI-11, RI-12, RI-13, RI-17, RI-18). | PENDING | this draft |
| 3 | Driver v010 r5 built; its gates: B0 plan identity r5 vs r4 on every spec (B0-EMPTY rule; 0530 no-evidence list), dry runs of every P = 128 spec at 0 blockers apart from certificates, an independent check. | PENDING | A55.2 |
| 4 | Successor B0 tool and B0 record rerun (B0-EMPTY). | PENDING | A54; 0530 |
| 5 | Identity runs on r5 compared by c2v004 (Z2 with the driver-derived tokens and independent verification, Z2_OFF_RO1, B0P_RERUN); record each comparison (earlier r4 results under c2v003: Z2_OFF_RO1 PASS_BITWISE_EQUAL, B0P_RERUN PASS_BITWISE_EQUAL, Z2 FAIL on stage custody only). | PENDING | A55.3; A57.3; A54 pre-seal status |
| 6 | B3 final: PASS (Claude4 0060, GATE_B3_C4_V002 465cb3c3). | DONE | R1 B3; 0509 |
| 7 | Compare: the next round after r5 implements A54 S9 and A56 (N1 alternating bound and q_i >= 1 unavailable, N2 RB_FP Picard path, N4 KBIG text, labels, pins) and root's RI rulings; independent recheck; set V007_PREREG_SHA256, PIN_ADDENDUM_V005, PIN_REVIEW_V009 (3bce7c02), PRODUCTION_K_BIG_A55 = 128.0. | PENDING | A54 S9; A56; 0526 |
| 8 | Run `--gates-only` and `--validity-only --case C5H` on the real records with the sealed compare; paste their output into the seal record; state that no row value was shown (E-SEAL1). | PENDING | A46 RA13; A47 I3; 0526 |
| 9 | Slot the A53-shape PICARD member successor specs with their B0 EXT evidence (gates_v004). | PENDING | A53; A57.2 |
| 10 | Slot certificates: EPS_CERT_V006 (598c8fa3; coverage 363; envelope; gas-independent), certificates_v003 GQ at M_s 128 over the full DDO reach on all nodes and LO recomputed with the M_s 128 source (A57.1), LO_NGC_CERT_V002 (33bc2190), I1T_NGC_T120L_V001 (3ae7981a). | PENDING (certificates_v003) | A52.4/5; A55.4; RA7; A57.1 |
| 11 | Register the P128 spec set with gas M_s 128 (case block schema C2V003; producers emit C4T-KLO (K_big 64) and C4T-KHI (K_big 256)), dry-run it again, and put its registry sha in binding_inputs. | PENDING | A55.1; A56; A57.1; 0530; 0532 |
| 12 | Key-equivalence map in the seal record. | PENDING | A48 AMB-13 |
| 13 | When driver_r5 lands: move the compare's custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, drivers_allowed I4 set) to r5's re-pinned shas read from r5's BUILD record, verified from bytes. | PENDING | A55.2; A56 (A55 follow-up 3) |
