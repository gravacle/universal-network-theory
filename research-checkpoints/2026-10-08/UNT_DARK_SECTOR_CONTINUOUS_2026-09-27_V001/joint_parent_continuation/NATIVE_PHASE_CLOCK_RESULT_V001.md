# Native formed records pass the local phase-clock test

2026-09-28. Saved-state postprocessing of the inherited native 16-state cell;
no formation, new pulse, parameter fit or enlarged calculation.

The actual formed record amplitude A_L+A_R remains nonzero and its phase
advances continuously throughout the entire inherited hold window [0,2].
The phase orientation and window were fixed before the calculation. All
518 computational checks pass; the independent audit additionally passes
279 checks, with maximum discrepancy 7.33e-15.

## The scientific result

At the finer of the two retained certification grids, the native state has

    |<A_L+A_R>| >= 0.9163300,
    Im(conj(a)*a_dot) >= 0.6597295,
    0.6699443 <= phase rate <= 0.9724974.

These are whole-window analytical interpolation bounds with the prospective
1e-10 numerical allowance, not merely minima over five selected ages. The
512-interval control also certifies positive orientation; the 1024-interval
calculation tightens the bounds without changing any physical time or input.
Both exclude a hidden zero, reversal or unwrapping jump on this window.

The exact native readouts at every inherited age are:

| Hold age | Amplitude | Phase rate | Accumulated phase |
|---:|---:|---:|---:|
| 0 | 0.940154061 | 0.767494823 | 0 |
| .25 | 0.934296529 | 0.757100561 | 0.189605425 |
| .5 | 0.928900454 | 0.790514477 | 0.382254685 |
| 1 | 0.922215872 | 0.913520003 | 0.808059723 |
| 2 | 0.917252385 | 0.898101245 | 1.748306155 |

All rates and times use the inherited hbar=epsilon_r=1 convention. The
feedback-off formed control has constant amplitude 0.955861290 and exactly
unit phase rate. The copying-off blank control has exactly zero amplitude
and no defined phase. Its numerical zeros were not converted into a clock.

The native record count stays 1.31433676545 while the phase progresses and
its rate changes. Thus this is a clock-like readout of retained record
coherence, not a count that must keep increasing to mark elapsed time. The
earlier sign reversal of a later copying pulse is consistent with this:
its Y quadrature crosses zero as the complex amplitude rotates; the phase
itself need not reverse.

## What fixes the rate

The owned held Hamiltonian gives the exact relation

    phase rate = epsilon_r/hbar
                  -(lambda_R/hbar)*Re(<nA>/<A>).

The native state therefore supplies a definite record/incidence-dependent
phase rate rather than a freely chosen clock function. Positive onsite
energy alone does not guarantee this result for arbitrary states: the
prospective note gives an explicit reverse-phase counterexample. The
successful result belongs to this actual preparation and full declared
window. No negative line, excited band or degeneracy was removed.

This is a useful native clock CANDIDATE, not yet a derived spacetime clock.
Physical seconds, a source/metric conversion and a timelike spatially
consistent phase field remain to be determined. The fixed writer reference
and calibrated pulse readout must be retained; a time-dependent rephasing
would change the clock being tested. No covariant kinetic function or
cosmological abundance has been inferred from a monotone local phase alone.

## Calculation and custody

The primary calculation uses all 16 allowed transition lines from 12 analytic
energy projectors. Full original-matrix eigensolver and scaled-Taylor
evaluations at all five ages agree, as do the older saved K and Y readouts.
The maximum worker check residual is 2.66e-15. Runtime was 0.0310832 seconds,
with 38,273,024 bytes peak self RSS.

The independent result review is NATIVE_PHASE_CLOCK_V001_REVIEW.md. The
prospective candidate, protocol and worker remain unchanged under their freeze.

- Result: native_phase_clock_v001_results.json, SHA-256
  `5992e6daf072b3873670d22c280f4f1592e95a0f250eb703d919d6d548f21206`.
- Freeze: native_phase_clock_v001_frozen.json, SHA-256
  `e01ceac78343ea49d29cebc8b555d77509427d172439339380e6e80c4a4eb70f`.

The next narrow native bridge is to express the already owned incidence
response at equal values of this record phase, retaining its timing response
and source normalization instead of inserting an arbitrary clock rescaling.
