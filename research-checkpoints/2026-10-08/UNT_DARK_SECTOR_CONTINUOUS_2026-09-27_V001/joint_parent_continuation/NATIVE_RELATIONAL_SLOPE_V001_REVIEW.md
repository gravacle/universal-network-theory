# Independent review: incidence response against the native record clock

2026-09-28. All three stored preparations and five inherited ages retained;
no new formation, pulse, fit, physical time conversion or age selection.

The equal-phase response is well defined for the two qualified record clocks.
Its leading slope is positive at all ten defined sample states but is not
constant within either fixed Hamiltonian. In particular, the native clock
does not remove the native response's state dependence:

| Native age | Slope per native delay | Slope per record-phase increment |
|---:|---:|---:|
| 0 | 0.8845136231 | 1.1524685203 |
| 0.25 | 0.8869060984 | 1.1714508538 |
| 0.5 | 0.7611314110 | 0.9628304521 |
| 1 | 0.4045008615 | 0.4427936557 |
| 2 | 0.5817191250 | 0.6477210984 |

The native phase-normalized range is 0.4427936557–1.1714508538, a spread of
0.7286571981. This is resolved variation of the specified finite system, not
an observational significance estimate. Feedback-off has unit clock rate, so
its two slope conventions coincide; its own range is 0.1384765023–0.9348647038.
The copying-off blank control has the same unclocked incidence response as
that control here, but no record phase; all its relational quantities correctly
remain null. The changed Hamiltonians are not pooled into one state-independence
test.

## Response and source checks

The source convention is H−eta n delta(t−w), with eta a fixed integrated
native-time impulse of action units. The response is i mean([O(t),n])/hbar.
Changing the readout to elapsed phase divides the leading slope by the actual
phase rate once. It does not silently redefine a continuous forcing amplitude
per phase interval.

The same impulse preserves A and its first native-time derivative at the
instant of the kick exactly, because both commute with n. Clock backreaction
starts at order delay²:

    chi_An''(0) = −i lambda_R h mean(Xa A) / hbar³.

The readout-time shift and incidence correction have the correct signs and
one-half factors. They refer to the coefficient of eta times **native-delay
squared**, not a second derivative with respect to phase. Across the five
native states the phase-shift coefficient is negative, but the incidence
timing correction changes sign with the incidence drift: approximately
+0.0855592, −0.0227983, −0.0938910, −0.0501358, +0.0594110. These signs were
retained rather than imposing a universal delay or attraction interpretation.
The feedback-off clock backreaction vanishes exactly; the blank clock is not
regularized by dividing by noise.

## Independent audit

All new and ancestral freeze/source/payload identities were authenticated.
All 284 production checks pass (maximum absolute residual 2.77556e-15).
The independent audit rebuilt the original matrices, transformed the readouts
to the energy basis, and obtained time derivatives by powers of energy
differences, independently of the production nested-commutator calculation.
It checked every retained row against the old flip-energy and clock evidence,
all complex XA and clock-response values, timing coefficients, nulls and
per-preparation summaries. All 245 independent comparisons pass; maximum
absolute discrepancy 1.35065e-15. No new impulse was propagated.

Reproducible audit: `native_relational_slope_independent_audit.py` and
`NATIVE_RELATIONAL_SLOPE_INDEPENDENT_REVIEW_DATA.json`.

- Production source SHA-256: `c4e518d3f801b6caa188699f5e8162b07c648b2adccf111f587a95cd33263366`.
- Freeze SHA-256: `d8a0e6853ba409e1f6465ee09d22ed4bb0a048f73d5e70e26afdaffbfe09251f`.
- Production result SHA-256: `95d51edcf1b2738bb815c5876ba2e80355feea58c4ed6e837bab2e85f404b6e6`.
- Independent source SHA-256: `1362a55c22fa211b3a5c1c8e27cc622083dbbf58c617dc8baecacfbb28ee586d`.
- Independent result SHA-256: `3b3db13b9459685fa59f6ed05889d4c0b2767680c1f2be78419b65fc7135e9b1`.

## Constructive consequence

This is an owned internal readout of an owned native source response, with
the clock's response included. It constrains a proposed bridge to a mechanical
effective theory: a single state-independent canonical source moment cannot
simply be equated to these varying numbers under fixed calibration. A successful
bridge must derive the relevant source, state, inertia and volume dependence,
or a justified restricted state, rather than adjust a clock normalization at
each age. It does not rule out that richer bridge, establish a spacetime metric,
or turn a positive susceptibility into an already calibrated gravitational
inertia.
