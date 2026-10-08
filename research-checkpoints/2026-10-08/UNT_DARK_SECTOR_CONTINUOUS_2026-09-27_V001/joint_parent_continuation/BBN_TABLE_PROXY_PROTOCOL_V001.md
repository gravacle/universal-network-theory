# Prospective BBN table-proxy and heating-interface qualification V001

Root is the sole executor. `bbn_table_proxy_v001.py freeze|run` emits JSON
to stdout only; no PRIMAT import, installation, network, ODE, orbit, optimizer
or file mutation. Existing sources/results remain unchanged. This is **not**
a completed abundance prediction of the conserved scalar history.

## Inputs and comparisons fixed before execution

Authenticate all 360 `FINITE_GAP_PHOTON_BUDGET_V001_RESULTS.json` rows,
its freeze recursively, and the wrapped `GLOBAL_GAP_LIMIT_CALIBRATION_V001`
reference receipt/freeze. Retain exactly four spectra, 18 references and
R={32,128,512,2048,8192}. The inherited standard-BBN baryon densities remain
conditional inputs, not independent evidence for the changed history. Their
quoted errors are metadata, not propagated or used to choose rows.

Pin the primary 2026 table, all eleven inert official code/data snapshots,
`BBN_OBSERVATIONS_V001.json`, this protocol, the interface audit, the earlier
design and this source. No downloaded program is imported. The table's
1300 rows must be a unique complete 52×25 grid, with the documented columns,
T0=2.7255 K, baseline Neff=3.044, tau=878.4±.5 s and 1000 Monte-Carlo draws.
The pinned public generator establishes the column/API mapping, not an
exact execution receipt for the primary published table.

Each source's late proxy coordinate is
Delta=r/[(7/8)(4/11)^(4/3)], with r its saved asymptotic photon ratio.
Keep the physical inherited omega_b as the primary table coordinate; the
table's T0 is a declared tiny thermal-reference change. Separately report
the leading constant-mean-baryon-mass eta-matched coordinate
omega_b*(2.7255/2.72548)^3 and its prediction difference. Do not reinterpret
this sensitivity as a new exact baryon-mass conversion or change old input.
Every row gets the matched Delta=0 comparator. Outside the primary grid,
retain `OUTSIDE_TABLE_DOMAIN`; no extrapolation or automatic exclusion.

## Interpolation controls, fixed without outcome access

The primary interpolant is local tensor cubic Lagrange, four contiguous
nodes per axis, centered around the bracketing interval and one-sided only
at the physical table edge. Theory marginal sigmas use bilinear interpolation
to retain positivity; their difference from cubic is descriptive only.
All 1300 nodes are recovered for every stored column. Synthetic products
x^i y^j, i,j=0..3 qualify value interpolation. Arithmetic tolerance is
2e-12 normalized by max(1, absolute values) for dimensionless identities;
abundance node recovery is 2e-12 relative with a 1e-30 floor.

Withheld checks cover **every table node** in the prospectively specified
local comparison rectangle omega_b=[.020,.024], Delta=[0,3]. Remove its
baryon node, its radiation node, and both nodes in three separate controls;
interpolate with the remaining neighbors. Predeclared absolute allowances
are 2e-5 in YpBBN and 5e-8 in D/H. The ordinary and candidate coordinates
must also have cubic-versus-local-quadratic differences within these same
allowances. Results and failures are retained without tolerance adjustment.
Values outside this rectangle but inside the full grid are computed and
labeled outside the *local numerical qualification*; the table is not
silently shrunk or those rows deleted.

These allowances are a declared numerical budget tested by finite-grid
cross-validation, **not a mathematical supremum bound on unknown continuous
BBN solutions**. Theory Monte-Carlo errors are separate. Qualification
failure does not turn a prediction into an observational rejection.

## Thermal-history envelope, not an abundance-error estimate

Implement the exact pinned-source identities (6)–(8) of
`PRIMAT_2026_INTERFACE_AUDIT_V001.md`. For the official electron and summed
QED tables, reconstruct not-a-knot cubic splines with a tridiagonal solve.
Qualify every knot, C1/C2 and endpoint third-derivative conditions, and
synthetic degree≤3 polynomial recovery. No old producer is imported.

