# Inert saved-potential lensing algorithm

2026-09-28. Prospective postprocessing only. No code has been run under this
protocol. It uses the existing K=0 stationary weak-field prediction derived
in `WEAK_FIELD_LENSING_PATHWAY.md`; it does not choose a new force law,
source, lensing mass component or distance fit.

## Fixed input and ray census

Retain all 16 completed original galaxy fields: all four HI/H2-tail choices
and each original mesh/domain/Newtonian-control combination. Also retain
all four completed `ML36_CAL_HI1_H21_V001` calibration fields. Authenticate
each result against its original freeze and canonical payload seal and
require its original checks to pass. Do not read a partial checkpoint when
a completed case exists. Freeze the exact 20-case file/hash census before
postprocessing; no selecting the best rotation residual.

For each case use physical impact radii

    b = 2.7, 8.7, 20.7, 35.7, 43.7 kpc.

These are the previously specified independent-oracle radii, reused without
looking at a lensing result. Evaluate a face-on ray at (X,Y)=(b,0), and the
adopted i=72-degree major- and minor-axis rays (b,0) and (0,b). Retain every
ray. Inclination is the existing source geometry, not adjusted to lensing.
No angular-diameter distance or background source redshift is invented:
the primary output is the two-component physical bending angle in radians,
with arcseconds only as a unit conversion.

## A continuous field representation and an explicit exterior

Let c be the saved centers and L the old box extent. Reconstruct the exact
old mesh from N,L and verify the saved centers. The corresponding boundary
monopole uses

    q = G_KPC_KMS2_MSUN*sum(component_masses_Msun)/A0_KMS2_KPC,
    phi_sph'(r) = inverse(q/r^2)       for the candidate,
                 q/r^2              for Newtonian controls.

The inverse is the unchanged frozen mechanical flux inverse. Its potential
has exactly the original reference at 1 kpc; additive constants never enter
the bending. Use the old spherical-potential routine, with its original
quadrature and an independent doubled-order comparison, not an arbitrary
new asymptotic force throughout the box.

Identify crossed interpolation cells first and evaluate the spherical
reference only at the distinct nodes needed by these fixed rays. Process
one case at a time, in batches of at most 512 reference radii; do not allocate
an N-by-N-by-quadrature array or recompute a full field. Batching changes no
formula or ray census and keeps this a small saved-data calculation.

At the stored center nodes write

    delta_phi(R,z)=phi_saved(R,z)-phi_sph(sqrt(R^2+z^2)).

Add z=0 residual values by first-two-height linear extrapolation of
delta_phi. This uses the same stencil as the old midplane readout but is
not identical to extrapolating the full phi and then subtracting the exact
spherical reference: the reference has its own height curvature. This is
the declared residual-field interpolation, not a claim to reproduce the
previous midplane derivative exactly. Add R=0 residual values by extrapolation
linear in R^2 from the first two radial centers, which preserves regular axial behavior.
At either old outer face R=L or z=L set delta_phi=0, as prescribed by the
old boundary potential. Interpolate delta_phi bilinearly in `(s=R^2,Z=|z|)`
between those nodes, and set it to zero outside the old cylindrical box.

The full reconstruction is `phi_sph(r)+delta_phi`. It agrees with every
saved interior potential value and is continuous at the exterior faces;
there is no potential jump whose distributional derivative has been
silently omitted. Its gradients are a declared postprocessing interpolant,
not a newly solved field. Grid/domain comparisons must be retained.

The monopole reference is singular at the origin, so do not invent a value
for delta_phi at the node (0,0) or regularize it. Exclude the innermost
interpolation cell from this projection; all specified rays have
`r>=b>=2.7 kpc`, well outside it. Verify this before evaluation and refuse
a ray that would touch a cell needing that undefined corner. No central
source is changed by this restriction.

## Exact finite-box ray integration of that interpolant

