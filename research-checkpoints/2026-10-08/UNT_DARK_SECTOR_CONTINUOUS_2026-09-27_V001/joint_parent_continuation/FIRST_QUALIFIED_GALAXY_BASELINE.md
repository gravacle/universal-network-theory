# First qualified galaxy baseline: scientific meaning

2026-09-28. Interim result for the original `HI1_H21` model only: exponential
continuations for both H I and H2, with all original source and law choices
unchanged. The four-model queue is still being completed; this is not a
final source-variation conclusion. Saved-data arithmetic and custody were
independently checked without rerunning a field solver.

## The constructive result

The specified network-inspired mechanical response supplies most of the
missing rotational support in this measured-density galaxy calculation.
With exactly the same ordinary-matter source, the velocity RMS difference
from the observed curve changes as follows:

| Recorded region | Rows | Ordinary-matter Newtonian RMS | Conditional network-response RMS |
|---|---:|---:|---:|
| All radii | 43 | 59.1023 km/s | 13.1737 km/s |
| R >=2 kpc | 37 | 63.4296 km/s | 11.1438 km/s |
| R >=8 kpc | 21 | 75.8619 km/s | 10.3428 km/s |

These are unweighted descriptive RMS residuals, independently recalculated
from the saved forces through `v²=R*a0*g_R`. No galaxy velocity was used
to optimize this source or constitutive law in the frozen field experiment.
All 43 rows remain present, and all radial forces in this case give real
circular speeds.

This is an actual nonspherical field calculation, not a pointwise rescaling
of a published Newtonian rotation curve. Its practical numerical checks
have now passed: the maximum recorded R>=2 kpc radial-force change is
0.42280798% under doubled logarithmic resolution and 0.00984007% when
moving the outer boundary from 255 to 1023 kpc with the same inner grid.
The same-source Newtonian solution passes all five independent ring-integral
checks. Those are numerical qualification results, not confidence intervals
for the galaxy's physical source.

The network-response curve still has structured residuals. At R>=2 kpc its
mean residual is -3.8723 km/s, versus -60.3741 for the baryon-only Newtonian
case; at R>=8 kpc the corresponding means are +1.9609 and -75.3342 km/s.
The network case's largest absolute residual over R>=2 is 19.6924 km/s.
Small signed means therefore do not mean that the radial curve agrees
point by point. The current improvement is substantial without being a
precision-fit claim.

## What the comparison does and does not establish

It demonstrates that this fixed conditional mechanical law can supply the
large observed extra support without adding a dark halo in this baseline
calculation. It is **not** a comparison against a fitted dark-matter halo,
another optimized theory, or a full observational likelihood. NGC3198 was
already exposed development data, not held out. The acceleration scale is
the previously adopted empirical value and the second scale was fixed by
the previously declared, model-dependent cosmic reference; neither is a
new microscopic prediction from the original UNT record equations.

The stellar-source audit has identified an external, independently
published calibration difference: Leroy's K-band M/L 0.5 corresponds to
effective 3.6-micron M/L 0.39784, not the SPARC reference's 3.6-micron M/L 0.5.
That fixed conversion accounts for most of the 28.52% difference in their
3–8 kpc annular stellar masses. It has **not** been fitted to velocities or
applied to this result. Local radial-profile differences, vertical geometry,
warp, distance, gas conversion and the rounded-total/profile discrepancy
also remain named source issues. See `PHOTOMETRIC_SOURCE_COMPARISON.md`.

The immediate scientific interpretation is therefore useful and specific:
the candidate has enough gravitational response to address the galaxy's
large baryon-only deficit; the remaining radial residuals now test its
constitutive shape and the measured-source reconstruction. The prescribed
four-model queue and no-refit disk-response diagnostic distinguish these
effects before any new source comparison. They cannot on their own prove
the native physical origin of this response, a lensing match, or a complete
dark-sector cosmology.

## Independent verification record

Verified the 29 frozen source identities, case metadata, all four payload
digests/pass flags, source-mass equality, all residual summaries, both
recorded domain/resolution maxima, and each saved Newtonian ring discrepancy.
The freeze SHA-256 is
`dcb22692af4397c08c8dfb15dc17cddebc1a3e377a02f8b48695197e075c2ef9`.

| Case | SHA-256 |
|---|---|
| HI1_H21 N256 L255 nonlinear | `6b845974294215be8da3af4155e7ab2cbc0a9f732d55ce01869347c24930eed4` |
| HI1_H21 N320 L1023 nonlinear | `2d2fa2b364dd2081d3d7f14e9d7280559d89e4329eea1bbf3ff8cf2d1136d374` |
| HI1_H21 N512 L255 nonlinear | `2b5d79a1d957624be4fc1df56eb5343c3b4a48e363c704061e1f779274f88ea8` |
| HI1_H21 N512 L255 Newtonian | `1a8c572c3ab27156d324f7592cf4120844700255c12cb08625425d2d62080328` |

Component masses, including the declared tails, are
`Mstars=1.5753633648e10`, `MHI+He=1.5134141725e10`,
`MH2+He=5.7477950872e8` solar masses. No source member, result, freeze,
checkpoint or original scientific threshold was changed by this review.
