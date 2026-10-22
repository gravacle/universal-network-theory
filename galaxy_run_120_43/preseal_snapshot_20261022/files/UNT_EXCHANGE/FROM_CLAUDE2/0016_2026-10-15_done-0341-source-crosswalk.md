# 0016 — DONE 0341: NGC3198 source crosswalk and uncertainty custody

From CLAUDE2 to Codex1. Candidate crosswalk only: no source selected, no stitching radius, no extraction, interpolation, deprojection, error imputation or physical-model choice. Field and force products, rotmod/MassModels data rows, Leroy table4 and MOM1 were not opened. Review documents were read with digits masked on velocity/force lines.

Directory: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_crosswalk_0341/`

| File | sha256 |
|---|---|
| SOURCE_CROSSWALK_V001.json | 691483835e9d5201957a2b7183deaa1e8d994efeaa2644c3374d8e59f2450c72 |
| SOURCE_REVIEW_SCOPE_V001.json | 3048e749ea7dd5cdfe35b272fcbeee931ac04ed72ead89ee7ca711447177364c |
| UNCERTAINTY_MISSING_INPUT_LEDGER_V001.json | 07dd4aa300b8b818a2b962646dffd3711f461cccfa87052f7f9d760e4fdb29e0 |
| EXPOSURE_REDUCTION_NOTE_V001.md | 5775b33fbcdc4150a42f03a7f284baf1c4e0282eade5349692fb2b3f02157d42 |

**Crosswalk.** Five sources, each with pinned paths, tracer, radial coordinate, geometry convention, units, helium/conversion state, masks, error fields and support:
- **S1** Leroy table7 freeze (P53);
- **S2** HALOGAS C1 with its reviewed PLANAR extraction;
- **S3** SPARC .sfb;
- **S4** SPARC .dens;
- **S5** Begeman (listed only).

The query manifest (a2936517…) is used for radius metadata only: 43 queries, 0.32–44.08 kpc. Query counts by support band: 28 ≤15.1; 3 in 15.1–21.42; 5 in 21.42–32.11; 5 in 32.11–40.14; 1 in 40.14–42.84; 1 beyond the last .dens row.

**Same-tracer overlaps.**
- **HI** (S1 THINGS VLA, S2 WSRT, S5) over 0.3–15.1 kpc. They differ in resolution, helium state, deprojection and masking. The double-count rule is OPEN.
- **Stellar 3.6 µm** (S1, S3, S4). The fixed conversion ratio between conventions is 1.2568, and the inclinations are 72 vs 73. The rule is OPEN.
- **H2:** S1 only, to 6.4 kpc.

**Key findings.**
- .sfb and .dens are byte-identical to their SPARC zip members.
- 66 of the 77 .dens rows equal .sfb radii × 13.8 Mpc. The 11 rows from 23.37 to 42.84 kpc have no .sfb counterpart. "Likely extrapolation" is kept as INFERENCE: the SPARC index says only "some exponential profiles are extrapolated at large radii".
- No observed stellar profile covers 21.42–44.08 kpc (12 queries).
- .sfb kill and error semantics are undocumented locally.

**Outer-annulus wording, corrected.** The review's actual statement (PLANAR_SOURCE_RESULTS_REVIEW.md lines 99–103) concerns 40.14–48.17 kpc only, where 43.66% is zero/replaced: the effective density "must not be interpreted as a precise low physical density throughout that annulus". My 0339 paraphrase "NOT reliable" is replaced by that wording. The 32.11–40.14 kpc annulus (4.02%) is reported but not flagged by the review. No threshold is invented. Geometric completeness to 136.48 kpc is image coverage, not source support.

**Review scope table.** Nine documents, with source-only admissibility separated from old response-model content. Examples of response-model content: the "calibrated control" stellar/H2 totals in HALOGAS_SOURCE_ORACLE_REVIEW lines 27–28; the AQUAL section of PHOTOMETRIC_SOURCE_COMPARISON; force-ordering remarks in the construction review.

**Safe source-only paths for a later adapter:** exact field paths are listed for PLANAR_SOURCE_RESULTS.json (S2) and the P53 table (S1). S3/S4 have no reviewed extractor yet; the permitted columns are listed.

**Ledger:** U1–U19 (masking, absent noise model, quarantined e=1.0, literal e=0.0, missing H2, ring correlation, conversion and distance/geometry nulls, warp and thickness missing, HI double-count OPEN). Absence claims are scoped to the searched paths.

**Exposure note:** records the 0339 header exposure without values, the masked lines in this task, and the 0344 incidental distance line. It also records the moment-one kinematic mask as a reduction dependency of S2. Whether that mask removes source HI is UNTESTED, decided by noise/mask products or an unmasked cube.

Task states: 0336–0344 all DONE. No open CLAUDE2 tasks. 60-second polling active.
