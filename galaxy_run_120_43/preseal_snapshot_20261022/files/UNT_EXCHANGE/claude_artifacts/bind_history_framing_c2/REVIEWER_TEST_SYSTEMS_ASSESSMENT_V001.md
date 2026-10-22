# Reviewer-proposed test systems for a Bind-history ("lock-duration") weighting: root assessment V001

Claude2 (root), 2026-10-17. The principal forwarded these as ideas, not as instructions. Disposition: **recorded as candidate deciding tests for a derived Bind-history weighting. They are not calibration anchors, and nothing changes in the 120/43 protocol.**

## Why these systems are useful

The proposal itself is sound in shape. The tests should be systems with similar present-day baryonic mass and very different record histories:
- tidal dwarf galaxies (TDGs);
- starless or nearly starless HI structures such as the Leo Ring;
- dark-matter-deficient galaxies with old stars, such as NGC 1052-DF2 and DF4.

They also test the *current* forward route, which weights sources by mass only. The lapse audit (`lapse_integration_audit_c2`, 857e8f7d) measured the current response as about 8× Newtonian and attractive at short wavelength, independent of record history. So the current route predicts the same enhancement for a TDG as for a primordial dwarf with the same baryon distribution.

## Corrections to the reviewer's factual claims

These are needed before any of the systems is used:
1. **TDGs.**
   - Bournaud et al. (2007) reported a missing-mass factor of about 2–3 in the NGC 5291 TDGs and attributed it to unseen baryons. They did not report "zero dark matter".
   - Later kinematic analyses found the data consistent with little or no dark matter, with large inclination uncertainty. Lelli et al. (2015) is one.
   - Standard cold dark matter *expects* TDGs to be dark-matter-poor, because they form from disk material. TDGs therefore discriminate mainly against mass-only modified-gravity laws, which includes the current route.
2. **Leo Ring.**
   - Sparse star formation has been reported in it.
   - Its gas metallicity suggests pre-enriched, tidal material rather than primordial gas.
   - Its kinematics trace an orbit in the group potential, so it does not cleanly test a halo of its own.
   - It is a weak "zero-lock" baseline.
3. **NGC 1052-DF2 and DF4.**
   - The dark-matter deficit is debated, partly through the distance.
   - Dark-matter-poor formation channels exist within standard cosmology, so it is not true that a galaxy "cannot form without a halo".
   - For a Bind-history hypothesis, DF2 is the hard case: it has old stars but little extra gravity. Explaining it by "wake stripping" is admissible only with a stripping criterion declared *before* the data are examined. Otherwise the hypothesis cannot fail.

## What is not adopted

**Calibrating a "Lock-State Multiplier" on TDG mass-to-light ratios is not adopted.**
- That would make a weight fitted to external data. Program rule: effective terms are derived as outputs, never fitted.
- It would also change the pre-registered 120/43 calibration (DDO154, 12 rows).
- No such multiplier exists in the model.

If a Bind-history weighting is derived from the owned parent (see `BIND_HISTORY_FRAMING_V001.md`), TDGs, DF2/DF4 and the Bullet Cluster become **out-of-sample** deciding tests, frozen in advance like NGC3198.

## Data requirement (later, not on the 120/43 path)

The test needs:
- published rotation curves or velocity dispersions, with baryonic mass models, for NGC 5291 TDGs and comparison dwarfs;
- the DF2/DF4 dispersion data together with the distance alternatives.

The rule is the same as for NGC3198: everything is frozen before any target is opened.
