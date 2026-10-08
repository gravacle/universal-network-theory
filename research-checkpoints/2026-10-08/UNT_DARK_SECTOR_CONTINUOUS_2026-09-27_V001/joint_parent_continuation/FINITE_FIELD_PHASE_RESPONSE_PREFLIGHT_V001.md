# Finite-field common-phase screen: independent preflight V001

2026-09-29. Read-only mathematical/code review; no import, numerical science,
new preparation, fit, producer execution or change to the reviewed files.

## Bound sources

- `finite_field_phase_response_v001.py`:
  `e88cad8d0b9235d14bd702154a4c87ac021635fddf55711455868aef938b6b1b`.
- `FINITE_FIELD_PHASE_RESPONSE_PROTOCOL_V001.md`:
  `467abaccda419df621344d12f68aeaaa8dfc12da5465b84eed8a0f005a8cda9f`.
- Analytical basis `FINITE_FIELD_COMMON_PHASE_DENSITY_V001.md`:
  `cb8ec369a4e70f78b0bd54e2142f746bdf414c8982b141ba9027bd4958d7bb59`.

The full source and protocol were read. The sole final source change from
the earlier full read was `D` to `D_normalized`; reversing that label in a
read-only stream reproduces the earlier source SHA
`f20f5506fb4fa0b0d91ec6b7d46a8b7b1c9a5e0373c38522b09a3736c6730105`.

## Independent checks

Accepted without a requested correction:

- Paired half-interval normalization and rationalized odd inverse-half and
  inverse-three-half weights have the correct factors. The action, period,
  kinetic energy, covariance derivatives and exact moment identity use the
  same normalized measure.
- Stable frequency excess and target avoid subtracting rounded frequencies.
  The exact all-radius hardening certificate, positive action derivative
  and quantitative curvature bound support branch inversion. Empty branches
  retain their minimum energy/source and omit occupied J and action-response
  square; certification failure is not relabeled physical nonexistence.
- The M3 derivatives, Maxwell/chain-rule checks and source parity agree with
  the exact derivation. The longitudinal contact uses the stable bare deficit
  plus the full h'' term, then subtracts the compulsory common-phase square.
- I_g, F_Phi, J, absolute energy/pressure and the envelope identity carry the
  correct R and beta powers. `D_normalized=G-F/Kb`, not the unnormalized BVP
  flux. The local lengths use c^2/gstar and the parsec conversion consistently.
- The same-field fixed cosmic I_b comparison is separate from holding the
  newly solved local I fixed in the derivative. The square inequality applies
  only to the latter; no false sign ordering of the two different states is
  imposed.
- All 1,296 prospective labels are retained with their 144 source indices.
  The chosen two-gap subset is disclosed as exploratory following the old
  five-gap screen. Physical signs/ellipticity are outputs, not numerical
  success gates. The independently inverted quadrature checks, source hashes,
  inherited census, stdout-only publication and fixed tolerances are explicit.

This preflight accepts the specified constitutive calculation, not its as-yet
uncomputed outcomes. It does not establish a galaxy BVP solution, physical
boundary selection, microscopic identification, static stability or an
observational result. The root remains the sole numerical producer.
