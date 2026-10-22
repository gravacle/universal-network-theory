# 0356 source semantics: notes (CLAUDE2 helper 0356-A)

This is a documentary addendum covering UR-4 and UR-5 from the 0352 join. It uses metadata only.
- The machine-readable record is `SOURCE_SEMANTICS_ADDENDUM_0356_V001.json`.
- Every quoted source line there is checked against `PROBE_EVIDENCE_0356_V001.json`.
- No interpolation, extrapolation, mask threshold, uncertainty distribution, galaxy state, response law, calibration, query-mapping rule or source choice is made.
- Root's 0352 review (`60551a33…`) and correction 0346 (`988e871a…`) are preserved:
  - N1, N2, N3, D2 and D3 are unchanged.
  - D1 is re-grounded on primary ReadMe lines.

## Outcome

| Item | Status | Short answer |
|---|---|---|
| UR-4 / U9: column meaning of e = 1.0 | RESOLVED_DOCUMENTARY | CDS ReadMe Note (3) "1.0 = upper limit." It is attached to e_SigmaHI (line 172) and e_Sigma* (line 176) only. It does not say which quantity is limited, the bound, or the significance. |
| UR-4 / U9: stars row 2 (the only NGC 3198 occurrence; Sigma* populated) | UNRESOLVED_MISSING_DOCUMENT | Two local readings conflict (below). The deciding statement is Leroy 2008 Appendix E and its printed Table 7 example, which is not local. |
| UR-4 / D1: HI column note | RESOLVED_DOCUMENTARY | The HI Note-3 attachment is column-level. No NGC 3198 HI row carries the marker, so no query gets an HI upper-limit attachment under either reading. |
| UR-4 / U10: e_Sigma* = 0.0 (rows 16, 18, 19, 20) | PARTIAL | This is an explicit literal that is present, not an absence. It is neither a documented zero error nor the Note-3 marker. Its meaning beyond "rms uncertainty at F5.1" is not stated. |
| UR-4 / U11: blank H2 (rows 10–22) | PARTIAL | Blank is a CDS null ("?" on SigmaH2 and e_SigmaH2). No H2 limit marker is defined. Whether the printed paper gives limits there is not local. |
| UR-5 / U14: commented .sfb rows, kill, error | UNRESOLVED_MISSING_DOCUMENT | No local document read defines them. A local SPARC paper PDF exists but is outside the 0341/0346 set and was not read. |
| UR-5 / U15: S3/S4 observed support | PARTIAL | Structure is confirmed. By counting alone, at least 9 of the 11 outer .dens rows have no .sfb row of any kind, whatever is decided for the commented rows. |

## UR-4: Leroy table7 error and flag literals

### Primary source statements
Source: `leroy2008_ReadMe.html`, sha `cbd9a431…`, 0346 line method. All four local copies of this ReadMe are byte-identical.
- Line 171: SigmaHI "? Surface density of H I (2)". It is nullable.
- Line 172: e_SigmaHI F3.1 "rms uncertainty in SigmaHI (3)".
- Line 173: SigmaH2 "?". Line 174: e_SigmaH2 "? RMS uncertainty in SigmaH2". Both are nullable, and e_SigmaH2 has no Note 3.
- Line 175: Sigma* "Surface density of stars". It has no "?", so it is never blank.
- Line 176: e_Sigma* F5.1 "rms uncertainty in Sigma* (3)".
- Line 186: "Note (3): 1.0 = upper limit."
- Line 196: the ReadMe follows the CDS Standard Description. The meaning of "?" comes from that cited standard, which is not pinned locally.

### The stars row-2 conflict (not adjudicated)
Two readings of stars row 2 conflict:

- **(a) Literal CDS reading.** Every 1.0 in e_Sigma* is the marker. This is how the stored labels read the row:
  - P53 label `UPPER_LIMIT_NOTE3`;
  - bundle `upper_limit_marker` true and `value_missing` false;
  - raw table7 line 322;
  - contract V006 line 58.
- **(b) Secondary note.** `GALAXY_INPUT_READINESS.md` (`6e23d981…`), lines 170–179, digits masked in the record:
  - It reports the paper's printed Appendix E example, which shows populated values with RMS 1.0.
  - It states that NGC 3198's populated stellar row with RMS 1.0 "is not a limit flag".
  - It states that HI limits are a blank density with 1.0 in the error slot.

A schema fact applies to both readings: only SigmaHI is nullable. The blank-density encoding in (b) therefore cannot occur for stars, and the ReadMe gives no other stellar-limit encoding.

The P53 freeze already records `SEMANTIC_CONFLICT_PENDING_DISTINCT_REVIEW` with `Gaussian_likelihood` null. **Missing:** Leroy et al. 2008, AJ 136, 2782 (arXiv:0810.2556), Appendix E and the printed Table 7. A name-only search of the 0341 paths finds no copy.

### e = 0.0 (U10)
- **Documentary facts.**
  - The column holds a documented rms quantity.
  - It has no null flag.
  - Note (3) defines only 1.0.
