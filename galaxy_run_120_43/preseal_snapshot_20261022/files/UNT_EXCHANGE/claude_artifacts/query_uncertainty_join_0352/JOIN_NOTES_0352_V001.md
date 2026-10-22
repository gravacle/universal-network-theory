# 0352 query-uncertainty join: notes (CLAUDE2 helper 0352-join)

This is a documentary join with metadata only. It makes no source, threshold, transfer-rule or physical choice. It contains no density values, error literals, masses, areas or scatter. Nothing was interpolated, resampled, converted or fitted, and no adapter was rerun.

## What was joined
- **Inputs.** The join reads the ledger items U1-U19 and the bundle's open issues OPEN-1..OPEN-10. It joins them onto the root-run coverage output (`NGC3198_QUERY_SOURCE_COVERAGE_CANDIDATE_V001.json`, d22ea850...). Each query has five stored settings: S1 (Leroy rings) and four S2 settings (order 4 or 8 subpixels × width 40 or 120 arcsec).
- **How annuli were identified.** Annuli come from the stored `annulus_index` and the stored edge text. The ledger prose was used only to find the match. For example, U1 = 120-arcsec `annulus_index` 5 in both orders, with stored edges `40.142572795869576` to `48.171087355043504`. Its members are Q42 and Q43 in both orders.
- **Flags.** `value_missing`, `upper_limit_marker` and `effective_density_present` are copied exactly as stored.
- **Pointer checks.** Each of the 172 S2 entries' edge, completeness and mask-fraction pointers was resolved against the bundle by text equality. All 213 S1 component labels match the bundle labels.

## Scope classes
| Class | Items |
|---|---|
| ROW_LEVEL (S1 component) | U9 (stars row 2 only), U10 (stars rows 16, 18, 19, 20), U11 (H2 rows 10-22) |
| ANNULUS_LEVEL (S2, 120 arcsec) | U1 (annulus 5, group full), U2 (annulus 4), U3 (annuli 0-3) |
| SOURCE_WIDE | U4, U5, U6, U7 (attaches to no query), U8, U12, U13, U14, U16, U17, U18, U19; also OPEN-6, OPEN-8 (rms semantics), OPEN-9, OPEN-10 |
| QUERY_LEVEL_LEDGER_STATED | U15. It rests on prose only: S3/S4 grids are not stored in the allowed inputs |
| UNRESOLVED_APPLICABILITY | UR-1..UR-5 (below) |

Geometry (U8, U16), conversion (U13, U19, OPEN-10), overlapping HI (U17) and the stellar convention (U18) remain unresolved source-wide dependencies. They are listed once and referenced by ID. Wherever a crosswalk conversion or geometry statement is referenced, its 0346 correction comes with it:

| Items | Corrections and class |
|---|---|
| U8 | C6 (PROGRAM-DECLARED / CITED), C4 (SECONDARY) |
| U13 | C2 (PRIMARY-STATED helium-included; SECONDARY numbers), C3 (SECONDARY) |
| U16 | C4, C6 |
| U17 | C1 (PRIMARY-STATED / SECONDARY), C5 (PRIMARY / PROGRAM-DECLARED), C8 (SECONDARY) |
| U18 | C3, C7, C4 (all SECONDARY) |
| U19 | C7 (SECONDARY) |
| OPEN-10 | C1-C8 |

## Issue-to-query summary
| Item | Queries | Attachment |
|---|---|---|
| U1 | Q42-Q43 | 120-arcsec annulus 5, both orders, group full (literal) |
| U2 | Q37-Q41 | 120-arcsec annulus 4 (reported, not flagged) |
| U3 | Q01-Q36 | 120-arcsec annuli 0-3 (reported zero fraction; not a completeness statement) |
| U9 | Q04-Q07 | Through bracketing row 2/stars only |
| U10 | Q26-Q28 | Through rows 16, 18 and 20. Row 19 brackets no query |
| U11 | Q20-Q28 | H2 MISSING on a bracketing row. Q29-Q43 get an absence statement only, because they have no S1 row |
| U15 | Q32-Q43 (12) | Ledger prose. Q43 also lies beyond the last .dens row |
| U12, U13, U18 | Q01-Q28 | Through S1 rows; S1 rows exist only for the BRACKETED queries |
| U4, U5, U6, U8, U16, U17 | All 43 | Through S2 |
| U7 | None | |
| U14, U19 | None | S3/S4 are not in the coverage output, so there is no per-query join |

