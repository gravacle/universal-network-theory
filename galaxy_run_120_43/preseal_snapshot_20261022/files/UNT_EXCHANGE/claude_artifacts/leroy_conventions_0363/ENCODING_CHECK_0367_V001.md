# 0367 encoding check: printed Table E1 vs CDS table7, NGC 628 only (distinct source checker)

## Sources
- **Printed:** Leroy et al. 2008, arXiv:0810.2556v1, `UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/LEROY_2008_ARXIV_0810_2556V1_PRIMARY_SOURCE_V001.pdf`.
  - sha256 `b9537561b4dbc2d96bf953ddb80566154d6c0694e7be5bb7a0e8c375a58b69ca`, 3,549,376 bytes, 68 pages.
  - Table E1 is on p.44 and was read from the text layer only (`pdftotext -layout`); the page was not rendered.
  - Its columns are: Galaxy, r_gal (kpc), r_gal (r25), ΣHI, ΣH2, Σ*, FUV+24, FUV part, 24µm part. **It has no velocity field.**
- **Electronic:** `joint_parent_continuation/leroy2008_table7.dat`, sha256 `43165045c50d534ff7789dda05627328c23ba71c708ded9cf87cf0773fe02d99`.
  - This is the 0341 pin.
  - It was read through the CDS ReadMe `cbd9a431…` byte layout.
  - Only the 35 `NGC  628` records were parsed; every other record, NGC 3198 included, was skipped on its name field.
- **Pairing:** the 35 printed rings pair with the 35 CDS records in order. Both radius columns match at all 35 rings.
- **Method:** a one-off in-memory comparison in scratch; nothing was installed or added to the program. Only the encoding classes below were printed. No density, uncertainty or radius value was printed or is reproduced here.

## Per-ring class correspondence (NGC 628, 35 rings)
| Column | Printed form | CDS encoding | Rings |
|---|---|---|---|
| HI | ± 1.0 | value present (equal at print precision); e_SigmaHI = 1.0, equal to the printed σ | 2 (rings 15, 16) |
| HI | ± other | value present; e equals the printed σ | 33 |
| Stars | ± 1.0 | value present (equal); e_Sigma* = 1.0, equal to the printed σ | 1 (ring 3) |
| Stars | ± 0.0 | value present (equal); e_Sigma* = 0.0 | 2 (rings 30, 31) |
| Stars | ± other | value present; e equals the printed σ | 32 |
| H2 | ± | value present; e equals the printed σ | 17 (rings 1–17) |
| H2 | ≤ | SigmaH2 blank, e_SigmaH2 blank | 18 (rings 18–35) |
| FUV+24 | ± | value present; e equals the printed σ | 30 |
| FUV+24 | ≤ | FUV+24 blank, e_FUV+24 = 1.0; FUV and 24 also blank | 5 (rings 30, 31, 33, 34, 35) |

## Conclusions on the three points
1. **Printed ±1.0 (settled for NGC 628).**
   - At all 3 printed ±1.0 rings (HI rings 15 and 16, stars ring 3), the CDS keeps the populated value and writes e = 1.0. That is the same literal that ReadMe Note (3) (line 186) calls "upper limit".
   - So a populated e = 1.0 in e_SigmaHI or e_Sigma* can be an ordinary printed σ of 1.0. The literal alone does not identify a limit.
   - NGC 628 prints no HI or stellar limit, so the file gives no example of how such a limit would be encoded in those columns.
   - The only electronic limit form seen in NGC 628 is a blank value with e = 1.0, in e_FUV+24 (5 of 5 printed SFR limits). The ReadMe does not attach Note (3) to that column. Whether the note's attachment is incomplete is not established.
   - A blank-plus-1.0 form cannot occur for stars, because Sigma* carries no "?".
2. **Printed H2 "≤ value" (settled for NGC 628).**
   - All 18 such rings have SigmaH2 and e_SigmaH2 both blank.
   - The printed limit value is not carried, and there is no marker, so an electronic blank H2 looks the same as a no-data blank.
