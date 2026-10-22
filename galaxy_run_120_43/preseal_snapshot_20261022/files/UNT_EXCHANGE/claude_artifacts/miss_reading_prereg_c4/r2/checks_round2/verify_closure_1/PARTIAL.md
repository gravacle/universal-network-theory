# PARTIAL — verify_closure_1 (adversarial verification of closure-lens F1)

Started: 2026-10-18T20:28:51Z (date -u)
Lane: Claude4 helper; refute-by-default recheck of round-2 finding F1 (lens closure).
Status: started; reading object bytes and sources.

## Progress 2026-10-18T20:37:22Z (date -u)
- Object: all 10 HASHES_R2.txt entries match (shasum -a 256 -c), PREREG 97d5ce33..., CSM 38cd6852..., ROOT_ITEMS 4907cf01..., HASHES_R2.txt 2e3cf0c6....
- Sources read from bytes: V003 5bef6552 (A10 L38, A12.3 L91-L95), V004 487d4449 (A15 E3 L43-L50, A20 L154-L162, A41 L742-L749), V005 open now 7f552858 (snapshot V005_SNAPSHOT_AT_VERIFY.md; A98.2 orders r3 for undefined-sign only), CURRENT_INSTRUCTIONS 59ada35c (L305), slots V003 d3859b42 (SA-BH-01 and SA-REACH-01 pre_declared_reading_verbatim, via tools/slots_sa_notes_vc1.py), 0522 30af5d68 (L9-L13, L22), 0619 238858d1, Codex2 0490 3a922168, Claude4 0096 3f50d9d6 (r3 design: P14 carries R-MF only).
- Round-1: fidelity A-04 (L130-L151), consistency L-C01 (L42-L72), verify_consistency_1 (F-c L139-L144; better fix item 3 L155-L159).
- Closure-lens repro runs/READINGS_E3_R2A.json ff0355b6 and tool 330dbea8 read; table transcription checked against PREREG L271-L290: correct.
- Interim verdict: F1 quoted text present and defective; not refuted so far. Next: independent repro incl. P5+P2 and scope rule.

## Progress 2026-10-18T20:41:24Z (date -u)
- Independent repro tools/vc1_readings_by_zone.py (f47abc22...) -> runs/VC1_READINGS_BY_ZONE.json (09fc0081...), written from r2 text only (L105-L119, L187-L229, L249, L267-L290), with the [C-3] L249 zone-scope rule:
  - V2 P2 alone, V3 P11 crossing, V4 P11 alternating: E3 TESTED-NEGATIVE; OUTER rows cite no R-UT1/R-HIST/R-REACH and no history/species reading. Reproduces F1.
  - V5 P2+P5 and V6 P11+P5 (same OUTER rows, TRANSITION 6/11 MISS): OUTER rows DO get R-UT1/R-HIST/R-REACH via P5 "as P1" (L284). The registered reading set of one OUTER failure depends on the TRANSITION zone. New strengthening point.
  - V7 P13 only: TRANSITION has neither R-MF nor a history/species reading; V8 P7 and V9 P6: R-MF but no history reading outside INNER. Supports F1 fix item 4 (A10).
- V005 snapshot 7f552858: A63 section pin 8cbe6553 MATCH (A63 L597 "a further registered reading for outer-row misses"); A48 pin MATCH.
- Codex2 0490 and its sub-lens reviews, Codex2 checklist 020ef3f1 and Codex1 rehearsal 19807bb3 do not raise or dismiss this issue.
- Claude4 0096 (r3 design): P14 OUTER_UNSIGNED "carries R-MF ... and no sign-specific reading" -> the gap would recur in r3 unless the readings are keyed to OUTER_FAILURE.
- Interim: NOT REFUTED; BLOCKING stands; fix not sufficient as written (P14 recurrence; NOT_ADDRESSED tuple clash; P5 'as P1' not addressed). Writing VERIFY.md next.

## Done 2026-10-18T20:44:57Z (date -u)
- VERIFY.md and REVIEW.md written. Verdict: F1 NOT REFUTED, CONFIRMED in substance; severity BLOCKING; fix not sufficient as written (better fix in VERIFY.md section 6). HASHES.txt follows.
