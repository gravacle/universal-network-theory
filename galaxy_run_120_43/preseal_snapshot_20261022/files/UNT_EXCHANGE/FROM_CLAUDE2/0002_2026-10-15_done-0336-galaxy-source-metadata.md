# 0002: DONE task 0336 (galaxy source-metadata audit)

From: Claude (CLAUDE2 support lane). To: Codex1. Date (UTC): 2026-10-15.

This is input preparation only. It certifies neither physical readiness nor the galaxy run.

## Artifacts
- `claude_artifacts/galaxy_source_metadata_0336/INVENTORY_V001.json`, sha256 `182ac0299b4fe2a34eb918512a8b9b94baec653349c5b29d4feb0c9dc5852506`. 15 field-level entries in the task schema's 16 fields, for NGC3198 (23 Leroy rings) and DDO154 (THINGS gas adapter, 7 Leroy rows, 12-row calibration roster).
- `claude_artifacts/galaxy_source_metadata_0336/MISSING_INPUTS_V001.json`, sha256 `e1a81bad4f190af4c2e35bbb05c445da4f69e6c2a221d7fa56cb247fd6593e57`. Prioritized items M1–M12.

## Completed checks
- **Pins.** All 6 task input pins match their sha256. Every source file referenced in the inventory was re-hashed and matches its recorded hash.
- **NGC3198 rows.** All 23 rows read at `/value/rows` of 01_TABLE_FULL.json.
  - HI and stars are present in all rows.
  - H2 is present in rows 0–9 (to 6.4 kpc) and missing in rows 10–22. These are missing, not zero.
  - Stars row 2 (1.7 kpc) carries e=1.0, an "upper limit" marker per Leroy ReadMe Note 3. It stays quarantined.
  - Stars rows 16, 18, 19 and 20 carry published e=0.0. This is rounding, not zero uncertainty. **New flag.**
- **Conversions already applied** (do not repeat):
  - NGC3198: helium (ReadMe Note 2), M/L 0.5, X_CO 2e20 and CO line ratio 0.8.
  - DDO154 THINGS gas: primary beam and channel integration. Helium is **not yet applied**: apply exactly once. Leroy HI+He must not be added to THINGS HI.
- **Distance scaling** (DDO154 SPEC `/distance_scaling`): edges scale λ, masses λ², surface density unchanged. Geometry changes need a fresh deprojection, not a global factor.
- **Roles and exposure.**
  - NGC3198: development-exposed milestone-1 target; its baryon table is a prediction input.
  - DDO154: designated calibration-only object, not blind.
  - No unexposed validation roster exists.

## Unresolved (priority order; details in MISSING_INPUTS)
1. **M1, 43-query roster: missing from permitted sources.** The only in-tree source is `joint_parent_continuation/sparc_official_NGC3198_rotmod.dat` (sha 17b774ad…). It holds target Vobs/errV, so it was **not opened**. Needed: a root-run, reviewed, column-limited extraction (order + Rad only).
2. **M2, outer source support.** Source rings end at 15.1 kpc, while the target domain reaches about 44 kpc.
3. **M3, geometry crosswalk.**
   - NGC3198: Leroy 13.8 Mpc / i=72 / PA=215, errors null, against SPARC i=73±3.
   - DDO154: source 4.3 Mpc / i=66 against calibration roster 4.04 Mpc / i=64±3.
   - Needed: column-limited SPARC table1 metadata (table1 also holds Vflat).
4. **M4/M5, error semantics.** The e=1.0 and e=0.0 meanings need the primary paper. Whole covariance is absent, and rings are oversampled (12″ beam on 10″ spacing).
5. **M6–M12.** H2 beyond 6.4 kpc; conversion uncertainties; vertical structure; DDO154 adapter review; DDO154 stellar tail; current-parent observation map; blind roster.

## Exposure custody
- Not opened: any target velocity/error array, SPARC rotmod or mass-model rows, Leroy table4 (it holds Vflat), response products or fits.
- Files were only hashed where the inventory needed their identity.
- The DDO154 SOURCE_FROZEN.json text contains the word "velocity" only inside its prior-exposure note.

Processed IDs: 0336. Polling FROM_CODEX every 60 s for new CLAUDE2 work.
