# Same-source fitted-halo comparison: completed V002

2026-09-29. Nine fixed baryonic-source variants in two galaxies, 72 fits.
This executes a previously missing comparator; it is not a new fit of UNT.

## Result and its use

**This was an in-sample fitting benchmark, not a predictive contest.** Each
halo received two parameters adjusted to these same observations; the network
curve received no new local adjustment. Lower halo residuals alone therefore
do not establish a stronger explanation or a predictive defeat for UNT.
The profiles are constrained two-parameter families, not arbitrary exact
interpolation: their nonzero residuals and retained full curves matter.

Both fitted halo families reproduce the existing rotation curves more closely
than the unchanged conditional network law under every predeclared fitting
objective. The result persists across all nine retained source variants, both
radius masks and both weighting choices. The current network law's substantial
improvement over baryons alone therefore does not establish an advantage over
fitted dark-component models.

The immediate research target is now sharper: account for the actual radial
response with the network's own state and shared dynamics. An independently
fitted halo density or a rescaling of the saved network velocities is not that
derivation. The prepared-state/clock/volume continuation remains a prospective
way to test the missing response while retaining its energy and state history.

This does not prohibit calibration of a derived UNT model or require every
constant to be derived first. Shared coefficients and any physically justified
local initial conditions may be inferred transparently, with their calibration
data, prior choices and uncertainties recorded. A comparison of predictive
strength must then use genuinely unused data, comparable treatment of baryonic
uncertainties, and the actual freedom used by BOTH frameworks. The exposed
galaxy residuals here may inform model development but cannot later be called
unused predictions. The joint galaxy/expansion connection is especially useful
if it constrains the same coefficients rather than introducing a separate fit.

The table displays equal-weight velocity RMS in km/s, with both halo parameters
fitted on the displayed mask. For NGC3198 the numerically better-qualified R≥2
kpc comparison is displayed; every inner point also remains in the all-radius
fits/results. For DDO154 all twelve qualified points are displayed. This is not
a post-hoc omission: both masks were fixed before execution.

| Fixed source | Displayed rows | Unchanged network | Fitted NFW | Fitted cored ISO |
| --- | --- | ---: | ---: | ---: |
| galaxy_HI1_H21 | R≥2, 37 | 11.1438 | 4.1695 | 3.1482 |
| galaxy_HI0_H21 | R≥2, 37 | 11.2195 | 4.1699 | 3.1552 |
| galaxy_HI1_H20 | R≥2, 37 | 11.0378 | 4.1987 | 3.1907 |
| galaxy_HI0_H20 | R≥2, 37 | 11.1130 | 4.1993 | 3.1978 |
| ML36_CAL_HI1_H21_V001 | R≥2, 37 | 9.5770 | 4.0141 | 2.5791 |
| HALOGAS40_ML36_RETAINED_V001 | R≥2, 37 | 10.5644 | 4.2365 | 2.8624 |
| HALOGAS120_ML36_RETAINED_V001 | R≥2, 37 | 10.4642 | 4.3415 | 2.9286 |
| DDO154_THINGS_NA40_ML36_H2OMIT_V001 | All, 12 | 4.7793 | 2.2141 | 1.2729 |
| DDO154_THINGS_RO40_ML36_H2OMIT_V001 | All, 12 | 4.6921 | 2.2074 | 1.2614 |

The seven NGC3198 rows are source sensitivities in the same galaxy; the two
DDO154 rows are two source-map treatments of that galaxy. They are not nine
independent tests and are not nine alternatives from which to select a winner.

## All prescribed comparisons remain in the evidence

Every source file includes all original radii, velocities, quoted errors,
the exact same-source Newtonian squared speed, the unchanged network speed,
and every fitted halo/total speed and signed residual. Each of eight fits
per source records all-row and R≥2 summaries, with NGC3198's outer R≥8 summary
also retained. Both equal-weight and quoted-error objectives were optimized
separately. A fitted subset never deletes its excluded rows from the output.

For context, the original NGC3198 HI1/H21 all-radius network RMS is 13.1737
km/s, versus 10.6976 for fitted NFW and 7.7308 for fitted ISO. In the
fixed-stellar-calibration case those all-radius values are 13.7895, 11.6600
and 9.0566 km/s. Thus the central mismatch is still present even in the halo
comparators and is not hidden by the R≥2 display above.

All 72 selected minima were finite interior profile candidates with positive
halo amplitude. Zero-halo choices, both exact scale limits, finite search
endpoints and every sampled local-minimum bracket were retained in each
profile. No boundary minimum was discarded. Agreement of two scale grids
and local refinement is a numerical convergence check, not a global
mathematical proof that no narrower unsampled minimum could exist.

The baryonic masses, source geometry, distances, gas treatments and error
values were not adjusted. NFW and ISO each have two local halo parameters.
The network curve has no newly fitted local parameter in this comparison,
but its prior shared calibrations and exposed development choices remain;
it is not globally parameter-free. No cosmological concentration–mass prior
was imposed on NFW. This is a spherical rotation-profile benchmark, not a
fit or rejection of the whole standard cosmological model.

Quoted-error sums are descriptive. They omit complete radial/source/geometry
covariance and nuisance marginalization. No likelihood ratio, AIC/BIC,
Bayesian evidence or discovery significance is claimed. These observations
were already exposed before the comparison; none is relabelled held-out.

## Qualification and preservation

- 42 synthetic/analytic controls passed before observational fitting: positive
  mass integrals, stable kernels/derivatives, limiting shapes, normalization,
  constrained amplitude boundary and exact synthetic-profile recovery.
- All 72 observational fits completed; all 369 recorded execution checks
  passed, with no changed criterion or scientific input.
- The final nine workers used 100.739 seconds total. Maximum observed peak
  process RSS was 121,995,264 bytes. They ran sequentially and have exited.
  That is a measured process peak, not an enforced aggregate resource limit.
- All 147 current frozen inputs were authenticated. Original fields were
  neither rerun nor changed.
- V001's pre-freeze receipt-status failure is preserved. V002 recognizes
  DDO154's exact COMPLETE_DESCRIPTIVE_COMPARISON status. No science ran V001.
- The first completed V002 source00 capture was truncated by the caller's
  output allowance; its received text is preserved. The same frozen source
  was rerun unchanged with a sufficient capture allowance. It is not a
  second, retuned fit or a discarded unfavorable scientific result.

## Evidence and next step

Definitions and exact inputs: HALO_COMPARATOR_PROPOSAL_V001.md.
Numerical controls: HALO_COMPARATOR_EXECUTION_V001.md and
HALO_COMPARATOR_V002_TESTS.json.
Source: halo_profile_fitter_v001.py and halo_comparator_v002.py.
Freeze: HALO_COMPARATOR_V002_FROZEN.json.
Complete results: HALO_COMPARATOR_V002_SOURCE_00.json through SOURCE_08.json,
in the fixed source order of the table above.
Independent review: HALO_COMPARATOR_V002_REVIEW.md.

The comparator definitions follow [Navarro, Frenk and White](https://arxiv.org/pdf/astro-ph/9611107)
and [de Blok et al., sections5.3.1–5.3.2](https://arxiv.org/pdf/0810.2100);
our saved baryonic fields and the prospective protocol specify this particular
comparison.

This closes the **fixed-source descriptive halo-comparator task**, not joint
Stage2 or Stage3. The next forward calculation must retain actual prepared
network state, gravity/clock constraints and volume work together. Its state
cannot be chosen separately at each observed radius to imitate these fits.
