# PARTIAL -- verify_consistency_1 (finding L-C01)

Started: 2026-10-18T19:23:37Z (date -u)

Status: in progress.

- Object hashes verified from bytes against HASHES_R2.txt: all 10 match
  (PREREG 6437ea33..., CLAUSE_SOURCE_MAP b105b55d..., ROOT_ITEMS 1d7af792...,
  NUMBER_PROVENANCE c81b5a7a..., check tool 85457a43...).
- Next: read PREREG r2, lens report, A15 source, CASES_RESULTS_V2.json.

## Update 2026-10-18T19:30:32Z (date -u)

- Quotes checked against PREREG r2 bytes: C-P L17, C-3.2 L195 and L200, C-8 L347 -- all present verbatim.
- V004 A15 L43-44 verified (E3 binding, "An outer-row failure would be TESTED-NEGATIVE for exactly this").
  E3 is sign-agnostic. V003 A10 L38 ("Every 120/43 miss is therefore read two ways") and A12.3 L91-95
  ("A miss reads three ways") are sign-agnostic too.
- V001 (6aecf0cb) had the P1-only trigger but NOT the C-P quote of E3: r2 added the C-P sentence (CSM row C-P,
  "quotes the A15 E3 scope"). A60 summarises V001 and rules nothing on the trigger.
- Partial refutation points so far: C-3.2 says "If P1 holds", not "only if"; the "consistent and against at once"
  in (a) depends on evaluating the P1-row against-column outside the P1 row (the lens classifier does this by
  construction; the CONFLICT 'C-P vs C-3.2' event is asserted by a lens rule, not derived).
- Supporting points the lens did not cite: C-5.3 L260 "E3 is the reading rule, applied through section 3";
  M-12 recommends a sealed classifier implementing sections 1-6 "exactly" (C-P is outside 1-6);
  R-DRIFT row L199 uses "OUTER miss-dominated" sign-agnostically; A63 L597 registers R-DRIFT for "outer-row misses".
- V005 read at 2026-10-18T19:26:54Z: 50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477 (has A92).
- Next: independent reproduction script (synthetic r only), fix check.

## Update 2026-10-18T19:35:33Z (date -u)

- Independent reproduction (tools/vc1_patterns.py, from the r2 text only, synthetic r) -> VC1_CASES.json.
  V1 (C08 replica) [P0] only, gap; V2 (falling curve crossing inside OUTER, delta_out -3.5) [P0] only, gap;
  V3 (crossing + TRANSITION not hit-dominated) [P0,P5]; V4 (C12 replica) [P0,P2], no explicit TN;
  V5 (2/8 OUTER MISS) [P0,P7]: C-P literal TN, C-3.2 no, fix no; V6 (3 MISS + 2 NEAR + 3 HIT, DEFICIT) [P0,P7]:
  fix no TN although the reference member fails 5/8; V7 (P1/P1g) all triggers TN.
  Enumeration 6^8 = 1679616 OUTER vectors: gap 835380 of 1531904 miss-dominated; P1-row against-column
  true while P1 reported: 0 (current) and 0 (lens fix replacement).
- Interim verdict: CONFIRMED (not refuted), BLOCKING stands; fix not sufficient as written
  (C-P L17 not rewritten; replacement against-column still unreachable; P11 omits A15 E3 readings 2-3; NEAR dilution).
- Next: VERIFY.md, REVIEW.md, HASHES.txt.

## Update 2026-10-18T19:38:28Z (date -u)

- VERIFY.md and REVIEW.md written. Final verdict: L-C01 NOT REFUTED, CONFIRMED in substance, BLOCKING;
  fix not sufficient as written (better fix in VERIFY.md section 5).
- V005 re-read at 2026-10-18T19:36:10Z: 6145a1f92cbace8d36f86a7c15be4d79ee6992717a5c57438cdd62045e070c7c (A93 added);
  no entry rules on R-MF or the patterns; cited lines L34, L507-L513, L597 unchanged.
- Status: complete; HASHES.txt written last.
