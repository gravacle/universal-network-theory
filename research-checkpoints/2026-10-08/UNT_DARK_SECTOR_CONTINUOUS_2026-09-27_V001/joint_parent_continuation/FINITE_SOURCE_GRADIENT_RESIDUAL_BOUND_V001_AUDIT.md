# Finite-source gradient residual bound: independent review

2026-10-04. Source and protocol were read completely. A saved-scalar audit passes **300/300 checks** in 0.0018 seconds. It imports no producer and repeats neither the spectral enclosure grids nor a physical solve. It checks custody, all 90 saved controls, enclosure nesting/refinement, both tail constants, coercivity gaps, error bounds, finite-window corrections, SI conversions and nominal intervals. No original file changed; the numerical slot was explicitly released.

## Meaning of the 100 pc illustration

For the declared Gaussian source and external equilibrium, at ell=100 pc the quartic argument gives the following upper bounds on the nonlinear-minus-linear finite-shell observable:

| Shell radius | Bound on absolute Q_R difference (s^-2) |
|---|---:|
| 1 AU | 1.10384649e-26 |
| 10 AU | 3.49066910e-28 |
| 30 AU | 6.71779582e-29 |

These are **bounds, not predicted corrections**. Subject to existence of the boundary-fixed finite-energy static solution, they genuinely control a nonlinear error; they are more than an unchecked linear extrapolation. They concern the specified Gaussian with sigma=1e9 m, not measured Solar structure. Q_R is an angular quadrupole projection on one finite sphere, not a bound on all forces, the origin Hessian, or the Cassini data estimator.

The inherited nominal linear point value at this length is 7.38950903e-37 s^-2. The separately controlled finite-source/shell linear changes are at most 1.15e-43, 1.15e-42 and 3.44e-42 s^-2 for these radii. The saved combined intervals still exclude inherited point-quadrature uncertainty, as explicitly labeled; they are not confidence intervals. No length was selected by this audit. Choosing 100 pc after these results would be disclosed development selection, not a new independent Solar prediction.

## Why the quadratic and quartic bounds differ enormously

At ell=100 pc the L2/Gamma bound is about 1.01e16 times weaker than the quartic bound. This is not evidence of a huge physical correction, a missing tail, a unit error, or a wrong energy sign. The linear coercivity gap is a comfortable 0.61350878, not a nearly singular denominator.

The quadratic estimate bounds the cubic residual against a quadratic restoring coefficient that can fall to one for very soft modes when the trial-amplitude envelope exceeds the external equilibrium amplitude. It thereby loses their strong nonlinear restoration. The independent quartic secant identity retains that restoration:

    [F(x+e)-F(x)] dot e >= |e|^4/4,   F(x)=|x|^2 x.

The metric-eliminated quadratic variance is nonnegative for normalized weight dW=2s ds. With T=integral dW a_s|e_s|^4, Holder duality gives

    ell^2 ||grad e||_w^2 + T/4 <= I4^(3/4) T^(1/4),
    ell^2 ||grad e||_w^2 <= 3 I4/4.

The finite-shell adjoint is proportional to P2(cos theta), and has squared norm 3/(14 pi R^3). This reproduces the stated coefficient 3/sqrt(56 pi), without a sign reversal or extra vector-dimension factor. Taking the smaller of two valid upper bounds is legitimate and does not change a physical parameter.

## No discarded soft tail

The source uses the correct distinct tails: Gamma_tail <= eta^2 and S_tail <= Bsoft^2 eta^2 for the quadratic route, while the quartic route uses eta^(10/3). It does not substitute the stronger exponent into the weaker quadratic estimate.

The independent dimensional expression for the quartic tail reproduces the saved value 1.06081117e-64. Even at the smallest saved S and I4 upper bounds (ell=100 pc), omitted-tail fractions are only 4.21e-44 and 1.40e-84, respectively. The tail is therefore neither omitted nor the reason for the discrepancy between methods.

The monotonic endpoint constructions are algebraically correct: t^2 and aU/ge decrease with s, while V increases. Mixed endpoint products bound whole cells even though their combined integrands need not themselves be monotone. At ell=100 pc the finest finite-enclosure relative widths are 0.12465% for Gamma, 0.85291% for S, and 0.52680% for I4. The upper endpoints are retained. These are analytic enclosures evaluated in binary64 with assigned arithmetic checks, not directed-rounding interval certificates.

## Finite-source/readout correction

The shell window W(x)=15 j2(x)/x^2 is correctly normalized. Its positive-weight cosine representation gives |W|<=1 and 0<=1-W<=min(2,x^2/14). Combining it with the Gaussian factor yields the used min(2,D q^2) bound. Independent integration of the two positive Fourier envelopes reproduces every saved finite-linear correction. Thus the conversion from the exact linear point coefficient to the Gaussian finite-shell observable is explicitly accounted for, not silently identified.

## Conclusion and ceiling

No mathematical/source transcription blocker was found. This is useful conditional finite-source nonlinear control for the changed linear-source gradient parent. It does not establish existence or formation, determine ell natively, validate a Solar ephemeris, transfer previous galaxy scores, supply a photon/clock metric, or solve the shared expansion problem. An upper-bound success for a selected readout is not whole-theory success; a loose upper bound in another illustration is not a physical failure.

Audit JSON: `FINITE_SOURCE_GRADIENT_RESIDUAL_BOUND_V001_AUDIT.json`, SHA256 `09172529e76b0c07f74e0c4df913525ca449780d0d95e54c2ab3293f6e3dc7ec`.
