# Independent review: complete original galaxy queue and response diagnostic

2026-09-28. All16 original galaxy cases and the frozen four-model response
diagnostic were independently audited using their saved fields and readouts.
No PDE, physical propagation, new quadrature, velocity fit or source change
was performed by this review. The additive stellar-calibration comparison
is separate and is not included among these original outcomes.

## Verdict and scientific result

**All original numerical qualifications and diagnostic identities pass.**
For every retained source model, the same fixed conditional network-response
law supplies most of the rotational support missing from the corresponding
ordinary-matter-only Newtonian calculation. No dark halo was included in
any of these16 runs. The residual differences are now much smaller and
structured, rather than an overall lack of the required force.

The result is a no-refit development comparison with an explicitly specified
ordinary-matter source and conditional gravity law. It is not a comparison
against a fitted dark-matter halo, a likelihood-based preference between
complete theories, an independent derivation of the physical law from the
original UNT record equations, or a completed explanation of all dark-sector
observations. The galaxy was exposed development data. The law's acceleration
scale and its second, cosmic-reference calibration were existing inputs;
reproducing those inputs cannot be counted again as independent successes.

## 1. Complete source-model census

`HI1` and `H21` retain their declared exponential continuations; `HI0` and
`H20` truncate the respective profile at its last supplied radius. These
are four prescribed source models, not a confidence interval or an optimized
selection. Every model uses the same stellar profile, conversion, distance,
geometry, gravitational function and calibrated scales.

Each row below reports the finest N512/L255 result, retaining43,37 and21
observed radii for the all-radius, R>=2 and R>=8 summaries, respectively.
All velocities are real in every original case; no negative-force row was
discarded. Units are km/s.

| Source model | Network RMS, all | Network RMS, >=2 | Network RMS, >=8 | Newtonian RMS, all | Newtonian RMS, >=2 | Newtonian RMS, >=8 |
|---|---:|---:|---:|---:|---:|---:|
| HI1_H21 | 13.17366 | 11.14382 | 10.34278 | 59.10226 | 63.42959 | 75.86190 |
| HI0_H21 | 13.22884 | 11.21947 | 10.48847 | 59.07141 | 63.39619 | 75.81284 |
| HI1_H20 | 13.09875 | 11.03782 | 10.40542 | 59.22812 | 63.56590 | 76.16506 |
| HI0_H20 | 13.15342 | 11.11305 | 10.54804 | 59.19719 | 63.53241 | 76.11597 |

The fine network signed residuals remain:

| Source model | Mean >=2 | Mean >=8 | Maximum absolute >=2 |
|---|---:|---:|---:|
| HI1_H21 | -3.87229 | +1.96088 | 19.69241 |
| HI0_H21 | -3.80591 | +2.07557 | 20.35365 |
| HI1_H20 | -3.95245 | +1.57917 | 19.49362 |
| HI0_H20 | -3.88580 | +1.69433 | 20.15707 |

The apparent cancellation in signed means is not pointwise agreement.
Nominal quoted-error squared residuals are retained, but are not interpreted
as a likelihood: source conversions, ring correlations, geometry, warp and
distance systematics are not represented by those quoted errors alone.

The two tails together account for only0.9790112% of the HI1_H21 mass:
H I tail `1.227685025e8` and H2 tail `1.852534356e8` solar masses, compared
with baseline total `3.146255488e10`. Thus the agreement across the four
models tests these particular endpoint continuations, not every uncertainty
in the stellar conversion or three-dimensional mass distribution. A small
tail mass does not imply a uniform small local force effect near a thin-disk
edge; the original edge warnings are retained.

## 2. Numerical qualification independently rechecked

The remote-domain grid is N320/L1023 with the original inner spacing;
the refinement is N512/L255 versus N256/L255. The listed quantities are
maximum force changes at the fixed comparison radii R>=2, not rigorous
error bars or physical uncertainty bounds.

| Source model | Refinement change | Remote-domain change | Maximum five-point Newtonian/ring relative difference |
|---|---:|---:|---:|
| HI1_H21 | 0.4228080% | 0.00984007% | 0.0350766% |
| HI0_H21 | 0.4226579% | 0.00945971% | 0.0350933% |
| HI1_H20 | 0.4277098% | 0.00986758% | 0.0351440% |
| HI0_H20 | 0.4275564% | 0.00948482% | 0.0351605% |

All20 ring comparisons pass their original2% allowance plus retained
quadrature/extrapolation differences. Each original case passes convergence,
global flux balance, exact annular mass, residual and no-clipping criteria;
all92 stored original case checks pass. The pre-existing original stretched
V001 failure is not erased by these V002-based qualified results.

As an independent arithmetic check beyond trusting pass flags, this review
reconstructed the midplane trace from the first two saved vertical samples
of every potential matrix and differentiated it with independently written
nonuniform three-point slope formulas. The largest difference from a saved
radial grid force was `1.182588749149005e-12` in a0 units. Every observed-radius
interpolation and velocity-squared conversion was checked. All192 scalar
RMS/mean/maximum/nominal-error summaries were recomputed; the largest absolute
roundoff difference was `1.4551915228366852e-11` in their respective units.

