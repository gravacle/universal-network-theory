# 0352 independent check record

**Join author:** CLAUDE2 helper 0352-join.
**Checker:** CLAUDE2 helper 0348/0350/0352-check, a separate Claude helper.
- It read real coverage, bundle metadata and the 0341/0346 files.
- It never resolved value, error, mass, density, area or scatter fields.
- No network, no edits, no deletions.

**Verdict: PASS_WITH_NOTES** (presentation-level only).
- 978/978 genuine pointers resolve. The 979th pointer-named field is a prose note.
- 2477 claimed-metadata checks, 0 mismatches.
- Issue→query lists reproduced from stored indices:
  - U1 = Q42–Q43 (120-arcsec annulus 5, both orders)
  - U2 = Q37–Q41
  - U3 = Q01–Q36
  - U9 = Q04–Q07
  - U10 = Q26–Q28
  - U11 = Q20–Q28
  - U12, U13 and U18 attach via S1 to Q01–Q28; U4–U8, U16 and U17 via S2 to all 43 queries (U7 attaches to none).
- D1, D2 and D3 confirmed; no missed disagreement.
- UR-1 to UR-5 are genuinely choice-dependent and correctly named; no hidden choice.
- 0346 correction ids are correctly attached.
- No forbidden value leaked.
- The re-run is byte-identical.

**Notes:**
- **N1:** UR-2's candidate list mixes contained annuli (Q42–Q43 via 40-arcsec annuli 15–17) with the overlap-sliver case (Q40–Q41 via annulus 14, a 4e-15 edge-text difference, see D3). The per-query references do not separate the two.
- **N2:** the issue_to_query_summary entries for U8, U13 and U16–U19 carry correction ids by reference only.
- **N3:** U15 membership rests on ledger prose, unavoidably and as labelled.