3. **Printed stellar ±0.0 (settled for NGC 628).**
   - Both such rings have e_Sigma* = 0.0 next to the populated value. The CDS 0.0 transcribes the printed 0.0.
   - The rounding rule is unstated, so 0.0 is not a known zero.

## Still unresolved for NGC 3198
NGC 3198 is not printed in v1, and its rows were not read here. The facts below come from the stored 0352 labels.
- **Stars row 2** (populated, e = 1.0):
  - Its electronic form is identical to NGC 628's ordinary printed ±1.0.
  - Under its actual column note (e_Sigma*, Note (3) "1.0 = upper limit"), it can also be read as a marker.
  - Neither reading is established. NGC 628 removes "e = 1.0, so it is a limit" as a valid inference, but it does not classify row 2.
- **Rows 16, 18, 19 and 20** (e = 0.0): same form as a printed ±0.0. This is a σ printed as 0.0 with an unstated rounding; it is not a known zero.
- **H2 rows 10–22** (blank/blank): same form as printed limits and as no data. Whether they were limits, and at what level, cannot be recovered from the electronic file.
- No likelihood was chosen, and no absent or rounded value was replaced.

## Source check of the 0363 answer (`a81477be…`)
**Verified against the text layer of the same PDF:**
- **Quotes on the stated pages:**
  - p.43: "Table E1 in the print edition…NGC 628, as an example", "the RMS scatter within the tilted ring", "Where there are no data, we take ΣHI = 0 and ΣH2 = 0", "observed but masked out because no signal was identified" and the Table 4 / Walter et al. (2008) phrase;
  - p.44: "It does not capture systematic uncertainties…tracer";
  - p.34: the helium factor and "at our working resolution and adopted conversion factor";
  - p.37: the M/L sentence;
  - p.7: "methodology in Appendix E".
- **Placement:**
  - "RADIAL PROFILES" is the unlettered heading on p.43, Table E1 is on p.44, and Appendix F starts on p.44.
  - Equations A1–A3 are on p.34 and C1 on p.37. TABLE 4 is on p.8.
  - "Upper limit" occurs only on pp.8, 9, 20 and 45.
  - BIMA SONG for NGC 3627 and NGC 5194 is on p.34. The 10″ rings, 60°, half resolution and THINGS centres are on p.43.
- **Counts:** 35 rings, H2 ≤ 18, SFR ≤ 5, one stellar ±1.0, two HI ±1.0, two stellar ±0.0. All are correct.
- **Hashes:** the PDF sha, bytes, 68 pages and the sidecar sha `4c4da91a…` all match.
- **DOI:** the DOI is in the sidecar, which was created 2026-10-15 13:15 local, after the 0361 check. The 0361 "DOI absent locally" was true when it was checked and is now superseded.

**Qualifications this check supplies:**
- 0363 §1: "not necessarily a marker" now has electronic support (NGC 628 stars ring 3).
- 0363 §1 "two encodings": the electronic 1.0 also carries ordinary σ. The observed electronic limit form is blank + 1.0, and only in e_FUV+24.
- 0363 §2: "printed limits became blanks" is now verified for H2, 18 of 18.
- The only differences in the quotes are typographic (en dash in "lowest–mass", "X CO" for XCO).

## Exposures
- **0363 answer:** viewed with every decimal masked except 1.0 and 0.0.
- **Leroy PDF:**
  - It was decoded in memory, and no page was rendered.
  - Printed: booleans, digit-masked contexts from pp.43–44, and the p.44 table structure with every digit masked (header, 35 rows, the table note and the start of Appendix F).
  - p.8 (Table 4, which holds the NGC 3198 velocity parameters) was tested only for the string "TABLE 4". Nothing from it was displayed.
- **CDS table7:** a census of galaxy names and record counts was displayed. Only the NGC 628 records were parsed, in memory, and only class labels and ring indices were printed.
- **Sidecar:** its key names and boolean string tests were displayed.
- No NGC 3198 value, target velocity, rotation field or table value was seen.
