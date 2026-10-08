# Paired spectral conventions: bounded reference V001

A common static gravitational frequency factor does not supply a ten-percent rotation correction in the ideal paired, axisymmetric spectrum. The approaching/receding normalized wavelength difference cancels the common factor. Unequal rays, time dependence, asymmetric line weights and the actual source/detector clocks require the full model.

This new calculation uses all43 saved FINE_Q3 speeds and all43 observed speeds as separate reference inputs. It changes neither dataset nor the galaxy source. The stated inclination is73degrees. A common special-relativistic systemic reference660km/s is a declared test, not a reconstruction of the actual survey pipeline. The scalar-chart reference uses the positive maximum Phi_observer−Phi_emitter=1.0256198871e−6 as a common wavelength factor, not a derived per-radius optical correction.

With beta=v/c, x=beta sin(i), gamma=(1−beta²)^−1/2 and a common positive factorA:

    lambda_plus/lambda_rest=A gamma(1+x)
    lambda_minus/lambda_rest=A gamma(1−x)
    c(lambda_plus−lambda_minus)/(lambda_plus+lambda_minus)/sin(i)=v

Optical, radio and SR conversion functions are respectively c(q−1), c(1−1/q) and c(q²−1)/(q²+1), whereq=lambda_observed/lambda_rest. Their odd, deprojected difference is retained explicitly. No convention is selected as an actual SPARC re-reduction.

| Synthetic branch | Maximum optical change, km/s | Maximum radio change, km/s | Maximum SR change, km/s |
|---|---:|---:|---:|
| No common systemic factor |0.00002525|0.00002093|3.36e−11|
| Common660km/s SR reference |0.364912|0.364064|0.0008024|
| Same plus conditional common static factor |0.365083|0.364233|0.0008032|

These maxima cover both43-row reference sets. At44.08kpc the saved diagnostic speed is165.5604km/s; it needs a13.5604km/s downward change to enter149±3km/s. The systemic-reference optical and radio changes there are+0.364912 and−0.364064km/s. A convention mismatch at this scale does not supply the required change. The no-systemic SR odd difference agrees with the input at arithmetic precision.

Root PID29763 naturally CLOSED0 on2026-10-07 at02:58:13.154420UTC. Independent algebraic optical/radio and normalized-pair controls have maximum absolute discrepancy4.39116e−11km/s against the predeclared3e−8 gate. This is a synthetic arithmetic/observation reference, not a solved galaxy metric, photon history, atomic-clock correction or physical success.

RESULT SHA256 faf574f9cb4dc3460f441eda50ae2029f5ca855500c1a159bb3e7c010da3c0a5.
RECEIPT SHA256 b0066310bfa4de884e1c825d0855a25f61cd8a1c7452cf0a012f96364751b4e1.
Released source SHA2564c0cfc7cb54b532dc31fb8f5217e1fd916d4e395d1115564d562ddbec4894283; full root/independent static review and guard-only release retained. No producer/helper/operator/field replay occurred. All physical qualification flags remain false.
