# DDO154 local source inventory and minimal reuse manifest

2026-10-14. response_packet_audit. Filename-first read-only inventory, then source-only provenance/header/extraction summaries. No downloads, fits, scientific execution, FITS pixels, DDO response arrays or NGC3198 velocity values read. ZIP central directories were inspected without extracting any member. New documentary inventory only.

**Conclusion:** substantial DDO154 source material already exists locally. No reacquisition of its basic moment-zero maps is needed for a conditional source/geometry pilot. These files do NOT yet provide the new joint distance/geometry/error contract or a complete physical calibration. NGC3741 has local SPARC photometry/rotation bundle members but no identified local original HI map/cube or independently admitted distance likelihood in the inspected scope.

## Exact local paths

Archive base J=/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation

DDO directory D=/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/external_ddo154_v001

| Product path | Type and provenance | Current use |
|---|---|---|
| D/DDO154_NA_MOM0_THINGS.FITS | 4,242,240-byte original THINGS natural moment-zero image; documented SHA49d84c9f3e9efa826ecf3c03fdba7bac4e22b627f3e5f704efe703b389031a7c | Existing primary ordinary-HI source image; pixels not read now |
| D/DDO154_RO_MOM0_THINGS.FITS | 4,242,240-byte original THINGS robust moment-zero image; documented SHAf35b204c9abb3c1c28f210b51fe7e49ea38cfa70d48a15ff79968e68feb8d1e2 | Correlated imaging control, not independent likelihood |
| D/SOURCE_RESULTS.json | Existing source-only annular/half-disk extraction and retained-flux ledger, documented SHA32921f5e4834a06e3fd7901371f9046dd0746c9343c050b46b1ffde6dbfffdcf | Candidate reusable ordinary-source profile; array not opened now |
| D/SOURCE_FROZEN.json; SOURCE_EXTRACTION_PROTOCOL.md; SOURCE_EXTRACTION_RESULT.md; SOURCE_REVIEW_DATA.json | Original extraction settings, input pins and saved arithmetic qualification | Read now; scopes below remain binding |
| D/SOURCE_HEADER_AND_RETRIEVAL.md; INDEPENDENT_HEADER_REVIEW.md | Exact release/WCS/beam/units/mask provenance | Read now; documented raw-byte hashes are not claimed freshly rechecked |
| D/things2008_table1.dat; things2008_refs.dat; things2008_ReadMe.html | THINGS original catalogue/schema/reference codes | Existing geometry/distance conventions, not a distance likelihood; tables not opened now |
| D/leroy2008_table2.dat; J/leroy2008_table4.dat; J/leroy2008_table7.dat; J/leroy2008_ReadMe.html | Original Leroy tables/schema; extraction protocol references seven stellar rings | Existing stellar-source route; array rows not opened or adopted now |
| D/SPARC_Lelli2016c.mrt; D/SPARC_MassModels_Lelli2016c.mrt; D/SPARC_ReadMe.html | Existing catalogue/mass-model copies | Not treated as new independent source/state measurements; numerical contents not opened |
| J/sparc_official_Rotmod_LTG_2026-10-06_v001.zip :: DDO154_rotmod.dat (622 bytes), NGC3741_rotmod.dat (993 bytes) | Central-directory member presence verified; SOURCE.json gives official SPARC retrieval | Calibration-response products already local; contents NOT read |
| J/sparc_official_sfb_LTG_2026-10-06_v001.zip :: DDO154.sfb, NGC3741.sfb (1235 bytes each) | Original SPARC surface-brightness bundle, official-source receipt | Candidate photometric profiles; inspect schema/distance/geometry dependencies before future use |
| J/sparc_official_BulgeDiskDec_LTG_2026-10-06_v001.zip :: DDO154.dens (2059 bytes), NGC3741.dens (2729 bytes) | Original decomposition bundle, official-source receipt | Derived photometric product, not automatically independent physical density |

All three ZIP acquisition receipts were read. They identify https://astroweb.case.edu/SPARC/Rotmod_LTG.zip, /sfb_LTG.zip and /BulgeDiskDec_LTG.zip, retrieved2026-10-06. No network request was made and no bundle member, including NGC3198, was extracted/read.

## Critical provenance corrections and existing error custody

The existing HI files are the original THINGS release from the URLs already recorded in SOURCE_HEADER_AND_RETRIEVAL.md:

- https://things.www3.mpia.de/Data_files/DDO154_NA_MOM0_THINGS.FITS
- https://things.www3.mpia.de/Data_files/DDO154_RO_MOM0_THINGS.FITS

