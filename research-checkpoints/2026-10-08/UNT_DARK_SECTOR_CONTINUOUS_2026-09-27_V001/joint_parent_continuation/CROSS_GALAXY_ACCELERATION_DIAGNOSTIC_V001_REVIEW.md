# Cross-galaxy residual acceleration: independent review

2026-09-28. Saved-data arithmetic only; no new field, curve fit, threshold fit,
sample cut or constitutive-law inversion.

**The tabulated results do not identify one common transition acceleration.**
Both galaxies develop an outer positive residual at sub-a0 acceleration, but
their final sign-change brackets are distinct. That distinction usefully tests
a proposed mechanism: it must account for the different sources/history/geometry,
not merely assert one threshold from the shared sign of the outer residual.

## Definitions and independent check

For every retained row, `g_obs/a0 = v_obs²/(R*a0)` and
`g_pred/a0 = v_pred²/(R*a0)`, with the same fixed `a0=1.2e-10 m/s²` and
`1 kpc=3.085677581491367e19 m`. Velocity units are converted explicitly.
The terminal positive run is the final contiguous sequence with
`v_pred-v_obs>0`; its bracket is the immediately preceding nonpositive row
and the first row in that sequence. No row is removed from the original scores.

The independent audit authenticated both original freezes and their member
hashes, the original receipts and field/comparison payloads. It independently
regenerated all sign changes, terminal runs, acceleration values and maxima.
The subsequently read parent script/result agree: 990 acceleration/row
arithmetic comparisons pass, maximum scaled discrepancy `4.44090e-16`.
All 43 NGC3198 rows and all 12 DDO154 rows are retained for each paired source
reduction—110 stored rows, but only two different galaxies.

## Terminal sign-change brackets

| Source reduction | Radius bracket, kpc | Observed g/a0 at bracket endpoints | Predicted g/a0 at endpoints | Terminal positive rows |
|---|---:|---:|---:|---:|
| NGC3198 modern 40 arcsec | 14.05 → 16.07 | 0.473796 → 0.393401 | 0.459436 → 0.415054 | 15 |
| NGC3198 modern 120 arcsec | 14.05 → 16.07 | 0.473796 → 0.393401 | 0.469284 → 0.418724 | 15 |
| DDO154 natural map | 3.682673 → 4.204208 | 0.145873 → 0.137704 | 0.145185 → 0.147270 | 5 |
| DDO154 robust map | 3.682673 → 4.204208 | 0.145873 → 0.137704 | 0.145280 → 0.146885 | 5 |

The observed-acceleration intervals do not overlap: even the nearest endpoints
differ by a factor of approximately 2.70. The predicted-acceleration brackets
are also separate. In DDO154 the predicted acceleration actually rises across
this particular final crossing; a unique monotonically decreasing local
acceleration threshold is not established by the radius sequence.

These are exact signs of the saved point estimates, not confidence intervals
for a physical transition. In particular the last preceding DDO154 residuals
are only -0.10537/-0.09069 km/s, smaller than its quoted 0.2-km/s error and not
secured by a full numerical/observational covariance model. An exact-sign
definition must not be reinterpreted as a statistically robust boundary.

All earlier sign changes remain visible:

- NGC3198 40: +→− at 2.57–2.89; −→+ at 7.06–8.04; +→− at 9.04–10.04;
  −→+ at 14.05–16.07 kpc.
- NGC3198 120: +→− at 2.57–2.89; −→+ at 5.78–6.10; +→− at 9.04–10.04;
  −→+ at 14.05–16.07 kpc.
- Both DDO154 maps: −→+ at 2.628960–3.150495; +→− at
  3.150495–3.682673; −→+ at 3.682673–4.204208 kpc.

## Maximum excess within the terminal run

| Source reduction | Maximum Δg/a0 | Radius of maximum, kpc | Maximum Δg/g_obs anywhere in terminal run |
|---|---:|---:|---:|
| NGC3198 40 | 0.05687760 | 34.06 | 32.7487% at 34.06 kpc |
| NGC3198 120 | 0.06603200 | 30.08 | 34.5031% at 30.08 kpc |
| DDO154 natural | 0.04621921 | 6.300990 | 52.0883% at 6.300990 kpc |
| DDO154 robust | 0.04487723 | 5.779455 | 50.5625% at 6.300990 kpc |

The similar order of magnitude of the absolute maxima, approximately
0.045–0.066 a0, is a post-existing-data maximum statistic. It is not the
transition acceleration, an independently discovered constant acceleration
offset or a measured new constitutive law. In the robust DDO154 case even the
maximum absolute and maximum fractional excess occur at different rows.

## Scope and custody

The useful common observation is outer overresponse in the frozen conditional
field calculation, across two distinct galaxies. No single precise transition
scale follows. Paired map weights or annular reductions are correlated source
representations, not additional independent galaxies. Source geometry,
kinematic-product mismatch, omitted matter and covariance limitations are
unchanged. Disk geometry also prevents reading a scalar constitutive function
directly from a radial force ratio without solving its field problem.

Reviewed parent script:
`cross_galaxy_acceleration_diagnostic_v001.py`, SHA-256
`c9be5c2391ebc854db3c60e4d40088abb48321fe79ec7e16fc15bd6a7fa587c6`.
Reviewed complete result:
`CROSS_GALAXY_ACCELERATION_DIAGNOSTIC_V001.json`, SHA-256
`a047b6973bc2623488af30ac26a404141562e0a039f0070460f9b3c52f1e82f4`.
Its flat payload digest is
`d478a42119b1ecf4f5db740246a7dba43b8bce4a8ddcc276deb45367cd518ba3`;
all original input identities are preserved inside it. No frozen input or
existing result was edited in this review.
