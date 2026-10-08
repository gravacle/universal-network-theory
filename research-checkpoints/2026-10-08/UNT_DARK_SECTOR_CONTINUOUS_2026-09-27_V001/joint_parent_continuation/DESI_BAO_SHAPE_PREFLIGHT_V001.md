# Independent preflight: DESI DR2 expansion-shape census

2026-09-29. **Accepted for the declared calculation.** This review read the
complete producer, protocol, preselection and external-data README; it did
not execute the producer, calculate an observational score, or select an
outcome. No source or scientific threshold was changed.

## Reviewed identities

| File | SHA-256 |
|---|---|
| `desi_bao_shape_v001.py` | `8c5cb5febaccb1d4320840add24addccd7002ae03905e36876f222256d5fabe6` |
| `DESI_BAO_SHAPE_PROTOCOL_V001.md` | `3144f98ea5f91ce6dec600dc0ab0452de69cb5e3952819be896c7ec403429d2e` |
| Mean data | `9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585` |
| Covariance data | `252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509` |

The last two files reside in `desi_dr2_bao_external_v001/`. Their exact
13-entry ordering agrees with the pinned primary-release files at Cobaya's
`bb0c1c9009dc76d1391300e169e8df38fd1096db` commit. In particular, the final
Ly-alpha pair is **DH then DM**. The separate AP display reverses that pair
only for its two-component presentation, not the scored vector or covariance.
Sources: [pinned mean file](https://raw.githubusercontent.com/CobayaSampler/bao_data/bb0c1c9009dc76d1391300e169e8df38fd1096db/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt),
[pinned covariance](https://raw.githubusercontent.com/CobayaSampler/bao_data/bb0c1c9009dc76d1391300e169e8df38fd1096db/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt),
and [DESI DR2 primary paper](https://arxiv.org/html/2503.14738v3).

## Mathematical and implementation checks

* The adopted flat dust-plus-vacuum shape uses all 18 inherited reference
  rows, with `Omega_b + Omega_exc = 1 - Omega_Lambda`; duplicate shapes are
  retained as reference alternatives, not independent experiments. The same
  shape is recovered whether the two pressureless coefficients are added
  before or after constructing the expansion function.
* The distance formulas and units are correct. A single nonnegative shared
  amplitude `A = c/(H0 rd)` is analytically profiled with the full Cholesky
  covariance. Its derivative, Hessian, active boundary and conditional
  acoustic length are retained. This is one fitted acoustic nuisance, not a
  predicted network sound horizon. The independent direct-covariance solve
  tests the same minimizer and quadratic score.
* The free-shape comparator counts its additional `Omega_m` fit. Both
  257/513 grids, both finite endpoints and every sampled local-minimum
  bracket are retained and refined. This is a numerical profile census,
  not an analytic guarantee of global optimality. Gauss rules are checked
  against each other and a separately constructed Simpson integration.
  The exact dust/vacuum endpoint and synthetic-amplitude controls are
  independent of any desired observed score.
* The six AP ratios use the appropriate full two-row subcovariance and
  delta-method gradient. They are descriptive displays, not an additional
  independently scored or Gaussian ratio likelihood.
* The photon energy-density formula has the correct SI energy units;
  dividing by `c^2` in the gravitational density fraction is necessary and
  present. The 108 radiation sensitivity rows keep the original physical
  dust and vacuum coefficients fixed, so their present Hubble value changes
  by `sqrt(1 + Omega_rad)`. They neither refit nor score the radiation-added
  model. Monotonicity of
  `Omega_rad (1+z)^4 / [Omega_m (1+z)^3 + Omega_Lambda]` gives the stated
  interval bounds for DH, DM and their geometric-mean DV combination.
* Custody checks bind the exact external files, current code/protocol,
  physical interface and inherited reference ancestry. The producer prints
  rather than writes its freeze/results; it imports no previous numerical
  worker. Frozen numerical checks do not encode a preferred physical result.

## What the calculation can establish

This is an outside-calibration, explicitly **not blinded**, comparison of
conditional expansion shapes against survey-inferred BAO distances. A
successful numerical status is not an observational success. Lower fitted
scores alone do not establish predictive or explanatory superiority; the
acoustic amplitude, extra comparator shape freedom, inherited reference
calibration and survey/template assumptions remain visible. The finite-hard
state, clock dynamics and network origin of the physical interface are not
certified by this distance test. Ordinary radiation is an imported diagnostic,
not a demonstration of a network-origin microwave background.
