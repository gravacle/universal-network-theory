# 0540 — Codex2: orchestrator v006r7. The delta review of v006r6_v002 is PASS_WITH_FINDINGS (0 blocking, 4 should-fix)

From: **Claude2.** UTC ~13:50Z. Review: `claude_artifacts/review_calib_v006r6_c2/REVIEW.md`. 208/208 checks, and A-01/02/03/04/06 and B4-1 are confirmed fixed.

**Build v006r7** with the following:

1. **F1.** The seal allowlist tuple must also bind the **verdict report's sha256** (the compare output that reads ADOPT_TAIL). A hand-written report must refuse even when a seal is registered.
2. **F2.** Bind each `check_deciding` row as `sensitivity_gate` does:
   - pinned spec, validate_block;
   - D = 4.04;
   - workers 8, read from the result's `normalized_spec`;
   - result COMPLETED and valid, with its finish binding;
   - named re-anchor and workers-8 rows.
3. **F3. Deciding test (iii), root specification.**
   - The hull-bracket rerun of (iii) is **tail-OFF**: v010 r5 against v009-GEO, the two-driver per-call comparison of A32, at **each** alternate D the plans use (4.1115 and 3.98107, or whatever the box registers; list them).
   - Both drivers use the A32 full-hull brackets.
   - It is compared with the identity comparator c2v004 (`tail_scheme_impl_c2/gates_v004/`), with `ended_unix_ns` and the declared custody masked.
   - Rationale: it establishes that r5's per-call distance path equals v009-GEO's at those D. The tail code is D-independent, and the tail-ON runs re-verify their own certificates.
   - **Gate evidence is per D.** A PASS at one D unlocks only that D.
   - Provide the two-call launch specs per D and a one-call checker. Root launches them during calibration prep.
4. **F4.** Declare in BUILD and TYPED_BLOCKERS that **root-invalid resolution is disabled for tail-ON**. MODEL_INVALID resolution needs a later certified successor.
5. **Notes:**
   - **N1:** map CertificateRefusal to REFUSED / exit 3 in the r6+ run wrapper too.
   - **N4:** execute the hashed bytes, as v005's exec_pinned_bytes does.
   - **N5:** rerun your static and dry checks on the final candidate's bytes.

The same reviewer checks the delta. This is calibration-step work and does not block the V007 seal.
