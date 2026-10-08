# FIRAS source-screen independent saved-result audit V001

Accepted as a conditional residual-space source-template screen, not a full FIRAS likelihood or a cosmological-origin result. No scientific producer, fit optimizer, or history evolution was rerun.

## Binding and arithmetic

- Original result `FIRAS_SOURCE_SCREEN_V001.json`: SHA256 `51ff63572314134612877be2a89f157fab6b1841861b80f6a6d81dd5e67471e9`.
- Frozen receipt: `40612c7202e74d400efb1be0cd28b022d037ad1d4dcd4d4d23afeb97958f10eb`; all seven member bytes and hashes authenticated.
- Canonical payload: `1e32fec232cd651f206cc50ebad42c42675468af008c78df9cc0055058967adb`.
- Reviewed producer/protocol: `20d28a7f801f62d7cb5901a4a7e4006f0c8c6407e1265846fe997d5995897f0b` / `d6469e25a8568b79a7c755cb9ea926b319990fa9f0e9d660b70d03563103c049`.
- Saved-only reproducer `firas_source_saved_audit_v001.py`: `903f825e15a5f6b553e49090c5d81ea4851667d8212d04af2aff3372bfab500d`.
- Audit receipt `FIRAS_SOURCE_SAVED_AUDIT_V001.json`: `b08a900cc5f4910499bee9d78c709d24fc8cf0b93dcfc827cfd6a9b18717aaa7`.

All 1,914 independent saved-arithmetic checks passed, retaining six baselines and all 90 source rows. They reconstruct the 43-channel covariance from the published lag sequence, invert it independently of producer Cholesky, check saved model/residual vectors, normal equations, coefficient covariance, projected template norms, profile curvature, bands, source-energy/number conversions and exact degeneracies. All 508 original controls remain recorded; these are numerical checks, not independent physical tests. Producer runtime was 0.029745 s.

The first audit attempt is preserved in `FIRAS_SOURCE_SAVED_AUDIT_V001_ATTEMPT_001.json` (SHA `a78b26a80ac0b2ef256106c0e1e225ce3104c044ee09beea0b00b13e5fe2d371`). Its failures were audit-local: a transcribed freeze hash omitted one `d4`, and exact float equality compared independently evaluated mixture endpoints. Correcting that pin and using the existing audit numerical comparison resolved them. No original input, source, result, or scientific criterion changed.

## What the screen actually finds

The maximum absolute identifiable source amplitude divided by its conditional standard error is 0.509861. Every nonnegative source band begins at zero: none of these templates is detected. Twelve rows are exactly unidentifiable: six inverse-Planck-tangent directions absorbed by temperature and six equal-temperature grey-exchange directions with zero template.

The following are ranges of the nominal profile upper amplitude across **all six** predeclared temperature/foreground choices, not selection of a preferred nuisance model:

| Bath/initial temperature ratio | Grey exchange upper amplitude | Pure emission upper amplitude |
|---|---:|---:|
| 0.5 | 1.1221e-4–1.4258e-4 | 4.9913e-4–5.3100e-4 |
| 0.9 | 1.5994e-3–2.5426e-3 | 1.1500e-4–1.4506e-4 |
| 1 | unidentifiable | 1.0843e-4–1.3893e-4 |
| 1.1 | 1.3939e-3–2.5455e-3 | 1.1585e-4–1.4491e-4 |
| 4/3 | 1.1546e-4–2.4769e-4 | 2.1360e-4–2.2182e-4 |
| 2 | 1.2907e-5–4.0495e-5 | 1.4536e-5–5.8872e-5 |

The roughly fourfold foreground sensitivity of the ratio-two emission limit is material. The ratio-4/3 source is not made spectrally invisible by matching two integrated moments. Conversely, an equal-temperature balanced replacement mechanism cannot be constrained by this zero monopole template alone; native energetics, opacity and angular correlations would require their own model and tests.

## Scope

The public Table 4 column is already temperature/Galactic-subtracted; reconstructed column 2 is not an independent observation. This calculation conditions on local nuisance spans and the supplied channel covariance. Its nominal design degrees of freedom do not reconstruct the earlier subtraction's true degrees of freedom or covariance, and the nuisance alternatives are not a complete systematic-error envelope. The nonnegative intervals use the declared profile increment; they are not asserted universal-coverage cosmological confidence intervals.

No native network emission law, absolute mixing rate, thermal-history origin, inflation premise, or complete competing cosmology has been inferred. These are useful quantitative constraints on explicitly stated local spectral source templates, including real null directions. The primary source/data scope is documented in the pinned protocol and [Fixsen et al.](https://arxiv.org/html/astro-ph/9605054), with the public product described by [NASA LAMBDA](https://lambda.gsfc.nasa.gov/product/cobe/firas_monopole_spect.html).
