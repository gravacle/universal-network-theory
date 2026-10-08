# Disk response diagnostic — fixed fields, no new fit

This is a prospective **postprocessing recipe** for the four already specified
NGC 3198 source models. It neither changes their law/source parameters nor solves
another field equation. Its interpretation is descriptive, not a new independent
prediction. The observed curve and the reported tendency toward overprediction
have already been seen. Freeze this note and `disk_response_diagnostic.py` before
running it; wait for all 16 galaxy cases, retaining every model and all 43 radii.

## 1. Reconstruct the actual sheet field

All lower-case accelerations below are in the existing physical `a0` units and
are components of **grad Phi**: a positive radial component corresponds to an
inward gravitational acceleration. At each stored comparison radius define

```
x = nonlinear radial field,       n = Newtonian radial field,
b = 2 pi G Sigma_total(R) / a0,    f(s) = s mu(s).
```

Use the same density model and the same **N512, L255** domain for `x` and `n`.
Both fields include their previously specified monopole outer-boundary
approximation; the nonlinear and Newtonian boundary potentials are their
respective law-consistent ones, not numerically identical potentials.

Reflection symmetry and the actual surface-density jump imply the one-sided
vertical field `z >= 0` is the unique solution

```
mu(sqrt(x^2+z^2)) z = b.                         (1)
```

The derivative of the left side with respect to `z`, for `s>0`, is
`mu(s) x^2/s^2 + f'(s) z^2/s^2 > 0`. Its range extends from zero to infinity.
This uses the qualified positive monotone flux, not an assumption that the
radial algebraic approximation solves a disk. The zero-density case has `z=0`.
For this fixed bounded mechanical law, its positive contact term gives
`mu(s) >= 1-[1+(s/r)^2]^-2`. Consequently
`z_hi=2(b+abs(x)+r)` is a safe bisection bracket: `z_hi>=2r,2b` and the left
side is at least `24 z_hi/25`. Use 70 iterations, without fitted tolerances.

Define the signed radial **flux difference**

```
S_R = mu(s) x - n,             S_z = mu(s) z - b = 0.       (2)
```

In the exact common-source continuum equations,
`div[mu(|grad Phi|) grad Phi - grad Phi_N]=0`. Thus (2) measures its radial
solenoidal component at the sheet. The saved numerical trace makes it an
*estimate*: it includes differentiation/interpolation error and the differing
finite-domain boundary approximations. It is not itself a measurement of the
curl, a new force, or a uniquely isolated intrinsic disk correction. Imposing
(1) tests algebraic reconstruction; it does **not** independently certify the
solver's vertical boundary implementation.

## 2. Exact decomposition into four diagnostics

Write `inv=f^-1`, with `inv(0)=0`, and use the existing mass including the chosen
tails. Define

```
N = hypot(n,b)
v = (n/N) inv(N)                   [v=0 when N=0]
a = sign(n) inv(abs(n))
d = sign(n) sqrt(abs(n))
k = sqrt(G M_total/a0) / R.
```

`v` is the radial part of a **full-vector algebraic shortcut**; `a` is the
radial-only shortcut. Neither is a disk solution in general: replacing the
Newtonian field by a pointwise nonlinear multiple usually loses integrability.
`d` is the ideal deep-law radial shortcut. `k` is the ideal deep spherical
total-mass reference, not a claim that a finite-radius disk is already outside
all its mass. Negative `n` is retained in `v,a,d`; never take its unsigned force
as an inward prediction.

The exact accounting identity is

```
x - k = (x-v) + (v-a) + (a-d) + (d-k).                      (3)
```

The ordered terms mean:

1. Remaining nonlocal/solenoidal-plus-boundary numerical field correction.
2. Vertical-field projection in the algebraic diagnostic.
3. Existing constitutive-law shape relative to its ideal deep asymptote.
4. Newtonian disk/source geometry relative to the total-mass monopole reference.

This is a deliberately defined decomposition, not a unique causal partition.
For a given `S_R`, equation (1) also implies the exact local consistency identity
`x = (n+S_R)/hypot(n+S_R,b) * inv(hypot(n+S_R,b))` (zero-vector convention as
above). It checks the bookkeeping without an additional field solve.

The already derived exact Kuzmin disk is a useful analytical reference: with
`s0=sqrt(R^2+a^2)`, its Newtonian components are proportional to `(R,a)/s0^3`,
and its true nonlinear field is `inv(GM/(a0 s0^2)) (R,a)/s0`. Thus `S_R=0`
and `x=v` exactly, while `v-a` and `d-k` generally remain nonzero. A vanishing
solenoidal term therefore does **not** mean that disk geometry is irrelevant.

Multiply (3) by `R a0` to obtain **signed velocity-squared** contributions in
`(km/s)^2`. Add the reference residual `R a0 k - v_observed^2` to get the actual
`v_predicted^2 - v_observed^2` exactly. Contributions can cancel; percentages
of a nearly zero residual would be misleading and are not reported. Real
diagnostic velocities are reported only when their signed squared value is
nonnegative. These are not likelihoods or error-weighted parameter estimates.

The ideal flat reference is conditional on the infinite continuum static law.
A physical thermal, quantum, pinning, or finite-gap floor can end its low-field
window. None of those unmeasured ingredients is introduced or tuned here.

## 3. Numerical custody and scope

Authenticate the galaxy source freeze, each of the 16 case payloads, identities,
and all original case checks before postprocessing. Use all four models and all
43 existing radii. Also retain the signed force shifts `N512/L255-N256/L255` and
`N320/L1023-N256/L255` already available; these are resolution/domain diagnostics,
not rigorous error bars. Do not mix a remote-domain nonlinear field with the
L255 Newtonian field when forming (2) or (3).

For every row report the nearest source knot, nearest hard truncation edge (if
any), and local radial center spacing. Flag a radius within twice that spacing
of a hard edge; retain it, do not silently exclude it. A nonzero hard-cutoff
surface density has a logarithmically singular ideal midplane radial field at
the exact edge. Reconstruction there is not a physical finite-thickness model.

Only numerical identities are acceptance tests: sheet-jump reconstruction,
flux inversion, and both versions of (3), each within `1e-11 * max(1, scale)`;
source mass closure within `1e-13` relative. Preserve signed values and report
any failed identity. The inherited `R>=0,2,8 kpc` summaries are unweighted means
and maximum absolute terms, including all selected rows. There is no sign,
observational-success, or small-solenoidal-correction acceptance threshold.

This can answer whether the *existing* outer excess is dominated by the curve's
interpolation, projection/nonlocal disk effects, or a finite-radius departure
from the total-mass flat reference. It cannot by itself establish an acceptable
galaxy fit, an independent native UNT constitutive derivation, or lensing.
