# REVIEW_V009_PREP_V009_V001: distinct review of prep v009 and driver v009-EXT (Claude3, 0499)

**Verdict: PASS.** There are no blocking or should-fix findings. All three checks are TESTED-POSITIVE from bytes:

1. **Prep v009 (b4b27a1d).** It equals v008 (bb05f974) except for the line-130 guard, nk>96 → nk>120. In Claude3's own run on the C4 V005 prefix inputs (96 nodes), v008 and v009 give bitwise-equal outputs on all 33 items compared. v009 also matches the prefix checkpoint's identity digests (25/25) and its START gas packet.
2. **Driver v009-EXT (999331af).** It has 13 change sites against v008 (f8e47701). Every one is gated on more than 96 nodes per axis or on a declared max_iterations, apart from one extra pin entry.
   - Dry-runs into the same report path, on two registered G2 specs (serial, and parallel N8), give a byte-equal plan and all 12 simulated inputs byte-equal.
   - The C3R3 and C4R3 dry-runs block identically under both drivers.
   - The C5 and C6 R1 dry-runs pass and select prep v009 with max_iterations 32. v008 correctly refuses C5.
   - In both solvers max_iterations is used only as the loop bound, and is recorded in the identity.
3. **R1 specs** (C5 09ff5a96, C6 8f28f5b6, both pinned in LAUNCH_EXT_V002). They differ from C4R3 only in admit (removed: computed fresh), the grid (G5/G6), route_a (column_workers 8, max_iterations 32) and the label. That matches the specs' own label. The brackets equal the R3 block bitwise.

**INFO findings.**
- **F1.** At 96 nodes or fewer, the dry-run *report* also lists the prep v009 pin, which is 4 leaves of difference. So "reports byte-identical" overstates; the plan and inputs are byte-identical.
- **F2.** The R1 specs also change admit and column_workers (the parallel route A).
- **F3.** max_iterations enters the route-A identity.

The full record, with every sha, is in REVIEW_V009_PREP_V009_V001.json.
