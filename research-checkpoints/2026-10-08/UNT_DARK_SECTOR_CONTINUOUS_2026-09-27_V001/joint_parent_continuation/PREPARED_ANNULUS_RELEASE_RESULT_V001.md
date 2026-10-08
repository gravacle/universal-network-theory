# Prepared gravity release: result

2026-09-29. The actual saved coherent preparation admits a compatible weakly
curved initial geometry, but it does **not** admit its earlier clamped response
as a quasistatic source in this particular uniform annulus embedding. Its own
constraint determines a rapid initial source change. This identifies which
state assumption must change in a stationary candidate; it does not select
that replacement by fitting galaxy residuals.

All 12 predeclared cases (three inherited preparations, two annulus sizes,
two radial grids) completed. All 173 numerical checks and 31,721 independent
saved-result arithmetic checks pass. The successful worker took 0.11637 seconds
and measured 40,861,696 bytes peak self RSS. No large-memory job was required.

## What was solved

The existing covariant mechanical parent, its finite-band baseline and actual
signed mode positions/velocities were retained. One scalar metric ODE gives
the initial geometry; two radial quadratures give the initial lapse rate
required by constraint preservation. Both boundary lapse rates are fixed to
zero. Neither a zero-velocity reset nor a stationary phase mean was substituted.

For B=sum(w*delta*y), VB=sum(w*delta*v), and eta=Ndot/N, the exact initial
constraint-preserving flux is

    N r² [B h'' sqrt(f) eta' + N VB h'] = constant.

Its weak-field limit for r_out=2 r_in is

    eta' = [VB h'/(B h'')] [2/(r/r_in)² - 1].

This already predicts why reducing the annulus size reduces eta's amplitude
without suppressing its gradient or the proper source-change rate.

## Retained numerical finding

All geometries and lapses stay positive on the initial slice: the full-census
minimum f is 0.9999928072 and minimum N is 0.9999993896. The finite-parent
endpoint energy is DeltaU=12.7792881751, not an arbitrary subtracted zero.

At the finest preparation and radial grid, the larger annulus has proper
source rates of about -3128.84934 at its inner edge and +1564.42531 at its
outer edge. The corresponding fractional rates are about -1.25154e6 and
+6.25772e5. These are **internal, uncalibrated time units**, not seconds.
Halving the annulus size leaves these rates essentially unchanged. Both
spectral and preparation-step comparisons retain the finding. The source
rate changes sign inside; it is not uniformly nonzero everywhere.

Those boundary fractional rates exceed the initial local-curvature frequency
scales by many orders of magnitude. These frequency scales are not exact
finite-amplitude orbit frequencies. No finite-time spacetime evolution or
numerical action-drift calculation was performed.

## Consequence for the next calculation

A different state is needed before using a stationary galaxy response. The
separately declared shared phase-ensemble and boundary-determined equilibrium
in `SHARED_MODE_INFERENCE_AND_STATIC_CLOSURE_V001.md` provide a concrete
candidate, with their real excitation energy and vector/scalar distinction
retained. They do not rewrite the coherent state tested here. The pressure
bound tests that candidate's cosmic energy requirement before a new fit.

## Evidence

- `PREPARED_ANNULUS_RELEASE_V001_FROZEN.json`: 21 authenticated inputs.
- `PREPARED_ANNULUS_RELEASE_V001_RESULTS.json`: all 1,164 radial rows;
  SHA-256 `f73b01fe7f80c285f4fc3525017abbbd909d718a87878c198f24c6e295fe8f4a`.
- `PREPARED_ANNULUS_RELEASE_REVIEW_V001.md`: independent full review.
- `PREPARED_ANNULUS_RELEASE_V001_AUDIT_DATA.json`: independent arithmetic.
- `PREPARED_ANNULUS_RELEASE_V001_CAPTURE_RETRY.md`: preserved truncated
  first capture and unchanged-worker compressed capture retry. The final
  transport reproduces all 1,240,186 result bytes exactly. No model, input,
  gate or scientific outcome was altered to repair the transport.

This is an initial-state consistency result for the adopted effective parent,
not a measured galaxy curve, physical clock calibration, or native metric
derivation. All earlier frozen evidence remains unchanged.
