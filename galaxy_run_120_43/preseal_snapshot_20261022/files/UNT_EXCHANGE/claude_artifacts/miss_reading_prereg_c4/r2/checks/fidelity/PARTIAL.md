# PARTIAL — Lens A (fidelity and coverage), miss-reading prereg r2 round1

Started: 2026-10-18T18:48:31Z (date -u). Last update: 2026-10-18T18:58:25Z (date -u).
Status: IN PROGRESS. Object hashes verified from bytes (all 10 match HASHES_R2.txt and the task list).
V005 read: bba6daf53ad07d691d09648801bc113b61718e4be0568a6d870cdb87982d1a17 (18:49:07Z, newest A90; snapshot in this folder),
then 0753f2d8dc437592a4ad70140f309c774837cb07e9c04e2c213c4421eeb8e87e (18:52:42Z, newest A91). All 11 cited per-entry pins MATCH on 0753f2d8.

Findings so far (draft severities):
- F-M7 (BLOCKING?): M-7 rule "[r_lo, r_hi] exactly as stored in that record" — the record of record (K32_COMPARE_COMPLETE_V001.json 6f095f64, 0056/A90)
  stores radial_support {kind: sampled_ring, R_kpc: 10.540847190215317}: a point, no interval. Closed-interval rule flags 0 rows;
  ring sits 0.0008 kpc above the Q25/Q26 midpoint (10.54) -> any cell definition is knife-edge. Undefined on the actual record.
- F-0512 (SHOULD_FIX): I-6 "Under the 0512 ruling ... only N_PASS is an input to route A/B" misreads 0512 ("N_PASS licenses nothing by
  itself. It is an input to the NGC route-A/B step") and contradicts A66.2/0550/A90 (N_FAIL_N1 confined -> gate OPEN). Gate object is
  n_route_ab_gate (0550), not cited.
- F-NEAR (SHOULD_FIX): "NEAR means some admitted representative member state reaches the error bar" — false; band overlap (pointwise
  min/max) does not imply any member within error (straddling band). Same in M-1 reasoning.
- F-INV (SHOULD_FIX): §1.1 "INVALID_AS_MISS holds exactly when roster registers q INVALID with one of the three registered reasons" —
  gate reasons also yield INVALID_AS_MISS (code _authorized_row_registration/_score_members); and gate rows are INVALID only if the
  producer reports them so (gates authorize, do not require; _root_frozen_rows). §4 "INVALID set is exactly the set the roster registers" over-claims for gates.
- F-S11 (SHOULD_FIX): §11 "Every other V005 entry predates V001 and was used there through V001's citations" is false (V001 cited only A48 and the A55 log);
  A50 is cited (C-I7 map, M-8) but not pinned, not in the M-6 seal-check list. 0512, 0519, 0521, 0523 cited but not pinned; NUMBER_PROVENANCE says "(section 11 pins it)" for 0519/0521/0523 — false.
- F-MAP (NOTE/SHOULD_FIX): map lists A62 and A70 among "read with no change" while C-4/§11 cite them; map omits A89; §11 vs map lists disagree.
- F-COV (SHOULD_FIX): coverage gaps: 0550 (A66 consequence dispatch: compare lists radial support; n_route_ab_gate) not cited; A90 (formal K32 N-test result, gate OPEN, LO I1-T step-5 open item) post-dates assembly;
  M-6 item 3 covers only V006 entries, not V005 entries after A89 (A90, A91) before the V005 freeze; NGC I1-T (A52.4/0512) absent from I-6.

Update 2026-10-18T19:13:41Z (date -u):
- New dispatches 0605/0606 read (0606 dbb80c77: rehearsal rough edges for r2 — corroborates I6 0512 wording, M-7 carrier, P8 C3 carrier).
- Codex1 0056 (4b67319d) + K32_COMPARE_COMPLETE_V001.json (6f095f64): radial_support = {kind: sampled_ring, R_kpc: 10.5408...}; confirms F-M7.
- Codex1 0032: GQ_NGC MS96 holds on [2, 91] (be148bab) -> RI-23 antecedent false before assembly; not registered in r2.
- New finding F-E3 (SHOULD_FIX): R-MF TESTED-NEGATIVE only on P1; A15 E3 / C-P say any outer-row failure. Repro R5: OUTER miss-dominated + CENTERED -> no pattern P1-P9 at all.
- New: R-GRID/P8 rely on A17 tier-1 C3 record (G80C FAIL); in-use T120L passes C3 (A27 L365/L370); I-6 says only numerical reading is R-TSR.
- New: D-2 omits A65 "A2's own single chains span -5.20 to -1.76"; D-1 omits A63 "R-LIT and R-MA fail. The background passes."
- New: r2 dropped V001 §4 "with its truncation radius and mass fraction" (A14 C3/A12.5), unrecorded in the map.
- New NOTE: v003g D2 guarantees the twin (same log_index) for every evaluated alternative (L3164/L3184/L3644); M-10 "UNTESTED" wrong.
- K-1: no consequence found beyond the description (no odd-backtick lines; digit-bearing code spans are file names only).
Repro outputs: REPRO_LENSA_OUT.json (R1-R4), REPRO_LENSA_OUT_V2.txt (R1-R5). Next: write REVIEW.md and HASHES.txt.

Final 2026-10-18T19:17:02Z (date -u): COMPLETE. REVIEW.md written (verdict FAIL: 1 BLOCKING, 10 SHOULD_FIX, 7 NOTE).
V005 final read b7a900c4c495b4e9876701918a32ed8e1770da3438a8561e2b18bbd8d0b3ccda (newest A92, V007-only); all 11 cited pins MATCH.
Dispatches read through 0609. HASHES.txt written last.