Use T in [.001,40] MeV. Partition at the union of every NEVO, electron and
QED knot in this range and at the electron cutoff. Each panel is subdivided
4 and 8 times. Exact local polynomial numerators are converted to Bernstein
form before division by positive T^4; a 2e-12×max absolute coefficient
floating-point padding is added before bounding, retaining the pre-cancellation
coefficient scale for the derivative-drift numerator. Coincident thermal
knots within 2e-14 relative are represented by their larger endpoint to avoid
a decimal-roundoff-width interval at m_e/30. This is a padded arithmetic
certificate, not formally directed interval arithmetic. All denominators,
actual and supplied heat-capacity and plasma-density lower bounds must remain
positive.
The known raw negative NEVO heating tail is counted and clipped only as in
the pinned source. No sample is deleted. The supply-derivative versus
interpolant-derivative drift is bounded separately, not assumed zero.

Accumulate lower/upper log-history bounds and a midpoint readout, which must
lie within the padded bounds. Retain both subdivisions, their intersection
and changes. Check a zero-heating/thermodynamically consistent synthetic
limit analytically; no requirement that the actual heating effect vanish.
Check that their interval intersection is nonempty. Test the raw and factored
history integrands independently on fixed synthetic sigma={.5,1,3},
C_true/sigma={2,3,5}, (N,C_supplied-C_true)={(0,.01),(.003,0),(.1,-.02)}
and the nine zero-heating consistent limits. Report both endpoint entropy
and scale-factor normalizations: the official boundary condition is
a_end*T_end/T0=(sigma_end/sigma_gamma)^(-1/3). Their fourth-power product
cancels exactly; retain/check the product and include its log in the history
envelope, rather than double-counting the entropy factor alone.
The fixed ordinary thermal history
and positive neutrino density permit a conservative H envelope using the
plasma-only lower density bound. Apply this row-wise using each positive
Delta. Also retain the scalar finite-gap bound at a fixed 10-keV photon
reference. Report T/T0 from exact kB/eV conversion as a photon-scale reference,
not an exact scale factor. The actual source relation is
A=(T/T0)(sigma/sigma_gamma)^(1/3)exp(-L/4); use the global positive sigma
lower bound and log-history upper bound to lower-bound A and upper-bound
the finite-gap energy correction, including residual heating.
Do not insert the resulting H envelope into an abundance sigma.

This envelope holds for the inspected source prescription and its fixed
ordinary-neutrino heating, not automatically the exact unpublished invocation
that made the public table or self-consistent altered neutrino decoupling.
Neither altered ordinary reheating nor a temperature-dependent abundance
response bound is supplied by this interpolation calculation.

## Output interpretation fixed in advance

Actual proxy YpBBN and D/H predictions, matched Delta=0 values and signed
differences are returned for every in-domain row. Compare with the fixed
Cooke D/H and Aver helium products. Report observation sigma, table marginal
theory sigma, interpolation allowance and each signed residual separately.
For a descriptive marginal standardized residual only, add independent
observation/theory source variances; do not claim Gaussian-tail probabilities,
cross-observable independence, a joint chi-square or exclusion confidence.

The nominal helium residual uses nucleon-number YpBBN, not atomic-mass Yp.
Display the D-only observational-denominator correction
Y(1+2D)/(1+2YD)-Y and the derivative 3Y(1-Y)/(1+2YD)^2 multiplying an
unprovided He3/H ratio. No bound on unprovided minor nuclides is invented.
This subleading convention limit remains visible alongside the much larger
quoted helium observational error; no precision claim conceals it.

Status `COMPLETE_PROXY_AND_INTERFACE_QUALIFICATION` means those restricted
calculations completed and their numerical controls passed. The output must
separately retain `conserved_scalar_abundance_status=NOT_YET_QUALIFIED`.
There is no observational success/failure gate and no selection of a best
gap/reference. All 360 labels, withheld residuals, thermal bounds and every
failed numerical control remain; no per-small-job checkpoint machinery.