In the bracketing-row items above, "applies to a bracketing row" is not an interpolation claim. ABOVE_SAMPLED_RANGE queries (Q29-Q43) have no S1 row; the last row is carried for orientation only.

## Unresolved applicability (choice named, not made)
- **UR-1 (Q42, Q43).** Does U1 transfer to the half-footprint groups X_negative and X_nonnegative of annulus 5?
- **UR-2 (Q40-Q43).** Does U1 transfer to 40-arcsec annuli? This needs a containment-or-overlap rule (see D3). By exact text, annuli 15-17 are contained in annulus 5, and annulus 14 overlaps it by a sliver.
- **UR-3 (Q39-Q43).** 40-arcsec annuli with a nonzero stored zero fraction have no ledger classification. A threshold or reliability rule would be needed.
- **UR-4 (Q04-Q07, Q20-Q28).** What a bracketing-row item means for the query depends on an S1 query-mapping rule (OPEN-9). It also depends on the Appendix E meaning of e=1 (U9) and the meaning of literal e=0 (U10).
- **UR-5 (Q32-Q43).** U15 depends on whether the two commented .sfb rows (352.17 and 387.39 arcsec) count as observed support. Saying which queries this affects would need an arcsec-to-kpc conversion, which was not done.

## Ledger prose vs exact saved coverage
- **D1.** U9 reads "e=1.0 entries (HI rms; stars row 2)", and OPEN-8 reads "e=1 on HI/stars". In the saved bundle the Note-3 marker occurs only at `/sources/S1_LEROY_T7/rows/2/components/stars`. No HI component in any of the 23 rows is labelled UPPER_LIMIT_NOTE3. So "HI rms" is a column-level note, not a row occurrence, and U9 attaches to no query through HI.
- **D2.** U1, the crosswalk and OPEN-7 quote "43.66%" / "0.4366". The stored full-group zero fractions for annulus 5 are `0.43667663156285635` (order 0) and `0.4365616072529975` (order 1). The prose figure matches order 1 when rounded, but matches order 0 only when truncated (order 0 rounds to 43.67%). The prose names no order. The finite fraction is 1.0, so "of finite sky area" and the stored "of footprint" are the same thing here. This changes no attachment.
- **D3.** This is a difference between two saved profiles, not between the ledger and the coverage. The 600-arcsec edge is stored as `40.142572795869576` in the 120-arcsec profile and as `40.14257279586958` in the 40-arcsec profile, at the same pointers in both orders. By exact comparison, 40-arcsec annulus 14 is contained in neither the U2 annulus nor the U1 annulus. No query lies between the two values. Within the query domain this is the only nested edge whose text differs; across the full grid there are 16 per order.
- **Agreements.** The following prose matches the saved coverage exactly:
  - U1 edges (to 4 decimal places), U1's "2 queries", and Q41 (40.10) falling in annulus 4.
  - U2 = 0.0402 in both orders, with 5 queries.
  - U3 = 0 in all groups of annuli 0-3.
  - U10 rows; U11 rows 10-22, which equal OPEN-4.
  - U15's "12 queries".
  - The crosswalk band counts (28/3/5/5/1/1) and the S2 grid sizes (237/79 annuli; complete prefix 51/17 to 136.4847475059566 kpc).
- **Clarification.** "Outer" in U1 means annulus 5 of 79 stored annuli: the outermost annulus that holds a query, not the last stored annulus.

## Other notes
- The coverage `context.open_issue_refs` lists 8 of the 10 OPEN items. OPEN-2 (U18) and OPEN-6 are carried here directly from the bundle.
- S2 conversion conventions (1.25e20 per Msun/pc^2 and the helium factor) have no ledger U item. They are carried through C5 (PROGRAM-DECLARED) and OPEN-10.
