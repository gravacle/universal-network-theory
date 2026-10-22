# PARTIAL — verify_targetfree_1 (adversarial verification of targetfree finding B-1)

Started: 2026-10-18T19:20:03Z (date -u)
Lane: Claude4 helper. Authority: dispatch 0585 (assigns r2), 0592 (independent lenses). Read-only on object.

## Step 0: object hashes verified from bytes (shasum -a 256), all match HASHES_R2.txt
- PREREG_MISS_READING_R2.md 6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143 MATCH
- CLAUSE_SOURCE_MAP_R2.md b105b55d7f80c5868d936f577ce81e92992999440f5cd85a06decbc62650d24b MATCH
- ROOT_ITEMS_R2.md 1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f MATCH
- NUMBER_PROVENANCE_R2.json c81b5a7a579476480a085681ebd6eb8aa445e38b6a7abe2284dba3716b0c2832 MATCH
- TARGET_FREE_CHECK_R2.json aab683236116bc3562df86f3b9542a54eec3446c44a8f0e5569ff2b305d2180b MATCH
- TARGET_FREE_MUTATION_TEST_R2.json 2a8202b823beb5cd0bc03c9e1e2b0377d9de59410a698c8d185f39739d66bc41 MATCH
- tools/check_target_free_c4v001.py 85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7 MATCH

## Progress
- (in progress) reading finding quote sites and evidence

## Update 2026-10-18T19:26:33Z
Sources read (sha256 from bytes):
- V005 open addendum read at 19:21:30Z: 50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477 (holds A47-A92; copy in snapshots/V005_AT_VERIFY.md). Differs from r2's 17cb4fd4 and the lens's 0753f2d8 (A92 added at 19:16Z, inserted at L890).
- V004 487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b MATCH; V003 5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468 MATCH.
- RUNBOOK_V001 9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b MATCH; module 48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405 MATCH.
- 0585 9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd MATCH; 0594 19e874ecb927be6ead60e363648d5768b2c1b66d87782ae167e68f5e9d09bd90; 0606 dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e; 0522 30af5d68...(matches r2 C-11).

Quote checks (all CONFIRMED verbatim):
- r2 L12 seal clause: present; only constraint "before any NGC3198 target is opened". M-6 item 1 (ROOT_ITEMS L117): "in a root entry made before any target access". No r2 clause ties the seal or the M rulings to step 5.
- r2 L369-372 residual rows: present; each closes only "before the seal".
- V005 L513 (A60): "Root rules on them and seals the prereg **before targets are opened**, in the freeze step." CONFIRMED.
- Step numbering CONFIRMED: V005 L739 (A70) "Step 6's freeze code is ready"; L848 (A77) "NGC route A/B run (step 5)"; L1120 (A80) "Step 5 is more than a day away". So the freeze step is after step 5.
- RUNBOOK L7-L15: first pass step 1 saves raw forward results; root registration (step 4) follows. CONFIRMED.
- V004 L747 is inside A41 (L717-752): CONFIRMED. V004 L28 (A15) CONFIRMED. V005 L24 (A47 I3) CONFIRMED.
- 0594 L3: "Step 5 launches after the V007 adoption (step 3) and the DDO recalibration (step 4)". CONFIRMED; latest A92 (19:16Z) is still V007 identity gates, so step 5 has not launched.

Extra evidence found (strengthens B-1):
- 0606 L5 + L11: rough edge 5 "Adoption of the unsealed prereg and the production classifier" needs a ruling "before step 6" - coordinator's live deadline is step 6, i.e. after step-5 outputs exist.
- step5 readiness ROOT_ITEMS_CX3V002.json R12 (3e9e31d4...): "Root decides its radial-support interval before freezing flags."
- V005 L189 (A52): C5H model outputs kept blinded until the V007 seal ("--validity-only", A47 I3) - the program does blind model outputs before a prereg seal.
- 0522 L9: coordinator: "A41 says static present-mass gravity cannot give a flat outer curve ... So outer-row misses are expected".
- freeze module has no print/logging and no __main__: a validity-only freeze is feasible from the module side.

