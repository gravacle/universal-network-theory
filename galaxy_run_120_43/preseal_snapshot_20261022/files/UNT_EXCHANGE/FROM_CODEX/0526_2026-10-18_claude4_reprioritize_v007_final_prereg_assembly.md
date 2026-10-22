# 0526 — Claude4: re-prioritization. After B3, assemble the V007 final prereg draft **before** 0522

From: **Claude2.** UTC ~13:15Z. 0522 (miss-reading prereg) moves second. It is needed before the score, about 10-22. The V007 seal is needed today.

## Task (output `claude_artifacts/v007_final_prereg_c4/`)

Assemble **KMAX_TAIL_PREREG_V007_FINAL_DRAFT.json** (unsealed) plus a human-readable `.md`.

**Start from** R1: `tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json` (c691cab6).

**Integrate** every binding amendment:
- RA1–RA13 (A46, frozen V004 addendum 487d4449);
- A47–A54, and A55 when it appears (production K_big P ∈ {64, 128}). Leave P as a single declared parameter until then.

**Rewrite the superseded R1 texts** (A47 I2 / A48 AMB-24) so the sealed text needs no erratum:
- T2_numerics and T2I (C5H, G5\G4);
- T2c (C4T-C5c);
- cites_by_name;
- run_list;
- brackets (RA4);
- the T1 pass text (V005 shape_pass AND RA6, with TINY applying only to RA6);
- the generic T3 (A54);
- the final outcome order (A50, with INCOMPLETE per A47 I1);
- the noise allowance (A51 as tightened by A54 S7, and NEW-7);
- R-PAIR (A53 and the R3-4 ruling);
- identity runs (A52.1, Z2_OFF_RO1);
- LO_NGC (A52.4);
- the GQ/EPS coverage rules.

**Binding inputs, with shas from bytes:**

| Input | Value |
|---|---|
| driver v010 r4 | b9ae92d5 |
| RO1 c2v002 pins | |
| nodes_v001 | c8a04fb5 |
| route-A / route-B successors | |
| spec registry | 9bfe9674 |
| certificates | certificates_v002 |
| comparator | c2v003 |
| C5H spec | 60b46130 |
| REVIEW_V009 ORIG | 3bce7c02 |
| compare | "PENDING r5 final sha", filled at seal |
| V005 addendum | "PENDING freeze sha" |

**Also write:**
- a **clause → source ruling map**, so every clause cites the A-entry it comes from;
- a **SEAL_CHECKLIST**: freeze V005; set the compare's V007_PREREG_SHA256 and PIN_ADDENDUM_V005; run `--gates-only` and `--validity-only --case C5H` on the real records with their output pasted in (E-SEAL1); B0 rerun with the B0-EMPTY fix (A54); B3 final; record the identity-run comparisons.

Flag every place where the rulings conflict or leave a clause undefined, as an item for root.

Read-only elsewhere. No launches. No C5H, `UVT_*` or target reads.
