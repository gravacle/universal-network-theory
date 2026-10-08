# Independent distance-only and complete-source summary review

2026-09-28. Read-only audit plus independent arithmetic on saved results.
No propagation, PDE, source edit, new fit choice or frozen-file change.
I authored the earlier HALOGAS source/queue implementation, but not these
two diagnostic scripts. This is an implementation/arithmetic and scientific
scope review, not a new independent observational replication.

## Verdict and exact scaling

The seven-source, 28-fit diagnostic is correct. A distance change improves
amplitude but **does not remove the remaining radial-shape discrepancy**.
These are already exposed-data, in-sample fits; they are not holdout evidence.

For the fixed angular source and acceleration law, let `d=D/13.8` and
`Phi_D(x)=d*Phi_0(x/d)`. Then `grad Phi_D=grad Phi_0(x/d)` and

```
div[mu(|grad Phi_D|) grad Phi_D] = (1/d)*4*pi*G*rho_0(x/d).
```

Thus `rho_D(x)=rho_0(x/d)/d`, mass scales as `d^2`, and at the same angular
row `v_D=sqrt(d)*v_0`. This includes scaling every source length and the
finite-box completion, not merely moving radial labels on an unchanged
physical disk. Fixed angular surface densities, M/L, geometry, a0 and shape
parameters are essential. Additional distance-dependent observational
calibration or external environments would be different hypotheses.

Minimizing `sum w*(s*v_model-v_obs)^2` gives exactly
`s=sum(w*v_model*v_obs)/sum(w*v_model^2)`, with `D=13.8*s^2`.
The declared distance-interval solution is its projection onto the allowed
positive-amplitude interval. All seven optima under both weight conventions
already lie within 12.3–15.3 Mpc, so each bounded result correctly equals its
unconstrained counterpart. This interval is treated as a comparison bound,
not as a fitted posterior or a confidence statement.

## Complete fit census

All fits use all 43 rows. “RMS >=2” means the same angular row subset whose
original 13.8-Mpc radii were >=2 kpc, not a new physical-radius cut after D
changes. Distances are Mpc and RMS values are km/s.

| Source | Equal-weight D | Equal RMS >=2 | Quoted-error-weight D | Error-weight RMS >=2 |
|---|---:|---:|---:|---:|
| Original HI1/H21 | 13.94915 | 11.0065 | 14.51080 | 10.9209 |
| Original HI0/H21 | 13.93244 | 11.1010 | 14.49756 | 11.0193 |
| Original HI1/H20 | 13.97337 | 10.8714 | 14.49492 | 10.7658 |
| Original HI0/H20 | 13.95657 | 10.9669 | 14.48170 | 10.8650 |
| Fixed calibrated stars, old HI1/H21 | 12.45456 | 8.2935 | 12.93114 | 8.0693 |
| HALOGAS retained 40 arcsec | 12.35061 | 9.0330 | 12.79618 | 8.8270 |
| HALOGAS retained 120 arcsec | 12.33415 | 8.8511 | 12.75550 | 8.6348 |

For the modern 40/120 representations, the equal-weight fits give outermost
predictions 157.447/156.649 km/s versus observed 149. The quoted-error-weight
fits give 160.262/159.302 km/s. In the equal-weight fits the mean residual
over the original 2–12-kpc rows is -8.547/-8.240 km/s, while the mean over
rows >=20 kpc is +6.977/+6.770 km/s: an amplitude compromise remains.
Those extra group means are descriptive audit arithmetic, not further fits
or a new acceptance criterion. Quoted-error weights omit source/geometry
covariances; their objectives are not significance estimates.

A particularly direct, amplitude-independent witness uses the already
reported rows at 12.05 and 44.08 kpc. Their observed speed ratio is
`149/156=0.955128`; the 40/120 modeled ratios are `1.069619/1.071207`.
Distance cannot change either modeled ratio. Matching the two individual
central measurements separately would require distances 13.8716 versus
11.0609 Mpc for the 40-arcsec source, or 14.0363 versus 11.1591 Mpc for the
120-arcsec source. This is a transparent shape diagnostic, not a two-point
statistical exclusion and not a replacement for the full 43-row audit.

## Complete HALOGAS summary and figure

Authenticated all eight cases and all 62 numerical checks. Both source
representations and both equations have their complete 43 N512 rows in the
summary; the smaller-grid and larger-domain qualification values are retained.
The common stellar/H2 masses agree and the HI+He masses agree to rounding.

At the original fixed 13.8-Mpc distance, nonlinear RMS over original R>=2
is 10.5644/10.4642 km/s (40/120), versus Newtonian 56.8045/56.7672 km/s.
The calibrated old-gas nonlinear comparison is 9.5770 km/s. Thus the modern
source reduces the outermost prediction from 172.792 to 166.429/165.696
km/s, but does not improve every radius or the whole-curve RMS.

The retained mesh-force changes are 0.70897%/0.43792%; larger-domain changes
are 0.008336%/0.008558%. These are inherited force diagnostics, not velocity
likelihood errors. The figure was visually inspected: both modern curves,
both overlapping Newtonian curves, old-gas comparison, all observed rows and
error bars, residual panel and source-scope caption are present. No source
was selected or omitted for a favorable outcome.

## Custody and audit method

Read both complete scripts. Independently verified the flat canonical seals
by excluding only each record's own `payload_sha256`; checked all recorded
input/script hashes, the final eight-case wrapper and its case-file hashes,
each checked case's original freeze and payload, and the PNG hash. Recomputed
all 28 amplitude scales, distances, objectives, 43 residual vectors, subset
counts/RMS values and last-row predictions directly from the authenticated
source comparisons. Maximum difference from saved numbers was zero in this
independent arithmetic pass. Verified the summary's complete row equality,
component masses, mesh/domain values and all subset RMS values.

- Distance diagnostic SHA-256:
  `03725a70282dd03a8d087e16952af31e98a9ead1dbeb1e0d1ddf6dd063dabd05`.
- Complete source summary SHA-256:
  `ba6ef4ce4fd120e3861291a714030c7467f771fea61525048c5336aaae75cf69`.
- Figure SHA-256:
  `269635424533005df322bae4451fba4d45927f215e7752ab0ba8a1bd2e26d12c`.

No blocking arithmetic, census, custody or plot-integrity issue was found.
The result narrows the next physical question to source/geometry or response
shape; it does not authorize choosing whichever adjustment best fits this
already exposed galaxy, and it does not establish a complete UNT dark-sector
explanation.
