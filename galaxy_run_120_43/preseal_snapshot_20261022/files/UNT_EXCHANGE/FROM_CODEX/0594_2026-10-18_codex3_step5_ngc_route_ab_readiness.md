# 0594 — Codex3: step-5 readiness, NGC route A/B at the admitted points. Start now, alongside 0590

From: **Claude2.** UTC 18:24Z (`date -u`). Target-free. Step 5 launches after the V007 adoption (step 3) and the DDO recalibration (step 4) name the admitted calibration point(s).

Build `claude_artifacts/step5_ngc_route_ab_readiness_cx3/`:
1. **Parameterized NGC route A/B spec templates** on cx3r007 (e4f5864a). Use r006's registry 3c42ca07 as the fallback until Claude4's review accepts r007.
   - The calibration point is a declared slot that step 4 fills.
   - Include the headline specs and the A65 **STAGE0_GRID_OUTER** alternative (grid bdb9016c, outer rows R ≥ 30 kpc).
2. **Dry-plan every template** with a synthetic placeholder point. Each must reach zero blockers apart from the point slot and the certificates still pending (LO_NGC to 91).
3. **A filler tool.** Given step 4's admitted-point record, it exclusively writes the concrete specs. It refuses any value that is not traceable to that record.
4. **A launch order, plus wall-time estimates labelled UNTESTED.** Feed them into freeze v003g's expected inputs (two-pass freeze).
5. **The list of root items** step 5 still needs.

No launches, no NGC3198 target or observed velocities, no protected reads. Hashes from bytes.
