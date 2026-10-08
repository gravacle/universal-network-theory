# Outer H I input decision: NGC 3198

2026-09-28. Primary-source discovery and visual transcription only. No
galaxy field calculation, rotation-curve fit, cube download or new numerical
worker. The same previously exposed development galaxy is retained.

## Decision

**A directly measured historical outer-density profile is available.**
Use Begeman (1989), Table 3, as the next independently checkable H I input,
with its original geometry and finite coverage declared. This is materially
better than inventing an outer mass distribution from a rotation curve.
It is not the newer HALOGAS reduction or a precision complete-galaxy model.

Original paper: K. G. Begeman, *H I rotation curves of spiral galaxies.
I. NGC 3198*, A&A 223, 47–60 (1989),
[university-hosted original ADS scan](https://sites.ualberta.ca/~pogosyan/teaching/ASTRO_322/WINTER_2008/Begeman1989A%2BA...223...47B.pdf).
The scan was retrieved with an 8-MB cap; actual size 2,552,528 bytes:

    begeman1989_original.pdf
    SHA-256 7745f7e83d2e31f90f493fa6c35b8e090c344b4dbdf83bc3bb206bde2899420c

The PDF skill guided visual checks of complete printed pages 52–58,
especially Table 3 on p55 and the helium statement on p56. No figure was
digitized to manufacture table values.

## Exact Table 3 transcription

Columns are angular radius in arcminutes and bare H I surface density in
solar masses per square parsec. The table contains no per-ring errors.
Figure 13 identifies the smooth profile as the average of the two halves;
their outer asymmetry is not an error covariance. The original density was
obtained by integrating the observed H I in the adopted tilted rings.

```text
R_arcmin  Sigma_HI_Msun_pc2
0.0       3.17
0.5       3.88
1.0       4.53
1.5       4.97
2.0       5.24
2.5       5.19
3.0       4.73
3.5       3.95
4.0       3.26
4.5       2.94
5.0       2.66
5.5       2.29
6.0       2.12
6.5       1.98
7.0       1.62
7.5       1.27
8.0       1.14
8.5       1.11
9.0       1.01
9.5       0.86
10.0      0.72
10.5      0.57
11.0      0.36
11.5      0.14
```

The paper uses 9.4 Mpc; its later gas-gravity calculation multiplies this
H I profile by 1.4 for helium. **Do not apply 1.4 and then 1.36.** Preserve
the bare column and, for a common Leroy comparison, apply the chosen 1.36
once. Table 2 gives radius-dependent orientation rather than one universal
inclination: outer inclinations rise to 77 degrees. [Tables 2–4 and
section 6–7](https://sites.ualberta.ca/~pogosyan/teaching/ASTRO_322/WINTER_2008/Begeman1989A%2BA...223...47B.pdf)

For a distance-only change at fixed angular rings and deprojection,

    R_kpc = D_Mpc * 1000 * pi/(180*60) * R_arcmin.

At D=13.8 Mpc the factor is 4.014257279586958 kpc/arcmin; the endpoint is
46.16395871525 kpc, beyond the existing 44.08-kpc SPARC endpoint. Surface
density is unchanged by this distance-only rescaling because inferred mass
and physical area both scale as D squared. A change of inclination or ring
geometry is a different transformation and must not be hidden in this rule.

## Small modern alternative, not downloaded

[Gentile et al. (2013)](https://arxiv.org/pdf/1304.4232) presents newer
approaching/receding density profiles in Figure 8; this search did not
verify an original numerical radial-profile table or corresponding CDS
catalogue. The paper reports total H I mass 1.08e10 solar masses at 13.8 Mpc,
and a thick component containing about 15 percent of it. These are not
additional unseen matter to add to an already total H I column profile.

[HALOGAS DR1 version 2, original survey data release](https://zenodo.org/records/3715549)
does provide `NGC3198-LR_coldens.fits` and `NGC3198-HR_coldens.fits`, each
4.2 MB, separately from the 415.3-MB cubes. Published version-2 MD5 values
are respectively `2420677647c332214ef0878ca90475c3` and
`3a985f5fdb45d4da49c390dfa890d5af`. No map or cube was downloaded. A future
bounded map extraction could recover an updated radial profile using a
predeclared ring geometry, but it requires inspection of FITS units, masks,
beam, primary-beam correction and source-finding conventions. Do not equate
this possible future reduction with the already published Figure 8 samples.

## Do not force the Leroy global-mass discrepancy into a tail

The earlier readiness note correctly read the literal section 3.3 statement
that table4 masses integrate to 1.5 r25. The parent has now found that its
radial-profile reconstruction fails closure against those totals: the
stellar inner profile already exceeds the rounded table4 mass, while the
H I difference would require a sharply enhanced outer annulus. Neither
result licenses adding mass to make the catalogue columns agree.

This is an unresolved difference of aperture, map/profile estimators,
conversion or metadata; its cause is not established. **Until reconciled,
do not use table4 as a hard equality that fixes the 15.1–19.5-kpc tail.**
The new measured outer profile supplies independent information instead.
Leroy's ring estimator and its stated aperture remain useful provenance,
not an internally qualified conservation constraint.

## Proposed input-only development comparison

1. Independently verify the 24-number transcription against the retained
   PDF, then freeze angular values, bare-H I units, distance and helium.
2. Retain one complete Begeman gas profile rather than silently grafting an
   outer tail onto a different inner reduction. Compare its overlapping
   baryonic values with Leroy after the declared conversions; preserve any
   disagreement without a velocity-based rescaling. A separately labeled
   splice is permissible only after choosing its overlap rule from density
   data alone.
3. Use positive piecewise-linear interpolation as a declared reconstruction.
   Beyond the last sample, compare a truncation with a continuous exponential
   continuation whose scale is fixed by the last two positive density
   samples, `ell = Delta_R/log(Sigma_penultimate/Sigma_last)`. These are
   modeled-endpoint alternatives, not observational confidence bounds.
   Do not optimize either against rotation speeds.
4. A first axisymmetric coplanar thin-disk experiment explicitly flattens the
   measured warped rings; it therefore tests a modeled source. Retain
   uncertainty in vertical/thick-gas distribution, stellar continuation and
   missing H2 rather than claiming a complete reconstructed 3D galaxy.
5. Qualify the source through its own mass and Newtonian-field calculation,
   then pass that identical density to the qualified nonlinear solver.
   Keep the existing velocity data out of density/tail choices. Report
   both endpoint alternatives, including a poor outcome.

This closes the specific absence of an observed outer H I radial input.
It does not by itself close geometry, uncertainties, all baryonic components,
the nonlinear field calculation, or agreement with the galaxy.
