# Independent analytical review: finite-age energy-source response

2026-09-30. Reviewer: `short_path_adversarial`. **PASS for the analytic
identities and explicitly conditional scope; not a numerical certificate or
authorization to interpret approximate spectral clusters as exact degeneracy.**

Reviewed the complete `NATIVE_ENERGY_SOURCE_AGE_AVERAGE_V001.md`, final SHA-256
`764bb3f333aab4750fcb564c043ad715343dfaf15a5519e9fafa3b7cb18cf4d6`,
against the complete adopted energy-dipole bridge and saved-state protocol.
The final note's two notation corrections retain the explicit `i/hbar*theta`
factor in the two-time kernel and the actual predecessor filename. No numerical
job, eigensolve, propagation or producer import was performed for this review.

## Algebra checked

1. With `H(lambda)=H+lambda_i G_i+...` and
   `chi_ij=(i/hbar)theta<[G_i(t),G_j(s)]>`, the response is **minus chi**.
   Thus `G=(Z/gamma0,-B_eta)` and the conjugate-energy kernel `C-chi` agree
   with the adopted source family. Rescaling acceleration to alpha rescales
   its mixed contact by `1/gamma0`; it does not remove the volume contact.
2. Spectral age integration gives the stated phase times sinc for each
   ordered energy block. Pinching retains the entire exactly degenerate
   block. Triangle inequality, trace-norm distance at most two, and the sinc
   envelope give (4). For a pure initial state the off-diagonal block is
   rank one with trace norm `sqrt(p_E p_F)`. No population thermalization or
   favorable age selection follows.
3. Trace/operator norm duality and the commutator norm bound give (5),
   uniformly in both times. A finite lag window contributes its length L;
   exponential resolution contributes `1/kappa`. Stationary endpoint terms
   and finite-T two-time residuals cannot be silently omitted. The bound is
   not uniform as kappa tends to zero; a joint limit requires control of
   `b(T)/kappa`.
4. For a cyclic source the stationary one-point contribution to first-order
   work vanishes, but the finite-age drift need not. Integrating the bounded
   mean difference against `lambda_dot` gives (7). This term scales linearly
   in probe amplitude and cannot be discarded to infer quadratic passivity.
5. Real symmetric H, sources and the stated real initial preparations make
   each exact energy block real symmetric. Its trace against a real
   antisymmetric same-energy commutator vanishes. The paired unequal-energy
   residues are real symmetric matrices. This is a property of this packet,
   not a universal permission to erase zero-frequency terms.
6. For a positive gap Delta the time-domain term is
   `2 M_Delta sin(Delta*tau/hbar)/hbar`. Its upper-half-plane transform is
   `2 Delta M_Delta/(Delta^2-hbar^2 z^2)`, confirming the inverse-gap signs
   and powers in (9). Expanding the geometric denominator and using
   `|1-x| >= 1-|x|` yields exactly the matrix-norm remainder (10).
7. All exactly equal gaps must be summed before a line's sign is judged.
   Negative eigenvalues of that grouped matrix permit negative linear
   absorbed work in an accessible source combination. Positive static or
   quadratic coefficients do not establish passivity. The absence of an
   absorptive line below the first finite gap is vacuous evidence for passivity;
   finite-duration pulse tails still matter. Instantaneous first moments,
   age-averaged first moments and inverse-gap coefficients remain distinct.

## Required numerical boundary

The word **certified** in the analytic note is a prospective obligation. An
ordinary double-precision eigensolve, a convenient degeneracy tolerance, or
small reconstruction residuals alone do not establish exact degeneracies,
exact zero residues, or a strictly positive smallest contributing gap.

A later protocol must freeze eigenvalue/projector error bounds and gap rules
before evaluation. It must retain all four initial states and all source
directions; include uncertainty in H, projectors, residues and contacts; and
preserve weak signed lines. A numerical cluster is not an exact energy block.
When exact separation or degeneracy is unresolved, retain its possible internal
coherences/near-zero transitions or give a conservative enclosure and report
the corresponding static/inverse-gap certificate as unresolved. Do not obtain
an infinite-age stationary comparator by arbitrarily deleting those terms.
If all exact contributing residues vanish, report that case directly instead
of assigning a fictitious minimum gap.

Two finite 96D spectra can support a conditional finite-apparatus diagnostic.
They cannot establish a continuous soft spectrum, physical averaging duration,
passive attractor, gravitational constitutive law, galaxy state selection,
empirical replacement of dark matter/dark energy, or Stage 3 completion.

## Cross-checked source identities

- `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`:
  `81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96`.
- `NATIVE_ENERGY_DIPOLE_SAVED_STATE_V001_PROTOCOL.md`:
  `0cce4c0169b45fd1452b87fe262eb5abf79d17fb1821670fbcfe8f665f1f9d7d`.

No correction to the final analytic note is required by this review. The
numerical certification boundary above must remain explicit in any producer.
