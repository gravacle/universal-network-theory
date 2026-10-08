# Native carrier subdivision: prospective numerical protocol V001

2026-09-29. No execution is authorized by this file alone. The parent agent
reviews, freezes and runs the sole worker. This is the new populated-carrier
test derived in `NATIVE_CARRIER_RULER_PATHWAY_V001.md`, independently reviewed
in `NATIVE_CARRIER_RULER_REVIEW_V001.md`; it is not the earlier blank-register
growth experiment and does not contain a new creation port.

Use exactly the note's inherited constants, fixed-content one-carrier held
sector, masks 15/11 at N=2 and 350/342 at N=3, carrier initially at L0,
reader at old R0, and eleven times
`0,1/32,1/16,1/8,1/4,1/2,1,pi/2,2,pi,4` in hbar/Omega units.
Keep both graph types and every time. No source, hopping, onsite coefficient,
clock normalization, graph or readout time is selected from results.

`native_carrier_ruler_v001.py freeze` hashes its own source, this protocol,
the analytical note/review, the resident BS action, and subdivision source
identities, and prints the full snapshot as JSON. The parent saves that
snapshot under `NATIVE_CARRIER_RULER_V001_FROZEN.json` using `apply_patch`;
`run` reads it and requires byte-identical inputs/configuration. The program
prints the complete result wrapper as JSON; the parent similarly publishes
`NATIVE_CARRIER_RULER_V001_RESULTS.json`, preserving any existing artifact.
The worker performs NO filesystem writes and no execution starts on import.

The primary exact-invariant-sector action is matrix-free on dimensions
64 and 3072, two prepared inputs batched at each size. An independently
assembled, fixed-width row-sparse operator supplies a second implementation.
No dense 3072-square matrix is built. Structured probes, Hermiticity and
the exact initial moments test the two operator constructions.

For each time, the primary exponential uses a Gershgorin center/radius and
Chebyshev recurrence. Its Fourier coefficients come from a uniform-angle
FFT of `exp(-i z cos(theta))`. With

    B_n(z)=(|z|/2)^n/n! * exp(z²/[4(n+1)]),
    sum_(n>=L)|J_n(z)| <= B_L(z)/(1-|z|/[2(L+1)]),

when that denominator is positive, choose degree K with twice the tail
from K+1 below 1e-18. Use a power-of-two FFT length M at least
`max(64,4(K+1))`. The conservative additional alias bound is
`4(K+1)` times the same tail from M-K. Record both log bounds, including
when their floating-point exponentials underflow. K<=4096 is an algorithm
guard, not a run deadline or an outcome-adjustable physics gate.

Independently apply the shifted exponential through the row-sparse operator
using equal substeps with `radius*|dt|<=.75`. Every Taylor polynomial has
tail bound below 1e-19, using its factorial-series geometric remainder;
the product bound is `expm1(nsteps*log1p(substep_tail))`. Maximum 256 terms
is an algorithm guard. Both algorithms act from the original state at each
requested time, not from a different method's previously evolved vector.
The center phase and all absolute energy offsets are retained.

These analytic tails bound truncation/aliasing in exact arithmetic, NOT
floating-point roundoff. Actual two-method vector agreement must be <=2e-9.
Operator identities, norm, continuity, frozen-cycle amplitudes and tiny
Schur controls use 2e-11 absolute error. Mean-energy and variance conservation
use 2e-8 absolute error. N=2 also
has a dense 64-state eigensolver oracle; only frozen 4/6 carrier controls
are diagonalized at N=3. All checks and failures are saved; no retry or
tolerance change is implicit in a failed check.

Check H²/H³ shortcut coefficients as EXACT derivative/power identities,
not by requiring finite-time probability ratios to equal their limiting
coefficients. Retain their finite-time ratios as descriptive diagnostics.
Check the inherited graph/backbone leakage bounds including the case in
which a bound is uninformative. No scientific pass criterion demands that
the target is slower, more stable or more connected than the source.

Save each preparation/time's complete carrier populations, native currents
on every possible edge, current-continuity residual, source return, old-reader
arrival, new-node carrier population, exact-graph/joint-reader/backbone/full
connectivity probabilities, full-state return amplitude, frozen control,
and component energies (incidence diagonal, incidence flips, carrier hopping,
carrier onsite, current square). Preserve norm, energy variance, both-method
error and algorithm diagnostics. The exact initial work is +10 for each
declared localized-carrier image, not a free preparation assumption.

Interpretation is an owned finite native transfer/ruler comparison under a
specified clock and prepared state. It is not photon identification, an
inferred physical distance, autonomous growth, a cosmological fit, or an
extension of the single-carrier sector to populated record formation.
