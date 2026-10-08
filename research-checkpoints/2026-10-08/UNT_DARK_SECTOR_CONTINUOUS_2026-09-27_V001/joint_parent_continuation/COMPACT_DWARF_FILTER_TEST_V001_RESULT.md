# Compact-dwarf conditional force bound and matched local control

2026-10-05 UTC (2026-10-04 local). Frozen protocols and machine results are
`COMPACT_DWARF_FILTER_TEST_V001*` and `COMPACT_DWARF_LOCAL_CONTROL_V001*`.
No inferred dark mass was used as input. This is a test of a declared
stationary external-field state, not all possible network-clock states.

## Result

The fixed-state, 100 pc filtered model has a strong conditional tension with
Segue 1's published stellar velocities. All six nonlinear branch certificates
and all 40 numerical controls pass. The conservative aperture upper bound
is at most 0.76717 km/s across the declared cases, versus a published
intrinsic-dispersion estimate near 3.7 km/s. This is not a fitted likelihood,
posterior confidence exclusion, or rejection of UNT generally.

| Stellar mass (nominal solar masses) | External acceleration / a0 | Filtered aperture upper bound (km/s) | Matched ell=0 upper bound (km/s) |
| --- | --- | --- | --- |
| 340 | 0.5 | 0.242600 | 0.706983 |
| 1020 | 0.5 | 0.420195 | Uncertified |
| 3400 | 0.5 | 0.767168 | Uncertified |
| 340 | 1.0 | 0.189942 | 0.480410 |
| 1020 | 1.0 | 0.328989 | 0.832095 |
| 3400 | 1.0 | 0.600649 | Uncertified |

The matched local control changes only ell to zero. Its seven arithmetic
controls pass; three self-map tests do not certify their branches. Those
three entries are unknown under this proof, not physical failures. The
three certified local cases show that the warning is not unique to the
100 pc filter. Loose upper bounds do not rank actual model predictions.

## What was assumed and bounded

Ordinary mass and tracer light share a spherical Plummer profile with
projected half-light radius 28 pc. Nominal luminosity 340 solar luminosities
is multiplied by stellar M/L values 1, 3 and 10. This is a declared range,
not a marginalized population posterior. The aperture is 67 pc; ell is
100 pc, a0=1.0059833281731022e-10 m/s² and r=25.51664211557329.
External fields 0.5a0 and a0 are explicit state assumptions, not a complete
Milky Way environment posterior.

The Plummer Gaussian-mixture representation and a Wiener-norm contraction
bound give the full nonlinear anomalous force upper bound within the
frozen ball. In the ell=0 control the exact input norm is
`epsilon0=4GM/(pi a² e)`. No ball was enlarged after looking at failures.

The stationary integrated stress identity gives
`<v²> <= 3pi GM/(32a) + 2a A`, where A bounds anomalous acceleration.
We use `sigma_LOS² <= <v²>`, without dividing by three. An unbiased
projected-aperture moment is bounded by dividing this second moment by
`Fap=Rap²/(Rap²+a²)`. The argument uses vanishing surface stresses, not a
finite Plummer moment of inertia, which diverges. Real membership-weighted
Gaussian estimators need not equal this luminosity-weighted moment.

## Observational interpretation and alternatives

[Martinez et al.](https://arxiv.org/abs/1008.4585) infer approximately
3.7 (+1.4/-1.1) km/s with hierarchical membership and binary modeling.
Those asymmetric intervals are not a Gaussian significance calculation.
[Simon et al.](https://arxiv.org/html/1007.4198) provide the nominal light,
geometry and spectroscopic selection; the galaxy is elliptical, whereas
this benchmark is spherical. Their inferred dynamical dark mass is not
an input here.

The [2026 archival analysis](https://arxiv.org/html/2602.10200v1) reports
3.97 (+0.97/-0.86) km/s for 53 members with its own selection, including
an aperture of two effective radii and flagged-variable removal. It is
not a new independent realization of all the older measurements and not
the same hierarchical binary-marginalized estimator. Do not multiply these
results as independent likelihoods.

A [tidally disrupting star-cluster realization](https://academic.oup.com/mnras/article/461/4/3630/2608639)
is a genuine non-equilibrium alternative to this test, but uses a chosen
orbit and a Milky Way potential with an analytic dark halo. It is not a
shared UNT prediction. The [measured orbit study](https://arxiv.org/abs/1711.09097)
is relevant to testing such histories. A [compact black-hole alternative](https://arxiv.org/html/2505.06198v2)
adds gravitating mass; it cannot be counted as a stellar-only success.
Binary contamination, selection, geometry, stellar population and tidal
history require an explicit forward comparison before statistical rejection.

## Custody and continuation

The filtered proof/source/results were independently analytically reviewed.
Filtered source SHA256:
`7882b40cde209e76a1806ae0e4c6646dc1b6a9c6023bb1d743d269a6f671f25d`.
Filtered result SHA256:
`e6ddd8aae780f785f12d4973300108815230aceac8bdfdf310c68785f4618258`.
Local source SHA256:
`c9aeaf788f7d5a568d35c17e894f0a7b0d00facf441ecb713d078e45bda4a0ad`.
Local result SHA256:
`e67ea211ddaa89a15c9fe283f59248a9fe02e545228abf45a7528758760ae34b`.
Sequential numerical times: 0.01598 and 0.01502 seconds internally.
All global controls, not merely a row's certificate flag, are required.

Next: derive one physical clock preparation and evolution that selects
external and internal response together. A coordinate transformation alone
does not remove a preferred clock's invariant acceleration. Independently
assigning a Solar, Galactic and satellite clock is extra state fitting.

The independent matched-local audit subsequently accepted all seven controls,
custody hashes, the three quoted aperture bounds and the three correctly
uncertified entries, without rerunning a numerical calculation.
