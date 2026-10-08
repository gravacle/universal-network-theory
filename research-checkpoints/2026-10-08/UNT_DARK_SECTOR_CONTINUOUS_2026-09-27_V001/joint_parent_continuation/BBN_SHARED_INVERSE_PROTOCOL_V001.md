# Prospective shared BBN table-proxy inverse V001

Root alone freezes/runs `bbn_shared_inverse_v001.py freeze|run`. This is
inert source plus prospective protocol, not a completed inverse calculation.
No BBN engine, ODE, finite-field orbit, galaxy PDE, installation or new data.

## Family, data, freedom count

Use `SHARED_BBN_PROXY_INVERSE_CALIBRATION_V001.md` exactly: two continuous
shared inference parameters (omega_b,R), beta=.005, alpha=1, exposed common
a0=1.2e-10 m/s2, two existing soft cutoffs and their 64/128 controls. Preserve
all 18 old labels/BBN markers and their exact mapping to five distinct
H0/Omega_m backgrounds. Do not use the old standard-BBN omega_b errors as
additional likelihood information. Do not count quadrature copies or repeated
reference labels as independent evidence. There is no independent Delta,
excitation abundance, vacuum offset, source length or galaxy density fit.

Authenticate the completed BBN proxy wrapper and recursive freeze, the
global calibration and photon-budget wrappers, their ancestry, this source,
protocol and derivation. The old proxy payload used integer matched_Delta0
keys before JSON publication: reconstruct those keys as integers solely for
its documented canonical hash check; preserve the raw bytes as well.
Import only the authenticated old table module's definitions and call its
table reader/interpolator/qualification, never its run/main/thermal producer.
No downloaded PRIMAT code is imported. The old qualified heating envelope is
read from its result, not recomputed.

## Fixed contour census (not a hidden joint likelihood)

Use every nonnegative primary Delta node (17 nodes, [0,7]) as the coarse
mesh; add every adjacent midpoint for the fine mesh (33 nodes). No node is
chosen from a residual or gap outcome. Retain both meshes via membership tags.
At each Delta find every baryon-coordinate root of each observable's central
contour and the signed bands

    prediction-observation = sign*(k*hypot(sigma_obs,sigma_theory)+b),
    sign={-1,+1}, k={1,2,3}.

Use the existing cubic abundance and bilinear positive theory-sigma
interpolants, b_He=2e-5, b_D=5e-8. On each baryon table interval form the
local polynomial after squaring the band equation, isolate its roots by
recursive derivative partitions and 80 bisections, and reject extraneous
squared roots with the original signed equation. Retain root/control counts.
All interval endpoints and central/tangent roots are checked. This is floating
point polynomial isolation, not a formally directed root certificate.

Return both separate marginal bands and their intersections as unions of
baryon intervals at every Delta, including empty/outside-qualified results.
Retain signed residuals and each uncertainty contribution at contour points.
No Gaussian joint chi-square, probability, confidence exclusion or claimed
degrees-of-freedom goodness-of-fit is produced. k=1,2,3 are descriptive band
labels only. Unknown systematics and unprovided He3 conversion remain visible.
The helium and deuterium products are both calibration data now, not holdouts.

The physical state map includes every central-contour root and every endpoint
of every joint-band interval on the fixed 33-node mesh, without selecting a
best row. Identical points are stored once with all roles. Other marginal
boundary roots remain in the complete table-space output. Matched Delta=0
values are returned at every mapped baryon coordinate. Global extrema of an
unsampled continuous feasible set are not claimed; coarse/fine profile-range
changes are descriptive, with no success gate or precision retuning.

In-domain table values outside [.020,.024]x[0,3] are retained but marked
outside the inherited local interpolation qualification. The old node,
withheld and synthetic tests are repeated unchanged; local target
cubic/quadratic tests keep the old allowances. There is no extrapolation.

## Exact state inversion and calibration controls

Use the s parameterization in equation (5) of the derivation with GL128
primary and GL64 comparison, 80 bisections in [0,1]. GL nodes/weights are
constructed with the standard Legendre recurrence/Newton roots; qualify
positive weights, symmetry and low polynomial moments. Synthetic s values
{1e-8,.01,.5,1}, including the pure-quartic Gamma endpoint, qualify forward
and inverse action. Independently integrate the energy-centered action with
composite Simpson1024 at those synthetic witnesses. No action trajectory is
generated. Exact R>1, positive excitation and pure-quartic existence checks
are domain statuses, not tolerances widened to admit a candidate.

Each finite supported point recomputes Omega_b, Omega_exc, e, I, R, Q, D,
cosmic omega, pressure, curvature, K0,J, and the unique matched S. Match S
with its actual soft nodes and exact finite-R hard endpoint by 80 bisections;
use zero as the safe lower bracket and the inherited harmonic-limit S as
initial upper trial, doubling until it contains the root. Check cubic residuals and
energy/vacuum reconstruction independently. Use positive moment expressions
for pressure/curvature, not subtracting large action-energy terms.

Inherited algebra/root tolerance is 2e-11 relative to positive quantities;
zero/contact identities use 2e-12 times max(1, contribution scales).
GL64/128 action, gap and moment comparisons and Simpson witnesses use 2e-8
relative. Polynomial root residuals use 2e-8 in observational-sigma units;
synthetic polynomial/simple and repeated roots use 2e-11 absolute x error.
Any failure is retained; no outcome-dependent tolerance or parameter change.

Delta=0 with positive E is explicitly the R=infinity singular comparison,
not a finite zero-action/zero-energy candidate. No NaN/Infinity is serialized:
use null plus exact limiting labels. R<=1 and nonpositive E are retained
unsupported states. Every point/reference/spectrum mapping is counted.

## Required linked outputs and limits

Return complete table contour/band geometry and exact five-to-18 reference
mapping, all finite/infinite/unsupported state labels, updated energy/action,
vacuum match and source hardening certificate S/R^2<1/sqrt(12), Q/E, proxy
Delta reconstruction, D/(Q A10keV_lower^2), inherited fixed-heating H envelope,
K0,J and cold-limit R^4/J descriptors. Preserve the soft64/128 contrasts and
coarse/fine contour profile ranges. The full pressure/energy and same-state
current are not replaced by an extra free abundance.

Use the old actual lower bound on A at 10 keV and recalculate every state's
finite-gap bound. It is not an abundance uncertainty or observational gate.
Retain the same tiny T0/eta-coordinate sensitivity and helium-denominator
metadata at all table-space points. `conserved_scalar_abundance_status` must
remain `NOT_YET_QUALIFIED`; the inverse is explicitly fixed-heating proxy-only.

This new inference amends the old conditional baryon allocation; later galaxy
use must carry its new cosmic state and full reaction. It cannot rescale old
velocity fields or silently select a fitted halo radius. Output is a complete
stdout JSON wrapper with canonical payload/freeze hashes, actual runtime/RSS,
all controls and failures. No files are written by the worker. No numerical
observational-success status is assigned.
