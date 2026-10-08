# Finite-pressure BAO and required-ruler census: prospective controls

2026-09-29. Root alone freezes and executes this stdout-only worker after
read-only preflight. No numerical outcome was examined to choose these
rules. BBN inverse metadata/census and old exposed DESI products were read.
The physical derivation/scope is FINITE_PRESSURE_BAO_AND_RULER_DESIGN_V001.md.

## Fixed input census and ordinary history

Read the complete authenticated BBN_SHARED_INVERSE_V001_RESULTS.json:
67 inverse-table points, five backgrounds, four source-spectrum copies,
1,340 labels. These are named contour/profile samples, not a probability
sample or a complete continuous inverse region. Preserve every point's role,
coarse/fine Delta flag and local-interpolation qualification. The old 18
reference labels remain mapped to the five backgrounds. Do not choose a
best BBN or BAO point or optimize anything else in this worker.

At a common point/background the normalized zero-source homogeneous history
is independent of all four soft copies. Check this using their saved s and
I/e^(3/4), then calculate once: 335 histories. Unsupported inherited physical
states remain explicit; do not force them into the hard band. The Delta=0
row is the R->infinity, nonzero-energy dust limit, never called a finite
empty state. No source energy, matched vacuum, acceleration scale or global
hard gap is changed. Their galaxy constitutive differences remain intact.

Use the declared massless ordinary-neutrino value 3.044 and inherited photon
normalization T0=2.72548 K. Preserve Hcal and the matched physical vacuum;
report the resulting H(1)/Hcal. This is a post-annihilation reference history
through A_cut=10^7, not exact altered neutrino decoupling and not the PRIMAT
fixed-heating proxy continued unchanged. The scalar background current is
exact for the adopted alpha-one fluid, conditional on that effective action.
The hard density is never replaced by constant extra radiation at late times.

## Numerical representation and complete observables

Implement the positive angle integrals and the exact t=log(r/r1) variable
change in the design note. Primary angular quadrature is 128-point Gauss,
independently compared with 64. Endpoints use 64 monotone bisections in the
proved bracket [2 log A,3 log A]. The dust limit has t=3 log A exactly.
No action trajectory, orbit propagation, cosmological ODE or interpolated
equation-of-state table is introduced.

Read the unchanged 13 DESI distances and complete covariance. Retain their
original order including the final DH,DM pair. Profile exactly ONE common
nonnegative B=c/(Hcal rd) using Cholesky whitening, check a direct linear
solve, and retain all predictions, signed residuals, covariance contributions,
profile derivative/curvature and score. There is no observational pass gate,
new free Omega_m, significance, fitted galaxy parameter or acoustic-ruler
prediction. These data and their earlier score were already exposed.

Compute the same-background dust+identical ordinary-radiation comparator,
with its one ruler profile. Also recover the old zero-radiation dust shape
as a saved-receipt numerical control, without overwriting that old result.
Do not compare mismatched radiation conventions silently.

BAO distance integrals use Gauss64 in t versus Gauss32 at the SAME angle128,
plus angle64/Gauss64 separately. Acoustic integrals use those same orders on
uniform t panels of maximum width2; retain independent angular and integral
refinements rather than relying solely on a combined coarse calculation.
Every history also has a composite Simpson512 BAO distance check at z=2.33
and Simpson4096 acoustic integrals over the full truncated interval. Simpson
uses fresh equispaced t nodes, not a resampling of the Gauss values.

Save material history and both photon-baryon and hard sound-horizon intervals
at A={1,11,101,501,1101,3001,10001}. The photon sound speed contains only the
ordinary baryon loading. The hard horizon uses the same-state sqrt(cI2),
not a neutrino propagation model. Save descriptive w={.01,.1,.3} transition
markers; these are not empirical cutoffs or selected epochs. Crossing below
the present or above the thermal domain is labeled explicitly.

