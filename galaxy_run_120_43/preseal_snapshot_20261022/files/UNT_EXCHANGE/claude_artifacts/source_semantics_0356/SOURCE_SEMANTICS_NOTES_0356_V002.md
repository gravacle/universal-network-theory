# 0356 source semantics V002: notes (CLAUDE2 helper 0356-A)

V002 replaces V001 for reading; the V001 files are kept unchanged. It is a documentary addendum for UR-4 and UR-5 of the 0352 join, metadata only.
- The machine-readable record is `SOURCE_SEMANTICS_ADDENDUM_0356_V002.json`.
- Every quoted source line there is checked against `PROBE_EVIDENCE_0356_V002.json`.
- No data value is reproduced: densities, errors, radii, distances, velocities and photometry are referenced by pointer.
- A literal scan in the builder fails if any decimal outside the allowed classes appears in any V002 file. The allowed classes are hashes, timestamps, format codes, arXiv ids, the band label 3.6-micron, the flag literals 1.0/0.0 and the F5.1 quantum statements 0.05/0.1.
- No interpolation, extrapolation, mask threshold, uncertainty distribution, galaxy state, response law, calibration, query-mapping rule or source choice is made.
- Root's 0352 review (`60551a33…`) and correction 0346 (`988e871a…`) are preserved:
  - N1, N2, N3, D2 and D3 are unchanged.
  - D1 is re-grounded on the primary ReadMe lines.

## Outcome

| Item | Status | Short answer |
|---|---|---|
| UR-4 / U9: column meaning of e = 1.0 | RESOLVED_DOCUMENTARY | CDS ReadMe Note (3) "1.0 = upper limit." It is attached to e_SigmaHI (line 172) and e_Sigma* (line 176) only. It does not say which quantity is limited, the bound, or the significance. |
| UR-4 / U9: stars row 2 (the only NGC 3198 occurrence; Sigma* populated) | UNRESOLVED_MISSING_DOCUMENT | Two local readings conflict (below). The deciding statement is Leroy 2008 Appendix E and its printed Table 7 example, which is not local. |
| UR-4 / D1: HI column note | RESOLVED_DOCUMENTARY | The HI Note-3 attachment is column-level. No NGC 3198 HI row carries the marker, so no query gets an HI upper-limit attachment under either reading. |
| UR-4 / U10: e_Sigma* = 0.0 (rows 16, 18, 19, 20) | PARTIAL | This is an explicit literal that is present, not an absence. It is neither a documented zero error nor the Note-3 marker. Its meaning beyond "rms uncertainty at F5.1" is not stated. |
| UR-4 / U11: blank H2 (rows 10–22) | PARTIAL | Blank is a CDS null ("?" on SigmaH2 and e_SigmaH2). No H2 limit marker is defined. Whether the printed paper gives limits for NGC 3198 is not local. |
| UR-5 / U14: commented .sfb rows, kill, error | UNRESOLVED_MISSING_DOCUMENT | No local document read defines them. A candidate SPARC paper PDF exists locally; its content is unverified (hashed only). |
| UR-5 / U15: S3/S4 observed support | PARTIAL | Structure is confirmed. By counting alone, at least 9 of the 11 outer .dens rows have no .sfb row of any kind, whatever is decided for the commented rows. |

## UR-4: Leroy table7 error and flag literals

### Primary source statements
Source: `leroy2008_ReadMe.html`, sha `cbd9a431…`, 0346 line method. All four local copies of this ReadMe are byte-identical.
- Line 186: "Note (3): 1.0 = upper limit."
- Note (3) is attached to e_SigmaHI (line 172, F3.1) and e_Sigma* (line 176, F5.1) only.
- The "?" null flag is carried by SigmaHI, SigmaH2, e_SigmaH2, FUV+24, FUV and 24. Sigma* and e_Sigma* carry no "?". The probe records this label by label.
- Line 196: the ReadMe follows the CDS Standard Description. The meaning of "?" comes from that cited standard, which is not pinned locally.

### The stars row-2 conflict (not adjudicated)
- **(a) Literal CDS reading.** Every 1.0 in e_Sigma* is the marker. This is how the stored labels read the row:
  - P53 label `UPPER_LIMIT_NOTE3`;
  - bundle `upper_limit_marker` true and `value_missing` false;
  - raw table7 line 322;
  - contract V006 line 58.
- **(b) Secondary note.** `GALAXY_INPUT_READINESS.md` (`6e23d981…`), lines 170–179, quoted with every digit masked:
  - It reports the paper's printed Appendix E example, which shows populated values with RMS 1.0.
  - It states that NGC 3198's populated stellar row with RMS 1.0 "is not a limit flag".
  - It states that HI limits are a blank density with 1.0 in the error slot.

