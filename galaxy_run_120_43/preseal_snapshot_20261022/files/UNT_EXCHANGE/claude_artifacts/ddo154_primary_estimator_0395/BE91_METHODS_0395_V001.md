# 0395 Be91 methods note V001: DDO154 data provenance in Begeman, Broeils & Sanders 1991 (CLAUDE2 helper, author)

**Source.** Begeman, Broeils & Sanders 1991, MNRAS 249, 523–537 (1991MNRAS.249..523B). Local read-only copy at /private/tmp/unt_primary_methods_0395/Be91.pdf, sha256 079adcac7a0ca031ab6171e82bd9bc5d9ab557349846df1c484c7fafa31598ed (verified). Page numbers p.N are PDF pages; the journal pages are 523 + (N−1).

**Scope.** Data provenance and reduction statements only. Be91's MOND and halo fits are excluded, and none of their content is reported.

**Quoting.** Statements are close paraphrases with locators. There is one verbatim quote, kept under 15 words, because the paper is copyrighted. A separate checker should compare each paraphrase against the PDF.

## 1. Origin of the DDO154 curve
- **DOCUMENTED (p.3, Table 1 and its Note 4).** The DDO154 row gives reference code 4 for both photometry and the 21-cm rotation curve. Note 4 decodes code 4 as Carignan & Beaulieu (1989).
- **DOCUMENTED (p.4, §2 "Sample selection").** Be91 describes DDO154 as a dwarf with a well-determined, regular velocity field observed with the VLA by Carignan & Freeman (1988).
- **DOCUMENTED (p.3, §2).** Six sample galaxies come from Begeman's (1987) sample. The remaining four, which include DDO154, are added from other sources.
- **INFERRED.** Be91 adopts the published CB89 curve; CF88 is cited for the underlying VLA observations.
  - Be91's statement that the curve was re-derived by fitting concentric rings to the full 2-D velocity field (p.3) sits in the paragraph about the six Begeman galaxies.
  - That statement is not made for DDO154.
- **NOT FOUND.** No statement that Be91 re-derived, rescaled, resampled, re-binned, interpolated or smoothed the DDO154 curve.
  - The text layer has no occurrence of "resampl", "rebin", "interpol", "beam", "smear" or "SPARC".
  - "averag" occurs once, in the excluded Results section.

## 2. Inclination, position angle and distance for DDO154
- **Distance, DOCUMENTED (p.3, Table 1 Note 1).** The DDO154 distance-method code is 4, which Note 1 defines as the distance to the CVn I group. It is not a Hubble-flow distance (code 2 assumes H0 = 75). The value is not transcribed.
  - This convention differs from the SPARC TRGB method code recorded in GEO (see 0394).
- **Inclination, DOCUMENTED (p.3, Table 1).** DDO154 has a single inclination entry; the value is not transcribed. Several NGC rows give an inclination range instead.
- **Inclination, DOCUMENTED (p.3, criterion (v)).** The sample is restricted to inclinations between 50° and 80°. The lower bound limits the effect of outer warps; the upper bound avoids an uncertain azimuthal gas distribution.
- **Inclination, NOT FOUND in Be91.** Whether the adopted CB89 curve used a radially varying i(R). That belongs to the CB89 author.
- **Position angle, NOT FOUND for DDO154.** The only PA and line-of-nodes statements (p.3) concern the six Begeman galaxies. Their rings have free inclination, line of nodes and circular velocity; two NGC galaxies show large systematic variation.

## 3. Beam and resolution; pressure and asymmetric drift
- **Resolution, DOCUMENTED (p.3, criterion (ii); generic).** Observations are required to come from Westerbork or the VLA interferometers, for resolution and sensitivity. DDO154 is a VLA object (p.4).
- **Resolution, NOT FOUND.** The DDO154 beam, ring or annulus width, and radial sampling. "beam" does not occur in the text.
- **Generic reduction criteria, DOCUMENTED (p.3).** These are selection criteria applied to every sample galaxy:
  - (iv) the gas-extent ratio between the two sides of the major axis must be below 1.2;
  - (v) the rotation velocities from opposite sides must agree within 10 per cent;
  - (vi) the full 2-D velocity field must be used.

  They are pass/fail thresholds, not per-point error models.
- **Pressure, DOCUMENTED (p.3, criterion (vii)).** Selection criterion (vii) reads "The gas pressure gradient term is negligible compared to the centrifugal term". Be91 gives no DDO154 computation, bound or correction behind this.
- **Asymmetric drift, NOT FOUND.** "drift" occurs 0 times, and "pressure" only once, in criterion (vii).
- **INFERRED.** Be91 applies no pressure or asymmetric-drift correction. Its negligibility is a selection assumption, not a measured bound usable as an uncertainty.

## 4. Does Be91 establish the SPARC 12-row mapping?
- **NOT FOUND.** Be91 predates SPARC and says nothing about how a later compilation derived its rows. That covers radii or sampling, rescaling between the CVn-group and TRGB distances, inclination rescaling, and error transfer.
- **INFERRED.** Be91 documents only one link in the chain: its DDO154 curve is CB89's, at a CVn I group distance. SPARC's reference pair "Be91, CB89" is consistent with Be91 being an intermediate compilation of the CB89 curve. Whether SPARC took its rows from Be91's tabulation or directly from CB89 is undocumented here.

## Raw measurement versus the later fits
- **Raw measurement and reduction assumptions** are criteria (i)–(viii) and the data sources: Table 1 Note 4, plus the CF88 VLA attribution.
- **Fit-model setup** (constant M/L per galaxy, gas included with a helium factor; p.4) belongs to the gravitational fits. It was displayed with digits masked and is not used here. No fit result was read.

## Pages and exposure
- **Text layer.** pdftotext found an OCR text layer on all 15 pages, decoded in memory.
- **Rendering.** No page image was rendered with the Read tool.
- **Not displayed:** keyword hit counts, heading lists (digits masked), and per-sentence topic flags, used for all pages.
- **Displayed:**
  - p.3–4: the §2 "Sample selection" text, digits masked. The selective unmasking covered only the criteria thresholds, the DDO identifiers, citation years, the Table 1 notes, and the DDO154/DDO170 distance-method and reference codes.
  - p.3: Table 1 with every numeric column masked, including the radius and acceleration of each galaxy's last measured point; only column formats were seen.
  - p.4: the fit-setup paragraph, digits masked.
  - p.2: two generic sentences, about Lake's irregulars and about higher-resolution observations.
  - p.14: one sentence mentioning DDO154 in an unclear, probably fit-related context. It contained no numbers and is not used.
- **Not displayed:** the DDO154 sentences on p.7, p.8 and p.13, which were flagged as fit/MOND content; the Results, Disc-halo and Addendum prose; and all figures.
- **Not seen:** no velocity, curve or fit numbers.
- **Limit.** The NOT FOUND results rely on OCR keyword searches and were not checked against rendered pages.
- No network was used, the PDF was not copied, and nothing was written under Universal Network Theory.