- **Format fact.** F5.1 prints one decimal, so 0.0 is what any rms that was rounded or truncated below 0.1 would show.
- **Not established.** Rounding, an exact zero, and "not computed" are all undocumented. The ledger's "rounding is a hypothesis" stands.

## UR-5: .sfb commented rows and S3/S4 support

### Observed structure of the NGC 3198 .sfb file
File sha `ae071272…`. Only structure and equality checks were read; no data literal was read out.
- Line 1 is the uncommented header `radius mu kill error`.
- Lines 2–67 hold 66 four-token rows.
- Lines 68–69 hold two `#`-prefixed four-token rows. The `#` is attached to the radius, they follow the last uncommented row, and their radius texts are `#352.17` and `#387.39`.
- kill is `1` on both commented rows.

### What the local documentation says
- **SPARC index** (`ee7e3eab…`):
  - line 55: "on sky values in mag/arcsec^2 with no corrections for disk inclination or extinction";
  - line 56: "some exponential profiles are extrapolated at large radii" (generic);
  - line 64: Archangel (Schombert 2007).
  - The page never mentions kill, comments, `.sfb` or `#`.
- **The zips** contain no documentation member.
- **The SPARC CDS ReadMe** has no `.sfb` description.

### Observed pattern across the distributor zip (not a meaning)
- 3 of 219 .sfb files have commented rows, 5 rows in all, every one data-shaped.
- They come after the last uncommented row only in NGC 3198. In the other two files they are interleaved, so the format alone does not support a universal "outer truncation" reading.

### Missing documents
- The SPARC master paper (Lelli, McGaugh & Schombert 2016). It is present locally but unread:
  - path: `joint_parent_continuation/sparc_lelli_mcgaugh_schombert_2016_AJv152n157_v001.pdf`;
  - sha `87fa3959…`;
  - sidecar `astroweb.case.edu/ssm/papers/AJv152n157.pdf`, retrieved 2026-10-06.
- The Archangel documentation, which is not local.

### Counting bound on S3/S4 support (no conversion)
- The .dens file has a commented header `# Rad[kpc] SBdisk[Lsun/pc^2] SBbulge[Lsun/pc^2]` and 77 rows.
- Per 0341, 66 of those rows match the uncommented .sfb radii.
- The 2 commented rows can match at most 2 of the remaining 11, so at least 9 have no .sfb row.
- Which of Q32–Q43 are affected still needs the C4-bound arcsec-to-kpc conversion, which was not done. N3 stands.

## Qualifications of earlier wording (prior files not edited)
- **Q1.** Crosswalk `e_SigmaHI` reads "F5.1". The ReadMe says F3.1 (bytes 26–28); F5.1 is e_Sigma*.
- **Q2.** The ledger U14 absence claim covered `joint_parent_continuation/`, which holds the unread SPARC paper PDF. It should read "not documented in the local documents read".
- **Q3.** U9 "Appendix E not local" is confirmed. The secondary note and the P53 freeze conflict status should be read alongside it, and QUARANTINED stands.

## Still open, physically
- Stars row 2: is it a measurement or a limit?
- The size of the stellar rms on rows 16, 18, 19 and 20.
- H2 on rows 10–22: absent, with no zero and no bound.
- Whether the commented .sfb rows count as observed support, and which queries that affects.
- Whether the outer .dens rows are extrapolated or observed.
- **Named choices not made:**
  - the OPEN-9 mapping;
  - the UR-5 support choice;
  - the C4 conversion.

## Exposure incidents (disclosed; values not reproduced)
- **E1.** A keyword search displayed `GALAXY_INPUT_READINESS.md` lines 172–174 unmasked. They contain one NGC 3198 stellar density literal with its rms at the row-2 radius, plus literals from the NGC 628 example.
- **E2.** During discovery, a census of the distributor zips printed:
  - one data row of a non-target .sfb file that has no header line;
  - the first-line header comments, with luminosity and distance, of two non-target .dens files.

  No galaxy name was printed. The delivered probe emits counts only.

## Reads
- The task file.
- The 0352 notes, check record, manifest and JSON.
- The 0341 crosswalk, ledger, scope and correction 0346.
- The root review `60551a33…`.
- The Leroy ReadMe, read in full, plus hashes of its copies and the recovery custody record.
- The readiness note: keyword lines, then cited lines with digits masked.
- The P53 freeze: keys, plus the choices with digits masked.
- Bundle contract V006 lines.
- The SPARC index page, with digits masked on velocity lines.
- The .sfb and .dens files: structure and headers only.
- The zip sidecars, member metadata and a header/comment census.
- The SPARC CDS ReadMe, for absence booleans only.
- The SPARC paper PDF, hash only.
- A name-only `find` over the 0341 scope paths, with forbidden names filtered out.

**Not read:**
- table7, table4 or table2 data rows;
- the P53 parsed-input REVIEW.json;
- velocity, rotmod and MassModels files, or any file with a forbidden name;
- S2 products.