For each profiled positive B, invert the truncated photon integral at 1/B
and at 1/B minus the positive early-tail upper bound. These give the required
endpoint interval; retain below-present/above-cutoff statuses. A=1+z, so the
reported quantity is NOT redshift itself. If a bound does not invert inside
the integrated domain, retain null with its reason. No standard z_d, z_star,
147 Mpc or fitting formula is substituted. The tail interval is a physical-
scope uncertainty under the continued scalar/current, not a quadrature error.

## Controls fixed before outcomes

All errors are absolute differences divided by the explicitly supplied
natural scale; they are not percent differences unless named as such.

- Default identities, copy cancellation and endpoints: 2e-11 normalized.
- Covariance symmetry/Cholesky: 2e-12 absolute.
- Angle refinement of material quantities: 2e-10 relative (zero dust
  pressure/curvature must remain exactly zero).
- BAO distance refinement and Simpson: 2e-10 relative.
- Direct/refined quadratic scores: 2e-7 absolute.
- Acoustic Gauss32/64 and independent angle64/128: 2e-8 relative.
- Acoustic Simpson4096: 2e-7 relative.
- Required endpoint inverse: 2e-9 relative in the integral, not in a
  potentially small difference of redshifts.

Synthetic qualification precedes real scores: r={1e-12,.01,1,1e4}; independent
Simpson1024 action integrals; action/virial and finite-gap energy bounds;
endpoints A={1,3,1101,10^7}; action scaling, energy envelope and known
positive bounded w,cI2 and logarithmic slope. Synthetic covariance profile
recovers amplitude42 and score<1e-18; a negative synthetic data vector must
choose B=0 with the correct one-sided derivative. These are arithmetic/
representation tests, not a favorable physical-state selection.

At every finite real state's A=1, directly compare the universal w,cI2,
omega/R and f(r1) with the saved inverse's w,cI2,omega/R and I/R^3 at the
same 2e-10 material tolerance. No new moment is fitted or re-prepared.

All checks/failures remain, and COMPLETE certifies only this numerical
calculation. Refinement deltas are saved for every real history. No tolerance
is tuned after seeing results. The early-tail interval may be wide, especially
in the dust limit; that is not silently shrunk or reclassified as a numerical
failure. Required drag and CMB/recombination status remain NOT_COMPUTED.

## Custody, resources and first timing benchmark

`freeze` reads/authenticates only, prints the complete source/configuration
snapshot and performs no prediction. Bind the exact inverse raw bytes,
wrapper/payload, its source freeze and all named ancestors; likewise the old
DESI source/result freeze, covariance and data. Include the new source,
protocol/design and analytical current/radiation/CMB notes. No ancestral
producer module is imported or executed.

After publishing the freeze, root may run `benchmark`: it selects the first
FINITE_HARD_STATE in the already fixed inverse row order, keeps all synthetic
controls and the matching dust comparator, and outputs exactly one history
with `benchmark_only=true`. This is a timing/qualification preview, not a
new favorable-point choice or the completed 335-history census. The eventual
`run` recalculates and retains ALL histories under the identical frozen
settings. Benchmark outcomes cannot change the physical census or tolerances;
a technical repair must preserve the failed version and result.

For recoverable sequential execution, `run-background 0` through
`run-background 4` are also fixed before the first benchmark. Each produces
the same67 histories for exactly that already named background, repeating
the same synthetic controls; it explicitly reports COMPLETE_BACKGROUND_SUBSET,
not completion of the whole335-history census. Root may publish five separate
immutable wrappers. All five are required for the alternative complete run;
the background choice is not an observational selection. Existing published
subsets must authenticate before any future read-only aggregate/reuse. No
hidden checkpoint, automatic file overwrite or resume from a different freeze.

NumPy plus the standard library; thread counts1 before NumPy import. One
history at a time, bounded positive angle arrays and no dense cosmological
state matrix. The largest primary acoustic panel uses64x128 entries; the
independent Simpson4096 uses4097x128, a few MiB. Record per-history elapsed
times, actual total elapsed time and self RSS. No arbitrary deadline or new
installation. Stdout wrappers include freeze and payload SHA256; root owns
publication. Large stdout may be paged by the existing root procedure;
no cases, epochs or channels may be deleted to meet a display budget.
