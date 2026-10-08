# BBN table proxy V001: independent saved-result review

## Verdict and scope

Accepted as the frozen **table-proxy and pinned-interface calculation**, with all original limitations retained. The saved arithmetic audit passes 3,633 checks, maximum scaled difference 1.672e-16; the producer retains 108,679 controls and zero failures. Its status is `COMPLETE_PROXY_AND_INTERFACE_QUALIFICATION`, not completion of conserved-scalar BBN. All 360 labels are present: four inherited spectra, eighteen reference combinations, and five hard gaps. These are parameter/numerical variants, not 360 independent observations.

The review authenticates 81 unique files across 12 manifests and 323 member occurrences, then recombines saved quantities. It does not rerun abundance interpolation, thermal integration, nuclear evolution, oscillator dynamics, or fitting. The underlying interpolants, source semantics, and prospective tests were independently source-reviewed before execution in `BBN_TABLE_PROXY_PREFLIGHT_V001.md`. The shifted-temperature interpolation sensitivity is retained but not independently reevaluated here.

## Custody and a serialization qualification

Exact SHA256 identities:

- Result `BBN_TABLE_PROXY_V001_RESULTS.json`: `de26bdb564d92853211652933456d7b8a594278fd67fb15c50875c66b1ed4ec9`.
- Freeze: `feb45f421c088290013685c28599731d3d45f5519bb0e3312b8907e64c467cdb`.
- Producer: `96059bdb6f236b84e4d82edf2d6dc7c8d6c61b59504fab84831515a636d3a4c0`.
- Protocol: `43227176ed42d0580116e672228aa0cd45ff4b1aec043c4b5e8601977b9d0e98`.
- Interface note: `dd5f14980d2c5a9a7d9a9f552a7f873274348e73c1d933da85eb52df6f472c51`.
- Producer payload: `33b0cabd7c17fb8c27bbe9e3bf128b48324203ec9617c1552a5c46a7e32689b8`.
- Independent reproducer `bbn_table_proxy_saved_audit_v001.py`: `ea08155e1e767a47efca4b0324b3d410c58114e2b83c1f91e8ed048e344a84b6`.
- Independent receipt `BBN_TABLE_PROXY_V001_SAVED_AUDIT.json`: `42c86f8b3d3417bb510a5a0cd6998ce77770ce164a70fd1f2fe4380a11382334`.

The first generic payload verifier refused the result. This is an identified canonicalization issue, not lost result bytes: the frozen producer builds `matched_Delta0` with integer keys 0 through 17, whereas loading JSON makes those keys strings. Sorted encoding then changes their order. Restoring **only that schema-defined key type**, with an exact key census, reproduces the original payload hash above. Generic string-key encoding gives `7d554e1c5e692f74b99913adb3f6fc2ccf7e60dadbf940c65aa7a86f391fa454`. Both hashes and the rule are recorded in the receipt. No frozen bytes, scientific values, or stored hashes were changed. Future consumers need this documented verification rule rather than an unrestricted payload normalization.

## Abundance result and matched baselines

Every gap retains 72 rows. Only the largest gap lies within the published table domain:

| Hard gap R | Late proxy Delta range | Supported rows |
| --- | --- | --- |
| 32 | 2218.84–2878.72 | 0/72 |
| 128 | 349.619–453.645 | 0/72 |
| 512 | 55.0617–71.4447 | 0/72 |
| 2048 | 8.67167–11.2518 | 0/72 |
| 8192 | 1.36570–1.77205 | 72/72 |

The 288 out-of-domain rows are explicitly unsupported; there is no extrapolated abundance or numerical exclusion for them. For the 72 supported rows:

| Quantity | Proxy prediction | Signed observation residual | Same-baryon increase over Delta=0 |
| --- | --- | --- | --- |
| Helium Y | 0.263441–0.267980 | +0.018141–+0.022680 | +0.016668–+0.021104 |
| D/H | 2.897425e-5–3.186972e-5 | +3.704249e-6–+6.599724e-6 | +4.482599e-6–+6.088868e-6 |

The eighteen matched Delta=0 baselines give Y=0.246673–0.246977 and D/H=2.449165e-5–2.578086e-5. Their marginal standardized residual ranges are respectively +0.404 to +0.493 and −1.949 to +1.261. Adding the declared extra component raises the supported proxy ranges to +5.333 to +6.667 for helium and +8.822 to +15.215 for deuterium. These are the frozen **descriptive marginal** residuals divided by the quadrature sum of the table-theory and observational standard deviations. They are not a joint likelihood, a confidence exclusion, or a propagated shared-parameter posterior. In particular, the inherited conditional baryon benchmarks and their uncertainties are not freshly inferred or propagated here, and the deuterium data are not an unused holdout.

This is genuine adverse evidence for the specified supported proxy states: the increases are much larger than the prospective numerical allowances (2e-5 in Y and 5e-8 in D/H). The producer's largest target cubic-versus-quadratic differences are 2.0812e-6 and 4.0892e-11, respectively; all prospective numerical controls pass. The conclusion is not explained away by interpolation precision. A different shared gap/state calibration is a new transparently counted inference task, not a reason to alter these outcomes.

The declared helium convention remains explicit: the atomic-mass table column is retained but not silently substituted for the scored nucleon-mass quantity; the D-only denominator correction and the coefficient of the unprovided helium-3 term are retained. No bound on an unprovided helium-3 abundance is invented.

## Thermal-interface meaning

The pinned ordinary-neutrino heating history and supplied plasma interpolation distinguish the official table proxy from a separately conserved extra scalar. The endpoint entropy factor and the owned scale-factor normalization cancel; both factors are explicitly retained and equal one for this saved endpoint. The all-temperature logarithmic ratio enclosure is

`L in [-3.4122682e-7, 0.00554170554]`.

The audit independently recombines the heating/derivative-drift split, resolution intersection, endpoint product, fractional H envelope, and finite-gap bound from their saved inputs. For R=8192 the conservative proxy-minus-conserved fractional H range over all supported rows is contained in `[-1.04187e-7, +0.001691643]` under that fixed ordinary history. The all-gap upper bound reaches approximately 0.002774. These are background-expansion envelopes, **not abundance error bars**, and do not validate altered neutrino decoupling or the feedback of a new self-consistent thermal solution.

At 10 keV, the photon-temperature reference A is 42,577,887.64, while the heating-aware lower bound is 42,354,095.82. The R=8192 finite-gap fractional energy bound is 1.3880e-7–1.5811e-7; the other gaps have smaller bounds. Thus the same-action high-temperature radiation approximation is tightly controlled within this stated mapping. The main remaining distinction is not a large finite-gap energy correction; it is that the table's source history and the true conserved-scalar thermal/nuclear evolution have not been solved as the same system. Padded polynomial bounds qualify the pinned interpolants, not unknown physical QED or nuclear uncertainties.

Every row and the aggregate retain `conserved_scalar_abundance_status=NOT_YET_QUALIFIED`. The proxy tension is useful for designing common-parameter inference, but it must not be relabeled a completed BBN rejection of the covariant candidate, still less of all UNT. Likewise, numerical completion alone is not observational agreement.

Observed producer resources: 1.847073625 s and 32,194,560 bytes peak self RSS, not whole-machine memory.
