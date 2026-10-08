# Fixed external-galaxy selection: DDO 154

2026-09-28. Source-led selection before a new force calculation. DDO 154 is now
the fixed next target; a disappointing source or velocity comparison is not a
reason to substitute another target. No target observed rotation table, velocity
map, force prediction or residual has been opened/computed in this selection.

## Why this target

The already resident [Leroy et al. (2008) source catalogue](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/AJ/136/2782?format=html&tex=true)
gives DDO 154 distance 4.3 Mpc, inclination 66 degrees, PA 230 degrees,
optical radius 1.2 kpc, stellar exponential scale 0.8 kpc, and rounded log
stellar/atomic-gas masses 7.1/8.7. Their ratio is about 40. This gas-dominated
choice reduces stellar-normalization leverage and has original, separately
downloadable HI integrated-intensity maps. Selection used those baryonic and
availability facts, not a rotation-curve residual or a survey of model fits.

The seven [table7 density rings](https://cdsarc.cds.unistra.fr/ftp/J/AJ/136/2782/table7.dat)
run only 0.1--1.4 kpc. They supply stellar densities
5.0, 4.5, 4.1, 3.4, 2.3, 1.8, 1.5 Msun/pc^2 and atomic-gas densities
7.3, 7.2, 7.1, 6.8, 6.6, 6.9, 7.0 Msun/pc^2. **These are not a complete
outer-HI source.** Their gas convention includes helium 1.36 already. H2
profile entries are blank; table4 supplies a rounded log molecular-mass upper
limit 6.8, not a measured zero or a radial profile. Table4 aperture masses are
not exact closure targets for truncated/rounded profiles. The paper defines
them within 1.5 r25; their tracer and aperture conventions must be preserved.
[Original table4 and definitions](https://cdsarc.cds.unistra.fr/ftp/J/AJ/136/2782/table4.dat),
[Leroy paper](https://arxiv.org/pdf/0810.2556).

## Public source route

The [official NRAO DDO 154 page](https://science.nrao.edu/science/surveys/littlethings/data/d154.html)
links its [individual HI products](https://things.cv.nrao.edu/littlethings/ddo154/HI/).
The [official product documentation](https://science.nrao.edu/science/surveys/littlethings/data)
identifies these two small maps as primary-beam-corrected moment-zero
integrated flux, from natural and robust=0.5 weighting respectively:

- [DDO154_NA_X0_P_R.FITS](https://things.cv.nrao.edu/littlethings/ddo154/HI/DDO154_NA_X0_P_R.FITS)
- [DDO154_R_X0_P_R.FITS](https://things.cv.nrao.edu/littlethings/ddo154/HI/DDO154_R_X0_P_R.FITS)

Only those source maps and small original metadata will be staged in
`external_ddo154_v001/`. Cubes and the separately named moment-one velocity
maps are excluded. Natural versus robust remains a predeclared source-resolution
contrast, not a choice to be made from velocity agreement. Original header
WCS, beam, BUNIT, blanking/mask, flux conversion and all signed retained pixels
must be qualified before any radial extraction.

An independent original geometry record is
[Walter et al. (2008) THINGS table1](https://cdsarc.cds.unistra.fr/ftp/J/AJ/136/2563/table1.dat),
with [reference codes](https://cdsarc.cds.unistra.fr/ftp/J/AJ/136/2563/refs.dat)
and [schema](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/AJ/136/2563?format=html&tex=true).
Unlike that catalogue's table4, table1 contains no sampled velocities.

## Fixed-source implementation path

1. Authenticate original source bytes and independently qualify geometry,
   units, mask/blank semantics and signed HI mass. Keep missing/blank pixels
   distinct from measured zero. No inclination factor belongs in a total
   sky-flux HI mass; helium is applied once, explicitly.
2. Freeze one planar source convention at the externally adopted D=4.3 Mpc,
   i=66 degrees and PA=230 degrees, with an original center record. Use radial
   bins no narrower than the beam, full footprint/retained-flux bookkeeping,
   and explicit inner/exterior support. A fixed plane is not a measured warped
   disk. Do not use velocities to choose radial support or reconstruction.
3. Retain the seven stellar rings, flat center and an explicitly modeled
   outer continuation using the published 0.8-kpc stellar scale. Carry the
   already fixed Leroy-to-M/L3.6=0.5 scalar 1.2567828155112788 into the complete
   stellar profile, including its tail; this imports a published convention,
   not a new fitted normalization. A zero-H2 baseline is an explicit omission,
   with the published upper-limit mass and missing spatial allocation recorded;
   it must not be relabeled an observed zero. Freeze any H2 sensitivity source
   from baryonic information before kinematic scoring.
4. Only after the source and valid-radius rules are frozen, obtain an observed
   velocity table and retain every valid row with its original angular/linear
   radius, distance, inclination and uncertainty conventions. Any conversion
   must be explicit. Solve the same-density Newtonian reference and the same
   previously frozen nonlinear law, a0 and second scale. No local scale,
   distance, inclination, stellar normalization or source-tail optimization.

This is a transfer test of the **adopted nonlinear gravitational field
interface**. It does not independently derive that interface from the native
UNT network Hamiltonian or qualify a cosmological/lensing completion.

## Exposure and limits

A broad source-discovery search inadvertently returned general published
kinematic/halo discussion and a smooth-fit velocity parameter from a source
table. No target observed velocity samples or model residuals were inspected;
the target was not changed. Accordingly this is an **out-of-program prospective
transfer**, not a blind test. Its primary immediate gap is outer-HI source
qualification, not a lack of an available map. Further limitations are the
stellar tail, unresolved molecular allocation, interferometric missing flux,
fixed-plane approximation, finite thickness, and the future tracer/source
geometry match. No force calculation has been authorized by this selection
note itself.

## Resident source custody

Previously authenticated, unchanged primary files in the parent directory:

- `leroy2008_table7.dat`: SHA-256
  `43165045c50d534ff7789dda05627328c23ba71c708ded9cf87cf0773fe02d99`.
- `leroy2008_table4.dat`: SHA-256
  `938104d0289f93f9fed0843028555e92f63a61889d623ee5b5f132e9d6ea1f44`.
- `leroy2008_ReadMe.html`: SHA-256
  `cbd9a431c5ef4d9ae1bcda8bc141210bd03360a4d2b0ea5d8dd40e9079763c48`.

New retrieval identities and header findings will be recorded additively in
`external_ddo154_v001/`; they do not replace those source records.
