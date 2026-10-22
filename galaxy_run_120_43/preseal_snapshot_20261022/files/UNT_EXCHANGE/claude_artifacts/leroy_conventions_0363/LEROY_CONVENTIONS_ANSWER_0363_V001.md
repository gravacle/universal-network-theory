# 0363 Leroy 2008 conventions: answer (CLAUDE2 helper 0363-A)

## Source
- **File:** `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/LEROY_2008_ARXIV_0810_2556V1_PRIMARY_SOURCE_V001.pdf`. Both values below were verified from the bytes.
  - sha256 `b9537561b4dbc2d96bf953ddb80566154d6c0694e7be5bb7a0e8c375a58b69ca`
  - 3,549,376 bytes
- **Sidecar:** `.pdf.SOURCE.json`, sha256 `4c4da91ab4db5f869978f308165294cbc3da128738888d7c8ed50d36b9c841be`.
- **Version:** arXiv 0810.2556v1 (68 pages). The journal version is AJ 136:2782–2845, DOI 10.1088/0004-6256/136/6/2782 (per root's record and the sidecar).
- **Table numbering.** In v1 the printed profile table is **Table E1**, "Table of Radial Profiles" (p.44); the journal and the CDS `table7.dat` call it Table 7. The appendix heading is "RADIAL PROFILES" (p.43) and carries no letter in v1. It is Appendix E by its Table E1, its Eq. (E1), and p.7's "methodology in Appendix E".
- **How it was read.**
  - Rendered with the Read tool: p.43 only (prose).
  - p.44 holds Table E1 plus the Appendix F start. It was **not rendered**; its title and note are quoted from the text layer.
  - The other pages were used through an in-memory text grep, digits masked.

## 1. Is a populated stellar e = 1.0 necessarily an upper-limit marker? **No**, but the NGC 3198 row is still undetermined.

**Printed primary convention** (p.44, Table E1; the non-target NGC 628 example, 35 rings). These are entry-form counts only; no value was printed.
- Limits are printed as "≤ value" with **no** ± uncertainty: H2 in 18 rings, ΣSFR in 5.
- Every one of the 35 stellar entries is printed "value ± uncertainty"; there is no stellar limit. **One** stellar entry and **two** HI entries print an uncertainty of exactly 1.0 next to a populated value.
- The printed table therefore shows 1.0 used as an ordinary numeric uncertainty.

What the printed uncertainty means:
- p.43, Appendix E: "Table E1 in the print edition shows the results for our lowest–mass spiral galaxy, NGC 628, as an example."
- p.43, Eq. (E1): the uncertainty σ is built from σ_RMS, "the RMS scatter within the tilted ring".

**CDS side.** ReadMe `cbd9a431…`, line 186 reads "Note (3): 1.0 = upper limit." It is attached to e_SigmaHI (line 172) and e_Sigma* (line 176) only.

**Reconciliation.** Neither side is preferred.
- The paper (v1) never states a "1.0 = upper limit" rule. "Upper limit" occurs only on pp.8, 9, 20 and 45 (SFR and plot conventions), not in Appendix E or the Table E1 note.
- Note (3) is therefore an electronic-table (CDS/AAS) encoding that the paper does not document.
- The two statements describe different encodings: the printed "≤" form, and the electronic 1.0 marker.
- Together they establish that a populated stellar 1.0 is **not necessarily** a marker.
- They do **not** establish which kind NGC 3198 stars row 2 is. NGC 3198 is not printed, and the paper gives no rule mapping "≤" entries to the electronic file.

**Status.** UR-4/U9/STARS_ROW2: UNRESOLVED_MISSING_DOCUMENT (0356 V002 and 0361) → **PARTIAL**.

**Next local check (root's call).** Compare the non-target NGC 628 rows of the local CDS `table7.dat` with the printed Table E1, at the three printed "± 1.0" rings and the H2 "≤" rings. This would show how the electronic file encodes each printed form.

UR-4/U9/COLUMN_NOTE3 and D1 (HI column note) are unchanged: RESOLVED_DOCUMENTARY, CDS-side.

## 2. What printed 0.0 and absent H2 establish

### Printed 0.0 (U10)
**Established:**
- Two printed NGC 628 stellar entries are "value ± 0.0". So 0.0 is a published uncertainty of a populated entry.
- It is neither a null nor a limit.

**Unspecified:**
- No rounding rule is stated, so whether the true σ is below the print precision or exactly zero is not established.
- Systematics are excluded. p.44, continuing the E1 text: "It does not capture systematic uncertainties, e.g., due to choice of X CO or star formation tracer".

**Status:** PARTIAL → **PARTIAL** (class established). 0.0 is not a known zero.

### Absent H2 (U11)
**Established:**
- p.43, Appendix E: "Where there are no data, we take ΣHI = 0 and ΣH2 = 0." These are regions "observed but masked out because no signal was identified", and they enter the ring averages as zeros.
- In print, H2 limits appear as "≤ value" with no uncertainty (18 of 35 NGC 628 rings).

**Unspecified:**
- How "≤" entries are encoded electronically. The CDS file has blanks; the secondary note's claim that printed limits became blanks is consistent with this but unverified here.
- The significance or level of a profile H2 limit. Only a map sensitivity "at our working resolution and adopted conversion factor" is stated (p.34).
- Whether NGC 3198 rows 10–22 are printed limits.

**Status:** PARTIAL → **PARTIAL**. Blank H2 is absent, not zero. The "= 0" rule applies to pixel averaging, not to blank table cells.

## 3. Reduction assumptions that stay attached to the source inputs (named only; none adopted)
1. **Ring averaging.** The mean is used for HI, H2 and SFR and the median for stars, in 10″ tilted rings spaced at half the working resolution, so adjacent rings are correlated. The rings use "the position angle and inclination in Table 4, adopted from Walter et al. (2008)" (p.43, App. E). The THINGS centres are used, and only data within 60° of the major axis.
2. **Zero substitution** for observed no-signal HI/H2 pixels; pixels without SFR are ignored (p.43).
3. **Uncertainty** is the scatter-based σ of Eq. (E1). It includes azimuthal structure and excludes systematics (pp.43–44).
4. **HI.** Inclination and helium are folded into Eq. (A1): it "includes a factor of 1.36 to reflect the presence of helium" (p.34, App. A).
5. **H2.**
   - A constant X_CO, a CO(2→1)/(1→0) line ratio and an inclination correction (Eqs. A2–A3, p.34).
   - X_CO is treated as unknown in low-mass, low-metallicity galaxies (p.34).
   - BIMA SONG replaces HERACLES only for NGC 3627 and NGC 5194 (p.34).
   - Signal masks are applied to the cubes (p.35).
6. **Stars.**
   - Median 3.6 μm rings, an empirical 3.6 μm→K scaling, a fixed K-band M/L, a Kroupa IMF and an inclination correction (Eq. C1, p.37).
   - "The major uncertainty in Equation C1 is the mass–to–light ratio" (p.37).

**Documentary consequence for correction 0346.** The primary-verification gaps C1–C3 can now cite Eq. A1, the X_CO and line-ratio sentences, and Eq. C1 of v1. The values recorded in 0346 agree with this text. C4 (geometry) stays open: Table 4 sits on p.8, which also holds the NGC 3198 row with velocity parameters, and was not read.

## Remaining ambiguities
- **Version.** This is v1. The journal's printed Table 7 and its notes could differ, and this was not checked.
- **Electronic encoding.** The paper does not document how printed "≤" entries become CDS fields: the HI/stellar 1.0 marker versus blanks.
- **NGC 3198 rows.** Stars row 2, the rows 16/18/19/20 at 0.0, and the H2 rows 10–22 cannot be classified from the paper. NGC 3198 is not printed.
- **Limit significance.** No significance is stated for printed profile limits.
- **Filename searches.** A bounded filename search cannot rule out a differently named copy of any document. Earlier "none exists" phrasing should be read as "none found by filename search".

## Binds and aliases (unchanged)
- **OPEN binds** stay as in 0356 V002:
  - stars row 2 → OPEN-8 and OPEN-9;
  - U10 → OPEN-8 and OPEN-9;
  - U11 → OPEN-4 and OPEN-9.
- **Aliases.** Under the 0361 review's note H2, which is binding, the 0361 U14 items map to 0356 V002 `SFB_COMMENTED_ROWS_AND_KILL` and the 0361 U15 item to `S3_S4_OBSERVED_SUPPORT`.
- The SPARC items are unaffected by 0363.

## Exposures
- **Text layer.** All 68 pages were decoded in memory, for keyword counts only.
- **Masked contexts.** Digit-masked keyword contexts were printed, with velocity contexts suppressed. They include p.8, the Table 4 page that holds the NGC 3198 row; no digit or velocity field was shown.
- **p.44 (non-target NGC 628 table).**
  - About 40 digit-masked row fragments were printed (structure only).
  - The masked header and note were printed.
  - The rows were parsed in memory into the counts above.
  - The table has no velocity fields.
- **p.43 render.** This showed the end of Appendix D (non-target ensemble ratios) and the mention "v_flat and l_flat from Table 4", with no values.
- **Unmasked text.** Galaxy names NGC 3627 and NGC 5194 were unmasked, and so were the conversion phrases from Eqs. A1–A3 and C1, which are documentation constants.
- No NGC 3198 value, target velocity or validation curve was viewed.

## Files
- **Delivered:** this file only, per the 0364 scope change.
- **Scratch only, kept and not delivered:**
  - `work0363/leroy_page_locator_0363_v001.py`
  - `work0363/locator_run1.json` (an empty first run)
  - `work0363/leroy_pdf_0363_v001.py`
