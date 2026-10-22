# 0395 checker note: CB89 and Be91 methods notes (separate source checker)

**Notes under review.** Both hashes were verified from the bytes:
- `CB89_METHODS_0395_V001.md`, `af4c12dd80629d80ab5c8a9f0f4d79ad16c4db6136e1c497db9b506f2ee0fc6b`;
- `BE91_METHODS_0395_V001.md`, `5b7b60025c860d9a601a1dbe716de6f955d9c71753b2321e9e187f50caa47fca`. This file was mode rw-r--r-- when checked, whereas the CB89 note is read-only.

**Sources.** Both hashes were verified:
- `CB89.pdf`, `a2a8d44413612b9ef5d5b55dd37c2e48b042a480fa0a66daa8b475f01fd0c0ee`;
- `Be91.pdf`, `079adcac7a0ca031ab6171e82bd9bc5d9ab557349846df1c484c7fafa31598ed`.

**Method.** Each OCR text layer was decoded in memory with poppler `pdftotext`. Quotes were matched with whitespace and hyphens ignored, and section membership was taken from heading order in the text layer. Only booleans, positions and digit-masked excerpts were printed. One narrow crop was rendered (see Be91 C1). Nothing from the PDFs was executed.

**Verdict: CONFIRMED_WITH_CORRECTIONS.** Every substantive claim in both notes checks out against the text. The corrections concern one evidence basis and three minor locator or wording points. No claim is wrong in substance.

## CB89 note: confirmed
- **Page map.** PDF p.7 is ApJ 764, p.9 is 765 and p.10 is 766, matching the running heads.
- **§IV(b) "H i Kinematics" (PDF p.7)**, all after the heading:
  - "A Gaussian profile fitting technique was also used…";
  - "essentially similar results";
  - "For the rest of the analysis, the results from the moment analysis will be used.";
  - "To derive the rotation curve, the 45" resolution data were used.";
  - the 30" annuli with the least-squares solution for "the five kinematical parameters". These are listed as the centre [x0, y0], Vsys, i and the position angle, and the phrase "best represent the velocity field at each radius" is on p.9;
  - the method references Carignan, Sancisi & van Albada (1988) and van Albada et al. (1985).
- **Two-step i/PA procedure (PDF p.9, ApJ 765):**
  - i and PA are first fixed "(using the optical values)" while the centre and Vsys are found;
  - "Then, keeping those parameters fixed, we let i and [θ] vary at all radii";
  - a warp is "clearly seen through variations of i and [θ]";
  - inner values are "very close to the ones found for the last optical isophote";
  - beyond that, "the galaxy becomes more face-on";
  - the last-point sentence is present. The OCR inserts a stray token between "not" and "enough".
- **Separate sides (p.9):** "along with separate solutions for the approaching and receding sides" and "the global rotation curve is a good representation of both sides of the galaxy."
- **Beam (PDF p.2, §II(b) "Radio", before §III):**
  - "the D-configuration was used";
  - a 33.5" × 35.3" synthesized beam with "uniform weighting; no taper";
  - 10" × 10" pixels;
  - "restored with a circular Gaussian beam of 45"";
  - a 60" resolution cube;
  - the continuum built from the line-free first and last channels;
  - the November run not used.
- **Asymmetric drift (p.9):** "Corrections for the asymmetric drift have been calculated and found negligible at all radii."
  - It is the last sentence of §IV(b); "c) Rotation Curve Analysis" follows immediately.
  - "asymmetric" occurs only on p.9, and "dispersion" only on pp.11–12, which is §V (the "V. MASS…" heading is on p.11).
  - So no method, dispersion, magnitude or bound is given. The NOT FOUND label is justified.
- **Distance (PDF p.7, §III(c) "Adopted Distance"):**
  - "we favor a distance of 4 Mpc over 10 Mpc (Krumm and Burstein 1984) as would be obtained using the Tully-Fisher relation";
  - the basis is the brightest blue stars and the association with the CVn I cloud;
  - "even the small distance is probably an upper limit".
- **Errors:**
  - The §IV(a) missing-flux sentence is confirmed.
  - The p.9 mean SW–NE difference, largest difference and comparison with the CF88 Gaussian curve are present (values masked).
  - "error" and "uncertainty" occur in the prose of neither p.7 nor p.9. "error" appears only on p.10 (the table) and p.12 (§V), so per-point error construction is NOT FOUND, as stated.
- **Labels:** the INFERRED items (per-annulus deprojection by the fitted i(R); 30" rings inside a 45" beam, so the points are correlated; drift not applied) are labelled as inferences.
- **Scope:** no SPARC mapping, correction, bound or range is chosen.

## CB89 note: correction
- **CB1 (locator, minor).** The exposure list says §IV(c) starts on PDF p.10. The text layer puts "c) Rotation Curve Analysis" on PDF p.9 (ApJ 765), directly after the drift sentence. The body claims are unaffected.

