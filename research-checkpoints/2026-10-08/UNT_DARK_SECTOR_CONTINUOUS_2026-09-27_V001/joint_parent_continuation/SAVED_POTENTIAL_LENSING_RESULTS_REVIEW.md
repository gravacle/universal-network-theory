# Independent V001 lensing review: numerical qualification failed

The full 20-case/300-ray census and all 7,645 checks were preserved. Exactly
five checks fail: the five Newtonian face-on controls at impact 2.7 kpc
overpredict their exact projected-mass angles by 5.0020–5.5183%, against the
unchanged 1% target. Every other projected-mass point is within 0.8836%.
This is a reconstruction failure, not an observational lensing result or
a failure of the physical response law.

## Independent audit

All 77 frozen members and the result's canonical seal match. The twenty
case identities, 300 distinct ray identities, 25 source-own projected-mass
controls and all gate/pass associations were checked. The audit independently
recomputes component/unit closure, raw two/four-node and reflection errors,
64/128 spherical differences, analytic monopole expressions, source enclosed
masses and mesh/domain differences from the saved values. No ray propagator,
new physical quadrature or force solver was run. Reproducible arithmetic and
diagnosis are in `saved_lensing_audit.py` and
`SAVED_POTENTIAL_LENSING_REVIEW_DATA.json`.

Reported numerical checks other than the five projected-mass failures pass.
This confirms accurate integration of the **declared interpolant**, not that
its gradient is accurate enough. The maximum candidate mesh difference is
11.6943%, at face-on b=2.7 kpc; maximum domain difference is 0.152221%, at
face-on b=43.7 kpc. The failed reconstruction's raw candidate angles span
0.11061–0.37142 arcsec and its Newtonian angles 0.02644–0.13951 arcsec.
Matched fine-field candidate/Newtonian magnitude ratios span 2.1687–12.4348.
These ranges are retained diagnostics, **not qualified physical predictions**.

## Exact saved-node diagnosis

For a face-on ray, let I_h denote the old radial-slope/interpolated-height
projection operator, with the same extrapolated and outer boundary nodes.
Linearity gives

    alpha_V001 = I_h(phi_saved)
                   + [alpha_spherical_inside - I_h(phi_spherical)]
                   + alpha_spherical_outside.

Newtonian reference potentials are available in exact closed form,
`q*(1-1/sqrt(R^2+z^2))`. Applying only the existing saved-node stencil to
these known values isolates the reference-interpolation error. This is
algebraic diagnosis of saved data, not a new field solution.

At b=2.7 kpc in the original HI1/H21 source:

- The direct full-saved-potential interpolation plus the unchanged exterior
  is only **−0.220224%** from the exact projected-mass angle.
- The mismatch between the exact interior monopole and its low-order
  interpolated slope adds **+5.738511%** of that target angle.
- Their sum is the observed **+5.518287%** V001 error; the decomposition
  closes at approximately 1e−20 rad.

The same radial cell, 2.6879872115–2.7281467592 kpc, is used in all five
controls. Across them, the full-field interpolation contribution is
−0.2202 to −0.2220%, while the reference-slope defect contributes
+5.2240 to +5.7385%. At 8.7 kpc the corresponding reference defect is
+1.0881 to +1.1751%, partly canceled by a −0.2910 to −0.2989% full-field
interpolation contribution. This explains the radius and mass dependence.

The underlying numerical issue is cancellation amplification: the inner
full angle is a small remainder of a large monopole term and a negative
disk correction. A modest low-order slope error in the subtracted monopole
becomes a much larger relative error in that remainder. Newtonian reference
order-64/128 effects are exactly zero; analytic normalization/exterior
identities pass. The failure is therefore not evidence for a sign, unit,
extra-mass, or outer-boundary normalization error.

## Constructive next numerical step

A separately identified higher-order radial reconstruction of the same
residual field is justified by this diagnosis. Local four-node interpolation
in R², linear interpolation in |z|, and four-node ray quadrature with an
eight-node cross-check can remove the leading slope error while preserving
the same potentials, sources, law, rays and exterior. Its own controls must
be run before claiming success. A face-on projected-flux reconstruction is
another independent diagnostic, not permission to substitute its target
value for the full inclined calculation.

Keep V001 and its five failures unchanged. Do not relax the 1% criterion,
retune physical parameters, drop the inner radius or report repaired values
as though they came from this attempt. Numerical repair is distinct from
the adopted metric/clock/exterior assumptions, which remain in either case.

Result SHA-256:
`6b22078428d45cc233b21e205bf969565695f6f765c7afbcf6a4dec29fc2fa94`.
Freeze SHA-256:
`208a3a0f72c9e389fe2af32b7e6313fa4bee34e065f80f6fd11dccb2e7f26feb`.
No frozen source, tolerance or evidence was edited.
