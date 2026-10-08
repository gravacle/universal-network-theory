# Independent review: high-gap shared-spectrum candidate

2026-09-29. Full analytical review; no fit, propagation, or new physical data.

Reviewed `HIGH_GAP_SHARED_SPECTRUM_CANDIDATE_V001.md`, SHA-256
`e7abd950514c6fa29213fa62292d2e9f41c3286716f25353159981210e9d041c`.
The finite-cutoff normalization clarification was made by its author before
this review was settled and before any numerical freeze.

## Finding

Accepted as an internally consistent, constructive **conditional spectral
extension**. A small amount of sufficiently high-gap weight has a nonempty
parameter regime with substantial cold energy capacity and small averaged
force cost. The note correctly retains its changed contact, absolute vacuum
matching, actual preparation work, and coherent response. It does not establish
that native UNT supplies this spectrum or that the extension solves the joint
galaxy/expansion problem.

## Independently checked equations

- `Kb=A(1-epsilon^2)/2+wH` and `C=2M^2/Kb` consistently normalize the force,
  excitation density and pressure moment. The pressure inequality follows
  from `E=2<V2>+3P` and `<V2> <= sqrt(S4 P)`; it permits vector orbits without
  assuming the scalar harmonic coefficient applies to them.
- The hard minimum solves `R^2 y+y^3=R h`. Its polarization expansion, the
  exact convex component decomposition of the relaxed force, and
  `a0_new=16Kb/(3pi A)` check. The multiplier is exactly `1/(1-f)` relative
  to the same-cutoff zero-atom contact. Relative to the inherited zero-cutoff
  `8/(3pi)` it is `(1-epsilon^2)/(1-f)`. A positive fixed lower cutoff still
  removes the strictly quadratic zero-field asymptote.
- The endpoint lowering is `R^2 ys^2/2+3ys^4/4`; its stated large-gap series
  and the compulsory weighted change in the vacuum density check. No
  independent compensating constant is introduced.
- At fixed scalar action, shifting the harmonic center and averaging its
  quartic energy gives every displayed term of equation (7). The leading
  excited force floor is `3 ebar_H g/R^4`, not zero. For the exact check,
  `m (y^2)ddot=4eH-4R^2 y^2-3y^4` proves that
  `xi=(R^2+y^2)/(R^4+4eH)` solves the unit-forcing variational equation.
  Its turning-point value has fixed-action normalization. The exact
  susceptibility and both stated deficit bounds follow; the scalar/vector
  distinction is necessary and correctly retained.
- Resolving the proposed pulse into three cosine frequencies gives the
  harmonic resonant integral `Hp T/4` and `eH=pi^2 n^2 Hp^2/8`. The
  off-resonant denominator bound gives both equation (12) estimates and
  the during-pulse displacement bound. These are harmonic controls, not
  exact nonlinear energy limits. The note explicitly requires the full
  parent test and identifies accumulated nonlinear detuning `n chi`.
- Differentiating the complete clamped Hamiltonian gives exactly
  `[Kb g-B h'(g)] gdot`. A closed pulse from rest therefore pays the entire
  retained soft-plus-hard energy. The matched constant supplies none of it.

## What the next small calculation can establish

The proposed full-parent pulse can test whether one common, paid-for source
actually prepares the predicted spectral separation and how its retained
state responds. It must retain nonlinear discrepancies, signed oscillations,
the soft-mode distribution and the changed endpoint. High gap alone suppresses
neither the coherent polarization amplitude nor its possible metric response.
An orbit mean, isotropic ensemble, autonomous source, and physical clock remain
distinct constructions; none is silently supplied by this analytical review.

No load-bearing algebraic defect remains in the reviewed version.
