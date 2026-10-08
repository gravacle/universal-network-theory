# Prepared annulus V001: independent saved-result review

2026-09-29. **Accepted for the declared initial-slice and initial-clock-rate
diagnostic.** All numerical controls pass. The physical result is a compatible
weakly curved initial slice with a very fast required source rate for this
particular coherent, uniform prepared state. A successful numerical solve is
not a successful quasistatic approximation.

## Custody, census and capture

All 21 input hashes in the freeze match resident bytes. The numerical source
and protocol are the same independently reviewed pre-run versions:

| Artifact | SHA-256 |
|---|---|
| `prepared_annulus_release_v001.py` | `d7595be62f12a1574b98a22ad808e3a7fb56e5408ae9bd6d07633bc4722633c3` |
| Protocol | `28375c681355fa5d4c6686149fa9cf4798533fbc1bb2da638463adce16345b26` |
| Freeze | `bca6d8a49923a377548067a90126f5b5f99ca0f2a72a07a345ba1916bcf0288e` |
| Full result | `f73b01fe7f80c285f4fc3525017abbbd909d718a87878c198f24c6e295fe8f4a` |
| Canonical result payload | `7d4dfb7f5cbcca2c02998330472da04b756d3e4fe232710b1a16ab2867f27f73` |
| Independent audit source | `4c7db74639d99ca5a21272a6026cebf2e63c5ffb39dce0636557d19e57aca088` |

The complete census contains three inherited preparations × two annulus sizes
× two metric grids: **12 cases, 1,164 radial rows, 173 distinct passing checks**.
No state, sign, boundary row or case was selected away. The original saved
preparation payload is independently reauthenticated.

`PREPARED_ANNULUS_RELEASE_V001_CAPTURE_RETRY.md` records the first run's
truncated stdout and unchanged-worker capture retry. The separately retained
zlib/base64 transport decompresses to **exactly 1,240,186 bytes**, byte-for-byte
equal to the published full JSON and its transport SHA-256. The retry changed
transport, not the model, inputs, numerical tolerance or census. A truncated
first capture is not treated as complete numerical evidence.

## Independent checks without another ODE solve

`prepared_annulus_saved_audit_v001.py` reads only existing artifacts and imports
no scientific worker. Its **31,721 arithmetic checks** reconstruct the original
state summaries, positive endpoint baseline, complete local energy and clamp
work, every radial field/readout formula, density constraint, constant release
flux, mass/boundary formulas, and both finite-difference residual arrays from
the stored rows. It performs no ODE integration or mode evolution. Its output
is `PREPARED_ANNULUS_RELEASE_V001_AUDIT_DATA.json`.

Maximum independent density-constraint discrepancy is `5.684341886080802e-14`;
constant scaled-flux discrepancy is `2.710505431213761e-20`. Recomputed metric
and release finite-difference arrays match the stored arrays. The largest
original gate fraction is about `6.0145e-4` of its allowed tolerance (the
clock-quadrature check); none is marginal. Zeroing either endpoint eta was
not imposed on a stored result after integration: the primary integrated
outer value is at most `1.9905951886833861e-16`, and the independent Gauss
evaluation of the Simpson-defined flux gives at most `4.594311042716015e-11`,
within its unchanged `2e-7` gate.

The worker reports **0.11636733400519006 seconds** and **40,861,696 bytes peak
self RSS** (about 38.97 MiB). These describe the successfully captured process,
not aggregate memory or the total time of both capture attempts.

## Baseline and actual prepared state were retained

The three states use `Kb≈0.4999995`, `C≈4.000004`, the same inherited
`gs=21.65919852693508`, and their actual signed y,v arrays. Recombination gives
`B≈0.00172035974227`, `VB≈8.60555703e-5`, with both signs of individual mode
velocity retained. No minimum, RMS velocity, rephasing or zero-velocity reset
was substituted.

The owned finite-parent positive endpoint is
`DeltaU=12.77928817511152…` and `Lambda≈51.11720381765`, rather than zero.
The 64-node endpoint is `12.779288175111567`; both 128-node endpoints are
`12.779288175111521`. The independent same-band continuum contrast is
`12.779288175111864`; the full zero-cutoff contrast is
`12.779288176470354`. The finite-to-same-band differences are about
`−3e-13`, whereas the distinct cutoff/full-band difference is about
`−1.359e-9`. These are not conflated or used to replace the finite action's
baseline. The original prepared energy `≈8.845073644e-7` and the local
interaction change from its old clamp remain separately accounted.

## Physical finding: positive geometry, fast required source

Every stored initial f and lapse is positive. Across the full census,
`min f=0.9999928071624828` and `min N=0.9999993896486238`; the metric ODE
denominator remains near one. The release coefficient has the required
negative sign and is nonzero; its smallest absolute scaled value is about
`2.75039e-8`. Thus this result is not a failed numerical branch or a singular
initial metric.

For the finest inherited preparation (128 modes, preparation dt=.005),
using the 128-cell radial grid:

| Quantity | r_in=1/4096 | r_in=1/8192 |
|---|---:|---:|
| Proper source rate at inner edge | −3128.84934057 | −3128.84323327 |
| Proper source rate at outer edge | +1564.42531027 | +1564.42173803 |
| Fractional source rate at inner edge | −1.251541144e6 | −1.251537842e6 |
| Fractional source rate at outer edge | +6.257723788e5 | +6.257695069e5 |
| Maximum sampled absolute eta | 0.1310611972 | 0.06553038733 |
| Maximum weak-oracle discrepancy / fixed rate scale | 3.81923e-6 | 1.48644e-6 |

These are uncalibrated internal-clock units. The boundary fractional rates
greatly exceed all retained initial local-curvature frequency scales, whose
largest value is about 0.99993. The source rate passes through a sign change
inside the annulus, so this is not a claim of a uniformly nonzero rate at
every radius. The curvature frequencies are not exact finite-amplitude orbit
frequencies, and no numerical action-drift calculation is claimed.

The leading weak-field prediction is independently known:
`eta_r=(VB*h'/(B*h''))*(2/x²−1)`. The observed inner/outer signs and magnitudes
converge toward it as the annulus shrinks. Halving the radius roughly halves
eta's amplitude but leaves the physical source-change rates essentially
unchanged. Fixed lapse values at the two boundaries therefore do not mean a
stationary acceleration/source field in between.

The 64/.01→128/.01 contrast is the spectral-resolution comparison; the
128/.01→128/.005 contrast is the preparation-time-step comparison. Both retain
the fast-rate finding. No combined contrast is called a purely spectral test.

## Scientific consequence

For this declared coherent uniform embedding, one cannot promote its earlier
clamped phase mean to an autonomous quasistatic gravitational response: its
own clock/metric constraint requires immediate rapid source change. The
calculation identifies the failure of that preparation's quasistatic use,
not a failure of all states, the mechanical parent, or UNT. A separately
owned phase ensemble or a different common formation history would be a new
state to test with its full energy and constraints, not a silent repair of
these stored trajectories.

Only the compatible initial slice and required first derivative have been
computed. No finite-time release evolution, nonlinear stability theorem,
regular-center whole galaxy, physical clock calibration, galaxy fit or
native BS-to-metric identification follows from these numbers. All original
frozen artifacts and the capture history remain unchanged.
