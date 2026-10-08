# Galaxy measurements weakly constrain the shared saturation scale

2026-10-03. New fixed-source NGC3198 sensitivity calculation, using saved
full fields rather than a new nonlinear fit. Three serial NumPy workers
completed with all revised numerical acceptance controls passing. This is
a local development-data result, not an observational success for UNT.

## Result and practical meaning

For the inherited HALOGAS40 source and r=25.51664211557329, define
d_i=partial v_i/partial ln r at the43 existing observation radii. Holding
the baryonic source, a0, distances and inclination fixed,

| Saved field | max abs d in km/s | sum (d/error)^2 | Inverse derivative norm |
| --- | ---: | ---: | ---: |
| N256 L255 | 1.007745836 | .465137073 | 1.46625505 |
| N512 L255 | 1.009548790 | .464917072 | 1.46660193 |
| N320 L1023 | 1.007746061 | .465141817 | 1.46624758 |

The last column is 1/sqrt[I], I=sum(d/error)^2. It is NOT a confidence
interval or the curvature of the actual nonlinear fit. Source/nuisance
projection, residual-dependent second derivatives and a wider parameter
range were not fitted. All observations and residuals were already exposed.

The new geometric-family expansion ceiling requires r>33.3191 for one
exposed baryon reference, a logarithmic displacement .266799625. The LOCAL
linear forecast of its squared prediction displacement is .033093746 in
the N512 diagonal-error norm, or norm .1819. Its largest predicted velocity
shift is approximately .2693 km/s. This is small relative to the collective
quoted errors even with source nuisances held fixed. It demonstrates weak
local leverage, not a verified finite-r fit or a global bound on r.

Important correction to output terminology: JSON key
linear_forecast_delta_chi2 contains ONLY (delta ln r)^2 I, the squared
prediction-shift norm. It is NOT the change in observed chi-square. At an
imperfect baseline that change also has the linear term
2 delta ln r (v_model-v_observed)^T W d, even before nonlinear corrections.
JSON bytes are preserved and interpreted with this correction. Likewise
local_curvature_scale_ln_r is merely the inverse derivative norm above.

The physical implication is narrower and useful: these particular
low-field galaxy curves cannot be assumed to determine the saturation
scale merely because they constrain the leading flat-rotation scale a0.
The old r was chosen from cosmology. Do not call the resulting expansion
normalization a galaxy-only prediction or repeat low-field sweeps hoping
that the same data become a precise independent calibration.

## Numerical qualification and preserved failed attempts

The full discrete tangent differentiates the transverse gradients, source
law and BOTH outer-boundary derivatives; the baryonic bottom flux is fixed.
The nonsymmetric Jacobian uses flexible GMRES, not the frozen-mu PCG matrix.
Existing code, sources, solver fields and observation errors were unchanged.

V001 stopped before solving: one field-direction finite difference failed
at1.195e-5 versus1e-5. V002 retained this failure because longdouble is only
float64 on this runtime, not genuinely higher precision. Both attempts and
their original thresholds remain. V003 changed the validation method, not
the physical equations or solver tolerances: an independently differentiated
complete residual uses complex steps1e-20 and1e-24, with1e-10 acceptance.
The old finite-difference errors remain visible as arithmetic diagnostics.
Parameter-direction finite differences remain acceptance tests. Independent
internal source review checked this repair and the complete discrete action.

All complex-step discrepancies are <=1.253e-13. True tangent residuals
relative to the small parameter RHS are8.494e-10,6.195e-10 and3.164e-10.
The saved-base correction is only3.64e-6,9.14e-6 and7.19e-6 of the maximum
velocity sensitivity. Re-evaluating the SAME tangent at the corrected base
gives residuals below8.50e-10, within the frozen1e-3 diagnostic gate.
No corrected field overwrites a saved one.

The derivative-specific mesh change is .00822012 (0.822%) in max norm;
the domain change is1.83577e-6. Both pass the prospective5% gate. Run times
were15.095,75.758 and31.551 seconds, with peak self RSS below280MB.
No workers overlapped. The120-arcsec representation, DDO154, a0/nuisance
derivatives and global fits were NOT executed; no results are imputed.
This qualifies the stated40-arcsec fixed-source local diagnostic only.

The protocols are GALAXY_SATURATION_TANGENT_V001.md through V003.md.
The executed successful script is galaxy_saturation_tangent_v003.py,
SHA256 2f0b804808d600b92ba23bea73f9087d94e8e2cedc4e6c73d2c0ffd15a4c0bbd.
The three successful JSON files use prefix
GALAXY_SATURATION_TANGENT_V003_40_ followed by N256_L255, N512_L255 and
N320_L1023. They authenticate the original fields and store all controls
and43 velocity sensitivities. No native formation or Stage3 lane is closed.
