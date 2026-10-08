# Prospective measured-density development test, NGC3198

2026-09-28. Freeze before any field output or velocity scoring. The galaxy
is exposed development data, not a held-out discovery. No rotation velocity
is used to choose or rescale its baryonic density, its acceleration law,
stellar mass normalization, distance or tail scales.

## Physical inputs fixed from independently read baryonic data

Use D=13.8Mpc. Begeman1989 Table3 supplies all24 bare-HI surface densities
at0,.5,...,11.5arcmin. The root and input reviewer both visually checked
the original p55. Convert only angular radius by D*1000*pi/(180*60);
multiply the bare-HI column by1.36 once, matching Leroy's helium convention.
This retains the old tilted-ring deprojection, flattened into an explicitly
coplanar axisymmetric thin-disk source; it does not undo the measured warp.
The profile reaches46.164kpc. Keep the complete old profile rather than
grafting a new outer tail onto a different inner reduction.

Use all23 Leroy stellar measurements0.3–15.1kpc, with their already adopted
K-band M/L=.5 (not SPARC3.6-micron M/L=.5). Piecewise-linear surface density,
constant central continuation0–.3kpc, and an exponential outer continuation
of length3.2kpc, the independently reported stellar scale. No global-mass
renormalization: the table4/profile mass discrepancy is retained separately.

Use all10 populated molecular-gas measurements0.3–6.4kpc; these already
include helium. Keep blank measurements as missing, not measured zero.
Compare two explicit continuations after6.4: truncation, or exponential
length2.7kpc, the table4 CO scale. The first is a missing-component stress
case, not an observational upper/lower confidence bound.

Compare two HI continuations after its endpoint: truncation, or continuous
exponential of length (R_last-R_previous)/log(.36/.14), determined only
from the final two density measurements. Cross both HI and H2 alternatives
to give four source models; retain every outcome. Sharp truncations produce
ideal razor-thin edge singularities, so do not identify a grid-smoothed edge
as a resolved physical feature. Stellar conversion, central density,
thickness/flaring, warp and gas conversion systematics remain unvaried named
limitations of this first comparison.

## Law and numerical choices

Keep the prior frozen mechanical law, a0=1.2e-10m/s² and r=25.51664211557329.
Neither is selected against NGC3198. The r calibration is conditional on
the previously declared cosmic reference; it is not a native derivation.
Use G=4.30091e-6 kpc(km/s)²/Msun and
a0=1.2e-10*3.085677581491367e19/1e6 (km/s)²/kpc.
Integrate every annular baryonic source exactly for its declared linear/
exponential interpolant. Apply the nonlinear equation to the total source,
not separately transformed Newtonian component velocities.

Use the qualified nonuniform cylindrical disk solver. Dirichlet boundaries
use the isolated spherical monopole of this same total mass, not an exact
disk boundary. Qualification must therefore include remote-domain and mesh
checks before judging physical residuals. Prospective grids: L=255kpc,N=256;
L=1023kpc,N=320 (same logarithmic cell spacing, identical inner grid); and
L=255kpc,N=512 (twice the logarithmic resolution). Require fixed-source
radial-force changes below2% at the recorded comparison radii R>=2kpc for
both domain and resolution checks. If they fail, preserve results and
diagnose numerical error without adjusting the physical density or law.
All four source models run on all three declared nonlinear grids. Run a corresponding
Newtonian solve for each identical source, with its source normalization
and an independent ring-integral cross-check.
At its five fixed radii, compare the Newtonian grid force with the saved
ring-oracle height extrapolant. Require a difference no larger than2% of
max(1,absolute reference) in (km/s)²/kpc, plus the oracle's retained
successive-extrapolation and48/96-order differences. This is a practical
numerical comparison, not a rigorous uncertainty interval or galaxy-fit gate.
Keep the existing residual, global-flux and no-clipping thresholds.
One worker/thread. Publish complete
cases atomically for restart; jobs long enough to require mid-case recovery
also preserve iterative state in a separately authenticated checkpoint.

## Comparison output, not a pass-by-fitting criterion

Keep all43 SPARC observed rows and their stated errors. The observed curve
is used with its published geometry; do not silently inclination-rescale it
to match the older gas or Leroy reductions. Compute vc²=R a0 g_R on the
model midplane. Report every residual and summaries for R>=2 and R>=8kpc,
plus all43 rows descriptively. Negative radial force, if any, is retained
as such rather than turned into a real circular speed.

Report RMS velocity residual, mean signed residual, maximum absolute
residual, and nominal error-weighted squared residual. The latter is NOT a
precision likelihood or significance: ring covariances, warp, thickness,
distance and conversion systematics are not included. No observational
acceptance threshold, nuisance optimization, selected-row deletion or
retrofitted tail follows from a favorable or unfavorable result. This is
a no-refit development prediction of the declared conditional network
response law with a measured, explicitly simplified baryonic source.
