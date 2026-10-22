# 0395: CB89 methods for DDO154 (CLAUDE2 helper, author; Be91 is covered by another helper)

## Source
- **File:** `/private/tmp/unt_primary_methods_0395/CB89.pdf`, sha256 `a2a8d44413612b9ef5d5b55dd37c2e48b042a480fa0a66daa8b475f01fd0c0ee` (verified from the bytes).
- **Paper:** Carignan & Beaulieu 1989, ApJ 347, 760–770, 1989ApJ...347..760C. The file is an ADS scan with an OCR text layer, 14 PDF pages.
- **Page map** (from the scan's page headers):

  | PDF page | Journal page |
  |---|---|
  | 1, 2 | 760, 761 |
  | 3, 4 | Plates 9, 10 |
  | 5, 6, 7 | 762, 763, 764 |
  | 8 | Plate 11 |
  | 9 → 14 | 765 → 770 |

- **How it was read.**
  - Rendered with the Read tool: PDF p.7 (ApJ p.764) only.
  - Other quotes come from the OCR text layer, decoded in memory and displayed digit-masked. The exception is the method-parameter phrases quoted below.
  - OCR renders the position-angle symbol as a digit; it is written [θ] below.
- **Labels:** DOCUMENTED / INFERRED / NOT FOUND.

## 1. What was fitted
- **DOCUMENTED.** The velocity field came from moment analysis; a Gaussian-profile velocity field gave "essentially similar results".
  - p.764 §IV(b): "For the rest of the analysis, the results from the moment analysis will be used."
  - p.764 §IV(b): "A Gaussian profile fitting technique was also used to derive the velocity field."
- **DOCUMENTED.** The rotation curve was fitted on 30″ tilted annuli. p.764 §IV(b): "After dividing the velocity data into 30" concentric annuli in the plane of the galaxy, a least-squares solution is found for the five kinematical parameters".
  - The five parameters are the centre (x0, y0), Vsys, i and [θ], chosen to "best represent the velocity field at each radius" (pp.764–765).
  - p.764: "The method is described in Carignan, Sancisi, and van Albada (1988), and van Albada et al. (1985)."
- **DOCUMENTED.** Approaching and receding sides were checked separately, and the global solution was adopted.
  - p.765 §IV(b): the final solution is shown "along with separate solutions for the approaching and receding sides".
  - p.765: "the global rotation curve is a good representation of both sides of the galaxy."
- **INFERRED.** The adopted curve is the global, both-sides moment-field tilted-ring rotation velocity. It is deprojected per annulus with the fitted i(R), and it is not a line-of-sight speed.

## 2. Inclination and PA conventions
- **DOCUMENTED.** Step 1, on the inner unwarped data: "keeping i and [θ] fixed (using the optical values), we looked for the rotation center and the systemic velocity" (p.765 §IV(b)).
- **DOCUMENTED.** Step 2 frees i and PA at every radius: "Then, keeping those parameters fixed, we let i and [θ] vary at all radii" (p.765). And: "any warp of the H i disk is clearly seen through variations of i and [θ] with radius" (p.765).
- **DOCUMENTED.** Inner i and PA are nearly constant and "very close to the ones found for the last optical isophote". Beyond the warp radius "the galaxy becomes more face-on" (p.765). The values are not transcribed.
- **DOCUMENTED.** The last point has no northeast-side geometry: "there is not enough H i on the northeast side to find a solution for the inclination and position angle at the last point" (p.765).
- **NOT FOUND.** No stated bound or prior on how far i and PA could vary. No uncertainty on i(R) or PA(R) was found in the prose.

## 3. Beam and annulus support
- **DOCUMENTED, p.761 §II(b):**
  - "the D-configuration was used";
  - Table 1 gives "FWHM of synthesized beam 33.5" x 35.3"" with "uniform weighting; no taper";
  - "gridded in 10" x 10" pixels".
- **DOCUMENTED, p.761:** the maps were "CLEANed separately and restored with a circular Gaussian beam of 45"". A "60" resolution" cube was also made.
- **DOCUMENTED, p.764 §IV(b):** "To derive the rotation curve, the 45" resolution data were used." The rings are 30″ annuli (§1).
- **INFERRED.**
  - The 30″ annuli are narrower than the 45″ beam, so adjacent points are not independent.
  - The radial support of each point is set by both the 45″ beam and the 30″ ring.
  - No per-point kernel or weights are stated.

## 4. Asymmetric drift / pressure
- **DOCUMENTED, p.765 §IV(b):** "Corrections for the asymmetric drift have been calculated and found negligible at all radii."
- **NOT FOUND.**
  - The paper gives no method, assumed velocity dispersion, magnitude, bound or uncertainty for this correction.
  - The only other "dispersion" in the paper is the halo-model parameter in §V, which belongs to a gravitational fit and is excluded.
- **INFERRED.** No asymmetric-drift correction is applied to the adopted curve. "Negligible" is a qualitative published statement, not a usable numerical bound. No correction or range is chosen here.

## 5. Distance convention
- **DOCUMENTED, p.764 §III(c):** "we favor a distance of 4 Mpc over 10 Mpc (Krumm and Burstein 1984) as would be obtained using the Tully-Fisher relation". The basis is the brightest blue stars plus association with the CVn I cloud. The paper adds that "even the small distance is probably an upper limit".
- **NOT FOUND.** No statement links this 4 Mpc convention to any later compilation's distance. CB89 predates SPARC and establishes no SPARC mapping.

## 6. Raw measurement and reduction assumptions (kept separate from fits)
- **DOCUMENTED.**
  - Continuum came from line-free end channels.
  - A second, lower-quality run was discarded (p.761): "We thus decided not to use the November … observation."
  - The VLA flux fell below single-dish values (p.764 §IV(a)): "we have been missing flux with our VLA observations". This bears on the HI mass, not directly on the kinematics.
- **DOCUMENTED, uncertainty statements (values not transcribed):** p.765 gives the mean southwest–northeast difference and the largest difference, plus the maximum difference from the Carignan & Freeman (1988) Gaussian-analysis curve.
- **NOT FOUND in the prose:** how per-point rotation-curve errors were computed. The adopted curve and its errors sit in a table referenced on p.765, which was not opened.
- **EXCLUDED:** §V "Mass Distribution" (two-component and isothermal-halo fits, pp.767–769). It was not read for content, and no result is reported.

## Missing for the 0394 mapping (M3)
CB89 documents the original estimator: moment field, 45″ data, 30″ annuli, free i(R) and PA(R), a 4 Mpc distance, and asymmetric drift negligible. It does **not** document:
- any later resampling or rescaling to the 12 SPARC rows;
- any error transfer;
- a numerical pressure bound.

## Pages rendered and exposures
- **Rendered:** PDF p.7 (ApJ p.764) only. It showed, without transcription:
  - DDO154's global-profile midpoint and systemic velocities and its HI flux and mass;
  - photometric distance-modulus numbers;
  - group velocities and distances;
  - two channel velocities marking the warp.
- **Text layer, digit-masked displays:**
  - PDF p.2 §II(b), including the Table 1 parameter lines;
  - PDF p.7 §III(c)–§IV(b);
  - the PDF p.8 Plate 11 caption (isovelocity figure);
  - the full PDF p.9 text, where Vsys, side differences and i/PA values appeared masked;
  - the first 500 characters of PDF p.10 (the Fig. 7 caption and the start of §IV(c));
  - masked fragments of the §V halo-fit text on PDF pp.11–12, from a dispersion keyword search.
- **Unmasked:** the method-parameter phrases quoted above (beam, pixels, resolutions, annuli, distance, method references) and the page-header tokens.
- **In memory only:** keyword counts were computed over all 14 pages, including table and figure pages.
- **Not done:**
  - No velocity array, rotation-curve table or figure, or fit result was transcribed.
  - The PDF was not copied into the program tree.
  - No network was used.