A schema fact applies to both readings: Sigma* and e_Sigma* carry no "?". A stellar entry is therefore never blank, and the blank-density encoding in (b) cannot occur for stars. Note (3) on e_Sigma* is the stellar-limit encoding the ReadMe gives.

The P53 freeze records `SEMANTIC_CONFLICT_PENDING_DISTINCT_REVIEW` with `Gaussian_likelihood` null. **Missing:** Leroy et al. 2008, AJ 136, 2782 (arXiv:0810.2556), Appendix E and the printed Table 7. The probe's name-only search finds no copy.

### e = 0.0 (U10)
- **Documentary facts.**
  - The column holds a documented rms quantity.
  - It has no null flag.
  - Note (3) defines only 1.0.
- **Format hypothesis about the writer, not a source statement.** F5.1 prints one decimal. If the producer rounded, only values below 0.05 print as 0.0; if it truncated, values below 0.1 do. Which rule applies, if either, is undocumented.
- **Not established.** Rounding, truncation, an exact zero and "not computed" are all undocumented.

### Blank H2 (U11)
- Blank is a CDS null, and no H2 limit marker is defined.
- For its single NGC 628 example, the secondary note reports that printed H2 upper limits became blank/blank in the electronic file. It also states that galaxies without CO are blank/blank.
- Whether the same holds for NGC 3198 rows 10–22 is not stated locally.

## UR-5: .sfb commented rows and S3/S4 support

### Observed structure of the NGC 3198 .sfb file
File sha `ae071272…`. Only structure and equality checks were read; no data literal was read out.
- Line 1 is the uncommented header `radius mu kill error`.
- Lines 2–67 hold 66 four-token rows.
- Lines 68–69, the last two lines of the file, are `#`-prefixed four-token rows:
  - the `#` is attached to the first token;
  - their radius tokens equal the texts stored at crosswalk_0341 `/sources/S3_SPARC_SFB/radial_coordinate`;
  - kill is the flag literal one on both.

### What the local documentation says
- **SPARC index** (`ee7e3eab…`):
  - line 55: "on sky values in mag/arcsec^2 with no corrections for disk inclination or extinction";
  - line 56: the extrapolation statement, which is generic;
  - line 64: Archangel (Schombert 2007).
  - The page never mentions kill, comments, `.sfb` or `#`.
- **The zips** contain no documentation member.
- **The SPARC CDS ReadMe** has no `.sfb` description.

### Observed pattern across the distributor zip (not a meaning)
- 3 of 219 .sfb files have commented rows, 5 rows in all, every one data-shaped.
- They come after the last uncommented row only in NGC 3198. In the other two files they are interleaved.

### Missing documents
- **SPARC master paper.** Candidate, content unverified:
  - path: `joint_parent_continuation/sparc_lelli_mcgaugh_schombert_2016_AJv152n157_v001.pdf`;
  - sha `87fa3959…`;
  - sidecar sha `0413b819…`, pinned in the probe.
- **Archangel documentation.** Not local. The name search matches only the SPARC paper and its sidecar.

### Counting bound on S3/S4 support (no conversion)
- The .dens file has a commented header and 77 rows.
- Per crosswalk_0341 `/sources/S4_SPARC_DENS/radial_coordinate` (counts only), 66 of those rows match the uncommented .sfb radii.
- The 2 commented rows can match at most 2 of the remaining 11, so at least 9 have no .sfb row.
- Which of Q32–Q43 are affected needs the C4-bound conversion at the program reference distance, which was not done. N3 stands.

## Qualifications of earlier wording (prior files not edited)
- **Q1.** Crosswalk `e_SigmaHI` gives F5.1. The ReadMe says F3.1; F5.1 is e_Sigma*.
- **Q2.** The ledger U14 and crosswalk S3 statement "not documented locally" should read "not documented in the local documents read". The candidate PDF sits in a searched path and was never opened.
- **Q3.** U9 "Appendix E not local" is confirmed. Read it alongside the secondary note and the P53 freeze conflict status; QUARANTINED stands.
- **Q4.** Crosswalk e_Sigma* "not zero uncertainty" should read "meaning unspecified (neither a documented zero uncertainty nor an absence)". "No replacement" is unchanged.

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

## Exposure
- The V001 discovery incidents E1 and E2 are restated in the addendum. No values from them are reproduced.
- V002 work added no exposure.
