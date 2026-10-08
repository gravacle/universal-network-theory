# Prepared annulus V001: independent implementation preflight

2026-09-29, before execution. Accepted for the declared small initial-slice
and initial-clock-rate calculation; no load-bearing issue found. No model
import, numerical worker or outcome inspection was performed by this reviewer.

Reviewed complete source/protocol and the final pre-freeze quarter-point
quadrature update. Exact settled identities:

- `prepared_annulus_release_v001.py`:
  `d7595be62f12a1574b98a22ad808e3a7fb56e5408ae9bd6d07633bc4722633c3`.
- `PREPARED_ANNULUS_RELEASE_PROTOCOL_V001.md`:
  `28375c681355fa5d4c6686149fa9cf4798533fbc1bb2da638463adce16345b26`.

The source authenticates the prepared result's exact bytes, canonical payload,
freeze and transitive source identities; it selects all three specified
resolution inputs and their original signed positions/velocities. The frozen
source defines the experiment; this review is not an independent authorization.

The same finite-parent positive baseline follows from its stationary endpoint:
`delta²*y_s+y_s³=delta*g_s` implies
`DeltaU=sum w(.5*delta²*y_s²+.75*y_s⁴)`.
The analytic sinh root, bisection control and complete-energy identity are
consistent. `delta=z³` correctly transforms the density `delta d(delta)` into
`3z⁵ dz`. Full-band and same-band continuum values are separate contrasts,
not substituted baselines. No prepared energy or offset is subtracted.

The conditioned `u=(1-f)/r_in` ODE, initial value, N profile and `C=2/Kb`
normalization agree with the original constraint at M²=1. Reconstructed
curvature density `(u+x*u_x)/(r_in*x²)` and polarization divergence
`2B sqrt(f) h'/(r_in*x)-B h'' g_c*u_x/2` retain the correct signs and avoid
subtracting nearly equal metric numbers. Geometric mass and its explicitly
Lambda-subtracted counterpart are labeled as slice quantities, not ADM energy.

The scaled release fluxes correctly remove `r_in²`; in particular the state
source is `A=N²*x²*VB*h'`, not `N*x²*VB*h'`. Eta integrates with one factor
of r_in whereas eta_r is the physical radial derivative. The RK4 refinement,
Hermite interpolation, two-half-panel Simpson weights `(1,4,2,4,1)/12`, and
independent four-point Gauss quadrature are consistent. The latter tests
quadrature on a shared metric interpolant, which the protocol states honestly.

The original-density residual, sixth-order centered derivative signs and
interior index census check correctly. The second derivative test reconstructs
the flux from numerically differentiated eta instead of merely differentiating
an identically constant stored flux. Exact algebraic flux and metric checks
remain useful but are not misrepresented as independent discretization tests.
The baseline-only Schwarzschild-plus-Lambda control is a metric constraint
control, not a null accelerated-clock solution.

No numerical gate depends on obtaining a small physical release rate. The
stated fixed input scales avoid division by the clock-rate zero crossing.
The eta quadrature tolerance was considered analytically before outcomes:
the leading weak integrand x^-2 has a one-panel-per-cell Simpson integral
error bound `1/(24*64^4)≈2.48e-9`; two half-cell panels lower that leading
bound sixteen-fold. The dimensional multiplier is r_in times the ~3.1e3
eta_r scale, not the ~1e6 fractional source-rate scale. This supports the
prospective independent endpoint gate without adjusting it from outcomes.

The source preserves all twelve state/radius/grid cases, reports failures,
does not write files, and qualifies neither action evolution nor a long-time
coupled spacetime. The retained local-curvature frequencies are not mislabeled
as exact finite-amplitude orbit frequencies. Positive initial geometry and
an invertible release operator can coexist with a large required source rate;
that is a scientific result to retain, not a numerical failure to tune away.