The measured profiles' mass integrals were also recomputed from their own
linear polynomials and analytic exponential tails, independently of the
density helper's antiderivative: all component masses agree to at most
`4.440892098500626e-16` fractionally. This is numerical input consistency,
not a verification of the physical true mass-to-light ratio.

## 3. What the complete disk diagnostic shows

The frozen postprocessor contains4 models,172 radial records and700
internal checks. All pass. Its input hashes exactly match the16 originals.
An independent scalar implementation of the closed mechanical law, evaluated
on the saved diagnostic values, reproduces the sheet jump, vector/radial
flux inversion, force terms and signed velocity-squared accounting. The
largest scaled difference in this recomputation was `4.720405706490792e-15`.
The source surface densities were independently reconstructed to a maximum
absolute difference of `1.4210854715202004e-14` solar masses/pc². Summary
means/maxima and hard-edge warnings also agree.

An illustrative retained row makes the outer excess concrete. At the last
observed radius44.08 kpc for the original HI1_H21 baseline, the observed
speed is149 km/s. The diagnostic sequence is

| Defined diagnostic | Speed (km/s) |
|---|---:|
| Ideal total-mass deep spherical reference | 149.61376 |
| Deep radial transformation of the actual Newtonian disk field | 160.61214 |
| Full-law radial-only transformation | 165.75734 |
| Full-vector algebraic disk projection | 165.34933 |
| Solved nonlinear disk field | 168.69241 |

Only the last row is the actual nonlinear field solution. The preceding
rows are explicitly defined diagnostics, not alternative solved models.
In the exact signed velocity-squared decomposition at this radius:

| Contribution | (km/s)² |
|---|---:|
| Reference residual relative to observed speed squared | +183.27672 |
| Newtonian disk versus total-mass monopole | +3411.98402 |
| Full law versus its ideal deep form | +1679.23388 |
| Vertical projection | -135.09215 |
| Remaining field/nonlocal-plus-boundary numerical correction | +1116.72646 |
| Total actual residual | +6256.12893 |

Thus the endpoint discrepancy cannot be described simply as an excessive
total-mass asymptotic speed. Finite-radius disk/source geometry, the law's
transition shape, and the remaining solved-field difference all contribute
under this declared decomposition. It is not a unique causal partition;
changing its ordered reference steps would change the assigned terms.

Across all R>=8 baseline rows the *mean* signed contributions are instead
`+2677.61` from law shape, `-1096.71` from disk/monopole geometry,
`-734.63` from vertical projection and `+110.46` from the remaining field,
added to a reference residual of `-297.15`, giving `+659.58 (km/s)²`.
This difference from the endpoint illustrates why a single averaged label
such as “disk geometry causes the excess” would be too broad. Full radial
values for every source are retained in the diagnostic output.

Only the H2-truncated models flag an observed radius within twice its local
radial spacing of a hard truncation:6.43 kpc, close to the6.4 kpc cutoff.
The row remains included. It is not a resolved finite-thickness edge feature.
The inferred vertical field satisfies the sheet boundary condition by
construction; that closure is not an independent vertical measurement.

## 4. Strongest justified dark-sector implication

For this fixed conditional candidate and these stated ordinary-matter
reconstructions, a dark-matter halo is not needed to supply **most of the
observed extra rotational support**. The same law does so in all four
retained source scenarios with no galaxy-specific parameter adjustment.
It still requires the retained residuals and source approximations to be
understood before claiming a satisfactory fit. It does not yet establish
that dark matter is physically absent or superfluous across galaxies,
lensing, clusters and cosmological structure.

The separate25.68% stellar-conversion difference is external to these
outputs, identified from the published light-to-mass conventions and never
fitted to the rotation curve. Its proposed additive comparison keeps both
the original results and changed source identity. It cannot retroactively
turn the present galaxy into a held-out test or establish which mass
conversion is correct.

The related full-pressure theorem likewise remains conditional on the
adopted metric/clock interface and absolute high-field-zero matching.
Its negative proper-slice averaged trace pressure is not directly applicable
to an arbitrary finite galaxy domain with nonzero boundary flux, and it is
not a solved averaged cosmological expansion. Its value is a linked
force/stress constraint within one candidate, not independent empirical
confirmation of a native common parent. See `FULL_RESPONSE_PRESSURE_REVIEW.md`.

## 5. Custody

Authenticated four manifests and every named entry: galaxy29, stretched8,
ring11 and diagnostic7 (overlapping entries are not independent scientific
checks). Verified all16 case identities, payload hashes, original pass
flags and the complete diagnostic input-hash mapping. File digests, complete
four-model summaries, numerical shifts and endpoint decompositions are
retained in `GALAXY_FIELD_RESULTS_REVIEW_DATA.json`.

The galaxy freeze is
`dcb22692af4397c08c8dfb15dc17cddebc1a3e377a02f8b48695197e075c2ef9`.
The diagnostic freeze is
`f92d93431819bf068f482ab6cc00fc2e6417a3a1fbaf9432c5d246fa22cac0b5`.
The complete diagnostic result SHA-256 is
`4c71167497303ec85322ae9ba624c15c5d43e0331e3ad3bbc20eef3749f08c9e`.

No original source, result, checkpoint, freeze, observational row or
scientific tolerance was changed during this review.