## Be91 note: confirmed (paraphrases checked against the text)
- **§2 "Sample selection" (PDF p.3):**
  - (ii) the observations come from Westerbork or the VLA, for resolution and sensitivity;
  - (iv) the gas-extent ratio between the two sides is less than 1.2;
  - (v) the inclinations are greater than 50° and less than 80°, with the warp and azimuthal-uncertainty rationale as paraphrased;
  - (v) also requires the two sides to agree "to within 10 per cent". The note splits criterion (v) across two bullets, which is correct;
  - (vi) the entire two-dimensional velocity field is used;
  - (vii) the quote "The gas pressure gradient term is negligible compared to the centrifugal term" is verbatim.
- **Sample composition:** six of the galaxies come from Begeman (1987), and "To these six galaxies four more are added from other sources."
- **The ring re-derivation:**
  - The sentence "In all cases … fitting concentric rings where the inclination, line-of-nodes, and circular velocity … is allowed to vary" sits in the six-galaxy paragraph, before the four additions are introduced.
  - The note labels its scoping as INFERRED, which is the right label. "In all cases" is lexically ambiguous, but placement supports the reading.
  - Criterion (vi) still requires a full 2-D field for every galaxy.
- **Two NGC galaxies with large i/PA variation:** confirmed.
- **Table 1 notes:**
  - Note 1 defines code 4 as "distance to CVn I group" and code 2 as the Hubble distance with H0 = 75.
  - Note 4 defines code 4 as Carignan & Beaulieu (1989).
  - The DDO 154 row has distance code 4 and photometry code 4.
  - DDO 154 has a single inclination entry; several NGC rows give a range.
- **p.4:** DDO 154 is described as a dwarf with a well-determined, regular VLA velocity field from Carignan & Freeman (1988). The fit-setup paragraph mentions M/L and helium.
- **Absences:** "drift", "resampl", "rebin", "interpol", "beam", "smear" and "sparc" occur 0 times; "pressure" occurs once, in (vii); "averag" occurs once, on p.7.
- **Labels and scope:** the INFERRED and NOT FOUND labels are justified. No SPARC mapping, correction or bound is established or chosen.

## Be91 note: corrections
- **C1 (evidence basis).** The claim "code 4 for both photometry and the 21-cm rotation curve" is correct, but the rotation-curve half cannot come from the text layer.
  - The OCR layer carries only one code column, at x ≈ 421–437 pt under "photo-". Its values (5,7 / 5 / 7 / … / 3,5 / 4) are the photometry references.
  - The rot.-curve column is absent from the text layer.
  - I verified it from a single 300-dpi crop of that column alone (pdftoppm, PDF p.3, x ≈ 440–482 pt), which excludes every data column. It reads 1,1,1,1,1,1,2,3,4,6, so DDO 154 = 4 (CB89).
  - The note says no page was rendered, so it should state how the rotation-curve code was obtained, or cite this check.
- **C2 (minor).** "averag … in the excluded Results section": the paper has no section of that name. PDF p.7 lies in the excluded fit/MOND part (§3 "DARK HALOES AND MOND" begins on p.4; §2 "SAMPLE SELECTION" is on p.3).
- **C3 (qualification).** Be91 p.4 attributes DDO 154's VLA velocity field to Carignan & Freeman (1988), while Table 1 cites CB89 for the curve.
  - CB89 describes its own new D-configuration VLA observations (§II(b)) and only compares its curve with CF88's Gaussian-analysis curve (p.765).
  - So "CF88 is cited for the underlying VLA observations" accurately reports what Be91 says, but should not be read as CB89's data being CF88's.

## Exposure
- **Authors' disclosures:** adequate. CB89's render of PDF p.7 is disclosed with its content classes. Be91's text-layer-only displays are disclosed, apart from the evidence-basis gap in C1.
- **Mine:**
  - **CB89** (digits masked throughout):
    - §II(b) channel and continuum text (p.2);
    - the §III(c) distance passage, including masked group-velocity ranges (p.7);
    - the five-parameter phrase;
    - the drift, mean-difference and last-point contexts (p.9).
    - A "last point" keyword search displayed, digits masked, a fragment of the p.10 rotation-curve table (the Vrot and Error rows) and two §IV(c) sentences. No digit was visible. This was unintended.
  - **Be91:**
    - §2 prose, digits masked;
    - the Table 1 layout with every decimal and multi-digit number masked (morphological types, DDO names and single-digit codes visible);
    - the Table 1 notes with codes and years visible;
    - masked contexts of every "Carignan"/"Beaulieu" mention, including qualitative MOND/addendum sentences on pp.13–14;
    - section headings.
  - **Crop render:** one crop of the Be91 rot.-curve code column (header plus ten single-digit codes).
- No velocity, curve, fit or table value was seen. No network was used, and nothing was written under Universal Network Theory.