Imprecisions found in the finding (minor):
- "C-Status" is not an r2 clause tag: the Status block (L3-13) carries no [C-..] tag and has no row in CLAUSE_SOURCE_MAP_R2.md, though L13 says each clause carries a tag.
- "RUNBOOK steps 2, 4 and 7 need only finiteness, cut records and projections": step 7 says nothing about projections; it calls evaluate_envelopes, which does consume predicted values in code (no human read needed).

## Update 2026-10-18T19:28:37Z
More object evidence (strengthens B-1):
- ROOT_ITEMS_R2 M-12 L220 + L226: the classifier "is sealed together with this text" and "costs a few hours of target-free work, off the critical path until step 6" - the author's own plan puts the seal near step 6, after step 5.
- r2 L367 uses "before step 5" for K_big/M_s/certificates only; no reading rule or M item gets that bound.
- V005 L1259 (A65.2): STAGE0 runs come after the headline NGC runs; adoption decided at the freeze (overlaps B-3).
- check tool T6 (L8): only checks that existing tags are mapped; the untagged Status/Seal block escapes it, so INDEX L24 "Every clause is mapped (T6)" over-claims (side observation).
- T1-T6 are all text scans (tool header L3-L8): "T1-T6 cannot detect this" CONFIRMED.
Next: a synthetic toy (dimensionless, non-physical) showing that M-1/M-3 options flip P1 and are predictable once predictions are visible.

## Update 2026-10-18T19:32:13Z
- Correction to my earlier note: "projections" in the finding is ACCURATE. v003g REFERENCE_RULE (module L85) and SELECTION_RULE (L66) use parameter-space (u-space) projections, finiteness and log_index, never predicted values. So D1, member selection and reference choice need no human read of a prediction. Module has no print/logging.
- Blinding precedent is V005 L189, which sits in A51 (L140-190), not A52: "C5H stays blinded until V007 is sealed ... read only through the compare's --validity-only mode (A47 I3)".
- Synthetic toy (tools/steer_toy_v001.py 57a6abe8..., runs/STEER_TOY_V001.json 65f7ecf0...; dimensionless sentinels, numpy only):
  P(P1) by option once predictions are known, rough level knowledge sd 3%:
  - marginal deficit, wide band: M-1(a) 0.069, M-1(b) 0.632, M-1(c) 0.821, M-3 two-thirds 0.039 -> option choice decides P1;
  - marginal deficit, narrow band: 0.526 / 0.637 / 0.828 / 0.413;
  - no deficit: 0.054 / 0.103 / 0.253; large deficit: 1.0 for every option (choice free of cost).
  Blind (predictions unknown, broad prior): 0.756 / 0.839 / 0.904 / 0.708.
  => B-1's "could be tuned" REPRODUCED in a toy; the band width alone (visible in step-5 outputs, no target needed) tells the ruler whether M-1(a) will absorb outer misses as NEAR, which C-9 L370 claims cannot be steered.
- Working verdict: NOT REFUTED; severity SHOULD_FIX agreed; fix right in direction, insufficient as worded (produced-or-read conflict; fallback covers only M items; non-executable M-7 / conditional M-11 under "exactly as written"; who is blinded; tag/map row).

## Update 2026-10-18T19:34:00Z
- V005 changed during the check: at 19:33:21Z it reads 6145a1f92cbace8d36f86a7c15be4d79ee6992717a5c57438cdd62045e070c7c (copy snapshots/V005_AT_VERIFY_2.md). The only change is the new A93 (19:31Z) inserted at L890: cx3r007 accepted; registry cd30429c is the step-5 launch registry; should-fix items "before any step-5 launch". So step 5 is still not launched. Nothing on the prereg seal timing. VERIFY.md cites line numbers against 6145a1f9 (lines below L890 are unchanged from 50fe0f1c; later lines shift by +6).
- V001 L4 "Root seals it before the score step opens the targets." The weak timing is inherited from V001, not a regression in r2.
- CURRENT_INSTRUCTIONS (59ada35c...) L114/L133: freeze predictions before target scoring; L133 discourages documentary cycles, so the fix should cost no new tooling.
- Next: write VERIFY.md, REVIEW.md, HASHES.txt.

## Update 2026-10-18T19:36:03Z
- VERIFY.md and REVIEW.md written. Verdict: NOT REFUTED; SHOULD_FIX agreed; fix insufficient as worded (amended fix in VERIFY.md section 4.2). Next: HASHES.txt.