They are NOT the LITTLE THINGS filenames in the newly inspected directory. The old retrieval record reports404 responses for those alternative products. Thus the newer metadata listing must not overwrite the actual retained release or mask recipe. Existing data are sufficient to avoid repeating that retrieval attempt.

The local header review owns JY/B*M/S integrated units (divide by1000 once), beam sizes in HISTORY, already applied primary-beam correction and blank replacement byzero. Neither zeros nor spatial scatter provide a physical missing-flux/noise covariance. Natural and robust maps remain correlated.

The historical extraction fixes D=4.3Mpc, inclination66degrees and PA230degrees, with catalogue reference codes K04 and dB08. These numbers were encountered in the provenance records only and are NOT newly adopted. This distance lineage is not the proposed Jacobs/TRGB posterior; reconcile them rather than label the old fixed value the new independent likelihood. The fixed orientation was not a joint geometry/read inference. The source extraction has40-arcsec bins and an aperture-limited retained-emission contrast, not a physical zero exterior. Its stellar M/L convention, outer extrapolation and explicitly omitted H2 remain assumptions, not current physical measurements.

The saved source result reports114 numerical extraction checks and the source review records independent arithmetic comparisons. This qualifies the historical extraction under its frozen assumptions; it does not bound opacity, missing flux, molecular content, warp/thickness, geometry/distance covariance or stellar-population error. No filename explicitly identifying a DDO154 TRGB likelihood, full geometry/read covariance, original cube or velocity moment product was found in D. This is a bounded filename/provenance conclusion, not proof that no such information is embedded elsewhere.

## Prior exposure must be stronger than incidental snippets

The same local directory contains ROTATION_COMPARISON_REVIEW_DATA.json, ROTATION_COMPARISON_RESULTS_REVIEW.md, compare_rotation.py and DDO154_FIXED_SOURCE_ROTATION.png, plus historical field outputs. Their contents were NOT opened. Their presence establishes an existing comparison-work lineage requiring reconciliation in the exposure ledger; it is unsafe to describe prior exposure as only the recent web snippets. It does not establish the scientific correctness of those comparisons or make their fitted parameters/states measurements. DDO154 can still serve an explicitly allocated calibration role; it cannot become a fresh blind validation object.

## Minimal next reuse/acquisition manifest

1. **Reuse now, after present contract adoption:** qualify the existing NA/RO moment-zero maps and source-profile extraction provenance against the current source-only interface. Reuse the photometric tables/profile candidates after isolating their ordinary-light/conversion columns and dependencies. A pilot may assess geometry/source sensitivity using declared conditional geometry ranges; it cannot call the historical fixed geometry an empirical uncertainty region.
2. **Essential before quantitative physical calibration:** obtain or identify the object-level independent distance/error product; own the source-mask/flux/conversion uncertainty and joint geometry/read uncertainty. The already inspected https://arxiv.org/abs/0902.3675 supplies only the TRGB method route, not an identified ready posterior. The already inspected NRAO DDO154 page and THINGS lineage identify product routes, but no new numerical likelihood URL is invented here. First audit local source schemas/metadata and the local SPARC photometry members; do not redownload their bundles.
3. **Response ingestion can wait for role/read admission:** DDO154_rotmod.dat is already local. Inspect its schema and original estimator/support/geometry dependencies before opening its response values under a prospective calibration manifest. It is not automatically a joint likelihood, and Newtonian component columns cannot be inserted as this action's observation equation.
4. **Cubes/moment1/2 can wait:** the existing official listing https://things.cv.nrao.edu/littlethings/ddo154/HI/ names DDO154_NA_ICL001.FITS / DDO154_R_ICL001.FITS and XMOM1/XMOM2 products. Acquire only if the admitted published read cannot provide required geometry/pressure/covariance, and requalify the actual release first. Do not launch a full-cube reduction by default.
5. **NGC3741 stays reserve:** its local .sfb/.dens and rotmod members avoid reacquiring those particular products, but the original GMRT source and independent distance/joint geometry interface remain unlocated. No verified new object-level cube URL is invented. Do not expand the pilot merely because the rotation table is local.

Therefore existing source-only inputs are enough for a CONDITIONAL retained-source geometry pilot, independently of reading response arrays. They are not enough for an observation-qualified source envelope or coefficient inference until distance/geometry/conversion/exterior errors are supplied. The smallest progress is reuse of the existing source bytes with a new explicit uncertainty/admission manifest, not another generic source search or replay of historical force fits.

Inventory scope: program-worktree filenames (including ignored files), the existing continuous/mechanism dark-sector archives, the identified external_ddo154_v001 directory and three official local ZIP central directories. Broad intermediate filename listings were large; conclusions rely on the subsequent targeted complete directory/member lists. No claim of whole-machine absence is made.
