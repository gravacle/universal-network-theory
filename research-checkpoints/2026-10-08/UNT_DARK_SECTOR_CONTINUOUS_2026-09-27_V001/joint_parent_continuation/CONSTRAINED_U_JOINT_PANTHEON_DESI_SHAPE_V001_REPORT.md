# Conditional shared SNe plus BAO late-shape comparison

NUMERICAL_PASS

1590 full-covariance SNe and13 full-covariance BAO rows. Their likelihood product assumes zero cross-survey covariance.
All four fixed native epsilon curves are retained with M+A nuisances; comparator fits one common Omega_m plus M+A.
The eps1e-6 physically predicted ruler interval is copied separately, without refitting. Wide-epsilon physical rulers remain open.

| Family | Grid/SN/BAO order | Common Omega_m | Joint score | SN score | BAO score | M | Aref |
|---|---|---:|---:|---:|---:|---:|---:|
| MATCHED_FIXED_RADIATION | 257/16/48 | 0.303930250855 | 1416.18266116 | 1405.29390265 | 10.888758504 | 23.7983142079 | 29.676758149 |
| MATCHED_FIXED_RADIATION | 513/32/96 | 0.303930244292 | 1416.18266116 | 1405.29390381 | 10.8887573487 | 23.7983142057 | 29.6767580002 |
| ZERO_RADIATION_SUPPLEMENT | 257/16/48 | 0.304214198574 | 1416.13917288 | 1405.26927382 | 10.869899056 | 23.7983618332 | 29.6786041055 |
| ZERO_RADIATION_SUPPLEMENT | 513/32/96 | 0.304214214159 | 1416.13917288 | 1405.2692711 | 10.8699017857 | 23.7983618383 | 29.6786044588 |

| Fixed epsilon | Copied SN score | Profiled BAO score | Joint score | Native inferred Htoday*r_d km/s |
|---|---:|---:|---:|---:|
| 1e-06 | 1406.39688975 | 10.3012112161 | 1416.69810097 | 10145.90451566607 |
| 1e-05 | 1406.39683661 | 10.3012847419 | 1416.69812135 | 10145.900900845823 |
| 1e-04 | 1406.39630558 | 10.3020210541 | 1416.69832663 | 10145.864768343654 |
| 1e-03 | 1406.39102498 | 10.3094908575 | 1416.70051583 | 10145.504648067576 |

Aref=c/(Href*r_d); native Href=Hstar and Htoday*r_d=c*E(1)/Aref. No H0 or physical ruler is separately measured.
Primary matched radiation and zero-radiation supplement are both retained, without outcome selection. No epsilon adoption, p-value, superiority, blind validation or full early-universe joint inference. All numerical failures and original controls remain.
