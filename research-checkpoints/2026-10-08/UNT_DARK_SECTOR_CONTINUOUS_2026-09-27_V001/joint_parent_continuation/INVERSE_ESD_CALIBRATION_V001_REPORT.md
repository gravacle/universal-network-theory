# What baryonic recalibration would the type contrast require?

2026-10-04. The fixed-force inverse diagnostic is complete and independently
audited. It requires approximately a factor-two differential TOTAL-baryon
scale between the high and low galaxy-type samples under the adopted compact
spherical source and representative-bin mapping. It does not measure that
mass difference or establish that the force law is wrong.

| Classification | Required differential log10 mass scale | Ratio | First-order statistical error (dex) | Residual shape Q, 7 bins/1 constant |
| --- | ---: | ---: | ---: | ---: |
| Red versus blue | .3016052533 | 2.002650915 | .076752190 | 5.248765527 |
| High versus low Sersic | .2942476548 | 1.969008790 | .075142314 | 2.246482085 |

Each summary fits ONE descriptive constant to the seven inferred differences.
No a0, shape, lensing slip or halo parameter was refitted. The two
classifications overlap and are not independent confirmations. Inverse of a
stack is not mean inferred galaxy mass. Catalogue weights, source geometry,
gas distribution, bin-coordinate uncertainty and mass scatter remain open.
The per-bin offsets and conditional bin-coordinate brackets are in the
result, not promoted to seven adjustable prediction parameters.

The covariance uses the full paired 14-by-14 ESD covariance, including the
cross-type blocks. Its inverse-map slope is evaluated at inferred gbar, not
the original catalogue coordinate. All fourteen frozen numerical controls
passed, including doubled inverse-grid resolution, projection round trips,
derivative steps and propagated covariance. Runtime was 1.29 seconds.
Independent saved-only review rebuilt both covariance matrices directly from
the archive and reproduced the summaries within 7e-16; covariance absolute
discrepancies were below 1.4e-17. No force calculation was repeated for that
audit.

Minimum individual ESD signal/noise is 3.21/3.89. Accordingly the tabulated
errors are descriptive delta-method scales, not exact coverage intervals or
rejection significances. In the deep limit, the leading inverse-log bias
is -(sigma_E/E)^2/ln(10), reaching about .04/.03 dex for the weakest individual
measurements. Cancellation in the differential statistic is not guaranteed.

## What external calibration does and does not establish

Brouwer et al. section 5.4 estimates stellar-method offsets .14/.12 dex
for colour/Sersic and selection offsets .027/.021 dex. These are internal
study estimates, not externally certified hard limits. They concern stars,
not all baryons. With the study's cold-gas relation f proportional to
Mstar^(-.69), dln[Mstar(1+f)]/dlnMstar=(1+.31f)/(1+f), so a stellar shift is
not the same total-baryon shift. Extended hot gas remains an independent
uncertainty. The paper itself discusses type-dependent gas as an alternative
explanation; our inverse diagnostic is not discovery of that possibility.
[Primary source, sections 4.3 and 5.2–5.4](https://arxiv.org/html/2106.11677v1).

The next useful data-facing check is therefore a *forward projection* of the
paper's explicit extended-gas benchmark with the same inherited force law,
not an unqualified horizontal mass translation. Preserve nominal failures
and every benchmark. Without actual catalogue weights and independent gas
measurements this remains a sensitivity study, not empirical validation.

Receipt: INVERSE_ESD_CALIBRATION_V001_RESULT.json

SHA256: bf4280d4d9cc40c87ef616e84d4cf6c02def610554d62d1ca4af0115be6e36d7

Protocol, frozen inputs and producer are the adjacent V001 files. Source and
saved-arithmetic review: endpoint_equations_check, 2026-10-04. Internal review
does not substitute for independent observations or the remaining Stage 3
lanes. UNT superiority remains unestablished.
