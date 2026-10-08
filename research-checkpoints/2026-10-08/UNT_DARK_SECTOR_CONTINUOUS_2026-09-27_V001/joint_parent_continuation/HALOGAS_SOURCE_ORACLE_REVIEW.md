# Independent retained-H I source and ring-reference audit

Accepted within the declared source-sensitivity scope. The two source
representations and their independent Newtonian force references pass. This
review recomputes saved-data arithmetic and verifies custody; it does not run
the field solver, ring quadrature, extraction, or a new scientific model.

## Source closure

All 86 members of `HALOGAS_FIELD_FROZEN.json` match their recorded hashes. The
canonical payload seals and freeze links of both new result packets also
match. `halogas_saved_results_audit.py` independently checks the extracted bin
identities, complete-prefix flags, Bernstein controls, polynomial primitives,
saved full/subinterval quadratures and mass ledger without importing numerical
worker modules. Its reproducible source-only snapshot is
`HALOGAS_SOURCE_ORACLE_REVIEW_DATA.json`.

The qualification contains 438 passing checks: 325 for the 51-bin 40-arcsec
representation, 110 for the 17-bin 120-arcsec representation, and three common
checks. Both have the same 136.4847475059566-kpc support and included signed
bare-H I mass, approximately 10,230,590,443.2167 solar masses. The common
excluded retained mass is 19,869,054.8002 solar masses (0.19383575% of the
whole retained map). The included negative-pixel contribution,
−3,245.03845 solar masses, remains included; it was not clipped.

Multiplication by 1.36 occurs exactly once: H I plus helium is
13,913,603,002.7748 solar masses. The stars and H2 plus helium remain exactly
the calibrated control's 19,798,896,050.1033 and 574,779,508.7155 solar masses.
The complete-aperture bins, all zero-retention intervals and the common
nonnegative endpoint construction match the frozen source. Independent
polynomial-integral arithmetic differs from saved full integrals by at most
3.31e−15 scaled units, and partial integrals by at most 8.50e−15.

This mass-conserving C0 interpolation is not a unique reconstruction, a
monotone interpolation, or new angular resolution. Completeness here refers
only to the conservative geometric aperture, not detection completeness or
association of every retained pixel with the galaxy. The exterior zero is a
declared contrast boundary, not an observation that gas is absent.

## Independent force reference

All ten cases (two sources at five fixed radii) and 170 checks pass. The audit
recomputes every reported gate from the saved 48/96-order values, source
masses and three heights; it checks component sums, nearest-knot height
selection, extrapolation signs, omitted mass and both tail bounds. It does
not treat matching hashes as mathematical validation.

The maximum reported order difference is 4.48332e−15 in the prescribed scaled
units; maximum component mass-closure error is 3.52581e−15. The largest
finite-height extrapolation change is 3.03512e−4 (0.0303512%), within the
unchanged 0.1% criterion. The maximum tail-force fraction is 1.63687e−18.
Signed component forces remain signed: for example the 40-arcsec H I
component pulls outward at the innermost reference radius, while the total
force is inward. Nothing is absolute-valued to repair that behavior.

These checks establish a numerically resolved reference for each exact
adopted source. They do not establish accuracy of the planar source as a
three-dimensional gas reconstruction, nor agreement with rotation data.
The PDE outcomes require their separate eight-case review; neither width
may be selected or discarded by its eventual residuals.

## Custody

| Artifact | SHA-256 |
|---|---|
| `HALOGAS_FIELD_FROZEN.json` | `81d01ef269d70f2699424b6576553c69944d92f51c169831c6d7a249584d694a` |
| `HALOGAS_FIELD_SOURCE_QUALIFICATION.json` | `28d10542bab8b8fb2b5c21e2de90adec03141c66e12de9cc888118c6e87d3736` |
| `HALOGAS_FIELD_ORACLE.json` | `0aa41b74b133248be8965eee8a4a66495b8f695c034c832c83255671979ee60e` |

No frozen file was edited. This is an explicitly post-execution audit.
