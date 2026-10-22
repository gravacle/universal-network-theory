# Exposure and reduction-dependence note (task 0341)

## Exposure record
- **0339 (incidental, previously disclosed):** a read-only helper saw two moment-one velocity-window thresholds in a HALOGAS MATHS HISTORY card and the VOBS header value. These are header velocity numbers, not rotation-curve data. The values are not recorded here or anywhere in Claude's artifacts.
- **0341 (this task):** every review document was read with digits masked on any line mentioning velocity, force, Newton, acceleration, channel, moment-one or rotation curve.
  - One masked line in PLANAR_DENSITY_REPRESENTATION_PROPOSAL.md (line 23) hid the radius range of an exterior emission concentration, because the same line mentions a velocity curve. That range is not reported.
  - The IRAC zero-point line of PHOTOMETRIC_SOURCE_COMPARISON.md was masked (it mentions a channel). Its value was already recorded in the 0339 inventory.
  - Not opened: HALOGAS_FIELD_*, HALOGAS Newton JSONs, rotmod files, MassModels data rows, Leroy table4, MOM1 maps and cubes, and the force section of HALOGAS_SOURCE_ORACLE_REVIEW.md.
- **0344 (incidental):** a grep for parsers displayed one code line that asserts the DDO154 MassModels distance value. It is a distance, not a velocity.
- **Status:** NGC3198 remains development-exposed (not blind) under the existing labels. This task adds no velocity exposure.

## Reduction dependence of the HALOGAS source (S2)
- The release mask that defines retained emission uses a moment-one velocity window. Pixels outside it are set to exactly zero (zero_or_replaced_mask).
- The retained-signal map therefore depends on a kinematic selection made during reduction. This is a reduction dependency of the source, not a velocity input to any later model.
- **Consequences:**
  1. The mask cannot be undone from the released maps (PLANAR_SOURCE_RESULTS_REVIEW.md lines 101–103).
  2. Masked zeros are not measurements of empty sky.
  3. Where masking is large (40.14–48.17 kpc, 43.66%), the effective density must not be read as a precise physical density (review lines 99–101).
  4. Any later claim that the source is velocity-independent must cite this dependency.
- **Labelling:** whether the kinematic mask removes real disk HI that should count as source is UNTESTED. Deciding input: noise/mask products or an unmasked cube (not in the release; absence scoped to halogas_source_candidate/).

## Other reduction dependencies recorded
- **S1 (Leroy):** the ReadMe abstract says the work "use[s] kinematics from THINGS". The local ReadMe does not state whether this affects the table7 surface densities. Recorded as such, with no claim.
- **S4 (.dens):** radii in kpc assume 13.8 Mpc (66 rows equal .sfb radii × 13.8 Mpc). Rows beyond 21.42 kpc are an inferred extrapolation.
