# V002: additive radial-interpolation repair

2026-09-28. Prospective numerical repair after the preserved V001 failure.
No source, potential field, photon impact, constitutive law, exterior model,
distance or acceptance threshold is changed. V001 source, freeze, complete
results and all five failed 1% projected-mass checks remain untouched and
are explicit inputs to this attempt. This is not new blind scientific evidence.

## Identified mechanism and sole method change

The independent decomposition at the failing 2.7-kpc face-on Newtonian
impact separates direct interpolation of the saved full potential from the
spherical-reference interpolation defect. For original HI1/H21 the direct
full-field-plus-exterior error is -0.220224%, while reference subtraction
adds +5.738511%, yielding +5.518287% total. All five source controls show the
same mechanism. The analytic monopole units/signs and exact decomposition
close; the effect is not a new mass normalization or an exterior-force error.

Upgrade only radial interpolation of `delta_phi` from linear to local cubic
Lagrange in `s=R^2`. Retain linear interpolation in `Z=|z|`, the clarified
residual-node extrapolation, all boundaries, source data and undefined origin.
For radial interval i use four consecutive nodes starting at
`j=min(max(i-1,0),node_count-4)`. This stencil is fixed throughout each split
ray segment. Evaluate Lagrange basis and derivatives in locally normalized
coordinates `t=(s-s_j)/(s_(j+3)-s_j)`; do not form large global powers.

Each neighboring interval still interpolates its shared radial node exactly,
so the representation is C0. Its radial derivative can jump when the stencil
changes. The value remains zero at R=L because its last node is zero; all
four values on Z=L are zero, so that entire face remains zero. No derivative
boundary condition or artificial smoothing is added. Polynomial dependence
on R^2 retains regular axial gradients. Reject any stencil requiring the
undefined corner (0,0), even if the original two-node cell would not require
it. All fixed physical rays stay well outside this patch.

## Exact ray integration and numerical controls

Within each segment write `delta_phi=P3(s)+Z*Q3(s)`. Its sky-X derivative has
degree at most five in affine ray parameter ell. The sky-Y derivative can
have degree six because it contains `y_d*Z*Q2(s)` and `Q3(s)`. Therefore
**four-point Gauss** is exact in real arithmetic for this representation;
use eight points as the independent rule. Keep all signed contributions and
the same 4096-epsilon cancellation-scaled comparisons as V001, now using
absolute Lagrange derivative/basis contributions from all eight corners.

For face-on rays the analytic cubic radial derivative remains piecewise
linear in z, so the independent full-ray trapezoidal integration still
applies. Retain opposite-impact parity, cross-axis zero, every 64/128
reference-potential node/effect check, and the original **1%** face-on
Newtonian projected-mass target. Numerical mesh/domain changes remain
descriptive-only. No accuracy limit is widened after seeing V001.

Before real-field postprocessing, qualify this implementation using a fixed
N12/L16-kpc synthetic mesh and radii 2.7 and 8.7 kpc, each face-on and at the
same 72-degree major/minor orientations:

- Reproduce all dimensionless monomials `(s/16^2)^p*(Z/16)^q` for
  `p=0,1,2,3` and `q=0,1`, together with their analytic s and Z derivatives.
  Tests evaluate both values/derivatives inside every radial interval.
- Compare four/eight-point ray integrals and direct eight-point evaluation
  of the known analytic monomial sky gradients. The latter does not use
  Lagrange derivatives. Use `4096*eps*max(1,sum cancellation scales)`.
- Verify exact nodal interpolation, continuity at every stencil switch
  using deterministic arbitrary nodal values, and both zero outer-face
  identities at `1024*eps` times absolute evaluation scales. Derivative
  comparisons use dimensionless derivatives (`16^2*d/ds`, `16*d/dZ`).
- Verify refusal of the original origin cell and the additional four-node
  origin-dependency case. No undefined source value is manufactured.

These synthetic polynomials test interpolation and integration only; they
are not new physical source fields, and their generic polynomial boundary
values need not obey the physical zero-residual faces.

## Exact reuse and custody

The original frozen helper module supplies the unchanged custody readers,
20-case census, ray crossings, crossed-node-only batched reference-potential
evaluation, unit factors, source factories and descriptive comparison code.
No helper globals or functions are monkey-patched. Expanded radial stencils
add only their explicitly planned positive-center dependencies, in the same
maximum batches of 512; no full quadrature mesh is built.

The spherical line integrals, decomposition and analytic monopole tests are
unchanged. Reuse their authenticated V001 values and passing checks rather
than running identical integrals again; label that reuse. Re-evaluate both
64/128 reference-node potentials because the expanded stencil may require
additional nodes. Recalculate every finite-box correction and projected-mass
test from the same saved fields. Preserve V001/V002 angle differences without
using them to select a source or a numerical tolerance.

The new freeze recursively retains V001's complete source manifest and
failure-result hash, plus this note and `saved_potential_lensing_v002.py`.
New freeze/result filenames contain V002; no V001 file is overwritten.
If synthetic qualification fails, save that failure and do not start the
real-field projections. Otherwise save all twenty cases and every numerical
failure before returning status.
There is no new PDE, optimizer, source fit or checkpoint scheme. Root reviews,
freezes and runs this small one-worker postprocessing attempt.
