# PARTIAL — verify_targetfree_2 (adversarial verification of targetfree finding B-2)

Started: 2026-10-18T19:20:04Z (date -u)
Lane: Claude4 helper. Authority: dispatch 0585 (Claude2) and dispatch 0592 (independent refute-by-default lenses).
Object: miss_reading_prereg_c4/r2/round1 (not edited).

Status: started. Steps:
1. verify object hashes from bytes - pending
2. read r2 C-1.4, C-9, ROOT_ITEMS M-7 - pending
3. read lens report B-2 - pending
4. verify evidence (K32 compare record, N1 record, query radii, flag-set table) - pending
5. assess severity and fix - pending

## Progress log
- 2026-10-18T19:26:32Z: step 1 done. All 10 HASHES_R2.txt entries match shasum -a 256 (prereg 6437ea33..., root items 1d7af792..., etc.).
- step 2 done. Quote is real: ROOT_ITEMS_R2.md L138 "the radial support [r_lo, r_hi], exactly as stored in that record;" and L140 "A query q is flagged if and only if r_lo ≤ R_q ≤ r_hi." (finding uses ASCII <= and an ellipsis splice). C-1.4 L126 and C-9 L371 present as cited.
- step 4 (evidence) so far:
  - K32_COMPARE_COMPLETE_V001.json sha 6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9 (matches Codex1 0056 pin); failing_TRUNCATION_SHAPE_rings[0].radial_support = {kind: sampled_ring, R_kpc: 10.540847190215317}. CONFIRMED.
  - N1 record K32_RECORDS_COMPLETE_V001_N1.json sha 8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70 (pinned by manifest cf8dc2c9...): stores ring_radii_kpc (100 points) and no radial_support or interval key at all. ring 14 = 9.901810628740723, ring 15 = 10.540847190215317, ring 16 = 10.911721936765339. CONFIRMED.
  - Producer intent: ntests_compare_k32_cxv003.py docstring "Failing ring support is the sampled radius, not an invented finite radial interval."; BUILD_K32_COMPLETE_V001.md L9 "Its support is the sampled ring, not an invented radial interval." The point form is by design.
  - Dispatch 0550 L11 (root): compare must list failing rings "with S/θ and radial support. The freeze flags the overlapping rows". Dispatch 0606 (18:59Z, after r2) item 2: "A carrier for the TSR flag and radial support" still a rough edge. Codex1 rehearsal REHEARSAL_COMPLETE_V001.json: "No sealed TSR flag carrier/radial support rule ... do not infer physical flagged rows."
  - Query radii from slots V003 (d3859b42...): Q24 9.04, Q25 10.04, Q26 11.04. CONFIRMED.
  - New: the 100 N-test rings equal the 100 registered GL4 route-B nodes bitwise (REGISTERED_ROUTE_B_GL_NODES_CX3V001.json ec1dcca5...), and the registered observation rule interpolates node means piecewise-linearly onto query radii. So a registered, target-free footprint exists: rows bracketed by ring 15 and a neighbour, (r14, r16) -> Q25 only.
  - RUNBOOK step 1 saves raw forward results; step 4 (rosters) comes after. CONFIRMED that M-7's record registration is after predictions exist.
- V005 at verify: 50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477 (adds A92; no entry defines radial support; A66.2 L635 is the only use).
- Next: independent recomputation of flag sets (kpc and metre arithmetic), severity and fix assessment.
- 2026-10-18T19:30:43Z: independent recomputation (tools/recompute_tsr_flagsets_vt2.py -> runs/TSR_FLAGSET_RECOMPUTE_VT2.json): reproduces the lens table exactly (point none; midpoints none; neighbour rings Q25; two each side Q24-Q26; +-0.5 kpc Q26). Extra: open (r14,r16) interpolation footprint Q25; +-0.25 none; +-1.0 Q25,Q26. kpc and metre arithmetic agree for all 8 candidates; min query-to-endpoint distance 0.00085 kpc. Synthetic P10 reachability: point 0/20000; neighbour rings 4933/20000.
- Corroboration: Claude4 0091 (18:59:25Z) states the point-support fact and plans the open (r14,r16) neighbour interval flagging exactly Q25 for the final r2. Round1 bytes still carry the defective M-7.
- Draft verdict: B-2 CONFIRMED (not refuted); severity SHOULD_FIX agreed; fix works in direction but needs binding + fail-closed, a derived (not picked) rule, timing tie to B-1, and kpc/metre wording. Two minor over-statements in the finding ("Any interval ... changes the flagged set"; "M-7 places that choice at step 4").
- Next: write VERIFY.md, REVIEW.md, HASHES.txt.
- 2026-10-18T19:33:25Z: VERIFY.md written (sha256 098d5d8fc44ccac4479cf8ab06ded468bb5f858a0a6ab762535a64388bdf380f). Verdict: B-2 CONFIRMED, SHOULD_FIX agreed, fix needs refinements R1-R6. REVIEW.md and HASHES.txt follow. Status: complete.
