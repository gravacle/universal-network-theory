# Independent descriptive-summary and distance-diagnostic review

Accepted. These are post-exposure summaries of existing fields, not new
force solves, fits of source shape, or held-out predictions. No numerical
worker was run for this review.

Read both scripts before execution. The complete eight-case summary and
all source/model/control pairings were consistent. Before the distance
script ran, the reviewer requested two corrections: authenticate and retain
the completed eight-case index, and distinguish unchanged angular surface
density from the distance-scaled three-dimensional density. Both corrections
are present in the executed source.

After execution, independently verified the canonical seals, script/input
hashes, all 43 copied rows per fine case, all RMS values and all seven
distance-case identities. All 28 stated fit checks pass; independent
recalculation reproduces each speed multiplier, inferred distance, weighted
objective, complete 43-element residual vector and retained-group RMS.

The exact scaling used is appropriate to the stated isolated source problem:
for `d=D/D0`, all physical lengths scale by d, surface density at fixed
angle stays fixed, `rho_D(x)=rho_0(x/d)/d`, and
`Phi_D(x)=d Phi_0(x/d)`. Thus `v_D(theta)=sqrt(d) v_0(theta)` with the same
acceleration-dependent law. It changes the overall speed amplitude, not
its angular shape. The least-squares minimum in the speed multiplier is
`s=sum(w v_model v_obs)/sum(w v_model^2)`; clipping s to the distance interval
gives the constrained minimum. Keeping groups labelled by their **original**
radius avoids silently changing which angular observations enter a summary.

All fourteen unconstrained optima already lie inside the declared
12.3–15.3-Mpc comparison interval, so the bounded versions are identical.
For the modern gas sources:

| Source | Objective weights | In-sample D (Mpc) | RMS at original R≥2 kpc (km/s) | Last-point speed (km/s) |
|---|---|---:|---:|---:|
| 40 arcsec | Equal, all 43 | 12.35061 | 9.03296 | 157.44715 |
| 120 arcsec | Equal, all 43 | 12.33415 | 8.85109 | 156.64872 |
| 40 arcsec | Quoted inverse variance, all 43 | 12.79618 | 8.82698 | 160.26209 |
| 120 arcsec | Quoted inverse variance, all 43 | 12.75550 | 8.63485 | 159.30187 |

The last observation is 149 km/s. The old calibrated gas control also improves
under this one-amplitude diagnostic: equal-weight D=12.45456 Mpc gives
R≥2-kpc RMS 8.29347 km/s; inverse-variance D=12.93114 Mpc gives 8.06933 km/s.
All original uncalibrated alternatives remain in the saved seven-source
census, rather than selecting a photometric convention by its fitted result.

This shows that a distance-like amplitude change can explain part of the
residual but does not remove the source-dependent shape discrepancy. The
reported optima are conditional in-sample fit parameters, not new independent
distance measurements. The published interval is a declared bound, not a
prior/posterior or confidence calculation. Quoted velocity errors do not
include the correlated source, geometry or reconstruction uncertainty.

The summary/figure code retains both modern widths, both Newtonian controls,
all observed rows and signed residuals. This review checks its source and
saved numerical content; it does not claim a separate visual-layout review.

Reviewed output SHA-256 identities:

- `HALOGAS_FIELD_DESCRIPTIVE_SUMMARY.json`:
  `ba6ef4ce4fd120e3861291a714030c7467f771fea61525048c5336aaae75cf69`
- `DISTANCE_ONLY_DIAGNOSTIC.json`:
  `03725a70282dd03a8d087e16952af31e98a9ead1dbeb1e0d1ddf6dd063dabd05`

No source or scientific acceptance threshold was changed after output.
