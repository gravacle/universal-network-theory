# Independent preflight: stretched axisymmetric disk solver

2026-09-28. Read the complete unrun `axisymmetric_disk.py`,
`test_stretched_disk.py` and `STRETCHED_DISK_PROTOCOL.md`, alongside the
accepted frozen uniform-grid law. No operator/solver benchmark executed by
this reviewer. This is a prospective source review, not a result review.

## Mathematical disposition

No field-equation, flux-sign or geometric-weight blocker was found.

1. Arithmetic edge midpoints and actual neighbouring centre separations
   are used consistently. At an internal face, the weight of the right
   cell value is `width_left/(width_left+width_right)`, exactly the linear
   interpolation fraction from its left centre. This is the implemented
   transverse-gradient interpolation, not an incorrect equal average.
2. Radial conductance is `R_face*vertical_width/radial_centre_separation`;
   vertical conductance is `annular_area/vertical_centre_separation`, with
   `annular_area=(R_high^2-R_low^2)/2`. Dirichlet boundary distances are
   actual half-cell widths. The axis is zero radial flux and the bottom
   has only the separately prescribed baryonic flux.
3. The internal conductances are shared by adjacent cells. Their frozen
   Picard operator is therefore symmetric positive definite, with the
   positive boundary terms fixing its constant mode. An undivided
   finite-volume system supports the existing Euclidean PCG scheme;
   no extra cell-volume weighting of that solver is required.
4. Both gradient components enter the same frozen scalar flux function.
   `np.gradient` is given the nonuniform centre coordinates. The secant
   normal derivative and interpolated transverse derivative are
   consistent on this smooth exponentially stretched mesh. Their
   observed convergence must still be tested; the source review does
   not assert an error order on arbitrary irregular meshes.
5. The logarithmic substitution `u=exp(t)` transforms the same potential
   integral exactly to `integral exp(t)*g(eta exp(-2t)) dt`. The 64/128
   comparison is a prospective quadrature check, not a change in law.
   Newtonian mode uses the analytical integral and coefficient one.
6. The lower-face annular flux, total finite-domain mass, disk-plane
   extrapolation using the actual first two vertical centres, and
   nonuniform radial derivative all have the intended signs/distances.
7. The thirteen-case plan matches the protocol: nine near-domain
   refinement cases, three larger-domain cases and one Newtonian case.
   Failed completed cases remain saved. Resume checks identity, payload,
   freeze, pass flags and successive near-domain refinement before
   accepting/skipping a completed case.

The Newtonian initial potential is the analytical continuum potential in
that comparison mode, not an exact solution of the finite-volume matrix.
Its solved discretization error therefore remains a meaningful check,
though not an independent test of the nonlinear iteration.

## Required prospective custody correction

The reviewed draft freezes `disk_solver.py` and its old
`DISK_SOLVER_FROZEN.json`, but importing the law also reads the actual
`../joint_parent_dynamics/SHAPE_REFERENCE_RESULTS.json` to select `r`.
The new runner does not yet validate that actual file against the old
freeze. Consequently a changed inherited shape file could change the law
without changing the currently compared stretched-source entries.

Before freezing/running, include that actual inherited shape result in the
new source map and/or verify every old disk-freeze entry against its actual
file. Using both gives an explicit current input hash and a checked
transitive link. This is a narrow unrun input-integrity correction, not a
changed physical law or tolerance. The parent was notified; acceptance for
execution is conditional on that correction being present.

## Scope

A pass would establish refining exact-boundary performance on this
stretched mesh and its larger radial/vertical extent. It would not prove
an arbitrary observed galaxy's remote-boundary approximation or eliminate
the later source-tail and domain-enlargement comparison. No new native
source, physical volume, or cosmological claim follows from this numerical
qualification alone.
