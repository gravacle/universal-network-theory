# Independent saved-spectrum review

2026-09-29. The main finite quantum spectrum, bright spacing readouts, source
sum rules and ground susceptibilities are independently accepted. **One
secondary numerical issue is retained:** weak-flip near-degenerate excited
source-energy curvatures need the additive positive-strength refinement
described below. This is not an unqualified endorsement of every V001 number.

## Custody and method

* Result SHA-256:
  `93b9130e3e6d8684865d4852fafa810cc92cf60ae429dde09fd55c44889d4049`.
* Freeze SHA-256:
  `9f254af41d1523b23168f2d29153e86c4b35aad1c01d6ffa9ad4fcef432e8816`.
* Payload SHA-256:
  `d6a89992e280fcca7892058e384f85b986c15c41da6fc9902b622aa4228112df`.

All seven frozen members match. The original publication refusal occurred
before any spectrum calculation: reserialization changed floating 1.0 to
integer 1 in the snapshot. The preserved failed and corrected freezes are
equal as parsed data but have different bytes/types, matching the saved
`ATTEMPT_001_FAILURE.json`. The accepted result uses the original exact
producer snapshot; no source, parameter or tolerance change was made.

`native_interacting_spectrum_saved_audit_v001.py` (SHA-256
`38969b8b0eb08fb4467af3e0ba6974e0a65c4f792a42d9c3af7c719531b8318c`)
rebuilds the actual full matrix from incidence degrees and reconstructs every
saved projector in full16, bright6 and dark10. Its 407,640 scalar comparisons
check isometries, completeness, projector equations, absolute matrices,
degeneracies, source strengths, signed moments, ground quantities and
collective readouts. No eigensolver, linear solve or propagation was rerun.
The output is `NATIVE_INTERACTING_SPECTRUM_V001_AUDIT_DATA.json`.

The producer's 87,644 controls passed in 0.029207416 seconds, with 33,931,264
bytes peak self RSS. Projector-equation/reconstruction residuals are at most
`2.83e-11`; the largest independent source-strength discrepancy is
`5.87e-14`. These do not, by themselves, bound an inverse-small-gap derivative.

## Main inherited-parameter result

| Uniform records q; native h=1/2 | First-three bright spacing curvature | Ground incidence | Passive ground susceptibility | Lowest pair/first source-strength ratio |
| --- | --- | --- | --- | --- |
| 0 | -0.264483083287 | 0.189913657653 | 0.141079121013 | 0.549357724 |
| 1 | -0.468192514769 | 0.431230037242 | 0.377048762489 | 0.752371802 |

The spacing correction is softening for both inherited cases, not the
hardening or bosonic source ladder of the proposed constant-mass positive
quartic oscillator. All ten complementary states and other bright channels
were retained. The weak-flip controls approach the separately derived
coefficients and lowest source ratio 1/2; their changed h values are not
retuned native predictions.

This identifies a concrete constraint on a future collective reduction:
it must reproduce the native spectrum and source matrix elements, not just
a positive coordinate-potential Taylor coefficient. It does not rule out
other collective sectors or establish continuous classical E_II, a dynamical
instability, a physical metric or cosmological stress. Ground response is
explicitly a diagnostic, not a substituted actual formation state.

## Preserved secondary finding

Using `||P_a M P_b||_F^2` rather than the cancellation-prone but mathematically
equivalent trace product changes 24 weak-flip excited source-energy curvature
entries by more than the original absolute `1e-10` spectral tolerance. The
largest change is `4.6588651653e-6`. The tiny transition strengths differ only
at floating roundoff, but some denominators are approximately `1e-10`.
No main h=1/2 source curvature or bright spacing shows that discrepancy at
the stated tolerance.

The finding is preserved in `NATIVE_INTERACTING_SPECTRUM_AUDIT_FINDING_V001.md`
and the audit JSON. An additive saved-projector refinement has been prepared;
its future output must retain the old values and conditioning metadata.
Neither a relaxed tolerance nor a new eigenvalue grouping is used to hide
this issue. Stable norm-square strengths improve the arithmetic but do not
alone certify relative precision of arbitrarily tiny excited derivatives.
