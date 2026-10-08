# NGC 3198: highest-information next source test

2026-09-28. Input investigation only; no profile extraction, fit, or new field calculation.

## Recommendation

Replace the **whole observed H I profile** with an independently reconstructed HALOGAS profile before trying another tail, distance, or external-field adjustment. The original four source models and fixed stellar-calibration comparison remain intact. This recommendation follows the age and geometry of the source measurements, not a choice of correction that lowers the predicted speed.

The original model uses the full Begeman profile flattened into one plane. HALOGAS provides deeper observations and a modern gas-distribution/kinematics analysis: its reported bare-H I mass is `1.08e10 Msun` at the same 13.8 Mpc, close to our reference `1.113e10 Msun`. Thus its principal leverage is **radial distribution, warp and tracer interpretation**, not a presumed large reduction of total mass. Its Figure 8 contains side-dependent inclination, position angle, rotation and H I density; a corresponding numerical ring-geometry table was **not verified** in this search. The 2013 analysis also models a roughly 15% thick component, with approximately 3 kpc scale height. Those are redistribution/kinematic inputs, not additional gas. [Gentile et al. 2013](https://arxiv.org/abs/1304.4232)

## Actual small public input obtained

The [HALOGAS DR1 version 2 archive](https://doi.org/10.5281/zenodo.3715549) provides the [NGC 3198 LR column-density map](https://zenodo.org/records/3715549/files/NGC3198-LR_coldens.fits?download=1). One original 4,236,480-byte FITS file is preserved in `halogas_source_candidate/`; no cube was downloaded. The [creator's institutional release description](https://research.rug.nl/en/datasets/the-westerbork-halogas-survey-data-release-1/) identifies the column-density and separate moment products and SoFiA processing. Full header findings and hashes are in `halogas_source_candidate/HEADER_AUDIT.md`.

Most consequential: **the inherited BUNIT is stale** (`JY/BEAM.km/s`), whereas the final recorded arithmetic has already converted the map to H I column density. Blindly trusting BUNIT would double-convert it. The file is a masked, primary-beam-corrected sky projection, not a face-on, helium-inclusive surface-density table. It contains no usable radial geometry or uncertainty table. The released SoFiA mask is not automatically the exact mask used for the older paper's Figure 8.

## Small next experiment, with no kinematic tuning

1. Qualify the FITS interpretation and mask bookkeeping; retain the original bytes. Use its explicit conversion history, not BUNIT alone. A paired moment-zero comparison could independently check the scale, but has not been downloaded here.
2. Fix the center, projected annuli, inclination/position angle and radial resolution from a declared observational source **before** computing the profile. Prefer the actual HALOGAS ring solution if a numerical publication product can be obtained. Otherwise label any fixed-plane reconstruction as such; do not call it the published warped profile. A 35-arcsec beam cannot provide independent 4-arcsec rings.
3. Report the whole radial profile, both sides, detected-area fraction and sky-integrated mass. Do not renormalize to the paper's total or use masked pixels as precise zero-gas measurements. Keep helium at the existing factor exactly once. Preserve source/geometry alternatives rather than selecting on rotation residuals.
4. Only then replace H I, keeping distance, stars, H2 and constitutive parameters fixed. Compare density and Newtonian forces before the one nonlinear calculation. A change of gas-plane geometry must not silently retain circular speeds deprojected using another geometry; a full joint source/tracer update is a separate comparison.

## What to defer

- **Distance:** an independent calibration lists 13.3 +/- 0.55 Mpc, rather than 13.8. Our fixed-angular-source scaling would change speeds by about 1.8%, uniformly; it is not an independently justified shape correction or a value to select against the residual. [Ponomareva et al. 2017, Table 1](https://academic.oup.com/mnras/article/469/2/2387/3779720)
- **Thickness/warp:** a volumetric source test is useful after the radial input audit. It cannot be implemented by softening the Newtonian force and applying a radial scalar shortcut. Signed ring forces also prevent inferring the direction of every local change merely from spreading the gas vertically.
- **Environment:** published independent Newtonian-environment estimates exist, but are not the rotation-fitted external-field parameter. They have large dependence on treatment of missing baryons and provide neither the required vector boundary nor its mapping under this constitutive law. Do not insert the fitted `0.055` parameter. [Chae et al. 2021, Tables 2-3 and environment construction](https://astroweb.case.edu/ssm/papers/Chae_2021_ApJ_921_104.pdf)

The immediate gain is a modern measured source, not another adjustable way to absorb a discrepancy. Astropy is absent from the bundled Python; no package was installed. Header inspection used the standard library only.
