# REVIEW_RECORD_0361_V001: distinct provenance check of the primary-document follow-up

**Task:** Codex1 0361. Documentary only.

| Role | Who |
|---|---|
| Author | Claude helper a9f7371c107f28a8c |
| Distinct provenance checker | Claude helper a206adb4d5d6cf2d1 (wrote none of the checked files) |
| Coordinator | CLAUDE2 main |

## Verdict: PASS_WITH_NOTES

All 8 artifact hashes matched, and so did the PDF (87fa3959…).

**1. Quotes.** The checker used an independent decoder, poppler pdftotext, in memory, and rendered no page.
- SP-1 to SP-8 match verbatim after mapping the paper's three Symbol-font glyphs. Each occurs only on its stated page.
- Sections were confirmed from word coordinates:

  | Quote | Page | Section |
  |---|---|---|
  | SP-1, SP-2, SP-3 | p.3 | §3.1 |
  | SP-4, SP-5 | p.5 | §3.1, above the §3.2 header |
  | SP-6 | p.6 | §3.3 Mass Models |
  | SP-7, SP-8 | p.14 | references |

  In the plain text stream, SP-6 appears before the §3.3 header. This is a reading-order artefact.
- "kill", "comment", "sfb", ".sfb" and "#" each occur 0 times across all 14 pages.

**2. Statuses are justified.**

| Item | Status |
|---|---|
| U14 marker / kill / error | UNRESOLVED_MISSING_DOCUMENT |
| U15 | PARTIAL, strengthened; the row-level .dens reading is marked as interpretation |
| Stars row 2, U10, U11 | Unchanged |

The "from" statuses match 0356 V002 (13ebe908…).

**3. Leroy and related search.** The checker re-ran the name-only search over /Users/bgm/Research: 962,425 files, no walk errors. It found no Leroy paper, Appendix E, printed Table 7, Archangel documentation or Schombert & McGaugh 2014b.
- The identifiers match CDS ReadMe lines 58–64 exactly.
- arXiv 0810.2556 appears at readiness-note lines 72, 179 and 188.
- No DOI appears locally; a content search for "0004-6256/136" found 0 files.
- The retrieval target is correct and minimal.

**4. Preservation.**
- Correction 0346 still hashes to 988e871a…, and C4 is still binding.
- e=0.0 is not treated as zero, blank H2 is treated as absent, and commented rows are not adopted.
- No likelihood, conversion or choice was introduced.

**5. Values.** No data value appears in any delivered file. Every decimal is one of: a section number, the 3.6 band, ascl:1107.011, the bibcode, the arXiv id, a timestamp, or 1.0/0.0. "3198" occurs on no page of the paper.

**6. Reproducibility.** Evidence (71596a7f…) and delta (9e86eaf6…) reproduce byte-identically. They depend on the live /Users/bgm/Research tree, as the manifest states.

**7. Exposure.** The author's disclosures X1–X5 are adequate. Every rendered or decoded page holds non-target material only. The checker incurred no target or table exposure: it printed only masked contexts and block coordinates.

## Notes (LOW/INFO), recorded as errata; no V002 issued

- **H1 (LOW).** The retrieval target says "no value rows are needed". The secondary note's account, however, rests on the printed **NGC 628 example rows**, so adjudication may need those non-target example rows. Read "expected sufficient: Appendix E conventions text plus the printed Table 7 header and notes; the non-target NGC 628 example rows may be needed".
- **H2 (LOW).** Two binding and id inconsistencies with 0356 V002:
  - The delta drops OPEN-9 from the binds of stars row 2, U10 and U11. 0356 V002 binds stars row 2 to OPEN-8 and OPEN-9, and U10/U11 to OPEN-4 and OPEN-9. **These 0356 V002 binds remain in force.**
  - The delta also renames the U14/U15 items. Read its U14 items as 0356 V002 `SFB_COMMENTED_ROWS_AND_KILL`, and its U15 item as 0356 V002 `S3_S4_OBSERVED_SUPPORT`.
- **H3 (INFO).** Two relevant generic statements are not cited, and neither changes a status:
  - p.6 §3.3, on the bulge: "linearly extrapolated at R > Rbul to avoid unphysical truncations";
  - the p.10 figure caption: "Open circles show extrapolated values for bulge … and disk … components".
- **H4 (INFO).** `doi_in_local_documents` is computed from the ReadMe only. The checker's wider search confirms there is no DOI locally.
- **H5 (INFO).** The builder hard-codes the Leroy identifiers rather than asserting them; the checker verified them manually. The evidence-script docstring says "scratch" is excluded, but the code excludes only .git. This has no effect.

## Checker evidence (read-only copies in `check_0361/`)

| File | sha256 |
|---|---|
| strict_decimal_scan_0361.txt | 53248c82410a989bbab0b4abcd4a94e542985bcf315c76ca632cd77f373e23ad |
| quotes_from_evidence.json | 9242d7ae68c2232d669e08d20f78c3bb342b7ee81345e5b2abb21f4f7bd542e0 |

`evidence_log_0361.txt` was not copied because it contains unclassified decimals. It remains in the session scratch `check0361/`.

## Status

REVIEWED. The documentary result is that no status changes. The missing primary documents are:

| Question | Documents |
|---|---|
| .sfb `#`, kill, error | Archangel (ascl:1107.011) and Schombert & McGaugh 2014b, PASA 31, 11 |
| e=1.0 marker on stars row 2 | Leroy et al. 2008, AJ 136, 2782; arXiv:0810.2556; Appendix E and Table 7 |

Retrieving them needs root's separately authorized search. No likelihood or physical source state is chosen.
