# Prospective saved-potential lensing numerical controls

This additive specification accompanies `SAVED_POTENTIAL_LENSING_PROTOCOL.md`.
It is fixed before lensing output. No new PDE or observational fit is involved.
The twenty original/calibrated completed fields are the entire input census;
the new HALOGAS contrasts are excluded. All five radii and three projections
are retained. `saved_potential_lensing.py` is inert until freeze or run.

## Representation and computation

Use the clarified residual-node convention in the main protocol: subtract the
reference at positive saved centers, then extrapolate that residual to zero
height and zero radius. This is not exactly the old full-potential midplane
gradient. The outer residual is zero; the undefined (0,0) residual is never
evaluated. Identify every crossed cell before evaluating reference potentials.
Only required positive saved-center nodes and their extrapolation dependencies
are evaluated, in batches no larger than 512. No dense grid of reference
potential quadrature points is allocated.

Use the unchanged log-radius spherical-potential routine at its original
order 64 and independent doubled order 128. The primary residual uses order
64. The second residual is a numerical-reference diagnostic, not a second
physical model. For each ray split exactly at all radial/positive-and-negative
height nodes, the midplane and box faces; integrate each polynomial segment
with two Gauss nodes and independently with four. Near-identical crossing
locations are deduplicated at 64 machine epsilons times the largest endpoint
length (minimum 1 kpc); no physically resolvable cell is merged.

The spherical deflection uses fixed theta quadrature at orders 64 and 128,
subtracting the exact deep endpoint for the candidate. Newtonian controls use
their exact analytic full monopole bending as an independent identity check.
The reported primary full angle uses order-128 spherical **interior plus
exterior** and the order-64-reference/two-node correction. Independently
integrate the whole spherical interval and compare its value with those
pieces. Preserve every component and the difference, not just the total.

## Frozen targets, not inherited force tolerances

Let `eps` be IEEE float64 machine epsilon. Raw correction integrals are in
the numeric kpc convention of the saved fields; angles multiply these by
`2*A0_KMS2_KPC/(299792.458)^2`. A minimum scale of 1 below means one unit in
that raw convention, never one radian.

1. **Polynomial integration, reflection and face-on integration.** For each
   Gauss segment compute a cancellation scale using the *sum of absolute
   corner-potential contributions* to its two sky gradients, integrated with
   positive weights. This dominates the sum of absolute signed-gradient
   contributions and accounts for differencing adjacent potentials. The
   two/four-node, opposite-impact reflection and principal cross-axis checks
   must agree within `4096*eps*max(1,sum of relevant cancellation scales)`.
   Use compensated summation. For face-on rays independently integrate the
   piecewise-linear radial residual derivative by the trapezoidal rule at
   every z node, with the same cancellation-scale tolerance.

2. **Monopole analytic identities.** On every actual ray use its own q and
   entry/exit angles to check both exact Newtonian and exact deep-log fields
   against their analytic whole, interior and exterior values. Compare the
   directly evaluated 64/128 theta quadratures with those formulas using
   `512*eps*max(1,abs(exact scalar integral),absolute contribution scale)`.
   This tests the impact-length vector prefactor, signs and finite-box split.
   Check reconstruction of a total from its three saved angle components
   at `128*eps` times their absolute sum. The physical exact full magnitudes
   are `4GM/(c^2*b)` and `2*pi*sqrt(G*M*a0)/c^2`.

3. **Spherical quadrature.** The 64/128 difference of every candidate
   whole/interior/exterior raw vector must be at most `1e-8` times
   `max(1, norm(order128 whole sphere), absolute integration scale)`.
   The independently integrated whole versus interior-plus-exterior vector
   has the same target. These fixed numerical tolerances are not data errors.

4. **Reference potential integration.** Every needed 64/128 reference-node
   potential must agree to `1e-9*max(1,abs(order128 potential))`. The resulting
   correction-integral change must be at most `1e-7` times
   `max(1, norm(full spherical integral), norm(primary correction))`.
   Report both node and final-projection effects. This specifically tests
   reference integration and its differencing, independent of the ray rule.

5. **Newtonian projected-mass accuracy.** For each of the five N512
   Newtonian fields and each face-on impact radius, compare the completed
   physical radial angle with `4G*M_disk(<b)/(c^2*b)`, using the same source's
   exact enclosed-mass integral. The first-implementation numerical target
   is **1% relative in bending** at all twenty-five points. This newly stated
   target does not follow from the old 2% radial-force oracle. It tests the
   combined saved field, residual interpolant and spherical completion;
   finite-box modeling error can contribute. It is not a lensing-data fit or
   a pure quadrature certificate. A failure is retained and reported, not
   repaired by importing a looser force threshold.

Keep candidate N256/N512 mesh and L255/L1023 domain changes descriptive-only,
as well as all source and stellar-calibration differences. No observational
success gate, source choice, tolerance adaptation or new force solve occurs.
Save all twenty cases and all failed numerical checks before final status;
custody, shape or invalid-geometry errors instead fail immediately. This
small postprocessing can be rerun as a separately identified attempt if an
implementation repair is needed; it receives no checkpoint system.

## Custody and scope

Freeze this note, the algorithm, action pathway, pressure derivation, new
source code and exact twenty-case census with recursive inherited manifests.
Verify existing payload seals and numerical checks. Freeze cited scientific
notes, not an implied local copy of every linked primary paper. New outputs
are exclusive atomic publications with source-freeze and canonical payload
hashes. All input fields are read-only. The adopted weak-field aligned-clock
metric and isolated spherical exterior remain physical assumptions; the
numerical controls do not turn them into native UNT derivations or solve the
external environment/cosmological light path.
