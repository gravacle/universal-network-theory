# Independent saved-potential lensing preflight

Accepted for the specified conditional forward calculation. Read the complete
source, both protocols and analytical pathway; AST parsing passes. No import,
projection, quadrature or new force solve was performed for this preflight.

The frozen-input design keeps all twenty original/calibrated fields, five
impact radii and three projections per field (300 rays), with the exact
inherited physical source and law. Recursive file checks, canonical payload
seals, case identities and original numerical checks are consistent. The
new HALOGAS source contrasts are deliberately outside this census.

The inclined coordinate transformation, potential-gradient signs and physical
factor `2*A0/c^2` agree with the pathway. Splitting at every crossed radial
surface, height plane and midplane makes each bilinear `(R^2,|z|)` residual
sky-gradient component at most quadratic along a segment. Two-node Gauss
integration is therefore exact for that interpolant in real arithmetic;
four-node, reflected-ray and face-on trapezoidal checks are independent
implementation controls. Absolute corner-contribution scales explicitly
allow for cancellation in differences of potential values.

The planning pass supplies all nodes used by those ray and trapezoid checks.
Reference-potential dependencies are evaluated only at required positive
saved centers, in batches no larger than 512. Rays requiring the undefined
origin corner are refused. The outer residual is zero, giving a continuous
potential with the chosen spherical exterior, not an omitted potential jump.

The clarified protocol **extrapolates the residual itself** to zero height
and zero radius. That preserves interior saved-node values but is not the
old full-potential midplane readout. The implementation now matches this
explicit convention; the interpolation and grid/domain sensitivities remain
scientifically relevant even if quadrature errors are tiny.

The spherical angular integral retains the impact vector, not only its unit
direction. Newtonian `4GM/(c^2 b)` and deep `2*pi*sqrt(G M a0)/c^2` identities,
their interior/exterior pieces, order-64/128 comparisons and the angle-unit
conversion are consistent. Reporting interior monopole, residual correction
and exterior monopole separately keeps the adopted outer completion visible.

The 25 face-on Newtonian source-own projected-mass controls are particularly
useful: they test the combined saved field, interpolation and finite-box
completion against a different analytic observable. Their prospective 1%
criterion is explicitly new, not borrowed from the old radial-force
tolerance. A failure should remain a numerical/model-completion result, not
be repaired by changing this criterion after viewing output. All failed
numerical checks are retained across the whole input census.

The result will be physical bending for the adopted weak-field, stationary,
aligned-clock metric branch. It is not an observed reduced-lensing fit, a
native derivation of the metric interface, or cosmological/environmental
matching. Leading equality of metric potentials supplies the photon bridge;
a nonrelativistic force law alone would not supply it.

## Reviewed prefreeze identities

| File | SHA-256 |
|---|---|
| `saved_potential_lensing.py` | `db4c5082d2b45168cabac027250b54fc81b5d84960f4c8ef40951881aeccaf92` |
| `LENSING_NUMERICAL_CONTROLS.md` | `b37acf81a8780bb665cd6157a45361e3aa3a4eca3746a4348d57a2cc75f7441e` |
| `SAVED_POTENTIAL_LENSING_PROTOCOL.md` | `7ed5bb501f639f7e151c51646bd2241e19855abc1761292320dad92356d876b6` |
| `WEAK_FIELD_LENSING_PATHWAY.md` | `d79f9f32c39555d65085f9420536b6c912330559950897c4416a535dc4ffb06e` |

No source change requested and no frozen input edited.
