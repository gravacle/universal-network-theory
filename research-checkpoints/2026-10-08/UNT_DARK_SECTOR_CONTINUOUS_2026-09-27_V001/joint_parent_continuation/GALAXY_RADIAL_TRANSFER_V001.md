# Saved-galaxy radial extrapolation, prospective V001

2026-10-04. Code and protocol only until root review/release. This is exposed
development prediction across radius, not blinded validation, an exact disk
field calculation, or a test of cosmological halo formation.

## Frozen source and split

Use ONLY `SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json` central.predictions and
its existing 100 evaluation galaxies. The 51 former calibration galaxies
remain excluded from this new comparison. Retain the original frozen row
exclusions, central invalid list, and every new galaxy exclusion. No force
law, acceleration inverse, a0 calibration or baryonic field is recomputed.

Within each evaluation galaxy sort by (R_kpc, source_line). Require n>=6;
otherwise retain an excluded-galaxy receipt with its original rows. The first
floor(n/2) rows are halo calibration; the remaining rows are evaluation.
Tied split radii are retained and explicitly reported. The pivot is the
median INNER radius, never the full-radius median. Distances, inclinations,
stellar mass conversion and the full-radius baryonic source remain fixed.

For every retained row use b²=gbar_si*R_kpc/CONV, CONV=1e6/kpc_in_metres,
and the saved observed velocity and quoted error. Recover fixed predicted
velocities from the SAVED gpred_si for baryons, inherited_calibrated and
rar_calibrated. Do not run the force producer. Both effective laws retain
their previous global a0 calibration on 51 other galaxies. The inherited
r=25.51664211557329 also retains its earlier exposed cosmological calibration.
Zero new network/RAR/baryonic parameters are fitted here.

## Conventional comparison and fitting discipline

For NFW and pseudo-isothermal (ISO) use the inert existing helper
`halo_profile_fitter_v001.py`: v_model²=b²+A*s(R), A>=0, shape normalized
to one at the INNER pivot. The two local parameters are A (km/s)² and the
halo scale. Fit ONLY inner equal-weight velocity SSE; quoted errors are
retained but do not set fit weights. No mass-concentration, population or
virial-radius prior is added. These are phenomenological halo profile
families, not a complete LCDM prediction.

Use natural log(scale/pivot) grids of 257 and 513 points on [-20,20]. Profile
amplitudes by 96 vectorized bisections using the inherited exact bracket.
Include both finite boundaries, both EXACT zero/infinite-scale limiting
profiles, and the lowest sampled grid point. Refine every STRICT interior
sampled local minimum (lower than BOTH neighbors), with the inherited
80-step golden search, batched across strict minima for cost control, with
independent inherited scalar amplitude checks and final-candidate solves.
Do not refine tied/flat
plateaus repeatedly. If every sampled and exact-limit amplitude is zero,
retain the zero-amplitude boundary and report scale unidentified. Exact
scale limits are infimum profiles, not claimed finite physical halos.

Selection and tie breaking use inner loss ONLY, deterministic candidate
order. The 513-grid result is the predeclared finer representative, not a
choice based on outer agreement. Retain both fits and all candidates.
Require objective agreement <=1e-6*max(1,Jfine), and max outer prediction
difference/max(1,max(abs(vfine_outer))) <=1e-5. A loss-degenerate fit whose
outer predictions disagree remains UNRESOLVED; do not choose the nicer
outer prediction. Retain all full-radius predictions and signed residuals.

## Controls, custody and bounded execution

Before fitting galaxies, run the inherited positive-density quadrature
oracles for the NFW/ISO shapes, pivot/limit checks, exact-amplitude recovery,
synthetic two-parameter recovery and zero-amplitude plateau controls.
Compare vectorized grid amplitudes/losses with the independent old scalar
amplitude implementation at selected scales. Alter synthetic OUTER observed
velocities by large radius-dependent factors and require the fitted inner
parameters/losses to remain exactly unchanged. Each actual receipt also
checks that the fitting-input digest is unchanged by that outer mutation.
No outer velocity enters the fitter, its pivot, brackets or objective.

Frozen control gates: shape mass integrals 2e-11, analytic slopes 2e-8,
amplitude recovery 1e-11 relative, synthetic fitted parameters 1e-4,
synthetic inner SSE 1e-8, vector/scalar amplitude and loss 1e-10 scaled,
row acceleration identities 1e-12 relative, and zero-amplitude/leakage
identities exact. No tolerance or scientific score threshold is changed.

Root first reads both files, then runs `galaxy_radial_transfer_v001.py freeze`
to pin source, protocol, inert helper, saved source result and original
SPARC freeze plus the entire new 100-galaxy census. This is custody-only.
The default invocation (or `run`) executes synthetic controls if no pinned
test receipt exists, then resumes missing galaxy receipts in fixed name
order. A `tests` invocation is available without galaxy fitting.

One process, one BLAS thread, no installs or pycache. Every invocation has
a 55-second wall budget checked inside amplitude/golden loops. Completed
galaxies publish atomically without overwrite in
`GALAXY_RADIAL_TRANSFER_V001_CASES`; an interrupted current galaxy is not
published and resumes from its beginning. Existing receipts must match
the exact freeze and input digest. Exceptions are retained as error receipts,
not silently retried or excluded. No new model fitting is introduced by
resuming the same declared census.

Aggregate ONLY after all 100 census receipts exist. An exclusion remains
in the census. A failed numerical comparison remains in it as unresolved.
If all eligible fits exist, save full-census coarse and fine aggregate
metrics even when refinement failed, clearly marked unqualified; never
silently restrict the headline to a numerically favorable subset. A missing
halo prediction withholds that full-census halo aggregate. Fixed-model
predictions and all per-galaxy outcomes remain available.

## Primary outputs and interpretation

The PRIMARY OUTER metric is galaxy-balanced velocity MSE (km/s)²; log10
acceleration MSE (dex²) is SECONDARY, not a substitute used to choose a
winner. First average radii within each galaxy, then average
galaxies equally. Save paired per-galaxy differences for the fixed network
prediction versus baryons, RAR and each halo model at both resolutions.
Save inner/outer masks, pivot, full rows/predictions/residuals, numerical
controls, exclusion counts, amplitude/finite-scale/limiting-profile boundary
frequencies, source hashes and resources. No bootstrap or observational
pass threshold is introduced in this first calculation.

The two halo parameters are learned from inner data; both force-law a0
calibrations predate this radial split and use the separate calibration
galaxies. This compares those specific predictive preparations fairly; it
does not establish that two halo parameters exhaust cosmological freedom,
that source systematics cancel, or that the effective network law is native
UNT. Outer source photometry is allowed for ALL models, but outer kinematics
are not used for fitting. Shared source errors, catalogue selection,
correlated radii, and earlier public-data exposure remain qualifications.
An independently established mass-concentration relation would be a
legitimate different predictive halo baseline, not an outer-data fit; it is
not implemented or adopted in this two-free-parameter comparison. NFW and
ISO are always reported separately, never selected per galaxy by outer loss.