Use the ray coordinates in the pathway note. Inside one interpolation cell

    delta_phi(s,Z)=a+b_s*s+c_Z*Z+d*s*Z,
    partial_X delta_phi=2X*(b_s+d*Z),
    partial_Y delta_phi=2*y_d*cos(i)*(b_s+d*Z)
                        -sign(z_d)*sin(i)*(c_Z+d*s).

Along a ray, y_d and signed z_d are affine in ell, s is quadratic, and the
sign of z_d is fixed within a split segment. Each displayed sky-gradient
component is therefore a polynomial of degree at most two in ell.

Split at all crossed R-node surfaces, z-node planes of either sign, the
midplane, and the entry/exit faces. Radial crossings solve
`y_d=+/-sqrt(R_node^2-X^2)` when the square root exists; z crossings solve
`z_d=+/-z_node`. Handle the face-on limits directly, not by dividing by
sin(i)=0. Sort and deduplicate crossings before integration.

A two-node Gauss rule is then exact in real arithmetic on each segment.
Cross-check with four nodes, retaining differences; there is no adaptive
ray search. Face-on correction can also be integrated independently by
the trapezoidal rule in z at all nodes because its radial derivative is
piecewise linear there. Use even/odd reflections and regular axis limits.

Multiply the correction integral by `2*A0_KMS2_KPC/c_kms^2`, using
`c_kms=299792.458`. This conversion follows the original potential units;
no new acceleration or length normalization is supplied.

## Keep the exterior contribution visible

Integrate the whole spherical reference separately, and add only the
finite-box delta_phi correction. With `b=sqrt(X^2+Y^2)` and
`ell=b*tan(theta)`, the monopole gradient integral has a finite angular
domain. Its vector is parallel to (X,Y). For the candidate its scalar
integrand is `inverse(q*cos(theta)^2/b^2)/cos(theta)`, whose endpoint limit
is `sqrt(q)/b`. Subtract that analytic endpoint before fixed 64/128-node
quadratures and add its exact constant integral. Newtonian reference
bending is exactly `4*G*M/(c^2*b)`.
Explicitly, the full candidate monopole vector is
`2*A0_KMS2_KPC/c_kms^2 * (X,Y) * integral_(-pi/2)^(pi/2) integrand dtheta`.
This vector prefactor, rather than a unit vector alone, retains the impact
length and the physical units.

Use the same theta representation at the box entry/exit to label the part
of the monopole integral exterior to the original field domain. Report
separately: interior spherical term, interpolated correction, exterior
monopole term, and their vector total. The resulting completion reproduces
the inherited isolated spherical exterior; it does not certify environmental
or cosmological matching. Formal integration to infinity is a completion
diagnostic whose physical limits are discussed in the pathway note.

## Controls and interpretation

- Exact spherical Newtonian and deep-logarithmic fields must reproduce
  `4GM/(c^2*b)` and `2*pi*sqrt(G*M*a0)/c^2` respectively, including the
  finite entry/exit decomposition. No new field solve is needed for these
  analytic integration identities.
- Verify ray reflection/parity, vanishing cross-axis deflection on the
  chosen principal axes, independent face-on integration, and quadrature
  agreement. Preserve signed components, including any unexpected sign.
- For Newtonian face-on controls, compare the total prediction to
  `4G*M_disk(<b)/(c^2*b)` from the unchanged source profiles. This is a
  separate projected-mass identity, not the rotation-force oracle. Record
  discrepancies; do not silently transfer a radial-force tolerance into
  a lensing qualification.
- Carry all existing N256/N512 and L255/L1023 candidate differences, all
  four source alternatives, and the fixed stellar-calibration change.
  Mesh/interpolation/boundary sensitivity is numerical/model evidence,
  not a lensing-data uncertainty or a likelihood.

This protocol defines a small forward prediction, not an empirical pass
criterion. Any implementation should freeze its code and exact input list
before evaluation, keep new outputs separate, and retain all failures.
There is no new propagation, fitting, source retuning, population reset or
need for a long-job checkpoint. The root owns the eventual execution.
