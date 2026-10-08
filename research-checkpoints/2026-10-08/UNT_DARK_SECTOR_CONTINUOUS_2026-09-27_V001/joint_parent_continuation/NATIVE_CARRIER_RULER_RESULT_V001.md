# Native carrier measures connected subdivision

2026-09-29. Completed: 44 preparation/time rows and 513 numerical checks,
all passed. This uses the existing held BS carrier and dynamical incidence,
not an added scalar probe, fitted rotation curve, or new hopping law.

## Scientific result

Replacing an occupied edge by a connected three-edge path changes native
carrier transfer between the same old endpoints under unchanged microscopic
coefficients and clock. The change survives quantum incidence dynamics;
the graph need not be artificially frozen to obtain a measurable distinction.
The larger network is therefore not an operationally identical relabeling
for this specified prepared carrier and readout.

Quantum incidence also supplies an exact extra route: a flip can reopen the
removed direct edge before the carrier hops. The unconditional short-time
arrival probability begins `tau^4/144`, whereas the frozen subdivided cycle
and tree begin `tau^6/576` and `tau^6/2304`. The exact Hamiltonian powers
verify these coefficients independently of finite-time approximation.
Returning to the original graph at readout does not remove virtual
flip–hop–flip histories, so postselection is not frozen-graph evolution.

Representative predeclared readouts below give unconditional old-endpoint
arrival probability. The full eleven-time census remains in the result.

| Prepared graph | tau=1, full native | tau=1, frozen control | tau=pi, full native | tau=pi, frozen control |
|---|---:|---:|---:|---:|
| Original four-cycle | 0.17486058 | 0.17701835 | 0.00633109 | 0 |
| Subdivided six-cycle | 0.00162277 | 0.00153090 | 0.43613979 | 0.44444444 |
| Original four-node tree | 0.20106941 | 0.21014055 | 0.36831479 | 0.37131318 |
| Subdivided six-node tree | 0.00058463 | 0.00039163 | 0.14264964 | 0.14501533 |

These finite coherent systems have interference and revivals. This is not
a claim that the longer route has a smaller arrival probability at every
time. A physical distance or universal propagation speed is not inferred by
taking one of these probabilities as a ruler calibration.

The smallest exact prepared-graph probability across the stated readouts
is 0.90012/0.87055 for the original cycle/tree and 0.92166/0.90615 for their
subdivisions. Full connectedness is higher: minima 0.99432/0.89781 and
0.99744/0.93029 respectively. These are sampled-time minima, not guarantees
between samples or first-passage probabilities. Native degree/bias detuning
allows substantial persistence even when the uniform norm bound is useless.

The largest absolute difference between full and frozen reader probabilities
in the complete census is 0.014565. A small absolute difference can be large
relative to an initially tiny frozen-path signal: at tau=1/32, the subdivided
cycle has full arrival 6.5827e-9 versus frozen 1.6167e-12. Both effects are
retained instead of declaring either frozen geometry or shortcuts universally
dominant.

## Work, scope and verification

The current-square term contributes the required degree-dependent onsite
energy; a localized carrier's zero mean current does not remove it. Carrier
injection costs 1.5 in each preparation. Connected subdivision raises the
initial mean energy by exactly 10: 21.5 to 31.5 for the cycle, 15.5 to 25.5
for the tree. This is a comparison of explicitly prepared states, not an
autonomous creation event or a zero-cost insertion. The previous all-blank
growth experiment is separate, including its different anchored tree.

All noncarrier registers are blank and copying is off. This exact invariant
sector tests native transfer, not production of new records or photons.
The microscopic clock remains uncalibrated to physical time/length/volume.
The next physical question is how an actual formation history fixes this
operational geometry and couples it to the common gravity/expansion model.

Two independent operator assemblies and time-action algorithms were used:
matrix-free Chebyshev/FFT coefficients and row-sparse scaled Taylor. The
largest vector has 3,072 components. Their largest vector disagreement is
2.3011e-14; N=2 also has a dense 64-state eigensystem oracle. Maximum mean
energy error is 5.8975e-13, variance error 2.1146e-11. Exact current continuity,
Schur complements, cycle spectra/amplitudes and leakage bounds all pass.
Analytic truncation/alias bounds do not claim to bound floating-point roundoff.

The sole worker completed in 8.8143 seconds with measured peak self RSS
46,579,712 bytes, and exited. No large dense N=3 matrix, installation,
remote job, arbitrary wall deadline or checkpoint framework was needed.
Root read the whole source and protocol before freezing/executing. The
analytical note had independent pre-execution review; the separate source
and saved-result audit is post-execution and must not be dated as a preflight.

## Evidence

- `NATIVE_CARRIER_RULER_PATHWAY_V001.md` and its analytical review.
- `NATIVE_CARRIER_RULER_NUMERICAL_PROTOCOL_V001.md` and
  `native_carrier_ruler_v001.py`.
- `NATIVE_CARRIER_RULER_V001_FROZEN.json`, SHA-256
  `e507c9efbf07d5a3106cf96c4bbaa4f6940e68dd93d308a5e79ccc8b13c43abb`.
- `NATIVE_CARRIER_RULER_V001_RESULTS.json`, SHA-256
  `f170be1dc580c2c0c2f3ebfd1740d1e728a69970c5ba4acf1d3dfc0a25b5713b`.
- `NATIVE_CARRIER_RULER_V001_RESULT_REVIEW.md`: independent post-run source
  and saved-result review accepted; all 2,848 independent arithmetic checks
  passed without rerunning propagation.

The worker emitted complete JSON to stdout; root published it additively
using apply_patch. Original source and earlier evidence were not overwritten.
