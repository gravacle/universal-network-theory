# UA_CHAIN_G10_PARTIAL_C3V001: G-10 (row 32's middle steps). The KS4 forms come from tool bytes; the ρ-registration and LO slot-proof tools stay open

From: Claude3 (lead). 2026-10-22T08:27:16Z (`date -u`). Procedure A `4da9ddb5`, step 6 (L82–88). FORMAL, UNTESTED.

**KS4:** `claude_artifacts/ks_k3_chain_successor_cx1/registry_assembler_ks4_cx1v002.py` `ef821296`, which its README L5 names with `s4rc1_common_ks3_cx1v002.py` (the A268 cxv002 successor). argparse is at L579–592.
```bash
K4=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_successor_cx1/registry_assembler_ks4_cx1v002.py
"$PY" -I -B "$K4" bundle --out-root "<NEW>" --point 32 --eps-proof "<EPS_PROOF>" --gq-proof "<GQ_PROOF>" --lo-proof "<LO_SLOT_PROOF>" --approved-producers "<APPROVED_PRODUCERS>"   # exactly one point
"$PY" -I -B "$K4" registry --out-root "<NEW>" --bundle "<BUNDLE_32>" --approved-producers "<APPROVED_PRODUCERS>"   # repeat --bundle for every row the S1 C1 needs
"$PY" -I -B "$K4" verify --registry "<REGISTRY>" --registry-sha256 "<SHA>" --c1 "<S1_C1>" --c1-sha256 "<SHA>" --points 32 --out-root "<NEW>"   # producers and custody deriver come from the C1 (L589)
```

**Open (root, with G-01 and G-02):**
- **The ρ-registration tool for a single u_A row.** The adopted list helper `cp1_list_rho_slot_cx1v004.py` (`820d16a5`, `register|stage`, L122–125) is built for CP-1 list mode (P300–P302). Root rules whether it serves row 32 as a one-point list, or whether procedure A's single-point registration applies.
- **The LO slot proof:** c3v003, or its K=3 successor if K6 fails (procedure A step 6.4).
- **KS4 `verify` needs the S1 C1,** which is G-06's unbuilt freeze tool.
