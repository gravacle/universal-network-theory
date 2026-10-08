# Independent saved-array audit

2026-10-04. PASS: **7,591/7,591 audit checks**, preserving the original
**1,228/1,228 producer controls**. One 0.200-second audit; no producer
import, inverse rerun, fit, or field evolution. The numerical slot is released.

Authenticated the producer, protocol, result, prior radial result and all
100 prior galaxy receipts. The same 94 eligible galaxies, six exclusions,
1,913 full-radius rows and 981 outer rows are retained. Verified every
source-line/radius/source value and exact inner/outer split, all new and
reference velocity/log-acceleration/error-normalized residuals, per-galaxy
metrics and paired differences, and the galaxy-balanced aggregates.

The independent flux check evaluates the positive angular integral at each
saved g prediction, using Newton iteration for the cubic mode root rather
than the producer's closed form. The relative flux residual is
1.93e-15; independent 64/96-node quadrature differs by 8.69e-16.
This verifies the saved inverse values without solving the galaxy inverse again.

| Saved/recomputed model | Outer velocity MSE (km/s)^2 |
|---|---:|
| New h=g local reference | 285.398202117 |
| Prior bounded response | 285.872069047 |
| Separately calibrated RAR | 285.221205059 |
| Baryons | 3873.052006196 |
| NFW, inner-only 513-grid fit | 988.661224255 |
| ISO, inner-only 513-grid fit | 1702.299750176 |

The new secondary log-acceleration MSE is 0.018982531607 dex^2.
Relative to the prior bounded response the primary mean changes by
-0.473866930 (km/s)^2; relative to RAR it changes by +0.176997059.
These very small differences do not establish observational discrimination.
The old a0 is adopted for the changed parent, while the saved RAR a0 was
separately calibrated. No new calibration was performed here.

Verified beta=0.36025309739497874 and Mcrit=20,034,223.584001154 Msun
for the illustrative ell=100 pc. This dimensional arithmetic is separate
from the score: ell is absent from the local catalogue prediction. The
formal finite-gradient coefficient receives a source-only review in
LINEAR_SOURCE_GALAXY_REFERENCE_V001_REVIEW.md; neither audit supplies a
full asymptotic/existence theorem or a finite-100-pc disk calculation.
All exposed-data, fixed-source, disk-versus-spherical-proxy and finite-halo
comparison qualifications remain. No Cassini pass, native formation,
shared cosmology, blind test, or global superiority follows.

## Custody

- Producer result: `6bef7739471ce1ae5ed0714c3572693162fc2d3ac0780345ba43894ccef947fb`.
- Audit source: `f3d9c27047ff0e2ee753625dc529079869556c547dedb779a65f861272e075b2`.
- Audit JSON: `e8e5caece644461f37389a9aa01b37b24914d47c53b38f268abdfcbb1c470213`.
- Analytic review: `485f42b5eefc24dc36a3107ff2496e7bc45ca18717430ffb35ed23fde4a254a8`.

All frozen input files were read only; the new audit receipt was published
atomically with no-overwrite semantics.
